// src/index.ts — Public API barrel export
export { generateKeyPair, sign, verify, exportJWK, importJWK, canonicalizeJSON } from './crypto.js';
export type { PrivateKey, PublicKey, KeyPair } from './crypto.js';
export { TrustEngine } from './trust-engine.js';
export type { TrustLevel } from './trust-engine.js';
export { signAgentCard, verifyAgentCard } from './agent-card.js';
export type { AgentCard, SignedAgentCard, Skill, TrustExtension } from './agent-card.js';
export { createMiddleware } from './middleware.js';
export type { Middleware } from './middleware.js';
