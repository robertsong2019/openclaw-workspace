# key-development-2 — 2026-09-19 (C587, kd-2 00:00 Sat cron)

**结论：keep。banked 333→335 (0.666→0.670)，+2 rescues，0 kill，23 连 keep 零回滚。**
commits `4d5d47c`（代码，+521）+ `2b95f6b`（tsv），push `efab82d..2b95f6b`。
新权威链 `/tmp/c587/live500_c587.json`。suite 10777→10798 全绿后才 replay（1161s PASS）。

## 本轮成果：knowledge-update state faces（双 head 单机制）

C582 遗留族收尾——两个 qid 的 GT 都是**知识的最新状态**，而链上 pred 引用**旧版本**：

| qid | 问题 | 旧 pred（stale） | 新 pred | GT |
|-----|------|------------------|---------|-----|
| 830ce83f | Where did Rachel move to...? | s32 "new apartment in the city" | `the suburbs again` | the suburbs（s45 最新） |
| 07741c45 | Where do I currently keep my old sneakers? | s3 "under my bed" | `in a shoe rack in my closet` | 同（s32 最新，含代词展开） |

机制 = **latest-session-wins 状态召回**：
- **ku_reloc**：名字锚定的 user 句 + moved/relocated (back) to 提取；代词句（"She moved to Chicago."）零贡献（无诚实信号可链回主题，禁止跨句代词链）；winning session 内 >1 目的地 = ambiguous fall-through。census 恰 1/500。
- **ku_storage**：user-role 墙；接受条件 = 存储动词 **OR 现时状态标记词**（currently/right now/...，与问句 recency 词镜像——GT 句 "…in a shoe rack in it, they're **currently** taking up space" 没有 keep 动词！）；loc NP 必须在对象 NP **之后**；`…in it` 尾部做**句内物主先行词展开**（最近的 "my <noun>"，对象词过滤；解析不了就原样渲染，不编造）；**subsumption 去重**（"in a shoe rack" ⊂ "in a shoe rack in my closet" → 留长）；从句截断（for/this/now/...）。

## 🏆 本 cycle 最有价值的拦截（census 阶段）

**孪生题 07741c44 "Where do I initially keep my old sneakers?" 当前 banked=True（GT='under my bed' 旧状态）**。如果 recency 词做成可选修饰词，新 face 会接住它并渲染新状态 → **杀掉一条 banked 行**。裁决：currently/right now/at the moment/these days 是 form **硬要求**，"initially" 结构性出局——**form gate = banked protection**。replay 证实 07741c44 未被触碰。

另有队列过期发现：3249768e 上一轮记为待办，探查发现已 banked（gate=ordinal）→ 划掉，未花一分钟。

## 三个实现 bug（miniature 抓住的）

1. **状态标记缺失**：GT 承重句无 keep 动词 → 加 marker OR-arm + loc-follows-object 规则
2. **期望过度指定**：pronoun 测试期望 no_match，但唯一诚实行为是渲染最近可解析（名字锚定）状态 → **改测试不是改代码**（face 看不见 pronoun 句与主题的关联，假装看不见就是编造）
3. **obj_end 中毒**：锚词 `\bmy\b` 把 "under **my** bed" 里的 my 算进对象结尾 → loc 永远追不上 → 物主/指示限定词从锚模式剔除（_KU_DET）

## C582 判决降级

07741c45 当年判"需要 anaphora-aware judging"（爆炸半径大）。实测先行词 "my closet" 与 "in a shoe rack in it" **同句**，渲染侧展开后现有 containment judge 直接通过——**无需动 judge**。教训：judge 改动判决前，先探渲染侧能不能绕。

## 流程纪律（全部执行）

幂等三查 ✓ → census-first（两 form 各恰 1/500 + near-miss 扫出孪生题）→ TDD red-first（ImportError RED → 修 3 bug → 21 miniatures GREEN，verbatim repr 注入 fixture）→ live probe（真实 47-52 session 图，两目标 + 4 banked 邻居全复现）→ suite 全绿（290s, 0F/0E）→ replay PASS（drift 恰 = 预期集，全 False→True）→ tsv + 2 commits + push。memory_graph.py dirty hunk 未碰未 stage。

## 下轮队列（给 kd-3/kd-1）

- counting-rest coordinated-sum：e3038f8c (99=12+57+5+25)、60036106 (12000) + enum-count (60159905/a3838d2b)——需要算术机制
- 9ea5eabc recency priors——评分侧改动，风险大，需 form 化
- ollama oracle——human-blocked（解锁 ~169 NJ cascade）
- 注意：队列条目先探查再动工（3249768e 教训：可能已被其他 gate 收编）

**轨迹**：0.502 → … → 0.658(C583) → 0.662(C584) → 0.664(C585) → 0.666(C586) → **0.670(C587)**
