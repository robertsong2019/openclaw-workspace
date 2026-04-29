# Key Development Task 2 (Loop B) - 2026-04-29 00:00

## Focus: Autoresearch Methodology — Experiment Loop B (Build on 2026-04-28 results)

### Baseline
- 519 tests passing (after searchByContent + contentBranch + searchGraph + searchTemporal from previous loops)
- Full pipeline including pattern search, content branching, graph traversal, temporal search

### 🎯 Target
Add **`memoryMerge(id1, id2, opts)`** — merge two memories with configurable conflict resolution.

**Problem:** No way to merge duplicate or related memories. When memories are identified as duplicates (via `findDuplicatePairs`) or when clusters are consolidated, there's no primitive to merge two memories while handling conflicts in content, tags, entities, and links.

**Solution:** `memoryMerge` accepts primary + secondary memory IDs with strategies for content (`concat`/`keep-longer`/`keep-newer`/`manual`), tags (`union`/`primary`/`secondary`), and links (`rewire`/`drop`). Entities always union. Deletes secondary after merging.

### 🛠 Implementation

**Added to src/index.js (~60 lines):**
- `memoryMerge(id1, id2, opts)`: validates both memories exist and differ
- Content strategies: concat (default), keep-longer, keep-newer, manual override
- Tag strategies: union (default), primary-only, secondary-only
- Entity strategy: always union (deduped)
- Link strategy: rewire (migrate secondary's links to primary) or drop
- Skips self-links and duplicate links during rewiring
- Deletes secondary from store + BM25 index after merge

### 📊 Testing

**10 new tests:**
1. ✅ Merges with concat strategy (default) — content joined, tags unioned, secondary deleted
2. ✅ Supports keep-longer content strategy
3. ✅ Supports keep-newer content strategy
4. ✅ Supports manual content strategy
5. ✅ Merges entities as union (deduped)
6. ✅ Supports tag strategy: primary only
7. ✅ Rewires links from secondary to primary by default
8. ✅ Drops links with drop strategy
9. ✅ Returns null for non-existent memories
10. ✅ Returns null when merging same memory

**Results:**
- 519 → 529 tests (+10, all passing)
- Zero failures
- ~60 lines added to src/index.js
- Committed: `19d763d`

### ✅ Decision: RETAIN

**Rationale:**
- Completes the deduplication pipeline: `findDuplicatePairs` → `compareMemories` → `memoryMerge`
- Content strategies cover the main use cases (concat for complementary info, keep-longer for verbose, keep-newer for freshness, manual for full control)
- Link rewiring preserves graph connectivity when memories merge
- Complements existing APIs: `clusterMerge` (topic-level) now has `memoryMerge` (item-level)
- Minimal surface area — all strategies are optional with sensible defaults

### experiments.tsv
```
2026-04-29T00:00	19d763d	test_count	529/529	keep	memoryMerge(id1, id2, opts) — merge two memories with conflict resolution. Content strategies (concat/keep-longer/keep-newer/manual), tag strategies (union/primary/secondary), entity union, link rewiring/dropping. 10 new tests (519→529).
```

### 🔮 Potential Next Steps
1. `memoryMerge` v2 with embedding similarity scoring for auto-detecting merge candidates
2. Persist contentVersions to disk (JSON sidecar) — survive restarts
3. `searchByBranch(id)` — find all branches of a memory via derived_from links
4. Batch merge: `bulkMerge(pairs, opts)` — merge multiple duplicate pairs in one call

---

**Generated**: 2026-04-29 00:00 AM
**Status:** ✅ Complete — memoryMerge() API added, 10 new tests, 529/529 passing
