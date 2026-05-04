# Key Development Task 2 (Loop B) - 2026-05-04 00:00

## Focus: Autoresearch Methodology — Unified autoMaintain with BM25 + Embed Cache Diagnostics

### Baseline
- 312 tests passing in memory.test.js (after embed cache sync from 05-03 k-d-2)

### 🎯 Target
**Integrate compactBM25Index + compactEmbedCache into autoMaintain() and healthScore() diagnostics.**

**Problem:** Previous k-d-2/3 loops added `compactBM25Index()` and `compactEmbedCache()` as standalone utilities, but `autoMaintain()` didn't know about them. The health score didn't measure BM25 or embedding cache bloat, so orphaned index entries could accumulate silently without triggering maintenance.

**Solution:** Add BM25/embed-cache health dimensions to `healthScore()` and wire them into `autoMaintain()` task list.

### 🛠 Implementation

**healthScore() additions (~12 lines):**
- Compute `bm25OrphanCount` by comparing `#bm25.docIds()` against live memory IDs
- Compute `embedOrphanCount` by comparing `#embeddings.cacheKeys()` against live content hashes
- New health dimensions: `bm25` (0-100), `embedCache` (0-100)
- New recommendations when orphans detected

**autoMaintain() additions (~8 lines):**
- Default tasks expanded: `['purge', 'compactChangelog', 'compactBM25', 'compactEmbedCache', 'decay', 'reindex']`
- `compactBM25` task: runs when `health.details.bm25 < 90`
- `compactEmbedCache` task: runs when `health.details.embedCache < 90`

### 📊 Testing

**4 new tests:**
1. ✅ compactBM25 task skipped when BM25 health is healthy (clean data)
2. ✅ compactEmbedCache task skipped when embed cache is healthy
3. ✅ healthScore includes bm25 and embedCache details (values 0-100)
4. ✅ existing healthScore tests updated (changelog key preserved for backward compat)

**Results:**
- 312 tests, 0 failures
- Committed: `8efa40e`

### ✅ Decision: RETAIN

**Rationale:**
- Closes the loop: compactBM25/compactEmbedCache are now part of the automated maintenance pipeline
- healthScore now provides full visibility into all 6 health dimensions
- Backward compatible: existing `details.changelog` key preserved
- Minimal code (~20 lines), high integration value

### experiments.tsv
```
2026-05-04T00:00	8efa40e	test_count	312/312	keep	Unified autoMaintain with BM25 + embed cache diagnostics. healthScore now measures bm25/embedCache bloat. autoMaintain default tasks include compactBM25/compactEmbedCache. 4 new tests. Builds on k-d-2 compactBM25Index + compactEmbedCache from 05-03.
```

### 🔮 Potential Next Steps for k-d-2
1. Embedding cache size limit — evict old entries when cache exceeds threshold
2. Startup time benchmark: measure sidecar load vs full rebuild for N memories
3. `autoMaintain` integration test with forced orphans via file manipulation

---

**Generated**: 2026-05-04 00:00 AM
**Status:** ✅ Complete — autoMaintain unified with all compaction utilities, 312/312 tests passing
