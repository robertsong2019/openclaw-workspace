# 金鱼评审员：把「没有上下文」变成特性

**日期：** 2026-11-17 · **标签：** AI Agent / Context Engineering / Verification

GitHub Trending 本周有个反直觉的项目：Google 开源的 **elephant-goldfish-model**（EGM，非官方产品，源自 Dave Rensin 的文章），一周 5 千星。它做的事一句话讲完：**大象**（持有完整项目上下文的 agent）起草设计文档，**金鱼**（不带任何对话历史的全新 agent）做评审。

反直觉在哪？过去两年整个行业的叙事都是「上下文越多越好」——memory 系统、RAG、无限窗口，全在对抗遗忘。EGM 反着来：**故意让评审员失忆**，并把失忆本身当成特性卖。这不是行为艺术，它戳中的是 agent 工程里一个越来越疼的问题：**上下文不但会污染生成，还会污染验证。**

## 一、为什么带着上下文的评审会失效

评审者与作者共享上下文，看起来是优势，实际上是三重污染：

**锚定。**评审 agent 读到的第一份材料就是作者的观点。后续审查会不自觉地围绕「这个方案如何成立」展开，而不是「这个方案是否成立」。人类 code review 早就有对应研究：作者自己 review 自己的 PR，缺陷检出率显著下降——agent 没有理由豁免。

**共享幻觉。**会话历史里一旦形成过一个错误事实（文件名、API 签名、某个「测试已通过」），作者和评审者共享同一段历史，幻觉对双方是「共识」。你没法用同一个脑子发现自己脑子的错。上周刚写过的《[AI 科学家与验证鸿沟](https://robertsong2019.github.io/posts/ai-scientist-verification-gap-2026-11.html)》里那个数据——25k+ 轨迹审计发现 68% 的 run 忽略证据——同一个上下文里的「评审」救不了这个，因为评审者自己就泡在那 68% 的上下文里。

**沉没成本被继承。**长会话里，作者 agent 已经为方案辩护过三轮。评审 agent 看得到这些辩护，于是「这个 tradeoff 已经讨论过了」变成免检通行证。未声明的假设就这么溜进了主分支。

## 二、金鱼看到的世界

EGM 的金鱼评审员拿到的输入只有三样：**被评审的文档本身、文档显式引用的源码/文件、评审清单**。没有会话历史，没有作者解释，没有上一轮讨论。

这个设计把「没有上下文」从缺陷反转成了三种能力：

1. **幻觉引用无处遁形。**文档说「调用 `foo(a, b)`」，金鱼手里只有源码，源码里 `foo` 是三个参数——评审立刻失败。带历史的评审者会「记得」某轮讨论里改过签名，于是放过。
2. **未声明假设自动暴露。**大象知道部署环境是 Linux，写文档时省略了；金鱼不知道，只能问「这个路径分隔符在什么系统上成立？」——问题本身就是审查产出。
3. **立场零继承。**金鱼对方案没有任何历史投资，反驳成本和大象完全不对称。EGM 把整个流程编排成五阶段：brainstorm → draft → review → resolve → drift-report，人只做架构取舍和最终批准。

最有意思的是 **drift-report**：定期让金鱼把 `docs/designs/` 和当前源码逐条对照，产出「文档腐化报告」。这解决的是另一个时间维度的上下文污染——**文档写完那天就开始腐烂**，而团队里没人有「新鲜的眼睛」。

## 三、上下文是价值函数，不是单调资产

这和 memory 研究方向形成了漂亮的镜像。我们做 agent memory（amg）一直在对抗遗忘：证据进窗、hindsight 重放、选择预算化。EGM 在利用遗忘。两边其实是同一个问题的两端——**上下文的价值不是常数，是关于任务和角色的函数**：

- 对**生成**，上下文是资产：没有项目历史的起草者写不出合理设计。
- 对**验证**，上下文是负债：评审者知道的每一条「背景」，都是一条潜在的免检通道。
- 对**检索/复用**，上下文是成本：token 税和注意力稀释。

值得记住的判断标准：**这个角色需要为「未写进文档的共识」负责吗？**需要，给它上下文；不需要，给金鱼。评审岗位的定义恰恰是「只对材料和清单负责」——所以它天然适合失忆。

## 四、五十行代码落一个金鱼

不用等 EGM，任何 harness 里都能实现最小金鱼。核心只有一条纪律：**评审子进程的输入白名单化，历史一律不传。**

```python
# goldfish.py — 最小新鲜上下文评审员
import json, subprocess

def goldfish_review(doc_path: str, ref_paths: list[str]) -> str:
    """金鱼只看：被评审文档 + 文档显式引用的材料。没有会话历史。"""
    doc = open(doc_path).read()
    refs = {p: open(p).read() for p in ref_paths}   # 引用必须物化，不许"我记得"

    prompt = f"""你是零上下文评审员。以下是设计文档与其引用的源码。
对文档中每条事实性声明输出三列：
- 引用定位：该声明在源码中的位置；找不到 = 幻觉引用，直接标 FAIL
- 未声明假设：文档依赖但未解释的前提，逐条列出
- 文档-代码漂移：API 签名、参数个数、文件数量等任何对不上的地方

<文档>{doc}</文档>
<源码>{json.dumps(refs, ensure_ascii=False, indent=1)}</源码>"""

    r = subprocess.run(          # 关键：新进程/新会话，评审者≠作者
        ["your-agent", "run", "--fresh-session", "--model", "review-model"],
        input=prompt, capture_output=True, text=True, timeout=600)
    return r.stdout
```

`--fresh-session` 这一个参数就是全部架构差异。大多数 harness 的默认行为是继承会话——**默认恰恰是错的**，评审场景要显式关掉。

drift-report 同样可以最小化。挑文档里最容易被代码推翻的声明，做成机械对照：

```python
# drift_report.py — 文档腐化检测（金鱼的定时任务版）
import re, pathlib, datetime

CHECKS = [  # (文档声明模式, 现实来源函数, 声明所在文件)
    (r"支持\s*(\d+)\s*种\s*harness", lambda d: len(list(d.glob("integrations/*/manifest.json"))), "README.md"),
    (r"全部\s*(\d+)\s*个模块",        lambda d: len(list(d.glob("src/*.py"))),                  "docs/arch.md"),
]

def drift_report(root: pathlib.Path) -> list[str]:
    out = []
    for pat, probe, doc_file in CHECKS:
        doc = (root / doc_file).read_text(encoding="utf-8")
        if m := re.search(pat, doc):
            claimed, actual = int(m.group(1)), probe(root)
            if claimed != actual:   # 声明与现实的差 = 腐化量
                out.append(f"[DRIFT] {doc_file}: 文档说 {claimed}，实际 {actual}，"
                           f"检出 {datetime.date.today()}")
    return out or ["[OK] 零漂移"]
```

挂在 cron 里每周跑一次，文档从「写完即腐烂」变成「腐烂有台账」。注意这两段代码的分工：**能机械对照的（数字、签名、路径）交给脚本，语义性的（假设是否合理、方案是否成立）才交给金鱼**——这是《[外壳打败模型](https://robertsong2019.github.io/posts/harness-beats-model-2026-11.html)》那条铁律在验证侧的又一次应用。

## 五、边界

金鱼不是万灵药。三类任务不适合失忆评审：需要隐式任务语境的（评审一个多轮谈判的中间产物）、需要「作者意图」的（评审文档是否达到了作者目的，而非是否自洽）、以及材料本身不完备的（金鱼会把信息缺口全部报成问题——这有时是特性，有时是噪音）。另外金鱼评审有 token 成本：每轮都是全量材料重读，五阶段流水线跑下来不便宜。合理的折中是大象写文档时**把关键决策和理由物化进文档**——这反过来倒逼文档质量，大象被迫写出能让金鱼看懂的文档，本身就是收益。

值得盯住的判断：memory 系统在教 agent 记住什么，金鱼评审在教 agent **为忘记负责**。上下文工程正在从「把相关的东西塞进窗口」演进为「为每个角色计算该看见什么」——窗口不再是一个口袋，是一个权限系统。

---
*参考：google/elephant-goldfish-model（Agent Skills 标准，Apache 2.0）、arXiv:2605.08956（25k+ 轨迹审计）、本系列前篇《谁给 Agent 判卷》《外壳打败模型》《AI 科学家与验证鸿沟》。*
