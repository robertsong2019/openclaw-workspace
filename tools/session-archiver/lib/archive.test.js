const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs");
const path = require("path");
const os = require("os");
const {
  archiveSession,
  listArchives,
  searchArchives,
  exportSession,
  getStats,
  cleanOldArchives,
} = require("./archive");

const TMP_DIR = fs.mkdtempSync(path.join(os.tmpdir(), "sa-test-"));

// Override archive dir for tests
process.env.SESSION_ARCHIVE_DIR = TMP_DIR;

test("archiveSession creates archive file", () => {
  const result = archiveSession({
    id: "test-001",
    label: "Test Session",
    history: [
      { role: "user", content: "Hello world" },
      { role: "assistant", content: "Hi there! How can I help?" },
    ],
  });
  assert.equal(result.id, "test-001");
  assert.equal(result.messageCount, 2);
  assert.ok(fs.existsSync(result.path));
});

test("listArchives returns archived sessions", () => {
  const archives = listArchives();
  assert.equal(archives.length, 1);
  assert.equal(archives[0].id, "test-001");
  assert.equal(archives[0].messageCount, 2);
});

test("searchArchives finds matching content", () => {
  const results = searchArchives("hello");
  assert.equal(results.length, 1);
  assert.ok(results[0].score > 0);
  assert.equal(results[0].archiveId, "test-001");
});

test("searchArchives returns empty for no match", () => {
  const results = searchArchives("xyznonexistent");
  assert.equal(results.length, 0);
});

test("exportSession markdown format", () => {
  const md = exportSession("test-001", "markdown");
  assert.ok(md.includes("Test Session"));
  assert.ok(md.includes("Hello world"));
  assert.ok(md.includes("USER"));
});

test("exportSession json format", () => {
  const json = exportSession("test-001", "json");
  const parsed = JSON.parse(json);
  assert.equal(parsed.id, "test-001");
});

test("exportSession html format", () => {
  const html = exportSession("test-001", "html");
  assert.ok(html.includes("<!DOCTYPE html>"));
  assert.ok(html.includes("Hello world"));
});

test("getStats returns correct stats", () => {
  const stats = getStats();
  assert.equal(stats.totalArchives, 1);
  assert.equal(stats.totalMessages, 2);
});

test("cleanOldArchives dry run", () => {
  const result = cleanOldArchives(0, true);
  assert.equal(result.count, 1);
  // Should still exist
  assert.equal(listArchives().length, 1);
});

test("cleanOldArchives removes old", () => {
  cleanOldArchives(0, false);
  assert.equal(listArchives().length, 0);
});

// Cleanup
test.after(() => {
  fs.rmSync(TMP_DIR, { recursive: true, force: true });
});
