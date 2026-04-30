import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtemp, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

describe('contentVersionCompact', () => {
  let service, dir;

  beforeEach(async () => {
    dir = await mkdtemp(join(tmpdir(), 'am-cvc-'));
    service = new MemoryService({ dbPath: dir });
  });

  afterEach(async () => {
    try { await rm(dir, { recursive: true }); } catch {}
  });

  it('does nothing when no memories have versions', async () => {
    const result = await service.contentVersionCompact();
    assert.equal(result.compacted, 0);
    assert.equal(result.totalVersions, 0);
    assert.equal(result.dryRun, false);
  });

  it('compacts versions beyond maxVersions', async () => {
    const mem = await service.add({ content: 'v0 initial content for testing compact' });
    // Create 15 versions by updating
    for (let i = 1; i <= 15; i++) {
      await service.update(mem.id, { content: `v${i} updated content for testing compact iteration ${i}` });
    }

    const history = await service.contentHistory(mem.id);
    assert.ok(history.versions.length > 10);

    const result = await service.contentVersionCompact({ maxVersions: 5 });
    assert.ok(result.compacted > 0);
    assert.ok(result.details.length > 0);

    // Verify versions were removed
    const after = await service.contentHistory(mem.id);
    assert.ok(after.versions.length <= 6); // 5 snapshots + 1 current
  });

  it('removes versions older than timestamp', async () => {
    const mem = await service.add({ content: 'original content for older than test' });
    await service.update(mem.id, { content: 'second version for older than test' });
    await service.update(mem.id, { content: 'third version for older than test' });

    // Compact with olderThan = very old timestamp (should remove nothing)
    const result1 = await service.contentVersionCompact({ olderThan: 0 });
    assert.equal(result1.compacted, 0);

    // Compact with olderThan = far future (should remove all snapshots)
    const result2 = await service.contentVersionCompact({ olderThan: Date.now() + 100000 });
    assert.ok(result2.compacted >= 0);
  });

  it('dryRun does not actually remove', async () => {
    const mem = await service.add({ content: 'dry run test content for compact feature' });
    for (let i = 1; i <= 12; i++) {
      await service.update(mem.id, { content: `dry run v${i} content for compact feature testing` });
    }

    const before = await service.contentHistory(mem.id);
    const result = await service.contentVersionCompact({ maxVersions: 3, dryRun: true });
    assert.equal(result.dryRun, true);
    assert.ok(result.compacted > 0);

    // Versions should still be there
    const after = await service.contentHistory(mem.id);
    assert.equal(after.versions.length, before.versions.length);
  });

  it('handles maxVersions with no trimming needed', async () => {
    const mem = await service.add({ content: 'few versions test content' });
    await service.update(mem.id, { content: 'second few versions test' });

    const result = await service.contentVersionCompact({ maxVersions: 100 });
    assert.equal(result.compacted, 0);
  });
});
