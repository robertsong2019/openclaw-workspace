import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { Tracer } from '../src/tracer.js';
import { PolicyEngine } from '../src/policy-engine.js';
import { Evaluator, policyComplianceCheck, reliabilityCheck } from '../src/evaluator.js';

describe('Tracer.getOperationTimeline', () => {
  it('returns empty for no spans', () => {
    const t = new Tracer();
    assert.deepEqual(t.getOperationTimeline(), []);
  });

  it('returns spans sorted by startTime with durations', () => {
    const t = new Tracer();
    const s1 = t.startSpan('llm.call');
    const s2 = t.startSpan('tool.execute');
    t.endSpan(s1.spanId);
    t.endSpan(s2.spanId);
    const timeline = t.getOperationTimeline();
    assert.equal(timeline.length, 2);
    assert.equal(timeline[0].operation, 'llm.call');
    assert.equal(typeof timeline[0].durationMs, 'number');
    assert.ok(timeline[0].durationMs! >= 0);
    assert.equal(timeline[1].operation, 'tool.execute');
  });

  it('returns null duration for active spans', () => {
    const t = new Tracer();
    const s = t.startSpan('agent.run');
    const timeline = t.getOperationTimeline();
    assert.equal(timeline.length, 1);
    assert.equal(timeline[0].durationMs, null);
    assert.equal(timeline[0].status, 'unset');
    t.endSpan(s.spanId);
  });
});

describe('PolicyEngine.merge', () => {
  it('merges rules from another engine', () => {
    const e1 = new PolicyEngine();
    const e2 = new PolicyEngine();
    e1.addPolicy('tool_execution', {
      name: 'rule_a', description: 'A', category: 'tool_execution',
      evaluate: () => ({ allow: true }),
    });
    e2.addPolicy('tool_execution', {
      name: 'rule_b', description: 'B', category: 'tool_execution',
      evaluate: () => ({ allow: true }),
    });
    e2.addPolicy('data_privacy', {
      name: 'rule_c', description: 'C', category: 'data_privacy',
      evaluate: () => ({ allow: true }),
    });
    const added = e1.merge(e2);
    assert.equal(added, 2);
    assert.equal(e1.ruleCount('tool_execution'), 2);
    assert.equal(e1.ruleCount('data_privacy'), 1);
  });

  it('skips duplicate rule names', () => {
    const e1 = new PolicyEngine();
    const e2 = new PolicyEngine();
    const rule = { name: 'dup', description: 'D', category: 'x', evaluate: () => ({ allow: true } as any) };
    e1.addPolicy('x', rule);
    e2.addPolicy('x', { ...rule });
    const added = e1.merge(e2);
    assert.equal(added, 0);
  });
});

describe('Evaluator.runComparison', () => {
  it('detects regression between two span sets', () => {
    const ev = new Evaluator();
    ev.addCheck('reliability', reliabilityCheck, 1.0);
    // Baseline: all ok
    const tracer1 = new Tracer();
    const s1 = tracer1.startSpan('tool.execute');
    tracer1.endSpan(s1.spanId, 'ok');
    // Current: has errors
    const tracer2 = new Tracer();
    const s2 = tracer2.startSpan('tool.execute');
    tracer2.endSpan(s2.spanId, 'error');
    const comp = ev.runComparison(tracer1.getSpans(), tracer2.getSpans());
    assert.ok(comp.length >= 1);
    const reliability = comp.find(c => c.dimension === 'reliability');
    assert.ok(reliability);
    assert.ok(reliability.delta < 0);
    assert.equal(reliability.regression, true);
  });
});
