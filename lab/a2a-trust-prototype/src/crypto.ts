// src/crypto.ts — ES256 signing/verification using Web Crypto API (zero deps)
import { webcrypto } from 'node:crypto';

const { subtle } = webcrypto;

export type PrivateKey = CryptoKey;
export type PublicKey = CryptoKey;
export type KeyPair = { publicKey: PublicKey; privateKey: PrivateKey };

/** Generate an ES256 (ECDSA P-256) key pair */
export async function generateKeyPair(): Promise<KeyPair> {
  const keyPair = await subtle.generateKey(
    { name: 'ECDSA', namedCurve: 'P-256' },
    true,
    ['sign', 'verify'],
  );
  return { publicKey: keyPair.publicKey, privateKey: keyPair.privateKey };
}

/** JCS-lite canonical JSON: recursive key sort, no whitespace */
function canonicalize(obj: unknown): string {
  if (obj === null || typeof obj !== 'object') {
    return JSON.stringify(obj);
  }
  if (Array.isArray(obj)) {
    return '[' + obj.map(canonicalize).join(',') + "]";
  }
  const sorted = Object.keys(obj as Record<string, unknown>)
    .sort()
    .map((k) => JSON.stringify(k) + ':' + canonicalize((obj as Record<string, unknown>)[k]));
  return '{' + sorted.join(',') + '}';
}

function toUint8Array(data: string): Uint8Array {
  return new TextEncoder().encode(data);
}

/** Sign a JSON object, return base64url signature */
export async function sign(privateKey: PrivateKey, data: unknown): Promise<string> {
  const canonical = canonicalize(data);
  const encoded = toUint8Array(canonical);
  const sigBuf = await subtle.sign(
    { name: 'ECDSA', hash: 'SHA-256' },
    privateKey,
    encoded,
  );
  return Buffer.from(sigBuf).toString('base64url');
}

/** Verify a signed JSON object */
export async function verify(
  publicKey: PublicKey,
  data: unknown,
  signature: string,
): Promise<boolean> {
  const canonical = canonicalize(data);
  const encoded = toUint8Array(canonical);
  const sigBuf = Buffer.from(signature, 'base64url');
  return subtle.verify(
    { name: 'ECDSA', hash: 'SHA-256' },
    publicKey,
    sigBuf,
    encoded,
  );
}

/** Export a CryptoKey as JWK */
export async function exportJWK(key: CryptoKey): Promise<JsonWebKey> {
  return subtle.exportKey('jwk', key);
}

/** Import a JWK as a public key (for verification) */
export async function importJWK(jwk: JsonWebKey, usages: KeyUsage[] = ['verify']): Promise<PublicKey> {
  return subtle.importKey(
    'jwk',
    jwk,
    { name: 'ECDSA', namedCurve: 'P-256' },
    true,
    usages,
  );
}

/** Canonicalize a JSON object (exported for reuse) */
export function canonicalizeJSON(obj: unknown): string {
  return canonicalize(obj);
}
