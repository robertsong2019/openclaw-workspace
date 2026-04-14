# Agent Memory Service

> Mem0 风格的 Agent 记忆管理服务 — 自动提取、三层存储、语义检索

## 概述

从对话和交互中自动提取记忆，分层存储（短期/长期/核心），支持语义搜索和遗忘衰减。

灵感来源：
- **Mem0** — 三层存储 + 自动提取 pipeline
- **Hindsight** — 多策略检索 (91.4% 准确率)
- **Ebbinghaus 遗忘曲线** — 记忆衰减与复习增强

## 核心设计

### 三层存储

```
┌─────────────┐
│  Core (L0)   │ ← 身份、偏好、关键决策（永不过期）
├─────────────┤
│  Long (L1)   │ ← 项目、人物、经验（衰减周期30天）
├─────────────┤
│  Short (L2)  │ ← 近期对话、临时上下文（衰减周期1天）
└─────────────┘
```

### 记忆提取 Pipeline

```
对话/事件 → 提取器 → 分类 → 存储 → 索引
                ↓
         [实体/关系/事实/偏好/决策]
```

### 检索策略

1. **关键词** — 快速精确匹配
2. **语义** — embedding 相似度
3. **关联** — 图谱遍历（BFS/随机游走）
4. **时序** — 时间衰减加权

## 快速开始

```bash
cd agent-memory-service
npm install
npm test
```

## API

```typescript
import { MemoryService } from './src';

const mem = new MemoryService({ dbPath: './memories.db' });

// 添加记忆
await mem.add({
  content: '罗嵩正在研究 Mem0 框架的 API 设计',
  layer: 'long',
  tags: ['mem0', 'research']
});

// 从对话自动提取
await mem.extractFromConversation([
  { role: 'user', content: '我偏好用 TypeScript 写项目' },
  { role: 'assistant', content: '好的，已记录您的偏好' }
]);

// 搜索
const results = await mem.search('Mem0 API', { limit: 5 });

// 衰减
await mem.decay();
```

## 纯 Node.js，零外部依赖

仅使用 Node.js 内置模块（sqlite3 除外，通过 better-sqlite33）。

## License

MIT
