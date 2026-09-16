#!/usr/bin/env bats
# F27: stats — JSON 转义 + latest 递归一致性（red-verified ×2）+ characterization。
#
# Bug 1: stats --json 的 latest_note 未过 esc_json（hot 的 terms 都转义了），
#        文件名含引号/反斜杠即打穿 JSON —— 显示层伪影家族。
# Bug 2: memory_files 计数用 find 递归，latest 却只 glob 顶层 —— 同一命令
#        两套文件集定义，子目录最新笔记永远当不了 latest_note。

setup() {
  local test_dir
  test_dir="$(cd "$(dirname "$BATS_TEST_FILENAME")" && pwd)"
  source "$test_dir/setup_fixture.sh"
  setup
  AGENT_LOG="$test_dir/../agent-log.sh"
  JSON_FIELD="$test_dir/json_field.py"
  export AGENT_LOG JSON_FIELD
  OUT="$BATS_TMPDIR/f27-out.json"
  export OUT
  # 固定 mtime：D2 < D1 < D0，保证 latest 判定确定
  touch -d "$FIX_D2 10:00:00" "$MEMORY_DIR/$FIX_D2.md"
  touch -d "$FIX_D1 10:00:00" "$MEMORY_DIR/$FIX_D1.md"
  touch -d "$FIX_D0 10:00:00" "$MEMORY_DIR/$FIX_D0.md"
  SESS="$FAKEHOME/.openclaw/sessions"
  printf 'alpha\n' > "$SESS/20260901-alpha.md"
  printf 'beta\n'  > "$SESS/20260902-beta.md"
}

teardown() { teardown; }

stats_json() {
  run "$AGENT_LOG" stats --json
  [ "$status" -eq 0 ]
  printf '%s' "$output" > "$OUT"
}

# ── Bug 1: JSON 转义 ──

@test "F27: stats --json escapes quotes in latest_note (valid JSON)" {
  local weird='2026-01-01 weird "quote".md'
  printf 'naughty\n' > "$MEMORY_DIR/$weird"
  touch -d "$FIX_D0 12:00:00" "$MEMORY_DIR/$weird"
  stats_json
  run python3 "$JSON_FIELD" "$OUT" latest_note
  [ "$status" -eq 0 ]
  [ "$output" = "$weird" ]
}

@test "F27: stats --json escapes backslash in latest_note" {
  local weird='2026-01-01 back\slash.md'
  printf 'x\n' > "$MEMORY_DIR/$weird"
  touch -d "$FIX_D0 12:00:00" "$MEMORY_DIR/$weird"
  stats_json
  run python3 "$JSON_FIELD" "$OUT" latest_note
  [ "$status" -eq 0 ]
  [ "$output" = "$weird" ]
}

# ── Bug 2: latest 必须与递归计数同一文件集 ──

@test "F27: latest_note considers subdirectory notes (recursive like the count)" {
  mkdir -p "$MEMORY_DIR/sub"
  printf 'deep\n' > "$MEMORY_DIR/sub/2026-02-02-sub.md"
  touch -d "$FIX_D0 12:00:00" "$MEMORY_DIR/sub/2026-02-02-sub.md"
  stats_json
  run python3 "$JSON_FIELD" "$OUT" latest_note
  [ "$status" -eq 0 ]
  [ "$output" = "2026-02-02-sub.md" ]
  run python3 "$JSON_FIELD" "$OUT" memory_files
  [ "$output" = "4" ]   # D2/D1/D0 + sub
}

# ── characterization ──

@test "F27: stats --json shape with flat fixture" {
  stats_json
  run python3 "$JSON_FIELD" "$OUT" memory_files
  [ "$output" = "3" ]
  run python3 "$JSON_FIELD" "$OUT" session_files
  [ "$output" = "2" ]
  run python3 "$JSON_FIELD" "$OUT" latest_note
  [ "$output" = "$FIX_D0.md" ]   # 最新的顶层笔记
}

@test "F27: stats --md renders table with counts" {
  run "$AGENT_LOG" stats --md
  [ "$status" -eq 0 ]
  [[ "$output" == *"| Memory files | 3 |"* ]]
  [[ "$output" == *"| Session files | 2 |"* ]]
  [[ "$output" == *"| Latest note | $FIX_D0.md |"* ]]
}

@test "F27: stats --json on empty workspace degrades cleanly" {
  rm -f "$MEMORY_DIR"/*.md
  stats_json
  run python3 "$JSON_FIELD" "$OUT" memory_files
  [ "$output" = "0" ]
  run python3 "$JSON_FIELD" "$OUT" latest_note
  [ "$output" = "" ]
}
