import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { EmbeddingProvider } from '../src/index.js';

describe('Embedding Cache Eviction', () => {
  let dir;

  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), 'evict-'));
  });

  it('evicts oldest entries when cache exceeds maxCacheSize', async () => {
    const embedFn = async (text) => [text.length, 0];
    const ep = new EmbeddingProvider(dir, embedFn, { maxCacheSize: 3 });

    await ep.embed('alpha one');
    await ep.embed('beta two');
    await ep.embed('gamma three');
    assert.equal(ep.cacheSize, 3);

    await ep.embed('delta four');
    assert.equal(ep.cacheSize, 3);
    // 'alpha one' evicted; only 3 remain
    const keys = ep.cacheKeys();
    assert.equal(keys.length, 3);
    assert.ok(!keys.some(k => k.includes('alpha')), 'oldest should be evicted');
  });

  it('maxCacheSize=0 means unlimited (no eviction)', async () => {
    const embedFn = async (text) => [text.length, 0];
    const ep = new EmbeddingProvider(dir, embedFn); // default maxCacheSize=0

    for (let i = 0; i < 10; i++) {
      await ep.embed(`item ${i}`);
    }
    assert.equal(ep.cacheSize, 10);
  });

  it('setMaxCacheSize changes limit at runtime', async () => {
    const embedFn = async (text) => [text.length, 0];
    const ep = new EmbeddingProvider(dir, embedFn, { maxCacheSize: 5 });

    await ep.embed('a');
    await ep.embed('b');
    await ep.embed('c');
    assert.equal(ep.cacheSize, 3);

    ep.setMaxCacheSize(2);
    await ep.embed('d');
    assert.ok(ep.cacheSize <= 2, `cacheSize should be <= 2, got ${ep.cacheSize}`);
  });

  it('evicted entry can be re-embedded (cache miss)', async () => {
    const embedFn = async (text) => [text.length, 0];
    const ep = new EmbeddingProvider(dir, embedFn, { maxCacheSize: 2 });

    await ep.embed('first');
    await ep.embed('second');
    await ep.embed('third'); // evicts 'first'
    assert.equal(ep.cacheSize, 2);

    const vec = await ep.embed('first');
    assert.deepEqual(vec, [5, 0]);
    assert.equal(ep.cacheSize, 2); // evicts 'second'
  });

  it('persisted cache after eviction respects size on reload', async () => {
    const embedFn = async (text) => [text.length, 0];
    const ep = new EmbeddingProvider(dir, embedFn, { maxCacheSize: 3 });

    await ep.embed('one');
    await ep.embed('two');
    await ep.embed('three');
    await ep.embed('four'); // evicts 'one'
    await ep.saveCache();

    const ep2 = new EmbeddingProvider(dir, embedFn, { maxCacheSize: 3 });
    await ep2.loadCache();
    assert.equal(ep2.cacheSize, 3);
  });
});
