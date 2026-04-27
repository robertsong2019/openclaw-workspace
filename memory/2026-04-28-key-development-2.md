# Key Development Task 2 (Loop B) - 2026-04-28 00:00

## Focus: Autoresearch Methodology — Experiment Loop B (Build on k-d-2/3 from 2026-04-27)

### Baseline
- 481 tests passing (after bulkReclassify + Hindsight Phase 1)
- Full pipeline including temporal search, content versioning/rollback, fact classification, entity search, cluster merge

### 🎯 Target
Add **`searchByContent(pattern, opts)`** — regex/substring content search across memories.

**Problem:** Existing `search()` is BM25 text search (good for relevance ranking), but there's no way to do exact pattern matching, regex search, or substring matching on memory content. Need pattern-based search for validation, deduplication, and structured queries.

**Solution:** `searchByContent` accepts a pattern string with regex/substring mode, layer/tag filtering, case sensitivity toggle, and pagination. Returns matched results with the actual matched substring for verification.

### 🛠 Implementation

**Added to src/index.js (~30 lines):**
- `searchByContent(pattern, opts)`: regex or escaped-substring matching on memory content
- Options: `regex` (bool), `layer`, `tags` (OR match), `caseSensitive` (bool), `limit`/`offset` pagination
- Returns `{ total, offset, limit, pattern, results: [{id, content, layer, tags, match}] }`
- Invalid regex returns empty results gracefully (no crash)

### 📊 Testing

**10 new tests:**
1. ✅ Returns matching memories with correct metadata
2. ✅ Filters by layer
3. ✅ Filters by tags (OR match)
4. ✅ Supports regex mode
5. ✅ Supports case-sensitive mode
6. ✅ Paginates with offset and limit
7. ✅ Returns empty for no matches
8. ✅ Handles invalid regex gracefully
9. ✅ Match field contains actual matched substring
10. ✅ Substring mode escapes special regex chars ($50.00)

**Results:**
- 481 → 491 tests (+10, all passing)
- Zero failures (0/0, pre-existing flaky expire test also passed this run)
- ~30 lines added to src/index.js
- Committed: `9ec9af3`

### ✅ Decision: RETAIN

**Rationale:**
- Closes the pattern search gap — BM25 is relevance, this is precision
- Complements existing search APIs: BM25 (`search`), entity (`searchByEntity`), temporal (`searchByTimeRange`), fact (`searchByFactType`), tag (`tagSearch`) → now content pattern
- Substring auto-escaping makes it safe for non-regex users
- Invalid regex is graceful, not crashy

### experiments.tsv
```
2026-04-28T00:00	9ec9af3	test_count	491/491	keep	searchByContent(pattern, opts) — regex/substring content search. Layer/tag filter, caseSensitive, pagination, invalid regex handling. 10 new tests (481→491), ~30 lines src. Builds on k-d-2 searchByTimeRange + k-d-3 contentRollback.
```

### 🔮 Potential Next Steps
1. `memoryMerge(id1, id2, opts)` — merge two memories with conflict resolution (content strategy, tag union, link rewiring)
2. Persist contentVersions to disk (JSON sidecar) — survive restarts
3. `autoTag` v2 with embedding-based similarity
4. `contentBranch(id, content)` — create a branch from current version

---

**Generated**: 2026-04-28 00:00 AM
**Status:** ✅ Complete — searchByContent() API added, 10 new tests, 491/491 passing
