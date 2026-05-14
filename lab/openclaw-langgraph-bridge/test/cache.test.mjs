import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { withCache } from "../dist/cache.js";

describe("withCache", () => {
  it("caches result for same input", async () => {
    let calls = 0;
    const node = withCache(
      async (state) => ({ doubled: (state.x) * 2 }),
      { name: "test" }
    );

    const r1 = await node({ x: 5 });
    assert.equal(r1.doubled, 10);
    assert.equal(r1.testHit, false);

    const r2 = await node({ x: 5 });
    assert.equal(r2.doubled, 10);
    assert.equal(r2.testHit, true);

    calls++; // we track via hit/miss stats
    const stats = (node).cacheStats();
    assert.equal(stats.hits, 1);
    assert.equal(stats.misses, 1);
    assert.equal(stats.hitRate, 0.5);
  });

  it("different inputs are separate cache entries", async () => {
    const node = withCache(
      async (state) => ({ v: state.x }),
      { name: "sep" }
    );

    await node({ x: 1 });
    await node({ x: 2 });
    await node({ x: 1 }); // cache hit

    const stats = (node).cacheStats();
    assert.equal(stats.hits, 1);
    assert.equal(stats.misses, 2);
    assert.equal(stats.size, 2);
  });

  it("respects maxSize eviction (FIFO)", async () => {
    const node = withCache(
      async (state) => ({ v: state.x }),
      { maxSize: 2, name: "evict" }
    );

    await node({ x: 1 });
    await node({ x: 2 });
    await node({ x: 3 }); // evicts x=1

    const stats = (node).cacheStats();
    assert.equal(stats.size, 2);

    // x=1 should be evicted → cache miss
    const r = await node({ x: 1 });
    assert.equal(r.evictHit, false);
  });

  it("respects TTL expiration", async () => {
    const node = withCache(
      async (state) => ({ v: state.x }),
      { ttlMs: 50, name: "ttl" }
    );

    await node({ x: 1 });
    // Wait for TTL
    await new Promise((r) => setTimeout(r, 60));

    const r = await node({ x: 1 });
    assert.equal(r.ttlHit, false); // expired → miss
  });

  it("custom keyFn uses only specified fields", async () => {
    const node = withCache(
      async (state) => ({ v: state.val }),
      { keyFn: (s) => String(s.key), name: "custom" }
    );

    await node({ key: "a", val: 1 });
    const r = await node({ key: "a", val: 999 }); // same key → hit
    assert.equal(r.customHit, true);
    // val=1 from cache, not 999
    assert.equal(r.v, 1);
  });

  it("maxSize=0 disables caching", async () => {
    const node = withCache(
      async (state) => ({ v: state.x }),
      { maxSize: 0, name: "off" }
    );

    await node({ x: 1 });
    await node({ x: 1 }); // still miss

    const stats = (node).cacheStats();
    assert.equal(stats.size, 0);
    assert.equal(stats.misses, 2);
  });

  it("cacheClear resets everything", async () => {
    const node = withCache(
      async (state) => ({ v: state.x }),
      { name: "clear" }
    );

    await node({ x: 1 });
    await node({ x: 1 });
    (node).cacheClear();

    const stats = (node).cacheStats();
    assert.equal(stats.size, 0);
    assert.equal(stats.hits, 0);
    assert.equal(stats.misses, 0);
  });
});
