# Key Development Task 3 (Loop C) - 2026-04-29 01:00

## Focus: Autoresearch Methodology — Experiment Loop C (Build on k-d-2/3)

### Baseline
- 529 tests passing (after searchByContent + contentBranch + contentRollback + searchGraph + searchTemporal + memoryMerge from previous loops)

### 🎯 Target
Add **`searchByBranch(id, opts)`** + **`bulkMerge(pairs, opts)`** — branch discovery and batch merge primitives.

**Problem:** 
1. After creating branches via `contentBranch()`, there was no way to query "what branches exist for this memory?" — the branching system lacked a traversal/query primitive.
2. After detecting duplicates via `findDuplicatePairs()`, merging them one-by-one was tedious — no batch operation existed.

**Solution:**
- `searchByBranch(id, opts)`: BFS traversal via `derived_from` links from a root memory. Supports `depth` limit and `includeSelf`. Returns branches with depth and link info.
- `bulkMerge(pairs, opts)`: Sequential merge of multiple [primary, secondary] pairs with error handling. Skips already-deleted memories, reports per-pair errors.

### 🛠 Implementation

**Added to src/index.js (~45 lines):**

`searchByBranch(id, opts)`:
- BFS via outgoing `derived_from` links from root
- `depth` option limits traversal depth
- `includeSelf` includes root memory at depth 0
- Returns `{ branches: [{ memory, depth, link }] }`

`bulkMerge(pairs, opts)`:
- Iterates pairs sequentially, calling `memoryMerge` for each
- Handles already-deleted memories gracefully (skip + report)
- Passes opts through to each merge call
- Returns `{ results, errors, merged, failed }`

### 📊 Testing

**11 new tests (6 searchByBranch + 5 bulkMerge):**

searchByBranch:
1. ✅ Returns empty for non-existent root
2. ✅ Returns empty when root has no branches
3. ✅ Finds direct branches (2 branches from 1 root)
4. ✅ Finds nested branches (branch of branch)
5. ✅ Respects depth limit
6. ✅ Includes self with includeSelf option

bulkMerge:
1. ✅ Merges multiple pairs in sequence
2. ✅ Reports errors for already-merged memories
3. ✅ Passes options through to memoryMerge
4. ✅ Handles empty pairs array
5. ✅ Handles all invalid pairs gracefully

**Results:**
- 529 → 540 tests (+11, all passing)
- Zero failures
- ~45 lines added to src/index.js
- Committed: `d83326b`

### ✅ Decision: RETAIN

**Rationale:**
- `searchByBranch` completes the branching API triad: `contentBranch` (create) → `searchByBranch` (query) → `memoryMerge` (consolidate)
- `bulkMerge` completes the deduplication pipeline: `findDuplicatePairs` → `bulkMerge` (batch version)
- Both are thin wrappers over existing primitives — minimal surface area, maximum composability
- Error handling in bulkMerge makes it safe for automated deduplication workflows

### experiments.tsv
```
2026-04-29T01:00	d83326b	test_count	540/540	keep	searchByBranch(id,opts) + bulkMerge(pairs,opts). 11 new tests (529→540). ~45 lines src. Builds on k-d-2 memoryMerge + k-d-3 contentBranch.
```

### 🔮 Potential Next Steps
1. Persist contentVersions to disk (JSON sidecar) — survive restarts
2. `autoTag` v2 with embedding-based similarity
3. `mergeSuggestions(opts)` — auto-detect merge candidates using embedding similarity + shared entities
4. `branchDiff(id)` — diff between a branch and its source at branch time
5. `timeline()` v2 with branch visualization

---

**Generated**: 2026-04-29 01:00 AM
**Status:** ✅ Complete — searchByBranch() + bulkMerge() added, 11 new tests, 540/540 passing
