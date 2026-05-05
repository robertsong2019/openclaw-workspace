/**
 * Config file support for session-archiver.
 * Reads ~/.openclaw/session-archiver.json (or SESSION_ARCHIVER_CONFIG env).
 */

const fs = require("fs");
const path = require("path");
const os = require("os");

const DEFAULT_CONFIG_PATH = path.join(os.homedir(), ".openclaw", "session-archiver.json");

const DEFAULTS = {
  exportFormat: "markdown",
  retentionDays: 0,  // 0 = never auto-clean
  listLimit: 50,
  archiveDir: "",    // empty = default
};

function getConfigPath() {
  return process.env.SESSION_ARCHIVER_CONFIG || DEFAULT_CONFIG_PATH;
}

/**
 * Load config from disk, merged with defaults.
 * Missing file = all defaults (no error).
 */
function loadConfig() {
  const configPath = getConfigPath();
  if (!fs.existsSync(configPath)) {
    return { ...DEFAULTS, _path: configPath };
  }
  try {
    const raw = JSON.parse(fs.readFileSync(configPath, "utf-8"));
    return { ...DEFAULTS, ...raw, _path: configPath };
  } catch (e) {
    return { ...DEFAULTS, _path: configPath, _error: e.message };
  }
}

/**
 * Write config to disk, merging with existing values.
 */
function saveConfig(updates) {
  const configPath = getConfigPath();
  const dir = path.dirname(configPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  let existing = {};
  if (fs.existsSync(configPath)) {
    try { existing = JSON.parse(fs.readFileSync(configPath, "utf-8")); } catch {}
  }

  const merged = { ...existing, ...updates };
  // Strip internal keys
  delete merged._path;
  delete merged._error;

  fs.writeFileSync(configPath, JSON.stringify(merged, null, 2), "utf-8");
  return { ...DEFAULTS, ...merged, _path: configPath };
}

/**
 * Validate config values, return array of warning strings.
 */
function validateConfig(config) {
  const warnings = [];
  if (config.exportFormat && !["markdown", "html", "json"].includes(config.exportFormat)) {
    warnings.push(`Unknown exportFormat: ${config.exportFormat}`);
  }
  if (typeof config.retentionDays !== "number" || config.retentionDays < 0) {
    warnings.push("retentionDays must be a non-negative number");
  }
  if (typeof config.listLimit !== "number" || config.listLimit < 1) {
    warnings.push("listLimit must be a positive number");
  }
  return warnings;
}

module.exports = { loadConfig, saveConfig, validateConfig, DEFAULTS, getConfigPath };
