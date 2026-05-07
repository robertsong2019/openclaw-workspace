# HEARTBEAT.md - May 7, 2026 (Thursday)

## 待办任务

### 高优先级（本周）
- [ ] **创建 lab/openclaw-langgraph-bridge/** — createOpenClawNode() 工厂函数
  - 研究已完成, 3测试全通过(invoke+stream+动态复用)
  - 核心设计: executor 参数抽象 sessions_spawn
- [ ] **创建 lab/a2a-trust-prototype/** — Node.js ES256 签名中间件 + Trust Score 计算
  - 研究完成(三层信任模型), 代码验证通过
- [x] **创建 lab/openclaw-mcp-server/** ✅ 2026-05-02 (367a188)
- [ ] **AMS 生产化** — EmbeddingProvider真实接入(ONNX/远程API), Docker化

### 中优先级（本月）
- [ ] Hindsight Mini 原型 — lab/hindsight-mini/
- [ ] Agent Trust Network Web UI
- [ ] Edge Agent Runtime Dashboard

### 探索性（下季度）
- [ ] Edge Agent Runtime 增强
- [ ] Agent Mesh Network P2P通信协议

## 系统状态
- **AMS v1.0-dev**: 645/645 tests, embed cache: LRU+TTL+compact+embedBatch()
- **MemoryManager**: 200/200 tests (session lifecycle, _detect_project_name修复)
- **better-ralph-core**: 136/136 tests
- **agent-task-cli**: 408/408 tests
- **prompt-router**: 111/111 tests
- **prompt-weaver**: 148/148 tests
- **autoresearch**: 零回滚率持续保持（连续40天）🏆

## 近期发现
- AMS embedBatch() 批量嵌入: 去重+N→K调用+缓存感知+TTL安全 — 批量导入场景的性能关键
- MemoryManager _detect_project_name 从"截取文件名"改为"解析配置文件" — bug修复验证了集成测试的价值
- embed cache 四重管理闭环完成: LRU(大小) + TTL(新鲜度) + compact(恢复) + embedBatch(批量效率)
- **突破点**: 研究积累充足，本周重点是 lab/ 实现（A2A Trust + LangGraph Bridge）
