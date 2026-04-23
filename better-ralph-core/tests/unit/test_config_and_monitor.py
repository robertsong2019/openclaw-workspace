"""
Tests for Config and PerformanceMonitor utility classes.
"""

import pytest
import time
from pathlib import Path

from utils.config import Config
from utils.monitor import PerformanceMonitor


class TestConfig:
    """Tests for Config class."""

    def test_default_empty_config(self):
        config = Config()
        assert config.config == {}

    def test_get_existing_key(self):
        config = Config({"key1": "value1", "key2": 42})
        assert config.get("key1") == "value1"
        assert config.get("key2") == 42

    def test_get_missing_key_returns_default(self):
        config = Config()
        assert config.get("nonexistent") is None
        assert config.get("nonexistent", "fallback") == "fallback"

    def test_set_key(self):
        config = Config()
        config.set("foo", "bar")
        assert config.get("foo") == "bar"

    def test_overwrite_key(self):
        config = Config({"key": "old"})
        config.set("key", "new")
        assert config.get("key") == "new"

    def test_load_from_file_returns_empty(self):
        """Config.load_from_file is a stub returning empty config."""
        config = Config.load_from_file(Path("/nonexistent"))
        assert config.config == {}

    def test_nested_values(self):
        config = Config({"nested": {"deep": {"val": True}}})
        assert config.get("nested") == {"deep": {"val": True}}


class TestPerformanceMonitor:
    """Tests for PerformanceMonitor class."""

    def test_initial_metrics_empty(self):
        monitor = PerformanceMonitor()
        assert monitor.metrics == {}

    def test_start_creates_metric(self):
        monitor = PerformanceMonitor()
        monitor.start("test_op")
        assert "test_op" in monitor.metrics
        assert "start" in monitor.metrics["test_op"]

    def test_end_returns_duration(self):
        monitor = PerformanceMonitor()
        monitor.start("test_op")
        duration = monitor.end("test_op")
        assert duration >= 0
        assert "duration" in monitor.metrics["test_op"]

    def test_end_nonexistent_returns_zero(self):
        monitor = PerformanceMonitor()
        duration = monitor.end("nonexistent")
        assert duration == 0.0

    def test_get_metrics(self):
        monitor = PerformanceMonitor()
        monitor.start("op1")
        monitor.end("op1")
        metrics = monitor.get_metrics()
        assert "op1" in metrics
        assert "duration" in metrics["op1"]

    def test_multiple_metrics(self):
        monitor = PerformanceMonitor()
        monitor.start("a")
        monitor.start("b")
        monitor.end("a")
        monitor.end("b")
        metrics = monitor.get_metrics()
        assert len(metrics) == 2

    def test_duration_is_positive(self):
        monitor = PerformanceMonitor()
        monitor.start("timed")
        time.sleep(0.01)
        duration = monitor.end("timed")
        assert duration >= 0.01
