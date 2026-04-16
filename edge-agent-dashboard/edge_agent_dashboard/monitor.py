"""
Resource Monitor - 监控系统资源使用情况
"""

import asyncio
import psutil
from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel


class ResourceMetrics(BaseModel):
    """资源指标模型"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_total_mb: float
    network_sent_mb: float
    network_recv_mb: float
    disk_usage_percent: float
    load_average: Optional[float] = None


class ResourceMonitor:
    """资源监控器"""

    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self.current_metrics: Optional[ResourceMetrics] = None
        self.history: list = []
        self.max_history = 300  # 保留5分钟历史（每秒更新）
        self._network_counters = None
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """启动监控"""
        if self._running:
            return

        self._running = True
        self._network_counters = psutil.net_io_counters()
        self._task = asyncio.create_task(self._update_loop())

    async def stop(self):
        """停止监控"""
        if not self._running:
            return

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    async def _update_loop(self):
        """更新循环"""
        while self._running:
            await self._update_metrics()
            await asyncio.sleep(self.update_interval)

    async def _update_metrics(self):
        """更新资源指标"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=None)

            # 内存使用
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / (1024 * 1024)
            memory_total_mb = memory.total / (1024 * 1024)

            # 网络流量
            net_io = psutil.net_io_counters()
            network_sent_mb = (net_io.bytes_sent - self._network_counters.bytes_sent) / (1024 * 1024)
            network_recv_mb = (net_io.bytes_recv - self._network_counters.bytes_recv) / (1024 * 1024)
            self._network_counters = net_io

            # 磁盘使用
            disk = psutil.disk_usage('/')
            disk_usage_percent = disk.percent

            # 负载平均值（仅Unix）
            load_avg = None
            try:
                load_avg = psutil.getloadavg()[0]
            except (AttributeError, OSError):
                pass

            # 创建指标对象
            metrics = ResourceMetrics(
                timestamp=datetime.now().timestamp(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_used_mb=memory_used_mb,
                memory_total_mb=memory_total_mb,
                network_sent_mb=network_sent_mb,
                network_recv_mb=network_recv_mb,
                disk_usage_percent=disk_usage_percent,
                load_average=load_avg
            )

            self.current_metrics = metrics
            self.history.append(metrics)

            # 限制历史记录大小
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]

        except Exception as e:
            print(f"Error updating metrics: {e}")

    def get_current_metrics(self) -> Optional[ResourceMetrics]:
        """获取当前指标"""
        return self.current_metrics

    def get_history(self, seconds: int = 60) -> list:
        """获取历史数据"""
        now = datetime.now().timestamp()
        return [
            m for m in self.history
            if m.timestamp >= now - seconds
        ]

    def get_history_dict(self, seconds: int = 60) -> Dict[str, list]:
        """获取格式化的历史数据（用于图表）"""
        history = self.get_history(seconds)

        return {
            "timestamps": [m.timestamp * 1000 for m in history],  # 转换为毫秒
            "cpu": [m.cpu_percent for m in history],
            "memory": [m.memory_percent for m in history],
            "network_sent": [m.network_sent_mb for m in history],
            "network_recv": [m.network_recv_mb for m in history],
        }
