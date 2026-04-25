import { describe, it, beforeEach, afterEach } from "node:test";
import assert from "node:assert/strict";
import { mkdir, rm, stat, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { toolHandlers, setWorkspaceRoot } from "../dist/tools.js";

const executeCreateDirectory = toolHandlers["create_directory"];
const TEST_DIR = "/tmp/mcp-test-create-dir";
const originalWorkspace = process.env.OPENCLAW_WORKSPACE;

describe("create_directory", () => {
  beforeEach(async () => {
    await rm(TEST_DIR, { recursive: true, force: true });
    await mkdir(TEST_DIR, { recursive: true });
    setWorkspaceRoot(TEST_DIR);
  });

  afterEach(async () => {
    setWorkspaceRoot(originalWorkspace || process.cwd());
    await rm(TEST_DIR, { recursive: true, force: true });
  });

  it("should create a new directory", async () => {
    const result = await executeCreateDirectory({ path: "new-folder" });
    assert.equal(result.success, true);
    assert.equal(result.created, true);

    const s = await stat(join(TEST_DIR, "new-folder"));
    assert.ok(s.isDirectory());
  });

  it("should create nested directories recursively", async () => {
    const result = await executeCreateDirectory({ path: "a/b/c/d" });
    assert.equal(result.success, true);
    assert.equal(result.created, true);

    const s = await stat(join(TEST_DIR, "a/b/c/d"));
    assert.ok(s.isDirectory());
  });

  it("should report created=false if directory already exists", async () => {
    await mkdir(join(TEST_DIR, "existing"), { recursive: true });
    const result = await executeCreateDirectory({ path: "existing" });
    assert.equal(result.success, true);
    assert.equal(result.created, false);
  });

  it("should fail if a file with same name exists", async () => {
    await writeFile(join(TEST_DIR, "conflict"), "data");
    const result = await executeCreateDirectory({ path: "conflict" });
    assert.equal(result.success, false);
    assert.ok(result.error.includes("already exists"));
  });

  it("should reject path traversal", async () => {
    await assert.rejects(
      () => executeCreateDirectory({ path: "../../etc/evil" }),
      { message: /traversal/i }
    );
  });
});
