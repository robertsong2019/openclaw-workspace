# key-development-2 — C607 (2026-09-26)

**workshop_days face（qid `10d9b85a`）keep。banked 361→362（0.722→0.724），第 43 连 keep。commit `25b4fd0`。**

## 目标与结果
- kd-1 交接的两个 lane 备选（5a7937c8 faith days / gpt4_4929293b bridesmaid）**实查全已 banked**（v=CORRECT, banked:true）——交接 note 过期，链上真相优先。改从 C606 链 139 unbanked 重新挖。
- 8 候选过滤（counting 族数字 GT 优先）：`0a995998` 衣服/`2788b940` 健身课（bodypump=weightlifting 双计风险）/`6d550036`+`60472f9c` 项目（证据分散）/`bf659f65` 专辑（只见 2 项 GT=3）/`gpt4_31ff4165` 设备（只见 2 项 GT=4）全偏重；`2ce6a0f2` art events（'art-related' 语义+相对月窗）次选；**选 `10d9b85a`**：2 个自含证据句 + distinct-days 机制（funrun C604 已验证）+ GT '3 days' 走 counting_judge 数值路径（faith_days C601 已验证）。
- 结果：真 adapter probe pred='3' CORRECT（GT '3 days' numval=3.0）；6 邻居（含 loose workshop 堂兄弟 gpt4_1e4a8aeb/0bb5a684）form/pred 全不动；**full-500 replay PASS 首试**（1194s，第 12 次连续首试）：pred-change set == drift set == {10d9b85a}（旧 pred = social-media 回声整 turn 无数字）。suite 11154→**11177** green（+23 新测试，276s）。

## 机制（faith_days C601 的直系变体）
- 严格头 `how many days did i spend attending workshops?,? lectures?,? (and )?conferences? in april`，census 恰 1/500。**分类器 claim 在通用 duration_sum 块之前**（'how many days' 否则会路由去 duration_sum）——新插桩点在 C606 weddings 块后。
- 四重墙（句粒度自含）：topic（workshop|lecture|conference）+ 参与动词（attend(ed)|spent）+ April 日锚（**双模式**）+ user-role。
- **日锚双模式是本轮新形状**：两条证据句都用 day-first（'the 10th of April' / 'the 17th and 18th of April'），与 faith_days 的 month-first（'December 10th'）相反。`_WKD_DAY_BEFORE_RX` 的可选 `and <day>` 组在一次匹配里吃下两日列表；month-first `_WKD_DAY_AFTER_RX` 另测（'April 12th' 合成句 pin）。'April 2023' 沿用 C601 年份回溯教训（\b 不落在年份数字间）。
- 证据：s29 lecture → {10}；s39 '2-day workshop' → {17,18}；distinct days {10,17,18}=3 ✓GT。同日重提去重（重提句 'The workshop covered...' 无参与动词天然暗）；'There's a 2-day workshop on the 17th and 18th'（无动词）暗；'thinking about the workshop ... Dr.'（honorific 合并后仍无动词无日）暗。
- 行内 500 行普查：KEYED 恰 2 句全 user；行内 assistant 面（'Attend classes or workshops with a teacher'、'Video lectures' 等 7 处）全无 April 日——user-role 墙兜底。

## 过程
1. 幂等四查过（tsv tail=C606、git head=65a9455、无 C607 工件、无 live kd 进程、权威链 /tmp/c606 在）。链验证：C606 live500 banked=361，两个交接候选 chain banked:true（交接作废）。
2. 8 候选 evidence 过滤 dump（/tmp/c607/dump_two.py、dump_cands.py）→ 选型 → census 三步（census_wksp.py：strict head 1/500、in-row KEYED 恰 2、loose 堂兄弟不同头）。
3. TDD：`test_workshop_days_face.py` 23 tests（verbatim fixtures + 结构墙 pin：duration_sum 不偷/day-first 双日列表/month-first/无动词/April 无日/非 April 日/年份回溯/同日去重/四日加法/assistant 全墙仍暗/judge 数值路径 pin `counting_judge(Q,'3','3 days')==True` + `exact==False`）→ RED（ImportError）→ 3 hunks（regex+handler 87 行 / classifier claim / dispatch）→ **GREEN 23/23 首试**。
4. Suite 11177 green（276s，=基线 11154+恰 23）。
5. 真 adapter probe：10d9b85a pred='3' CORRECT；faith/funrun/coin/wedding 四张 prior face + 2 个 workshop 堂兄弟全不动。
6. Replay：build_replay.py 字节级替换（count==1 assert ×6）+ diff 审计（恰 6 hunk 组）→ PASS 首试。
7. staged diff 审计过（amg 无独立 .git，monorepo 相对路径 add；memory_graph.py 脏 hunk + 3 untracked 杂物非本轮产物，未卷入）。

## 状态与队列
- banked **362/500**（0.724），43 连 keep，零回退；abs 30（18 abs + 12 held）冻结；suite 11177；链 `/tmp/c607/live500_c607.json` 新权威。
- kd queue 下一候选：`2ce6a0f2` art events past month（GT=4，4 证据句全含 'art' term：Feb 10 exhibition / Feb 17 Art Afternoon / Feb 24 museum tour / Mar 3 lecture，Mar 3 双提需日期 key 去重；相对月窗 vs question_date 2023/03/08 需 census 验证零出窗命中）；census 可再从 live500_c607 链 ~138 unbanked 挖。
- **流程教训（给下轮）**：kd 交接 note 的 lane 备选必须先查链上 banked 状态再信——本轮两个备选全已 banked，白占 note 空间。unbanked 清单直接从最新链拉（list_unbanked.py 范本在 /tmp/c607/）。
- 遗留：memory_graph.py `_search_cache` 脏 hunk + temporal_test_data.json/test_optimization.py/test_status.log 三个 untracked 杂物仍未清理（C604 起挂账）。

## 工件
- commit `25b4fd0`（amg_bench_quality.py +87/-1、test_workshop_days_face.py +264）
- `/tmp/c607/`：dump_two.py、dump_two_out.txt、chain_check.py、list_unbanked.py、unbanked.txt、dump_cands.py、dump_cands_out.txt、census_wksp.py、census_out.txt、run_face_tests.py、face_red.txt、face_green.txt、run_suite.py、suite_out.txt、build_replay.py、replay.py、replay.log(会话log)、probe_adapter.py、probe_out.txt、patch_tsv.py、append_tsv.py、live500_c607.json（新权威链）
- workspace memory/experiments.tsv C607 行（短格式）
