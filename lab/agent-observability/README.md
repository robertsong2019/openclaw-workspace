# 🔍 Agent Observability

A minimal TypeScript toolkit for observing, governing, and evaluating AI agent execution. Three composable components: **Tracer** (distributed tracing), **PolicyEngine** (guardrails), and **Evaluator** (quality scoring) — unified via a high-level `AgentObserver` facade.

## Features

- **Structured Tracing** — OpenTelemetry-style spans with parent-child relationships, events, and trace reports
- **Policy Guardrails** — Block destructive ops, enforce rate/cost limits, detect PII; extensible via custom rules
- **Quality Evaluation** — Score agent runs across dimensions (latency, reliability, policy compliance, cost efficiency)
- **Unified API** — `AgentObserver` wraps all three components into a single interface for drop-in use
- **Zero Dependencies** — Pure TypeScript, runs on Node.js built-ins

## Quick Start

```ts
import { AgentObserver } from './src/index.js';

const observer = new AgentObserver();

// Load policy rules (optional — some are pre-loaded)
observer.getPolicyEngine().loadFromJSON([
  { name: 'block_rm', description: 'Block destructive ops', category: 'tool_execution', type: 'blockDestructiveOps' },
  { name: 'rate', description: 'Rate limit', category: 'rate_control', type: 'rateLimit', config: { maxCalls: 20, windowMs: 60000 } },
]);

// Start an agent run
const runSpan = observer.startRun('my-agent', 'Summarize document');

// Log an LLM call
observer.llmCall('gpt-4', 'Summarize...', 'Here is the summary...', { promptTokens: 120, completionTokens: 80 });

// Execute a tool (checked against policies)
const { allowed, span } = observer.toolExecute('bash', 'rm -rf /tmp/test');
if (!allowed) console.log('Blocked:', span.attributes.policyViolations);

// End the run and get a report
observer.endRun();
const report = observer.getReport();
console.log('Aggregate score:', report.aggregateScore);
console.log('Errors:', report.traceReport.errorCount);
```

## API Reference

### Tracer

| Method | Description |
|--------|-------------|
| `startSpan(operation, attributes?)` | Start a new span (pushes onto active stack) |
| `endSpan(spanId, status?)` | End a span, record duration |
| `addEvent(spanId, name, attributes?)` | Attach a timestamped event to a span |
| `getActiveSpan()` | Get the current top-of-stack span |
| `getSpans()` | Return all spans |
| `getTraceReport()` | Aggregate report: duration by operation, error count |
| `findSpansByOperation(op)` | Filter spans by operation type |
| `exportJSON()` / `importJSON(json)` | Serialize/restore trace data |

### PolicyEngine

| Method | Description |
|--------|-------------|
| `addPolicy(category, rule)` | Register a rule under a category |
| `removePolicy(category, ruleName)` | Remove a rule |
| `evaluate(category, input)` | Run all rules in a category; returns `{ allowed, violations }` |
| `loadFromJSON(data)` | Bulk-load rules from JSON config |
| `exportJSON()` | Export current rule definitions |

**Built-in rule builders:** `blockDestructiveOps()`, `costLimit(cfg)`, `rateLimit(cfg)`, `piiFilter()`

### Evaluator

| Method | Description |
|--------|-------------|
| `addCheck(name, fn, weight?)` | Register an evaluation check |
| `evaluate(spans)` | Run all checks against spans |
| `aggregateScore(results)` | Weighted average of check scores (0–1) |

**Built-in checks:** `policyComplianceCheck`, `latencyCheck`, `reliabilityCheck`, `costEfficiencyCheck`

### AgentObserver (Facade)

| Method | Description |
|--------|-------------|
| `startRun(agentId, task)` | Begin a root agent span |
| `llmCall(model, prompt, completion, tokenUsage?)` | Trace an LLM call |
| `toolExecute(tool, input)` | Execute tool through policy engine |
| `memoryOperation(type, attrs)` | Trace memory read/write |
| `retrievalSearch(method, attrs)` | Trace a retrieval operation |
| `endRun()` | End the root span |
| `getReport()` | Full observability report with scores |

## Project Structure

```
src/
  index.ts          # AgentObserver facade + types
  tracer.ts         # Distributed tracing (Span, TraceReport)
  policy-engine.ts  # Guardrails & policy evaluation
  evaluator.ts      # Quality scoring across dimensions
tests/
  tracer.test.ts
  policy-engine.test.ts
  evaluator.test.ts
  integration.test.ts
```

## Running Tests

```bash
npm test
```
