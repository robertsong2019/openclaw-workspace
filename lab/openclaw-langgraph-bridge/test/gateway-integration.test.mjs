/**
 * Gateway integration tests — real local HTTP server (node:http), no fetch mocking.
 *
 * Covers OpenClawClient.health() and end-to-end spawn() through a real socket,
 * complementing the mocked-fetch unit tests in openclaw-client.test.mjs.
 *
 * Endpoint contract mirrors the real OpenClaw gateway:
 * GET /healthz -> 200 {ok: true, status: "live"}
 */
import { test, describe, beforeEach, afterEach } from "node:test";
import assert from "node:assert/strict";
import http from "node:http";
import { OpenClawClient } from "../dist/openclaw-client.js";

let server;
let baseUrl;
let handler; // per-test request handler

function startServer() {
  return new Promise((resolve) => {
    server = http.createServer((req, res) => {
      Promise.resolve(handler(req, res)).catch((err) => {
        res.writeHead(500, { "Content-Type": "text/plain" });
        res.end(String(err));
      });
    });
    server.listen(0, "127.0.0.1", () => {
      baseUrl = `http://127.0.0.1:${server.address().port}`;
      resolve();
    });
  });
}

beforeEach(() => startServer());
afterEach(() => new Promise((resolve) => server.close(resolve)));

function readBody(req) {
  return new Promise((resolve) => {
    let data = "";
    req.on("data", (c) => (data += c));
    req.on("end", () => resolve(data));
  });
}

describe("OpenClawClient.health() against a real server", () => {
  test("ok: 200 {ok:true,status:'live'} -> status ok, gatewayStatus preserved", async () => {
    handler = (req, res) => {
      assert.equal(req.method, "GET");
      assert.equal(req.url, "/healthz");
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: true, status: "live" }));
    };
    const result = await new OpenClawClient({ baseUrl }).health();
    assert.equal(result.status, "ok");
    assert.equal(result.httpStatus, 200);
    assert.equal(result.ok, true);
    assert.equal(result.gatewayStatus, "live");
  });

  test("down: unreachable host -> status down with reason", async () => {
    const result = await new OpenClawClient({ baseUrl: "http://127.0.0.1:1" }).health({ timeoutMs: 1000 });
    assert.equal(result.status, "down");
    assert.ok(result.reason, "reason must be present when down");
  });

  test("down: HTTP 500 -> httpStatus surfaced", async () => {
    handler = (req, res) => {
      res.writeHead(500, { "Content-Type": "text/plain" });
      res.end("boom");
    };
    const result = await new OpenClawClient({ baseUrl }).health();
    assert.equal(result.status, "down");
    assert.equal(result.httpStatus, 500);
    assert.match(result.reason, /500|boom/);
  });

  test("down: 2xx non-JSON body (proxy hijack) -> invalid JSON reason", async () => {
    handler = (req, res) => {
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end("<html>login page</html>");
    };
    const result = await new OpenClawClient({ baseUrl }).health();
    assert.equal(result.status, "down");
    assert.match(result.reason, /invalid JSON/i);
    assert.match(result.reason, /<html>/);
  });

  test("down: gateway self-reports ok:false -> down, gatewayStatus preserved", async () => {
    handler = (req, res) => {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: false, status: "degraded" }));
    };
    const result = await new OpenClawClient({ baseUrl }).health();
    assert.equal(result.status, "down");
    assert.equal(result.gatewayStatus, "degraded");
  });

  test("down: slow server exceeds timeoutMs (default budget must not hang)", async () => {
    handler = () => {}; // never responds
    const result = await new OpenClawClient({ baseUrl }).health({ timeoutMs: 120 });
    assert.equal(result.status, "down");
    assert.match(result.reason, /timed out|timeout|abort/i);
  });
});

describe("OpenClawClient.spawn() end-to-end through a real socket", () => {
  test("happy path: string result, Authorization header arrives, body shape correct", async () => {
    handler = async (req, res) => {
      assert.equal(req.method, "POST");
      assert.equal(req.url, "/api/sessions/spawn");
      assert.equal(req.headers.authorization, "Bearer sk-test");
      const body = JSON.parse(await readBody(req));
      assert.equal(body.task, "do the thing");
      assert.equal(body.mode, "session");
      assert.equal(body.timeoutSeconds, 0); // explicit zero must survive
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify("agent says hi"));
    };
    const client = new OpenClawClient({ baseUrl, apiKey: "sk-test" });
    const out = await client.spawn("do the thing", { mode: "session", timeoutSeconds: 0 });
    assert.equal(out, "agent says hi");
  });

  test("error path: 502 from real server -> throw with status and body", async () => {
    handler = (req, res) => {
      res.writeHead(502, { "Content-Type": "text/plain" });
      res.end("bad gateway");
    };
    await assert.rejects(
      new OpenClawClient({ baseUrl }).spawn("x"),
      /502[\s\S]*bad gateway/
    );
  });
});
