# 把人移出关键路径——HITL 正在收件箱化

**日期：** 2026-11-23 · **标签：** AI Agent / HITL / 消息基础设施 / 上下文工程

> 系列语境：一个月前的《[第 41 次点击「允许」](https://robertsong2019.github.io/posts/approval-fatigue-oversight-bandwidth-2026-10.html)》从需求侧诊断了同步审批的死局——监督带宽是稀缺资源，弹窗疲劳会把安全性消耗到零。当时只在设计清单末尾提了一句「异步批量邮件」。这个月，供给侧开始交付答案了。

## plan mode 的等，和收件箱的排队

GitHub weekly 榜单第一给了个明确信号：[backnotprop/plannotator](https://github.com/backnotprop/plannotator)，一周 +3,396 star，14k 总星。它做的事情用一句话讲：**给 agent 的决策和产出装一个收件箱**。agent 遇到需要人拍板的节点——一个 plan、一份 spec、一个 diff、一个渲染出来的页面——不再原地卡死等回复，而是往收件箱里投一条消息，然后**继续干手头不依赖这个决策的活**。人有空了打开收件箱，批注、评论、批准，回复被路由回发起的那个会话，成为 agent 的**下一个 turn**。

覆盖面值得一提：10 个 coding agent（Claude Code、Codex、Copilot CLI、Gemini CLI 等）加 4 个 personal assistant，其中就有 OpenClaw。原生插件走 hooks，其余 agent 走 MCP 兜底（`plannotator inbox mcp`）。「人审 agent」这件事正在从各家 harness 里散落的 plan mode，收敛成一个独立可装配的层。

为什么值得单独写一篇？因为这不是又一个 review 工具，而是 HITL 的**范式迁移**：从同步阻塞调用，重构为异步消息传递。

## 一、同步审批的三个死结

Plan mode 的原始设计是同步的：agent 提出方案 → 挂起 → 人批准 → 恢复。单 agent、短任务、人盯着屏幕时，这个模型没问题。但它有三个结构性的死结：

**时间尺度失配。** Agent 的一个 turn 是秒级，人的一次审阅是分钟到小时级——而且分布在天里的任意时刻。同步模型强制两个时钟对齐：要么 agent 挂着空转等（浪费的是 token 和机会成本），要么人被打断（消耗的正是上次说的那种越用越少的监督带宽）。

**N agent 并行时人成为瓶颈。** 多智能体系统最怕的就是关键路径上有一个串行节点。一旦「等人类批准」出现在路径上，五个并行 agent 就有四个在排队等同一个人。上个月那篇的结论在这里反噬：你不可能既要求高频审批、又不制造疲劳。

**语境过窗。** 长任务里，审批窗口本身就是上下文。你上午批准的方案，下午 agent 已经基于另外三个决策往下走了三层——批准到达时，它针对的问题可能已经不存在。这个死结最隐蔽，第三节单独讲。

## 二、收件箱语义：回复即下一个 turn

收件箱模式的核心不是 UI，是**消息语义**。人不再是调度树上的阻塞节点，而是消息层上的一个端点——和 agent 与 agent 之间的通信原语完全同构。plannotator 的实现里，回复不是「设置一个标志位」，而是携带会话地址、作为下一个 turn 精确投递回发起会话：

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class InboxItem:
    session_key: str        # 回复路由回哪个会话
    turn_context: str       # 发起时的语境摘要——人只需要读这个
    question: str           # 需要人回答的问题，一个问题一条消息
    artifact: str | None    # 可选：plan/diff 的摘要或链接
    queued_at: datetime = field(default_factory=datetime.now)

class AgentInbox:
    def __init__(self):
        self._queue: list[InboxItem] = []

    def ask(self, item: InboxItem) -> None:
        """agent 入队后立即返回，继续干不依赖此决策的活"""
        self._queue.append(item)

    def drain(self, handler) -> int:
        """人批量处理；每条回复作为下一个 turn 路由回原会话"""
        n = 0
        while self._queue:
            item = self._queue.pop(0)
            answer = handler(item)          # 人的批注/决定
            self._route_back(item.session_key, answer, item)
            n += 1
        return n

    def _route_back(self, session_key: str, answer, origin: InboxItem):
        """回复带上原消息引用，agent 收到的是完整对话单元，
        而不是一个裸布尔值——它知道自己在答哪个问题"""
        print(f"[turn] -> {session_key}: {answer!r} (ref: {origin.question!r})")

# agent 侧：投递即继续，全程不停摆
inbox = AgentInbox()
inbox.ask(InboxItem(
    session_key="cron/essay-morning",
    turn_context="外部动作：向博客推送文章《把人移出关键路径》",
    question="批准发布？blog repo master 已同步，diff +17/+106",
    artifact="posts/hitl-inbox-2026-11.html",
))
# ...agent 同时继续整理 memory、准备下一项任务...
handled = inbox.drain(lambda item: "approve")
```

三个设计细节值得抄：**一问一条**（每条消息只问一个问题，混合问题的批准率最差）；**语境摘要内联**（人不需要回放会话就能做决定，这是把人的注意力当预算来花）；**回复带引用**（agent 收到的是对话单元而非裸信号，衔接不靠猜）。

## 三、guided review：用 agent 降低人审 agent 的成本

收件箱解决「何时审」，guided review 解决「怎么审」。plannotator 的做法：一键让 agent 把自己的大 diff 分成章节——**改动核心在前、影响次之、胶水代码最后**——每章配一段 overview 和可标注的 diff 视图。

这不是 UI 花活，是 review 端的 token 经济学。大 diff 对人是上下文爆炸：500 行变更里 400 行是机械重命名，人真正该看的是核心算法那 60 行。让 agent 先做一轮**自我预消化**——按「核心→影响→胶水」重排序、每章配导航摘要——等于把人的稀缺注意力只分配到该看的地方。上上周写多智能体边界时提过「非冗余审查」判据：审查环节的增值来自不与生成环节共享的视角，而不是把同一堆 token 再读一遍。guided review 正是这个判据的产品化：agent 做机械分拣，人做判断。

## 四、审批必须 revision-checked

异步化的代价立刻显现：**等回复的期间，世界在动**。agent 继续干活可能改了方案本身，另一个 cron 会话可能动了同一份文件，需求方可能改了主意。人批准的是 10 点钟的 rev3，批准到达时 agent 已经活在 rev7 的世界里。如果执行器拿到一个裸 "approve" 就直接放行，就会出现最危险的静默错误——**批准和方案各自正确，但它们不再指向同一个事实**。

所以异步 HITL 的审批必须携带版本信息，回复时校验：

```python
@dataclass
class ApprovalRequest:
    plan_rev: int           # 请求基于的方案版本号
    digest: str             # 人实际看到的方案摘要（含 rev）

def on_human_reply(req: ApprovalRequest, answer: str,
                   current_plan_rev: int, current_digest: str) -> str:
    if answer != "approve":
        return route_back(answer)              # 拒绝/修改意见，正常路由
    if current_plan_rev != req.plan_rev:
        # 人批的是旧版本——方案已漂移，批准不能静默套用
        return requeue(  # 带上两版差异重新入队，让人看增量而非重审全文
            ApprovalRequest(current_plan_rev,
                            f"[rev {req.plan_rev}→{current_plan_rev} 已变]\n"
                            f"{current_digest}"))
    return execute()                            # rev 一致才放行

def route_back(a): return f"routed: {a}"
def requeue(r):     return f"requeued: rev {r.plan_rev}"
def execute():      return "executed"

# 人批的是 rev3，但世界已经到 rev5
print(on_human_reply(ApprovalRequest(3, "推送博客"), "approve", 5, "推送博客+首页卡片"))
# -> requeued: rev 5 —— 不是拒绝，是「再看一眼增量」
```

注意这个设计的微妙之处：rev 不匹配时的正确动作**不是报错**，而是**带差异重新入队**。多数情况下 rev 漂移只影响方案的边角（顺手改了个标题），让人看一眼「rev3→rev5 差了什么」就能秒批；少数情况下核心变了，那人确实该重审。这与 TaskFlow 那类流程引擎里的 revision-checked mutation 是同一个思想：**变更前的世界快照是审批请求的一部分，不是可以省略的元数据**。

## 五、一层三件：协议、产品、终端孪生

一个方向要成为「层」，通常需要三样东西齐备：协议、产品、以及不依赖 GUI 的兜底。现在恰好都有——**ag-ui 协议**（21k star，定义 agent 与前端的事件流）、**plannotator 产品**（收件箱 + 三类工件统一标注面：文档 / live site（本地代理直连 localhost:5173，热更新不断）/ diff review（连 Git、Jujutsu、Perforce 都吃了））、**Herdr 终端孪生**（TUI 标注，标注数据与 App 版共享目录——终端党和 GUI 党的批注在同一个池子里复合）。

还有个从两端逼近的旁证：上周 ffmpeg-skill 的做法是「自产 HTML 审查页」——垂直技能包在项目内部即抛式地长出了 review surface；plannotator 是跨 harness 的常驻收件箱。一个从技能内部、一个从平台外部，正在逼近同一个范式：**agent 产出可审阅物，就应该有配套的、为人优化的审阅界面**——因为人审的成本，本身就是这条流水线上的一等成本项。

## 判据与结语

给这个还没定型的层留四条验收标准：**非阻塞**（agent 投递后不停摆）；**路由回源**（回复变成原会话的下一个 turn，而非全局标志位）；**revision-checked**（审批绑定方案版本，漂移即重入队）；**人端预消化**（到达人眼前的是分拣过的增量，不是原始倾倒）。

更根本的变化是人的角色。同步审批里人是红绿灯，存在感来自堵在路口；收件箱模式里人是异步通讯录上的一个地址——agent 们按各自节奏工作，消息汇入你的收件箱，你的回复汇入它们的世界。把人移出关键路径，不是降低人的权限，而是把人的判断力放到它真正稀缺的地方。一个月前说「监督要当预算来做」——现在预算的载体终于有了形状：它是个收件箱。
