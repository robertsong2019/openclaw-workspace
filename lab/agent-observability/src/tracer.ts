import { randomUUID } from 'node:crypto';

export type SpanStatus = 'ok' | 'error' | 'unset';
export type SpanOperation =
  | 'agent.run' | 'llm.call' | 'tool.execute'
  | 'retrieval.search' | 'memory.read' | 'memory.write';

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

export interface TraceReport {
  traceId: string;
  spans: Span[];
  totalSpans: number;
  durationByOp: Record<string, number>;
  errorCount: number;
  totalDurationMs: number;
}

export class Tracer {
  private spans: Span[] = [];
  private activeStack: string[] = []; // stack of spanIds
  private traceId: string;

  constructor() {
    this.traceId = randomUUID();
  }

  startSpan(operation: SpanOperation, attributes?: Record<string, unknown>): Span {
    const parentSpanId = this.activeStack.length > 0 ? this.activeStack[this.activeStack.length - 1] : null;
    const span: Span = {
      traceId: this.traceId,
      spanId: randomUUID(),
      parentSpanId,
      operation,
      startTime: performance.now(),
      endTime: null,
      attributes: { ...attributes },
      status: 'unset',
      events: [],
    };
    this.spans.push(span);
    this.activeStack.push(span.spanId);
    return span;
  }

  endSpan(spanId: string, status: SpanStatus = 'ok'): Span | undefined {
    const span = this.spans.find(s => s.spanId === spanId);
    if (!span || span.endTime !== null) return undefined;
    span.endTime = performance.now();
    span.status = status;
    this.activeStack = this.activeStack.filter(id => id !== spanId);
    return span;
  }

  addEvent(spanId: string, name: string, attributes?: Record<string, unknown>): void {
    const span = this.spans.find(s => s.spanId === spanId);
    if (span) {
      span.events.push({ name, timestamp: Date.now(), attributes });
    }
  }

  getActiveSpan(): Span | undefined {
    if (this.activeStack.length === 0) return undefined;
    const id = this.activeStack[this.activeStack.length - 1];
    return this.spans.find(s => s.spanId === id);
  }

  getSpans(): Span[] {
    return [...this.spans];
  }

  getTraceReport(): TraceReport {
    const durationByOp: Record<string, number> = {};
    let errorCount = 0;
    for (const span of this.spans) {
      const dur = span.endTime !== null ? span.endTime - span.startTime : 0;
      durationByOp[span.operation] = (durationByOp[span.operation] ?? 0) + dur;
      if (span.status === 'error') errorCount++;
    }
    const root = this.spans.find(s => s.parentSpanId === null);
    const totalDurationMs = root?.endTime !== null && root?.endTime !== undefined
      ? root.endTime - root.startTime : 0;
    return {
      traceId: this.traceId,
      spans: this.spans,
      totalSpans: this.spans.length,
      durationByOp,
      errorCount,
      totalDurationMs,
    };
  }

  exportJSON(): string {
    return JSON.stringify({ traceId: this.traceId, spans: this.spans }, null, 2);
  }

  importJSON(json: string): void {
    const data = JSON.parse(json);
    if (data.traceId) this.traceId = data.traceId;
    if (Array.isArray(data.spans)) this.spans = data.spans;
  }

  findSpans(predicate: (span: Span) => boolean): Span[] {
    return this.spans.filter(predicate);
  }

  findSpansByOperation(op: SpanOperation): Span[] {
    return this.spans.filter(s => s.operation === op);
  }

  getSpanById(spanId: string): Span | undefined {
    return this.spans.find(s => s.spanId === spanId);
  }

  spanCount(): number {
    return this.spans.length;
  }

  reset(): void {
    this.spans = [];
    this.activeStack = [];
    this.traceId = randomUUID();
  }
}
