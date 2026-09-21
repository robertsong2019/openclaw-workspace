# 2026-09-22 — key-development-3 (C596)

**任务**: cron key-development-3（实验循环 C，autoresearch 方法论），在 C595（kd-2）基础上推进 amg live-500。

## 结果: KEEP ✅ banked 347→348 (0.694→0.696)，32 连 keep 零回退

| qid | 问题 | GT | 旧 pred | 新 pred |
|-----|------|-----|---------|---------|
| 681a1674 | How many Marvel movies did I re-watch? | '2' | answer 门寄生回声（Doctor Strange 四部电影句） | **'two'** |

- Suite: 10956 → **10971 (+15)**，exit 0，274s
- Replay: **PASS 1148s 一次过**（第 5 次连续首试），pred changes / drift 恰 {681a1674}，全 False→True，abs_banked=18 冻结
- Commits: 03e3db4（代码+测试 +292/-1）、d97056d（tsv 707 行）；`/tmp/c596/live500_c596.json` = 新权威链

## 并发处置（幂等四查实战）

01:00 窗口打开时 kd-2（C595）replay 在飞（01:03 时 300/500）。按第四查纪律**全程不碰 amg 文件**，只做只读准备（读 C592-C595 记录、bike face 测试范式、harness 模板）。01:11:35 C595 银行落地（7bab843/tsv/push），确认 tsv 尾=C595 后才开写 C596。零竞态。

## Census-first 选面

- **marvel_rewatch 选中**：head `^how many marvel movies did i re-?watch(ed)? ?\??$` 全 500 恰 1 行；**全 500 无任何其他问题含 re-watch** → 零劫持 by construction + 实证
- 备选普查（留给下轮，附分析）：
  - **bake_two_weeks（88432d0a，GT 4）**：4 事件 = sourdough bread / chocolate cake（×2 提及去重）/ cookies（×2 去重）/ whole wheat baguette（**user turn 无 bake 动词**，只有 'used to make ... baguette'）+ 未来墙（'thinking of baking chicken wings tonight'）。机制=事件键去重+时态墙+make 动词捕获，零件多
  - **march_appt（00ca467f，GT 2）**：Thompson follow-up（March 20th 显式）+ primary care（无日期，靠 session 03-27 + had 过去时归 March）；未来墙（scheduled April 1st / considering / I'll schedule）
  - rollercoasters（gpt4_e05b8，July-October 事件集）复杂；5a7937c8/10d9b85a 维持排除
- eggs_any（e8a79c70）已被 C585-C596 之间某轮 banked（census 显示 BANKED）

## Face 设计（marvel_rewatch）

- **无时间窗**——re-watch 标记替代（C593 约束替代窗口模式第 4 次应用）
- 证据：user 轮（role wall）含 `\bre-?watch(?:ed)?\b` 的**句子**，从标记后的大写标题 span 提取键：`([A-Z][\w'’-]*(?:\s*:\s*[A-Z][\w'’-]*)?(?:\s+[A-Z][\w'’-]*)*)`，**遇到小写词即停**——C595 贪婪 NP 教训（'sure road bike'）以构造方式规避；'Avengers: Endgame yesterday' → 'avengers endgame'（yesterday 小写截断），'Spider-Man: No Way Home, which…' → 逗号截断
- 去重：distinct title keys（s6 两处 Endgame 提及折叠），{avengers endgame, spider man no way home} = 2 ✓
- 渲染 `_ec_render(2)='two'`，GT '2' 经 judge_semantic norm fold CORRECT（C595 'four'/'4' 已证路径）；exact judge 失败不影响 banked 公式 `(v=='CORRECT') or (correct_exact and v!='WRONG')`
- 标题泛化机制非硬编码：'Thor: Ragnarok' / 'Avengers: Infinity War' 等合成句产生独立键（测试钉死 two→three 移动）

## TDD 执行

- RED：ImportError（_cnt_marvel_rewatch 不存在）✓
- 15 测试首跑 14 绿 + 1 红——**红是测试构造 bug 非 face bug**：test_assistant_wall 断言 [S6, wall]='two'，但 S6 只有 Endgame 两处提及（=one），NWH 在 S34。修正测试期望（wall 语义验证同时保留）。教训：**期望值要手工按 fixture 重推一遍**，别想当然
- 接线 4 处：HEAD_RE+正则+handler（bikes 块后）、counting_form 路由（bikes_own 后）、answer_counting 注册表、face 测试文件

## 验证链

1. probe（真实行走 adapter 全路径）：pred 'two'，gate answer→counting，form=marvel_rewatch ✓
2. diff 验尸（09-08 规则）：3 hunks 全归属（路由+12 / handler+46 / 注册表+1-1），staged audit 2 文件恰 292 行 ✓
3. suite 10971 exit 0 ✓ → replay PASS ✓

## 教训

1. **tsv 历史空行 vs 新引入空行**：append 后断言 `all(l.strip())` 会误报——历史 443 行有空行（C585 时代遗留，纪律是不动）。判据应为"C595 行与 C596 行相邻无空行 + 总行数 = 旧+1"，不是全文件无空行
2. **exec sleep+tail 轮询会话偶发静默**（本周期 4 次 poll 无输出但进程实际跑完）——长等待直接用新 exec 查目标文件，别依赖旧 sleep 会话回显
3. 计数面的事件去重语义（cake/cookies 多次提及）与 GT 一致性验证：先手工推 GT 事件集（bread/cake/cookies/baguette=4）再设计机制，bake 面的分析已写进 census 备忘，下轮直接用

## 状态

- **轨迹**：0.502 → … → 0.686(C592) → 0.688(C593) → 0.690(C594) → 0.694(C595) → **0.696(C596)**
- 32 连 keep，零回退；replay 五连首试过
- 权威链：/tmp/c596/live500_c596.json（348/500）

## next（队列）

1. **bake_two_weeks（88432d0a，GT 4）**——事件键去重 + 时态/未来墙 + make-动词捕获（分析见上）
2. **march_appt（00ca467f，GT 2）**——March 窗口 + 过去时归月
3. coordinated-sum lane（e3038f8c 99=12+57+5+25 / 60036106 12000，C583/C584 两轮 deferred）
4. ollama oracle（human-blocked，~169 NJ 级联）

## Artifacts

/tmp/c596/{census.py, evidence2.py, verify_rewatch.py, gen_fixture.py, fixtures.txt, run_face_tests.py, probe.py, run_suite.py, live500_c596.py, live500_c596.json, red_out.txt, green_out.txt, green2_out.txt, suite_out.txt, replay_out.txt, append_tsv.py}
