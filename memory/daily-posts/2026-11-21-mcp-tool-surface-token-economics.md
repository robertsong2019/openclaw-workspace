# 没打字，先计费——MCP 工具面的常驻税与供给侧经济学

> 系列语境：ATC 篇（11-13）治理的是请求侧——agent 发起的调用该不该放行；本文治理供给侧——工具清单本身对上下文的占用。两侧合起来，才是一份完整的上下文财政预算。

## 一、账单在第一个字之前就产生了

一个反直觉的事实：MCP server 连上的那一刻，你还没打一个字，token 账单已经开始累计。

Anthropic 官方文档给过一组数字：一套再普通不过的五服务器配置——GitHub（35 个工具，约 26K token）、Slack（11 个，约 21K）、Sentry（5 个，约 3K）、Grafana（5 个，约 3K）、Splunk（2 个，约 2K）——合计 58 个工具、约 55K token 的定义，在对话开始之前就已经塞进了上下文。再加一个 Jira（约 17K），就逼近 100K。Anthropic 说他们内部见过工具定义吃掉 134K token 的案例。

更扎心的是实测：有人抓包自己一周的配置，发现 63 个**整周从未被调用**的工具，贡献了 schema 字符数的 69%。你没看错——闲置工具才是账单的大头。

这就是本文的核心概念：**常驻税（standing charge）**。工具定义不是用的时候才付费，而是从连接那一刻起、每一轮请求都在付费的固定成本。

## 二、常驻税的三重伤害

**第一重：钱。** 工具定义渲染在 system prompt 之前，位于 cache 前缀的最前端。prompt cache 能把它降到全新输入约十分之一的价格——但前提是前缀稳定。server 中途连接、工具列表发生变化，都会打断 cache，当轮全额计费。也就是说，这笔税即使有减免，减免本身也是脆弱的。

**第二重：准。** 这是更隐蔽的伤害。Anthropic 的数据：工具超过 30–50 个，选择准确率开始退化。而启用 Tool Search（只呈现按需检索的少量工具）后，Opus 4 在 MCP 评测上从 49% 升到 74%，Opus 4.5 从 79.5% 升到 88.1%。**工具不是越多能力越强——工具越多，选错的概率越大。**多余的工具同时在烧钱和降准，这是名副其实的「负贡献税基」。

**第三重：挤占。** 上下文窗口是零和的。55K token 的工具定义，意味着留给系统提示、对话历史、检索文档的空间少 55K。在长会话 agent 场景里，这直接缩短了记忆寿命。

一篇 2026 年 5 月的 arXiv 研究给出了设计目标的量化版本：平均 7 个精选工具的覆盖率，几乎追平展示全部 50 个工具（90.3% vs 90.8%）；而对请求自适应的短列表，把正确选择率从 87.1% 提到 93.1%。结论清晰得近乎无情：**模型需要的不是全量目录，是为眼前这个请求挑好的短列表。**

## 三、供给侧：好 server 的自我修养

协议层方案（下一节）是消费端的补救，但更优雅的解法在供给侧——server 作者管好自己的输出。参考样本是 Google 官方的 **chrome-devtools-mcp**（58.4k★，63 个工具 / 13 大类，底层 Puppeteer + CDP）。它有份 design-principles.md，其中三条直指 token 经济学：

1. **token-optimized**：返回语义摘要，不返回 50K 行原始 JSON。heap snapshot 这种动辄几十万节点的数据，摘要出「泄漏嫌疑对象 Top-N + 保留链路径」比倾倒全量有价值得多。
2. **reference over value**：重资产只回文件引用（路径 + 摘要 + 读取方式），值本身留在磁盘上。模型需要时再按需读。
3. **渐进披露**：`--slim` 模式裁剪工具面，按用户实际工作流暴露子集；配合官方 skills 把复杂用法封装成流程文档。

第 2 条是杠杆最大的一条，值得所有工具作者抄写十遍。改造前后的对比：

```python
# ❌ 改造前：把值搬进上下文（每次调用 ~30K token 起）
@mcp.tool()
def list_heap_objects(snapshot_path: str) -> dict:
    snap = load_snapshot(snapshot_path)
    return {"objects": snap.objects}          # 200k 个对象全量序列化

# ✅ 改造后：reference over value（每次调用 ~400 token）
@mcp.tool()
def list_heap_objects(snapshot_path: str) -> dict:
    snap = load_snapshot(snapshot_path)
    report = f"{snapshot_path}.summary.json"  # 落盘，值留在磁盘
    write_summary(report, snap.top_retained(n=20))
    return {
        "total_objects": len(snap.objects),
        "summary_ref": report,                # 引用，不是值
        "hint": "用 read_object_details(ref, id) 查单个对象；"
                "可疑对象已按保留大小排序取 Top-20",
    }
```

同样的信息量，上下文成本差两个数量级。注意两个细节：`hint` 字段把「下一步怎么深入」写进返回值，这是把导航图嵌进摘要；Top-20 排序是预消化，不是让模型自己在 20 万行里找异常。

## 四、协议层：把目录从「常驻」变「检索」

如果工具面已经膨胀（或者你只是消费第三方 server），协议层现在有原生解法：**deferred tool loading + Tool Search**。核心思想一句话：工具目录不再常驻上下文，而是退化成一个约 500 token 的搜索器；模型需要某项能力时先搜索、命中后按需展开完整定义。

```json
{
  "tools": [
    { "type": "tool_search_tool_regex_20251119",
      "name": "tool_search_tool_regex" },
    { "name": "github_create_pull_request",
      "description": "Create a pull request",
      "input_schema": { "...": "..." },
      "defer_loading": true },
    { "name": "github_get_file_contents",
      "description": "Read file contents from a repo",
      "input_schema": { "...": "..." },
      "defer_loading": false }
  ]
}
```

对整台 MCP server 还可以打包处理——默认全部延迟，高频工具白名单直通：

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "github",
  "default_config": { "defer_loading": true },
  "configs": { "get_file_contents": { "defer_loading": false } }
}
```

实测效果：传统方式约 77K token 的工作前占用，降到约 8.7K（500 token 搜索器 + 3–5 个按需工具），**削减 85% 以上**，且完整保留对全量工具库的访问——官方口径可扩展到单请求 10,000 个延迟工具。经验触发线：工具 ≥10 个，或定义总量 >10K token，就该开 defer。

两个容易踩的坑：

- **defer 改变的是模型读到的，不是你传输的**。每个请求仍然发送全量定义，由 API 侧决定展开哪些进上下文。所以基于用户权限的工具过滤必须在 search 之前完成，否则会出现「模型搜得到、用户调不了」的权限幻觉。
- **列表稳定性是 cache 的命**。server 尽量在会话开始时全部连好；运行中追加工具要 append 在 cache 断点之后而不是重排数组；变更放到会话边界做。

## 五、第二张账单：中转税

工具定义是固定成本，还有一张变量账单：**中间结果的中转税**。WorkOS 把它点破了——工具间传递的每一字节数据都要途经模型。截图给工具 A、A 的原始输出给工具 B、B 再给 C，每一跳都按上下文价格全额计费，而且常常是双倍（进一次上下文，回一次结果）。

对照证据来自本周趋势项目 alibaba/open-code-review（52.8k★）：代码审查场景里，它用确定性管线做 diff 打包、文件选择、规则预筛，LLM 只在最后做语义判断。AACR-Bench 的结果：**同模型下 P/F1 更高，token 消耗只有全量上下文基线的 1/9**。这印证了一条通用法则——**数据在工具间流转时，尽量走进程内管道，不要走模型上下文这条最贵的总线**。

发现自己是否在交这两张账单，只需要一段审计脚本：

```python
#!/usr/bin/env python3
"""token-budget-audit.py — 工具面财政审计"""
import json, pathlib

TOOLS = pathlib.Path("tools/").glob("*.json")  # 每工具一个 schema 文件
CHARS_PER_TOKEN = 4                            # 英文粗估

rows = []
for f in sorted(TOOLS):
    schema = f.read_text(encoding="utf-8")
    rows.append((f.stem, len(schema) // CHARS_PER_TOKEN))

total = sum(t for _, t in rows)
print(f"{'tool':40s} {'tokens':>8s} {'share':>6s}")
for name, tok in sorted(rows, key=lambda r: -r[1]):
    flag = " ← 瘦身候选" if tok > 800 else ""
    print(f"{name:40s} {tok:8d} {tok/total:6.1%}{flag}")
print(f"{'TOTAL':40s} {total:8d}"
      f"  ({'⚠️ 超 defer 触发线' if total > 10_000 else 'OK'})")

# 顺手查返回值：哪个工具的示例输出最大？
worst = max(pathlib.Path("samples/").glob("*.json"),
            key=lambda p: p.stat().st_size, default=None)
if worst:
    print(f"\n最大示例返回: {worst.name} "
          f"~{worst.stat().st_size // CHARS_PER_TOKEN} tokens → 考虑 reference over value")
```

跑一遍，top 消耗者通常会让你吃惊——它们往往是你最不常用的工具。

## 六、行动清单

**如果你写 MCP server：**
- 返回值三问：能否摘要？能否落盘给引用？能否把「下一步」写进 hint？
- 工具数是预算不是资产：超过 30 个就该考虑合并或分层
- 每个工具的 description 按「搜索命中」优化——defer 时代它就是检索索引

**如果你做 agent 应用：**
- 工具 ≥10 或定义 >10K token，开 defer_loading；高频工具白名单控制在 5 个以内
- 会话开始连全部 server，之后列表只 append 不重排
- 工具间数据传递走进程内管道，模型只看摘要

**如果你只是用户：**
- 在 Claude Code 里跑 `/context`，看工具占了多少份额——超两成就该清理闲置 server
- 慎用聚合器：省了连接管理，但常驻税往往翻倍

## 七、收尾：上下文是公共财政

把上下文想象成一座城市的财政：对话历史是民生支出，检索文档是公共投资，而工具定义是基础设施税——不管你用不用，每轮都在收。城市的治理水平，不看它收多少税，看它收得克制不克制。

本文与 ATC 篇正好构成两侧：ATC 管「请求该怎么批」，本文管「税基该怎么缩」。合起来的原则只有一条：**模型的注意力是这片土地上最贵的资源，任何想在上面常驻的东西，都要为占用给出正当理由。**最好的工具面，是你感觉不到的工具面。
