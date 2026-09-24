/**
 * Budget/clear input-validation gates + budget-check cost divergence.
 * RED-first: 2026-09-24 probes confirmed all three bugs before fixing.
 *
 * Hermetic via HOME override (storage writes to $HOME/.config/agent-cost-tracker;
 * os.homedir() reads $HOME at call time, so setting it before import redirects conf).
 */

const { mkdtempSync } = require('node:fs');
const { tmpdir } = require('node:os');
const { join } = require('node:path');

process.env.HOME = mkdtempSync(join(tmpdir(), 'act-gates-')); // BEFORE first storage.js import

const test = require('node:test');
const assert = require('node:assert');
const { spawnSync } = require('node:child_process');

const ROOT = join(__dirname, '..');
const BIN = join(ROOT, 'bin', 'act.js');

function act(...args) {
  const res = spawnSync(process.execPath, [BIN, ...args], {
    env: { ...process.env, NO_COLOR: '1', CI: '1' },
    encoding: 'utf-8',
    timeout: 30000,
  });
  return { code: res.status, out: strip(res.stdout), err: strip(res.stderr) };
}

function strip(s) {
  return (s || '').replace(/\x1b\[[0-9;]*m/g, '');
}

test('storage: setBudget rejects non-numeric amount (NaN must never reach disk as null)', async () => {
  const storage = await import('../lib/storage.js');
  assert.throws(() => storage.setBudget('abc', 'month', 80), /abc/);
  assert.equal(storage.getBudget().enabled, false, 'budget must stay disabled after failed set');
});

test('storage: setBudget rejects negative amount (negative-gate family)', async () => {
  const storage = await import('../lib/storage.js');
  assert.throws(() => storage.setBudget('-50', 'month', 80), /-50/);
});

test('storage: setBudget rejects out-of-range warning threshold', async () => {
  const storage = await import('../lib/storage.js');
  assert.throws(() => storage.setBudget('100', 'month', 150), /150/);
  assert.throws(() => storage.setBudget('100', 'month', 'abc'), /abc/);
});

test('storage: setBudget legality pin — valid set roundtrips', async () => {
  const storage = await import('../lib/storage.js');
  storage.setBudget('100', 'month', 80);
  const b = storage.getBudget();
  assert.equal(b.enabled, true);
  assert.equal(b.amount, 100);
  assert.equal(b.warningThreshold, 80);
  storage.resetBudget();
});

test('storage: clearLogs rejects invalid date (silent-no-op family — garbage date deleted 0 rows with success msg)', async () => {
  const storage = await import('../lib/storage.js');
  storage.addLog({ model: 'gpt-4', promptTokens: 1000, completionTokens: 500 });
  assert.throws(() => storage.clearLogs('garbage'), /garbage/);
  assert.ok(storage.getLogs({ period: 'all' }).length >= 1, 'logs must survive failed clear');
});

test('storage: clearLogs legality pin — valid cutoff deletes only older rows', async () => {
  const storage = await import('../lib/storage.js');
  storage.addLog({ model: 'gpt-4', promptTokens: 1000, completionTokens: 500 }); // now
  assert.ok(storage.clearLogs('2020-01-01') === 0); // nothing older than 2020
  assert.ok(storage.getLogs({ period: 'all' }).length >= 1);
});

test('CLI: budget set -a abc exits 1 naming the value (was: rc 0 storing amount:null)', () => {
  const r = act('budget', 'set', '-a', 'abc');
  assert.strictEqual(r.code, 1);
  assert.match(r.out + r.err, /abc/);
});

test('CLI: budget set -a -50 exits 1 (negative-gate family)', () => {
  const r = act('budget', 'set', '-a', '-50');
  assert.strictEqual(r.code, 1);
  assert.match(r.out + r.err, /-50/);
});

test('CLI: budget set -w 150 exits 1 naming threshold (was: silently stored)', () => {
  const r = act('budget', 'set', '-a', '100', '-w', '150');
  assert.strictEqual(r.code, 1);
  assert.match(r.out + r.err, /150/);
});

test('CLI: budget set legality pin — valid args exit 0 and enable budget', () => {
  const r = act('budget', 'set', '-a', '200', '-w', '80');
  assert.strictEqual(r.code, 0, r.err);
  const c = act('budget', 'check');
  assert.strictEqual(c.code, 0, c.err);
  assert.ok(!c.out.includes('未启用'), 'budget must be enabled after valid set');
});

test('CLI: clear --before garbage exits 1 naming the date (was: rc 0 "已删除 0 条")', () => {
  const r = act('clear', '--before', 'garbage', '-y');
  assert.strictEqual(r.code, 1);
  assert.match(r.out + r.err, /garbage/);
});

test('CLI: budget check cost uses model price table, not hardcoded $0.01/$0.03', () => {
  // 1M in + 1M out on gpt-4 (30/60 per 1M) = $90.00 via price table;
  // hardcoded 0.01/0.03 printed $40 — parallel-constant divergence from `act stats`.
  act('clear', '-y');
  const add = act('log', '-m', 'gpt-4', '-p', '1000000', '-c', '1000000');
  assert.strictEqual(add.code, 0, add.err);
  act('budget', 'set', '-a', '200');
  const c = act('budget', 'check');
  assert.strictEqual(c.code, 0, c.err);
  assert.match(c.out, /已用金额: \$90\.0000/, 'budget check must price via model table (calculateCost)');
});
