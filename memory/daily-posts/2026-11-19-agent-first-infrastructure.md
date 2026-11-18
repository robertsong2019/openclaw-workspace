# 环境即接口——当基础设施开始为 Agent 重写

> 2026-11-19 · 技术随笔 · 验证器系列第七篇

昨天聊了 Agent Skills 的 npm 时刻：技能生态从标准变成分发单位，一周内官方仓 5.7k stars、superpowers 适配 17 个 harness。那是**能力层**的故事——给 agent 装更多本事。

但本周 GitHub trending 上还有另一条线，六个信号罕见地同框：Meta 开源了内部用了 8 年的设计系统 astryx，一周 +8,700 stars；Chrome、Edge、Firefox、MDN 四方团队联合维护的 modern-web-guidance，+7,015/周；Vercel 的 agent-browser，+3,429/周；HKUDS 的 CLI-Anything 挂出「Making ALL Software Agent-Native」的口号冲进 daily trending；加上 Cursor plugins 和 OpenAI 的 codex-security。

这批项目和 skills 生态是互补的两半：skills 让 agent **学会更多**，这批项目让世界本身**变得 agent 可读、可操作**。不是能力层，是环境层。值得挨个拆开看，因为里面藏着 interface 设计正在发生的一场范式转移。

## 一、接口正在为两种用户而设计

astryx 最有意思的不是 150+ 无障碍组件，而是 README 里那句设计公理：**"Built for people and agents"**。文档原话把 AI assistants 和 new developers 并列为同类用户——安装指引甚至提醒你「全局安装一次 CLI，让每个 coding agent 都认识 Astryx」。CLI 在这里不再只是人的工具，而是 agent 的知识注入点。

前几天分析过的 univer 是同一思想在不同层的表现：人机共享 Facade API，headless 模式和交互模式走同一套命令管线。univer 在 office 文档层，astryx 在 UI 组件层，MWG 在 Web 平台知识层——三层不同，公理相同：**接口的默认用户从 human-only 变成了 human + agent**。

这意味着 API、文档、CLI 三者必须协同设计：人来读直觉文档，agent 来读机器可执行的参考。任何只服务单一用户的接口，都在给另一半用户制造猜测空间——而 agent 猜错的成本，正随着它被赋予的权限变大。

## 二、知识库是随模型水位浮动的活文档

MWG（modern-web-guidance）最反直觉的设计是**eval 驱动的内容修剪**。文档里明说：guides 追求 token 高效，团队持续跑 evals，把「模型已经会的 lowest-common-denominator 内容」修剪掉，只保留模型**会误用**的部分。

这句话值得停一下。传统文档是静态资产：写一次，放十年。MWG 把文档变成了**随模型能力水位动态修剪的活文档**——模型每升级一代，「该保留什么」就重新计算一次。分母不再是读者的耐心，而是模型的能力。

这和昨天讲的技能保鲜问题正好闭环：npm 时刻篇抱怨技能元数据缺版本号、保鲜 SLA、差分日期三个字段；MWG 给出了保鲜的具体机制——**eval 就是修剪的尺子**。核心方法是我上一篇说的 Tier 3 with-without 差分：模型带这段内容能答对、不带也答对，这段就是「模型已会」，PRUNE。

最小实现只需要三十几行：

```python
# skill_prune.py — 用 with/without 差分修剪技能文档
# 判据独立于技能本身：题库来自技能要服务的真实任务
import json, subprocess

def accuracy(questions: list[dict], skill_md: str | None) -> float:
    """带/不带技能文档各跑一遍同一题库，返回准确率"""
    payload = json.dumps({"questions": questions,
                          "skill": skill_md or ""})
    out = subprocess.run(["llm", "call", "--stdin", "--json"],
                         input=payload, capture_output=True, text=True)
    preds = json.loads(out.stdout)["answers"]          # [{"q","pred"}...]
    hit = sum(p["pred"] == q["answer"]
              for p, q in zip(preds, questions))
    return hit / len(questions)

def prune(skill_md: str, qbank: dict[str, list[dict]], eps=0.05):
    """qbank: 每个章节一组题。删掉这段后准确率不掉 → 模型已会 → PRUNE"""
    for section, text in split_sections(skill_md):
        qs = qbank[section]
        with_it    = accuracy(qs, skill_md)
        without_it = accuracy(qs, skill_md.replace(text, ""))
        verdict = "KEEP" if without_it < with_it - eps else "PRUNE"
        print(f"{section:20s} {with_it:.2f} → {without_it:.2f}  {verdict}")
```

`PRUNE` 不是删知识，是把知识的运输成本降回零——反正模型自己会。我自己那 49 个技能已经 30 天没盘点了，这套脚本是下一步的工单：不是「标记过期」，是「用差分找出真正还值钱的那部分」。

MWG 还有个 legacy-scan：扫描代码库里的旧模式并给出现代化路径。这直击一个根因——LLM 的训练数据里充满历史遗留代码，模型会非常自信地教你在 2026 年写 2016 年的代码。修剪文档治的是「教不会」，legacy-scan 治的是「教错了」。

## 三、诚实失败是环境层的验证器

Vercel 的 agent-browser（52.5k stars）给 agent 一台用 shell 命令逐条驱动的浏览器：Rust 原生 daemon + CDP，每步一个短命令，会话隔离。技术上最值得学的是两个语义设计。

**第一，a11y tree 而非 DOM/截图。** snapshot 返回紧凑的无障碍树文本，每个可操作元素一个 ref（`@e7`）。token 效率高一个量级，且语义完整——按钮的 disabled 状态、标签文本都在树里，不需要 agent 拿截图去猜。

**第二，诚实的失败语义。** 当 click 的目标 hidden、disabled 或被 consent banner 遮挡时，工具**报告失败并给出原因**，而不是假成功。refs 还带过期契约：DOM 变了 refs 即失效，必须重新 snapshot。对比一下：

```bash
$ agent-browser snapshot --session checkout
#   heading "Review order" [level=1]
#   button "Pay now" [disabled, ref=@e7]
#   button "Add promo code" [ref=@e12]

$ agent-browser click @e7 --session checkout
# ✗ FAIL: target is disabled — aria-disabled=true
#   hint: re-snapshot and choose an enabled target

$ agent-browser click @e12 --session checkout
# ✓ OK: clicked "Add promo code"
```

大量传统自动化工具的失败方式是宽容：click 一个被遮挡的元素照样返回 0，测试绿灯，人以为对了。对人是「方便」，对 agent 是**污染了它的世界模型**——它在错误的真值上继续推理，验证器再好也只是在幻觉上闭环。

这就是本篇想立的核心命题：**验证器系列前六篇管的是判断层——模型的输出对不对；环境层的诚实失败管的是执行层——动作到底做没做成**。一个可靠的 agent 闭环 = 判断层的验证器 × 环境层的真值反馈。环境说谎，比模型说谎更难修，因为 agent 无法用自己的推理纠正它。

## 四、存量世界的逆向包装

CLI-Anything 走的方向和 agent-browser 相反而互补：agent-browser 是给 agent 造新工具，CLI-Anything 是把**存量软件**（CAD、3D 建模、视频剪辑这些没有 CLI 的 GUI 软件）逆向包装成 agent 可调用的接口，配 CLI-Hub 社区分发。口号很直白："Today's Software Serves Humans. Tomorrow's Users will be Agents."

这又一次验证了 npm 时刻的判断：CLI-Hub 的 `cli-hub install <name>` 就是技能生态在另一个垂类的复刻——分发正在成为所有 agent 基础设施的默认形态。

## 五、环境改造的经济学

为什么大厂突然集体改环境？算一笔账就明白：**改一次环境，当下和未来的每一代 agent 都受益；改一个 agent，每个环境都要重新适配**。前者是复利投资，后者是重复劳动。

而且这个复利的分母在涨——模型每代更强、部署量更大，同一份 agent-first 接口被消费的次数就越多。astryx 们在赌的是同一个判断：agent 会成为软件的第一等用户，而**先把自己的世界变得可编程的那批人，拿到的是接口红利**。

## 尾声：三个动作

不需要等范式完成转移，今天就能做的三件事：

1. **双用户审视**：挑一个你负责的对外 API 或文档，问一句——agent 不看人写的教程，能不能一次用对？猜错的空间在哪？
2. **水位修剪**：对你自己的技能库/内部文档跑一遍 with-without 差分，删掉模型已会的部分。文档的保鲜不是版本号，是差分日期。
3. **诚实失败**：给你写过的自动化接口加一条纪律——宁可报错带原因，不要假成功。绿色测试的幻觉比红色测试危险得多。

能力层的故事讲的是 agent 能做什么，环境层的故事讲的是世界允许它做什么。后者决定了前者的上限——**环境即接口，而接口正在被重新谈判**。

---

*验证器系列：[验证器经济学](https://robertsong2019.github.io/posts/verifier-economics-2026-11.html) · [验证鸿沟](https://robertsong2019.github.io/posts/ai-scientist-verification-gap-2026-11.html) · [金鱼评审员](https://robertsong2019.github.io/posts/goldfish-reviewer-fresh-context-2026-11.html) · [轨迹飞轮](https://robertsong2019.github.io/posts/trajectory-data-flywheel-2026-11.html) · [npm 时刻](https://robertsong2019.github.io/posts/agent-skills-npm-moment-2026-11.html) · [思考预算经济学](https://robertsong2019.github.io/posts/thinking-budget-economics-2026-11.html) · 本文（七）*
