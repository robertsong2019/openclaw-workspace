import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { MemoryService } from '../src/index.js';
import { mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

describe('merge re-link persistence (RED: links.json kept dangling refs)', () => {
  it('persists re-pointed links across reload — no dangling refs to absorbed memory', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'merge-relink-'));
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();

    const a = await svc.add({ content: 'keeper memory', layer: 'long', tags: [] });
    const b = await svc.add({ content: 'absorbed memory', layer: 'short', tags: [] });
    const c = await svc.add({ content: 'bystander memory', layer: 'short', tags: [] });
    await svc.link({ source: c.id, target: b.id, type: 'related', weight: 0.9 });

    const merged = await svc.merge(a.id, b.id);
    assert.ok(merged);
    assert.equal(await svc.get(b.id), undefined, 'absorbed memory deleted');

    // Fresh service on same dbPath — persisted state must be consistent
    const svc2 = new MemoryService({ dbPath: dir });
    await svc2.init();

    // 1. Raw links.json: no reference to the deleted absorbed memory
    const raw = JSON.parse(readFileSync(join(dir, 'links.json'), 'utf-8'));
    for (const l of raw) {
      assert.notEqual(l.source, b.id, `links.json source still references deleted memory ${b.id}`);
      assert.notEqual(l.target, b.id, `links.json target still references deleted memory ${b.id}`);
    }

    // 2. Reloaded graph: bystander's link now points at the keeper
    const cLinks = await svc2.getLinks(c.id);
    assert.equal(cLinks.length, 1, 'reloaded graph lost the bystander link entirely');
    assert.ok(
      cLinks[0].source === a.id || cLinks[0].target === a.id,
      `reloaded link still references absorbed memory: ${JSON.stringify(cLinks[0])}`
    );
  });

  it('keeps in-memory index consistent — forMemory(a) sees the rewritten link before save', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'merge-relink-'));
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();
    const a = await svc.add({ content: 'keeper', layer: 'short', tags: [] });
    const b = await svc.add({ content: 'absorbed', layer: 'short', tags: [] });
    const c = await svc.add({ content: 'bystander', layer: 'short', tags: [] });
    await svc.link({ source: c.id, target: b.id, type: 'related', weight: 0.5 });

    await svc.merge(a.id, b.id);

    // getLinks is a live read over the index — must show keeper, not absorbed
    const aLinks = await svc.getLinks(a.id);
    assert.equal(aLinks.length, 1, 'in-memory index missing re-pointed link on keeper');
    const bLinks = await svc.getLinks(b.id);
    assert.equal(bLinks.length, 0, 'in-memory index still routes through deleted absorbed id');
  });

  it('merge with no inbound links still succeeds (repoint is a no-op)', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'merge-relink-'));
    const svc = new MemoryService({ dbPath: dir });
    await svc.init();
    const a = await svc.add({ content: 'keeper', layer: 'short', tags: [] });
    const b = await svc.add({ content: 'absorbed', layer: 'short', tags: [] });

    const merged = await svc.merge(a.id, b.id);
    assert.ok(merged);
    assert.ok(merged.content.includes('keeper'));
    // links.json is written lazily (only when dirty) — verify via fresh reload instead
    const svc2 = new MemoryService({ dbPath: dir });
    await svc2.init();
    assert.deepEqual(await svc2.getLinks(a.id), []);
    assert.equal(await svc2.get(b.id), undefined);
  });
});
