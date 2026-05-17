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

  getChildren(spanId: string): Span[] {
    return this.spans.filter(s => s.parentSpanId === spanId);
  }

  getSpanTree(spanId?: string): Array<Span & { children: Span[] }> {
    const roots = spanId
      ? this.spans.filter(s => s.spanId === spanId)
      : this.spans.filter(s => s.parentSpanId === null);
    const build = (span: Span): Span & { children: Span[] } => {
      const kids = this.getChildren(span.spanId).map(build);
      return { ...span, children: kids };
    };
    return roots.map(build);
  }

  // --- Causal links ---

  private causalLinks: Array<{ from: string; to: string; type: string }> = [];

  linkSpans(fromSpanId: string, toSpanId: string, type: string = 'causal'): boolean {
    const from = this.spans.find(s => s.spanId === fromSpanId);
    const to = this.spans.find(s => s.spanId === toSpanId);
    if (!from || !to) return false;
    this.causalLinks.push({ from: fromSpanId, to: toSpanId, type });
    return true;
  }

  getCausalChain(spanId: string, direction: 'upstream' | 'downstream' = 'upstream'): Span[] {
    const visited = new Set<string>();
    const result: Span[] = [];
    const queue = [spanId];
    while (queue.length > 0) {
      const current = queue.shift()!;
      if (visited.has(current)) continue;
      visited.add(current);
      const links = direction === 'upstream'
        ? this.causalLinks.filter(l => l.to === current)
        : this.causalLinks.filter(l => l.from === current);
      for (const link of links) {
        const nextId = direction === 'upstream' ? link.from : link.to;
        const span = this.spans.find(s => s.spanId === nextId);
        if (span && !visited.has(nextId)) {
          result.push(span);
          queue.push(nextId);
        }
      }
    }
    return result;
  }

  getCausalLinks(): Array<{ from: string; to: string; type: string }> {
    return [...this.causalLinks];
  }

  getActiveSpanCount(): number {
    return this.activeStack.length;
  }

  getSpanDepth(spanId: string): number {
    let depth = 0;
    let current = this.spans.find(s => s.spanId === spanId);
    while (current?.parentSpanId) {
      depth++;
      current = this.spans.find(s => s.spanId === current!.parentSpanId);
    }
    return depth;
  }
}
