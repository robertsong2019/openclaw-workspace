# A2A Trust Prototype

A minimal Agent-to-Agent (A2A) Trust Layer implemented in TypeScript with **zero external dependencies**.

## Overview

This prototype demonstrates how autonomous agents can establish and manage trust relationships using:

- **Cryptographic identity** — ES256 (ECDSA P-256) signed agent cards
- **Trust scoring** — Per-agent and per-skill trust levels with time decay
- **Access gating** — Middleware that enforces trust requirements per skill

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Agent Card  │────▶│  Middleware   │────▶│ TrustEngine │
│ (signed ID)  │     │ (verify/gate) │     │  (scoring)  │
└─────────────┘     └──────────────┘     └─────────────┘
       │                    │
   Crypto layer        Access control
   (ES256/JWK)        (per-skill trust)
```

## Components

### 1. Crypto (`src/crypto.ts`)
ES256 key generation, JCS canonicalization, sign/verify, JWK import/export.

### 2. TrustEngine (`src/trust-engine.ts`)
Per-agent trust scoring (0–100) with levels: `unknown`, `untrusted`, `neutral`, `trusted`.
Supports per-skill scoring, time decay, and trust reports.

### 3. SignedAgentCard (`src/agent-card.ts`)
Tamper-evident agent identity cards with cryptographic signatures and extension support.

### 4. TrustMiddleware (`src/middleware.ts`)
Inbound verification, outbound signing, and per-skill access gating.

## Quick Start

```bash
# Install dev dependencies (tsx + typescript only)
npm install

# Run all tests
npx tsx --test tests/*.test.ts
```

## Trust Levels

| Level | Score | Meaning |
|-------|-------|---------|
| unknown | — | No interaction record |
| untrusted | 0–49 | Failed interactions or decayed trust |
| neutral | 50–79 | Some positive interactions |
| trusted | 80–100 | Strong track record |

## Scoring Rules

- **Success**: +5 × max(0.1, 1 − count × 0.01) — diminishing returns
- **Failure**: −15 — significant penalty
- **Decay**: −0.1 per hour elapsed — trust stale if unused

## Example

```typescript
import { generateKeyPair, TrustEngine, signAgentCard, createMiddleware, exportJWK } from './src/index.js';

const keyPair = await generateKeyPair();
const engine = new TrustEngine();
const mw = createMiddleware(engine, keyPair);

// Build trust over interactions
engine.recordSkillInteraction('agent-bob', 'sql', true);
engine.recordSkillInteraction('agent-bob', 'sql', true);

// Check access
mw.checkAccess('agent-bob', 'sql', 'neutral'); // true
```

## Constraints

- **Zero runtime deps** — only `node:test`, `node:assert`, `node:crypto`
- TypeScript strict mode
- Each source file < 200 lines
- 27+ tests covering all components

## License

MIT
