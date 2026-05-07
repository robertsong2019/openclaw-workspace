"""Tests for PerformanceMonitor reset, get_summary, get_active."""
import pytest
import time

from utils.monitor import PerformanceMonitor


class TestReset:
    def test_reset_clears_all(self):
        m = PerformanceMonitor()
        m.start("a")
        m.end("a")
        m.reset()
        assert m.get_metrics() == {}

    def test_reset_on_empty(self):
        m = PerformanceMonitor()
        m.reset()
        assert m.get_metrics() == {}


class TestGetSummary:
    def test_empty(self):
        m = PerformanceMonitor()
        assert m.get_summary() == {"completed": 0, "total_duration": 0.0, "average_duration": 0.0}

    def test_single_completed(self):
        m = PerformanceMonitor()
        m.start("x")
        time.sleep(0.01)
        m.end("x")
        s = m.get_summary()
        assert s["completed"] == 1
        assert s["total_duration"] >= 0.01
        assert s["average_duration"] >= 0.01

    def test_multiple_mixed(self):
        m = PerformanceMonitor()
        m.start("a")
        m.end("a")
        m.start("b")  # not ended
        s = m.get_summary()
        assert s["completed"] == 1
        assert "b" not in [k for k in m.get_metrics() if "duration" in m.get_metrics()[k]]

    def test_two_completed(self):
        m = PerformanceMonitor()
        m.start("a")
        m.end("a")
        m.start("b")
        m.end("b")
        s = m.get_summary()
        assert s["completed"] == 2


class TestGetActive:
    def test_none_active(self):
        m = PerformanceMonitor()
        m.start("a")
        m.end("a")
        assert m.get_active() == []

    def test_one_active(self):
        m = PerformanceMonitor()
        m.start("a")
        assert m.get_active() == ["a"]

    def test_mixed(self):
        m = PerformanceMonitor()
        m.start("a")
        m.end("a")
        m.start("b")
        m.start("c")
        active = m.get_active()
        assert set(active) == {"b", "c"}

    def test_all_active(self):
        m = PerformanceMonitor()
        m.start("x")
        m.start("y")
        assert set(m.get_active()) == {"x", "y"}
