import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { AgentObserver } from '../src/index.js';
import { blockDestructiveOps } from '../src/policy-engine.js';

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

  it('generates markdown report', () => {
    const obs = new AgentObserver();
    obs.startRun('a7', 'report-test');
    obs.llmCall('gpt-4', 'prompt', 'response', { promptTokens: 50, completionTokens: 30 });
    obs.endRun();
    const md = obs.reportMarkdown();
    assert.ok(md.includes('Observability Report'));
    assert.ok(md.includes('**Spans:** 2'));
    assert.ok(md.includes('Evaluation'));
    assert.ok(md.includes('Duration by Operation'));
  });

  it('spanStats returns summary', () => {
    const obs = new AgentObserver();
    obs.startRun('a8', 'stats');
    obs.llmCall('gpt-4', 'hi', 'hello');
    const tool = obs.toolExecute('bash', 'ls');
    assert.equal(tool.allowed, true);
    obs.endRun();
    const stats = obs.spanStats();
    assert.equal(stats.total, 3);
    assert.equal(stats.completed, 3);
    assert.equal(stats.errors, 0);
    assert.equal(stats.byOperation['agent.run'], 1);
    assert.equal(stats.byOperation['llm.call'], 1);
    assert.equal(stats.byOperation['tool.execute'], 1);
  });

  it('observeSync wraps function and returns result with report', () => {
    const obs = new AgentObserver();
    const { result, report } = obs.observeSync(() => 42);
    assert.equal(result, 42);
    assert.ok(report.traceReport.totalSpans >= 1);
  });

  it('getErrorSummary returns error details', () => {
    const obs = new AgentObserver();
    obs.startRun('e1', 'test');
    obs.getPolicyEngine().addPolicy('tool_execution', blockDestructiveOps());
    obs.toolExecute('bash', 'rm -rf /'); // blocked by policy
    obs.endRun();
    const summary = obs.getErrorSummary();
    assert.equal(summary.length, 1);
    assert.equal(summary[0].operation, 'tool.execute');
  });

  it('observeWithPolicy provides guarded tool context', () => {
    const obs = new AgentObserver();
    obs.getPolicyEngine().addPolicy('tool_execution', blockDestructiveOps());
    const { result, report } = obs.observeWithPolicy((ctx) => {
      const r1 = ctx.tool('safe', 'echo hello');
      const r2 = ctx.tool('bash', 'rm -rf /');
      return { safe: r1.allowed, blocked: r2.allowed };
    }, 'test-agent');
    assert.strictEqual(result.safe, true);
    assert.strictEqual(result.blocked, false);
    assert.ok(report.aggregateScore > 0);
  });

  it('getErrorRate returns correct ratio', () => {
    const obs = new AgentObserver();
    obs.startRun('test', 'task');
    obs.toolExecute('safe', 'echo hi');
    obs.getPolicyEngine().addPolicy('tool_execution', blockDestructiveOps());
    obs.toolExecute('bash', 'rm -rf /');
    obs.endRun();
    // 3 spans: agent.run(ok), tool.execute(ok), tool.execute(error)
    assert.ok(obs.getErrorRate() > 0);
    assert.ok(obs.getErrorRate() <= 1);
  });
});
