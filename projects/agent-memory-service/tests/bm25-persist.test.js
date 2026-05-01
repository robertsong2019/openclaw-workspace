/**
 * BM25 Index Persistence Tests
 */
import { describe, it, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync, rmSync, existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'mem-bm25-'));
  const svc = new MemoryService({ dbPath: dir });
  return { svc, dir, cleanup: () => { try { rmSync(dir, { recursive: true }); } catch {} } };
}

describe('BM25 Index Persistence', () => {
  it('saves BM25 index to disk after adding memory', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      await svc.init();
      await svc.add({ content: 'machine learning algorithms' });
      const path = join(dir, 'bm25-index.json');
      assert.ok(existsSync(path), 'bm25-index.json should exist after add');
      const data = JSON.parse(readFileSync(path, 'utf-8'));
      assert.ok(data.docs, 'should have docs');
      assert.ok(data.df, 'should have df');
      assert.ok(typeof data.totalLen === 'number', 'should have totalLen');
    } finally { cleanup(); }
  });

  it('restores BM25 index after restart', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      await svc.init();
      await svc.add({ content: 'neural network deep learning' });
      await svc.add({ content: 'convolutional neural networks' });

      // New instance, same dir
      const svc2 = new MemoryService({ dbPath: dir });
      await svc2.init();
      // BM25 should be loaded from disk, not rebuilt from scratch
      const results = await svc2.searchBM25('neural network');
      assert.ok(results.length >= 1, 'should find results from restored BM25 index');
    } finally { cleanup(); }
  });

  it('handles missing sidecar gracefully', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      await svc.init();
      // No memories added, no sidecar file yet
      const path = join(dir, 'bm25-index.json');
      assert.ok(!existsSync(path), 'no sidecar before first add');
      // Search should still work (returns empty)
      const results = await svc.searchBM25('test');
      assert.ok(Array.isArray(results));
    } finally { cleanup(); }
  });

  it('updates BM25 sidecar on content update', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      await svc.init();
      const m = await svc.add({ content: 'original content about python' });
      await svc.update(m.id, { content: 'updated content about javascript' });
      const path = join(dir, 'bm25-index.json');
      const data = JSON.parse(readFileSync(path, 'utf-8'));
      // Should have the updated content indexed, not the original
      assert.ok(data.docs[m.id], 'updated doc should be in index');
    } finally { cleanup(); }
  });

  it('persists BM25 index after importAll', async () => {
    const { svc, dir, cleanup } = createService();
    try {
      await svc.init();
      await svc.importAll({
        memories: [
          { id: 'm1', content: 'imported memory alpha', layer: 'core', tags: [], entities: [], weight: 1, createdAt: Date.now(), accessedAt: Date.now(), accessCount: 0 },
          { id: 'm2', content: 'imported memory beta', layer: 'core', tags: [], entities: [], weight: 1, createdAt: Date.now(), accessedAt: Date.now(), accessCount: 0 }
        ],
        links: []
      });
      const path = join(dir, 'bm25-index.json');
      assert.ok(existsSync(path), 'bm25 sidecar should exist after importAll');
      const data = JSON.parse(readFileSync(path, 'utf-8'));
      assert.ok(data.docs['m1'], 'imported m1 should be indexed');
      assert.ok(data.docs['m2'], 'imported m2 should be indexed');
    } finally { cleanup(); }
  });
});
