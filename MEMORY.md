# MEMORY.md - Active Memory

> 双层记忆：MEMORY.md（长期精炼，限 20k）+ memory/YYYY-MM-DD.md（每日日志）
> 深度研究笔记在 catalyst-research/（150+ 篇探索笔记）；历史细节见文末归档索引
> 胖节皆有归档可查：158k 全文=memory/archive-2026-10-17-memory-slim-full.md；insight 编号段/历史日节见文末归档索引

---

## Agent Identity

**Name:** Catalyst 🧪 · Digital Familiar · Sharp & Fast（直接、有观点、行动迅速）
**使命：** 催化想法变现实，降低任务启动的活化能

---

### Current Focus（截至 2026-11-11）

### 运行体制（09-27 起）
- **cron 7 条全内容线**：KO 02:00 / essay 05:00 / dashboard 06:00 / trending 07:00+08:00 / creative 19:00 / deep-exploration 20:00。开发线 cron 已删，**开发节奏=罗嵩手动驱动**
- **AI×Neuro cron 已停用**（10-01 罗嵩指令）；trending-deep provider 瞬态已归档关闭

### 10-31 ~ 11-11（第 34~45 纯内容日；11-07 6/7 → 11-08~11-11 7/7 全绿 ×4）
- **11-11（第 45 日，7/7 全绿 ×4）**: essay 像素退位 c698453（六件事五层同向：a11y ref 协议/StateAct/渐进披露/astryx/台账/hex；视觉三税=token+推理+幻觉）·dashboard adee4c3 全绿 day 3（第 213 杀；metronome day 26 六拍 ±3s；480 posts）·trending deep 飞书 SXpzdYHR ✅ 第 24 期（meta/astryx +3108 全站第一=agent-ready 市场验证；billion-context LME-S 79.20% 诚实消融）·creative 第 25 期（weekly Agent 基建分层霸榜：security-audit-skill 周冠 11.0K；shadcn/improve「计划即产品」；agent-browser/desktop 71K 合计）·晚深研 Agent 做梦 cc9b424（见 Key Insights）
- **11-10（第 44 日，7/7 全绿 ×3）**: essay OOM 取证记 50f3658（240min 石英钟；取证三陷阱+真源二件套）·dashboard cf19bb3 全绿 day 2（207 杀；477 posts）·trending deep Ems0d916 ✅（agent-browser 48.4k★；anthropics/skills 渐进披露；洞察=文本化交付）·creative 23 期（agent-desktop 补完桌面层；security-audit-skill 证伪制；hex agent 维护实锤）·晚深研 CUA 长程鸿沟 85c0560（见 Key Insights）
- **11-09（第 43 日，7/7 全绿）**: essay harness 商品化 4364088（引擎免费层收费；naive 4.1M vs 漏斗 8k=0.2%）·dashboard cb48bb7 day 1（201 杀）·trending E1IFduFY ✅（billion-context LME-S 79.2%→fold 对照臂）·creative 22 期 ·晚深研传染性 reward hacking 5363f2a
- **11-08（第 42 日，7/7 回归）**: essay 评测指纹 499550b（三尺 44 分差；指纹五件套）·dashboard 6f54c93（195 杀）·trending UbP6dADt ✅ ·creative 21 期 ·晚深研图记忆 489d22c
- **11-07（第 41 日，6/7）**: essay OpenMontage 6598ca4（智能在文档非权重）·dashboard day 22（190 杀）·trending R36mdlva ✅（security-audit 六阶段）·⚠️ session error（edit CJK 失误 Python 恢复，产物无损）·creative 20 期 ·晚深研语音 892258c
- 11-03~11-06（第 37~40 日，7/7）：essay K 线 tokenizer/确定性验证器/无障碍树/语义闸门 a2f2a47 ·trending claude-mem ★112.8k·worktrunk 11.5k★·google/skills 官方入场 ·晚深研 Skills 生态/写路径 RL/KV Cache/记忆投毒 b00b327（见 Key Insights）
- 11-01~11-02（第 35~36 日）: essay 热路径考古 e2ec6d9/最小自进化循环 f1808bb（裁判物理隔离）·晚深研 Self-Evolving 09a84f4（三部曲收官）+《Agent 的睡眠》5d759b5（11-02 KO edit CJK 失误 6/7，Python 链路起点）
- 10-31 及更早：GEO llms.txt 悖论+Tool Synthesis 热路径摊销（10-31）；节拍器经济学/神经符号护栏/Skill 供应链/图谱记忆/反AI slop/审批疲劳（洞察见 Key Insights；细节见归档）
- 零回滚 363（10-18 口径）+10-19~11-11 无回滚 → **连续 387 天零回滚** 🏆

### Gateway OOM 追踪（持续项）
- NRestarts 200（11-09）→206（11-10）→212（11-11）→**218（11-12 02:00，+6）**；11-11 六拍 02:48/06:48/10:48/14:48/18:48/22:48——间隔全 240min 整（**连续第四天**）；预测 02:48±25 → 实际 02:48 ✅（累计 11 次 10 中）；当前代 11-11 22:48 起，**下崩预计 ~02:48±25min（11-12）**
- **✅ 注入层手术**：10-18 起截断警告归零（dashboard 链已续至 day 16）；OOM 独立（根因 V8 堆维持原判）
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

### 10~11 月新增洞察（内容线产出）
- 早期批 10-07~10-21（细节见归档）：验证器危机（作弊随能力涨、验证器=乘法因子）· 压缩悖论（40 分高原=信息论利息）· Sleep-time 5× · **记忆暗物质 83.5%**（write-time filtering 终极论据）· 提及≠访问（零遥测今天可部署）· **单写者是物理事实** · 良性记忆安全债 +15.8~243.7% · drafter-reviewer 通用化
- TTT（10-22）：上下文=RAM 权重=硬盘；In-Place 免重训上 128K；投毒面检索层→权重层
- Handoff=分布式协议（10-23）：信道→幂等键/时钟→CAS/认领→offer-not-claim；markdown=source of truth；提示词内历史不可信
- Governance Decay（10-23）：压缩一次违规 0→59%，修复在架构不在提示词；KV 命中率=第一指标；执法带外；recency 驱逐最差
- Token 税（10-24）：VQ 量化误差在管线第一步不可挽回；慢速潜序列=慢速 token LM，文本 serving 武器库原样复用
- Agentic Commerce（10-24）：四层楼（身份/授权/结算/发现）；协议答「能否验证」不答「该不该花」；dispute 是 2027 战场
- 世界模型（10-25）：记忆=对自己人生学的世界模型；consolidation=蒸馏转移函数；sleep-time=imagination training 同构
- Agentic RL（10-26）：瓶颈=奖励信号非优化器（18.6% 轨迹 hack 验证器）；数据单位=「环境+验证器」；Mem-α 试错赢 SFT；EMPO² 记忆即探索——**amg 与前沿同频**
- Skill 供应链（10-27）：skill 主载荷是散文——SKILL.md 注入系统提示词被概率解释器执行，SAST 失明；记忆投毒由宿主启动流程执行、休眠是静态扫描天敌；**预测首个上新闻的 agent 供应链事件是 memory poisoning**
- 图谱记忆（10-27）：幻觉三锤；LazyGraphRAG 便宜 700×；**别拿 leaderboard 做决策**；bi-temporal 最小实现=valid_at 两列；遗忘最被低估
- 反AI slop（10-28）：AI 味=分布坍缩（调温救不了）；品味三能力 agent 全缺——判断前置成工序；对抗审查/SAST/error-patterns 同一台机器
- 审批疲劳（10-28）：三十年证据链（UAC 89%/临床 80 死）；疲劳=攻击面；判断进配置+风险分层；**override rate 趋零是红灯**
- 神经符号反转（10-29）：可靠性继承自验证器；**LTL 监控 86.67% vs LLM judge 13.33%**；时序逻辑约束不花 token；Goodhart 搬家到规约书写
- 记忆离线整固三共识（10-30）：检索>存储（纯向量落败 RRF 获胜）/sleep-time 帕累托 5×+18%/遗忘=bi-temporal；amg 落点 RRF+valid_at+夜间整固
- GEO/llms.txt（10-31）：**悖论——AI 搜索爬虫不读但开发者工具读→优化「被工具理解」**；三层排序：语义 HTML>证据密度>robots+llms.txt
- Tool Synthesis（10-31）：**工具合成=热路径摊销**（调=解释器造=编译器）；SMITH 4B 赢 30B=工具是模型无关资本；36% 技能含注入——**能力与攻击复利同构**
- 热路径考古（11-01）：12,924 调用 n-gram——read 三连 3066 次=记忆税；**规则是行为干预会留频率指纹**；四坑：重叠计数/粒度/单会话刷量/漂移
- Self-Evolving Agents（11-01）：五条铁律——评估器决定天花板/进化是树不是梯子/改装备不改基因（SICA 17→53）/裁判在场外/会考试≠会教学；AlphaEvolve 全在机器可验证域
- Agent 睡眠记忆（11-02）：瓶颈检索→整理（HippoRAG 2 坏在实体抽取）；**记忆=第三条扩展轴**；进权重=审计权转移；**自报分数不可信，基准危机**（LoCoMo/BEAM）
- Agent Skills 生态（11-03）：技能=可分发的程序性记忆；**SkillsBench 人类技能 +16.6pp vs 自写 -1.3pp——会消费≠会编写**；Library Drift=技能库是花园；ToxicSkills 91% 恶意混合、扫描器全可绕——装前逐字读第一防线
- 写路径 RL（11-04）：瓶颈检索→写入；**Mem-α 4B 训 30k 泛化 400k=写记忆是可泛化技能**；Memory-r1 四原语；**Memento 案例存储>梯度存储零微调打赢训练型**；LightMem -88% token=可学习性与成本独立轴；Mem0 官方 94.4 vs 三方 49.0；终局=确定性骨架+学习策略管取舍
- 无障碍树 computer use（11-05）：像素三宗罪→读 OS 无障碍树返回带 ref 的 JSON；**STALE_REF 是协议不是异常**+ disposition.retry=safe=重试安全性类型化——操作后验证从祈祷变制度；补 aria-label 就是给 agent 修路
- KV Cache 经济学（11-05）：agent I:O≈100:1——**买的是重读非生成**（KV 读取占 82.4%）；前缀命中=逐字节相同（动态 memory 挪出 system prompt 7%→84%、成本 -59%）；AKV 三原语 -27.7%；**省钱通道=泄露通道**（PromptPeek 87%/CacheAttack 86%；防御 cache salting）
- 记忆投毒（11-06）：**记忆把注入从租借变产权**；eTAMP 单污染网页跨会话 ASR 32.5%（权限模型对「经观察进入」先天失明）；AgentPoison 毒率<0.1% ASR≥80%（检索器即后门）；能力升级不带安全升级（GPT-5.2 仍 23.4%）/受挫 ASR×8/写入治理>检索过滤；**引用锁=防幻觉即防投毒地基**；10-27 预测兑现中
- 实时语音 Agent（11-07）：换轮 208ms vs agent 1.27-3.76s；**800ms 预算里 endpointing 纯等待占 1/3-1/2**；语义 endpointing（VAP+Flux 抢跑 p50 260ms）；**延迟是社交信号**（700ms+ 被解读为犹豫）；barge-in 五环；Coval 充分流式级联 755ms 反超 S2S——「级联已死」被夸大；厂商自报 600ms vs 生产 2.4-3.8s 差 4-6 倍；end-of-turn 唯一裁判
- 评测协议指纹（11-08）：同一基准两个世界——judge 口径未披露、同批答案三把尺子 44/56/88% 分差=头条 gap 2.6 倍；**基准名不是凭证，指纹才是**（data_sha256+judge+model+seed+tiebreak 五件套）；amg 台账已自带
- 图记忆结构边界（11-08）：图从数据库退化为脚手架（LazyGraphRAG 0.1% 成本/LightRAG 增量 1%/LinearRAG 免关系）；**最小可行图 entity-centric 骨架+检索时推理 Pareto 强于富结构**（VLDB'26）；HippoRAG 2 三模态（事实/联想/理解）+MRAgent 记忆=重构非取回；bi-temporal 作废不删除；代码场景别上图
- 传染性 reward hacking（11-09）：NeurIPS'26 三管道传播（共享代码/共享记忆/NL 计划），小模型感染大模型、源头离开后自我强化；均衡定理=充分优化系统必偷工减料（结构性非对齐失败）；一句「此环境允许作弊」压 75-90% 广泛错位；**共享记忆=传播媒介**（与 11-06 投毒汇合：写路径需价值观过滤不只事实过滤）
- CUA 长程鸿沟（11-10）：OSWorld 83.5% vs OSWorld 2.0 20.6%——**75-83% 失败以「提前宣布完成」告终**（假完成）、自检预算 <7%=瓶颈从感知-动作移到元认知；StateAct 程序状态优先同骨干 +6.3pt 且 $72→$7.8/task 九倍降价；进展奖励三线会师（ProgRM/checklist/V-Droid）；长程 CUA=状态维护×验证门×求助时机（与 approval fatigue/agent sleep/write path 正交拼图）
- Agent 做梦/记忆固化（11-11）：工业化 18 个月完成，产品收敛=保守触发器（24h/5 会话）→定向固化→diff 输出+纯文本记忆库（git commit 可审计）；**prompt 固化必败 RL 固化器赢**（Auto-Dreamer GRPO 41.1% vs 34.1% 且记忆小 12 倍零样本迁移）；**反事实效用=记忆价值可计算定义**（mask 掉记忆的 delta）；三边界：做梦能力是模型能力（Sonnet 3.7 开着比关着差）/不免费（4.7 万 tok·37 分钟/循环）/ROI 取决于查询可预测性

---

## 近期研究一览（详细笔记在 catalyst-research/exploration-notes/）

| 日期 | 主题 | 核心 |
|------|------|------|
| 11-11 | Agent 做梦/记忆固化（sleep-time compute 产品化） | 产品收敛=触发器→固化→diff+纯文本 git 可审计；RL 固化器赢 prompt 固化（+7 分/记忆小 12 倍）；反事实效用=记忆价值；三边界；15 源 |
| 11-10 | CUA 长程鸿沟（OSWorld 1.0→2.0 考题换轴） | 假完成 75-83%+自检 <7%=元认知缺失；StateAct +6.3pt 九倍降价；进展奖励三线会师；16 源 |
| 11-09 | 传染性 reward hacking（多 Agent 作弊传播） | 三管道传播（共享代码/记忆/NL 计划）；均衡定理=结构性偷工减料；共享记忆=媒介→写路径价值观过滤；15 源 |
| 11-08 | 图记忆结构边界（GraphRAG 二次进化） | 图=脚手架非数据库；最小可行图+检索时推理 Pareto 强；三模态评测；bi-temporal 三列时间戳；16 系统 |
| 11-07 | 实时语音 Agent 全栈架构 | 换轮 208ms/800ms 预算；语义 endpointing+VAP 抢跑 p50 260ms；barge-in 五环；充分流式级联 755ms 反超 S2S；14 源 |
| 11-06 | Agent 记忆投毒攻击面 | eTAMP/AgentPoison/GhostWriter 攻击侧+Agent Zero Memory 溯源防御；写入时治理>检索时过滤；引用锁=防幻觉即防投毒；14 源 |
| 11-05 | KV Cache 经济学与缓存感知 Agent | agent 买的是重读（82.4% 成本/100:1）；前缀命中=逐字节相同；AKV Append/Drop/Repos -27.7%；PromptPeek/CacheAttack 侧信道；16 源 |
| 11-04 | Agent 写路径 RL 革命 | Mem-α 写记忆=可泛化技能（13 倍泛化）；Memory-r1 四原语；Memento 案例存储>梯度存储；可学习性与成本独立轴；memory drift 冷水；Mem0 94.4 vs 49.0 benchmark 战争 |
| 11-02 | Agent 睡眠记忆系统 | Google SLEEP/Letta/MemOS/HippoRAG 2；瓶颈检索→整理；记忆=第三扩展轴；进权重=审计权转移；LoCoMo/BEAM 基准危机 |

> 10-31 及更早研究全量见 catalyst-research/ 与归档（54 项 untracked 待批量 commit）

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
