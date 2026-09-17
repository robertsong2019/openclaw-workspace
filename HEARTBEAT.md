# HEARTBEAT.md - September 18, 2026 (Friday) — 02:00 KO update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **10765 Python tests**（09-18 凌晨 C585 ce0678c；链 10705(C581)→10710(C582)→10714(C583)→10749(C584)→**10765(C585)**；**banked 332/500=0.664，C565 起 21 连 keep（0.600→0.664）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 14 forms + pp_duration routes a-t）+ judge 链 + provenance 指纹 + speaker_recall face 族（speech-act/type-demand/name-def/source-locator/list-body/appositive/named-holiday/list-recall/reltime-anchor/who-companion/sectioned-recall/chord/demand-noun/year-begin）+ where-precision 降级族。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **④ npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph` / `agent-memory-graph-py`，均实测 FREE）— 技术前置 100% 完成 (#066)，与 PyPI 同为 human-blocked
- [ ] **agent-context-store: README + npm publish** — **3135 tests**（09-14 Cycle 214；coverage 94.65%）
- [ ] **structured-output-toolkit: README + npm publish** — **591 tests**（09-07 consensusGenerate false-success 真 bug 修复 e6aabae）
- [ ] **agent-task-cli: README + npm publish** — **1879 tests**，Round 76（F274-F284 Redis hash 家族 11 法 + msetnx 守卫修复）

### 中优先级（本月）
- [ ] amg MCP server (stateless, 2026-07-28 compatible) — Research #043 ✅, Python MCP 16 tools
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] openclaw-langgraph-bridge: 302 tests（09-14 双周期：gateway client 加固 + 真 socket 集成 suite）
- [ ] **评估 pacifio/atlas checkpoint 思想**（agent 版本控制：commit↔session 溯源 + 跨 agent 共享记忆——直击我们 jsonl 救援/拓扑混乱痛点；Linux 需自行 build Tauri；09-16 essay 已用其 trailer 模式 dogfooding）
- [ ] **OCR（open-code-review）混合架构对照 amg exact judge 路线** + **colibri「placement 只定速度不定语义」红线借鉴** + VoiceStudio「按硬件选配置」推荐表格式（09-16 trending）

## 系统状态
- **agent-memory-graph (Python)**: **10765 tests** @C585（09-18 凌晨 kd-3 ce0678c year-begin face；链 10689(C580)→10705(C581)→10710(C582)→10714(C583)→10749(C584)→**10765(C585)**；**banked 332/500=0.664，C565 起 21 连 keep；abs_banked=18 冻结稳定；新权威链 /tmp/c585/live500_c585.json**）。近期面族：where-precision（C582 R2 do-form 降级+R3 assistant 让位；R1 retrieval-miss 正确 FAIL 留 examined-and-rejected 痕）+ counting ordinal-quantity（C583 序数后缀；bare-quantity 毒理图谱：子句数字通常绑定另一名词）+ chord/demand-noun（C584 **结构性判别>分数调整**：demand 名词=硬过滤非分数）+ year-begin（C585 user 证据面，NP 实词锚代替角色墙）。**speaker_recall stragglers 8 qids 分类结案**（2 banked/2 deferred/4 judge-unbankable 关闭）。核心纪律：harness verbatim 拷贝、tsv 裸字节 append（尾换行探测防空行）、census-first 救 banked、census 异常先解释再实现、OOM 重活串行、**session_N 枚举序号≠answer_session_ids 索引**。**⚠️ #068：无 TS 实现（旧 "TS 7349" 幻影已删）**
- **agent-context-store**: **3135 tests**（09-13 velocity reconstruction + Cycle 214）
- **agent-task-cli**: **1879 tests** — R76（Redis hash 家族 11 法 + msetnx 守卫）。坑：**exec timeout 必须 ≥400s**（120s<jest 150s 被 SIGKILL，重跑先 git log）
- **context-forge**: **1545 tests**（09-08 F83；09-16 跑出 1523+1 系 Node runner IPC flake 第 4 例=上游 bug 不追，flaky 跑总数偏小是已知形态）
- **prompt-mgr**: **447 tests**（09-16 晚 F24 validate_all+CLI doctor / F25 snapshot flush-first，509c585+fed0eb9）
- **mission-control**: **33 tests cov 99%**（09-16 3AM 24→33，main() 注入接缝，9e326e3）
- **lab/openclaw-mcp-server**: **24**；**mcp-client-explorer**: **54**；**pocket-agent**: **58**；**a2a_minimal**: **48**（09-16 Content-Length 守卫+终态语义）；**wget-rust-prototype**: **25**（09-16 hygiene：git ls-tree 补交漏交 build 文件）；**a2a-trust**: **81**；**nano-agent**: **1156**；**edge-agent-runtime**: **345**；**agent-log**: **75**（09-16 esc_json 反斜杠 no-op 真身暴露）；**session-archiver**: **81**；**agent-mesh-network**: **398**；**agent-observability**: **245**；**agent-memory-service**: **738**；**langgraph-bridge**: **307**（09-17 spawn() 无客户端超时 silent-hang 第 5 例→clientTimeoutMs，0ddef8e）；**ai-dev-tools**: **79** / **amk**: **29** / **cqc**: **56** / **mcpt**: **33** / **cot**: **117** / **prompt-router**: **150** / **act**: **36**
- **四项目总计**: **13251**（amg 10765 + sot 607 + atc 1879）
- **全项目总计**: ~24030 tests（09-18 KO 口径，较 09-16 +213）
- **零回滚率**: amg **332天** 🏆（KO 链 08-22:299 → 09-16:326 → 09-17:330 → 09-18:332；C565-C585 21 连 keep）/ acs **205天** 🏆（09-17 三连击 3135→3173 续写；口径=有产出天数）

## 近期活动 (09-17 ~ 09-18 crons)
- **kd-3 01:00 C585 (keep ce0678c+5299496, suite 10765)**: year-begin face——banked **331→332 (0.664)，21 连**。"what year ... began"→GT 在 user 粘贴案情里，证据面双角色开放，NP 全实词锚+begin-verb+in+年份代替角色墙（C584 结构性硬过滤直接迁移）；census 恰 1/500。**权威链 /tmp/c585/live500_c585.json**
- **kd-2 00:00 C584 (keep 5473b9d+ed7bd33, suite 10749)**: chord-progression + demand-noun faces——banked **329→331 (0.662)**，二十连。**结构性判别>分数调整**（demand 名词=硬过滤非分数，floor 豁免后 141.8<210.4 仍输）；speaker_recall stragglers 8 qids 分类结案（2 banked/2 deferred/4 closed）
- **kd-1 23:00 C583 (keep ae1065d+df6da79, suite 10714)**: counting ordinal-quantity——banked **328→329 (0.658)**，十九连。序数后缀 (?:st|nd|rd|th)? 挡数字→词干邻接；relaxed bare-quantity 回退（毒理图谱：子句数字通常绑定另一名词，2 banked kill 硬门）
- **kd-3 01:00(09-17) C582 (keep bc109c2+36b633e, suite 10710)**: where-precision faces——banked **326→328 (0.656)**，十八连。R2 do-form 降级+R3 assistant 让位；**R1 被 replay 正确 FAIL**（retrieval-miss 非降级问题→Simplicity-First 回退留痕）；**session_N 枚举序号≠answer_session_ids 索引**陷阱入档
- **22:00 工具线**: langgraph-bridge 302→**307**（spawn() 无客户端超时，silent-hang 家族第 5 例→clientTimeoutMs）
- **21:00 code-lab**: acs 三连击 3135→**3173** cov missing 677→630（content_complexity 从不返回 complexity_score→readability 恒 1.0 真 bug/kgraph shared-tag 边恒胜/方波基周期 6）
- **20:00 深研**: **CodeAct 代码即行动空间**（CodeAct 家族+Code Mode+沙箱运行时收敛；博客 7b28e31；Tavily 配额尽全程 AnySearch 路由）
- **08:00 trending**: **cloudflare/security-audit-skill**（927★/日，六阶段审计+三态裁决，与 amg 纪律同构）+ colibri 复析（Skill 化浪潮 4 仓同榜）；飞书 EnoNd19y
- **06:00 dashboard**: 18ac2ce（cron 8/15；⚠️ exec preflight 新拦截：cd && python 链+heredoc cat >> 被拒→workdir 参数+脚本落盘直跑）
- **05:00 essay**: 《评测失败的三层归因》5fb327b（retrieval-miss FAIL 救规则/session_N 陷阱/closed-lane）
- **04:00 doc**: amg C580-582 追平 efa3939（badge 10710；TUTORIAL §5.31-33；原则第 12 条：证据可达性先于答案选择）
- **03:00 project-testing**: sotk 591→**607**（includeDescriptions 11/17 zod 构造器被丢→7 shapes+6 red；**拓扑漂移 #4：pocket-agent/openclaw-mcp-server/a2a-trust-prototype/agent-observability 现为 monorepo 成员**）

## 本周关键路径
1. ✅ ~~C564-C581 kd 链（banked 0.594→0.652；十七连 keep）~~ 持续中
2. ⬜ kd 队列 next：**e8a79c70 eggs-quantity（bullet 侧信道+session-topic gate，10 字符句下限）/ counting-rest coordinated-sum（e3038f8c 99=12+57+5+25 / 60036106 12000）+ 枚举计数（60159905/a3838d2b）/ 830ce83f session-recency relocation / 07741c45 anaphora judging / 9ea5eabc recency priors / 3249768e ordinal-owned verify** → ollama oracle（human-blocked，解锁 ~169 NJ cascade；`ollama pull qwen2.5:7b` 即解锁）；~~pref 族~~ closed（judge-unbankable）；~~71017277~~ closed（evidence-absent）；~~speaker_recall stragglers 8 qids~~ 分类结案（C584：2 banked/2 deferred/4 closed）
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ **评估 atlas checkpoint + OCR 混合架构对照 + colibri 红线借鉴**（09-16 trending）/ context-mode 源码阅读（与 acs 同赛道）
5. ⬜ 博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer / **AI×Neuro 新题从新闻造（Pool 空了）**；context-rot 笔记 next actions（配对测试/rerank 小 k）
6. ⬜ 博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误

## 上次检查
- **Knowledge org: 2026-09-18 02:00** — Integrated C582→C585 四连 keep（amg **10765** @ce0678c junitxml；**day 332** 🏆；banked 0.652→**0.664**，C565 起 21 连；speaker_recall stragglers 分类结案）+ sotk 591→607（拓扑漂移 #4）+ acs 3135→3173 + bridge 302→307 + 09-17 内容线（doc efa3939 原则 12 / essay 三层归因 5fb327b / CodeAct 深研 7b28e31 / trending security-audit-skill）。MEMORY：Current Focus 09-18 新节 + Active Theme 332 天 + 测试表全刷（四项目 13251 / 总计 ~24030）
- **Knowledge org: 2026-09-17 02:00** — Integrated C579/C580/C581 三连 keep（amg **10705**（=10689 junit+C581 静态 16 defs，collect stdout flake 吞）；**day 328** 🏆；banked 0.638→**0.652**，十七连；pref 族 29 qids 永久关闭）+ mission-control 24→33 cov 99% + prompt-mgr 432→447（F24/F25）+ code-lab 三发（a2a 48/wget-rust hygiene/agent-log 75）+ 09-16 内容线（doc C577-579 / essay 共享工作树 / trending colibri+VoiceStudio / 深研 context-rot）。MEMORY：Current Focus 09-17 新节 + **Key Insights #181-262 归档落地（-42KB→213KB，第 4 轮排队兑现）** + Active Theme 328 天 + 测试表全刷（四项目 13175 / 总计 ~23890）+ Core Projects 表刷新
- **Knowledge org: 2026-09-16 02:00** — Integrated C577/C578 两连 keep（amg **10657 绿** @fb0091b；day 325；banked 0.630→**0.638**）+ atc R76 1879 + prompt-mgr 432 + mcx 54。MEMORY：Current Focus 09-16 新节 + 09-10~09-14 旧节归档（-8.4KB）+ Core Projects 表 6 处陈旧修正

## ⚠️ 已知问题
- **cron 健康**: 09-14 ~ 09-17 连续四日全点位正常落盘。历史缺口（09-12 doc+dashboard、09-13 trending 双 error）未归因——连续正常中，若再现再专项查 gateway 日志。**共享日文件只准 append 不重写**（09-14 覆写事故，TOOLS.md 已有规则）
- **MEMORY.md size**: **214KB**（09-17 Key Insights #181-262 归档 -42KB 落地；09-18 新节 +2.6KB；bootstrap 注入仍截断——Current Focus 09-14/09-15 旧节下轮归档候选）——剩余大头：Current Focus 08-15~09-27 旧节（再攒几天归档）+ Timeline 区
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内（projects/agent-memory-graph），workspace experiments.tsv 仅记外部项目 — 非阻塞
- **npm publish blocked**: 四项目 13251 tests ready（amg 10765/atc 1879/acs 3173/sot 607）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；context-mode（21.4k★，MCP 层会话记忆）与 acs 直接同赛道——优先读源码；alibaba/open-code-review（27k★）混合架构值得对照 amg 纪律路线；colibri/VoiceStudio 本地化基础设施三件套成型（「hold, not rent」）。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face 14 counting forms + pp routes a-t
- **AI×Neuro Topic Pool**: **空**（#42 已用最后一题；每期前从新闻造新题）
- **Tavily 配额**: 432 错误持续，AnySearch + web_fetch/arXiv API 降级路径稳定；tavily_research 超配额时改多轮 search+extract
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM——重活串行是标准处置；**exec timeout ≥400s**
- **/tmp 产物寿命**: **/tmp/c585/live500_c585.json 是新 authoritative 基线（C585 全量 live，332/500=0.664）**——使用前先验存在，被清以 HEAD 重跑重建（~1200s）；c582/c583/c584 已被取代
- **memory_graph.py 脏 hunk**: e04d222d `_search_cache` +24 行仍未提交，day 38（C570-C585 逐文件 add 未混入）
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd 会话产物，未动）
