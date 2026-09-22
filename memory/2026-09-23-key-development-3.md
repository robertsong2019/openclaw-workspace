# key-development-3 — C599 (2026-09-23, autoresearch 循环 C)

## 结果：KEEP ✅（banked 351 → 353 = 0.702 → 0.706，35th consecutive keep，零回滚）

## 本轮 Lane
**March 窗口锚定计数，一机制双面**（C598 队列候选 #2，同机制对 → 一轮双救）：

| qid | 问题 | GT | 证据面 | 旧 pred（诱饵回声） |
|-----|------|----|--------|--------------------|
| a9f6b44c | How many bikes did I service or plan to service in March? | `2` | F1 serviced：road bike @ Pedal Power **March 10th**；F2 plan：commuter bike 换胎意图 + **"this month, before April comes"** | Toyota Camry 汽车保养回声 |
| 00ca467f | How many doctor's appointments did I go to in March? | `2` | Dr. Smith（**March 3rd** went to see）+ Dr. Thompson（**March 20th** follow-up appointment） | bronchitis 咳嗽回声 |

## 机制要点
- **bike 面**：F1 句粒度（allowlisted `<type> bike` + servic(e|ed) + March 日）；F2 **turn 粒度**（换胎意图 + March 锚——bike NP 与锚分属同 turn 兄弟句，句粒度必失配）；turn 粒度安全因为锚文本上钉死 March（'before April comes'）
- **appt 面**：**句粒度是承重墙**——t6 把 "March 15th" 和 "Dr. Smith/Dr. Johnson" 放在不同句（'should discuss with'），turn 粒度会 2→3 多算 johnson
- **序数后缀坑**（第 1 个 face bug）：`\bmarch\s+\d{1,2}\b` 在 "March 10**th**" 失配——`\b` 落在 0 和 t 之间（都是 word char）。修法 `(?:st|nd|rd|th)?` 消费后缀；"March 2023" 仍经回溯正确拒绝
- **F2 守卫坑**（第 2 个 face bug）：`if not keys` 使 F1 命中后 F2 被跳过 → commuter 丢失。F2 必须无条件跑，set 天然去重
- **敬称边界修复**：`_cnt_sents` 按 `.` 切句会把 "Dr. Smith" 切成两半——`_map_sents` 合并以 Dr./Mr./Mrs./Ms./St. 结尾的碎片
- 墙全部逐 turn 钉死：bike rack "two bikes"（复数永不键）/ mountain bike 只 got 水壶架 / 链条清洁≠serviced / 系动词谓语 "just a regular hybrid bike"（无锚不键，hybrid 不计入 → GT 2 非 3）/ lock-computer-shops 修饰语 / 无日期 re-mention / considering Patel 意图 / I'll schedule 将来 / April EMG / PT "since March 25th ... cleared me" 无拜访动词
- 渲染数字 '2'：**三 judge 全绿**（counting_judge 数值 + judge_semantic + exact）

## 选面插曲（C598 队列过时）
- **603deb26 Negroni 已 banked**——answer 门回声恰含 "10 times"，exact 命中 GT；做仲裁 face 零增量
- coordinated-sum（e3038f8c '99' / 60036106 '12,000'）也已 banked
- 教训：**链上查证先于队列信任**——候选先查 live500 chain 的 banked 态再动工
- a9f6b44c 原路由 enum_count（generic block），strict head 先行认领，无测试 pin 冲突（bike_face pin 只要求 != bikes_own）

## 验证链
- census：两 strict head 全 500 各恰 1 行；broad 扫描不偷 bikes_own（6b168ec8/89941a93）、March 兄弟（21d02d0d fun-runs / gpt4_9a159967 airline）；全 haystack 诱饵扫描：bike 面全在 4 session、appt 面全在 3 ANS session，零隐藏面
- TDD 红→绿：28 测试（form claim / no-steal / 42-turn 逐字 fixture + 17 drift pins / 双面 / 墙 / 三 judge）
- suite **11029 green**（11001+28，254s）
- probe（真实 adapter 全路径）：两行 gate=counting，pred '2'，三 judge 全绿
- live500 replay **PASS**（1159s，第 6 次连续首试）：pred 变化恰 {a9f6b44c, 00ca467f}、drift 恰 2 全 False→True、banked 353、abs_banked 18 frozen
- commit `64674a7`（+643/-1：amg_bench_quality.py 3 hunks + test_march_faces.py；staged audit 零外来 hunk，memory_graph.py 外来 +24 未碰）；tsv C599 行已加（710 行）

## 产物
- `/tmp/c599/live500_c599.json`（新权威链）
- `/tmp/c599/{gen_fixture,fixtures_verbatim,decoy_scan,census_march,probe2rows,run_face_tests,run_suite,live500_c599,run_replay,append_tsv}.py`

## 下轮候选（按价值排序）
1. **5a7937c8** faith days December（GT '3 days.'）——句式 GT 需渲染对齐
2. **affe2881** bird species（GT '32'）/ **d682f1a2** food delivery（GT 3）
3. ollama oracle（human-blocked，~169 NJ 级联）仍是最大鱼

## 状态
- **轨迹**：0.502 → … → 0.702(C598) → **0.706(C599)**
- 35 连 keep，零回退；replay 六连首试过
- 权威链：/tmp/c599/live500_c599.json（353/500）
