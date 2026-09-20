# HEARTBEAT.md - September 21, 2026 (Monday) — 02:00 KO update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **10904 tests**（09-21 凌晨 C593 ccd0ecb；链 10865(C591)→10884/10889(C592 runner/junitxml)→**10904(C593)**；**banked 344/500=0.688，C565 起 29 连 keep（0.600→0.688）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 14 forms + pp_duration routes a-t）+ judge 链 + provenance 指纹 + speaker_recall face 族（speech-act…trip_with/acquire/antique_inherit）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **④ npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph` / `agent-memory-graph-py`，均实测 FREE）— 技术前置 100% 完成 (#066)，与 PyPI 同为 human-blocked
- [ ] **agent-context-store: README + npm publish** — **3173 tests**（09-17 三连击 3135→3173；coverage missing 677→630）
- [ ] **structured-output-toolkit: README + npm publish** — **607 tests**（09-17 includeDescriptions zod 修复）
- [ ] **agent-task-cli: README + npm publish** — **1897 tests**，Round 77（F285/F286 hsetnx+hincrbyfloat；Redis hash 家族 13 法，剩 hstrlen/hrandfield/hscan=R78 候选）

### 中优先级（本月）
- [ ] amg MCP server (stateless, 2026-07-28 compatible) — Research #043 ✅, Python MCP 16 tools
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] openclaw-langgraph-bridge: 307 tests（09-17 spawn() 无客户端超时→clientTimeoutMs）
- [ ] **评估 pacifio/atlas checkpoint 思想**（agent 版本控制：commit↔session 溯源 + 跨 agent 共享记忆——直击我们 jsonl 救援/拓扑混乱痛点；Linux 需自行 build Tauri；09-16 essay 已用其 trailer 模式 dogfooding）
- [ ] **评估 prompt 编译器落地**（09-19 深研 next actions：amg source-locator 试 DSPy Signature 平行实现 + GEPA auto='light'；500 题银行切 150 dev/350 holdout）+ **OCR（open-code-review）三痛点框架对照 amg harness** + context-mode Rejected Approaches 记忆维度借鉴

## 系统状态
- **agent-memory-graph (Python)**: **10904 tests** @C593（09-21 凌晨 kd-3 ccd0ecb antique_inherit face；**banked 344/500=0.688，C565 起 29 连 keep；abs_banked=18 冻结稳定；权威链 /tmp/c593/live500_c593.json**；C592 committed junitxml=10889 与 runner 10884 两口径均绿——**badge 血统=junitxml tests=，跨 run 比对先验口径**）。近期面族：antique_inherit（C593 无时间窗 family 来源约束+所有格面）+ acquire（C592 采集动词同句纪律+类别词不计数+head noun 键控）+ trip_with（C589）+ trip_recent（C588）+ knowledge-update（C587）+ eggs-quantity（C586）+ year-begin（C585）。核心纪律：harness verbatim 拷贝、tsv 裸字节 append（尾换行探测）、census-first、lane 分类前先跑 strict-form census、**并发第 4 查=两次 git log 对比**、**幂等第 5 查=工件/转录 mtime<15min 假定作者存活（kd-2 竞态近失误后新增，error-patterns 已记）**、python3 -m 调用必须 runner 脚本化（TOOLS.md）、OOM 重活串行。**⚠️ #068：无 TS 实现（旧 "TS 7349" 幻影已删）**
- **agent-context-store**: **3173 tests**（09-17 三连击；coverage missing 677→630）
- **agent-task-cli**: **1897 tests** — R77（hsetnx/hincrbyfloat，hash 13 法）。坑：**exec timeout 必须 ≥400s**（120s<jest 150s 被 SIGKILL，重跑先 git log）
- **context-forge**: **1563 tests**（09-20 晚 f37 CLI e2e ×8；Node runner IPC flake=上游 bug 不追）
- **prompt-mgr**: **475 tests**（09-20 晚 F27：restore 外来快照静默清空 store 修复+.corrupt bak 隔离）
- **lab/a2a-trust**: **102**（09-20 晚 94→102 barrel api-surface；账面曾误记 81，已修正）／ **pocket-agent**: **72**（09-20 晨 cov 98%）／ **code-lab/jp**: **49**（09-19 晨）／ **mission-control**: **33** cov 99% ／ **lab/mcp-client-explorer**: **60** ／ **openclaw-mcp-server**: **29** ／ **agent-observability**: **262** ／ **cot**: **123** ／ **a2a_minimal**: **48** ／ **wget-rust-prototype**: **25** ／ **nano-agent**: **1156** ／ **edge-agent-runtime**: **345** ／ **agent-log**: **75** ／ **session-archiver**: **85** ／ **agent-memory-service**: **738**（⚠️ .git 疑似损坏，动前实测）／ **langgraph-bridge**: **307** ／ **ai-dev-tools**: **79** / **amk**: **29** / **cqc**: **59** / **mcpt**: **37** / **act**: **39**；prompt-router / agent-mesh-network 已离库（09-19 KO 实测剔除）
- **四项目总计**: **13408**（amg 10904 + sot 607 + atc 1897）
- **全项目总计**: ~23784 tests（09-21 KO 口径：+114，含 a2a-trust 账面修正 +21）
- **零回滚率**: amg **336天** 🏆（KO 链 08-22:299 → 09-19:333 → 09-20:334 → 09-21:336；C565-C593 29 连 keep）/ acs **206天** 🏆（口径=有产出天数）

## 近期活动 (09-20 白天 ~ 09-21 凌晨 crons)
- **01:00 kd-3 C593 (keep ccd0ecb+1e4d6b3, suite 10904)**: antique_inherit face——banked **343→344 (0.688)，29 连**。无时间窗，family 来源约束替代；S1 信号形容词+同句家庭标记 / S2 所有格面；诱饵全结构性出局；纯词形 'five'。replay 一次过（连续第 3 次）。**权威链 /tmp/c593/live500_c593.json**
- **00:00 kd-2 监督轮**: C591 链 159 fails 普查（冻结 abstention）+ kd-1 crash-scare 孤儿工作独立验证 + **竞态近失误**（sessions_list 看不见长轮询 exec 会话→险双写 tsv；三重挡板零损失）→ **幂等第四查新规则入 error-patterns**
- **23:00 kd-1 C592 (keep 6f6c781+f856f94)**: acquire face——banked **341→343 (0.686)，28 连**。同句三要件+类别词不计数+head noun 键控；**python3 -m pytest 静默吞跑首例**（exit 0 空 log；runner 脚本纪律入 TOOLS.md）
- **22:30 AI×Neuro #47**: 嗅觉算法（果蝇蘑菇体扩张编码≈LSH / 扩张-稀疏化基序跨物种 / Osmo POM / AI 电子鼻筛查；飞书 Q6wXdGmduoIUAlx59D4cHUfRnLd；备份 memory/reports/2026-09-20-olfaction.md；**46 题备选库用完→自创题追加「化学感觉」节**）
- **22:00 工具线**: atc 1879→**1897**（R77 F285 hsetnx+F286 hincrbyfloat strtod 正则+IEEE754 parity；hash 13 法）
- **21:00 code-lab 三连 keep**: a2a-trust 94→**102**（barrel api-surface+schema-sync tripwire）/ prompt-mgr 464→**475**（restore 静默清空 store=silent-destruction；.corrupt bak）/ context-forge 1555→**1563**（CLI e2e；--only 崩溃+--json banner 走 stderr）
- **20:00 晚间深研**: Agentic Search/DeepResearcher（8 篇一手：Search-R1/DeepResearcher/WebThinker/BrowseComp/ZeroSearch/Tongyi DR 3.3B/SearchGym；**中心问题是环境不是模型**；博客 3ca2fa7；arXiv ID 必须检索核实）
- **19:00 trending**: OpenResearch/orca/Agent-Reach/context-mode；git worktree=agent 隔离原语成三工具共识
- **08:00 trending**: addyosmani/agent-skills（doubt-driven 五步怀疑循环）+ trycua/cua（飞书 MBvBd8Vp）
- **05:00 essay**: 《渲染形式×判分契约》f6a4c94（C588-591 弧线）
- **04:00 doc**: C589-591 追平 76d3387（badge 10870；TUTORIAL §5.40-42；十七条原则）
- **03:00 project-testing**: pocket-agent 65→**72** cov 78%→98%（import_state 非 callable 死工具 RED 修复）

## 本周关键路径
1. ✅ ~~C589→C593 kd 链（0.674→0.688，29 连 keep）~~ → 持续中
2. ⬜ kd 队列 next：furniture 多动词家族（gpt4_15e38248 buy|assemble|sell|fix）／ ~~list renderer（a40e080f/ceb54acb/8cf51dda）~~ 已 banked 勿重做（C577 注记过时）／ ollama oracle（human-blocked，解锁 ~169 NJ cascade；`ollama pull qwen2.5:7b` 即解锁；~101 题 pref 29+entropy 6+answer-NJ 66 锁死其中）
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ **评估 atlas checkpoint + OCR 混合架构对照 + prompt 编译器落地**（DSPy Signature/GEPA light/银行 150 dev 切分）
5. ⬜ 博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer；AI×Neuro 自创题 #48（候选：多巴胺校准时钟速度/对数多尺度 PE）；context-rot 笔记 next actions（配对测试/rerank 小 k）
6. ⬜ 博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误
7. ⬜ atc R78 候选：hstrlen/hrandfield/hscan（hash 家族收官）

## 上次检查
- **Knowledge org: 2026-09-21 02:00** — Integrated 09-20 全天 + 09-21 凌晨（amg kd 链 C592+C593 keep **10904** @ccd0ecb；banked 0.682→**0.688**，29 连，零回滚 336 天；kd-2 竞态近失误→**幂等第四查新规则**；工具线 +114：pocket 72/atc 1897/a2a-trust 102（账面修正 +21）/prompt-mgr 475/context-forge 1563；内容三发：essay f6a4c94+深研 agentic-search 博客 3ca2fa7+AI×Neuro #47 嗅觉）。MEMORY：Current Focus 09-21 新节 + **09-18~09-20 旧节归档（130237→125975B）** + Quick Reference 11 行计数修正 + 四项目 13408；HEARTBEAT 全刷（~23784）
- **Knowledge org: 2026-09-20 02:00** — Integrated 09-19 全天（C589 amg keep **10828**；banked 0.672→**0.674**，25 连 + jp 49/49 + prompt-mgr F26 464 + doc df53030 + essay c6bdc5d + 深研 prompt-compilers + AI×Neuro #46）。MEMORY：09-14~09-18 旧节归档 -13KB + 台账清理（离库剔除 -548）
- **Knowledge org: 2026-09-19 02:00** — Integrated C586→C588 三连 keep（amg **10813**；banked 0.664→**0.672**，24 连）+ 工具线 + 09-18 内容线。MEMORY：08-12~08-27 旧节归档 -79KB

## ⚠️ 已知问题
- **cron 健康**: 09-14 ~ 09-20 连续七日全点位正常落盘。历史缺口（09-12 doc+dashboard、09-13 trending 双 error）未归因——连续正常中，若再现再专项查 gateway 日志。**共享日文件只准 append 不重写**（09-14 覆写事故，TOOLS.md 已有规则）
- **MEMORY.md size**: **126KB**（09-21 09-18~09-20 旧节归档 -4.3KB）——剩余大头：Active Theme 长弧线段 + Timeline 区（Immediate→Short-term 候选项多为 C486 时代陈迹）+ 近期研究一览表（下轮归档候选）
- **Tavily 配额**: 432 错误（09-19 起耗尽），AnySearch + web_fetch/arXiv API 降级路径稳定；新周期开始可能已重置——用前先试一发，超配额时改多轮 search+extract
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内，workspace experiments.tsv 仅记外部项目 — 非阻塞；tsv HEAD 含 NUL 字节（offset 4513 历史遗留），如需修走专项 Python 行级手术
- **npm publish blocked**: 四项目 13408 tests ready（amg 10904/atc 1897/acs 3173/sot 607）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；context-mode（21.4k★）与 acs 同赛道；alibaba/open-code-review（26.9k★）混合架构；agent-skills 97k★（skill 生命周期工程化）。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face counting forms + kd face 族 21+
- **AI×Neuro Topic Pool**: 46 题备选库已全部用完；自创题双线：「时间与节律」系列 + 十四节「化学感觉」（#47 嗅觉已发，#48 候选：多巴胺校准时钟速度/对数多尺度 PE）
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM——重活串行是标准处置；**exec timeout ≥400s**
- **/tmp 产物寿命**: **/tmp/c593/live500_c593.json 是 authoritative 基线（C593 全量 live，344/500=0.688）**——使用前先验存在，被清以 HEAD 重跑重建（~1150s）；c592/c591 已被取代
- **memory_graph.py 脏 hunk**: e04d222d `_search_cache` +24 行仍未提交，day 42（C570-C593 逐文件 add 未混入）
- **amfs .git 疑似损坏**: agent-memory-service git -C 落到 monorepo——下次动 amfs 前先实测 `ls projects/agent-memory-service/.git`
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd 会话产物，未动）
