import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { aggregate, mergeAll, collectAll } from "../dist/aggregate.js";

describe("aggregate", () => {
  it("reduces partials with custom reducer", () => {
    const sumValues = aggregate((acc, partial) => ({
      total: (acc.total || 0) + (partial.v || 0),
    }));

    const result = sumValues([{ v: 1 }, { v: 2 }, { v: 3 }]);
    assert.deepEqual(result, { total: 6 });
  });

  it("passes index to reducer", () => {
    const withIndex = aggregate((acc, _partial, i) => ({
      indices: [...((acc.indices || [])), i],
    }));

    const result = withIndex([{}, {}, {}]);
    assert.deepEqual(result, { indices: [0, 1, 2] });
  });

  it("throws on non-array input", () => {
    const agg = aggregate((a, b) => ({ ...a, ...b }));
    assert.throws(() => agg({}), /expected array/);
  });

  it("empty array returns empty object", () => {
    const agg = aggregate((a, b) => ({ ...a, ...b }));
    assert.deepEqual(agg([]), {});
  });
});

describe("mergeAll", () => {
  it("merges partials last-write-wins", () => {
    const merge = mergeAll();
    const result = merge([{ a: 1 }, { b: 2 }, { a: 3 }]);
    assert.deepEqual(result, { a: 3, b: 2 });
  });

  it("empty array returns empty object", () => {
    assert.deepEqual(mergeAll()([]), {});
  });
});

describe("collectAll", () => {
  it("collects values into arrays per key", () => {
    const collect = collectAll();
    const result = collect([{ a: 1 }, { a: 2, b: 3 }]);
    assert.deepEqual(result, { a: [1, 2], b: [undefined, 3] });
  });

  it("throws on non-array input", () => {
    assert.throws(() => collectAll()({}), /expected array/);
  });

  it("empty array returns empty object", () => {
    assert.deepEqual(collectAll()([]), {});
  });
});
