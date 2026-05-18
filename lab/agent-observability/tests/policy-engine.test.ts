import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { PolicyEngine, blockDestructiveOps, costLimit, piiFilter } from '../src/policy-engine.js';

describe('PolicyEngine', () => {
  it('allows when no rules exist for category', () => {
    const engine = new PolicyEngine();
    const result = engine.evaluate('nonexistent', {});
    assert.equal(result.allowed, true);
    assert.equal(result.violations.length, 0);
  });

  it('blocks when a rule denies', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('tool_execution', blockDestructiveOps());
    const result = engine.evaluate('tool_execution', { command: 'rm -rf /' });
    assert.equal(result.allowed, false);
    assert.equal(result.violations.length, 1);
    assert.ok(result.violations[0].reason.includes('Destructive'));
  });

  it('allows non-destructive commands', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('tool_execution', blockDestructiveOps());
    const result = engine.evaluate('tool_execution', { command: 'ls -la' });
    assert.equal(result.allowed, true);
  });

  it('enforces cost limit', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('cost_control', costLimit({ maxCost: 0.5 }));
    const over = engine.evaluate('cost_control', { cost: 1.0 });
    assert.equal(over.allowed, false);
    const under = engine.evaluate('cost_control', { cost: 0.3 });
    assert.equal(under.allowed, true);
  });

  it('filters PII (email)', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('data_privacy', piiFilter());
    const bad = engine.evaluate('data_privacy', { text: 'Contact me at user@example.com' });
    assert.equal(bad.allowed, false);
    const ok = engine.evaluate('data_privacy', { text: 'Hello world' });
    assert.equal(ok.allowed, true);
  });

  it('removes a policy by name', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('test', { name: 'rule1', description: '', category: 'test', evaluate: () => ({ allow: false }) });
    const removed = engine.removePolicy('test', 'rule1');
    assert.equal(removed, true);
    const result = engine.evaluate('test', {});
    assert.equal(result.allowed, true);
  });

  it('loads rules from JSON array', () => {
    const engine = new PolicyEngine();
    engine.loadFromJSON([
      { name: 'cost_check', description: '', category: 'cost', type: 'costLimit', config: { maxCost: 2 } },
    ]);
    const result = engine.evaluate('cost', { cost: 3 });
    assert.equal(result.allowed, false);
  });

  it('lists categories', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('cat_a', { name: 'r1', description: '', category: 'cat_a', evaluate: () => ({ allow: true }) });
    engine.addPolicy('cat_b', { name: 'r2', description: '', category: 'cat_b', evaluate: () => ({ allow: true }) });
    engine.addPolicy('cat_a', { name: 'r3', description: '', category: 'cat_a', evaluate: () => ({ allow: true }) });
    const cats = engine.listCategories();
    assert.deepEqual(cats.sort(), ['cat_a', 'cat_b']);
  });

  it('counts rules per category', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('cat_a', { name: 'r1', description: '', category: 'cat_a', evaluate: () => ({ allow: true }) });
    engine.addPolicy('cat_a', { name: 'r2', description: '', category: 'cat_a', evaluate: () => ({ allow: true }) });
    assert.equal(engine.ruleCount('cat_a'), 2);
    assert.equal(engine.ruleCount('cat_b'), 0);
  });

  it('exports rules as JSON array', () => {
    const engine = new PolicyEngine();
    engine.loadFromJSON([
      { name: 'cost_check', description: 'test', category: 'cost', type: 'costLimit', config: { maxCost: 5 } },
    ]);
    const exported = engine.exportJSON();
    assert.equal(exported.length, 1);
    assert.equal(exported[0].category, 'cost');
  });

  it('disableRule skips rule in evaluation', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('tool_execution', blockDestructiveOps());
    engine.disableRule('tool_execution', 'block_destructive_ops');
    const result = engine.evaluate('tool_execution', { command: 'rm -rf /' });
    assert.equal(result.allowed, true);
  });

  it('enableRule re-enables a disabled rule', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('tool_execution', blockDestructiveOps());
    engine.disableRule('tool_execution', 'block_destructive_ops');
    engine.enableRule('tool_execution', 'block_destructive_ops');
    const result = engine.evaluate('tool_execution', { command: 'rm -rf /' });
    assert.equal(result.allowed, false);
  });

  it('isRuleEnabled reports status', () => {
    const engine = new PolicyEngine();
    assert.equal(engine.isRuleEnabled('cat', 'rule1'), true);
    engine.disableRule('cat', 'rule1');
    assert.equal(engine.isRuleEnabled('cat', 'rule1'), false);
    engine.enableRule('cat', 'rule1');
    assert.equal(engine.isRuleEnabled('cat', 'rule1'), true);
  });

  it('evaluateAll checks all categories at once', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('tool_execution', blockDestructiveOps());
    engine.addPolicy('data_privacy', piiFilter());
    const results = engine.evaluateAll({ command: 'rm -rf /', text: 'clean email@x.com here' });
    assert.equal(results['tool_execution']?.allowed, false);
    assert.equal(results['data_privacy']?.allowed, false);
  });

  it('evaluateAll returns empty for no categories', () => {
    const engine = new PolicyEngine();
    const results = engine.evaluateAll({});
    assert.deepEqual(results, {});
  });

  it('addPolicies adds multiple rules at once', () => {
    const engine = new PolicyEngine();
    engine.addPolicies('safety', [blockDestructiveOps(), piiFilter()]);
    assert.equal(engine.ruleCount('safety'), 2);
  });

  it('batchEvaluate evaluates multiple categories with different inputs', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('tool_execution', blockDestructiveOps());
    engine.addPolicy('data_privacy', piiFilter());
    const results = engine.batchEvaluate({
      tool_execution: { command: 'ls' },
      data_privacy: { text: 'clean email@x.com' },
    });
    assert.equal(results['tool_execution']?.allowed, true);
    assert.equal(results['data_privacy']?.allowed, false);
  });

  // --- getRule + hasCategory ---

  it('getRule returns specific rule from category', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('tool_execution', blockDestructiveOps());
    const rule = engine.getRule('tool_execution', 'block_destructive_ops');
    assert.ok(rule);
    assert.equal(rule!.name, 'block_destructive_ops');
  });

  it('getRule returns undefined for missing rule', () => {
    const engine = new PolicyEngine();
    assert.strictEqual(engine.getRule('tool_execution', 'nonexistent'), undefined);
  });

  it('hasCategory returns true for non-empty category', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('test', blockDestructiveOps());
    assert.strictEqual(engine.hasCategory('test'), true);
  });

  it('hasCategory returns false for empty/missing category', () => {
    const engine = new PolicyEngine();
    assert.strictEqual(engine.hasCategory('missing'), false);
  });

  it('clearCategory removes all rules in category', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('test', { name: 'r1', description: '', category: 'test', evaluate: () => ({ allow: true }) });
    engine.addPolicy('test', { name: 'r2', description: '', category: 'test', evaluate: () => ({ allow: true }) });
    assert.strictEqual(engine.ruleCount('test'), 2);
    assert.strictEqual(engine.clearCategory('test'), true);
    assert.strictEqual(engine.ruleCount('test'), 0);
    assert.strictEqual(engine.clearCategory('nonexistent'), false);
  });

  it('importRules replaces all rules', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('old', { name: 'old-rule', description: '', category: 'old', evaluate: () => ({ allow: true }) });
    const count = engine.importRules([
      { name: 'block_rm', description: 'Block rm', category: 'security', type: 'blockDestructiveOps' },
      { name: 'cheap', description: 'Cost limit', category: 'cost', type: 'costLimit', config: { maxCost: 0.5 } },
    ]);
    assert.strictEqual(count, 2);
    assert.strictEqual(engine.hasCategory('old'), false);
    assert.strictEqual(engine.hasCategory('security'), true);
    assert.strictEqual(engine.hasCategory('cost'), true);
  });

  it('ruleNames returns all rule names', () => {
    const engine = new PolicyEngine();
    engine.addPolicy('a', { name: 'rule1', description: '', category: 'a', evaluate: () => ({ allow: true }) });
    engine.addPolicy('b', { name: 'rule2', description: '', category: 'b', evaluate: () => ({ allow: true }) });
    const names = engine.ruleNames();
    assert.deepEqual(names.sort(), ['rule1', 'rule2']);
  });
});
