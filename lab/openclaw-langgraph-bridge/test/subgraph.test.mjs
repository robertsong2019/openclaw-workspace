import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { subgraph } from "../dist/subgraph.js";

describe("subgraph", () => {
  it("runs nodes sequentially and merges state", async () => {
    const sg = subgraph({
      name: "basic",
      nodes: [
        async (s) => ({ count: ((s.count) ?? 0) + 1 }),
        async (s) => ({ count: (s.count) + 10 }),
      ],
    });
    const result = await sg({ count: 0 });
    assert.equal(result.count, 11);
  });

  it("maps input state before execution", async () => {
    const sg = subgraph({
      name: "input-map",
      nodes: [async (s) => ({ total: s.x + s.y })],
      inputMapping: (outer) => ({ x: outer.a, y: outer.b }),
    });
    const result = await sg({ a: 3, b: 4 });
    assert.equal(result.total, 7);
  });

  it("maps output state after execution", async () => {
    const sg = subgraph({
      name: "output-map",
      nodes: [async () => ({ secret: 42 })],
      outputMapping: (inner) => ({ answer: inner.secret }),
    });
    const result = await sg({});
    assert.equal(result.answer, 42);
    assert.equal(result.secret, undefined);
  });

  it("isolates errors when isolateErrors is true", async () => {
    const sg = subgraph({
      name: "isolated",
      nodes: [
        async () => ({ step: 1 }),
        async () => { throw new Error("boom"); },
        async () => ({ step: 3 }),
      ],
      isolateErrors: true,
    });
    const result = await sg({});
    assert.equal(result.step, 3);
    const errs = result.isolatedErrors;
    assert.equal(errs.length, 1);
    assert.equal(errs[0].step, 1);
  });

  it("throws on error when isolateErrors is false", async () => {
    const sg = subgraph({
      name: "throw",
      nodes: [async () => { throw new Error("fail"); }],
    });
    await assert.rejects(() => sg({}), /Subgraph "throw" failed at node 0/);
  });

  it("combines input and output mapping", async () => {
    const sg = subgraph({
      name: "round-trip",
      nodes: [async (s) => ({ doubled: s.val * 2 })],
      inputMapping: (outer) => ({ val: outer.input }),
      outputMapping: (inner) => ({ result: inner.doubled }),
    });
    const result = await sg({ input: 5 });
    assert.equal(result.result, 10);
  });
});
