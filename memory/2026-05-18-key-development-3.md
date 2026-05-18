# Key Development Task 3 (Loop C) - 2026-05-18 01:00

## Focus: Autoresearch Methodology — Key Watchers on agent-context-store

### Baseline
- 194/194 tests (middleware pipeline from 2026-05-18 k-d-2)

### 🎯 Target
**Add key-level watchers — `watch(key, callback)` for per-key mutation observation.**

**Problem:** Event hooks (`on/off`) fire on ALL mutations — no way to observe a specific key. In practice, agents often care about "tell me when *this* key changes", not every put/delete in the store. Filtering in the hook callback is verbose and wasteful.

**Solution:** `watch(key, callback)` / `unwatch(key, callback?)` — register per-key observers. Callback receives `(key, event, **kwargs)`. Fires on create/update/delete for that key only. `unwatch` without callback removes all watchers for that key.

### 🛠 Implementation
- `_watchers: dict[str, list[callable]]` on init
- `watch(key, callback)`: append to key's watcher list
- `unwatch(key, callback?)`: remove specific or all, returns count removed
- `_emit_watchers(key, event)`: fires all watchers for that key
- Wired into `put()` (create/update) and `delete()`
- ~15 lines added, zero external dependencies

### 📊 Results
- 194 → 202 tests (+8, all passing)
- Zero regressions
- Committed: `334f9ae`

### ✅ Decision: RETAIN

**Rationale:**
- Complements event hooks: hooks = global broadcast, watchers = targeted subscribe
- Natural API: `store.watch('config', on_config_change)` — no boilerplate
- `unwatch` with count return enables cleanup patterns
- Independent of middleware (before) and hooks (after) — watchers are a third axis of reactivity
- Minimal footprint: 3 new public methods, 1 internal, 1 data field

### experiments.tsv
```
2026-05-18T01:00	334f9ae	test_count	202/202	keep	key watchers: watch/unwatch per-key mutation observers. +8 tests (194→202). Fires on create/update/delete for watched key only.
```

---

**Generated**: 2026-05-18 01:00 AM
**Status:** ✅ Complete — 202/202 tests passing, committed 334f9ae
