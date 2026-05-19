#!/usr/bin/env bash
# Tests for F11 (CSV export) and F15 (clean command)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$SCRIPT_DIR/agent-log.sh"

# Setup temp workspace
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

export OPENCLAW_WORKSPACE="$TMPDIR"
MEMORY="$TMPDIR/memory"
mkdir -p "$MEMORY"

# Create sample daily notes
for i in 0 1 2 3; do
  d=$(date -d "$i days ago" +%Y-%m-%d 2>/dev/null || date -v-${i}d +%Y-%m-%d)
  echo "Line 1 for $d" > "$MEMORY/$d.md"
  echo "Line 2 for $d" >> "$MEMORY/$d.md"
  echo "Line 3 for $d" >> "$MEMORY/$d.md"
done

# Create one empty file
echo -n "" > "$MEMORY/2020-01-01.md"

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

# ── F11: CSV export tests ──
echo ""
echo "=== F11: CSV export ==="

# Test 1: summary --csv outputs CSV header
output=$(bash "$SCRIPT" summary --csv 4)
header_found=0; echo "$output" | grep -q "date,weekday,lines" && header_found=1
assert "CSV header present" "1" "$header_found"

# Test 2: CSV has correct number of data rows
row_count=$(echo "$output" | grep -c "^[0-9].*,.*,.*[0-9]$" || true)
assert "CSV has data rows" "1" "$([[ $row_count -ge 3 ]] && echo 1 || echo 0)"

# Test 3: CSV format is valid (date,weekday,number)
first_row=$(echo "$output" | grep "^[0-9]" | head -1)
csv_valid=0
[[ "$first_row" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2},[A-Za-z]{3},[0-9]+$ ]] && csv_valid=1
assert "CSV row format valid" "1" "$csv_valid"

# Test 4: --csv with keyword filter
output2=$(bash "$SCRIPT" summary --csv -k "Line" 4)
header_found2=0; echo "$output2" | grep -q "date,weekday,lines" && header_found2=1
assert "CSV with keyword has header" "1" "$header_found2"

# ── F15: clean command tests ──
echo ""
echo "=== F15: clean command ==="

# Test 5: dry run doesn't delete files
file_count_before=$(find "$MEMORY" -name '*.md' | wc -l)
bash "$SCRIPT" clean --dry-run > /dev/null 2>&1
file_count_after=$(find "$MEMORY" -name '*.md' | wc -l)
assert "Dry run preserves files" "$file_count_before" "$file_count_after"

# Test 6: clean removes empty files
bash "$SCRIPT" clean > /dev/null 2>&1
empty_exists=1
[[ -f "$MEMORY/2020-01-01.md" ]] || empty_exists=0
assert "Empty file removed" "0" "$empty_exists"

# Test 7: clean --age removes old files
echo "old content" > "$MEMORY/2019-12-31.md"
bash "$SCRIPT" clean --age 365 > /dev/null 2>&1
old_exists=1
[[ -f "$MEMORY/2019-12-31.md" ]] || old_exists=0
assert "Old file removed by age" "0" "$old_exists"

# Test 8: clean --age preserves recent files
today=$(date +%Y-%m-%d)
recent_exists=0
[[ -f "$MEMORY/$today.md" ]] && recent_exists=1
assert "Recent file preserved" "1" "$recent_exists"

echo ""
echo "Results: $pass passed, $fail failed"
exit $fail
