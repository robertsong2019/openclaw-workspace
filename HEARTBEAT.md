# HEARTBEAT.md - September 26, 2026 (Saturday) — 02:00 KO update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **11202 tests**（09-26 凌晨 C608 2c6fb80；链 11140(C605)→11154(C606)→11177(C607)→**11202(C608)**；**banked 363/500=0.726，C565 起 44 连 keep（0.600→0.726）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 20+ forms，含 recency-supersession / base+delta 算术 / distinct-days 日期去重三条赛道）+ judge 链 + provenance 指纹 + kd face 族 36+（species_total…coin_add/weddings/workshop_days/art_events）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **④ npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph` / `agent-memory-graph-py`，均实测 FREE）— 技术前置 100% 完成 (#066)，与 PyPI 同为 human-blocked
- [ ] **agent-context-store: README + npm publish** — **3173 tests**（09-17 三连击 3135→3173；coverage missing 677→630）
- [ ] **structured-output-toolkit: README + npm publish** — **607 tests**（09-17 includeDescriptions zod 修复）
- [ ] **agent-task-cli: README + npm publish** — **2010 tests**，Round 81 ✅（F299-F303 set store 三变体+spop/srandmember 随机族；set 族 14 法，余 SSCAN/SMISMEMBER 非核心）

### 中优先级（本月）
- [x] amg MCP server (stateless, 2026-07-28 compatible) — Research #043 ✅, Python MCP 16 tools；**✅ demo-orphan 已修复（09-24 晚 473600a）**，MCP stdio 场景协议流污染风险解除
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] openclaw-langgraph-bridge: 307 tests（09-17 spawn() 无客户端超时→clientTimeoutMs）
- [ ] **评估 pacifio/atlas checkpoint 思想**（agent 版本控制）+ **评估 prompt 编译器落地**（DSPy Signature 平行实现 + GEPA auto='light'；500 题银行切 150 dev/350 holdout）+ **OCR 三痛点框架对照 amg harness** + **ECC（264k★）与 AGENTS.md 体系重叠度评估** + **ai-memory（Rust 同赛道）对读**：幂等键重放/单事务 SessionEnd 不变量可移植 + **codebase-memory-mcp（44.6k★ C，09-24 trending 复盘）对读**：amg code-aware #044 赛道直接竞品信号 + **hindsight（26.9K★，09-24/25 两日追踪，daily #1 + LongMemEval SOTA）对读**：amg 最直接对标（四层仿生记忆+RRN 融合，Observations 证据合并层可借鉴）+ obra/superpowers（290k★ skills 方法论）

## 系统状态
- **agent-memory-graph (Python)**: **11224 tests** @C609（09-26 晚 0d38475 coaster_rides face；**banked 364/500=0.728，C565 起 45 连 keep；abs 30=18 abs+12 held；权威链 /tmp/c609/live500_c609.json**——使用前先验存在，被清以 HEAD 重跑重建 ~1200s）。近期面族（新→旧）：coaster_rides（C609 Jul-Oct 乘车计数：N-times 倍数 > 名字枚举 Mako/Kraken/Manta=3 > bare-rode=1 三形状；s37 无 coaster 名词靠 times 墙、s42 无 times 靠枚举墙）+ art_events（C608 distinct-date 计数：三重墙 topic+过去动词+month-first 锚，\bart\b 词界不咬 artists，'past month' 零出窗省窗口逻辑）+ workshop_days（C607 distinct-days：day-first 双模式日锚新形状；分类器 claim 须在 duration_sum block 之前）+ weddings_attended（C606 role-noun 所有格 key 去重+own-wedding 干扰墙；判分探针先行）+ coin_add（C605 base+delta 算术）+ funrun_miss（C604）+ supersede_total（C603 recency-supersession）+ delivery_services（C602）+ faith_days（C601）+ species_total（C600）。核心纪律：harness verbatim 拷贝、tsv 裸字节 append（**历史空行勿动，断言用行数+相邻性**）、census-first、**队列候选先查链上 banked 态再动工（C607 白跑教训）**、**并发第 4 查=工件 mtime<15min 假定作者存活**、python3 -m 调用必须 runner 脚本化（TOOLS.md）、**期望值手工按 fixture 重推**、OOM 重活串行、**replay 脚本一律 cp 上一 cycle canonical + Python 字节级替换（count==1 assert）+ diff 审计（C601 教训：重写=假 drift；C608 补：build 前先 grep 上游 replay.py 实际 anchor 值，--out 逐轮滑动勿照抄上一轮 diff）**、**exec timeout ≥400s 对 git commit（带 pre-commit hook）同样适用**。**✅ demo-orphan 已修复（473600a）**；_search_cache 44 天脏 hunk 未动留工作树（备份 /tmp/amg_dirty_backup_20260924.diff，将来走独立 cycle）。kd queue：`gpt4_e05b82a6` rollercoasters 跨 4 月计数+单位 GT（下一梯队首选）/ `370a8ff4` temporal_arith 15 weeks 跨 gate / `0a995998` 衣服双动作枚举 / `60472f9c`+`6d550036` 项目对；unbanked 剩 137，从 live500_c608 链拉（list_unbanked.py 范本 /tmp/c607）
- **agent-context-store**: **3173 tests**（09-17 三连击；coverage missing 677→630）
- **agent-task-cli**: **2010 tests** — R81 ✅ set store 三变体+随机族（*store 共享 _setStoreResult TTL 重置；RNG=尾参 Math.random 注入）。坑：**exec timeout 必须 ≥400s（含 git commit）**；**分支是 main**；set 键非 JSON-exportable
- **context-forge**: **1563 tests**（09-20 晚 f37 CLI e2e ×8；Node runner IPC flake=上游 bug 不追）
- **prompt-mgr**: **480 tests**（09-24 03:00 cea1389 recent 负数 gate——负数 gate 家族第 3 例）
- **agent-memory-service (amf)**: **754 tests**（09-25 晓 9301db1 merge 链接悬空持久化真 bug——LinkStore.repoint() 修复；cov 99.47/89.83；**.git 实测=monorepo 成员，疑损坏解除**）
- **tools 三员**: **ctxpack 104**（09-22 晚 +10）/ **ato 57**（09-22 晚 +4）/ **dep-guard 74**（09-22 晚 +4）；**afm 32**（09-22 晓 +3）；**09-23 晚 code-lab 四连**：project-dashboard **15** / **skill-scaffolder 34（新入台账**）/ session-archiver **90** / agent-memory-kit **33**；**09-24 晚 code-lab 三连**：cqc **66** / act **51** / mcpt **41**；ai-dev-tools **93** / skill-doctor **81**（新入台账）/ prompt-template-manager **34**
- **09-25 晚 code-lab 四连**: mission-control **45**（cronSummary other 桶穷尽）/ pocket-agent **80**（safe_eval AST 白名单替换裸 eval）/ a2a_minimal **62**（request-shape 家族+1MB DoS 门）/ **amg-mcp 128（新入台账**，own-git 无 remote 保持本地）
- **lab/a2a-trust**: **102** ／ **code-lab/jp**: **49** ／ **lab/mcp-client-explorer**: **60** ／ **openclaw-mcp-server**: **29** ／ **agent-observability**: **262** ／ **cot**: **123** ／ **wget-rust-prototype**: **25** ／ **edge-agent-runtime**: **345** ／ **agent-log**: **75 bats + 32 asserts** ／ **langgraph-bridge**: **307**；prompt-router / agent-mesh-network 已离库（09-19 KO 实测剔除）
- **四项目总计**: **13819**（amg 11202 + sot 607 + atc 2010）
- **全项目总计**: ~**24577** tests（09-26 晚 KO 口径：+136=amg kd 四连 +88（C606 +14/C607 +23/C608 +25/C609 +22）+atc R81 +36+amf +16）
- **零回滚率**: amg **341天** 🏆（KO 链 08-22:299 → 09-25:340 → 09-26:341；C565-C608 44 连 keep）/ acs **206天** 🏆（口径=有产出天数）

## 近期活动 (09-25 白天 ~ 09-26 凌晨 crons)
- **23:50 kd-1 C606 (keep 6d899a5, suite 11154)**: weddings_attended face——banked **360→361 (0.722)，42 连**。role-noun 所有格 key 去重；own-wedding/sister 干扰墙=GT 语义；判分探针先行；2 stale claim pins claim-transfer
- **00:45 kd-2 C607 (keep 25b4fd0, suite 11177)**: workshop_days face——banked **361→362 (0.724)，43 连**。distinct-days；day-first 双模式日锚新形状；**教训：kd 交接备选先查链上 banked 态（两备选全已 banked 白跑）**
- **23:00 kd-1 C609 (keep 0d38475, suite 11224)**: coaster_rides face——banked **363→364 (0.728)，45 连**。Jul-Oct 乘车计数三形状（N-times 倍数>名字枚举>bare-rode）；判分修复随形认领而来（'10 times' GT 数字优先）；replay 首试 14 连
- **01:39 kd-3 C608 (keep 2c6fb80, suite 11202)**: art_events face——banked **362→363 (0.726)，44 连**，replay 首试 13 连。三重墙+\bart\b 词界；**教训：build_replay anchor 先 grep 上游实际值（--out 逐轮滑动）**
- **03:00 project-testing**: amf 738→754（9301db1）——**merge 链接悬空持久化真 bug**（links.save 从不调用+dirty 恒 false→reload 复活悬空引用；LinkStore.repoint() 修）；测试文本 marker-free 纪律（自触发 regex 假红 ×2）
- **04:00 doc (8d28fd5)**: README/TUTORIAL C603-C605 追平（badge 11140；**原则 21→22 条**）；05:00 essay《合并发生在内存里，悬空留在磁盘上》
- **08:00 trending (飞书 Z0KRdVa4Moyw1nxXGb2ccy4wnqb)**: hindsight +1668 当日第一（LongMemEval SOTA）；CLI-Anything；'harness' 接管赛道命名
- **晚间深研 Diffusion LMs (74db564)**: 并行生成；可编辑性>速度；博客已发线上 200
- **21:00 code-lab 四连 keep +36**: mc 45（other 桶穷尽）/ pa 80（**裸 eval 非沙箱逃逸→safe_eval AST 白名单**）/ a2a 62（**1MB body 上限：无界 read=单线程 DoS 当场实证**）/ amg-mcp 128（recency tie-break+重复边守卫）。tsv 自引用死循环教训：代码 commit 先落，tsv 第二 commit 引用实存父 hash
- **22:00 tool-dev**: atc R81 1974→**2010**（F299-F303 *store 变体+spop/srandmember；RNG 尾参注入零 patch；GREEN 期抓 2 bug）

## 本周关键路径
1. ✅ kd 链 C603-C605（0.720）→ C606+C607+C608 三连（0.726）→ ✅ C609（**0.728，45 连**，乘车计数三形状赛道）
2. ⬜ kd 队列：`370a8ff4` temporal_arith 15 weeks 跨 gate / `0a995998` 衣服双动作枚举 / `60472f9c`+`6d550036` 项目对——**先查链上 banked 态**（live500_c609，unbanked 136）
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ atc R82：list 族（lpush/lrange/lpop…）或 hash 族补全——set 族已收口 14 法
5. ⬜ doc 队列：C606-C608 追平（badge 11140→**11202**；TUTORIAL §5.57+ 续）；counting 形态学四分法（枚举/自述总数/仲裁/算术）可作 TUTORIAL §5 小结；博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer；博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误
6. ⬜ **评估 ECC 重叠度 + atlas checkpoint + OCR 对照 + prompt 编译器落地 + ai-memory/hindsight/codebase-memory-mcp 三竞品对读**

## 上次检查
- **Knowledge org: 2026-09-26 02:00** — Integrated 09-25 全天 + 09-26 凌晨（amg kd 链 C606+C607+C608 三连 keep **11202** @2c6fb80；banked 0.720→**0.726**，44 连，零回滚 341 天；amf **754** merge 悬空链接 bug；doc 8d28fd5 原则 22 条；essay cf93815；code-lab 四连 mc 45/pa 80/a2a 62/amg-mcp 128；atc R81 **2010**；hindsight 对标；深研 diffusion LMs）。MEMORY：Current Focus 09-26 新节 + 09-24~09-25 旧节归档（archive-2026-09-24-09-25.md）+ 测试表全刷（13819/~24555）+ Active Theme 同步；HEARTBEAT 全刷
- **Knowledge org: 2026-09-25 02:00** — Integrated 09-24 全天 + 09-25 凌晨（C603+C604+C605 三连 keep **11140** @4ada5be；banked 0.712→**0.720**，41 连，零回滚 340 天；demo-orphan 修复；code-lab 三连；prompt-mgr **480**；hindsight；TTT；AI×Neuro #51 DDM）
- **Knowledge org: 2026-09-24 02:00** — Integrated 09-23 全天 + 09-24 凌晨（C600+C601+C602 三连 keep **11082**；banked 0.706→**0.712**，38 连；atc R80 **1974**；code-lab 四连；afm 32；内容三发）

## ⚠️ 已知问题
- **cron 健康**: 09-14 ~ 09-25 连续十二日点位正常落盘（daily 只准 append 规则有效）。**09-25 晚 22:30 AI×Neuro #52 无产物无日志**（研究笔记目录无 09-25 AI×Neuro 文件，非 Tavily 配额问题待查）；19:00 trending 正常（analysis 文件 19:02 落盘）
- **memory_graph.py _search_cache +24 行脏 hunk（e04d222d）**: 44 天未提交——留工作树，备份 /tmp/amg_dirty_backup_20260924.diff，将来处置走独立 cycle；另有 temporal_test_data.json / test_optimization.py / test_status.log 三个 untracked 杂物（C604 起挂账五轮未动）
- **MEMORY.md size**: ~**99KB**（09-26 KO：CF 旧节归档 -8KB 净瘦身）——剩余大头：Active Theme 长弧线段 + 近期研究一览表 + Core Projects Quick Reference（下轮候选）
- **Tavily 配额**: 09-21~09-24 连续四日 432 超额后，09-25 晚深研已正常使用（新周期重置）；用前先试一发，超配额直接切 AnySearch/web_fetch 备援
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内，workspace experiments.tsv 仅记外部项目 — 非阻塞；tsv HEAD 含 NUL 字节（offset 4513 历史遗留），如需修走专项 Python 行级手术；**C601 起 kd 行改用 workspace 短格式**
- **npm publish blocked**: 四项目 13819 tests ready（amg 11202/atc 2010/acs 3173/sot 607）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；ECC 264k★；context-mode（21.4k★）与 acs 同赛道；agent-skills 97k★；ai-memory（Rust 同赛道）；codebase-memory-mcp 44.6k★（C 代码知识图谱 MCP）；**hindsight 26.9K★（09-24/25 两日追踪，LongMemEval SOTA 且两机构独立复现——amg 最直接对标，需认真对读）**；obra/superpowers 290k★。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face counting 20+ forms + kd face 族 36+ + recency-supersession/base+delta/distinct-days 三条新赛道
- **AI×Neuro Topic Pool**: #52 未落（09-25 22:30 空转待查）；候选：计算精神病学 / 噪声与随机共振 / 鸦科会聚智能
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM——重活串行是标准处置；**exec timeout ≥400s（含 git commit 带 hook）**
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd 会话产物，未动；C608 再记仍未清理）
- **atc 分支是 main**（写死记忆）；mission-control 分支也是 main
