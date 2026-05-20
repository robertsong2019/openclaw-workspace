import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { seal, isSealed, unseal } from "../dist/seal.js";

describe("seal", () => {
  it("returns frozen state", async () => {
    const node = async () => ({ x: 1, y: "hello" });
    const sealed = seal(node);
    const result = await sealed({});
    assert.strictEqual(Object.isFrozen(result), true);
  });

  it("preserves node output values", async () => {
    const node = async (s) => ({ ...s, added: 42 });
    const sealed = seal(node);
    const result = await sealed({ input: "test" });
    assert.strictEqual(result.input, "test");
    assert.strictEqual(result.added, 42);
  });

  it("prevents mutation of sealed output", async () => {
    const node = async () => ({ count: 0 });
    const sealed = seal(node);
    const result = await sealed({});
    assert.throws(() => { result.count = 99; }, /read only|Cannot assign/i);
    assert.strictEqual(result.count, 0);
  });

  it("detectMutations fires onChange", async () => {
    const mutations = [];
    const node = async () => ({ x: 1 });
    const sealed = seal(node, {
      detectMutations: true,
      onChange: (key, value, old) => mutations.push({ key, value, old }),
    });
    const result = await sealed({});
    assert.throws(() => { result.x = 99; }, /falsish|trap/i);
    assert.strictEqual(mutations.length, 1);
    assert.strictEqual(mutations[0].key, "x");
    assert.strictEqual(mutations[0].value, 99);
    assert.strictEqual(mutations[0].old, 1);
  });
});

describe("isSealed", () => {
  it("returns true for frozen objects", () => {
    assert.strictEqual(isSealed(Object.freeze({})), true);
  });

  it("returns false for regular objects", () => {
    assert.strictEqual(isSealed({}), false);
  });
});

describe("unseal", () => {
  it("creates writable copy of frozen state", async () => {
    const node = async () => ({ x: 1 });
    const sealed = seal(node);
    const frozen = await sealed({});
    const writable = unseal(frozen);
    writable.x = 42;
    assert.strictEqual(writable.x, 42);
    assert.strictEqual(frozen.x, 1); // original unchanged
  });
});
