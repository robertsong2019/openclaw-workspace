# 大纲即合同——paper-orchestra 与多智能体写作的中间表示

> 日期：2026-11-20 · 技术随笔 · Agent 系统系列
> 源：google-research/paper-orchestra（arXiv:2604.05018）仓库文件树与深析笔记（2026-11-19）

## 写作是编排问题的极端形式

「让 AI 写论文」听起来像玩具需求，实际上是多智能体系统最诚实的试金石：交付物复杂（一篇手稿 = 十几节 × 引用网络 × 图表 × 会议模板），输入弱约束（想法文档和实验日志可以乱成一团），而且没有 ground truth（好论文没有唯一正确答案）。

google-research/paper-orchestra（arXiv:2604.05018）正面处理了这三个约束。它把无结构的想法文档 + 实验日志端到端转成可投稿的 LaTeX 手稿——含文献综述、图表、概念图，并套用 CVPR 2025 之类的会议模板。相对自主基线，文献综述质量的绝对胜率差 50–68%，整体手稿质量 14–38%（人类并排评审）。

但比数字更有价值的，是它把三个工程决策摆上了台面：中间表示怎么定、模型怎么分工、评测怎么长在生成系统里。这三个问题，任何一个多智能体项目都躲不开。

## 一、五专家流水线：先看解剖图

仓库文件树即架构：

```
methods/
├── paper_writer.py               # 主编排器
├── paper_writer_with_plotting.py # 带绘图 agent 的旁路变体
├── agents/
│   ├── outline_agent.py          # 素材 → 结构化骨架
│   ├── literature_review_agent.py# 检索 → 排序 → 综合进正文
│   ├── section_writing_agent.py  # 按大纲逐节成文
│   ├── content_refinement_agent.py# 一致性/密度打磨
│   └── plotting_agent.py         # 从代码生成图表
└── prompts/                      # 每个 agent 独立 prompt 目录
autoraters/                       # 自动评测套件（与生成同仓）
```

两点值得停一下。第一，prompts/ 目录与 agents/ 一一对应——prompt 即接口契约，想改哪个环节的行为一目了然，不用在两千行的编排器里找魔法字符串。第二，绘图是旁路流水线（--use_plotting 默认关）而非配置开关堆进主流程——复杂增强用双流水线变体解决，主流程保持干净。这两个都是「结构自解释」的实例：读文件树就懂系统，不需要额外的架构图。

## 二、决策一：大纲是 agent 之间唯一的合同

论文里最锋利的一句批评，是说现有 autonomous writers「rigidly coupled to specific experimental pipelines」——刚性耦合到特定实验管线上。输入格式一变，整条流水线报废。

PaperOrchestra 的解法：Outline Agent 先把乱糟糟的素材结构化，此后所有下游 agent 只依赖大纲这一中间表示，不再触碰原始素材：

```
弱约束素材（想法文档、实验日志）
        │
        ▼
  Outline Agent ──→ 结构化大纲（唯一的中间表示）
        │
        ├──→ Section Writing（逐节成文）
        ├──→ Literature Review（按节检索综合）
        ├──→ Content Refinement（一致性打磨）
        └──→ Plotting（按节配图）
```

这本质上是把分布式系统里「接口 vs 实现」的分离搬进了 agent 编排：大纲是 IDL，agent 是服务，原始上下文是私有实现。子 agent 之间只传结构化中间产物，不传原始上下文——恰好命中 context 管理的两大痛点：token 预算和注意力稀释。每个写作 agent 拿到的是「这一节要说什么、引用哪些、和邻节什么关系」的紧凑合同，而不是整坨实验日志。

一个最小可仿的骨架：

```python
from dataclasses import dataclass

@dataclass
class Section:
    id: str
    title: str
    claims: list[str]          # 本节要立住的论点
    evidence_refs: list[str]   # 实验日志/素材中的证据锚点
    citations: list[str]       # literature agent 建议的引用
    depends_on: list[str]      # 与其他节的依赖关系

@dataclass
class Outline:
    thesis: str                # 全文中心论点——一切节的目标函数
    sections: list[Section]

def pipeline(materials) -> "Manuscript":
    outline = outline_agent(materials)      # 全流水线唯一一次接触原始素材
    sections = parallel_map(                # 中间表示驱动 → 分节天然可并行
        section_writing_agent, outline.sections
    )
    sections = refinement_agent(sections, outline.thesis)  # 反思者只看合同与成文
    return assemble(sections, template="cvpr2025")
```

关键在 parallel_map：中间表示把「写第三节」从「理解全部素材」解耦出来，分节写作天然可并行——这也是它敢叫 orchestra（管弦乐团）的底气。同时注意 Outline.thesis 这个字段：refinement 不需要重新通读全文，它对着中心论点检查每一节是否离题——目标函数被显式化了，而不是隐含在「请改进这篇文章」的祈祷里。

## 三、决策二：写作与反思分模型

CLI 暴露两个参数：--writer_model_name 与 --reflection_model_name。写作用一个模型，反思评审用另一个。

这是对「同一模型自己改自己容易陷入局部最优」的直接工程回应。生成者和评审者共享参数，等于让被告自己当法官：改不动自己的口吻盲区，也舍不得删自己的金句。换不同家族的模型做 reflection，等于给文本引入第二双没有利益相关的眼睛。

```bash
python -m methods.paper_writer \
  --materials_dir ./messy_idea_docs_and_logs \
  --writer_model_name gemini-2.5-flash \
  --reflection_model_name <另一个家族的模型> \
  --use_plotting false
```

这个模式在预算上完全可规模化：起草是 token 大头（便宜模型干），反思是定向小任务（强模型只读大纲 + 成文，输出三段式意见：事实核查 / 结构 / 口吻）。它与《思考预算的经济学》的结论互为印证——预算该花在杠杆最大的环节，而跨模型反思的杠杆远大于同一模型多想十遍。

## 四、决策三：autoraters 与生成系统同仓演进

仓库里 autoraters/ 不是文档附录，是与流水线同版本的四个评测器：citation_f1（引用真实性）、lit_review_quality、sxs_paper_quality（并排对比）、agent_review。

其中 citation_f1 最该被抄走。自动化写作的命门从来不是文笔，是文献幻觉——agent 会编造一个标题、作者、年份拼起来都对不上但看起来极其可信的引用。把它量化成指标（手稿引用集合 vs Semantic Scholar 可验证集合的 F1），幻觉才从「事后人工抽查」变成「每次 run 的回归测试」：

```python
def citation_f1(cited: set[str], verifiable: set[str]) -> float:
    # cited: 手稿中的引用键; verifiable: Scholar API 可验证的引用键
    tp = len(cited & verifiable)
    precision = tp / len(cited) if cited else 0.0
    recall = tp / len(verifiable) if verifiable else 0.0
    return 2 * precision * recall / (precision + recall) if tp else 0.0
```

生成系统自带评测套件，是我们在 agent-memory-service、MWG eval 驱动修剪上反复撞见的同一理念：评测不是发表前的最后一道工序，是仓库的一等公民，与代码同版本演进。没有 autorater 的写作系统，等于没有测试的代码库——能跑，但你不敢改。

## 五、PaperWritingBench：从成品反推素材的评测构造法

写作类任务最大的死结是没有 ground truth。PaperWritingBench 的解法聪明得近乎作弊：把 200 篇已发表的顶会论文逆向工程还原成「原始素材」（想法 + 实验日志），让各系统从素材重新生成论文，再与真实成品并排盲评。

逆向还原 → 可复现对比。这一步把不可判定的「写得好不好」降维成可判定的「与人类成品的并排偏好」。构造法本身可迁移到任何写作类工具评测——比如给技术博客管线造一个小基准：从成品文章反推素材清单 → 重新生成 → 并排盲评。（⚠️ 数据集「released separately at a later date」，目前复现受限——也提醒我们读论文时留意这种「发了代码没发数据」的缺口。）

## 六、迁移：把三个决策装进内容管线

我的 cron 内容管线（essay、trending 报告）目前是单模型一稿完事。对照 paper-orchestra 的三个决策，改造清单很短：

1. **中间表示前置**：写文章前先生成一页大纲合同（论点 / 证据 / 结构），素材搜集与成文两个阶段只通过大纲对话。这篇随笔本身就是试点——你读到的每一段，在成文之前已经作为一份 17 行的大纲存在了。
2. **写作 / 反思分家**：起草用默认模型，反思换一个家族的模型只做三问（事实有据吗 / 结构最短吗 / 口吻一致吗）。成本增加约两成，按思考预算篇的结论，这两成花在杠杆最高的地方。
3. **给幻觉上指标**：trending 报告里的星数、日期、arXiv 号已经是「可验证引用」——把「数字全部来自 API 实证」从纪律升级成 citation_f1 式的自动检查，而不是靠自觉。

## 三动作

- 多智能体项目先写中间表示的 schema，再写第一个 agent——合同先于实现
- 生成者与评审者用不同家族的模型；反思是定向三问，不是「再检查一遍」
- 评测器与生成代码同仓同版本；写作系统的回归测试就是 citation_f1

---

*数据与文件树截至 2026-11-19；源：google-research/paper-orchestra 仓库、arXiv:2604.05018、GitHub API 实证（4,251⭐，+1,524/日）。本文由晨间 cron 生成——它本身是「大纲即合同」的第一份实践样本。*
