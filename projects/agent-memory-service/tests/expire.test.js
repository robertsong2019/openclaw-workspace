import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';

describe('expiresAt + purgeExpired', () => {
  let svc;

  beforeEach(async () => {
    svc = new MemoryService({ dbPath: `/tmp/mem-expire-${Date.now()}` });
    await svc.init();
  });

  it('stores expiresAt when provided', async () => {
    const ts = Date.now() + 3600_000;
    const m = await svc.add({ content: 'temp note', expiresAt: ts });
    assert.equal(m.expiresAt, ts);
  });

  it('omits expiresAt when not provided', async () => {
    const m = await svc.add({ content: 'permanent note' });
    assert.equal(m.expiresAt, undefined);
  });

  it('purgeExpired removes expired memories', async () => {
    const past = Date.now() - 1000;
    const m1 = await svc.add({ content: 'expired', expiresAt: past });
    const m2 = await svc.add({ content: 'valid', expiresAt: Date.now() + 3600_000 });
    const m3 = await svc.add({ content: 'no expiry' });

    const { purged } = await svc.purgeExpired();
    assert.equal(purged.length, 1);
    assert.equal(purged[0], m1.id);

    // m2 and m3 still exist
    assert.ok(await svc.get(m2.id));
    assert.ok(await svc.get(m3.id));
    // m1 gone
    assert.equal(await svc.get(m1.id), undefined);
  });

  it('purgeExpired returns empty when nothing expired', async () => {
    await svc.add({ content: 'future', expiresAt: Date.now() + 9999_000 });
    const { purged } = await svc.purgeExpired();
    assert.equal(purged.length, 0);
  });

  it('expired memory not found via get after purge', async () => {
    const past = Date.now() - 1000;
    const m = await svc.add({ content: 'unique expired xyz', expiresAt: past });
    await svc.purgeExpired();

    assert.equal(await svc.get(m.id), undefined);
  });
});
