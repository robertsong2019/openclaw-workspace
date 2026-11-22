# GitHub Trending 创新点分析 — 2026-11-22 晚（github-creative-evening）

> 数据源：daily + weekly trending @ 2026-11-22 19:00 CST，GitHub API 实证 star/fork/created/pushed
> 幂等：今日无 prior 晚间产物；选题避开 11-21 晚（ffmpeg-skill / app-store-compliance）、11-22 晨（Claude-BugHunter / superpowers / CLI-Anything 附注）、11-20 晚（trading-skills / opensre / autoclip）、11-19 晚（last30days-skill / stitch-skills）、11-17（ag-ui / modern-web-guidance）、8 月（diagram-design）
> 🎯 头条：**backnotprop/plannotator +3,396/周登 weekly #1 —「Agent 决策收件箱」把 HITL 从协议理想做成产品，且显式支持 OpenClaw**

## 本周双主线收敛

①**HITL 基础设施自成一层**：ag-ui（协议，21k⭐）+ plannotator（产品，weekly #1）+ Herdr（终端 TUI）——「人审 agent 产出」从散落在各 harness 的 plan mode 变成独立可装配层，且 inbox 异步模式（agent 继续干活、人有空再回）是关键差异化。②**大厂 agent-ready 基建持续开源**：继 Google modern-web-guidance-src / stitch-skills 后，Meta 把内部 8 年、13k+ app 的设计系统以 agent-first 姿态开源（astryx，+3,967/周）——UI 代码生成的下一块拼图是「agent 可消费的设计系统」。

## 重点项目深析

### 1. backnotprop/plannotator — Agent 决策与反馈的收件箱层（14,268⭐，+3,396/周 weekly #1，created 2025-12，fork:star 0.099）
**是什么**：本地浏览器 review surface，覆盖 10 个 coding agent（Claude Code/Codex/Copilot CLI/Gemini CLI/OpenCode/Kiro/Droid/Amp/DeepSeek Harness/Pi）+ 4 个 personal assistant（**Grok Bot / Muse / Hermes / OpenClaw**）。通过 plugins/hooks/commands 直插 agent：agent 提出决策/计划/HTML 或完工时，浏览器自动打开标注页，人画批注、写评论，一键回传给 agent 执行。新版 **Plannotator Inbox** 是多 agent 工作的「缺失的 review 层」。

**创新点**：
- **Inbox = 人与 N 个 agent 的异步消息层**：agent 留下消息/提问/文件/guided review 后继续干活，人不被阻塞；回复作为「下一个 turn」精确路由回发起会话。这是 agent 时代的收件箱——把「审批」从同步阻塞（plan mode 卡住等待）重构为异步排队（像邮件），**多 agent 并行时人成为瓶颈的解法**。Claude Code/Pi/OpenCode 走原生插件，其余 agent 走 MCP（`plannotator inbox mcp`）；`--help` 文档按「agent 会读」来写——docs-as-prompt 再添一例。
- **三类工件统一标注面**：plan/spec/markdown 文档、渲染 HTML 与**本机 live site**（`plannotator annotate http://localhost:5173` 走本地代理，热更新不中断）、diff/PR review（支持 Git/GitButler/Jujutsu/Perforce/GitHub/GitLab）——一个 surface 吃下 agent 产出的全部形态。
- **Guided review：agent 预消化自己的 diff**：一键让 agent 把大 diff 分成章节，「改动核心在前、影响次之、胶水最后」，每章配 overview + 可标注 diff。**用 agent 降低人审 agent 的成本**，是 review 端的 token 经济学。
- **终端孪生 Herdr Annotate**：TUI 版标注 agent 回复/Markdown 文档，标注数据与 App 版共享目录——终端 review 与 GUI review 累积复合，而非两套孤岛。
- 与 11-21 ffmpeg-skill「Review page HITL（自产 HTML 审查页）」同哲学的平台化版本：ffmpeg-skill 是项目内即抛方案，plannotator 是跨 harness 常驻层——**垂直技能包的审查页与通用收件箱正在从两端逼近同一范式**。

**技术栈**：TypeScript，本地运行（plannotator.ai），集成路径三件套（plugins/hooks/commands + MCP fallback + agent-readable help）。

**与自有工作连接**：①**试装价值最高（本周新增）**——显式支持 OpenClaw，Inbox 可直接当 cron/heartbeat 流的 HITL 层（外部动作投递前人工审一道）；②「回复作为下一 turn 路由回原会话」对自家 sessions_send 编排是现成参考；③ag-ui（协议）vs plannotator（产品）的分工值得在「Agent 前端」主题 essay 里并置。

### 2. meta/astryx — Meta 8 年内部设计系统以 agent-first 姿态开源（31,991⭐，+3,967/周，created 2026-01，fork:star 0.078，pushed 就在抓取瞬间）
**是什么**：Meta 内部最大设计系统（服务 13,000+ app、8 年沉淀）开源版：150+ 无障碍组件、150+ 模板与 patterns、7 主题、CLI，React 19+ / StyleX。卖点是「fully customizable and agent ready」——这是**首个把 agent 当一等公民用户的大厂设计系统**。

**创新点**：
- **「人与 agent 同一套工具」作为架构原则**：API、文档、CLI 三者协同设计，「a person and an AI assistant build the same way, from the same reference」；作者的经验法则直白写在 Principles 里——**「Every change that made Astryx easier for AI made it easier for people too」**（对 AI 更容易 = 对人也更容易，反直觉但可复用的设计启发式）。
- **CLI 即 agent 文档面**：`astryx init` 问零问题、把 Astryx 指南直接写进 `AGENTS.md`/`CLAUDE.md`；`astryx docs global` 等命令让 agent 自助读文档而非翻网页——文档不是给人看的网页附录，而是 agent 的可执行引用。支持 project/global 双模式装 CLI，让「每台机器上所有 coding agent 都认识 Astryx」。
- **零锁定三层设计**：StyleX 对消费者不可见（用 className + Tailwind/CSS modules 覆写）；主题 = 纯 CSS custom properties（设计师改品牌不用 fork/包裹组件）；`swizzle` 把组件源码 eject 进项目归你所有。原则是「Guidance over enforcement」——给能力不给护栏对抗。
- **工程纪律可审计**：README 顶部 SYNC CONTRACT（架构变更必须同步文档）；Contributing wiki 含 API Conventions / Design Conventions / Component Lifecycle / **Blog Review Rubric（三个打分维度）**——把评审标准写成 rubric 而非口头传统；「Earned by measurement. We test conventions rather than assert them」+ internal/ 里的 vibe tests——**约定不靠主张靠测试**，与本周确定性护栏主线同频。
- 与 modern-web-guidance-src（知识供给流）、stitch-skills（技能库）并列成第三种大厂姿势：**「可被 agent 消费的 UI 基建」**。UI 代码生成质量的上限开始取决于设计系统是否 agent-native——这对「AI 前端拼凑感」是个结构性答案。

**技术栈**：TypeScript、React 19+、StyleX（源码构建插件可选，消费者零配置）、pnpm 11 / Node 22、Storybook + Sandbox 在线。

**与自有工作连接**：①「对 AI 更容易也对人更容易」原则适用于自家一切内部工具文档化；②AGENTS.md 写入的 init 模式可被 prompt-weaver / 项目脚手架借鉴；③如果做 agent 生成 UI 的实验（如 babylon-js-playground 延伸），astryx 是现成的 agent-friendly 组件层。

## 增量速览（已析项目动态 + 信号记录）

- **Claude-BugHunter 16,733⭐**（昨日 15,042，+1,691/日续烧，daily #1 连庄）——fork:star 0.113，显著高于 app-store-compliance 的 0.060：**red-team 技能包的用户参与深度（fork 率）高于合规数据库型 repo**，攻击性安全社区不只是围观。
- **firecrawl 206,536⭐ 回 daily**——描述已改写为「Knowledge infrastructure... Search, scrape and access **550+ data providers** through one API」：从爬虫工具向**数据聚合层**重新定位，one-API-for-550-providers 是新的整合叙事；知识基建赛道（抓取→清洗→供 agent）在向上游收编。
- **app-store-compliance 3,651⭐**（昨日 3,034，+617/日）+ fork 220——solo 数据库型 repo 低 fork 需求的判断再确认（0.060 vs 昨日 0.064，稳定）；拒审模式数 117→124、deadline 95→111，数据集仍在高频更新。
- **cursor/plugins 18,239⭐ +260/日**（昨日 +299/日）——增速略降但仍在放量；与 Agent Skills 标准的收敛/分叉继续观察。
- 非 agent：Ghost-Downloader-3 +779/日、AFFiNE +574/日（版本事件）、minimind（教育向）、HermesEnabler（Apple Watch 越狱向）、sure（Ruby 记账）——不追。

## 昨日观察清单回收

1. **ffmpeg-skill 12/42 按需披露被抄作业了吗** → 今晚无新实证；chrome-devtools `--slim` 仍是唯一同向先例，继续观察。
2. **app-store-compliance fork:star 低 fork 假设** → 0.060 再确认，solo 数据库型 repo 低 fork 需求成立。
3. **cursor/plugins vs Agent Skills 收敛** → 无新事件，继续挂。
4. **Claude-BugHunter 安全社区合规讨论** → 未检索到讨论（本报告未专门检索，存疑挂起）。

## 明日观察清单

1. plannotator Inbox 的 OpenClaw 集成深度（插件级还是 MCP only）——若成熟，评估接入自家 cron 投递流做 HITL 门禁
2. astryx Beta → stable 的节奏；`astryx docs` 命令式文档是否被其他设计系统（shadcn/radix）跟进
3. firecrawl「550+ providers one API」聚合叙事是否会挤压垂直抓取工具（如 last30days-skill 依赖的多源拼装）
4. Claude-BugHunter fork 率 0.113 是否持续高于同类——攻击性安全技能包的活跃度信号
