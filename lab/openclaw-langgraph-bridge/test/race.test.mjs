import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { race } from "../dist/race.js";

describe("race", () => {
  it("returns result of first node to resolve", async () => {
    const fast = async () => ({ answer: "fast" });
    const slow = async () =>
      new Promise((r) => setTimeout(() => r({ answer: "slow" }), 100));

    const raceNode = race({
      name: "speed",
      nodes: { fast, slow },
    });

    const result = await raceNode({});
    assert.equal(result.answer, "fast");
    assert.equal(result._raceWinner, "fast");
  });

  it("records which node won via _raceWinner", async () => {
    const a = async () =>
      new Promise((r) => setTimeout(() => r({ v: "a" }), 50));
    const b = async () => ({ v: "b" });

    const raceNode = race({ name: "ab", nodes: { a, b } });
    const result = await raceNode({});
    assert.equal(result._raceWinner, "b");
    assert.equal(result.v, "b");
  });

  it("passes state to all competing nodes", async () => {
    const node = async (state) => ({ echo: state.msg });
    const raceNode = race({ name: "echo", nodes: { n1: node } });
    const result = await raceNode({ msg: "hello" });
    assert.equal(result.echo, "hello");
  });

  it("returns fallback if all nodes reject and fallback provided", async () => {
    const fail = async () => {
      throw new Error("boom");
    };

    const raceNode = race({
      name: "fallback",
      nodes: { f1: fail, f2: fail },
      fallback: { answer: "default" },
    });

    const result = await raceNode({});
    assert.equal(result.answer, "default");
    assert.equal(result._raceWinner, undefined);
  });

  it("throws if all nodes reject with no fallback", async () => {
    const fail = async () => {
      throw new Error("nope");
    };

    const raceNode = race({
      name: "noFallback",
      nodes: { f1: fail },
    });

    await assert.rejects(() => raceNode({}), /all nodes failed/);
  });

  it("returns empty object for empty nodes map", async () => {
    const raceNode = race({ name: "empty", nodes: {} });
    const result = await raceNode({});
    assert.deepEqual(result, {});
  });

  it("uses fallback for empty nodes when provided", async () => {
    const raceNode = race({
      name: "emptyFallback",
      nodes: {},
      fallback: { data: 42 },
    });
    const result = await raceNode({});
    assert.deepEqual(result, { data: 42 });
  });

  it("single node wins immediately", async () => {
    const solo = async () => ({ only: true });
    const raceNode = race({ name: "solo", nodes: { s: solo } });
    const result = await raceNode({});
    assert.equal(result.only, true);
    assert.equal(result._raceWinner, "s");
  });
});
