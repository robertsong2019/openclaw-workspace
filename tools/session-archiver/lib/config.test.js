/**
 * Tests for config.js
 */
const { describe, it } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs");
const path = require("path");
const os = require("os");
const { loadConfig, saveConfig, validateConfig, DEFAULTS } = require("./config.js");

const TMP_DIR = path.join(os.tmpdir(), `sa-config-test-${Date.now()}`);
const CONFIG_PATH = path.join(TMP_DIR, "session-archiver.json");

// Override config path via env
process.env.SESSION_ARCHIVER_CONFIG = CONFIG_PATH;

// Cleanup helper
function cleanup() {
  if (fs.existsSync(CONFIG_PATH)) fs.unlinkSync(CONFIG_PATH);
  if (fs.existsSync(TMP_DIR)) fs.rmSync(TMP_DIR, { recursive: true });
}

describe("config - loadConfig", () => {
  it("returns defaults when no config file exists", () => {
    cleanup();
    const cfg = loadConfig();
    assert.equal(cfg.exportFormat, "markdown");
    assert.equal(cfg.retentionDays, 0);
    assert.equal(cfg.listLimit, 50);
    assert.equal(cfg.archiveDir, "");
  });

  it("merges file values over defaults", () => {
    cleanup();
    fs.mkdirSync(TMP_DIR, { recursive: true });
    fs.writeFileSync(CONFIG_PATH, JSON.stringify({ exportFormat: "html", listLimit: 10 }));
    const cfg = loadConfig();
    assert.equal(cfg.exportFormat, "html");
    assert.equal(cfg.listLimit, 10);
    assert.equal(cfg.retentionDays, 0); // default preserved
    cleanup();
  });

  it("handles corrupt config file gracefully", () => {
    cleanup();
    fs.mkdirSync(TMP_DIR, { recursive: true });
    fs.writeFileSync(CONFIG_PATH, "not json {{{");
    const cfg = loadConfig();
    assert.ok(cfg._error);
    assert.equal(cfg.exportFormat, "markdown"); // still has defaults
    cleanup();
  });
});

describe("config - saveConfig", () => {
  it("creates new config file", () => {
    cleanup();
    const cfg = saveConfig({ exportFormat: "json", retentionDays: 30 });
    assert.equal(cfg.exportFormat, "json");
    assert.equal(cfg.retentionDays, 30);
    assert.ok(fs.existsSync(CONFIG_PATH));
    cleanup();
  });

  it("merges with existing values", () => {
    cleanup();
    fs.mkdirSync(TMP_DIR, { recursive: true });
    fs.writeFileSync(CONFIG_PATH, JSON.stringify({ exportFormat: "html" }));
    saveConfig({ retentionDays: 7 });
    const raw = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf-8"));
    assert.equal(raw.exportFormat, "html"); // preserved
    assert.equal(raw.retentionDays, 7);     // added
    cleanup();
  });

  it("strips internal keys from saved file", () => {
    cleanup();
    saveConfig({ exportFormat: "markdown" });
    const raw = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf-8"));
    assert.equal(raw._path, undefined);
    assert.equal(raw._error, undefined);
    cleanup();
  });
});

describe("config - validateConfig", () => {
  it("returns no warnings for valid config", () => {
    const w = validateConfig({ exportFormat: "markdown", retentionDays: 0, listLimit: 50 });
    assert.equal(w.length, 0);
  });

  it("warns on invalid exportFormat", () => {
    const w = validateConfig({ exportFormat: "pdf", retentionDays: 5, listLimit: 10 });
    assert.equal(w.length, 1);
    assert.ok(w[0].includes("pdf"));
  });

  it("warns on negative retentionDays", () => {
    const w = validateConfig({ exportFormat: "markdown", retentionDays: -1, listLimit: 10 });
    assert.equal(w.length, 1);
  });

  it("warns on zero listLimit", () => {
    const w = validateConfig({ exportFormat: "markdown", retentionDays: 5, listLimit: 0 });
    assert.equal(w.length, 1);
  });
});

// Cleanup after all tests
process.on("exit", cleanup);
