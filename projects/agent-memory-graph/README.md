# Agent Memory Graph

> 基于 SQLite 的轻量知识图谱，模拟 AI Agent 的长期记忆管理

## 🎯 概述

用知识图谱管理 Agent 的记忆——节点是概念/实体/事件，边是关系。核心特性：

- **记忆衰减** — 基于 Ebbinghaus 遗忘曲线，未访问的记忆逐渐弱化
- **访问增强** — 被 recall 的记忆强度恢复，模拟人类复习效果
- **关联遍历** — BFS 遍历记忆网络，发现关联上下文
- **零依赖** — 仅用 Python 标准库（sqlite3 + json + math）

## 快速开始

```bash
python memory_graph.py
```

无需安装任何依赖，直接运行即可看到演示。

## 核心概念

### 节点类型 (Kind)

| Kind | 用途 | 示例 |
|------|------|------|
| `fact` | 事实性知识 | "Python 是动态类型语言" |
| `event` | 事件记录 | "深夜 debug session" |
| `person` | 人物信息 | "罗嵩" |
| `concept` | 概念/想法 | "Rust 嵌入式 AI" |
| `skill` | 技能标签 | "Python 快速原型" |

### 记忆衰减机制

```python
# Ebbinghaus 遗忘曲线
weight = initial_weight × e^(-0.3 × elapsed_days)

# 每次访问恢复
weight = min(1.0, decayed_weight + 0.4)

# 低于阈值自动遗忘
MIN_WEIGHT = 0.05
```

## API 参考

### `MemoryGraph(db_path=":memory:")`

创建记忆图谱实例。

```python
mg = MemoryGraph()           # 内存数据库
mg = MemoryGraph("mem.db")   # 持久化到文件
```

### `add(label, kind="fact", data=None) -> Node`

添加记忆节点。

```python
node = mg.add("OpenClaw", "concept", {"lang": "TypeScript"})
```

### `link(source_id, target_id, relation, weight=1.0)`

建立节点间关系。

```python
mg.link(user.id, project.id, "works_on")
```

### `recall(query, limit=5) -> list[Node]`

按关键词召回记忆（自动增强访问强度）。

```python
results = mg.recall("Python")
for r in results:
    print(f"{r.label} (weight={r.weight:.2f})")
```

### `neighbors(node_id, depth=1) -> list[Node]`

BFS 遍历获取关联记忆。

```python
related = mg.neighbors(user.id, depth=2)
```

### `decay_all()`

对所有记忆应用遗忘衰减，清除已遗忘节点。

### `stats() -> dict`

返回记忆网络统计（节点数、边数、平均强度、类型分布）。

### `visualize_ascii() -> str`

终端可视化，显示记忆强度条形图和关系图。

## 设计思路

这个项目是一个**概念原型**，探索几个问题：

1. **Agent 记忆应该用什么结构？** — 图谱比列表更适合表达关联
2. **如何避免记忆膨胀？** — 遗忘曲线是自然的"垃圾回收"
3. **如何模拟人类回忆？** — recall 时增强 + 关联遍历 = 上下文感知

## 可能的扩展

- [ ] 语义搜索（embedding 替代关键词匹配）
- [ ] 摘要压缩（长期未访问的记忆自动摘要）
- [ ] 可视化 UI（Web 图谱浏览器）
- [ ] 与 LLM 集成（自动提取实体和关系）

## 许可

MIT
