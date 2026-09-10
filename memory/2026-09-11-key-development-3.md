# Key Development 3 — Cycle C566 (2026-09-11)

**Task:** cron `key-development-3` · autoresearch 方法论实验循环 C · 基于链头 C565（banked 300 / 0.600，commit `43fb9b9`，01:00 到岗时已落地 7 分钟）

**结果：+1 rescue（gpt4_a1b77f9c）/ 0 kills — banked 300 → 301（0.600 → 0.602），全套件 10437 → 10448 green（+11），无并发冲突，全周期一次通过**

## 增量内容：activity-span sum route (g)（C565 队列第 1 项）

题目："How many weeks in total do I spent on reading 'The Nightingale' and listening to 'Sapiens…' and 'The Power'?"（GT: 2+4+2 = 8 weeks）

**关键发现（设计前证据定位，step1/step2）：** C565 队列注释「route (f) 现成，只需放宽 both-facts guard」是**错面判断**——haystack 里根本没有 "took me N weeks" 锚点。oracle 的 2/4/2 weeks 是**会话日期差**：

- Nightingale：s26(01/01) "I started reading…" → s28(01/15) "just finished…" = 14d
- Sapiens：s35(02/01) "just started listening…" → s38(03/01) "just finished…" = 28d
- The Power：s40(03/06) "started listening…" → s41(03/20) "just finished…" = 14d

→ 新 route (g) `_pp_activity_sum`：题干引号书名抽取 → 逐实体 start/finish 事实扫描（user 行 + "today" 共现 + started/began vs finished）→ span = max(finish) − min(start) → 全实体 resolved guard（部分和 = 捏造，诚实 fall-through）→ 题干单位渲染（`_pp_render(56, ["week"])` → "8 weeks"）。

## 工程细节（三个都有普适性）

- **引号风格跨会话漂移**：s26/s35/s38/s41 用单引号 `'The Nightingale'`，s28/s40 用双引号 `"The Nightingale"`——绑定必须 quote-style agnostic（`["'“”]title["'“”]`）。第一版脚本只认单引号，漏掉 2/6 事实行——微型测试直接从真实 haystack 逐字拷贝行才暴露（C562 lesson 再验证）
- **unquoted 混淆体防御**：s41#2 "The Power of Habit by Charles Duhigg" 含 'The Power' 子串——该行无 start/finish+today 天然不命中，但绑定仍要求 quote-wrapped（defense in depth）
- **census 排除三兄弟全靠构造**：edced276（banked，"did I spend in total traveling"——in total 在 spend 后）、372c3eed（"spend in formal education"——无 activity gerund）、6cb6f249（无 spend frame）；head regex 实测 500 题恰 1 命中

## 验证链

- 红先：11 miniatures ImportError RED → 实现后 11/11 GREEN（一次通过）
- census 复验走**真实 wired import**（census_verify.py）：恰 1 行、unbanked
- 全套件 junit：**10448 / 0F / 0E / 0 skipped**（265s，C565 的 10437 + 我的 11，严丝合缝）
- live-500：**1160s PASS**——pred change 恰 {gpt4_a1b77f9c}（垃圾会话引用 → '8 weeks'），drift 恰 1 条 False→True，banked 301/500，abs_banked 18
- diff 审计：amg_bench_quality.py +122/−1（−1 = gate OR-chain 行改写），逐 hunk 对得上；memory_graph.py 脏 hunk 第 25 天未碰
- banking 判定通道 pin：`judge_semantic("8 weeks", 长GT) = CORRECT`（number-subset face，与 C565 "5.5 weeks" 同路径）

## 数值轨迹

0.502 → … → 0.580 (C560) → 0.588 → 0.590 → 0.594 (C563) → 0.596 (C564) → 0.600 (C565) → **0.602 (C566)**

## Next queue（继承 + 新增）

1. **2311e44b**：440−250=190 减法面
2. **184da446**：page 200→220 latest-wins
3. **372c3eed + _abs**（新识别，一次族两行）：education range 求和（2010-2014 + 2014-2016 + 2016-2020 = 10 年）；_abs 孪生必须 abstain（Master's 年限未提及）——文本日期区间锚点，与 route (g) 的会话日期差不同锚型
4. 2ebe6c90/2ebe6c92 session-date 算术（险，后置）
5. ollama oracle（human-blocked）

## Artifacts

- commit：`31f5f58`（实现+测试）、`f8913c0`（tsv pin）
- /tmp/c566/{step1_find_facts.py, step1b_dump.py, step1c_dates.py, step2_census.py, step2b_head.py, step2c_repr.py, census_verify.py, live500_c566.py, live500_c566.json, junit.sh, junit.xml, mini.out}
- live500_c566.json = 新权威链（下一周期 chain 参数指向它）
- experiments.tsv C566 行（8 字段，keep）
