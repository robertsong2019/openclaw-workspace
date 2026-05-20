import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { partition, splitBy } from "../dist/partition.js";

describe("partition", () => {
  it("returns matching branches with full state", () => {
    const p = partition({
      branches: {
        high: { when: (s) => s.priority === "high" },
        low: { when: (s) => s.priority === "low" },
      },
    });
    const result = p({ priority: "high", data: 42 });
    assert.ok(result.high);
    assert.strictEqual(result.low, undefined);
    assert.strictEqual(result.high.data, 42);
  });

  it("returns multiple matching branches", () => {
    const p = partition({
      branches: {
        a: { when: (s) => s.x > 0 },
        b: { when: (s) => s.x < 10 },
      },
    });
    const result = p({ x: 5 });
    assert.ok(result.a);
    assert.ok(result.b);
  });

  it("applies select transform to matching branches", () => {
    const p = partition({
      branches: {
        summary: {
          when: (s) => s.type === "report",
          select: (s) => ({ title: s.title }),
        },
      },
    });
    const result = p({ type: "report", title: "Q1", body: "long text" });
    assert.deepStrictEqual(result.summary, { title: "Q1" });
  });

  it("returns defaultResult when no branch matches", () => {
    const p = partition({
      branches: {
        a: { when: (s) => s.x === 1 },
      },
      defaultResult: { fallback: true },
    });
    const result = p({ x: 99 });
    assert.deepStrictEqual(result._default, { fallback: true });
  });

  it("returns empty object when nothing matches and no default", () => {
    const p = partition({
      branches: { a: { when: () => false } },
    });
    const result = p({ x: 1 });
    assert.deepStrictEqual(result, {});
  });
});

describe("splitBy", () => {
  it("splits array field by predicate", () => {
    const sp = splitBy("items", (n) => n > 5);
    const result = sp({ items: [1, 6, 3, 8, 2, 10] });
    assert.deepStrictEqual(result.match, [6, 8, 10]);
    assert.deepStrictEqual(result.rest, [1, 3, 2]);
  });

  it("handles missing field as empty", () => {
    const sp = splitBy("missing", (n) => n > 0);
    const result = sp({ other: 1 });
    assert.deepStrictEqual(result.match, []);
    assert.deepStrictEqual(result.rest, []);
  });

  it("handles non-array field as empty", () => {
    const sp = splitBy("notarray", () => true);
    const result = sp({ notarray: "string" });
    assert.deepStrictEqual(result.match, []);
    assert.deepStrictEqual(result.rest, []);
  });
});
