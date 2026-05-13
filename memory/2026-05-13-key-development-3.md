# Key Development Task 3 (Loop C) - 2026-05-13 01:00

## Focus: Autoresearch Methodology — `plan_batch()` on Orchestrator

### Baseline
- 278 tests passing (after checkpoint/resume from 05-12)

### 🎯 Target
**Add dry-run batch planning capability.**

**Problem:** `run_batch()` commits to executing stories immediately — no way to preview what will run, in what order, or whether the budget is sufficient. Users must guess or manually inspect the PRD.

**Solution:** `plan_batch(max_iterations, max_consecutive_failures)` — simulates story selection order without executing iterations. Returns planned stories with step/title/priority, remaining count, and `would_complete_all` flag.

### 🛠 Implementation
- ~40 lines on `RalphOrchestrator`
- Returns structured dict: `planned_stories`, `total_planned`, `remaining_after_plan`, `would_complete_all`, `budget`, `failure_threshold`
- Raises `ValueError` if no active session (consistent with other methods)
- Excludes already-completed stories from plan

### 📊 Results
- 278 → 285 tests (+7, all passing)
- Zero regressions
- Committed: `214e16b`

### ✅ Decision: RETAIN

**Rationale:**
- Natural companion to `run_batch` + checkpoint/resume — plan → execute → checkpoint → resume
- Zero dependencies, pure computation
- Tests cover: budget limits, completion check, story order, field presence, no-session guard, completed exclusion, metadata reflection

### experiments.tsv
```
2026-05-13T01:00	214e16b	test_count	285/285	keep	plan_batch(): dry-run batch planning with story preview and completion estimate. +7 tests (278→285).
```

---

**Generated**: 2026-05-13 01:00 AM
**Status:** ✅ Complete — 285/285 tests passing, committed 214e16b
