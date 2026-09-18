# HEARTBEAT.md - September 19, 2026 (Saturday) — 02:00 KO update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **10813 Python tests**（09-19 凌晨 C588 4295f26；链 10765(C585)→10777(C586)→10798(C587)→**10813(C588)**；**banked 336/500=0.672，C565 起 24 连 keep（0.600→0.672）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 14 forms + pp_duration routes a-t）+ judge 链 + provenance 指纹 + speaker_recall face 族（speech-act/type-demand/name-def/source-locator/list-body/appositive/named-holiday/list-recall/reltime-anchor/who-companion/sectioned-recall/chord/demand-noun/year-begin/eggs-quantity/knowledge-update/trip_recent）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **④ npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph` / `agent-memory-graph-py`，均实测 FREE）— 技术前置 100% 完成 (#066)，与 PyPI 同为 human-blocked
- [ ] **agent-context-store: README + npm publish** — **3173 tests**（09-17 三连击 3135→3173；coverage missing 677→630）
- [ ] **structured-output-toolkit: README + npm publish** — **607 tests**（09-17 includeDescriptions zod 修复）
- [ ] **agent-task-cli: README + npm publish** — **1879 tests**，Round 76（F274-F284 Redis hash 家族 11 法 + msetnx 守卫修复）

### 中优先级（本月）
- [ ] amg MCP server (stateless, 2026-07-28 compatible) — Research #043 ✅, Python MCP 16 tools
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] openclaw-langgraph-bridge: 307 tests（09-17 spawn() 无客户端超时→clientTimeoutMs）
- [ ] **评估 pacifio/atlas checkpoint 思想**（agent 版本控制：commit↔session 溯源 + 跨 agent 共享记忆——直击我们 jsonl 救援/拓扑混乱痛点；Linux 需自行 build Tauri；09-16 essay 已用其 trailer 模式 dogfooding）
- [ ] **OCR（open-code-review）混合架构对照 amg exact judge 路线** + **colibri「placement 只定速度不定语义」红线借鉴** + VoiceStudio「按硬件选配置」推荐表格式（09-16 trending）

## 系统状态
- **agent-memory-graph (Python)**: **10813 tests** @C588（09-19 凌晨 kd-3 4295f26 trip_recent face；**banked 336/500=0.672，C565 起 24 连 keep；abs_banked=18 冻结稳定；新权威链 /tmp/c588/live500_c588.json**）。近期面族：trip_recent（C588 过去时/recency 标记+专有名词守卫挡未来计划）+ knowledge-update ku_reloc/ku_storage（C587 latest-session-wins 状态召回；**form gate=banked protection**——孪生题 initially 结构性出局）+ eggs-quantity（C586 bullet 侧信道+session-topic gate）+ year-begin（C585）+ chord/demand-noun（C584）+ counting ordinal-quantity（C583）+ where-precision（C582）。核心纪律：harness verbatim 拷贝（程序化替换 count==1 assert + diff 审计）、tsv 裸字节 append（尾换行探测）、census-first、**lane 分类前先跑 strict-form census（"risky lane"可能只是没做 census 的 lane）**、**并发第 4 查=两次 git log 对比**（HEAD 移动=兄弟会话存活铁证）、OOM 重活串行、session_N 枚举序号≠answer_session_ids 索引。**⚠️ #068：无 TS 实现（旧 "TS 7349" 幻影已删）**
- **agent-context-store**: **3173 tests**（09-17 三连击；coverage missing 677→630）
- **agent-task-cli**: **1879 tests** — R76（Redis hash 家族 11 法 + msetnx 守卫）。坑：**exec timeout 必须 ≥400s**（120s<jest 150s 被 SIGKILL，重跑先 git log）
- **context-forge**: **1545 tests**（09-08 F83；Node runner IPC flake 第 4 例=上游 bug 不追，flaky 跑总数偏小是已知形态）
- **prompt-mgr**: **447 tests**（09-16 晚 F24/F25，509c585+fed0eb9）
- **mission-control**: **33 tests cov 99%**（09-16，9e326e3）
- **lab/mcp-client-explorer**: **60**（09-18 server-initiated request/ping/-32601/id=0 falsy）；**pocket-agent**: **65**（09-18 export/import_state+compile 先行）；**openclaw-mcp-server**: **29**（09-18 MAX_SESSIONS DoS 防护）；**agent-observability**: **262**（09-18 两轮：export 边界空 kvlist 静默丢数据+span 属性四坑）；**cot**: **123**（09-18 round-trip 压平=export 家族第 3 例）；**a2a_minimal**: **48**；**wget-rust-prototype**: **25**；**a2a-trust**: **81**；**nano-agent**: **1156**；**edge-agent-runtime**: **345**；**agent-log**: **75**；**session-archiver**: **81**；**agent-mesh-network**: **398**；**agent-memory-service**: **738**；**langgraph-bridge**: **307**（09-17 spawn() 超时，0ddef8e）；**ai-dev-tools**: **79** / **amk**: **29** / **cqc**: **56** / **mcpt**: **33** / **prompt-router**: **150** / **act**: **36**
- **四项目总计**: **13299**（amg 10813 + sot 607 + atc 1879）
- **全项目总计**: ~24119 tests（09-19 KO 口径，较 09-18 +89）
- **零回滚率**: amg **332天** 🏆（KO 链 08-22:299 → 09-17:330 → 09-18:332；C565-C588 24 连 keep）/ acs **205天** 🏆（口径=有产出天数）

## 近期活动 (09-18 ~ 09-19 凌晨 crons)
- **kd-3 01:00 C588 (keep 16623bf+4295f26, suite 10813)**: trip_recent face——banked **335→336 (0.672)，24 连**。most-recent-trip 目的地；专有名词守卫挡 Tokyo 未来计划；**并发处置范本**：kd-2 in-flight 期间静默期只读探查，tsv+memory+push 三件套齐后才动工作区；**"risky scoring lane"正名为零分结构 face**（census-first 教训）。**权威链 /tmp/c588/live500_c588.json**
- **kd-2 00:00 C587 (keep 4d5d47c+2b95f6b, suite 10798)**: knowledge-update 双 face（ku_reloc+ku_storage）——banked **333→335 (0.670)，23 连**。latest-session-wins 状态召回；**form gate=banked protection**（孪生题 07741c44 initially 结构性出局，replay 证实未被触碰）；C582 anaphora 判决降级（渲染侧先行词展开替代 judge 改动）
- **kd-1 23:00 C586 (keep f9d261a+efab82d, suite 10777)**: eggs-quantity face——banked **332→333 (0.666)，22 连**。bullet 侧信道（10 字符句下限丢句）+ session-topic gate；tail 换行探测实战
- **22:30 AI×Neuro #45**: 时间的大脑（time cells/SBF 节拍器/小脑 forward model；LLM time neurons 有表征无行为；飞书 L1wPdyFv；**Topic Pool 44 题用完→新系列「时间与节律」自创题**）
- **22:00 工具线**: cot 117→**123**（export/import round-trip 压平分支树=export 边界数据丢失家族当日第 3 例；strip-types 假绿）
- **21:00 code-lab 四连 keep**: mcx 54→**60**（server-initiated request/id=0 falsy）/ pocket 58→**65**（self_evolving_agent 持久化）/ obs 256→**262**（span 属性编码四坑）/ mc-server 24→**29**（MAX_SESSIONS DoS 防护）
- **20:00 晚间深研**: ⚠️ **选题撞车事故+恢复**（self-evolving-agents 文件名与 09-10 已发布博文撞车，write 覆盖+index 重复；staged diff 验尸拦截零线上损害；重构续篇 self-evolving-frontier d886a40；error-patterns 已记预防规则）
- **19:00 trending**: orca/ADE 产品化/Anthropic 职能插件/Octop 新面孔（memory/github-trending-analysis-2026-09-18-evening.md）
- **08:00 trending**: cloudflare/security-audit-skill（927★/日，finder≠verifier 与 amg A/B 纪律同构）+ colibri 复析（飞书 OAR9dkxc）
- **05:00 essay**: 《数字绑定的毒理学》08354d9（bare-quantity 放宽回退：9 diffs 2 banked kill）
- **04:00 doc**: amg C583-585 追平 5b5e13d（badge 10765；TUTORIAL §5.34-36；原则→十四条；导语行连续 3 轮漏更→与主标题同批检查）
- **3AM project-testing**: agent-observability 245→**256**（exportGenAiOtlp 空 kvlist 静默数据丢失——导出边界测试必须断言 wire 内容非「事件存在」）

## 本周关键路径
1. ✅ ~~C582-C585 kd 链~~ → ✅ ~~C586-C588 kd 链（0.664→0.672，24 连 keep）~~ 持续中
2. ⬜ kd 队列 next：**e01b8e2f week-long-family-trip lane**（C588 form 的 no-recency 孪生，pred=New York 寄生行，census 先行）/ counting-rest coordinated-sum（e3038f8c 99=12+57+5+25 / 60036106 12000）+ 枚举计数（60159905/a3838d2b）→ ollama oracle（human-blocked，解锁 ~169 NJ cascade；`ollama pull qwen2.5:7b` 即解锁）；~~830ce83f/07741c45~~ C587 关闭；~~9ea5eabc~~ C588 关闭；~~3249768e~~ ordinal gate 收编
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ **评估 atlas checkpoint + OCR 混合架构对照 + colibri 红线借鉴**（09-16 trending）/ context-mode 源码阅读（与 acs 同赛道）
5. ⬜ 博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer / **AI×Neuro 新系列「时间与节律」自创题**（#46 候选：多巴胺校准时钟速度/对数多尺度 PE）；context-rot 笔记 next actions（配对测试/rerank 小 k）
6. ⬜ 博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误

## 上次检查
- **Knowledge org: 2026-09-19 02:00** — Integrated C586→C588 三连 keep（amg **10813** @4295f26；banked 0.664→**0.672**，C565 起 24 连）+ 工具线（obs 245→262 两轮/mcx 60/pocket 65/mc-server 29/cot 123）+ 09-18 内容线（doc 5b5e13d 十四条原则 / essay 毒理学 08354d9 / 撞车事故+续篇 d886a40 / AI×Neuro #45）。MEMORY：Current Focus 09-19 新节 + **08-12~08-27 旧节归档 -79KB（219KB→140KB）** + Active Theme C586-588 弧线 + 测试表全刷（四项目 13299 / 总计 ~24119）
- **Knowledge org: 2026-09-18 02:00** — Integrated C582→C585 四连 keep（amg 10765；day 332；banked 0.652→0.664，21 连）+ sotk 591→607 + acs 3135→3173 + bridge 302→307 + 09-17 内容线。MEMORY：Current Focus 09-18 新节 + Active Theme 332 天 + 测试表全刷（四项目 13251 / 总计 ~24030）
- **Knowledge org: 2026-09-17 02:00** — Integrated C579-C581 三连 keep + Key Insights #181-262 归档（-42KB）+ 09-16 内容线

## ⚠️ 已知问题
- **cron 健康**: 09-14 ~ 09-18 连续五日全点位正常落盘。历史缺口（09-12 doc+dashboard、09-13 trending 双 error）未归因——连续正常中，若再现再专项查 gateway 日志。**共享日文件只准 append 不重写**（09-14 覆写事故，TOOLS.md 已有规则）
- **MEMORY.md size**: **140KB**（09-19 08-12~08-27 旧节归档 -79KB 落地；bootstrap 注入仍可能截断）——剩余大头：Current Focus 09-14~09-17 旧节（下轮归档候选）+ Timeline 区 + 近期研究一览表
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内（projects/agent-memory-graph），workspace experiments.tsv 仅记外部项目 — 非阻塞
- **npm publish blocked**: 四项目 13299 tests ready（amg 10813/atc 1879/acs 3173/sot 607）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；context-mode（21.4k★，MCP 层会话记忆）与 acs 直接同赛道——优先读源码；alibaba/open-code-review（27k★）混合架构值得对照 amg 纪律路线；colibri/VoiceStudio 本地化基础设施三件套成型（「hold, not rent」）。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face 14 counting forms + pp routes a-t + kd face 族 17+
- **AI×Neuro Topic Pool**: 44 题已用完；新系列「时间与节律」已开（#45 时间的大脑），下期继续自创题
- **Tavily 配额**: 432 错误持续，AnySearch + web_fetch/arXiv API 降级路径稳定；tavily_research 超配额时改多轮 search+extract
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM——重活串行是标准处置；**exec timeout ≥400s**
- **/tmp 产物寿命**: **/tmp/c588/live500_c588.json 是新 authoritative 基线（C588 全量 live，336/500=0.672）**——使用前先验存在，被清以 HEAD 重跑重建（~1150s）；c586/c587 已被取代
- **memory_graph.py 脏 hunk**: e04d222d `_search_cache` +24 行仍未提交，day 39（C570-C588 逐文件 add 未混入）
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd 会话产物，未动）
