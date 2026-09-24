import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService, MemoryExtractor } from '../src/index.js';
import { mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'guards-'));
  return new MemoryService({ dbPath: dir });
}

describe('MemoryService constructor guards (09-04 incident fix, previously untested)', () => {
  it('rejects non-object options (string dbPath legacy form)', () => {
    assert.throws(
      () => new MemoryService('./data/memory'),
      /expected an options object/
    );
  });

  it('rejects null options', () => {
    assert.throws(() => new MemoryService(null), /expected an options object/);
  });

  it('rejects array options', () => {
    assert.throws(() => new MemoryService(['dbPath']), /expected an options object/);
  });

  it('rejects unknown options, naming the offender', () => {
    assert.throws(
      () => new MemoryService({ dataDir: '/x' }),
      /unknown option\(s\) 'dataDir'/
    );
  });

  it('rejects the known 2026-09-04 incident aliases', () => {
    assert.throws(() => new MemoryService({ dir: '/x' }), /unknown option\(s\) 'dir'/);
  });
});

describe('MemoryExtractor user context-fact branch (20 < len < 500, no other memories)', () => {
  const x = new MemoryExtractor();

  it('keeps substantial user text as low-confidence context when nothing else matched', () => {
    const text = 'the quick brown fox jumps over the lazy dog near the riverbank each evening, quick brown fox again';
    assert.ok(text.length > 20 && text.length < 500);
    const out = x.extract(text, 'user');
    assert.ok(out.length >= 1);
    const ctx = out.find(m => m.type === 'context');
    assert.ok(ctx, 'expected a context-type memory');
    assert.equal(ctx.confidence, 0.3);
    assert.equal(ctx.content, text.trim());
  });

  it('skips context memory when text is too short (<=20 chars)', () => {
    const out = x.extract('just a short note', 'user');
    assert.equal(out.find(m => m.type === 'context'), undefined);
  });

  it('skips context memory when text is too long (>=500 chars)', () => {
    const text = 'x'.repeat(500);
    const out = x.extract(text, 'user');
    assert.equal(out.find(m => m.type === 'context'), undefined);
  });

  it('skips context memory for assistant role', () => {
    const text = 'assistant reply without markers, quick brown fox jumps near the riverbank each evening';
    const out = x.extract(text, 'assistant');
    assert.equal(out.find(m => m.type === 'context'), undefined);
  });
});

describe('extractHybrid ngram dedupe (>0.8 similarity collapses near-duplicates)', () => {
  it('drops LLM result that is a near-duplicate of a rule-based hit', async () => {
    const x = new MemoryExtractor();
    const ruleHit = 'user prefers dark mode for night coding sessions and hates bright screens';
    const llmHit = 'user prefers dark mode for night coding sessions and hates bright screenz';
    const llmFn = async () => [{ content: llmHit, type: 'preference', confidence: 0.9, entities: [] }];
    const out = await x.extractHybrid(ruleHit, llmFn);
    assert.equal(out.length, 1, 'near-duplicate LLM hit should be collapsed into the rule-based one');
    assert.match(out[0].content, /dark mode/);
  });

  it('keeps genuinely different LLM results', async () => {
    const x = new MemoryExtractor();
    const ruleHit = 'user prefers dark mode for night coding sessions and hates bright screens';
    const llmHit = 'totally unrelated fact about the kubernetes cluster in the basement';
    const llmFn = async () => [{ content: llmHit, type: 'fact', confidence: 0.9, entities: [] }];
    const out = await x.extractHybrid(ruleHit, llmFn);
    assert.equal(out.length, 2);
  });
});

describe('merge layer resolution pins', () => {
  it('opts.layer overrides merged layer', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'keeper', layer: 'short', tags: [] });
    const b = await svc.add({ content: 'absorbed', layer: 'short', tags: [] });
    const m = await svc.merge(a.id, b.id, { layer: 'core' });
    assert.equal(m.layer, 'core');
  });

  it('stronger absorbed layer wins without override', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'keeper', layer: 'short', tags: [] });
    const b = await svc.add({ content: 'absorbed', layer: 'core', tags: [] });
    const m = await svc.merge(a.id, b.id);
    assert.equal(m.layer, 'core');
  });
});
