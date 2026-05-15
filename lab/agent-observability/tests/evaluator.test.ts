import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { Evaluator, policyComplianceCheck, latencyCheck, reliabilityCheck, costEfficiencyCheck } from '../src/evaluator.js';
import type { Span } from '../src/tracer.js';

function makeSpan(overrides: Partial<Span> = {}): Span {
  return {
    traceId: 't1',
    spanId: 's1',
    parentSpanId: null,
    operation: 'agent.run',
    startTime: 0,
    endTime: 100,
    attributes: {},
    status: 'ok',
    events: [],
    ...overrides,
  };
}

describe('Evaluator', () => {
  it('returns empty results with no checks', () => {
    const ev = new Evaluator();
    const results = ev.evaluate([makeSpan()]);
    assert.equal(results.length, 0);
  });

  it('runs added checks', () => {
    const ev = new Evaluator();
    ev.addCheck('test', () => [{ dimension: 'test', score: 0.9, reason: 'looks good' }]);
    const results = ev.evaluate([makeSpan()]);
    assert.equal(results.length, 1);
    assert.equal(results[0].score, 0.9);
  });

  it('computes weighted aggregate score', () => {
    const ev = new Evaluator();
    ev.addCheck('a', () => [{ dimension: 'a', score: 1.0, reason: '' }], 2.0);
    ev.addCheck('b', () => [{ dimension: 'b', score: 0.0, reason: '' }], 1.0);
    const results = ev.evaluate([makeSpan()]);
    const agg = ev.aggregateScore(results);
    assert.equal(agg, 2 / 3); // (1*2 + 0*1) / (2+1)
  });

  it('policy_compliance scores 1 when no blocks', () => {
    const spans = [makeSpan({ operation: 'tool.execute', attributes: {} })];
    const results = policyComplianceCheck(spans);
    assert.equal(results[0].score, 1);
  });

  it('policy_compliance degrades on blocks', () => {
    const spans = [
      makeSpan({ spanId: 's1', operation: 'tool.execute', status: 'ok' }),
      makeSpan({ spanId: 's2', operation: 'tool.execute', status: 'error', attributes: { policyDenied: true } }),
    ];
    const results = policyComplianceCheck(spans);
    assert.equal(results[0].score, 0.5);
  });

  it('reliability scores based on error ratio', () => {
    const spans = [
      makeSpan({ spanId: 's1', status: 'ok' }),
      makeSpan({ spanId: 's2', status: 'error' }),
    ];
    const results = reliabilityCheck(spans);
    assert.equal(results[0].score, 0.5);
  });

  it('cost_efficiency scores based on token usage', () => {
    const spans = [makeSpan({ operation: 'llm.call', attributes: { totalTokens: 500 } })];
    const results = costEfficiencyCheck(spans);
    assert.equal(results[0].score, 1);
  });

  it('lists registered check names', () => {
    const ev = new Evaluator();
    ev.addCheck('a', () => []);
    ev.addCheck('b', () => []);
    assert.deepEqual(ev.listChecks(), ['a', 'b']);
  });

  it('removes a check by name', () => {
    const ev = new Evaluator();
    ev.addCheck('a', () => [{ dimension: 'a', score: 1, reason: '' }]);
    ev.removeCheck('a');
    assert.equal(ev.evaluate([makeSpan()]).length, 0);
  });

  it('aggregateScore returns 0 for empty results', () => {
    const ev = new Evaluator();
    assert.equal(ev.aggregateScore([]), 0);
  });
});
