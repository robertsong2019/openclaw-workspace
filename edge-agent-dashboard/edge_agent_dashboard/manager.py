"""
Agent Manager - 管理所有Edge Agent的生命周期
"""

import asyncio
import json
import subprocess
import os
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime
import aiofiles
from pydantic import BaseModel


class AgentState(str, Enum):
    """Agent状态枚举"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


class AgentConfig(BaseModel):
    """Agent配置模型"""
    id: str
    name: str
    command: str
    working_dir: Optional[str] = None
    env_vars: Optional[Dict[str, str]] = None
    auto_start: bool = False


class AgentInfo(BaseModel):
    """Agent信息模型"""
    id: str
    name: str
    state: AgentState
    pid: Optional[int] = None
    uptime: Optional[float] = None
    last_error: Optional[str] = None
    config: AgentConfig


class AgentManager:
    """Agent管理器"""

    def __init__(self, config_dir: str = "./agents"):
        self.config_dir = config_dir
        self.agents: Dict[str, AgentInfo] = {}
        self.processes: Dict[str, asyncio.subprocess.Process] = {}
        self.log_buffers: Dict[str, List[str]] = {}
        self._ensure_config_dir()
        self._load_agents()

    def _ensure_config_dir(self):
        """确保配置目录存在"""
        os.makedirs(self.config_dir, exist_ok=True)

    def _load_agents(self):
        """加载所有Agent配置"""
        if not os.path.exists(self.config_dir):
            return

        for filename in os.listdir(self.config_dir):
            if filename.endswith(".json"):
                agent_id = filename[:-5]
                config_path = os.path.join(self.config_dir, filename)
                self._load_agent_config(agent_id, config_path)

    def _load_agent_config(self, agent_id: str, config_path: str):
        """加载单个Agent配置"""
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)

            config = AgentConfig(**config_data)
            agent = AgentInfo(
                id=agent_id,
                name=config.name,
                state=AgentState.STOPPED,
                config=config
            )
            self.agents[agent_id] = agent
            self.log_buffers[agent_id] = []
        except Exception as e:
            print(f"Failed to load agent {agent_id}: {e}")

    async def get_agents(self) -> List[AgentInfo]:
        """获取所有Agent信息"""
        return list(self.agents.values())

    async def get_agent(self, agent_id: str) -> Optional[AgentInfo]:
        """获取单个Agent信息"""
        return self.agents.get(agent_id)

    async def start_agent(self, agent_id: str) -> bool:
        """启动Agent"""
        if agent_id not in self.agents:
            return False

        agent = self.agents[agent_id]
        if agent.state in [AgentState.RUNNING, AgentState.STARTING]:
            return True

        agent.state = AgentState.STARTING
        agent.last_error = None

        try:
            env = os.environ.copy()
            if agent.config.env_vars:
                env.update(agent.config.env_vars)

            process = await asyncio.create_subprocess_shell(
                agent.config.command,
                cwd=agent.config.working_dir,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            self.processes[agent_id] = process
            agent.pid = process.pid
            agent.state = AgentState.RUNNING
            agent.uptime = datetime.now().timestamp()

            # 启动日志收集
            asyncio.create_task(self._collect_logs(agent_id, process))

            return True

        except Exception as e:
            agent.state = AgentState.ERROR
            agent.last_error = str(e)
            return False

    async def stop_agent(self, agent_id: str) -> bool:
        """停止Agent"""
        if agent_id not in self.agents:
            return False

        agent = self.agents[agent_id]
        if agent.state not in [AgentState.RUNNING, AgentState.ERROR]:
            return True

        agent.state = AgentState.STOPPING

        if agent_id in self.processes:
            process = self.processes[agent_id]
            try:
                process.terminate()
                await asyncio.wait_for(process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
            except Exception as e:
                print(f"Error stopping agent {agent_id}: {e}")

            del self.processes[agent_id]

        agent.state = AgentState.STOPPED
        agent.pid = None
        agent.uptime = None

        return True

    async def restart_agent(self, agent_id: str) -> bool:
        """重启Agent"""
        await self.stop_agent(agent_id)
        await asyncio.sleep(1)
        return await self.start_agent(agent_id)

    async def delete_agent(self, agent_id: str) -> bool:
        """删除Agent"""
        if agent_id not in self.agents:
            return False

        await self.stop_agent(agent_id)
        del self.agents[agent_id]
        del self.log_buffers[agent_id]

        # 删除配置文件
        config_path = os.path.join(self.config_dir, f"{agent_id}.json")
        if os.path.exists(config_path):
            os.remove(config_path)

        return True

    async def create_agent(self, config: AgentConfig) -> AgentInfo:
        """创建新Agent"""
        agent_id = config.id

        agent = AgentInfo(
            id=agent_id,
            name=config.name,
            state=AgentState.STOPPED,
            config=config
        )

        self.agents[agent_id] = agent
        self.log_buffers[agent_id] = []

        # 保存配置
        config_path = os.path.join(self.config_dir, f"{agent_id}.json")
        async with aiofiles.open(config_path, 'w') as f:
            await f.write(config.model_dump_json(indent=2))

        if config.auto_start:
            await self.start_agent(agent_id)

        return agent

    async def update_agent_config(self, agent_id: str, config: AgentConfig) -> Optional[AgentInfo]:
        """更新Agent配置"""
        if agent_id not in self.agents:
            return None

        agent = self.agents[agent_id]
        was_running = agent.state == AgentState.RUNNING

        if was_running:
            await self.stop_agent(agent_id)

        agent.config = config
        agent.name = config.name

        # 保存配置
        config_path = os.path.join(self.config_dir, f"{agent_id}.json")
        async with aiofiles.open(config_path, 'w') as f:
            await f.write(config.model_dump_json(indent=2))

        if was_running or config.auto_start:
            await self.start_agent(agent_id)

        return agent

    async def get_agent_logs(self, agent_id: str, lines: int = 100) -> List[str]:
        """获取Agent日志"""
        if agent_id not in self.log_buffers:
            return []

        return self.log_buffers[agent_id][-lines:]

    async def _collect_logs(self, agent_id: str, process: asyncio.subprocess.Process):
        """收集Agent输出日志"""
        async def read_stream(stream, prefix):
            while True:
                line = await stream.readline()
                if not line:
                    break
                log_line = f"{prefix} {line.decode('utf-8', errors='replace').strip()}"
                self.log_buffers[agent_id].append(log_line)
                # 限制缓冲区大小
                if len(self.log_buffers[agent_id]) > 1000:
                    self.log_buffers[agent_id] = self.log_buffers[agent_id][-500:]

        asyncio.create_task(read_stream(process.stdout, "[OUT]"))
        asyncio.create_task(read_stream(process.stderr, "[ERR]"))

        await process.wait()

        # 进程结束
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            if process.returncode != 0:
                agent.state = AgentState.ERROR
                agent.last_error = f"Process exited with code {process.returncode}"
            else:
                agent.state = AgentState.STOPPED

            if agent_id in self.processes:
                del self.processes[agent_id]
