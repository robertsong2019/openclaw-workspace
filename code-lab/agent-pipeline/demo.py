"""
🧪 Agent Pipeline — 轻量级 AI Agent 框架
演示核心概念: Chain, Router, Parallel, Loop, Memory
纯 Python 标准库实现
"""

from __future__ import annotations
import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Awaitable


# ─── Context & Memory ───────────────────────────────────────────────

@dataclass
class Memory:
    """短期记忆：键值存储 + 历史记录"""
    store: dict[str, Any] = field(default_factory=dict)
    history: list[dict] = field(default_factory=list)

    def set(self, key: str, value: Any) -> None:
        self.store[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.store.get(key, default)

    def log(self, entry: dict) -> None:
        entry.setdefault("_ts", time.time())
        self.history.append(entry)

    def recent(self, n: int = 5) -> list[dict]:
        return self.history[-n:]


@dataclass
class Context:
    """Agent 执行上下文"""
    data: Any = None
    memory: Memory = field(default_factory=Memory)
    meta: dict = field(default_factory=dict)
    run_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def clone(self, data: Any = None) -> "Context":
        return Context(
            data=data if data is not None else self.data,
            memory=self.memory,
            meta={**self.meta},
            run_id=self.run_id,
        )


# ─── Node Base ──────────────────────────────────────────────────────

NodeFunc = Callable[[Context], Awaitable[Any]]


class Node:
    """单个处理节点"""
    def __init__(self, name: str, fn: NodeFunc):
        self.name = name
        self.fn = fn

    async def run(self, ctx: Context) -> Context:
        result = await self.fn(ctx)
        ctx.memory.log({"node": self.name, "in": _summary(ctx.data), "out": _summary(result)})
        return ctx.clone(data=result)

    def __repr__(self):
        return f"Node({self.name})"


# ─── Composites ─────────────────────────────────────────────────────

class Chain:
    """串行管道：A → B → C"""
    def __init__(self, *nodes: Node, name: str = "chain"):
        self.nodes = nodes
        self.name = name

    async def run(self, ctx: Context) -> Context:
        for node in self.nodes:
            ctx = await node.run(ctx)
        return ctx


class Router:
    """条件路由：根据断言选择分支"""
    def __init__(self, predicate: Callable[[Context], str], branches: dict[str, Node], name: str = "router"):
        self.predicate = predicate
        self.branches = branches
        self.name = name

    async def run(self, ctx: Context) -> Context:
        key = self.predicate(ctx)
        branch = self.branches.get(key)
        if branch is None:
            raise ValueError(f"Router '{self.name}': no branch for key '{key}'")
        ctx.memory.log({"router": self.name, "chose": key})
        return await branch.run(ctx)


class Parallel:
    """并行执行，结果合并为列表"""
    def __init__(self, *nodes: Node, name: str = "parallel"):
        self.nodes = nodes
        self.name = name

    async def run(self, ctx: Context) -> Context:
        results = await asyncio.gather(*[n.run(ctx.clone(data=ctx.data)) for n in self.nodes])
        return ctx.clone(data=[r.data for r in results])


class Loop:
    """循环执行直到退出条件满足"""
    def __init__(self, body: Node, until: Callable[[Context, int], bool], max_iter: int = 10, name: str = "loop"):
        self.body = body
        self.until = until
        self.max_iter = max_iter
        self.name = name

    async def run(self, ctx: Context) -> Context:
        for i in range(self.max_iter):
            ctx = await self.body.run(ctx)
            if self.until(ctx, i):
                ctx.memory.log({"loop": self.name, "iterations": i + 1})
                return ctx
        ctx.memory.log({"loop": self.name, "iterations": self.max_iter, "warn": "hit max"})
        return ctx


# ─── Helpers ────────────────────────────────────────────────────────

def _summary(data: Any, max_len: int = 80) -> str:
    s = json.dumps(data, ensure_ascii=False, default=str)
    return s[:max_len] + ("…" if len(s) > max_len else "")


def node(name: str):
    """装饰器：快速创建节点"""
    def decorator(fn):
        async def wrapper(ctx: Context):
            return await fn(ctx)
        return Node(name, wrapper)
    return decorator


# ─── Demo ───────────────────────────────────────────────────────────

async def demo():
    print("🧪 Agent Pipeline Demo\n" + "=" * 40)

    # 1. 简单 Chain
    print("\n📋 1. Chain: 文本处理管道\n")

    n1 = Node("upper", lambda ctx: f"[UPPER] {str(ctx.data).upper()}")
    n2 = Node("reverse", lambda ctx: f"[REV] {str(ctx.data)[::-1]}")
    n3 = Node("count", lambda ctx: f"[LEN={len(str(ctx.data))}] {ctx.data}")

    # Wrap sync functions
    def make_node(name, fn):
        async def wrapper(ctx):
            return fn(ctx)
        return Node(name, wrapper)

    chain = Chain(
        make_node("upper", lambda c: str(c.data).upper()),
        make_node("tag", lambda c: f"📝 {c.data}"),
        make_node("count", lambda c: {"text": c.data, "chars": len(c.data)}),
        name="text-pipeline"
    )

    ctx = Context(data="hello agent pipeline")
    result = await chain.run(ctx)
    print(f"   输入: 'hello agent pipeline'")
    print(f"   输出: {result.data}")
    print(f"   记忆: {len(result.memory.history)} 条记录")

    # 2. Router
    print("\n🔀 2. Router: 智能路由\n")

    def sentiment_router(ctx: Context) -> str:
        text = str(ctx.data).lower()
        if any(w in text for w in ["好", "棒", "great", "love", "happy"]):
            return "positive"
        elif any(w in text for w in ["差", "坏", "bad", "hate", "sad"]):
            return "negative"
        return "neutral"

    branches = {
        "positive": make_node("😊", lambda c: f"正面情感! {c.data} → 回复: 感谢您的积极反馈!"),
        "negative": make_node("😢", lambda c: f"负面情感! {c.data} → 回复: 抱歉让您不满意，我们会改进。"),
        "neutral": make_node("😐", lambda c: f"中性情感! {c.data} → 回复: 感谢您的反馈。"),
    }

    router = Router(sentiment_router, branches, name="sentiment")

    for text in ["这个产品太棒了!", "体验很差", "今天天气不错"]:
        r = await router.run(Context(data=text))
        print(f"   '{text}' → {r.data}")

    # 3. Parallel
    print("\n⚡ 3. Parallel: 多角度分析\n")

    analysis = Parallel(
        make_node("word_count", lambda c: {"视角": "词数", "值": len(str(c.data).split())}),
        make_node("char_count", lambda c: {"视角": "字符数", "值": len(str(c.data))}),
        make_node("emoji_score", lambda c: {"视角": "表情密度", "值": sum(1 for ch in str(c.data) if ord(ch) > 0x1F000) / max(len(str(c.data)), 1)}),
        name="multi-analysis"
    )

    r = await analysis.run(Context(data="这个 AI Agent 🧪 框架太酷了 🚀"))
    for item in r.data:
        print(f"   {item}")

    # 4. Loop
    print("\n🔄 4. Loop: 迭代优化\n")

    counter = {"n": 0}

    def improve(ctx: Context):
        counter["n"] += 1
        return f"方案 v{counter['n']}: 准确率={60 + counter['n'] * 8}%"

    loop = Loop(
        make_node("improve", lambda c: improve(c)),
        until=lambda ctx, i: "准确率=9" in str(ctx.data) or "准确率=100" in str(ctx.data),
        max_iter=6,
        name="optimizer"
    )

    r = await loop.run(Context(data="start"))
    print(f"   最终: {r.data}")
    print(f"   迭代: {counter['n']} 次")

    # 5. 综合示例：Mini Agent
    print("\n🤖 5. 综合示例: Mini 问答 Agent\n")

    qa_chain = Chain(
        make_node("parse", lambda c: {"query": str(c.data), "type": "calc" if any(op in str(c.data) for op in "+-*/") else "chat"}),
        make_node("process", lambda c: (
            {"query": c.data["query"], "answer": eval(c.data["query"]), "confidence": 0.95}
            if c.data["type"] == "calc"
            else {"query": c.data["query"], "answer": "这是一个有趣的问题!", "confidence": 0.7}
        )),
        make_node("format", lambda c: f"🤖 Q: {c.data['query']}\n   A: {c.data['answer']} (置信度: {c.data['confidence']})"),
        name="qa-agent"
    )

    for q in ["2+3*4", "AI的未来是什么?", "100/5+3"]:
        r = await qa_chain.run(Context(data=q))
        print(f"   {r.data}\n")

    # Memory 摘要
    print("🧠 记忆摘要:")
    for entry in r.memory.recent(3):
        print(f"   [{entry.get('node', entry.get('router', entry.get('loop', '?')))}] {_summary(entry)}")

    print("\n✅ Demo 完成!")


if __name__ == "__main__":
    asyncio.run(demo())
