export type SpanStatus = 'ok' | 'error' | 'unset';
export type SpanOperation = 'agent.run' | 'llm.call' | 'tool.execute' | 'retrieval.search' | 'memory.read' | 'memory.write';
export interface SpanEvent {
    name: string;
    timestamp: number;
    attributes?: Record<string, unknown>;
}
export interface Span {
    traceId: string;
    spanId: string;
    parentSpanId: string | null;
    operation: SpanOperation;
    startTime: number;
    endTime: number | null;
    attributes: Record<string, unknown>;
    status: SpanStatus;
    events: SpanEvent[];
}
export interface SpanTreeNode extends Span {
    children: SpanTreeNode[];
}
export interface TraceReport {
    traceId: string;
    spans: Span[];
    totalSpans: number;
    durationByOp: Record<string, number>;
    errorCount: number;
    totalDurationMs: number;
}
export declare class Tracer {
    private spans;
    private activeStack;
    private traceId;
    constructor();
    startSpan(operation: SpanOperation, attributes?: Record<string, unknown>): Span;
    endSpan(spanId: string, status?: SpanStatus): Span | undefined;
    addEvent(spanId: string, name: string, attributes?: Record<string, unknown>): void;
    getActiveSpan(): Span | undefined;
    getSpans(): Span[];
    getTraceReport(): TraceReport;
    exportJSON(): string;
    importJSON(json: string): void;
    findSpans(predicate: (span: Span) => boolean): Span[];
    findSpansByOperation(op: SpanOperation): Span[];
    getSpanById(spanId: string): Span | undefined;
    spanCount(): number;
    reset(): void;
    getChildren(spanId: string): Span[];
    getSpanTree(spanId?: string): SpanTreeNode[];
    private causalLinks;
    linkSpans(fromSpanId: string, toSpanId: string, type?: string): boolean;
    getCausalChain(spanId: string, direction?: 'upstream' | 'downstream'): Span[];
    getCausalLinks(): Array<{
        from: string;
        to: string;
        type: string;
    }>;
    getActiveSpanCount(): number;
    getSpanDepth(spanId: string): number;
    /** Export spans in OTLP JSON format (compatible with OTel Collector) */
    exportOTLP(): Record<string, unknown>;
    /** Return spans with duration >= thresholdMs */
    getSlowSpans(thresholdMs: number): Span[];
    /** Return all spans with status='error' */
    getErrorSpans(): Span[];
    /** Filter spans by a predicate */
    filter(predicate: (span: Span) => boolean): Span[];
    /** Group spans by operation name */
    groupByOperation(): Record<string, Span[]>;
    /** Count spans by status */
    spanCountByStatus(): Record<string, number>;
    /** Clear all spans and reset trace */
    clear(): void;
    /** Get duration of a completed span in ms, or null if still active */
    getSpanDuration(spanId: string): number | null;
    /** Convenience: run fn inside a span, auto-end, return result */
    traceFn<T>(operation: SpanOperation, fn: () => T, attributes?: Record<string, unknown>): {
        result: T;
        span: Span;
    };
    /** Async version of traceFn */
    traceAsync<T>(operation: SpanOperation, fn: () => Promise<T>, attributes?: Record<string, unknown>): Promise<{
        result: T;
        span: Span;
    }>;
    /** Get total duration of all completed spans */
    totalDuration(): number;
    /** Get duration at a given percentile (0-100) among completed spans */
    getPercentile(p: number): number;
}
