/**
 * multi-agent.test.mjs — 多 Agent 编排测试
 */

import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { AgentPool, Orchestrator, createCodeWorkflow } from "../dist/multi-agent.js";

// ── Helper ─────────────────────────────────────────────

const makeExecutor = (output) => async (_task) => output;

const testRoles = [
  {
    id: "analyzer",
    description: "分析代码",
    capabilities: ["analyze", "codegraph"],
    config: { name: "analyzer", systemPrompt: "You are an analyzer.", executor: makeExecutor("analysis done") },
  },
  {
    id: "coder",
    description: "写代码",
    capabilities: ["code", "fix"],
    config: { name: "coder", systemPrompt: "You are a coder.", executor: makeExecutor("code written") },
  },
  {
    id: "tester",
    description: "跑测试",
    capabilities: ["test", "verify"],
    config: { name: "tester", systemPrompt: "You are a tester.", executor: makeExecutor("tests passed") },
  },
  {
    id: "reviewer",
    description: "审查代码",
    capabilities: ["review"],
    config: { name: "reviewer", systemPrompt: "You are a reviewer.", executor: makeExecutor("approved") },
  },
  {
    id: "general",
    description: "通用",
    capabilities: ["*"],
    config: { name: "general", systemPrompt: "General agent.", executor: makeExecutor("done") },
  },
];

// ── AgentPool Tests ────────────────────────────────────

describe("AgentPool", () => {
  const pool = new AgentPool({ roles: testRoles });

  it("lists all roles", () => {
    assert.equal(pool.listRoles().length, 5);
  });

  it("gets a role by id", () => {
    assert.equal(pool.getRole("coder")?.id, "coder");
  });

  it("returns undefined for unknown role", () => {
    assert.equal(pool.getRole("nonexistent"), undefined);
  });

  it("finds best agent by exact capability", () => {
    assert.equal(pool.findBestAgent("code")?.id, "coder");
    assert.equal(pool.findBestAgent("test")?.id, "tester");
    assert.equal(pool.findBestAgent("analyze")?.id, "analyzer");
  });

  it("finds fix agent (coder handles fixes)", () => {
    assert.equal(pool.findBestAgent("fix")?.id, "coder");
  });

  it("falls back to wildcard agent", () => {
    assert.equal(pool.findBestAgent("deploy")?.id, "general");
  });

  it("returns undefined when no agent matches and no wildcard", () => {
    const smallPool = new AgentPool({
      roles: [testRoles[0]], // only analyzer, no wildcard
    });
    assert.equal(smallPool.findBestAgent("deploy"), undefined);
  });

  it("executes a task with a role", async () => {
    const result = await pool.execute("coder", "implement feature X");
    assert.equal(result, "code written");
  });

  it("throws for unknown role on execute", async () => {
    await assert.rejects(() => pool.execute("nonexistent", "task"), /Unknown agent role/);
  });

  it("creates a LangGraph node for a role", async () => {
    const node = pool.createNode("coder");
    assert.ok(typeof node === "function");
  });

  it("throws for unknown role on createNode", () => {
    assert.throws(() => pool.createNode("nonexistent"), /Unknown agent role/);
  });

  it("routeAndExecute finds right agent", async () => {
    const { agent, result } = await pool.routeAndExecute("test", "run all tests");
    assert.equal(agent, "tester");
    assert.equal(result, "tests passed");
  });

  it("routeAndExecute throws when no agent available", async () => {
    const smallPool = new AgentPool({ roles: [testRoles[0]] });
    await assert.rejects(() => smallPool.routeAndExecute("deploy", "deploy to prod"), /No agent available/);
  });
});

// ── Orchestrator Tests ─────────────────────────────────

describe("Orchestrator", () => {
  const pool = new AgentPool({ roles: testRoles });
  const orch = new Orchestrator(pool);

  it("runs a single task", async () => {
    const result = await orch.run([
      { id: "t1", description: "analyze codebase", type: "analyze", input: {} },
    ]);
    assert.equal(result.stats.total, 1);
    assert.equal(result.stats.passed, 1);
    assert.equal(result.stats.failed, 0);
    assert.equal(result.results.get("t1"), "analysis done");
  });

  it("runs multiple independent tasks in parallel", async () => {
    const result = await orch.run([
      { id: "t1", description: "analyze", type: "analyze", input: {} },
      { id: "t2", description: "write code", type: "code", input: {} },
      { id: "t3", description: "run tests", type: "test", input: {} },
    ]);
    assert.equal(result.stats.passed, 3);
    assert.equal(result.results.get("t1"), "analysis done");
    assert.equal(result.results.get("t2"), "code written");
    assert.equal(result.results.get("t3"), "tests passed");
  });

  it("respects task dependencies (runs in order)", async () => {
    const order = [];
    const depPool = new AgentPool({
      roles: [
        {
          id: "worker",
          description: "worker",
          capabilities: ["*"],
          config: {
            name: "worker",
            systemPrompt: "worker",
            executor: async (task) => { order.push(task); return task + " done"; },
          },
        },
      ],
    });
    const depOrch = new Orchestrator(depPool);

    await depOrch.run([
      { id: "step1", description: "step1", type: "step", input: {} },
      { id: "step2", description: "step2", type: "step", input: {}, dependsOn: ["step1"] },
      { id: "step3", description: "step3", type: "step", input: {}, dependsOn: ["step2"] },
    ]);

    // step1 must come before step2, step2 before step3
    assert.ok(order.indexOf("step1") < order.indexOf("step2"));
    assert.ok(order.indexOf("step2") < order.indexOf("step3"));
  });

  it("handles failing tasks gracefully", async () => {
    const failPool = new AgentPool({
      roles: [{
        id: "failer",
        description: "always fails",
        capabilities: ["*"],
        config: {
          name: "failer",
          systemPrompt: "fail",
          executor: async () => { throw new Error("boom"); },
        },
      }],
    });
    const failOrch = new Orchestrator(failPool);

    const result = await failOrch.run([
      { id: "t1", description: "try this", type: "any", input: {} },
    ]);
    assert.equal(result.stats.failed, 1);
    assert.equal(result.stats.passed, 0);
    assert.equal(result.log[0].status, "failure");
  });
});

// ── Code Workflow Tests ────────────────────────────────

describe("createCodeWorkflow", () => {
  it("creates workflow with pool", () => {
    const wf = createCodeWorkflow({ pool: { roles: testRoles } });
    assert.ok(wf.pool);
    assert.equal(wf.maxLoops, 3);
  });

  it("respects custom maxFixLoops", () => {
    const wf = createCodeWorkflow({ pool: { roles: [] }, maxFixLoops: 5 });
    assert.equal(wf.maxLoops, 5);
  });

  it("pool routes correctly within workflow", async () => {
    const wf = createCodeWorkflow({ pool: { roles: testRoles } });
    const { agent } = await wf.pool.routeAndExecute("code", "implement feature");
    assert.equal(agent, "coder");
  });
});
