import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { Tracer } from '../src/tracer.js';

describe('Tracer', () => {
  it('creates a span with correct fields', () => {
    const tracer = new Tracer();
    const span = tracer.startSpan('agent.run', { agentId: 'a1' });
    assert.equal(span.operation, 'agent.run');
    assert.equal(span.parentSpanId, null);
    assert.equal(span.status, 'unset');
    assert.equal(span.endTime, null);
    assert.equal(span.attributes.agentId, 'a1');
    assert.ok(span.traceId);
    assert.ok(span.spanId);
  });

  it('ends a span and sets status', () => {
    const tracer = new Tracer();
    const span = tracer.startSpan('agent.run');
    const ended = tracer.endSpan(span.spanId, 'ok');
    assert.ok(ended);
    assert.equal(ended!.status, 'ok');
    assert.ok(ended!.endTime !== null);
  });

  it('creates parent-child relationships', () => {
    const tracer = new Tracer();
    const parent = tracer.startSpan('agent.run');
    const child = tracer.startSpan('llm.call');
    assert.equal(child.parentSpanId, parent.spanId);
    assert.equal(child.traceId, parent.traceId);
    tracer.endSpan(child.spanId);
    tracer.endSpan(parent.spanId);
  });

  it('tracks active span via stack', () => {
    const tracer = new Tracer();
    const s1 = tracer.startSpan('agent.run');
    assert.equal(tracer.getActiveSpan()?.spanId, s1.spanId);
    const s2 = tracer.startSpan('llm.call');
    assert.equal(tracer.getActiveSpan()?.spanId, s2.spanId);
    tracer.endSpan(s2.spanId);
    assert.equal(tracer.getActiveSpan()?.spanId, s1.spanId);
    tracer.endSpan(s1.spanId);
    assert.equal(tracer.getActiveSpan(), undefined);
  });

  it('adds events to spans', () => {
    const tracer = new Tracer();
    const span = tracer.startSpan('agent.run');
    tracer.addEvent(span.spanId, 'retry', { attempt: 2 });
    assert.equal(span.events.length, 1);
    assert.equal(span.events[0].name, 'retry');
    assert.equal(span.events[0].attributes?.attempt, 2);
  });

  it('generates trace report with summary stats', () => {
    const tracer = new Tracer();
    const s1 = tracer.startSpan('agent.run');
    const s2 = tracer.startSpan('llm.call');
    tracer.endSpan(s2.spanId);
    tracer.endSpan(s1.spanId, 'error');
    const report = tracer.getTraceReport();
    assert.equal(report.totalSpans, 2);
    assert.equal(report.errorCount, 1);
    assert.ok(report.durationByOp['agent.run'] > 0);
    assert.ok(report.durationByOp['llm.call'] > 0);
  });

  it('exports and imports traces preserving traceId', () => {
    const tracer = new Tracer();
    const span = tracer.startSpan('agent.run');
    tracer.endSpan(span.spanId);
    const json = tracer.exportJSON();
    const parsed = JSON.parse(json);
    assert.ok(parsed.traceId);
    assert.equal(parsed.spans.length, 1);
    assert.equal(parsed.spans[0].operation, 'agent.run');
    // Import into new tracer
    const tracer2 = new Tracer();
    tracer2.importJSON(json);
    assert.equal(tracer2.spanCount(), 1);
    assert.equal(tracer2.getSpans()[0].operation, 'agent.run');
  });

  it('finds spans by predicate', () => {
    const tracer = new Tracer();
    tracer.startSpan('agent.run');
    tracer.startSpan('llm.call');
    tracer.startSpan('llm.call');
    const llmSpans = tracer.findSpans(s => s.operation === 'llm.call');
    assert.equal(llmSpans.length, 2);
  });

  it('finds spans by operation', () => {
    const tracer = new Tracer();
    tracer.startSpan('agent.run');
    tracer.startSpan('llm.call');
    assert.equal(tracer.findSpansByOperation('llm.call').length, 1);
    assert.equal(tracer.findSpansByOperation('tool.execute').length, 0);
  });

  it('gets span by id', () => {
    const tracer = new Tracer();
    const span = tracer.startSpan('agent.run');
    assert.equal(tracer.getSpanById(span.spanId)?.operation, 'agent.run');
    assert.equal(tracer.getSpanById('nonexistent'), undefined);
  });

  it('reports span count', () => {
    const tracer = new Tracer();
    assert.equal(tracer.spanCount(), 0);
    tracer.startSpan('agent.run');
    assert.equal(tracer.spanCount(), 1);
  });

  it('getChildren returns direct child spans', () => {
    const tracer = new Tracer();
    const parent = tracer.startSpan('agent.run');
    const c1 = tracer.startSpan('llm.call');
    tracer.endSpan(c1.spanId);
    // Must end c1 before starting c2 so c2's parent is root, not c1
    const c2 = tracer.startSpan('tool.execute');
    tracer.endSpan(c2.spanId);
    tracer.endSpan(parent.spanId);
    const kids = tracer.getChildren(parent.spanId);
    assert.equal(kids.length, 2);
    assert.ok(kids.some(k => k.operation === 'llm.call'));
    assert.ok(kids.some(k => k.operation === 'tool.execute'));
  });

  it('getChildren returns empty for leaf span', () => {
    const tracer = new Tracer();
    const span = tracer.startSpan('agent.run');
    tracer.endSpan(span.spanId);
    assert.equal(tracer.getChildren(span.spanId).length, 0);
  });

  it('getSpanTree builds full hierarchy', () => {
    const tracer = new Tracer();
    const root = tracer.startSpan('agent.run');
    const c1 = tracer.startSpan('llm.call');
    tracer.endSpan(c1.spanId);
    const c2 = tracer.startSpan('tool.execute');
    const gc = tracer.startSpan('llm.call');
    tracer.endSpan(gc.spanId);
    tracer.endSpan(c2.spanId);
    tracer.endSpan(root.spanId);
    const tree = tracer.getSpanTree();
    assert.equal(tree.length, 1);
    assert.equal(tree[0].operation, 'agent.run');
    assert.equal(tree[0].children.length, 2);
    const toolNode = tree[0].children.find(c => c.operation === 'tool.execute');
    assert.ok(toolNode);
    assert.equal(toolNode!.children.length, 1);
    assert.equal(toolNode!.children[0].operation, 'llm.call');
  });

  it('getSpanTree with spanId returns subtree', () => {
    const tracer = new Tracer();
    const root = tracer.startSpan('agent.run');
    const c1 = tracer.startSpan('tool.execute');
    const gc = tracer.startSpan('llm.call');
    tracer.endSpan(gc.spanId);
    tracer.endSpan(c1.spanId);
    tracer.endSpan(root.spanId);
    const subtree = tracer.getSpanTree(c1.spanId);
    assert.equal(subtree.length, 1);
    assert.equal(subtree[0].operation, 'tool.execute');
    assert.equal(subtree[0].children.length, 1);
  });
});
