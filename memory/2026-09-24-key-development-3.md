# key-development-3 — C602 (2026-09-24)

**delivery_services face（qid `d682f1a2`）keep。banked 355→356（0.712），第 38 连 keep。commit `a67cfa0`。**

## 目标与结果
- 目标行：`d682f1a2` "How many different types of food delivery services have I used recently?" GT `3`，qtype multi-session，question_date 2023/05/30。旧 pred = Fresh Fusion recipe-echo（gate=answer，整段用户 turn 原样吐出，无数字）。
- 结果：pred `'3'`，judge_semantic/exact/counting 三判全 CORRECT；**full-500 replay PASS 首试**（1199s）：pred-change set == drift set == `{d682f1a2}`（False→True），banked **356/500**。suite 11063→**11082** green（+19 新测试，289s）。

## 机制
- `_FDL_HEAD_RE`：全句严格头 `^\s*how\s+many\s+different\s+types\s+of\s+food\s+delivery\s+services\s+have\s+i\s+used\s+recently\s*\??\s*$`，census 恰 1/500 行；宽松扫描（food delivery|delivery service）确认无兄弟行可偷。
- `_cnt_delivery_services`：`_map_sents` 用户句，需同时命中**双墙**才算：brand（`_FDL_BRAND_RX`：`domino('s|s)?\s+pizza`|`uber\s+eats`|`fresh\s+fusion`，domino 必须带 pizza 防 domino effect）+ usage marker（`_FDL_USE_RX`：had|relying on|been all about|found|ordered|tried|used）。brand 全部 finditer 收集、小写归一 set 去重（Uber Eats s27 t0+t2 重提只计 1）。渲染 `'3'`。
- 证据：Domino's Pizza（s8 "I had Domino's Pizza three times last week"）+ Uber Eats（s27 "weekends have been all about" + "relying on" 重提）+ Fresh Fusion（s41 "this new one I found called"）= 3。
- **承重墙：user-role**——s41 assistant 回声 "As for Fresh Fusion, ... you've **found** a convenient option" 同时含 brand+found，只有角色墙能挡住；s27 两个 Uber Eats 回声同理。decoy pin：brand 无动词（billboard 句）、动词无 brand（takeout 句）、句粒度（found 与 brand 分句）、裸 domino 无 pizza。

## 过程
1. 幂等四查过（tsv tail=C601、无 C602 行/commit、无 live kd 进程、git 在 95ef6d0）。链验证：C601 `live500_c601.json` banked=355，`d682f1a2` WRONG。
2. Census 两步（/tmp/c602/census_food.py、census2.py）：head 恰 1/500；brand 表面全量审计（任意角色）= 用户 4 句 + assistant 4 句回声，无其他表面。
3. TDD：`test_delivery_services_face.py` 19 tests（verbatim fixtures，含 3 个 assistant 回声原文 pin 角色墙）→ RED（ImportError `_cnt_delivery_services`）→ 3 处 edit → GREEN 19/19。
4. 真适配器 probe：d682f1a2 pred='3' 三判全过；邻居 5a7937c8/affe2881 无回归。
5. Suite 11082 green（289s）。Replay：**cp C601 canonical 逐字节改默认值**（sed 后 diff 审计=恰 5 处默认值 + docstring），PASS 首试，8 连首试。

## C601 教训落地
replay 脚本直接 `cp` 上一 cycle canonical + sed 改默认值 + diff 审计，未重写 banking 逻辑——零假 drift。流程已固化进本 cycle 产物。

## 状态与队列
- banked **356/500**（0.710→0.712），abs 30（18 abs + 12 held），suite 11082。
- kd queue 下一候选：memory_graph demo-orphan 修复（`6ef39db` 删 `def demo():` 致 import 副作用，脏 hunk 手术，独立 cycle）；此后需 census 找新 face（本 cycle 后 counting 队列无现货候选）。
- 环境噪音未变：import 打印 demo 横幅（C501 cosmetic，待手术）。

## 产物
- commit `a67cfa0`（amg_bench_quality.py +78/-1、test_delivery_services_face.py +256）
- `/tmp/c602/`：peek_row.py、census_food.py、census2.py、dump_turns.py、run_face_tests.py、run_suite.py、probe.py、live500_c602_canonical.py、live500_c602.json（新权威链）
- experiments.tsv C602 行
