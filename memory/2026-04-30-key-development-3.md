# Key Development Task 3 (Loop C) - 2026-04-30 01:00

## Focus: Autoresearch Methodology — Experiment Loop C (Build on k-d-2/3)

### Baseline
- 574 tests passing (after contentVersions persistence, opinion network, searchByBranch, bulkMerge from previous loops)

### 🎯 Target
Add **`mergeSuggestions(opts)`** — auto-detect merge candidates using multi-signal scoring (content similarity + shared entities + shared tags).

**Problem:** The deduplication pipeline (`findDuplicatePairs` → `compareMemories` → `memoryMerge` → `bulkMerge`) lacked an intelligent candidate suggestion system. `findDuplicatePairs` only uses ngram similarity, missing memories that are semantically related via shared entities or tags but have different wording.

**Solution:** `mergeSuggestions(opts)` uses a weighted 3-signal scoring system:
- Content ngram similarity (weight: 0.5)
- Shared entity overlap (weight: 0.3)  
- Shared tag overlap (weight: 0.2)

Returns candidates sorted by composite score with explainability (reasons array) and suggested merge strategy.

### 🛠 Implementation

**Added to src/index.js (~55 lines):**
- `mergeSuggestions(opts)`: multi-signal merge candidate detection
- `minScore` (default 0.5), `limit` (default 20), `layer` filter
- Per-pair reasons array: `content:86%`, `entities:2`, `tags:1`
- `suggestedStrategy`: recommends `keep-longer` vs `concat` based on content length, always `union` for tags

### 📊 Testing

**9 new tests:**
1. ✅ Returns empty when no memories
2. ✅ Detects duplicate-like memories by content similarity
3. ✅ Considers shared entities in scoring
4. ✅ Considers shared tags in scoring
5. ✅ Respects minScore filter
6. ✅ Respects limit option
7. ✅ Respects layer filter
8. ✅ Suggests keep-longer when first is longer
9. ✅ Returns results sorted by score descending

**Results:**
- 574 → 583 tests (+9, all passing)
- Zero failures
- ~55 lines added to src/index.js
- Committed: `0414852`

### ✅ Decision: RETAIN

**Rationale:**
- Completes the dedup pipeline with intelligent candidate discovery: `mergeSuggestions` → `bulkMerge`
- Multi-signal scoring catches related memories that pure text similarity misses
- Explainability (reasons array) makes suggestions auditable
- Suggested strategies reduce decision burden in automated workflows
- Minimal surface area — thin wrapper over existing similarity + index primitives

### experiments.tsv
```
2026-04-30T01:00	0414852	test_count	583/583	keep	mergeSuggestions(opts) — auto-detect merge candidates via content similarity + shared entities/tags. 3-signal scoring (ngram 50%, entities 30%, tags 20%). Suggested strategy, layer filter, limit, minScore. 9 new tests (574→583).
```

### 🔮 Potential Next Steps
1. `mergeSuggestions` v2 with embedding similarity as 4th signal
2. `autoMerge(opts)` — end-to-end: mergeSuggestions → user confirmation → bulkMerge
3. `branchDiff(id)` — diff between a branch and its source at branch time
4. `timeline()` v2 with branch visualization

---

**Generated**: 2026-04-30 01:00 AM
**Status:** ✅ Complete — mergeSuggestions() API added, 9 new tests, 583/583 passing
