# Key Development Task 3 (Loop C) - 2026-05-09 01:00

## Focus: Autoresearch Methodology — `append()` + `expire_in()` + `age()` on agent-context-store

### Baseline
- 39 tests passing (after search_regex from k-d-2 05-09, retag from k-d-3 05-08)
- No way to append to content without full `put()` overwrite
- No way to set/update TTL without touching content
- No way to query entry age

### 🎯 Target
**Add 3 APIs: `append(key, text, separator)` + `expire_in(key, ttl_hours)` + `age(key)`**

**Problems:**
1. To add a line to a log entry, you need `get()` → concatenate → `put()`, which is fragile and verbose
2. `touch()` can extend TTL but only if entry already has one; setting initial TTL requires `put()` with content
3. No way to check how old an entry is for TTL-aware logic

**Solutions:**
1. `append(key, text, separator="\\n")` — appends to content, preserves created_at
2. `expire_in(key, ttl_hours)` — set/update TTL independently, can revive expired entries (sets new TTL before _save purge)
3. `age(key)` — returns seconds since creation, None if missing

### 🛠 Implementation

**context_store.py (~30 lines added):**
- `append(key, text, separator)` → Optional[Entry], preserves created_at, default newline separator
- `expire_in(key, ttl_hours)` → bool, works on any entry including expired (revives)
- `age(key)` → Optional[float], seconds since created_at

**9 new tests:**
1. ✅ append basic: content concatenation with newline
2. ✅ append custom separator (comma)
3. ✅ append preserves created_at
4. ✅ append missing key returns None
5. ✅ expire_in sets TTL on entry without one
6. ✅ expire_in missing key returns False
7. ✅ expire_in revives manually-expired entries
8. ✅ age returns non-negative float for fresh entry
9. ✅ age returns None for missing key

### 📊 Results
- 39 → 48 tests (+9, all passing)
- Zero regressions
- Committed: `cfc8132`

### ✅ Decision: RETAIN

**Rationale:**
- Real API gaps — agents frequently need to append logs/notes, manage TTLs independently, and check age
- `append` avoids the get→modify→put pattern that risks losing created_at
- `expire_in` decouples TTL from content, supports revival of stale entries
- `age` enables TTL-aware conditional logic in agent code
- Minimal code, no external deps, orthogonal to existing APIs

### experiments.tsv
```
2026-05-09T01:00	cfc8132	test_count	48/48	keep	Add append(key, text, separator) + expire_in(key, ttl_hours) + age(key): surgical content mutation + TTL management without overwrite + entry age query. append preserves created_at. expire_in can revive expired entries. age returns seconds since creation. +9 tests (39→48).
```

### 🔮 Potential Next Steps
1. `prepend(key, text)` — add content to the beginning
2. `replace_content(key, old, new)` — substring replacement within content
3. `snapshot()` / `restore()` — save/restore full store state for undo
4. `watch(key, callback)` — register change listeners (advanced)

---

**Generated**: 2026-05-09 01:00 AM
**Context**: Key Development Task 3 cron execution
**Focus**: Autoresearch methodology — incremental experiment loop C
**Status:** ✅ Session complete — 48/48 tests passing, committed cfc8132
