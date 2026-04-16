# Getting Started - OpenClaw Workspace

> 从零开始,快速上手你的 AI Agent 工作区

## 🎯 这是什么?

这是一个集成了多种 AI Agent 工具、技能和实验项目的工作区。每个组件都可以独立使用,也可以组合起来构建强大的 AI 应用。

**核心价值:**
- 🛠️ **工具集** - 项目管理、任务编排、记忆搜索等实用工具
- 🤖 **技能库** - 可直接在 OpenClaw 中使用的技能
- 🧪 **实验室** - 探索 AI Agent 前沿技术的实验项目
- 📚 **知识库** - 学习 AI Agent 开发的最佳实践

## 🚀 快速开始(5分钟)

### 1. 了解工作区结构

```
.openclaw/workspace/
├── projects/           # 🛠️ 主要工具项目
│   ├── agent-task-cli/     # 多 Agent 任务编排 CLI
│   ├── mission-control/    # Agent 监控仪表板
│   └── prompt-mgr/         # Prompt 管理系统
├── skills/             # 🤖 OpenClaw 技能
│   ├── akshare-finance/    # 财经数据接口
│   ├── finance-news-pro/   # 财经新闻聚合
│   ├── memory-manager/     # 记忆管理
│   └── ...                 # 更多技能
├── experiments/        # 🧪 实验项目
│   ├── local-embedding-memory/   # 语义搜索
│   ├── agent-trust-network/      # 信任网络
│   └── agent-workflow-viz/       # 工作流可视化
└── memory/             # 📝 工作区记忆
    ├── MEMORY.md           # 长期记忆
    ├── episodic/           # 事件记忆
    ├── semantic/           # 语义记忆
    └── procedural/         # 过程记忆
```

### 2. 选择你的起点

#### 🎓 **初学者路径**

**目标:** 理解 AI Agent 的核心概念

1. **学习 12-Factor Agents**
   ```bash
   # 打开交互式探索器
   open index.html
   ```
   - 位置: `index.html` (工作区根目录)
   - 时间: 20-30 分钟
   - 学习: AI Agent 的 12 个核心原则

2. **探索记忆系统**
   ```bash
   cd skills/memory-manager
   cat README.md
   ```
   - 了解: Episodic/Semantic/Procedural 记忆架构
   - 理解: 为什么结构化记忆比扁平文件更好

3. **运行第一个实验**
   ```bash
   cd experiments/local-embedding-memory
   pip install sentence-transformers numpy
   python memory_embedder.py --index
   python memory_embedder.py --search "AI Agent"
   ```
   - 体验: 语义搜索的威力
   - 时间: 10 分钟

#### 🛠️ **开发者路径**

**目标:** 使用工具提升开发效率

1. **安装 Agent Task CLI**
   ```bash
   cd projects/agent-task-cli
   npm install
   npm link
   agent-task patterns  # 查看可用的编排模式
   ```

2. **运行第一个多 Agent 任务**
   ```bash
   cd projects/agent-task-cli/examples
   agent-task run work-crew.yaml --dry-run
   ```
   - 了解: 5 种编排模式(Work Crew/Supervisor/Pipeline/Council/Auto-Routing)
   - 时间: 15 分钟

3. **创建自定义任务**
   ```yaml
   # my-task.yaml
   name: "Research Project"
   pattern: "work-crew"
   agents:
     - name: "researcher"
       role: "Research technical aspects"
     - name: "analyst"
       role: "Analyze business impact"
   task: "Research AI Agent frameworks"
   ```
   ```bash
   agent-task run my-task.yaml
   ```

#### 🔬 **实验者路径**

**目标:** 探索前沿技术

1. **语义记忆搜索**
   ```bash
   cd experiments/local-embedding-memory
   python web_ui.py --port 8080
   # 打开 http://localhost:8080
   ```
   - 功能: 实时语义搜索、对比模式
   - 文档: `TUTORIAL.md` (30 分钟教程)

2. **信任网络模拟**
   ```bash
   cd experiments/agent-trust-network
   npm install
   npm run demo
   ```
   - 学习: 去中心化信任机制
   - 实验: 不同 Agent 行为模式的影响
   - 文档: `TUTORIAL.md` (完整的教程)

3. **集成演示**
   ```bash
   cd projects/agent-task-cli/examples
   python integration-demo.py
   ```
   - 查看: 工具如何协同工作
   - 学习: 真实应用场景

### 3. 选择你的使用场景

#### 📊 **场景 1: 财经数据分析**

```bash
# 安装技能
cd skills/akshare-finance
pip install akshare pandas

# 获取股票数据
python -c "import akshare as ak; print(ak.stock_zh_a_spot_em())"

# 聚合财经新闻
cd ../finance-news-pro
python fetch_news.py
```

**相关文档:**
- `skills/akshare-finance/SKILL.md`
- `skills/finance-news-pro/README.md`

#### 🤖 **场景 2: 多 Agent 协作**

```bash
# 创建任务
cd projects/agent-task-cli
agent-task run examples/supervisor.yaml

# 监控进度
agent-task monitor <task-id>

# 导出结果
agent-task export <task-id> --format markdown
```

**相关文档:**
- `projects/agent-task-cli/README.md`
- `projects/agent-task-cli/examples/README.md`

#### 🧠 **场景 3: AI 记忆增强**

```bash
# 设置记忆结构
cd skills/memory-manager
./init.sh

# 语义搜索记忆
cd ../../experiments/local-embedding-memory
python memory_embedder.py --index
python memory_embedder.py --search "project decisions"
```

**相关文档:**
- `skills/memory-manager/README.md`
- `experiments/local-embedding-memory/TUTORIAL.md`

#### 🌐 **场景 4: 信任网络**

```bash
# 运行信任网络模拟
cd experiments/agent-trust-network
npm run demo

# 自定义网络
# 编辑 src/demo.ts 或创建自己的模拟
```

**相关文档:**
- `experiments/agent-trust-network/TUTORIAL.md`
- `experiments/agent-trust-network/API.md`

## 📚 学习路径

### 初级(1-2 天)

1. ✅ 完成 12-Factor Agents 交互式学习
2. ✅ 理解记忆系统架构
3. ✅ 运行 local-embedding-memory 实验
4. ✅ 使用 agent-task-cli 基础功能

### 中级(3-5 天)

1. ✅ 创建自定义 agent-task 任务
2. ✅ 集成多个工具
3. ✅ 运行 agent-trust-network 实验
4. ✅ 探索财经数据技能

### 高级(1-2 周)

1. ✅ 开发自定义 OpenClaw 技能
2. ✅ 扩展 agent-task-cli 功能
3. ✅ 实现自定义记忆系统
4. ✅ 构建真实应用

## 🛠️ 常用命令速查

### Agent Task CLI

```bash
agent-task run <file>           # 运行任务
agent-task list                 # 列出所有任务
agent-task monitor <task-id>    # 监控任务
agent-task export <task-id>     # 导出结果
agent-task patterns             # 查看编排模式
```

### Memory Manager

```bash
./init.sh                       # 初始化记忆结构
./detect.sh                     # 检查压缩风险
./organize.sh                   # 组织记忆文件
./search.sh <type> <query>      # 按类型搜索
./stats.sh                      # 查看统计
```

### Local Embedding Memory

```bash
python memory_embedder.py --index              # 索引记忆
python memory_embedder.py --search "query"     # 搜索
python memory_embedder.py --compare "query"    # 对比搜索
python web_ui.py --port 8080                   # 启动 Web UI
```

### Finance Tools

```bash
# AKShare
python -c "import akshare as ak; print(ak.stock_zh_a_spot_em())"

# Finance News Pro
python fetch_news.py --source cls,wallstreet
python fetch_news.py --keyword "AI,新能源"
```

## 🔍 故障排除

### 问题 1: 依赖安装失败

```bash
# Python 依赖
pip install -r requirements.txt --upgrade

# Node.js 依赖
npm install --force
```

### 问题 2: 命令未找到

```bash
# 确保 npm link 成功
cd projects/agent-task-cli
npm link

# 验证
which agent-task
```

### 问题 3: 权限错误

```bash
# 给脚本执行权限
chmod +x skills/memory-manager/*.sh
```

### 问题 4: 模型下载慢

```bash
# 使用国内镜像
export HF_ENDPOINT=https://hf-mirror.com
```

## 📖 深入学习

### 推荐阅读顺序

1. **基础概念**
   - `index.html` - 12-Factor Agents
   - `skills/memory-manager/README.md` - 记忆架构

2. **工具使用**
   - `projects/agent-task-cli/README.md` - CLI 完整文档
   - `experiments/local-embedding-memory/TUTORIAL.md` - 语义搜索教程

3. **高级主题**
   - `experiments/agent-trust-network/TUTORIAL.md` - 信任网络
   - `catalyst-research/exploration-notes/` - 探索笔记

### 外部资源

- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) - 原始项目
- [AKShare 文档](https://akshare.akfamily.xyz/) - 财经数据 API
- [Sentence Transformers](https://www.sbert.net/) - 嵌入模型库
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) - 框架源码

## 🤝 贡献指南

想要改进这个工作区?

1. **改进文档** - 修复错误、添加示例
2. **报告问题** - 在 `memory/` 中记录发现的问题
3. **添加技能** - 创建新的 OpenClaw 技能
4. **分享经验** - 在 `catalyst-research/exploration-notes/` 中记录你的探索

详见: `CONTRIBUTING.md`

## 📞 获取帮助

- **文档问题**: 检查对应的 README.md 或 TUTORIAL.md
- **工具使用**: 查看项目的 `--help` 或 API 文档
- **概念理解**: 阅读 `catalyst-research/exploration-notes/` 中的笔记
- **Bug 报告**: 记录在 `memory/` 或提交 issue

## 🎯 下一步

根据你的目标选择:

- **学习 AI Agent**: 从 `index.html` 开始
- **提升效率**: 试用 `agent-task-cli`
- **探索前沿**: 运行 `experiments/` 中的项目
- **财经分析**: 使用 `skills/akshare-finance`

---

**祝你探索愉快!** 🚀

*最后更新: 2026-03-24*
