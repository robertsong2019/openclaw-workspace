import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'sbc-'));
  const svc = new MemoryService({ dbPath: dir });
  return { svc, dir };
}

describe('searchByContent', () => {
  it('returns matching memories with correct metadata', async () => {
    const { svc, dir } = createService();
    await svc.add({ content: 'The quick brown fox jumps over the lazy dog', layer: 'L1', tags: ['animals'] });
    await svc.add({ content: 'Python is a great programming language', layer: 'L2', tags: ['tech', 'python'] });
    await svc.add({ content: 'The lazy cat sleeps all day', layer: 'L1', tags: ['animals'] });
    await svc.add({ content: 'JavaScript frameworks in 2026', layer: 'L2', tags: ['tech'] });
    const res = await svc.searchByContent('lazy');
    assert.equal(res.total, 2);
    assert.equal(res.pattern, 'lazy');
    assert.ok(res.results.every(r => r.match === 'lazy'));
    rmSync(dir, { recursive: true });
  });

  it('filters by layer', async () => {
    const { svc, dir } = createService();
    await svc.add({ content: 'lazy fox', layer: 'L1' });
    await svc.add({ content: 'lazy python', layer: 'L2' });
    const res = await svc.searchByContent('lazy', { layer: 'L1' });
    assert.equal(res.total, 1);
    assert.equal(res.results[0].layer, 'L1');
    rmSync(dir, { recursive: true });
  });

  it('filters by tags (OR match)', async () => {
    const { svc, dir } = createService();
    await svc.add({ content: 'Python programming', layer: 'L2', tags: ['tech'] });
    await svc.add({ content: 'Snake programming', layer: 'L1', tags: ['nature'] });
    const res = await svc.searchByContent('programming', { tags: ['tech'] });
    assert.equal(res.total, 1);
    rmSync(dir, { recursive: true });
  });

  it('supports regex mode', async () => {
    const { svc, dir } = createService();
    await svc.add({ content: 'fox jumps', layer: 'L1' });
    await svc.add({ content: 'cat sleeps', layer: 'L1' });
    await svc.add({ content: 'bird flies', layer: 'L1' });
    const res = await svc.searchByContent('(fox|cat)', { regex: true });
    assert.equal(res.total, 2);
    rmSync(dir, { recursive: true });
  });

  it('supports case-sensitive mode', async () => {
    const { svc, dir } = createService();
    await svc.add({ content: 'Python is great', layer: 'L1' });
    await svc.add({ content: 'python the snake', layer: 'L1' });
    const res = await svc.searchByContent('Python', { caseSensitive: true });
    assert.equal(res.total, 1);
    rmSync(dir, { recursive: true });
  });

  it('paginates with offset and limit', async () => {
    const { svc, dir } = createService();
    await svc.add({ content: 'the dog', layer: 'L1' });
    await svc.add({ content: 'the cat', layer: 'L1' });
    await svc.add({ content: 'the bird', layer: 'L1' });
    const res = await svc.searchByContent('the', { offset: 0, limit: 2 });
    assert.equal(res.total, 3);
    assert.equal(res.results.length, 2);
    assert.equal(res.offset, 0);
    assert.equal(res.limit, 2);
    rmSync(dir, { recursive: true });
  });

  it('returns empty for no matches', async () => {
    const { svc, dir } = createService();
    await svc.add({ content: 'hello world', layer: 'L1' });
    const res = await svc.searchByContent('xyzzy12345');
    assert.equal(res.total, 0);
    assert.deepEqual(res.results, []);
    rmSync(dir, { recursive: true });
  });

  it('handles invalid regex gracefully', async () => {
    const { svc, dir } = createService();
    await svc.add({ content: 'test', layer: 'L1' });
    const res = await svc.searchByContent('([invalid', { regex: true });
    assert.equal(res.total, 0);
    assert.deepEqual(res.results, []);
    rmSync(dir, { recursive: true });
  });

  it('match field contains the actual matched substring', async () => {
    const { svc, dir } = createService();
    await svc.add({ content: 'The quick brown fox', layer: 'L1' });
    const res = await svc.searchByContent('quick brown');
    assert.equal(res.total, 1);
    assert.equal(res.results[0].match, 'quick brown');
    rmSync(dir, { recursive: true });
  });

  it('substring mode escapes special regex chars', async () => {
    const { svc, dir } = createService();
    await svc.add({ content: 'Price: $50.00 (discount)', layer: 'L1' });
    const res = await svc.searchByContent('$50.00');
    assert.equal(res.total, 1);
    assert.equal(res.results[0].match, '$50.00');
    rmSync(dir, { recursive: true });
  });
});
