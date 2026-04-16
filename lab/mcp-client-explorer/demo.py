#!/usr/bin/env python3
"""
MCP Client 演示

展示如何使用 MCP Client 连接到服务器并使用各种功能
"""

import sys
import json
from typing import Any
from mcp_client import MCPClient, connect


def print_header(title: str):
    """打印标题"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def print_json(data: Any, indent: int = 2):
    """美化打印 JSON"""
    print(json.dumps(data, ensure_ascii=False, indent=indent))


def main():
    """主函数"""
    server_command = ["python3", "mcp_server.py"]

    # 使用上下文管理器自动管理连接
    with connect(server_command) as client:
        if not client._initialized:
            print("❌ 服务器初始化失败")
            sys.exit(1)

        print("✅ MCP 服务器连接成功\n")

        # ========== 资源演示 ==========
        print_header("1. 资源操作 (Resources)")

        print("📋 列出所有资源:")
        resources = client.list_resources()
        for resource in resources:
            print(f"  • {resource.name}")
            print(f"    URI: {resource.uri}")
            print(f"    描述: {resource.description}")
            print(f"    类型: {resource.mime_type}")
            print()

        print("\n📖 读取资源内容:")
        for resource in resources:
            content = client.read_resource(resource.uri)
            if content:
                print(f"\n  资源: {resource.name}")
                print(f"  内容:")
                print_json(json.loads(content["contents"][0]["text"]), indent=4)

        # ========== 工具演示 ==========
        print_header("2. 工具操作 (Tools)")

        print("🔧 列出所有工具:")
        tools = client.list_tools()
        for tool in tools:
            print(f"  • {tool.name}")
            print(f"    描述: {tool.description}")
            print(f"    参数: {json.dumps(tool.input_schema, ensure_ascii=False)}")
            print()

        print("\n⚙️  调用工具示例:")

        # 计算
        result = client.call_tool("calculate", {"operation": "add", "a": 10, "b": 32})
        print(f"\n  calculate(10 + 32) = {json.loads(result['content'][0]['text'])}")

        result = client.call_tool("calculate", {"operation": "multiply", "a": 7, "b": 8})
        print(f"  calculate(7 × 8) = {json.loads(result['content'][0]['text'])}")

        # 斐波那契
        result = client.call_tool("fibonacci", {"n": 10})
        print(f"\n  fibonacci(10) = {json.loads(result['content'][0]['text'])}")

        # 反转字符串
        result = client.call_tool("reverse_string", {"text": "Hello, MCP!"})
        print(f"  reverse_string('Hello, MCP!') = {json.loads(result['content'][0]['text'])}")

        # ========== 提示模板演示 ==========
        print_header("3. 提示模板操作 (Prompts)")

        print("📝 列出所有提示模板:")
        prompts = client.list_prompts()
        for prompt in prompts:
            print(f"  • {prompt.name}")
            print(f"    描述: {prompt.description}")
            if prompt.arguments:
                print(f"    参数:")
                for arg in prompt.arguments:
                    required = "（必需）" if arg.get("required", False) else "（可选）"
                    print(f"      - {arg['name']}: {arg.get('description', '')} {required}")
            print()

        print("\n💬 获取提示模板内容:")

        # 代码审查模板
        prompt_result = client.get_prompt("code_review", {"language": "Python", "focus": "performance"})
        print(f"\n  提示模板: code_review (Python, 性能重点)")
        print(f"  消息:")
        for i, msg in enumerate(prompt_result["messages"], 1):
            print(f"\n    消息 {i} ({msg['role']}):")
            print(f"    {msg['content']}")

        # 任务分解模板
        prompt_result = client.get_prompt("task_breakdown", {"task": "Build a REST API for todo management"})
        print(f"\n\n  提示模板: task_breakdown")
        print(f"  消息:")
        for i, msg in enumerate(prompt_result["messages"], 1):
            print(f"\n    消息 {i} ({msg['role']}):")
            print(f"    {msg['content']}")

        # ========== 总结 ==========
        print_header("4. 总结")

        print("""
✅ MCP Client 功能演示完成

核心功能：
  • 资源列表与读取 - 访问服务器暴露的数据
  • 工具列表与调用 - 执行远程函数
  • 提示模板列表与获取 - 获取结构化的 LLM 提示

应用场景：
  • AI Agent 工具集成 - Agent 通过 MCP 访问各种工具
  • 插件系统 - 服务器提供可扩展的功能
  • 上下文管理 - 提示模板统一管理 LLM 上下文

下一步：
  • 实现更复杂的 MCP Server（真实工具集成）
  • 将 OpenClaw 工具暴露为 MCP 接口
  • 探索 MCP 在多 Agent 编排中的应用
        """)


if __name__ == "__main__":
    main()
