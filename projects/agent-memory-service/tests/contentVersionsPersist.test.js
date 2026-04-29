import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync, rmSync, existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'cvp-'));
  const svc = new MemoryService({ dbPath: dir });
  return { svc, dir, cleanup: () => { try { rmSync(dir, { recursive: true }); } catch {} } };
}

describe('contentVersions persistence', () => {
  it('persists versions to disk after update', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'v1', layer: 'core' });
      await svc.update(m.id, { content: 'v2' });
      // Check sidecar file exists
      const sidecarPath = join(dir, 'content-versions.json');
      assert.ok(existsSync(sidecarPath), 'sidecar file should exist');
      const data = JSON.parse(readFileSync(sidecarPath, 'utf-8'));
      assert.ok(data[m.id], 'version entry should exist for memory');
      assert.equal(data[m.id].length, 1);
      assert.equal(data[m.id][0].content, 'v1');
    } finally { cleanup(); }
  });

  it('restores versions after restart', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'alpha', layer: 'core' });
      await svc.update(m.id, { content: 'beta' });
      await svc.update(m.id, { content: 'gamma' });

      // Simulate restart: create new service instance on same dir
      const svc2 = new MemoryService({ dbPath: dir });
      await svc2.init();
      const h = await svc2.contentHistory(m.id);
      assert.equal(h.found, true);
      assert.equal(h.versions.length, 3); // gamma(current) + beta + alpha
    } finally { cleanup(); }
  });

  it('handles missing sidecar gracefully', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'hello', layer: 'core' });
      // No update = no versions file
      const h = await svc.contentHistory(m.id);
      assert.equal(h.found, true);
      assert.equal(h.versions.length, 1);
    } finally { cleanup(); }
  });

  it('persists versions after contentBranch', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'original', layer: 'core' });
      await svc.update(m.id, { content: 'updated' });
      await svc.contentBranch(m.id, { content: 'branched' });

      // Restart and verify all versions survived
      const svc2 = new MemoryService({ dbPath: dir });
      await svc2.init();
      const h = await svc2.contentHistory(m.id);
      assert.equal(h.found, true);
      assert.ok(h.versions.length >= 2, 'should have versions from update');
    } finally { cleanup(); }
  });

  it('does not write sidecar when no content changed', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'stable', layer: 'core' });
      await svc.update(m.id, { tags: ['new-tag'] }); // no content change
      const sidecarPath = join(dir, 'content-versions.json');
      // Sidecar may not exist or should be empty for this id
      if (existsSync(sidecarPath)) {
        const data = JSON.parse(readFileSync(sidecarPath, 'utf-8'));
        assert.ok(!data[m.id] || data[m.id].length === 0, 'no versions should be saved for content-unchanged update');
      }
    } finally { cleanup(); }
  });
});
