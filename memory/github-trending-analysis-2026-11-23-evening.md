# GitHub Trending 创新点分析 — 2026-11-23 晚（github-creative-evening）

> 数据源：daily + weekly trending @ 2026-11-23 19:00 CST，GitHub API 实证 star/fork/created/pushed
> 幂等：今日无 prior 晚间产物；选题避开 11-22 晚（plannotator 头条 / astryx 头条）、11-22 晨（Claude-BugHunter / superpowers / CLI-Anything）、11-21 晚（ffmpeg-skill / app-store-compliance）、11-20 晚（trading-skills / opensre / autoclip）、11-19（last30days-skill）、11-17（ag-ui / modern-web-guidance / stitch-skills）、9-10 月多次覆盖（univer）
> 🎯 头条：**alibaba/open-code-review 携 AACR-Bench 回归 weekly（+3,700/周，55,555⭐）——垂直 agent 开始用「自带基准 + 显式 trade-off 声明」自证，这是 skill 生态从堆料走向可验证的成熟信号**

## 本周主线：垂直 agent 的「评测化」转向

本周 trending 上 skill 包仍然扎堆（Claude-BugHunter +1,716/日、superpowers、CLI-Anything），但 open-code-review 的回归展示了另一条路：**不做更多 skill，而是给自己的垂直能力造基准**——50 仓库 / 200 真实 PR / 10 语言 / 80+ 工程师标注 1,505 个 ground-truth issue，发布在 HuggingFace（AACR-Bench）。这与罗嵩侧 amg 的 LongMemEval 纪律同构：**没有基准的 agent 主张只是 marketing，有基准的 trade-off 才是工程**。

## 重点项目深析

### 1. alibaba/open-code-review — 混合架构 Code Review 回归，这次带着基准（55,555⭐，4,615 forks，fork:star 0.083，created 2026-05，weekly +3,700，Go，Trendshift 周/月 Go 双榜）

**既往覆盖**：6-8 月已析「确定性工程 + LLM 混合架构优于纯 LLM」主线（2026-08-02 / 07-29 等报告）。**今晚增量是基准与 packaging**：

- **AACR-Bench 自证闭环**：50 个热门 OSS 仓库、200 条真实 PR、10 种语言，80+ 资深工程师交叉标注 1,505 个 ground-truth issue，数据集挂 HuggingFace（Alibaba-Aone/aacr-bench）。同底层模型对比 Claude Code：**Precision/F1 显著更高、token 消耗 ~1/9、速度更快**——并且主动声明 Recall 更低是「刻意的 precision-over-noise 取舍」。**垂直 agent 主动声明自己放弃了什么**，这在 trending 生态里极少见，是工程成熟度的标志。
- **「为什么纯 agent 不行」的病理学写进 README**：coverage 不全（大 changeset 时 agent 偷懒挑文件审）、position drift（行号漂移）、质量不稳（prompt 微小变动导致波动）——根因归结为「纯语言驱动架构对审查流程缺乏硬约束」。这是 6-8 月「混合架构」论的 README 级展开，可直接当论证素材。
- **分工边界清晰**：确定性侧管「不能错的」——精确文件选择、关联文件捆绑（如 i18n 中英文件捆成一个 review unit）、模板引擎级规则匹配、独立的定位与反思模块；agent 侧管「动态的」——场景调优 prompt + **从生产环境工具调用 trace 蒸馏出的专用 toolset**（分析调用频率分布/重复率后裁剪，比通用工具集更稳）。「从 trace 蒸馏 toolset」是个可迁移的做法。
- **分发方式升级为 Agent Skills**：`ocr` CLI + skills 可装进 Claude Code / Codex / Cursor / Kimi Code——垂直工具不再自带 UI，而是寄生到通用 agent 里，与 Agent Skills 标准收敛趋势同频。
- OpenSSF Gold Best Practices、DeepWiki 接入、8 语言 README——大厂开源工程纪律的样板。

**技术栈**：Go CLI（npm 包分发 @alibaba-group/open-code-review），Git >= 2.41 依赖，子 agent 隔离上下文并发审查。

**与自有工作连接**：①「垂直能力 + 自建基准 + 显式 trade-off」三件套是 amg/prompt-mgr 可直接复用的发布打法；②「从调用 trace 蒸馏专用 toolset」可反哺自家 agent 工具面裁剪；③若做 code review 类任务，`ocr scan`（全文件审计陌生代码库）模式值得一试。

### 2. dream-num/univer — v1.6.0 感恩节版本驱动的复燃（31,370⭐，+6,436/周 = 本周全榜最高增量，v1.6.0 @ 11-21「🦃」+ v1.6.1 @ 今日）

9-10 月及 11-16/17 晚已多次覆盖（AI Office SDK、「connect your application or agent」定位）。本次**纯版本事件复燃**，不重复展开，只记两个新信号：①README 目录新增「CLI, agent integrations, and developer skills」章节——agent 集成面从 API 层上浮到 CLI/skills 层，与 open-code-review 同一道收敛；②两天连发两版（v1.6.0/v1.6.1），高频发布节奏本身是复燃的燃料。「AI Office」赛道 univer（SDK）vs AFFiNE（应用）的分工继续清晰。

## 增量速览（已析项目动态 + 信号记录）

- **Claude-BugHunter 18,731⭐**（昨日 16,733，+1,998/24h 提速，daily #1 三连庄），fork:star 0.109（昨日 0.113）——**red-team 技能包高 fork 率假设连续两日成立**（>2 倍于 app-store-compliance 的 0.063）；攻击性安全社区参与深度是真实需求信号。
- **plannotator 14,562⭐**（昨日 14,268，+294/24h；weekly 显示 +2,815），pushed 就在抓取瞬间——README L42 确认 **Plannotator Inbox 显式支持 OpenClaw**（与 Grok Bot / Muse / Hermes 并列）。昨日观察项 #1 回收：支持是 inbox 级（README 无更深的 OpenClaw 原生插件线索），接入自家 cron 投递流做 HITL 门禁仍可行，优先级维持「试装价值最高」。
- **app-store-compliance 4,404⭐**（昨日 3,651，+753/24h 提速），fork:star 0.063 稳定——solo 数据库型 repo 低 fork 需求第三次确认；拒审模式 124 条（README 实证，昨日 124→持续更新中）。
- **firecrawl +915/日** 续烧——「550+ data providers one API」聚合叙事（昨日析）持续放量，无新事件。
- **cursor/plugins 18,633⭐**（+394/24h，增速与 astryx 同档），pushed 11-22——与 Agent Skills 标准收敛/分叉继续观察。
- **astryx 32,385⭐**（昨日 31,991，+394/24h 稳态）——无 stable 发布新信号，观察项挂起。
- **last30days-skill weekly +4,731**（11-19 析）——多源研究 skill 持续放量，是「skill 单体也能进 weekly 前五」的证据。
- 非 agent：nginx / openvino（基础设施常规上榜）、minimind（教育向）、sure / AFFiNE / Ghost-Downloader-3（既往已记）——不追。

## 昨日观察清单回收

1. **plannotator OpenClaw 集成深度** → README 确认 inbox 级支持，无原生插件证据；结论：可作为 HITL 收件箱试用，不必等更深集成。✅
2. **astryx stable 节奏 / docs 命令被跟进** → 无新事件，继续挂。
3. **firecrawl 聚合叙事挤压垂直抓取** → 无新事件，继续挂。
4. **Claude-BugHunter fork 率持续性** → 0.109 连续两日 >0.10，假设成立（攻击性安全技能包参与深度显著更高）。✅

## 明日观察清单

1. AACR-Bench 是否被第三方复跑（HuggingFace 数据集可下载）——若有独立复现，「自带基准」打法获得外部背书的路径就通了
2. open-code-review 的 Agent Skills 打包是否带动其他垂直工具跟进（与 cursor/plugins 收敛线交汇）
3. univer v1.6.x 高频发布是否持续（两天两版 → 若一周 >4 版则确认发布驱动复燃模式）
4. Claude-BugHunter 提速（+1,998/24h）是否与安全事件/讨论相关——首次值得专门检索一次社区讨论
