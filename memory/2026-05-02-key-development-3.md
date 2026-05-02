# Key Development Task 3 (Loop C) - 2026-05-02 01:00

## Focus: Autoresearch Methodology — BM25 Sync Fixes + compactBM25Index()

### Baseline
- 635 tests passing (after BM25 index persistence from k-d-2)

### 🎯 Target
**Fix BM25 sidecar sync bugs on delete/batchDelete + add compactBM25Index() utility.**

**Problem:** After k-d-2 added BM25 index persistence, two bugs were discovered:
1. `delete()` called `#bm25.remove(id)` but never set `#bm25Dirty = true` or saved — BM25 sidecar went stale after deletes
2. `batchDelete()` didn't call `#bm25.remove()` at all — batch-deleted memories still appeared in BM25 search results
3. No utility to recover from BM25/store divergence (e.g., manual file deletions)

**Bonus:** Found and fixed pre-existing bug in `expire.test.js` using `{ dir }` instead of `{ dbPath }`, causing all instances to share `./data/memory` — masked until BM25 persistence made stale data visible across test runs.

### 🛠 Implementation

**Bug fixes (~5 lines):**
- `delete()`: add `this.#bm25Dirty = true` + `await this.#saveBM25Index()` after remove
- `batchDelete()`: add `this.#bm25.remove(id)` in loop + dirty flag + save after

**New API (~20 lines):**
- `compactBM25Index(opts)`: compare BM25 doc IDs against live store, remove orphans
- `dryRun` option returns count without modifying
- `BM25Index.docIds()`: expose indexed IDs for compaction

**Test fix (1 line):**
- `expire.test.js`: `{ dir }` → `{ dbPath }`

### 📊 Testing

**5 new tests (bm25-sync.test.js):**
1. ✅ delete() persists BM25 index to sidecar
2. ✅ batchDelete() removes from BM25 index
3. ✅ compactBM25Index() removes stale entries
4. ✅ compactBM25Index() dryRun does not modify index
5. ✅ compactBM25Index() cleans orphan after manual store manipulation

**Results:**
- 635 → 640 tests (+5, all passing)
- 640/640 total, zero failures (including previously-failing expire tests now fixed)
- Committed: `ecc4c16`

### ✅ Decision: RETAIN

**Rationale:**
- Fixes real data correctness bugs introduced by k-d-2's BM25 persistence
- `compactBM25Index()` provides recovery mechanism for edge cases
- Pre-existing expire test bug fix is a bonus — better test isolation
- Minimal code change, high impact on correctness

### experiments.tsv
```
2026-05-02T01:00	ecc4c16	test_count	640/640	keep	BM25 sync fixes + compactBM25Index. delete() now saves BM25 sidecar. batchDelete() now removes from BM25. compactBM25Index() prunes orphans with dryRun. BM25Index.docIds(). Fix expire.test.js dbPath bug. 5 new tests (635→640). Builds on k-d-2 BM25 persistence.
```

### 🔮 Potential Next Steps
1. Embedding cache sync — similar dirty-tracking on delete/batchDelete
2. `autoMaintain()` v2 — include compactBM25Index in periodic maintenance
3. Startup time benchmark: measure sidecar load vs full rebuild for N memories

---

**Generated**: 2026-05-02 01:00 AM
**Status:** ✅ Complete — BM25 sync bugs fixed, compactBM25Index() added, 640/640 tests passing
