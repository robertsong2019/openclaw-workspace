#!/usr/bin/env bash
# Tests for F23 (hot command): top-K term ranking, JSON export, date window, error paths
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$SCRIPT_DIR/agent-log.sh"

# Setup temp workspace
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

export OPENCLAW_WORKSPACE="$TMPDIR"
MEMORY="$TMPDIR/memory"
mkdir -p "$MEMORY"

# Fixture: three daily notes with known term frequencies.
# alpha=4, beta=4, gamma=2, zeta=1 across the window; omega only outside window.
printf 'alpha beta gamma alpha\nfoo bar alpha gamma\n' > "$MEMORY/2026-09-20.md"
printf 'beta beta zeta\n' > "$MEMORY/2026-09-19.md"
printf 'alpha beta\n' > "$MEMORY/2026-09-18.md"
printf 'old stuff omega omega\n' > "$MEMORY/2026-08-01.md"

pass=0 fail=0
assert() {
  local label="$1" expected="$2" actual="$3"
  if [[ "$actual" == "$expected" ]]; then
    echo "  ✅ $label"
    ((pass++)) || true
  else
    echo "  ❌ $label"
    echo "    expected: $expected"
    echo "    actual:   $actual"
    ((fail++)) || true
  fi
}

echo ""
echo "=== hot: ranking ==="

# Test 1: plain output shows header with file count
output=$(bash "$SCRIPT" hot -n 5)
header_found=0; echo "$output" | grep -q "Top terms:" && header_found=1
assert "plain output has header" "1" "$header_found"

# Test 2: file count line reports all 4 files
fc=$(echo "$output" | grep -oE '\(4 files, top 5\)' || true)
assert "file count shown" "(4 files, top 5)" "$fc"

# Test 3: top-1 picks a max-count term (alpha or beta, both = 4)
top1=$(bash "$SCRIPT" hot -n 1 | grep -oE '(alpha|beta)' | head -1)
assert "top-1 is a max term" "1" "$([[ -n "$top1" ]] && echo 1 || echo 0)"

# Test 4: -n 2 returns exactly 2 term lines
n_lines=$(bash "$SCRIPT" hot -n 2 | grep -cE '^ +[0-9]+ ' || true)
assert "-n 2 returns 2 terms" "2" "$n_lines"

# Test 5: tie-break — equal counts ordered by term descending (beta before alpha)
tie=$(bash "$SCRIPT" hot -n 2 -j | grep -o '"term":"[a-z]*"' | head -2 | tr '\n' ' ')
assert "tie-break: beta before alpha at count=4" '"term":"beta" "term":"alpha" ' "$tie"

# Test 6: stopwords excluded (the/and/with never ranked)
sw=$(bash "$SCRIPT" hot -j | grep -cE '"term":"(the|and|with)"' || true)
assert "stopwords excluded" "0" "$sw"

# Test 7: terms shorter than 3 chars excluded
short=$(printf 'ab ab ab cd\n' > "$MEMORY/2026-09-17.md"; bash "$SCRIPT" hot -j | grep -cE '"term":"(ab|cd)"' || true)
assert "min-length-3 enforced" "0" "$short"
rm -f "$MEMORY/2026-09-17.md"

echo ""
echo "=== hot: JSON export ==="

# Test 8: JSON structure has command/n/file_count/terms
j=$(bash "$SCRIPT" hot -n 3 -j)
valid=0
echo "$j" | grep -q '"command":"hot"' && echo "$j" | grep -q '"file_count":4' && echo "$j" | grep -q '"terms":\[' && valid=1
assert "JSON has command/file_count/terms" "1" "$valid"

# Test 9: JSON counts correct — zeta appears exactly once
zeta_cnt=$(bash "$SCRIPT" hot -j | grep -o '{"term":"zeta","count":[0-9]*}' | grep -o '[0-9]*}$' | tr -d '}')
assert "zeta count = 1" "1" "$zeta_cnt"

# Test 10: JSON parses with python3 (well-formed)
py_ok=$(bash "$SCRIPT" hot -n 3 -j | python3 -c 'import json,sys; d=json.load(sys.stdin); print(1 if len(d["terms"])==3 else 0)')
assert "JSON well-formed, 3 terms" "1" "$py_ok"

echo ""
echo "=== hot: date window ==="

# Test 11: --from filters out older files (omega gone)
from_j=$(bash "$SCRIPT" hot --from 2026-09-15 -j)
omega=0; echo "$from_j" | grep -q '"term":"omega"' && omega=1
assert "--from excludes omega" "0" "$omega"

# Test 12: --from window file_count = 3
fc3=$(echo "$from_j" | grep -o '"file_count":[0-9]*' | grep -o '[0-9]*$')
assert "--from file_count = 3" "3" "$fc3"

# Test 13: --to narrows window to older files only
to_j=$(bash "$SCRIPT" hot --to 2026-08-31 -j)
omega2=$(echo "$to_j" | grep -o '"term":"omega","count":[0-9]*' | grep -o '[0-9]*$')
assert "--to window keeps omega" "2" "$omega2"

# Test 14: --from + --to narrow band
band=$(bash "$SCRIPT" hot --from 2026-09-19 --to 2026-09-20 -j | grep -o '"file_count":[0-9]*' | grep -o '[0-9]*$')
assert "band window file_count = 2" "2" "$band"

# Test 15: window with no files dies
bash "$SCRIPT" hot --from 2020-01-01 --to 2020-01-02 >/dev/null 2>&1 && rc=0 || rc=$?
assert "empty window exits 1" "1" "$rc"

echo ""
echo "=== hot: error paths ==="

# Test 16: -n 0 rejected
err=$(bash "$SCRIPT" hot -n 0 2>&1 || true)
rc_ok=0; echo "$err" | grep -q "requires a positive integer" && rc_ok=1
assert "-n 0 error message" "1" "$rc_ok"

# Test 17: -n 0 exit code
bash "$SCRIPT" hot -n 0 >/dev/null 2>&1 && rc=0 || rc=$?
assert "-n 0 exits 1" "1" "$rc"

# Test 18: bad --from date rejected
bash "$SCRIPT" hot --from notadate >/dev/null 2>&1 && rc=0 || rc=$?
assert "bad --from exits 1" "1" "$rc"

# Test 19: bad --to date message
msg=$(bash "$SCRIPT" hot --to bad 2>&1 || true)
m_ok=0; echo "$msg" | grep -q "requires YYYY-MM-DD format" && m_ok=1
assert "bad --to message" "1" "$m_ok"

# Test 20: empty workspace dies
T2=$(mktemp -d); mkdir -p "$T2/memory"
OPENCLAW_WORKSPACE="$T2" bash "$SCRIPT" hot >/dev/null 2>&1 && rc=0 || rc=$?
assert "empty workspace exits 1" "1" "$rc"
rm -rf "$T2"

# Test 21: positional N works (hot 2 == hot -n 2)
pos=$(bash "$SCRIPT" hot 2 | grep -cE '^ +[0-9]+ ' || true)
assert "positional N" "2" "$pos"

echo ""
echo "Results: $pass pass / $fail fail"
[[ $fail -eq 0 ]]
