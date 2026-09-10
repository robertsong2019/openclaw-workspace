// tests/security-hardening.test.ts — RED-first security characterization
// Family: fail-open / identity-assertion bugs in the trust layer.
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { generateKeyPair, exportJWK } from '../src/crypto.js';
import { TrustEngine } from '../src/trust-engine.js';
import { createMiddleware } from '../src/middleware.js';
import { signAgentCard } from '../src/agent-card.js';
import type { AgentCard, SignedAgentCard } from '../src/agent-card.js';
import type { KeyPair } from '../src/crypto.js';

async function makeCard(key: KeyPair, id: string): Promise<SignedAgentCard> {
  const pubJwk = await exportJWK(key.publicKey);
  const card: AgentCard = {
    id,
    name: `Agent ${id}`,
    description: 'test agent',
    url: `https://${id}.example.com`,
    skills: [{ id: 'sql', name: 'SQL', description: 'Query' }],
    publicKeyJwk: pubJwk,
    signedAt: Date.now(),
  };
  return signAgentCard(card, key.privateKey);
}

describe('verifyInbound identity pinning', () => {
  it('rejects attacker self-signed card claiming a pinned identity', async () => {
    const victimKey = await generateKeyPair();
    const mw = createMiddleware(new TrustEngine(), await generateKeyPair());
    // Attacker generates their OWN keypair but claims the victim's agent id.
    const forged = await makeCard(await generateKeyPair(), 'trusted-agent');
    // Registry-pinned public key for 'trusted-agent' is the VICTIM's key.
    const pinnedJwk = await exportJWK(victimKey.publicKey);
    const valid = await mw.verifyInbound(forged, pinnedJwk);
    assert.equal(valid, false, 'self-consistent forgery must not pass pinning check');
  });

  it('accepts genuine card signed by the pinned key', async () => {
    const genuineKey = await generateKeyPair();
    const mw = createMiddleware(new TrustEngine(), await generateKeyPair());
    const genuine = await makeCard(genuineKey, 'trusted-agent');
    const pinnedJwk = await exportJWK(genuineKey.publicKey);
    assert.equal(await mw.verifyInbound(genuine, pinnedJwk), true);
  });

  it('rejects tampered card even when signed by the pinned key', async () => {
    const genuineKey = await generateKeyPair();
    const mw = createMiddleware(new TrustEngine(), await generateKeyPair());
    const genuine = await makeCard(genuineKey, 'trusted-agent');
    const pinnedJwk = await exportJWK(genuineKey.publicKey);
    genuine.description = 'tampered after signing';
    assert.equal(await mw.verifyInbound(genuine, pinnedJwk), false);
  });

  it('without a pinned key, self-consistency mode is unchanged (documented legacy behavior)', async () => {
    const mw = createMiddleware(new TrustEngine(), await generateKeyPair());
    const forged = await makeCard(await generateKeyPair(), 'trusted-agent');
    // Legacy mode only proves the card agrees with its embedded key.
    assert.equal(await mw.verifyInbound(forged), true);
  });
});

describe('scoreDecay input validation', () => {
  it('negative hours is a no-op — no time travel trust boost', () => {
    const engine = new TrustEngine();
    engine.recordInteraction('a', true);
    const before = engine.getScore('a');
    engine.scoreDecay('a', -24);
    assert.equal(engine.getScore('a'), before, 'negative elapsed time must not increase score');
  });

  it('NaN hours is a no-op — score must stay a number', () => {
    const engine = new TrustEngine();
    engine.recordInteraction('a', true);
    const before = engine.getScore('a');
    engine.scoreDecay('a', Number.NaN);
    const after = engine.getScore('a');
    assert.equal(typeof after, 'number');
    assert.equal(after, before, 'NaN elapsed time must not change score');
  });
});
