# 2026-09-23 23:00 kd-1 — C600 species_total face (keep edcc784/77e0b8b)

## Cycle
- Lane: kd queue #2 **affe2881 bird species**（GT '32'，qtype knowledge-update）——queue #1 faith-days 因语义类别+十二月窗+句式 GT 最重而顺延
- Mechanism: running-total **declaration 构造** `"brings my total ... count to N"`（gap ≤3 词）+ species|bird 同句 topic wall；user role only；冲突弃权/同值去重（C598 cum_total 家族）
- Key insight: knowledge-update 对（May 24 snapshot "27 so far" → May 29 declaration "32"）用**构造语义**直接解析新值，无需 session dating/recency 仲裁；stale snapshot 构造上永不 key
- Loop: census-first（head 恰 1/500、in-row evidence 恰 {32}）→ TDD 红（ImportError 14 miniatures, verbatim fixtures）→ 绿 14/14 → suite **11043**（+14，pytest 272s，零漂移）→ full-500 replay **PASS 首试**（pred 变化恰 {affe2881}：27-echo→'32'；drift 恰 1 False→True；banked **353→354=0.708**，36 连 keep；abs 18 冻结）
- Commits: edcc784（face+tests，3 hunks 66 insertions，add 前 diff 审计）→ 77e0b8b（tsv 行 711 尾部断言 C599→C600）
- Chain: /tmp/c600/live500_c600.json（新权威）；artifacts /tmp/c600/*

## 🐛 Discovered bug（C501 遗留，非本 cycle 修复）
- 6ef39db「删除demo函数减少代码行数(1行)」删掉了 memory_graph.py 的 `def demo():` 行 → demo 函数体孤儿落入前一 class 的 class-scope → **import memory_graph（连带 amg_bench_quality）即执行 demo**（横幅 art ×2 + MemoryGraph() DB 副作用在 import 时发生）
- `if __name__ == "__main__": demo()` 守卫仍在 → 直跑 memory_graph.py 会 NameError（demo 未定义）
- 证据：C599 suite_out.txt / replay.log 就有横幅（每进程一次 import = 一次 demo；banner ×2 是 demo 内部双 print，非跑了两次）
- 影响：eval 链无害（cosmetic noise）；但 MCP stdio server 场景 = 协议流污染风险
- 修复（1 行补回 def demo():）**blocked 本 cycle**：memory_graph.py 带 44 天 `_search_cache` 脏 hunk（+24 行未提交），git add 会整体卷入——需独立 cycle 做脏 hunk 手术（stash 或逐 hunk add）

## kd queue next
- 5a7937c8 faith days December（GT '3 days.'——句式 GT 渲染对齐）
- d682f1a2 food delivery（GT 3，distinct-brand counting）
- memory_graph.py demo-orphan 修复（脏 hunk 手术）
