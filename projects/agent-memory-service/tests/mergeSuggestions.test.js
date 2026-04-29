import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdir, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { randomUUID } from 'node:crypto';

function tmpDir() {
  return join('/tmp', `ms_merge_sug_${randomUUID()}`);
}

describe('mergeSuggestions()', () => {
  it('returns empty when no memories', async () => {
    const dir = tmpDir();
    await mkdir(dir, { recursive: true });
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();
    const result = await svc.mergeSuggestions();
    assert.deepEqual(result, []);
    await rm(dir, { recursive: true, force: true });
  });

  it('detects duplicate-like memories by content similarity', async () => {
    const dir = tmpDir();
    await mkdir(dir, { recursive: true });
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();
    await svc.add({ content: 'The quick brown fox jumps over the lazy dog', tags: ['animal'], entities: ['fox'] });
    await svc.add({ content: 'The quick brown fox jumped over the lazy dogs', tags: ['mammal'], entities: ['fox'] });
    const result = await svc.mergeSuggestions();
    assert.equal(result.length, 1);
    assert.equal(result[0].reasons[0].startsWith('content:'), true);
    assert.ok(result[0].score > 0);
    await rm(dir, { recursive: true, force: true });
  });

  it('considers shared entities in scoring', async () => {
    const dir = tmpDir();
    await mkdir(dir, { recursive: true });
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();
    await svc.add({ content: 'Project Alpha uses React', entities: ['react', 'alpha'] });
    await svc.add({ content: 'Different text entirely about Vue framework', entities: ['react', 'vue'] });
    const result = await svc.mergeSuggestions({ minScore: 0.05 });
    assert.equal(result.length, 1);
    assert.ok(result[0].reasons.some(r => r.startsWith('entities:')));
    await rm(dir, { recursive: true, force: true });
  });

  it('considers shared tags in scoring', async () => {
    const dir = tmpDir();
    await mkdir(dir, { recursive: true });
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();
    await svc.add({ content: 'Completely different content A', tags: ['tech', 'ai'] });
    await svc.add({ content: 'Totally unrelated text about weather B', tags: ['tech', 'weather'] });
    const result = await svc.mergeSuggestions({ minScore: 0.05 });
    assert.equal(result.length, 1);
    assert.ok(result[0].reasons.some(r => r.startsWith('tags:')));
    await rm(dir, { recursive: true, force: true });
  });

  it('respects minScore filter', async () => {
    const dir = tmpDir();
    await mkdir(dir, { recursive: true });
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();
    await svc.add({ content: 'Memory about cats', tags: ['pet'] });
    await svc.add({ content: 'Memory about dogs', tags: ['pet'] });
    const result = await svc.mergeSuggestions({ minScore: 0.5 });
    assert.equal(result.length, 0);
    await rm(dir, { recursive: true, force: true });
  });

  it('respects limit option', async () => {
    const dir = tmpDir();
    await mkdir(dir, { recursive: true });
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();
    for (let i = 0; i < 5; i++) {
      await svc.add({ content: `The quick brown fox jumps variant ${i}`, tags: ['animal'], entities: ['fox'] });
    }
    const result = await svc.mergeSuggestions({ minScore: 0.1, limit: 3 });
    assert.ok(result.length <= 3);
    await rm(dir, { recursive: true, force: true });
  });

  it('respects layer filter', async () => {
    const dir = tmpDir();
    await mkdir(dir, { recursive: true });
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();
    await svc.add({ content: 'The quick brown fox jumps over the lazy dog', layer: 'L1', tags: ['a'] });
    await svc.add({ content: 'The quick brown fox jumped over the lazy dogs', layer: 'L2', tags: ['a'] });
    const result = await svc.mergeSuggestions({ layer: 'L1' });
    assert.equal(result.length, 0);
    await rm(dir, { recursive: true, force: true });
  });

  it('suggests keep-longer when first is longer', async () => {
    const dir = tmpDir();
    await mkdir(dir, { recursive: true });
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();
    await svc.add({ content: 'A very long detailed description about the project architecture and design', entities: ['proj'] });
    await svc.add({ content: 'Short note', entities: ['proj'] });
    const result = await svc.mergeSuggestions({ minScore: 0.05 });
    assert.equal(result.length, 1);
    assert.equal(result[0].suggestedStrategy.content, 'keep-longer');
    assert.equal(result[0].suggestedStrategy.tags, 'union');
    await rm(dir, { recursive: true, force: true });
  });

  it('returns results sorted by score descending', async () => {
    const dir = tmpDir();
    await mkdir(dir, { recursive: true });
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();
    await svc.add({ content: 'alpha beta gamma delta epsilon', tags: ['a'], entities: ['x'] });
    await svc.add({ content: 'alpha beta gamma delta epsilon zeta', tags: ['a'], entities: ['x'] });
    await svc.add({ content: 'alpha beta completely different text here', tags: ['a'] });
    const result = await svc.mergeSuggestions({ minScore: 0.05 });
    if (result.length >= 2) {
      assert.ok(result[0].score >= result[1].score);
    }
    await rm(dir, { recursive: true, force: true });
  });
});
