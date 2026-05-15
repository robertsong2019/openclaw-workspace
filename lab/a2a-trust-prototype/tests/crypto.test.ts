// tests/crypto.test.ts
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { generateKeyPair, sign, verify, exportJWK, importJWK, canonicalizeJSON } from '../src/crypto.js';

describe('Crypto', () => {
  it('generates an ES256 key pair', async () => {
    const kp = await generateKeyPair();
    assert.ok(kp.publicKey);
    assert.ok(kp.privateKey);
    assert.equal(kp.publicKey.type, 'public');
    assert.equal(kp.privateKey.type, 'private');
  });

  it('signs and verifies a JSON object', async () => {
    const kp = await generateKeyPair();
    const data = { hello: 'world', num: 42 };
    const sig = await sign(kp.privateKey, data);
    assert.ok(typeof sig === 'string' && sig.length > 0);
    const valid = await verify(kp.publicKey, data, sig);
    assert.equal(valid, true);
  });

  it('rejects tampered data', async () => {
    const kp = await generateKeyPair();
    const data = { value: 100 };
    const sig = await sign(kp.privateKey, data);
    const tampered = { value: 999 };
    const valid = await verify(kp.publicKey, tampered, sig);
    assert.equal(valid, false);
  });

  it('rejects wrong key', async () => {
    const kp1 = await generateKeyPair();
    const kp2 = await generateKeyPair();
    const data = { foo: 'bar' };
    const sig = await sign(kp1.privateKey, data);
    const valid = await verify(kp2.publicKey, data, sig);
    assert.equal(valid, false);
  });

  it('exports and imports JWK for public key', async () => {
    const kp = await generateKeyPair();
    const jwk = await exportJWK(kp.publicKey);
    assert.equal(jwk.kty, 'EC');
    assert.equal(jwk.crv, 'P-256');
    assert.ok(jwk.x);
    assert.ok(jwk.y);
    const imported = await importJWK(jwk);
    // Verify it works
    const data = { test: 'jwk' };
    const sig = await sign(kp.privateKey, data);
    const valid = await verify(imported, data, sig);
    assert.equal(valid, true);
  });

  it('exports and imports JWK for private key', async () => {
    const kp = await generateKeyPair();
    const jwk = await exportJWK(kp.privateKey);
    assert.equal(jwk.kty, 'EC');
    // Re-import private key
    const imported = await importJWK(jwk, ['sign']);
    const data = { private: true };
    const sig = await sign(imported, data);
    const valid = await verify(kp.publicKey, data, sig);
    assert.equal(valid, true);
  });

  it('canonicalizes JSON with sorted keys', () => {
    const obj = { b: 2, a: 1, c: { z: 3, y: 2 } };
    const canonical = canonicalizeJSON(obj);
    assert.equal(canonical, '{"a":1,"b":2,"c":{"y":2,"z":3}}');
  });

  it('handles nested arrays in canonicalization', () => {
    const obj = { items: [3, 1, 2], name: 'test' };
    const canonical = canonicalizeJSON(obj);
    assert.equal(canonical, '{"items":[3,1,2],"name":"test"}');
  });
});
