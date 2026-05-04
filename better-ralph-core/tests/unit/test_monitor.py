"""Tests for utils/monitor.py PerformanceMonitor"""
import time
import pytest
from utils.monitor import PerformanceMonitor


class TestPerformanceMonitor:
    def test_start_creates_metric(self):
        m = PerformanceMonitor()
        m.start("foo")
        assert "foo" in m.metrics
        assert "start" in m.metrics["foo"]

    def test_end_returns_duration(self):
        m = PerformanceMonitor()
        m.start("foo")
        time.sleep(0.05)
        dur = m.end("foo")
        assert dur >= 0.04
        assert m.metrics["foo"]["duration"] == dur

    def test_end_unknown_returns_zero(self):
        m = PerformanceMonitor()
        assert m.end("nonexistent") == 0.0

    def test_get_metrics(self):
        m = PerformanceMonitor()
        m.start("a")
        m.start("b")
        m.end("a")
        metrics = m.get_metrics()
        assert "a" in metrics
        assert "b" in metrics
        assert "duration" in metrics["a"]
        assert "duration" not in metrics["b"]  # b not ended yet
