# Key Development Task 2 (Loop B) - 2026-04-30 00:00

## Focus: Autoresearch Methodology — Persist contentVersions to Disk

### Baseline
- 569 tests passing (after memoryMerge + searchByBranch + bulkMerge + opinion network from previous loops)

### 🎯 Target
**Persist `#contentVersions` Map to disk** so version history survives service restarts.

**Problem:** Content version snapshots were stored in an in-memory `Map`. On restart, all version history was lost — `contentHistory()` and `contentVersionDiff()` would return empty results for pre-existing memories that were updated before the restart.

**Solution:** JSON sidecar file (`content-versions.json`) in the data directory. Load on `init()`, save on content change (with dirty flag to avoid unnecessary writes).

### 🛠 Implementation

**Added to src/index.js (~25 lines):**
- `#contentVersionsDirty` flag for write coalescing
- `#contentVersionsPath()` — returns sidecar file path
- `#loadContentVersions()` — reads JSON sidecar into Map (graceful on missing file)
- `#saveContentVersions()` — writes Map to JSON only when dirty
- Hooks into `init()` (load) and content update path (mark dirty + save)

### 📊 Testing

**5 new tests:**
1. ✅ Persists versions to disk after update — sidecar file exists with correct data
2. ✅ Restores versions after restart — new service instance sees 3 versions
3. ✅ Handles missing sidecar gracefully — no crash, returns current only
4. ✅ Persists versions after contentBranch — survives across restart
5. ✅ No sidecar write when content unchanged — tag-only updates don't trigger version save

**Results:**
- 569 → 574 tests (+5, all passing)
- Zero failures
- ~25 lines added to src/index.js
- Committed: `67df45d`

### ✅ Decision: RETAIN

**Rationale:**
- Fixes real data loss bug — version history was ephemeral before this
- Minimal surface area — follows existing store patterns (load/save/dirty)
- Sidecar approach doesn't interfere with existing store files
- Graceful degradation when sidecar missing (fresh installs)

### experiments.tsv
```
2026-04-30T00:00	67df45d	test_count	574/574	keep	persist contentVersions to JSON sidecar — survive restarts. 5 new tests (569→574). Builds on k-d-2 memoryMerge.
```

### 🔮 Potential Next Steps
1. Periodic flush instead of write-on-change (reduce I/O for bulk updates)
2. `contentVersionCompact(id, keepLast)` — prune old versions to limit sidecar growth
3. Verify BM25 index persistence across restart (similar pattern to contentVersions)

---

**Generated**: 2026-04-30 00:00 AM
**Status:** ✅ Complete — contentVersions now persist to disk, 574/574 tests passing
