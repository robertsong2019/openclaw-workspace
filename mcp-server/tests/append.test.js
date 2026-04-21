import { describe, it, before, after } from "node:test";
import assert from "node:assert/strict";
import { mkdir, readFile, rm } from "node:fs/promises";
import { join } from "node:path";
import { toolHandlers, safePath } from "../dist/tools.js";

const TEST_DIR = join(process.cwd(), ".test-append");
const append = toolHandlers.append;

describe("append tool", () => {
  before(async () => {
    await mkdir(TEST_DIR, { recursive: true });
  });

  after(async () => {
    await rm(TEST_DIR, { recursive: true, force: true });
  });

  it("should create file if it doesn't exist", async () => {
    const f = join(TEST_DIR, "new.txt");
    const r = await append({ path: f, content: "first line" });
    assert.equal(r.success, true);
    assert.equal(r.tool, "append");
    const content = await readFile(f, "utf-8");
    assert.equal(content, "first line");
  });

  it("should append to existing file with newline", async () => {
    const f = join(TEST_DIR, "existing.txt");
    await append({ path: f, content: "line1" });
    await append({ path: f, content: "line2" });
    const content = await readFile(f, "utf-8");
    assert.equal(content, "line1\nline2");
  });

  it("should append without newline when newline=false", async () => {
    const f = join(TEST_DIR, "noline.txt");
    await append({ path: f, content: "abc" });
    await append({ path: f, content: "def", newline: false });
    const content = await readFile(f, "utf-8");
    assert.equal(content, "abcdef");
  });

  it("should create parent directories", async () => {
    const f = join(TEST_DIR, "deep", "nested", "file.txt");
    const r = await append({ path: f, content: "deep content" });
    assert.equal(r.success, true);
    const content = await readFile(f, "utf-8");
    assert.equal(content, "deep content");
  });

  it("should reject path traversal", () => {
    assert.throws(() => safePath("../../etc/passwd"), /Path traversal/);
  });

  it("should report totalSize and bytesWritten", async () => {
    const f = join(TEST_DIR, "sizes.txt");
    const r1 = await append({ path: f, content: "hello" });
    assert.equal(r1.bytesWritten, 5);
    assert.equal(r1.totalSize, 5);
    const r2 = await append({ path: f, content: "world" });
    assert.equal(r2.bytesWritten, 5);
    assert.equal(r2.totalSize, 11); // "hello\nworld"
  });
});
