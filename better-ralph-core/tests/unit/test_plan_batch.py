"""Tests for plan_batch() dry-run batch planning."""
import pytest
from core.orchestrator import RalphOrchestrator
from core.prd_manager import PRDManager, UserStory


@pytest.fixture
def orchestrator_with_session(tmp_path):
    """Orchestrator with active session and 5 pending stories."""
    orch = RalphOrchestrator()
    prd = PRDManager()
    for i in range(5):
        prd.add_story(UserStory(
            id=f"S{i+1}",
            title=f"Story {i+1}",
            description=f"Desc {i+1}",
            acceptance_criteria=[f"AC{i+1}"],
            priority=i + 1,
            passes=False,
        ))
    prd_path = tmp_path / "prd.json"
    prd.save_prd(prd_path)
    orch.start_session(prd_path, tmp_path)
    return orch


class TestPlanBatch:
    def test_plan_within_budget(self, orchestrator_with_session):
        plan = orchestrator_with_session.plan_batch(max_iterations=3)
        assert plan["total_planned"] == 3
        assert plan["remaining_after_plan"] == 2
        assert plan["would_complete_all"] is False
        assert len(plan["planned_stories"]) == 3

    def test_plan_completes_all(self, orchestrator_with_session):
        plan = orchestrator_with_session.plan_batch(max_iterations=10)
        assert plan["total_planned"] == 5
        assert plan["remaining_after_plan"] == 0
        assert plan["would_complete_all"] is True

    def test_plan_story_order(self, orchestrator_with_session):
        plan = orchestrator_with_session.plan_batch(max_iterations=5)
        ids = [s["story_id"] for s in plan["planned_stories"]]
        assert ids == ["S1", "S2", "S3", "S4", "S5"]

    def test_plan_fields(self, orchestrator_with_session):
        plan = orchestrator_with_session.plan_batch(max_iterations=2)
        story = plan["planned_stories"][0]
        assert "step" in story
        assert "story_id" in story
        assert "title" in story
        assert "priority" in story
        assert story["step"] == 1

    def test_plan_no_session_raises(self):
        orch = RalphOrchestrator()
        with pytest.raises(ValueError, match="No active session"):
            orch.plan_batch()

    def test_plan_excludes_completed(self, orchestrator_with_session):
        orchestrator_with_session.prd_manager.mark_story_complete("S1")
        plan = orchestrator_with_session.plan_batch(max_iterations=10)
        ids = [s["story_id"] for s in plan["planned_stories"]]
        assert "S1" not in ids
        assert plan["total_planned"] == 4

    def test_plan_reflects_budget_and_threshold(self, orchestrator_with_session):
        plan = orchestrator_with_session.plan_batch(max_iterations=7, max_consecutive_failures=5)
        assert plan["budget"] == 7
        assert plan["failure_threshold"] == 5
