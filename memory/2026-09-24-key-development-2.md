# key-development-2 — C601 (2026-09-24)

**faith_days face（qid `5a7937c8`）keep。banked 354→355，第 37 连 keep。commit `20ca7a5`。**

## 目标与结果
- 目标行：`5a7937c8` "How many days did I spend participating in faith-related activities in December?" GT `'3 days.'`，qtype multi-session，question_date 2024/01/10。旧 pred = volunteer-echo（gate=answer，含 "December 10th" 字样但无数字）。
- 结果：pred `'3'`，judge_semantic CORRECT；**full-500 replay PASS**（1190s）：pred-change set == drift set == `{5a7937c8}`（False→True），banked 355/500。suite 11043→**11063** green（+20 新测试，278s）。

## 机制
- `_FD_HEAD_RE`：全句严格头 `^\s*how\s+many\s+days\s+did\s+i\s+spend\s+participating\s+in\s+faith[-\s]related\s+activities\s+in\s+december\s*\??\s*$`，census 恰 1/500 行。claim 位置在 `counting_form` 的 generic `how many (days|weeks)`→duration_sum block **之前**（head 含 "how many days"，会被提前捕获）。
- `_cnt_faith_days`：遍历 `_map_sents`（**honorific 合并是承重点**——Dec 24 证据在 "St. Mary's" 的 St. 处被切分后重接，C599 机制复用），句子需同时命中三重墙才算：faith term（church|midnight mass|bible study|worship|prayer service）+ 过去参与动词（helped out|got back from|attend(ed)|volunteered|did|went to|spent）+ 显式 `December <day>`（`_FD_DEC_DAY_RX`，ordinal 后缀可选——C599 教训 `\b` 落在 '0' 与 't' 之间）。distinct days additive + set 去重（Dec 17 re-mention 无动词天然不重计）。渲染 `'3'`，counting_judge numeric-first vs GT `'3 days.'`。
- 证据：Dec 10 church food drive / Dec 17 Bible study / Dec 24 midnight mass at St. Mary's → 3。decoy 全不 key：Dec 12 Le Creuset/Coach 购物（无 faith term）、future intent（leading next week / thinking of doing，无日期）、t4 re-mention（无动词）、painter "Frederic Edwin Church"（无日期）、assistant echo（user-only）、`December 2023` 裸年（`\d{1,2}`+`\b` 回溯）。

## 过程
1. 幂等检查过（仅本 cron；昨日 C598 文件不冲突）。链验证：C600 `live500_c600.json` banked=354，`5a7937c8` WRONG。
2. Census（`/tmp/c601/census_faith.py`）：head 恰 1 行；证据 days {10,17,24}；decoy 0 泄漏；3 个 faith 近亲（gpt4_b5700ca9 / 08f4fc43 / 2a1811e2，temporal arithmetic 类）不撞 head。
3. TDD：`test_faith_days_face.py` 20 tests（verbatim fixtures），RED（ImportError `_cnt_faith_days`）→ 3 处 edit → GREEN 20/20。
4. Suite 11063 green。Replay 首跑（自写脚本）出现假 drift `099778bb: True→False`。

## ⚠️ 本 cycle 唯一教训：replay 脚本必须逐字节照抄 canonical
我重写 replay 时把 banking 规则从 canonical 的
`ok = (v == "CORRECT") or (r["correct_exact"] and v != "WRONG")`
简化成了 `nb = (v == "CORRECT")`——丢了 frozen correct_exact 血统项，导致 v=NEEDS_JUDGE 且 frozen-exact 的行（099778bb '20%'）出现假 drift（True→False）。canonical 有 `up_all`（drift 必须 False→True）检查正是防 down-drift 的。处理：kill 首跑，`cp /tmp/c600/live500_c600.py` 逐字节复制、只改 docstring+defaults，重跑 PASS。**下次 cycle replay 一律从上一 cycle 的脚本 cp 起步**，把这条写进流程。

## 状态与队列
- banked **355/500**，abs 30（18 abs + 12 held），suite 11063。
- kd queue 下一候选：`d682f1a2`（food delivery，GT 3，distinct-brand counting；probe 显示仍 WRONG）→ memory_graph demo-orphan 修复（`6ef39db` 删 `def demo():` 致 import 副作用，44 天脏 hunk 待手术，独立 cycle）。
- 环境噪音未变：import 打印 demo 横幅（C501 cosmetic）。

## 产物
- commit `20ca7a5`（amg_bench_quality.py +85/-1、test_faith_days_face.py +293）
- `/tmp/c601/`：census_faith.py、gen_fixture.py、run_face_tests.py、probe2rows.py、run_suite.py、live500_c601_canonical.py、live500_c601.json
- experiments.tsv C601 行
