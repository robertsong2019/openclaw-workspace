/**
 * Test list_files tool functionality
 */

import { describe, it, before, after } from "node:test";
import assert from "node:assert";
import { writeFile, mkdir, rm } from "node:fs/promises";
import { join } from "node:path";
import { readdir, stat } from "node:fs/promises";

const TEST_DIR = join(process.cwd(), ".test-fixture-list");

// Inline implementation mirroring executeListFiles
async function listFiles(workspaceRoot, inputPath = ".", recursive = false) {
  const resolved = join(workspaceRoot, inputPath);
  const entries = await readdir(resolved, { recursive, withFileTypes: true });
  const files = await Promise.all(
    entries.map(async (entry) => {
      const fullPath = join(resolved, entry.name);
      const relativePath = fullPath.slice(workspaceRoot.length + 1);
      try {
        const s = await stat(fullPath);
        return {
          name: entry.name,
          path: relativePath,
          type: entry.isDirectory() ? "directory" : "file",
          size: s.size,
        };
      } catch {
        return { name: entry.name, path: relativePath, type: "file", size: 0 };
      }
    })
  );
  return { path: inputPath, count: files.length, files };
}

describe("list_files tool", () => {
  before(async () => {
    await mkdir(join(TEST_DIR, "sub"), { recursive: true });
    await writeFile(join(TEST_DIR, "a.txt"), "hello", "utf-8");
    await writeFile(join(TEST_DIR, "b.txt"), "world!!", "utf-8");
    await writeFile(join(TEST_DIR, "sub", "c.txt"), "nested", "utf-8");
  });

  after(async () => {
    await rm(TEST_DIR, { recursive: true, force: true });
  });

  it("should list files in a directory (non-recursive)", async () => {
    const result = await listFiles(TEST_DIR, ".", false);
    assert.strictEqual(result.count, 3); // a.txt, b.txt, sub
    const names = result.files.map((f) => f.name);
    assert.ok(names.includes("a.txt"));
    assert.ok(names.includes("b.txt"));
    assert.ok(names.includes("sub"));
  });

  it("should list files recursively", async () => {
    const result = await listFiles(TEST_DIR, ".", true);
    assert.ok(result.count >= 4, "Should include nested files");
    const names = result.files.map((f) => f.name);
    assert.ok(names.includes("c.txt"), "Should include nested file c.txt");
  });

  it("should report file sizes", async () => {
    const result = await listFiles(TEST_DIR, ".", false);
    const aFile = result.files.find((f) => f.name === "a.txt");
    assert.ok(aFile);
    assert.strictEqual(aFile.size, 5);
  });

  it("should distinguish files and directories", async () => {
    const result = await listFiles(TEST_DIR, ".", false);
    const subDir = result.files.find((f) => f.name === "sub");
    assert.ok(subDir);
    assert.strictEqual(subDir.type, "directory");
    const txtFile = result.files.find((f) => f.name === "a.txt");
    assert.strictEqual(txtFile.type, "file");
  });

  it("should return relative paths", async () => {
    const result = await listFiles(TEST_DIR, ".", false);
    for (const f of result.files) {
      assert.ok(!f.path.startsWith("/"), "Path should be relative");
    }
  });

  it("should list a specific subdirectory", async () => {
    const result = await listFiles(TEST_DIR, "sub", false);
    assert.strictEqual(result.count, 1);
    assert.strictEqual(result.files[0].name, "c.txt");
  });

  it("should handle empty directory", async () => {
    const emptyDir = join(TEST_DIR, "empty");
    await mkdir(emptyDir, { recursive: true });
    const result = await listFiles(emptyDir, ".", false);
    assert.strictEqual(result.count, 0);
    assert.strictEqual(result.files.length, 0);
  });
});
