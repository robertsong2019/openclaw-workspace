#!/usr/bin/env python3
"""
Mini MCP Bus - 一个极简的工具协议总线演示
模拟MCP协议的核心概念：Agent通过标准协议调用工具

概念：
- ToolServer: 注册并暴露工具
- MCPBus: 中央总线，路由工具调用
- Agent: 通过总线发现和调用工具

运行：python mini-mcp-bus.py
"""

import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable
from enum import Enum


class MessageType(Enum):
    DISCOVER = "discover"
    CALL = "call"
    RESULT = "result"
    ERROR = "error"


@dataclass
class ToolDescriptor:
    name: str
    description: str
    parameters: dict  # JSON Schema style
    server_id: str


@dataclass
class MCPMessage:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: MessageType = MessageType.CALL
    sender: str = ""
    tool: str = ""
    args: dict = field(default_factory=dict)
    result: Any = None
    error: str = ""
    timestamp: float = field(default_factory=time.time)


class ToolServer:
    """工具服务器 - 注册并暴露工具给总线"""
    
    def __init__(self, name: str):
        self.name = name
        self._tools: dict[str, Callable] = {}
        self._descriptors: dict[str, ToolDescriptor] = {}
    
    def register(self, name: str, desc: str, params: dict):
        """装饰器：注册一个工具"""
        def decorator(fn: Callable):
            self._tools[name] = fn
            self._descriptors[name] = ToolDescriptor(
                name=name, description=desc,
                parameters=params, server_id=self.name
            )
            return fn
        return decorator
    
    def get_descriptors(self) -> list[ToolDescriptor]:
        return list(self._descriptors.values())
    
    def call(self, tool_name: str, args: dict) -> Any:
        if tool_name not in self._tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        return self._tools[tool_name](**args)


class MCPBus:
    """MCP总线 - 连接Agent和ToolServer"""
    
    def __init__(self):
        self._servers: dict[str, ToolServer] = {}
        self._log: list[MCPMessage] = []
    
    def register_server(self, server: ToolServer):
        self._servers[server.name] = server
        print(f"  📡 服务器 '{server.name}' 已注册")
    
    def discover(self) -> list[ToolDescriptor]:
        """发现所有可用工具"""
        tools = []
        for server in self._servers.values():
            tools.extend(server.get_descriptors())
        return tools
    
    def call(self, sender: str, tool_name: str, args: dict) -> MCPMessage:
        """路由工具调用到对应服务器"""
        msg = MCPMessage(
            type=MessageType.CALL,
            sender=sender,
            tool=tool_name,
            args=args
        )
        
        # 查找目标服务器
        for server in self._servers.values():
            desc = server._descriptors.get(tool_name)
            if desc:
                try:
                    result = server.call(tool_name, args)
                    msg.type = MessageType.RESULT
                    msg.result = result
                    print(f"  ✅ {sender} → {tool_name}({json.dumps(args, ensure_ascii=False)})")
                except Exception as e:
                    msg.type = MessageType.ERROR
                    msg.error = str(e)
                    print(f"  ❌ {sender} → {tool_name}: {e}")
                break
        else:
            msg.type = MessageType.ERROR
            msg.error = f"Tool not found: {tool_name}"
        
        self._log.append(msg)
        return msg
    
    def print_stats(self):
        print(f"\n📊 总线统计:")
        print(f"   服务器数: {len(self._servers)}")
        print(f"   总调用数: {len(self._log)}")
        success = sum(1 for m in self._log if m.type == MessageType.RESULT)
        print(f"   成功/失败: {success}/{len(self._log) - success}")


class Agent:
    """AI Agent - 通过总线发现和调用工具"""
    
    def __init__(self, name: str, bus: MCPBus):
        self.name = name
        self.bus = bus
        self._known_tools: list[ToolDescriptor] = []
    
    def discover_tools(self):
        """发现可用工具"""
        self._known_tools = self.bus.discover(self)
        print(f"\n🔍 {self.name} 发现 {len(self._known_tools)} 个工具:")
        for t in self._known_tools:
            print(f"   🔧 {t.name}: {t.description}")
        return self._known_tools
    
    def use(self, tool_name: str, **kwargs) -> Any:
        """调用工具"""
        msg = self.bus.call(self.name, tool_name, kwargs)
        if msg.type == MessageType.ERROR:
            print(f"  ⚠️ 错误: {msg.error}")
            return None
        return msg.result
    
    def plan_and_execute(self, task: str):
        """简单的规划执行循环"""
        print(f"\n🤖 {self.name} 收到任务: {task}")
        
        # 简单的任务路由逻辑
        if "天气" in task:
            self.use("get_weather", city="上海")
        elif "计算" in task or "+" in task:
            self.use("calculate", expression="2+3*4")
        elif "时间" in task:
            self.use("get_time", timezone="Asia/Shanghai")
        elif "翻译" in task:
            self.use("translate", text="Hello World", target_lang="zh")
        else:
            print("  🤔 无法自动处理，列出可用工具...")
            self.discover_tools()


# ============================================================
# Demo: 搭建一个微型工具生态
# ============================================================

def main():
    print("=" * 60)
    print("  🧪 Mini MCP Bus - AI Agent 工具协议演示")
    print("=" * 60)
    
    bus = MCPBus()
    
    # --- 服务器1: 天气与环境 ---
    weather_server = ToolServer("weather-service")
    
    @weather_server.register(
        "get_weather",
        "获取指定城市天气",
        {"city": {"type": "string"}}
    )
    def get_weather(city: str) -> dict:
        # 模拟天气数据
        import random
        temps = {"上海": (18, 26), "北京": (12, 22), "深圳": (24, 30)}
        low, high = temps.get(city, (15, 25))
        return {
            "city": city,
            "temp": random.randint(low, high),
            "condition": random.choice(["晴", "多云", "阵雨", "晴转多云"]),
            "humidity": random.randint(40, 80)
        }
    
    @weather_server.register(
        "get_time",
        "获取当前时间",
        {"timezone": {"type": "string"}}
    )
    def get_time(timezone: str) -> str:
        from datetime import datetime
        now = datetime.now()
        return f"{timezone} 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    bus.register_server(weather_server)
    
    # --- 服务器2: 计算服务 ---
    calc_server = ToolServer("calc-service")
    
    @calc_server.register(
        "calculate",
        "安全计算数学表达式",
        {"expression": {"type": "string"}}
    )
    def calculate(expression: str) -> dict:
        # 安全计算（只允许数字和运算符）
        allowed = set("0123456789+-*/().% ")
        if not all(c in allowed for c in expression):
            return {"error": "表达式包含非法字符"}
        result = eval(expression)  # 仅用于演示，生产环境禁用eval
        return {"expression": expression, "result": result}
    
    @calc_server.register(
        "translate",
        "模拟翻译（概念演示）",
        {"text": {"type": "string"}, "target_lang": {"type": "string"}}
    )
    def translate(text: str, target_lang: str) -> dict:
        translations = {
            ("Hello World", "zh"): "你好世界",
            ("你好世界", "en"): "Hello World",
        }
        result = translations.get((text, target_lang), f"[{target_lang}] {text}")
        return {"original": text, "translated": result, "lang": target_lang}
    
    bus.register_server(calc_server)
    
    # --- 创建Agent并运行演示 ---
    print("\n" + "─" * 40)
    
    agent = Agent("Catalyst", bus)
    
    # Step 1: 发现工具
    agent.discover_tools()
    
    # Step 2: 执行任务
    print("\n" + "─" * 40)
    print("  开始执行任务序列...")
    print("─" * 40)
    
    # 调用天气
    weather = agent.use("get_weather", city="上海")
    print(f"     → {weather}")
    
    # 调用计算
    calc = agent.use("calculate", expression="1024 * 768")
    print(f"     → {calc}")
    
    # 调用翻译
    trans = agent.use("translate", text="Hello World", target_lang="zh")
    print(f"     → {trans}")
    
    # 调用时间
    ts = agent.use("get_time", timezone="Asia/Shanghai")
    print(f"     → {ts}")
    
    # 测试错误处理
    print("\n  测试错误处理:")
    agent.use("nonexistent_tool")
    agent.use("calculate", expression="<script>alert(1)</script>")
    
    # 统计
    print("\n" + "─" * 40)
    bus.print_stats()
    
    print("\n✨ 演示完成！核心概念:")
    print("   1. ToolServer 注册工具（类似MCP Server）")
    print("   2. MCPBus 路由调用（类似MCP协议层）")
    print("   3. Agent 通过标准协议发现和调用（解耦）")
    print("   4. 新工具只需注册，Agent自动发现")


if __name__ == "__main__":
    main()
