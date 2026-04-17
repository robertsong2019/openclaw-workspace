# Key Development Task 2 (Loop B) - 2026-04-18 00:00

## Focus: Autoresearch Methodology — Experiment Loop B

### Baseline
- v0.9.5, 184 tests, LLM extraction + various APIs

### 🎯 Target
Add `query()` — a unified filter API so agents don't need to chain multiple specific methods.

### 🛠 Implementation
**`MemoryService.query(opts)`** — single method supporting:
- `tags[]` + `tagsOp` (and/or)
- `entities[]` + `entitiesOp` (and/or)  
- `layer`, `minWeight`, `maxWeight`
- `since`, `until` (time range)
- `text` (case-insensitive substring)
- `sort` (weight/created/updated) + `sortDir` (asc/desc)
- `limit` + `offset` (pagination)
- Returns `{ results, total }` (total = unpaginated count)

~55 lines added to src.

### 📊 Results
- **195/195 tests pass** (184 → +11)
- 11 new tests covering all filter combinations
- Zero regressions

### ✅ Decision: RETAIN
- Solves real agent ergonomics gap
- Backward compatible, no changes to existing APIs
- Replaces need for agents to call search/tag/entity methods separately

### experiments.tsv
```
2026-04-18T00:00	key-dev-2b	test_count	195/195	keep	v0.9.6: query() unified filter API. 11 new tests (184→195).
```
