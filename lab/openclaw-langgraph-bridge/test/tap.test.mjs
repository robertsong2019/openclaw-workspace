import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { tap, tapBefore, tapAfter } from "../dist/tap.js";

describe("tap", () => {
  it("returns original state unchanged", async () => {
    const state = { x: 1, y: "hello" };
    const sideEffects = [];
    const t = tap({ onState: (s) => sideEffects.push(s) });
    const result = await t(state);
    assert.deepStrictEqual(result, state);
    assert.strictEqual(sideEffects.length, 1);
    assert.deepStrictEqual(sideEffects[0], state);
  });

  it("supports async onState callback", async () => {
    const state = { a: 42 };
    let called = false;
    const t = tap({
      onState: async () => {
        await Promise.resolve();
        called = true;
      },
    });
    const result = await t(state);
    assert.deepStrictEqual(result, state);
    assert.strictEqual(called, true);
  });

  it("swallows errors from onState", async () => {
    const state = { z: true };
    const t = tap({
      onState: () => {
        throw new Error("boom");
      },
    });
    const result = await t(state);
    assert.deepStrictEqual(result, state);
  });

  it("calls onError when onState throws", async () => {
    const state = { n: 0 };
    let captured;
    const t = tap({
      onState: () => {
        throw new Error("fail");
      },
      onError: (err, s) => {
        captured = { err, s };
      },
    });
    await t(state);
    assert.ok(captured);
    assert.deepStrictEqual(captured.s, state);
    assert.ok(captured.err instanceof Error);
  });

  it("tapBefore runs side effect before node", async () => {
    const order = [];
    const node = async (s) => {
      order.push("node");
      return { ...s, done: true };
    };
    const wrapped = tapBefore(node, () => order.push("tap"));
    const result = await wrapped({ x: 1 });
    assert.deepStrictEqual(order, ["tap", "node"]);
    assert.strictEqual(result.done, true);
  });

  it("tapBefore swallows tap errors", async () => {
    const node = async (s) => ({ ...s, ok: true });
    const wrapped = tapBefore(node, () => {
      throw new Error("tap fail");
    });
    const result = await wrapped({ x: 1 });
    assert.strictEqual(result.ok, true);
  });

  it("tapAfter sees output state", async () => {
    let captured;
    const node = async (s) => ({ ...s, added: 99 });
    const wrapped = tapAfter(node, (s) => { captured = s; });
    await wrapped({ x: 1 });
    assert.deepStrictEqual(captured, { x: 1, added: 99 });
  });

  it("tapAfter swallows tap errors", async () => {
    const node = async (s) => ({ ...s, ok: true });
    const wrapped = tapAfter(node, () => {
      throw new Error("tap fail");
    });
    const result = await wrapped({ x: 1 });
    assert.strictEqual(result.ok, true);
  });
});
