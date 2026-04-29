#!/usr/bin/env bash
# agent-log — Search, filter, and summarize OpenClaw session logs
# Zero dependencies. Works with standard OpenClaw directory layout.

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
SESSIONS_DIR="$HOME/.openclaw/sessions"
HEARTBEAT_STATE="$MEMORY_DIR/heartbeat-state.json"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; GRAY='\033[0;90m'; RESET='\033[0m'

die() { echo -e "${RED}Error:${RESET} $*" >&2; exit 1; }

# ── Commands ──

cmd_search() {
  local use_regex=0
  local query=""

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -r|--regex) use_regex=1 ;;
      *) query="$1" ;;
    esac
    shift
  done

  [[ -z "$query" ]] && die "Usage: agent-log search [-r|--regex] <query>"

  local files=()
  # Gather searchable files
  while IFS= read -r -d '' f; do files+=("$f"); done < <(
    find "$MEMORY_DIR" -name '*.md' -print0 2>/dev/null
    find "$WORKSPACE" -maxdepth 1 -name '*.md' -print0 2>/dev/null
    find "$SESSIONS_DIR" -name '*.md' -print0 2>/dev/null
  )

  if [[ ${#files[@]} -eq 0 ]]; then
    die "No log files found. Check WORKSPACE=$WORKSPACE"
  fi

  local search_type="text"
  [[ $use_regex -eq 1 ]] && search_type="regex"

  echo -e "${CYAN}Searching for ($search_type):${RESET} $query"
  echo -e "${GRAY}(${#files[@]} files)${RESET}"
  echo

  local grep_opts=(--include='*.md' -i)
  [[ $use_regex -eq 1 ]] && grep_opts+=(-E)

  grep -rl "${grep_opts[@]}" "$query" "${files[@]}" 2>/dev/null | while read -r f; do
    local rel="${f#$HOME/}"
    echo -e "${BLUE}$rel${RESET}"
    grep --color=always "${grep_opts[@]}" -n -C 1 "$query" "$f" 2>/dev/null | head -20 | sed 's/^/  /'
    echo
  done
}

cmd_today() {
  local today
  today=$(date +%Y-%m-%d)
  cmd_date "$today"
}

cmd_date() {
  local d="$1"
  local file="$MEMORY_DIR/${d}.md"

  echo -e "${CYAN}📅 $d${RESET}"
  echo

  if [[ -f "$file" ]]; then
    cat "$file"
  else
    echo -e "${GRAY}(no daily notes for $d)${RESET}"
  fi

  # Check session files modified on that date
  if [[ -d "$SESSIONS_DIR" ]]; then
    echo
    echo -e "${YELLOW}Session activity:${RESET}"
    find "$SESSIONS_DIR" -name '*.md' -newermt "$d 00:00:00" ! -newermt "$d 23:59:59" -print0 2>/dev/null \
      | xargs -0 -I{} bash -c 'echo -e "  ${GRAY}$(stat -c %y "{}" 2>/dev/null | cut -d. -f1)${RESET} {}"' 2>/dev/null \
      | sort | head -20
  fi
}

cmd_summary() {
  local days="${1:-7}"
  echo -e "${CYAN}📊 Activity summary (last $days days)${RESET}"
  echo

  local total_lines=0 total_files=0
  for ((i=0; i<days; i++)); do
    local d
    d=$(date -d "$i days ago" +%Y-%m-%d 2>/dev/null || date -v-${i}d +%Y-%m-%d 2>/dev/null)
    local file="$MEMORY_DIR/${d}.md"
    if [[ -f "$file" ]]; then
      local lines
      lines=$(wc -l < "$file")
      total_lines=$((total_lines + lines))
      total_files=$((total_files + 1))
      local weekday
      weekday=$(date -d "$d" +%a 2>/dev/null || date -j -f "%Y-%m-%d" "$d" +%a 2>/dev/null)
      printf "  ${GREEN}%s %-3s${RESET} %4d lines\n" "$d" "$weekday" "$lines"
    fi
  done

  echo
  echo -e "  ${YELLOW}Total:${RESET} $total_files files, $total_lines lines"

  # MEMORY.md size
  if [[ -f "$WORKSPACE/MEMORY.md" ]]; then
    local mem_lines
    mem_lines=$(wc -l < "$WORKSPACE/MEMORY.md")
    echo -e "  ${YELLOW}MEMORY.md:${RESET} $mem_lines lines"
  fi
}

cmd_cron() {
  echo -e "${CYAN}⏰ Cron logs${RESET}"
  echo
  if command -v openclaw &>/dev/null; then
    openclaw cron list 2>/dev/null || echo -e "${GRAY}(openclaw cron not available)${RESET}"
  else
    echo -e "${GRAY}(openclaw CLI not in PATH)${RESET}"
  fi
}

cmd_stats() {
  echo -e "${CYAN}📈 Workspace stats${RESET}"
  echo

  # Memory files
  local mem_count=0
  [[ -d "$MEMORY_DIR" ]] && mem_count=$(find "$MEMORY_DIR" -name '*.md' | wc -l)
  echo -e "  Memory files:   ${GREEN}$mem_count${RESET}"

  # Session files
  local sess_count=0
  [[ -d "$SESSIONS_DIR" ]] && sess_count=$(find "$SESSIONS_DIR" -name '*.md' | wc -l)
  echo -e "  Session files:  ${GREEN}$sess_count${RESET}"

  # Workspace size
  local ws_size
  ws_size=$(du -sh "$WORKSPACE" 2>/dev/null | cut -f1)
  echo -e "  Workspace size: ${GREEN}$ws_size${RESET}"

  # Recent activity
  local latest_file=""
  local latest_time=0
  for f in "$MEMORY_DIR"/*.md; do
    [[ -f "$f" ]] || continue
    local t
    t=$(stat -c %Y "$f" 2>/dev/null || echo 0)
    if (( t > latest_time )); then
      latest_time=$t
      latest_file="$f"
    fi
  done
  if [[ -n "$latest_file" ]]; then
    echo -e "  Latest note:    ${BLUE}$(basename "$latest_file")${RESET}"
  fi
}

# ── Main ──

usage() {
  sed -n '/^## Usage/,/^## /p' "$0" | head -n -1 | sed 's/^## //;s/^# //' | tail -n +2
}

case "${1:-help}" in
  search)  shift; cmd_search "$@" ;;
  today)   cmd_today ;;
  date)    [[ -z "${2:-}" ]] && die "Usage: agent-log date YYYY-MM-DD"; cmd_date "$2" ;;
  summary) cmd_summary "${2:-7}" ;;
  cron)    cmd_cron ;;
  stats)   cmd_stats ;;
  help|*)  usage ;;
esac
