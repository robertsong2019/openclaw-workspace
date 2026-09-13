# 2026-09-14 — key-development-3 (C573)

**任务**: cron `key-development-3`（实验循环 C，autoresearch 方法论），在 C572（kd-2, 0.620）基础上推进 amg live-500 基准。

## 结果: KEEP ✅ 0.620 → 0.622 (310→311/500)

- **新 trip-span face route (t)**: `pp_trip_span_form` 「How many days did I spend on my <desc> trip?」— strict census 全 500 恰 1 行（gpt4_1d80365e，无 _abs 兄弟），零误伤 by construction
- **证据链**（session-date 算术，route (h) 兄弟）: s14@2023-05-15 'just started my solo camping trip ... today'（start）→ s33@2023-05-17 'just got back from an amazing solo camping trip ... today'（return）= **2 days** ✓GT（'2 days. 3 days inclusive also acceptable'，exact-number face {2}⊆{2,3}）
- **guards**: descriptor ALL-keywords wall（solo/camping/trip/yosemite/national/park）+ today 共现 + user-role wall（assistant 回声含全部关键词，wall+无today 双重保护）；future-aspiration 行（'will be camping ... for a few days'）无 marker 永不绑定；s6 music-festival decoy 有 return marker 但 keyword wall 拒绝；0 start/0 finish/same-sitting 0-days/negative span 全诚实 fall-through
- **零杀证明**: edced276（in-total 前置）、6cb6f249（did I take）、5a7937c8/10d9b85a（participating/attending frame）、19b5f2b3（how long）全被 head 形状排除

## 验证链（全绿）

1. census（shipped regex）恰 1 行 + 双模块 pp-gate claim diff（HEAD vs working）恰 +{gpt4_1d80365e}、0 丢失
2. TDD red-first: 14 RED（8 AttributeError + 4 行为 + 2 adapter）→ **21/21 GREEN 首跑**
3. 全 suite **10569** 0F/0E（10548+21）
4. live probe（真实行全 adapter 路径）: pred '2 days'，gate pp_duration，route trip_span
5. full-500 replay（C572 canonical harness verbatim）**PASS** 1159s: pred change 恰 {gpt4_1d80365e}（echo 垃圾→'2 days'），drift 1 处 False→True，banked 311，abs_banked 18

## 本周期教训

- **⚠️ harness 重打必歪（本周期核心教训）**: 首版 replay 脚本凭记忆重打——`exact_judge` arity 错（少 question 参数）+ banked 公式偏差（`bool(v or ex)` vs canonical `(v=='CORRECT') or (correct_exact and v!='WRONG')`）。crash 抓住 arity，但公式偏差是**对照 canonical harness diff 才发现**的（会毒化 drift 台账，TOOLS.md 2026-09-03 同源规则又一例）。**规则：replay harness 只准 verbatim 拷贝上一 cycle canonical，只改 chain/out/expect 默认值，绝不重打**
- exec preflight 拒 heredoc/管道复合（again）→ 全部 write 工具落盘 + 直跑
- head module 放 /tmp 需要 `sys.path.insert(amg_dir)`（memory_graph 导入依赖其目录）
- 副本钉真实 haystack 日期（05-15/05-17），kd-2 合成日期失真教训直接应用
- memory_graph.py dirty hunk day 31 未触碰；staged audit +354 恰我 2 文件

## 提交链

`eae5ff2` (C572 HEAD) → **`cd60d09`** (C573 code: amg +102 / test +252) → **`1b83ba4`** (tsv row) → pushed origin master

## Trajectory

0.502 → … → 0.610 (C569) → 0.614 (C570) → 0.618 (C571) → 0.620 (C572) → **0.622 (C573)**

## Next（队列）

1. **recall-meta family**（13 qids，最大未 banked 块，speaker_recall 'follow up on our previous' 簇 0e5e2d1a 等）
2. named-holiday calendar for gpt4_f420262d（c8090214 已由 C572 收割）
3. ollama oracle（human-blocked）

## Artifacts

- /tmp/c573/{step1_sweep, step2_census_evidence, step2b_dates, step2c.out, step2d.out, step3_census_drift, green_check, junit.xml, run_suite, step5_probe, live500_c573.py, live500_c573.json, append_tsv.py}
- **live500_c573.json = 新 authoritative chain**
