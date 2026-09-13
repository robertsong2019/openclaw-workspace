/**
 * openclaw-client.test.mjs — Gateway HTTP client hardening + multi-agent coverage.
 *
 * Red-first targets (2026-09-14 cycle):
 *   1. timeoutSeconds: 0 silently dropped (falsy-zero family)
 *   2. 200 + non-JSON body → raw SyntaxError, no diagnostic (unguarded-parse family)
 *   3. connection refused → raw "fetch failed", baseUrl lost (diagnostics)
 *
 * Also pins Orchestrator circular-dependency + dep-on-failed semantics and
 * AgentPool.createNode retry-wrapping path (previously uncovered lines).
 */

import { describe, it } from "node:test";
import assert from "node:assert/strict";
import http from "node:http";
import { OpenClawClient } from "../dist/openclaw-client.js";
import { AgentPool, Orchestrator } from "../dist/multi-agent.js";

// ── HTTP harness ───────────────────────────────────────

/**
 * Start a one-shot capture server. Returns { server, port, requests }.
 * `requests` records { method, url, headers, body } per hit.
 */
function startCaptureServer(handler) {
  const requests = [];
  const server = http.createServer((req, res) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      requests.push({
        method: req.method,
        url: req.url,
        headers: req.headers,
        body: Buffer.concat(chunks).toString("utf8"),
      });
      handler(req, res, requests[requests.length - 1]);
    });
  });
  return new Promise((resolve) => {
    server.listen(0, "127.0.0.1", () =>
      resolve({ server, port: server.address().port, requests })
    );
  });
}

const jsonResponse = (res, status, payload) => {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(typeof payload === "string" ? payload : JSON.stringify(payload));
};

// ── spawn(): request shape ─────────────────────────────

describe("OpenClawClient.spawn request shape", () => {
  it("POSTs task JSON to /api/sessions/spawn with mode/runtime defaults", async () => {
    const { server, port, requests } = await startCaptureServer((req, res) =>
      jsonResponse(res, 200, { ok: true })
    );
    try {
      const client = new OpenClawClient({ baseUrl: `http://127.0.0.1:${port}` });
      const result = await client.spawn("hello world");
      assert.equal(requests.length, 1);
      assert.equal(requests[0].method, "POST");
      assert.equal(requests[0].url, "/api/sessions/spawn");
      const body = JSON.parse(requests[0].body);
      assert.equal(body.task, "hello world");
      assert.equal(body.mode, "run");
      assert.equal(body.runtime, "subagent");
      assert.equal("timeoutSeconds" in body, false);
      // object response is stringified for the node-return contract
      assert.equal(result, '{"ok":true}');
    } finally {
      server.close();
    }
  });

  it("sends Bearer auth only when apiKey is provided", async () => {
    const { server, port, requests } = await startCaptureServer((req, res) =>
      jsonResponse(res, 200, {})
    );
    try {
      const bare = new OpenClawClient({ baseUrl: `http://127.0.0.1:${port}` });
      await bare.spawn("t1");
      assert.equal("authorization" in requests[0].headers, false);

      const keyed = new OpenClawClient({
        baseUrl: `http://127.0.0.1:${port}`,
        apiKey: "secret-key",
      });
      await keyed.spawn("t2");
      assert.equal(requests[1].headers.authorization, "Bearer secret-key");
    } finally {
      server.close();
    }
  });

  it("strips trailing slash from baseUrl", async () => {
    const { server, port, requests } = await startCaptureServer((req, res) =>
      jsonResponse(res, 200, {})
    );
    try {
      const client = new OpenClawClient({ baseUrl: `http://127.0.0.1:${port}/` });
      await client.spawn("t");
      assert.equal(requests[0].url, "/api/sessions/spawn");
    } finally {
      server.close();
    }
  });

  it("passes through explicit mode/runtime/timeoutSeconds options", async () => {
    const { server, port, requests } = await startCaptureServer((req, res) =>
      jsonResponse(res, 200, {})
    );
    try {
      const client = new OpenClawClient({ baseUrl: `http://127.0.0.1:${port}` });
      await client.spawn("t", { mode: "session", runtime: "acp", timeoutSeconds: 5 });
      const body = JSON.parse(requests[0].body);
      assert.equal(body.mode, "session");
      assert.equal(body.runtime, "acp");
      assert.equal(body.timeoutSeconds, 5);
    } finally {
      server.close();
    }
  });

  it("passes timeoutSeconds: 0 through instead of dropping it", async () => {
    const { server, port, requests } = await startCaptureServer((req, res) =>
      jsonResponse(res, 200, {})
    );
    try {
      const client = new OpenClawClient({ baseUrl: `http://127.0.0.1:${port}` });
      await client.spawn("t", { timeoutSeconds: 0 });
      const body = JSON.parse(requests[0].body);
      assert.equal(body.timeoutSeconds, 0);
    } finally {
      server.close();
    }
  });

  it("JSON string response is returned as-is, not double-encoded", async () => {
    const { server, port } = await startCaptureServer((req, res) =>
      jsonResponse(res, 200, JSON.stringify("done"))
    );
    try {
      const client = new OpenClawClient({ baseUrl: `http://127.0.0.1:${port}` });
      assert.equal(await client.spawn("t"), "done");
    } finally {
      server.close();
    }
  });
});

describe("OpenClawClient.executor", () => {
  it("prepends systemPrompt separated by a blank line", async () => {
    const { server, port, requests } = await startCaptureServer((req, res) =>
      jsonResponse(res, 200, {})
    );
    try {
      const client = new OpenClawClient({ baseUrl: `http://127.0.0.1:${port}` });
      await client.executor("SYSTEM PROMPT")("user task");
      assert.equal(JSON.parse(requests[0].body).task, "SYSTEM PROMPT\n\nuser task");

      await client.executor()("plain task");
      assert.equal(JSON.parse(requests[1].body).task, "plain task");
    } finally {
      server.close();
    }
  });
});

// ── spawn(): error surfaces ────────────────────────────

describe("OpenClawClient.spawn error surfaces", () => {
  it("non-ok status throws with status code and response body", async () => {
    const { server, port } = await startCaptureServer((req, res) =>
      jsonResponse(res, 418, "teapot detected")
    );
    try {
      const client = new OpenClawClient({ baseUrl: `http://127.0.0.1:${port}` });
      await assert.rejects(
        () => client.spawn("t"),
        (err) =>
          err instanceof Error &&
          err.message.includes("418") &&
          err.message.includes("teapot detected")
      );
    } finally {
      server.close();
    }
  });

  it("200 with non-JSON body throws a diagnostic error, not a raw SyntaxError", async () => {
    const { server, port } = await startCaptureServer((req, res) => {
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end("<html>proxy error page</html>");
    });
    try {
      const client = new OpenClawClient({ baseUrl: `http://127.0.0.1:${port}` });
      await assert.rejects(
        () => client.spawn("t"),
        (err) =>
          err instanceof Error &&
          err.message.startsWith("OpenClaw spawn failed") &&
          err.message.includes("invalid JSON") &&
          err.message.includes("proxy error page")
      );
    } finally {
      server.close();
    }
  });

  it("connection refused produces an error naming the gateway baseUrl", async () => {
    // grab a free port, then release it so nothing listens there
    const probe = http.createServer();
    const port = await new Promise((resolve) =>
      probe.listen(0, "127.0.0.1", () => resolve(probe.address().port))
    );
    await new Promise((resolve) => probe.close(resolve));

    const client = new OpenClawClient({ baseUrl: `http://127.0.0.1:${port}` });
    await assert.rejects(
      () => client.spawn("t"),
      (err) =>
        err instanceof Error &&
        err.message.includes("cannot reach gateway") &&
        err.message.includes(`http://127.0.0.1:${port}`)
    );
  });
});

// ── AgentPool / Orchestrator previously-uncovered paths ─

describe("AgentPool.createNode retry wrapping", () => {
  it("wraps the node with retry when role.config.retry is set", async () => {
    let calls = 0;
    const pool = new AgentPool({
      roles: [
        {
          id: "flaky",
          description: "fails once",
          capabilities: ["do"],
          config: {
            name: "flaky",
            systemPrompt: "x",
            executor: async () => {
              calls += 1;
              if (calls === 1) throw new Error("transient");
              return "recovered";
            },
            retry: { maxAttempts: 3, baseDelayMs: 1 },
          },
        },
      ],
    });
    const node = pool.createNode("flaky");
    const out = await node({});
    // output key defaults to `${name}Result` (create-node.ts contract)
    assert.equal(out.flakyResult, "recovered");
    assert.equal(calls, 2);
  });

  it("returns an unwrapped node when no retry config is present", async () => {
    let calls = 0;
    const pool = new AgentPool({
      roles: [
        {
          id: "plain",
          description: "no retry",
          capabilities: ["do"],
          config: {
            name: "plain",
            systemPrompt: "x",
            executor: async () => {
              calls += 1;
              throw new Error("boom");
            },
          },
        },
      ],
    });
    await assert.rejects(() => pool.createNode("plain")({}), /boom/);
    assert.equal(calls, 1); // no retry happened
  });
});

describe("Orchestrator dependency handling", () => {
  const makePool = (behavior) =>
    new AgentPool({
      roles: [
        {
          id: "worker",
          description: "worker",
          capabilities: [...Object.keys(behavior ?? {}), "do"],
          config: {
            name: "worker",
            systemPrompt: "x",
            executor: async (task) =>
              behavior && behavior[task] ? behavior[task](task) : `did:${task}`,
          },
        },
      ],
    });

  it("marks tasks in a dependency cycle as failures without hanging", async () => {
    const orch = new Orchestrator(makePool());
    const result = await orch.run([
      { id: "a", type: "do", description: "a", dependsOn: ["b"] },
      { id: "b", type: "do", description: "b", dependsOn: ["a"] },
    ]);
    assert.deepEqual(result.stats, { total: 2, passed: 0, failed: 2 });
    for (const entry of result.log) {
      assert.equal(entry.status, "failure");
      assert.equal(entry.agent, "none");
    }
  });

  it("runs a dependent task even when its dependency failed (best-effort, pinned)", async () => {
    const orch = new Orchestrator(
      makePool({ "will fail": () => { throw new Error("upstream blew up"); } })
    );
    const result = await orch.run([
      { id: "up", type: "failtype", description: "will fail" },
      { id: "down", type: "do", description: "runs anyway", dependsOn: ["up"] },
    ]);
    assert.equal(result.stats.failed, 1);
    assert.equal(result.stats.passed, 1);
    const down = result.log.find((l) => l.task === "down");
    assert.equal(down.status, "success"); // pinned: no input flows between tasks, so this is safe today
  });
});
