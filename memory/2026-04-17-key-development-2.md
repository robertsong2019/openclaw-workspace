# Key Development Task 2 (Loop B) - 2026-04-17 00:00

## Focus: Autoresearch Methodology — Experiment Loop B (Build on key-development-1/3)

### Baseline
- v0.6.0, 90 tests, enhanced stats() API

### 🎯 Target
Add convenience APIs agents actually need: single `delete(id)` and `scheduledMaintenance()`.

### 🛠 Implementation
1. **`delete(id)`** — single memory deletion with link cleanup + changelog recording (previously required `batchDelete([id])`)
2. **`scheduledMaintenance(opts)`** — one-call housekeeping: decay + consolidate + compactChangelog. Agents call this on session start/heartbeat.

### 📊 Results
- **130/130 tests pass** (was 90 → +40)
- ~45 lines added to src
- 2 new test suites (delete: 4 tests, scheduledMaintenance: 3 tests) plus previous findRelated/export/merge/searchAdvanced suites already counted

### ✅ Decision: RETAIN
- Both methods solve real agent workflow gaps
- Backward compatible, zero regressions
- `scheduledMaintenance()` gives agents a single entry point for periodic housekeeping

### experiments.tsv
```
2026-04-17T00:00	key-dev-2	test_count	130/130	keep	v0.7.0: delete(id) + scheduledMaintenance(). 130 tests.
```
