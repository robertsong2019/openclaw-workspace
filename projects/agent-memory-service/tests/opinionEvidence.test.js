import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

describe('Opinion Evidence Evolution', () => {
  let ms, dir;

  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), 'evidence-'));
    ms = new MemoryService({ dbPath: dir });
  });

  describe('opinionEvolveFromEvidence(topic, evidence, delta)', () => {
    it('evolves all opinions on a topic', async () => {
      await ms.addOpinion('ai', 'AI is great', { confidence: 0.5 });
      await ms.addOpinion('ai', 'AI is decent', { confidence: 0.6 });
      const result = await ms.opinionEvolveFromEvidence('ai', 'New GPT-5 benchmark results', 0.2);
      assert.equal(result.evolved, 2);
      assert.equal(result.topic, 'ai');
      // searchOpinions returns sorted by confidence desc
      // so 0.6 (now 0.8) comes first, then 0.5 (now 0.7)
      const drift1 = await ms.opinionDrift(result.opinions[0].id);
      assert.equal(drift1.current, 0.8); // 0.6 + 0.2
      const drift2 = await ms.opinionDrift(result.opinions[1].id);
      assert.equal(drift2.current, 0.7); // 0.5 + 0.2
    });

    it('returns empty for unknown topic', async () => {
      const result = await ms.opinionEvolveFromEvidence('none', 'nothing', 0.1);
      assert.equal(result.evolved, 0);
      assert.equal(result.opinions.length, 0);
    });

    it('records evidence in all opinion histories', async () => {
      await ms.addOpinion('py', 'Python is ok', { confidence: 0.5 });
      await ms.addOpinion('py', 'Python is good', { confidence: 0.7 });
      await ms.opinionEvolveFromEvidence('py', 'Python 4.0 announced', 0.15);
      for (const o of await ms.searchOpinions('py')) {
        const drift = await ms.opinionDrift(o.id);
        assert.equal(drift.history.length, 1);
        assert.equal(drift.history[0].evidence, 'Python 4.0 announced');
      }
    });

    it('respects confidence clamping during batch evolution', async () => {
      await ms.addOpinion('x', 'Already high', { confidence: 0.95 });
      const result = await ms.opinionEvolveFromEvidence('x', 'Big boost', 0.5);
      assert.equal(result.opinions[0]._confidence, 1); // clamped at 1
    });

    it('negative delta reduces all confidences', async () => {
      await ms.addOpinion('test', 'Opinion A', { confidence: 0.7 });
      await ms.addOpinion('test', 'Opinion B', { confidence: 0.8 });
      const result = await ms.opinionEvolveFromEvidence('test', 'Scandal revealed', -0.3);
      assert.equal(result.opinions[0]._confidence, 0.5); // was 0.8 - 0.3
      assert.equal(result.opinions[1]._confidence, 0.4); // was 0.7 - 0.3
    });
  });
});
