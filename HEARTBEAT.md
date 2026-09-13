# HEARTBEAT.md - September 14, 2026 (Monday) — 02:00 update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **10569 Python tests**（09-14 凌晨 C573 1b83ba4 junit 0F/0E；链 10491(C569)→10522(C570)→10530(C571)→10548(C572)→10569(C573)；**banked 311/500=0.622，C565 起九连 keep（0.600→0.622）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 14 forms + pp_duration routes a-t）+ judge 链 + provenance 指纹。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **④ npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph` / `agent-memory-graph-py`，均实测 FREE）— 技术前置 100% 完成 (#066)，与 PyPI 同为 human-blocked
- [ ] **agent-context-store: README + npm publish** — **3135 tests**（09-14 Cycle 214 momentum+mutation_impact +27 a169909，coverage 94.65%；09-13 velocity reconstruction 真 bug 9fb179e；真实全量覆盖 93.7%，旧 68% 系分母伪影）
- [ ] **structured-output-toolkit: README + npm publish** — **591 tests**（09-07 consensusGenerate false-success 真 bug 修复 e6aabae）
- [ ] **agent-task-cli: README + npm publish** — **1823 tests**，Round 75 (F272 setrange + F273 touchLru，e12b6aa) — Round 74 (F271 defaultTTL 吞 0 修复，29cd7a5)

### 中优先级（本月）
- [ ] amg MCP server (stateless, 2026-07-28 compatible) — Research #043 ✅, Python MCP 16 tools
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] openclaw-langgraph-bridge: Gateway 集成测试 (280 tests，~14d stale，C214 后代码周期首选)
- [ ] prompt-mgr: 继续 template management features (**409 tests**, F84 fence-safety ✅ 09-11)
- [x] lab/agent-observability: OTel GenAI 对齐 — Research #070 ✅ → src/otel-genai.ts 落地（245 tests）

## 系统状态
- **agent-memory-graph (Python)**: **10569 tests** @C573（C564→C573 十连 keep；**banked 298→311 (0.596→0.622)，0.600 里程碑 C565 🎉 后又 +11**；abs_banked=18 冻结稳定；**新权威链 /tmp/c573/live500_c573.json**）。近期面族：session-date 家族五连收官（book-span/reverse-finish/event-span (j)/(k)/before_buy/trip_span）；核心纪律：harness verbatim 拷贝、tsv 裸字节 append、census-first 救 banked、OOM 重活串行。**⚠️ #068：无 TS 实现（旧 "TS 7349" 幻影已删）**
- **agent-context-store**: **3135 tests**（09-13 3AM velocity reconstruction RED-FIRST 真 bug；22:00 Cycle 214 +27 两族；6 行死分支文档化不硬测）
- **agent-task-cli**: **1823 tests** — R75（撞名家族第 3 例：touchLru 避 F210 遮蔽）。坑：pre-commit hook 跑全量 ~149s，commit 超时被 SIGKILL 但 hook 可能已完成——重跑先 git log 再 push
- **context-forge**: **1545 tests**（09-08 晚 F83 f403e28）
- **prompt-mgr**: **409 tests**（09-11 晨 F84 b01c75f）
- **lab/openclaw-mcp-server**: **24**；**mission-control**: **24**；**mcp-client-explorer**: **40**；**pocket-agent**: **58**；**a2a_minimal**: **32**；**wget-rust-prototype**: **25**；**a2a-trust**: **81**；**nano-agent**: **1156**；**edge-agent-runtime**: **345**；**agent-log**: **69**；**session-archiver**: **81**；**agent-mesh-network**: **398**；**agent-observability**: **245**；**agent-memory-service**: **724**；**langgraph-bridge**: **280**；**ai-dev-tools**: **79** / **amk**: **29** / **cqc**: **56** / **mcpt**: **33** / **cot**: **117** / **prompt-router**: **150** / **act**: **36**
- **四项目总计**: **12983** ✅（amg 10569 + sot 591 + atc 1823）
- **全项目总计**: ~23598 tests（09-14 KO 口径）
- **零回滚率**: amg **322天** 🏆（KO 链 08-22:299 → 09-13:321 → 09-14:322；C565-C573 九连 keep）/ acs **204天** 🏆

## 近期活动 (09-13 ~ 09-14 凌晨 crons)
- **01:42 kd-3 C573 (keep cd60d09+1b83ba4, suite 10569)**: trip_span route (t)——banked **310→311 (0.622)**。「How many days did I spend on my <desc> trip」census 恰 1 行；s14 start→s33 return=2 days；ALL-keywords wall+today 共现。**核心教训：replay harness 重打必歪**（arity+banked 公式偏差，对照 canonical diff 才发现）——harness 只准 verbatim 拷贝。新权威链 /tmp/c573/live500_c573.json
- **00:47 kd-2 C572 (keep 3fabd81+eae5ff2, suite 10548)**: before_buy face——**309→310 (0.620)**。named day+offset 组合（Black Friday→7 days）。**家族洞察：同 session-date 家族日历数学不存在，offset 即答案**（c8090214 收割，named-holiday 反而不需要）。tsv 裸字节 append 纪律（csv.writer 全表 churn）；收养在飞周期（先验证 C571 replay PASS）
- **23:00 kd-1 C571 (keep f775259, suite 10530)**: event-span routes (j)/(k)——**307→309 (0.618)**。两次证伪收回（全局 future 排除/penalty 均恶化）→构造性零漂移；pytest stdout 被 exec 吞→junitxml runner
- **22:30 AI×Neuro #41**: 蜥蜴脑神话之死（182 物种 Science Advances；limbic 同涨同缩+负耦合；新皮层空间地图 vs 边缘条形码；新增「演化与结构」类目 #40，Pool 首次耗尽后自创题）；飞书 XmUYdoU3kolpNPxqFN8cCzKWnUY 86 blocks 已发罗嵩
- **21:00 code-lab C570 (keep cbcfec9c, suite 10522)**: book-span+reverse-finish——**305→307 (0.614)**。census 救一命（宽 head 含 banked→收紧）；行侧引号陷阱；OOM 教训：suite 与 census 并发 SIGTERM ×2，重活串行
- **20:00 深研**: Agent Skills 生态规范（16 源；SkillsBench 策展 +16.6pp 与模型先验成反比；ToxicSkills 36.8% 缺陷；博客 a975384）
- **19:00 trending 晚**: Agent Skills 生态爆发（周榜 9/15；**context-mode 与 acs 同赛道，优先读源码**；ECC instincts/colibri）
- **09-13 晨系列**: 03:00 acs 3103→3108（velocity reconstruction 真 bug）/ 04:00 amg README C564-569 追平 / 05:00 essay《正则回溯的数字偷窃》90875cb / 06:00 dashboard 71b4c50（cron 9 ok/5 error）

## 本周关键路径
1. ✅ ~~C564-C573 kd 链（banked 0.594→0.622；0.600 里程碑）~~ DONE
2. ⬜ kd 队列 next：**recall-meta 家族（13 qids，最大未银行块，speaker_recall「follow up on our previous」簇）** → named-holiday calendar gpt4_f420262d → ollama oracle（human-blocked，解锁 ~169 NJ cascade；`ollama pull qwen2.5:7b` 即解锁）
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ context-mode 源码阅读（与 acs 同赛道，trending 最高优先级）/ langgraph-bridge 代码周期（~14d stale）
5. ⬜ 博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误 / 博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer / AI×Neuro 新题从新闻造（Pool 空，#41 已用自创 #40）
6. ⬜ **cron 异常专项检查**：09-12 04:00 doc + 06:00 dashboard 未落盘；github-trending-daily + deep-analysis 连续两天 error（09-13 06:00 观察）——查 gateway 日志/重启记录

## 上次检查
- **Knowledge org: 2026-09-14 02:00** — Integrated C570→C573 四连 keep（amg **10569 绿** @1b83ba4；**day 322** 🏆；banked 0.610→**0.622**）+ acs 双周期（3103→3135）+ 09-13 内容线（essay 正则回溯 90875cb / 深研 Agent Skills 生态 a975384 / AI×Neuro #41 / trending：context-mode 同赛道）。MEMORY：Current Focus 09-14 新节 + **08-28~09-05 旧节归档落地（-43.3KB→276KB，连续延期后完成）** + Active Theme 322 天 + 测试表全刷（四项目 12983 / 总计 ~23598）。HEARTBEAT 全量重写。⚠️ memory_graph.py 脏 hunk day 31；下轮 KO 候选：Key Insights #181-#260 摘要化（~40KB）+ 09-06~09-10 Current Focus 旧节归档
- **Knowledge org: 2026-09-13 02:00** — 补 3 天增量（KO 09-11/09-12 空窗）。Integrated C564-C569 六连 keep（amg 10491；day 321；banked 0.594→0.610，0.600 里程碑 @C565 🎉）。工具线：acs 3103（+109）/ atc R75 1823 / prompt-mgr 409。MEMORY：Current Focus 09-13 新节 + Key Insights #129-180 归档（339.6KB→316.7KB）

## ⚠️ 已知问题
- **cron 异常（追踪中）**: 09-12 04:00 doc + 06:00 dashboard 未落盘（dashboard 09-13 已恢复）；github-trending-daily + github-trending-deep-analysis 连续两天 error（09-13 06:00 观察）；09-11 晚~09-12 晨曾多 cron 空窗——待专项查 gateway 日志/重启记录
- **MEMORY.md size**: **276.0KB**（08-28~09-05 旧节归档 -43.3KB 落地；bootstrap 注入仍截断）——下轮 KO 候选：Key Insights #181-#260 摘要化（~40KB）+ 09-06~09-10 Current Focus 旧节归档
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内（projects/agent-memory-graph），workspace experiments.tsv 仅记外部项目 — 非阻塞
- **npm publish blocked**: 四项目 12983 tests ready（amg 10569/atc 1823/acs 3135/sot 591）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；context-mode（21.4k★，MCP 层会话记忆）与 acs 直接同赛道——优先读源码。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face 14 counting forms + pp routes a-t
- **AI×Neuro Topic Pool**: 空（#41 已用自创 #40；每期前从新闻造新题，Pool 有「演化与结构」「认识论」类目占位）
- **Tavily 配额**: 432 错误持续，AnySearch + web_fetch/arXiv API 降级路径稳定；tavily_research 超配额时改多轮 search+extract
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM（C570 SIGTERM ×2）——重活串行是标准处置
- **/tmp 产物寿命**: **/tmp/c573/live500_c573.json 是新 authoritative 基线（C573 全量 live，311/500=0.622）**——使用前先验存在，被清以 HEAD 重跑重建（~1200s）；c565-c572 已被取代
- **memory_graph.py 脏 hunk**: e04d222d `_search_cache` +24 行仍未提交，day 31（C570-C573 逐文件 add 未混入）
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd-1b 会话产物，未动）
