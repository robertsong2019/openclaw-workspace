import { describe, it, before, after } from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { join } from "node:path";

let toolHandlers;

before(async () => {
  const mod = await import("../dist/tools.js");
  toolHandlers = mod.toolHandlers;
});

const TMP = join(import.meta.dirname, "__head_tail_test__");

before(() => {
  mkdirSync(TMP, { recursive: true });
  writeFileSync(join(TMP, "sample.txt"), Array.from({ length: 20 }, (_, i) => `line ${i + 1}`).join("\n"));
  writeFileSync(join(TMP, "short.txt"), "a\nb\nc");
});

after(() => { rmSync(TMP, { recursive: true, force: true }); });

describe("head tool", () => {
  it("returns first 10 lines by default", async () => {
    const res = await toolHandlers.head({ path: join(TMP, "sample.txt") });
    assert.equal(res.tool, "head");
    assert.equal(res.requestedLines, 10);
    assert.equal(res.totalLines, 20);
    assert.equal(res.returnedLines, 10);
    const lines = res.content.split("\n");
    assert.equal(lines[0], "line 1");
    assert.equal(lines[9], "line 10");
  });

  it("returns first N lines when lines specified", async () => {
    const res = await toolHandlers.head({ path: join(TMP, "sample.txt"), lines: 5 });
    assert.equal(res.returnedLines, 5);
    assert.equal(res.totalLines, 20);
    const lines = res.content.split("\n");
    assert.equal(lines.length, 5);
    assert.equal(lines[4], "line 5");
  });

  it("handles file shorter than requested lines", async () => {
    const res = await toolHandlers.head({ path: join(TMP, "short.txt"), lines: 10 });
    assert.equal(res.totalLines, 3);
    assert.equal(res.returnedLines, 3);
    assert.equal(res.content, "a\nb\nc");
  });

  it("returns single line when lines=1", async () => {
    const res = await toolHandlers.head({ path: join(TMP, "sample.txt"), lines: 1 });
    assert.equal(res.returnedLines, 1);
    assert.equal(res.content, "line 1");
  });
});

describe("tail tool", () => {
  it("returns last 10 lines by default", async () => {
    const res = await toolHandlers.tail({ path: join(TMP, "sample.txt") });
    assert.equal(res.tool, "tail");
    assert.equal(res.requestedLines, 10);
    assert.equal(res.totalLines, 20);
    assert.equal(res.returnedLines, 10);
    const lines = res.content.split("\n");
    assert.equal(lines[0], "line 11");
    assert.equal(lines[9], "line 20");
  });

  it("returns last N lines when lines specified", async () => {
    const res = await toolHandlers.tail({ path: join(TMP, "sample.txt"), lines: 3 });
    assert.equal(res.returnedLines, 3);
    const lines = res.content.split("\n");
    assert.equal(lines[0], "line 18");
    assert.equal(lines[2], "line 20");
  });

  it("handles file shorter than requested lines", async () => {
    const res = await toolHandlers.tail({ path: join(TMP, "short.txt"), lines: 10 });
    assert.equal(res.totalLines, 3);
    assert.equal(res.returnedLines, 3);
    assert.equal(res.content, "a\nb\nc");
  });

  it("returns single line when lines=1", async () => {
    const res = await toolHandlers.tail({ path: join(TMP, "sample.txt"), lines: 1 });
    assert.equal(res.returnedLines, 1);
    assert.equal(res.content, "line 20");
  });
});
