# API Reference Index

> 所有项目、技能和实验的 API 文档索引

## 📚 目录

- [核心项目](#核心项目)
- [OpenClaw 技能](#openclaw-技能)
- [实验项目](#实验项目)
- [工具函数](#工具函数)

---

## 核心项目

### 1. Agent Task CLI

**位置:** `projects/agent-task-cli/`

**文档:**
- [README.md](projects/agent-task-cli/README.md) - 完整使用指南
- [API Documentation](projects/agent-task-cli/README.md#api-usage) - Node.js API

**主要 API:**

```javascript
const { Orchestrator, Patterns } = require('agent-task-cli');

// 创建编排器
const orchestrator = new Orchestrator();

// 运行任务
const task = await orchestrator.run({
  name: "My Task",
  pattern: "work-crew",
  agents: [...],
  task: "Description"
});

// 监控进度
task.on('progress', (update) => console.log(update));

// 获取结果
const results = await task.results;
```

**可用模式:**
- `WorkCrewPattern` - 并行工作模式
- `SupervisorPattern` - 监督者模式
- `PipelinePattern` - 流水线模式
- `CouncilPattern` - 委员会模式
- `AutoRoutingPattern` - 自动路由模式

**详细文档:** [projects/agent-task-cli/README.md](projects/agent-task-cli/README.md)

---

### 2. Mission Control

**位置:** `projects/mission-control/`

**文档:**
- [README.md](projects/mission-control/README.md) - 项目概览

**状态:** 早期开发阶段

---

### 3. Prompt Manager

**位置:** `projects/prompt-mgr/`

**文档:**
- [Tutorial](projects/prompt-mgr/docs/TUTORIAL.md) - 使用教程

---

## OpenClaw 技能

### 1. AKShare Finance

**位置:** `skills/akshare-finance/`

**文档:**
- [SKILL.md](skills/akshare-finance/SKILL.md) - 技能说明和 API 示例

**主要功能:**

```python
import akshare as ak

# 股票行情
ak.stock_zh_a_spot_em()           # A 股实时
ak.stock_zh_kline(symbol="000001", period="daily")

# 宏观经济
ak.macro_china_gdp()              # GDP
ak.macro_china_cpi()              # CPI
ak.macro_china_pmi()              # PMI

# 加密货币
ak.crypto_binance_btc_usdt_spot() # BTC/USDT

# 外汇贵金属
ak.forex_usd_cny()                # 美元兑人民币
```

**详细文档:** [skills/akshare-finance/SKILL.md](skills/akshare-finance/SKILL.md)

---

### 2. Finance News Pro

**位置:** `skills/finance-news-pro/`

**文档:**
- [README.md](skills/finance-news-pro/README.md) - 功能说明和配置

**主要功能:**

```bash
# 基础使用
python fetch_news.py

# 指定数据源
python fetch_news.py --source cls,wallstreet

# 关键词过滤
python fetch_news.py --keyword "AI,算力"
```

**详细文档:** [skills/finance-news-pro/README.md](skills/finance-news-pro/README.md)

---

### 3. Memory Manager

**位置:** `skills/memory-manager/`

**文档:**
- [README.md](skills/memory-manager/README.md) - 架构说明和使用指南

**主要命令:**

```bash
./init.sh                       # 初始化记忆结构
./detect.sh                     # 检查压缩风险
./organize.sh                   # 组织记忆文件
./search.sh <type> <query>      # 按类型搜索
./snapshot.sh                   # 创建快照
./stats.sh                      # 查看统计
```

**记忆类型:**
- **Episodic** - 事件记忆(时间序列)
- **Semantic** - 语义记忆(事实和概念)
- **Procedural** - 过程记忆(工作流和流程)

**详细文档:** [skills/memory-manager/README.md](skills/memory-manager/README.md)

---

### 4. Ralph Autonomous Agent Loop

**位置:** `skills/ralph-autonomous-agent-loop/`

**文档:**
- [SKILL.md](skills/ralph-autonomous-agent-loop/SKILL.md) - 完整教程和配置

**主要功能:**

```bash
# 运行 Ralph 循环
./scripts/ralph/ralph.sh

# 指定迭代次数
./scripts/ralph/ralph.sh 20

# 使用 Claude Code
./scripts/ralph/ralph.sh --tool claude 15
```

**核心概念:**
- `prd.json` - 任务列表和状态
- `progress.txt` - 学习记录
- 增量迭代直到所有任务完成

**详细文档:** [skills/ralph-autonomous-agent-loop/SKILL.md](skills/ralph-autonomous-agent-loop/SKILL.md)

---

## 实验项目

### 1. Local Embedding Memory

**位置:** `experiments/local-embedding-memory/`

**文档:**
- [README.md](experiments/local-embedding-memory/README.md) - 项目概览
- [TUTORIAL.md](experiments/local-embedding-memory/TUTORIAL.md) - 30 分钟教程
- [API.md](experiments/local-embedding-memory/API.md) - API 参考

**Python API:**

```python
from memory_embedder import MemoryEmbedder

# 初始化
embedder = MemoryEmbedder(memory_dir="../memory")

# 索引
embedder.build_index()

# 搜索
results = embedder.search("query", top_k=5)

# 结果
for result in results:
    print(f"[{result.score:.3f}] {result.file_path}: {result.section}")
    print(result.content)
```

**CLI 命令:**

```bash
python memory_embedder.py --index              # 索引
python memory_embedder.py --search "query"     # 搜索
python memory_embedder.py --compare "query"    # 对比模式
python web_ui.py --port 8080                   # Web UI
```

**详细文档:**
- [完整教程](experiments/local-embedding-memory/TUTORIAL.md)
- [API 参考](experiments/local-embedding-memory/API.md)

---

### 2. Agent Trust Network

**位置:** `experiments/agent-trust-network/`

**文档:**
- [README.md](experiments/agent-trust-network/README.md) - 项目概览
- [TUTORIAL.md](experiments/agent-trust-network/TUTORIAL.md) - 30 分钟教程
- [API.md](experiments/agent-trust-network/API.md) - API 参考

**TypeScript API:**

```typescript
import { Agent, TrustNetwork } from './src';

// 创建 Agent
const agent = new Agent({
  id: 'agent-1',
  name: 'Alice',
  behavior: 'cooperative',
  reliability: 0.95
});

// 创建网络
const network = new TrustNetwork({
  dampingFactor: 0.85,
  trustDecayRate: 0.001
});

// 添加 Agent
network.addAgent(agent);

// 建立信任关系
network.setTrustRelation('agent-1', 'agent-2', 0.8);

// 模拟交互
const result = network.simulateInteraction('agent-1', 'agent-2', 0.5);

// 计算信任分数
network.calculateTrustScores();

// 获取可信 Agent
const trusted = network.getTrustedAgents(0.7);

// 识别恶意 Agent
const malicious = network.identifyMaliciousAgents(0.3);
```

**详细文档:**
- [完整教程](experiments/agent-trust-network/TUTORIAL.md)
- [API 参考](experiments/agent-trust-network/API.md)

---

### 3. Agent Workflow Visualization

**位置:** `experiments/agent-workflow-viz/`

**文档:**
- [CONTRIBUTING.md](experiments/agent-workflow-viz/CONTRIBUTING.md) - 贡献指南

**状态:** 早期开发阶段

---

## 工具函数

### 项目上下文生成器

**位置:** `tools/project-context-generator/`

**功能:** 生成 AI 就绪的项目上下文摘要

```bash
python tools/project-context-generator/generate_context.py /path/to/project
```

**输出:** Markdown 格式的项目摘要,适合 AI Agent 快速理解项目

---

### 项目仪表板生成器

**位置:** `tools/project-dashboard-generator/`

**功能:** 多项目健康状态追踪

```bash
python tools/project-dashboard-generator/generate_dashboard.py /path/to/workspace
```

**输出:** 
- `projects-dash.md` - 项目健康报告
- `experiments-dash.md` - 实验健康报告

---

## 快速查找

### 按功能查找

| 功能 | 项目/技能 | 文档位置 |
|------|----------|----------|
| **多 Agent 编排** | agent-task-cli | [README](projects/agent-task-cli/README.md) |
| **语义搜索** | local-embedding-memory | [TUTORIAL](experiments/local-embedding-memory/TUTORIAL.md) |
| **信任网络** | agent-trust-network | [TUTORIAL](experiments/agent-trust-network/TUTORIAL.md) |
| **财经数据** | akshare-finance | [SKILL](skills/akshare-finance/SKILL.md) |
| **新闻聚合** | finance-news-pro | [README](skills/finance-news-pro/README.md) |
| **记忆管理** | memory-manager | [README](skills/memory-manager/README.md) |
| **自主 Agent** | ralph-loop | [SKILL](skills/ralph-autonomous-agent-loop/SKILL.md) |
| **项目摘要** | context-generator | [使用说明](tools/project-context-generator/) |
| **健康监控** | dashboard-generator | [使用说明](tools/project-dashboard-generator/) |

### 按类型查找

| 类型 | 项目 | 文档 |
|------|------|------|
| **CLI 工具** | agent-task-cli | [README](projects/agent-task-cli/README.md) |
| **Python 库** | local-embedding-memory | [API.md](experiments/local-embedding-memory/API.md) |
| **TypeScript 库** | agent-trust-network | [API.md](experiments/agent-trust-network/API.md) |
| **Shell 脚本** | memory-manager | [README](skills/memory-manager/README.md) |
| **OpenClaw 技能** | 所有 skills/ | 各自的 SKILL.md |

---

## 常见 API 模式

### 初始化和配置

大多数项目遵循类似的初始化模式:

```python
# Python 项目
from module import MainClass

instance = MainClass(
    config_param_1="value1",
    config_param_2="value2"
)
```

```typescript
// TypeScript 项目
import { MainClass } from 'module';

const instance = new MainClass({
  configParam1: 'value1',
  configParam2: 'value2'
});
```

### 搜索和查询

```python
# 搜索模式
results = searcher.search(
    query="search query",
    top_k=5,
    filters={"type": "episodic"}
)

# 结果处理
for result in results:
    print(result.score, result.content)
```

### 任务执行

```javascript
// 任务运行模式
const task = await orchestrator.run(taskConfig);

// 监听事件
task.on('progress', (update) => { /* ... */ });
task.on('complete', (results) => { /* ... */ });
task.on('error', (error) => { /* ... */ });

// 等待结果
const finalResults = await task.results;
```

---

## API 版本说明

- **agent-task-cli**: v1.0.0
- **local-embedding-memory**: v1.0.0
- **agent-trust-network**: v1.0.0
- **akshare-finance**: v1.0.0
- **finance-news-pro**: v1.0.0
- **memory-manager**: v1.0.0

---

## 获取帮助

1. **查看具体文档** - 每个项目都有详细的 README 和 TUTORIAL
2. **检查示例** - 大多数项目有 `examples/` 目录
3. **阅读代码** - 代码注释和类型定义提供额外信息
4. **查看测试** - 测试文件展示 API 使用方式

---

*最后更新: 2026-03-24*
