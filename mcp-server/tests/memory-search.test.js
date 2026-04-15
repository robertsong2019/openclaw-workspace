/**
 * Test memory_search tool functionality
 */

import { describe, it, before, after } from "node:test";
import assert from "node:assert";
import { writeFile, mkdir, rm } from "node:fs/promises";
import { join } from "node:path";
import { readFile, readdir } from "node:fs/promises";

const TEST_DIR = join(process.cwd(), ".test-fixture-mem");

// Inline implementation mirroring executeMemorySearch for unit testing
async function memorySearch(workspaceRoot, query) {
  const keyword = query.toLowerCase();
  const results = [];

  const searchFile = async (filePath, displayName) => {
    try {
      const content = await readFile(filePath, "utf-8");
      const lines = content.split("\n");
      const matches = lines
        .map((line, i) => ({ line: i + 1, text: line }))
        .filter((m) => m.text.toLowerCase().includes(keyword));
      if (matches.length > 0) {
        results.push({ file: displayName, matches });
      }
    } catch {
      // skip
    }
  };

  await searchFile(join(workspaceRoot, "MEMORY.md"), "MEMORY.md");

  try {
    const memDir = join(workspaceRoot, "memory");
    const entries = await readdir(memDir);
    for (const entry of entries) {
      if (entry.endsWith(".md")) {
        await searchFile(join(memDir, entry), `memory/${entry}`);
      }
    }
  } catch {
    // skip
  }

  return {
    query,
    totalMatches: results.reduce((sum, r) => sum + r.matches.length, 0),
    results,
  };
}

describe("memory_search tool", () => {
  before(async () => {
    await mkdir(join(TEST_DIR, "memory"), { recursive: true });
    await writeFile(join(TEST_DIR, "MEMORY.md"), "# My Memory\nImportant notes about AI\n", "utf-8");
    await writeFile(join(TEST_DIR, "memory", "2025-01-15.md"), "# Daily\nWorked on AI project today\n", "utf-8");
    await writeFile(join(TEST_DIR, "memory", "2025-01-16.md"), "# Daily\nWent hiking\n", "utf-8");
  });

  after(async () => {
    await rm(TEST_DIR, { recursive: true, force: true });
  });

  it("should find matches in MEMORY.md", async () => {
    const result = await memorySearch(TEST_DIR, "AI");
    assert.ok(result.results.length > 0);
    const memResult = result.results.find((r) => r.file === "MEMORY.md");
    assert.ok(memResult, "Should find match in MEMORY.md");
    assert.ok(memResult.matches.some((m) => m.text.includes("AI")));
  });

  it("should find matches in memory/*.md files", async () => {
    const result = await memorySearch(TEST_DIR, "AI");
    const dailyResult = result.results.find((r) => r.file === "memory/2025-01-15.md");
    assert.ok(dailyResult, "Should find match in daily file");
  });

  it("should be case-insensitive", async () => {
    const result = await memorySearch(TEST_DIR, "ai");
    assert.ok(result.totalMatches >= 2, "Should find matches case-insensitively");
  });

  it("should return empty results for no matches", async () => {
    const result = await memorySearch(TEST_DIR, "quantum computing xyz");
    assert.strictEqual(result.results.length, 0);
    assert.strictEqual(result.totalMatches, 0);
  });

  it("should report correct line numbers", async () => {
    const result = await memorySearch(TEST_DIR, "Important");
    const memResult = result.results.find((r) => r.file === "MEMORY.md");
    assert.ok(memResult);
    assert.strictEqual(memResult.matches[0].line, 2);
  });

  it("should include match text in results", async () => {
    const result = await memorySearch(TEST_DIR, "hiking");
    const dailyResult = result.results.find((r) => r.file === "memory/2025-01-16.md");
    assert.ok(dailyResult);
    assert.ok(dailyResult.matches[0].text.includes("hiking"));
  });

  it("should handle missing MEMORY.md gracefully", async () => {
    const emptyDir = join(TEST_DIR, "empty");
    await mkdir(emptyDir, { recursive: true });
    const result = await memorySearch(emptyDir, "anything");
    assert.strictEqual(result.results.length, 0);
    await rm(emptyDir, { recursive: true, force: true });
  });

  it("should handle missing memory/ directory gracefully", async () => {
    const noMemDir = join(TEST_DIR, "nomem");
    await mkdir(noMemDir, { recursive: true });
    await writeFile(join(noMemDir, "MEMORY.md"), "test content here\n", "utf-8");
    const result = await memorySearch(noMemDir, "test");
    assert.strictEqual(result.results.length, 1);
    await rm(noMemDir, { recursive: true, force: true });
  });
});
