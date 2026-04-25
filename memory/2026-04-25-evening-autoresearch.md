# 2026-04-25 Evening — Autoresearch 实验循环

## Agent Memory Service — 3 Cycles, 0 Rollbacks ✅

### Cycle 1: topEntities(opts) — 415→421 tests (+6)
- 实体排名：按 count * avgWeight 排序
- 支持 limit, layer, minCount, topTags
- commit: c8ccc9d

### Cycle 2: tagSearch(query, opts) — 421→427 tests (+6)
- 模糊标签搜索：精确/前缀/子串/字符重叠评分
- 支持 limit, minScore
- commit: 0f2be50

### Cycle 3: memoryDiff(id1, id2) — 427→433 tests (+6)
- 两记忆对比：内容相似度 + 标签/实体/层级/权重差异
- 优雅处理缺失记忆
- commit: 1b2d111
- Bug: JSDoc 类型中多余 `]`，单行对象字面量中 `]}` 解析错误 → 拆为多行

### 汇总
- **总新增**: 18 tests, 3 APIs, ~90 lines src
- **零回滚率持续**: 连续 15 天
- **experiments.tsv**: 3 条 keep
