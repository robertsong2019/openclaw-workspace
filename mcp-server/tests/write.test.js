import { describe, it, before, after } from "node:test";
import assert from "node:assert/strict";
import { mkdir, readFile, rm } from "node:fs/promises";
import { join } from "node:path";
import { toolHandlers, safePath } from "../dist/tools.js";

const TEST_DIR = join(process.cwd(), ".test-write");
const write = toolHandlers.write;

describe("write tool", () => {
  before(async () => {
    await mkdir(TEST_DIR, { recursive: true });
  });

  after(async () => {
    await rm(TEST_DIR, { recursive: true, force: true });
  });

  it("should create a new file", async () => {
    const f = join(TEST_DIR, "new.txt");
    const r = await write({ path: f, content: "hello" });
    assert.equal(r.success, true);
    assert.equal(r.tool, "write");
    assert.equal(r.bytesWritten, 5);
    const content = await readFile(f, "utf-8");
    assert.equal(content, "hello");
  });

  it("should overwrite existing file", async () => {
    const f = join(TEST_DIR, "overwrite.txt");
    await write({ path: f, content: "old" });
    await write({ path: f, content: "new content" });
    const content = await readFile(f, "utf-8");
    assert.equal(content, "new content");
  });

  it("should create parent directories", async () => {
    const f = join(TEST_DIR, "deep", "nested", "file.txt");
    const r = await write({ path: f, content: "nested" });
    assert.equal(r.success, true);
    const content = await readFile(f, "utf-8");
    assert.equal(content, "nested");
  });

  it("should write empty content", async () => {
    const f = join(TEST_DIR, "empty.txt");
    const r = await write({ path: f, content: "" });
    assert.equal(r.success, true);
    assert.equal(r.bytesWritten, 0);
    const content = await readFile(f, "utf-8");
    assert.equal(content, "");
  });

  it("should write unicode content", async () => {
    const f = join(TEST_DIR, "unicode.txt");
    const r = await write({ path: f, content: "你好世界 🌍" });
    assert.equal(r.success, true);
    const content = await readFile(f, "utf-8");
    assert.equal(content, "你好世界 🌍");
  });

  it("should report correct bytesWritten for multiline", async () => {
    const f = join(TEST_DIR, "multi.txt");
    const r = await write({ path: f, content: "line1\nline2\nline3" });
    assert.equal(r.bytesWritten, Buffer.byteLength("line1\nline2\nline3", "utf-8"));
  });
});
