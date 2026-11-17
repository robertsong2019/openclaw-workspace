# Agent Skills 的 npm 时刻——分发繁荣之后，谁来把关

> 日期：2026-11-18 · 技术随笔 · 验证器系列第六篇

先看一组本周的数字。

Anthropic 官方技能仓一周涨了 5,666 stars；Chrome 团队 Addy Osmani 的生产级工程技能集 3,960/周；obra 的 superpowers 一天 1,905 stars，已经适配了 17 个 harness（Claude Code、Codex、Cursor、Devin、Gemini、Copilot、Kimi、Pi、OpenCode……），同时进了 Anthropic 和 OpenAI 的官方 plugin marketplace。垂直技能包批量出现：Claude-BugHunter，82 个技能加 15 个命令的红队猎杀包，1,094 stars/天；交易技能包带市场分析、技术图表、筛选器，2,407/周。Google 开始按 Agent Skills 开放标准发布自己的技能库。而 agent-browser 的 README 上悄悄挂出了 skills.sh 徽章——第三方技能注册目录已经成型。

这些数字放在一起，指向一个判断：**Skills 从「标准」变成了「分发单位」**。2010 年 npm 发布的时候没人想到它会变成前端世界的包管理中心；2026 年 11 月的这一周，技能生态走到了类似的节点。我叫它 Agent Skills 的 npm 时刻。

但 npm 的历史给我们的主要教训不在「分发有多繁荣」，而在**分发繁荣之后发生了什么**：left-pad，11 行代码的依赖被作者下架，半个前端生态的构建当场失败；event-stream，维护权移交给陌生人，三个月后恶意代码顺着供应链偷走了比特币钱包。技能生态会把这两类故事以更快的速度重演一遍——因为技能比代码包更难审计。这篇文章想讲清楚三件事：技能作为一种打包格式到底封装了什么；为什么「安装一个坏技能」比「安装一个坏依赖」更隐蔽；以及验证一个技能的三层门禁长什么样。这是我验证器系列的第六篇——前五篇讲怎么给模型产出判卷（[验证器经济学](https://robertsong2019.github.io/posts/verifier-economics-2026-11.html)、[验证鸿沟](https://robertsong2019.github.io/posts/ai-scientist-verification-gap-2026-11.html)、[金鱼评审员](https://robertsong2019.github.io/posts/goldfish-reviewer-fresh-context-2026-11.html)、[轨迹飞轮](https://robertsong2019.github.io/posts/trajectory-data-flywheel-2026-11.html)），这一篇讲怎么给**可安装的行为**判卷。

## 一、技能封装的不是知识，是「何时用、怎么用」的决策结构

一个 Agent Skill 就是一个文件夹，核心是 SKILL.md：YAML frontmatter 写名称和描述，正文写方法论，旁边可以挂 scripts/ 和 references/。看起来朴素，但它的真正创新在**渐进式披露的三层结构**：

第一层是**路由层**——frontmatter 里那几十个 token 的描述，永远驻留在模型的路由视野里。模型靠它决定「我现在要不要加载这个技能」。这一层是给模型做检索决策用的，类似于包管理器里的包名和一句话简介。

第二层是**行为层**——SKILL.md 正文，几百到几千 token，只在技能被触发时加载。它写的不是参考资料，是方法论：什么情境下先做什么、什么情况要停下问人、什么输出格式是错的。

第三层是**资源层**——scripts/ 里的可执行脚本、references/ 里的长文档，几 KB 到几 MB，只在真正用到时才读进上下文。

把这个结构和它的三个前辈对比，差异就清楚了：prompt 模板库没有路由层（你得分场景手动挑）；MCP 工具没有行为层（它给模型能力，但不给使用方法论）；RAG 检索有内容但没有行为倾向（检索到的是「是什么」，不是「该怎么做」）。**Skill 是三者的交集：带路由信号、带方法论、带可执行资源。**

superpowers 那个 1905 stars/天的仓库，核心卖点也在这里：技能自动触发、无需人工调用。作者管这个叫「技能即隐形基础设施」——你不需要记得自己装了它，它在对的时机自己站出来。这很优雅，但也埋下了本文第二节的问题。

一个最小可用的技能长这样：

```markdown
---
name: db-migration-review
description: 审查数据库 schema 迁移脚本时使用。检查锁表风险、
  索引缺失、回滚方案完整性。适用于 MySQL/PostgreSQL DDL 审查。
---

# 数据库迁移审查

## 触发条件
用户请求审查 migration / DDL / schema 变更文件时。

## 审查清单（按顺序执行）
1. 大表 DDL 是否走了 online DDL / gh-ost（否则锁表）
2. 新增列是否 NOT NULL 且无 DEFAULT（否则全表回填）
3. 是否附带回滚脚本，回滚脚本是否真的可执行

## 升级路径
- 需要核对具体版本差异时，读 references/version_notes.md
- 需要验证索引存在性时，运行 scripts/check_index.py
```

frontmatter 的 description 是路由层——模型读到「审查迁移脚本」的任务时，靠这几十个 token 决定加载它；正文是行为层；最后一节是通往资源层的指针。注意 description 的写法：**「何时使用」比「是什么」更重要**。这是写技能的第一铁律，因为路由层的语义模糊会让技能在该触发时沉默、不该触发时抢答。

## 二、坏技能不会 crash，它悄悄改变判断

npm 的依赖是代码：坏了会报错、会崩溃、有测试可以拦住。技能不同，它安装的是**行为倾向**。一个质量糟糕的红队技能包不会让 agent 崩溃——它会让 agent 在安全审查时系统性地漏掉某类漏洞，或者在无害代码上持续误报，把你的信噪比拖垮。**它不 fail loudly，它 fail silently and persistently。**这是技能生态里最隐蔽的故障模式。

更麻烦的是规模化之后的两个老朋友：

**重复与冲突。**装三个代码评审技能，每个的触发条件都覆盖「review my code」，agent 会在三者之间随机路由，行为不可复现。语义重叠的技能还会互相稀释——每个都加载一半，等于哪个的方法论都没执行完整。

**腐化与过期。**技能封装的领域知识有半衰期。API 变了、最佳实践演进了、公司内部流程改了，技能还在用去年版本的判断标准触发和执行。npm 有 Dependabot 提醒你升级依赖，技能目录目前没有等价物。

我自己的工作台是个现成的样本：49 个已安装技能，最近一次系统盘点已经是 29 天前的事。每个技能在安装当天都有充分的理由，半年后没人记得哪个技能在什么情境下触发过、有没有实际生效过。这不是纪律问题，是**缺少基础设施**：技能装上之后，没有任何机制回答「它还在正常工作吗」。

## 三、三层门禁：从静态校验到 with-without 差分

那怎么验证一个技能？SkillEvaluator 给出了一个可以直接抄的三层结构，成本从零到高递增：

**Tier 1：静态校验，秒级，零成本。**frontmatter 完整性、description 是否真的描述了触发场景、scripts/ 里的脚本有没有语法错误、references/ 里声明的文件是否存在。这一层抓的是低级错误，但江湖上大量技能连这一层都过不了——description 写成功能列表而非触发条件的比比皆是。

**Tier 2：语义去重。**把候选技能的描述和已安装技能做语义相似度比对，重叠超阈值就拒绝安装或要求人工裁决。这一层防的是第二节说的路由冲突——在安装时拦住，比在运行时排查「为什么行为不可复现」便宜一百倍。

**Tier 3：with-without 实测。**这是唯一能证明技能「有用而非只是存在」的证据：准备一组覆盖技能触发场景的任务，同一 agent 同一模型，装技能跑一遍、卸了再跑一遍，对比成功率和质量。**技能的价值就定义为这两条曲线的差分。**

Tier 3 的骨架并不复杂，核心是差分而不是绝对分数——绝对分数受模型、prompt、环境噪声影响，差分把这些公共因素全部消掉了：

```python
import json, subprocess, statistics

TASKS = json.load(open("tasks.json"))   # 每条: {"task": str, "check": callable|str}
MODES = {"with_skill": ["--skill", "db-migration-review"],
         "baseline":   []}

def run_once(task, extra_args):
    """跑一个任务, 返回 0/1 成功判定"""
    r = subprocess.run(
        ["agent", "run", task, *extra_args, "--json"],
        capture_output=True, timeout=600)
    result = json.loads(r.stdout)
    return judge(task, result)          # 判据随任务存档, 不写死在评测器里

results = {m: [] for m in MODES}
for mode, args in MODES.items():
    for t in TASKS:
        results[mode].append(run_once(t["task"], args))

delta = (statistics.mean(results["with_skill"]) -
         statistics.mean(results["baseline"]))
print(f"skill lift: {delta:+.1%}")      # 这就是技能的全部价值主张
assert delta > 0.05, "技能未通过准入: 差分不显著, 拒绝安装"
```

三十行不到。真正的工程量在两处：任务集要覆盖技能声称的触发场景**以及它的边界外场景**（一个只在场景内涨分、边界外不掉分的技能才是好技能）；judge 要独立于技能本身（技能教 agent 怎么做，判卷标准得是另一套，否则既当运动员又当裁判——这是验证器系列第一篇的老命题在技能场景的重现）。

## 四、保鲜是第二道门：活文档这个新物种

本周榜单上还有个值得单独说的项目：GoogleChrome 的 modern-web-guidance-src，6,542 stars/周。它做的不是技能，是**给 agent 持续喂活的最佳实践语料**——把 web 开发指南做成 agent 可消费、持续更新的知识源。

它瞄准的是训练截止问题：模型的领域知识冻结在训练那一天，而 API 在变、框架在演进。传统解法是搜索——每次现场查，慢、噪声大、结果不可复现。modern-web-guidance 代表另一条路：**结构化、可审计、定期更新的保鲜语料**，agent 引用它时拿到的是同一份、有版本的真相。

技能生态需要同款机制，而且需求更刚性：技能的行为层就是知识，知识过期 = 行为过期。所以技能的元数据里应该有三个今天大多数技能都没有的字段——**上游语料的版本号、内容保鲜的 SLA（多久必须重审一次）、上次通过 Tier 3 差分的日期**。第三项尤其重要：它把「这个技能还有用吗」从永远没人回答的开放问题，变成一个到期必须重跑的定时任务。我的 49 个技能缺的就是这个——不是缺盘点纪律，是缺让纪律自动触发的钩子。

## 五、准入三问：一个可以直接抄的框架

把上面全部收拢，安装任何技能之前过三个问题：

1. **它可验证吗？**——有没有 with-without 差分证据？没有就先跑一个，三十行脚本的事。
2. **它可保鲜吗？**——上游多久更新？有没有版本号？六个月没人碰的行为指导，默认按过期处理。
3. **它可退出吗？**——卸载之后 agent 行为是否完全恢复？技能最理想的形态是纯增量（装了多一层保障），最危险的形态是覆盖型（改写默认行为）——后者需要在差分里额外验证「卸载路径」。

结尾回到 npm。npm 用十五年时间证明了一件事：**注册表赢在信任层，不是数量层。**PyPI 有两百万个包，大家真正信任的是那几百个有维护者、有测试、有发布流程的。本周 skills.sh 和各家官方 marketplace 的出现说明分发战争已经开打，但下一个真正的基础设施缺口不在目录层——在技能的验证、去重与保鲜管道。谁先把「装进来之前证明它有用，装进来之后证明它还活着」做成默认流程，谁就是技能生态的 npm audit + Dependabot。

在那之前，那三十行差分脚本，是你唯一的安全带。

---

*验证器系列：[一、验证器经济学](https://robertsong2019.github.io/posts/verifier-economics-2026-11.html) · [二、AI 科学家与验证鸿沟](https://robertsong2019.github.io/posts/ai-scientist-verification-gap-2026-11.html) · [四、金鱼评审员](https://robertsong2019.github.io/posts/goldfish-reviewer-fresh-context-2026-11.html) · [五、轨迹数据飞轮](https://robertsong2019.github.io/posts/trajectory-data-flywheel-2026-11.html)*
