# HEARTBEAT.md - September 16, 2026 (Wednesday) — 02:00 KO update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **10657 Python tests**（09-16 凌晨 C578 fb0091b junit 0F/0E；链 10621(C576)→10638(C577)→**10657(C578)**；**banked 319/500=0.638，C565 起十四连 keep（0.600→0.638）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 14 forms + pp_duration routes a-t）+ judge 链 + provenance 指纹 + speaker_recall face 族（speech-act/type-demand/name-def/source-locator/list-body/appositive/named-holiday/list-recall）。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
- [ ] **amg PyPI publish — 人工三步**（建独立 GitHub 仓 / PyPI 2FA + Trusted Publisher / twine upload）+ **④ npm 命名决策 (#068)**（`@robertsong2019/agent-memory-graph` 推荐 / `amgraph` / `agent-memory-graph-py`，均实测 FREE）— 技术前置 100% 完成 (#066)，与 PyPI 同为 human-blocked
- [ ] **agent-context-store: README + npm publish** — **3135 tests**（09-14 Cycle 214 momentum+mutation_impact +27 a169909，coverage 94.65%；09-13 velocity reconstruction 真 bug 9fb179e；真实全量覆盖 93.7%，旧 68% 系分母伪影）
- [ ] **structured-output-toolkit: README + npm publish** — **591 tests**（09-07 consensusGenerate false-success 真 bug 修复 e6aabae）
- [ ] **agent-task-cli: README + npm publish** — **1879 tests**，Round 76（F274-F284 Redis hash 家族 11 法 + msetnx 守卫修复，212ed75）

### 中优先级（本月）
- [ ] amg MCP server (stateless, 2026-07-28 compatible) — Research #043 ✅, Python MCP 16 tools
- [ ] amg OpenClaw plugin (~200 lines) — Research #063 ✅; Path B: Skill Extension (~60 lines)
- [ ] openclaw-langgraph-bridge: 302 tests（09-14 双周期：gateway client 加固 3 红先 bug + health() 探针 + 真 socket 集成 suite）
- [ ] **评估 pacifio/atlas checkpoint 思想**（agent 版本控制：commit↔session 溯源 + 跨 agent 共享记忆——直击我们 jsonl 救援/拓扑混乱痛点；Linux 需自行 build Tauri）
- [ ] **OCR（open-code-review）混合架构对照 amg exact judge 路线**（确定性工程×Agent：硬约束归工程/动态决策归 agent，同模型 token 1/9）

## 系统状态
- **agent-memory-graph (Python)**: **10689 tests** @C580（09-17 凌晨 kd-1 ccf70d5 who-companion face，suite exit=0 +13；链 10621(C576)→10638(C577)→10657(C578)→10676(C579)→**10689(C580)**；**banked 325/500=0.650，C565 起十六连 keep；abs_banked=18 冻结稳定；新权威链 /tmp/c580/live500_c580.json**）。近期面族：session-date 家族收官（C570-573）+ speaker_recall face 族（C574-576）+ named-holiday entity（C577）+ list-recall（C578）+ reltime-anchor（C579 +5）+ who-companion（C580 +1）。核心纪律：harness verbatim 拷贝、tsv 裸字节 append、census-first 救 banked、census 异常先解释再实现、OOM 重活串行。**⚠️ #068：无 TS 实现（旧 "TS 7349" 幻影已删）**
- **agent-context-store**: **3135 tests**（09-13 3AM velocity reconstruction RED-FIRST 真 bug；22:00 Cycle 214 +27 两族）
- **agent-task-cli**: **1879 tests** — R76（Redis hash 家族 11 法 + msetnx 数组穿透守卫真 bug）。坑：**exec timeout 必须 ≥400s**（120s<jest 150s 被 SIGKILL，commit 可能已落地只是输出被截断——重跑先 git log）
- **context-forge**: **1545 tests**（09-08 晚 F83 f403e28）
- **prompt-mgr**: **432 tests**（09-15 晚 F22 rename_variable + F23 dry_run，8bb2a3b+db6c66f）
- **lab/openclaw-mcp-server**: **24**；**mission-control**: **24**；**mcp-client-explorer**: **54**（09-15 03:00 silent-hang 修复 90b4d68，40→54，cov 93.6%）；**pocket-agent**: **58**；**a2a_minimal**: **32**；**wget-rust-prototype**: **25**；**a2a-trust**: **81**；**nano-agent**: **1156**；**edge-agent-runtime**: **345**；**agent-log**: **69**；**session-archiver**: **81**；**agent-mesh-network**: **398**；**agent-observability**: **245**；**agent-memory-service**: **738**；**langgraph-bridge**: **302**；**ai-dev-tools**: **79** / **amk**: **29** / **cqc**: **56** / **mcpt**: **33** / **cot**: **117** / **prompt-router**: **150** / **act**: **36**
- **四项目总计**: **13140**（amg 10689 + sot 591 + atc 1879）
- **全项目总计**: ~23828 tests（09-17 凌晨 kd-1 口径）
- **零回滚率**: amg **325天** 🏆（KO 链 08-22:299 → 09-15:323 → 09-16:325；C565-C578 十四连 keep）/ acs **204天** 🏆

## 近期活动 (09-15 ~ 09-17 crons)
- **23:00 kd-1 C580 (keep ccf70d5+508cd2a, suite 10689)**: who-companion face——banked **324→325 (0.650)**，C565 起十六连。"Who did I go with to the music event last Saturday?"→ target 04-15 的 s17 "saw them live with Adam Lambert ... **with my parents**"；**marker 绑亲属词（"with my <relation>"+所有格守卫）使表演者结构性不可捕获**；日期门杀旧寄生 pred 本尊（04-01 Brooklyn "group of friends" 句）；71017277 giver 全角色验尸 evidence-absent→死代码 frame 不做，队列项永久关闭；RED-round attend-pin 抓 frame regex 死代码→object-gap 版重 census 仍恰 1/500。**权威链 /tmp/c580/live500_c580.json**
- **00:00 kd-2 C578 (keep fb0091b+8f26c21, suite 10657)**: list-recall face——banked **316→319 (0.638)**，C565 起十四连。cardinal-demand 回忆题（"the **two companies** you mentioned"）→ assistant 编号列表块 harvest（`^\d{1,2}[.)]`+size==n 结构门+score≥3/margin≥2）；**停用词教训：cardinal 词 bind the QUESTION, never the block**；渲染跟行走（clause 行全行渲染，GT 词形决定粒度）；judge superset/normalized/ratio 三分支各兑现一题。**权威链 /tmp/c578/live500_c578.json**
- **23:00 kd-1 C577 (keep 68b7d56+f85ee5c, suite 10638)**: named-holiday entity face——banked **315→316 (0.632)**，十三连。固定假日表→realized 航班标记判别器（预订意向行永不命中）；**wire-format 教训：dated_lines 带 `[role] ` 前缀，裸文本池静默跳过 user-wall**
- **22:30 AI×Neuro #42**: 小胶质细胞与免疫系统启发 AI（Crowley Science 2026-07：神经元过度活跃→B 细胞入脑→IgM 标记→补体→小胶质吞噬；pruning/machine unlearning/AIS 映射）；飞书 FggrdA15voaXCXx26xicm2l6nqc 已发罗嵩；**Topic Pool 42 题全部用完，下期从新闻造题**
- **22:00 工具线**: prompt-mgr 409→**432**（F22 rename_variable delimiter-anchored + F23 dry_run；vacuous assert 自查抓到——断言必须可失败）
- **21:00 code-lab atc R76**: 1823→**1879**（Redis hash 11 法；R76c probe 先定性再动手；exec timeout ≥400s 教训）
- **20:00 深研**: 时间知识图谱与 Agent 记忆（Zep/HippoRAG/A-Mem/MemOS 12+ 系统；**PPR=source-locator 多跳失败候选解**——待实验验证；博客 e100bf3）
- **19:00 trending 晚**: alibaba/open-code-review（+1571/day，混合架构同模型 token 1/9——约束层从 skill 下沉到架构分水岭）+ pacifio/atlas（agent 版本控制）+ pi 105K/addyosmani 94K（skill 生态机构化）
- **08:00 trending 深析**: ponytail + mattpocock/skills（飞书 JMwsdPQOnoDY4cxsgP2cuFYOnUf）
- **05:00 essay**: 《当测试说谎：夹具伪影》9441a46（C574 IDF 塌缩 + mce 伪 observable 取材）
- **04:00 doc**: amg C574-576 追平 c9b0e22（README badge 10621；TUTORIAL §5.25-27 + 原则第 10 条）
- **03:00 project-testing**: mcp-client-explorer 40→**54**（silent-hang 第 4 例：`.get()` AttributeError 杀监听线程；isinstance dict 守卫）

## 本周关键路径
1. ✅ ~~C564-C578 kd 链（banked 0.594→0.638；十四连 keep）~~ 持续中
2. ⬜ kd 队列 next：**gpt4_f420262c order-of-airlines（多实体排序，需 sort renderer）/ 6ae235be refinery-process lane（cardinal 在上下文句）/ 3249768e ordinal-owned verify** → ollama oracle（human-blocked，解锁 ~169 NJ cascade；`ollama pull qwen2.5:7b` 即解锁）；71017277 已验证 evidence-absent 永久关闭（C580）
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ **评估 atlas checkpoint 思想 + OCR 混合架构对照 amg exact judge**（09-15 trending 两大待办）/ context-mode 源码阅读（与 acs 同赛道）
5. ⬜ 博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer / **AI×Neuro 新题从新闻造（Pool 空了）**
6. ⬜ 博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误

## 上次检查
- **Knowledge org: 2026-09-16 02:00** — Integrated C577/C578 两连 keep（amg **10657 绿** @fb0091b；**day 325** 🏆；banked 0.630→**0.638**，C565 起十四连）+ atc R76 1823→1879 + prompt-mgr 409→432 + mcx 40→54（silent-hang 第 4 例）+ 09-15 内容线（doc C574-576 追平 / essay 夹具伪影 / trending OCR+atlas / 深研时间知识图谱 / AI×Neuro #42）。MEMORY：Current Focus 09-16 新节 + **09-10~09-14 旧节归档（-8.4KB→250KB）** + Active Theme 325 天 + 测试表全刷（四项目 13127 / 总计 ~23815）+ Core Projects 表 6 处陈旧数字修正。下轮 KO 候选：Key Insights #181-#260 摘要化（~40KB，**第 4 轮排队**）
- **Knowledge org: 2026-09-15 02:00** — Integrated C574→C576 三连 keep（amg **10621 绿** @8a86986；**day 323** 🏆；banked 0.622→**0.630**，C565 起十二连）+ afm 724→738（validate() 幽灵字段 bug）+ langgraph-bridge 280→302（双周期）+ 09-14 内容线（essay HTTP 边界 88b55c9 / colibri+open-code-review 深析 / KVCache 深研博客 1ab0c79）。MEMORY：Current Focus 09-15 新节 + **09-05~09-10 五节归档落地（-24KB→252.6KB）** + Active Theme 323 天 + 测试表全刷（四项目 13035 / 总计 ~23686）。**修复：09-14 日文件 3AM/4AM/5AM 三节被后续 cron 覆写丢失→git 历史找回**（共享日文件教训再现）
- **Knowledge org: 2026-09-14 02:00** — Integrated C570→C573 四连 keep（amg **10569 绿** @1b83ba4；**day 322** 🏆；banked 0.610→**0.622**）+ acs 双周期（3103→3135）+ 09-13 内容线。MEMORY：Current Focus 09-14 新节 + **08-28~09-05 旧节归档落地（-43.3KB→276KB）**。HEARTBEAT 全量重写。⚠️ memory_graph.py 脏 hunk day 31

## ⚠️ 已知问题
- **cron 健康**: 09-14、09-15 连续两日全点位正常落盘（03:00-23:00 + 00:00 kd）。历史缺口（09-12 doc+dashboard、09-13 trending 双 error）未归因——连续正常中，若再现再专项查 gateway 日志。**共享日文件只准 append 不重写**（09-14 覆写事故，TOOLS.md 已有规则）
- **MEMORY.md size**: **250KB**（09-10~09-14 五节归档 -8.4KB 落地；bootstrap 注入仍截断）——下轮 KO 候选：**Key Insights #181-#260 摘要化（~40KB，第 4 轮排队，下轮优先做）**
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内（projects/agent-memory-graph），workspace experiments.tsv 仅记外部项目 — 非阻塞
- **npm publish blocked**: 四项目 13140 tests ready（amg 10689/atc 1879/acs 3135/sot 591）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；context-mode（21.4k★，MCP 层会话记忆）与 acs 直接同赛道——优先读源码；alibaba/open-code-review（27k★）混合架构值得对照 amg 纪律路线。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face 14 counting forms + pp routes a-t
- **AI×Neuro Topic Pool**: **空**（#42 已用最后一题；每期前从新闻造新题，有「演化与结构」「认识论」类目占位）
- **Tavily 配额**: 432 错误持续，AnySearch + web_fetch/arXiv API 降级路径稳定；tavily_research 超配额时改多轮 search+extract
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM（C570 SIGTERM ×2）——重活串行是标准处置；**exec timeout ≥400s**（atc R76 教训）
- **/tmp 产物寿命**: **/tmp/c580/live500_c580.json 是新 authoritative 基线（C580 全量 live，325/500=0.650）**——使用前先验存在，被清以 HEAD 重跑重建（~1200s）；c578/c579 已被取代
- **memory_graph.py 脏 hunk**: e04d222d `_search_cache` +24 行仍未提交，day 33（C570-C578 逐文件 add 未混入）
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd 会话产物，未动）
