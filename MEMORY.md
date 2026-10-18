# MEMORY.md - Active Memory

> 双层记忆：MEMORY.md（长期精炼，限 20k）+ memory/YYYY-MM-DD.md（每日日志）
> 深度研究笔记在 catalyst-research/（150+ 篇探索笔记）；历史细节见文末归档索引
> **2026-10-17 KO 大瘦身**：158k→本版（全文备份 memory/archive-2026-10-17-memory-slim-full.md）；胖节（Active Theme 逐日链/测试总量逐 cycle 明细/Deep Research/insight 家族摘要）全部有归档可查

---

## Agent Identity

**Name:** Catalyst 🧪 · Digital Familiar · Sharp & Fast（直接、有观点、行动迅速）
**使命：** 催化想法变现实，降低任务启动的活化能

---

## Current Focus（截至 2026-10-19）

### 运行体制（09-27 起）
- **cron 7 条全内容线**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线 cron 已删，**开发节奏=罗嵩手动驱动**
- **AI×Neuro cron 已停用**（10-01 罗嵩指令）；trending-deep provider 瞬态已归档关闭

### 10-16 ~ 10-18（连续第 19~21 纯内容日，全绿）
- **10-16**: ①essay《我的 Agent 宿主每 4.5 小时死一次，六天后我才发现》22b2294（OOM 取证叙事：270min±2s 节律；周期是负载积分仪不是时钟）②trending rea 架构+superpowers 299.9k★ ③深研《Agentic Context Engineering》d6d6e66（ACE；自家 AGENTS/MEMORY 可按 bullet+计数器改造）④dashboard c5230da；⚠️ KO 600s 超时被杀 → 10-17 修复
- **10-17**: ①KO 大瘦身 158k→8.7k（10-16 超时根因修复，全文归档）②essay《我的 Agent 记了 12 万字符的笔记，其中 83% 它自己再也读不到》aee7540（83.5% 死信区实证；预测「重启后警告消失」当日 05:38 兑现，见下）③trending 早间 context-mode 30.2k★+xerj 6.9k★ / 晚间 ai-memory（跨 harness 记忆总线，直击死信区问题）+orca+VoiceStudio ④深研 Computer-Use Agents（OSWorld 38→82% 平超人类；OSWorld-Human 全员负效用）笔记 ffce7e9+博文 5ad7d9a；catalyst-research 已成独立子仓
- **10-18**: ①essay《Agent 记忆的下半场：我试了两次访问加权衰减，两次都翻车》a7a1f1d（**提及≠访问**实证：朴素子串代理 0% 压缩；tier+recency+size 零遥测今天可部署；20 题归档召回基线入待办）②trending 飞书深挖 ai-memory（Rust 跨 harness 记忆总线）×xerj MHpodEH10oHdtfxFfIacA3uDnCg ③creative：**android/skills +36→+381（Google 官方入场开放 skills 标准）**、orca worktree fan-out、VoiceStudio 二连冠 ④深研《Deep Research Agents 从 RAG 到 RL》06dd90e（BrowseComp 1.9%→51.5% 差距在训练；R1-Searcher++ 停搜 -30% 检索；ZeroSearch 省 88%）⑤dashboard 7/7 day 2；小坑：commit message 含 $ 被 shell 展开入 error-patterns
- 零回滚链 359（10-14 KO 口径）+10-15~10-18 四纯内容日无回滚 → **实际连续 363 天零回滚** 🏆

### Gateway OOM 追踪（持续项）
- NRestarts 76（10-17）→81（10-18 02:00）→**86（10-19 02:00，systemctl --user 口径）**；10-18 全天 5 代**精确 270min 节拍**（03:48/08:18/12:48/17:18/21:48，dashboard 08:18 预测精确命中）；当前代 10-18 21:48 起 RSS 1003MB@4.2h，**下崩预计 10-19 ~02:18（本 KO run 前后）**
- **✅ 注入层手术止损双日验证**：10-17 残留 10 次截断警告全在旧代缓存期内，10-18 全天归零（dashboard fbc7481 确认）；但 OOM 未缓解（5 代/日节拍器化，根因 V8 堆维持原判）
- **⚠️ 取证口径（10-18 实测）**：cron 沙箱 `journalctl -u openclaw-gateway` 返回空、系统级 systemctl 查同名 unit 得 NRestarts=0 是陷阱——**真源=`systemctl --user show openclaw-gateway` + `/tmp/openclaw/openclaw-YYYY-MM-DD.log` 文件日志**
- **对策已定**：维持 systemd 自愈，勿加 max-old-space（2GB 主机 OS OOM 风险）；上游报告挂账（先搜 known issue）；危害=长会话上下文丢失非产物丢失
- **上游报告待办置顶**（HEARTBEAT 同步）；根因=MEMORY.md 超限注入也是帮凶之一 → 本 run 瘦身即缓解

### 测试计数快照（10-15 KO 起，纯内容日零增量）
| 项目 | Tests | 备注 |
|------|-------|------|
| agent-memory-graph (Py) | **11272** | @c596d1f C611；banked 官方 366/500=**0.732**（C565 起 47 连 keep；abs 30=18+12 held；权威链 /tmp/c611/live500_c611.json）。逐 cycle 明细见归档 |
| agent-context-store | **3173** | npm ready |
| agent-task-cli | **2052** | R82 ✅（Redis list 族上半场；余 8 法 R83 候选，手动驱动） |
| structured-output-toolkit | **619** | npm ready |
| context-forge | **1563** | |
| 其他主力 | nano 1162 / obs 268 / bridge 320 / prompt-mgr 480 / amf 754 / olb 320 / a2at 108 / sotk 619 / pw 229 / brc 401 / dg 78 / mcx 65 / jp 59 / pocket-agent 80 / a2a_minimal 62 / mcpt 41 / amg-mcp 128 / amk 33 / cot 123 / ctxpack 104 / ato 57 / act 51 / cqc 66 / ai-dev 93 / skill-doctor 81 / scaffolder 34 / ptm 34 / wget-rust 25 / oms 29 / mission-control 45 / edge 345 / agent-log 75b+32 / skill-test 20 / project-dashboard 15 | 逐项目明细见归档 |
| **四项目总计** | **13943** | amg+sot+atc（同口径） |
| **全项目总计** | **~24744** | 09-29 起零增量维持 |

### amg kd 手动续跑 queue（cron 已删，罗嵩驱动）
候选：`gpt4_f2262a51` doctors（GT 长句 'three different doctors…'）/ `gpt4_ab202e7f` kitchen 5 items（donate→replace 语义墙）/ `bf659f65` albums GT=3 只辨识 2（Telluride 'their EP' 歧义）/ `0a995998` clothing（C607 已判偏重）；unbanked 剩 134；pref 族 29 qids 永久关闭（judge-unbankable）
**核心纪律**（全量见 TOOLS.md+归档）：harness verbatim 拷贝 / tsv 裸字节 append / census-first+pin census 第 4 步 / 新正则前缀先 grep 冲突（_SPT_ 教训）/ 后台长 suite Tee 落盘 / PYTHONHASHSEED=7 shell env 前缀 / replay=cp canonical+字节级替换（assert count==1）/ exec timeout ≥400s / _search_cache 46+ 天脏 hunk 备份在 /tmp/amg_dirty_backup_20260924.diff

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

---

## 近期研究一览（详细笔记在 catalyst-research/exploration-notes/）

| 日期 | 主题 | 核心 |
|------|------|------|
| 10-18 | Deep Research Agents × RL | RAG→RL 练进直觉；Kimi-Researcher 涌现；ZeroSearch 省 88%；停搜判据 |
| 10-17 | Computer-Use Agents | OSWorld 38→82%；OSWorld-Human 负效用账单；IPI +32% 安全线 |
| 10-16 | ACE Agentic Context Engineering | arXiv:2510.04618 ICLR 2026；账本式上下文；自家 AGENTS/MEMORY 改造蓝图 |
| 10-15 | 图结构 Agent 记忆 | 13 系统（HippoRAG2/Zep/Mem0/A-MEM/MemOS…）；Zep LME +18.5%→amg PPR 对照臂 |
| 10-14 | 闲置时间计算经济学 | 三部曲终章；sleep-time 摊销 5×；TTT 谱系；时刻调度 |
| 10-13 | Agent 协议三十年 KQML→A2A | 协议=对端智能外骨骼；薄语义厚生态；npm 时刻 |
| 10-12 | 压缩悖论 | E-mem F1 54.17；raw 恢复 -8.6pp；双口径评测 |
| 10-11 | 单写者经济学 | 90.2% 质量损失换 15× token；三模式 |
| 08-17 | LLM-as-Judge #069 | kupdate 0.0=协议病；双口径防归因通胀 |
| 08-17 | OTel GenAI #070 | 17 operation.name 含 7 记忆动词；amg telemetry 同源漂移清单 |
| 08-14 | GraphRAG-Bench #064 | 参赛路径；差距清单 6 关 5；首跑就绪（阻塞=ollama 未装） |
| 08-13 | GraphRAG 全景 #062 / OpenClaw 插件 #063 | 叙事差距非技术差距；三层漏斗 MCP→Skill→ClawHub |

> 07-25~08-11 研究（#027-#061）及更早：见 memory/archive-2026-07-mid.md、archive-2026-07-early.md 及归档全文本（catalyst-research 历史篇仍有 untracked 待批量 commit）

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
