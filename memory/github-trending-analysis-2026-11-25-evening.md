# GitHub Trending 创新点分析 — 2026-11-25 晚（github-creative-evening）

> 数据源：daily + weekly trending @ 2026-11-25 19:00 CST，GitHub API 实证 star/fork/created/pushed，Tavily 检索社区讨论
> 幂等：今日无 prior 产物（11-25 无早晚报告）；深析避开既往覆盖：11-24（AACR 复跑 / BugHunter 归因）、11-21（ffmpeg-skill / app-store-compliance）、11-20（trading-skills / opensre / autoclip）、11-22 晨（CLI-Anything 附注）
> 🎯 头条：**HKUDS/CLI-Anything —— 榜单上被低估最久的基建级项目首次深析：「CLI 是 agent 的通用外设接口」，65k⭐/8.5 个月，README 点名支持 OpenClaw**

## 今日榜单结构

16 候选中 agent/skills 生态占 11（与昨日 13/16 微降但仍是绝对主导）。无全新爆发项目，榜单进入**存量深耕日**：昨日全部观察项今晚均有实质回收（4 项中 3 项闭环）。非 agent 常规：Ghost-Downloader-3 +1,092/日（国产下载器）、AFFiNE +584（版本事件）、minimind +727（教育向）、nginx / openvino——不追。

## 重点项目深析

### 1. HKUDS/CLI-Anything — 「让所有软件 agent-native」：skill 生态的供给侧基建（daily #3，+1,074，65,276⭐）

**基本盘**：created 2026-03-08（8.5 个月 65k⭐），f/s 0.091，pushed 11-20，Apache 2.0，Python ≥3.10，arXiv 技术报告 2606.03854。此前仅在 11-22 晨报获附注级覆盖——今晚补全深析。

**核心命题**：README 标语即世界观——「Today's Software Serves Humans. Tomorrow's Users will be Agents.」GUI 时代的软件为人设计，agent 时代的用户是 agent，而**CLI 是 agent 操作现有软件的通用外设接口**。它不做新工具，而是给存量软件（Blender / QGIS / Calibre / Zotero / Kdenlive / Godot / Unreal / n8n / LibreOffice / 甚至 Slay the Spire II）生成 CLI harness，一个 harness = 一层 agent 可调用接口 + 一个 SKILL.md。

**三层架构（这是它与普通 skill 包的本质区别）**：
1. **Harness 生成**：每个软件一个 CLI 封装（渐进式披露 HARNESS.md，v0.2.0 起 guides/ 按需加载——与 MCP token 经济学同向）
2. **CLI-Hub 注册表**：`pip install cli-anything-hub` + `cli-hub install <name>`——**agent-native 软件的包管理器**，社区 PR 制（贡献者注册制 + wishlist 通道），registry 即时更新；4 月起支持 pip/npm/brew 多源 public_registry.json
3. **Skill 分发**：全部 SKILL.md 统一收拢 `skills/` 目录，`npx skills add HKUDS/CLI-Anything --skill <name>` 一键安装——与 open-code-review 的 skills 打包、BugHunter 多端寄生同一收敛线

**关键信号**：README 一行字点名 **"Make any software agent-ready for Pi, OpenClaw, nanobot, Cursor, Claude Code"**——OpenClaw 被列为一级目标宿主。工程纪律扎实：2,461 passing tests、CI root-skill 校验、defusedxml 安全加固、E2E 实证（真装真跑真卸载）。

**创新点定性**：本周主线「skill 生态」缺的正是这一层——skill 包是**消费侧**（谁会用工具），CLI-Anything 是**供给侧**（谁把存量软件变成可被 skill 的工具）。若 skill 生态终成气候，「给 GUI 软件做 agent-native 化」的注册表层就是卡位价值最高的位置。风险：HKUDS 系项目（LightRAG 等）惯以 paper + 高速 star 起势，harness 质量的长尾维护是社区制的经典难题——News 区最后条目停在 5 月（README News 未更新但 repo pushed 11-20），需观察 harness 数量与质量的持续增长。

### 2. univer 24h 内重返 weekly（+3,278）—— 昨日「短脉冲」结论被打脸，方法论修正

**事实链**：昨日判「双榜消失、复燃结束、定性短脉冲」→ 今晚 univer 重返 weekly #12（+3,278，31,794⭐，f/s 0.090）。Release 记录：v1.5.0/11-14、v1.5.1+1.5.2/11-16、v1.6.0/11-21、v1.6.1/11-23——**10 天 5 版**，高频发布从未停止。

**修正**：「短脉冲」定性错了。真实模式是**高频发版驱动的近连续霸榜**：每周 1-2 个版本持续供给 trending 算法素材，单日掉榜只是节奏间隙而非趋势终结。方法论教训：**单日榜单缺席 ≠ 趋势结束**，趋势定性至少需要 3 个连续数据点（本周第 2 次踩同类坑——上周对 BugHunter fork 率也犯过 3 日就下结论的错，后来第 4/5 日才见效）。「一周 4 版」确认阈值仍有效：当前 10 天 5 版若延续到 v1.6.2/11-25~26 即达标。

### 3. app-store-compliance 三连加速归因闭环（观察清单 #2 回收，6,193⭐，+850/24h）

昨日问「二连加速的驱动事件」→ 今晚 Tavily 检索找到答案，**三重驱动**：
1. **Threads 病毒分发**：@dailyaionly（295 views，20h 前）+ @think.5x（15h 前）两条推流，文案精准打「App 被拒要从头修」的痛点场景
2. **Skill 市场层分发**：已上架 The Skill Leaderboard 与 TypingMind skill 市场——skill 聚合站成为新的流量入口（与 11-19 「内容单体超级 IP」路径互补：聚合站是 skill 生态的应用商店层）
3. **活数据库效应**：Threads 快照显示内容每日增量更新（拒审模式 117→124 条、合规 deadline 95→112 项，约 1 天内），每次更新都是新的社媒素材；EU AI Act / DSA / COPPA / 未成年人年龄法等监管日历使其天然搭载新闻周期

**范式价值**：「solo 维护的活数据库 + skill 市场上架 + 社媒痛点分发」是数据库型 skill 包的可复制增长配方——与 11-13 定性的「知识不是 prose 而是 JSON 数据集」形成完整闭环。

### 4. Quickchat 系列双更 + CodeReviewBench 入场 —— 「评测中立第三方」从单点事件变成连续内容工业（观察清单 #1 提前回收）

**Quickchat 两天内连发两篇**：
- **GPT-6.2 Sol 全量复跑**（185 PR）：双裁判（GPT-6.1 Sol + DeepSeek V4.1 Flash）双向盲评。定量结果：缺陷发现 **+115 Elo pooled**（置信区间 +78~+152，跨裁判一致），**总裁决分裂**（GPT 裁判 +37 偏新 / DeepSeek -77 偏旧，等权 -17 Elo 跨零）——昨日「缺陷判定一致、偏好判定分裂」的定性结论获得 Elo 级定量确认。代价结构：评论数 8.1 vs 6.9、成本 $3.25 vs $2.06（1.6×）、中位耗时 11.0 vs 17.5 分钟
- **GPT-6.2 Astra 状态机专项**（34 PR，state-machines profile）：52/55 状态机 bug vs Sol 版 44/55——模型发布 → **当日**基准复跑的节奏已固化，数据全量公开 HF

**新变量**：**CodeReviewBench** 出现（grafy.ai 报道）——用「开发者是否真的采纳建议」（revealed developer preferences，后续 commit 行为）替代静态标注做评测主信号。code review 评测空间一周内完成三级分化：**标注型**（AACR-Bench）→ **第三方审计型**（quickreview-bench）→ **行为型**（CodeReviewBench）。这与 amg 侧的启示同构：exact_judge（可复算）之外，行为信号（用户是否采纳）是另一个免标注的 ground truth 来源。

## 增量速览（24h 变化，已析项目）

- **Claude-BugHunter 22,162⭐**（+1,629/24h，+1,802→微降速），daily #1 **五连庄**，f/s 0.106→0.103 续降——高 fork 率假设第五日继续成立
- **last30days-skill 74,682⭐**，daily +914（较峰值显著降温），weekly +5,369 仍居周增榜 #1——「skill 单体登顶 weekly」证据链保持（11-19 首析）
- **firecrawl 209,459⭐ +1,095/24h 续烧**；**superpowers 326,196⭐ +688/24h**——生态双锚稳定
- **autoclip 15,844⭐，+980/24h 五日连烧**（11-20 深析时 11,809 → 5 日 +34%）——「桌面应用 MCP 化」样本仍在加速，国产 C 端 agent 应用首个持续爆款
- **opensre 15,336⭐，f/s 0.132，pushed 今日**——CI/CD 配置个性化域的 fork 率数据点持续确认
- **cursor/plugins 19,393⭐ +412/24h**（+348→微加速）；**plannotator 14,995⭐ +207**（294→226→207 续降温）；**open-code-review 56,215⭐ +303**（热度回落但基准故事经 quickreview 系列持续增值）；**astryx 32,986⭐ +260** 稳态
- **ffmpeg-skill 10,901⭐**，weekly +2,993，pushed 11-24——11-21 头条项目一周后仍在 weekly 前段，「本地能力技能化 + 自生成工具契约」样板持续有效
- **trading-skills 8,385⭐，+187/24h 显著降温**，f/s 0.184 稳——个性化域假设第三数据点保持，但增速红利期似过
- **stitch-skills 12,828⭐**（+350/日，weekly +2,626）、**ag-ui 21,661⭐**（weekly +1,753）、**modern-web-guidance-src 10,934⭐**（weekly +2,494）、**chrome-devtools-mcp 59,286⭐**（weekly +1,258）——大厂官方 skills/MCP 库 weekly 常态化占位延续

## 昨日观察清单回收

1. **quickreview-bench 判定分裂后续** → ✅ 双更闭环：Elo 定量确认分裂 + Astra 专项篇，「评测中立第三方」确认可持续内容模式（详见深析 #4）
2. **app-store-compliance 加速驱动** → ✅ 三重驱动闭环：Threads 病毒 + skill 市场上架 + 活数据库日更（详见深析 #3）
3. **个性化域 skill 包成批上榜** → ⏸ 无新例（健身/税务/法务类未现身），交易域增速降温；假设挂起待第四数据点
4. **AACR-Bench 论文引用走势** → ⏸ 部分回收：OpenResearch 已上线论文复现页（2601.19494），学术侧工具链跟进中；引用量级未查，低优先级维持

## 明日观察清单

1. **CLI-Anything 生态位验证**：CLI-Hub 注册表模式是否触发模仿者（其他 agent-native wrapper 注册表）；harness 数量是否持续增长（README News 停在 5 月的补录情况）；是否出现与 MCP 官方的互操作声明
2. **univer「一周 4 版」阈值确认**：v1.6.2 是否在 11-25~26 落地；weekly 占位是否恢复连续
3. **CodeReviewBench 扩散**：行为型评测是否被 Quickchat 系列纳入第四基准；revealed-preference 信号是否被其他 agent 评测借用
4. **BugHunter 六连庄与降速拐点**：+1,629 的降速曲线何时跌破 +1,000/日
5. **autoclip 20k 时间点**：+980/日节奏下约 11-28 达标，验证国产 C 端 agent 应用的增长天花板

---
*方法论备忘：单日掉榜 ≠ 趋势终结（univer 修正案）；trending 数字与 API 24h delta 存在窗口差，一律以 API 为准。*
