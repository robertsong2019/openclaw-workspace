# Projects Overview — 项目全景图

> 工作区中所有项目的定位、关系和快速入口

## 🗺️ 项目地图

```
                        ┌──────────────┐
                        │  agent-log   │ 记录和查询
                        │  (Python)    │
                        └──────┬───────┘
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
          ┌─────────────┐ ┌──────────┐ ┌──────────────┐
          │ memory-graph│ │ memory-  │ │ agent-task-  │
          │ (Python)    │ │ service  │ │ cli (Node)   │
          │ 知识图谱    │ │ (Node)   │ │ 任务编排     │
          └─────────────┘ │ 记忆服务 │ └──────────────┘
                         └──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
     ┌──────────────┐  ┌──────────┐  ┌──────────────┐
     │ context-forge│  │prompt-mgr│  │mission-      │
     │ (Node)       │  │ (Python) │  │control(Node) │
     │ AI上下文生成 │  │ 提示词   │  │ 项目管理     │
     └──────────────┘  └──────────┘  └──────────────┘
```

## 📋 项目清单

| 项目 | 语言 | 一句话描述 | 状态 |
|------|------|-----------|------|
| [agent-task-cli](./agent-task-cli) | Node.js | AI Agent 任务编排 CLI | ✅ 可用 |
| [agent-memory-service](./agent-memory-service) | Node.js | 多策略记忆检索服务 | ✅ 可用 |
| [agent-memory-graph](./agent-memory-graph) | Python | 知识图谱存储和查询 | ✅ 可用 |
| [agent-log](./agent-log) | Python | Agent 行为日志记录 | ✅ 可用 |
| [context-forge](./context-forge) | Node.js | AI 编码助手上下文文件生成 | ✅ 可用 |
| [prompt-mgr](./prompt-mgr) | Python | AI 提示词模板管理 | ✅ 可用 |
| [mission-control](./mission-control) | Node.js | 多项目仪表盘和管理 | ✅ 可用 |
| [context-forge](./context-forge) | Node.js | AI 上下文文件生成器 | ✅ 可用 |

## 🔗 项目关系

### Agent 基础设施（核心三件套）

**agent-task-cli** + **agent-memory-service** + **agent-log** 构成 Agent 运行时基础：

- **agent-task-cli**: "做什么" — 任务分解、依赖管理、执行编排
- **agent-memory-service**: "记住什么" — 跨会话记忆存储和检索
- **agent-log**: "做了什么" — 行为日志、审计追踪

### 辅助工具

- **context-forge**: 让外部 AI 工具（Cursor/Copilot）理解你的项目
- **prompt-mgr**: 管理和复用提示词模板
- **mission-control**: 统一查看和管理所有项目

## 📚 教程索引

| 教程 | 内容 |
|------|------|
| [记忆系统教程](./TUTORIAL-memory-systems.md) | 三个记忆项目的概念和关系 |
| [context-forge 教程](./TUTORIAL-context-forge.md) | 让 AI 编码助手理解你的项目 |

## 🤝 贡献指南

见 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

_最后更新: 2026-04-16_
