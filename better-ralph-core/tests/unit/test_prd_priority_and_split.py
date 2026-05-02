"""
Tests for PRDManager.auto_adjust_priorities(), split_large_story(), and _calculate_dependency_depth.
"""
import pytest
from core.prd_manager import PRDManager, UserStory


@pytest.fixture
def manager():
    m = PRDManager()
    m.create_prd("test-project", "main", "Test project", stories=[])
    return m


def _story(sid, deps=None, priority=5, passes=False):
    return UserStory(
        id=sid,
        title=f"Story {sid}",
        description=f"Description for {sid}",
        acceptance_criteria=[f"AC1 for {sid}"],
        priority=priority,
        passes=passes,
        dependencies=deps or [],
    )


class TestAutoAdjustPriorities:
    """Tests for auto_adjust_priorities()."""

    def test_no_stories_no_error(self, manager):
        """auto_adjust on empty PRD should not raise."""
        manager.auto_adjust_priorities()

    def test_completed_stories_unchanged(self, manager):
        """Completed stories should not be reprioritized."""
        s = _story("s1", priority=3, passes=True)
        manager.add_story(s)
        manager.auto_adjust_priorities()
        assert manager.get_story_by_id("s1").priority == 3

    def test_incomplete_stories_get_priority_based_on_depth(self, manager):
        """Stories with deeper dependency chains should get lower priority numbers (higher priority)."""
        s1 = _story("s1", deps=[])
        s2 = _story("s2", deps=["s1"])
        s3 = _story("s3", deps=["s2"])
        for s in [s3, s2, s1]:
            manager.add_story(s)

        manager.auto_adjust_priorities()

        r1 = manager.get_story_by_id("s1")
        r2 = manager.get_story_by_id("s2")
        r3 = manager.get_story_by_id("s3")

        # s1 has depth 0, s2 depth 1, s3 depth 2
        # priority = 1 + min(depth, 5)
        assert r1.priority == 1  # depth=0
        assert r2.priority == 2  # depth=1
        assert r3.priority == 3  # depth=2

    def test_circular_dependency_handled(self, manager):
        """Circular dependencies should not cause infinite recursion."""
        s1 = _story("s1", deps=["s2"])
        s2 = _story("s2", deps=["s1"])
        manager.add_story(s1)
        manager.add_story(s2)
        # Should not hang
        manager.auto_adjust_priorities()
        # Both should get a valid priority
        assert isinstance(manager.get_story_by_id("s1").priority, int)
        assert isinstance(manager.get_story_by_id("s2").priority, int)

    def test_max_depth_capped_at_5(self, manager):
        """Priority bonus should be capped at depth 5."""
        stories = []
        for i in range(7):
            deps = [f"s{i-1}"] if i > 0 else []
            stories.append(_story(f"s{i}", deps=deps))
        for s in stories:
            manager.add_story(s)

        manager.auto_adjust_priorities()

        # s6 has depth 6, but capped to 5 → priority = 1 + 5 = 6
        assert manager.get_story_by_id("s6").priority == 6


class TestSplitLargeStory:
    """Tests for split_large_story()."""

    def test_split_nonexistent_story_returns_empty(self, manager):
        result = manager.split_large_story("nonexistent")
        assert result == []

    def test_split_story_creates_parts(self, manager):
        """Splitting a story with 5 criteria and max 2 creates 3 parts."""
        s = UserStory(
            id="big1",
            title="Big story",
            description="A big story",
            acceptance_criteria=["ac1", "ac2", "ac3", "ac4", "ac5"],
            priority=2,
            passes=False,
            estimated_hours=6.0,
        )
        manager.add_story(s)

        result = manager.split_large_story("big1", max_criteria=2)
        assert len(result) == 3
        # Original removed
        assert manager.get_story_by_id("big1") is None
        # Parts exist
        assert manager.get_story_by_id("big1-1") is not None
        assert manager.get_story_by_id("big1-2") is not None
        assert manager.get_story_by_id("big1-3") is not None

    def test_split_preserves_criteria_distribution(self, manager):
        """Criteria should be evenly distributed across parts."""
        s = UserStory(
            id="big2",
            title="Story",
            description="desc",
            acceptance_criteria=["a", "b", "c", "d"],
            priority=1,
            passes=False,
        )
        manager.add_story(s)
        result = manager.split_large_story("big2", max_criteria=3)

        all_criteria = []
        for part in result:
            all_criteria.extend(part.acceptance_criteria)
        assert all_criteria == ["a", "b", "c", "d"]

    def test_split_preserves_dependencies(self, manager):
        """Split parts should inherit original dependencies."""
        s = UserStory(
            id="big3",
            title="Story",
            description="desc",
            acceptance_criteria=["a", "b"],
            priority=1,
            passes=False,
            dependencies=["s0"],
        )
        manager.add_story(s)
        result = manager.split_large_story("big3", max_criteria=1)
        for part in result:
            assert "s0" in part.dependencies

    def test_split_divides_estimated_hours(self, manager):
        """estimated_hours should be divided among parts."""
        s = UserStory(
            id="big4",
            title="Story",
            description="desc",
            acceptance_criteria=["a", "b", "c"],
            priority=1,
            passes=False,
            estimated_hours=9.0,
        )
        manager.add_story(s)
        result = manager.split_large_story("big4", max_criteria=1)
        assert len(result) == 3
        for part in result:
            assert part.estimated_hours == pytest.approx(3.0)


class TestCalculateDependencyDepth:
    """Tests for _calculate_dependency_depth()."""

    def test_no_dependencies(self, manager):
        depth = manager._calculate_dependency_depth("s1", {"s1": []})
        assert depth == 0

    def test_single_chain(self, manager):
        graph = {"s3": ["s2"], "s2": ["s1"], "s1": []}
        assert manager._calculate_dependency_depth("s3", graph) == 2

    def test_diamond_dependency(self, manager):
        graph = {"s4": ["s2", "s3"], "s2": ["s1"], "s3": ["s1"], "s1": []}
        # s4 → s2 → s1 (depth 2), s4 → s3 → s1 (depth 2)
        assert manager._calculate_dependency_depth("s4", graph) == 2

    def test_missing_story_in_graph(self, manager):
        graph = {"s1": ["s_missing"]}
        # s_missing not in graph → treated as no deps
        depth = manager._calculate_dependency_depth("s1", graph)
        assert depth == 1  # s1 depends on s_missing which has depth 0
