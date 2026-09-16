# key-development-3 — C582 (2026-09-17)

**任务**: where-face precision（C581 tsv 里排队的 where 族 8 unbanked）。
**结果**: banked 326 → **328** / 500（0.652 → **0.656**），+2 rescue，0 kill。18 连 keep。

## 交付

- commits: **bc109c2**（face + test，+108/−10）→ **36b633e**（tsv 行）；push `179222b..36b633e`
- 链: `/tmp/c582/live500_c582.json` = 新权威 chain（frozen=/tmp/c530/post_cascade500.json, chain=/tmp/c581/live500_c581.json, PYTHONHASHSEED=7 self-re-exec）
- 套件: 10710 tests / 0 failures（junitxml 证据；+6 miniatures `test_where_c582.py`）

## 两条落地面规则（answer_where, amg_bench_quality.py L4940+）

1. **R2 — do-form 降级门**（`_WHERE_DO_RE` + `_where_interrogates_user`）：C541 的意图降级门从 did-form 扩到 do-form 习惯式问句（"Where do I take yoga classes?" 问的是当前现实；"planning to visit Emily / thinking of taking a day trip to Bainbridge Island" 是同一错位）。am-form 刻意不匹配——问句本身就是计划（eace081b banked 守卫）。
2. **R3 — assistant 角色降级**：did/do-form 下只要存在 user 候选就丢弃 assistant 候选（assistant 轮是建议/回声，不是第一人称记忆）。51a45a95：assistant 优惠建议行与 user Target 行 9-9 平分，靠追加顺序赢。

R2 救 **6ade9755**（Serenity Yoga），R3 救 **51a45a95**（Target，superset judge：GT 词全在整句里，冠词/语境差异被 `_SEM_STOPWORDS` 吸收）。

## 横向翻转（已记录爆炸半径）

**gpt4_b5700ca0** wrong→wrong（banked 冻结）：R3 移走了 assistant kh=1 "Focus on How You Feel" 行——它原来是被 C533 relevance floor 选中的；floor 沉默后 kh=0 user 行上位。不正确→不正确，drift 门确认零 banked 影响。exact-change 门因此把 expect 改成 3 qid。

## R1 事件（本 cycle 最重要的方法论时刻）

初始设计含 **R1 realized-past carve-out**（"thinking of going back to Hawaii, ... when I went ..."——意图标记瞄未来、实现动词陈述过去）。第一次 replay **FAIL 得对**：expect 含 e01b8e2f 但无 pred 变化。step6/7 取证：

- e01b8e2f 证据句在 **hay[17] = session_18**，而检索只给了 {session_12, session_7} → **retrieval-miss，不是降级问题**
- R1 在全 500 上零可观测效果 → Simplicity-First 回退，代码注释留"examined and rejected"记录

**关键取证陷阱（写进记忆）**：harness 的 `session_N` 是 haystack_sessions 枚举序号，与 `answer_session_ids` 索引**不对应**。step3 探针里 e01b8e2f 的 "session_7" 其实是铁三计划 session——差点据此造出一条修不到真问题的规则。任何"证据在 session_X"的结论必须用 haystack_session_ids 逐题核对。

## 另一个险情

第一次 replay 启动后 50/500 处发现 **chained sed 把 --out 改了但 --chain 留在 C580**（"chain banked=325"≠预期 326 立刻暴露）——若跑完会把 C581 的 face 变化误报为未设计变化。杀掉重启用显式 `--chain`。**教训：复用 canonical replay 脚本时，chain/out/expect 三个默认值逐个 grep 确认。**

## where 族剩余失败模式地图（下一棒直接用）

| qid | 类别 | 需要什么 |
|---|---|---|
| f8c5f88b | 检索缺失（证据 session_28 不在 13 个检索内） | 检索拓宽 + C508 分心物纪律 |
| e01b8e2f | 检索缺失（session_18） | 同上 |
| gpt4_b5700ca0 | 检索缺失（Episcopal session） | 同上 |
| 830ce83f | 旧州/新州（clean pool 全是 city 线） | session-recency 搬迁 lane |
| 07741c45 | 且回指（"in it" ⊉ "in my closet"，5/7 < 0.75） | anaphora-aware judging |
| 9ea5eabc | superlative（Paris 线 10-11 < Yosemite 12） | recency priors |
| 51a45a95 ✓ 6ade9755 ✓ | — | 已救 |

## Trajectory

0.502 → ... → 0.638 (C578) → 0.648 (C579) → 0.650 (C580) → 0.652 (C581) → **0.656 (C582)**。18 连 keep，零回退。
