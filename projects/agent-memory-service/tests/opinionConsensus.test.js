import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

describe('Opinion Consensus & Drift', () => {
  let ms, dir;

  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), 'consensus-'));
    ms = new MemoryService({ dbPath: dir });
  });

  describe('opinionConsensus(topic)', () => {
    it('returns empty consensus for unknown topic', async () => {
      const c = await ms.opinionConsensus('unknown');
      assert.equal(c.count, 0);
      assert.equal(c.avgConfidence, 0);
      assert.equal(c.majority, 'mixed');
    });

    it('computes consensus for single opinion', async () => {
      await ms.addOpinion('py', 'Python is great', { confidence: 0.9 });
      const c = await ms.opinionConsensus('py');
      assert.equal(c.count, 1);
      assert.equal(c.avgConfidence, 0.9);
      assert.equal(c.divergence, 0);
      assert.equal(c.majority, 'for');
    });

    it('computes consensus with divergence for mixed opinions', async () => {
      await ms.addOpinion('ai', 'AI is great', { confidence: 0.9 });
      await ms.addOpinion('ai', 'AI is overhyped', { confidence: 0.2 });
      const c = await ms.opinionConsensus('ai');
      assert.equal(c.count, 2);
      assert.equal(c.avgConfidence, 0.55);
      assert.ok(c.divergence > 0);
      assert.equal(c.majority, 'mixed');
    });

    it('detects majority for unanimous high confidence', async () => {
      await ms.addOpinion('ts', 'TS is excellent', { confidence: 0.85 });
      await ms.addOpinion('ts', 'TS rocks', { confidence: 0.95 });
      const c = await ms.opinionConsensus('ts');
      assert.equal(c.majority, 'for');
    });

    it('detects against majority for low confidence opinions', async () => {
      await ms.addOpinion('x', 'X is bad', { confidence: 0.1 });
      await ms.addOpinion('x', 'X is terrible', { confidence: 0.2 });
      const c = await ms.opinionConsensus('x');
      assert.equal(c.majority, 'against');
    });
  });

  describe('opinionDrift(id)', () => {
    it('returns empty history for newly created opinion', async () => {
      const o = await ms.addOpinion('test', 'Test', { confidence: 0.5 });
      const drift = await ms.opinionDrift(o.id);
      assert.equal(drift.current, 0.5);
      assert.deepEqual(drift.history, []);
    });

    it('tracks confidence changes over time', async () => {
      const o = await ms.addOpinion('test', 'Test', { confidence: 0.5 });
      await ms.evolveConfidence(o.id, 0.2, { evidence: 'evidence A' });
      await ms.evolveConfidence(o.id, -0.1, { evidence: 'evidence B' });
      const drift = await ms.opinionDrift(o.id);
      assert.equal(drift.current, 0.6);
      assert.equal(drift.history.length, 2);
      assert.equal(drift.history[0].delta, 0.2);
      assert.equal(drift.history[1].delta, -0.1);
      assert.equal(drift.history[0].evidence, 'evidence A');
    });

    it('throws for non-opinion memory', async () => {
      const m = await ms.add({ content: 'A fact', factType: 'world' });
      await assert.rejects(() => ms.opinionDrift(m.id), /not an opinion/);
    });
  });
});
