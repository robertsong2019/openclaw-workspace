# HEARTBEAT.md - May 2, 2026 (Saturday)

## 待办任务

### 高优先级（本周）
- [x] **创建 lab/openclaw-mcp-server/** — TypeScript SDK + Streamable HTTP, 3 tools MVP ✅ 2026-05-02 (367a188)
  - 完成: McpServer + registerTool(), StreamableHTTPServerTransport (stateful), 5/5 integration tests
  - 下一步: 接入真实 memory_search/tavily_search API, Resources+Prompts
- [ ] **创建 lab/openclaw-langgraph-bridge/** — createOpenClawNode() 工厂函数
  - 研究已完成, 3测试全通过(invoke+stream+动态复用)
  - 核心设计: executor 参数抽象 sessions_spawn
- [ ] **AMS 生产化** — EmbeddingProvider真实接入(ONNX/远程API), Docker化
- [ ] **A2A Agent Trust 集成原型** - Agent Card嵌入信任元数据

### 中优先级（本月）
- [ ] AMS: embedding cache sync (类似 BM25 dirty-tracking)
- [ ] Hindsight Mini 原型 — lab/hindsight-mini/
- [ ] Agent Trust Network Web UI
- [ ] Edge Agent Runtime Dashboard

### 探索性（下季度）
- [ ] Edge Agent Runtime 增强
- [ ] Agent Mesh Network P2P通信协议

## 系统状态
- **AMS v1.0-dev**: 640/640 tests, BM25持久化+sync修复+分支管道完整
- **agent-task-cli**: 380/380 tests
- **prompt-router**: 34/34 tests
- **autoresearch**: 零回滚率持续保持（连续30天）🏆

## 近期发现
- AMS BM25 sidecar 模式成熟: 持久化 → 同步修复 → 孤立清理 → 可复用于 embedding cache
- delete/batchDelete 的 BM25 同步是易遗漏的 bug — dirty flag 模式是防御手段
- LangGraph.js v1.2.9 StateSchema + ReducedValue 新 API 比 Annotation.Root 更清晰
- 两个 lab 项目准备就绪: MCP Server + LangGraph Bridge (研究阶段全部完成)
- 下一步突破点: 从研究转向实现, 两个 lab 项目动手
