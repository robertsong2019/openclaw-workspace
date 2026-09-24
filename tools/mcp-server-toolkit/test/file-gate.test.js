import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const ROOT = path.resolve(import.meta.dirname, '..');
const BIN = path.join(ROOT, 'bin', 'mcpt.js');

function tmp() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'mcpt-filegate-'));
}

function mcpt(args, cwd) {
  return spawnSync(process.execPath, [BIN, ...args], { encoding: 'utf8', cwd, timeout: 30000 });
}

const VALID = {
  name: 'demo-server',
  version: '1.0.0',
  transport: 'stdio',
};

test('RED: validate on a directory exits 1 with clean message, no raw EISDIR stack', () => {
  const dir = tmp();
  const sub = path.join(dir, 'i-am-a-dir');
  fs.mkdirSync(sub);
  const r = mcpt(['validate', sub], dir);
  assert.equal(r.status, 1);
  assert.match(r.stdout + r.stderr, /不是配置文件|配置文件/);
  assert.doesNotMatch(r.stdout + r.stderr, /EISDIR/, 'must not leak raw EISDIR stack');
  fs.rmSync(dir, { recursive: true, force: true });
});

test('RED: generate --file on a directory exits 1 with clean message, no raw EISDIR stack', () => {
  const dir = tmp();
  const sub = path.join(dir, 'i-am-a-dir');
  fs.mkdirSync(sub);
  const r = mcpt(['generate', '--file', sub, '--output', path.join(dir, 'out')], dir);
  assert.equal(r.status, 1);
  assert.match(r.stdout + r.stderr, /不是配置文件|配置文件/);
  assert.doesNotMatch(r.stdout + r.stderr, /EISDIR/, 'must not leak raw EISDIR stack');
  fs.rmSync(dir, { recursive: true, force: true });
});

test('legality pin: validate on a good config file still exits 0', () => {
  const dir = tmp();
  fs.writeFileSync(path.join(dir, 'mcp-server.json'), JSON.stringify(VALID));
  const r = mcpt(['validate', 'mcp-server.json'], dir);
  assert.equal(r.status, 0);
  fs.rmSync(dir, { recursive: true, force: true });
});

test('legality pin: generate on a good config file still writes index.ts', () => {
  const dir = tmp();
  fs.writeFileSync(path.join(dir, 'mcp-server.json'), JSON.stringify(VALID));
  const r = mcpt(['generate', '--output', 'dist'], dir);
  assert.equal(r.status, 0, r.stdout + r.stderr);
  assert.ok(fs.existsSync(path.join(dir, 'dist', 'index.ts')));
  fs.rmSync(dir, { recursive: true, force: true });
});
