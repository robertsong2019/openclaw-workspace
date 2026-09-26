import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { withRateLimit } from "../dist/rate-limit.js";

const noop = async (s) => ({ ...s });

describe("withRateLimit", () => {
  it("allows calls within limit", async () => {
    const node = async (s) => ({ ...s, done: true });
    const limited = withRateLimit(node, { maxCalls: 3, windowMs: 1000 });

    for (let i = 0; i < 3; i++) {
      const r = await limited({ i });
      assert.equal(r.done, true);
    }
  });

  it("rejects calls exceeding limit", async () => {
    const node = async () => ({ ok: true });
    const limited = withRateLimit(node, { maxCalls: 2, windowMs: 5000 });

    await limited({});
    await limited({});
    await assert.rejects(() => limited({}), /Rate limit exceeded/);
  });

  it("returns fallback state with strategy=return", async () => {
    const node = async () => ({ ok: true });
    const limited = withRateLimit(node, {
      maxCalls: 1,
      windowMs: 5000,
      strategy: "return",
      fallbackState: { queued: true },
    });

    await limited({});
    const result = await limited({});
    assert.equal(result.rateLimited, true);
    assert.equal(result.queued, true);
  });

  it("partitions by keyFn", async () => {
    const node = async () => ({ ok: true });
    const limited = withRateLimit(node, {
      maxCalls: 1,
      windowMs: 5000,
      keyFn: (s) => s.userId,
    });

    const r1 = await limited({ userId: "a" });
    const r2 = await limited({ userId: "b" });
    assert.equal(r1.ok, true);
    assert.equal(r2.ok, true);
    // Third call for "a" should fail
    await assert.rejects(() => limited({ userId: "a" }), /Rate limit exceeded/);
  });

  it("window expires and allows new calls", async () => {
    const node = async () => ({ ok: true });
    const limited = withRateLimit(node, { maxCalls: 1, windowMs: 50 });

    await limited({});
    await assert.rejects(() => limited({}), /Rate limit exceeded/);

    // Wait for window to expire
    await new Promise((r) => setTimeout(r, 60));
    const result = await limited({});
    assert.equal(result.ok, true);
  });

  it("cleans up expired entries", async () => {
    const node = async (s) => ({ ok: true });
    const limited = withRateLimit(node, { maxCalls: 1, windowMs: 30 });

    await limited({ key: "a" });
    await new Promise((r) => setTimeout(r, 40));
    // After expiry, calling with different key triggers cleanup
    const result = await limited({ key: "b" });
    assert.equal(result.ok, true);
  });

  // --- config validation pins (mirror throttle's RangeError contract) ---
  // Before the guard, maxCalls=NaN made `length >= NaN` always false and
  // windowMs<=0/NaN emptied the window every call: the limiter silently
  // became a no-op instead of failing loudly.

  it("maxCalls=0 must throw RangeError (deny-all is a config mistake)", () => {
    assert.throws(
      () => withRateLimit(noop, { maxCalls: 0, windowMs: 50 }),
      RangeError
    );
  });

  it("maxCalls negative must throw RangeError", () => {
    assert.throws(
      () => withRateLimit(noop, { maxCalls: -1, windowMs: 50 }),
      RangeError
    );
  });

  it("maxCalls NaN must throw RangeError (silently disabled the limiter)", () => {
    assert.throws(
      () => withRateLimit(noop, { maxCalls: NaN, windowMs: 50 }),
      RangeError
    );
  });

  it("maxCalls Infinity must throw RangeError", () => {
    assert.throws(
      () => withRateLimit(noop, { maxCalls: Infinity, windowMs: 50 }),
      RangeError
    );
  });

  it("maxCalls fractional < 1 must throw RangeError", () => {
    assert.throws(
      () => withRateLimit(noop, { maxCalls: 0.5, windowMs: 50 }),
      RangeError
    );
  });

  it("maxCalls non-number string must throw RangeError (no coercion)", () => {
    assert.throws(
      () => withRateLimit(noop, { maxCalls: "3", windowMs: 50 }),
      RangeError
    );
  });

  it("windowMs=0 must throw RangeError (silently disabled the limiter)", () => {
    assert.throws(
      () => withRateLimit(noop, { maxCalls: 1, windowMs: 0 }),
      RangeError
    );
  });

  it("windowMs negative must throw RangeError", () => {
    assert.throws(
      () => withRateLimit(noop, { maxCalls: 1, windowMs: -100 }),
      RangeError
    );
  });

  it("windowMs NaN must throw RangeError", () => {
    assert.throws(
      () => withRateLimit(noop, { maxCalls: 1, windowMs: NaN }),
      RangeError
    );
  });

  it("valid config still works after guards (maxCalls=1, windowMs=20)", async () => {
    const limited = withRateLimit(noop, { maxCalls: 1, windowMs: 20 });
    const r = await limited({ ok: true });
    assert.equal(r.ok, true);
  });
});
