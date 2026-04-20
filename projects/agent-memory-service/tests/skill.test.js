/**
 * Agent Memory Service — Skill/SOP Layer Tests (L3)
 */
import { describe, it, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService, SkillStore } from '../src/index.js';
import { mkdtempSync, rmSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'skill-test-'));
  const svc = new MemoryService({ dbPath: dir });
  return { svc, dir, cleanup: () => { try { rmSync(dir, { recursive: true }); } catch {} } };
}

// ─── SkillStore Unit Tests ───────────────────────────────

describe('SkillStore', () => {
  it('put() creates a skill with defaults', () => {
    const dir = mkdtempSync(join(tmpdir(), 'ss-'));
    const store = new SkillStore(dir);
    const skill = store.put({
      name: 'code-review',
      steps: ['read diff', 'check style', 'check logic'],
      trigger: 'review, code',
    });
    assert.equal(skill.name, 'code-review');
    assert.equal(skill.steps.length, 3);
    assert.equal(skill.successRate, 1.0);
    assert.equal(skill.usageCount, 0);
    rmSync(dir, { recursive: true });
  });

  it('match() finds skills by trigger keywords', () => {
    const dir = mkdtempSync(join(tmpdir(), 'ss-'));
    const store = new SkillStore(dir);
    store.put({ name: 'bug-fix', steps: ['reproduce', 'fix', 'test'], trigger: 'bug, fix, error' });
    store.put({ name: 'deploy', steps: ['build', 'test', 'push'], trigger: 'deploy, release' });

    const results = store.match('fix the bug in login');
    assert.equal(results.length, 1);
    assert.equal(results[0].name, 'bug-fix');
    rmSync(dir, { recursive: true });
  });

  it('match() returns empty for no match', () => {
    const dir = mkdtempSync(join(tmpdir(), 'ss-'));
    const store = new SkillStore(dir);
    store.put({ name: 'deploy', steps: ['build'], trigger: 'deploy' });
    assert.equal(store.match('write docs').length, 0);
    rmSync(dir, { recursive: true });
  });

  it('recordUsage() updates successRate', () => {
    const dir = mkdtempSync(join(tmpdir(), 'ss-'));
    const store = new SkillStore(dir);
    const skill = store.put({ name: 'test', steps: ['a'], trigger: 'test' });

    store.recordUsage(skill.id, { success: true });
    assert.equal(skill.usageCount, 1);
    assert.equal(skill.successRate, 1.0);

    store.recordUsage(skill.id, { success: false });
    assert.equal(skill.usageCount, 2);
    assert.equal(skill.successRate, 0.5);
    rmSync(dir, { recursive: true });
  });

  it('match() sorts by successRate then usageCount', () => {
    const dir = mkdtempSync(join(tmpdir(), 'ss-'));
    const store = new SkillStore(dir);
    const s1 = store.put({ name: 'low-rate', steps: ['a'], trigger: 'test' });
    const s2 = store.put({ name: 'high-rate', steps: ['b'], trigger: 'test' });
    store.recordUsage(s1.id, { success: false }); // rate = 0
    store.recordUsage(s2.id, { success: true });  // rate = 1

    const results = store.match('test');
    assert.equal(results[0].name, 'high-rate');
    assert.equal(results[1].name, 'low-rate');
    rmSync(dir, { recursive: true });
  });

  it('delete() removes a skill', () => {
    const dir = mkdtempSync(join(tmpdir(), 'ss-'));
    const store = new SkillStore(dir);
    const skill = store.put({ name: 'temp', steps: ['a'], trigger: 'temp' });
    assert.equal(store.size, 1);
    store.delete(skill.id);
    assert.equal(store.size, 0);
    assert.equal(store.get(skill.id), undefined);
    rmSync(dir, { recursive: true });
  });

  it('persists to disk via save/load', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'ss-'));
    mkdirSync(dir, { recursive: true });
    const store1 = new SkillStore(dir);
    store1.put({ name: 'persist-test', steps: ['a', 'b'], trigger: 'persist' });
    await store1.save();

    const store2 = new SkillStore(dir);
    await store2.load();
    assert.equal(store2.size, 1);
    const skills = store2.all();
    assert.equal(skills[0].name, 'persist-test');
    rmSync(dir, { recursive: true });
  });
});

// ─── MemoryService Skill API Tests ───────────────────────

describe('MemoryService — Skill API', () => {
  /** @type {{svc: MemoryService, cleanup: Function}} */
  let ctx;

  before(() => {
    ctx = createService();
  });

  after(() => {
    ctx.cleanup();
  });

  it('learnSkill() creates a skill', async () => {
    const skill = await ctx.svc.learnSkill({
      name: 'debug-api',
      steps: ['check logs', 'reproduce', 'fix', 'verify'],
      trigger: 'debug, api, 500',
      successRate: 0.9,
    });
    assert.ok(skill.id);
    assert.equal(skill.name, 'debug-api');
    assert.equal(skill.steps.length, 4);
    assert.equal(skill.successRate, 0.9);
  });

  it('getSkill() matches by trigger', async () => {
    await ctx.svc.learnSkill({
      name: 'deploy-steps',
      steps: ['build', 'test', 'deploy'],
      trigger: 'deploy, release',
    });

    const results = await ctx.svc.getSkill('deploy to production');
    assert.ok(results.length >= 1);
    assert.ok(results.some(s => s.name === 'deploy-steps'));
  });

  it('listSkills() returns all skills', async () => {
    const skills = await ctx.svc.listSkills();
    assert.ok(skills.length >= 2);
  });

  it('deleteSkill() removes a skill', async () => {
    const skill = await ctx.svc.learnSkill({
      name: 'temp-delete',
      steps: ['a'],
      trigger: 'temp',
    });
    const existed = await ctx.svc.deleteSkill(skill.id);
    assert.equal(existed, true);
    const existed2 = await ctx.svc.deleteSkill(skill.id);
    assert.equal(existed2, false);
  });

  it('recordSkillUsage() updates stats', async () => {
    const skill = await ctx.svc.learnSkill({
      name: 'usage-test',
      steps: ['a', 'b'],
      trigger: 'usage',
    });
    const ok = await ctx.svc.recordSkillUsage(skill.id, { success: true });
    assert.equal(ok, true);

    const skills = await ctx.svc.listSkills();
    const found = skills.find(s => s.id === skill.id);
    assert.equal(found.usageCount, 1);
    assert.equal(found.successRate, 1.0);

    const ok2 = await ctx.svc.recordSkillUsage(skill.id, { success: false });
    assert.equal(ok2, true);
    const skills2 = await ctx.svc.listSkills();
    const found2 = skills2.find(s => s.id === skill.id);
    assert.equal(found2.usageCount, 2);
    assert.equal(found2.successRate, 0.5);
  });

  it('recordSkillUsage() returns false for unknown id', async () => {
    const ok = await ctx.svc.recordSkillUsage('nonexistent', { success: true });
    assert.equal(ok, false);
  });
});
