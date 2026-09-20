// api-surface.test.ts — public API barrel + signAgentCard schema fidelity
// The barrel (src/index.ts) is the public API contract: nothing imported it
// before this file, so a renamed/moved export would rot silently.
// signAgentCard builds its signed payload via a MANUAL whitelist copy of the
// AgentCard schema — a field added to the interface but not to the copy is
// dropped from every signed card with no error (silent-field-loss family).
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import {
  generateKeyPair, sign, verify, exportJWK, importJWK, canonicalizeJSON,
  TrustEngine, signAgentCard, verifyAgentCard, createMiddleware,
  type AgentCard, type SignedAgentCard,
} from '../src/index.js';

const RUNTIME_EXPORTS: Array<[string, unknown]> = [
  ['generateKeyPair', generateKeyPair],
  ['sign', sign],
  ['verify', verify],
  ['exportJWK', exportJWK],
  ['importJWK', importJWK],
  ['canonicalizeJSON', canonicalizeJSON],
  ['TrustEngine', TrustEngine],
  ['signAgentCard', signAgentCard],
  ['verifyAgentCard', verifyAgentCard],
  ['createMiddleware', createMiddleware],
];

describe('api-surface: barrel export contract', () => {
  it('exposes every documented runtime export as a function/constructor', () => {
    for (const [name, val] of RUNTIME_EXPORTS) {
      assert.equal(typeof val, 'function', `${name} must be exported and callable`);
    }
  });

  it('TrustEngine is constructible from the barrel', () => {
    const engine = new TrustEngine();
    assert.equal(engine.getTrustLevel('nobody'), 'unknown');
  });

  it('full round-trip works through the barrel import path alone', async () => {
    const { publicKey, privateKey } = await generateKeyPair();
    const card: AgentCard = {
      id: 'did:a2a:barrel-agent', name: 'Barrel Agent', description: 'e2e',
      url: 'https://example.agents/barrel',
      skills: [{ id: 's1', name: 'search', description: 'web search' }],
      publicKeyJwk: await exportJWK(publicKey),
      signedAt: 1726848000000,
      extensions: { trust: { requiredLevel: 'neutral' } },
    };
    const signed = await signAgentCard(card, privateKey);
    const jwk = await importJWK(card.publicKeyJwk);
    assert.equal(await verifyAgentCard(signed, jwk), true);
  });
});

function maxCard(publicKeyJwk: JsonWebKey): AgentCard & { futureField: string } {
  return {
    id: 'did:a2a:max', name: 'Max', description: 'schema-sync probe',
    url: 'https://example.agents/max',
    skills: [{ id: 's', name: 'n', description: 'd' }],
    publicKeyJwk,
    signedAt: 1,
    extensions: { trust: { requiredLevel: 'trusted', perSkillPolicies: { s: 'neutral' } } },
    futureField: 'added-to-interface-but-forgot-signAgentCard',
  };
}

describe('signAgentCard: schema fidelity', () => {
  it('signed payload carries every schema field incl. both trust sub-fields', async () => {
    const { privateKey } = await generateKeyPair();
    const card = maxCard((await generateKeyPair()).publicKey as unknown as JsonWebKey);
    const signed = await signAgentCard(card, privateKey);
    for (const key of ['id', 'name', 'description', 'url', 'skills', 'publicKeyJwk', 'signedAt', 'extensions'] as const) {
      assert.ok(key in signed, `schema field ${key} missing from signed card`);
    }
    assert.deepEqual(signed.extensions?.trust?.perSkillPolicies, { s: 'neutral' });
  });

  it('unknown extra fields are whitelisted OUT of the signed payload (pinned semantics)', async () => {
    const { privateKey } = await generateKeyPair();
    const card = maxCard((await generateKeyPair()).publicKey as unknown as JsonWebKey);
    const signed = await signAgentCard(card, privateKey);
    assert.equal('futureField' in signed, false,
      'extra fields must not leak into the signed card — if this fails, the whitelist was widened');
  });

  it('post-signature mutation of skills breaks verify (fail-closed tamper evidence)', async () => {
    const { publicKey, privateKey } = await generateKeyPair();
    const card = maxCard(await exportJWK(publicKey));
    const signed: SignedAgentCard = await signAgentCard(card, privateKey);
    signed.skills.push({ id: 'injected', name: 'x', description: 'added after signing' });
    const jwk = await importJWK(card.publicKeyJwk);
    assert.equal(await verifyAgentCard(signed, jwk), false);
  });
});

describe('card-path wire fidelity', () => {
  it('signed card survives JSON.stringify/parse and key-order permutation', async () => {
    const { publicKey, privateKey } = await generateKeyPair();
    const card = maxCard(await exportJWK(publicKey));
    const signed = await signAgentCard(card, privateKey);
    const jwk = await importJWK(card.publicKeyJwk);

    const wire = JSON.parse(JSON.stringify(signed)) as SignedAgentCard;
    assert.equal(await verifyAgentCard(wire, jwk), true);

    // Reverse top-level key order (canonicalize must absorb ordering)
    const reordered = Object.fromEntries(
      Object.entries({ signature: wire.signature, ...wire }).reverse(),
    ) as SignedAgentCard;
    assert.equal(await verifyAgentCard(reordered, jwk), true);
  });

  it('canonicalizeJSON from the barrel matches crypto-internal canonical form', () => {
    assert.equal(canonicalizeJSON({ b: 1, a: [undefined, { d: 2, c: undefined }] }),
      '{"a":[null,{"d":2}],"b":1}');
  });
});
