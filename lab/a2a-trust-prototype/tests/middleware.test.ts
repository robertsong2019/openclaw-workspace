// tests/middleware.test.ts
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { generateKeyPair, exportJWK, sign } from '../src/crypto.js';
import { TrustEngine } from '../src/trust-engine.js';
import { createMiddleware } from '../src/middleware.js';
import { signAgentCard } from '../src/agent-card.js';
import type { AgentCard } from '../src/agent-card.js';

async function setup() {
  const myKey = await generateKeyPair();
  const engine = new TrustEngine();
  const mw = createMiddleware(engine, myKey);
  return { myKey, engine, mw };
}

async function makeCallerCard(callerKey: Awaited<ReturnType<typeof generateKeyPair>>) {
  const pubJwk = await exportJWK(callerKey.publicKey);
  const card: AgentCard = {
    id: 'caller-1',
    name: 'Caller',
    description: 'A caller agent',
    url: 'https://caller.example.com',
    skills: [{ id: 'sql', name: 'SQL', description: 'Query' }],
    publicKeyJwk: pubJwk,
    signedAt: Date.now(),
  };
  return signAgentCard(card, callerKey.privateKey);
}

describe('TrustMiddleware', () => {
  it('verifies a valid inbound signed card', async () => {
    const { mw } = await setup();
    const callerKey = await generateKeyPair();
    const signedCard = await makeCallerCard(callerKey);
    const valid = await mw.verifyInbound(signedCard);
    assert.equal(valid, true);
  });

  it('rejects tampered inbound card', async () => {
    const { mw } = await setup();
    const callerKey = await generateKeyPair();
    const signedCard = await makeCallerCard(callerKey);
    signedCard.name = 'Imposter';
    const valid = await mw.verifyInbound(signedCard);
    assert.equal(valid, false);
  });

  it('signs outbound data', async () => {
    const { myKey, mw } = await setup();
    const data = { response: 'ok', timestamp: Date.now() };
    const sig = await mw.signOutbound(data);
    // Verify with our own public key
    const { verify: cryptoVerify } = await import('../src/crypto.js');
    const valid = await cryptoVerify(myKey.publicKey, data, sig);
    assert.equal(valid, true);
  });

  it('grants access when trust is sufficient', async () => {
    const { engine, mw } = await setup();
    engine.recordInteraction('caller-1', true);
    engine.recordInteraction('caller-1', true);
    engine.recordSkillInteraction('caller-1', 'sql', true);
    // Should have neutral level at least
    assert.equal(mw.checkAccess('caller-1', 'sql', 'untrusted'), true);
    assert.equal(mw.checkAccess('caller-1', 'sql', 'neutral'), true);
  });

  it('denies access when trust is insufficient', async () => {
    const { engine, mw } = await setup();
    engine.recordInteraction('caller-1', false);
    // Untrusted agent
    assert.equal(mw.checkAccess('caller-1', 'sql', 'neutral'), false);
  });

  it('uses per-skill trust for gating', async () => {
    const { engine, mw } = await setup();
    // Good overall trust, bad skill-specific trust
    engine.recordInteraction('caller-1', true);
    engine.recordInteraction('caller-1', true);
    engine.recordSkillInteraction('caller-1', 'sql', false);
    // Overall is okay but sql-specific is bad
    assert.equal(mw.checkAccess('caller-1', 'sql', 'trusted'), false);
    // Unknown skill falls back to overall
    assert.equal(mw.checkAccess('caller-1', 'http', 'untrusted'), true);
  });
});
