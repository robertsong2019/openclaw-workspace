# HEARTBEAT.md - May 17, 2026 (Sunday)

## 待办任务

### 高优先级（本周）
- [ ] **创建 lab/openclaw-langgraph-bridge/** — createOpenClawNode() 工厂函数
  - 研究已完成, 18/18 tests (Executor双模式 + createTask + BridgeState)
- [ ] **创建 lab/a2a-trust-prototype/** — Node.js ES256 签名中间件 + Trust Score
- [ ] **创建 lab/structured-output-toolkit/** — StructuredLLMClient + SchemaCache
- [ ] **创建 lab/agent-observability/** — Tracer + PolicyEngine + Evaluator
- [ ] **AMS 生产化** — EmbeddingProvider真实接入(ONNX/远程API), Docker化

### 中优先级（本月）
- [ ] Hindsight Mini 原型 — lab/hindsight-mini/ (TS原型已有，需接入agent-context-store)
- [ ] Agent Trust Network Web UI
- [ ] Edge Agent Runtime Dashboard

## 系统状态
- **agent-context-store**: 186/186 tests (新增: event hooks on/off/_emit + xrefs)
- **better-ralph-core**: 307/307 tests (新增: story_digest + checkpoint_diff)
- **lab/agent-observability**: 60/60 tests (实现中: Tracer因果链接 + Evaluator回归检测 + Policy批量评估 + Observer同步模式)
- **AMS v1.0-dev**: 645/645 tests
- **agent-memory-graph**: 30/30 tests
- **prompt-router**: 244/244 tests
- **prompt-weaver**: 148/148 tests
- **autoresearch**: 零回滚率持续保持（连续58天）🏆

## 近期发现
- **agent-context-store event hooks** 实现了 pub/sub 模式，解耦 changelog(审计) 与 hooks(响应)，为 agent 自动同步奠定基础
- **story_digest** 是单调用状态快照，填补 get_status(轻量) 与 get_session_summary(详细) 之间的缺口
- **lab/agent-observability 已启动实现**: 60 tests 覆盖因果链接追踪、回归检测、批量策略评估、同步观察——这是第一个从研究笔记进入 lab/ 的项目
- 下周目标: agent-observability 继续迭代 + 启动 Hindsight Mini lab 实现
