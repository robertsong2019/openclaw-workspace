# Key Development Task 3 (Loop C) - 2026-04-26 01:00

## Focus: Autoresearch Methodology — Experiment Loop C (Build on key-development-2)

### Baseline
- 438 tests passing (after clusterAutoMerge from key-development-2)
- Full pipeline: clusterByTopic → summarizeCluster → mergeClusters → autoTag → clusterHealth → clusterAutoMerge → searchByEntity

### 🎯 Target
Add **`contentHistory(id)`** + **`contentVersionDiff(id, opts)`** — content versioning for individual memories.

**Problem:** `memoryDiff` compares two *different* memories, but there's no way to track how a single memory's content evolved over time. When content is updated via `update()`, the previous version is lost.

**Solution:** Store content snapshots in `#contentVersions` map on every update where content actually changes. `contentHistory(id)` returns all versions (oldest→current). `contentVersionDiff(id, opts)` computes n-gram similarity between any two versions.

### 🛠 Implementation

**Added to src/index.js (~30 lines):**
- `#contentVersions` Map field for in-memory version tracking
- On `update()`: if content changed, push `{content, hash, ts}` to version array
- `contentHistory(id)`: returns `{id, found, versions: [{content, hash, ts, current}]}` (oldest→newest, last=current)
- `contentVersionDiff(id, {from?, to?})`: picks two version indices, returns `{from, to, similarity}` via ngramSimilarity

**Key design decisions:**
- Only snapshots when content *actually* changes (skips no-op updates)
- `contentVersionDiff` defaults: from=first, to=last(current)
- In-memory only (versions lost on restart — acceptable for v1)

### 📊 Testing

**7 new tests:**
1. ✅ Returns single version for memory with no updates
2. ✅ Tracks content versions across multiple updates (v1→v2→v3)
3. ✅ Does not snapshot when content unchanged
4. ✅ Returns found:false for non-existent memory
5. ✅ Diffs two versions with similarity score
6. ✅ Diffs specific version indices (from:1, to:2)
7. ✅ Returns similarity 1 for identical content (single version)

**Results:**
- 438 → 445 tests (+7, all passing)
- Zero regressions
- ~30 lines added to src/index.js
- Committed: `d674486`

### ✅ Decision: RETAIN

**Rationale:**
- Closes the versioning gap — now you can audit how any memory evolved
- Complements existing `memoryDiff` (cross-memory) with intra-memory diffing
- Zero overhead when not used (no version stored if no updates)
- Clean API, minimal footprint

### experiments.tsv
```
2026-04-26T01:00	d674486	test_count	445/445	keep	contentHistory(id) + contentVersionDiff(id, opts) — content versioning on update. 7 new tests (438→445), ~30 lines src.
```

### 🔮 Potential Next Steps
1. Persist contentVersions to disk (JSON sidecar)
2. `searchByTimeRange(opts)` — temporal search across memories
3. `autoTag` v2 with embedding-based similarity for better tag suggestions
4. `contentRollback(id, versionIndex)` — restore a previous content version

---

**Generated**: 2026-04-26 01:00 AM
**Status:** ✅ Complete — contentHistory() + contentVersionDiff() added, 7 new tests, 445/445 passing
