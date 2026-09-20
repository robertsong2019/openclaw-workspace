// f37-cli-main.test.mjs — spawn-based end-to-end tests of the main() CLI entry.
// main() (~L2576-2691) and runAnalysis() (watch pipeline) were import-
// untestable and had ZERO coverage: every test before this file imported
// exported functions. These tests spawn the real CLI as a child process.
//
// RED-verified bugs pinned here (2026-09-20):
// 1. `--only=bogus` built { bogus: undefined } and the loop's
//    `const [name, { file, gen }]` destructure crashed with an internal
//    "Cannot read properties of undefined (reading 'file')" — the intended
//    "❌ Unknown type" guard was dead code. Same bug in runAnalysis().
// 2. The `🔨 Analyzing...` banner went to STDOUT even in --json mode,
//    making the machine-readable export unparseable (jq/pipe breakage).
//    Fixed: banner routed to stderr in export modes; stdout = pure payload.
import { describe, it, after } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync, rmSync, existsSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CLI = join(__dirname, '..', 'context-forge.mjs');

const tmpRoot = join(process.env.TMPDIR || '/tmp', 'cfx-f37');

let seq = 0;
function makeFixture() {
  // per-test fixture: default mode generates 4 files, so tests must not share
  const dir = join(tmpRoot, `case-${++seq}`);
  mkdirSync(join(dir, 'src'), { recursive: true });
  writeFileSync(join(dir, 'package.json'),
    JSON.stringify({ name: 'fixture-app', version: '1.0.0', description: 'f37 spawn fixture' }));
  writeFileSync(join(dir, 'src', 'index.mjs'),
    'export function hello(){ return "hi"; }\n');
  return dir;
}

function runCli(args) {
  return spawnSync(process.execPath, [CLI, ...args], {
    encoding: 'utf8', timeout: 20000, cwd: tmpRoot,
  });
}

after(() => { rmSync(tmpRoot, { recursive: true, force: true }); });

describe('F37: CLI main() — spawn-based end-to-end', () => {
  it('RED-pinned: --json stdout is pure parseable JSON (banner on stderr)', () => {
    const fixture = makeFixture();
    const r = runCli([fixture, '--json']);
    assert.equal(r.status, 0, `stderr: ${r.stderr}`);
    const parsed = JSON.parse(r.stdout); // throws if banner polluted stdout
    assert.ok(Array.isArray(parsed.gitignore));
    assert.ok(r.stderr.includes('Analyzing'), 'banner should be on stderr');
  });

  it('default mode writes AGENTS.md into the target project', () => {
    const fixture = makeFixture();
    const r = runCli([fixture]);
    assert.equal(r.status, 0, `stderr: ${r.stderr}`);
    const agents = join(fixture, 'AGENTS.md');
    assert.ok(existsSync(agents), 'AGENTS.md must be created');
    assert.ok(readFileSync(agents, 'utf8').length > 50);
  });

  it('--dry-run exits 0, reports dry run, writes nothing', () => {
    const fixture = makeFixture();
    const r = runCli([fixture, '--dry-run']);
    assert.equal(r.status, 0, `stderr: ${r.stderr}`);
    assert.ok(r.stdout.includes('dry run'));
    assert.equal(existsSync(join(fixture, 'AGENTS.md')), false);
  });

  it('--only=agents generates ONLY AGENTS.md (no .cursorrules)', () => {
    const fixture = makeFixture();
    const r = runCli([fixture, '--only=agents']);
    assert.equal(r.status, 0, `stderr: ${r.stderr}`);
    assert.ok(existsSync(join(fixture, 'AGENTS.md')));
    assert.equal(existsSync(join(fixture, '.cursorrules')), false);
  });

  it('nonexistent path: exit 1 with "Path not found" diagnostic', () => {
    const r = runCli([join(tmpRoot, 'case-missing')]);
    assert.equal(r.status, 1);
    assert.ok(r.stderr.includes('Path not found'), `stderr: ${r.stderr}`);
  });

  it('--format=bogus: exit 1 with "Unknown format" diagnostic', () => {
    const fixture = makeFixture();
    const r = runCli([fixture, '--format=bogus']);
    assert.equal(r.status, 1);
    assert.ok(r.stderr.includes('Unknown format'), `stderr: ${r.stderr}`);
  });

  it('RED-pinned: --only=bogus exits 1 with the "Unknown type" diagnostic', () => {
    const fixture = makeFixture();
    const r = runCli([fixture, '--only=bogus']);
    assert.equal(r.status, 1);
    assert.ok(r.stderr.includes('Unknown type: bogus'),
      `expected the Unknown-type diagnostic, got: ${r.stderr.trim()}`);
    assert.ok(!r.stderr.includes('Cannot read properties of undefined'),
      'internal TypeError must not leak to CLI users');
  });

  it('--format=toml and --format=yaml exit 0 with nonempty stdout payload', () => {
    for (const fmt of ['toml', 'yaml']) {
      const fixture = makeFixture();
      const r = runCli([fixture, `--format=${fmt}`]);
      assert.equal(r.status, 0, `format=${fmt} stderr: ${r.stderr}`);
      assert.ok(r.stdout.trim().length > 10, `format=${fmt} output too short`);
      assert.ok(!r.stdout.includes('🔨'), `format=${fmt} stdout must not carry the banner`);
    }
  });
});
