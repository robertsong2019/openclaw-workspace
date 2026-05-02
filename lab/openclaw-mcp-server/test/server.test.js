import { describe, it, before, after } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";

const BASE = "http://localhost:3199";
let serverProc;
let sessionId = null;

// Parse SSE response: extract JSON-RPC result from SSE stream
async function parseSSE(response) {
  const text = await response.text();
  // SSE format: "event: message\ndata: {...}\n\n"
  const lines = text.split("\n");
  for (const line of lines) {
    if (line.startsWith("data: ")) {
      return JSON.parse(line.slice(6));
    }
  }
  // Fallback: might be plain JSON
  return JSON.parse(text);
}

// Send JSON-RPC, auto-attach session if available
async function rpc(method, params = {}, id = 1) {
  const headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
  };
  if (sessionId) {
    headers["Mcp-Session-Id"] = sessionId;
  }
  const res = await fetch(BASE, {
    method: "POST",
    headers,
    body: JSON.stringify({ jsonrpc: "2.0", id, method, params }),
  });
  // Capture session from init response
  const sid = res.headers.get("mcp-session-id");
  if (sid) sessionId = sid;
  return res;
}

before(async () => {
  serverProc = spawn("node", ["dist/index.js"], {
    env: { ...process.env, PORT: "3199" },
    stdio: ["pipe", "pipe", "pipe"],
  });
  await new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error("Server startup timeout")), 5000);
    serverProc.stdout.on("data", (data) => {
      if (data.toString().includes("OpenClaw MCP Server running")) {
        clearTimeout(timeout);
        resolve();
      }
    });
    serverProc.on("error", (err) => {
      clearTimeout(timeout);
      reject(err);
    });
  });
});

after(() => {
  serverProc?.kill();
});

describe("OpenClaw MCP Server", () => {
  it("initializes and returns server info", async () => {
    const res = await rpc("initialize", {
      protocolVersion: "2025-06-18",
      capabilities: {},
      clientInfo: { name: "test-client", version: "1.0.0" },
    });
    assert.ok(res.status === 200 || res.status === 201, `Expected 200/201, got ${res.status}`);
    assert.ok(sessionId, "Should have session ID after init");
    const body = await parseSSE(res);
    assert.equal(body.jsonrpc, "2.0");
    assert.ok(body.result);
    assert.equal(body.result.serverInfo.name, "openclaw-mcp-server");
  });

  it("lists 3 tools", async () => {
    const res = await rpc("tools/list", {});
    assert.equal(res.status, 200, `Expected 200, got ${res.status}`);
    const body = await parseSSE(res);
    assert.ok(body.result);
    assert.equal(body.result.tools.length, 3);
    const names = body.result.tools.map(t => t.name).sort();
    assert.deepEqual(names, ["get_status", "query_memory", "web_search"]);
  });

  it("calls get_status tool", async () => {
    const res = await rpc("tools/call", { name: "get_status", arguments: {} });
    assert.equal(res.status, 200);
    const body = await parseSSE(res);
    assert.ok(body.result);
    const text = body.result.content[0].text;
    assert.ok(text.includes("ams"));
    assert.ok(text.includes("640/640"));
  });

  it("calls query_memory with limit", async () => {
    const res = await rpc("tools/call", {
      name: "query_memory",
      arguments: { query: "test", limit: 2 },
    });
    assert.equal(res.status, 200);
    const body = await parseSSE(res);
    assert.ok(body.result);
    assert.equal(body.result.content.length, 2);
  });

  it("calls web_search tool", async () => {
    const res = await rpc("tools/call", {
      name: "web_search",
      arguments: { query: "MCP protocol" },
    });
    assert.equal(res.status, 200);
    const body = await parseSSE(res);
    assert.ok(body.result);
    assert.ok(body.result.content[0].text.includes("MCP protocol"));
  });
});
