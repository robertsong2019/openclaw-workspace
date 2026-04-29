import { describe, it, before, after } from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, rm } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";

describe("find_files", () => {
  let handler, setWorkspaceRoot;
  let testDir;

  before(async () => {
    const mod = await import("../dist/tools.js");
    handler = mod.toolHandlers.find_files;
    setWorkspaceRoot = mod.setWorkspaceRoot;

    testDir = await mkdtemp(join(tmpdir(), "findfiles-"));
    setWorkspaceRoot(testDir);

    // Create test file structure:
    // testDir/
    //   a.ts
    //   a.js
    //   readme.md
    //   src/
    //     index.ts
    //     utils.ts
    //     helpers.js
    //   tests/
    //     a.test.ts
    //     b.test.js
    //   deep/
    //     level1/
    //       level2/
    //         deep.txt
    await writeFile(join(testDir, "a.ts"), "ts");
    await writeFile(join(testDir, "a.js"), "js");
    await writeFile(join(testDir, "readme.md"), "# readme");
    await mkdir(join(testDir, "src"), { recursive: true });
    await writeFile(join(testDir, "src", "index.ts"), "export");
    await writeFile(join(testDir, "src", "utils.ts"), "util");
    await writeFile(join(testDir, "src", "helpers.js"), "help");
    await mkdir(join(testDir, "tests"), { recursive: true });
    await writeFile(join(testDir, "tests", "a.test.ts"), "test1");
    await writeFile(join(testDir, "tests", "b.test.js"), "test2");
    await mkdir(join(testDir, "deep", "level1", "level2"), { recursive: true });
    await writeFile(join(testDir, "deep", "level1", "level2", "deep.txt"), "deep");
  });

  after(async () => {
    try { await rm(testDir, { recursive: true }); } catch {}
  });

  it("should find .ts files with recursive glob", async () => {
    const result = await handler({ pattern: "**/*.ts" });
    assert.ok(result.tool === "find_files");
    assert.ok(result.count >= 4); // a.ts, src/index.ts, src/utils.ts, tests/a.test.ts
    assert.ok(result.files.every((f) => f.endsWith(".ts")));
  });

  it("should find files with double-star glob", async () => {
    const result = await handler({ pattern: "**/*.test.js" });
    assert.ok(result.files.some((f) => f.includes("b.test.js")));
  });

  it("should respect maxResults", async () => {
    const result = await handler({ pattern: "**/*", maxResults: 2 });
    assert.equal(result.files.length, 2);
  });

  it("should not return deeply nested files with root-only glob", async () => {
    const result = await handler({ pattern: "*.txt" });
    // *.txt only matches at root, not deep/level1/level2/deep.txt
    assert.ok(!result.files.some((f) => f.includes("deep.txt")));
  });

  it("should find deeply nested files", async () => {
    const result = await handler({ pattern: "**/*.txt" });
    assert.ok(result.files.some((f) => f.includes("deep.txt")));
  });

  it("should search within a subdirectory via path", async () => {
    const result = await handler({ pattern: "*.ts", path: "src" });
    assert.equal(result.count, 2); // index.ts + utils.ts
    assert.ok(result.files.every((f) => f.startsWith("src/")));
  });

  it("should return empty array for no matches", async () => {
    const result = await handler({ pattern: "*.xyz" });
    assert.equal(result.count, 0);
    assert.deepEqual(result.files, []);
  });
});
