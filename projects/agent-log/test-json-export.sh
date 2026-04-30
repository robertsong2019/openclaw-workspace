#!/usr/bin/env bash
# Test script for F10: JSON output + F3: search export

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_LOG="$SCRIPT_DIR/agent-log.sh"

GREEN='\033[0;32m'; RED='\033[0;31m'; RESET='\033[0m'

test_count=0 passed_count=0 failed_count=0

run_test() {
  local name="$1" cmd="$2" expected="$3" expect_fail="${4:-0}"
  ((test_count++))
  echo -n "Test $test_count: $name ... "
  local output; output=$(eval "$cmd" 2>&1); local ec=$?
  if [[ $expect_fail -eq 1 ]]; then
    if [[ $ec -ne 0 ]] && echo "$output" | grep -qF "$expected"; then
      echo -e "${GREEN}PASSED${RESET}"; ((passed_count++))
    else
      echo -e "${RED}FAILED${RESET}"; ((failed_count++))
    fi
  else
    if [[ $ec -ne 0 ]]; then
      echo -e "${RED}FAILED${RESET} (exit $ec)"; ((failed_count++))
      echo "$output" | head -3 | sed 's/^/  /'
    elif echo "$output" | grep -qF "$expected"; then
      echo -e "${GREEN}PASSED${RESET}"; ((passed_count++))
    else
      echo -e "${RED}FAILED${RESET} (pattern not found)"; ((failed_count++))
      echo "  Expected: $expected"
      echo "$output" | head -3 | sed 's/^/  /'
    fi
  fi
}

echo "=== Tests for F10: JSON output ==="
echo

run_test "stats --json outputs valid JSON" \
  "$AGENT_LOG stats --json" \
  '"command":"stats"'

run_test "stats -j includes memory_files" \
  "$AGENT_LOG stats -j" \
  '"memory_files":'

run_test "summary --json outputs valid JSON" \
  "$AGENT_LOG summary --json" \
  '"command":"summary"'

run_test "summary -j includes entries" \
  "$AGENT_LOG summary 7 -j" \
  '"entries":'

run_test "summary -j -d 3" \
  "$AGENT_LOG summary -d 3 -j" \
  '"days":3'

run_test "search --json outputs valid JSON" \
  "$AGENT_LOG search --json 'agent'" \
  '"command":"search"'

run_test "search -j includes file_count" \
  "$AGENT_LOG search -j 'memory'" \
  '"file_count":'

echo
echo "=== Tests for F3: search export ==="
echo

EXPORT_FILE="/tmp/agent-log-export-test-$$.txt"
# Use || true to avoid pipefail issues
run_test "search -o exports results to file" \
  "$AGENT_LOG search 'agent' -o $EXPORT_FILE; test -s $EXPORT_FILE && echo FILE_EXISTS" \
  "FILE_EXISTS"

run_test "export file contains header" \
  "grep -F 'Search results' $EXPORT_FILE" \
  "Search results"

run_test "export file contains matched content" \
  "grep -i 'agent' $EXPORT_FILE | head -1" \
  "agent"

rm -f "$EXPORT_FILE"

echo
echo "=== Summary ==="
echo -e "  Total: $test_count  ${GREEN}Passed: $passed_count${RESET}  ${RED}Failed: $failed_count${RESET}"
[[ $failed_count -eq 0 ]] && echo -e "\n${GREEN}All tests passed!${RESET}" && exit 0
echo -e "\n${RED}Some tests failed!${RESET}" && exit 1
