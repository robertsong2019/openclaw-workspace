# 2026-09-20 — key-development-3 (C591)

**Cycle:** C591, cron 01:00 +08, lane = C590 队列首位 enum-count 双题
**Result:** ✅ keep — banked **339→341 (0.678→0.682)**，27 连 keep 零回退

## 目标与结果

| qid | 问题 | GT | 旧 pred | 新 pred |
|-----|------|-----|---------|---------|
| 60159905 | How many dinner parties have I attended in the past month? | three | '1' (enum_count) | **'three'** |
| a3838d2b | How many charity events did I participate in before the 'Run for the Cure' event? | 4 | '1' (enum_count) | **'four'** |

- Suite: 10847 → **10865 (+5 subtests)**，exit 0（replay 前绿）
- Replay: PASS 1160s，pred changes / drift 恰 {60159905, a3838d2b}，全 False→True，abs_banked=18 冻结
- Commits: ad3d6b1（代码+测试）、bba8f52（tsv 702 行）；`/tmp/c591/live500_c591.json` = 新权威 chain

## Face 设计（event_count，一机制两约束面）

- **Head A**（dinner parties past-month）：user 行 `attended|had ... at <Name>'s place` + 同句有界过去标记（yesterday=1 / last week=13 / **two weeks ago=14 拼写数词** / N days|weeks ago），窗口 ≤31 天；session-topic 门（session 的 user 行须含 dinner-party/feast 词——杀 David 生日会诱饵）；host 去重 → sarah+mike+alex=3
- **Head B**（charity before-anchor）：问题引号事件 = 时序锚（Run for the Cure，日期从 user 句解析 Oct 15 x2 一致，冲突→None）；实例 = 过去时参与动词 + charity 信号（charity/gala/fundraiser NP **或 volunteered 动词**——Walk for Wildlife 无 charity 名词）+ 月粒度日期，键 (month, day)；strictly-before 排除 November Bike-a-Thon 陷阱；锚名句永不计数 → 4
- 渲染纯词形 'three'/'four'（见教训 2）；证据不可解析 → None fall-through（enum_count 零重叠）

## 教训（本轮 3 个）

1. **拼写数词**（face bug，miniature 在 replay 前抓到）：数据集表面是 'two weeks ago' 不是 '2 weeks ago'；marker 正则只匹配数字时 Mike 的 BBQ 静默丢失（n=2 ≠ 3）。用 _CNT_WORD2NUM 支持词数。
2. **渲染必须过 judge_semantic，不是 exact_judge**（replay #2 FAIL 339≠341）：'three (3)' 过 exact_judge containment，但 _sem_norm 把它折叠成 '3 3'（重复 token）→ NEEDS_JUDGE；这两行 frozen correct_exact=False，harness ok 公式完全由 judge_semantic 决定。纯词形渲染修复。**新规则已记 error-patterns.md：replay 前双 judge 探针。**
3. **exec timeout 会 SIGTERM 自己的后台任务**（replay #1 死于 450/500）：timeout=1200 是从启动算的；长任务一律 background=true 无 timeout + 轮询日志文件。

测试构造 bug 4 个（非 face bug）：u() 返回 dict；'How many books' 本就是真 enum_count 行；U_S4_M4 含 'dinner parties' 所以 topic 门合法放行；U_S8_M0 本身含真实 attended feast（期望改成 'one (1)'——渲染修复后语义为 'one'）。

## 附带

- tsv_append.py C590 版 print bug：f-string 里 `back.count(b'\\n')` 数的是两字符字面量——C591 版修复（行数移出 f-string）。
- 下轮队列：list renderer（a40e080f / ceb54acb / 8cf51dda）；ollama oracle（human-blocked，解锁 ~169 NJ 级联）。
