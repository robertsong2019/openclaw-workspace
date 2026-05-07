/**
 * Tests for withFallback and mapState utilities.
 * Run: npm run build && node --test test/fallback.test.mjs
 */

import { describe, it } from "node:test";
import assert from "node:assert/strict";

import { withFallback, mapState } from "../dist/fallback.js";

describe("withFallback", () => {
  it("returns node result on success", async () => {
    const node = async () => ({ result: "ok" });
    const wrapped = withFallback(node, { result: "fallback" });

    const out = await wrapped({});
    assert.deepEqual(out, { result: "ok" });
  });

  it("returns fallback on node error", async () => {
    const node = async () => { throw new Error("boom"); };
    const wrapped = withFallback(node, { result: "fallback" });

    const out = await wrapped({});
    assert.deepEqual(out, { result: "fallback" });
  });

  it("calls onError callback on failure", async () => {
    let captured = null;
    const node = async () => { throw new Error("boom"); };
    const wrapped = withFallback(node, { result: "fallback" }, (err, state) => {
      captured = { err: err.message, state };
    });

    await wrapped({ task: "test" });
    assert.equal(captured.err, "boom");
    assert.equal(captured.state.task, "test");
  });

  it("does not call onError on success", async () => {
    let called = false;
    const node = async () => ({ ok: true });
    const wrapped = withFallback(node, {}, () => { called = true; });

    await wrapped({});
    assert.equal(called, false);
  });
});

describe("mapState", () => {
  it("renames fields per mapping", () => {
    const mapper = mapState({ input: "query", score: "rating" });
    const out = mapper({ input: "hello", score: 5, extra: "ignored" });
    assert.deepEqual(out, { query: "hello", rating: 5 });
  });

  it("skips missing fields silently", () => {
    const mapper = mapState({ missing: "output" });
    const out = mapper({ other: 1 });
    assert.deepEqual(out, {});
  });

  it("passes through all fields when passthrough=true", () => {
    const mapper = mapState({ a: "alpha" }, true);
    const out = mapper({ a: 1, b: 2 });
    assert.equal(out.alpha, 1);
    assert.equal(out.b, 2);
    assert.equal(out.a, 1); // original kept
  });

  it("returns empty object with no matching fields", () => {
    const mapper = mapState({ x: "y" });
    const out = mapper({});
    assert.deepEqual(out, {});
  });
});
