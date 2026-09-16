# HEARTBEAT.md - September 17, 2026 (Thursday) — 02:00 KO update

## 待办任务

### 🔴 最高优先级（本周）
- [ ] **agent-memory-graph: README + PyPI/npm publish** — **10705 Python tests**（09-17 凌晨 C581 509063b；=C580 junit 10689+C581 新文件 16 defs，collect stdout flake 吞改静态口径；链 10657(C578)→10676(C579)→10689(C580)→**10705(C581)**；**banked 326/500=0.652，C565 起十七连 keep（0.600→0.652）**），990+ APIs。能力全景（详 tsv/README）：entropy/classification/FINGEREntropy 谱系 + PPR + spreading family + SummaryTree + code-aware + OWASP 安全套件 + amg-bench + MCP 16 tools + OTel telemetry + MESI 多智能体 + consolidate + retrieval QA + Experience Compression + GraphRAG lifecycle + 双基准适配 + 时序/计数答案侧机制族（counting 14 forms + pp_duration routes a-t）+ judge 链 + provenance 指纹 + speaker_recall face 族（speech-act/type-demand/name-def/source-locator/list-body/appositive/named-holiday/list-recall/reltime-anchor/who-companion/sectioned-recall）。⚠️ #068：无 TS 实现；npm 裸名被占，命名决策 human-blocked，README 终稿前须定
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
- **agent-memory-graph (Python)**: **10705 tests** @C581（09-17 凌晨 kd-2 509063b sectioned-recall face；链 10657(C578)→10676(C579)→10689(C580)→**10705(C581)**；**banked 326/500=0.652，C565 起十七连 keep；abs_banked=18 冻结稳定；新权威链 /tmp/c581/live500_c581.json**）。近期面族：named-holiday entity（C577）+ list-recall（C578）+ reltime-anchor（C579 +5）+ who-companion（C580 +1）+ sectioned-recall（C581 +1，header-only 实体匹配）。**pref 族 29 qids 永久关闭**（GT 是元句式，离线 judge 永远无法 bank）。核心纪律：harness verbatim 拷贝、tsv 裸字节 append、census-first 救 banked、census 异常先解释再实现、OOM 重活串行。**⚠️ #068：无 TS 实现（旧 "TS 7349" 幻影已删）**
- **agent-context-store**: **3135 tests**（09-13 velocity reconstruction + Cycle 214）
- **agent-task-cli**: **1879 tests** — R76（Redis hash 家族 11 法 + msetnx 守卫）。坑：**exec timeout 必须 ≥400s**（120s<jest 150s 被 SIGKILL，重跑先 git log）
- **context-forge**: **1545 tests**（09-08 F83；09-16 跑出 1523+1 系 Node runner IPC flake 第 4 例=上游 bug 不追，flaky 跑总数偏小是已知形态）
- **prompt-mgr**: **447 tests**（09-16 晚 F24 validate_all+CLI doctor / F25 snapshot flush-first，509c585+fed0eb9）
- **mission-control**: **33 tests cov 99%**（09-16 3AM 24→33，main() 注入接缝，9e326e3）
- **lab/openclaw-mcp-server**: **24**；**mcp-client-explorer**: **54**；**pocket-agent**: **58**；**a2a_minimal**: **48**（09-16 Content-Length 守卫+终态语义）；**wget-rust-prototype**: **25**（09-16 hygiene：git ls-tree 补交漏交 build 文件）；**a2a-trust**: **81**；**nano-agent**: **1156**；**edge-agent-runtime**: **345**；**agent-log**: **75**（09-16 esc_json 反斜杠 no-op 真身暴露）；**session-archiver**: **81**；**agent-mesh-network**: **398**；**agent-observability**: **245**；**agent-memory-service**: **738**；**langgraph-bridge**: **302**；**ai-dev-tools**: **79** / **amk**: **29** / **cqc**: **56** / **mcpt**: **33** / **cot**: **117** / **prompt-router**: **150** / **act**: **36**
- **四项目总计**: **13175**（amg 10705 + sot 591 + atc 1879）
- **全项目总计**: ~23890 tests（09-17 KO 口径）
- **零回滚率**: amg **328天** 🏆（KO 链 08-22:299 → 09-15:323 → 09-16:326 → 09-17:328；C565-C581 十七连 keep）/ acs **205天** 🏆

## 近期活动 (09-16 ~ 09-17 crons)
- **00:58 kd-2 C581 (keep 509063b+e6e0194, suite 10705)**: sectioned-recall face——banked **325→326 (0.652)**，十七连。named-section demand → assistant 自己的 "N. <Header>:" 编号 section harvest；**header-only 实体匹配**（兄弟 section 行文本也提 "Lake Charles"）；唯一性门 ≥2 headers=fall-through；**pref 族 29 qids 永久关闭**（judge-unbankable offline）。**权威链 /tmp/c581/live500_c581.json**
- **23:00 kd-1 C580 (keep ccf70d5+508cd2a, suite 10689)**: who-companion face——banked **324→325 (0.650)**。亲属词 marker "with my <relation>"+所有格守卫，表演者（Adam Lambert）结构性排除；71017277 evidence-absent 永久关闭；ops 三课（pytest 孤儿/pgrep 自匹配/chained-sed 假 PASS 险情）
- **01:00 kd-3 C579 (keep 00966e8+0653598, suite 10676)**: reltime-anchor face——banked **319→324 (0.648)，+5**。相对偏移→绝对目标日期（month=30d）→realized fact；demand frame 绑问题端
- **22:00 工具线**: prompt-mgr 432→**447**（F24 doctor：lone `}` 对称补齐；F25 snapshot：flush-first+同秒 .N 防撞）
- **21:00 code-lab 三发**: a2a-minimal 32→**48**（Content-Length 守卫+终态语义）/ wget-rust hygiene（**git ls-tree 查项目完整性**，4 个历史 cycle 漏交 build 文件）/ agent-log 69→**75**（**esc_json 反斜杠翻倍从来是 no-op**——双引号 bash 解析坑）
- **20:00 深研**: **Context Rot 与有效上下文长度**（Chroma/NoLiMa/RULER/FLenQA/Anthropic 12 源；与 09-15 时间知识图谱「记忆即压缩」闭环；博客 2460bab；next：长度敏感性配对测试/tool result clearing/rerank 小 k/mini-RULER）
- **08:00 trending 深析**: **colibri**（+2173/日，纯 C 磁盘流式 MoE；「placement 只定速度不定语义」红线）+ **VoiceStudio**（+2776/日，本地 16 TTS+11 ASR）；飞书 S3vsdOgw
- **05:00 essay**: 《共享工作树下的 agent 版本控制》f9ef935（git 三隐含假设失效→拓扑探针/staged 验尸/transcript 重放三防线+atlas-lite trailer，dogfooding）
- **04:00 doc**: amg C577-579 追平 b483ebe（badge 10676；TUTORIAL §5.28-30 + 原则第 11 条：demand 词作用域显式绑定）
- **03:00 project-testing**: mission-control 24→**33 cov 99%**（main() 注入接缝）；prompt-mgr 432/atc 1879 全绿；context-forge IPC flake 第 4 例（上游不追）

## 本周关键路径
1. ✅ ~~C564-C581 kd 链（banked 0.594→0.652；十七连 keep）~~ 持续中
2. ⬜ kd 队列 next（C581 重排后）：**where 族（8 qids: 51a45a95/6ade9755/f8c5f88b/e01b8e2f/gpt4_b5700ca0/830ce83f/9ea5eabc/07741c45）/ counting 族（7 qids）/ speaker_recall stragglers（8 qids）/ 3249768e ordinal-owned verify** → ollama oracle（human-blocked，解锁 ~169 NJ cascade；`ollama pull qwen2.5:7b` 即解锁）；~~pref 族~~ closed（judge-unbankable）；~~71017277~~ closed（evidence-absent）
3. ⬜ README(agent-memory-graph) → npm publish + **amg PyPI 人工三步 + npm 命名决策** — **BLOCKED on human action**
4. ⬜ **评估 atlas checkpoint + OCR 混合架构对照 + colibri 红线借鉴**（09-16 trending）/ context-mode 源码阅读（与 acs 同赛道）
5. ⬜ 博客候选 the-question-is-the-join-condition + presupposition-failure-is-an-answer / **AI×Neuro 新题从新闻造（Pool 空了）**；context-rot 笔记 next actions（配对测试/rerank 小 k）
6. ⬜ 博客勘误节（e9dd6a4 6.1×→1.02×）+ C538 0.508 勘误

## 上次检查
- **Knowledge org: 2026-09-17 02:00** — Integrated C579/C580/C581 三连 keep（amg **10705**（=10689 junit+C581 静态 16 defs，collect stdout flake 吞）；**day 328** 🏆；banked 0.638→**0.652**，十七连；pref 族 29 qids 永久关闭）+ mission-control 24→33 cov 99% + prompt-mgr 432→447（F24/F25）+ code-lab 三发（a2a 48/wget-rust hygiene/agent-log 75）+ 09-16 内容线（doc C577-579 / essay 共享工作树 / trending colibri+VoiceStudio / 深研 context-rot）。MEMORY：Current Focus 09-17 新节 + **Key Insights #181-262 归档落地（-42KB→213KB，第 4 轮排队兑现）** + Active Theme 328 天 + 测试表全刷（四项目 13175 / 总计 ~23890）+ Core Projects 表刷新
- **Knowledge org: 2026-09-16 02:00** — Integrated C577/C578 两连 keep（amg **10657 绿** @fb0091b；day 325；banked 0.630→**0.638**）+ atc R76 1879 + prompt-mgr 432 + mcx 54。MEMORY：Current Focus 09-16 新节 + 09-10~09-14 旧节归档（-8.4KB）+ Core Projects 表 6 处陈旧修正
- **Knowledge org: 2026-09-15 02:00** — Integrated C574→C576 三连 keep（amg **10621 绿**；day 323；banked 0.622→**0.630**）+ afm 724→738 + bridge 280→302。MEMORY：09-05~09-10 五节归档（-24KB）。**修复：09-14 日文件三节被覆写丢失→git 找回**

## ⚠️ 已知问题
- **cron 健康**: 09-14 ~ 09-16 连续三日全点位正常落盘。历史缺口（09-12 doc+dashboard、09-13 trending 双 error）未归因——连续正常中，若再现再专项查 gateway 日志。**共享日文件只准 append 不重写**（09-14 覆写事故，TOOLS.md 已有规则）
- **MEMORY.md size**: **213KB**（09-17 Key Insights #181-262 归档 -42KB 落地；bootstrap 注入仍截断）——剩余大头：Current Focus 08-15~09-27 旧节（再攒几天归档）+ Timeline 区
- **experiments.tsv 结构性缺口**: amg C410+ cycle 条目记录在项目仓内（projects/agent-memory-graph），workspace experiments.tsv 仅记外部项目 — 非阻塞
- **npm publish blocked**: 四项目 13175 tests ready（amg 10705/atc 1879/acs 3135/sot 591）。README 需 human review + amg npm 命名决策（#068 human-blocked）
- **Competitive pressure**: hermes-agent 242k★；context-mode（21.4k★，MCP 层会话记忆）与 acs 直接同赛道——优先读源码；alibaba/open-code-review（27k★）混合架构值得对照 amg 纪律路线；colibri/VoiceStudio 本地化基础设施三件套成型（「hold, not rent」）。amg differentiators: GraphRAG lifecycle + code-aware + OWASP suite + judge/cascade A/B 工具链 + answer-face 14 counting forms + pp routes a-t
- **AI×Neuro Topic Pool**: **空**（#42 已用最后一题；每期前从新闻造新题）
- **Tavily 配额**: 432 错误持续，AnySearch + web_fetch/arXiv API 降级路径稳定；tavily_research 超配额时改多轮 search+extract
- **相邻 cron CPU 竞争**: suite 与 census/A/B 并行争核且 2GB 内存下 OOM——重活串行是标准处置；**exec timeout ≥400s**
- **/tmp 产物寿命**: **/tmp/c581/live500_c581.json 是新 authoritative 基线（C581 全量 live，326/500=0.652）**——使用前先验存在，被清以 HEAD 重跑重建（~1200s）；c579/c580 已被取代
- **memory_graph.py 脏 hunk**: e04d222d `_search_cache` +24 行仍未提交，day 34（C570-C581 逐文件 add 未混入）
- **amg 工作树杂物**: temporal_test_data.json / test_optimization.py / test_status.log 未跟踪（kd 会话产物，未动）
