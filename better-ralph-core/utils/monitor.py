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
