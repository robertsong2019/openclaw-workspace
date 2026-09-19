# HEARTBEAT.md - September 20, 2026 (Sunday) — 02:00 KO update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **10828 tests**（09-19 深夜 C589 4b632c9；链 10798(C587)→10813(C588)→**10828(C589)**；**banked 337/500=0.674，C565 起 25 连 keep（0.600→0.674）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 14 forms + pp_duration routes a-t）+ judge 链 + provenance 指纹 + speaker_recall face 族（speech-act/type-demand/name-def/source-locator/list-body/appositive/named-holiday/list-recall/reltime-anchor/who-companion/sectioned-recall/chord/demand-noun/year-begin/eggs-quantity/knowledge-update/trip_recent/trip_with）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **④ npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph` / `agent-memory-graph-py`，均实测 FREE）— 技术前置 100% 完成 (#066)，与 PyPI 同为 human-blocked
- [ ] **agent-context-store: README + npm publish** — **3173 tests**（09-17 三连击 3135→3173；coverage missing 677→630）
- [ ] **structured-output-toolkit: README + npm publish** — **607 tests**（09-17 includeDescriptions zod 修复）
- [ ] **agent-task-cli: README + npm publish** — **1879 tests**，Round 76（F274-F284 Redis hash 家族 11 法 + msetnx 守卫修复）

### 中优先级（本月）
- [ ] amg MCP server (stateless, 2026-07-28 compatible) — Research #043 ✅, Python MCP 16 tools
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] openclaw-langgraph-bridge: 307 tests（09-17 spawn() 无客户端超时→clientTimeoutMs）
- [ ] **评估 pacifio/atlas checkpoint 思想**（agent 版本控制：commit↔session 溯源 + 跨 agent 共享记忆——直击我们 jsonl 救援/拓扑混乱痛点；Linux 需自行 build Tauri；09-16 essay 已用其 trailer 模式 dogfooding）
- [ ] **评估 prompt 编译器落地**（09-19 深研 next actions：amg source-locator 试 DSPy Signature 平行实现 + GEPA auto='light'；500 题银行切 150 dev/350 holdout）+ **OCR（open-code-review）三痛点框架对照 amg harness** + context-mode Rejected Approaches 记忆维度借鉴

## 系统状态
- **agent-memory-graph (Python)**: **10828 tests** @C589（09-19 深夜 kd-1 4b632c9 trip_with face；**banked 337/500=0.674，C565 起 25 连 keep；abs_banked=18 冻结稳定；权威链 /tmp/c589/live500_c589.json**）。近期面族：trip_with（C589 无 recency 属性唯一性：伴随者+时长 C584 硬过滤 + going-back-to 须同句过去伴随从句，纯未来计划永不渲染）+ trip_recent（C588 过去时/recency 标记+专有名词守卫）+ knowledge-update ku_reloc/ku_storage（C587 latest-session-wins）+ eggs-quantity（C586 bullet 侧信道）+ year-begin（C585）+ chord/demand-noun（C584）+ counting ordinal-quantity（C583）+ where-precision（C582）。核心纪律：harness verbatim 拷贝（程序化替换 count==1 assert + diff 审计）、tsv 裸字节 append（尾换行探测）、census-first、**lane 分类前先跑 strict-form census（"risky lane"可能只是没做 census 的 lane）**、**并发第 4 查=两次 git log 对比**（HEAD 移动=兄弟会话存活铁证）、OOM 重活串行、session_N 枚举序号≠answer_session_ids 索引。**⚠️ #068：无 TS 实现（旧 "TS 7349" 幻影已删）**
- **agent-context-store**: **3173 tests**（09-17 三连击；coverage missing 677→630）
- **agent-task-cli**: **1879 tests** — R76（Redis hash 家族 11 法 + msetnx 守卫）。坑：**exec timeout 必须 ≥400s**（120s<jest 150s 被 SIGKILL，重跑先 git log）
- **context-forge**: **1545 tests**（09-08 F83；Node runner IPC flake 第 4 例=上游 bug 不追，flaky 跑总数偏小是已知形态）
- **prompt-mgr**: **464 tests**（09-19 晚 F26 快照恢复回路 list_snapshots+restore 自动 safety-snapshot 可逆，61f1dca）
- **mission-control**: **33 tests cov 99%**（09-16，9e326e3）
- **lab/mcp-client-explorer**: **60**（09-18）；**pocket-agent**: **65**（09-18）；**openclaw-mcp-server**: **29**（09-18）；**agent-observability**: **262**（09-18 两轮）；**cot**: **123**（09-18）；**code-lab/jp**: **49**（09-19 晨 18(4红)→49/49，own-git 25a476e）；**a2a_minimal**: **48**；**wget-rust-prototype**: **25**；**a2a-trust**: **81**；**nano-agent**: **1156**；**edge-agent-runtime**: **345**；**agent-log**: **75**；**session-archiver**: **85**（09-19 路径穿越守卫）；**agent-memory-service**: **738**（⚠️ .git 疑似损坏，动前实测）；**langgraph-bridge**: **307**；**ai-dev-tools**: **79** / **amk**: **29** / **cqc**: **59**（09-19 lines[]） / **mcpt**: **37**（09-19） / **act**: **39**（09-19 RFC 4180）；prompt-router / agent-mesh-network **已离库**（09-19 KO 实测 repo 无目录，计数剔除）
- **四项目总计**: **13314**（amg 10828 + sot 607 + atc 1879）
- **全项目总计**: ~23670 tests（09-20 KO 口径：剔除已离库 -548 + amg 15/prompt-mgr 17/code-lab 14/jp 49）
- **零回滚率**: amg **333天** 🏆（KO 链 08-22:299 → 09-17:330 → 09-18:332 → 09-19:333；C565-C589 25 连 keep）/ acs **205天** 🏆（口径=有产出天数）

## 近期活动 (09-19 白天 ~ 09-20 凌晨 crons)
- **23:00 kd-1 C589 (keep 4b632c9+feb4783, suite 10828)**: trip_with face——banked **336→337 (0.674)，25 连**。week-long family trip 无 recency 属性唯一性；going-back-to 须同句过去伴随从句；中 cycle 红=测试构造 bug（第二渲染面缺 own going-back-to，C588 教训第 2 次）。**权威链 /tmp/c589/live500_c589.json**
- **22:30 AI×Neuro #46**: 大脑元认知与 AI 校准（NRN 2026 双层架构 / Kalai base model 本来校准 / MIT RLCR Brier 奖励校准误差↓90%；飞书 Oy36dTOL；Topic Pool 45 题备选库耗尽→自创题追加）
- **22:00 工具线**: prompt-mgr 447→**464**（F26 快照恢复回路：restore 先自动 safety-snapshot=可逆 + corrupt 零触碰；latent bug cli.py 未 import json；61f1dca）
- **21:00 code-lab 四连 keep**: session-archiver 81→**85**（路径穿越 assertValidId+deleteArchive）/ cqc 56→**59**（security lines[] 1-based）/ mcpt 33→**37**（resources 重复 URI+prompt.arguments validate）/ act 36→**39**（RFC 4180 CSV+公式注入防护）
- **20:00 晚间深研**: Prompt 编译器（DSPy/GEPA/TextGrad/OPRO 12 源；GEPA ICLR 2026 Oral 超 GRPO 6pp rollout 少 35×；博客 9f21dc0；**Tavily 配额耗尽全程 AnySearch**；next：DSPy Signature 平行实现+GEPA light+银行切 150 dev/350 holdout）
- **19:00 trending**: alibaba/open-code-review 周增 14,144★ 确定性×Agent 混合架构（code review 三痛点框架可对照 amg harness）；四信号：确定性护栏/skill 分发单元/上下文经济学/端侧 agent
- **08:00 trending**: cloudflare/security-audit-skill（+3006★/日榜首，validators-as-gates）+ ECC harness 商品化（飞书 AVe0dt5dY）
- **05:00 essay**: 《导出边界三连解剖》c6bdc5d（09-18 一日三项目同族 bug；与 fence/HTTP 边界文互链）
- **04:00 doc**: C586-588 追平 df53030（badge 10813；TUTORIAL §5.37-39；原则→十六条：+15 渲染侧先行 +16 lane 风险=census 函数）
- **03:00 project-testing**: code-lab/jp 18(4红)→**49/49**（query() 吞 QueryError + CLI -r no-op 两 RED-VERIFIED 真 bug；own-git 25a476e）

## 本周关键路径
1. ✅ ~~C582-C585 kd 链~~ → ✅ ~~C586-C588~~ → ✅ ~~C589 (0.674，25 连 keep)~~ → 持续中
2. ⬜ kd 队列 next：counting-rest coordinated-sum（e3038f8c 99=12+57+5+25 / 60036106 12000）+ 枚举计数（60159905/a3838d2b）→ ollama oracle（human-blocked，解锁 ~169 NJ cascade；`ollama pull qwen2.5:7b` 即解锁）；~~e01b8e2f~~ C589 关闭
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ **评估 atlas checkpoint + OCR 混合架构对照 + prompt 编译器落地**（DSPy Signature/GEPA light/银行 150 dev 切分）
5. ⬜ 博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer / **AI×Neuro 自创题 #47**（候选：多巴胺校准时钟速度/对数多尺度 PE）；context-rot 笔记 next actions（配对测试/rerank 小 k）
6. ⬜ 博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误

## 上次检查
- **Knowledge org: 2026-09-20 02:00** — Integrated 09-19 全天（C589 amg keep **10828** @feb4783；banked 0.672→**0.674**，25 连，零回滚 333 天 + jp 49/49 + prompt-mgr F26 464 + doc df53030 十六条原则 + essay c6bdc5d + 深研 prompt-compilers 9f21dc0 + AI×Neuro #46）。MEMORY：Current Focus 09-20 新节 + **09-14~09-18 旧节归档 -13KB（140KB→128KB）** + 台账清理（prompt-router/agent-mesh 已离库剔除 -548 + jp 入账）；HEARTBEAT 全刷（全项目 ~23670）
- **Knowledge org: 2026-09-19 02:00** — Integrated C586→C588 三连 keep（amg **10813** @4295f26；banked 0.664→**0.672**，24 连）+ 工具线（obs 245→262 两轮/mcx 60/pocket 65/mc-server 29/cot 123）+ 09-18 内容线。MEMORY：Current Focus 09-19 新节 + **08-12~08-27 旧节归档 -79KB（219KB→140KB）**
- **Knowledge org: 2026-09-18 02:00** — Integrated C582→C585 四连 keep（amg 10765；day 332；banked 0.652→0.664，21 连）+ sotk 591→607 + acs 3135→3173 + bridge 302→307 + 09-17 内容线

## ⚠️ 已知问题
- **cron 健康**: 09-14 ~ 09-19 连续六日全点位正常落盘。历史缺口（09-12 doc+dashboard、09-13 trending 双 error）未归因——连续正常中，若再现再专项查 gateway 日志。**共享日文件只准 append 不重写**（09-14 覆写事故，TOOLS.md 已有规则）
- **MEMORY.md size**: **128KB**（09-20 09-14~09-18 旧节归档 -13KB）——剩余大头：Current Focus 09-18~19 旧节 + Timeline 区 + 近期研究一览表（下轮归档候选）
- **Tavily 配额**: 432 错误持续（09-19 晚耗尽），AnySearch + web_fetch/arXiv API 降级路径稳定；tavily_research 超配额时改多轮 search+extract
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内（projects/agent-memory-graph），workspace experiments.tsv 仅记外部项目 — 非阻塞；tsv HEAD 含 NUL 字节（offset 4513 历史遗留，git 判 binary），如需修走专项 Python 行级手术
- **npm publish blocked**: 四项目 13314 tests ready（amg 10828/atc 1879/acs 3173/sot 607）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；context-mode（21.4k★，MCP 层会话记忆）与 acs 直接同赛道；alibaba/open-code-review（26.9k★）混合架构对照 amg 纪律路线；colibri/VoiceStudio 本地化基础设施三件套。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face 14 counting forms + pp routes a-t + kd face 族 18+
- **AI×Neuro Topic Pool**: 45 题备选库已耗尽；「时间与节律」+自创题双线并行（#46 元认知已发，下期 #47 候选：多巴胺校准时钟速度/对数多尺度 PE）
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM——重活串行是标准处置；**exec timeout ≥400s**
- **/tmp 产物寿命**: **/tmp/c589/live500_c589.json 是 authoritative 基线（C589 全量 live，337/500=0.674）**——使用前先验存在，被清以 HEAD 重跑重建（~1150s）；c588 已被取代
- **memory_graph.py 脏 hunk**: e04d222d `_search_cache` +24 行仍未提交，day 40（C570-C589 逐文件 add 未混入）
- **amfs .git 疑似损坏**: agent-memory-service git -C 落到 monorepo——下次动 amfs 前先实测 `ls projects/agent-memory-service/.git`
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd 会话产物，未动）
