/**
 * withCache() — Memoization wrapper for LangGraph nodes.
 *
 * Caches node results based on a configurable key derived from state.
 * Avoids re-executing expensive nodes when the same input is seen again.
 */

export interface CacheConfig {
  /** Maximum cache entries (default: 100). Set to 0 to disable. */
  maxSize?: number;
  /** TTL in milliseconds (default: Infinity). Expired entries are lazily evicted. */
  ttlMs?: number;
  /** Derive cache key from state (default: JSON.stringify of entire state) */
  keyFn?: (state: Record<string, unknown>) => string;
  /** Cache name for stats key */
  name?: string;
}

interface CacheEntry {
  result: Record<string, unknown>;
  timestamp: number;
}

/**
 * Wrap a node with in-memory caching.
 */
export function withCache(
  node: (state: Record<string, unknown>) => Promise<Record<string, unknown>>,
  config: CacheConfig = {}
): (state: Record<string, unknown>) => Promise<Record<string, unknown>> {
  const maxSize = config.maxSize ?? 100;
  const ttlMs = config.ttlMs ?? Infinity;
  const keyFn = config.keyFn ?? ((s) => JSON.stringify(s));
  const name = config.name ?? "cache";

  const cache = new Map<string, CacheEntry>();
  let hits = 0;
  let misses = 0;

  async function cachedNode(state: Record<string, unknown>): Promise<Record<string, unknown>> {
    const key = keyFn(state);
    const now = Date.now();

    // Check cache
    const entry = cache.get(key);
    if (entry) {
      const age = now - entry.timestamp;
      if (age < ttlMs) {
        hits++;
        return { ...entry.result, [`${name}Hit`]: true };
      }
      // Expired — evict
      cache.delete(key);
    }

    // Cache miss
    misses++;
    const result = await node(state);

    // Evict oldest if at capacity
    if (maxSize > 0 && cache.size >= maxSize) {
      const oldest = cache.keys().next().value;
      if (oldest !== undefined) cache.delete(oldest);
    }

    if (maxSize > 0) {
      cache.set(key, { result, timestamp: now });
    }

    return { ...result, [`${name}Hit`]: false };
  }

  /** Get cache statistics */
  cachedNode.cacheStats = () => ({
    size: cache.size,
    maxSize,
    hits,
    misses,
    hitRate: hits + misses > 0 ? hits / (hits + misses) : 0,
  });

  /** Clear the cache */
  cachedNode.cacheClear = () => {
    cache.clear();
    hits = 0;
    misses = 0;
  };

  return cachedNode;
}
