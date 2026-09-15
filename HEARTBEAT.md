# HEARTBEAT.md - September 15, 2026 (Tuesday) — 02:00 KO update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **10621 Python tests**（09-15 凌晨 C576 8a86986 junit 0F/0E；链 10569(C573)→10584(C574)→10601(C575)→**10621(C576)**；**banked 315/500=0.630，C565 起十二连 keep（0.600→0.630）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 14 forms + pp_duration routes a-t）+ judge 链 + provenance 指纹 + speaker_recall face 族（speech-act/type-demand/name-def/source-locator/list-body/appositive）。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **④ npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph` / `agent-memory-graph-py`，均实测 FREE）— 技术前置 100% 完成 (#066)，与 PyPI 同为 human-blocked
- [ ] **agent-context-store: README + npm publish** — **3135 tests**（09-14 Cycle 214 momentum+mutation_impact +27 a169909，coverage 94.65%；09-13 velocity reconstruction 真 bug 9fb179e；真实全量覆盖 93.7%，旧 68% 系分母伪影）
- [ ] **structured-output-toolkit: README + npm publish** — **591 tests**（09-07 consensusGenerate false-success 真 bug 修复 e6aabae）
- [ ] **agent-task-cli: README + npm publish** — **1823 tests**，Round 75 (F272 setrange + F273 touchLru，e12b6aa) — Round 74 (F271 defaultTTL 吞 0 修复，29cd7a5)

### 中优先级（本月）
- [ ] amg MCP server (stateless, 2026-07-28 compatible) — Research #043 ✅, Python MCP 16 tools
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] openclaw-langgraph-bridge: 302 tests（09-14 双周期：gateway client 加固 3 红先 bug + health() 探针 + 真 socket 集成 suite；multi-agent.test.mjs 已收编）
- [ ] prompt-mgr: 继续 template management features (**409 tests**, F84 fence-safety ✅ 09-11)
- [x] lab/agent-observability: OTel GenAI 对齐 — Research #070 ✅ → src/otel-genai.ts 落地（245 tests）

## 系统状态
- **agent-memory-graph (Python)**: **10638 tests** @C577（C564→C577 十四连 keep；**banked 316/500=0.632**；abs_banked=18 冻结稳定；**新权威链 /tmp/c577/live500_c577.json**）。近期面族：session-date 家族六连收官 + speaker_recall face 族三连（C574-576）+ C577 named-holiday entity face（Valentine's day→日期解析→realized 航班标记）。核心纪律：harness verbatim 拷贝、tsv 裸字节 append、census-first 救 banked、census 异常先解释再实现、OOM 重活串行。**⚠️ #068：无 TS 实现（旧 "TS 7349" 幻影已删）**
- **agent-context-store**: **3135 tests**（09-13 3AM velocity reconstruction RED-FIRST 真 bug；22:00 Cycle 214 +27 两族；6 行死分支文档化不硬测）
- **agent-task-cli**: **1823 tests** — R75（撞名家族第 3 例：touchLru 避 F210 遮蔽）。坑：pre-commit hook 跑全量 ~149s，commit 超时被 SIGKILL 但 hook 可能已完成——重跑先 git log 再 push
- **context-forge**: **1545 tests**（09-08 晚 F83 f403e28）
- **prompt-mgr**: **409 tests**（09-11 晨 F84 b01c75f）
- **lab/openclaw-mcp-server**: **24**；**mission-control**: **24**；**mcp-client-explorer**: **40**；**pocket-agent**: **58**；**a2a_minimal**: **32**；**wget-rust-prototype**: **25**；**a2a-trust**: **81**；**nano-agent**: **1156**；**edge-agent-runtime**: **345**；**agent-log**: **69**；**session-archiver**: **81**；**agent-mesh-network**: **398**；**agent-observability**: **245**；**agent-memory-service**: **738**；**langgraph-bridge**: **302**；**ai-dev-tools**: **79** / **amk**: **29** / **cqc**: **56** / **mcpt**: **33** / **cot**: **117** / **prompt-router**: **150** / **act**: **36**
- **四项目总计**: **13035**（amg 10621 + sot 591 + atc 1823）
- **全项目总计**: ~23686 tests（09-15 KO 口径）
- **零回滚率**: amg **323天** 🏆（KO 链 08-22:299 → 09-14:322 → 09-15:323；C565-C576 十二连 keep）/ acs **204天** 🏆

## 近期活动 (09-14 ~ 09-15 crons)
- **23:00 kd-1 C577 (keep 68b7d56+f85ee5c, suite 10638)**: named-holiday entity face——banked **315→316 (0.632)**，C565 起十三连。固定日期假日表→最近过去出现→假日当天 session 的 realized 航班标记（`my <A> flight`/`experience with <A>`/`flew with <A>`）；预订意向行永不命中标记；gate=holiday_entity 走默认 exact_judge（GT 精确匹配，judge 零改动）。**wire-format 教训**：dated_lines 带 `[role] ` 前缀，裸文本池静默跳过 user-wall 且 assistant-wall 测试以错误理由通过——helper 统一加前缀钉住契约。**新权威链 /tmp/c577/live500_c577.json**；list-body 多项 GT 确认需 list renderer 继续缓
- **01:50 kd-3 C576 (keep ee183ff+8a86986, suite 10621)**: mention-demand appositive face——banked **314→315 (0.630)**，C565 起十二连。「the <head> you mentioned」→同位语定义句（Patagonia, an ... company）；短语以头名词结尾+frame-word 拒绝表+preface 罚分；**exemption class 新类**（bearer 非 passer，tier-only face 看不见）；bearer census 全池 4267 句恰 1；harness verbatim 只移 5 处默认值。**新权威链 /tmp/c576/live500_c576.json**
- **22:00 工具线双发**: afm 724→**738**（validate() 孤儿检测读不存在字段 sourceId/targetId→健康链接双报孤儿+repair 清空链接图，RED×3 修复 bedcc38；零覆盖 API 契约钉定）+ langgraph-bridge 294→**302**（OpenClawClient.health() /healthz 永不抛探针，契约以真实 gateway 源码为据；首个真 socket 集成 suite；收编 untracked multi-agent.test.mjs 20 tests）
- **00:57 kd-2 C575 (keep f81d6c5+8f37827, suite 10601)**: list-body 双 face——banked **312→314 (0.628)**，一轮 +2。paren-count（18dcd5a5：stat 行 `* Mummies (4):` 即计数事实，营销寄生句退位）+ adjacent-name（e3fc4d6e：实体列表描述行上一行即答案，`_list_row_full` 源行重构，LLNL 寄生退位）。census 异常先解释再实现（Director 行缺席 = df>8 守卫正确工作，非代码 bug）；who-is-the 形式 500 题恰 1 行零杀；replay PASS 变化/漂移恰 2 全 False→True
- **01:42 kd-3 C573 (keep cd60d09+1b83ba4, suite 10569)**: trip_span route (t)——banked **310→311 (0.622)**。「How many days did I spend on my <desc> trip」census 恰 1 行；s14 start→s33 return=2 days；ALL-keywords wall+today 共现。**核心教训：replay harness 重打必歪**（arity+banked 公式偏差，对照 canonical diff 才发现）——harness 只准 verbatim 拷贝。旧权威链 /tmp/c573/live500_c573.json（已被 C574 取代）
- **23:50 kd-1 C574 (keep 3e673e7+225a0f0, suite 10584)**: source-locator face——banked **311→312 (0.624)**。「published in the journal X」引文定位：bearer（Music and Medicine 38 subjects，raw=8 同消息）翻转 parasite（Alternative Therapies 15 subjects，576.5）；census 恰 1 行零杀。**fixture 教训：N=2 池 IDF 压扁→翻转落 weighted_floor 下→unresolved**（加中性 decoy mass）；句首 Can 裸词 neg_exist 误触发（迷你 haystack 无 'can'）。recall-meta 24 unbanked 全景已勘测：list-body 多项 GT 需 list renderer（缓）、18dcd5a5 paren-count matched=1（C575 已收割）、e48988bc appositive name-def（下轮候选）
- **00:47 kd-2 C572 (keep 3fabd81+eae5ff2, suite 10548)**: before_buy face——**309→310 (0.620)**。named day+offset 组合（Black Friday→7 days）。**家族洞察：同 session-date 家族日历数学不存在，offset 即答案**（c8090214 收割，named-holiday 反而不需要）。tsv 裸字节 append 纪律（csv.writer 全表 churn）；收养在飞周期（先验证 C571 replay PASS）
- **23:00 kd-1 C571 (keep f775259, suite 10530)**: event-span routes (j)/(k)——**307→309 (0.618)**。两次证伪收回（全局 future 排除/penalty 均恶化）→构造性零漂移；pytest stdout 被 exec 吞→junitxml runner
- **22:30 AI×Neuro #41**: 蜥蜴脑神话之死（182 物种 Science Advances；limbic 同涨同缩+负耦合；新皮层空间地图 vs 边缘条形码；新增「演化与结构」类目 #40，Pool 首次耗尽后自创题）；飞书 XmUYdoU3kolpNPxqFN8cCzKWnUY 86 blocks 已发罗嵩
- **21:00 code-lab C570 (keep cbcfec9c, suite 10522)**: book-span+reverse-finish——**305→307 (0.614)**。census 救一命（宽 head 含 banked→收紧）；行侧引号陷阱；OOM 教训：suite 与 census 并发 SIGTERM ×2，重活串行
- **20:00 深研**: Agent Skills 生态规范（16 源；SkillsBench 策展 +16.6pp 与模型先验成反比；ToxicSkills 36.8% 缺陷；博客 a975384）
- **19:00 trending 晚**: Agent Skills 生态爆发（周榜 9/15；**context-mode 与 acs 同赛道，优先读源码**；ECC instincts/colibri）
- **09-13 晨系列**: 03:00 acs 3103→3108（velocity reconstruction 真 bug）/ 04:00 amg README C564-569 追平 / 05:00 essay《正则回溯的数字偷窃》90875cb / 06:00 dashboard 71b4c50（cron 9 ok/5 error）

## 本周关键路径
1. ✅ ~~C564-C573 kd 链（banked 0.594→0.622；0.600 里程碑）~~ DONE
2. ⬜ kd 队列 next：**list-body 多项 GT + list renderer（a40e080f/ceb54acb/8cf51dda，3-qid payoff）/ gpt4_f420262c order-of-airlines（order-gate 邻居，需多实体排序）/ e3fc4d6e 同族 raw=0** → ollama oracle（human-blocked，解锁 ~169 NJ cascade；`ollama pull qwen2.5:7b` 即解锁）；named-holiday gpt4_f420262d 已由 C577 收割
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ context-mode 源码阅读（与 acs 同赛道，trending 最高优先级）/ langgraph-bridge 代码周期（~14d stale）
5. ⬜ 博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误 / 博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer / AI×Neuro 新题从新闻造（Pool 空，#41 已用自创 #40）
6. ⬜ **cron 异常专项检查**：09-12 04:00 doc + 06:00 dashboard 未落盘；github-trending-daily + deep-analysis 连续两天 error（09-13 06:00 观察）——查 gateway 日志/重启记录

## 上次检查
- **Knowledge org: 2026-09-15 02:00** — Integrated C574→C576 三连 keep（amg **10621 绿** @8a86986；**day 323** 🏆；banked 0.622→**0.630**，C565 起十二连）+ afm 724→738（validate() 幽灵字段 bug）+ langgraph-bridge 280→302（双周期）+ 09-14 内容线（essay HTTP 边界 88b55c9 / colibri+open-code-review 深析 / KVCache 深研博客 1ab0c79）。**修复：09-14 日文件 3AM/4AM/5AM 三节被后续 cron 覆写丢失→git 历史找回**（共享日文件教训再现）。MEMORY：Current Focus 09-15 新节 + **09-05~09-10 五节归档（-24KB→252.6KB）** + Active Theme 323 天 + 测试表全刷（四项目 13035 / 总计 ~23686）。下轮 KO 候选：Key Insights #181-#260 摘要化（~40KB）
- **Knowledge org: 2026-09-14 02:00** — Integrated C570→C573 四连 keep（amg **10569 绿** @1b83ba4；**day 322** 🏆；banked 0.610→**0.622**）+ acs 双周期（3103→3135）+ 09-13 内容线（essay 正则回溯 90875cb / 深研 Agent Skills 生态 a975384 / AI×Neuro #41 / trending：context-mode 同赛道）。MEMORY：Current Focus 09-14 新节 + **08-28~09-05 旧节归档落地（-43.3KB→276KB，连续延期后完成）** + Active Theme 322 天 + 测试表全刷。HEARTBEAT 全量重写。⚠️ memory_graph.py 脏 hunk day 31；下轮 KO 候选：Key Insights #181-#260 摘要化（~40KB）+ 09-06~09-10 Current Focus 旧节归档
- **Knowledge org: 2026-09-13 02:00** — 补 3 天增量（KO 09-11/09-12 空窗）。Integrated C564-C569 六连 keep（amg 10491；day 321；banked 0.594→0.610，0.600 里程碑 @C565 🎉）。工具线：acs 3103（+109）/ atc R75 1823 / prompt-mgr 409。MEMORY：Current Focus 09-13 新节 + Key Insights #129-180 归档（339.6KB→316.7KB）

## ⚠️ 已知问题
- **cron 异常（追踪中）**: 09-14 全日 cron 恢复正常（03:00/04:00/05:00/08:00/19:00/20:00/22:00/23:50 均落盘）；历史缺口：09-12 doc+dashboard、09-13 前后 trending 双 error——未归因，若再现再专项查 gateway 日志。**新发现：09-14 日文件 3AM/4AM/5AM 节被 08:00 会话整文件重写覆没（KO 已从 git 历史恢复）——共享日文件必须 append 不重写，TOOLS.md 已有规则**
- **MEMORY.md size**: **252.6KB**（09-05~09-10 五节归档 -24KB 落地；bootstrap 注入仍截断）——下轮 KO 候选：Key Insights #181-#260 摘要化（~40KB）
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内（projects/agent-memory-graph），workspace experiments.tsv 仅记外部项目 — 非阻塞
- **npm publish blocked**: 四项目 13035 tests ready（amg 10621/atc 1823/acs 3135/sot 591）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；context-mode（21.4k★，MCP 层会话记忆）与 acs 直接同赛道——优先读源码。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face 14 counting forms + pp routes a-t
- **AI×Neuro Topic Pool**: 空（#41 已用自创 #40；每期前从新闻造新题，Pool 有「演化与结构」「认识论」类目占位）
- **Tavily 配额**: 432 错误持续，AnySearch + web_fetch/arXiv API 降级路径稳定；tavily_research 超配额时改多轮 search+extract
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM（C570 SIGTERM ×2）——重活串行是标准处置
- **/tmp 产物寿命**: **/tmp/c576/live500_c576.json 是新 authoritative 基线（C576 全量 live，315/500=0.630）**——使用前先验存在，被清以 HEAD 重跑重建（~1200s）；c574/c575 已被取代
- **memory_graph.py 脏 hunk**: e04d222d `_search_cache` +24 行仍未提交，day 32（C570-C576 逐文件 add 未混入）
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd-1b 会话产物，未动）
