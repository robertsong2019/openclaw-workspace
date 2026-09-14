# 2026-09-14 (晚) — code-lab 实验循环 (afm)

## 总结
- 项目：**agent-memory-service (afm)**（24 天未循环，全库最长）
- 基线：724/724 ×2 绿 11.1s；coverage 98.59% line / 89% branch
- 3 cycles，全部 keep：724 → **738** (+14 tests, 0 fail)
- commits: bedcc38 (bug fix), aa5510f (contract ×7), 38c7681 (contract ×4)

## C1 — 真 bug（红×3 验证）
`validate()` 孤儿链接检测读 `link.sourceId/link.targetId`——**不存在的字段**（Link = `{source, target}`）。后果：每条健康链接被双报孤儿，`validate({repair:true})` **清空整个链接图**且 `repaired=2×N`。修复：读 source/target、每端点报一次、每链接删一次。
- 教训：测试断言 `includes('orphan')` 小写 vs 实际 `'Orphan'` 大写——自己的测试先错一次。

## C2/C3 — 零覆盖公开 API 契约钉定（诚实标注非 bug）
- `findByTimeRange` 整个函数体零覆盖；`compactBM25Index` 删除+保存路径零覆盖；`autoMaintain` 编排分支零覆盖。
- 契约发现：健康 store healthScore **恰好 100**，`threshold:100` 永不触发；`query()` 返回 `{results,total}` 不是数组（我自己第一次就踩了）。
- BM25 幽灵条目良性（searchBM25 有 `if (!m) continue` 过滤）。

## 环境备忘
- **afm 拓扑修正**：`projects/agent-memory-service/.git` 是空目录（假 own-repo）→ 实际归 monorepo，TOOLS.md 中"afm 有独立 .git"的说法过时（勿信缓存，逐目录实测）。
- `data/test-*` 测试产物在 monorepo 里显示 dirty（历史遗留被提交过）——**不要卷入 commit**，只 add 目标文件。
- node --test 目录模式（`node --test tests/`）1 fail 是误用；必须用 package script 的 glob 形式。

## 待办线索
- 剩余未覆盖小洞：411-412, 737-743, 802, 829-831, 877-882, 2142-2143, 2226, 2238-2240, 2809-2811, 5102-5103, 5210-5214, 5436-5437, 5485-5491（多为 2-3 行 error 分支）
- `validate()` 内死变量 `const byTag = this.#store.byTag('__check__')`（L2608）——tag 索引检查路径也未测，下轮候选
