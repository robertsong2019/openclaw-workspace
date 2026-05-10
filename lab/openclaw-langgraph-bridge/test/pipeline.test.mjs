/**
 * Tests for pipeline — sequential node composition
 * Run: npm run build && node --test test/pipeline.test.mjs
 */
import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { pipeline } from "../dist/pipeline.js";

describe("pipeline", () => {
  it("runs nodes sequentially, merging state", async () => {
    const node1 = async (s) => ({ step1: "done", count: (s.count ?? 0) + 1 });
    const node2 = async (s) => ({ step2: "done", count: (s.count ?? 0) + 10 });

    const pipe = pipeline({ name: "basic", nodes: [node1, node2] });
    const result = await pipe({ task: "hello" });

    assert.equal(result.step1, "done");
    assert.equal(result.step2, "done");
    assert.equal(result.count, 11);
  });

  it("passes accumulated state through chain", async () => {
    const enrich = async () => ({ data: "enriched" });
    const transform = async (s) => ({ result: `${s.data}-transformed` });

    const pipe = pipeline({ name: "chain", nodes: [enrich, transform] });
    const result = await pipe({});

    assert.equal(result.result, "enriched-transformed");
  });

  it("throws on first error by default", async () => {
    const fail = async () => { throw new Error("boom"); };

    const pipe = pipeline({ name: "fail-fast", nodes: [async () => ({ a: 1 }), fail, async () => ({ b: 2 })] });
    await assert.rejects(() => pipe({}), /Pipeline "fail-fast" failed at node 1: boom/);
  });

  it("continues on error when continueOnError is true", async () => {
    const pipe = pipeline({
      name: "tolerant",
      nodes: [
        async () => ({ a: 1 }),
        async () => { throw new Error("soft fail"); },
        async () => ({ c: 3 }),
      ],
      continueOnError: true,
    });
    const result = await pipe({});

    assert.equal(result.a, 1);
    assert.equal(result.c, 3);
    assert.ok(result.tolerantErrors);
    assert.equal(Object.keys(result.tolerantErrors).length, 1);
  });

  it("collects completedSteps from child nodes", async () => {
    const pipe = pipeline({
      name: "steps",
      nodes: [
        async () => ({ completedSteps: "agent-a" }),
        async () => ({ completedSteps: "agent-b" }),
      ],
    });
    const result = await pipe({});

    assert.deepEqual(result.completedSteps, ["agent-a", "agent-b"]);
  });

  it("handles empty node list", async () => {
    const pipe = pipeline({ name: "empty", nodes: [] });
    const result = await pipe({ task: "noop" });

    assert.equal(result.task, "noop");
    assert.deepEqual(result.completedSteps, []);
  });
});
