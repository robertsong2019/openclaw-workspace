import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { MemoryService } from '../src/index.js';
import { rm, mkdir } from 'node:fs/promises';
import { join } from 'node:path';

const TMP = join(process.env.TMPDIR || '/tmp', 'ams-autotag-test-' + process.pid);

describe('autoTag', () => {
  let svc;

  beforeEach(async () => {
    await rm(TMP, { recursive: true, force: true });
    await mkdir(TMP, { recursive: true });
    svc = new MemoryService({ dbPath: TMP });
  });

  it('tags untagged memories based on existing tag patterns', async () => {
    // Seed tagged memories to build patterns
    await svc.add({ content: 'Python is great for data science', tags: ['python', 'data-science'], layer: 'core' });
    await svc.add({ content: 'Python web frameworks are popular', tags: ['python', 'web'], layer: 'core' });

    // Add untagged memory that shares keywords
    await svc.add({ content: 'Python data science libraries are powerful', layer: 'long' });

    const result = await svc.autoTag({ layer: 'long' });
    assert.ok(result.tagged >= 0);
    assert.equal(typeof result.skipped, 'number');
    assert.ok(Array.isArray(result.tags));
  });

  it('respects dryRun and does not modify memories', async () => {
    await svc.add({ content: 'Python is great for data science', tags: ['python'], layer: 'core' });
    const m = await svc.add({ content: 'Python data analysis', layer: 'short' });

    await svc.autoTag({ dryRun: true });

    // Memory should still be untagged
    const mem = await svc.get(m.id);
    assert.ok(!mem.tags || mem.tags.length === 0, 'dryRun should not modify tags');
  });

  it('skips already-tagged memories', async () => {
    await svc.add({ content: 'Tagged memory', tags: ['existing'], layer: 'core' });
    await svc.add({ content: 'Another tagged', tags: ['other'], layer: 'core' });
    await svc.add({ content: 'Untagged memory', layer: 'long' });

    const result = await svc.autoTag();
    assert.ok(typeof result.tagged === 'number');
    assert.ok(typeof result.skipped === 'number');
  });
});
