# Agent Memory 系统 — 概念教程

> 本教程帮助你理解工作区中三个记忆相关项目的核心概念和它们之间的关系。

## 目录

1. [为什么 Agent 需要记忆？](#为什么-agent-需要记忆)
2. [三个项目的关系](#三个项目的关系)
3. [核心概念](#核心概念)
4. [实战：构建一个记忆系统](#实战构建一个记忆系统)
5. [设计权衡](#设计权衡)

---

## 为什么 Agent 需要记忆？

LLM 本身是无状态的——每次对话都是全新的。但一个有用的 Agent 需要：

- **记住你是谁** — 你的偏好、项目、工作习惯
- **记住发生了什么** — 昨天讨论的决定、上周的进展
- **关联上下文** — "这个 bug 和上周那个问题有关"

没有记忆，Agent 就是金鱼。有了记忆，Agent 才能真正协作。

## 三个项目的关系

```
┌─────────────────────┐
│  agent-memory-graph  │  ← 知识图谱：概念、关系、遍历
│  (Python, SQLite)    │
└──────────┬──────────┘
           │ 互补
┌──────────▼──────────┐
│ agent-memory-service │  ← 三层存储：短期/长期/核心 + 自动提取
│ (Node.js, SQLite)    │
└──────────┬──────────┘
           │ 查询
┌──────────▼──────────┐
│     agent-log        │  ← 日志搜索：快速查找历史记录
│   (Bash, grep)       │
└─────────────────────┘
```

| 项目 | 核心问题 | 技术选型 | 适用场景 |
|------|---------|---------|---------|
| memory-graph | "事物之间有什么关系？" | Python + SQLite | 探索关联、知识发现 |
| memory-service | "Agent 该记住什么、忘掉什么？" | Node.js + SQLite | 生产级记忆管理 |
| agent-log | "什么时候讨论过 X？" | Bash + grep | 快速查找历史 |

## 核心概念

### 1. 记忆衰减（Ebbinghaus 遗忘曲线）

人类不会永远记住所有事，Agent 也不应该。

```python
# 衰减公式
weight = initial × e^(-0.3 × elapsed_days)

# 访问时恢复（模拟"复习"）
weight = min(1.0, decayed_weight + 0.4)

# 低于阈值 → 遗忘（删除）
if weight < 0.05: forget()
```

**为什么？** 记忆无限增长会导致检索变慢、成本增加、噪音增多。遗忘是自然的信息过滤器。

### 2. 三层存储

```
L0 (Core)    — 身份、核心偏好。永不过期。
L1 (Long)    — 项目、人物、经验。30天衰减。
L2 (Short)   — 近期对话、临时上下文。1天衰减。
```

**类比：** L0 是你的性格，L1 是你的经历，L2 是你今天早饭吃了什么。

### 3. 知识图谱

记忆不只是列表，而是网络：

```
(罗嵩) --works_on--> (OpenClaw)
   |                     |
   | prefers              | uses
   v                     v
(TypeScript)        (SQLite)
```

图谱让你通过遍历发现关联："罗嵩 → works_on → OpenClaw → uses → SQLite"

### 4. 多策略检索

单一搜索方式不够好：

| 策略 | 优势 | 劣势 |
|------|------|------|
| 关键词 | 快、精确 | 找不到同义词 |
| 语义 | 理解含义 | 需要 embedding |
| 图遍历 | 发现关联 | 可能跑偏 |
| 时间衰减 | 优先近期 | 遗漏旧但重要的 |

**最佳实践：** 组合使用，加权合并结果。

## 实战：构建一个记忆系统

### Step 1: 最简实现（5 分钟）

```bash
# 用 agent-log 快速查找
agent-log search "数据库设计"
```

这已经是一个"记忆系统"——从历史中检索信息。

### Step 2: 加入结构化存储

```python
from memory_graph import MemoryGraph

mg = MemoryGraph("my_agent.db")

# 记住实体
user = mg.add("罗嵩", "person", {"role": "developer"})
project = mg.add("Memory System", "concept")

# 记住关系
mg.link(user.id, project.id, "builds")

# 检索
results = mg.recall("罗嵩")  # 找到用户和相关项目
```

### Step 3: 加入自动提取

```javascript
import { MemoryService } from './src';

const mem = new MemoryService({ dbPath: './memories.db' });

// 从对话自动提取记忆
await mem.extractFromConversation([
  { role: 'user', content: '我喜欢用 TypeScript' },
  { role: 'assistant', content: '好的' }
]);
// → 自动提取偏好 "喜欢用 TypeScript"，存入 L1

// 搜索
const results = await mem.search('编程语言偏好');
```

## 设计权衡

### 存储选择：SQLite vs 向量数据库 vs 纯文本

| 方案 | 优点 | 缺点 |
|------|------|------|
| **纯文本** (agent-log) | 零成本，grep 即可 | 无结构，难关联 |
| **SQLite** (本项目) | 轻量，嵌入式，SQL 查询 | 语义搜索需额外 embedding |
| **向量数据库** | 原生语义搜索 | 依赖重，运维成本 |

**我们的选择：** SQLite + 可选 embedding。生产级但不重。

### 衰减参数选择

```python
# 激进遗忘（适合高频交互）
decay_rate = 0.5, min_weight = 0.1, review_boost = 0.3

# 温和遗忘（适合长期项目）
decay_rate = 0.1, min_weight = 0.05, review_boost = 0.5
```

### 什么时候该忘记？

- ✅ 过时的技术决策（已被推翻）
- ✅ 临时上下文（"今天的天气"）
- ✅ 低频访问的操作细节
- ❌ 用户身份和核心偏好
- ❌ 重要的项目决策
- ❌ 安全相关的信息

---

## 延伸阅读

- [Ebbinghaus 遗忘曲线](https://en.wikipedia.org/wiki/Forgetting_curve)
- [Mem0: 生产级 AI 记忆](https://github.com/mem0ai/mem0)
- [Hindsight: 多策略记忆检索](https://arxiv.org/abs/2503.21766)
- [LangChain Memory 模块](https://python.langchain.com/docs/modules/memory/)

---

_最后更新: 2026-04-15_
