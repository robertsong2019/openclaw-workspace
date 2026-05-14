import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { withMiddleware } from "../dist/middleware.js";

const baseNode = async (state) => ({ ...state, base: true });

describe("withMiddleware", () => {
  it("returns node result when no middleware", async () => {
    const wrapped = withMiddleware(baseNode, []);
    const result = await wrapped({ input: "hello" });
    assert.deepEqual(result, { input: "hello", base: true });
  });

  it("applies single middleware", async () => {
    const addTs = async (next, state) => {
      const result = await next(state);
      return { ...result, ts: 12345 };
    };
    const wrapped = withMiddleware(baseNode, [addTs]);
    const result = await wrapped({ x: 1 });
    assert.deepEqual(result, { x: 1, base: true, ts: 12345 });
  });

  it("applies middleware left-to-right (outer first)", async () => {
    const order = [];
    const mw1 = async (next, state) => {
      order.push("mw1-before");
      const result = await next(state);
      order.push("mw1-after");
      return { ...result, mw1: true };
    };
    const mw2 = async (next, state) => {
      order.push("mw2-before");
      const result = await next(state);
      order.push("mw2-after");
      return { ...result, mw2: true };
    };
    const wrapped = withMiddleware(baseNode, [mw1, mw2]);
    const result = await wrapped({});

    assert.equal(result.mw1, true);
    assert.equal(result.mw2, true);
    assert.equal(result.base, true);
    assert.deepEqual(order, [
      "mw1-before", "mw2-before", "mw2-after", "mw1-after",
    ]);
  });

  it("middleware can modify state before calling next", async () => {
    const inject = async (next, state) => next({ ...state, injected: 42 });
    const node = async (state) => ({ ...state, got: state.injected });
    const wrapped = withMiddleware(node, [inject]);
    const result = await wrapped({});
    assert.equal(result.got, 42);
  });

  it("middleware can short-circuit without calling next", async () => {
    const guard = async (next, state) => {
      if (state.blocked) return { blocked: true, shortCircuited: true };
      return next(state);
    };
    const wrapped = withMiddleware(baseNode, [guard]);

    const blocked = await wrapped({ blocked: true });
    assert.equal(blocked.shortCircuited, true);
    assert.equal(blocked.base, undefined);

    const passed = await wrapped({ blocked: false });
    assert.equal(passed.base, true);
    assert.equal(passed.shortCircuited, undefined);
  });

  it("composes with retry-like pattern", async () => {
    let attempts = 0;
    const retryMw = async (next, state) => {
      for (let i = 0; i < 3; i++) {
        try {
          return await next(state);
        } catch {
          attempts++;
        }
      }
      throw new Error("all retries exhausted");
    };
    const failNode = async () => { throw new Error("fail"); };
    const wrapped = withMiddleware(failNode, [retryMw]);

    await assert.rejects(() => wrapped({}), { message: "all retries exhausted" });
    assert.equal(attempts, 3);
  });

  it("composes three middleware in correct order", async () => {
    const log = [];
    const mw = (name) => async (next, state) => {
      log.push(`${name}-in`);
      const r = await next(state);
      log.push(`${name}-out`);
      return { ...r, [name]: true };
    };
    const wrapped = withMiddleware(baseNode, [mw("a"), mw("b"), mw("c")]);
    const result = await wrapped({});

    assert.equal(result.a, true);
    assert.equal(result.b, true);
    assert.equal(result.c, true);
    assert.equal(result.base, true);
    assert.deepEqual(log, ["a-in", "b-in", "c-in", "c-out", "b-out", "a-out"]);
  });

  it("preserves state fields from node and all middleware", async () => {
    const m1 = async (next, state) => ({ ...(await next(state)), m1: "yes" });
    const m2 = async (next, state) => ({ ...(await next(state)), m2: 99 });
    const node = async (s) => ({ ...s, node: "ok" });
    const wrapped = withMiddleware(node, [m1, m2]);
    const result = await wrapped({ orig: 1 });

    assert.equal(result.orig, 1);
    assert.equal(result.node, "ok");
    assert.equal(result.m1, "yes");
    assert.equal(result.m2, 99);
  });
});
