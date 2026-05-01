# Key Development Task 2 (Loop B) - 2026-05-01 00:00

## Focus: Autoresearch Methodology — BM25 Index Persistence to Disk

### Baseline
- 630 tests passing (after branchMerge + retryAll from previous loops)

### 🎯 Target
**Persist BM25 index to disk** so keyword search index survives service restarts.

**Problem:** BM25 index was rebuilt from all memories on every `init()`. For large stores, this is O(n) startup cost. More importantly, it was the last non-persistent index (contentVersions was already persisted in k-d-2 04-30).

**Solution:** JSON sidecar file (`bm25-index.json`) following the exact pattern of content-versions persistence.

### 🛠 Implementation

**BM25Index class additions (~20 lines):**
- `toJSON()` — serializes #docs (id→{tf, dl}), #df (term→count), #totalLen
- `static fromJSON(json)` — reconstructs BM25Index from serialized data

**MemoryService additions (~20 lines):**
- `#bm25Dirty` flag for write coalescing
- `#loadBM25Index()` — reads JSON sidecar into BM25Index (graceful on missing)
- `#saveBM25Index()` — writes index to JSON only when dirty
- Init: load sidecar first, fallback to rebuild if empty, then save
- Hooked into add(), update content path, and importAll()

### 📊 Testing

**5 new tests:**
1. ✅ Saves BM25 index to disk after adding memory — sidecar file exists with correct structure
2. ✅ Restores BM25 index after restart — new instance finds results from persisted index
3. ✅ Handles missing sidecar gracefully — no crash, search returns empty array
4. ✅ Updates BM25 sidecar on content update — re-indexed content persisted
5. ✅ Persists BM25 index after importAll — imported memories indexed in sidecar

**Results:**
- 630 → 635 tests (+5, all passing)
- Zero failures
- ~40 lines added total (20 in BM25Index, 20 in MemoryService)
- Committed: `2fd1bd1`

### ✅ Decision: RETAIN

**Rationale:**
- Completes the persistence story — all indices now survive restarts
- Follows established sidecar pattern (content-versions.json, bm25-index.json)
- Graceful fallback: missing sidecar → rebuild from store (zero data loss)
- Dirty flag avoids unnecessary I/O on tag-only updates

### experiments.tsv
```
2026-05-01T24:00	2fd1bd1	test_count	635/635	keep	BM25 index persistence to JSON sidecar. toJSON/fromJSON on BM25Index class. Load on init (fallback rebuild), save on add/update/import with dirty flag. 5 new tests (630→635). Builds on k-d-2 contentVersions pattern.
```

### 🔮 Potential Next Steps for k-d-2
1. BM25 index compaction — prune removed docs from sidecar periodically
2. Embedding cache persistence (similar sidecar pattern for embedding vectors)
3. Startup time benchmark: measure rebuild vs load for N memories

---

**Generated**: 2026-05-01 00:00 AM
**Status:** ✅ Complete — BM25 index now persists to disk, 635/635 tests passing
