# HEARTBEAT.md - May 13, 2026 (Wednesday)

## 待办任务

### 高优先级（本周）
- [ ] **创建 lab/openclaw-langgraph-bridge/** — createOpenClawNode() 工厂函数
  - 研究已完成, 18/18 tests (Executor双模式 + createTask + BridgeState)
  - 核心设计: executor 参数抽象 sessions_spawn
- [ ] **创建 lab/a2a-trust-prototype/** — Node.js ES256 签名中间件 + Trust Score 计算
  - 研究完成(v1.2 spec + RFC 8785), 代码验证通过
- [ ] **创建 lab/structured-output-toolkit/** — StructuredLLMClient + SchemaCache
  - 05-10 深度研究完成, 5/5 tests, Ollama JSON mode + XGrammar
- [ ] **创建 lab/agent-observability/** — Tracer + PolicyEngine + Evaluator
  - 05-10 深度研究完成, 可运行 TS 代码
- [ ] **AMS 生产化** — EmbeddingProvider真实接入(ONNX/远程API), Docker化

### 中优先级（本月）
- [ ] Hindsight Mini 原型 — lab/hindsight-mini/ (TS原型已有，需接入agent-context-store)
- [ ] Agent Trust Network Web UI
- [ ] Edge Agent Runtime Dashboard

## 系统状态
- **AMS v1.0-dev**: 645/645 tests
- **better-ralph-core**: 285/285 tests
- **agent-context-store**: 76/76 tests (05-12 重建后基线)
- **agent-memory-graph**: 30/30 tests (NEW)
- **prompt-router**: 230/230 tests
- **prompt-weaver**: 148/148 tests
- **autoresearch**: 零回滚率持续保持（连续49天）🏆

## 近期发现
- **突破点**: 研究积累已饱和，本周重点是 lab/ 实现（Structured Output > Observability > Hindsight Mini > A2A Trust > LangGraph Bridge）
- agent-memory-graph 新项目: SQLite知识图谱+merge_nodes+shortest_path, 补充 AMS 图遍历能力
- better-ralph-core plan_batch() 是 run_batch() 的天然搭档: plan→execute→checkpoint→resume
- search_combined() 填补复合查询缺口, 避免多次搜索手动交集
