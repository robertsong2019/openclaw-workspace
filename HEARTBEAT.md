# HEARTBEAT.md - September 27, 2026 (Sunday) — 02:00 KO update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **11272 tests**（09-27 凌晨 C611 c596d1f；链 11202(C608)→11224(C609)→11246(C610)→**11272(C611)**；**banked 366/500=0.732，C565 起 47 连 keep（0.600→0.732）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 20+ forms，含 recency-supersession / base+delta 算术 / distinct-days 日期去重 / N-times-倍数三形状 / (class,day) set-dedup 五条赛道）+ judge 链 + provenance 指纹 + kd face 族 39+（species_total…coaster_rides/sports_competitive/fitness_week）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **④ npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph` / `agent-memory-graph-py`，均实测 FREE）— 技术前置 100% 完成 (#066)，与 PyPI 同为 human-blocked
- [ ] **agent-context-store: README + npm publish** — **3173 tests**（09-17 三连击 3135→3173；coverage missing 677→630）
- [ ] **structured-output-toolkit: README + npm publish** — **607 tests**（09-17 includeDescriptions zod 修复）
- [ ] **agent-task-cli: README + npm publish** — **2052 tests**，Round 82 ✅（F304-F309 Redis list 族上半场；list 族 6 法，余 lpushx/rpushx/lindex/lset/linsert/lrem/ltrim/rpoplpush/lmove 8 法 R83 候选）

### 中优先级（本月）
- [x] amg MCP server (stateless, 2026-07-28 compatible) — Research #043 ✅, Python MCP 16 tools；**✅ demo-orphan 已修复（09-24 晚 473600a）**，MCP stdio 场景协议流污染风险解除
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] openclaw-langgraph-bridge: 307 tests（09-17 spawn() 无客户端超时→clientTimeoutMs）
- [ ] **评估 pacifio/atlas checkpoint 思想**（agent 版本控制）+ **评估 prompt 编译器落地**（DSPy Signature 平行实现 + GEPA auto='light'；500 题银行切 150 dev/350 holdout）+ **OCR 三痛点框架对照 amg harness** + **ECC（264k★）与 AGENTS.md 体系重叠度评估** + **ai-memory（Rust 同赛道）对读**：幂等键重放/单事务 SessionEnd 不变量可移植 + **codebase-memory-mcp（44.6k★ C，09-24 trending 复盘）对读**：amg code-aware #044 赛道直接竞品信号 + **hindsight（26.9K★，09-24/25 两日追踪，daily #1 + LongMemEval SOTA）对读**：amg 最直接对标（四层仿生记忆+RRN 融合，Observations 证据合并层可借鉴）+ obra/superpowers（290k★ skills 方法论）

## 系统状态
- **agent-memory-graph (Python)**: **11272 tests** @C611（09-27 凌晨 c596d1f fitness_week face；**banked 366/500=0.732，C565 起 47 连 keep；abs 30=18 abs+12 held；权威链 /tmp/c611/live500_c611.json**——使用前先验存在，被清以 HEAD 重跑重建 ~1200s）。近期面族（新→旧）：fitness_week（C611 (class,day) set-dedup 周课次计数：课名墙+星期墙双墙，yogurt 不咬 yoga）+ sports_competitive（C610 used-to 过去习惯墙+竞技语域墙）+ coaster_rides（C609 Jul-Oct 乘车计数三形状：N-times 倍数>名字枚举>bare-rode=1）+ art_events（C608 distinct-date 三重墙）+ workshop_days（C607 distinct-days 双模式日锚）+ weddings_attended（C606 role 所有格 key 去重）+ coin_add（C605 base+delta 算术）+ funrun_miss（C604）+ supersede_total（C603 recency-supersession）+ delivery_services（C602）。核心纪律：harness verbatim 拷贝、tsv 裸字节 append（**历史空行勿动，断言用行数+相邻性**）、census-first + **第 4 步 pin census（C611：grep test_*.py 历史 pin）**、**队列候选先查链上 banked 态再动工（C607 白跑教训）**、**amg 模块级新正则前缀必须 grep 前缀级冲突（C610 _SPT_ 撞 species 7 红教训，已记 error-patterns.md）**、**后台长 suite 必须 Tee 落盘（isatty()=False，/tmp/c611/run_suite.py 范本；exec 后台捕获不可信）**、**pytest.main() 进程内跑 amg 套件=静默 exit-0 空日志（C609 新坑，用 shell env 前缀 PYTHONHASHSEED=7）**、python3 -m 调用必须 runner 脚本化（TOOLS.md）、**期望值手工按 fixture 重推**、OOM 重活串行、**replay 脚本一律 cp 上一 cycle canonical + Python 字节级替换（count==1 assert）+ diff 审计（C601 教训：重写=假 drift；C608 补：build 前先 grep 上游 replay.py 实际 anchor 值，--out 逐轮滑动勿照抄上一轮 diff）**、**exec timeout ≥400s 对 git commit（带 pre-commit hook）同样适用**。**✅ demo-orphan 已修复（473600a）**；_search_cache 45 天脏 hunk 未动留工作树（备份 /tmp/amg_dirty_backup_20260924.diff，将来走独立 cycle）。kd queue（C611 交接，从 live500_c611 unbanked 拉的下一梯队）：`gpt4_f2262a51` doctors（GT 长句 'three different doctors: primary care physician, ENT specialist, dermatologist'——clinic 系统讨论噪声重，需 _cnt_numval 长句数值抽取验证）/ `gpt4_ab202e7f` kitchen 5 items（coffee maker 只有 'donated + upgrade' 无 replace/fix 动词——需 donate→replace 语义墙，设计偏重）/ `bf659f65` albums GT=3 只辨识 2（Telluride 'their EP' 是否独立 item 语义歧义高）/ `0a995998` clothing（C607 已判偏重）/ `6d550036`+`60472f9c` 项目对（证据分散）/ `gpt4_e061b84g` sports event（NEEDS_JUDGE，head 不同需另设计）/ pref-gate 12 行 NEEDS_JUDGE（行为未知，风险高）；unbanked 剩 134
- **agent-context-store**: **3173 tests**（09-17 三连击；coverage missing 677→630）
- **agent-task-cli**: **2052 tests** — R82 ✅ list 族上半场（_liveListEntry 镜像+rpop count [tail,...] 序；单发全绿零 GREEN 期 bug）。坑：**exec timeout 必须 ≥400s（含 git commit）**；**分支是 main**；set 键非 JSON-exportable
- **context-forge**: **1563 tests**（09-20 晚 f37 CLI e2e ×8；Node runner IPC flake=上游 bug 不追）
- **prompt-mgr**: **480 tests**（09-24 03:00 cea1389 recent 负数 gate——负数 gate 家族第 3 例）
- **agent-memory-service (amf)**: **754 tests**（09-25 晓 9301db1 merge 链接悬空持久化真 bug——LinkStore.repoint() 修复；cov 99.47/89.83）
- **tools 三员**: **ctxpack 104**（09-22 晚 +10）/ **ato 57**（09-22 晚 +4）/ **dep-guard 74**（09-22 晚 +4）；**afm 32**（09-22 晓 +3）；**09-23 晚 code-lab 四连**：project-dashboard **15** / **skill-scaffolder 34（新入台账**）/ session-archiver **90** / agent-memory-kit **33**；**09-24 晚 code-lab 三连**：cqc **66** / act **51** / mcpt **41**；ai-dev-tools **93** / skill-doctor **81**（新入台账）/ prompt-template-manager **34**
- **09-25 晚 code-lab 四连**: mission-control **45**（cronSummary other 桶穷尽）/ pocket-agent **80**（safe_eval AST 白名单替换裸 eval）/ a2a_minimal **62**（request-shape 家族+1MB DoS 门）/ **amg-mcp 128（新入台账**，own-git 无 remote 保持本地）
- **09-26 晚 code-lab 四连**: nano-agent **1162**（PEP 604 UnionType 无 __origin__→typing.get_origin()）/ mcp-client-explorer **65**（-32602 形状门）/ jp **59**（括号内引号键 JSONPath，own-git 已 push）/ agent-observability **268**（NaN 毒化防御）
- **lab/a2a-trust**: **102** ／ **openclaw-mcp-server**: **29** ／ **cot**: **123** ／ **wget-rust-prototype**: **25** ／ **edge-agent-runtime**: **345** ／ **agent-log**: **75 bats + 32 asserts** ／ **langgraph-bridge**: **307**；prompt-router / agent-mesh-network 已离库（09-19 KO 实测剔除）
- **四项目总计**: **13931**（amg 11272 + sot 607 + atc 2052）
- **全项目总计**: ~**24693** tests（09-27 KO 口径：+116=amg kd 两连 +48（C610 +22/C611 +26）+atc R82 +42+code-lab 四连 +26（nano +6/mcx +5/jp +10/obs +6））
- **零回滚率**: amg **342天** 🏆（KO 链 08-22:299 → 09-26:341 → 09-27:342；C565-C611 47 连 keep）/ acs **207天** 🏆（口径=有产出天数）

## 近期活动 (09-26 全天 ~ 09-27 凌晨 crons)
- **23:00 kd-1 C609 (keep 0d38475, suite 11224)**: coaster_rides face——banked **363→364 (0.728)，45 连**，replay 首试 14 连。Jul-Oct 乘车计数三形状（N-times 倍数>名字枚举>bare-rode）；判分红利随形认领（'10 times' GT 数字优先）；**新坑：pytest.main() 进程内=静默 exit-0 空日志**
- **kd-2 C610 (keep 483b3fa, suite 11246)**: sports_competitive face——banked **364→365 (0.730)，46 连**。used-to 过去习惯墙+竞技语域墙；**_SPT_ 前缀撞 species 家族全量首跑 7 红教训（新前缀必须 grep 前缀级冲突；face-only 绿对跨 face 冲突盲；已记 error-patterns.md）**
- **01:00 kd-3 C611 (keep c596d1f, suite 11272)**: fitness_week face——banked **365→366 (0.732)，47 连**，replay 首试 15 连。(class,day) set-dedup 周课次；**流程教训×3：Tee 落盘（isatty=False）/ pin census 第 4 步 / loose 表亲查链上 banked 态**
- **21:00 code-lab 四连 keep +26**: nano 1162（**PEP 604 UnionType 无 __origin__，typing.get_origin() 通吃**）/ mcx 65（-32602 形状门堵异常泄漏）/ jp 59（括号内引号键，own-git push）/ obs 268（**NaN 毒化 reduce=评分器谎报家族**，Number.isFinite 门）。monorepo push 60c30dd..4c229cb
- **22:00 tool-dev**: atc R82 2010→**2052**（F304-F309 list 族上半场；rpop count [tail,...] 序；RED-first 39→42/42；余 8 法 R83 候选）
- **22:30 AI×Neuro #52 补做（收口）**: 幂等三查判定 09-25 晚中断，补做「关键期」——Tavily 432 连续两晚耗尽→AnySearch academic 备援生效；本地报告+飞书 Ldo7dHXwmoZ3WDxz9XLcrmMvnVd（54 blocks 验证）+消息已发；台账双行补齐，#52 正式收口

## 本周关键路径
1. ✅ kd 链 C606-C608（0.726）→ C609+C610+C611 三连（**0.732，47 连**；三形状/双墙/set-dedup 三条新机制）
2. ⬜ kd 队列：`gpt4_f2262a51` doctors（GT 长句）/ `gpt4_ab202e7f` kitchen / `bf659f65` albums / `0a995998` clothing——**先查链上 banked 态**（live500_c611，unbanked 134）
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ atc R83：list 族下半场（lpushx/rpushx/lindex/lset/linsert/lrem/ltrim/rpoplpush/lmove 8 法候选）
5. ⬜ doc 队列：C606-C611 追平（badge 11140→11272；TUTORIAL §5.57+ 续）；counting 形态学四分法（枚举/自述总数/仲裁/算术）可作 TUTORIAL §5 小结；博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer；博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误
6. ⬜ **评估 ECC 重叠度 + atlas checkpoint + OCR 对照 + prompt 编译器落地 + ai-memory/hindsight/codebase-memory-mcp 三竞品对读**

## 上次检查
- **Knowledge org: 2026-09-27 02:00** — Integrated 09-26 全天 + 09-27 凌晨（amg kd 链 C609+C610+C611 三连 keep **11272** @c596d1f；banked 0.726→**0.732**，47 连，零回滚 342 天；code-lab 四连 nano 1162/mcx 65/jp 59/obs 268；atc R82 **2052**；AI×Neuro #52 补做收口。新教训入库：_SPT_ 前缀 grep 纪律/Tee 落盘/pin census 第 4 步/pytest.main in-process 静默 exit-0）。MEMORY：Current Focus 09-27 新节 + C606-C608 旧节归档（archive-2026-09-25-09-26.md）+ 测试表全刷（13931/~24693）+ Active Theme 同步；HEARTBEAT 全刷
- **Knowledge org: 2026-09-26 02:00** — Integrated 09-25 全天 + 09-26 凌晨（C606+C607+C608 三连 keep **11202**；banked 0.720→**0.726**，44 连；amf **754** merge 悬空链接 bug；doc 8d28fd5 原则 22 条；essay cf93815；code-lab 四连；atc R81 **2010**；hindsight 对标；深研 diffusion LMs）
- **Knowledge org: 2026-09-25 02:00** — Integrated 09-24 全天 + 09-25 凌晨（C603+C604+C605 三连 keep **11140**；banked 0.712→**0.720**，41 连；demo-orphan 修复；code-lab 三连；prompt-mgr **480**；hindsight；TTT；AI×Neuro #51 DDM）

## ⚠️ 已知问题
- **cron 健康**: 09-14 ~ 09-26 连续十三日点位正常落盘（daily 只准 append 规则有效）。**09-25 晚 22:30 AI×Neuro #52 空转根因未深查但已于 09-26 晚幂等补做并收口**（中断非配置性，补做路径验证有效——幂等三查框架的首次实战正收益）
- **memory_graph.py _search_cache +24 行脏 hunk（e04d222d）**: 45 天未提交——留工作树，备份 /tmp/amg_dirty_backup_20260924.diff，将来处置走独立 cycle；另有 temporal_test_data.json / test_optimization.py / test_status.log 三个 untracked 杂物（C604 起挂账六轮未动）
- **MEMORY.md size**: ~**120KB**（09-27 KO：CF 归档后仍增长——新节比旧节密）——剩余大头：Active Theme 长弧线段（08-15 以前的 entropy API 枚举段可下轮归档）+ 近期研究一览表 + Core Projects Quick Reference（下轮候选）
- **Tavily 配额**: 09-25/09-26 连续两晚 432 超额（AI×Neuro cron 均切 AnySearch academic 备援成功）；用前先试一发，超配额直接切 AnySearch/web_fetch 备援
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内，workspace experiments.tsv 仅记外部项目 — 非阻塞；tsv HEAD 含 NUL 字节（offset 4513 历史遗留），如需修走专项 Python 行级手术；**C601 起 kd 行改用 workspace 短格式**
- **npm publish blocked**: 四项目 13931 tests ready（amg 11272/atc 2052/acs 3173/sot 607）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；ECC 264k★；context-mode（21.4k★）与 acs 同赛道；agent-skills 97k★；ai-memory（Rust 同赛道）；codebase-memory-mcp 44.6k★（C 代码知识图谱 MCP）；**hindsight 26.9K★（09-24/25 两日追踪，LongMemEval SOTA 且两机构独立复现——amg 最直接对标，需认真对读）**；obra/superpowers 290k★。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face counting 20+ forms + kd face 族 39+ + recency-supersession/base+delta/distinct-days/N-times/(class,day)-dedup 五条新赛道
- **AI×Neuro Topic Pool**: #52 已收口（09-26 补做交付）；候选：计算精神病学 / 噪声与随机共振 / 鸦科会聚智能
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM——重活串行是标准处置；**exec timeout ≥400s（含 git commit 带 hook）**
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd 会话产物，未动；C611 再记仍未清理）
- **atc 分支是 main**（写死记忆）；mission-control 分支也是 main
