"""
Tests for project scanning: _detect_project_name, _scan_project_patterns, _detect_conventions.
Covers zero-coverage private methods in MemoryManager.
"""

import sys
from pathlib import Path
import importlib.util

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

spec = importlib.util.spec_from_file_location(
    "memory_manager",
    Path(__file__).parent.parent.parent / "core" / "memory_manager.py"
)
mm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mm)

MemoryManager = mm.MemoryManager


class TestDetectProjectName:
    """_detect_project_name from project root directory."""

    def test_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("{}")
        mgr = MemoryManager()
        assert mgr._detect_project_name(tmp_path) == "package"

    def test_pyproject_toml(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]")
        mgr = MemoryManager()
        assert mgr._detect_project_name(tmp_path) == "pyproject"

    def test_setup_py(self, tmp_path):
        (tmp_path / "setup.py").write_text("")
        mgr = MemoryManager()
        assert mgr._detect_project_name(tmp_path) == "setup"

    def test_cargo_toml(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text("")
        mgr = MemoryManager()
        assert mgr._detect_project_name(tmp_path) == "Cargo"

    def test_go_mod(self, tmp_path):
        (tmp_path / "go.mod").write_text("")
        mgr = MemoryManager()
        assert mgr._detect_project_name(tmp_path) == "go"

    def test_fallback_to_dirname(self, tmp_path):
        mgr = MemoryManager()
        assert mgr._detect_project_name(tmp_path) == tmp_path.name


class TestScanProjectPatterns:
    """_scan_project_patterns scans file extensions and detects conventions."""

    def test_scans_file_types(self, tmp_path):
        (tmp_path / "main.py").write_text("")
        (tmp_path / "utils.js").write_text("")
        (tmp_path / "readme.md").write_text("")
        mgr = MemoryManager()
        mgr.project_context = mm.ProjectContext(project_name="test", project_root=tmp_path)
        mgr._scan_project_patterns(tmp_path)
        assert ".py" in mgr.project_context.file_types
        assert ".js" in mgr.project_context.file_types
        assert ".md" in mgr.project_context.file_types

    def test_ignores_dotfiles(self, tmp_path):
        (tmp_path / ".hidden").write_text("")
        mgr = MemoryManager()
        mgr.project_context = mm.ProjectContext(project_name="test", project_root=tmp_path)
        mgr._scan_project_patterns(tmp_path)
        assert len(mgr.project_context.file_types) == 0

    def test_ignores_pyc_and_class(self, tmp_path):
        (tmp_path / "cache.pyc").write_text("")
        (tmp_path / "Main.class").write_text("")
        mgr = MemoryManager()
        mgr.project_context = mm.ProjectContext(project_name="test", project_root=tmp_path)
        mgr._scan_project_patterns(tmp_path)
        assert ".pyc" not in mgr.project_context.file_types
        assert ".class" not in mgr.project_context.file_types

    def test_counts_multiple_files_same_ext(self, tmp_path):
        (tmp_path / "a.py").write_text("")
        (tmp_path / "b.py").write_text("")
        (tmp_path / "c.py").write_text("")
        mgr = MemoryManager()
        mgr.project_context = mm.ProjectContext(project_name="test", project_root=tmp_path)
        mgr._scan_project_patterns(tmp_path)
        assert mgr.project_context.file_types[".py"] == 3


class TestDetectConventions:
    """_detect_conventions identifies common dirs and build files."""

    def test_detects_common_dirs(self, tmp_path):
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        (tmp_path / "docs").mkdir()
        mgr = MemoryManager()
        mgr.project_context = mm.ProjectContext(project_name="test", project_root=tmp_path)
        mgr._detect_conventions(tmp_path)
        assert "src" in mgr.project_context.conventions
        assert "tests" in mgr.project_context.conventions
        assert "docs" in mgr.project_context.conventions

    def test_detects_build_files(self, tmp_path):
        (tmp_path / "Makefile").write_text("")
        (tmp_path / "package.json").write_text("{}")
        mgr = MemoryManager()
        mgr.project_context = mm.ProjectContext(project_name="test", project_root=tmp_path)
        mgr._detect_conventions(tmp_path)
        assert mgr.project_context.conventions["Makefile"] == "build"
        assert mgr.project_context.conventions["package.json"] == "build"

    def test_empty_dir_no_conventions(self, tmp_path):
        mgr = MemoryManager()
        mgr.project_context = mm.ProjectContext(project_name="test", project_root=tmp_path)
        mgr._detect_conventions(tmp_path)
        assert mgr.project_context.conventions == {}

    def test_nonexistent_dir_no_crash(self, tmp_path):
        nonexistent = tmp_path / "nope"
        nonexistent.mkdir()
        mgr = MemoryManager()
        mgr.project_context = mm.ProjectContext(project_name="test", project_root=nonexistent)
        mgr._detect_conventions(nonexistent)
        assert mgr.project_context.conventions == {}
