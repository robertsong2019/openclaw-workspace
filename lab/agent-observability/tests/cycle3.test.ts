import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { Tracer } from '../src/tracer.js';
import { PolicyEngine } from '../src/policy-engine.js';
import { Evaluator } from '../src/evaluator.js';

describe('Tracer.getStats', () => {
  it('returns zeros for empty tracer', () => {
    const t = new Tracer();
    const stats = t.getStats();
    assert.equal(stats.total, 0);
    assert.equal(stats.active, 0);
    assert.equal(stats.completed, 0);
    assert.equal(stats.errors, 0);
    assert.equal(stats.avgDurationMs, 0);
  });

  it('counts active, completed, and errors correctly', () => {
    const t = new Tracer();
    const s1 = t.startSpan('llm.call');
    const s2 = t.startSpan('tool.execute');
    t.endSpan(s1.spanId, 'ok');
    t.endSpan(s2.spanId, 'error');
    const s3 = t.startSpan('agent.run'); // active
    const stats = t.getStats();
    assert.equal(stats.total, 3);
    assert.equal(stats.active, 1);
    assert.equal(stats.completed, 2);
    assert.equal(stats.errors, 1);
    assert.ok(stats.avgDurationMs >= 0);
    t.endSpan(s3.spanId);
  });
});

describe('PolicyEngine.countByCategory', () => {
  it('returns empty for no rules', () => {
    const pe = new PolicyEngine();
    assert.deepEqual(pe.countByCategory(), {});
  });

  it('counts rules per category', () => {
    const pe = new PolicyEngine();
    const mkRule = (n: string, cat: string) => ({
      name: n, description: n, category: cat,
      evaluate: () => ({ allow: true } as any),
    });
    pe.addPolicy('a', mkRule('r1', 'a'));
    pe.addPolicy('a', mkRule('r2', 'a'));
    pe.addPolicy('b', mkRule('r3', 'b'));
    const counts = pe.countByCategory();
    assert.equal(counts.a, 2);
    assert.equal(counts.b, 1);
  });
});

describe('Evaluator.getWeights', () => {
  it('returns configured weights', () => {
    const ev = new Evaluator();
    ev.addCheck('latency', () => [], 2.5);
    ev.addCheck('reliability', () => [], 1.0);
    const w = ev.getWeights();
    assert.equal(w.get('latency'), 2.5);
    assert.equal(w.get('reliability'), 1.0);
  });
});
