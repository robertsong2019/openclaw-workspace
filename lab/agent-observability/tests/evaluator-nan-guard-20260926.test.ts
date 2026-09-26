/**
 * costEfficiencyCheck NaN 防御 + compareTraces 不对称契约 pin（2026-09-26）
 *
 * RED：attributes.totalTokens 为非 numeric 字符串（跨 JSON/上游脏数据）时
 * Number('abc')=NaN，reduce 污染总和，Math.max/min 对 NaN 全部失效 →
 * score=NaN 静默传播（JSON.stringify→null，compareTraces delta=NaN，
 * regression 判定 NaN<threshold=false → 评分器谎报满分的兄弟形态）。
 *
 * 修复语义：不可解析的 token 计数按 0 处理（NaN 属性不参与求和），
 * 有效数字字符串 '500' 保持可解析。
 *
 * 附 compareTraces 契约 pin：current 侧多出的 dimension 被静默丢弃
 * （只迭代 baseline 侧 dims）——文档化现状，非本 cycle 修改。
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';

import {
  costEfficiencyCheck,
  compareTraces,
  type EvalCheck,
  type EvalCheckResult,
} from '../src/evaluator.js';
import type { Span } from '../src/tracer.js';

function span(overrides: Partial<Span> = {}): Span {
  return {
    traceId: 't1',
    spanId: 's1',
    parentSpanId: null,
    operation: 'llm.call',
    startTime: 0,
    endTime: 10,
    status: 'ok',
    attributes: {},
    events: [],
    ...overrides,
  };
}

test('costEfficiencyCheck: garbage totalTokens does not produce NaN score', () => {
  const spans = [span({ attributes: { totalTokens: 'abc' } })];
  const results = costEfficiencyCheck(spans);
  const score = results[0].score;
  assert.equal(
    Number.isFinite(score),
    true,
    `score must be finite, got ${score}`
  );
  assert.equal(score, 1, '0 valid tokens (< 1000) should score 1');
});

test('costEfficiencyCheck: NaN attribute value treated as 0 not poison', () => {
  const spans = [
    span({ attributes: { totalTokens: 500 } }),
    span({ attributes: { totalTokens: Number.NaN } }),
  ];
  const results = costEfficiencyCheck(spans);
  assert.equal(Number.isFinite(results[0].score), true);
  assert.equal(results[0].score, 1, '500 valid tokens still < 1000 → 1');
});

test('costEfficiencyCheck: numeric string totalTokens still parseable', () => {
  const spans = [span({ attributes: { totalTokens: '500' } })];
  const results = costEfficiencyCheck(spans);
  assert.equal(results[0].score, 1);
});

test('costEfficiencyCheck: legit high token count still degrades', () => {
  const spans = [span({ attributes: { totalTokens: 100000 } })];
  const results = costEfficiencyCheck(spans);
  assert.equal(results[0].score, 0);
});

// ---------- compareTraces 契约 pin（现状文档化） ----------

test('compareTraces: baseline-only dims are compared, current treated as 0 when missing', () => {
  const onlyBaseline: EvalCheck = (spans: Span[]): EvalCheckResult[] => {
    if (spans.length === 0) return [];
    return [{ dimension: 'custom_dim', score: 0.5, reason: 'baseline has spans' }];
  };
  // current 无 spans → check 返回 [] → cv=??0 → delta=-0.5 → regression
  const diffs = compareTraces([span()], [], [onlyBaseline]);
  assert.equal(diffs.length, 1);
  assert.equal(diffs[0].dimension, 'custom_dim');
  assert.equal(diffs[0].current, 0);
  assert.equal(diffs[0].regression, true);
});

test('compareTraces: current-only extra dims are dropped (documented asymmetry)', () => {
  const currentOnly: EvalCheck = (spans: Span[]): EvalCheckResult[] => {
    if (spans.length === 0) return [];
    return [{ dimension: 'extra_dim', score: 0.9, reason: 'current has spans' }];
  };
  const diffs = compareTraces([], [span()], [currentOnly]);
  assert.equal(diffs.length, 0, 'extra current dims silently dropped');
});
