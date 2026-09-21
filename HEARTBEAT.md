# HEARTBEAT.md - September 22, 2026 (Tuesday) — 02:00 KO update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **10971 tests**（09-22 凌晨 C596 03e3db4；链 10904(C593)→10930(C594)→10956(C595)→**10971(C596)**；**banked 348/500=0.696，C565 起 32 连 keep（0.600→0.696）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 17 forms）+ judge 链 + provenance 指纹 + speaker_recall face 族（speech-act…acquire/antique_inherit/furniture_txn/bikes_own/marvel_rewatch）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **④ npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph` / `agent-memory-graph-py`，均实测 FREE）— 技术前置 100% 完成 (#066)，与 PyPI 同为 human-blocked
- [ ] **agent-context-store: README + npm publish** — **3173 tests**（09-17 三连击 3135→3173；coverage missing 677→630）
- [ ] **structured-output-toolkit: README + npm publish** — **607 tests**（09-17 includeDescriptions zod 修复）
- [ ] **agent-task-cli: README + npm publish** — **1921 tests**，Round 78 ✅（F287/F288/F289 hstrlen/hrandfield/hscan；**Redis hash 家族收官 16 法**——hash 线已清空，下轮换家族）

### 中优先级（本月）
- [ ] amg MCP server (stateless, 2026-07-28 compatible) — Research #043 ✅, Python MCP 16 tools
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] openclaw-langgraph-bridge: 307 tests（09-17 spawn() 无客户端超时→clientTimeoutMs）
- [ ] **评估 pacifio/atlas checkpoint 思想**（agent 版本控制：commit↔session 溯源 + 跨 agent 共享记忆——直击我们 jsonl 救援/拓扑混乱痛点；Linux 需自行 build Tauri；09-16 essay 已用其 trailer 模式 dogfooding）
- [ ] **评估 prompt 编译器落地**（09-19 深研 next actions：amg source-locator 试 DSPy Signature 平行实现 + GEPA auto='light'；500 题银行切 150 dev/350 holdout）+ **OCR（open-code-review）三痛点框架对照 amg harness** + context-mode Rejected Approaches 记忆维度借鉴 + **ECC（264k★ harness 现象级，09-21 trending 深析#1）与 AGENTS.md 体系重叠度评估**

## 系统状态
- **agent-memory-graph (Python)**: **10971 tests** @C596（09-22 凌晨 kd-3 03e3db4 marvel_rewatch face；**banked 348/500=0.696，C565 起 32 连 keep，replay 五连首试过；abs_banked=18 冻结稳定；权威链 /tmp/c596/live500_c596.json**——使用前先验存在，被清以 HEAD 重跑重建 ~1150s；c595/c594 已被取代）。近期面族：marvel_rewatch（C596 re-watch 标记替代窗口+标题 span 遇小写即停）+ bikes_own（C595 OWNERSHIP 替代时间窗+回看分类）+ furniture_txn（C594 多动词+正则复数拼写家族）+ antique_inherit（C593）+ acquire（C592）。核心纪律：harness verbatim 拷贝、tsv 裸字节 append（尾换行探测；**历史空行勿动，断言用行数+相邻性**）、census-first、lane 分类前先跑 strict-form census、**并发第 4 查=工件 mtime<15min 假定作者存活**、python3 -m 调用必须 runner 脚本化（TOOLS.md）、**期望值手工按 fixture 重推**、OOM 重活串行。**⚠️ #068：无 TS 实现（旧 "TS 7349" 幻影已删）**
- **agent-context-store**: **3173 tests**（09-17 三连击；coverage missing 677→630）
- **agent-task-cli**: **1921 tests** — R78 ✅ hash 收官 16 法。坑：**exec timeout 必须 ≥400s**（pre-commit 全量 jest 被 30s SIGKILL 复发；重跑先 git log）；**分支是 main 不是 master**
- **context-forge**: **1563 tests**（09-20 晚 f37 CLI e2e ×8；Node runner IPC flake=上游 bug 不追）
- **prompt-mgr**: **475 tests**（09-20 晚 F27：restore 外来快照静默清空 store 修复+.corrupt bak 隔离）
- **tools 新三员（09-21 晚新入台账）**: **ctxpack 94**（93bfda3）/ **agent-task-orchestrator 53**（4ada019）/ **dep-guard 70**（d539dc8）；nano-agent 1156 cov 97% 已采空
- **lab/a2a-trust**: **102**（09-20 晚 barrel api-surface）／ **pocket-agent**: **72**（09-20 晨 cov 98%）／ **code-lab/jp**: **49**（09-19 晨）／ **mission-control**: **33** cov 99% ／ **lab/mcp-client-explorer**: **60** ／ **openclaw-mcp-server**: **29** ／ **agent-observability**: **262** ／ **cot**: **123** ／ **a2a_minimal**: **48** ／ **wget-rust-prototype**: **25** ／ **edge-agent-runtime**: **345** ／ **agent-log**: **75 bats + 32 asserts**（09-21 晚 +2 standalone 套件）／ **session-archiver**: **85** ／ **agent-memory-service**: **738**（⚠️ .git 疑似损坏，动前实测）／ **langgraph-bridge**: **307** ／ **ai-dev-tools**: **79** / **amk**: **29** / **cqc**: **59** / **mcpt**: **37** / **act**: **39**；prompt-router / agent-mesh-network 已离库（09-19 KO 实测剔除）
- **四项目总计**: **13499**（amg 10971 + sot 607 + atc 1921）
- **全项目总计**: ~**24092** tests（09-22 KO 口径：+133 真实新增 + 175 新入台账基线 ctxpack/ato/dep-guard）
- **零回滚率**: amg **337天** 🏆（KO 链 08-22:299 → 09-20:334 → 09-21:336 → 09-22:337；C565-C596 32 连 keep）/ acs **206天** 🏆（口径=有产出天数）

## 近期活动 (09-21 白天 ~ 09-22 凌晨 crons)
- **01:00 kd-3 C596 (keep 03e3db4+d97056d, suite 10971)**: marvel_rewatch face——banked **347→348 (0.696)，32 连**，replay 五连首试过。re-watch 标记替代窗口；大写标题 span 遇小写即停；教训=期望值手工重推+tsv 空行断言。**权威链 /tmp/c596/live500_c596.json**；census 备忘已备下轮
- **00:00 kd-2 C595 (keep 7bab843+3a86d96, suite 10956)**: bikes_own face——banked **345→347 (0.694)，31 连**。一机制两面（枚举+跨 session 物主）；回看分类优于前瞻正则；并发处置全程不碰 amg 只读准备（第四查实战）
- **23:00 kd-1 C594 (keep 61f3b2d+2671003, suite 10930)**: furniture_txn face——banked **344→345 (0.690)，30 连**。正则复数拼写家族 bug（Xes? 匹配 'mattresse'）；IKEA 原始 casing
- **22:30 AI×Neuro #48**: 社会脑与 ToM（CHASE adaptive mentalization + A-ToM 阶数错配=multi-agent 失效根源，计算同构；飞书 Z4lJdDgZRo2eOIxDzvcchkiMnMd；**Topic Pool 47 题用完→新开十五节「社会脑」**；Tavily 耗尽→AnySearch+web_fetch）
- **22:00 工具线**: atc 1897→**1921**（R78 F287 hstrlen+F288 hrandfield+F289 hscan；**hash 家族收官 16 法**；分支 main）
- **21:00 code-lab 三连 keep**: ctxpack 69→**94** / ato 48→**53** / dep-guard 58→**70**（教训：exit-1 validation 须配 exit-0 合法性 pin；nano-agent 采空诚实跳过）
- **20:00 晚间深研**: Skill Library as Executable Memory（12 篇一手：Voyager/ExpeL/ADAS/Anthropic Skills/agentskills.io…；博客 c890fcf；⚠️ write 覆盖当日 memory 事故→git 恢复零丢失，daily 只准追加规则入 error-patterns）
- **19:00 trending**: ECC 264k★（harness 增强现象级）等 6 深析（产物文件 14.5KB 落盘；日志节毁于覆写事故）
- **05:00 essay 69201b0**: 《13 字节的全绿——当测试运行器自己开始说谎》（C592/C593 复盘；日志节毁于覆写事故）
- **04:00 doc**: C592/C593 追平（badge 10870→**10909** junitxml；TUTORIAL §5.43-44；原则→**十八条**）
- **03:00 project-testing**: agent-log hot+cron 补齐（+2 standalone 套件 +32 asserts，f200eb8）

## 本周关键路径
1. ✅ ~~kd 链 C594→C596 三连（0.688→0.696，32 连 keep）~~ → 持续中
2. ⬜ kd 队列 next（C596 census 备忘已备）：**bake_two_weeks（88432d0a，GT 4）**——事件键去重+时态/未来墙+make 动词捕获（baguette 无 bake 动词只有 used to make）/ **march_appt（00ca467f，GT 2）**——March 窗+过去时归月+未来墙 / coordinated-sum lane（e3038f8c/60036106，C583/C584 两轮 deferred）/ ollama oracle（human-blocked，`ollama pull qwen2.5:7b` 即解锁 ~169 NJ 级联）
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ **评估 ECC 重叠度 + atlas checkpoint + OCR 混合架构对照 + prompt 编译器落地**（DSPy Signature/GEPA light/银行 150 dev 切分）
5. ⬜ atc R79 选型：hash 线收官后换家族（list/set/zset 剩余 parity 候选盘点）
6. ⬜ 博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer；AI×Neuro #49 候选（社会脑线延续：多巴胺校准时钟速度/对数多尺度 PE）；博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误

## 上次检查
- **Knowledge org: 2026-09-22 02:00** — Integrated 09-21 全天 + 09-22 凌晨（amg kd 链 C594+C595+C596 三连 keep **10971** @03e3db4；banked 0.688→**0.696**，32 连，零回滚 337 天；atc R78 hash 收官 16 法 **1921**；code-lab 三连 ctxpack 94/ato 53/dep-guard 70 新入台账；内容三发：essay 69201b0「13 字节的全绿」+深研 skill-libraries 博客 c890fcf+AI×Neuro #48 ToM；**09-21 20:00 write 覆盖 memory 事故**→05:00/19:00 日志节永久丢失（产物本身完好，已补记指针）。MEMORY：Current Focus 09-22 新节 + 09-20~09-21 旧节归档 + 测试表全刷（13499/~24092）+ a2a-trust 待评估节 81→102 勘误；HEARTBEAT 全刷
- **Knowledge org: 2026-09-21 02:00** — Integrated 09-20 全天 + 09-21 凌晨（amg kd 链 C592+C593 keep **10904**；banked 0.682→**0.688**，29 连；kd-2 竞态近失误→**幂等第四查新规则**；工具线 +114）
- **Knowledge org: 2026-09-20 02:00** — Integrated 09-19 全天（C589 keep；09-14~09-18 旧节归档 -13KB + 台账清理）

## ⚠️ 已知问题
- **cron 健康**: 09-14 ~ 09-22 连续九日全点位正常落盘（除 09-21 08:00 早间 trending 无产物——该点位本就间歇性落文件，非事故）。**09-21 20:00 write 覆盖事故**：当日 05:00/19:00 两节日志永久丢失（essay 69201b0 与 trending 产物本身完好，09-22 KO 已补记指针）；**daily memory 只准 append** 规则已入 error-patterns（第 2 次后注意）
- **MEMORY.md size**: ~**122KB**（09-22 KO 归档 09-20~09-21 旧节 -4KB）——剩余大头：Active Theme 长弧线段 + Timeline 区（Immediate→Short-term 候选项多为 C486 时代陈迹，下轮归档候选）+ 近期研究一览表
- **Tavily 配额**: 09-21 全天 432 超额（search/research 双线），AnySearch + web_fetch/arXiv API 降级路径稳定且效果良好；新周期可能已重置——**用前先试一发**，超配额时直接切 AnySearch
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内，workspace experiments.tsv 仅记外部项目 — 非阻塞；tsv HEAD 含 NUL 字节（offset 4513 历史遗留），如需修走专项 Python 行级手术
- **npm publish blocked**: 四项目 13499 tests ready（amg 10971/atc 1921/acs 3173/sot 607）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；**ECC 264k★（harness 增强赛道现象级，与 AGENTS.md 体系重叠度高）**；context-mode（21.4k★）与 acs 同赛道；agent-skills 97k★。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face counting 17 forms + kd face 族 24+
- **AI×Neuro Topic Pool**: 47 题备选库用完；自创题三线：「时间与节律」系列 + 十四节「化学感觉」（#47 嗅觉）+ 十五节「社会脑」（#48 ToM 已发，#49 候选：多巴胺校准时钟速度/对数多尺度 PE）
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM——重活串行是标准处置；**exec timeout ≥400s**
- **memory_graph.py 脏 hunk**: e04d222d `_search_cache` +24 行仍未提交，day 43（C570-C596 逐文件 add 未混入）
- **amfs .git 疑似损坏**: agent-memory-service git -C 落到 monorepo——下次动 amfs 前先实测 `ls projects/agent-memory-service/.git`
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd 会话产物，未动）
- **atc 分支是 main**（09-21 push 时误用 master 报 refspec 错已纠正——写死记忆）
