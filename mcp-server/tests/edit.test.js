/**
 * Test edit tool functionality
 */

import { describe, it, before, after } from "node:test";
import assert from "node:assert";
import { readFile, writeFile, mkdir, rm } from "node:fs/promises";
import { join } from "node:path";

const TEST_DIR = join(process.cwd(), ".test-fixture-edit");

// Inline implementation mirroring executeEdit for unit testing
async function editFile(testDir, path, oldText, newText) {
  const resolved = join(testDir, path);
  const content = await readFile(resolved, "utf-8");

  if (!content.includes(oldText)) {
    return { success: false, error: "oldText not found in file" };
  }

  const newContent = content.replaceAll(oldText, newText);
  await writeFile(resolved, newContent, "utf-8");

  return {
    success: true,
    replacements: (content.match(new RegExp(oldText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "g")) || []).length,
    bytesChanged: Buffer.byteLength(newContent, "utf-8") - Buffer.byteLength(content, "utf-8"),
  };
}

describe("edit tool", () => {
  before(async () => {
    await mkdir(TEST_DIR, { recursive: true });
  });

  after(async () => {
    await rm(TEST_DIR, { recursive: true, force: true });
  });

  it("should replace exact text match", async () => {
    const testFile = "test.txt";
    await writeFile(join(TEST_DIR, testFile), "Hello World\nGoodbye World\n", "utf-8");

    const result = await editFile(TEST_DIR, testFile, "World", "Universe");

    assert.strictEqual(result.success, true);
    assert.strictEqual(result.replacements, 2);

    const content = await readFile(join(TEST_DIR, testFile), "utf-8");
    assert.ok(content.includes("Hello Universe"));
    assert.ok(content.includes("Goodbye Universe"));
    assert.ok(!content.includes("World"));
  });

  it("should handle single replacement", async () => {
    const testFile = "single.txt";
    await writeFile(join(TEST_DIR, testFile), "foo bar baz\n", "utf-8");

    const result = await editFile(TEST_DIR, testFile, "bar", "qux");

    assert.strictEqual(result.success, true);
    assert.strictEqual(result.replacements, 1);

    const content = await readFile(join(TEST_DIR, testFile), "utf-8");
    assert.strictEqual(content, "foo qux baz\n");
  });

  it("should fail when oldText not found", async () => {
    const testFile = "notfound.txt";
    await writeFile(join(TEST_DIR, testFile), "Hello World\n", "utf-8");

    const result = await editFile(TEST_DIR, testFile, "Goodbye", "Hello");

    assert.strictEqual(result.success, false);
    assert.ok(result.error.includes("not found"));
  });

  it("should preserve whitespace exactly", async () => {
    const testFile = "whitespace.txt";
    await writeFile(join(TEST_DIR, testFile), "  indented  text  \n", "utf-8");

    const result = await editFile(TEST_DIR, testFile, "  indented  ", "\ttabbed\t");

    assert.strictEqual(result.success, true);

    const content = await readFile(join(TEST_DIR, testFile), "utf-8");
    assert.strictEqual(content, "\ttabbed\ttext  \n");
  });

  it("should handle empty newText (deletion)", async () => {
    const testFile = "delete.txt";
    await writeFile(join(TEST_DIR, testFile), "remove this text\nkeep this\n", "utf-8");

    const result = await editFile(TEST_DIR, testFile, "remove this ", "");

    assert.strictEqual(result.success, true);

    const content = await readFile(join(TEST_DIR, testFile), "utf-8");
    assert.strictEqual(content, "text\nkeep this\n");
  });

  it("should report bytes changed correctly", async () => {
    const testFile = "bytes.txt";
    await writeFile(join(TEST_DIR, testFile), "short\n", "utf-8");

    const result = await editFile(TEST_DIR, testFile, "short", "much longer replacement");

    assert.strictEqual(result.success, true);
    assert.ok(result.bytesChanged > 0);
  });

  it("should handle multiline text replacement", async () => {
    const testFile = "multiline.txt";
    await writeFile(
      join(TEST_DIR, testFile),
      "line1\nline2\nline3\nline4\nline5\n",
      "utf-8"
    );

    const result = await editFile(TEST_DIR, testFile, "line2\nline3", "NEW LINE");

    assert.strictEqual(result.success, true);
    assert.strictEqual(result.replacements, 1);

    const content = await readFile(join(TEST_DIR, testFile), "utf-8");
    assert.strictEqual(content, "line1\nNEW LINE\nline4\nline5\n");
  });

  it("should handle unicode characters", async () => {
    const testFile = "unicode.txt";
    await writeFile(join(TEST_DIR, testFile), "Hello 世界\n你好 World\n", "utf-8");

    const result = await editFile(TEST_DIR, testFile, "世界", "🌍");

    assert.strictEqual(result.success, true);

    const content = await readFile(join(TEST_DIR, testFile), "utf-8");
    assert.ok(content.includes("Hello 🌍"));
    assert.ok(!content.includes("世界"));
  });
});
