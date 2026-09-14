import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'ams-am-'));
  const svc = new MemoryService({ dbPath: dir });
  return { svc, cleanup: () => { try { rmSync(dir, { recursive: true }); } catch {} } };
}

describe('autoMaintain', () => {
  it('healthy store: not triggered, no actions', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.add({ content: 'healthy memory' });
      const r = await svc.autoMaintain();
      assert.equal(r.triggered, false);
      assert.deepEqual(r.actions, {});
    } finally { cleanup(); }
  });

  it('dryRun reports recommendations without executing', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.add({ content: 'temp note', expiresAt: Date.now() - 1000 });
      const r = await svc.autoMaintain({ threshold: 100, dryRun: true });
      assert.equal(r.triggered, true, 'threshold 100 forces trigger');
      assert.ok(Array.isArray(r.actions), 'dryRun actions = recommendations array');
      assert.ok(r.actions.length >= 1, 'at least one recommendation reported');
      // dry-run must not purge
      const survivors = await svc.query({ limit: 100 });
      assert.ok(survivors.total >= 1, 'expired memory survives dry-run');
    } finally { cleanup(); }
  });

  it('task whitelist: only decay and reindex run', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.add({ content: 'some memory' });
      await svc.add({ content: 'score-dropper', expiresAt: Date.now() - 1000 });
      const r = await svc.autoMaintain({ threshold: 100, tasks: ['decay', 'reindex'] });
      assert.equal(r.triggered, true);
      assert.ok('decay' in r.actions, 'decay ran');
      assert.ok('reindex' in r.actions, 'reindex ran');
      assert.ok(!('purge' in r.actions), 'purge not in whitelist even though expiry gate would fire');
      assert.ok(!('compactBM25' in r.actions), 'compactBM25 not in whitelist');
    } finally { cleanup(); }
  });

  it('health gate: expired memory triggers purge through default tasks', async () => {
    const { svc, cleanup } = createService();
    try {
      const keep = await svc.add({ content: 'keeper' });
      await svc.add({ content: 'stale note', expiresAt: Date.now() - 1000 });
      const r = await svc.autoMaintain({ threshold: 100, tasks: ['purge'] });
      assert.equal(r.triggered, true);
      assert.ok('purge' in r.actions, 'purge ran via gate');
      assert.ok(r.actions.purge.purged.length >= 1);
      const got = await svc.get(keep.id);
      assert.ok(got, 'keeper survives');
    } finally { cleanup(); }
  });
});
