import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync, rmSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'ams-hyg-'));
  const svc = new MemoryService({ dbPath: dir });
  return { svc, dir, cleanup: () => { try { rmSync(dir, { recursive: true }); } catch {} } };
}

const HOUR = 3600 * 1000;

describe('findByTimeRange', () => {
  it('returns memories with createdAt in range, newest first', async () => {
    const { svc, cleanup } = createService();
    try {
      const now = Date.now();
      await svc.add({ content: 'alpha one' });
      await svc.add({ content: 'beta two' });
      const r = await svc.findByTimeRange(now - HOUR, now + HOUR);
      assert.equal(r.length, 2);
      for (const m of r) assert.ok(m.createdAt >= now - HOUR && m.createdAt <= now + HOUR);
      assert.ok(r[0].createdAt >= r[r.length - 1].createdAt, 'sorted newest first');
    } finally { cleanup(); }
  });

  it('returns empty when nothing matches', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.add({ content: 'present' });
      const r = await svc.findByTimeRange(0, 1); // 1970 epoch window
      assert.deepEqual(r, []);
    } finally { cleanup(); }
  });

  it('respects layer filter and limit', async () => {
    const { svc, cleanup } = createService();
    try {
      const now = Date.now();
      await svc.add({ content: 'short one', layer: 'short' });
      await svc.add({ content: 'core one', layer: 'core' });
      const r = await svc.findByTimeRange(now - HOUR, now + HOUR, { layer: 'core' });
      assert.equal(r.length, 1);
      assert.equal(r[0].content, 'core one');
      const limited = await svc.findByTimeRange(now - HOUR, now + HOUR, { limit: 1 });
      assert.equal(limited.length, 1);
    } finally { cleanup(); }
  });

  it('silently drops memories when field is missing (documented semantics)', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.add({ content: 'anything' });
      const r = await svc.findByTimeRange(0, Date.now() + HOUR, { field: 'nonexistentField' });
      assert.deepEqual(r, []);
    } finally { cleanup(); }
  });

  it('field accessedAt finds freshly accessed memories', async () => {
    const { svc, cleanup } = createService();
    try {
      const now = Date.now();
      const a = await svc.add({ content: 'accessed target' });
      await svc.get(a.id); // touches accessedAt
      const r = await svc.findByTimeRange(now - HOUR, now + HOUR, { field: 'accessedAt' });
      assert.equal(r.length, 1);
      assert.equal(r[0].id, a.id);
    } finally { cleanup(); }
  });
});

describe('compactBM25Index', () => {
  it('healthy store: nothing to remove', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.add({ content: 'document one about cats' });
      await svc.add({ content: 'document two about dogs' });
      const dry = await svc.compactBM25Index({ dryRun: true });
      assert.deepEqual(dry, { removed: 0, remaining: 2 });
      const real = await svc.compactBM25Index();
      assert.deepEqual(real, { removed: 0, remaining: 2 });
    } finally { cleanup(); }
  });

  it('removes ghost docs after out-of-band memory deletion (dryRun first, then real)', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      const a = await svc.add({ content: 'survivor about cats' });
      const b = await svc.add({ content: 'doomed about dogs' });

      // corruption scenario: remove b from memories.json, leaving its BM25 entry
      const memPath = join(dir, 'memories.json');
      const arr = JSON.parse(readFileSync(memPath, 'utf-8'));
      writeFileSync(memPath, JSON.stringify(arr.filter(m => m.id !== b.id), null, 2));

      const svc2 = new MemoryService({ dbPath: dir });
      const dry = await svc2.compactBM25Index({ dryRun: true });
      assert.deepEqual(dry, { removed: 1, remaining: 2 });
      // dry-run must not mutate: second dry-run sees the same ghost
      const dry2 = await svc2.compactBM25Index({ dryRun: true });
      assert.deepEqual(dry2, { removed: 1, remaining: 2 });

      const real = await svc2.compactBM25Index();
      assert.deepEqual(real, { removed: 1, remaining: 1 });
      const after = await svc2.compactBM25Index();
      assert.deepEqual(after, { removed: 0, remaining: 1 });

      // survivor still searchable
      const hits = await svc2.searchBM25('cats');
      assert.equal(hits.length, 1);
      assert.equal(hits[0].id, a.id);
    } finally { cleanup(); }
  });
});
