import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { pick, omit, rename, defaults, compose } from "../dist/transform.js";

describe("transform", () => {
  describe("pick", () => {
    it("picks specified fields", () => {
      const result = pick("a", "c")({ a: 1, b: 2, c: 3 });
      assert.deepEqual(result, { a: 1, c: 3 });
    });

    it("ignores missing fields", () => {
      const result = pick("x", "y")({ a: 1 });
      assert.deepEqual(result, {});
    });

    it("picks with undefined value", () => {
      const result = pick("a")({ a: undefined });
      assert.deepEqual(result, { a: undefined });
    });
  });

  describe("omit", () => {
    it("omits specified fields", () => {
      const result = omit("b")({ a: 1, b: 2, c: 3 });
      assert.deepEqual(result, { a: 1, c: 3 });
    });

    it("handles omitting non-existent fields", () => {
      const result = omit("x")({ a: 1 });
      assert.deepEqual(result, { a: 1 });
    });
  });

  describe("rename", () => {
    it("renames fields", () => {
      const result = rename({ old: "new" })({ old: 1, keep: 2 });
      assert.deepEqual(result, { new: 1, keep: 2 });
    });

    it("skips missing source fields", () => {
      const result = rename({ missing: "x" })({ a: 1 });
      assert.deepEqual(result, { a: 1 });
    });
  });

  describe("defaults", () => {
    it("fills missing fields", () => {
      const result = defaults({ x: 0, y: 0 })({ x: 5 });
      assert.deepEqual(result, { x: 5, y: 0 });
    });

    it("does not override existing values", () => {
      const result = defaults({ a: "default" })({ a: "existing" });
      assert.equal(result.a, "existing");
    });

    it("overrides undefined values", () => {
      const result = defaults({ a: "filled" })({ a: undefined });
      assert.equal(result.a, "filled");
    });
  });

  describe("compose", () => {
    it("chains transforms left to right", () => {
      const t = compose(
        pick("a", "b"),
        rename({ a: "alpha" }),
        defaults({ c: 0 })
      );
      const result = t({ a: 1, b: 2, d: 99 });
      assert.deepEqual(result, { alpha: 1, b: 2, c: 0 });
    });

    it("empty compose returns copy of state", () => {
      const t = compose();
      const state = { x: 1 };
      const result = t(state);
      assert.deepEqual(result, { x: 1 });
      assert.notEqual(result, state);
    });
  });
});
