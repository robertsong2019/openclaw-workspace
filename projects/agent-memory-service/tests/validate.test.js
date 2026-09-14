import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync, rmSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'ams-val-'));
  const svc = new MemoryService({ dbPath: dir });
  return { svc, dir, cleanup: () => { try { rmSync(dir, { recursive: true }); } catch {} } };
}

async function twoLinked(svc) {
  const a = await svc.add({ content: 'Memory A about project' });
  const b = await svc.add({ content: 'Memory B about project' });
  const link = await svc.link({ source: a.id, target: b.id, type: 'relates_to' });
  return { a, b, link };
}

describe('validate integrity', () => {
  it('healthy links are not flagged as orphans', async () => {
    const { svc, cleanup } = createService();
    try {
      await twoLinked(svc);
      const r = await svc.validate();
      assert.deepEqual(r.issues, [], 'a healthy link must produce zero issues');
      assert.equal(r.valid, true);
    } finally { cleanup(); }
  });

  it('repair on healthy store removes nothing', async () => {
    const { svc, cleanup } = createService();
    try {
      await twoLinked(svc);
      const r = await svc.validate({ repair: true });
      assert.equal(r.repaired ?? 0, 0, 'nothing to repair on a healthy store');
      const s = await svc.stats();
      assert.equal(s.links, 1, 'link must survive repair of a healthy store');
      assert.equal(r.valid, true);
    } finally { cleanup(); }
  });

  it('detects and surgically repairs a true orphan link', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      const { b } = await twoLinked(svc);
      // corruption scenario (per compactBM25Index jsdoc: manual file edits) —
      // remove B directly from memories.json so the link loses its target
      const memPath = join(dir, 'memories.json');
      const arr = JSON.parse(readFileSync(memPath, 'utf-8'));
      const filtered = arr.filter(m => m.id !== b.id);
      assert.equal(filtered.length, arr.length - 1);
      writeFileSync(memPath, JSON.stringify(filtered, null, 2));

      const svc2 = new MemoryService({ dbPath: dir });
      const r1 = await svc2.validate();
      assert.equal(r1.valid, false);
      assert.ok(r1.issues.some(i => i.toLowerCase().includes('orphan') && i.includes(b.id)),
        `expected orphan issue mentioning ${b.id}, got: ${JSON.stringify(r1.issues)}`);

      const r2 = await svc2.validate({ repair: true });
      assert.equal(r2.repaired, 1, 'one orphan link, one repair — not double-counted');
      assert.equal((await svc2.stats()).links, 0, 'orphaned link removed exactly once');
      const r3 = await svc2.validate();
      assert.equal(r3.valid, true, 'store valid after repair');
    } finally { cleanup(); }
  });
});
