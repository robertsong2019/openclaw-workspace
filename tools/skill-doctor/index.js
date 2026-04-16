#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

// ── ANSI helpers ──────────────────────────────────────────────
const c = {
  reset: "\x1b[0m", bold: "\x1b[1m",
  green: "\x1b[32m", yellow: "\x1b[33m", red: "\x1b[31m", dim: "\x1b[2m", cyan: "\x1b[36m",
};
const ok = (msg) => `${c.green}✓${c.reset} ${msg}`;
const warn = (msg) => `${c.yellow}⚠${c.reset} ${msg}`;
const fail = (msg) => `${c.red}✗${c.reset} ${msg}`;

// ── Check registry ────────────────────────────────────────────
const checks = [];

function check(name, fn) { checks.push({ name, fn }); }

// ── Individual checks ─────────────────────────────────────────

check("SKILL.md exists", (dir) => {
  const p = path.join(dir, "SKILL.md");
  if (!fs.existsSync(p)) return { status: "fail", msg: "SKILL.md not found" };
  const stat = fs.statSync(p);
  if (stat.size < 50) return { status: "warn", msg: `SKILL.md is only ${stat.size} bytes — likely too short` };
  return { status: "pass", msg: `${stat.size} bytes` };
});

check("SKILL.md has description", (dir) => {
  const p = path.join(dir, "SKILL.md");
  if (!fs.existsSync(p)) return { status: "skip", msg: "no SKILL.md" };
  const content = fs.readFileSync(p, "utf8");
  // Look for description field in frontmatter or a clear description paragraph
  const hasDescription = /description:/i.test(content) || content.length > 200;
  if (!hasDescription) return { status: "warn", msg: "No explicit description found" };
  return { status: "pass", msg: "description present" };
});

check("README.md exists", (dir) => {
  const p = path.join(dir, "README.md");
  if (!fs.existsSync(p)) return { status: "warn", msg: "No README.md" };
  return { status: "pass", msg: "present" };
});

check("No oversized files (>500KB)", (dir) => {
  const walk = (d) => {
    let big = [];
    for (const entry of fs.readdirSync(d, { withFileTypes: true })) {
      if (entry.name.startsWith(".") || entry.name === "node_modules") continue;
      const full = path.join(d, entry.name);
      if (entry.isDirectory()) big.push(...walk(full));
      else if (fs.statSync(full).size > 500_000)
        big.push(`${entry.name} (${(fs.statSync(full).size / 1024).toFixed(0)}KB)`);
    }
    return big;
  };
  const big = walk(dir);
  if (big.length) return { status: "warn", msg: `Large files: ${big.join(", ")}` };
  return { status: "pass", msg: "all files under 500KB" };
});

check("No suspicious patterns", (dir) => {
  const walk = (d) => {
    let results = [];
    for (const entry of fs.readdirSync(d, { withFileTypes: true })) {
      if (entry.name.startsWith(".") || entry.name === "node_modules") continue;
      const full = path.join(d, entry.name);
      if (entry.isDirectory()) { results.push(...walk(full)); continue; }
      if (!/\.(js|ts|sh|py|md)$/.test(entry.name)) continue;
      try {
        const content = fs.readFileSync(full, "utf8");
        // Check for common red flags
        if (/eval\s*\(/.test(content) && !/no.*eval/i.test(content))
          results.push(`${entry.name}: eval() usage`);
        if (/child_process.*execSync.*\+/.test(content))
          results.push(`${entry.name}: possible command injection`);
        if (/curl.*\|.*sh/.test(content))
          results.push(`${entry.name}: pipe to shell`);
        if (/process\.env\.\w+.*(?:fetch|axios|http)/i.test(content))
          results.push(`${entry.name}: env var in network call — verify no exfiltration`);
      } catch {}
    }
    return results;
  };
  const issues = walk(dir);
  if (issues.length) return { status: "warn", msg: issues.join("; ") };
  return { status: "pass", msg: "no suspicious patterns" };
});

check("Scripts referenced in SKILL.md exist", (dir) => {
  const skillPath = path.join(dir, "SKILL.md");
  if (!fs.existsSync(skillPath)) return { status: "skip", msg: "no SKILL.md" };
  const content = fs.readFileSync(skillPath, "utf8");
  // Find script references: ./scripts/foo.sh, ./foo.py, etc.
  const refs = [...content.matchAll(/[`'"]\.\/(?:scripts\/)?[\w.-]+\.(?:sh|py|js|ts)[`'"]/g)]
    .map((m) => m[0].replace(/[`'"]/g, ""));
  const missing = refs.filter((r) => !fs.existsSync(path.join(dir, r)));
  if (missing.length) return { status: "fail", msg: `Missing: ${missing.join(", ")}` };
  if (refs.length === 0) return { status: "pass", msg: "no script references" };
  return { status: "pass", msg: `${refs.length} script(s) found and valid` };
});

check("No node_modules committed", (dir) => {
  if (fs.existsSync(path.join(dir, "node_modules"))) {
    const hasGitignore = fs.existsSync(path.join(dir, ".gitignore"));
    if (hasGitignore) {
      const gi = fs.readFileSync(path.join(dir, ".gitignore"), "utf8");
      if (/node_modules/.test(gi)) return { status: "pass", msg: "in .gitignore" };
    }
    return { status: "warn", msg: "node_modules present, not in .gitignore" };
  }
  return { status: "pass", msg: "no node_modules" };
});

check("Valid package.json (if present)", (dir) => {
  const p = path.join(dir, "package.json");
  if (!fs.existsSync(p)) return { status: "pass", msg: "no package.json (not required)" };
  try {
    const pkg = JSON.parse(fs.readFileSync(p, "utf8"));
    const issues = [];
    if (!pkg.name) issues.push("missing name");
    if (!pkg.version) issues.push("missing version");
    if (issues.length) return { status: "warn", msg: issues.join(", ") };
    return { status: "pass", msg: `${pkg.name}@${pkg.version}` };
  } catch (e) {
    return { status: "fail", msg: `invalid JSON: ${e.message}` };
  }
});

// ── Runner ────────────────────────────────────────────────────

function diagnose(dir) {
  const resolved = path.resolve(dir);
  if (!fs.existsSync(resolved)) {
    console.error(fail(`Directory not found: ${resolved}`));
    process.exit(2);
  }

  console.log(`\n${c.bold}${c.cyan}🩺 skill-doctor${c.reset} — ${resolved}\n`);

  let passes = 0, warns = 0, fails = 0, skips = 0;

  for (const { name, fn } of checks) {
    try {
      const result = fn(resolved);
      const icon =
        result.status === "pass" ? ok(name) :
        result.status === "warn" ? warn(name) :
        result.status === "fail" ? fail(name) :
        `${c.dim}→ ${name}${c.reset}`;

      console.log(`  ${icon}  ${c.dim}${result.msg}${c.reset}`);
      if (result.status === "pass") passes++;
      else if (result.status === "warn") warns++;
      else if (result.status === "fail") fails++;
      else skips++;
    } catch (e) {
      console.log(`  ${fail(name)}  ${c.dim}check error: ${e.message}${c.reset}`);
      fails++;
    }
  }

  console.log(
    `\n  ${c.bold}Summary:${c.reset} ${c.green}${passes} pass${c.reset} / ${c.yellow}${warns} warn${c.reset} / ${c.red}${fails} fail${c.reset} / ${c.dim}${skips} skip${c.reset}\n`
  );

  return fails > 0 ? 2 : warns > 0 ? 1 : 0;
}

// ── CLI ───────────────────────────────────────────────────────
const args = process.argv.slice(2);
if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
  console.log(`${c.bold}skill-doctor${c.reset} — Diagnose OpenClaw Agent Skills

${c.bold}Usage:${c.reset}
  skill-doctor <skill-dir> [skill-dir ...]
  skill-doctor --help

${c.bold}Exit codes:${c.reset}
  0  all checks pass
  1  warnings (no failures)
  2  failures detected`);
  process.exit(0);
}

let exitCode = 0;
for (const arg of args) {
  const code = diagnose(arg);
  if (code > exitCode) exitCode = code;
}
process.exit(exitCode);
