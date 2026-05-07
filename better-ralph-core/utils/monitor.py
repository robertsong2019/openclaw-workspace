"""Monitor utility for Better Ralph Core tests"""
import time
from typing import Dict, Any


class PerformanceMonitor:
    """Simple performance monitor"""

    def __init__(self):
        self.metrics = {}

    def start(self, name: str) -> None:
        """Start timing a metric"""
        self.metrics[name] = {"start": time.time()}

    def end(self, name: str) -> float:
        """End timing a metric and return duration"""
        if name in self.metrics:
            duration = time.time() - self.metrics[name]["start"]
            self.metrics[name]["duration"] = duration
            return duration
        return 0.0

    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics"""
        return self.metrics

    def reset(self) -> None:
        """Clear all metrics."""
        self.metrics = {}

    def get_summary(self) -> Dict[str, Any]:
        """Get summary: completed count, total duration, avg duration."""
        completed = {k: v for k, v in self.metrics.items() if "duration" in v}
        total = sum(v["duration"] for v in completed.values())
        count = len(completed)
        return {
            "completed": count,
            "total_duration": total,
            "average_duration": total / count if count else 0.0,
        }

    def get_active(self) -> list:
        """Return names of started but not yet ended metrics."""
        return [k for k, v in self.metrics.items() if "duration" not in v]
