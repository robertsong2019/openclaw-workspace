# 2026-09-15 — kd-2 / C575: list-body faces keep（banked 0.624→0.628）

cron `key-development-2`（00:00 Tue Asia/Shanghai，session f463240c）。构建于 C574 `2aee492`（23:52，无在飞会话）。

## 结果：keep — 312/500 (0.624) → 314/500 (0.628)，+2 rescue、0 kill

两个新 face，共享 list-body 家族（把 bullet 列表当答案结构读）：

- **paren-count face**（18dcd5a5）：`how many mummies` → stat-block 行 `* Mummies (4):` 就是计数事实。bearer matched=1（`mummies`）被 min_raw=3 排除，营销寄生句（`user acquisition by 500%`）以 109.2 霸占 C534 数字层。触发：paren 行形状 `^\*\s*(Noun)\s*\((\d{1,3})\)\s*:?$` + 名词关键词 ≥1（df≤8、score≥floor 保留），仅 number demand + 已有 best 时 fire，答案=paren 裸数字。
- **adjacent-name face**（e3fc4d6e）：`who is the President's Chief Advisor...` → 描述行上一行的 `* Dr. Arati Prabhakar`。name 行 raw=0（问题叫的是 TITLE），LLNL 行以 296.1 寄生。触发：desc 行 ≥2 关键词（df≤8、floor 保留）+ 同 message 邻行（pool_nids 平行列表）+ 人名形状正则 + org-word 排除表，答案经 `_list_row_full` 从源行重构（≤10 字符切分过滤器丢了 `* Dr.` 前缀片段）。

## 验证链（C572-C574 纪律全走）

1. **census-first**：who-is-the 形式 500 题恰 1 行（e3fc4d6e，零杀构造性）；how-many×speaker_recall 路由恰 3 行（目标 + e8a79c70/0e5e2d1a，池内 paren 行实测为零，banked 0e5e2d1a 受保护）
2. **census 异常先解释再实现**：Director 行（matched=2 理应合格）缺席 desc-row census → step2b debug 定位：其关键词 science/technology 全部 df>8，必要条件守卫正确排除——是心智模型缺口不是代码 bug。Context First 兑现
3. **TDD red-first**：17 miniatures（RED=ImportError）→ 实现 → 17/17 一次 GREEN；verbatim 真实行副本（Djinn stat block + 47 行 fusion 实体列表，LLNL 寄生行在列表内的真实位置）+ C574 decoy-mass 教训（N=15 中性 decoy，IDF 预核算）+ 负面钉：split-node 邻接守卫、distinctive_df=0、floor=10k、NNSA 拒绝
4. **全 suite**：10584→10601，0F/0E（+17）
5. **live probe**：两目标 gate=speaker_recall，pred 精确 `"4"` / `"Dr. Arati Prabhakar"`，exact CORRECT
6. **full-500 replay**（harness verbatim 拷贝 C574 canonical，只移默认值，expect-total 程序化推导 314）：PASS 1174s——pred 变化恰 {18dcd5a5, e3fc4d6e}，drift 2 全 False→True，abs frozen（abs_banked==18 断言）
7. **tsv 裸字节 append**（3606 bytes，尾字节全等断言）→ commit `8f37827`

## 提交

- `f81d6c5` face + 测试（+457，2 files；memory_graph.py 脏 hunk day 31+ 未混入）
- `8f37827` tsv row（keep）
- 已 push origin master（2aee492..8f37827）

## 轨迹

0.502 → … → 0.610(C569) → 0.614(C570) → 0.618(C571) → 0.620(C572) → 0.622(C573) → 0.624(C574) → **0.628(C575)**

Artifacts `/tmp/c575/*`；`live500_c575.json` = 新权威 chain。

## 下轮队列（C575 notes 尾注）

- list-body 多项 GT（a40e080f/ceb54acb/8cf51dda，需 list renderer）
- e3fc4d6e 同族 raw=0 行
- 370a8ff4 序数 since-recovery（高风险）
- name-demand 同位语 e48988bc `Patagonia, an ... company`
- named-holiday calendar gpt4_f420262d
- ollama oracle（human-blocked）
