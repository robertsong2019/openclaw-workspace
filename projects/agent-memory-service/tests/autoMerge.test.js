import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtemp, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

describe('autoMerge', () => {
  let service, dir;

  beforeEach(async () => {
    dir = await mkdtemp(join(tmpdir(), 'am-auto-'));
    service = new MemoryService({ dbPath: dir });
  });

  afterEach(async () => {
    try { await rm(dir, { recursive: true }); } catch {}
  });

  it('returns empty result when no duplicates exist', async () => {
    await service.add({ content: 'xK9mP2vR', tags: ['a'] });
    await service.add({ content: 'wL3nQ7tY', tags: ['b'] });

    const result = await service.autoMerge();
    assert.equal(result.merged, 0);
    assert.equal(result.failed, 0);
    assert.equal(result.dryRun, false);
  });

  it('detects and merges similar memories', async () => {
    const a = await service.add({ content: 'The cat sat on the mat at home', tags: ['pets'], entities: ['cat'] });
    const b = await service.add({ content: 'The cat sat on the mat outside', tags: ['pets'], entities: ['cat'] });

    const result = await service.autoMerge({ minScore: 0.3 });
    assert.equal(result.merged, 1);
    assert.equal(result.failed, 0);
    assert.ok(result.pairs.length >= 1);

    // One of the two should be deleted
    const deleted = result.results[0].deletedId;
    assert.ok(deleted === a.id || deleted === b.id);
  });

  it('respects maxMerges limit', async () => {
    await service.add({ content: 'Similar text about alpha beta gamma', tags: ['x'] });
    await service.add({ content: 'Similar text about alpha beta delta', tags: ['x'] });
    await service.add({ content: 'Similar text about alpha beta epsilon', tags: ['x'] });
    await service.add({ content: 'Similar text about alpha beta zeta', tags: ['x'] });

    const result = await service.autoMerge({ minScore: 0.3, maxMerges: 1 });
    assert.ok(result.pairs.length <= 1);
    assert.ok(result.skipped >= 0);
  });

  it('dryRun does not merge', async () => {
    const a = await service.add({ content: 'The dog played fetch at park', tags: ['dogs'] });
    const b = await service.add({ content: 'The dog played fetch at beach', tags: ['dogs'] });

    const result = await service.autoMerge({ minScore: 0.3, dryRun: true });
    assert.equal(result.merged, 0);
    assert.equal(result.dryRun, true);
    assert.ok(result.pairs.length >= 1);

    // Both still exist
    assert.ok(await service.get(a.id));
    assert.ok(await service.get(b.id));
  });

  it('deduplicates ids — each memory used at most once', async () => {
    await service.add({ content: 'Alpha beta gamma shared text', tags: ['test'], entities: ['alpha'] });
    await service.add({ content: 'Alpha beta gamma shared text variant', tags: ['test'], entities: ['alpha'] });
    await service.add({ content: 'Alpha beta gamma shared text another', tags: ['test'], entities: ['alpha'] });

    const result = await service.autoMerge({ minScore: 0.3, maxMerges: 5 });
    const ids = result.pairs.flatMap(p => p.pair);
    assert.equal(new Set(ids).size, ids.length);
  });

  it('filters by layer', async () => {
    await service.add({ content: 'xK9mP2vR short', layer: 'short', tags: ['shared'] });
    await service.add({ content: 'wL3nQ7tY long', layer: 'long', tags: ['shared'] });

    // short layer filter should only see first memory, no pair possible
    const result = await service.autoMerge({ minScore: 0.3, layer: 'short' });
    assert.equal(result.merged, 0);
  });
});
