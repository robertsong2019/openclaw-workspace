import { Tracer } from './tracer.js';
import type { Span } from './tracer.js';
import { PolicyEngine } from './policy-engine.js';
import { Evaluator } from './evaluator.js';
import type { EvalCheckResult } from './evaluator.js';
export interface ObservabilityReport {
    traceReport: ReturnType<Tracer['getTraceReport']>;
    evalResults: EvalCheckResult[];
    aggregateScore: number;
}
export declare class AgentObserver {
    private tracer;
    private policyEngine;
    private evaluator;
    private rootSpanId;
    constructor();
    startRun(agentId: string, task: string): Span;
    llmCall(model: string, prompt: string, completion: string, tokenUsage?: {
        promptTokens: number;
        completionTokens: number;
    }): Span;
    toolExecute(tool: string, input: string): {
        span: Span;
        allowed: boolean;
    };
    endRun(): Span | undefined;
    memoryOperation(type: 'read' | 'write', attrs: Record<string, unknown>): Span;
    retrievalSearch(method: string, attrs: Record<string, unknown>): Span;
    getReport(): ObservabilityReport;
    getTracer(): Tracer;
    getPolicyEngine(): PolicyEngine;
    getEvaluator(): Evaluator;
    reportMarkdown(): string;
    spanStats(): {
        total: number;
        completed: number;
        errors: number;
        byOperation: Record<string, number>;
    };
    observeSync<T>(fn: () => T): {
        result: T;
        report: ObservabilityReport;
    };
    /** Observe with automatic policy-guarded tool execution */
    observeWithPolicy<T>(fn: (ctx: {
        tool: (name: string, input: string) => {
            allowed: boolean;
            reason?: string;
        };
    }) => T, agentId?: string): {
        result: T;
        report: ObservabilityReport;
    };
    getErrorSummary(): Array<{
        operation: string;
        reason: string;
    }>;
    /** Get error rate as a ratio (0-1) */
    getErrorRate(): number;
    /** Observe an async function with tracing */
    observeAsync<T>(fn: () => Promise<T>, agentId?: string): Promise<{
        result: T;
        report: ObservabilityReport;
    }>;
    /** Get the AgentObserver's root span ID */
    getRootSpanId(): string | null;
    /** Quick health check: returns { healthy, errorRate, spanCount } */
    healthCheck(threshold?: number): {
        healthy: boolean;
        errorRate: number;
        spanCount: number;
    };
    /** Reset observer state for reuse */
    reset(): void;
}
