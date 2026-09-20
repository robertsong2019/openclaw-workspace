#!/usr/bin/env bash
# Tests for cron command: CLI listing, --job pattern filter, missing-arg and no-CLI paths
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$SCRIPT_DIR/agent-log.sh"

# Setup temp dir with fake openclaw CLI on PATH
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT
BIN="$TMPDIR/bin"
mkdir -p "$BIN"
cat > "$BIN/openclaw" <<'FAKE'
#!/usr/bin/env bash
echo "cron: 2 ok / 0 error / 0 running / 3 total"
echo "  aaa11111 project-testing-morning  0 3 * * *"
echo "  bbb22222 essay-morning  0 7 * * *"
echo "  ccc33333 heartbeat  */30 * * * *"
FAKE
chmod +x "$BIN/openclaw"

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
echo "=== cron: listing ==="

# Test 1: header present
out=$(PATH="$BIN:$PATH" bash "$SCRIPT" cron)
h=0; echo "$out" | grep -q "Cron logs" && h=1
assert "header shown" "1" "$h"

# Test 2: fake CLI listing passes through (3 job lines)
n=$(PATH="$BIN:$PATH" bash "$SCRIPT" cron | grep -cE '^  [a-z0-9]{8} ' || true)
assert "3 job lines listed" "3" "$n"

# Test 3: CLI unavailable → fallback message
out2=$(PATH="/usr/bin" bash "$SCRIPT" cron)
fb=0; echo "$out2" | grep -q "openclaw CLI not in PATH" && fb=1
assert "no-CLI fallback message" "1" "$fb"

echo ""
echo "=== cron: --job filter ==="

# Test 4: --job matches only essay line
f=$(PATH="$BIN:$PATH" bash "$SCRIPT" cron --job essay | grep -cE '^  [a-z0-9]{8} ' || true)
assert "--job essay → 1 line" "1" "$f"

# Test 5: matched line contains the job name
m=$(PATH="$BIN:$PATH" bash "$SCRIPT" cron --job essay | grep -c "essay-morning" || true)
assert "--job line contains essay-morning" "1" "$m"

# Test 6: case-insensitive match
ci=$(PATH="$BIN:$PATH" bash "$SCRIPT" cron --job ESSAY | grep -c "essay-morning" || true)
assert "--job is case-insensitive" "1" "$ci"

# Test 7: no match → hint, zero job lines
nm=$(PATH="$BIN:$PATH" bash "$SCRIPT" cron --job zzznomatch)
nm_lines=$(echo "$nm" | grep -cE '^  [a-z0-9]{8} ' || true)
nm_hint=0; echo "$nm" | grep -q "no matching cron jobs for: zzznomatch" && nm_hint=1
assert "no-match hint shown" "1" "$nm_hint"
assert "no-match has 0 job lines" "0" "$nm_lines"

# Test 8: no match still exits 0
PATH="$BIN:$PATH" bash "$SCRIPT" cron --job zzznomatch >/dev/null 2>&1 && rc=0 || rc=$?
assert "no-match exit 0" "0" "$rc"

echo ""
echo "=== cron: error paths ==="

# Test 9: --job without pattern → stderr + exit 1
PATH="$BIN:$PATH" bash "$SCRIPT" cron --job >/dev/null 2>/dev/null && rc=0 || rc=$?
assert "--job missing arg exits 1" "1" "$rc"

# Test 10: --job missing arg message on stderr
errm=$(PATH="$BIN:$PATH" bash "$SCRIPT" cron --job 2>&1 >/dev/null || true)
em=0; echo "$errm" | grep -q "requires a pattern" && em=1
assert "--job missing arg stderr message" "1" "$em"

echo ""
echo "Results: $pass pass / $fail fail"
[[ $fail -eq 0 ]]
