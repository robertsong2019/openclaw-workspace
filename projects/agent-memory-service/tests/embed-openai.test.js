import { describe, it, mock } from 'node:test';
import assert from 'node:assert/strict';
import { createOpenAIEmbedFn, EmbeddingProvider } from '../src/index.js';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

describe('createOpenAIEmbedFn', () => {
  it('returns an async function', () => {
    const fn = createOpenAIEmbedFn({ apiKey: 'test-key' });
    assert.equal(typeof fn, 'function');
  });

  it('calls the embeddings API with correct parameters', async () => {
    const calls = [];
    const fakeVec = Array(8).fill(0.1);

    // Mock global fetch
    const originalFetch = globalThis.fetch;
    globalThis.fetch = async (url, opts) => {
      calls.push({ url, opts });
      return {
        ok: true,
        json: async () => ({ data: [{ embedding: fakeVec }] }),
      };
    };

    try {
      const fn = createOpenAIEmbedFn({
        baseUrl: 'https://example.com/v1',
        model: 'test-model',
        apiKey: 'sk-test',
        dimensions: 8,
      });
      const vec = await fn('hello world');
      assert.deepEqual(vec, fakeVec);

      assert.equal(calls.length, 1);
      assert.equal(calls[0].url, 'https://example.com/v1/embeddings');
      const body = JSON.parse(calls[0].opts.body);
      assert.equal(body.input, 'hello world');
      assert.equal(body.model, 'test-model');
      assert.equal(body.dimensions, 8);
      assert.equal(calls[0].opts.headers.Authorization, 'Bearer sk-test');
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it('uses defaults when opts are omitted', async () => {
    const calls = [];
    const originalFetch = globalThis.fetch;
    globalThis.fetch = async (url, opts) => {
      calls.push({ url, opts });
      return {
        ok: true,
        json: async () => ({ data: [{ embedding: [0.5] }] }),
      };
    };

    // Clear env temporarily
    const origEnv = process.env.OPENAI_API_KEY;
    process.env.OPENAI_API_KEY = 'env-key';
    try {
      const fn = createOpenAIEmbedFn();
      await fn('test');
      assert.equal(calls[0].url, 'https://api.openai.com/v1/embeddings');
      const body = JSON.parse(calls[0].opts.body);
      assert.equal(body.model, 'text-embedding-3-small');
      assert.ok(!body.dimensions);
      assert.equal(calls[0].opts.headers.Authorization, 'Bearer env-key');
    } finally {
      process.env.OPENAI_API_KEY = origEnv;
      globalThis.fetch = originalFetch;
    }
  });

  it('throws on non-ok response', async () => {
    const originalFetch = globalThis.fetch;
    globalThis.fetch = async () => ({
      ok: false,
      status: 401,
      text: async () => 'Unauthorized',
    });

    try {
      const fn = createOpenAIEmbedFn({ apiKey: 'bad' });
      await assert.rejects(() => fn('test'), /Embedding API 401/);
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it('throws when response has no embedding vector', async () => {
    const originalFetch = globalThis.fetch;
    globalThis.fetch = async () => ({
      ok: true,
      json: async () => ({ data: [{}] }),
    });

    try {
      const fn = createOpenAIEmbedFn({ apiKey: 'k' });
      await assert.rejects(() => fn('test'), /No embedding vector/);
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it('integrates with EmbeddingProvider for caching', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'embed-test-'));
    let callCount = 0;
    const fakeVec = [0.1, 0.2, 0.3];

    const originalFetch = globalThis.fetch;
    globalThis.fetch = async () => {
      callCount++;
      return { ok: true, json: async () => ({ data: [{ embedding: fakeVec }] }) };
    };

    try {
      const provider = new EmbeddingProvider(dir, createOpenAIEmbedFn({ apiKey: 'test' }));
      await provider.loadCache();

      // First call hits API
      const v1 = await provider.embed('hello');
      assert.deepEqual(v1, fakeVec);
      assert.equal(callCount, 1);

      // Second call uses cache
      const v2 = await provider.embed('hello');
      assert.deepEqual(v2, fakeVec);
      assert.equal(callCount, 1); // no additional API call
    } finally {
      globalThis.fetch = originalFetch;
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
