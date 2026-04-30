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

# Global JSON flag
JSON_OUTPUT=0

die() { echo -e "${RED}Error:${RESET} $*" >&2; exit 1; }

# ── Helper: build JSON result for search ──
build_search_json() {
  local query="$1" stype="$2"
  shift 2
  local items=("$@")
  local count=${#items[@]}
  printf '{"command":"search","query":"%s","type":"%s","file_count":%d,"results":[%s]}\n' \
    "$query" "$stype" "$count" "$(IFS=,; echo "${items[*]}")"
}

# ── Commands ──

cmd_search() {
  local use_regex=0 query="" output_file=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -r|--regex) use_regex=1 ;;
      -o|--output) shift; output_file="${1:-}" ;;
      -j|--json) JSON_OUTPUT=1 ;;
      *) query="$1" ;;
    esac
    shift
  done

  [[ -z "$query" ]] && die "Usage: agent-log search [-r|--regex] [-o file] [-j|--json] <query>"

  local files=()
  while IFS= read -r -d '' f; do files+=("$f"); done < <(
    find "$MEMORY_DIR" -name '*.md' -print0 2>/dev/null
    find "$WORKSPACE" -maxdepth 1 -name '*.md' -print0 2>/dev/null
    find "$SESSIONS_DIR" -name '*.md' -print0 2>/dev/null
  )
  [[ ${#files[@]} -eq 0 ]] && die "No log files found. Check WORKSPACE=$WORKSPACE"

  local search_type="text"
  [[ $use_regex -eq 1 ]] && search_type="regex"

  local grep_opts=(--include='*.md' -i)
  [[ $use_regex -eq 1 ]] && grep_opts+=(-E)

  local json_results=()
  local plain_output=""

  local found_files
  found_files=$(grep -rl "${grep_opts[@]}" "$query" "${files[@]}" 2>/dev/null || true)

  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    local rel="${f#$HOME/}"
    if [[ $JSON_OUTPUT -eq 1 ]]; then
      local matches
      matches=$(grep "${grep_opts[@]}" -c "$query" "$f" 2>/dev/null || echo 0)
      # Escape special chars in filename for JSON
      local esc_rel="${rel//\"/\\\"}"
      json_results+=("{\"file\":\"$esc_rel\",\"matches\":$matches}")
    else
      plain_output+="$(echo -e "${BLUE}$rel${RESET}")"$'\n'
      plain_output+="$(grep --color=always "${grep_opts[@]}" -n -C 1 "$query" "$f" 2>/dev/null | head -20 | sed 's/^/  /' || true)"$'\n\n'
    fi
  done <<< "$found_files"

  if [[ $JSON_OUTPUT -eq 1 ]]; then
    build_search_json "$query" "$search_type" "${json_results[@]+${json_results[@]}}"
  else
    echo -e "${CYAN}Searching for ($search_type):${RESET} $query"
    echo -e "${GRAY}(${#files[@]} files)${RESET}"
    echo
    echo -n "$plain_output"
  fi

  # Export to file
  if [[ -n "$output_file" ]]; then
    {
      echo "# Search results for: $query"
      echo "# Type: $search_type"
      echo "# Generated: $(date -Iseconds)"
      echo ""
      if [[ -n "$found_files" ]]; then
        while IFS= read -r f; do
          [[ -z "$f" ]] && continue
          echo "== ${f#$HOME/} =="
          grep "${grep_opts[@]}" -n -C 1 "$query" "$f" 2>/dev/null | head -20
          echo ""
        done <<< "$found_files"
      fi
    } > "$output_file"
    echo -e "${GREEN}Results exported to: $output_file${RESET}"
  fi
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
  if [[ -f "$file" ]]; then cat "$file"; else echo -e "${GRAY}(no daily notes for $d)${RESET}"; fi
  if [[ -d "$SESSIONS_DIR" ]]; then
    echo; echo -e "${YELLOW}Session activity:${RESET}"
    find "$SESSIONS_DIR" -name '*.md' -newermt "$d 00:00:00" ! -newermt "$d 23:59:59" -print0 2>/dev/null \
      | xargs -0 -I{} bash -c 'echo -e "  ${GRAY}$(stat -c %y "{}" 2>/dev/null | cut -d. -f1)${RESET} {}"' 2>/dev/null \
      | sort | head -20
  fi
}

cmd_summary() {
  local days="7" keyword=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -j|--json) JSON_OUTPUT=1 ;;
      -d|--days) shift; days="${1:-7}" ;;
      -k|--keyword) shift; keyword="${1:-}" ;;
      [0-9]*) days="$1" ;;
      *) keyword="$1" ;;
    esac
    shift
  done

  [[ $JSON_OUTPUT -eq 0 ]] && { echo -e "${CYAN}📊 Activity summary (last $days days)${RESET}"; [[ -n "$keyword" ]] && echo "  [filter: $keyword]"; echo; }

  local total_lines=0 total_files=0 json_entries=()

  for ((i=0; i<days; i++)); do
    local d
    d=$(date -d "$i days ago" +%Y-%m-%d 2>/dev/null || date -v-${i}d +%Y-%m-%d 2>/dev/null)
    local file="$MEMORY_DIR/${d}.md"
    [[ -f "$file" ]] || continue
    [[ -n "$keyword" ]] && ! grep -qi "$keyword" "$file" 2>/dev/null && continue
    local lines; lines=$(wc -l < "$file")
    total_lines=$((total_lines + lines)); total_files=$((total_files + 1))
    local weekday; weekday=$(date -d "$d" +%a 2>/dev/null || date -j -f "%Y-%m-%d" "$d" +%a 2>/dev/null)
    json_entries+=("{\"date\":\"$d\",\"weekday\":\"$weekday\",\"lines\":$lines}")
    [[ $JSON_OUTPUT -eq 0 ]] && printf "  ${GREEN}%s %-3s${RESET} %4d lines\n" "$d" "$weekday" "$lines"
  done

  if [[ $JSON_OUTPUT -eq 1 ]]; then
    printf '{"command":"summary","days":%s,"keyword":"%s","total_files":%d,"total_lines":%d,"entries":[%s]}\n' \
      "$days" "$keyword" "$total_files" "$total_lines" "$(IFS=,; echo "${json_entries[*]+${json_entries[*]}}")"
  else
    echo; echo -e "  ${YELLOW}Total:${RESET} $total_files files, $total_lines lines"
    if [[ -f "$WORKSPACE/MEMORY.md" ]]; then
      local mem_lines; mem_lines=$(wc -l < "$WORKSPACE/MEMORY.md")
      echo -e "  ${YELLOW}MEMORY.md:${RESET} $mem_lines lines"
    fi
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
  while [[ $# -gt 0 ]]; do case "$1" in -j|--json) JSON_OUTPUT=1 ;; esac; shift; done

  local mem_count=0 sess_count=0
  [[ -d "$MEMORY_DIR" ]] && mem_count=$(find "$MEMORY_DIR" -name '*.md' | wc -l)
  [[ -d "$SESSIONS_DIR" ]] && sess_count=$(find "$SESSIONS_DIR" -name '*.md' | wc -l)
  local ws_size; ws_size=$(du -sh "$WORKSPACE" 2>/dev/null | cut -f1)

  local latest_file="" latest_time=0
  for f in "$MEMORY_DIR"/*.md; do
    [[ -f "$f" ]] || continue
    local t; t=$(stat -c %Y "$f" 2>/dev/null || echo 0)
    (( t > latest_time )) && { latest_time=$t; latest_file="$f"; }
  done
  local latest_name=""; [[ -n "$latest_file" ]] && latest_name=$(basename "$latest_file")

  if [[ $JSON_OUTPUT -eq 1 ]]; then
    printf '{"command":"stats","memory_files":%d,"session_files":%d,"workspace_size":"%s","latest_note":"%s"}\n' \
      "$mem_count" "$sess_count" "$ws_size" "$latest_name"
  else
    echo -e "${CYAN}📈 Workspace stats${RESET}"
    echo
    echo -e "  Memory files:   ${GREEN}$mem_count${RESET}"
    echo -e "  Session files:  ${GREEN}$sess_count${RESET}"
    echo -e "  Workspace size: ${GREEN}$ws_size${RESET}"
    [[ -n "$latest_file" ]] && echo -e "  Latest note:    ${BLUE}$(basename "$latest_file")${RESET}"
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
  summary) shift; cmd_summary "$@" ;;
  cron)    cmd_cron ;;
  stats)   shift; cmd_stats "$@" ;;
  help|*)  usage ;;
esac
