import { describe, it, after } from "node:test";
import assert from "node:assert/strict";
import { mkdir, rm, readFile, stat } from "node:fs/promises";
import { join } from "node:path";
import { toolHandlers } from "../dist/tools.js";

const { move, write } = toolHandlers;
const TEST_DIR = "test-move-dir";
const TEST_FILE = "test-move-file.txt";

describe("move tool", () => {
  after(async () => {
    try { await rm(TEST_DIR, { recursive: true, force: true }); } catch {}
    try { await rm("test-move-dst", { recursive: true, force: true }); } catch {}
    try { await rm("test-move-deep", { recursive: true, force: true }); } catch {}
    try { await rm(TEST_FILE, { force: true }); } catch {}
    try { await rm("moved.txt", { force: true }); } catch {}
    try { await rm("stolen.txt", { force: true }); } catch {}
  });

  it("should move a file to a new name", async () => {
    await write({ path: TEST_FILE, content: "hello" });
    const result = await move({ source: TEST_FILE, destination: "moved.txt" });
    assert.equal(result.success, true);
    assert.equal(result.source, TEST_FILE);
    assert.equal(result.destination, "moved.txt");
    const content = await readFile("moved.txt", "utf-8");
    assert.equal(content, "hello");
    await assert.rejects(() => stat(TEST_FILE));
  });

  it("should move a file into a subdirectory", async () => {
    await write({ path: "test-move-dst-src.txt", content: "payload" });
    await mkdir(TEST_DIR, { recursive: true });
    const result = await move({ source: "test-move-dst-src.txt", destination: `${TEST_DIR}/data.txt` });
    assert.equal(result.success, true);
    const content = await readFile(join(TEST_DIR, "data.txt"), "utf-8");
    assert.equal(content, "payload");
  });

  it("should move a directory", async () => {
    await mkdir("test-move-deep/folder", { recursive: true });
    await write({ path: "test-move-deep/folder/item.txt", content: "inside" });
    const result = await move({ source: "test-move-deep/folder", destination: "test-move-deep/folder2" });
    assert.equal(result.success, true);
    const content = await readFile("test-move-deep/folder2/item.txt", "utf-8");
    assert.equal(content, "inside");
    await assert.rejects(() => stat("test-move-deep/folder"));
  });

  it("should create destination parent dirs", async () => {
    await write({ path: "test-move-deep/a.txt", content: "deep" });
    const result = await move({ source: "test-move-deep/a.txt", destination: "test-move-deep/x/y/z/a.txt" });
    assert.equal(result.success, true);
    const content = await readFile("test-move-deep/x/y/z/a.txt", "utf-8");
    assert.equal(content, "deep");
  });

  it("should fail if source does not exist", async () => {
    const result = await move({ source: "nonexistent-move.txt", destination: "target.txt" });
    assert.equal(result.success, false);
    assert.equal(result.error, "Source not found");
  });

  it("should reject path traversal in source", async () => {
    await assert.rejects(
      () => move({ source: "../../etc/passwd", destination: "stolen.txt" }),
      /Path traversal/
    );
  });

  it("should reject path traversal in destination", async () => {
    await assert.rejects(
      () => move({ source: "safe.txt", destination: "../../tmp/evil.txt" }),
      /Path traversal/
    );
  });
});
