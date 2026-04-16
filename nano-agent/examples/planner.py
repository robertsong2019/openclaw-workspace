"""
任务规划代理示例
"""

import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nano_agent import Agent, tool
import json


# 定义工具
@tool
def create_task(description: str, priority: str = "medium") -> str:
    """创建一个新任务

    Args:
        description: 任务描述
        priority: 任务优先级 (low, medium, high)

    Returns:
        创建的任务信息
    """
    task = {
        "description": description,
        "priority": priority,
        "status": "pending",
        "created_at": "2025-01-10"
    }
    return json.dumps(task, ensure_ascii=False, indent=2)


@tool
def estimate_effort(task_description: str) -> str:
    """估算任务工作量

    Args:
        task_description: 任务描述

    Returns:
        工作量估算
    """
    # 简单的基于长度的估算
    words = len(task_description.split())
    if words < 10:
        effort = "1-2 小时"
    elif words < 20:
        effort = "2-4 小时"
    else:
        effort = "1-2 天"

    return f"任务 '{task_description[:50]}...' 预计需要 {effort}"


@tool
def break_down_task(task: str) -> str:
    """将任务分解为子任务

    Args:
        task: 主任务

    Returns:
        子任务列表
    """
    subtasks = [
        f"需求分析: {task}",
        f"设计方案",
        f"实现功能",
        f"测试验证",
        f"部署上线"
    ]
    return json.dumps(subtasks, ensure_ascii=False, indent=2)


# 创建代理
planner = Agent(
    name="任务规划师",
    instructions="""你是一个专业的任务规划助手，帮助用户：
1. 理解项目需求
2. 分解任务为可执行的步骤
3. 估算工作量和优先级
4. 提供清晰的项目计划

请主动调用工具来完成任务规划。""",
    tools=[create_task, estimate_effort, break_down_task],
    verbose=True
)


if __name__ == "__main__":
    # 示例对话
    print("=" * 60)
    print("🧪 Nano-Agent 示例: 任务规划师")
    print("=" * 60)

    user_input = "帮我规划一个项目：开发一个 AI 聊天机器人"
    print(f"\n👤 用户: {user_input}\n")

    response = planner.run(user_input)

    print("\n" + "=" * 60)
    print("✅ 最终回复:")
    print("=" * 60)
    print(response)
