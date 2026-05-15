import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { AgentObserver } from '../src/index.js';

describe('AgentObserver integration', () => {
  it('runs a complete agent workflow', () => {
    const obs = new AgentObserver();
    obs.getPolicyEngine().addPolicy('tool_execution', {
      name: 'block_rm',
      description: '',
      category: 'tool_execution',
      evaluate: (input) => {
        const cmd = String(input.command ?? '');
        return cmd.includes('rm ') ? { allow: false, reason: 'destructive' } : { allow: true };
      },
    });

    // Start run
    obs.startRun('agent-1', 'Summarize the document');

    // LLM call
    const llm = obs.llmCall('gpt-4', 'Summarize', 'Here is the summary', {
      promptTokens: 100,
      completionTokens: 50,
    });
    assert.equal(llm.operation, 'llm.call');
    assert.equal(llm.attributes.totalTokens, 150);

    // Safe tool call
    const safe = obs.toolExecute('bash', 'ls -la');
    assert.equal(safe.allowed, true);
    assert.equal(safe.span.status, 'ok');

    // Blocked tool call
    const blocked = obs.toolExecute('bash', 'rm -rf /tmp/test');
    assert.equal(blocked.allowed, false);
    assert.equal(blocked.span.status, 'error');

    // End run
    const root = obs.endRun();
    assert.ok(root);
    assert.equal(root!.status, 'ok');

    // Report
    const report = obs.getReport();
    assert.equal(report.traceReport.totalSpans, 4); // root + llm + 2 tools
    assert.ok(report.evalResults.length >= 1);
    assert.ok(report.aggregateScore >= 0 && report.aggregateScore <= 1);
  });

  it('produces valid trace report after run', () => {
    const obs = new AgentObserver();
    obs.startRun('a2', 'test task');
    obs.llmCall('claude', 'hello', 'hi');
    obs.endRun();

    const report = obs.getReport();
    assert.equal(report.traceReport.spans.length, 2);
    assert.ok(report.traceReport.totalDurationMs > 0);
  });

  it('evaluates across all built-in dimensions', () => {
    const obs = new AgentObserver();
    obs.startRun('a3', 'task');
    obs.llmCall('gpt-4', 'prompt', 'answer', { promptTokens: 10, completionTokens: 10 });
    obs.toolExecute('read', 'file.txt');
    obs.endRun();

    const { evalResults } = obs.getReport();
    const dimensions = new Set(evalResults.map(r => r.dimension));
    assert.ok(dimensions.has('policy_compliance'));
    assert.ok(dimensions.has('latency'));
    assert.ok(dimensions.has('reliability'));
    assert.ok(dimensions.has('cost_efficiency'));
  });

  it('records memory operations', () => {
    const obs = new AgentObserver();
    obs.startRun('a4', 'memory task');
    const mem = obs.memoryOperation('read', { key: 'user_context' });
    assert.equal(mem.operation, 'memory.read');
    assert.equal(mem.attributes.key, 'user_context');
    obs.endRun();
    assert.equal(obs.getReport().traceReport.totalSpans, 2);
  });

  it('records retrieval operations', () => {
    const obs = new AgentObserver();
    obs.startRun('a5', 'search');
    const ret = obs.retrievalSearch('vector', { query: 'test', topK: 5 });
    assert.equal(ret.operation, 'retrieval.search');
    assert.equal(ret.attributes.topK, 5);
    obs.endRun();
    assert.equal(obs.getReport().traceReport.totalSpans, 2);
  });

  it('accesses tracer convenience methods', () => {
    const obs = new AgentObserver();
    obs.startRun('a6', 'conv');
    obs.llmCall('gpt-4', 'hi', 'hello');
    obs.endRun();
    assert.equal(obs.getTracer().spanCount(), 2);
    assert.equal(obs.getTracer().findSpansByOperation('llm.call').length, 1);
  });
});
