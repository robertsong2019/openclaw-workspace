// Session cap: MAX_SESSIONS bounds concurrent sessions (DoS guard).
//initialize flood otherwise creates unbounded McpServer+transport pairs —
// a real memory/leak vector on a small box (sibling of the 09-09 hardening:
// crash guard / 1MB cap / TTL reaper). Default (env unset) stays unlimited.
import { describe, it, before, after } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";

const PORT = 3199;
const BASE = `http://localhost:${PORT}`;
let serverProc;

const HEADERS = {
  "Content-Type": "application/json",
  Accept: "application/json, text/event-stream",
};

async function post(body, sessionId) {
  const headers = { ...HEADERS };
  if (sessionId) headers["Mcp-Session-Id"] = sessionId;
  return fetch(BASE, { method: "POST", headers, body });
}

async function init(clientName) {
  const res = await post(JSON.stringify({
    jsonrpc: "2.0", id: 1, method: "initialize",
    params: {
      protocolVersion: "2025-06-18", capabilities: {},
      clientInfo: { name: clientName, version: "1.0.0" },
    },
  }));
  return { status: res.status, sid: res.headers.get("mcp-session-id"), body: await res.text() };
}

async function listTools(sessionId) {
  const res = await post(JSON.stringify({
    jsonrpc: "2.0", id: 2, method: "tools/list", params: {},
  }), sessionId);
  assert.equal(res.status, 200, `tools/list must succeed, got ${res.status}`);
  const text = await res.text();
  let envelope;
  for (const line of text.split("\n")) {
    if (line.startsWith("data: ")) { envelope = JSON.parse(line.slice(6)); break; }
  }
  return envelope ?? JSON.parse(text);
}

before(async () => {
  serverProc = spawn("node", ["dist/index.js"], {
    env: { ...process.env, PORT: String(PORT), MAX_SESSIONS: "2", SESSION_TTL_MS: "3600000" },
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
    serverProc.on("error", (err) => { clearTimeout(timeout); reject(err); });
  });
});

after(() => {
  serverProc?.kill();
});

describe("session cap (MAX_SESSIONS)", () => {
  it("fills capacity up to the limit", async () => {
    const a = await init("client-A");
    assert.equal(a.status, 200, `first init must succeed: ${a.body}`);
    const b = await init("client-B");
    assert.equal(b.status, 200, `second init must succeed: ${b.body}`);
    globalThis.__capSids = [a.sid, b.sid];
  });

  it("initialize beyond capacity is rejected with 503, no session minted", async () => {
    const c = await init("client-C");
    assert.equal(c.status, 503, `expected 503, got ${c.status}: ${c.body}`);
    assert.equal(c.sid, null, "rejected init must not mint a session id");
    const parsed = JSON.parse(c.body);
    assert.equal(parsed.error.code, -32000);
    assert.match(parsed.error.message, /capacity/i);
  });

  it("existing sessions stay fully usable while at capacity", async () => {
    for (const sid of globalThis.__capSids) {
      const r = await listTools(sid);
      assert.ok(Array.isArray(r.result?.tools) && r.result.tools.length === 3,
        "tools/list must return 3 tools");
    }
  });

  it("freeing a slot (DELETE) admits a new session", async () => {
    const del = await fetch(BASE, {
      method: "DELETE", headers: { ...HEADERS, "Mcp-Session-Id": globalThis.__capSids[0] },
    });
    assert.ok(del.status === 200 || del.status === 405, `DELETE should close, got ${del.status}`);
    const c2 = await init("client-C2");
    assert.equal(c2.status, 200, `init after freeing a slot must succeed: ${c2.body}`);
    globalThis.__capSids[0] = c2.sid;
  });

  it("server is still healthy after cap churn", async () => {
    const r = await listTools(globalThis.__capSids[1]);
    assert.ok(r.result?.tools?.length === 3);
  });
});
