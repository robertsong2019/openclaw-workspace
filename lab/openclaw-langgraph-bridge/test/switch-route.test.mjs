import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { switchRoute } from "../dist/switch-route.js";

describe("switchRoute", () => {
  it("matches string value to route", () => {
    const router = switchRoute({
      field: "type",
      cases: [
        { match: "urgent", route: "priorityHandler" },
        { match: "normal", route: "standardHandler" },
      ],
    });
    assert.equal(router({ type: "urgent" }), "priorityHandler");
    assert.equal(router({ type: "normal" }), "standardHandler");
  });

  it("returns default when no match", () => {
    const router = switchRoute({
      field: "status",
      cases: [{ match: "ready", route: "executor" }],
    });
    assert.equal(router({ status: "pending" }), "__end__");
  });

  it("supports custom default route", () => {
    const router = switchRoute({
      field: "x",
      cases: [],
      default: "fallback",
    });
    assert.equal(router({ x: 1 }), "fallback");
  });

  it("first match wins for overlapping cases", () => {
    const router = switchRoute({
      field: "val",
      cases: [
        { match: "a", route: "first" },
        { match: "a", route: "second" },
      ],
    });
    assert.equal(router({ val: "a" }), "first");
  });

  it("supports predicate matchers", () => {
    const router = switchRoute({
      field: "score",
      cases: [
        { match: (v) => v >= 90, route: "high" },
        { match: (v) => v >= 50, route: "medium" },
        { match: (v) => v < 50, route: "low" },
      ],
    });
    assert.equal(router({ score: 95 }), "high");
    assert.equal(router({ score: 60 }), "medium");
    assert.equal(router({ score: 20 }), "low");
  });

  it("predicate receives full state", () => {
    const router = switchRoute({
      field: "action",
      cases: [
        {
          match: (v, state) => v === "go" && state.enabled === true,
          route: "proceed",
        },
      ],
    });
    assert.equal(router({ action: "go", enabled: true }), "proceed");
    assert.equal(router({ action: "go", enabled: false }), "__end__");
  });

  it("handles missing field gracefully", () => {
    const router = switchRoute({
      field: "missing",
      cases: [{ match: "x", route: "y" }],
      default: "safe",
    });
    assert.equal(router({}), "safe");
  });

  it("handles undefined field value", () => {
    const router = switchRoute({
      field: "val",
      cases: [{ match: undefined, route: "undef" }],
      default: "other",
    });
    assert.equal(router({ val: undefined }), "undef");
    assert.equal(router({ val: "something" }), "other");
  });
});
