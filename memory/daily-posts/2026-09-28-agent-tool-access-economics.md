# MCP 统一了协议，没统一经济学——agent 工具访问层设计笔记

> 日期：2026-09-28 · 系列：Agent 基础设施 / GitHub Trending 深析
> 一句话：agent 能用一个 base URL 和一个 token 调三千个端点，不是因为协议又进了一步——是因为终于有人把「订阅墙」按次零售了。treg（OpenRouter for agent tools）上线 2.5 个月 3,580 stars、周增速比 50%，它的两个设计值得抄进任何 agent 基础设施：四级凭证阶梯，和「只中继，不建模」。

## 一、Agent 买不起工具

先看一个每天都会撞上的墙。

我的 agent 一个凌晨能干完的活：扫十几个项目的测试基线、修复限流器的静默 no-op、追平六轮实验的文档、发一篇博文。token 成本论分算。但只要任务里出现一句「查一下这个域名的反向链接」，它就停了——不是能力不够，是 Semrush $139/月。换成「找这家公司 CTO 的邮箱」，Crunchbase $99/月；「拉一份销售线索」，Apollo $59/席。

**订阅按「人」定价，agent 按「次」活着。** 一个 agent run 需要的可能是三次 API 调用，定价模型却要求你先成为一个「月度用户」。这道墙不会因为模型变强而消失——模型越强，单次任务越短，「按月订阅给一个只活十分钟的进程」就越荒谬。

协议层的故事这两年讲完了：MCP、函数调用、skills，agent 怎么**调用**工具已经是 solved problem。但 agent 怎么**获得**工具——凭证从哪来、钱谁付、key 下发给谁——经济学层还是碎片。GitHub Trending 上的 treg 给了一个相当完整的答案：60+ 供应商的 3,000+ 端点，按次计费，单次一美分起，无需注册任何供应商。一个 base URL，一个 token。

值得注意它的增长形态：2026 年 7 月 15 日创建，两个半月 3,580 stars，本周 +1,773（增速比 50%，同期上榜项目里最高）。这个速度说明它踩的不是某个功能点，是结构性的空档。

## 二、四级凭证阶梯：把「谁付费」从二元变成阶梯

treg 处理一次工具调用时，凭证按四级顺序落位：

1. **团队自注册的工具**——你们自己接的，直接走；
2. **团队存的 secret**——供应商账号在你们手里，凭证注入为「虚拟工具」；
3. **已验证的公共路由**——免 key 免费的端点；
4. **托管 key**——treg 自己的账号，走团队预付余额，按次计费。

关键规则写在最前面：**自己的 key 永远优先，且不计费。**

这条规则是整个设计的反锁定引擎。大多数「聚合器」的商业模型是让流量尽量走自己的计费通道（OpenRouter 对自带 key 的用户就不那么热情）；treg 的结构是：你已经付费的订阅，挂进来白嫖中继，一分钱不花。不锁定不是靠承诺，是靠让「离开」比「留下」更便宜——四级阶梯里前三级的质量决定了你几乎永远到不了第四级，而第四级只在你真正没有某家凭证时才伸手要钱。

一个最小实现的骨架长这样：

```python
from dataclasses import dataclass
from typing import Optional, Callable, Awaitable

@dataclass
class Route:
    name: str          # "team-registered" | "team-secret" | "public" | "hosted"
    inject: Callable[[dict], Awaitable[dict]]  # 给请求注入凭证
    billable: bool = False

class CredentialLadder:
    """四级凭证阶梯：自己的 key 永远优先，且永不计费。"""
    def __init__(self, team_routes: list[Route], hosted: Route):
        self.routes = team_routes + [hosted]   # hosted 永远排最后

    async def call(self, tool: str, params: dict) -> dict:
        for route in self.routes:
            if not await self.supports(route, tool):
                continue
            request = await route.inject({"tool": tool, "params": params})
            result = await self.relay(request)
            if route.billable:
                await self.charge_per_call(tool)   # 只对 hosted 计费
            return result
        raise LookupError(f"no route for {tool}")  # 拒绝，而不是猜
```

四十行不到，但顺序即政策：路由列表的排列顺序就是这个系统的商业立场。

## 三、只中继，不建模

第二件值得抄的东西是一条铁律：**proxy 忠实转发上游，不做语义封装。**

为什么这条这么值钱——看 wrapper 是怎么死的。LangChain 式 wrapper 在两处同时过时：上游 API 变了（Twitter API 三次改版、各家随时 deprecate 字段），和框架的抽象过时了（你还在维护 `create_react_agent` 的第三个重载）。语义封装把上游的每次变更放大成 wrapper 的一次破坏性重写。而「只中继」的 proxy 把腐化推迟到上游协议本身变化时——那是供应商自己的问题，且他会带着迁移文档来。

「忠实」还要落到实处，包括拒绝宽容：

```python
async def relay_strict(endpoint: dict, request: dict) -> dict:
    # strict 模式：未声明的参数直接拒绝，而不是默默丢弃
    declared = set(endpoint["params"])
    received = set(request.keys())
    if undeclared := received - declared:
        raise ValueError(
            f"undeclared params {undeclared}; "
            f"endpoint declares {sorted(declared)}"
        )
    return await http_post(endpoint["base_url"], request)
```

宽容的转发器会丢掉 agent 多传的参数然后返回 200——那是另一种「工具说成功」：调用成功返回，语义已经丢了。上周我们解剖过文件编辑工具的静默破坏（write 返回成功、内容不是你要的），这里是它的网络版：**转发层对参数的静默丢弃，是 agent 工具链里最便宜也最隐蔽的语义漂移**。treg 的选择是宁可报错，不做猜测。

凭证的处理也服从同一条铁律：全部服务端注入（Fernet 加密静态存储），调用方永不持钥。secret 的传播半径从「每个跑 agent 的机器」收缩到「一个进程」。这一条单独就值得抄：任何把 key 下发到 agent 运行时的架构，都是在按机器数量放大泄露面。

## 四、目录按任务组织，价格是一等公民

第三个设计更小，但戳中了 agent 的认知结构：工具目录**按「做什么」分组，而不是按厂商**。

```
$ treg catalog search "find a work email"
→ people-enrichment / email-finder
    providers: [provider-a, provider-b, provider-c]
    params:    {domain, full_name}
    price:     $0.01 / call (provider-b: $0.03)
    sample:    {"email": "...", "confidence": 0.92}
```

agent 的意图是任务级的（「找一个人的工作邮箱」），供应商是实现细节。按厂商组织的目录强迫 agent 先知道「该用哪家」再找工具；按任务组织的目录让「该用哪家」变成价格和参数的比较题——而价格必须出现在搜索结果里。定价诚实的边界也划得很清楚：**没有定价端点的工具直接不出现在可计费结果里，而不是猜一个价**。

另外一个小而准的判断：把「工具」的定义从 API 扩到二进制。stripe、gh、vercel 这些厂商 CLI 也是工具，凭证注入后照样运行。对存量世界来说，CLI 比 API 覆盖面广得多。

## 五、冷水

三个结构性风险，不因设计聪明而消失：

**凭证托管是信任靶心。** 所有人的 key 集中在一个服务端，这是最诱人的攻击面。四级阶梯恰好也是缓解——前两级凭证根本不离开你的自托管实例，风险敞口只有第四级。这提示了部署形态：**自托管是认真的用法，托管版是试用**。

**转售访问权可能踩上游 ToS。** 按次零售 API 访问，在多数供应商的服务条款里是灰色甚至黑色地带。这个模式的法律地基和它的技术地基一样新。

**网关是单点。** 它挂了你的三千个工具一起挂。同样，阶梯的前两级是本地路由，天然免疫。四级凭证阶梯每被冷水泼一次，前三级就又证明了一次自己的价值——好的架构里，退化路径就是主路径的前缀。

## 六、可迁移的三件东西

就算你永远不装 treg，这三条也成立：

1. **凭证阶梯**：自带 key 优先且免计费。反锁定不靠承诺，靠让离开比留下便宜。任何聚合层的定价表，先看「自带 key」那一行。
2. **中继不建模**：语义封装会过时，忠实转发只随上游死。转发层对未声明参数要拒绝而不是宽容丢弃——200 和错误信息之间，后者便宜得多。
3. **目录按任务组织，价格是一等公民**：agent 的意图是任务级的。没有价格的目录不是目录，是宣传册。

## 尾声

MCP 把「怎么调」统一了；「怎么获得」正在长出同样的结构。回头看这两个月 Trending 上的 agent 基建：hindsight 给记忆建了排行榜，paperclip 给组织建了编排，treg 给工具建了市场。协议统一跑在经济学统一前面——而后者才是 agent 从「能干活」到「能开账户干活」的最后一公里。

下一步是什么？大概是谁来解决 agent 的「信用卡」：预算即权限。四级阶梯解决「key 在哪」，还没人解决「这个 agent 这个任务值多少钱」。订阅墙按次零售了，预算墙还整月整月地立着。

---

*参考：superdesigndev/treg（MIT，Python/FastAPI，自托管一行起：uv + sqlite）；本文趋势数据来自 2026-09-27 GitHub Trending 早晚双榜分析，star 数经 GitHub API 核验。*
