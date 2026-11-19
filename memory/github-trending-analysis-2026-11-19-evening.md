# GitHub Trending 创新点分析 — 2026-11-19 晚（github-creative-evening）

> 数据源：daily + weekly trending @ 2026-11-19 19:00 CST，GitHub API 实证 star/fork/created/pushed
> 幂等：今日无 prior 晚间产物；选题避开今晨 deep（paper-orchestra/SkillEvaluator/BugHunter）、11-18 晚 Agent-First 基建周（astryx/MWG/agent-browser/CLI-Anything/cursor-plugins/codex-security）、11-17 skills 生态、11-14 plannotator、11-15/16 open-code-review、11-04 superpowers/ECC
> 🎯 头条：**mvanhorn/last30days-skill 70.5k⭐ — 技能品类第一个"纯内容单体"超级 IP，topics 自带 openclaw/clawhub，从未析过**

## 🏆 主线：技能价值曲线从"框架平台"下沉到"内容单体"

盘点技能品类各层的量级（GitHub API 实证）：

| 层 | 代表 | 星数 | 首析 |
|----|------|------|------|
| 框架/平台层 | obra/superpowers | **321,616** | 11-04（312K 四厂收编） |
| harness 优化层 | affaan-m/ECC | **306,895** | 11-04 |
| 官方集合层 | anthropics/skills | 187K | 11-04 |
| 质量门禁层 | NVIDIA/SkillEvaluator | 3,989（+312/日 连续两天 daily） | 11-17 晨 |
| 分发层 | Claude-BugHunter | — | 11-19 晨 |
| 大厂供给层 | GoogleChrome/MWG、google-labs-code/stitch-skills | 8,978 / **10,554** | 11-18 晚 / **今晚新增** |
| **内容单体层** | **mvanhorn/last30days-skill** | **70,460（+1,059/日，今日榜 #1 徽章）** | **今晚头条** |

框架们 300k+ 早不新鲜，但**单体内容技能长到 70k 是新品类事件**：它不是 SDK、不是框架，就是一个 SKILL.md + 管线脚本。类比 App Store 时代单款 App 破亿下载——平台成熟后，内容创作者（而非平台工程师）也能做出超级 IP。叠加今晨的分发（BugHunter 矩阵）与质量（SkillEvaluator 门禁），生态四层齐活，这是技能品类成熟度的完整拼图。

## 重点项目深析

### 1. mvanhorn/last30days-skill — 单体技能超级 IP（70,460⭐，+1,059/日，+2,423/周）
**是什么**：`/last30days <任何主题>`——agent 主导的搜索引擎，跨 Reddit/X/YouTube/TikTok/HN/Polymarket/GitHub 等 30+ 源并行检索近 30 天内容，按真实用户参与度（upvotes/likes/真金赔率）打分，再由 agent judge 综合成一份 brief。v4 管线，spec 存于 `skills/last30days/SKILL.md`（运行时技能规范 = single source of truth）。Python。Created 2026-01-23，pushed 今日。

**创新点**：
- **"搜索人，不是编辑"（social relevancy, not SEO relevancy）**：Google 聚合的是编辑/SEO 内容；这里排名信号是 Reddit 1500 upvotes、TikTok 3.6M 播放、Polymarket $66K 真金赔率——用真金白银和集体注意力投票取代 Pagerank。
- **桥接孤岛是 unlock，不是"更好的搜索引擎"**：README 原话——"no single AI has access to all of it"（ChatGPT 有 Reddit 没 X，Gemini 有 YouTube 没 Reddit，Claude 都没有）。BYOK：自带 key + 浏览器会话，让 agent 并行搜全平台、互相打分。**定位是基础设施补位：把围墙花园间的缝隙变成产品。**
- **30+ 源的分层启用设计**：免费无 key（Reddit/HN/arXiv/GitHub/专利）→ setup wizard 30 秒解锁（X/YouTube/TikTok）→ 工具在 PATH 即自动启用（digg-pp-cli/arxiv-pp-cli/techmeme-pp-cli）→ 显式 opt-in（小红书/Amazon/Trustpilot）。渐进式披露，零配置起步。
- **Secret Signals（OSINT 式企业情报，最值得偷师）**：Jobs Page Secret Signal——从公司招聘 JD 里推断未发布产品（"a director role testing whether requests trigger transactions…reads like quality control for an assistant that completes purchases"）；Patent Secret Signal——只标记"不合该公司性格"或"描述了未发布之物"的专利申请。把公开但无人交叉的数据源变成情报。
- **Discovery mode**：问 "what's exploding in AI agents?" 时切换——扫 Reddit 类目/HN front page/Digg/X 生成提名，**agent 当评委**做名字/垃圾/内容价值过滤，输出 5-10 个 velocity-ranked 话题 + momentum 标签 + 一键 follow-up 命令。
- **分发矩阵**：Claude Code marketplace 插件自动更新 + `npx skills add`（50+ hosts）+ OpenClaw/clawhub 原生（topics 实证）。README 里对比工具示例直接 live 拉 GitHub API 星数（"not stale blog posts"）。

**技术栈**：Python 脚本 + SKILL.md spec + 各源 CLI 工具（*-pp-cli 模式）+ 浏览器会话。无自建后端——纯技能形态。

**与自有工作连接**：我的 trending/research cron 管线（tavily 多源→分析→报告）与它同构但源更窄。三点可偷师：①多源并行+交叉参与度打分；②discovery mode 的 agent-as-judge 提名过滤；③**Secret Signals 的 JD/专利异常推断——这是对 trending cron 的真增量**（给项目情报加"招聘信号/专利信号"维度）。可直接 `npx skills add mvanhorn/last30days-skill -g` 装进 OpenClaw 实测。

### 2. google-labs-code/stitch-skills — Google 官方第二技能仓（10,554⭐，+365/日，+1,567/周）
**是什么**：Google Labs 为 Stitch（AI UI 设计工具）发布的 Agent Skills 库 + 插件，遵循 agentskills.io 开放标准，兼容 Codex/Antigravity/Gemini CLI/Claude Code/Cursor/OpenCode。TypeScript。Created 2026-01-16。

**创新点**：
- **继 MWG 之后 Google 官方第二仓**，坐实"大厂供给层"是持续策略而非一次性公关。MWG 供给平台知识，stitch-skills 供给设计工具操作技能——Google 在把自家产品面全部 skills 化。
- **MCP + Skills 双通道**：Stitch MCP server（工具调用）+ skills（操作方法论）配套交付——工具给原子能力，技能给工作流知识，组合形态值得仿效（对比自家 doc/smartsheet MCP）。
- **三插件包分层**：stitch-design（设计）/ stitch-build（构建组件）/ stitch-utilities，Codex marketplace sparse-checkout 按需取。
- **兼容性碎片化仍存**：README 专门写 OpenCode 需要 kebab-case 重命名 `stitch::…` 命名、忽略 allowed-tools frontmatter——与 11-17 BugHunter manifest 标准化互证：跨 harness 兼容层是生态当前的脏活与机会。

### 3. appwrite — desc 重写信号：BaaS 老牌改口径为"agent 云"（58,378⭐，+232/日）
Desc 现为 **"The open-source cloud for agents & devs"**（原"Your Complete Backend"）。Auth/DB/Storage/Functions/Hosting/Realtime/WAF 全家桶不变，但**把 agents 排在 devs 前面**——老牌云厂商的 agent 叙事改口径，与 astryx/univer 的"人机共享接口"同一潮流：现有基础设施不重写，只重写自我描述。记录为叙事信号，无需深析。

## 增量速览（已析项目的今日动态）

- **paper-orchestra** +1,524/日 daily #2（今晨深析，持续验证）
- **cursor/plugins** +314/日——六信号之一连续多日在榜
- **ECC** 306,895⭐ + **superpowers** 321,616⭐ 双双回 daily——框架层热度未退
- **getarcaneapp/arcane** +547/日——维持 11-18 判断：纯 Docker 管理（Go+SvelteKit），非 agent-native，self-host 社区爆款，不追
- **jiangshan-map** 8,368⭐ +218/日——非 AI 亮点：中国历史交互地图（198 领土快照/诗词路线），Claude 协作开发的 viral 样本
- **daily_stock_analysis** 73,444⭐——fork:star=0.79 依旧（57.9k fork），通胀标注维持
- Weekly 榜固有面孔（astryx +6.2k/MWG +7.2k/univer +6.8k/agent-browser/codex-security/plannotator/ag-ui/open-code-review/chrome-devtools-mcp）均为已析项目稳态续烧，无新信息

## 📌 落地建议（按优先级）

1. **last30days-skill 试装**（`npx skills add mvanhorn/last30days-skill -g`，OpenClaw 原生）→ 跑一个已知主题对比自建 cron 管线质量；重点评估 discovery mode 与 Secret Signals 能否并入 trending cron
2. stitch-skills 只观察：Google 技能供给节奏的下一仓是什么
3. 技能四层拼图（框架/门禁/分发/单体）可作为 essay 系列下一篇候选——「单体技能的超级 IP 时刻」

> 值得告知罗嵩：last30days-skill（可直装试用 + 管线可偷师三点）；其余为记录性增量。
