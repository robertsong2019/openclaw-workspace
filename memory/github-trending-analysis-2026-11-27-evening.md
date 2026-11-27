# GitHub Trending 创新点分析 — 2026-11-27 晚（github-creative-evening）

> 数据源：daily + weekly trending @ 2026-11-27 19:00 CST，GitHub API 实证 star/fork/created/pushed，Tavily + README 实证背景
> 幂等：今日无 evening 产物（11-27 仅 08:00 晨报深析 superpowers / CLI-Anything / BugHunter 附注）；晚间选题避开晨报已析项
> 🎯 头条：**obsidianmd/obsidian-skills ——「app-skill」品类的官方天花板样板：应用厂商不教 agent 一门知识，而是教 agent 操作自己的软件**（54,172⭐，weekly +704，首次进入本系列深析视野）

## 今日榜单结构

双榜扫过 29 项（daily 16 + weekly 15，去重后），agent/skills 生态占约 23。榜单主旋律：**无一夜爆红，存量项目全部续更；唯一结构性新意是 obsidian-skills 进入 weekly 前 15——一个早已 54k⭐ 的官方库以「稳态期占位」姿态入榜，与 weekly 榜近期被大厂官方库（stitch/modern-web/astryx/chrome-devtools-mcp/ag-ui）常态占据的趋势合流**。daily 前列：BugHunter +1,597（七连庄但首现降温）、firecrawl +1,046、diagram-design +955（回归第二日）、Ghost-Downloader-3 +889、superpowers +854。**autoclip +774 次日回归 daily**（详见深析 #2）。非 agent 常规：minimind +702、nginx、openvino、sure、HermesEnabler——不追。

## 重点项目深析

### 1. obsidianmd/obsidian-skills — 应用厂商的 agent-native 接口声明（54,172⭐，weekly +704，f/s 0.071）

**基本盘**：Obsidian 官方仓库，created 2026-01-02（11 个月），Shell，pushed 11-26。增长史：2026 年 6 月病毒式爆发（Medium 作者实测数小时内 22k→36k），此后进入稳态供给期——周增仅 ~700，这解释了它为何从未进过 daily top 15、也从未被本系列覆盖：**它不是热度事件，是基础设施，本周入 weekly 是「官方库常态化占位」趋势的又一个数据点而非新爆发**。

**它是什么**：六个技能，全部围绕「让 agent 正确操作 Obsidian」：
- **文件格式三件套**：obsidian-markdown（Obsidian Flavored Markdown：wikilinks/embeds/callouts/properties）、obsidian-bases（.base 视图/过滤/公式）、json-canvas（.canvas 节点/边/分组）——把私有格式语法写成 agent 可执行的规范
- **obsidian-cli**：通过官方 CLI 驱动**运行中的** Obsidian 实例（搜索/读写/插件与主题开发）——agent 从「写文件」升级到「操作软件」
- **obsidian-headless**：无桌面应用同步/发布 vault——agent-native 的发布管线
- **defuddle**：网页→干净 markdown 提取，显式以省 token 为卖点

**创新点定性**：Medium 一篇评论给出了准确框架——**domain skill 与 app skill 的品类分野**。榜单上绝大多数技能包（BugHunter 红队、trading-skills 交易、diagram-design 图表）教 agent 一门知识；obsidian-skills 教 agent 操作一个已有软件。这不是同类竞品，是技能生态的第二大类。作为官方样板它的三个工程决策都值得抄：
1. **分发矩阵做到极限**：Claude/ChatGPT/Cursor/Grok Bot/Hermes/Kiro/Muse/Dots 七个官方插件市场直装 + `npx skills add` 通用安装器 + Gemini CLI 走 release archive（README 专门交代「release 只准挂一个文件，否则 Gemini 回退到源码归档」——多宿主分发的边角经验写进了维护文档）。11-26 diagram-design 条目观察到「多宿主兼容写进产品默认值」，obsidian-skills 是这件事的官方级完全体。
2. **省 token 是一等公民**：defuddle 独立成技能、README 通篇围绕「哪个宿主怎么装」而非「技能多厉害」——分发成本被当作产品核心工程问题对待。
3. **f/s 0.071 的分型意义**：与 app-store-compliance（0.064）同桶——**官方插件市场分发型 repo 天然低 fork**（用户装插件而非 fork 定制），与个性化域（trading-skills 0.181）、部署型（nod 0.151/autoclip 0.140）三分而立。fork 率分型法拿到第四个干净数据点。

**对本工作台的直接参照**：OpenClaw 的 MEMORY.md/memory/*.md 本质就是 markdown vault + agent 原生格式——obsidian-skills 演示的正是「厂商为自家格式写 agent 规范」这件事的完成态，可用作 workspace 格式规范化的对照样板；defuddle 思路（网页→干净 md）可直接借用于日报抓取链。

### 2. autoclip 次日回归 daily —— 「单日掉榜≠趋势终结」预防规则 24 小时内兑现（17,332⭐，daily +774）

昨日 autoclip 掉出 daily，按 univer 修正案做了预防性声明「观察一周不轻判」——**今天它以 +774 回归 daily**，规则首次即兑现。API 口径 +724/24h（+764→+724 微降温），20k 线还差 2,668，按 ~730/日节奏 **~12-01 到达**，与昨日推迟后的预测一致。方法论上这是「修正案防误判」的第二个实证（第一个是 univer 本身）：单日榜口径噪声大，API delta + 一周窗口才是判断单位。

### 3. BugHunter 七连庄但首现降温；双榜口径异常实锤（25,287⭐，daily +1,597）

- **增速拐点首次出现**：+1,652→+1,597（-3.3%），六连加速后第一次降温。幅度尚不足以判趋势，但昨日「等 weekly 口径衰减」的改判拿到了第一个支撑数据点。
- **weekly 榜双日缺席**：daily 七连庄（周增按日累加 ≈ 1.6k×7 > 11k）却连续两天不在 weekly top 15——本周 weekly #1 才 +5,090。结论：**GitHub trending 的 daily/weekly 不是同一增益口径的两张排行，weekly 更像「本周新近爆发」分桶**（附带解释了 nod、autoclip 昨日的 weekly/daily 各自缺席）。方法论备忘升级：**双榜各记各的，不做跨榜换算**。

## 增量速览（24h API delta，已析项目）

- **nod 4,147⭐**：+432/24h（增速放大），weekly +1,008→+1,165，f/s 0.151 仍顶档，pushed 今日——昨日头条项目第 2 日爬坡，daily 入场未发生但 API 曲线健康
- **last30days-skill 76,071⭐**：daily +759 + weekly +5,090，**weekly #1 第九日**（+5,302→+5,090 缓降温）——skill 单体超级 IP 的长尾仍在
- **trading-skills 8,661⭐**：+276/24h（+187 微回升），weekly +1,381，f/s 0.181 稳——个性化域假设第三数据点保持
- **ffmpeg-skill 11,712⭐**：weekly +3,048→+3,229 续升，pushed 今日——「本地能力技能化 + 工具契约」样板周榜前段
- **meta/astryx 33,448⭐**：+211/24h（+251 微降温），weekly +2,519 稳——agent-ready 设计系统的官方供给位
- **univer 32,018⭐**：API 仅 +107/24h vs weekly 口径 +1,825——**周增量明显前置**，「一周 4 版」高频发版模式进入消耗期，拐点两连将至
- **plannotator 15,342⭐**：+177/24h，weekly #1 +1,631——「agent 决策收件箱」稳态占位
- **stitch-skills 13,433⭐**：首次 daily/weekly 双榜同框（daily +309 / weekly #2 +2,619）——Google 官方技能库从 weekly 常客升格双榜
- **CLI-Anything 66,664⭐**：daily +746（+1,106→+746 明显降温），pushed 仍 11-20——连续第 4 日无模仿者/互操作信号，按既定规则**降频为周观察**
- **diagram-design 74,185⭐**：+720/24h，daily +955（回归第二日，教程供给延续）
- **app-store-compliance 7,278⭐**：+530/24h（+858→+562 降温），配方放量第五日
- **opensre 15,978⭐**：+321/24h 持平，f/s 0.131，pushed 今日
- **生态双锚**：superpowers 327,871⭐（+864/24h）、firecrawl 211,268⭐（+796/24h，daily +1,046）
- **大厂官方库 weekly 常态化**：modern-web-guidance-src +2,209、open-code-review +2,284（56,778⭐）、chrome-devtools-mcp +1,175（59,564⭐）、ag-ui +1,269（21,895⭐，+1,753→降温）、cursor/plugins daily +270

## 昨日观察清单回收

1. **nod 增长曲线** → ⏸ 半回收：API 增速 +432/24h 放大、weekly 续升，但 daily 入场未发生；n8n↔nod 互通与 Haiku 安全数据二创均无信号，续挂
2. **autoclip 一周窗口** → ✅ **次日即回归 daily**（+774），预防规则当日兑现；20k 维持 ~12-01（详见深析 #2）
3. **diagram-design 供给周期** → ⏸ 第二日 +955 仍在榜，短视频教程流未见衰减迹象，对照 9 月基线继续观察
4. **BugHunter weekly 口径拐点** → 🔶 半回收：daily 首现降温（-3.3%）；同时发现 weekly 双日缺席实锤双榜口径分桶（详见深析 #3），改用「API delta 连续三日 < +1,000」作拐点判据
5. **CLI-Anything 生态位验证** → ✅ 按规则执行：连续第四日无信号，降频为周观察（下周同一时间查一次）

## 明日观察清单

1. **obsidian-skills 持续性**：weekly 占位能否带动第二波「app-skill 品类」官方库上榜（Notion/Linear/1Password 类厂商跟进即是品类确认信号）
2. **autoclip 20k 线**：~12-01 预测第一检验日
3. **univer 拐点确认**：API +107/24h 已两连低，若第三日 < +150 即确认「高频发版模式」进入间歇期
4. **BugHunter 降温延续性**：+1,597 之后是否 < +1,500；daily #1 七连庄守卫战
5. **nod daily 入场**：API 曲线健康但双榜均未入场 daily，观察本周内是否升格

---
*方法论备忘：①trending 双榜是不同分桶算法，不做跨榜换算（BugHunter 双日缺席实锤）；②单日掉榜≠终结规则第二次实证（autoclip 次日回归）；③fork 率分型法第四数据点：官方插件分发型 ≈0.06-0.07 / 部署型 0.14-0.15 / 个性化域 0.18+；④「好得可疑」的增长先查分桶口径——weekly +1,825 与 API +107/24h 可以同时为真（univer，周增量前置）。*
