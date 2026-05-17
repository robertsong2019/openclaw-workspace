"""
Extended tests for MemoryManager — search, clear, error rate, project detection.
"""

import pytest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import importlib.util
spec = importlib.util.spec_from_file_location(
    "memory_manager",
    Path(__file__).parent.parent.parent / "core" / "memory_manager.py"
)
mm_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mm_mod)

MemoryManager = mm_mod.MemoryManager
IterationContext = mm_mod.IterationContext
ProjectContext = mm_mod.ProjectContext


class TestSearchIterations:
    """Tests for search_iterations method."""

    @pytest.fixture
    def mm(self, tmp_path):
        m = MemoryManager(memory_dir=tmp_path)
        # Add varied iterations
        m.add_iteration_result("s1", "Auth Login", [], ["l1"], ["p1"], [], {"d": 1})
        m.add_iteration_result("s2", "API Error", [], [], [], ["timeout"], {"d": 2})
        m.add_iteration_result("s1", "Auth Refresh", ["auth.py"], ["l2"], ["p2"], [], {"d": 3})
        m.add_iteration_result("s3", "DB Timeout", [], [], [], ["connection refused"], {"d": 4})
        return m

    def test_search_by_story_id(self, mm):
        results = mm.search_iterations(story_id="s1")
        assert len(results) == 2
        assert all(r.story_id == "s1" for r in results)

    def test_search_has_errors_true(self, mm):
        results = mm.search_iterations(has_errors=True)
        assert len(results) == 2
        assert all(r.errors for r in results)

    def test_search_has_errors_false(self, mm):
        results = mm.search_iterations(has_errors=False)
        assert len(results) == 2
        assert all(not r.errors for r in results)

    def test_search_by_keyword_in_title(self, mm):
        results = mm.search_iterations(query="auth")
        assert len(results) == 2  # "Auth Login" and "Auth Refresh"

    def test_search_by_keyword_in_errors(self, mm):
        results = mm.search_iterations(query="timeout")
        assert len(results) == 2  # "API Error" has timeout, "DB Timeout" title

    def test_search_combined_filters(self, mm):
        results = mm.search_iterations(story_id="s1", has_errors=False)
        assert len(results) == 2

    def test_search_no_match(self, mm):
        results = mm.search_iterations(query="nonexistent_xyz")
        assert results == []

    def test_search_empty_query(self, mm):
        results = mm.search_iterations(query="")
        assert len(results) == 4


class TestClearIterations:
    """Tests for clear_iterations method."""

    def test_clear_returns_count(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path)
        mm.add_iteration_result("s1", "T1", [], [], [], [], {})
        mm.add_iteration_result("s2", "T2", [], [], [], [], {})
        count = mm.clear_iterations()
        assert count == 2
        assert len(mm.iterations) == 0

    def test_clear_persists(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path)
        mm.add_iteration_result("s1", "T1", [], [], [], [], {})
        mm.clear_iterations()
        mm2 = MemoryManager(memory_dir=tmp_path)
        assert len(mm2.iterations) == 0

    def test_clear_empty(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path)
        assert mm.clear_iterations() == 0


class TestUniqueStoryIds:
    """Tests for get_unique_story_ids method."""

    def test_unique_ids_sorted(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path)
        mm.add_iteration_result("s3", "T3", [], [], [], [], {})
        mm.add_iteration_result("s1", "T1", [], [], [], [], {})
        mm.add_iteration_result("s2", "T2", [], [], [], [], {})
        mm.add_iteration_result("s1", "T1b", [], [], [], [], {})
        ids = mm.get_unique_story_ids()
        assert ids == ["s1", "s2", "s3"]

    def test_empty(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path)
        assert mm.get_unique_story_ids() == []


class TestErrorRate:
    """Tests for get_error_rate method."""

    def test_no_iterations(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path)
        assert mm.get_error_rate() == 0.0

    def test_all_success(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path)
        mm.add_iteration_result("s1", "T1", [], [], [], [], {})
        mm.add_iteration_result("s2", "T2", [], [], [], [], {})
        assert mm.get_error_rate() == 0.0

    def test_half_errors(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path)
        mm.add_iteration_result("s1", "T1", [], [], [], [], {})
        mm.add_iteration_result("s2", "T2", [], [], [], ["err"], {})
        assert mm.get_error_rate() == 0.5

    def test_all_errors(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path)
        mm.add_iteration_result("s1", "T1", [], [], [], ["e1"], {})
        assert mm.get_error_rate() == 1.0


class TestGetIterationContext:
    """Tests for get_iteration_context with a story object."""

    def test_returns_context_dict(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path)

        class FakeStory:
            id = "s1"
            title = "Test"
            description = "desc"
            acceptance_criteria = ["ac1"]

        ctx = mm.get_iteration_context(FakeStory())
        assert ctx["story"]["id"] == "s1"
        assert ctx["story"]["title"] == "Test"
        assert "project" in ctx
        assert "memory" in ctx
        assert "patterns" in ctx


class TestDetectProjectName:
    """Tests for _detect_project_name with config files."""

    def test_from_package_json(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path / "mem")
        proj = tmp_path / "myproj"
        proj.mkdir()
        (proj / "package.json").write_text('{"name": "cool-project"}')
        assert mm._detect_project_name(proj) == "cool-project"

    def test_from_pyproject_toml(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path / "mem2")
        proj = tmp_path / "myproj2"
        proj.mkdir()
        (proj / "pyproject.toml").write_text('[project]\nname = "py-proj"\n')
        assert mm._detect_project_name(proj) == "py-proj"

    def test_fallback_to_dirname(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path / "mem3")
        proj = tmp_path / "fallback-name"
        proj.mkdir()
        assert mm._detect_project_name(proj) == "fallback-name"


class TestUpdatePatternsLimit:
    """Test that _update_patterns respects the 100-item limit."""

    def test_patterns_truncated_at_100(self, tmp_path):
        mm = MemoryManager(memory_dir=tmp_path)
        # Add 110 patterns
        mm.add_iteration_result(
            "s1", "T1", [],
            [f"learning-{i}" for i in range(110)],
            [f"pattern-{i}" for i in range(110)],
            [], {}
        )
        assert len(mm.patterns["code_patterns"]) == 100
        assert len(mm.patterns["common_patterns"]) == 100
        # Last 100 kept
        assert mm.patterns["code_patterns"][0] == "pattern-10"
        assert mm.patterns["common_patterns"][0] == "learning-10"
