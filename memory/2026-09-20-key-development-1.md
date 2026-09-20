# 2026-09-20 — key-development-1 (C592)

**Cycle:** C592, cron 23:00 +08, lane = counting 方向延续（acquire 采集计数家族）
**Result:** ✅ keep — banked **341→343 (0.682→0.686)**，28 连 keep 零回退

## 目标与结果

| qid | 问题 | GT | 旧 pred | 新 pred |
|-----|------|-----|---------|---------|
| 3a704032 | How many plants did I acquire in the last month? | 3 | chit-chat | **'three'** |
| 9d25d4e0 | How many pieces of jewelry did I acquire in the last two months? | 3 | chit-chat | **'three'** |

- Census（all 500）：acquire_last 形式恰 2 行，均 GT '3'，无 _abs 兄弟
- Suite: 10870 → **10884 (+5 subtests)**，exit 0（replay 后绿）
- Replay: PASS 1230s **一次过**，pred changes / drift 恰 {3a704032, 9d25d4e0}，全 False→True，abs_banked=18 冻结
- Commits: 6f6c781（代码+测试）、f856f94（tsv 703 行）；`/tmp/c592/live500_c592.json` = 新权威 chain

## Face 设计（acquire，一机制两话题面）

- 同句纪律（C591）：采集动词（got|bought|purchased|acquired|received|inherited）+ 有界过去标记 + 话题 NP，三者必须在**同一句**；session-topic 门（C586 教训，session 粒度 user 行含话题词）
- **类别词不计数**（C519 教训）：裸 'plants'/'jewelry' 永不计数；'succulent plant' 折叠为 'succulent'；'snake plant' 复合键。植物 head NP 全名键控（'peace lily'）
- **珠宝按 head noun 键控**（单数化）：'new pair of earrings' == 'those emerald earrings'（重复提及折叠一次）；'a small pendant' 是 with-修饰语（pendant 不入 head 词典）；ring 的语料表面是单句 'I got my engagement ring a month ago'（s33）→ 无需跨句 anaphora
- 月粒度标记扩展 C591 相对集：N months ago=30N / a month ago=30 / last month=31；window = 31（单月）或 30N+1
- **form 门不偷 4f54b7c9**（antique/inherit-or-acquire from family，无 'in the last' 窗口）——保持 enum_count，留后续 cycle
- 证据不可解析 → None fall-through（census 零重叠）

## 教训（本轮 3 个）

1. **head 正则先过 miniature 再谈 replay**：初版只匹配 'last N months' 数字形，裸 'last month'（3a704032 的真实表面）落到 enum_count——15 项 unit probe 在语料探针前抓到（8/15 红，单根因）。可选数词组 + 回溯修复。
2. **python3 shim 会静默吞掉 `python3 -m pytest`**：exit 0 + 空 log，suite 根本没跑。可靠路径 = runner 脚本内 `pytest.main([...])`（/tmp/c592/run_suite.py 模式，已记 TOOLS.md）。
3. **测试夹具共享可变状态**：`dict(s)` 浅拷贝后 `mod[2]["turns"][0] = ...` 就地变异污染共享 turns 列表，后续用例读到脏数据——夹具构造函数化（每次 S() 重建）。

测试构造 bug 3 个（非 face bug）：非窗口变体合法落 enum_count（behavior-neutral，钉 enum_count 不是 None）；U_S7_B 含真实 flea-market dup 句（decoy 改 kit-only）；4f54b7c9 期望从 None 修为 enum_count。

## 附带

- Replay 一次过是链纪律（census-first + miniature-red-first + 双 judge 渲染规则 + 幂等三查）的直接收益——C591 三次 replay，C592 一次。
- 下轮队列：antique-inherit 家族 head（4f54b7c9，GT 5，无界窗口 + 家庭来源验证）/ furniture 多动词家族（gpt4_15e38248 buy|assemble|sell|fix）/ list renderer（a40e080f / ceb54acb / 8cf51dda）。
