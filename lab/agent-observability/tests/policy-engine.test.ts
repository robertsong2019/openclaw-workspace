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
});
