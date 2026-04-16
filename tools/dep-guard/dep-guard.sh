#!/usr/bin/env bash
# dep-guard 🔒 — Dependency health & security scanner
# Supports: Node.js (package.json), Python (requirements.txt)
set -euo pipefail

VERSION="1.0.0"
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# Defaults
FORMAT="text"
SECURITY_ONLY=false
MIN_SCORE=0
PROJECT_DIR="."

usage() {
  cat <<EOF
dep-guard v${VERSION} — Dependency health & security scanner

Usage: dep-guard.sh [options] [project-dir]

Options:
  --format FORMAT    Output: text, json, markdown (default: text)
  --security-only    Only check for vulnerabilities
  --min-score N      Exit 1 if health score < N (CI mode)
  --help             Show this help
  --version          Show version
EOF
  exit 0
}

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --format)   FORMAT="$2"; shift 2 ;;
    --security-only) SECURITY_ONLY=true; shift ;;
    --min-score) MIN_SCORE="$2"; shift 2 ;;
    --help) usage ;;
    --version) echo "dep-guard v${VERSION}"; exit 0 ;;
    -*) echo "Unknown option: $1"; exit 1 ;;
    *) PROJECT_DIR="$1"; shift ;;
  esac
done

cd "$PROJECT_DIR" 2>/dev/null || { echo "Error: cannot access $PROJECT_DIR"; exit 1; }

# ─── Detect project type ────────────────────────────
detect_project() {
  if [[ -f package.json ]]; then echo "node"
  elif [[ -f requirements.txt ]] || [[ -f pyproject.toml ]] || [[ -f Pipfile ]]; then echo "python"
  else echo "unknown"
  fi
}

PROJECT_TYPE=$(detect_project)
if [[ "$PROJECT_TYPE" == "unknown" ]]; then
  echo "Error: No package.json or requirements.txt found in $PROJECT_DIR"
  exit 1
fi

# ─── Data collectors ────────────────────────────────
declare -a VULNS=()
declare -a OUTDATED_MAJOR=()
declare -a OUTDATED_MINOR=()
HAS_LOCKFILE=false

scan_node() {
  # Lockfile check
  [[ -f package-lock.json || -f yarn.lock || -f pnpm-lock.yaml ]] && HAS_LOCKFILE=true

  # Security audit
  if command -v npm &>/dev/null; then
    local audit_output
    audit_output=$(npm audit --json 2>/dev/null || true)
    if [[ -n "$audit_output" ]]; then
      local vuln_count
      vuln_count=$(echo "$audit_output" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    v = d.get('metadata',{}).get('vulnerabilities',{})
    print(v.get('high',0) + v.get('critical',0))
except: print(0)
" 2>/dev/null || echo 0)
      local total_vulns
      total_vulns=$(echo "$audit_output" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    v = d.get('metadata',{}).get('vulnerabilities',{})
    print(sum(v.values()))
except: print(0)
" 2>/dev/null || echo 0)
      if [[ "$total_vulns" -gt 0 ]]; then
        # Extract individual vulns
        echo "$audit_output" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    for name, info in d.get('vulnerabilities',{}).items():
        severity = info.get('severity','?')
        title = info.get('title','')
        print(f'{severity}|{name}|{title}')
except: pass
" 2>/dev/null | while IFS='|' read -r sev name title; do
          VULNS+=("$sev|$name|$title")
        done
      fi
    fi
  fi

  # Outdated check
  if [[ "$SECURITY_ONLY" == "false" ]] && command -v npm &>/dev/null; then
    local outdated_output
    outdated_output=$(npm outdated --json 2>/dev/null || true)
    if [[ -n "$outdated_output" && "$outdated_output" != "{}" ]]; then
      echo "$outdated_output" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    for name, info in d.items():
        current = info.get('current','?')
        latest = info.get('latest','?')
        if current == 'missing' or latest == 'missing': continue
        # Check major version diff
        try:
            cm = int(current.split('.')[0])
            lm = int(latest.split('.')[0])
            if cm != lm:
                print(f'MAJOR|{name}|{current}|{latest}')
            else:
                print(f'MINOR|{name}|{current}|{latest}')
        except:
            print(f'MINOR|{name}|{current}|{latest}')
except: pass
" 2>/dev/null | while IFS='|' read -r kind name current latest; do
        if [[ "$kind" == "MAJOR" ]]; then
          OUTDATED_MAJOR+=("$name|$current|$latest")
        else
          OUTDATED_MINOR+=("$name|$current|$latest")
        fi
      done
    fi
  fi
}

scan_python() {
  [[ -f requirements.txt || -f Pipfile.lock ]] && HAS_LOCKFILE=true

  # pip-audit
  if command -v pip-audit &>/dev/null; then
    local audit
    audit=$(pip-audit --format json 2>/dev/null || true)
    if [[ -n "$audit" ]]; then
      echo "$audit" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    for v in d.get('vulnerabilities',[]):
        print(f\"{v.get('severity','?')}|{v.get('package','?')}|{v.get('summary','')}\")
except: pass
" 2>/dev/null | while IFS='|' read -r sev name title; do
        VULNS+=("$sev|$name|$title")
      done
    fi
  fi

  # Outdated via pip list --outdated
  if [[ "$SECURITY_ONLY" == "false" ]] && command -v pip &>/dev/null; then
    pip list --outdated --format=json 2>/dev/null | python3 -c "
import sys, json
try:
    for pkg in json.load(sys.stdin):
        name = pkg.get('name','?')
        ver = pkg.get('version','?')
        latest = pkg.get('latest_version','?')
        try:
            cm = int(ver.split('.')[0])
            lm = int(latest.split('.')[0])
            if cm != lm: print(f'MAJOR|{name}|{ver}|{latest}')
            else: print(f'MINOR|{name}|{ver}|{latest}')
        except: print(f'MINOR|{name}|{ver}|{latest}')
except: pass
" 2>/dev/null | while IFS='|' read -r kind name current latest; do
      if [[ "$kind" == "MAJOR" ]]; then
        OUTDATED_MAJOR+=("$name|$current|$latest")
      else
        OUTDATED_MINOR+=("$name|$current|$latest")
      fi
    done
  fi
}

# ─── Run scan ────────────────────────────────────────
if [[ "$PROJECT_TYPE" == "node" ]]; then scan_node; else scan_python; fi

# ─── Calculate score ────────────────────────────────
VULN_COUNT=${#VULNS[@]}
MAJOR_COUNT=${#OUTDATED_MAJOR[@]}
MINOR_COUNT=${#OUTDATED_MINOR[@]}

SCORE=100
# Vulnerabilities: -15 each (high/critical), -5 each (low/moderate)
for v in "${VULNS[@]+"${VULNS[@]}"}"; do
  IFS='|' read -r sev _ _ <<< "$v"
  if [[ "$sev" == "high" || "$sev" == "critical" ]]; then
    (( SCORE -= 15 ))
  else
    (( SCORE -= 5 ))
  fi
done
# Major outdated: -5 each
(( SCORE -= MAJOR_COUNT * 5 ))
# Minor outdated: -2 each
(( SCORE -= MINOR_COUNT * 2 ))
# Lockfile bonus: +5 if missing
[[ "$HAS_LOCKFILE" == "false" ]] && (( SCORE -= 5 ))

(( SCORE < 0 )) && SCORE=0
(( SCORE > 100 )) && SCORE=100

# ─── Output ──────────────────────────────────────────
score_emoji() {
  if (( SCORE >= 80 )); then echo "✅"
  elif (( SCORE >= 60 )); then echo "⚠️"
  else echo "🔴"
  fi
}

if [[ "$FORMAT" == "json" ]]; then
  python3 -c "
import json
print(json.dumps({
    'project': '$PROJECT_DIR',
    'type': '$PROJECT_TYPE',
    'score': $SCORE,
    'vulnerabilities': $VULN_COUNT,
    'outdated_major': $MAJOR_COUNT,
    'outdated_minor': $MINOR_COUNT,
    'lockfile': $( $HAS_LOCKFILE && echo 'true' || echo 'false' )
}, indent=2))
"

elif [[ "$FORMAT" == "markdown" ]]; then
  echo "# dep-guard Report"
  echo ""
  echo "| Metric | Value |"
  echo "|--------|-------|"
  echo "| Project | \`${PROJECT_DIR}\` |"
  echo "| Type | ${PROJECT_TYPE} |"
  echo "| **Score** | **${SCORE}/100 $(score_emoji)** |"
  echo "| Vulnerabilities | ${VULN_COUNT} |"
  echo "| Outdated (major) | ${MAJOR_COUNT} |"
  echo "| Outdated (minor) | ${MINOR_COUNT} |"
  echo "| Lockfile | $( $HAS_LOCKFILE && echo '✓' || echo '✗' ) |"
  echo ""
  if (( VULN_COUNT > 0 )); then
    echo "## Vulnerabilities"
    for v in "${VULNS[@]+"${VULNS[@]}"}"; do
      IFS='|' read -r sev name title <<< "$v"
      echo "- **[${sev}]** ${name}: ${title}"
    done
    echo ""
  fi
  if (( MAJOR_COUNT > 0 )); then
    echo "## Outdated (Major)"
    for o in "${OUTDATED_MAJOR[@]+"${OUTDATED_MAJOR[@]}"}"; do
      IFS='|' read -r name cur lat <<< "$o"
      echo "- **${name}** ${cur} → ${lat}"
    done
    echo ""
  fi

else
  # Text (default)
  echo ""
  echo -e "${CYAN}╔══════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║${NC}  ${BOLD}dep-guard${NC} · Dependency Health Scan   ${CYAN}║${NC}"
  echo -e "${CYAN}╠══════════════════════════════════════╣${NC}"
  echo -e "${CYAN}║${NC}  Project: $(basename "$PROJECT_DIR")$(printf '%*s' $((26 - ${#PROJECT_DIR})) '')  ${CYAN}║${NC}"
  echo -e "${CYAN}║${NC}  Type:    ${PROJECT_TYPE}$(printf '%*s' $((27 - ${#PROJECT_TYPE})) '')  ${CYAN}║${NC}"
  printf "${CYAN}║${NC}  ${BOLD}Score:   ${SCORE}/100 $(score_emoji)${NC}\n"
  echo -e "${CYAN}╠══════════════════════════════════════╣${NC}"
  echo -e "${CYAN}║${NC}                                      ${CYAN}║${NC}"

  # Vulnerabilities
  if (( VULN_COUNT == 0 )); then
    echo -e "${CYAN}║${NC}  🔒 Security: ${GREEN}0 issues${NC}               ${CYAN}║${NC}"
  else
    echo -e "${CYAN}║${NC}  🔒 Security: ${RED}${VULN_COUNT} issue(s)${NC}           ${CYAN}║${NC}"
    for v in "${VULNS[@]+"${VULNS[@]}"}"; do
      IFS='|' read -r sev name title <<< "$v"
      echo -e "${CYAN}║${NC}    ${RED}[${sev}]${NC} ${name}: ${title:0:25}  ${CYAN}║${NC}"
    done
  fi

  # Outdated
  if [[ "$SECURITY_ONLY" == "false" ]]; then
    local total_out=$((MAJOR_COUNT + MINOR_COUNT))
    if (( total_out == 0 )); then
      echo -e "${CYAN}║${NC}  📦 Outdated: ${GREEN}0 packages${NC}           ${CYAN}║${NC}"
    else
      echo -e "${CYAN}║${NC}  📦 Outdated: ${YELLOW}${total_out} package(s)${NC}         ${CYAN}║${NC}"
      for o in "${OUTDATED_MAJOR[@]+"${OUTDATED_MAJOR[@]}"}"; do
        IFS='|' read -r name cur lat <<< "$o"
        echo -e "${CYAN}║${NC}    ${YELLOW}•${NC} ${name} ${cur} → ${lat} (major)  ${CYAN}║${NC}"
      done
      for o in "${OUTDATED_MINOR[@]+"${OUTDATED_MINOR[@]}"}"; do
        IFS='|' read -r name cur lat <<< "$o"
        echo -e "${CYAN}║${NC}    ${DIM}•${NC} ${name} ${cur} → ${lat}  ${CYAN}║${NC}"
      done
    fi
  fi

  # Lockfile
  if $HAS_LOCKFILE; then
    echo -e "${CYAN}║${NC}  🔐 Lockfile: ${GREEN}present ✓${NC}            ${CYAN}║${NC}"
  else
    echo -e "${CYAN}║${NC}  🔐 Lockfile: ${YELLOW}missing ✗${NC}           ${CYAN}║${NC}"
  fi

  echo -e "${CYAN}║${NC}                                      ${CYAN}║${NC}"
  echo -e "${CYAN}╚══════════════════════════════════════╝${NC}"
  echo ""
fi

# CI gate
if (( MIN_SCORE > 0 && SCORE < MIN_SCORE )); then
  echo "❌ Health score ${SCORE} is below threshold ${MIN_SCORE}"
  exit 1
fi
