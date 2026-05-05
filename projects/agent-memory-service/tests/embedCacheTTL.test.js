import { describe, it, before, after, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { EmbeddingProvider } from '../src/index.js';

function makeProvider(opts = {}) {
  const dir = mkdtempSync(join(tmpdir(), 'embed-ttl-'));
  const embedFn = async (text) => {
    // Deterministic fake vector based on text length
    return [text.length, text.length * 2, text.length * 3];
  };
  const p = new EmbeddingProvider(dir, embedFn, opts);
  return { provider: p, dir };
}

describe('EmbeddingProvider TTL eviction', () => {
  it('cacheTTL=0 means no expiry', async () => {
    const { provider, dir } = makeProvider({ cacheTTL: 0 });
    await provider.embed('hello');
    await provider.embed('world');
    assert.equal(provider.cacheSize, 2);
    rmSync(dir, { recursive: true });
  });

  it('evicts expired entries on access', async () => {
    const { provider, dir } = makeProvider({ cacheTTL: 100 }); // 100ms TTL
    await provider.embed('alpha');
    assert.equal(provider.cacheSize, 1);

    // Wait for TTL to expire
    await new Promise(r => setTimeout(r, 150));

    // Access should detect expired entry and re-embed
    const vec = await provider.embed('alpha');
    assert.ok(vec, 'should return re-embedded vector');
    assert.equal(provider.cacheSize, 1);
    rmSync(dir, { recursive: true });
  });

  it('non-expired entries are served from cache', async () => {
    const { provider, dir } = makeProvider({ cacheTTL: 5000 });
    const v1 = await provider.embed('fresh');
    const v2 = await provider.embed('fresh');
    assert.deepEqual(v1, v2);
    rmSync(dir, { recursive: true });
  });

  it('evictExpired() removes all stale entries', async () => {
    const { provider, dir } = makeProvider({ cacheTTL: 100 });
    await provider.embed('a');
    await provider.embed('b');
    await provider.embed('c');
    assert.equal(provider.cacheSize, 3);

    await new Promise(r => setTimeout(r, 150));

    const evicted = provider.evictExpired();
    assert.equal(evicted, 3);
    assert.equal(provider.cacheSize, 0);
    rmSync(dir, { recursive: true });
  });

  it('setCacheTTL() changes TTL at runtime', async () => {
    const { provider, dir } = makeProvider({ cacheTTL: 5000 });
    await provider.embed('persistent');

    // Shrink TTL to force expiry
    provider.setCacheTTL(50);
    await new Promise(r => setTimeout(r, 100));

    const evicted = provider.evictExpired();
    assert.equal(evicted, 1);
    assert.equal(provider.cacheSize, 0);
    rmSync(dir, { recursive: true });
  });

  it('timestamps persist across loadCache/saveCache', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'embed-ttl-persist-'));
    const embedFn = async (text) => [1, 2, 3];

    // First provider: embed + save
    const p1 = new EmbeddingProvider(dir, embedFn, { cacheTTL: 60000 });
    await p1.embed('saved');
    await p1.saveCache();

    // Second provider: load cache
    const p2 = new EmbeddingProvider(dir, embedFn, { cacheTTL: 60000 });
    await p2.loadCache();
    assert.equal(p2.cacheSize, 1);

    // The loaded entry should have a timestamp (accessible via evictExpired with tiny TTL)
    p2.setCacheTTL(1);
    await new Promise(r => setTimeout(r, 5));
    const evicted = p2.evictExpired();
    // If timestamp was persisted, the old entry should be evicted
    assert.equal(evicted, 1, 'persisted entry should have timestamp and be evictable');
    rmSync(dir, { recursive: true });
  });

  it('legacy cache format (vector-only) loads correctly', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'embed-ttl-legacy-'));
    const embedFn = async (text) => [1, 2, 3];

    // Write legacy format manually
    const { writeFileSync } = await import('node:fs');
    const { join: j } = await import('node:path');
    writeFileSync(j(dir, 'embed-cache.json'), JSON.stringify({
      abc123: [1.0, 2.0, 3.0],
      def456: [4.0, 5.0, 6.0],
    }));

    const p = new EmbeddingProvider(dir, embedFn, { cacheTTL: 60000 });
    await p.loadCache();
    assert.equal(p.cacheSize, 2);
    rmSync(dir, { recursive: true });
  });
});
