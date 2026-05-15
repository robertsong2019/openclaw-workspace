import type { Span } from './tracer.js';

export interface EvalCheckResult {
  dimension: string;
  score: number; // 0-1
  reason: string;
}

export type EvalCheck = (spans: Span[]) => EvalCheckResult[];

export class Evaluator {
  private checks: Array<{ name: string; fn: EvalCheck; weight: number }> = [];
  private weights: Map<string, number> = new Map();

  addCheck(name: string, fn: EvalCheck, weight = 1.0): void {
    this.checks.push({ name, fn, weight });
    this.weights.set(name, weight);
  }

  evaluate(spans: Span[]): EvalCheckResult[] {
    const results: EvalCheckResult[] = [];
    for (const check of this.checks) {
      results.push(...check.fn(spans));
    }
    return results;
  }

  aggregateScore(results: EvalCheckResult[]): number {
    if (results.length === 0) return 0;
    let totalWeight = 0;
    let weightedSum = 0;
    for (const r of results) {
      const w = this.weights.get(r.dimension) ?? 1.0;
      weightedSum += r.score * w;
      totalWeight += w;
    }
    return totalWeight > 0 ? weightedSum / totalWeight : 0;
  }

  listChecks(): string[] {
    return this.checks.map(c => c.name);
  }

  removeCheck(name: string): boolean {
    const before = this.checks.length;
    this.checks = this.checks.filter(c => c.name !== name);
    return this.checks.length < before;
  }
}

// --- Built-in checks ---

export function policyComplianceCheck(spans: Span[]): EvalCheckResult[] {
  const toolSpans = spans.filter(s => s.operation === 'tool.execute');
  const blocked = toolSpans.filter(s => s.status === 'error' && s.attributes.policyDenied === true);
  const ratio = toolSpans.length > 0 ? 1 - blocked.length / toolSpans.length : 1;
  return [{
    dimension: 'policy_compliance',
    score: ratio,
    reason: `${blocked.length}/${toolSpans.length} tool calls blocked by policy`,
  }];
}

export function latencyCheck(spans: Span[]): EvalCheckResult[] {
  const completed = spans.filter(s => s.endTime !== null);
  if (completed.length === 0) return [{ dimension: 'latency', score: 1, reason: 'No completed spans' }];
  const durations = completed.map(s => s.endTime! - s.startTime);
  const avg = durations.reduce((a, b) => a + b, 0) / durations.length;
  // Score 1 if avg < 100ms, degrade to 0 at 5000ms
  const score = Math.max(0, Math.min(1, 1 - (avg - 100) / 4900));
  return [{
    dimension: 'latency',
    score: Math.round(score * 100) / 100,
    reason: `Avg span duration: ${avg.toFixed(1)}ms`,
  }];
}

export function reliabilityCheck(spans: Span[]): EvalCheckResult[] {
  if (spans.length === 0) return [{ dimension: 'reliability', score: 1, reason: 'No spans' }];
  const errors = spans.filter(s => s.status === 'error').length;
  const score = 1 - errors / spans.length;
  return [{
    dimension: 'reliability',
    score: Math.round(score * 100) / 100,
    reason: `${errors}/${spans.length} spans errored`,
  }];
}

export function costEfficiencyCheck(spans: Span[]): EvalCheckResult[] {
  const llmSpans = spans.filter(s => s.operation === 'llm.call');
  if (llmSpans.length === 0) return [{ dimension: 'cost_efficiency', score: 1, reason: 'No LLM calls' }];
  const totalTokens = llmSpans.reduce((sum, s) => sum + Number(s.attributes.totalTokens ?? 0), 0);
  // Score 1 if < 1000 tokens, degrade to 0 at 100k
  const score = Math.max(0, Math.min(1, 1 - (totalTokens - 1000) / 99000));
  return [{
    dimension: 'cost_efficiency',
    score: Math.round(score * 100) / 100,
    reason: `Total tokens: ${totalTokens}`,
  }];
}
