#!/usr/bin/env python3
"""Hermetic test suite for Project Dashboard Generator.

All fixtures are built in a tmp directory (real git init/commit), so the
suite never depends on the layout of the surrounding workspace monorepo.
Run: python3 -m pytest tests/ -q
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "project_dashboard.py"
GIT_ENV = {
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
    **__import__("os").environ,
}


def run_dashboard(*args):
    """Run dashboard CLI with args, return (code, stdout, stderr)."""
    cmd = [sys.executable, str(SCRIPT)] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return result.returncode, result.stdout, result.stderr


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, env=GIT_ENV, check=True,
                   capture_output=True, timeout=30)


@pytest.fixture()
def ws(tmp_path):
    """A hermetic workspace with 5 fixture projects."""
    # 1. healthy-proj: git clean + README/CHANGELOG/CONTRIBUTING + tests/ → score ~100
    p = tmp_path / "healthy-proj"
    (p / "tests").mkdir(parents=True)
    (p / "src").mkdir()
    (p / "README.md").write_text("# healthy\n")
    (p / "CHANGELOG.md").write_text("# changelog\n")
    (p / "CONTRIBUTING.md").write_text("# contributing\n")
    (p / "tests" / "test_main.py").write_text("def test_ok():\n    assert True\n")
    (p / "src" / "main.py").write_text("print('hi')\n")
    git(p, "init", "-q")
    git(p, "add", "-A")
    git(p, "commit", "-qm", "init")

    # 2. dirty-proj: jest config + README, tracked file modified after commit → dirty
    p = tmp_path / "dirty-proj"
    p.mkdir()
    (p / "package.json").write_text('{"name":"dirty"}\n')
    (p / "jest.config.js").write_text("module.exports = {};\n")
    (p / "README.md").write_text("# dirty\n// TODO: fix this later\n")
    git(p, "init", "-q")
    git(p, "add", "-A")
    git(p, "commit", "-qm", "init")
    (p / "README.md").write_text("# dirty edited\n// TODO: fix this later\n")

    # 3. plain-py: packaging-only pyproject.toml, NO test evidence → has_tests must be False
    p = tmp_path / "plain-py"
    p.mkdir()
    (p / "pyproject.toml").write_text("[build-system]\nrequires = [\"setuptools\"]\n")
    (p / "app.py").write_text("print('no tests here')\n")

    # 4. go-proj: go.mod + real *_test.go → has_tests=True, framework=go
    p = tmp_path / "go-proj"
    (p / "pkg").mkdir(parents=True)
    (p / "go.mod").write_text("module example.com/go-proj\n\ngo 1.21\n")
    (p / "main.go").write_text("package main\nfunc main() {}\n")
    (p / "pkg" / "math.go").write_text("package pkg\nfunc Add(a, b int) int { return a + b }\n")
    (p / "pkg" / "math_test.go").write_text("package pkg\nimport \"testing\"\nfunc TestAdd(t *testing.T) {}\n")

    # 5. cargo-bare: Cargo.toml but no tests dir → has_tests must be False
    p = tmp_path / "cargo-bare"
    (p / "src").mkdir(parents=True)
    (p / "Cargo.toml").write_text("[package]\nname = \"x\"\nversion = \"0.1.0\"\n")
    (p / "src" / "main.rs").write_text("fn main() {}\n")

    # noise: not-a-project (no indicators) and hidden dir must be excluded
    (tmp_path / "not-a-project").mkdir()
    (tmp_path / "not-a-project" / "notes.txt").write_text("hi\n")
    (tmp_path / ".hidden").mkdir()
    (tmp_path / ".hidden" / "package.json").write_text("{}\n")

    return tmp_path


def scan_json(ws):
    code, out, err = run_dashboard(str(ws), "-f", "json")
    assert code == 0, f"exit {code}: {err}"
    return json.loads(out)


def test_basic_scan_and_markdown(ws):
    code, out, err = run_dashboard(str(ws))
    assert code == 0, err
    assert "# 📊 Project Dashboard" in out
    for name in ("healthy-proj", "dirty-proj", "plain-py", "go-proj", "cargo-bare"):
        assert name in out, f"{name} missing from markdown"
    assert "not-a-project" not in out
    assert "hidden" not in out


def test_json_output_and_sorting(ws):
    data = scan_json(ws)
    assert set(data["summary"]) >= {"total_projects", "total_files", "avg_health_score",
                                    "with_tests", "with_docs"}
    names = [p["name"] for p in data["projects"]]
    assert set(names) == {"healthy-proj", "dirty-proj", "plain-py", "go-proj", "cargo-bare"}
    scores = [p["health_score"] for p in data["projects"]]
    assert scores == sorted(scores, reverse=True), "projects must be sorted by health desc"


def test_healthy_project_scores_high(ws):
    data = scan_json(ws)
    by = {p["name"]: p for p in data["projects"]}
    assert by["healthy-proj"]["git_status"] == "clean"
    assert by["healthy-proj"]["has_tests"] is True
    assert "README.md" in by["healthy-proj"]["doc_files"]
    assert by["healthy-proj"]["health_score"] >= 90


def test_dirty_project_detected(ws):
    data = scan_json(ws)
    by = {p["name"]: p for p in data["projects"]}
    assert by["dirty-proj"]["git_status"] == "dirty"
    assert by["dirty-proj"]["has_tests"] is True
    assert by["dirty-proj"]["test_framework"] == "jest"
    assert by["dirty-proj"]["todo_count"] >= 1


def test_pyproject_without_pytest_is_not_tested(ws):
    """Regression: packaging-only pyproject.toml must not award has_tests."""
    data = scan_json(ws)
    by = {p["name"]: p for p in data["projects"]}
    assert by["plain-py"]["has_tests"] is False
    assert by["plain-py"]["test_framework"] == ""


def test_cargo_without_tests_dir_is_not_tested(ws):
    """Regression: bare Cargo.toml must not award has_tests."""
    data = scan_json(ws)
    by = {p["name"]: p for p in data["projects"]}
    assert by["cargo-bare"]["has_tests"] is False


def test_go_real_test_file_detected(ws):
    data = scan_json(ws)
    by = {p["name"]: p for p in data["projects"]}
    assert by["go-proj"]["has_tests"] is True
    assert by["go-proj"]["test_framework"] == "go"


def test_min_health_filter(ws):
    data = scan_json(ws)
    cutoff = min(p["health_score"] for p in data["projects"]) + 1
    code, out, err = run_dashboard(str(ws), "-f", "json", "--min-health", str(cutoff))
    assert code == 0, err
    filtered = json.loads(out)["projects"]
    assert filtered, "cutoff too aggressive for this fixture"
    assert all(p["health_score"] >= cutoff for p in filtered)


def test_file_output(ws, tmp_path_factory):
    out_file = ws.parent / "dash.md"
    code, out, err = run_dashboard(str(ws), "-o", str(out_file))
    assert code == 0, err
    content = out_file.read_text()
    assert "# 📊 Project Dashboard" in content
    assert "healthy-proj" in content


def test_missing_workspace_errors_gracefully(tmp_path):
    code, out, err = run_dashboard(str(tmp_path / "nope"))
    assert code == 1
    assert "not found" in err.lower()
    assert "Traceback" not in err, "must not crash with a traceback"


def test_staged_rename_is_dirty(tmp_path):
    """Regression: porcelain 'R ' (staged rename) is a tracked change → dirty.
    Old code checked only M/A/D chars, so renames scored +10 as 'untracked'."""
    p = tmp_path / "rename-proj"
    p.mkdir()
    (p / "package.json").write_text('{"name":"r"}\n')
    (p / "old.py").write_text("print(1)\n")
    git(p, "init", "-q")
    git(p, "add", "-A")
    git(p, "commit", "-qm", "init")
    git(p, "mv", "old.py", "new.py")
    by = {pr["name"]: pr for pr in scan_json(tmp_path)["projects"]}
    assert by["rename-proj"]["git_status"] == "dirty"


def test_merge_conflict_is_dirty(tmp_path):
    """Regression: porcelain 'UU' (unresolved merge conflict) is worse than
    dirty and must not be reported as 'untracked' (+10 score inflation)."""
    p = tmp_path / "conflict-proj"
    p.mkdir()
    (p / "package.json").write_text('{"name":"c"}\n')
    (p / "f.txt").write_text("base\n")
    git(p, "init", "-q")
    git(p, "add", "-A")
    git(p, "commit", "-qm", "base")
    git(p, "checkout", "-q", "-b", "side")
    (p / "f.txt").write_text("side\n")
    git(p, "commit", "-aqm", "side")
    git(p, "checkout", "-q", "master")
    (p / "f.txt").write_text("main\n")
    git(p, "commit", "-aqm", "main")
    # merge conflicts on purpose; rc=1 is the expected outcome, not an error
    subprocess.run(["git", "merge", "side"], cwd=p, env=GIT_ENV,
                   capture_output=True, timeout=30)
    by = {pr["name"]: pr for pr in scan_json(tmp_path)["projects"]}
    assert by["conflict-proj"]["git_status"] == "dirty"


def test_untracked_only_is_untracked(tmp_path):
    """Legality pin: a pure-untracked state (?? only, no tracked changes)
    must stay 'untracked' — guards the dirty-classification chokepoint
    against over-tightening."""
    p = tmp_path / "untracked-proj"
    p.mkdir()
    (p / "package.json").write_text('{"name":"u"}\n')
    git(p, "init", "-q")
    git(p, "add", "-A")
    git(p, "commit", "-qm", "init")
    (p / "stray.txt").write_text("untracked\n")
    by = {pr["name"]: pr for pr in scan_json(tmp_path)["projects"]}
    assert by["untracked-proj"]["git_status"] == "untracked"


def test_equal_score_sorted_by_name(tmp_path):
    """Regression: equal health scores must tiebreak by name — filesystem
    iteration order is not a contract (dashboard output was nondeterministic)."""
    for name in ("zzz-proj", "aaa-proj"):  # created in reverse-alpha order
        p = tmp_path / name
        p.mkdir()
        (p / "app.py").write_text("print(1)\n")
        (p / "pyproject.toml").write_text('[build-system]\nrequires = ["setuptools"]\n')
    code, out, err = run_dashboard(str(tmp_path), "-f", "json")
    assert code == 0, err
    names = [pr["name"] for pr in json.loads(out)["projects"]]
    assert names == ["aaa-proj", "zzz-proj"]


def test_health_score_bounds(ws):
    for p in scan_json(ws)["projects"]:
        assert 0 <= p["health_score"] <= 100, f"{p['name']}: {p['health_score']}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
