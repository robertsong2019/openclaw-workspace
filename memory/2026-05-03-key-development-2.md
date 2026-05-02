# Key Development Task 2 (Loop B) - 2026-05-03 00:00

## Focus: Autoresearch Methodology — Embedding Cache Sync on Delete + compactEmbedCache()

### Baseline
- 640 tests passing (after BM25 sync fixes + compactBM25Index from k-d-3)

### 🎯 Target
**Fix embedding cache sync bugs on delete/batchDelete + add compactEmbedCache() utility.**

**Problem:** After k-d-2 added BM25 index persistence and k-d-3 fixed BM25 sync on delete, the same bug pattern existed for embedding cache:
1. `delete()` didn't remove the deleted memory's embedding from cache — orphaned vectors stayed in `embed-cache.json`
2. `batchDelete()` didn't remove embeddings either — batch-deleted memories still had cached vectors
3. No utility to recover from cache/store divergence (similar to `compactBM25Index()`)

**Same pattern as k-d-3 BM25 fix, applied to embeddings.**

### 🛠 Implementation

**EmbeddingProvider new methods (~15 lines):**
- `removeByContent(text)` — removes cached embedding by content hash
- `removeByKey(key)` — removes by hash key directly
- `cacheKeys()` — expose all cache keys for compaction

**MemoryService delete/batchDelete (~4 lines):**
- `delete()`: add `this.#embeddings.removeByContent(m.content)` + `await this.#embeddings.saveCache()`
- `batchDelete()`: add same cleanup in loop + save after

**New API (~20 lines):**
- `compactEmbedCache(opts)`: compare cache keys against live memory content hashes, remove orphans
- `dryRun` option returns count without modifying

### 📊 Testing

**5 new tests (embed-sync.test.js):**
1. ✅ delete() removes embedding from cache and persists
2. ✅ batchDelete() removes embeddings from cache
3. ✅ compactEmbedCache() removes orphan entries injected into file
4. ✅ compactEmbedCache() dryRun does not modify cache
5. ✅ compactEmbedCache() cleans orphan after external manipulation

**Results:**
- 640 → 645 tests (+5, all passing)
- Zero failures
- Committed: `a39d989`

### ✅ Decision: RETAIN

**Rationale:**
- Mirrors the BM25 sync fix pattern from k-d-3 — consistent approach across all cache types
- Fixes real resource leak — orphaned embedding vectors accumulate indefinitely
- `compactEmbedCache()` provides recovery for edge cases
- Discovered that `add()` returns the full memory object, not just the id — useful for future tests
- ~40 lines added total (15 in EmbeddingProvider, 4 in delete paths, 20 in compactEmbedCache)

### experiments.tsv
```
2026-05-03T00:00	a39d989	test_count	645/645	keep	Embed cache sync on delete/batchDelete + compactEmbedCache(). removeByContent/removeByKey/cacheKeys on EmbeddingProvider. compactEmbedCache(opts) with dryRun. Mirrors BM25 fix pattern from k-d-3. 5 new tests (640→645). Builds on k-d-2 BM25 persistence.
```

### 🔮 Potential Next Steps for k-d-2
1. Unified `autoMaintain()` — include compactEmbedCache + compactBM25Index in periodic maintenance
2. Embedding cache size limit — evict old entries when cache exceeds threshold
3. Startup time benchmark: measure sidecar load vs full rebuild for N memories

---

**Generated**: 2026-05-03 00:00 AM
**Status:** ✅ Complete — Embed cache sync fixed, compactEmbedCache() added, 645/645 tests passing
