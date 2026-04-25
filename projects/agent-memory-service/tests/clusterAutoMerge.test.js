/**
 * Agent Memory Service — clusterAutoMerge() Tests
 */
import { describe, it, before } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'mem-cam-'));
  const svc = new MemoryService({ dbPath: dir });
  return { svc, cleanup: () => { try { rmSync(dir, { recursive: true }); } catch {} } };
}

describe('clusterAutoMerge()', () => {
  let svc, cleanup;

  before(async () => {
    ({ svc, cleanup } = createService());
    // Create a large cluster 'ai'
    await svc.add({ content: 'Neural networks basics', layer: 'L0', tags: ['ai', 'ml'], weight: 0.9 });
    await svc.add({ content: 'Deep learning advances', layer: 'L1', tags: ['ai', 'dl'], weight: 0.8 });
    // Create orphaned cluster 'nlp' that co-occurs with 'ai' through shared entity
    await svc.add({ content: 'NLP text processing', layer: 'L0', tags: ['ai', 'nlp'], weight: 0.6 });
    // Create orphaned cluster 'rust' with no co-occurrence to anything
    await svc.add({ content: 'Rust systems programming', layer: 'L1', tags: ['rust'], weight: 0.5 });
  });

  it('returns empty when no small clusters exist', async () => {
    const result = await svc.clusterAutoMerge({ maxSourceSize: 0 });
    assert.equal(result.merged.length, 0);
  });

  it('dry run identifies merge plans without executing', async () => {
    const result = await svc.clusterAutoMerge({ maxSourceSize: 1, minTargetSize: 2, dryRun: true });
    assert.equal(result.dryRun, true);
    assert.ok(result.merged.length > 0);
    // Verify tags unchanged after dry run
    const health = await svc.clusterHealth({ minClusterSize: 1 });
    const rustCluster = health.clusters.find(c => c.topic === 'rust');
    assert.ok(rustCluster, 'rust cluster should still exist after dry run');
  });

  it('merges orphaned clusters into best target by co-occurrence', async () => {
    const result = await svc.clusterAutoMerge({ maxSourceSize: 1, minTargetSize: 2 });
    assert.ok(result.merged.length >= 1);
    // nlp co-occurs with ai, so it should merge into ai
    const nlpMerge = result.merged.find(m => m.source === 'nlp');
    assert.ok(nlpMerge, 'nlp should be merged');
    assert.equal(nlpMerge.target, 'ai');
  });

  it('skips clusters with no co-occurring target', async () => {
    // After merge, re-check: rust had no co-occurrence so might not merge
    const result = await svc.clusterAutoMerge({ maxSourceSize: 1, minTargetSize: 2, dryRun: true });
    const rustMerge = result.merged.find(m => m.source === 'rust');
    // rust has zero co-occurrence with any large cluster, so bestScore = 0 → should not be merged
    assert.ok(!rustMerge, 'rust should not merge (no co-occurrence)');
  });

  it('reports memoriesMoved for each merge', async () => {
    const result = await svc.clusterAutoMerge({ maxSourceSize: 1, minTargetSize: 2, dryRun: true });
    for (const plan of result.merged) {
      assert.ok(plan.memoriesMoved >= 1);
      assert.ok(typeof plan.cooccurrence === 'number');
    }
  });
});
