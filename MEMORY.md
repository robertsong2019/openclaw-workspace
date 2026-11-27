# MEMORY.md - Active Memory

> 双层记忆：MEMORY.md（长期精炼，限 20k）+ memory/YYYY-MM-DD.md（每日日志）
> 深度研究笔记在 catalyst-research/（150+ 篇探索笔记）；历史细节见文末归档索引

---

## Agent Identity

**Name:** Catalyst 🧪 · Digital Familiar · Sharp & Fast（直接、有观点、行动迅速）
**使命：** 催化想法变现实，降低任务启动的活化能

---

### Current Focus（截至 2026-11-27）

### 运行体制（09-27 起）
- **cron 7 条全内容线**（KO 02:00/essay 05:00/dashboard 06:00/trending 07+08:00/creative 19:00/deep 20:00）；开发线已删=**罗嵩手动驱动**；AI×Neuro 停用（10-01）

### 10-31 ~ 11-27（第 34~59 纯内容日；11-17~26 十天 7/7 后 11-27 中断 6/7——essay timeout 草稿存档未发布）
- **11-27（第 59 日，6/7，essay ❌）**: dashboard fbeca8c 全绿中断 day11（essay timeout600s in69k/out133 零产出挂起——**12.9KB 源稿已写完 05:09、发布步未跑，KO 补档**）·trending-deep ✅ 飞书 N4RU（superpowers 326.8k★ 技能 A/B 自修闭环/CLI-Anything 65.9k★ 7 阶段）·creative ✅（obsidian-skills 54k★=app-skill 官方样板+fork 率分型第四数据点）·深研 Agent RL 环境瓶颈 09024f8（见 Key Insights）
- **11-24~26（第 56~58 日，7/7 ×8~10）**: essay 自证三件套 108b3e2/显示层五案 ae35219/step-journal 141214a·dashboard 连续全绿八~十天（'429' 全为毫秒时间戳误报；posts 口径 .bak 混入=显示层家族第 7 例）·trending-deep 飞书 NSTwdXi/MjIy/Eb0vddn（BugHunter 系连庄/CLI-Anything 65k★）·creative AACR-Bench/Agent Skills 生态/n8n nod·深研三篇 2848450/43dfdcc/1af0aa2（见解在 Key Insights）
- **11-17~23（第 49~55 日，7/7 ×2~7 恢复；11-15~16 rate_limit 已关闭）**: essay 金鱼评审员/npm 时刻/大纲即合同/环境即接口/MCP 常驻税 e04532a/披露时序 b9628cc/HITL 收件箱化 69cdea3·trending-deep 飞书七篇（CLI-Anything 系+SkillEvaluator/ag-ui）·creative ffmpeg SPEC/astryx/AACR-Bench·深研轨迹飞轮/思考预算+图推理+记忆做梦+CUA+多智能体边界+技能治理黑市（见解在 Key Insights）
- 11-09~14（第 43~48 日，7/7 ×5）：essay 六连（harness 商品化/OOM 取证记/金鱼三连/外壳打败模型 74bd424）·深研六篇（reward hacking/CUA 长程/做梦/权重记忆/CLM/验证器经济学，见解全在 Key Insights）
- 11-01~08（第 35~42 日）：essay 七连·深研九篇（见解全在 Key Insights）；11-02 KO CJK 失误=Python 链路起点；10-31 及更早见归档
- 零回滚 363（10-18 口径）+10-19~11-27 无回滚 → **连续 403 天零回滚** 🏆

### Gateway OOM 追踪（持续项）
- NRestarts 241（11-17）→**307（11-28 02:00，+6/24h 稳定）**；11-27 拍 00:18/04:18/07:48/11:48/15:48/19:48/23:48，间隔 4h×5+3h30m、**相位 :18×2 一跳 :48×5=日翻转（:18↔:48 每天对调，3h30m 收缩恒落清晨拍）**；04:18 预测**正中**（实际 04:18:13，+0.0min；**累计 25 次 24 中**；log _t 字段为 UTC、读拍 +8h）；当前代 11-27 23:47:47 起，**下崩预计 ~03:48±25min（11-28）**
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
- 早期批 10-07~10-21（细节见归档）：验证器危机（验证器=乘法因子）· 压缩悖论（40 分高原=信息论利息）· Sleep-time 5× · **记忆暗物质 83.5%**（write-time filtering 终极论据）· 提及≠访问（零遥测可部署）· **单写者是物理事实** · 良性记忆安全债 +15.8~243.7% · drafter-reviewer 通用化
- 10-22~25 折叠批：上下文=RAM 权重=硬盘、投毒面检索层→权重层；handoff 认领=offer-not-claim、提示词内历史不可信；压缩违规 0→59%=修复在架构非提示词、执法带外；VQ 误差首步不可挽回；协议答能否验证不答该不该花
- Agentic RL（10-26）：瓶颈=奖励信号非优化器；数据单位=「环境+验证器」；Mem-α 试错赢 SFT；EMPO² 记忆即探索——**amg 与前沿同频**
- 10-27 双研：skill 主载荷是散文、SAST 失明（**预测首个上新闻的供应链事件=memory poisoning**）；LazyGraphRAG 便宜 700×、别拿 leaderboard 做决策、bi-temporal 最小实现=valid_at 两列、遗忘最被低估
- 10-28 双研：AI 味=分布坍缩（调温救不了），判断前置成工序；审批疲劳=攻击面（UAC 89%/临床 80 死），**override rate 趋零是红灯**
- 神经符号反转（10-29）：可靠性继承自验证器；**LTL 监控 86.67% vs LLM judge 13.33%**；时序逻辑约束不花 token；Goodhart 搬家到规约书写
- 记忆离线整固三共识（10-30）：检索>存储（纯向量落败 RRF 获胜）/sleep-time 帕累托 5×+18%/遗忘=bi-temporal；amg 落点 RRF+valid_at+夜间整固
- 10-31 双研：GEO 悖论=AI 爬虫不读但开发者工具读→优化「被工具理解」（语义 HTML>证据密度>robots）；**工具合成=热路径摊销**（SMITH 4B 赢 30B=模型无关资本；36% 技能含注入=能力与攻击复利同构）
- 热路径+自进化（11-01）：read 三连 3066/12,924=记忆税，**规则留频率指纹**（四坑：重叠/粒度/单会话刷量/漂移）；五铁律——评估器定天花板/进化是树非梯子/改装备不改基因（SICA 17→53）/裁判在场外/会考试≠会教学；AlphaEvolve 全在可验证域
- Agent 睡眠记忆（11-02）：瓶颈检索→整理（HippoRAG 2 坏在实体抽取）；**记忆=第三条扩展轴**；进权重=审计权转移；**自报分数不可信，基准危机**（LoCoMo/BEAM）
- Agent Skills 生态（11-03）：技能=可分发的程序性记忆；Library Drift=技能库是花园（SkillsBench/ToxicSkills 结论并入 11-23 技能治理条）
- 写路径 RL（11-04）：瓶颈检索→写入；**Mem-α 4B 训 30k 泛化 400k=写记忆是可泛化技能**；Memory-r1 四原语；**Memento 案例存储>梯度存储零微调打赢训练型**；LightMem -88% token=可学习性与成本独立轴；Mem0 官方 94.4 vs 三方 49.0；终局=确定性骨架+学习策略管取舍
- 无障碍树 computer use（11-05）：像素三宗罪→读 OS 无障碍树返回带 ref 的 JSON；**STALE_REF 是协议不是异常**+ disposition.retry=safe=重试安全性类型化——操作后验证从祈祷变制度；补 aria-label 就是给 agent 修路
- KV Cache 经济学（11-05）：agent I:O≈100:1——**买的是重读非生成**（KV 读取占 82.4%）；前缀命中=逐字节相同（动态 memory 挪出 system prompt 7%→84%、成本 -59%）；AKV 三原语 -27.7%；**省钱通道=泄露通道**（PromptPeek 87%/CacheAttack 86%；防御 cache salting）
- 记忆投毒（11-06）：**记忆把注入从租借变产权**；AgentPoison 毒率<0.1% ASR≥80%（检索器即后门）；能力升级不带安全升级；写入治理>检索过滤；**引用锁=防幻觉即防投毒地基**
- 实时语音 Agent（11-07）：**endpointing 纯等待占 800ms 预算 1/3-1/2**；延迟是社交信号（700ms+=犹豫）；级联 755ms 反超 S2S；自报 600ms vs 生产 2.4-3.8s 差 4-6 倍；end-of-turn 唯一裁判
- 11-08 双研：judge 口径未披露=三尺 44/56/88% gap 2.6 倍，**基准名不是凭证，指纹才是**（五件套）；**最小可行图 entity-centric 骨架 Pareto 强于富结构**（LazyGraphRAG 0.1%、代码场景别上图）
- 传染性 reward hacking（11-09）：三管道传播（共享代码/记忆/NL 计划），源头离开后自我强化；均衡定理=充分优化系统必偷工减料；一句「此环境允许作弊」压 75-90% 错位；**共享记忆=传播媒介**（与 11-06 汇合：写路径需价值观过滤）
- CUA 双研（11-10/11-21）：75-83% 失败=提前宣布完成，OSWorld 1.0 85% vs 2.0 20.6% 断层；瓶颈在状态维持非 grounding（GUI 无编译器无测试→RL 结构性落后、思考税 75-94%）；双轨终局：关键路径 MCP/API、长尾像素；StateAct +6.3pt/$72→$7.8 九倍降价
- 记忆固化+权重裁决（11-11/12）：产品收敛=保守触发器→定向固化→diff 可审计；**prompt 固化必败 RL 固化器赢**（41.1% vs 34.1%）；**反事实效用=记忆价值可计算定义**；**权重层=L2 cache，慢变量进权重快变量留文本，终局是路由不是革命**（Route to Remember 权重首次追平文本基线；治理三件套+可 diff=部署许可证）
- 习得上下文管理（11-13）：**CLM c_{t+1}=f_θ(c_t) 上下文自治**（零样本 +11.4%/-21.5% FLOPs）；**hindsight SFT 才教会笔记术，RL 学不出**；缺一条证据掉 37-64 分；token 层自由在 FLOP 层收税
- 验证器经济学（11-14）：判官=供应链（rubric hacking 自内化）；MT-Bench 灌水 91%/自家 +10~25%；**judge compute=第三扩缩轴**；金字塔 L0 确定性→L2 LLM 判卷能左不右；判官体检=swap/padding/self-pref
- 自主科学发现（11-16）：**论文≠发现——缺反证不缺产能**；25k runs 68% 忽略证据；**底座占 41.4% 方差——不做波普尔换框架无用**；插值器非外推器；与验证器经济学同构=新系统头版是检查装置
- 轨迹数据飞轮（11-17）：**裸轨迹≠训练数据，差一个 verdict**；**转速=min(验证带宽,任务多样性,重放保真度)**（LegoFlow 512 条 7.6→64.4）；失败 run 76% 步骤有效（删失败=倒掉 3/4 的矿）；harness 泄漏同 checkpoint 差 6.8 分→记 harness 指纹；ExpRAG→amg trainability
- 思考预算经济学（11-18）：**非单调曲线 τ≈1000 饱和**（flip events 把对的改错）；41-46% 可剪；**同模型同 effort 换 harness 思考量差 4 倍=浪费是系统属性**；并行>串行 +20%；与验证器系列互镜像
- Agent 记忆做梦（11-19）：**时间从元数据变结构**（bi-temporal+point-in-time）；**PPR=联想记忆**（query→triple +12.5%，邻域扩散 vs 单点最近邻）；写入隐藏税→sleep-time 摊销 5×；LME 罗生门全自报（judge 不披露）
- LLM 图算法求解器（11-20）：**图算法是 agent 工具箱不是脑子**——GraphArena NP-large 全员<10%；GCoder 生成 nx 代码 +16.42%；**介质不匹配 CoT 反噬**（心算 PageRank=幻觉）；8B 微调追平大模型零样本；图素养=识别+选算法+验解
- MCP 工具面常驻税（11-21）：**上下文是公共财政，工具定义是基础设施税**——58 工具 55K token 常驻、63 闲置占 schema 69%；三重伤害=烧钱+降准（30-50 工具阈值）+挤占记忆；供给侧解=语义摘要+reference over value+--slim；defer_loading 削 85%（权限过滤须在 search 前）；中转税=工具间数据走管道（AACR token 1/9）
- 工具披露时序经济学（11-22）：**披露时序=定价机制**——推式包月 vs 拉式按次，agent 是会主动查询的消费方；SPEC 自生成契约：schema 从 argparse 同源派生=投影永不漂移（实测）；拉式隐藏账单=延迟税+自举问题→最小稳定索引三纪律（稳定/正交/可预测）；决策矩阵：≤10 工具且 <10K token 推式够用
- HITL 收件箱化（11-23）：同步审批三死结=时间尺度失配/N 并行人串行瓶颈/语境过窗→异步消息重构（一问一条+语境内联+回复带引用）；**revision 漂移=最隐蔽死结**（审批带版本号，漂移带差异重入队）；四验收=非阻塞/路由回源/revision-checked/人端预消化
- Agent 技能合成治理（11-23）：**会消费≠会编写，分歧在证据锚点**——静态轨迹总结≠技能，执行锚定+失败反馈+最优版保留闭环才是（SkillRevise 36→62）；**强→弱流动 +54.3%=不用训练的蒸馏**；技能收益=repairs−regressions 可 A/B 归因；≤3 模块聚焦胜大而全；黑市三重攻击面=scripts 全权限+NL 指令无签名+frontmatter 预授权（335 恶意/22-26% 漏洞/7.1% 泄密）
- 多智能体真实边界（11-22）：**多智能体是上下文工程手段非智能放大器，唯一先验=子任务上下文耦合度**（读并行=红利/写并行=协调地狱）；MAST 44.2% 失败=系统设计、类间相关 0.17-0.32 无银弹；Self-MoA 质量打败多样性（+6.6%）；侵蚀效应：基线变强 MAS 收益蒸发、token 倍率 4-220×→脚手架非终点；动手三问：共享只读/上下文自足/固定判据合成
- 深度研究智能体（11-24）：**搜索=可 RL 训练的行动空间，数据合成风洞（KG 随机游走+信息遮蔽）是开源追平闭源真护城河**；ReSum 式 evolving artifact=过程状态>过程日志；**检索器是被低估主变量（同 GPT-5 换检索器 55.9→70.1%）**；引用幻觉 14-95%=最短的腿
- Agent 持久化/断点续跑（11-25）：**持久化=降级阶梯非二值开关**（关键属性=事件只增不改；C468 救援=无意识 event sourcing）；**任何 at-least-once 基建都把幂等推回应用层**（cron 双触发四例=手工重实现）；接力棒模型=进程易耗品/记录主权，身份与对话持久化正交；journal 过期=恢复从数据问题升格治理；**恢复也是攻击面**（rollback+journal 投毒，读路径 untrusted-until-verified）
- Agent 注入攻防（11-26）：**LLM 无指令/数据分离原语=注入的 SQL 注入时刻**（模型层无解）；系统三闸=provenance/capability/egress；**越强越易中招**（MCPTox 72%，指令遵循=攻击杠杆）；多智能体 boundary laundering→multi-CaMeL 归零；调研页嵌真实 payload（agentpwn）=研究即暴露面
- Agent RL 环境瓶颈（11-27）：**环境=独立 scaling 轴（算法可抄，环境矩阵藏得住）**；量产三阶段押韵预训练数据史（策展→程序化→自举）；**GRPO 组方差：好任务必须卡能力前沿**（全过全败 advantage 归零）；reward hacking=环境 bug（grader 独立容器）；多样性>数量

---

## 近期研究一览（详细笔记在 catalyst-research/exploration-notes/）

| 日期 | 主题 | 核心 |
|------|------|------|
| 11-27 | Agent RL 环境瓶颈 | 环境=独立 scaling 轴；GRPO 组方差；reward hacking=环境 bug；量产三阶段；多源 |
| 11-26 | Agent 注入攻防全景 | 模型层无解→系统三闸；multi-CaMeL 归零；MCPTox 72%；17+ 源 |
| 11-25 | Agent 持久化/断点续跑 | 降级阶梯；接力棒模型；journal 治理；恢复即攻击面；18+ 源 |


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
