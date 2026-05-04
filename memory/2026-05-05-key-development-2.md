# Key Development Task 2 (Loop B) - 2026-05-05 00:00

## Focus: Autoresearch Methodology — Embedding Cache Size Limit with LRU Eviction

### Baseline
- 36 embed-related tests passing (embed-sync, embedding, embed-openai)
- EmbeddingProvider had no size limit — cache grows unbounded with use
- Previous k-d-2 loops: embed cache sync on delete (05-03), autoMaintain integration (05-04)

### 🎯 Target
**Add maxCacheSize option to EmbeddingProvider with LRU-style eviction to prevent unbounded cache growth.**

**Problem:** The embedding cache (`embed-cache.json`) grows indefinitely. Long-running agents accumulate thousands of cached vectors with no mechanism to bound memory or disk usage. Previous loops fixed sync bugs and added compaction, but didn't address the root cause: no size limit.

**Solution:** Insertion-order eviction using Map's natural iteration order (oldest-first). When cache exceeds maxCacheSize after a new `embed()`, the oldest entries are removed.

### 🛠 Implementation

**EmbeddingProvider constructor (~3 lines):**
- New `opts.maxCacheSize` parameter (default 0 = unlimited)
- Private `#maxCacheSize` field

**New methods (~15 lines):**
- `#evictIfNeeded()` — removes oldest entries when `cache.size > maxCacheSize`
- `get maxCacheSize` — accessor
- `setMaxCacheSize(n)` — runtime adjustment

**EmbeddingProvider.embed() (1 line):**
- Call `this.#evictIfNeeded()` after setting new cache entry

**MemoryService constructor (1 line):**
- Pass `options.maxCacheSize` through to EmbeddingProvider

### 📊 Testing

**5 new tests (embedCacheEviction.test.js):**
1. ✅ Evicts oldest entries when cache exceeds maxCacheSize (3 limit, add 4 → size stays 3)
2. ✅ maxCacheSize=0 means unlimited (10 embeds → 10 cached)
3. ✅ setMaxCacheSize changes limit at runtime (shrink triggers eviction on next embed)
4. ✅ Evicted entry can be re-embedded (cache miss produces correct vector)
5. ✅ Persisted cache after eviction respects size on reload

**Results:**
- 36 → 41 embed tests (all passing)
- Zero failures in existing tests
- Committed: `846418b`

### ✅ Decision: RETAIN

**Rationale:**
- Prevents the exact problem compactEmbedCache was designed to recover from — now it can't happen if maxCacheSize is set
- LRU via Map insertion order is zero-cost (no separate timestamp tracking)
- Opt-in: default 0 means unlimited, backward compatible
- ~20 lines of implementation, clean and focused
- Closes the cache management loop: eviction (prevention) + compaction (recovery) + autoMaintain (automation)

### experiments.tsv
```
2026-05-05T00:00	846418b	test_count	41/41	keep	Embedding cache size limit with LRU eviction. EmbeddingProvider opts.maxCacheSize (0=unlimited). #evictIfNeeded() removes oldest entries. setMaxCacheSize(n) runtime. 5 new tests (36→41 embed tests). Builds on k-d-2 embed cache sync from 05-03, autoMaintain from 05-04.
```

### 🔮 Potential Next Steps for k-d-2
1. TTL-based cache eviction — evict entries older than N days (time-based LRU)
2. autoMaintain integration — compactEmbedCache could also trim to maxCacheSize if set
3. Startup time benchmark: measure sidecar load vs full rebuild for N memories
4. Cache warming: pre-embed recent memories on init

---

**Generated**: 2026-05-05 00:00 AM
**Status:** ✅ Complete — Embedding cache LRU eviction implemented, 41/41 tests passing, committed 846418b
