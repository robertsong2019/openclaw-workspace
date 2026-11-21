# --help 不上税——工具披露的时序经济学

> 系列语境：上一篇《没打字，先计费》讲的是工具 schema 的常驻税有多重；本篇讲更深一层的问题——信息在什么时刻进入上下文，本质上是一种定价机制。披露时序决定谁付钱、什么时候付、付多少。

## 同一个 FFmpeg 的两种出场方式

想象 agent 要剪一段视频。路 A：连接一个 MCP server，42 个工具的完整 JSON Schema——参数名、类型、枚举、描述——在你打出第一个字之前就全部塞进上下文。路 B：agent 执行 `ffmpeg-skill --help`，看到 12 个动词级命令的一句话摘要，挑中 `video-cut`，再执行 `video-cut --help` 拿到三个参数的细节，然后调用。

两条路都能完成任务，但计费结构完全不同。路 A 是包月制：不管这次对话用不用得上 HDR→SDR 转换和多机位对齐，42 份定义每一轮请求都在场、都在计费、都在参与注意力分配。路 B 是按次制：只为实际用到的信息付费，没问的不要钱。

上一篇讲过常驻税的量级（五个 server 58 个工具 55K token 起步、闲置工具占 schema 的 69%）。本篇的问题是：为什么会有这种税？答案是——**披露时序错位**。工具面把「模型需要知道工具存在」和「模型需要工具的全部细节」混成了同一时刻的同一份载荷，而对前者征税是合理的、对后者征税纯属浪费。

## 一、推与拉：两种货架的经济学

推式披露：把全部 schema 常驻注入上下文，像大卖场——进门就把所有货架摆在你面前。固定成本前置，每轮都付，不用也付。

拉式披露：`--help`、`search_tools`、Tool Search，像店员——你问什么，他递什么。变动成本，用了才付，代价是每次交互多一轮往返。

前端工程师会觉得眼熟：这正是 2014 年那场性能革命的原题——全量 bundle vs code splitting / lazy loading。区别只在计量单位：浏览器计的是字节数，LLM 计的是 token 和注意力。Web 生态花了十年才让「按需加载」成为默认，工具面正在以快得多的速度重演，因为它有浏览器时代没有的东西：**一个会主动发起查询的消费方**。模型自己会读 `--help`、自己会调 search，这是拉式披露在 agent 时代突然可行的根本原因——浏览器只能等代码去 lazy load，模型能自己决定去问。

经济学的表述更简洁：披露时序是定价机制。推式把信息当公共品预付（税），拉式把信息当检索品计费（meter）。闲置率越高，包月越亏。而工具面的实测闲置率高得惊人——63 个整周未调用的工具占掉 69% 的 schema。为一个闲置率七成的货架付包月费，这笔账怎么算都不成立。

## 二、一周三案收敛：按需披露正在成为默认

有意思的不是哪个项目在做按需披露，而是三个互不相识的生态在同一周收敛到了同一个答案：

**ffmpeg-skill**（9k★，周增 3.2k）：42 个 FFmpeg 工具，但 `tools/list` 默认只广告核心 12 个；`tools/call` 对全部 42 个按名永远可达；环境变量 `FFMPEG_SKILL_MCP_FULL=1` 才展开全量。广告面和调用面分离——这就是两层披露的标准形态。

**chrome-devtools-mcp**：官方给出一整套 `--slim` 模式——工具描述换语义摘要、参数值换引用（reference over value）、heap snapshot 场景 token 差两个数量级。

**CLI-Anything**（港大 HKUDS，61k★）：反方向但同答案——给 CAD、3D 建模、视频剪辑这些从无 CLI 的 GUI 软件批量生成 CLI。一旦软件有了 CLI，`--help` 就是天然的 JIT 披露：agent 不问，文档不存在；agent 问，文档才计费。

三个项目、三种路径、同一周。这不是品味巧合，是结构性压力：上下文的注意力预算就那么多，任何想在上面常驻的东西都要给出占用理由。供给侧最小化正在从论文建议变成默认配置。

## 三、--help 是史上最成功的 JIT 披露系统

回头看，Unix 五十年前就把披露时序做对了：没人会在登录时读完所有命令的 man 手册，`--help`、man 分节、tab 补全构成了人类用户已经用惯的按需披露体系。它对 agent 自动有效，因为「文本即协议」——`--help` 输出密集、确定、版本化、可 grep，为人类设计的工效学对读文本的模型天然友好。文档面就是 API 面，这是 astryx 那批 agent-ready 工具早就验证过的教训。

但 CLI 路线一直有个工程死结：同一个工具要维护两份资产——CLI 旗标一份、MCP schema 一份——漂移只是时间问题。ffmpeg-skill 的 SPEC（Self-Producing Execution Contract）把这个结剪断了：

```python
import argparse, json, sys

def build_parser():
    # 唯一事实源：旗标只在这里定义一次
    p = argparse.ArgumentParser(prog="video-cut",
                                description="无损剪切视频片段")
    p.add_argument("input", help="输入文件路径")
    p.add_argument("--start", type=float, required=True, help="起始秒")
    p.add_argument("--end",   type=float, required=True, help="结束秒")
    return p

TYPE_MAP = {float: "number", int: "integer"}

def schema_from_parser(p):
    """SPEC 核心：MCP input_schema 与 --help 同源派生。
    CI 里对拍两份产物，漂移即 fail——CLI 与 schema
    从两份资产变成同一事实源的两个投影视图。"""
    props, required = {}, []
    for a in p._actions:
        if a.dest == "help":
            continue
        props[a.dest] = {
            "type": TYPE_MAP.get(a.type, "string"),
            "description": a.help or "",
        }
        if a.required:
            required.append(a.dest)
    return {"type": "object", "properties": props,
            "required": required}

if __name__ == "__main__":
    parser = build_parser()
    if "--schema" in sys.argv:      # agent 通道：按需拉取 schema
        print(json.dumps(schema_from_parser(parser),
                         ensure_ascii=False, indent=2))
    else:                            # 人类通道：--help
        parser.parse_args(["--help"])
```

这段代码的核心不是哪个技巧，而是资产结构：**schema 不再是文档，是投影**。投影永远不可能和源漂移——因为投影每次都是现算的。这一个设计决定同时消灭了双维护成本和漂移风险，是本周最值得抄走工程模式。

## 四、拉式的隐藏账单：延迟与自举

按需披露不是免费的。两笔隐藏成本必须计入：

**延迟税**。每层披露多一次往返：查工具 → 读 schema → 调用。对高频工具，这几百毫秒乘以调用次数就是新账单。所以核心工具该常驻还常驻——两层披露不是全藏，是分级。

**自举问题**。这是拉式披露真正的深水区：藏起来的工具，模型怎么知道该去问？模型必须先知道「有这个东西可查」，查询行为才会发生。全部藏起来等于不存在。

解法是一个最小稳定索引：名称 + 一句话摘要，常驻；完整 schema，按需。ffmpeg-skill 的 12/42 正是这个数学——12 个动词级命令覆盖绝大多数意图，42 个参数级细节按名直达。这个最小索引有三条纪律：

1. **稳定**：列表不能漂移。索引一变，prompt cache 全部失效——昨文讲过，缓存是工具面的命。
2. **正交**：索引条目之间语义不重叠。模型是从名字猜功能的，两个名字都能匹配的查询，模型就会猜错。
3. **可预测**：命名成体系（`video-cut`/`video-join`/`extract-audio`），模型没读过细节也能猜对参数的大致形状。

于是决策矩阵很清晰：工具 ≤10 个且 schema <10K token，推式够用，别折腾；超过这条线，两层披露；如果工具本质是把 CLI 包了一层——考虑别包了，直接 CLI 化，让 `--help` 替你做披露。

## 五、两层披露的实现骨架

把上面的原则合成一个 MCP server 骨架（示意）：

```python
mcp = FastMCP("ffmpeg-skill")

CORE = {"video_cut", "video_join", "extract_audio", ...}  # 动词级，常驻广告
ALL = load_registry()                                      # 全量注册表

@mcp.tool
def search_tools(query: str, k: int = 5) -> list[dict]:
    """检索长尾工具的完整定义（拉式通道）。

    返回完整 input_schema 而非描述——模型读完即可调用。
    权限过滤必须在检索之前完成：模型不该看见无权工具的存在。
    """
    ranked = rank(ALL, query)[:k]
    return [t.full_schema for t in ranked if t.name not in CORE]

for tool in ALL:
    # 广告面 ≠ 调用面：core 进 tools/list，
    # 长尾不广告但对 tools/call 按名永远可达
    mcp.register(tool, advertise=tool.name in CORE)
```

三个不可妥协点：`tools/call` 必须对隐藏工具按名可达（隐藏是广告策略，不是访问控制）；`search_tools` 返回的必须是可执行调用的完整 schema，不是「请查看文档」；权限过滤在 search 之前。

## 收尾：schema 从身份牌变成查询结果

接口层这两年连着换判词：先是「像素退位，文本加冕」，现在是「常驻退位，按需登场」。本质上，披露时序从推式走向拉式，是把注意力预算的定价权从工具作者手里交还给对话本身——信息不再按「作者觉得重要」的时刻进入上下文，而是按「消费方要用」的时刻进入。

上一篇的结尾说，最好的工具面是你感觉不到的工具面。拉式披露就是达成它的路径：不是隐藏信息，而是把信息的暴露对齐到使用的时刻。--help 不上税，不意味着信息免费——意味着你只为真正读它的那一眼付钱。
