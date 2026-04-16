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
