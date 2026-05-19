import { Tracer } from './tracer.js';
import { PolicyEngine } from './policy-engine.js';
import { Evaluator, policyComplianceCheck, latencyCheck, reliabilityCheck, costEfficiencyCheck } from './evaluator.js';
export class AgentObserver {
    tracer;
    policyEngine;
    evaluator;
    rootSpanId = null;
    constructor() {
        this.tracer = new Tracer();
        this.policyEngine = new PolicyEngine();
        this.evaluator = new Evaluator();
        this.evaluator.addCheck('policy_compliance', policyComplianceCheck, 1.5);
        this.evaluator.addCheck('latency', latencyCheck, 1.0);
        this.evaluator.addCheck('reliability', reliabilityCheck, 2.0);
        this.evaluator.addCheck('cost_efficiency', costEfficiencyCheck, 1.0);
    }
    startRun(agentId, task) {
        const span = this.tracer.startSpan('agent.run', { agentId, task });
        this.rootSpanId = span.spanId;
        return span;
    }
    llmCall(model, prompt, completion, tokenUsage) {
        const span = this.tracer.startSpan('llm.call', {
            'gen_ai.request.model': model,
            'gen_ai.prompt': prompt,
            'gen_ai.completion': completion,
            promptTokens: tokenUsage?.promptTokens ?? 0,
            completionTokens: tokenUsage?.completionTokens ?? 0,
            totalTokens: (tokenUsage?.promptTokens ?? 0) + (tokenUsage?.completionTokens ?? 0),
        });
        this.tracer.endSpan(span.spanId);
        return span;
    }
    toolExecute(tool, input) {
        const policyResult = this.policyEngine.evaluate('tool_execution', { tool, command: input, input });
        const span = this.tracer.startSpan('tool.execute', {
            'tool.name': tool,
            'tool.input': input,
            policyDenied: !policyResult.allowed,
        });
        if (!policyResult.allowed) {
            span.status = 'error';
            span.attributes.policyViolations = policyResult.violations.map(v => v.reason);
        }
        this.tracer.endSpan(span.spanId, policyResult.allowed ? 'ok' : 'error');
        return { span, allowed: policyResult.allowed };
    }
    endRun() {
        if (!this.rootSpanId)
            return undefined;
        const span = this.tracer.endSpan(this.rootSpanId);
        this.rootSpanId = null;
        return span;
    }
    memoryOperation(type, attrs) {
        const span = this.tracer.startSpan(`memory.${type}`, attrs);
        this.tracer.endSpan(span.spanId);
        return span;
    }
    retrievalSearch(method, attrs) {
        const span = this.tracer.startSpan('retrieval.search', { method, ...attrs });
        this.tracer.endSpan(span.spanId);
        return span;
    }
    getReport() {
        const spans = this.tracer.getSpans();
        const evalResults = this.evaluator.evaluate(spans);
        return {
            traceReport: this.tracer.getTraceReport(),
            evalResults,
            aggregateScore: this.evaluator.aggregateScore(evalResults),
        };
    }
    getTracer() { return this.tracer; }
    getPolicyEngine() { return this.policyEngine; }
    getEvaluator() { return this.evaluator; }
    reportMarkdown() {
        const report = this.getReport();
        const lines = [];
        lines.push(`# Observability Report`);
        lines.push(``);
        lines.push(`**Trace:** ${report.traceReport.traceId.slice(0, 8)}...`);
        lines.push(`**Spans:** ${report.traceReport.totalSpans}`);
        lines.push(`**Errors:** ${report.traceReport.errorCount}`);
        lines.push(`**Duration:** ${report.traceReport.totalDurationMs.toFixed(1)}ms`);
        lines.push(`**Score:** ${(report.aggregateScore * 100).toFixed(0)}%`);
        lines.push(``);
        if (report.evalResults.length > 0) {
            lines.push(`## Evaluation`);
            for (const r of report.evalResults) {
                lines.push(`- **${r.dimension}:** ${(r.score * 100).toFixed(0)}% — ${r.reason}`);
            }
            lines.push(``);
        }
        if (report.traceReport.durationByOp) {
            lines.push(`## Duration by Operation`);
            for (const [op, dur] of Object.entries(report.traceReport.durationByOp)) {
                lines.push(`- ${op}: ${dur.toFixed(1)}ms`);
            }
        }
        return lines.join('\n');
    }
    spanStats() {
        const spans = this.tracer.getSpans();
        const byOperation = {};
        for (const s of spans) {
            byOperation[s.operation] = (byOperation[s.operation] ?? 0) + 1;
        }
        return {
            total: spans.length,
            completed: spans.filter(s => s.endTime !== null).length,
            errors: spans.filter(s => s.status === 'error').length,
            byOperation,
        };
    }
    observeSync(fn) {
        this.startRun('observer', 'observeSync');
        const result = fn();
        this.endRun();
        return { result, report: this.getReport() };
    }
    /** Observe with automatic policy-guarded tool execution */
    observeWithPolicy(fn, agentId = 'observer') {
        this.startRun(agentId, 'observeWithPolicy');
        const tool = (name, input) => {
            const { allowed, span } = this.toolExecute(name, input);
            return { allowed, reason: allowed ? undefined : String(span.attributes.policyViolations ?? 'denied') };
        };
        const result = fn({ tool });
        this.endRun();
        return { result, report: this.getReport() };
    }
    getErrorSummary() {
        const spans = this.tracer.getSpans();
        const errors = spans.filter(s => s.status === 'error');
        return errors.map(s => ({
            operation: s.operation,
            reason: String(s.attributes.policyViolations ?? s.attributes.error ?? 'unknown'),
        }));
    }
    /** Get error rate as a ratio (0-1) */
    getErrorRate() {
        const spans = this.tracer.getSpans();
        if (spans.length === 0)
            return 0;
        return spans.filter(s => s.status === 'error').length / spans.length;
    }
    /** Observe an async function with tracing */
    async observeAsync(fn, agentId = 'observer') {
        this.startRun(agentId, 'observeAsync');
        try {
            const result = await fn();
            this.endRun();
            return { result, report: this.getReport() };
        }
        catch (err) {
            this.endRun();
            throw err;
        }
    }
    /** Get the AgentObserver's root span ID */
    getRootSpanId() {
        return this.rootSpanId;
    }
    /** Quick health check: returns { healthy, errorRate, spanCount } */
    healthCheck(threshold = 0.1) {
        const errorRate = this.getErrorRate();
        return { healthy: errorRate <= threshold, errorRate, spanCount: this.tracer.spanCount() };
    }
    /** Reset observer state for reuse */
    reset() {
        this.tracer.reset();
        this.rootSpanId = null;
    }
}
