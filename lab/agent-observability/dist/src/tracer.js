import { randomUUID } from 'node:crypto';
export class Tracer {
    spans = [];
    activeStack = []; // stack of spanIds
    traceId;
    constructor() {
        this.traceId = randomUUID();
    }
    startSpan(operation, attributes) {
        const parentSpanId = this.activeStack.length > 0 ? this.activeStack[this.activeStack.length - 1] : null;
        const span = {
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
    endSpan(spanId, status = 'ok') {
        const span = this.spans.find(s => s.spanId === spanId);
        if (!span || span.endTime !== null)
            return undefined;
        span.endTime = performance.now();
        span.status = status;
        this.activeStack = this.activeStack.filter(id => id !== spanId);
        return span;
    }
    addEvent(spanId, name, attributes) {
        const span = this.spans.find(s => s.spanId === spanId);
        if (span) {
            span.events.push({ name, timestamp: Date.now(), attributes });
        }
    }
    getActiveSpan() {
        if (this.activeStack.length === 0)
            return undefined;
        const id = this.activeStack[this.activeStack.length - 1];
        return this.spans.find(s => s.spanId === id);
    }
    getSpans() {
        return [...this.spans];
    }
    getTraceReport() {
        const durationByOp = {};
        let errorCount = 0;
        for (const span of this.spans) {
            const dur = span.endTime !== null ? span.endTime - span.startTime : 0;
            durationByOp[span.operation] = (durationByOp[span.operation] ?? 0) + dur;
            if (span.status === 'error')
                errorCount++;
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
    exportJSON() {
        return JSON.stringify({ traceId: this.traceId, spans: this.spans }, null, 2);
    }
    importJSON(json) {
        const data = JSON.parse(json);
        if (data.traceId)
            this.traceId = data.traceId;
        if (Array.isArray(data.spans))
            this.spans = data.spans;
    }
    findSpans(predicate) {
        return this.spans.filter(predicate);
    }
    findSpansByOperation(op) {
        return this.spans.filter(s => s.operation === op);
    }
    getSpanById(spanId) {
        return this.spans.find(s => s.spanId === spanId);
    }
    spanCount() {
        return this.spans.length;
    }
    reset() {
        this.spans = [];
        this.activeStack = [];
        this.traceId = randomUUID();
    }
    getChildren(spanId) {
        return this.spans.filter(s => s.parentSpanId === spanId);
    }
    getSpanTree(spanId) {
        const roots = spanId
            ? this.spans.filter(s => s.spanId === spanId)
            : this.spans.filter(s => s.parentSpanId === null);
        const build = (span) => {
            const kids = this.getChildren(span.spanId).map(build);
            return { ...span, children: kids };
        };
        return roots.map(build);
    }
    // --- Causal links ---
    causalLinks = [];
    linkSpans(fromSpanId, toSpanId, type = 'causal') {
        const from = this.spans.find(s => s.spanId === fromSpanId);
        const to = this.spans.find(s => s.spanId === toSpanId);
        if (!from || !to)
            return false;
        this.causalLinks.push({ from: fromSpanId, to: toSpanId, type });
        return true;
    }
    getCausalChain(spanId, direction = 'upstream') {
        const visited = new Set();
        const result = [];
        const queue = [spanId];
        while (queue.length > 0) {
            const current = queue.shift();
            if (visited.has(current))
                continue;
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
    getCausalLinks() {
        return [...this.causalLinks];
    }
    getActiveSpanCount() {
        return this.activeStack.length;
    }
    getSpanDepth(spanId) {
        let depth = 0;
        let current = this.spans.find(s => s.spanId === spanId);
        while (current?.parentSpanId) {
            depth++;
            current = this.spans.find(s => s.spanId === current.parentSpanId);
        }
        return depth;
    }
    /** Export spans in OTLP JSON format (compatible with OTel Collector) */
    exportOTLP() {
        return {
            resourceSpans: [{
                    scopeSpans: [{
                            scope: { name: 'agent-observability', version: '1.0.0' },
                            spans: this.spans.map(s => ({
                                traceId: s.traceId,
                                spanId: s.spanId,
                                parentSpanId: s.parentSpanId ?? undefined,
                                name: s.operation,
                                kind: 1, // INTERNAL
                                startTimeUnixNano: Math.round(s.startTime * 1e6),
                                endTimeUnixNano: s.endTime !== null ? Math.round(s.endTime * 1e6) : undefined,
                                status: { code: s.status === 'error' ? 2 : s.status === 'ok' ? 1 : 0 },
                                attributes: Object.entries(s.attributes).map(([k, v]) => ({ key: k, value: { stringValue: String(v) } })),
                                events: s.events.map(e => ({
                                    timeUnixNano: e.timestamp * 1e6,
                                    name: e.name,
                                    attributes: Object.entries(e.attributes ?? {}).map(([k, v]) => ({ key: k, value: { stringValue: String(v) } })),
                                })),
                            })),
                        }],
                }],
        };
    }
    /** Return spans with duration >= thresholdMs */
    getSlowSpans(thresholdMs) {
        return this.spans.filter(s => s.endTime !== null && (s.endTime - s.startTime) >= thresholdMs);
    }
    /** Return all spans with status='error' */
    getErrorSpans() {
        return this.spans.filter(s => s.status === 'error');
    }
    /** Filter spans by a predicate */
    filter(predicate) {
        return this.spans.filter(predicate);
    }
    /** Group spans by operation name */
    groupByOperation() {
        const groups = {};
        for (const s of this.spans) {
            (groups[s.operation] ??= []).push(s);
        }
        return groups;
    }
    /** Count spans by status */
    spanCountByStatus() {
        const counts = {};
        for (const s of this.spans) {
            counts[s.status] = (counts[s.status] ?? 0) + 1;
        }
        return counts;
    }
    /** Clear all spans and reset trace */
    clear() {
        const newTraceId = randomUUID();
        this.spans = [];
        this.traceId = newTraceId;
    }
    /** Get duration of a completed span in ms, or null if still active */
    getSpanDuration(spanId) {
        const span = this.spans.find(s => s.spanId === spanId);
        if (!span || span.endTime === null)
            return null;
        return span.endTime - span.startTime;
    }
    /** Convenience: run fn inside a span, auto-end, return result */
    traceFn(operation, fn, attributes) {
        const span = this.startSpan(operation, attributes);
        try {
            const result = fn();
            this.endSpan(span.spanId, 'ok');
            return { result, span };
        }
        catch (err) {
            this.endSpan(span.spanId, 'error');
            throw err;
        }
    }
    /** Async version of traceFn */
    async traceAsync(operation, fn, attributes) {
        const span = this.startSpan(operation, attributes);
        try {
            const result = await fn();
            this.endSpan(span.spanId, 'ok');
            return { result, span };
        }
        catch (err) {
            this.endSpan(span.spanId, 'error');
            throw err;
        }
    }
    /** Get total duration of all completed spans */
    totalDuration() {
        return this.spans.reduce((sum, s) => {
            if (s.endTime === null)
                return sum;
            return sum + (s.endTime - s.startTime);
        }, 0);
    }
    /** Get duration at a given percentile (0-100) among completed spans */
    getPercentile(p) {
        const durs = this.spans
            .filter(s => s.endTime !== null)
            .map(s => s.endTime - s.startTime)
            .sort((a, b) => a - b);
        if (durs.length === 0)
            return 0;
        const idx = Math.min(Math.floor(p / 100 * durs.length), durs.length - 1);
        return durs[idx];
    }
}
