# 2026-09-21 — key-development-3 (C593)

**Cycle:** C593, cron 01:00 +08, lane = C592 队列首位 antique-inherit 家族 head
**Result:** ✅ keep — banked **343→344 (0.686→0.688)**，29 连 keep 零回退

## 目标与结果

| qid | 问题 | GT | 旧 pred | 新 pred |
|-----|------|-----|---------|---------|
| 4f54b7c9 | How many antique items did I inherit or acquire from my family members? | '5' | chit-chat 保险回显 | **'five'** |

- Suite: 10884 → **10904 (+20 subtests)**，exit 0（replay 前绿，零收集漂移）
- Replay: PASS 1144s **一次过**，pred changes / drift 恰 {4f54b7c9}，全 False→True，abs_banked=18 冻结
- Commits: ccd0ecb（代码+测试）、1e4d6b3（tsv 704 行）；`/tmp/c593/live500_c593.json` = 新权威 chain

## Face 设计（antique_inherit，一机制两来源面）

- **无时间窗**——family 来源约束替代窗口（C592 acquire 的 'in the last' 行不动；`_ANT_HEAD_RE` 钉 'antique' + 'famil' 双锚，结构上偷不走它们；census 全 500 恰 1 行）
- **S1 来源窗口面**：信号形容词（antique|vintage|depression-era）+ 物品 NP + 同句 NP 后家庭标记（from my cousin Rachel / came from / belonged to my dad / that belonged to）；标记必须在**该物品自己的窗口**内（本信号形容词 → 下一信号形容词），所以 'an antique music box and a vintage necklace from my mom' 只数 necklace
- **S2 所有格面**：家庭所有格在信号 NP 前（'my grandmother's vintage diamond necklace'）——跨句继承动词（'I inherited it recently' 在下一句）不需要
- 物品键：形容词后最多 3 个 NP 词，介词/关系词/分词墙（'insured'）截断，尾词单数化；9 行重复提及（s21 估价 + s42 保险）折叠成 5 件
- 诱饵全部结构性出局：'old glassware'（无信号）/ 'from a local estate sale'（非家庭）/ 'antique dealers who specialize in tea sets'（窗口纪律）/ 裸 'family heirlooms' 短语 / assistant 保险长文（user 墙）/ 'my grandmother's necklace'（所有格但无信号）
- 渲染纯词形 'five'（双 judge 探针：judge_semantic CORRECT 银行；'five (5)' 会折叠成 '5 5' NEEDS_JUDGE——C591 教训复用）

## 教训（本轮 2 个）

1. **pytest.main runner 也可能空日志失败**（近失误，2 分钟损失）：run_red_c593.py 用 pytest.main + 相对路径参数 → exit 2 + 零输出。TOOLS.md 的 shim 规则只覆盖 `python3 -m`；补强：**face 测试 runner 用 unittest.TextTestRunner + discover 模式（C592 run_face_tests.py 范本），runner 内 os.chdir + 绝对路径**。全量 suite 的 pytest.main（绝对 base + os.chdir）正常。
2. **C592 anti-steal pin 的演化是计划内行为**：`test_form_does_not_steal_antique_head` 钉的是 'enum_count'，注释里写着 "future cycle"——本 cycle 就是那个 future cycle，pin 更新为 'antique_inherit' 并注明因果。pin 演化必须：注释说明哪 cycle 为什么要改、更新前后语义都写清。

## 附带

- 幂等四查全过：tsv 尾=C592、无当日 kd-3 memory、无存活进程（kd-2 收尾后 45 分钟无新工件）、git 与 origin 同步。零竞态。
- 91b15a6e（同干草堆 'minimum amount sold vintage diamond necklace and antique vanity'）确认为 money-form 行，本 head 正确不认领。
- 连续第 3 次 replay 一次过（C592/C593/C591#3）——census-first + miniature-red + 双 judge 纪律的复利。
- 下轮队列：furniture 多动词家族（gpt4_15e38248 buy|assemble|sell|fix）/ list renderer（a40e080f/ceb54acb/8cf51dda——C577 注记称已做，排队前先验证）/ ollama oracle（human-blocked，解锁 ~169 NJ 级联）。
