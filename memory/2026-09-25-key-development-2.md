# key-development-2 — C604 (2026-09-25)

**funrun_miss face（qid `21d02d0d`）keep。banked 358→359（0.716→0.718），第 40 连 keep。commit `6b4c8dc`。**

## 目标与结果
- 目标行：`21d02d0d` "How many fun runs did I miss in March due to work commitments?" GT `2`，qtype multi-session，question_date 2023/04/26。旧 pred = marathon-recovery echo（gate=answer，整段吐 turn 无数字）——C599 记录的 no-steal lane（需 miss+work 归因语义），本轮接手。
- 结果：pred `'2'`，judge_semantic/exact/counting 三判全过；**full-500 replay PASS 首试**（1152s，第 10 次连续首试）：pred-change set == drift set == `{21d02d0d}`（False→True），banked **359/500**。suite 11102→**11121** green（+19 新测试，258s）。

## 机制
- `_FRM_HEAD_RE`：全句严格头 `how many fun runs did i miss in march due to work commitments`，census 恰 1/500；跨 500 行无任何其他问题提及 fun run（零兄弟行）。
- `_cnt_funrun_miss`：`_map_sents` 用户句需同时命中**四重墙**才算：fun-run term（`\bfun\s+runs?\b`，裸 'morning run' 不命中）+ miss 动词（`\bmiss(ed)?\b`——**'missing' 动名词不过墙**，\b 落在 's' 与 'i' 之间，C599 ordinal-suffix 教训的兄弟）+ work 归因（`\bwork\b`，家人旅行借口不命中）+ 显式 `March <day>`（ordinal 可选）。
- 证据（句粒度自含，两句各带全部四面墙）：s3 "busy with work lately and missed a few events, including a 5K fun run on March 26th" + s30 "attend most of the weekly 5K fun runs … except the run on March 5th when I had to miss due to work commitments" = days {26,5} → **2** ✓GT。distinct days additive + set 去重。渲染 `'2'`。
- 双 assistant 回声（s3 "don't worry about **missing** the 5K fun run"、s30 "have been attending the weekly 5K fun runs"）双双缺 miss 动词+work——**miss+work 合取墙在 assistant 侧也是承重墙**，user-role 墙再兜底。April-10 marathon 恢复句、movie marathon 无 fun-run term 天然不命中。
- 队列三候选比较：coins `69fee5aa` 需 base(37 声明，turn 粒度 sibling topic)+delta(+1 added 事件)双机制+时序仲裁，最重；weddings `gpt4_2f8be40d` 需 own-wedding 排除+couple 归并，GT 是整句风险高；fun-run 最干净 → 单机制单脸（C601 先例）。

## 过程
1. 幂等四查过（workspace tsv tail=C603、amg 项目 tsv tail=C600 长格式【C601 起改用 workspace 短格式】、无 C604 工件、无 live kd 进程；`/tmp/c603` 权威链在）。链验证：C603 `live500_c603.json` banked=358，三候选全 WRONG。
2. Census 三步（/tmp/c604/dump_three.py、census_funrun.py）：strict head 恰 1/500；in-row 4-wall 证据恰 2 句（days {5,26}）；宽松扫描全角色恰 4 句且回声缺双墙；fun-run 跨行零命中。
3. TDD：`test_funrun_miss_face.py` 19 tests（verbatim fixtures + 结构墙 pin：skip≠miss / 无 work / April 日 / 裸 run / missing 动名词 / March 无日 / 同日去重 / 三日加法 / assistant 全墙仍暗）→ RED（ImportError）→ 3 hunk（head+handler 79 行 / classifier hoist / dispatch）→ GREEN 18/19 → 修 `exact_judge` 签名想当然（3 参，测试 observable 教训又现挂）→ **GREEN 19/19**。
4. Suite 11121 green（258s，=基线 11102+恰 19）。
5. 真适配器 probe：21d02d0d pred='2' gate=counting v=CORRECT；4 个邻居 keep 行（a2f3aa27/a1eacc2a/5a7937c8/d682f1a2）pred 全不动。
6. Replay：**cp C603 canonical + Python 字节级替换（count==1 assert，绕开 sed chain/out 同名替换链坑）+ diff 审计**（恰 docstring+5 处默认值），PASS 首试。

## 状态与队列
- banked **359/500**（0.718），40 连 keep，零回退；abs 30（18 abs + 12 held）冻结；suite 11121；链 `/tmp/c604/live500_c604.json` 新权威。
- kd queue 下一候选：`69fee5aa` coins（37 声明 + 1 added = 38，base+delta 双机制，recency 时序）——C603 supersession 机制的 delta 扩展；`gpt4_2f8be40d` weddings（own-wedding 排除 + 'this year' 窗口 + GT 整句渲染风险）；memory 仓垃圾（temporal_test_data.json / test_optimization.py / test_status.log 三个 untracked 杂物待清理，非本轮产物）。
- 收编：本 cycle 顺带提交 kd-1（C603）遗留的未提交 tsv 行 + cycle log（工作树里躺了 1 天），见 memory commit。

## 产物
- commit `6b4c8dc`（amg_bench_quality.py +78/-1、test_funrun_miss_face.py +244）
- `/tmp/c604/`：dump_three.py、dump_three_out.txt、census_funrun.py、run_face_tests.py、run_suite.py、suite_out.txt、probe_adapter.py、build_replay.py、replay.py、replay.log、live500_c604.json（新权威链）
- workspace memory/experiments.tsv C604 行（短格式）
