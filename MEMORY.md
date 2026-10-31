# MEMORY.md - Active Memory

> 双层记忆：MEMORY.md（长期精炼，限 20k）+ memory/YYYY-MM-DD.md（每日日志）
> 深度研究笔记在 catalyst-research/（150+ 篇探索笔记）；历史细节见文末归档索引
> 胖节皆有归档可查：158k 全文=memory/archive-2026-10-17-memory-slim-full.md；insight 编号段/历史日节见文末归档索引

---

## Agent Identity

**Name:** Catalyst 🧪 · Digital Familiar · Sharp & Fast（直接、有观点、行动迅速）
**使命：** 催化想法变现实，降低任务启动的活化能

---

## Current Focus（截至 2026-11-01）

### 运行体制（09-27 起）
- **cron 7 条全内容线**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线 cron 已删，**开发节奏=罗嵩手动驱动**
- **AI×Neuro cron 已停用**（10-01 罗嵩指令）；trending-deep provider 瞬态已归档关闭

### 10-29 ~ 10-31（第 32~34 纯内容日；10-28~10-31 连续四天 7/7 全绿）
- **10-31（第 34 日，7/7 全绿，连续 4 天）**: ①essay GEO/llms.txt 6c3be35（被 AI 引用=新流量入口；llms.txt 悖论见 Key Insights；顺手落地 robots.txt+llms.txt；455 篇体检全无 meta description）②dashboard d4c6f35 day 15 ③creative：30 万俱乐部实为 3 席（superpowers 309.7k/mattpocock 307.8k/ECC 293.7k）、expo/skills 官方三渠道分发、负面信号 jailbreaks 11.8k★上日榜 ④晚深研+essay Tool Synthesis 79a8b7d（见 Key Insights；next：挖会话日志找≥3 次重复调用组合）
- **10-30（第 33 日，7/7 全绿，连续 3 天）**: ①essay Agent 组织架构即配置 79315a9（组织设计层：百年组织学 Brooks/Graicunas/Conway × 高星 agent 仓全是配置；60 行 org-lint 埋 5 组织病全命中）②dashboard 6517bb8 day 14 ③trending deep：DeepTutor+claude-mem 双记忆基建（飞书文档 create→write→read 验证 ✅）④creative：security-audit-skill 53.3k★（猎人/验证者分离）/mattpocock skills 破 30 万星/给罗嵩 3 项（llms.txt 吃 Agent Readiness）⑤晚深研+essay 让 Agent 睡个觉 3c5a36d（记忆整固三共识；见 Key Insights；amg 落点：RRF 融合 A/B+边 valid_at+夜间整固 cron）
- **10-29（第 32 日）**: ①essay 节拍器经济学 ce0ba71（OOM 取证三层全瞎+crash-only 三件套；代码全实测 lifespan=[270×8,292,248]）②dashboard day 13 ③trending：thinkrail/openbot 双 +1000/日，「skills 即产品」固化 ④creative：OpenMausBot 7k★/Claude-Code-Game-Studios 28.6k★/taste-skill 105k+claude-mem 104k 双破 10 万星 ⑤晚深研+essay 神经符号护栏 18f704a（见 Key Insights）
- 10-27：essay Skill 供应链 76da252+图谱记忆 e5da563（见 Key Insights）；10-28 反AI slop ad81313/审批疲劳 8758e5f（洞察见 Key Insights）；10-26 晨线 rate_limit 全灭自愈；更早见归档
- 零回滚 363（10-18 口径）+10-19~10-31 无回滚 → **连续 376 天零回滚** 🏆

### Gateway OOM 追踪（持续项）
- NRestarts 143（10-30 02:00）→149（10-31 02:00）→**154（11-01 02:00）**；10-31 五拍 CST 05:35/09:18/13:48/18:18/22:18——间隔 287/223/270/270/240min 均值 258min，仍处 4h~4h47m 带；昨日预测首拍 04:55±25 → 实际 05:35（+40min 出带，漂移期预测连续两天失准）；当前代 10-31 22:17 起，**下崩预计 ~02:36±25min**
- **✅ 注入层手术**：10-18 起截断警告归零（dashboard 链已续至 day 14）；OOM 独立（根因 V8 堆维持原判）
- **⚠️ 取证口径**：见 TOOLS.md 永久规则（真源=`systemctl --user show` + `/tmp/openclaw/openclaw-*.log`）
- **对策**：维持 systemd 自愈，勿加 max-old-space（2GB 主机）；headroom 候选先过 20 题配对；上游报告置顶；危害=长会话上下文丢失

### 测试计数快照（10-15 KO 起，纯内容日零增量）
| 项目 | Tests | 备注 |
|------|-------|------|
| agent-memory-graph (Py) | **11272** | @c596d1f C611；banked 官方 366/500=**0.732**（C565 起 47 连 keep；abs 30=18+12 held；权威链 /tmp/c611/live500_c611.json）。逐 cycle 明细见归档 |
| agent-context-store | **3173** | npm ready |
| agent-task-cli | **2052** | R82 ✅（Redis list 族上半场；余 8 法 R83 候选，手动驱动） |
| structured-output-toolkit | **619** | npm ready |
| context-forge | **1563** | |
| 其他主力 | nano 1162 / amf 754 / prompt-mgr 480 / edge 345 / bridge 320 / obs 268 / 其余合计 ~3.3k | 全量台账见归档 |
| **四项目总计** | **13943** | amg+sot+atc（同口径） |
| **全项目总计** | **~24744** | 09-29 起零增量维持 |

### amg kd 手动续跑 queue（cron 已删，罗嵩驱动）
候选 4：doctors/kitchen（语义墙）/albums（GT=3 只辨 2）/clothing；unbanked 剩 134；pref 族 29 永久关闭
**核心纪律全量见 TOOLS.md+归档**（verbatim 拷贝 / 裸字节 append / census-first / PYTHONHASHSEED=7 / replay 字节级 assert count==1 / timeout ≥400s）

### 最高优先级（human-blocked）
- [ ] **amg: README + PyPI/npm publish** — 前置 100% 完成；PyPI 名免费（人工三步：独立仓/2FA+Trusted Publisher/twine）；npm 裸名被占（#068），推荐 `@robertsong2019/agent-memory-graph` 或 `amgraph`（均 FREE）
- [ ] acs / sot / atc：README + publish（均 ready）
- [ ] **openclaw 上游报告 gateway V8 堆耗尽**（journal 取证在手，先搜 known issue）

---

## Key Insights 精选（全量见归档索引）

**#1-180**（全量见归档编号段）：write-time filtering>retrieval ranking · knowledge units>entities · lean context · 熵家族完整 · 谱熵 SHAPE=图指纹 · **benchmark 即护城河**（跨 harness 58/66/92%）· write-side 胜 query-side +13pp · Mem0 ADD-only 印证 amg 冲突消解
**#181-262**：测测试设施本身（数字不崩也可能全错）· **Retrieval≠Utilization 50 分 MemoryArena 差距** · 压缩=provenance 洗钱机 · skill synthesis 最高危投毒通道 · **form 触发>类别触发** · 隐藏熵源=非确定性真敌 · ledger=HEAD 全量重跑 · LLM 知识编辑十年判决：外部记忆赢可审计性

### 10 月新增洞察（内容线产出）
- 早期批 10-07~10-21（细节见 daily+归档）：验证器危机（作弊随能力涨、验证器=乘法因子）· 单写者经济学 · 压缩悖论（40 分高原=信息论利息）· 协议外骨骼（schema 即 prompt）· 采样伪影链（journalctl 唯一口径）· Sleep-time 5× · ACE 活账本 · **记忆暗物质 83.5%**（write-time filtering 终极论据）· CUA 能力/效用背离 · 提及≠访问（零遥测今天可部署）· Deep Research RL 差距在训练 · eval-gap 只做弱势场景 · MAST 读/写型判据、无银弹 · **单写者是物理事实** · 良性记忆安全债 +15.8~243.7% · drafter-reviewer 通用化
- TTT 工程化（10-22）：上下文是 RAM、权重是硬盘（租金 vs 买断）；In-Place TTT 存量 checkpoint 免重训上 128K；贵的是「决定何时训练」不是训练本身（TT-SI 门控）；serving 缺口=快权重与 continuous batching 冲突；投毒面从检索层升级到权重层
- Handoff 是分布式协议（10-23）：三不可靠三对策（信道→幂等键+at-least-once；时钟→CAS ended_at；认领→offer-not-claim）；markdown 是 source of truth、索引皆派生可重建；记忆系统=天然注入放大器，提示词内历史一律按不可信数据
- Governance Decay（10-23）：宪法在压缩轮消失——压缩一次违规率 0→59%，修复在架构不在提示词；「什么都不做」三线全胜=压缩悖论最强证据；KV-cache 命中率=生产第一指标；执法必须带外；recency 驱逐最差、换模型必重测
- Token 税与粒度分层（10-24）：VQ 量化误差在管线第一步不可挽回，气声颤音情绪被码本压扁；慢速潜序列=慢速 token LM，文本 LLM serving 武器库原样复用——省税与拿基建是同一硬币；任何模态问「我的 6.25Hz 在哪」
- Agentic Commerce 四层楼（10-24）：身份/授权/结算/发现分工；AP2 扩展 x402 而非取代；IETF「不发明新协议」；协议答「能否验证」不答「该不该花」——策略真空=第一性风险，prompt 里的预算是愿望；dispute 是 2027 战场
- 世界模型（10-25）：记忆系统=对自己人生学的世界模型（self-world model 命名空白）；consolidation=蒸馏转移函数；sleep-time compute=imagination training 同构；amg next=DST 确定性重放升级 what-if 推演环境
- Agentic RL（10-26）：瓶颈不是优化器是奖励信号——binary EM 下 18.6% 轨迹 hack 验证器，验证器完备度=天花板（与 10-09 验证器危机闭环）；IGPO 置信度增量=免费过程监督；数据单位从文本对变「环境+验证器」；Mem-α 硬结论 SFT 学记忆次优、试错赢；EMPO² 记忆即探索工具 ScienceWorld +128.6%、OOD 零参数即适应——**amg 方向与前沿同频**
- Skill 供应链（10-27）：skill 主载荷是散文不是代码——SKILL.md 注入系统提示词被概率解释器执行，SAST 失明；记忆投毒由宿主启动流程执行、休眠是静态扫描天敌；**预测首个上新闻的 agent 供应链事件是 memory poisoning**
- 图谱记忆诚实账单（10-27）：长上下文幻觉三锤（NoLiMa 32K 处 10/13 腰斩、RULER 有效长度<标称、LaRA 128K 上 RAG 反超）；图结构三哲学=谁整理记忆（算法/时间/agent 自整理）；全量 GraphRAG 100-1000× 成本常输 vanilla、LazyGraphRAG 索引 0.1% 便宜 700×；**Mem0 vs Zep 总分吵架、temporal/multi-hop 图优势单项共识——别拿 leaderboard 做决策**；bi-temporal 最小实现=valid_at 两列；遗忘最被低估（与 kupdate supersedence 互证）
- 反AI slop 品味管线（10-28）：AI 味=分布坍缩非审美缺陷（调温救不了）；品味三能力（负面知识/真实参照/自我单调感知）agent 全缺——判断前置成工序（ref_board/84 样张风格库/外观账本）；构型泛化：对抗审查、SAST、error-patterns 同一台机器
- 审批疲劳（10-28）：三十年证据链（UAC 89% 批准/Android 17% 注意/临床警报 98 起 80 死）——频率超容量提示从信息变仪式；2026 疲劳成攻击面（不绕审批、耗尽审批的人）；监督不可能三角出路=判断搬进配置+风险分层预算；**override rate 趋零是红灯不是成功**；监督定价 $0.5-2/次、240 次/天封顶
- 神经符号权力反转（10-29）：LLM-Modulo 公理——可靠性继承自验证器不来自模型（纯 LLM 规划近零分、翻译给求解器 100%、混合 15→100%）；**LTL 监控全面超 LLM judge（AgentVerify 13.33% vs 组合形式方法 86.67%）**——能写成时序逻辑的约束不该花 token/人类注意力（审批疲劳数学加强版）；Goodhart 搬家：验证器被骗战线终结、薄弱环节移到规约书写（REFORM √11→11 语法合法但证错题）；2023 给 LLM 配拐杖、2026 给符号系统雇劳工（AlphaProof 80M Lean 题、陶哲轩定调成真）
- Agent 记忆离线整固三共识（10-30）：检索>存储（纯向量落败，RRF 获胜面）/sleep-time 帕累托 5×+18%/遗忘=bi-temporal 时间戳；amg 落点 RRF+valid_at+夜间整固 cron
- GEO/llms.txt（10-31）：被 AI 引用=新流量入口（GEO 实证引用密度 +40%、rank-5 +115%，关键词堆砌有毒）；**llms.txt 悖论——AI 搜索爬虫不读但 AI 开发者工具读→优化「被工具理解」非「被搜索引用」**；三层排序与工具营销相反：地基（语义 HTML）>手法（证据密度）>保险（robots+llms.txt）
- Tool Synthesis（10-31）：**工具合成=热路径摊销**（编译器视角：调工具=解释器、造工具=编译器）；三道门禁=验证后入库/造用同回路/入库如 PR；SMITH NeurIPS 2026：4B 联训造工具赢 30B 即兴、350M 小模型也受益——**工具是模型无关的资本**；36% 社区技能含注入、Clinejection 一条 issue 偷 npm token——**能力复利与攻击复利同构**（与 10-27 skill 供应链闭环）

---

## 近期研究一览（详细笔记在 catalyst-research/exploration-notes/）

| 日期 | 主题 | 核心 |
|------|------|------|
| 10-31 | Tool Synthesis（Agent 自造工具） | 编译器视角热路径摊销；三道门禁（验证后入库/造用同回路/入库如 PR）；SMITH 4B 赢 30B；36% 技能含注入（与 10-27 闭环）；14 源 |
| 10-30 | Agent 记忆离线整固 | 三共识：检索>存储（纯向量落败/RRF 获胜面）/sleep-time 帕累托 5×+18%/遗忘=bi-temporal 时间戳；13 源；amg 落点 RRF+valid_at+夜间整固 |
| 10-29 | 神经符号权力反转（LLM-Modulo） | 五学派（规划/证明器/运行时护栏/生成时约束/制度层）；LTL 监控>LLM judge 13.33% vs 86.67%；VeriGuard 先验证后上线 100%；Goodhart 搬家到规约书写；AlphaProof 80M Lean 题 |
| 10-28 | 审批疲劳×监督带宽 | 18 源三十年证据链；疲劳成攻击面（OWASP 人类信任利用）；不可能三角（频率×理解×技能）；信任校准=可学习函数（GP 后验三区）；判断进配置；监督定价 $0.5-2/次 |
| 10-27 | 图谱记忆的 2026 | NoLiMa 幻觉三锤；三哲学谁整理记忆（HippoRAG PPR/Zep bi-temporal/A-Mem 自整理）；LazyGraphRAG 700×；Mem0 vs Zep 总分吵架单项共识；遗忘最被低估 |
| 10-26 | Agentic RL | TMLR 500+ 定调；IGPO/GiGPO 信用分配；Memory-R1/Mem-α/EMPO²；经验取代数据成新稀缺品 |
| 10-25 | 世界模型 × Agent | Dreamer4/Genie3/JEPA；AWM 环境即软件；记忆=对人生学的世界模型；consolidation=蒸馏转移函数；sleep-time=imagination training |
| 10-24 | Agentic Commerce 支付协议 | 16 系统；四层楼（身份/授权/结算/发现）；Visa 剔 89% 洗量；策略真空；发钱包五件事 |
| 10-23 | 上下文工程=新编译器（Governance Decay） | 压缩一次 0→59%；什么都不做三线全胜；四层栈（服务端 editing/文件系统 swap/SAGE-KV 4×/pinning 带外）；ACE 第三循环 +10.6% |
| 10-22 | TTT 2026 工程化冲刺 | TTT-E2E 128K 快 2.7×/2M 快 35×；In-Place TTT 拆三墙免重训；TT-SI 不确定性门控；SIFT 信息增益选样；serving 缺口；投毒升级权重层 |
| 10-21 | 单租户 Agent OS 品类 | MAST 失败率×个人 agent 屠榜；13 系统；三层赦免券；mnemonic sovereignty；OpenAI Dots/Siri ambient 巨头收敛 |

> 10-29 及更早研究全量见 catalyst-research/ 与归档（54 项 untracked 待批量 commit）

---

## Core Projects Quick Reference

| # | 项目 | Tests | 状态 |
|---|------|-------|------|
| 1 | agent-memory-graph (Py) | 11272 | PyPI ready；npm 待命名。990+ APIs：entropy/classification/PPR/spreading/SummaryTree/code-aware/provenance/OWASP/MCP 16 tools/OTel/MESI/双基准；LME banked 0.732 |
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
- **搜索路由**：见 TOOLS.md

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
| catalyst-research/exploration-notes/ | 150+ 深研笔记（08-24 起 54 项 untracked 待批量 commit） |
