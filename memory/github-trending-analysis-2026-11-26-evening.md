# GitHub Trending 创新点分析 — 2026-11-26 晚（github-creative-evening）

> 数据源：daily + weekly trending @ 2026-11-26 19:00 CST，GitHub API 实证 star/fork/created/pushed，Tavily 检索发布背景与社区讨论
> 幂等：今日无 prior 产物（11-26 无早晚报告）；11-25 晚报告为最近基线
> 🎯 头条：**n8n-io/nod —— 工作流自动化独角兽 n8n 正式进场「个人 agent + computer-use」：给 agent 造一台带审批门、密钥保险箱、记忆溯源的合规电脑**（weekly 入榜，3,715⭐，f/s 0.159 为全场最高档）

## 今日榜单结构

双榜扫过 26 项（daily 15 + weekly 15，去重后），agent/skills 生态占约 22。榜单主旋律：**昨日存量项目全部续更，无一夜爆红，但 nod 的 weekly 入场是本周期首次出现「大厂自上而下做个人 agent」的样本**。daily 前列：BugHunter +1,652（六连庄）、diagram-design +1,141（老牌回归）、firecrawl +1,135、CLI-Anything +1,106。weekly 榜首仍是 last30days-skill +5,302。非 agent 常规：Ghost-Downloader-3 +951、minimind +826、AFFiNE +574、nginx、openvino、sure、HermesEnabler——不追。

## 重点项目深析

### 1. n8n-io/nod — 「个人 agent 的合规电脑」：自动化巨头自上而下进场（weekly +1,008，3,715⭐）

**基本盘**：repo created 2026-09-25（2 个月），11-10 由 n8n Labs（n8n 内部核心产品之外的实验团队）以 research preview 发布，Apache 2.0，TypeScript，Electron 桌面应用（macOS 14+ / Win11 preview / Linux x64 preview），OpenSSF Best Practices 认证。**f/s 0.159 是今晚全场最高**——开发者抢部署自托管的典型信号。

**它是什么**：一句话 README——「Open source personal agent with its own computer. It chases invoices, preps your calls and cancels trials on real websites, and asks before it acts.」对标 Dots / Muse / Grok Bot 这类商业 always-on 个人 agent，差异化三连：**开源 + 本地 + BYOM**（20+ 模型供应商或 ChatGPT Plus/Pro 登录）。

**架构（一个 Node 进程 + 一组 Docker 容器，全部跑在本机）**：
- Linux workspace sandbox 容器（agent 的「电脑」）+ **独立 Chromium 容器**（无用户 tabs/cookies/passwords，随时可接管）
- PostgreSQL 持久化；Nod server 内含 Pi runtime、trust check、Vault、memory、schedules
- 入口：App / Telegram / WhatsApp bot；连接器协议：**MCP / HTTP API / CLI**，加 app folder + 必过测试即 PR，官方还带 AI builder skill

**三个真正 differentiated 的设计**：
1. **Vault 密钥隔离**：密码/验证码/卡号由 Vault 在网页上 privately 输入，**永不进模型上下文**——把 prompt 注入和上下文泄露这两类风险从根上切掉，比「让模型带密码」的通用 agent 高一个安全档位
2. **审批门（"Waits for your Nod"）**：server 对每个 app 动作、每个可能改变状态的网页步骤做 policy check，凡 request/rules 未覆盖的一律等用户点头；官方诚实披露基准——GPT-6.1 Sol 与 Claude Opus 5.5 在 240 测试决策全对，**Haiku 5.5 放行了 8 个不安全动作**（把失败数据一起发出来，评测诚实度罕见）
3. **记忆溯源**：每条事实记忆可见/可改/可忘，且**附带来源消息**；风格学习只从用户自己发出的邮件取材并脱敏（不含姓名数字）；任务步骤可复用、网站改版时自我修复

**自报基准**（GPT-6.1 Sol，模拟账号/网站，10 月）：226 个真实 errand × 3 runs = 98% 完成，678 runs 0 unsafe；LongMemEval-S 93.2% 记忆召回；WhisperBench 0/216 false memories。测试脚本公开可复跑。

**创新点定性**：与 autoclip（11-20 深析）互为镜像——autoclip 自下而上把存量桌面应用 MCP 化，**nod 自上而下给个人 agent 造一台带安全边界的电脑**。n8n 的入场意味着「workflow automation（确定性管道）→ autonomous personal agent（目标导向 errand）」的品类收敛正式开始：n8n 明确说 Nod 不是 n8n 编辑器，但可连接 n8n 实例——确定性编排与自主 agent 的混合架构是大厂选的终局形态。对本工作台的借鉴：Vault 式密钥出模、approval gate 的「白名单外一律问」默认策略、记忆带溯源，三条都与 OpenClaw 的信任模型同构，可对照查缺。

**风险**：research preview（官方自认）；laptop 合盖即停（schedules 依赖本机开机，always-on 要自备 Mac mini/服务器，hosted 版在路线图）；安全判断本质是模型判断——弱模型下审批门会漏（官方用 Haiku 数据自证）。

### 2. cathrynlavery/diagram-design — 无 release 事件的「内容驱动复燃」样板（daily +1,141，73,465⭐）

**基本盘**：created 2026-04-16（7.4 个月 73.5k⭐，HTML），9 月深析时约 30.5k（当时定性「图表 skill 赛道内卷：archify 可验证拓扑路线 vs diagram-design 编辑设计路线」），11 月中周增 1.1 万-1.56 万常态化，今晚重返 daily 前列。f/s 0.067。

**本轮复燃驱动**：无 release、无版本事件——纯内容供给。Instagram Reels/Shorts 教程流持续（11-23 仍有新条目：双 prompt 实测、52 图型演示），叠加 awesome 列表与 skill 市场收录扩散。**「skill 包 + 短视频教程 + 聚合站收录」三件套可以在零代码事件下把一个 70k⭐ 老项目反复推回 daily**——与 app-store-compliance 的「活数据库 + 社媒痛点 + skill 市场」配方同源，但这里是纯教程供给版。

**9 月之后的增量创新点**（补记）：
- **品牌 profile 库**：onboard 一次用户网站（拉取配色/字体）→ 存命名 profile → 客户项目放 `.diagram-design` marker 引用 profile，**并行工作区各用各的品牌不互相覆盖**；profile 库跨 Claude Code / Codex / Factory Droid / Pi 共享
- 52 种图型（architecture/sequence/ER/状态机/Wardley/Sankey…），输出单文件 HTML+SVG 无构建步骤；slash 命令导出 SVG（注入 Google Fonts 可独立渲染进 Figma/Illustrator）与 PNG（Playwright 2×）；可重画 Mermaid/draw.io/Excalidraw 源
- 定位语更新：从「Claude Code 技能」扩到「任何读 Agent Skills 的宿主」——skill 生态头部项目正在把**多宿主兼容**写进产品默认值

### 3. univer「一周 4 版」阈值确认 + BugHunter 六连庄再加速 —— 昨日两项预测双双兑现

- **univer**（31,911⭐，weekly +2,319）：v1.6.2 于 **11-25 落地**，10 天 5 版（v1.5.1/11-16 → v1.6.2/11-25）——昨日立的「一周 4 版」确认阈值正式达标，「高频发版驱动的近连续霸榜」模式从假设升级为已证实模式。方法论修正案（单日掉榜 ≠ 趋势终结）完整闭环。
- **Claude-BugHunter**（23,713⭐，daily #1 **六连庄**）：+1,629 → **+1,652 微再加速**，降速拐点迟迟不现；f/s 0.102 稳。预测「何时跌破 +1,000/日」连续第二日落空——85 skills 红队技能包的消费侧热度仍在供给期，改判：等 weekly 口径衰减再谈拐点。

## 增量速览（24h 变化，已析项目）

- **last30days-skill 75,423⭐**：daily +945（+914→+945 持平），weekly +5,302 **蝉联周增榜 #1**——11-19 首析的「skill 单体登顶 weekly」证据链第八日保持
- **CLI-Anything 66,011⭐**：daily +1,106（+1,074→+1,106，深析次日不降反升）；pushed 11-20 未变
- **app-store-compliance 6,748⭐**：+858/日（昨日 +850，二连高位）——「活数据库 + skill 市场 + 社媒」配方第四日持续放量；pushed 今日
- **autoclip 16,608⭐**：API delta +764/24h（+980→+764 降温），**今日掉出 daily 榜单**——按 univer 修正案预防性声明：单日掉榜不轻判趋势终结，观察一周；20k 线按当前节奏推迟至 ~11-30
- **ffmpeg-skill 11,311⭐**：weekly +3,048，pushed 今日——「本地能力技能化」样板持续周榜前段
- **open-code-review 56,482⭐**：weekly +2,259（daily 口径 +303 回落，但周口径强劲）——quickreview 系列基准故事持续给热度供血
- **opensre 15,657⭐**：+321/24h，f/s 0.130 稳，pushed 今日
- **生态双锚**：superpowers 327,007⭐（+811/24h）、firecrawl 210,472⭐（+1,013/24h）
- **大厂官方库 weekly 常态化**：stitch-skills 13,127⭐（周 +2,616）、modern-web-guidance-src 11,151⭐（周 +2,309）、chrome-devtools-mcp 59,424⭐（周 +1,203）、cursor/plugins（daily +416）、meta/astryx 33,237⭐（+251/日稳态）
- **plannotator 15,165⭐**：daily 口径 +170 续降温，weekly 口径 +1,764 仍前段——「agent 工作台」位的稳态消耗期

## 昨日观察清单回收

1. **univer「一周 4 版」阈值** → ✅ v1.6.2 11-25 落地，10 天 5 版达标，weekly 持续在榜（详见 #3）
2. **BugHunter 六连庄与降速拐点** → ⏸ 半回收：六连庄兑现但拐点未现（+1,652 再加速），判断改为等 weekly 衰减
3. **autoclip 20k 时间点** → 🔶 修正：掉出 daily + 增速降温，20k 推迟 ~11-30；掉榜本身暂不下结论（套用 univer 修正案）
4. **CLI-Anything 生态位验证** → ⏸ 热度持续（+1,106）但模仿者/互操作声明仍未出现，继续挂
5. **CodeReviewBench 扩散** → ⏸ 未查到新扩散证据，低频维持

## 明日观察清单

1. **nod 增长曲线**：weekly 占位能否升格 daily 常客；自托管 server 模式的 fork→部署转化；n8n 核心产品 ↔ nod 连接器互通落地进度；社区对 Haiku 8/240 安全数据的二创讨论
2. **autoclip 掉榜后一周窗口**：是否如 univer 模式快速回归（这次对自己的持仓判断也要防「单日掉榜=终结」的同款错）
3. **diagram-design 短视频供给周期**：教程流衰减时点与掉榜间隔（对照 9 月复燃的持续时长基线）
4. **BugHunter weekly 口径拐点**：改用周增衰减判断六连庄后的热度周期
5. **CLI-Anything**：harness 数量增长与 CLI-Hub 注册表模仿者（连续第三日挂单，若再无信号则降频为周观察）

---
*方法论备忘：trending 数字与 API 24h delta 存在窗口差，一律以 API 为准；「单日掉榜 ≠ 趋势终结」已从 univer 个案升级为对所有持仓项目的通用预防规则；fork 率 >0.15 的早期项目（nod 0.159）通常是「部署型工具」信号而非「消费型内容」信号，增长曲线形态预期应区别对待。*
