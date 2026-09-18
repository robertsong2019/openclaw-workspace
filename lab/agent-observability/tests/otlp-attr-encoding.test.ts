/**
 * exportGenAiOtlp span 属性编码一致性（RED-first，09-18 code-lab）
 *
 * 缺口：exportGenAiOtlp 里事件属性走规范形状的 toOtlpValue（数组→arrayValue、
 * 对象→kvlistValue、布尔→boolValue），span 属性却走了退化编码：
 *   typeof v === 'number' ? { intValue: v } : { stringValue: String(v) }
 * 后果：
 * 1. 布尔 → stringValue "true"（OTLP 应为 boolValue）
 * 2. 数组 → "a,b" 拼接串（应为 arrayValue）
 * 3. 对象 → "[object Object]"（应为 kvlistValue）
 * 4. 浮点 → intValue 1.5（protobuf int64 必须 integer，非法 OTLP；应为 doubleValue）
 *
 * 修复：span 属性与事件属性同源 —— 都走 toOtlpValue。
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { exportGenAiOtlp } from '../src/otel-genai.js';
import type { AdapterSpan } from '../src/otel-genai.js';

const EPOCH = 1_000_000;

function span(op: string, attrs: Record<string, unknown>): AdapterSpan {
  return { traceId: '11111111-2222-3333-4444-555555555555', spanId: 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', parentSpanId: null,
    operation: op, startTime: 100, endTime: 200, attributes: attrs, status: 'ok', events: [] };
}

function firstSpanAttrs(attrs: Record<string, unknown>): Array<{ key: string; value: Record<string, unknown> }> {
  // 未知 operation 走 default 分支全量透传 —— 任意类型属性出现在 OTLP 的真实入口
  // （已知 operation 的映射键都是 string/number，泛型透传才暴露编码缺陷）
  const s = exportGenAiOtlp([span('custom.op', attrs)], {}, EPOCH).resourceSpans[0].scopeSpans[0].spans[0];
  return s.attributes as Array<{ key: string; value: Record<string, unknown> }>;
}

function attr(attrs: Array<{ key: string; value: Record<string, unknown> }>, key: string): Record<string, unknown> {
  const found = attrs.find(a => a.key === key);
  assert.ok(found, `attribute ${key} missing`);
  return found!.value;
}

describe('exportGenAiOtlp — span attribute AnyValue encoding (spec-shaped)', () => {
  it('boolean attribute → boolValue, not stringValue "true"', () => {
    const v = attr(firstSpanAttrs({ 'ao.enabled': true }), 'ao.enabled');
    assert.deepEqual(v, { boolValue: true });
  });

  it('array attribute → arrayValue with per-element encoding', () => {
    const v = attr(firstSpanAttrs({ 'ao.tags': ['a', 'b'] }), 'ao.tags');
    assert.deepEqual(v, { arrayValue: { values: [{ stringValue: 'a' }, { stringValue: 'b' }] } });
  });

  it('object attribute → kvlistValue, not "[object Object]"', () => {
    const v = attr(firstSpanAttrs({ 'ao.meta': { depth: 2 } }), 'ao.meta');
    assert.deepEqual(v, { kvlistValue: { values: [{ key: 'depth', value: { intValue: 2 } }] } });
  });

  it('float attribute → doubleValue, not fractional intValue (invalid int64)', () => {
    const v = attr(firstSpanAttrs({ 'ao.score': 0.75 }), 'ao.score');
    assert.deepEqual(v, { doubleValue: 0.75 });
  });

  it('integer attribute stays intValue (no regression)', () => {
    const v = attr(firstSpanAttrs({ 'ao.count': 3 }), 'ao.count');
    assert.deepEqual(v, { intValue: 3 });
  });

  it('null/undefined attribute degrades to stringValue (documented fallthrough)', () => {
    const v = attr(firstSpanAttrs({ 'ao.maybe': null }), 'ao.maybe');
    assert.deepEqual(v, { stringValue: 'null' });
  });
});
