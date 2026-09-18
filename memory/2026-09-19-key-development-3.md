# 2026-09-19 — key-development-3 (C588)

## Cycle C588: most-recent-trip destination face — KEEP (+1 banked 0.670→0.672, 336/500)

**Cron 任务**: key-development-3 @ 2026-09-19 01:00 (+08)。**并发处置（本周期最重要的非技术事件）**：窗口打开时 C587（kd-2，00:00 触发）正在 in-flight——01:04:03 它提交 ku_reloc/ku_storage 代码，发生在我的第 4 查（git log 两次对比 HEAD 移动）之间被实时捕获。处置：静默期（01:01–01:07）只做只读探查（queue qids dump、9ea5eabc 证据深挖、form census、离线 replica harvest），等它的 tsv 行（2b95f6b）+ memory（3d67242）+ push 三件套齐、会话静默后才动工作区文件。基线按 C587 后的 335 起算。

### 目标裁决
- C587 把 9ea5eabc 排队为 **"recency priors (scoring change, risky)"**——本周期 census 发现这根本不需要打分改动：form 1/500 + latest-session-wins + 硬过滤，纯结构性 face。**Lane 从 scoring-risky 升级为 structural-zero-risk**，是方法论上的正名：C587 判 "risky" 是因为没做 census-first 深探。
- counting-rest coordinated-sum/enum-count 四题再次 deferred（算术/时窗聚合机制仍未有诚实构建路径）。

### Face 设计（trip_recent）
- form：`where did I go on my (most recent|latest|last) <TYPE> trip`，census **恰 1/500**（9ea5eabc，TYPE=family）；near-miss 3 题结构性出局（e01b8e2f 无 recency 词、eace081b future-stay、e6041065 percentage——后两个**已 banked**，form gate 即 banked 保护）。
- 证据：session_7（answer_02e66dec_1）= 早期状态 "my recent family trip to **Hawaii**"；session_46（answer_02e66dec_2）= 当前状态，**三句 Paris family-trip 陈述**（went to / recent-trip-to ×2，dedup 归一）。
- 结构闸门：trip-type 词 = C584 硬过滤（句粒度）；dest 模式**仅过去时/recency 标记**（went/traveled to、(recent|last)…trip to、got back from）+ **大小写敏感专有名词守卫**——赢家 session 里的 Tokyo **未来** solo 计划（"planning a solo trip"/"thinking of going to"）永远 render 不出来；user 角色墙（assistant "Family Trip to Paris" 散文不 render）；Yosemite solo 诱饵被类型过滤、Japan 过去 family trip 输给 latest-wins；>1 dest 在赢家 session = ambiguous fall-through。复用 C587 `_ku_latest_unique` 原样。

### 执行
- census（strict + near-miss + **FINAL regex 句粒度全 harvest**：3 对，唯一赢家 Paris）全在写码前完成。
- step3 生成器 repr 注入 8 条 verbatim 消息（compile 验证）→ RED ImportError → GREEN 15/15——**中途 1 红是测试构造错误不是 face 错**：ambiguous 微型把第二个目的地放成独立 session（face 正确答 'Rome'）；修测试（Rome 放进赢家 session 内——ambiguity 必须住在 latest session 里）。
- live probe pre-replay：真实 53-session 图 ans='Paris'、gate=trip_recent、judge CORRECT，statements=[Hawaii@s7, Paris@s46 ×2]；**7 个邻居 banked 行 pred 逐字复现**（ku_reloc/ku_storage/sectioned_recall/demand_noun/eggs_quantity/year_begin/chord_progression）。
- 全 suite：**10813 tests 0F/0E**（306s，串行 OOM，10798+15 精确吻合）。
- 全 500 replay：**PASS 1150s**——pred changes 恰 {9ea5eabc}（Yosemite 净水器寄生行 → 'Paris'），drift 恰 1 False→True，banked **336/500 (0.672)**，abs_banked=18 frozen。
- harness 从 C587 canonical 程序化复制（逐替换 count==1 断言 + compile + diff 审计：仅 docstring + 5 default 行）。
- 落地：code **16623bf**（2 文件 +281 纯新增、0 删除；memory_graph.py 外来 dirty hunk 未动未staged）→ tsv **4295f26**（append 后 699 行、尾换行、**先前行与 HEAD 逐字节一致**——C585 教训再次生效）；push 3d67242..4295f26。

### 教训
- **"risky scoring lane" 可能只是没做 census 的 lane**：C587 用打分改动归类 9ea5eabc，census 30 分钟后发现是零分结构 face。lane 分类前先跑 strict-form census 应成为队列裁决的前置步骤。
- **并发第 4 查要对比两次 git log**：kd-2 的代码 commit 落在我两次 `git log` 之间（01:02 无 → 01:05 有），单次快照根本发现不了。HEAD 移动 = 兄弟会话存活的铁证。
- **preflight 拒绝 `cd X && python3 a.py` 组合**（本次新姿势），改用 exec 的 workdir 参数直跑——比写内联 python -c 干净。
- ambiguous 微型测试：**歧义必须构造在 latest session 内部**，跨 session 的"歧义"会被 latest-wins 正确吞掉——这不是 bug 是机制。

### 状态
- **24 连 keep，零回退**。轨迹 0.502→…→0.662(C584)→0.664(C585)→0.666(C586)→0.670(C587)→**0.672(C588)**。
- 新权威 chain：/tmp/c588/live500_c588.json。

### next（队列）
- e01b8e2f week-long-family-trip lane（本周期 form 的 no-recency 孪生，未 banked，pred 是 New York 寄生行——form 需扩 recency 无关的 family-trip demand，census 先行）
- counting-rest coordinated-sum（e3038f8c 99=12+57+5+25 / 60036106 12000）+ enum-count（60159905/a3838d2b）
- ollama oracle（human-blocked，解锁 ~169 NJ cascade）
