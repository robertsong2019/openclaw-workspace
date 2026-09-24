import { describe, it, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'os';
import path from 'path';
import { spawnSync } from 'node:child_process';

const INDEX = path.resolve('index.js');
const made = [];

function mkProject(files) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'cqc-fmt-'));
  for (const [rel, content] of Object.entries(files)) {
    const full = path.join(dir, rel);
    fs.mkdirSync(path.dirname(full), { recursive: true });
    fs.writeFileSync(full, content);
  }
  made.push(dir);
  return dir;
}

function runCli(dir, args) {
  const r = spawnSync('node', [INDEX, 'check', dir, ...args], { encoding: 'utf8', timeout: 60000 });
  return { code: r.status, stdout: r.stdout || '', stderr: r.stderr || '' };
}

describe('format validation (silent-flag-loss family gate)', () => {
  const proj = () => ({ 'src/app.js': 'const a = 1;\n' });

  it('RED: --format xml exits 1 naming value + supported list, no report printed', () => {
    const dir = mkProject(proj());
    const r = runCli(dir, ['--security', '--format', 'xml']);
    assert.equal(r.code, 1);
    assert.match(r.stderr, /--format/);
    assert.match(r.stderr, /xml/);
    assert.match(r.stderr, /console/);
    assert.match(r.stderr, /json/);
    assert.ok(!r.stdout.includes('代码质量检查报告'), 'report must not be printed');
  });

  it('RED: --format jsn (typo variant) exits 1', () => {
    const dir = mkProject(proj());
    const r = runCli(dir, ['--security', '--format', 'jsn']);
    assert.equal(r.code, 1);
    assert.match(r.stderr, /jsn/);
    assert.ok(!r.stdout.includes('代码质量检查报告'));
  });

  it('legality pin: --format json exits 0 and emits JSON', () => {
    const dir = mkProject(proj());
    const r = runCli(dir, ['--security', '--format', 'json']);
    assert.equal(r.code, 0);
    assert.ok(r.stdout.includes('"checks"'));
  });

  it('legality pin: explicit --format console exits 0', () => {
    const dir = mkProject(proj());
    const r = runCli(dir, ['--security', '--format', 'console']);
    assert.equal(r.code, 0);
  });
});

describe('fail-on early validation + failed-check gate', () => {
  it('RED: --fail-on bogus exits 1 before running checks', () => {
    const dir = mkProject({ 'src/app.js': 'const a = 1;\n' });
    const r = runCli(dir, ['--security', '--fail-on', 'bogus']);
    assert.equal(r.code, 1);
    assert.match(r.stderr, /--fail-on/);
    assert.match(r.stderr, /bogus/);
    assert.ok(!r.stdout.includes('安全检查完成'), 'checks must not have run');
  });

  it('RED: --fail-on error fires (exit 1) when a requested check FAILED (broken eslintrc)', () => {
    const dir = mkProject({
      'src/app.js': 'const a = 1;\n',
      '.eslintrc.json': '{BROKEN'
    });
    const r = runCli(dir, ['--eslint', '--fail-on', 'error']);
    assert.equal(r.code, 1);
    assert.match(r.stderr, /eslint/);
    assert.match(r.stderr, /失败|failed/);
  });

  it('legality pin: --fail-on error passes clean project (no failures, no issues)', () => {
    const dir = mkProject({ 'src/app.js': 'const a = 1;\n' });
    const r = runCli(dir, ['--security', '--fail-on', 'error']);
    assert.equal(r.code, 0);
  });
});

after(() => {
  for (const d of made) fs.rmSync(d, { recursive: true, force: true });
});
