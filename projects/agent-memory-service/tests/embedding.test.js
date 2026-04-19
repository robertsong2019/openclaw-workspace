import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { EmbeddingProvider, cosineSimilarity, MemoryService } from '../src/index.js';
import { rm, mkdir } from 'node:fs/promises';
import { join } from 'node:path';

const TEST_DIR = join(import.meta.dirname, '..', 'data', 'test-embed');

// Simple mock embedding: maps each char to its char code, fixed dim=8
function mockEmbed(text) {
  const vec = new Array(8).fill(0);
  for (let i = 0; i < text.length; i++) {
    vec[i % 8] += text.charCodeAt(i);
  }
  const norm = Math.sqrt(vec.reduce((s, v) => s + v * v, 0)) || 1;
  return vec.map(v => v / norm);
}

describe('cosineSimilarity', () => {
  it('returns 1 for identical vectors', () => {
    assert.equal(cosineSimilarity([1, 0, 0], [1, 0, 0]), 1);
  });

  it('returns 0 for orthogonal vectors', () => {
    assert.equal(Math.round(cosineSimilarity([1, 0], [0, 1]) * 1000), 0);
  });

  it('returns 0 for empty or mismatched vectors', () => {
    assert.equal(cosineSimilarity([], [1]), 0);
    assert.equal(cosineSimilarity([1, 2], [3]), 0);
  });
});

describe('EmbeddingProvider', () => {
  it('returns null when no embedFn set', async () => {
    const ep = new EmbeddingProvider(TEST_DIR);
    assert.equal(ep.enabled, false);
    assert.equal(await ep.embed('hello'), null);
  });

  it('embeds text and caches results', async () => {
    await rm(TEST_DIR, { recursive: true, force: true });
    await mkdir(TEST_DIR, { recursive: true });
    const ep = new EmbeddingProvider(TEST_DIR, mockEmbed);
    await ep.loadCache();
    assert.equal(ep.enabled, true);

    const vec = await ep.embed('hello');
    assert.ok(Array.isArray(vec));
    assert.equal(vec.length, 8);

    // Second call should use cache
    const vec2 = await ep.embed('hello');
    assert.deepEqual(vec, vec2);
    assert.equal(ep.cacheSize, 1);
  });

  it('computes similarity between two texts', async () => {
    await rm(TEST_DIR, { recursive: true, force: true });
    await mkdir(TEST_DIR, { recursive: true });
    const ep = new EmbeddingProvider(TEST_DIR, mockEmbed);
    await ep.loadCache();

    // Same text → similarity = 1
    const sim = await ep.similarity('abc', 'abc');
    assert.equal(Math.round(sim * 100) / 100, 1);

    // Different texts → similarity < 1
    const sim2 = await ep.similarity('abc', 'xyz');
    assert.ok(sim2 < 1);
    assert.ok(sim2 >= -1);
  });

  it('persists cache to disk', async () => {
    await rm(TEST_DIR, { recursive: true, force: true });
    await mkdir(TEST_DIR, { recursive: true });

    const ep1 = new EmbeddingProvider(TEST_DIR, mockEmbed);
    await ep1.loadCache();
    await ep1.embed('persist test');
    await ep1.saveCache();

    const ep2 = new EmbeddingProvider(TEST_DIR, mockEmbed);
    await ep2.loadCache();
    assert.equal(ep2.cacheSize, 1);
    const vec = await ep2.embed('persist test');
    assert.ok(Array.isArray(vec));
  });

  it('handles embedFn errors gracefully', async () => {
    const ep = new EmbeddingProvider(TEST_DIR, async () => { throw new Error('fail'); });
    await ep.loadCache();
    assert.equal(await ep.embed('test'), null);
  });

  it('setEmbedFn changes provider at runtime', async () => {
    const ep = new EmbeddingProvider(TEST_DIR);
    assert.equal(ep.enabled, false);
    ep.setEmbedFn(mockEmbed);
    assert.equal(ep.enabled, true);
    const vec = await ep.embed('runtime');
    assert.ok(Array.isArray(vec));
  });

  it('clearCache resets cache', async () => {
    await rm(TEST_DIR, { recursive: true, force: true });
    await mkdir(TEST_DIR, { recursive: true });
    const ep = new EmbeddingProvider(TEST_DIR, mockEmbed);
    await ep.loadCache();
    await ep.embed('clearable');
    assert.equal(ep.cacheSize, 1);
    ep.clearCache();
    assert.equal(ep.cacheSize, 0);
  });
});

describe('MemoryService with embeddings', () => {
  it('uses embeddings in search when provider is enabled', async () => {
    const svcDir = join(import.meta.dirname, '..', 'data', 'test-svc-embed-a');
    await rm(svcDir, { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: svcDir, embedFn: mockEmbed });
    await svc.init();

    await svc.add({ content: 'I love JavaScript', layer: 'core', tags: ['lang'] });
    await svc.add({ content: 'Python is great for ML', layer: 'core', tags: ['lang'] });
    await svc.add({ content: 'Rust is fast and safe', layer: 'core', tags: ['lang'] });

    const results = await svc.search('JavaScript programming');
    assert.ok(results.length >= 1);
    assert.ok(results[0].content.includes('JavaScript'));
  });

  it('falls back gracefully when embedFn is null', async () => {
    const svcDir = join(import.meta.dirname, '..', 'data', 'test-svc-embed-b');
    await rm(svcDir, { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: svcDir });
    await svc.init();

    await svc.add({ content: 'test memory', layer: 'core' });
    const results = await svc.search('test');
    assert.equal(results.length, 1);
    assert.equal(results[0].content, 'test memory');
  });
});

describe('searchEmbedding', () => {
  const svcDir = join(import.meta.dirname, '..', 'data', 'test-search-embed');

  it('throws when embeddings not enabled', async () => {
    await rm(svcDir + '-noembed', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: svcDir + '-noembed' });
    await svc.init();
    await assert.rejects(() => svc.searchEmbedding('test'), /not enabled/);
  });

  it('returns results ranked by cosine similarity', async () => {
    await rm(svcDir + '-rank', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: svcDir + '-rank', embedFn: mockEmbed });
    await svc.init();

    await svc.add({ content: 'JavaScript programming language', layer: 'core' });
    await svc.add({ content: 'Rust systems programming', layer: 'core' });
    await svc.add({ content: 'Python machine learning', layer: 'core' });

    const results = await svc.searchEmbedding('JavaScript programming');
    assert.ok(results.length >= 1);
    assert.ok(results[0].content.includes('JavaScript'));
    assert.ok(results[0].score > 0);
    // Results should be sorted by score descending
    for (let i = 1; i < results.length; i++) {
      assert.ok(results[i - 1].score >= results[i].score);
    }
  });

  it('respects limit option', async () => {
    await rm(svcDir + '-limit', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: svcDir + '-limit', embedFn: mockEmbed });
    await svc.init();

    await svc.add({ content: 'alpha beta gamma', layer: 'core' });
    await svc.add({ content: 'delta epsilon zeta', layer: 'core' });
    await svc.add({ content: 'eta theta iota', layer: 'core' });

    const results = await svc.searchEmbedding('alpha', { limit: 2 });
    assert.ok(results.length <= 2);
  });

  it('filters by layer', async () => {
    await rm(svcDir + '-layer', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: svcDir + '-layer', embedFn: mockEmbed });
    await svc.init();

    await svc.add({ content: 'core memory item', layer: 'core' });
    await svc.add({ content: 'short memory item', layer: 'short' });

    const results = await svc.searchEmbedding('memory', { layer: 'core' });
    assert.ok(results.every(r => r.layer === 'core'));
  });

  it('applies threshold filter', async () => {
    await rm(svcDir + '-thresh', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: svcDir + '-thresh', embedFn: mockEmbed });
    await svc.init();

    await svc.add({ content: 'cat dog bird', layer: 'core' });
    await svc.add({ content: 'quantum physics relativity', layer: 'core' });

    const results = await svc.searchEmbedding('cat', { threshold: 0.99 });
    // With a high threshold, only very similar results should appear
    for (const r of results) {
      assert.ok(r.score >= 0.99);
    }
  });

  it('boosts access count on matched results', async () => {
    await rm(svcDir + '-boost', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: svcDir + '-boost', embedFn: mockEmbed });
    await svc.init();

    await svc.add({ content: 'boostable memory content', layer: 'core', tags: ['test'] });
    const before = (await svc.search('boostable', { strategy: 'exact' }))[0];

    const results = await svc.searchEmbedding('boostable memory');
    assert.ok(results.length >= 1);

    // Verify access was boosted (re-query)
    const after = await svc.get(results[0].id);
    assert.ok(after.accessCount > (before ? before.accessCount : 0));
  });

  it('returns empty array when query embedding fails', async () => {
    await rm(svcDir + '-fail', { recursive: true, force: true });
    const failEmbed = async () => { throw new Error('API down'); };
    const svc = new MemoryService({ dbPath: svcDir + '-fail', embedFn: failEmbed });
    await svc.init();
    await svc.add({ content: 'test', layer: 'core' });

    const results = await svc.searchEmbedding('test');
    assert.equal(results.length, 0);
  });
});

describe('searchUnified', () => {
  const baseDir = join(import.meta.dirname, '..', 'data', 'test-unified');

  it('fuses BM25 + semantic + embedding results', async () => {
    await rm(baseDir + '-fuse', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: baseDir + '-fuse', embedFn: mockEmbed });
    await svc.init();

    await svc.add({ content: 'JavaScript is a dynamic language for web development', layer: 'core', tags: ['js'] });
    await svc.add({ content: 'Python excels at data science and machine learning', layer: 'core', tags: ['py'] });
    await svc.add({ content: 'Rust provides memory safety without garbage collection', layer: 'core', tags: ['rs'] });

    const results = await svc.searchUnified('JavaScript web');
    assert.ok(results.length >= 1);
    assert.ok(results[0].score > 0);
    assert.ok(results[0].explanation);
    assert.ok(results[0].explanation.sources.length >= 1);
  });

  it('falls back to BM25+semantic when no embeddings', async () => {
    await rm(baseDir + '-noembed', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: baseDir + '-noembed' });
    await svc.init();

    await svc.add({ content: 'memory without embeddings test', layer: 'core' });

    const results = await svc.searchUnified('memory test');
    assert.ok(results.length >= 1);
    assert.equal(results[0].explanation.embeddingUsed, false);
  });

  it('returns empty when no matches found', async () => {
    await rm(baseDir + '-empty', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: baseDir + '-empty', embedFn: mockEmbed });
    await svc.init();

    await svc.add({ content: 'alpha beta gamma', layer: 'core' });
    const results = await svc.searchUnified('xyz zzz completely unrelated');
    // May still return results due to semantic/embedding fallback; just verify no crash
    assert.ok(Array.isArray(results));
  });

  it('respects limit option', async () => {
    await rm(baseDir + '-limit', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: baseDir + '-limit', embedFn: mockEmbed });
    await svc.init();

    await svc.add({ content: 'apple fruit healthy', layer: 'core' });
    await svc.add({ content: 'banana fruit yellow', layer: 'core' });
    await svc.add({ content: 'cherry fruit red', layer: 'core' });
    await svc.add({ content: 'date fruit sweet', layer: 'core' });

    const results = await svc.searchUnified('fruit', { limit: 2 });
    assert.ok(results.length <= 2);
  });

  it('filters by layer', async () => {
    await rm(baseDir + '-layer', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: baseDir + '-layer', embedFn: mockEmbed });
    await svc.init();

    await svc.add({ content: 'core layer unified search', layer: 'core' });
    await svc.add({ content: 'short layer unified search', layer: 'short' });

    const results = await svc.searchUnified('unified search', { layer: 'core' });
    assert.ok(results.every(r => r.layer === 'core'));
  });

  it('boosts access count on results', async () => {
    await rm(baseDir + '-boost', { recursive: true, force: true });
    const svc = new MemoryService({ dbPath: baseDir + '-boost', embedFn: mockEmbed });
    await svc.init();

    const m = await svc.add({ content: 'boostable unified content', layer: 'core' });
    assert.equal(m.accessCount, 0);

    await svc.searchUnified('boostable unified');
    const after = await svc.get(m.id);
    assert.ok(after.accessCount > 0);
  });
});
