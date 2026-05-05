# Key Development Task 2 (Loop B) - 2026-05-06 00:00

## Focus: Autoresearch Methodology — TTL-based Embedding Cache Eviction

### Baseline
- 41 embed-related tests passing (after LRU eviction from k-d-2 05-05)
- EmbeddingProvider had no time-based expiry — stale vectors could persist forever

### 🎯 Target
**Add TTL-based cache eviction to EmbeddingProvider.**

**Problem:** The LRU eviction (k-d-2 05-05) bounds cache by count, but stale embeddings from old data persist indefinitely. For agents that update memories frequently, cached vectors become outdated with no automatic refresh mechanism.

**Solution:** `cacheTTL` option (ms). Track insertion timestamps per cache entry. Auto-expire on access (transparent re-embed). `evictExpired()` for bulk cleanup.

### 🛠 Implementation

**EmbeddingProvider (~30 lines added):**
- `#cacheTimestamps` Map — parallel to #cache, tracks insertion time
- `opts.cacheTTL` constructor param (0 = no expiry, default)
- `setCacheTTL(ms)` / `get cacheTTL` — runtime adjustment
- `evictExpired()` — bulk remove entries older than TTL, returns count
- `embed()` — checks TTL on cache hit, re-embeds if expired
- `loadCache()` — reads both legacy `{key: vector}` and new `{key: {vector, ts}}` formats
- `saveCache()` — persists timestamps alongside vectors

**7 new tests (embedCacheTTL.test.js):**
1. ✅ cacheTTL=0 means no expiry
2. ✅ Evicts expired entries on access (transparent re-embed)
3. ✅ Non-expired entries served from cache
4. ✅ evictExpired() removes all stale entries
5. ✅ setCacheTTL() changes TTL at runtime
6. ✅ Timestamps persist across loadCache/saveCache
7. ✅ Legacy cache format (vector-only) loads correctly

### 📊 Results
- 41 → 48 embed tests (all passing)
- Zero regressions in existing tests
- Committed: `7e9089e`

### ✅ Decision: RETAIN

**Rationale:**
- Completes the cache management story: LRU (size) + TTL (freshness) + compact (recovery)
- Backward-compatible: legacy caches load without timestamps, new saves include them
- Opt-in: default cacheTTL=0 means no change for existing users
- Transparent: expired entries auto-re-embed without caller changes
- Clean ~30 lines implementation

### experiments.tsv
```
2026-05-06T00:00	7e9089e	test_count	48/48	keep	TTL-based embedding cache eviction. cacheTTL (0=no expiry). Auto-expiry on access + evictExpired() bulk. Backward-compatible persistence. 7 new tests (41→48). Builds on LRU eviction from k-d-2.
```

---

**Generated**: 2026-05-06 00:00 AM
**Status:** ✅ Complete — 48/48 embed tests passing, committed 7e9089e
