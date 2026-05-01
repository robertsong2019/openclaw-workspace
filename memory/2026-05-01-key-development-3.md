# Key Development Task 3 (Loop C) - 2026-05-01 01:00

## Focus: Autoresearch Methodology — branchDiff(id) on k-d-2/k-d-3 foundation

### Baseline
- 612 tests passing (after contentVersions persistence, autoMerge, safeMerge, mergePreview, opinion network, file_info hash from previous loops)

### 🎯 Target
**Add `branchDiff(id)`** — compare a branch memory back to its source, showing content similarity, tag/entity deltas.

**Problem:** `contentBranch()` creates branches with bidirectional links, but there was no way to diff a branch against its source to see what changed (content divergence, tag/entity additions/removals). This is essential for reviewing how branches have evolved.

**Solution:** `branchDiff(id)` finds the source via the `derived_from` link, then computes:
- Content: ngram similarity, lengths, identical/modified status
- Tags: added, removed, common
- Entities: added, removed, common

### 🛠 Implementation

**Added to src/index.js (~40 lines):**
- `branchDiff(id)`: source lookup via `getLinks` + `derived_from` filter
- Per-field delta computation with Set operations
- Returns structured diff with branch/source metadata

**New test file:** `tests/branchDiff.test.js` (8 tests)

### 📊 Testing

**8 new tests:**
1. ✅ Returns null for non-existent memory
2. ✅ Returns null for memory with no branch link
3. ✅ Compares branch to source with identical content
4. ✅ Detects content modification after branch
5. ✅ Detects tag changes (added/removed/common)
6. ✅ Detects entity changes
7. ✅ Returns source and branch metadata
8. ✅ Works with chained branches (b2→b1 diff)

**Results:**
- 612 → 620 tests (+8, all passing)
- Zero failures
- Committed: `5984206`

### ✅ Decision: RETAIN

**Rationale:**
- Completes the branch story: `contentBranch()` creates, `branchDiff()` inspects
- Zero dependencies on new code — uses existing `getLinks`, `ngramSimilarity`, `contentHash`
- Essential for branch review workflows before merging
- Works with chained branches (branch of branch)

### experiments.tsv
```
2026-05-01T01:00	5984206	test_count	620/620	keep	branchDiff(id) — compare branch to source: content similarity + tag/entity deltas. 8 new tests (612→620). Uses getLinks+derived_from for source lookup.
```

### 🔮 Potential Next Steps
1. `branchDiff` with word-level diff (not just identical/modified)
2. `branchMerge(id)` — merge branch changes back into source
3. `timeline()` v2 with branch visualization
4. Embedding similarity as alternative to ngram in branchDiff

---

**Generated**: 2026-05-01 01:00 AM
**Status:** ✅ Complete — branchDiff() API added, 8 new tests, 620/620 passing
