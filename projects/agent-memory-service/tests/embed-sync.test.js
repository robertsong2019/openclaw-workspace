import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { mkdir, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { readFile, writeFile } from 'node:fs/promises';

const DIR = join(import.meta.dirname, '..', 'data', 'test-embed-sync');

let callCount = 0;
const mockEmbed = async (text) => {
  callCount++;
  const len = text.length;
  return [len % 10, (len * 2) % 10, (len * 3) % 10];
};

const readEmbedCache = async () => {
  try {
    const raw = await readFile(join(DIR, 'embed-cache.json'), 'utf-8');
    return Object.keys(JSON.parse(raw)).length;
  } catch { return 0; }
};

const injectOrphan = async () => {
  const path = join(DIR, 'embed-cache.json');
  let obj = {};
  try {
    obj = JSON.parse(await readFile(path, 'utf-8'));
  } catch { /* empty */ }
  obj['__orphan_fake_hash__'] = [1, 2, 3];
  await writeFile(path, JSON.stringify(obj));
};

const freshStore = async () => {
  await rm(DIR, { recursive: true, force: true });
  await mkdir(DIR, { recursive: true });
  callCount = 0;
  const svc = new MemoryService({ dbPath: DIR, embedFn: mockEmbed });
  await svc.init();
  return svc;
};

describe('Embedding cache sync on delete/batchDelete', () => {
  it('delete() removes embedding from cache and persists', async () => {
    const store = await freshStore();
    const mem = await store.add({ content: 'hello world from embed sync test delete unique', layer: 'core' });
    const id = mem.id || mem;
    await store.search('hello');
    assert(callCount > 0, 'embed should have been called');
    const sizeBefore = await readEmbedCache();
    assert(sizeBefore > 0, 'cache should have entries');

    await store.delete(id);
    const sizeAfter = await readEmbedCache();
    assert(sizeAfter < sizeBefore, 'cache should shrink after delete');
  });

  it('batchDelete() removes embeddings from cache', async () => {
    const store = await freshStore();
    const mem1 = await store.add({ content: 'alpha beta gamma for batch embed sync test', layer: 'core' });
    const mem2 = await store.add({ content: 'delta epsilon zeta for batch embed sync test', layer: 'core' });
    const id1 = mem1.id || mem1;
    const id2 = mem2.id || mem2;
    await store.search('alpha');
    await store.search('delta');

    const sizeBefore = await readEmbedCache();
    await store.batchDelete([id1, id2]);
    const sizeAfter = await readEmbedCache();
    assert(sizeAfter < sizeBefore, 'cache should shrink after batchDelete');
  });

  it('compactEmbedCache() removes orphan entries injected into file', async () => {
    const store = await freshStore();
    const mem = await store.add({ content: 'orphan test content alpha unique string here', layer: 'core' });
    const id = mem.id || mem;
    await store.search('orphan');
    // Delete normally (cleans embed)
    await store.delete(id);
    // Inject orphan directly into file
    await injectOrphan();
    // Reload store from disk
    const store2 = new MemoryService({ dbPath: DIR, embedFn: mockEmbed });
    await store2.init();
    assert(store2.embeddings.cacheSize > 0, 'orphan should be loaded');

    const result = await store2.compactEmbedCache();
    assert.ok(result.removed >= 1, 'at least one orphan removed');
    assert.equal(store2.embeddings.cacheSize, 0, 'cache should be empty');
  });

  it('compactEmbedCache() dryRun does not modify cache', async () => {
    const store = await freshStore();
    const mem = await store.add({ content: 'dry run test content beta for embed cache check', layer: 'core' });
    const id = mem.id || mem;
    // Trigger embedding via search with content-like query
    await store.search('dry run test content beta for embed cache check');
    const sizeBefore = store.embeddings.cacheSize;
    assert(sizeBefore > 0, 'should have cached embeddings');

    const result = await store.compactEmbedCache({ dryRun: true });
    // Query embed hash != content hash, so it's an "orphan" in dryRun count
    // but cache should not actually change
    const sizeAfter = store.embeddings.cacheSize;
    assert.equal(sizeAfter, sizeBefore, 'cache unchanged in dryRun');
  });

  it('compactEmbedCache() cleans orphan after external manipulation', async () => {
    const store = await freshStore();
    const mem1 = await store.add({ content: 'manual cleanup gamma unique string here now', layer: 'core' });
    const mem2 = await store.add({ content: 'manual cleanup delta another unique string here', layer: 'core' });
    const id1 = mem1.id || mem1;
    const id2 = mem2.id || mem2;
    await store.search('manual cleanup');
    // Delete one (cleans its embed)
    await store.delete(id1);
    // Inject an orphan
    await injectOrphan();
    // Re-create store to pick up modified file
    const store2 = new MemoryService({ dbPath: DIR, embedFn: mockEmbed });
    await store2.init();
    const sizeWithOrphan = store2.embeddings.cacheSize;
    assert(sizeWithOrphan > 0, 'should have entries including orphan');

    const result = await store2.compactEmbedCache();
    assert.ok(result.removed >= 1, 'at least one orphan removed');
  });
});
