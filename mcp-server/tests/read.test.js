import { describe, it, before, after } from "node:test";
import assert from "node:assert/strict";
import { mkdir, writeFile, rm } from "node:fs/promises";
import { join } from "node:path";
import { toolHandlers, safePath } from "../dist/tools.js";

const TEST_DIR = join(process.cwd(), ".test-read");
const read = toolHandlers.read;

describe("read tool", () => {
  before(async () => {
    await mkdir(TEST_DIR, { recursive: true });
  });

  after(async () => {
    await rm(TEST_DIR, { recursive: true, force: true });
  });

  it("should read entire file content", async () => {
    const f = join(TEST_DIR, "full.txt");
    await writeFile(f, "hello\nworld\nfoo");
    const r = await read({ path: f });
    assert.equal(r.tool, "read");
    assert.equal(r.content, "hello\nworld\nfoo");
    assert.equal(r.lines, 3);
  });

  it("should read with offset (1-indexed)", async () => {
    const f = join(TEST_DIR, "offset.txt");
    await writeFile(f, "line1\nline2\nline3\nline4\nline5");
    const r = await read({ path: f, offset: 3 });
    assert.equal(r.content, "line3\nline4\nline5");
    assert.equal(r.lines, 3);
  });

  it("should read with limit", async () => {
    const f = join(TEST_DIR, "limit.txt");
    await writeFile(f, "a\nb\nc\nd\ne");
    const r = await read({ path: f, limit: 2 });
    assert.equal(r.content, "a\nb");
    assert.equal(r.lines, 2);
  });

  it("should read with offset and limit combined", async () => {
    const f = join(TEST_DIR, "both.txt");
    await writeFile(f, "a\nb\nc\nd\ne");
    const r = await read({ path: f, offset: 2, limit: 2 });
    assert.equal(r.content, "b\nc");
    assert.equal(r.lines, 2);
  });

  it("should handle single-line file", async () => {
    const f = join(TEST_DIR, "single.txt");
    await writeFile(f, "only line");
    const r = await read({ path: f });
    assert.equal(r.content, "only line");
    assert.equal(r.lines, 1);
  });

  it("should throw for non-existent file", async () => {
    await assert.rejects(() => read({ path: join(TEST_DIR, "nope.txt") }), /ENOENT/);
  });

  it("should reject path traversal", () => {
    assert.throws(() => safePath("../../../etc/shadow"), /Path traversal/);
  });
});
