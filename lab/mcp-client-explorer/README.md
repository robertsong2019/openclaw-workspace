# MCP Client Explorer

🧪 **代码实验室 - MCP 协议深度实践**

纯 Python 3 实现的轻量级 MCP (Model Context Protocol) 客户端和服务器，零依赖，演示 Agent 工具生态的核心概念。

## 什么是 MCP？

**MCP (Model Context Protocol)** 是 AI Agent 工具生态的标准协议，类似于 HTTP 对 Web 的意义。

- **97M+ 下载量**（2026-04）
- **标准化工具访问** - 统一的接口定义资源、工具、提示模板
- **多传输层支持** - stdio、SSE、WebSocket
- **JSON-RPC 2.0** - 简单可靠的通信协议

## 核心概念

### 1. 资源 (Resources)

服务器暴露的数据源，如文件、数据库记录、API 返回的数据。

```
资源示例：
  - data://weather/current    → 当前天气数据
  - data://system/status      → 系统状态
  - file:///path/to/doc.md    → 文件内容
```

### 2. 工具 (Tools)

可执行的函数，Agent 可以远程调用这些工具完成特定任务。

```
工具示例：
  - calculate(operation, a, b)    → 数学计算
  - fibonacci(n)                  → 斐波那契数列
  - reverse_string(text)          → 字符串反转
```

### 3. 提示模板 (Prompts)

结构化的 LLM 提示词，用于生成一致的上下文。

```
模板示例：
  - code_review(language, focus)  → 代码审查提示
  - task_breakdown(task)          → 任务分解提示
```

## 项目结构

```
mcp-client-explorer/
├── mcp_client.py   # MCP 客户端实现
├── mcp_server.py   # MCP 服务器实现（测试用）
├── demo.py         # 功能演示
└── README.md       # 本文档
```

## 快速开始

### 1. 运行演示

```bash
python3 demo.py
```

演示输出包括：
- 资源列表与读取
- 工具列表与调用
- 提示模板列表与获取

### 2. 作为模块使用

```python
from mcp_client import connect

# 连接到 MCP 服务器
with connect(["python3", "your_server.py"]) as client:
    # 列出工具
    tools = client.list_tools()
    for tool in tools:
        print(f"工具: {tool.name}")

    # 调用工具
    result = client.call_tool("calculate", {
        "operation": "add",
        "a": 10,
        "b": 32
    })
    print(f"结果: {result}")
```

## MCP Client API

### 初始化

```python
from mcp_client import MCPClient

client = MCPClient(["python3", "server.py"])
client.start()

# 或使用便捷函数
from mcp_client import connect
client = connect(["python3", "server.py"])
```

### 资源操作

```python
# 列出所有资源
resources = client.list_resources()
for resource in resources:
    print(f"{resource.name}: {resource.uri}")

# 读取资源内容
content = client.read_resource("data://weather/current")
print(content)
```

### 工具操作

```python
# 列出所有工具
tools = client.list_tools()

# 调用工具
result = client.call_tool("calculate", {
    "operation": "multiply",
    "a": 7,
    "b": 8
})
```

### 提示模板操作

```python
# 列出所有提示模板
prompts = client.list_prompts()

# 获取提示模板内容
prompt = client.get_prompt("code_review", {
    "language": "Python",
    "focus": "performance"
})
```

## MCP Server API（扩展指南）

如果你想实现自己的 MCP Server，需要处理以下方法：

### 必需方法

- `initialize` - 服务器初始化握手
- `notifications/initialized` - 初始化完成通知

### 资源方法

- `resources/list` - 返回可用资源列表
- `resources/read` - 读取指定资源内容

### 工具方法

- `tools/list` - 返回可用工具列表
- `tools/call` - 执行指定工具

### 提示模板方法

- `prompts/list` - 返回可用提示模板列表
- `prompts/get` - 获取指定提示模板内容

## JSON-RPC 2.0 协议

MCP 基于 JSON-RPC 2.0，请求/响应格式如下：

**请求：**
```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/call",
  "params": {
    "name": "calculate",
    "arguments": {"operation": "add", "a": 10, "b": 32}
  }
}
```

**响应：**
```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "42"
      }
    ]
  }
}
```

## 应用场景

### 1. AI Agent 工具集成

Agent 通过 MCP 访问各种工具，无需关心底层实现细节。

```python
# Agent 通过 MCP 调用 web_search 工具
result = client.call_tool("web_search", {"query": "MCP protocol"})
```

### 2. 插件系统

服务器提供可扩展的功能，客户端按需调用。

```python
# 动态发现并调用新工具
tools = client.list_tools()
for tool in tools:
    if tool.name.startswith("analysis_"):
        # 调用所有分析工具
        client.call_tool(tool.name, {...})
```

### 3. 上下文管理

统一管理 LLM 的提示模板，确保一致性。

```python
# 获取标准化的代码审查提示
prompt = client.get_prompt("code_review", {"language": "Python"})
# 发送给 LLM
llm_response = llm.generate(prompt["messages"])
```

## 下一步

### 立即可做

- [ ] 实现真实的 MCP Server（集成实际工具，如文件操作、数据库查询）
- [ ] 添加更多传输层支持（SSE、WebSocket）
- [ ] 实现资源订阅功能（`resources/subscribe`）

### 长期目标

- [ ] 将 OpenClaw 工具暴露为 MCP 接口
- [ ] 集成到 Agent 编排框架（LangGraph、CrewAI）
- [ ] 探索 Agent 联邦（A2A 协议）与 MCP 的结合

## 相关资源

- [MCP 官方规范](https://modelcontextprotocol.io)
- [OpenClaw 项目](https://github.com/openclaw)
- [AI Agent 编程指南](../memory/2026-04-10/ai-agent-programming.md)

## 技术细节

### 零依赖设计

- 纯 Python 3.7+
- 无第三方库
- 适合嵌入式环境

### 线程安全

- 使用线程池处理并发请求
- 请求 ID 唯一性保证
- 超时机制防止阻塞

### 错误处理

- JSON-RPC 标准错误码
- 优雅的异常传播
- 详细的错误信息

---

**实验日期：** 2026-04-12
**作者：** Catalyst 🧪 (Digital Familiar)
**目标：** 探索 MCP 协议，为 OpenClaw MCP Server 实现打基础
