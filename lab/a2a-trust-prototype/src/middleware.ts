// src/middleware.ts — Trust-gated middleware for A2A communication
import { TrustEngine, type TrustLevel } from './trust-engine.js';
import type { KeyPair, PrivateKey } from './crypto.js';
import { sign, verify } from './crypto.js';
import type { SignedAgentCard } from './agent-card.js';
import { verifyAgentCard } from './agent-card.js';

export interface Middleware {
  /** Verify an inbound signed agent card */
  verifyInbound(signedCard: SignedAgentCard): Promise<boolean>;
  /** Sign outbound data with this agent's key */
  signOutbound(data: unknown): Promise<string>;
  /** Check if caller has sufficient trust for a skill */
  checkAccess(agentId: string, skillId: string, requiredLevel: TrustLevel): boolean;
}

/** Create a trust middleware instance */
export function createMiddleware(
  trustEngine: TrustEngine,
  keyPair: KeyPair,
): Middleware {
  return {
    async verifyInbound(signedCard: SignedAgentCard): Promise<boolean> {
      // Import the caller's public key from their card
      const callerPubKey = await crypto.subtle.importKey(
        'jwk',
        signedCard.publicKeyJwk,
        { name: 'ECDSA', namedCurve: 'P-256' },
        true,
        ['verify'],
      );
      return verifyAgentCard(signedCard, callerPubKey);
    },

    async signOutbound(data: unknown): Promise<string> {
      return sign(keyPair.privateKey, data);
    },

    checkAccess(agentId: string, skillId: string, requiredLevel: TrustLevel): boolean {
      // Per-skill trust takes priority
      const skillLevel = trustEngine.getSkillTrustLevel(agentId, skillId);
      if (skillLevel !== 'unknown') {
        const levels: TrustLevel[] = ['untrusted', 'neutral', 'trusted'];
        return levels.indexOf(skillLevel) >= levels.indexOf(requiredLevel);
      }
      // Fall back to overall trust
      return trustEngine.canDelegate(agentId, requiredLevel);
    },
  };
}
