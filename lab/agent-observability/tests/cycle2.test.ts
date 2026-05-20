import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { Tracer } from '../src/tracer.js';
import { PolicyEngine } from '../src/policy-engine.js';
import { AgentObserver } from '../src/index.js';

describe('Tracer.annotate', () => {
  it('adds multiple attributes to a span', () => {
    const t = new Tracer();
    const s = t.startSpan('llm.call');
    const ok = t.annotate(s.spanId, { model: 'gpt-4', tokens: 42 });
    assert.equal(ok, true);
    assert.equal(s.attributes.model, 'gpt-4');
    assert.equal(s.attributes.tokens, 42);
    t.endSpan(s.spanId);
  });

  it('returns false for missing span', () => {
    const t = new Tracer();
    assert.equal(t.annotate('nope', { a: 1 }), false);
  });
});

describe('PolicyEngine.evaluateWithDetails', () => {
  it('returns per-rule details', () => {
    const pe = new PolicyEngine();
    pe.addPolicy('tool_execution', {
      name: 'allow_all', description: 'Allow', category: 'tool_execution',
      evaluate: () => ({ allow: true }),
    });
    pe.addPolicy('tool_execution', {
      name: 'block_rm', description: 'Block rm', category: 'tool_execution',
      evaluate: (input) => {
        const cmd = String(input.command ?? '');
        return cmd.includes('rm') ? { allow: false, reason: 'destructive' } : { allow: true };
      },
    });
    const r1 = pe.evaluateWithDetails('tool_execution', { command: 'ls' });
    assert.equal(r1.allowed, true);
    assert.equal(r1.details.length, 2);
    assert.equal(r1.details[1].allowed, true);

    const r2 = pe.evaluateWithDetails('tool_execution', { command: 'rm -rf /' });
    assert.equal(r2.allowed, false);
    assert.equal(r2.details[1].reason, 'destructive');
  });

  it('handles disabled rules', () => {
    const pe = new PolicyEngine();
    pe.addPolicy('x', {
      name: 'r1', description: 'R', category: 'x',
      evaluate: () => ({ allow: false }),
    });
    pe.disableRule('x', 'r1');
    const r = pe.evaluateWithDetails('x', {});
    assert.equal(r.allowed, true);
    assert.equal(r.details[0].reason, 'disabled');
  });
});

describe('AgentObserver.traceAgent', () => {
  it('wraps a function in startRun/endRun', () => {
    const obs = new AgentObserver();
    const { result, report } = obs.traceAgent('test-agent', 'do stuff', () => 42);
    assert.equal(result, 42);
    assert.ok(report.traceReport.totalSpans >= 1);
    assert.equal(report.traceReport.totalSpans, 1);
  });

  it('ends run even if fn throws', () => {
    const obs = new AgentObserver();
    assert.throws(() => obs.traceAgent('fail', 'crash', () => {
      throw new Error('boom');
    }));
    // Should still have the root span ended
    assert.equal(obs.getSpanCount(), 1);
  });
});
