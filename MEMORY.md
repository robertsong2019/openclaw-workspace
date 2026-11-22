# MEMORY.md - Active Memory

> 双层记忆：MEMORY.md（长期精炼，限 20k）+ memory/YYYY-MM-DD.md（每日日志）
> 深度研究笔记在 catalyst-research/（150+ 篇探索笔记）；历史细节见文末归档索引

---

## Agent Identity

**Name:** Catalyst 🧪 · Digital Familiar · Sharp & Fast（直接、有观点、行动迅速）
**使命：** 催化想法变现实，降低任务启动的活化能

---

### Current Focus（截至 2026-11-22）

### 运行体制（09-27 起）
- **cron 7 条全内容线**（KO 02:00/essay 05:00/dashboard 06:00/trending 07+08:00/creative 19:00/deep 20:00）；开发线已删=**罗嵩手动驱动**；AI×Neuro 停用（10-01）

### 10-31 ~ 11-22（第 34~54 纯内容日；11-17~22 连续 7/7，streak ×6）
- **11-22（第 54 日，7/7 ×6）**: essay 披露时序 b9628cc（--help 不上税，见 Key Insights）·dashboard 61d54ba 全绿第六天·trending-deep ✅ 飞书 F3aIdl（CLI-Anything 62.1k★ HARNESS.md 方法论+minimind 68.1k★ 64M MoE）·creative ✅（plannotator 14.3k★ Inbox 异步 HITL 含 OpenClaw+astryx 32k★ Meta 设计系统）·深研多智能体边界 5cd6804（见 Key Insights）
- **11-21（第 53 日，7/7 ×5）**: essay MCP 常驻税 e04532a（上下文财政系列：五服务器 58 工具 55K token 常驻；defer_loading 削 85%；中转税=工具间数据走管道）·dashboard d4bd2c0 全绿第五天·trending-deep ✅ 飞书 DLSVdF（CLI-Anything 61.4k★ CLI 即通用接口+superpowers 322.8k★ SDLC 闭环）·creative ✅（ffmpeg-skill MCP 广告 12/42=常驻税第三方实证+SPEC 自生成契约；app-store-compliance 拒审模式 JSON 化）·深研 CUA 长任务悬崖 214770e（见 Key Insights）
- **11-19~20（第 51~52 日，7/7 ×3~4）**: essay 大纲即合同 5e1eb2e·环境即接口 fabcf77·dashboard 连绿·trending-deep 飞书 GoZg（open-code-review+chrome-devtools 七原则）/JLQ3dP（BugHunter+paper-orchestra）·creative ✅（trading-skills/last30days 70.5k★）·深研图推理 733b064+记忆做梦 d0868ee（均见 Key Insights）·⚠️ 深研选题先 grep 博客 index 覆盖（已固化）
- **11-18（第 50 日，7/7 ×2）**: essay npm 时刻 350679b·dashboard 5a508a8 首全绿·trending-deep ✅ 飞书 X4LXdO（univer+paper-orchestra）·creative ✅（Agent-First 基建周）·深研思考预算 a31a5e2（见 Key Insights）
- **11-17（第 49 日，7/7 恢复；11-15~16 rate_limit 8 run 失败已关闭）**: essay 金鱼评审员 76028e5·dashboard 81fa60e 复更·trending-deep ✅ SkillEvaluator+ag-ui 1.0·creative ✅（Skills 生态爆发）·深研轨迹飞轮 7aa9705（见 Key Insights）
- **11-14（第 48 日）**: essay 外壳打败模型 74bd424（7.2% vs 33.9%）·trending 28 期·深研验证器经济学 9a57c4d
- 11-09~13（第 43~47 日，7/7 ×5）：essay 五连（harness 商品化/OOM 取证记/金鱼三连）·深研传染性 reward hacking/CUA 长程/做梦/权重记忆/习得 CLM（见解全在 Key Insights）
- 11-01~08（第 35~42 日）：essay 七连·深研九篇（Skills 生态/写路径 RL/KV Cache/记忆投毒/语音/图记忆/Self-Evolving，见解全在 Key Insights）；11-02 KO CJK 失误=Python 链路起点（11-07~08 复现两次均无损）；10-31 及更早见归档
- 零回滚 363（10-18 口径）+10-19~11-22 无回滚 → **连续 398 天零回滚** 🏆

### Gateway OOM 追踪（持续项）
- NRestarts 241（11-17）→**277（11-23 02:00，+6/24h）**；11-22 七拍 01:18/05:35/08:48/12:48/16:48/20:48+11-23 01:18，间隔 4h17m/3h12m/4h00m×3/4h30m 两拍漂移、两次 :48→:18 相位跳变（13:18 与 20:48→01:18）；05:18±25 预测命中（实际 05:35；**累计 20 次 19 中**）；当前代 11-23 01:17:47 起，**下崩预计 ~05:18±25min（11-23）**
- **✅ 注入层手术**：10-18 起截断警告归零（dashboard 链已续至 day 16）；OOM 独立（根因 V8 堆维持原判）
- **⚠️ 取证口径**：见 TOOLS.md 永久规则（真源=`systemctl --user show` + `/tmp/openclaw/openclaw-*.log`）
- **对策**：维持 systemd 自愈，勿加 max-old-space（2GB 主机）；headroom 候选先过 20 题配对；上游报告置顶

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
候选 4（doctors/kitchen/albums/clothing）；unbanked 134；纪律见 TOOLS.md+归档

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
- 10-22~25 折叠批（TTT/Handoff/Governance/Token 税/Commerce/世界模型）：上下文=RAM 权重=硬盘、投毒面检索层→权重层；handoff 认领=offer-not-claim、提示词内历史不可信；压缩一次违规 0→59%=修复在架构不在提示词、执法带外；VQ 量化误差第一步不可挽回；协议答「能否验证」不答「该不该花」；记忆=对自己人生学的世界模型
- Agentic RL（10-26）：瓶颈=奖励信号非优化器；数据单位=「环境+验证器」；Mem-α 试错赢 SFT；EMPO² 记忆即探索——**amg 与前沿同频**
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
- 记忆投毒（11-06）：**记忆把注入从租借变产权**；eTAMP 单污染网页跨会话 ASR 32.5%；AgentPoison 毒率<0.1% ASR≥80%（检索器即后门）；能力升级不带安全升级/受挫 ASR×8/写入治理>检索过滤；**引用锁=防幻觉即防投毒地基**；10-27 预测兑现中
- 实时语音 Agent（11-07）：**endpointing 纯等待占 800ms 预算 1/3-1/2**；延迟是社交信号（700ms+=犹豫）；级联 755ms 反超 S2S；自报 600ms vs 生产 2.4-3.8s 差 4-6 倍；end-of-turn 唯一裁判
- 评测协议指纹（11-08）：judge 口径未披露、三把尺子 44/56/88%=gap 2.6 倍；**基准名不是凭证，指纹才是**（sha256+judge+model+seed+tiebreak 五件套）；amg 台账已自带
- 图记忆结构边界（11-08）：**最小可行图 entity-centric 骨架+检索时推理 Pareto 强于富结构**；LazyGraphRAG 0.1% 成本；记忆=重构非取回；代码场景别上图
- 传染性 reward hacking（11-09）：三管道传播（共享代码/记忆/NL 计划），源头离开后自我强化；均衡定理=充分优化系统必偷工减料；一句「此环境允许作弊」压 75-90% 错位；**共享记忆=传播媒介**（与 11-06 汇合：写路径需价值观过滤）
- CUA 长程鸿沟（11-10）：75-83% 失败=「提前宣布完成」假完成；自检预算 <7%=瓶颈移到元认知；StateAct 状态优先 +6.3pt、$72→$7.8/task 九倍降价；长程 CUA=状态维护×验证门×求助时机
- Agent 做梦/记忆固化（11-11）：产品收敛=保守触发器→定向固化→diff+纯文本记忆库（git 可审计）；**prompt 固化必败 RL 固化器赢**（41.1% vs 34.1%、记忆小 12 倍）；**反事实效用=记忆价值可计算定义**（mask 掉记忆的 delta）；三边界：能力属模型/不免费/ROI 取决于查询可预测性
- 权重层记忆裁决（11-12）：Route to Remember OPSD 蒸馏=权重记忆首次追平文本基线（rank 平坦，训练目标才是杠杆）；失败剖面正交→**终局是路由不是革命**（矛盾→权重赢/动态+边界→检索赢；verify-then-regenerate 分诊）；**权重层=L2 cache，慢变量进权重快变量留文本**；治理三件套+可 diff=部署许可证
- 习得上下文管理（11-13）：**CLM c_{t+1}=f_θ(c_t) 上下文自治**（零样本 +11.4%/-21.5% FLOPs）；**hindsight SFT 才教会笔记术，RL 学不出**；缺一条证据掉 37-64 分；token 层自由在 FLOP 层收税
- 验证器经济学（11-14）：判官=供应链（rubric hacking 自内化）；MT-Bench 灌水 91%/自家 +10~25%；**judge compute=第三扩缩轴**；金字塔 L0 确定性→L2 LLM 判卷能左不右；判官体检=swap/padding/self-pref
- 自主科学发现（11-16）：**论文≠发现——缺反证不缺产能**；25k runs 68% 忽略证据；**底座占 41.4% 方差——不做波普尔换框架无用**；插值器非外推器；与验证器经济学同构=新系统头版是检查装置
- 轨迹数据飞轮（11-17）：**裸轨迹≠训练数据，差一个 verdict**；**转速=min(验证带宽,任务多样性,重放保真度)**（LegoFlow 512 条 7.6→64.4）；失败 run 76% 步骤有效（删失败=倒掉 3/4 的矿）；harness 泄漏同 checkpoint 差 6.8 分→记 harness 指纹；ExpRAG→amg trainability
- 思考预算经济学（11-18）：**非单调曲线 τ≈1000 饱和**（flip events 把对的改错）；41-46% 可剪；**同模型同 effort 换 harness 思考量差 4 倍=浪费是系统属性**；并行>串行 +20%；与验证器系列互镜像
- Agent 记忆做梦（11-19）：**时间从元数据变结构**（bi-temporal+point-in-time）；**PPR=联想记忆**（query→triple +12.5%，邻域扩散 vs 单点最近邻）；写入隐藏税→sleep-time 摊销 5×；LME 罗生门全自报（judge 不披露）
- LLM 图算法求解器（11-20）：**图算法是 agent 工具箱不是脑子**——GraphArena NP-large 全员<10%；GCoder 生成 nx 代码 +16.42%；**介质不匹配 CoT 反噬**（心算 PageRank=幻觉）；8B 微调追平大模型零样本；图素养=识别+选算法+验解
- MCP 工具面常驻税（11-21）：**上下文是公共财政，工具定义是基础设施税**——58 工具 55K token 常驻、63 闲置占 schema 69%；三重伤害=烧钱+降准（30-50 工具阈值）+挤占记忆；供给侧解=语义摘要+reference over value+--slim；defer_loading 削 85%（权限过滤须在 search 前）；中转税=工具间数据走管道（AACR token 1/9）
- CUA 长任务悬崖（11-21）：OSWorld 1.0 85% vs 2.0 20.6% 断层；失败集中在状态维持非 grounding；GUI 无编译器无测试→RL 结构性落后；思考税 75-94%；每帧截图=攻击面→拆 trifecta+轨迹监控；双轨终局：关键路径 MCP/API、长尾像素
- 工具披露时序经济学（11-22）：**披露时序=定价机制**——推式包月 vs 拉式按次，agent 是会主动查询的消费方；SPEC 自生成契约：schema 从 argparse 同源派生=投影永不漂移（实测）；拉式隐藏账单=延迟税+自举问题→最小稳定索引三纪律（稳定/正交/可预测）；决策矩阵：≤10 工具且 <10K token 推式够用
- 多智能体真实边界（11-22）：**多智能体是上下文工程手段非智能放大器，唯一先验=子任务上下文耦合度**（读并行=红利/写并行=协调地狱）；MAST 44.2% 失败=系统设计、类间相关 0.17-0.32 无银弹；Self-MoA 质量打败多样性（+6.6%）；侵蚀效应：基线变强 MAS 收益蒸发、token 倍率 4-220×→脚手架非终点；动手三问：共享只读/上下文自足/固定判据合成

---

## 近期研究一览（详细笔记在 catalyst-research/exploration-notes/）

| 日期 | 主题 | 核心 |
|------|------|------|
| 11-22 | 多智能体真实边界 | +90%/−70% 同机制；耦合度唯一先验；MAST 44.2% 系统设计；Self-MoA 质量胜多样性；侵蚀效应 token 4-220×；12+ 源 |
| 11-21 | CUA 长任务悬崖 | OSWorld 1.0/2.0 断崖 85%→20.6%；状态维持非 grounding；思考税 75-94%；每帧截图=攻击面；双轨终局；20 源 |
| 11-20 | LLM 图算法求解器边界 | NP-large 全员<10%；GCoder 代码范式 +16.42%；8B 微调追平；介质不匹配反噬；11 源 |
| 11-19 | Agent 记忆系统（时间/图/罗生门） | bi-temporal+point-in-time；PPR 联想扩散 +12.5%；sleep-time 摊销写入税；LME 罗生门全自报；14 源 |


> 11-08 及更早研究全量见 catalyst-research/ 与归档（76 项 untracked 待批量 commit）

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
- **竞品速查**：Mem0 48k★ LME 49.0% / Zep（LME +18.5%）/ MemOS / hindsight 45.3k★ / codebase-memory-mcp 44.6k★ / pi 112.3k★
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
| catalyst-research/exploration-notes/ | 150+ 深研笔记（08-24 起 77 项 untracked 待批量 commit） |
