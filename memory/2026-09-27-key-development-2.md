# 2026-09-27 — key-development-2 (C610): sports_competitive face

**结果：keep。banked 364 → 365/500（0.730），46 连 keep，15 连 replay 首试 PASS。**

## 本轮做了什么

- 目标 qid: **ef66a6e5** "How many sports have I played competitively in the past?"，GT 'two'，冻结 pred 是 home-insurance 回声句（gate=answer / NEEDS_JUDGE）。
- 机制：新 form `sports_competitive`——strict head（census 1/500，claim 在 coaster 之后、generic duration_sum 之前）+ 双墙：
  - 过去习惯墙 `\bused\s+to\s+(?:play|swim)\b`
  - 竞技语域墙 `\bcompetitiv`
  - sport key：动词直连 swim（三种 rephrase 折叠成一个 key）；`play <名词>` 取名词（tennis）；set-dedup 加法 → distinct count = 2
- 暗区钉死：gerund 习惯（"used to swimming competitively" 无 play|swim 词干）、现在时玩（"I've been playing soccer and tennis lately"）、yoga 课表、"competitive prices"、assistant 回声（"competitive background"/"former competitive tennis player"——role 墙兜底）。
- 判分：渲染 '2'，counting_judge 数值优先（GT 'two' 走 `_cnt_numval` 平价，C606 先例）。

## 事故与教训（已记 error-patterns.md 第 1 次）

**`_SPT_` 前缀撞名**：我把新正则起名 `_SPT_*`，臆断是 "SPortS"——实际是 **C600 species 家族**的既有前缀（`_SPT_HEAD_RE` 被 species claim + handler guard 引用）。模块级 shadow → species 路由断崖（claim 落 enum_count、guard 返 None），全量 suite 首跑 **7 红**。22 个 face 测试全绿（我的定义是幸存者）——**face-only 绿对跨 face 冲突是盲的**。改名 `_SPORT_`（grep 确认无占用）后 11246 全绿。

规则：amg_bench_quality.py 加模块级名字前必须查**前缀级**冲突（`grep -n "_<PREFIX>_"`），不是只查全名。

## 验证链

| 关卡 | 结果 |
|------|------|
| RED | ImportError（预期） |
| face GREEN | 22/22 |
| 全量 suite | 11224→**11246**（首跑 7 红→改名后全绿，245s） |
| 真实 adapter probe | ef66a6e5 → form=sports_competitive, pred='2', judge('two','2')=True；9 banked 邻居 + 3 loose sport 表亲全部 form=None/不动 |
| full-500 replay | PASS：pred-change==drift=={ef66a6e5}（False→True），banked **365**（1161s） |

## 工件

- amg commit: **483b3fa**（amg_bench_quality.py +82/-1、test_sports_competitive_face.py 22 tests）
- ledger: experiments.tsv C610 行
- 链：/tmp/c610/live500_c610.json（chain 来自 /tmp/c609/live500_c609.json）
- 脏文件隔离：memory_graph.py(+24) / temporal_test_data.json / test_optimization.py / test_status.log 非本 cycle，未卷入 commit

## 链状态（留给下一轮）

- banked **365/500 (0.730)**，unbanked 135
- 权威链 /tmp/c610/live500_c610.json；suite 基线 11246
- amg head 483b3fa（C610 后）
- 下一轮候选：unbanked 清单里 doctors/kitchen/clothing/albums 等 counting 行仍有证据缺口；C608 留的 gpt4_e061b84g（sports event two weeks ago，NEEDS_JUDGE）是 loose 表亲但 head 不同，需另设计
- replay harness：/tmp/c610/{replay.py, build_replay.py}（build 锚点经 grep 验证，byte-level count==1 替换——C608 教训沿用）
