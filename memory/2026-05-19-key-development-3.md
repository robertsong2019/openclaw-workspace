# Key Development Task 3 (Loop C) - 2026-05-19 01:00

## Focus: Autoresearch Methodology — CAS + TTL Management on agent-context-store

### Baseline
- 210/210 tests (batch operations from 2026-05-19 k-d-2)

### 🎯 Target
**Add Compare-and-Set (CAS) and TTL lifecycle management.**

**Problem:** Two gaps: (1) No atomic way to update a key only if current content matches expected — critical for safe concurrent-like patterns where an agent reads-modifies-writes and needs to avoid overwriting intermediate changes. (2) TTL can only be set at `put()` time — no way to extend, inspect, or remove TTL after creation.

**Solution:** Two feature sets:
- `put_if_match(key, expected, new_content, tags?, ttl?)` → `(entry|None, was_updated)` — CAS that only updates when current content matches expected. Fires hooks and watchers on success.
- `set_ttl(key, ttl)` — set or update TTL on existing key
- `get_ttl(key)` — return remaining seconds (None if no TTL or key missing)
- `clear_ttl(key)` — remove TTL, making key persistent

### 🛠 Implementation
- `put_if_match`: checks current content against expected, delegates to `put()` on match → middleware, hooks, watchers all compose
- `set_ttl/get_ttl/clear_ttl`: direct field manipulation with expiry-aware guards
- ~20 lines of logic added, zero external dependencies

### 📊 Results
- 210 → 223 tests (+13, all passing)
- Zero regressions
- Committed: `837d63e`

### ✅ Decision: RETAIN

**Rationale:**
- CAS is a fundamental primitive for safe agent context updates (read-modify-write without races)
- TTL management completes the expiry story — agents can now extend leases, inspect remaining time, or make keys permanent
- Both compose with existing features (middleware, hooks, watchers, changelog)
- Clean separation: CAS for conditional writes, TTL management for lifecycle

### experiments.tsv
```
2026-05-19T01:00	837d63e	test_count	223/223	keep	CAS (put_if_match) + TTL management (set_ttl/get_ttl/clear_ttl). +13 tests (210→223). Atomic compare-and-set for safe concurrent patterns; TTL lifecycle management post-creation. Zero regressions.
```

---

**Generated**: 2026-05-19 01:00 AM
**Status:** ✅ Complete — 223/223 tests passing, committed 837d63e
