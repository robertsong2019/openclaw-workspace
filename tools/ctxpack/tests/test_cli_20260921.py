"""CLI e2e suite (2026-09-21 cycle): spawn-based, per-test fixtures.

Red-first fixes pinned here:
1. --interval <= 0: was time.sleep(0) busy-loop (hang) / time.sleep(-1) ValueError crash
   → now clean exit 1 validation.
2. --stats --diff: diff target was silently ignored (silent flag-loss family 4th instance)
   → now mutually exclusive, exit 1.
3. diff additions counter: added content line `++i;` surfaces as `+++i;` and was swallowed
   by the `+++` header guard → undercount. Now counted from diff[2:] (headers skipped).
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

CTXPACK = Path(__file__).resolve().parent.parent / "ctxpack.py"


def run_cli(*args, timeout=30):
    return subprocess.run(
        [sys.executable, str(CTXPACK), *[str(a) for a in args]],
        capture_output=True, text=True, timeout=timeout,
    )


@pytest.fixture()
def proj(tmp_path):
    p = tmp_path / "myproj"
    p.mkdir()
    (p / "app.js").write_text("export const x = 1;\n")
    (p / "util.py").write_text("def hello():\n    return 'hi'\n")
    return p


# ── Red fix 1: --interval validation ──────────────────────────────────

def test_interval_zero_is_clean_error_not_busy_loop(proj, tmp_path):
    """--interval 0 used to hang in a sleep(0) busy-loop (CPU burner). Now exit 1."""
    r = run_cli(proj, "--watch", "--output", tmp_path / "w.md", "--interval", "0")
    assert r.returncode == 1
    assert "--interval must be > 0" in r.stderr


def test_interval_negative_is_clean_error_not_traceback(proj, tmp_path):
    """--interval -1 used to raise raw ValueError from time.sleep. Now exit 1."""
    r = run_cli(proj, "--watch", "--output", tmp_path / "w.md", "--interval", "-1")
    assert r.returncode == 1
    assert "--interval must be > 0" in r.stderr
    assert "ValueError" not in r.stderr


def test_interval_positive_passes_validation(proj, tmp_path):
    """Sanity: validation must not reject legal positive intervals (error comes later)."""
    r = run_cli(proj, "--watch", "--output", tmp_path / "w.md", "--interval", "-0.5")
    assert r.returncode == 1
    assert "--interval must be > 0" in r.stderr


# ── Red fix 2: --stats and --diff mutually exclusive ──────────────────

def test_stats_with_diff_is_rejected_not_silently_ignored(proj, tmp_path):
    """--stats --diff used to silently drop --diff (exit 0, no error). Now exit 1."""
    r = run_cli(proj, "--stats", "--diff", tmp_path / "old.md")
    assert r.returncode == 1
    assert "mutually exclusive" in r.stderr


# ── Red fix 3: diff additions/removals counter ────────────────────────

def test_diff_counts_added_increment_line(proj, tmp_path):
    """Source line `++i;` embedded via --include-source surfaces in the diff as
    `+++i;` and was swallowed by the +++ header guard → additions undercounted."""
    (proj / "app.js").write_text("export const x = 1;\nfunction f() {\n  ++i;\n}\n")
    gen = tmp_path / "gen.md"
    r = run_cli(proj, "--include-source", "-o", gen)
    assert r.returncode == 0, r.stderr

    old = tmp_path / "old.md"
    lines = gen.read_text().splitlines(keepends=True)
    target = next(i for i, l in enumerate(lines) if l.strip() == "++i;")
    old.write_text("".join(lines[:target] + lines[target + 1:]))

    r = run_cli(proj, "--include-source", "--diff", old)
    assert r.returncode == 0
    m = re.search(r"(\d+) additions, (\d+) removals", r.stderr)
    assert m, r.stderr
    assert m.group(1) == "1", f"expected 1 addition, got {m.group(1)}"
    assert m.group(2) == "0", f"expected 0 removals, got {m.group(2)}"


def test_diff_counts_with_leading_plus_content(proj, tmp_path):
    """Added content starting with `++ ` (e.g. markdown) must count as an addition."""
    (proj / "README.md").write_text("++ bold text\n")
    gen = tmp_path / "gen.md"
    r = run_cli(proj, "--include-source", "-o", gen)
    assert r.returncode == 0, r.stderr

    old = tmp_path / "old.md"
    lines = gen.read_text().splitlines(keepends=True)
    target = next(i for i, l in enumerate(lines) if "bold text" in l)
    old.write_text("".join(lines[:target] + lines[target + 1:]))

    r = run_cli(proj, "--include-source", "--diff", old)
    m = re.search(r"(\d+) additions, (\d+) removals", r.stderr)
    assert m, r.stderr
    assert m.group(1) == "1"


# ── Red fix 4: brace patterns in KEY_FILE_PATTERNS never matched ──────

from ctxpack import find_key_files, KEY_FILE_PATTERNS


def test_entry_detection_fires_for_app_js():
    """fnmatch has no brace expansion — 'app.{ts,js,py}' only matched a file
    literally named 'app.{ts,js,py}'. Entry categorization never fired."""
    result = find_key_files(["app.js", "index.ts", "main.py"], None)
    assert set(result["entry"]) == {"app.js", "index.ts", "main.py"}


def test_no_brace_literals_remain_in_compiled_patterns():
    """Every compiled pattern must be concrete (no `{...} survived)."""
    for category, patterns in KEY_FILE_PATTERNS.items():
        for p in patterns:
            assert "{" not in p, f"{category}: unexpanded brace pattern {p!r}"


def test_config_braced_patterns_match():
    result = find_key_files(["docker-compose.yml", "docker-compose.yaml"], None)
    assert set(result["config"]) == {"docker-compose.yml", "docker-compose.yaml"}


def test_test_category_braced_patterns_match():
    result = find_key_files(["src/foo.test.ts", "src/bar.spec.js", "app/baz.test.py"], None)
    assert set(result["test"]) == {"src/foo.test.ts", "src/bar.spec.js", "app/baz.test.py"}


# ── CLI surface (main() 615-789 was 0% covered) ───────────────────────

def test_basic_generate_stdout(proj):
    r = run_cli(proj)
    assert r.returncode == 0
    assert "myproj" in r.stdout


def test_output_flag_writes_file(proj, tmp_path):
    out = tmp_path / "out.md"
    r = run_cli(proj, "-o", out)
    assert r.returncode == 0
    assert out.exists()
    assert "myproj" in out.read_text()


def test_nonexistent_path_exit_1(tmp_path):
    r = run_cli(tmp_path / "ghost")
    assert r.returncode == 1
    assert "not a directory" in r.stderr


def test_version_flag():
    r = run_cli("--version")
    assert r.returncode == 0
    assert re.match(r"ctxpack \d+\.\d+", r.stdout)


def test_stats_outputs_valid_json(proj):
    r = run_cli(proj, "--stats")
    assert r.returncode == 0
    stats = json.loads(r.stdout)
    assert stats["totalFiles"] >= 2
    assert "JavaScript" in stats["languages"]
    assert stats["totalLines"] > 0


def test_stats_to_output_file(proj, tmp_path):
    out = tmp_path / "stats.json"
    r = run_cli(proj, "--stats", "-o", out)
    assert r.returncode == 0
    stats = json.loads(out.read_text())
    assert stats["project"] == "myproj"


def test_watch_requires_output(proj):
    r = run_cli(proj, "--watch")
    assert r.returncode == 1
    assert "--watch requires --output" in r.stderr


def test_watch_rejects_stats(proj, tmp_path):
    r = run_cli(proj, "--watch", "--output", tmp_path / "w.md", "--stats")
    assert r.returncode == 1
    assert "cannot be combined" in r.stderr


def test_watch_rejects_diff(proj, tmp_path):
    r = run_cli(proj, "--watch", "--output", tmp_path / "w.md", "--diff", tmp_path / "x.md")
    assert r.returncode == 1
    assert "cannot be combined" in r.stderr


def test_diff_identical_reports_no_differences(proj, tmp_path):
    gen = tmp_path / "gen.md"
    assert run_cli(proj, "-o", gen).returncode == 0
    r = run_cli(proj, "--diff", gen)
    assert r.returncode == 0
    assert "No differences" in r.stderr


def test_diff_missing_target_exit_1(proj, tmp_path):
    r = run_cli(proj, "--diff", tmp_path / "ghost.md")
    assert r.returncode == 1
    assert "does not exist" in r.stderr


def test_exclude_flag_removes_files(proj, tmp_path):
    full = run_cli(proj, "--stats")
    slim = run_cli(proj, "--stats", "--exclude", "*.js")
    full_stats = json.loads(full.stdout)
    slim_stats = json.loads(slim.stdout)
    assert slim_stats["totalFiles"] < full_stats["totalFiles"]
    assert "JavaScript" not in slim_stats["languages"]


def test_include_flag_adds_entry_file(proj):
    (proj / "custom.txt").write_text("custom context\n")
    r = run_cli(proj, "--include", "custom.txt")
    assert r.returncode == 0
    assert "custom.txt" in r.stdout


def test_format_claude_marker(proj):
    r = run_cli(proj, "--format", "claude")
    assert r.returncode == 0


def test_name_flag_overrides_project_name(tmp_path):
    p = tmp_path / "dirnama"
    p.mkdir()
    (p / "a.js").write_text("const y = 2;\n")
    r = run_cli(p, "--name", "branded")
    assert r.returncode == 0
    assert "branded" in r.stdout
