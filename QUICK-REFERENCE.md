# Quick Reference Card

> 一页纸速查手册 - 打印友好版

---

## 🚀 5 分钟快速开始

```bash
# 1. 查看 12-Factor Agents
open index.html

# 2. 运行语义搜索
cd experiments/local-embedding-memory
pip install sentence-transformers numpy
python memory_embedder.py --index
python memory_embedder.py --search "AI Agent"

# 3. 运行多 Agent 任务
cd projects/agent-task-cli
npm install && npm link
agent-task run examples/work-crew.yaml
```

---

## 📚 核心文档

| 文档 | 位置 | 用途 |
|------|------|------|
| **入门指南** | GETTING-STARTED.md | 新用户起点 |
| **API 索引** | API-REFERENCE.md | 查找 API 文档 |
| **维护指南** | DOCUMENTATION-GUIDE.md | 文档标准 |
| **项目概览** | README.md | 工作区介绍 |

---

## 🛠️ 常用命令

### Agent Task CLI

```bash
agent-task patterns              # 查看模式
agent-task run <file>           # 运行任务
agent-task list                 # 列出任务
agent-task monitor <id>         # 监控任务
agent-task export <id>          # 导出结果
```

### Memory Manager

```bash
./init.sh                       # 初始化
./detect.sh                     # 检查风险
./organize.sh                   # 组织文件
./search.sh <type> <query>      # 搜索
./stats.sh                      # 统计
```

### Local Embedding Memory

```bash
python memory_embedder.py --index              # 索引
python memory_embedder.py --search "query"     # 搜索
python memory_embedder.py --compare "query"    # 对比
python web_ui.py --port 8080                   # Web UI
```

### Finance Tools

```bash
# AKShare
python -c "import akshare as ak; print(ak.stock_zh_a_spot_em())"

# Finance News
python fetch_news.py --source cls,wallstreet
python fetch_news.py --keyword "AI,新能源"
```

---

## 🎯 5 种编排模式

| 模式 | 用途 | 示例 |
|------|------|------|
| **Work Crew** | 多视角分析 | 产品评估、创意生成 |
| **Supervisor** | 大型任务 | 功能开发、项目管理 |
| **Pipeline** | 流程化任务 | 内容创作、数据处理 |
| **Council** | 重要决策 | 伦理评估、战略规划 |
| **Auto-Routing** | 混合任务 | 智能客服、通用助手 |

---

## 📁 项目结构

```
workspace/
├── projects/           # 主要工具
│   ├── agent-task-cli/     # 多 Agent 编排
│   ├── mission-control/    # 监控仪表板
│   └── prompt-mgr/         # Prompt 管理
├── skills/             # OpenClaw 技能
│   ├── akshare-finance/    # 财经数据
│   ├── finance-news-pro/   # 新闻聚合
│   ├── memory-manager/     # 记忆管理
│   └── ralph-loop/         # 自主 Agent
├── experiments/        # 实验项目
│   ├── local-embedding-memory/   # 语义搜索
│   ├── agent-trust-network/      # 信任网络
│   └── agent-workflow-viz/       # 工作流可视化
└── memory/             # 工作区记忆
    ├── MEMORY.md           # 长期记忆
    ├── episodic/           # 事件记忆
    ├── semantic/           # 语义记忆
    └── procedural/         # 过程记忆
```

---

## 🎓 学习路径

### 初级 (1-2 天)
- [ ] 完成 12-Factor Agents 交互学习
- [ ] 理解记忆系统架构
- [ ] 运行 local-embedding-memory 实验

### 中级 (3-5 天)
- [ ] 使用 agent-task-cli 创建任务
- [ ] 运行 agent-trust-network 实验
- [ ] 探索财经数据技能

### 高级 (1-2 周)
- [ ] 开发自定义 OpenClaw 技能
- [ ] 扩展 agent-task-cli 功能
- [ ] 构建真实应用

---

## 🔍 故障排除

### 安装失败
```bash
npm install --force
# 或
pip install --upgrade -r requirements.txt
```

### 命令未找到
```bash
npm link
which agent-task
```

### 权限错误
```bash
chmod +x skills/memory-manager/*.sh
```

### 模型下载慢
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

---

## 📞 获取帮助

1. **查看文档:** README.md, TUTORIAL.md, API.md
2. **检查示例:** examples/ 目录
3. **查看代码:** 注释和类型定义
4. **查看测试:** 测试文件展示用法
5. **记录问题:** 在 memory/ 中记录

---

## 🌐 快速链接

- [入门指南](GETTING-STARTED.md)
- [API 参考](API-REFERENCE.md)
- [文档维护](DOCUMENTATION-GUIDE.md)
- [Agent Task 教程](projects/agent-task-cli/TUTORIAL.md)
- [记忆搜索教程](experiments/local-embedding-memory/TUTORIAL.md)
- [信任网络教程](experiments/agent-trust-network/TUTORIAL.md)

---

## 💡 最佳实践

### 选择编排模式
- 多视角 → Work Crew
- 大任务 → Supervisor
- 流程化 → Pipeline
- 重大决策 → Council
- 混合任务 → Auto-Routing

### 记忆管理
- Episodic: 事件和时间
- Semantic: 事实和概念
- Procedural: 流程和工作流

### 文档维护
- 定期审查(每月)
- 收集反馈
- 保持更新
- 使用模板

---

**打印提示:** 此文档为打印友好格式,适合作为速查手册。

*最后更新: 2026-03-24*
