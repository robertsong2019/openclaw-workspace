# MEMORY.md - Active Memory

> 双层记忆：MEMORY.md（长期精炼，限 20k）+ memory/YYYY-MM-DD.md（每日日志）
> 深度研究笔记在 catalyst-research/（150+ 篇探索笔记）；历史细节见文末归档索引
> **2026-10-17 KO 大瘦身**：158k→本版（全文备份 memory/archive-2026-10-17-memory-slim-full.md）；胖节（Active Theme 逐日链/测试总量逐 cycle 明细/Deep Research/insight 家族摘要）全部有归档可查

---

## Agent Identity

**Name:** Catalyst 🧪 · Digital Familiar · Sharp & Fast（直接、有观点、行动迅速）
**使命：** 催化想法变现实，降低任务启动的活化能

---

## Current Focus（截至 2026-10-23）

### 运行体制（09-27 起）
- **cron 7 条全内容线**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线 cron 已删，**开发节奏=罗嵩手动驱动**
- **AI×Neuro cron 已停用**（10-01 罗嵩指令）；trending-deep provider 瞬态已归档关闭

### 10-18 ~ 10-22（连续第 21~25 纯内容日）
- **10-22**: ①essay《Agent 不能给自己批作业》18a0946（drafter-reviewer 对抗式审查：分离信息与判据而非模型；上下文/判据/利益三分离+四眼原则；投票消独立噪声 vs 对抗消系统性盲区；45 行管线五纪律；自家 error-patterns 升级协议=第四例）②creative：CLI-Anything 56k★（⚠️代码冻结 1 月仍 +3.6k/wk）/ ai-memory 12.6k★（跨 vendor handoff 协议，同赛道待精读）/ android/skills（Google 官方入场 SKILL.md 标准，eval 驱动策展）③深研+essay《读完就忘，读完就学》f08d67e（TTT 工程化冲刺：上下文即 RAM 权重即硬盘；In-Place TTT 存量 checkpoint 免重训 128K；serving 缺口=vLLM 不支持 per-request 快权重）④dashboard 6/7（KO 02:00 被 cron 判 error，实为 edit 失配后改 Python 完成，产物全落）
- **10-21**: ①essay×2——晨《97k 星的 Agent 编排器，只做两件笨事》b6a12f1（orca 终端接入层 N×1；35 行 PTY 适配器三纪律；worktree fan-out 三免费）+ 晚《2026 年最火的 AI Agent，都只服务一个人》55153ba（单租户 Agent OS 品类独立，13 系统对照）②trending 飞书 TpTVdtO1：security-audit-skill 34.1k★+headroom 75.9k★ 官方 `wrap openclaw` ③creative：ai-job-search 62k★/VoiceStudio 79.6k★/context-mode 31.5k★（显式支持 OpenClaw gateway）；rea 周净增首次减速 ④dashboard 7/7 day 2；坑：CJK 近形字「兜/兑」edit 失配（error-patterns）
- **10-20**: essay《省 40% 的 token 账单却 3.3 倍》20cc992（KV-cache 分叉点后缓存全废；朴素截断三宗罪；headroom 未装三理由）· trending ZuHqd7rY · creative ponytail 168.6k★/graphify 129.5k★（OpenClaw 3 天被 4 项目点名）· 深研 MAST 40323e7 · dashboard 7/7 恢复
- （10-19 及更早逐日细节见归档 archive-2026-10-17-memory-slim-full.md + daily）
- 零回滚 363（10-18 口径）+10-19~10-22 无回滚 → **连续 367 天零回滚** 🏆

### Gateway OOM 追踪（持续项）
- NRestarts 97（10-21）→102（10-22）→**108（10-23 02:00，systemctl --user 口径）**；10-22 五代 02:48/07:48/12:18/16:48/21:18（首隔 5h 后 270min×4 精确；**02:48 预测命中精确到分=四连中**，节拍器化 5 日）+10-23 01:48 又一代；当前代 10-23 01:47 起，**下崩预计 10-23 ~06:18**
- **✅ 注入层手术六日验证**：10-18 起截断警告持续归零（dashboard 10-22 口径 day 5）；OOM 独立继续（根因 V8 堆维持原判）
- **⚠️ 取证口径（10-18 实测）**：cron 沙箱 `journalctl -u openclaw-gateway` 返回空、系统级 systemctl 同名 unit NRestarts=0 是陷阱——**真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log`**
- **对策**：维持 systemd 自愈，勿加 max-old-space（2GB 主机 OS OOM 风险）；**新候选（10-19）**：headroom README 明列 `wrap openclaw`——先 doctor+savings 实测，按 eval-gap 判据验收；上游报告挂账置顶（HEARTBEAT 同步）；危害=长会话上下文丢失非产物丢失

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
**核心纪律**（全量见 TOOLS.md+归档）：harness verbatim 拷贝 / tsv 裸字节 append / census-first+pin / 新正则前缀先 grep 冲突 / 后台长 suite Tee 落盘 / PYTHONHASHSEED=7 shell 前缀 / replay=cp canonical+字节级替换（assert count==1）/ exec timeout ≥400s

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

---

## 近期研究一览（详细笔记在 catalyst-research/exploration-notes/）

| 日期 | 主题 | 核心 |
|------|------|------|
| 10-22 | TTT 2026 工程化冲刺 | TTT-E2E 128K 快 2.7×/2M 快 35×；In-Place TTT 拆三墙免重训；TT-SI 不确定性门控；SIFT 信息增益选样；serving 缺口；投毒升级权重层 |
| 10-21 | 单租户 Agent OS 品类 | MAST 失败率×个人 agent 屠榜；13 系统；三层赦免券；mnemonic sovereignty；OpenAI Dots/Siri ambient 巨头收敛 |
| 10-20 | MAST 多智能体失败分类学 | 失败率 41-86.7%；规范缺陷 41.77%；概率链 95%^20≈36%；读型/写型判据；fan-out≤6 深≤1；相关性 0.17-0.32 |
| 10-19 | Self-Evolving Agents | DGM/AlphaEvolve/Gödel Agent/AgentEvolver；自改行为必须过 recall eval；metaproductivity 前后探针 |
| 10-18 | Deep Research Agents × RL | RAG→RL 练进直觉；Kimi-Researcher 涌现；ZeroSearch 省 88%；停搜判据 |
| 10-17 | Computer-Use Agents | OSWorld 38→82%；OSWorld-Human 负效用账单；IPI +32% 安全线 |
| 10-16 | ACE Agentic Context Engineering | arXiv:2510.04618 ICLR 2026；账本式上下文；自家 AGENTS/MEMORY 改造蓝图 |
| 10-15 | 图结构 Agent 记忆 | 13 系统；Zep LME +18.5%→amg PPR 对照臂 |
| 10-14 | 闲置时间计算经济学 | sleep-time 摊销 5×；TTT 谱系（三部曲终章） |

> 10-10 及更早研究（#027-#064，含 LLM-as-Judge/OTel/GraphRAG 全景）：见归档索引（archive-2026-07-* 等）及 catalyst-research/（历史篇仍有 untracked 待批量 commit）

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
- amg Positioning whitepaper「Beyond Retrieval: Write-Manage-Read」· get_operation_history()（MemOps 兼容）
- GraphRAG 侧：Passage Nodes（~40 行）· GraphRAG-Bench 参赛（唯一阻塞=ollama 未装）· README 对比矩阵+Awesome-GraphRAG PR
- OpenClaw 插件分发：extensions/amg-memory/（SKILL.md+plugin.json，Path B ~60 行）

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
