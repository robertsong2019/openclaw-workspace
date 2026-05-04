/**
 * Tests for openclaw-langgraph-bridge — uses built JS output
 * Run: npm run build && node --test test/bridge.test.mjs
 */

import { describe, it } from "node:test";
import assert from "node:assert/strict";

import {
  StateGraph,
  StateSchema,
  ReducedValue,
  MessagesValue,
  START,
  END,
  MemorySaver,
} from "@langchain/langgraph";
import { z } from "zod";
import { v4 as uuid } from "uuid";

import { createOpenClawNode } from "../dist/create-node.js";
import { sequentialRouter, conditionalRouter } from "../dist/supervisor.js";

// -- helpers --

function mockExecutor(role, ms = 50) {
  return async () => {
    await new Promise((r) => setTimeout(r, ms));
    return `${role} done`;
  };
}

function makeStateSchema(roleNames) {
  const fields = {
    messages: MessagesValue,
    task: z.string(),
    completedSteps: new ReducedValue(
      z.array(z.string()).default(() => []),
      { inputSchema: z.string(), reducer: (c, n) => [...c, n] }
    ),
  };
  for (const r of roleNames) {
    fields[`${r}Result`] = z.string().optional();
  }
  return new StateSchema(fields);
}

// -- tests --

describe("createOpenClawNode", () => {
  it("executes a single node workflow", async () => {
    const stateSchema = makeStateSchema(["worker"]);
    const worker = createOpenClawNode({
      name: "worker",
      systemPrompt: "Process: {input}",
      executor: mockExecutor("worker"),
    });

    const graph = new StateGraph(stateSchema)
      .addNode("worker", worker)
      .addEdge(START, "worker")
      .addEdge("worker", END)
      .compile();

    const result = await graph.invoke(
      { messages: [{ role: "user", content: "test" }], task: "test" },
      { configurable: { thread_id: uuid() } }
    );

    assert.equal(result.workerResult, "worker done");
    assert.deepEqual(result.completedSteps, ["worker"]);
  });

  it("executes a 3-step sequential pipeline", async () => {
    const roles = ["researcher", "analyst", "writer"];
    const stateSchema = makeStateSchema(roles);

    const nodes = Object.fromEntries(
      roles.map((r) => [
        r,
        createOpenClawNode({
          name: r,
          systemPrompt: `You are ${r}: {input}`,
          executor: mockExecutor(r, 30),
        }),
      ])
    );

    const router = sequentialRouter(roles);
    const possibleTargets = [...roles, END];

    let builder = new StateGraph(stateSchema);
    for (const [name, fn] of Object.entries(nodes)) {
      builder = builder.addNode(name, fn);
    }
    builder = builder
      .addConditionalEdges(START, router, possibleTargets)
      .addConditionalEdges("researcher", router, possibleTargets)
      .addConditionalEdges("analyst", router, possibleTargets)
      .addEdge("writer", END);

    const graph = builder.compile({ checkpointer: new MemorySaver() });
    const result = await graph.invoke(
      { messages: [{ role: "user", content: "pipeline test" }], task: "pipeline test" },
      { configurable: { thread_id: uuid() } }
    );

    assert.deepEqual(result.completedSteps, roles);
    assert.equal(result.researcherResult, "researcher done");
    assert.equal(result.analystResult, "analyst done");
    assert.equal(result.writerResult, "writer done");
  });

  it("falls back to task when no messages", async () => {
    const stateSchema = makeStateSchema(["agent"]);
    const agent = createOpenClawNode({
      name: "agent",
      systemPrompt: "Echo: {input}",
      executor: async (task) => `got: ${task}`,
    });

    const graph = new StateGraph(stateSchema)
      .addNode("agent", agent)
      .addEdge(START, "agent")
      .addEdge("agent", END)
      .compile();

    const result = await graph.invoke(
      { task: "hello world" },
      { configurable: { thread_id: uuid() } }
    );

    assert.equal(result.agentResult, "got: Echo: hello world");
  });
});

describe("createOpenClawNode with retry", () => {
  it("retries on executor failure and succeeds", async () => {
    let calls = 0;
    const flakyExecutor = async () => {
      calls++;
      if (calls < 3) throw new Error(`fail ${calls}`);
      return "recovered";
    };

    const stateSchema = makeStateSchema(["resilient"]);
    const node = createOpenClawNode({
      name: "resilient",
      systemPrompt: "Do: {input}",
      executor: flakyExecutor,
      retry: { maxRetries: 3, baseDelayMs: 10 },
    });

    const graph = new StateGraph(stateSchema)
      .addNode("resilient", node)
      .addEdge(START, "resilient")
      .addEdge("resilient", END)
      .compile();

    const result = await graph.invoke(
      { task: "test" },
      { configurable: { thread_id: uuid() } }
    );
    assert.equal(result.resilientResult, "recovered");
    assert.equal(calls, 3);
  });

  it("throws after exhausting retries", async () => {
    const alwaysFail = async () => { throw new Error("permanent"); };

    const stateSchema = makeStateSchema(["failnode"]);
    const node = createOpenClawNode({
      name: "failnode",
      systemPrompt: "Do: {input}",
      executor: alwaysFail,
      retry: { maxRetries: 2, baseDelayMs: 5 },
    });

    const graph = new StateGraph(stateSchema)
      .addNode("failnode", node)
      .addEdge(START, "failnode")
      .addEdge("failnode", END)
      .compile();

    await assert.rejects(
      () => graph.invoke({ task: "test" }, { configurable: { thread_id: uuid() } }),
      { message: "permanent" }
    );
  });
});

describe("sequentialRouter", () => {
  it("routes to first uncompleted step", () => {
    const router = sequentialRouter(["a", "b", "c"]);
    assert.equal(router({ completedSteps: [] }), "a");
    assert.equal(router({ completedSteps: ["a"] }), "b");
    assert.equal(router({ completedSteps: ["a", "b"] }), "c");
    assert.equal(router({ completedSteps: ["a", "b", "c"] }), END);
  });
});

describe("conditionalRouter", () => {
  it("routes based on state field value", () => {
    const router = conditionalRouter("sentiment", {
      positive: "cheer",
      negative: "comfort",
    });
    assert.equal(router({ sentiment: "positive" }), "cheer");
    assert.equal(router({ sentiment: "negative" }), "comfort");
  });

  it("falls back to END for unknown values", () => {
    const router = conditionalRouter("action", { go: "run" });
    assert.equal(router({ action: "go" }), "run");
    assert.equal(router({ action: "unknown" }), END);
    assert.equal(router({}), END);
  });

  it("supports custom fallback", () => {
    const router = conditionalRouter("type", { a: "nodeA" }, "nodeB");
    assert.equal(router({ type: "a" }), "nodeA");
    assert.equal(router({ type: "other" }), "nodeB");
  });

  it("integrates with LangGraph conditional branching", async () => {
    const roles = ["researcher", "writer"];
    const stateSchema = makeStateSchema(roles);
    // Add a branch field to the schema is not needed — it's dynamic

    const router = conditionalRouter(
      "messages",
      {}, // messages is an array, not a string → always fallback
      "researcher"
    );
    // Simpler: route based on a field we control
    const branchRouter = (state) => {
      // If researcher already ran, go to writer; else researcher
      const completed = new Set(state.completedSteps ?? []);
      return completed.has("researcher") ? "writer" : "researcher";
    };

    const graph = new StateGraph(stateSchema)
      .addNode(
        "researcher",
        createOpenClawNode({
          name: "researcher",
          systemPrompt: "Research: {input}",
          executor: async () => "research done",
        })
      )
      .addNode(
        "writer",
        createOpenClawNode({
          name: "writer",
          systemPrompt: "Write: {input}",
          executor: async () => "writer done",
        })
      )
      .addConditionalEdges(START, branchRouter, [...roles, END])
      .addEdge("researcher", "writer")
      .addEdge("writer", END)
      .compile();

    const result = await graph.invoke(
      { task: "test branching" },
      { configurable: { thread_id: uuid() } }
    );

    assert.equal(result.researcherResult, "research done");
    assert.equal(result.writerResult, "writer done");
    assert.deepEqual(result.completedSteps, ["researcher", "writer"]);
  });
});
