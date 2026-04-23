# Better Ralph Core 教程 🔄

> 从 PRD 到自动提交：学会用 Better Ralph 驱动自主开发循环

## 目录

1. [准备你的第一个 PRD](#1-准备你的第一个-prd)
2. [启动一个 Session](#2-启动一个-session)
3. [理解迭代循环](#3-理解迭代循环)
4. [记忆系统：跨迭代学习](#4-记忆系统跨迭代学习)
5. [实战：自动化一个真实项目](#5-实战自动化一个真实项目)
6. [自定义 Agent](#6-自定义-agent)
7. [常见问题与调试](#7-常见问题与调试)

---

## 1. 准备你的第一个 PRD

PRD（Product Requirements Document）是 Better Ralph 的工作蓝图。它是一个 JSON 文件，包含项目元信息和用户故事列表。

### 最小 PRD 示例

创建 `prd.json`：

```json
{
  "project": {
    "name": "hello-ralph",
    "description": "一个简单的示例项目",
    "tech_stack": ["python"]
  },
  "stories": [
    {
      "id": "US-001",
      "title": "创建入口文件",
      "description": "创建 main.py，包含一个 hello 函数，返回 'Hello from Ralph!'",
      "acceptance_criteria": [
        "main.py 文件存在",
        "hello() 函数返回正确的字符串",
        "运行 python main.py 输出预期内容"
      ],
      "priority": 1,
      "dependencies": []
    },
    {
      "id": "US-002",
      "title": "添加命令行参数",
      "description": "在 main.py 中使用 argparse 支持自定义问候语",
      "acceptance_criteria": [
        "支持 --name 参数",
        "默认问候语为 'World'",
        "输出格式: 'Hello, {name}!'"
      ],
      "priority": 2,
      "dependencies": ["US-001"]
    }
  ]
}
```

### PRD 字段说明

| 字段 | 说明 | 必填 |
|------|------|------|
| `project.name` | 项目名称 | ✅ |
| `project.description` | 项目描述 | ✅ |
| `project.tech_stack` | 技术栈标签 | 推荐 |
| `stories[].id` | 故事唯一标识 | ✅ |
| `stories[].title` | 故事标题 | ✅ |
| `stories[].description` | 详细描述 | ✅ |
| `stories[].acceptance_criteria` | 验收标准列表 | ✅ |
| `stories[].priority` | 优先级（数字越小越优先） | ✅ |
| `stories[].dependencies` | 依赖的故事 ID 列表 | 推荐 |

---

## 2. 启动一个 Session

```python
from pathlib import Path
from core.orchestrator import RalphOrchestrator

# 创建编排器
orchestrator = RalphOrchestrator()

# 启动 session
session_id = orchestrator.start_session(
    prd_path=Path("prd.json"),
    project_root=Path("/path/to/your/project")
)

print(f"Session started: {session_id}")
```

**发生了什么？**

1. PRD 被加载到 `PRDManager`
2. 故事列表按优先级和依赖关系排序
3. `MemoryManager` 恢复之前的上下文（如果有）
4. Git 工作区检查（确保干净状态）

---

## 3. 理解迭代循环

每次迭代是 **选择故事 → 执行 → 验证 → 提交** 的完整流程：

```python
# 单次迭代
result = orchestrator.execute_iteration()

print(f"Story: {result.story_id} - {result.story_title}")
print(f"Success: {result.success}")
print(f"Duration: {result.duration:.1f}s")
if result.commit_hash:
    print(f"Commit: {result.commit_hash}")
if result.error_message:
    print(f"Error: {result.error_message}")
```

### IterationResult 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `story_id` | str | 故事 ID |
| `story_title` | str | 故事标题 |
| `success` | bool | 是否通过验收 |
| `duration` | float | 耗时（秒） |
| `commit_hash` | str \| None | Git commit hash（成功时） |
| `error_message` | str \| None | 失败原因 |
| `artifacts` | list[str] | 创建/修改的文件列表 |

### 运行完整 Session

```python
# 自动运行直到所有故事完成
while not orchestrator.is_complete():
    result = orchestrator.execute_iteration()
    status = "✅" if result.success else "❌"
    print(f"{status} {result.story_id}: {result.story_title}")

# 获取总结
summary = orchestrator.get_session_summary()
print(f"完成 {summary.successful_iterations}/{summary.total_iterations} 个故事")
print(f"总耗时: {summary.total_duration:.1f}s")

# 结束 session
orchestrator.end_session()
```

---

## 4. 记忆系统：跨迭代学习

Better Ralph 的记忆系统让它越做越好。每次迭代积累的上下文会传递给下一次：

### 记忆包含什么

```
MemoryManager
├── iteration_context    — 每次迭代的产物、学到的模式
├── project_context      — 代码约定、常见陷阱、文件类型
└── progress             — 已完成故事、累计统计
```

### 记忆如何工作

```python
from core.memory_manager import MemoryManager

memory = MemoryManager()

# 迭代中自动记录
memory.add_iteration_context(
    iteration=3,
    story_id="US-003",
    artifacts=["src/api.py", "tests/test_api.py"],
    learnings=["项目使用 pytest 而非 unittest", "API 路由前缀是 /api/v1"]
)

# 下次迭代自动获取
context = memory.get_relevant_context("US-004")
# → 包含之前的 learnings，帮助 Agent 遵循既有约定
```

### 持久化

记忆默认持久化到项目目录，下次启动 session 时自动恢复：

```python
# 记忆文件位置
# .ralph/memory/iterations.json   — 迭代记录
# .ralph/memory/project.json      — 项目上下文
# .ralph/memory/progress.json     — 进度追踪
```

---

## 5. 实战：自动化一个真实项目

### 场景：给 Flask 项目添加用户认证

**prd.json：**

```json
{
  "project": {
    "name": "flask-auth",
    "description": "Flask 用户认证模块",
    "tech_stack": ["python", "flask", "sqlite"]
  },
  "stories": [
    {
      "id": "US-001",
      "title": "User 模型",
      "description": "创建 User SQLAlchemy 模型，包含 username, email, password_hash 字段",
      "acceptance_criteria": [
        "models/user.py 存在",
        "User 模型有 username, email, password_hash 列",
        "包含 set_password 和 check_password 方法"
      ],
      "priority": 1,
      "dependencies": []
    },
    {
      "id": "US-002",
      "title": "注册 API",
      "description": "POST /api/register 端点，接收 username, email, password",
      "acceptance_criteria": [
        "返回 201 和用户信息（不含密码）",
        "重复用户名返回 409",
        "缺少字段返回 422"
      ],
      "priority": 2,
      "dependencies": ["US-001"]
    },
    {
      "id": "US-003",
      "title": "登录 API",
      "description": "POST /api/login 端点，返回 JWT token",
      "acceptance_criteria": [
        "验证用户名和密码",
        "返回 JWT token",
        "错误凭据返回 401"
      ],
      "priority": 2,
      "dependencies": ["US-001"]
    },
    {
      "id": "US-004",
      "title": "认证测试",
      "description": "为注册和登录 API 编写 pytest 测试",
      "acceptance_criteria": [
        "测试文件 tests/test_auth.py 存在",
        "覆盖成功和失败场景",
        "所有测试通过"
      ],
      "priority": 3,
      "dependencies": ["US-002", "US-003"]
    }
  ]
}
```

**运行：**

```python
from pathlib import Path
from core.orchestrator import RalphOrchestrator

orchestrator = RalphOrchestrator()
session_id = orchestrator.start_session(
    prd_path=Path("prd.json"),
    project_root=Path("./flask-auth")
)

while not orchestrator.is_complete():
    result = orchestrator.execute_iteration()
    print(f"{'✅' if result.success else '❌'} {result.story_id}: {result.story_title}")
    if result.commit_hash:
        print(f"   → {result.commit_hash[:7]}")

orchestrator.end_session()
```

---

## 6. 自定义 Agent

默认的 Agent 处理代码生成和编辑。你可以注册自定义 Agent 处理特定任务：

```python
from core.agent_registry import Agent, AgentRegistry

class SecurityAgent(Agent):
    """专注于安全审查的 Agent"""
    
    name = "security-reviewer"
    capabilities = ["security_audit", "dependency_check"]
    
    def execute(self, story, context):
        # 自定义执行逻辑
        vulnerabilities = self.scan_code(context.project_root)
        report = self.generate_report(vulnerabilities)
        return report

# 注册
registry = AgentRegistry()
registry.register(SecurityAgent())

# 带有 security_audit 标签的故事会自动路由给这个 Agent
```

---

## 7. 常见问题与调试

### 迭代失败了怎么办？

```python
result = orchestrator.execute_iteration()
if not result.success:
    print(result.error_message)
    # 查看记忆中的上下文
    context = orchestrator.memory_manager.get_relevant_context(result.story_id)
    # 修复问题后重试
    result = orchestrator.retry_iteration()
```

### 常见陷阱

| 问题 | 原因 | 解决 |
|------|------|------|
| 故事一直跳过 | 依赖未完成 | 检查 dependencies 字段 |
| 验收不通过 | 标准太模糊 | 写具体的、可验证的标准 |
| commit 失败 | Git 工作区脏 | 运行前确保 `git status` 干净 |
| Agent 选错 | 故事描述不清 | 在 description 中指明技术细节 |

### 调试技巧

```python
# 开启详细日志
from utils.logger import Logger
Logger.set_level("DEBUG")

# 查看 PRD 解析结果
prd = orchestrator.prd_manager
for story in prd.stories:
    print(f"{story.id} | pri={story.priority} | passes={story.passes} | deps={story.dependencies}")

# 查看记忆内容
mem = orchestrator.memory_manager
print(mem.get_project_context())
```

---

## 设计理念

| 原则 | 体现 |
|------|------|
| **PRD 驱动** | 所有工作源自结构化需求，无歧义 |
| **渐进式** | 一次一个故事，每步可验证 |
| **有记忆** | 跨迭代学习，不重复犯错 |
| **可扩展** | 自定义 Agent、插件系统 |

---

_下一步：阅读 [源码](core/) — orchestrator.py 是入口，逻辑清晰。_ 🔄
