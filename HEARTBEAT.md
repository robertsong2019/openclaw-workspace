# HEARTBEAT.md - September 25, 2026 (Friday) — 02:00 KO update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **11140 tests**（09-25 凌晨 C605 4ada5be；链 11082(C602)→11102(C603)→11121(C604)→**11140(C605)**；**banked 360/500=0.720，C565 起 41 连 keep（0.600→0.720）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 20+ forms，含 recency-supersession C603 / base+delta 算术 C605 两条新赛道）+ judge 链 + provenance 指纹 + speaker_recall face 族（speech-act…species_total/faith_days/delivery_services/supersede_total/funrun_miss/coin_add）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **④ npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph` / `agent-memory-graph-py`，均实测 FREE）— 技术前置 100% 完成 (#066)，与 PyPI 同为 human-blocked
- [ ] **agent-context-store: README + npm publish** — **3173 tests**（09-17 三连击 3135→3173；coverage missing 677→630）
- [ ] **structured-output-toolkit: README + npm publish** — **607 tests**（09-17 includeDescriptions zod 修复）
- [ ] **agent-task-cli: README + npm publish** — **1974 tests**，Round 80 ✅（F296-F298 set 代数三法；余 spop/srandmember + *store 变体）

### 中优先级（本月）
- [x] amg MCP server (stateless, 2026-07-28 compatible) — Research #043 ✅, Python MCP 16 tools；**✅ demo-orphan 已修复（09-24 晚 473600a）**，MCP stdio 场景协议流污染风险解除
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] openclaw-langgraph-bridge: 307 tests（09-17 spawn() 无客户端超时→clientTimeoutMs）
- [ ] **评估 pacifio/atlas checkpoint 思想**（agent 版本控制）+ **评估 prompt 编译器落地**（DSPy Signature 平行实现 + GEPA auto='light'；500 题银行切 150 dev/350 holdout）+ **OCR 三痛点框架对照 amg harness** + **ECC（264k★）与 AGENTS.md 体系重叠度评估** + **ai-memory（Rust 同赛道）对读**：幂等键重放/单事务 SessionEnd 不变量可移植 + **codebase-memory-mcp（44.6k★ C，09-24 trending 复盘）对读**：amg code-aware #044 赛道直接竞品信号 + **hindsight（26.9K★，09-24 晚 daily #1）对读**：amg 最直接对标（LongMemEval SOTA，两机构独立复现）+ obra/superpowers（290k★ skills 方法论）

## 系统状态
- **agent-memory-graph (Python)**: **11140 tests** @C605（09-25 凌晨 4ada5be coin_add face；**banked 360/500=0.720，C565 起 41 连 keep；abs 30=18 abs+12 held；权威链 /tmp/c605/live500_c605.json**——使用前先验存在，被清以 HEAD 重跑重建 ~1200s）。近期面族（新→旧）：coin_add（C605 knowledge-update base+delta 算术：37 base 声明+delta "just added"，delta 只计严格晚于 base session，早/同 session 视作已烘进 base）+ funrun_miss（C604 四重墙 fun-run+miss 动词+work 归因+March day；'missing' 动名词 \b 坑）+ supersede_total（C603 recency-supersession 首赛道：latest-session-wins，双脸 followers/stories，渲染 as stated+判分探针先行）+ delivery_services（C602）+ faith_days（C601）+ species_total（C600）+ march-window（C599）+ cum_total（C598）+ bake_two_weeks（C597）+ marvel_rewatch（C596）+ bikes_own（C595）+ furniture_txn（C594）+ antique_inherit（C593）+ acquire（C592）。核心纪律：harness verbatim 拷贝、tsv 裸字节 append（**历史空行勿动，断言用行数+相邻性**）、census-first、**队列候选先查链上 banked 态再动工**、**并发第 4 查=工件 mtime<15min 假定作者存活**、python3 -m 调用必须 runner 脚本化（TOOLS.md）、**期望值手工按 fixture 重推**、OOM 重活串行、**replay 脚本一律 cp 上一 cycle canonical + Python 字节级替换（count==1 assert）+ diff 审计（C601 教训：重写=假 drift；C603 补：sed 同名链替换会串行命中→改 Python 替换；C604 落地）**、**exec timeout ≥400s 对 git commit（带 pre-commit hook）同样适用**。**✅ demo-orphan 已修复（473600a）**；_search_cache 44 天脏 hunk 未动留工作树（备份 /tmp/amg_dirty_backup_20260924.diff，将来走独立 cycle）。kd queue：`gpt4_2f8be40d` weddings（三候选最后遗留：own-wedding 排除+this-year 窗口，GT 整句枚举渲染风险，**判分探针先行**）+ census 从 live500_c605 链 ~140 unbanked 挖新 face
- **agent-context-store**: **3173 tests**（09-17 三连击；coverage missing 677→630）
- **agent-task-cli**: **1974 tests** — R80 ✅ set 代数三法（sinter/sunion/sdiff；共享 _setViewsFor；sdiff 只读）。坑：**exec timeout 必须 ≥400s（含 git commit）**；**分支是 main**；set 键非 JSON-exportable
- **context-forge**: **1563 tests**（09-20 晚 f37 CLI e2e ×8；Node runner IPC flake=上游 bug 不追）
- **prompt-mgr**: **480 tests**（09-24 03:00 cea1389 recent 负数 gate——负数 gate 家族第 3 例）
- **tools 三员**: **ctxpack 104**（09-22 晚 +10）/ **ato 57**（09-22 晚 +4）/ **dep-guard 74**（09-22 晚 +4）；**afm 32**（09-22 晓 +3）；**09-23 晚 code-lab 四连**：project-dashboard **15**（git-status 只认 M/A/D）/ **skill-scaffolder 34（新入台账**；../escape 路径穿越）/ session-archiver **90**（分母平行常量+negative-days gate）/ agent-memory-kit **33**（prune -5 清全库+merge 自合并）；**09-24 晚 code-lab 三连**：cqc **66**（--format 静默回落+CI 门放行崩溃检查）/ act **51**（budget 平行常量背离 calculateCost 收口）/ mcpt **41**（EISDIR isFile 门）；ai-dev-tools **93** / skill-doctor **81**（新入台账）/ prompt-template-manager **34**
- **lab/a2a-trust**: **102** ／ **pocket-agent**: **72** cov 98% ／ **code-lab/jp**: **49** ／ **mission-control**: **33** cov 99% ／ **lab/mcp-client-explorer**: **60** ／ **openclaw-mcp-server**: **29** ／ **agent-observability**: **262** ／ **cot**: **123** ／ **a2a_minimal**: **48** ／ **wget-rust-prototype**: **25** ／ **edge-agent-runtime**: **345** ／ **agent-log**: **75 bats + 32 asserts** ／ **agent-memory-service**: **738**（⚠️ .git 疑似损坏，动前实测）／ **langgraph-bridge**: **307**；prompt-router / agent-mesh-network 已离库（09-19 KO 实测剔除）
- **四项目总计**: **13721**（amg 11140 + sot 607 + atc 1974）
- **全项目总计**: ~**24405** tests（09-25 KO 口径：+63=amg kd 三连 +58（C603 +20/C604 +19/C605 +19）+prompt-mgr +5）
- **零回滚率**: amg **340天** 🏆（KO 链 08-22:299 → 09-24:339 → 09-25:340；C565-C605 41 连 keep）/ acs **206天** 🏆（口径=有产出天数）

## 近期活动 (09-24 白天 ~ 09-25 凌晨 crons)
- **23:44 kd-1 C603 (keep 646efa6, suite 11102)**: supersede_total 双脸——banked **356→358 (0.716)，39 连**。**新赛道 recency supersession**：两声明形状相同只能靠 session 序仲裁（latest-session-wins）；判分探针先行定渲染策略；census 从 144 unbanked 找同机制对
- **00:38 kd-2 C604 (keep 6b4c8dc, suite 11121)**: funrun_miss face——banked **358→359 (0.718)，40 连**。四重墙（fun-run+miss+work+March day）；'missing' 动名词 \b 坑；replay 改 Python 字节级替换
- **01:37 kd-3 C605 (keep 4ada5be, suite 11140)**: coin_add face——banked **359→360 (0.720)，41 连**，replay 首试 11 连。**新赛道 knowledge-update base+delta 算术**：37 base+delta 严格晚于 base session 才计；anaphoric 'in that collection' 键
- **22:00 tool-dev**: amg demo-orphan 修复（473600a keep）——C501 删行事故收口，import 静默；44 天脏 hunk 手术式避开（staged 验尸 1 file +2 lines）
- **21:18 code-lab-evening**: 双触发拦截（另一会话 3 commit 未 push 未记账→复验+补 TSV+push）+ cqc 66/act 51/mcpt 41 三 keep（+47）；MEMORY commit 31dfcbc staged-diff 超预期→验尸基准=启动时快照
- **03:00 project-testing**: prompt-mgr recent 负数 gate 475→480（cea1389）——负数 gate 家族第 3 例；ai-dev-tools 假红陷阱（ESM 须 npm test）
- **04:00 doc (4c151ed)**: README/TUTORIAL C600-C602 追平（badge 11082；原则 21 条）；**05:00 essay《负数是合法的谎言》(729f109)**
- **08:00/19:00 trending**: google/ax+substrate（agent infra 云原生分层）；**hindsight 26.9K★=amg 最直接对标**；open-code-review 40.5K★（确定性×Agent）；colibri 37.4K★（纯 C MoE）
- **20:00 深研 TTT (873826b)**: Test-Time Training 14 篇；博客已发
- **22:30 AI×Neuro #51**: 决策的数学——DDM 与 LLM 采样式推理（LIP↔test-time scaling 同构；飞书 RmwEdIIkToJFZlx2yL1cDcOunyg，129 blocks）

## 本周关键路径
1. ✅ kd 链 C600-C602（0.712）→ ✅ C603+C604+C605 三连（**0.720，41 连**，recency-supersession + base+delta 两条新赛道）
2. ⬜ kd 队列：weddings `gpt4_2f8be40d`（最后遗留候选，GT 整句枚举渲染风险，判分探针先行）+ census 从 live500_c605 ~140 unbanked 挖新 face（先查链上 banked 态）
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ atc R81：spop/srandmember（随机族，需 RNG 钩子决策）+ sinterstore/sunionstore/sdiffstore 变体
5. ⬜ doc 队列：C603-C605 追平（badge 11082→**11140**；TUTORIAL §5.54+ 续；demo-orphan 473600a 补记）；博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer；博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误
6. ⬜ **评估 ECC 重叠度 + atlas checkpoint + OCR 对照 + prompt 编译器落地 + ai-memory/hindsight/codebase-memory-mcp 三竞品对读**

## 上次检查
- **Knowledge org: 2026-09-25 02:00** — Integrated 09-24 全天 + 09-25 凌晨（amg kd 链 C603+C604+C605 三连 keep **11140** @4ada5be；banked 0.712→**0.720**，41 连，零回滚 340 天；demo-orphan 修复 473600a；code-lab 三连 cqc 66/act 51/mcpt 41；prompt-mgr **480** 负数 gate 第 3 例；hindsight 对标信号；TTT 深研；AI×Neuro #51 DDM）。MEMORY：Current Focus 09-25 新节 + 09-23~09-24 旧节归档（archive-2026-09-23-09-24.md）+ 测试表全刷（13721/~24405）+ Quick Reference 同步；HEARTBEAT 全刷
- **Knowledge org: 2026-09-24 02:00** — Integrated 09-23 全天 + 09-24 凌晨（C600+C601+C602 三连 keep **11082** @a67cfa0；banked 0.706→**0.712**，38 连，零回滚 339 天；atc R80 **1974**；code-lab 四连；AI×Neuro #50 好奇心）
- **Knowledge org: 2026-09-23 02:00** — Integrated 09-22 全天 + 09-23 凌晨（C597+C598+C599 三连 keep **11029**；banked 0.706，35 连；atc R79 **1948**；code-lab 四连；afm 32；内容三发）

## ⚠️ 已知问题
- **cron 健康**: 09-14 ~ 09-24 连续十一日全点位正常落盘（09-21 20:00 覆盖事故后无复发；daily 只准 append 规则有效）
- **memory_graph.py demo-orphan（已修复 09-24 晚 473600a）**: import 静默零副作用；_search_cache +24 行脏 hunk（e04d222d）仍未提交——留工作树，备份 /tmp/amg_dirty_backup_20260924.diff，将来处置走独立 cycle
- **MEMORY.md size**: ~**121KB**（09-25 KO：CF 旧节归档 -2 节 + 新节 +1，净 +2KB）——剩余大头：Active Theme 长弧线段 + 近期研究一览表 + Core Projects Quick Reference（下轮候选）
- **Tavily 配额**: 09-21~09-24 连续四日 432 超额（search/research/日报三线），AnySearch(mcporter) + web_fetch/arXiv API + curl raw.githubusercontent.com 降级路径全稳定；新周期可能已重置——**用前先试一发**，超配额直接切备援
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内，workspace experiments.tsv 仅记外部项目 — 非阻塞；tsv HEAD 含 NUL 字节（offset 4513 历史遗留），如需修走专项 Python 行级手术；**C601 起 kd 行改用 workspace 短格式**
- **npm publish blocked**: 四项目 13721 tests ready（amg 11140/atc 1974/acs 3173/sot 607）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；ECC 264k★；context-mode（21.4k★）与 acs 同赛道；agent-skills 97k★；ai-memory（Rust 同赛道）；codebase-memory-mcp 44.6k★（C 代码知识图谱 MCP，amg code-aware 直接竞品）；**hindsight 26.9K★（09-24 晚 daily #1，LongMemEval SOTA 且两机构独立复现——amg 最直接对标，需认真对读）**；obra/superpowers 290k★（skills 方法论）。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face counting 20+ forms + kd face 族 33+ + recency-supersession/base+delta 两条新赛道
- **AI×Neuro Topic Pool**: 备选库用尽后自创题线已到 **#51（决策的数学-DDM，已发）**；#52 候选：计算精神病学 / 噪声与随机共振 / 鸦科会聚智能
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM——重活串行是标准处置；**exec timeout ≥400s（含 git commit 带 hook）**
- **amfs .git 疑似损坏**: agent-memory-service git -C 落到 monorepo——下次动 amfs 前先实测 `ls projects/agent-memory-service/.git`
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd 会话产物，未动；C605 再记仍未清理）
- **atc 分支是 main**（写死记忆）
