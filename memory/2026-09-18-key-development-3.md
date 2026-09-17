# 2026-09-18 — key-development-3 (C585)

## Cycle C585: year-begin recall face — KEEP (+1 banked 0.662→0.664, 332/500)

**Cron 任务**: key-development-3 @ 2026-09-18 01:00 (+08)。基线 C584（kd-2 5473b9d/ed7bd33，落地于 01:03——本窗口开始后 3 分钟）。**并发处置**：sessions_list + jsonl mtime 确认 kd-2 会话 01:04 收尾（wrap-up 已发、push 完成 df6da79..ed7bd33），在其静默前不动任何文件；基线按 C584 后的 331 起算。

### 目标裁决
1. **year-begin face 选中（5809eb10）**：C584 队列里 "5809eb10 year-on-user-line face（you-addressed 需求 + user 证据面，新领域）"。问题 "what year the construction of the house began?"，GT "2014."，证据在 **user 粘贴的案情摘要**里（"The construction of the house began in 2014"）——当前 pred 是 speaker_recall 的寄生输出（assistant 改写段落行）。
2. e8a79c70（eggs-quantity）调查后 deferred：需 bullet 侧信道（10 字符句下限丢弃 "-2-3 eggs"）+ session-topic gate 防 "3 large eggs" 诱饵，双机制成本高，留给下一棒。
3. counting-rest（coordinated-sum/枚举计数）维持 C583/C584 两轮 deferred 判决。

### Face 设计（C584 结构性硬过滤教训的年 extraction 应用）
- form gate：recall frame（remind me|you told me|do you remember|i remember）+ "what year <NP> <begin-verb>"（NP = what year 与动词之间的名词短语，支持 did/was/were/is 直接变体）。**census：恰 1/500，且全基准 500 题再无任何其他 "what year" 问题**——零劫持面 by construction。
- 证据侧：句级扫描 `<begin-verb> + in <YEAR>`（began|started|commenced），**demand-NP 结构锚**：NP 的全部实词必须出现在证据句里（"construction"+"house"）。**证据面双角色开放**——事实是 user 说的（粘贴案情），所以不像 chord/sectioned 有 user-role wall；NP 锚 + begin-verb+in+年份 模式代替角色墙封住劫持面。
- 唯一门：全图锚定年份 >1 个不同值 = ambiguous = fall-through（歧义即编造）。render 裸年份，GT "2014." 归一化相等。

### 执行
- census（step2 form census 1/500 + near-miss 全查）→ fixture 生成器 repr 注入 verbatim 5.9KB 案情摘要（compile 验证，09-15 规则）→ RED ImportError → GREEN 16/16（form 接受/did 变体/三拒绝 pin、rescue、双年份 ambiguous、NP 锚脱靶诱饵、无年份证据、同年重复一致、assistant 角色证据、judge pins 含寄生 pred 冻结、adapter gate + flag-off）。
- live probe pre-replay：真实 52-session 全图 → candidates=1、gate=year_begin、judge CORRECT；**4 个相邻 banked 行（chord/demand_noun/counting/sectioned_recall）pred 全部复现 chain**。
- 全 suite：**10765 tests 0F/0E**（301s，串行 OOM 纪律，junitxml）。
- 全 500 replay：**PASS 1198s**——pred changes 恰 {5809eb10}（寄生段落行 → '2014'），drift 恰 1 个 False→True，banked 332/500，abs_banked=18 frozen。chain banked=331 开头验证（无 stale-chain）。
- harness 从 C584 canonical 逐字复制，仅 docstring + 5 个 default 行移动（diff 审计 + compile + stale-ref assert；审计脚本第一版误报自身——新 docstring 合法含 "331 chain"，修正审计而非掩盖）。
- 落地：code **ce0678c**（+269 纯新增：abq +117 / test +152）→ tsv **5299496**；staged audit 逐文件验尸（4 hunks 零删除行）；tsv 追加时产生空行立即发现修复（surgical：只删自建的 695 空行，历史 442 空行不动）；push ed7bd33..5299496。

### 教训
- **结构性判别可迁移**：C584 的 "demand noun = hard filter not score tweak" 直接迁移成年份面的 "NP 全实词锚"——不调分数，让证据在结构上必须含需求的实体词。
- **证据面角色开放时用结构锚代替角色墙**：chord/sectioned 靠 assistant-wall 防劫持，user 证据面（新领域）改靠 NP 锚 + 窄证据模式；census + 全 500 near-miss 全查是零劫持结论的实证。
- **tsv 追加防呆**：文件尾有换行时 `'\n'+row` 会造空行——append 前探测尾字符或 append 后立即 split 验证。
- 幂等三查 + 并发第四查（jsonl mtime + wrap-up 消息）在 kd-1/kd-2/kd-3 窗口重叠（23:00/00:00/01:00 触发、各跑 1-3h）下是刚需。

### 状态
- **21 连 keep，零回退**。轨迹 0.502→…→0.656(C582)→0.658(C583)→0.662(C584)→**0.664(C585)**。
- 新权威 chain：/tmp/c585/live500_c585.json。

### next（队列）
- e8a79c70 eggs-quantity face（bullet 侧信道 + session-topic gate）
- counting-rest coordinated-sum lane（e3038f8c 99=12+57+5+25 / 60036106 12000）
- 830ce83f session-recency relocation / 07741c45 anaphora judging / 9ea5eabc recency priors
- ollama oracle（human-blocked）
