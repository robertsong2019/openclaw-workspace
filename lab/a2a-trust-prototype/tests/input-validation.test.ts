// tests/input-validation.test.ts — RED-first: fail-open requiredLevel + JSON wire fidelity
// Family: invalid-config→silent-disaster (fail-fast-at-boundary is the standard fix).
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { generateKeyPair, sign, verify } from '../src/crypto.js';
import { TrustEngine, type TrustLevel } from '../src/trust-engine.js';
import { createMiddleware } from '../src/middleware.js';

describe('requiredLevel fail-open', () => {
  it('canDelegate throws on invalid requiredLevel instead of allowing everything', () => {
    const engine = new TrustEngine();
    engine.recordInteraction('a', true);
    // 'TRUSTED' (wrong case) and 'garbage' would both indexOf to -1 → allow-all before fix
    assert.throws(() => engine.canDelegate('a', 'TRUSTED' as TrustLevel), /invalid requiredLevel/);
    assert.throws(() => engine.canDelegate('a', 'trusted ' as TrustLevel), /invalid requiredLevel/);
    assert.throws(() => engine.canDelegate('a', undefined as unknown as TrustLevel), /invalid requiredLevel/);
  });

  it('canDelegate still accepts all four legitimate levels', () => {
    const engine = new TrustEngine();
    engine.recordInteraction('a', true); // neutral-ish
    for (const lvl of ['unknown', 'untrusted', 'neutral', 'trusted'] as TrustLevel[]) {
      engine.canDelegate('a', lvl); // must not throw
    }
  });

  it('checkAccess throws on invalid requiredLevel instead of allowing everything', () => {
    const engine = new TrustEngine();
    const mw = createMiddleware(engine, { publicKey: null as never, privateKey: null as never });
    engine.recordInteraction('caller', true);
    assert.throws(() => mw.checkAccess('caller', 'sql', 'TRUSTED' as TrustLevel), /invalid requiredLevel/);
    assert.throws(() => mw.checkAccess('caller', 'sql', 'unknown' as TrustLevel), /invalid requiredLevel/);
  });

  it('checkAccess still accepts the three legitimate gating levels', () => {
    const engine = new TrustEngine();
    const mw = createMiddleware(engine, { publicKey: null as never, privateKey: null as never });
    engine.recordInteraction('caller', true);
    engine.recordInteraction('caller', true);
    for (const lvl of ['untrusted', 'neutral', 'trusted'] as TrustLevel[]) {
      mw.checkAccess('caller', 'sql', lvl); // must not throw
    }
  });
});

describe('canonicalize JSON wire fidelity', () => {
  it('signature survives JSON.stringify round-trip (undefined properties)', async () => {
    const key = await generateKeyPair();
    const data = { a: 1, b: undefined, c: 'x' };
    const sig = await sign(key.privateKey, data);
    const wire = JSON.parse(JSON.stringify(data)); // b dropped by JSON semantics
    assert.equal(await verify(key.publicKey, wire, sig), true);
  });

  it('undefined array elements canonicalize as null like JSON', async () => {
    const key = await generateKeyPair();
    const data = { arr: [1, undefined, 2] };
    const sig = await sign(key.privateKey, data);
    const wire = JSON.parse(JSON.stringify(data)); // [1, null, 2]
    assert.equal(await verify(key.publicKey, wire, sig), true);
  });

  it('nested undefined inside objects and arrays', async () => {
    const key = await generateKeyPair();
    const data = { meta: { x: undefined, y: 2 }, list: [{ z: undefined }] };
    const sig = await sign(key.privateKey, data);
    const wire = JSON.parse(JSON.stringify(data));
    assert.equal(await verify(key.publicKey, wire, sig), true);
  });
});
