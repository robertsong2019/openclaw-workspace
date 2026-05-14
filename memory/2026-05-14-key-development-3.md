# Key Development Task 3 (Loop C) - 2026-05-14 01:00

## Focus: Autoresearch Methodology — `validate_dependencies()` on Orchestrator

### Baseline
- 285 tests passing (after plan_batch from 05-13)

### 🎯 Target
**Add dependency graph validation — detect circular, missing, and self-referencing dependencies.**

**Problem:** Stories declare `dependencies: []` but no one validates them. Circular deps cause infinite loops in `get_next_story`. Missing deps silently block stories forever. Self-deps are logical impossibilities.

**Solution:** `validate_dependencies()` — DFS-based cycle detection + missing/self-dep scanning. Returns structured report: `valid`, `circular_deps`, `missing_deps`, `self_deps`, `total_stories_checked`.

### 🛠 Implementation
- ~45 lines on `RalphOrchestrator`
- DFS traversal tracking `in_stack` for cycle extraction
- Three independent checks: circular (DFS), missing (set diff), self (id match)
- No external dependencies, pure computation

### 📊 Results
- 285 → 292 tests (+7, all passing)
- Zero regressions
- Committed: `cbd7772`

### ✅ Decision: RETAIN

**Rationale:**
- Pre-flight safety check before `run_batch()` — catch broken PRDs early
- Complements `plan_batch()` (planning) with validation (correctness)
- Tests cover: clean graph, valid chain, missing dep, self-dep, 2-node cycle, 3-node cycle, mixed issues

### experiments.tsv
```
2026-05-14T01:00	cbd7772	test_count	292/292	keep	validate_dependencies(): circular/missing/self-dep detection via DFS. +7 tests (285→292).
```

---

**Generated**: 2026-05-14 01:00 AM
**Status:** ✅ Complete — 292/292 tests passing, committed cbd7772
