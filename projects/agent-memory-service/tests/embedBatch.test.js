import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { EmbeddingProvider } from '../src/index.js';

function makeProvider(opts = {}) {
  const dir = mkdtempSync(join(tmpdir(), 'embed-batch-'));
  let embedCalls = [];
  const embedFn = async (text) => {
    embedCalls.push(text);
    return [text.length, text.charCodeAt(0)];
  };
  const p = new EmbeddingProvider(dir, embedFn, opts);
  return { provider: p, dir, embedCalls };
}

describe('embedBatch()', () => {
  it('returns empty array for empty input', async () => {
    const { provider, dir } = makeProvider();
    await provider.loadCache();
    const res = await provider.embedBatch([]);
    assert.deepEqual(res, []);
    rmSync(dir, { recursive: true });
  });

  it('embeds multiple unique texts', async () => {
    const { provider, dir, embedCalls } = makeProvider();
    await provider.loadCache();
    const res = await provider.embedBatch(['hello', 'world']);
    assert.equal(res.length, 2);
    assert.deepEqual(res[0], [5, 104]);
    assert.deepEqual(res[1], [5, 119]);
    assert.equal(embedCalls.length, 2);
    rmSync(dir, { recursive: true });
  });

  it('deduplicates identical texts, calls embedFn once', async () => {
    const { provider, dir, embedCalls } = makeProvider();
    await provider.loadCache();
    const res = await provider.embedBatch(['abc', 'abc', 'abc']);
    assert.equal(res.length, 3);
    assert.deepEqual(res[0], res[1]);
    assert.deepEqual(res[1], res[2]);
    assert.equal(embedCalls.length, 1);
    rmSync(dir, { recursive: true });
  });

  it('serves cached results on second call (no re-embed)', async () => {
    const { provider, dir, embedCalls } = makeProvider();
    await provider.loadCache();
    await provider.embedBatch(['cat', 'dog']);
    assert.equal(embedCalls.length, 2);
    const res = await provider.embedBatch(['cat', 'dog']);
    assert.equal(embedCalls.length, 2); // no new calls
    assert.equal(res.length, 2);
    rmSync(dir, { recursive: true });
  });

  it('mixes cached and uncached texts efficiently', async () => {
    const { provider, dir, embedCalls } = makeProvider();
    await provider.loadCache();
    await provider.embedBatch(['cached']);
    assert.equal(embedCalls.length, 1);
    const res = await provider.embedBatch(['cached', 'new']);
    assert.equal(embedCalls.length, 2); // only 1 new call
    assert.equal(res.length, 2);
    assert.ok(res[0] !== null);
    assert.ok(res[1] !== null);
    rmSync(dir, { recursive: true });
  });

  it('returns nulls when embedFn is null (disabled)', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'embed-batch-'));
    const provider = new EmbeddingProvider(dir, null);
    await provider.loadCache();
    const res = await provider.embedBatch(['a', 'b']);
    assert.deepEqual(res, [null, null]);
    rmSync(dir, { recursive: true });
  });

  it('throws on non-array input', async () => {
    const { provider, dir } = makeProvider();
    await provider.loadCache();
    await assert.rejects(() => provider.embedBatch('not array'), /array/);
    rmSync(dir, { recursive: true });
  });

  it('returns null for failed embed calls without affecting others', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'embed-batch-'));
    let callCount = 0;
    const failFn = async (text) => {
      callCount++;
      if (text === 'fail') throw new Error('API error');
      return [1, 2, 3];
    };
    const provider = new EmbeddingProvider(dir, failFn);
    await provider.loadCache();
    const res = await provider.embedBatch(['ok', 'fail', 'also ok']);
    assert.equal(res.length, 3);
    assert.deepEqual(res[0], [1, 2, 3]);
    assert.equal(res[1], null);
    assert.deepEqual(res[2], [1, 2, 3]);
    assert.equal(callCount, 3);
    rmSync(dir, { recursive: true });
  });

  it('respects TTL: expired entries re-embedded in batch', async () => {
    const { provider, dir, embedCalls } = makeProvider({ cacheTTL: 50 });
    await provider.loadCache();
    await provider.embedBatch(['old']);
    assert.equal(embedCalls.length, 1);
    await new Promise(r => setTimeout(r, 60));
    const res = await provider.embedBatch(['old']);
    assert.equal(embedCalls.length, 2); // re-embedded
    assert.ok(res[0] !== null);
    rmSync(dir, { recursive: true });
  });
});
