// src/agent-card.ts — Signed agent identity cards
import type { PrivateKey, PublicKey } from './crypto.js';
import { sign, verify } from './crypto.js';

export interface Skill {
  id: string;
  name: string;
  description: string;
}

export interface TrustExtension {
  requiredLevel?: string;
  perSkillPolicies?: Record<string, string>;
}

export interface AgentCard {
  id: string;
  name: string;
  description: string;
  url: string;
  skills: Skill[];
  publicKeyJwk: JsonWebKey;
  signedAt: number;
  extensions?: { trust?: TrustExtension; [k: string]: unknown };
}

export interface SignedAgentCard extends AgentCard {
  signature: string;
}

/** Sign an agent card with the agent's private key */
export async function signAgentCard(
  card: AgentCard,
  privateKey: PrivateKey,
): Promise<SignedAgentCard> {
  // Create a clean copy without signature for signing
  const payload: AgentCard = {
    id: card.id,
    name: card.name,
    description: card.description,
    url: card.url,
    skills: card.skills,
    publicKeyJwk: card.publicKeyJwk,
    signedAt: card.signedAt,
  };
  if (card.extensions) {
    payload.extensions = card.extensions;
  }
  const signature = await sign(privateKey, payload);
  return { ...payload, signature };
}

/** Verify a signed agent card's signature */
export async function verifyAgentCard(
  signedCard: SignedAgentCard,
  publicKey: PublicKey,
): Promise<boolean> {
  const { signature, ...payload } = signedCard;
  return verify(publicKey, payload, signature);
}
