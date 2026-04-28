import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

function createService() {
  const dir = mkdtempSync(join(tmpdir(), 'merge-'));
  return new MemoryService({ dbPath: dir });
}

describe('memoryMerge', () => {
  it('merges two memories with concat strategy (default)', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'hello', layer: 'L1', tags: ['a'] });
    const b = await svc.add({ content: 'world', layer: 'L1', tags: ['b'] });
    const result = await svc.memoryMerge(a.id, b.id);
    assert.ok(result);
    assert.equal(result.merged.content, 'hello\nworld');
    assert.deepEqual(result.merged.tags.sort(), ['a', 'b']);
    assert.equal(result.deletedId, b.id);
    assert.equal(await svc.get(b.id), undefined);
  });

  it('supports keep-longer content strategy', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'hi', layer: 'L1', tags: [] });
    const b = await svc.add({ content: 'hello world', layer: 'L1', tags: [] });
    const result = await svc.memoryMerge(a.id, b.id, { contentStrategy: 'keep-longer' });
    assert.equal(result.merged.content, 'hello world');
  });

  it('supports keep-newer content strategy', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'old', layer: 'L1', tags: [] });
    await new Promise(r => setTimeout(r, 10));
    const b = await svc.add({ content: 'new', layer: 'L1', tags: [] });
    const result = await svc.memoryMerge(a.id, b.id, { contentStrategy: 'keep-newer' });
    assert.equal(result.merged.content, 'new');
  });

  it('supports manual content strategy', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'aaa', layer: 'L1', tags: [] });
    const b = await svc.add({ content: 'bbb', layer: 'L1', tags: [] });
    const result = await svc.memoryMerge(a.id, b.id, { contentStrategy: 'manual', content: 'custom' });
    assert.equal(result.merged.content, 'custom');
  });

  it('merges entities as union', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'x', layer: 'L1', tags: [], entities: ['e1', 'e2'] });
    const b = await svc.add({ content: 'y', layer: 'L1', tags: [], entities: ['e2', 'e3'] });
    const result = await svc.memoryMerge(a.id, b.id);
    assert.deepEqual(result.merged.entities.sort(), ['e1', 'e2', 'e3']);
  });

  it('supports tag strategy: primary only', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'a', layer: 'L1', tags: ['keep'] });
    const b = await svc.add({ content: 'b', layer: 'L1', tags: ['drop'] });
    const result = await svc.memoryMerge(a.id, b.id, { tagStrategy: 'primary' });
    assert.deepEqual(result.merged.tags, ['keep']);
  });

  it('rewires links from secondary to primary by default', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'a', layer: 'L1', tags: [] });
    const b = await svc.add({ content: 'b', layer: 'L1', tags: [] });
    const c = await svc.add({ content: 'c', layer: 'L1', tags: [] });
    await svc.link({ source: b.id, target: c.id, type: 'ref' });
    const result = await svc.memoryMerge(a.id, b.id);
    assert.equal(result.stats.rewiredLinks, 1);
    const links = await svc.getLinks(a.id);
    const refLinks = links.filter(l => l.type === 'ref');
    assert.ok(refLinks.length >= 1, 'primary should have inherited ref link');
  });

  it('drops links with drop strategy', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'a', layer: 'L1', tags: [] });
    const b = await svc.add({ content: 'b', layer: 'L1', tags: [] });
    const c = await svc.add({ content: 'c', layer: 'L1', tags: [] });
    await svc.link({ source: b.id, target: c.id, type: 'ref' });
    const result = await svc.memoryMerge(a.id, b.id, { linkStrategy: 'drop' });
    assert.equal(result.stats.droppedLinks, 1);
    assert.equal(result.stats.rewiredLinks, 0);
  });

  it('returns null for non-existent memories', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'a', layer: 'L1', tags: [] });
    assert.equal(await svc.memoryMerge(a.id, 'nope'), null);
    assert.equal(await svc.memoryMerge('nope', a.id), null);
  });

  it('returns null when merging same memory', async () => {
    const svc = createService();
    await svc.init();
    const a = await svc.add({ content: 'a', layer: 'L1', tags: [] });
    assert.equal(await svc.memoryMerge(a.id, a.id), null);
  });
});
