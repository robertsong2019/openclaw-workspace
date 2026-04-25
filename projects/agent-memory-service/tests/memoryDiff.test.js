/**
 * Agent Memory Service — memoryDiff() Tests
 */
import { describe, it, before } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'mem-diff-'));
  const svc = new MemoryService({ dbPath: dir });
  return { svc, cleanup: () => { try { rmSync(dir, { recursive: true }); } catch {} } };
}

describe('memoryDiff()', () => {
  let svc, cleanup, id1, id2;

  before(async () => {
    ({ svc, cleanup } = createService());
    id1 = (await svc.add({ content: 'Python machine learning', layer: 'L0', tags: ['ai', 'python'], entities: ['python', 'ml'], weight: 0.9 })).id;
    id2 = (await svc.add({ content: 'Python deep learning', layer: 'L1', tags: ['ai', 'deep-learning'], entities: ['python', 'dl'], weight: 0.7 })).id;
  });

  it('returns found flags for both memories', async () => {
    const diff = await svc.memoryDiff(id1, id2);
    assert.equal(diff.found1, true);
    assert.equal(diff.found2, true);
  });

  it('computes content similarity', async () => {
    const diff = await svc.memoryDiff(id1, id2);
    assert.ok(typeof diff.contentSimilarity === 'number');
    assert.ok(diff.contentSimilarity > 0); // both contain "Python" and "learning"
  });

  it('shows tag differences', async () => {
    const diff = await svc.memoryDiff(id1, id2);
    assert.ok(diff.tags.common.includes('ai'));
    assert.ok(diff.tags.only1.includes('python'));
    assert.ok(diff.tags.only2.includes('deep-learning'));
  });

  it('shows entity differences', async () => {
    const diff = await svc.memoryDiff(id1, id2);
    assert.ok(diff.entities.common.includes('python'));
    assert.ok(diff.entities.only1.includes('ml'));
    assert.ok(diff.entities.only2.includes('dl'));
  });

  it('shows layer and weight diff', async () => {
    const diff = await svc.memoryDiff(id1, id2);
    assert.equal(diff.layers.same, false);
    assert.equal(diff.layers.m1, 'L0');
    assert.equal(diff.layers.m2, 'L1');
    assert.ok(diff.weights.diff > 0);
  });

  it('handles missing memory gracefully', async () => {
    const diff = await svc.memoryDiff(id1, 'nonexistent');
    assert.equal(diff.found1, true);
    assert.equal(diff.found2, false);
  });
});
