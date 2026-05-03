# Key Development Task 3 (Loop C) - 2026-05-03 01:00

## Focus: Autoresearch Methodology — PRD Priority Auto-Adjust + Story Splitting Tests

### Baseline
- 103 tests passing (better-ralph-core)

### 🎯 Target
**Add test coverage for 3 untested PRDManager methods: `auto_adjust_priorities()`, `split_large_story()`, `_calculate_dependency_depth()`.**

**Problem:** Three important PRD management methods had zero test coverage:
1. `auto_adjust_priorities()` — reorders incomplete stories based on dependency depth
2. `split_large_story()` — breaks oversized stories into smaller parts
3. `_calculate_dependency_depth()` — recursive depth calculation with circular dependency protection

**Bonus:** Fixed broken import chain by adding missing stubs for `agent_registry` and `version_control` modules referenced by orchestrator.

### 🛠 Implementation

**14 new tests (test_prd_priority_and_split.py):**

TestAutoAdjustPriorities (5):
- Empty PRD no error
- Completed stories unchanged
- Incomplete stories get priority based on dependency depth
- Circular dependency handled (no infinite recursion)
- Max depth capped at 5

TestSplitLargeStory (5):
- Nonexistent story returns empty
- Creates correct number of parts
- Criteria evenly distributed
- Dependencies preserved across parts
- Estimated hours divided among parts

TestCalculateDependencyDepth (4):
- No dependencies → depth 0
- Single chain depth calculation
- Diamond dependency (max path)
- Missing node in graph

**Stub modules (2 files):**
- `core/agent_registry.py` — Agent + AgentRegistry stubs
- `plugins/version_control.py` — VersionControl stub

### 📊 Testing

**Results:**
- 103 → 117 tests (+14, all passing)
- Committed: `dca3f7e`

### ✅ Decision: RETAIN

**Rationale:**
- Covers 3 previously-untested public methods
- Found and fixed import chain breakage (orchestrator can't be imported without stubs)
- Tests validate real behavior: dependency-based prioritization, story splitting semantics
- Minimal code, high coverage impact

### experiments.tsv
```
2026-05-03T01:00	dca3f7e	test_count	117/117	keep	PRD priority auto-adjust + split_large_story + dependency depth tests. 14 new tests (103→117). Fixed missing agent_registry + version_control stubs. AutoAdjustPriorities, SplitLargeStory, CalculateDependencyDepth coverage.
```

### 🔮 Potential Next Steps
1. `auto_adjust_priorities` edge case: stories with dependencies on completed stories
2. `get_progress_summary()` test coverage
3. Integration test: create PRD → split stories → adjust priorities → verify ordering

---

**Generated**: 2026-05-03 01:00 AM
**Status:** ✅ Complete — 14 new tests, 117/117 passing, 3 methods now covered
