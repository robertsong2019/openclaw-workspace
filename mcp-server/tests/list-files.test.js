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
async function listFiles(workspaceRoot, inputPath = ".", recursive = false, maxDepth = 0) {
  const resolved = join(workspaceRoot, inputPath);
  if (!recursive) {
    const entries = await readdir(resolved, { withFileTypes: true });
    const files = await Promise.all(
      entries.map(async (entry) => {
        const fullPath = join(resolved, entry.name);
        const relativePath = fullPath.slice(workspaceRoot.length + 1);
        try {
          const s = await stat(fullPath);
          return { name: entry.name, path: relativePath, type: entry.isDirectory() ? "directory" : "file", size: s.size };
        } catch {
          return { name: entry.name, path: relativePath, type: "file", size: 0 };
        }
      })
    );
    return { path: inputPath, count: files.length, files };
  }
  // Recursive mode: build correct paths using parentPath
  const entries = await readdir(resolved, { recursive: true, withFileTypes: true });
  const files = await Promise.all(
    entries
      .filter((entry) => {
        if (maxDepth <= 0) return true;
        const relFromRoot = (entry.parentPath + "/" + entry.name).slice(resolved.length + 1);
        const depth = relFromRoot.split("/").length - 1;
        return depth <= maxDepth;
      })
      .map(async (entry) => {
        const fullPath = join(entry.parentPath, entry.name);
        const relativePath = fullPath.slice(workspaceRoot.length + 1);
        try {
          const s = await stat(fullPath);
          return { name: entry.name, path: relativePath, type: entry.isDirectory() ? "directory" : "file", size: s.size };
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

  it("should list files recursively with correct paths", async () => {
    const result = await listFiles(TEST_DIR, ".", true);
    assert.ok(result.count >= 4, "Should include nested files");
    const paths = result.files.map((f) => f.path);
    assert.ok(paths.some((p) => p.includes("sub")), "Nested file path should include sub directory");
    const cFile = result.files.find((f) => f.name === "c.txt");
    assert.ok(cFile, "Should include nested file c.txt");
    assert.ok(cFile.path.includes("sub"), "c.txt path should include sub directory");
    assert.strictEqual(cFile.size, 6, "c.txt should have correct size");
  });

  it("should respect maxDepth when recursive", async () => {
    // Create deeper nesting: sub/deep/d.txt
    const deepDir = join(TEST_DIR, "sub", "deep");
    await mkdir(deepDir, { recursive: true });
    await writeFile(join(deepDir, "d.txt"), "deep", "utf-8");

    // maxDepth=1: only direct children (a.txt, b.txt, sub as dir, but not sub/c.txt)
    const result1 = await listFiles(TEST_DIR, ".", true, 1);
    const paths1 = result1.files.map((f) => f.path);
    assert.ok(paths1.some((p) => p === "a.txt"), "Should include top-level files");
    assert.ok(paths1.some((p) => p.includes("sub")), "Should include sub directory");
    // depth 1 should not include files inside sub (depth 2+)
    const nestedFiles = paths1.filter((p) => p.startsWith("sub/") && !p.endsWith("/"));
    // sub itself has depth 0, files inside sub have depth 1 — so they're included at maxDepth=1
    // But sub/deep/d.txt has depth 2, should be excluded
    assert.ok(!paths1.some((p) => p === "sub/deep/d.txt"), "Should not include depth-2 files at maxDepth=1");
  });

  it("should return correct relative paths in recursive mode", async () => {
    const result = await listFiles(TEST_DIR, ".", true);
    for (const f of result.files) {
      assert.ok(!f.path.startsWith("/"), "Path should be relative: " + f.path);
      // Verify the file actually exists at the reported path
      const fullPath = join(TEST_DIR, f.path);
      const s = await stat(fullPath);
      assert.strictEqual(s.size, f.size, `Size mismatch for ${f.path}`);
    }
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
    // sub/ contains c.txt and deep/ (created by maxDepth test)
    assert.ok(result.count >= 1, "Should have at least c.txt");
    const cFile = result.files.find((f) => f.name === "c.txt");
    assert.ok(cFile, "Should include c.txt");
  });

  it("should handle empty directory", async () => {
    const emptyDir = join(TEST_DIR, "empty");
    await mkdir(emptyDir, { recursive: true });
    const result = await listFiles(emptyDir, ".", false);
    assert.strictEqual(result.count, 0);
    assert.strictEqual(result.files.length, 0);
  });
});
