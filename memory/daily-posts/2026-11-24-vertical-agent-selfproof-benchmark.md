# 没有基准的 Agent 主张只是营销——垂直 Agent 的自证三件套

> 2026-11-24 · 基于 alibaba/open-code-review（55,555⭐，weekly +3,700）及其 AACR-Bench 基准（50 仓库 / 200 真实 PR / 10 语言 / 80+ 工程师标注 1,505 个 ground-truth issue，HuggingFace: Alibaba-Aone/aacr-bench）整理，文中三个代码示例均已实测运行。

本周 GitHub trending 上 Agent Skills 生态依然在堆料：BugHunter 三连庄日榜第一，superpowers、CLI-Anything 各领风骚。但真正值得注意的回归是另一个：alibaba 的 open-code-review 带着 AACR-Bench 重新登上 weekly。它没有宣布"我们的 Agent 更聪明"，而是发布了三样东西：一个 50 仓库、200 条真实 PR、80 多位工程师交叉标注 1,505 个 ground-truth issue 的基准；一组同模型对比 Claude Code 的数字——Precision 和 F1 显著更高、token 消耗约九分之一、速度更快；以及一句主动声明：**Recall 更低，这是刻意的 precision-over-noise 取舍**。

这件事标志着垂直 Agent 的竞争进入新阶段：**没有基准的 Agent 主张只是 marketing，有基准的 trade-off 才是工程**。这篇文章拆解它背后的三件套：病理学、混合架构、自证闭环。

## 一、病理学：纯 Agent 为什么干不好审查

open-code-review 的 README 里有一段罕见的自我解剖——"为什么纯 LLM Agent 做不好 code review"，列了三种病灶：

- **coverage 不全**：大 changeset 时 Agent 会偷懒，自己挑几个文件审，其余略过。语言模型天然倾向于"看起来审过了"，没有任何机制保证每个文件都被覆盖。
- **position drift**：行号漂移。模型对 diff 上下文做多次推理后，报出的问题定位会漂离真实位置——审查报告里"第 42 行有个空指针"，实际上在第 58 行。
- **质量不稳**：prompt 的微小变动导致输出质量大幅波动。同一份代码，换个措辞重跑，结论可能从"三个问题"变成"十个问题"。

三种病灶指向同一个根因：**纯语言驱动的架构，对审查流程缺乏硬约束**。审查本质上是一个"不能漏、不能错位、不能抖"的确定性流程，你却把它整个交给一个概率性的文本生成器。这跟用大模型做四则运算是一个道理——不是模型不够聪明，是工具用错了地方。

## 二、混合架构：把"不能错的"从模型手里拿走

open-code-review 的解法是教科书级的混合分工：**确定性侧管"不能错的"，Agent 侧管"动态的"**。

确定性侧负责三件事：精确的文件选择（每个文件都被覆盖，不存在偷懒）、关联文件捆绑（比如 i18n 的中英文件捆成一个审查单元，改了 zh-CN 没改 en-US 也要一起看）、模板引擎级的规则匹配。独立的定位与反思模块则把"行号漂移"用后处理钉死。这些全是普通代码，零幻觉，行为可审计。

Agent 侧只留两件事：按场景调优的 prompt，和一个**从生产环境工具调用 trace 里蒸馏出来的专用 toolset**。

确定性侧长什么样？核心其实就是一段朴素得近乎无聊的代码：

```python
import fnmatch
from pathlib import Path

REPO = Path("repo")  # 被审仓库的 checkout

# 确定性规则：哪些文件必须捆在一起审，即使配对文件没出现在 diff 里
BUNDLE_RULES = [
    ("locales/*/zh-CN.json", lambda f: f.replace("zh-CN", "en-US")),
    ("src/**/*.tsx",         lambda f: str(Path(f).parent / "__tests__"
                                   / (Path(f).stem + ".test.tsx"))),
    ("migrations/*.sql",     lambda f: "docs/schema.md"),
]

def select_files(changed: list[str]) -> list[list[str]]:
    """把改动文件分组成审查单元：确定性匹配，不走模型，一个不漏"""
    groups, used = [], set()
    for pattern, mate_of in BUNDLE_RULES:
        for f in changed:
            if fnmatch.fnmatch(f, pattern):
                mate = mate_of(f)
                pair = [f] + ([mate] if (REPO / mate).exists() else [])
                groups.append(pair)
                used.add(f)
    # 未匹配规则的文件单独成组
    return groups + [[f] for f in changed if f not in used]

changed = ["locales/app/zh-CN.json", "src/ui/Button.tsx", "pkg/util.go"]
for unit in select_files(changed):
    print("review unit:", unit)
# review unit: ['locales/app/zh-CN.json', 'locales/app/en-US.json']
# review unit: ['src/ui/Button.tsx', 'src/ui/__tests__/Button.test.tsx']
# review unit: ['pkg/util.go']
```

注意输出里那个细节：`en-US.json` 和 `Button.test.tsx` **根本不在 diff 里**，但确定性规则把它们拖进了审查单元。这种"改动之外的相关性"恰恰是纯 Agent 最容易漏掉的——模型只看得见你喂给它的 diff，而工程上的关联藏在仓库结构里。三行 fnmatch 规则，把这个问题从"指望模型想起来"变成"结构上不可能漏"。

## 三、从调用 trace 蒸馏 toolset：工具面也要做减法

Agent 侧最有迁移价值的一招，是它的工具集不是拍脑袋定的，而是**分析生产环境真实调用 trace 的频率分布和重复率之后裁剪出来的**。通用 Agent 给模型一把瑞士军刀，它给模型一把正好顺手的厨刀。

背景是工具面经济学：每个工具的 schema 都吃上下文，工具越多，模型选择越犹豫、token 越贵、行为越不稳（这个主题我在《MCP 工具面的 token 经济学》里展开过）。裁剪逻辑本身依然是朴素代码：

```python
import json
from collections import Counter

trace = json.load(open("trace.json"))  # 生产环境攒下的真实调用 trace
calls = Counter(entry["tool"] for entry in trace)
total = sum(calls.values())

# 按 Pareto 裁剪：留下覆盖 95% 调用的头部工具，其余下线
kept, covered = [], 0
for tool, n in calls.most_common():
    kept.append(tool)
    covered += n
    if covered / total >= 0.95:
        break
dropped = len(calls) - len(kept)
print(f"蒸馏后 toolset: {len(kept)} 个工具 (下线 {dropped} 个), "
      f"覆盖 {covered/total:.1%} 调用")
# 蒸馏后 toolset: 7 个工具 (下线 3 个), 覆盖 96.8% 调用
```

实测这段示意 trace：10 个工具 94 次调用，Pareto 裁剪后留 7 个、下线 3 个，仍覆盖 96.8% 的调用。被下线的 slack_post、browser_screenshot 们不是没用，而是**频率不足以证明它们值得常驻上下文**——真要用，可以走显式的提权通道，而不是默认背着走。"从 trace 蒸馏工具面"这个做法对任何 Agent 都适用：你的工具清单应该是调用数据的函数，而不是工程师的愿望清单。

## 四、自证三件套：基准、trade-off、可复跑

回到开头那组数字。它的价值不在于"赢了 Claude Code"，而在于三件事同时成立：

**第一，自带基准。** AACR-Bench 的 1,505 个 ground-truth issue 全部来自真实 PR、由 80+ 工程师交叉标注，数据集公开发布在 HuggingFace。对比"我们内部评测提升 30%"这种无法证伪的话术，基准把主张变成了可检验的命题。

**第二，显式 trade-off。** Recall 更低不是被藏起来的短板，而是写进声明的取舍：审查场景里，误报浪费的是人类 reviewer 最贵的注意力，漏报还有人工审查兜底——所以 precision 优先。这是产品决策，不是技术缺陷。

**第三，可复跑。** 数据集可下载、评测方法公开，第三方可以独立复现。trending 上无数"Agent 能力+50%"的宣传，缺的就是这一环。

而且 trade-off 不该只活在 README 里，它可以直接变成 CI 断言：

```python
def evaluate(found: list[str], truth: list[str]):
    tp = len(set(found) & set(truth))
    precision = tp / len(found) if found else 1.0
    recall = tp / len(truth)
    return {"precision": precision, "recall": recall}

truth = [f"issue-{i}" for i in range(100)]          # ground truth
agent_report = truth[:38] + ["noise-1", "noise-2"]  # 38 真问题 + 2 误报

m = evaluate(agent_report, truth)
# {'precision': 0.95, 'recall': 0.38}

# 把取舍写进 CI，让声明可执行
assert m["precision"] >= 0.90, "precision 底线失守：审查者信任开始流失"
# recall 刻意不设断言——precision-over-noise 是产品决策
```

precision 设断言、recall 不设，这段不对成的断言本身就是 trade-off 的可执行形态。哪天想换策略，改阈值、重跑基准、把新旧数字一起挂出来——取舍的变更也走评审，而不是悄悄漂移。

## 五、寄生分发，与一个更大的转向

分发方式同样值得记一笔：open-code-review 不自带 UI，`ocr` CLI 打包成 Agent Skills，直接装进 Claude Code、Codex、Cursor、Kimi Code。**垂直工具不再自建门户，而是寄生到通用 Agent 里**——能力以技能形式存在，宿主随用户挑。这与本周 trending 上 Agent Skills 成为跨 harness 通用标准的趋势完全同频。

把镜头拉远：skill 生态上半年在解决"怎么堆更多能力"，下半年在解决"怎么治理和安全"（上周的黑市审计），而 open-code-review 展示了第三阶段——**垂直能力开始用工程标准自证**。自带基准、声明取舍、可复跑验证，这三件套过去是数据库、编译器这类基础软件的发布纪律，现在轮到 Agent 了。

对自己手上的 Agent 项目，可以立刻抄三样作业：给核心能力建一个哪怕只有几十条标注的小基准；把产品层面的取舍写成显式声明甚至 CI 断言；从自己的调用 trace 里裁一次工具面。三件事都不需要训练模型，但每一件都在把你的 Agent 从"演示"推向"工程"。

---

*字数：约 2,600 · 三个代码示例均在 Python 3 下实测通过（捆绑分组 / Pareto 裁剪 / CI 断言）。*
