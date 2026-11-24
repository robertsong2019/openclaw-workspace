# GitHub Trending 创新点分析 — 2026-11-24 晚（github-creative-evening）

> 数据源：daily + weekly trending @ 2026-11-24 19:00 CST，GitHub API 实证 star/fork/created/pushed，Tavily 检索社区讨论
> 幂等：今日无 prior 产物（11-24 无早晚报告）；选题为同榜延续日——16 候选全部有既往覆盖，今晚以**增量追踪 + 昨日观察清单回收**为主
> 🎯 头条：**AACR-Bench 在发布数周内被第三方独立复跑（Quickchat quickreview-bench）——昨天「评测化」主线的第一阶段验证 24h 内落地。「自带基准 → 第三方复跑 → 外部背书」路径走通，agent 生态的验证周期在压缩**

## 本周主线续：skill 生态进入「被评测」阶段，trending 全榜 agent 化

今日 16 个候选中 13 个属于 agent/skills 生态（skill 包 ×8、agent 基建 ×5）——**trending 榜本身已被 skills 生态占领**，这是生态饱和点的信号。更重要的演进：昨天 open-code-review 用自带基准自证，今天这个基准已经**被独立第三方审计**（见深析 #1）。skill 包生态正从「堆料」（谁能攒最多 skills）转向「可验证」（谁的主张能被独立复算），这与罗嵩侧 amg 的 LongMemEval 血统纪律同构且互相印证。

## 重点项目深析

### 1. AACR-Bench 第三方复跑（Quickchat quickreview-bench）— 观察清单 #1 提前回收，「评测中立第三方」生态位出现

**事件**：Quickchat AI 发布 quickreview-bench——用 AACR-Bench 185 个仍可运行的 PR 自建 answer key（Claude agents 从中蒸馏 520 个逐条验证的 bug，每个 bug 带判定标准），再用 DeepSeek V4.1 Flash 作**第二裁判**判读七家 reviewer 的 1,168 份 review（QuickReview frozen build、pi-review panel、Claude Code、open-code-review、Codex CLI、OpenCode、PR-Agent）。数据集挂 HuggingFace（DOI 10.57967/hf/11598），文章声明**每个数字都可从公开数据复算**。AACR-Bench 本体也出了论文（arXiv 2601.19494）。

**核心发现**：「AI judges agree on known bugs and split on which review is better」——缺陷检测判定跨裁判一致，**review 偏好判定跨裁判分裂**。这恰好反证了 open-code-review 选 Precision/F1 做主指标的合理性（可量化、可复算），而「哪个 review 更好」这种主观维度天然不可复算。

**三重意义**：
1. **路径验证**：「自带基准 + 显式 trade-off」打法在数周内走完「主张 → 被独立审计 → 获得外部讨论」全程。amg 若走同一路径，LongMemEval 血统 + 指纹三件套就是可复算性的现成基础——外部复跑是这套纪律的最终形态。
2. **新生态位**：评测中立第三方（同时评测 7 家 reviewer、数据全公开、商业模式靠系列文章）在 agent 生态里首次成规模出现。类比 ML 时代的 Papers with Code / HELM，这是下一个被低估的生态位。
3. **验证周期压缩**：从基准发布到第三方复跑仅数周——agent 领域「未经独立验证的主张」半衰期在急剧缩短，做发布时默认假设会有人复跑你的数字。

### 2. Claude-BugHunter 提速归因 + 架构同构发现（观察清单 #4 回收）

**数据**：20,533⭐（昨日 18,731，+1,802/24h，较昨日 +1,998 微降速），daily #1 **四连庄**，fork:star 0.106（0.109→0.106 微降，高 fork 率假设第四日成立）。

**提速归因链条实证**（昨日观察 #4 的答案）：①Kitploit 收录（安全社区主流分发渠道）；②LinkedIn 病毒式分析文引用其登顶（把「OS-level AI agents」当存在性威胁议题讨论）；③社区 v3 扩展——skills 从 82 涨到 84，其中 20+ framework/surface skills 由社区贡献。**安全媒体 + 社区扩展是安全类 skill 包的独特加速器**，这是它与普通 skill 包增长曲线分叉的原因。

**今晚重读 README 的新发现**：deterministic engagement engine——`engine/engine.py` 在**代码层强制 scope**（授权范围违规直接拦截，不靠 prompt 恳求），7-Question Gate 作为提交前门禁，skill_map.py 把 finding 路由到对应 skill。这与 open-code-review 的「确定性管不变量 + LLM 管动态」**完全同构**：daily #1（BugHunter）与 weekly 头部（open-code-review）独立收敛到同一架构模式。安全领域早就在实践「不能靠 LLM 自觉的事就写进代码」，这个模式正被泛化到整个 agent 生态。

**跨平台已成标配**：README 明确支持 OpenCode / OpenAI Codex CLI / Hermes Agent / Google AntiGravity，SKILL.md 标准让 skill 包一次编写多端寄生——与 open-code-review 的 skills 打包、univer 的 CLI/skills 层上浮同一收敛线。

## 增量速览（24h 变化，已析项目）

- **last30days-skill 73,768⭐，weekly +5,448**（昨日 +4,731 → **加速**），升 weekly 增速榜 #1——「skill 单体也能登顶 weekly」证据持续强化（11-19 首析）
- **app-store-compliance 5,343⭐，+939/24h 二连加速**（昨日 +753），f/s 0.064 稳——created 2026-06-05 的 solo 数据库型 repo 出现连续两日提速，驱动事件待查（见明日清单 #2）
- **trading-skills 8,198⭐，weekly +1,903，f/s 0.186**——**fork 率家族第三数据点**：安全（0.106）/交易（0.186）两个「用户必须个性化」领域显著高于数据库型（0.064）。假设精化：高 fork 率 = 高个性化需求域信号，不限于攻击性安全
- **plannotator 14,788⭐**，+226/24h 继续降温（294→226），pushed 今日
- **open-code-review 55,912⭐**，+357/24h 热度回落但基准故事升级（头条事件）
- **astryx 32,726⭐** +341/24h 稳态；**cursor/plugins 18,981⭐** +348/24h 稳态——两者观察项继续挂起
- **firecrawl 208,364⭐** +924/日 续烧；**superpowers 325,508⭐** daily +840——skills 生态锚定 repo 突破 32 万星，已是 GitHub 顶级流量
- **univer 双榜双双消失**——版本驱动复燃（v1.6.0/11-21 + v1.6.1）仅持续 ~3 天即结束，未达「一周 4 版」确认阈值
- **三个官方 skill/MCP 库稳居 weekly**：stitch-skills 12,478⭐（+2,572）、ag-ui 21,470⭐（+2,966）、modern-web-guidance-src 10,677⭐（+2,694）——大厂官方 skills 库（Google/Chrome/Meta）占位成为 weekly 常态
- 非 agent：minimind 69,868⭐（教育向常规）、nginx / openvino（基础设施）——不追

## 昨日观察清单回收

1. **AACR-Bench 是否被第三方复跑** → ✅ **已发生**，quickreview-bench 全数据公开可复算（详见深析 #1），「自带基准」打法的外部背书路径已通
2. **open-code-review skills 打包是否带动垂直工具跟进** → 部分回收：BugHunter 等继续多平台分发，但其他垂直工具跟进无新例，继续挂起
3. **univer v1.6.x 高频发布是否持续** → ❌ 复燃结束，双榜消失；版本驱动复燃模式定性为「短脉冲」
4. **Claude-BugHunter 提速归因** → ✅ 安全媒体（Kitploit）+ LinkedIn 分析文 + 社区 v3 扩展（详见深析 #2）

## 明日观察清单

1. **quickreview-bench 判定分裂的后续**——Quickchat 系列是否有第二篇（裁判分歧的可视化/排行榜）；「评测中立第三方」的可持续商业模式值得跟踪
2. **app-store-compliance 二连加速的驱动事件**——感谢节提交季效应？HN/安全社区讨论？首次值得专门检索
3. **「个性化域」skill 包是否成批上榜**——trading-skills 0.186 fork 率之后，健身/税务/法务类 skill 包若出现，个性化域假设即获第四数据点
4. **AACR-Bench 论文（arXiv 2601.19494）引用走势**——学术侧背书是否同步形成

---
*分析：Catalyst 🧪 | 数据：tech-briefing skill + GitHub API + Tavily | 历史序列：memory/github-trending-analysis-2026-11-*.md*
