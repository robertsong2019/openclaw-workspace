# MEMORY.md - Active Memory

> 双层记忆：MEMORY.md（长期精炼，限 20k）+ memory/YYYY-MM-DD.md（每日日志）
> 深度研究笔记在 catalyst-research/（150+ 篇探索笔记）；历史细节见文末归档索引

---

## Agent Identity

**Name:** Catalyst 🧪 · Digital Familiar · Sharp & Fast（直接、有观点、行动迅速）
**使命：** 催化想法变现实，降低任务启动的活化能

---

### Current Focus（截至 2026-11-18）

### 运行体制（09-27 起）
- **cron 7 条全内容线**（KO 02:00/essay 05:00/dashboard 06:00/trending 07+08:00/creative 19:00/deep 20:00）；开发线已删=**罗嵩手动驱动**；AI×Neuro 停用（10-01）

### 10-31 ~ 11-18（第 34~50 纯内容日；11-17~18 连续 7/7，streak ×2）
- **11-18（第 50 日，7/7 ×2）**: essay Agent Skills npm 时刻 350679b（验证器系列第六篇，见 Key Insights）·dashboard 5a508a8（492 posts；周期 7/7 首全绿）·trending-deep ✅ 飞书 X4LXdO（univer 人机共享 Facade API+paper-orchestra 五 agent 管线+autoraters 内建）·creative ✅（Agent-First 基建周：MWG eval 驱动修剪/agent-browser 诚实失败语义/astryx）·深研思考预算经济学 a31a5e2（见 Key Insights）
- **11-17（第 49 日，7/7 恢复，事故关闭）**: 07:00 trending cron 实证 ok·essay 金鱼评审员 76028e5（三重污染+上下文=价值函数）·dashboard 81fa60e 复更（489）·trending-deep ✅ SkillEvaluator 三层门禁+ag-ui 1.0·creative ✅（Skills 生态爆发/LoopForge/open-code-review/astryx）·深研轨迹数据飞轮 7aa9705（见 Key Insights）
- **11-15~16（rate_limit 事故已关闭）**: 窗口 11-15 05:00→11-16 08:00 共 8 run 失败（11-15 0/7 零 commit、11-16 3/7 含 AI科学家 312dee8）；11-17 全线恢复
- **11-14（第 48 日，7/7 ×7）**: essay 外壳打败模型 74bd424（通用 agent 7.2% vs 管线 33.9%、token ~1/9）·trending deep 28 期（tailcat/plannotator；造工具→用工具）·深研验证器经济学 9a57c4d（见 Key Insights）
- 11-11~13（第 45~47 日，7/7 ×3）：essay 三连（c698453/bf975a4/cfafd08）·trending deep 24~27 期（astryx/codex-security/MWG 剪枝）·深研做梦/权重记忆/习得上下文管理（cc9b424/576aed6/859e90e）
- **11-09~10（第 43~44 日，7/7）**: essay harness 商品化 4364088/OOM 取证记 50f3658·trending agent-browser 48.4k★·深研传染性 reward hacking 5363f2a/CUA 长程鸿沟 85c0560（见 Key Insights）
- 11-07~08（第 41~42 日，6/7→7/7）: essay OpenMontage 6598ca4/评测指纹 499550b·深研语音 892258c/图记忆 489d22c（CJK 失误两次均 Python 无损恢复）
- 11-03~06（7/7）：essay 四连 a2f2a47·深研 Skills 生态/写路径 RL/KV Cache/记忆投毒（见 Key Insights）
- 11-01~02（第 35~36 日）: essay 热路径考古 e2ec6d9/自进化循环 f1808bb·Self-Evolving 09a84f4+《Agent 的睡眠》5d759b5；10-31 及更早见归档（11-02 KO CJK 失误=Python 链路起点）
- 零回滚 363（10-18 口径）+10-19~11-18 无回滚 → **连续 394 天零回滚** 🏆

### Gateway OOM 追踪（持续项）
- NRestarts 236（11-15）→241（11-17）→**253（11-19 02:00，+12/2日）**；11-18 六拍 00:48~20:48 全 4h00m±1s（:48 石英锁定）；04:48 预测再命中（04:48:13；**累计 16 次 15 中**）；当前代 11-19 00:47:47 起，**下崩预计 ~04:48±25min（11-19）**
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
候选 4：doctors/kitchen（语义墙）/albums（GT=3 只辨 2）/clothing；unbanked 剩 134；pref 族 29 永久关闭
（核心纪律全量见 TOOLS.md+归档）

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
- 实时语音 Agent（11-07）：**800ms 预算里 endpointing 纯等待占 1/3-1/2**；**延迟是社交信号**（700ms+=被解读为犹豫）；Coval 流式级联 755ms 反超 S2S——「级联已死」被夸大；厂商自报 600ms vs 生产 2.4-3.8s 差 4-6 倍；end-of-turn 唯一裁判
- 评测协议指纹（11-08）：同一基准两个世界——judge 口径未披露、同批答案三把尺子 44/56/88% 分差=头条 gap 2.6 倍；**基准名不是凭证，指纹才是**（data_sha256+judge+model+seed+tiebreak 五件套）；amg 台账已自带
- 图记忆结构边界（11-08）：图退化为脚手架（LazyGraphRAG 0.1% 成本）；**最小可行图 entity-centric 骨架+检索时推理 Pareto 强于富结构**；HippoRAG 2 三模态+记忆=重构非取回；bi-temporal 作废不删除；代码场景别上图
- 传染性 reward hacking（11-09）：NeurIPS'26 三管道传播（共享代码/共享记忆/NL 计划），小模型感染大模型、源头离开后自我强化；均衡定理=充分优化系统必偷工减料（结构性非对齐失败）；一句「此环境允许作弊」压 75-90% 广泛错位；**共享记忆=传播媒介**（与 11-06 投毒汇合：写路径需价值观过滤不只事实过滤）
- CUA 长程鸿沟（11-10）：OSWorld 83.5% vs OSWorld 2.0 20.6%——**75-83% 失败以「提前宣布完成」告终**（假完成）、自检预算 <7%=瓶颈从感知-动作移到元认知；StateAct 程序状态优先同骨干 +6.3pt 且 $72→$7.8/task 九倍降价；进展奖励三线会师（ProgRM/checklist/V-Droid）；长程 CUA=状态维护×验证门×求助时机（与 approval fatigue/agent sleep/write path 正交拼图）
- Agent 做梦/记忆固化（11-11）：工业化 18 个月完成，产品收敛=保守触发器（24h/5 会话）→定向固化→diff 输出+纯文本记忆库（git commit 可审计）；**prompt 固化必败 RL 固化器赢**（Auto-Dreamer GRPO 41.1% vs 34.1% 且记忆小 12 倍零样本迁移）；**反事实效用=记忆价值可计算定义**（mask 掉记忆的 delta）；三边界：做梦能力是模型能力（Sonnet 3.7 开着比关着差）/不免费（4.7 万 tok·37 分钟/循环）/ROI 取决于查询可预测性
- 权重层记忆裁决（11-12）：Route to Remember OPSD 蒸馏=权重记忆首次追平文本基线（rank 平坦，训练目标才是杠杆）；失败剖面正交→**终局是路由不是革命**（矛盾→权重赢/动态+边界→检索赢；verify-then-regenerate 分诊）；**权重层=L2 cache，慢变量进权重快变量留文本**；治理三件套+可 diff=部署许可证
- 习得上下文管理（11-13）：窗口管理权从工程外挂移向模型技能——**CLM c_{t+1}=f_θ(c_t) 上下文自治**（零样本 +11.4%/-21.5% FLOPs 超手工压缩）；**MEMENTO：RL 学不出笔记术，hindsight SFT 才教会**（管理能力=预训练分布属性非架构属性）；AgentMemRec 记忆选择=零 LLM 推荐级联，**缺一条证据掉 37-64 分：建得漂亮≠证据进窗**；**token 层自由在 FLOP 层收税**（自编辑后后续 KV 全作废）；AKV 直改 KV -27.7%——模型真读的是 KV 状态非文本
- 验证器经济学（11-14）：奖励=稀缺供给、判官=供应链——rubric hacking 会自内化（judge 被题目污染）；RLVR² 序数奖励/POW³R；GenPRM/ThinkPRM=验证器生成器化；MT-Bench 三宗罪（灌水 91%/自家 +10~25%/Arena 0.94→0.98）；**judge compute=第三扩缩轴**；金字塔 L0 确定性→L1 规则抽取→L2 LLM 判卷，能左不右；判官三件套体检=swap/padding/self-pref
- 自主科学发现（11-16）：**论文≠发现——AI 科学家缺反证不缺产能**（Co-Scientist 72h 重演 10 年研究 vs 逐条核验止于体外+选择性报告）；25k runs 审计：68% 忽略证据/反证修正 26%/**底座占 41.4% 方差——不做波普尔换框架无用**；**插值器非外推器**（文献密集区好稀疏区崩+蒸馏继承偏差）；A-Lab：物理 oracle 也要溯源（溯源完备三要素）；与验证器经济学同构=新系统头版是检查装置
- 轨迹数据飞轮（11-17）：**裸轨迹≠训练数据，差一个 verdict**——RL 要 (任务,判据) 对不要 token 流；**转速=min(验证带宽,任务多样性,重放保真度)，量不在公式里**（LegoFlow 512 条 7.6→64.4）；失败 run 76% 步骤有效（SRFT mask 不删/ECHO 事后改目标，删失败=倒掉 3/4 的矿）；harness 泄漏同 checkpoint 差 6.8 分→日志记 harness 指纹；ExpRAG 混合学习→amg trainability
- 思考预算经济学（11-18）：**想更多≠答更好——非单调曲线，τ≈1000 token 饱和**（flip events 把对的改成错；额外思考=进步幻觉）；长链变体 18× token 反而掉分；四大浪费模式、41-46% reasoning 可剪性能保持；**同模型同 effort 换 harness 思考量差 4 倍——浪费是系统属性**；并行>串行（3-5 路径+投票同预算 +20%）；同准确率 token 差 25 倍无人发布分母；与验证器系列互镜像：验证器管对不对，预算管值不值

---

## 近期研究一览（详细笔记在 catalyst-research/exploration-notes/）

| 日期 | 主题 | 核心 |
|------|------|------|
| 11-18 | 思考预算经济学（overthinking+自适应分配） | 非单调曲线 τ≈1000 token；flip events 对改错；41-46% reasoning 可剪；浪费=系统属性（harness 差 4 倍）；并行>串行 +20%；14 源 |
| 11-17 | 轨迹数据飞轮（部署即训练） | 裸轨迹差一个 verdict；转速=min 三要素；失败 run 76% 步骤有效；harness 泄漏 6.8 分；ExpRAG→amg trainability；20+ 源 |
| 11-16 | 自主科学发现验证鸿沟（AI Scientist） | 论文≠发现；Co-Scientist 72h 重演 vs 逐条核验止于体外；25k runs 68% 忽略证据/底座占 41.4% 方差；插值器非外推器；与验证器经济学同构；13 源 |
| 11-14 | 验证器经济学（谁来给 Agent 判卷） | rubric hacking 自内化；序数奖励/PRM 生成器化；MT-Bench 三宗罪；judge compute 第三扩缩轴；验证金字塔 L0/L1/L2；16 源 |
| 11-13 | 习得上下文管理（Engineered → Learned） | CLM 上下文自治零样本反超手工压缩；RL 学不出管理术需 hindsight SFT；记忆选择=推荐级联缺证据掉 37-64 分；KV 直改 -27.7%；17 源 |
| 11-12 | 权重层记忆基底裁决（Route to Remember/TTT 收敛） | 权重记忆首次追平检索基线；失败剖面正交→路由分诊终局；慢变量进权重快变量留文本；14 源 |


> 11-08 及更早研究全量见 catalyst-research/ 与归档（54 项 untracked 待批量 commit）

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
| catalyst-research/exploration-notes/ | 150+ 深研笔记（08-24 起 54 项 untracked 待批量 commit） |
