import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

describe('Opinion Network', () => {
  let ms, dir;

  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), 'opinion-'));
    ms = new MemoryService({ dbPath: dir });
  });

  describe('addOpinion(topic, content, opts)', () => {
    it('creates an opinion memory with confidence and topic', async () => {
      const opinion = await ms.addOpinion('typescript', 'TypeScript is the best language for large projects', { confidence: 0.8 });
      assert.equal(opinion.factType, 'opinion');
      assert.equal(opinion._topic, 'typescript');
      assert.equal(opinion._confidence, 0.8);
      assert.equal(opinion.layer, 'long');
    });

    it('defaults confidence to 0.5 and layer to long', async () => {
      const opinion = await ms.addOpinion('rust', 'Rust has a steep learning curve');
      assert.equal(opinion._confidence, 0.5);
      assert.equal(opinion.layer, 'long');
    });

    it('clamps confidence to [0, 1]', async () => {
      const o1 = await ms.addOpinion('x', 'test', { confidence: -0.5 });
      assert.equal(o1._confidence, 0);
      const o2 = await ms.addOpinion('y', 'test', { confidence: 1.5 });
      assert.equal(o2._confidence, 1);
    });

    it('supports custom tags, entities, source', async () => {
      const opinion = await ms.addOpinion('python', 'Python is great for ML', {
        confidence: 0.9,
        tags: ['programming', 'ml'],
        entities: ['python'],
        source: 'experience'
      });
      assert.deepEqual(opinion.tags, ['programming', 'ml']);
      assert.deepEqual(opinion.entities, ['python']);
      assert.equal(opinion.source, 'experience');
    });
  });

  describe('searchOpinions(topic, opts)', () => {
    it('returns opinions filtered by topic sorted by confidence desc', async () => {
      await ms.addOpinion('ai', 'AI will change everything', { confidence: 0.9 });
      await ms.addOpinion('ai', 'AI is overhyped', { confidence: 0.3 });
      await ms.addOpinion('rust', 'Rust is great'); // different topic

      const results = await ms.searchOpinions('ai');
      assert.equal(results.length, 2);
      assert.ok(results[0]._confidence >= results[1]._confidence);
      assert.equal(results[0]._confidence, 0.9);
    });

    it('filters by minConfidence', async () => {
      await ms.addOpinion('test', 'high conf', { confidence: 0.9 });
      await ms.addOpinion('test', 'low conf', { confidence: 0.2 });

      const results = await ms.searchOpinions('test', { minConfidence: 0.5 });
      assert.equal(results.length, 1);
      assert.equal(results[0]._confidence, 0.9);
    });

    it('returns empty for unknown topic', async () => {
      const results = await ms.searchOpinions('nonexistent');
      assert.equal(results.length, 0);
    });

    it('respects limit option', async () => {
      for (let i = 0; i < 5; i++) {
        await ms.addOpinion('lim', `opinion ${i}`, { confidence: 0.5 + i * 0.1 });
      }
      const results = await ms.searchOpinions('lim', { limit: 3 });
      assert.equal(results.length, 3);
    });

    it('only returns opinion-typed memories', async () => {
      await ms.add({ content: 'TypeScript compiles to JS', factType: 'world' });
      await ms.addOpinion('typescript', 'TypeScript is amazing', { confidence: 0.8 });

      const results = await ms.searchOpinions('typescript');
      assert.equal(results.length, 1);
      assert.equal(results[0].factType, 'opinion');
    });
  });

  describe('evolveConfidence(id, delta, opts)', () => {
    it('adjusts confidence by delta and clamps to [0, 1]', async () => {
      const opinion = await ms.addOpinion('test', 'Test opinion', { confidence: 0.5 });
      const evolved = await ms.evolveConfidence(opinion.id, 0.3);
      assert.equal(evolved._confidence, 0.8);
    });

    it('clamps at 1.0 for large positive delta', async () => {
      const opinion = await ms.addOpinion('test', 'Test', { confidence: 0.9 });
      const evolved = await ms.evolveConfidence(opinion.id, 0.5);
      assert.equal(evolved._confidence, 1);
    });

    it('clamps at 0.0 for large negative delta', async () => {
      const opinion = await ms.addOpinion('test', 'Test', { confidence: 0.1 });
      const evolved = await ms.evolveConfidence(opinion.id, -0.5);
      assert.equal(evolved._confidence, 0);
    });

    it('throws for non-existent id', async () => {
      await assert.rejects(() => ms.evolveConfidence('nonexistent', 0.1), /not found/);
    });

    it('records evidence in confidenceHistory', async () => {
      const opinion = await ms.addOpinion('test', 'Test', { confidence: 0.5 });
      const evolved = await ms.evolveConfidence(opinion.id, 0.2, { evidence: 'New study shows positive results' });
      assert.ok(Array.isArray(evolved._confidenceHistory));
      assert.equal(evolved._confidenceHistory.length, 1);
      assert.equal(evolved._confidenceHistory[0].delta, 0.2);
      assert.equal(evolved._confidenceHistory[0].evidence, 'New study shows positive results');
      assert.ok(evolved._confidenceHistory[0].timestamp);
    });

    it('accumulates multiple confidence changes', async () => {
      const opinion = await ms.addOpinion('test', 'Test', { confidence: 0.5 });
      await ms.evolveConfidence(opinion.id, 0.2);
      const final = await ms.evolveConfidence(opinion.id, -0.1, { evidence: 'Counter-evidence found' });

      assert.equal(final._confidence, 0.6); // 0.5 + 0.2 - 0.1
      assert.equal(final._confidenceHistory.length, 2);
    });

    it('throws when trying to evolve non-opinion memory', async () => {
      const mem = await ms.add({ content: 'A fact', factType: 'world' });
      await assert.rejects(() => ms.evolveConfidence(mem.id, 0.1), /not an opinion/);
    });
  });
});
