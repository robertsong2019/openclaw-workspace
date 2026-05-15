import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { loop } from "../src/loop.js";
import type { AgentState } from "../src/create-node.js";

describe("loop", () => {
  it("runs node until condition is met", async () => {
    const counter = async (state: AgentState) => ({
      count: ((state.count as number) ?? 0) + 1,
    });

    const loopNode = loop({
      name: "countUp",
      node: counter,
      until: (state) => (state.count as number) >= 5,
    });

    const result = await loopNode({});
    assert.equal(result.count, 5);
    assert.equal(result.countUpIterations, 5);
  });

  it("stops at maxIterations even if condition not met", async () => {
    const alwaysIncrement = async (state: AgentState) => ({
      count: ((state.count as number) ?? 0) + 1,
    });

    const loopNode = loop({
      name: "capped",
      node: alwaysIncrement,
      until: () => false, // never terminates
      maxIterations: 3,
    });

    const result = await loopNode({});
    assert.equal(result.count, 3);
    assert.equal(result.cappedIterations, 3);
  });

  it("does not run node if condition already met", async () => {
    let calls = 0;
    const node = async (state: AgentState) => {
      calls++;
      return { count: ((state.count as number) ?? 0) + 1 };
    };

    const loopNode = loop({
      name: "already",
      node,
      until: (state) => (state.count as number) >= 3,
      maxIterations: 5,
    });

    const result = await loopNode({ count: 3 });
    // Will run once then stop since condition met after first execution
    assert.equal(result.count, 4);
    assert.equal(result.alreadyIterations, 1);
    assert.equal(calls, 1);
  });

  it("threads accumulated state through iterations", async () => {
    const append = async (state: AgentState) => ({
      items: [...((state.items as string[]) ?? []), "x"],
    });

    const loopNode = loop({
      name: "append",
      node: append,
      until: (state) => (state.items as string[]).length >= 4,
    });

    const result = await loopNode({});
    assert.deepEqual(result.items, ["x", "x", "x", "x"]);
  });

  it("exposes iteration count in predicate", async () => {
    const node = async (state: AgentState) => ({
      value: ((state.value as number) ?? 0) + 10,
    });

    const loopNode = loop({
      name: "iterCheck",
      node,
      until: (_state, iteration) => iteration >= 2,
    });

    const result = await loopNode({});
    assert.equal(result.value, 20); // 2 iterations: 10, 20
    assert.equal(result.iterCheckIterations, 2);
  });

  it("works as a LangGraph-compatible node returning plain object", async () => {
    const node = async (state: AgentState) => ({
      result: `step-${((state.step as number) ?? 0) + 1}`,
      step: ((state.step as number) ?? 0) + 1,
    });

    const loopNode = loop({
      name: "graph",
      node,
      until: (state) => (state.step as number) >= 3,
    });

    const result = await loopNode({ messages: [{ content: "start" }] });
    assert.equal(result.step, 3);
    assert.equal(result.result, "step-3");
    assert.equal(result.graphIterations, 3);
  });
});
