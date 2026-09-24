# key-development-3 — C605 (2026-09-25)

**coin_add face（qid `69fee5aa`）keep。banked 359→360（0.718→0.720），第 41 连 keep。commit `4ada5be`。新赛道：knowledge-update base+delta 算术。**

## 目标与结果
- 队列：C604 留下两候选 `69fee5aa` coins / `gpt4_2f8be40d` weddings。dump 对比后选 coins：weddings GT 是整句枚举（"I attended three weddings. The couples were Rachel and Mike, Emily and Sarah, and Jen and Tom."）渲染风险高（C604 已预警）；coins GT=38 纯数字，qtype=**knowledge-update**（此前 counting 家族未覆盖的赛道）。
- 结果：真 adapter probe pred='38' CORRECT（6 行含 5 个邻居 keep 全不动）；**full-500 replay PASS 首试**（1151s，第 11 次连续首试）：pred-change set == drift set == `{69fee5aa}`（False→True），banked **360/500**。suite 11121→**11140** green（+19 新测试，264s）。

## 机制（base+delta，非 supersession）
- 证据链：s12 (2023/05/27) base 声明 "I have a total of 37 coins in that collection"（**topic 'pre-1920 American coins' 在同 turn 兄弟句** "organizing my pre-1920 American coins by denomination and mint mark"——base RX 键 anaphoric 'in that collection' 而非 topic，C603 stories 教训复用）+ s39 (2023/05/29) delta "I just added a new coin to my collection of pre-1920 American coins - a 1915-S Barber quarter"（全句自含）→ 37+1=**38** ✓GT。
- 仲裁规则：latest base wins（时序扫描）；delta 只计 **严格晚于 base session** 的事件（早于/同 session 的 add 视作已烘进 base，不双计）；identical add 句 dedup；distinct add 句 additive；无 base → None fall through。单遍扫描实现（adds dict sent→first si），无辅助函数。
- 墙：ADD RX 全自含（just added + a new coin + pre-1920 topic）——1972 doubled-die（'recently bought'）、1913 Liberty nickel（'meaning to get...appraised'）、'before adding a coin'、camera 'add to my collection' 全不命中；assistant echo（"Congratulations on adding a new coin"）双缺 + user-role 墙兜底。
- Census（全 500）：strict head 恰 1 行；BASE/ADD RX 跨 500 行**任意角色零兄弟句**（宽松 'add...coin' 兄弟 16 行全被严格墙挡死）；in-row assistant 零泄漏。

## 过程
1. 幂等四查过（workspace tsv tail=C604、amg git log head=67944ee/6b4c8dc、无 C605 工件、无 live kd 进程、权威链 /tmp/c604/live500_c604.json 在）。
2. dump 两候选全句面（/tmp/c605/dump_two_full.py，heredoc 被 preflight 拒——write+直跑绕开）→ census 三步（census_coin.py）。
3. TDD：`test_coin_add_face.py` 19 tests（verbatim fixtures + 结构墙 pin：no-base/add-only/base-only/晚加/早烘/同 session/最新 base 胜/dedup/assistant/bought/appraise/camera/anaphor）→ RED（ImportError）→ 3 hunks（regex+handler 66 行 / classifier hoist / dispatch）→ 首版带辅助函数两遍扫描，自审简化为单遍 dict（Simplicity First）→ **GREEN 19/19 首试**。
4. Suite 11140 green（264s，=基线 11121+恰 19）。
5. 真 adapter probe：69fee5aa pred='38' gate=counting CORRECT；5 邻居（21d02d0d/a2f3aa27/a1eacc2a/5a7937c8/d682f1a2）pred 全不动。
6. Replay：build_replay.py 字节级替换（count==1 assert ×6：docstring+chain+out+expect×2+total）+ diff 审计（恰 6 hunk）→ PASS 首试。

## 状态与队列
- banked **360/500**（0.720），41 连 keep，零回退；abs 30（18 abs + 12 held）冻结；suite 11140；链 `/tmp/c605/live500_c605.json` 新权威。
- kd queue 下一候选：`gpt4_2f8be40d` weddings this-year（pred '4' vs GT 整句 'I attended three weddings...couples were Rachel and Mike, Emily and Sarah, and Jen and Tom'——需 attended 语义 + own-wedding 排除 + 渲染策略探针先行，judge_semantic 对整句 GT 行为未知）；census 可再从 live500_c605 链 ~140 unbanked 挖新 face。
- 遗留：C599 起排队的三候选已消化 2/3（funrun C604、coins 本轮），weddings 是最后一个；memory 仓垃圾（temporal_test_data.json / test_optimization.py / test_status.log untracked）仍未清理。

## 产物
- commit `4ada5be`（amg_bench_quality.py +81/-1、test_coin_add_face.py +229）
- `/tmp/c605/`：dump_two.py、dump_two2.py、dump_two_full.py、dump_two_out.txt、census_coin.py、census_coin_out.txt、run_face_tests.py、run_suite.py、probe_adapter.py、build_replay.py、replay.py、replay.log、append_tsv.py、live500_c605.json（新权威链）
- workspace memory/experiments.tsv C605 行（短格式）
