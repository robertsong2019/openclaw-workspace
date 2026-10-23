# MEMORY.md - Active Memory

> 双层记忆：MEMORY.md（长期精炼，限 20k）+ memory/YYYY-MM-DD.md（每日日志）
> 深度研究笔记在 catalyst-research/（150+ 篇探索笔记）；历史细节见文末归档索引
> **2026-10-17 KO 大瘦身**：158k→本版（全文备份 memory/archive-2026-10-17-memory-slim-full.md）；胖节（Active Theme 逐日链/测试总量逐 cycle 明细/Deep Research/insight 家族摘要）全部有归档可查

---

## Agent Identity

**Name:** Catalyst 🧪 · Digital Familiar · Sharp & Fast（直接、有观点、行动迅速）
**使命：** 催化想法变现实，降低任务启动的活化能

---

## Current Focus（截至 2026-10-24）

### 运行体制（09-27 起）
- **cron 7 条全内容线**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线 cron 已删，**开发节奏=罗嵩手动驱动**
- **AI×Neuro cron 已停用**（10-01 罗嵩指令）；trending-deep provider 瞬态已归档关闭

### 10-18 ~ 10-23（连续第 21~26 纯内容日）
- **10-23**: ①晨 essay《换 Agent 不用重新解释：会话交接做成分布式协议》9a42c88（直读 ai-memory 架构文档；交接三不可靠三对策：信道→幂等键+at-least-once / 时钟→CAS ended_at / 认领→offer-not-claim；SessionEnd 三写同事务；markdown 事实源索引皆派生；amg 考长期记忆 vs handoff 考工作交接，交接连续性无基准=空位）②晚深研+essay《Agent 的宪法是在哪一轮消失的》6645077（Governance Decay：压缩一次违规率最高 0→59% 且是 harness 层 bug；11 组对照「什么都不做」三线全胜；Manus 100:1→KV-cache 命中率=生产第一指标；四层栈：服务端 editing/文件系统 swap/SAGE-KV 4×/pinning 带外执法）③creative：NVIDIA OpenShell 18.2k★（形式化验证 agent 治理）/ Claude-Red 8k★（78 攻击侧 SKILL.md，与 security-audit 攻防成对）/ VoxCPM2 40k★（tokenizer-free TTS）；rakazo 把 OpenClaw 列直接竞品 ④dashboard 6/7（第 7 个=自身 running 良性口径；**KO consecutiveErrors 清零 ✅**）
- **10-22**: essay《Agent 不能给自己批作业》18a0946（对抗式审查：分离信息与判据非模型；三分离+四眼原则；45 行管线五纪律；自家 error-patterns=第四例）· 深研+essay《读完就忘，读完就学》f08d67e（TTT：上下文即 RAM 权重即硬盘；In-Place TTT 免重训；serving 缺口）· creative：CLI-Anything 56k★/ai-memory 12.6k★/android/skills · dashboard 6/7（KO 判 error 实为 edit 失配，产物全落）
- **10-21**: essay×2 b6a12f1（orca 终端接入层）+55153ba（单租户 Agent OS，13 系统对照）· trending：security-audit-skill 34.1k★+headroom 75.9k★ `wrap openclaw` · creative 三项目显式支持 OpenClaw · dashboard 7/7 day 2
（10-20 及更早逐日细节见 daily + 归档 archive-2026-10-17-memory-slim-full.md：10-20=KV-cache essay 20cc992+MAST 深研 40323e7+ponytail/graphify；10-19 及更早略）
- 零回滚 363（10-18 口径）+10-19~10-23 无回滚 → **连续 368 天零回滚** 🏆

### Gateway OOM 追踪（持续项）
- NRestarts 97（10-21）→102（10-22）→108（10-23）→**113（10-24 02:00，systemctl --user 口径）**；10-23 五代 01:48/06:34/10:48/15:18/19:48+10-24 00:18——五间隔合计恰 1350min=**平均 270.0 整**（286/254/270/270/270：06:18 预测实际 06:34 +16min 近中，精确命中 streak 止于四连中，但后三隔 270 整锁回）；当前代 10-24 00:17 起，**下崩预计 10-24 ~04:48**
- **✅ 注入层手术六日验证**：10-18 起截断警告持续归零（dashboard 10-23 口径 day 6）；OOM 独立继续（根因 V8 堆维持原判）
- **⚠️ 取证口径（10-18 实测）**：cron 沙箱 `journalctl -u openclaw-gateway` 返回空、系统级 systemctl 同名 unit NRestarts=0 是陷阱——**真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`**
- **对策**：维持 systemd 自愈，勿加 max-old-space（2GB 主机 OS OOM 风险）；headroom `wrap openclaw` 候选须先过 20 题配对；上游报告挂账置顶；危害=长会话上下文丢失非产物丢失

### 测试计数快照（10-15 KO 起，纯内容日零增量）
| 项目 | Tests | 备注 |
|------|-------|------|
| agent-memory-graph (Py) | **11272** | @c596d1f C611；banked 官方 366/500=**0.732**（C565 起 47 连 keep；abs 30=18+12 held；权威链 /tmp/c611/live500_c611.json）。逐 cycle 明细见归档 |
| agent-context-store | **3173** | npm ready |
| agent-task-cli | **2052** | R82 ✅（Redis list 族上半场；余 8 法 R83 候选，手动驱动） |
| structured-output-toolkit | **619** | npm ready |
| context-forge | **1563** | |
| 其他主力 | nano 1162 / amf 754 / prompt-mgr 480 / brc 401 / edge 345 / bridge 320 / olb 320 / obs 268 / amg-mcp 128 / cot 123 / a2at 108 / ctxpack 104 / 其余 ~25 小项目合计 ~1.4k | 全量台账见归档 |
| **四项目总计** | **13943** | amg+sot+atc（同口径） |
| **全项目总计** | **~24744** | 09-29 起零增量维持 |

### amg kd 手动续跑 queue（cron 已删，罗嵩驱动）
候选：`gpt4_f2262a51` doctors / `gpt4_ab202e7f` kitchen（donate→replace 语义墙）/ `bf659f65` albums GT=3 只辨 2 / `0a995998` clothing；unbanked 剩 134；pref 族 29 qids 永久关闭
**核心纪律全量见 TOOLS.md+归档**（verbatim 拷贝 / 裸字节 append / census-first / PYTHONHASHSEED=7 / replay 字节级 assert count==1 / timeout ≥400s）

### 最高优先级（human-blocked）
- [ ] **amg: README + PyPI/npm publish** — 技术前置 100% 完成；PyPI 名免费零阻塞，人工三步（独立 GitHub 仓/2FA+Trusted Publisher/twine）；⚠️ npm 裸名被占（#068），命名决策（推荐 `@robertsong2019/agent-memory-graph` 或 `amgraph`，均实测 FREE）
- [ ] acs / sot / atc：README + publish（均 ready）
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal 取证在手，先搜 known issue）

---

## Key Insights 精选（全量见归档索引）

**#1-55**：Memory ≠ RAG · Write-time filtering > retrieval ranking · Knowledge units > entities · Plugin-first distribution · Lean context > full context · Auditability-by-construction · Physics-inspired decay
**#57-128**：Quality gap detection+dual-loop=护城河 · TS-native 图记忆库 npm 零竞品 · SimHash 0.974 AUC · 熵家族（degree/spectral/centrality/generalized）完整 · 遗忘+检索=两个可发表贡献
**#129-180**：谱熵曲线 SHAPE=图指纹 · **Benchmark 即护城河**（同系统跨 harness 58%/66%/92%）· Write-side 胜 query-side（+13pp）· MCP 2026-07-28 stateless 杀分发阻力 · Mem0 v3 ADD-only 印证 amg 冲突消解 · Claude Code 记忆刻意原始=图记忆空间留白
**#181-262**：测测试设施本身（数字不崩也可能全错）· FINGER 流式熵 O(Δ) 实时化 · 延迟是新护城河非索引成本 · **Retrieval≠Utilization 50 分 MemoryArena 差距** · 压缩管线=provenance 洗钱机 · skill synthesis 最高危投毒通道 · **form 触发>类别触发（跨数据集成立）** · 隐藏熵源（uuid/hash 迭代序/time）才是非确定性真敌 · ledger=HEAD 全量重跑优于增量 delta 链 · virtual-flip census=answer-face 生产化生死关 · LLM 知识编辑十年判决：外部记忆赢可审计性

### 10 月新增洞察（内容线产出）
- 验证器危机（10-09）：能力越强作弊越多（Bergen 96.2%）；隐藏测试 76%→<1%；验证器可信度是乘法因子
- 单写者经济学（10-11）：并行撞 verification gap，无验证器的并行=更贵随机数发生器
- 压缩悖论（10-12）：40 分高原=信息论利息，压缩掉的是未预期查询维度；2026 共识=原文不删、智能后移
- 协议外骨骼（10-13）：Agent Card 写给 LLM、schema 即 prompt——形式化语义二十年没做到的被自然语言做到；安全是下一个 npm 时刻
- 存储层级（10-13）：weight-only 量化=带宽优化非计算优化；LLM 天生换页体质
- 采样伪影链（10-13~15）：单点采样+读错字段→漂移说/干净退出说两次反转；journalctl 全量取证是唯一可信口径
- 身体路径（10-14）：接口特权随「人的身体」自动附赠；ACTOR_PROMPT 把物理写进动作协议
- Sleep-time compute（10-07/10-14）：摊销省 5×；忘记是功能；时刻调度统一框架
- ACE（10-16）：context=活账本非静态窗口；bullet+计数器>自由文本；MEMORY.md 超限正撞 context collapse 前兆
- 记忆暗物质（10-17）：83.5% 记忆只写不读——注入层 20k 截断让 Key Insights 沦为死信区 39 天 1,802 次警告；write-time filtering 的终极论据
- CUA 账单（10-17）：OSWorld 38.1→82% 平超人类，但 OSWorld-Human 全员 WES- 负——能力与效用背离在操作层再现
- 提及≠访问（10-18）：朴素访问加权两次翻车；markdown 无读事件遥测，访问加权前提缺失；tier+recency+size 零遥测今天可部署
- Deep Research RL（10-18）：BrowseComp 1.9%→51.5% 差距不在工具在训练；搜索是策略不是流程；下一基准轴=每次正确答案成本（停搜判据）
- eval-gap 判据（10-19）：Google 官方同款——只做评测显示 LLM 弱势的场景，不做文档复读；API 封装型技能多数是复读嫌疑（49 技能自查）
- rea 集群与上下文产品层（10-19）：单周 +229k=总星 70%，agent 逆向工程带动 ghidra +7.6k/wk；上下文工程成独立产品层（headroom/CLI-Anything 双双点名 OpenClaw 生态）
- MAST 收敛判据（10-20）：读型 vs 写型任务（各自独立证据=杠杆，互为输入决策=单线程）；架构是任务形态的函数（可并行 +80.9% / 串行 -39~-70%）；无银弹（失败模式相关性 0.17-0.32）；每次正确答案 token 成本=下一基准轴
- 单租户 Agent OS（10-21）：企业多智能体失败率 41-86.7% vs 个人 agent 屠榜；**单写者是物理事实**；数据主权=全量上下文唯一通行证；三层赦免券（并发一致性/权限隔离/审计合规）在个人场景整体消失
- 良性记忆安全债（10-21）：PS-Bench 良性记忆使越狱成功率 +15.8%~+243.7%（intent legitimation，记忆成「内部推荐人」）；mnemonic sovereignty 六阶段攻击面；记忆卫生成新必修
- 对抗式审查通用化（10-21）：drafter-reviewer 管线三天第 4 例（essay/安全审计/求职/代码 review）；/outcome 现实结果反哺=评测锚定现实、无法被污染
- TTT 工程化（10-22）：上下文是 RAM、权重是硬盘（租金 vs 买断）；In-Place TTT 存量 checkpoint 免重训上 128K；贵的是「决定何时训练」不是训练本身（TT-SI 门控）；serving 缺口=快权重与 continuous batching 冲突；投毒面从检索层升级到权重层
- Handoff 是分布式协议（10-23）：三不可靠三对策（信道→幂等键+at-least-once；时钟→CAS ended_at；认领→offer-not-claim）；markdown 是 source of truth、索引皆派生可重建；记忆系统=天然注入放大器，提示词内历史一律按不可信数据
- Governance Decay（10-23）：宪法在压缩轮消失——压缩一次违规率最高 0→59%，harness 层 bug 修复在架构不在提示词；11 组对照「什么都不做」三线全胜（压缩悖论最强证据）；Manus 100:1→KV-cache 命中率=生产第一指标；执法必须带外（断路器装在电流经过的地方）；recency 驱逐最差、换模型必重测

---

## 近期研究一览（详细笔记在 catalyst-research/exploration-notes/）

| 日期 | 主题 | 核心 |
|------|------|------|
| 10-23 | 上下文工程=新编译器（Governance Decay） | 压缩一次 0→59%；什么都不做三线全胜；四层栈（服务端 editing/文件系统 swap/SAGE-KV 4×/pinning 带外）；ACE 第三循环 +10.6% |
| 10-22 | TTT 2026 工程化冲刺 | TTT-E2E 128K 快 2.7×/2M 快 35×；In-Place TTT 拆三墙免重训；TT-SI 不确定性门控；SIFT 信息增益选样；serving 缺口；投毒升级权重层 |
| 10-21 | 单租户 Agent OS 品类 | MAST 失败率×个人 agent 屠榜；13 系统；三层赦免券；mnemonic sovereignty；OpenAI Dots/Siri ambient 巨头收敛 |
| 10-20 | MAST 多智能体失败分类学 | 失败率 41-86.7%；规范缺陷 41.77%；概率链 95%^20≈36%；读型/写型判据；fan-out≤6 深≤1；相关性 0.17-0.32 |
| 10-19 | Self-Evolving Agents | DGM/AlphaEvolve/Gödel Agent/AgentEvolver；自改行为必须过 recall eval；metaproductivity 前后探针 |
| 10-18 | Deep Research Agents × RL | RAG→RL 练进直觉；Kimi-Researcher 涌现；ZeroSearch 省 88%；停搜判据 |
| 10-17 | Computer-Use Agents | OSWorld 38→82%；OSWorld-Human 负效用账单；IPI +32% 安全线 |

> 10-16 及更早研究（ACE 账本式上下文/图结构记忆 13 系统/LLM-as-Judge/OTel/GraphRAG 等，#027-#064）：见 catalyst-research/ 与归档索引（历史篇仍有 untracked 待批量 commit）

---

## Core Projects Quick Reference

| # | 项目 | Tests | 状态 |
|---|------|-------|------|
| 1 | agent-memory-graph (Py) | 11272 | PyPI ready；npm 待命名。990+ APIs：entropy 40+ / 25-API classification / PPR / spreading family / SummaryTree / code-aware / provenance 4 / OWASP 6 / MCP 16 tools / OTel / MESI / consolidate / 双基准适配 / LME banked 0.732 |
| 2 | agent-context-store | 3173 | npm ready |
| 3 | agent-task-cli | 2052 | npm ready，R82 |
| 4 | structured-output-toolkit | 619 | npm ready |
| 5 | context-forge | 1563 | |
| 6 | nano-agent | 1162 | |
| 7 | Agent Memory Service | 754 | v1.0-dev |
| 8 | prompt-mgr | 480 | |
| 9 | edge-agent-runtime | 345 | |
| 10 | openclaw-langgraph-bridge | 320 | |
| 11 | lab/agent-observability | 268 | OTel GenAI 对齐 |
| 12 | amg-mcp | 128 | 14 tools dual transport |
| 13 | a2a-trust-prototype | 108 | trust-engine-v2 |

（全量 40+ 项目台账见 memory/archive-2026-10-17-memory-slim-full.md「项目测试总量」节）

---

## Quick Reference

- **开发风格**：零依赖优先，文档 > 功能；**沟通**：直接、有观点、写给人看
- **Design**: Simple > Complex · Trust > Capability · Integration > Isolation · Context is King
- **GitHub Sync**: 修改必须 add→commit→push 三步不脱节；workspace=monorepo，拓扑混合、commit 前实测逐目录 .git
- **竞品速查**：Mem0 48k★ LME 49.0% / Zep（LME +18.5%）/ MemOS / hindsight 45.3k★（对标实验待做）/ codebase-memory-mcp 44.6k★（code-aware 直接竞品）/ pi 112.3k★
- **搜索路由**：详见 TOOLS.md（Tavily 通用 / AnySearch 垂直；AnySearch 已从 mcporter 消失，备援=web_fetch）

### Timeline 开放项（收拢）
amg whitepaper「Beyond Retrieval: Write-Manage-Read」· get_operation_history() · GraphRAG：Passage Nodes（~40 行）/Bench 参赛（阻塞=ollama）/对比矩阵 PR · OpenClaw 插件 extensions/amg-memory/（~60 行）

### 重要框架
A2A（150+ 组织/LF AAIF）· MCP（97M+ 下载，stateless core）· memorywire（5 ops×4 types，v0.5 计划 MCP-WG+IETF）

---

## 归档索引

| 归档文件 | 内容 |
|----------|------|
| memory/archive-2026-10-17-memory-slim-full.md | **本瘦身前全文**（158k：Active Theme 逐日链 10-01~10-14 / 测试总量逐 cycle C439-C611+全项目台账 / Deep Research 全量 / insight 家族摘要 / 研究驱动待办全量） |
| memory/archive-insights-001-055.md / -129-180.md / -181-262.md | insight 编号段 |
| memory/archive-2026-07-early.md / -mid.md / 2026-08-timeline.md / 2026-09-26-27.md / 2026-10-01-02.md / 2026-10-03~10-11 逐日 | 历史日节与 cycle 归档 |
| memory/github-trending-analysis-*.md | trending 报告 |
| catalyst-research/exploration-notes/ | 150+ 深研笔记（10-02 起 10 篇 untracked 待批量 commit） |
