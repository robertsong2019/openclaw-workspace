import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'crollback-'));
  const svc = new MemoryService({ dbPath: dir });
  return { svc, cleanup: () => { try { rmSync(dir, { recursive: true }); } catch {} } };
}

describe('contentRollback()', () => {
  it('rolls back to a previous version', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'v1', layer: 'core' });
      await svc.update(m.id, { content: 'v2' });
      await svc.update(m.id, { content: 'v3' });
      // Roll back to v1 (index 0)
      const result = await svc.contentRollback(m.id, 0);
      assert.equal(result.found, true);
      assert.equal(result.rolledBack, true);
      assert.equal(result.version.content, 'v1');
      assert.equal(result.current.content, 'v1');
      // Verify actual memory content changed
      const mem = await svc.get(m.id);
      assert.equal(mem.content, 'v1');
    } finally { cleanup(); }
  });

  it('creates a version snapshot before rollback', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'original', layer: 'core' });
      await svc.update(m.id, { content: 'modified' });
      // Roll back to original (index 0)
      await svc.contentRollback(m.id, 0);
      // History should now have: original, modified, original(current)
      const h = await svc.contentHistory(m.id);
      assert.equal(h.versions.length, 3);
      assert.equal(h.versions[0].content, 'original');
      assert.equal(h.versions[1].content, 'modified');
      assert.equal(h.versions[2].content, 'original');
      assert.equal(h.versions[2].current, true);
    } finally { cleanup(); }
  });

  it('returns error when rolling back to current version', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'only version', layer: 'core' });
      const result = await svc.contentRollback(m.id, 0);
      assert.equal(result.found, true);
      assert.equal(result.rolledBack, false);
      assert.equal(result.error, 'already current version');
    } finally { cleanup(); }
  });

  it('returns error for invalid version index', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'test', layer: 'core' });
      const result = await svc.contentRollback(m.id, 99);
      assert.equal(result.found, true);
      assert.equal(result.rolledBack, false);
      assert.equal(result.error, 'invalid version index');
    } finally { cleanup(); }
  });

  it('returns found:false for non-existent memory', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.init();
      const result = await svc.contentRollback('no-such-id', 0);
      assert.equal(result.found, false);
      assert.equal(result.rolledBack, false);
    } finally { cleanup(); }
  });

  it('includes previous content in result', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'alpha', layer: 'core' });
      await svc.update(m.id, { content: 'beta' });
      const result = await svc.contentRollback(m.id, 0);
      assert.equal(result.previous.content, 'beta');
      assert.equal(result.current.content, 'alpha');
    } finally { cleanup(); }
  });

  it('can rollback multiple times (ping-pong)', async () => {
    const { svc, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'A', layer: 'core' });
      await svc.update(m.id, { content: 'B' });
      // Roll back to A
      await svc.contentRollback(m.id, 0);
      let mem = await svc.get(m.id);
      assert.equal(mem.content, 'A');
      // Now roll back to B (version index 1 in the original sequence)
      await svc.contentRollback(m.id, 1);
      mem = await svc.get(m.id);
      assert.equal(mem.content, 'B');
    } finally { cleanup(); }
  });
});
