#!/usr/bin/env python3
"""
Server-initiated request 处理（MCP 规范缺口，RED-first）

缺口：_listen_responses 只处理"响应"（id ∈ pending_requests）。server 主动发来的
请求（有 id + method：ping / sampling/createMessage / roots/list …）被静默丢弃：
- 规范要求 ping 的接收方必须尽快回空 result —— 沉默 = server 侧超时
- 客户端不支持的能力应回 -32601 Method not found —— 沉默 = server 永久等待
（silent-hang 家族的客户端侧镜像：以前是客户端等 server 响应，这次是 server 等客户端）

fake server 协议：argv[1]=回包落盘路径 argv[2]=探针请求 JSON。
时序：initialize 握手 → 收到 tools/list 后先发探针再回响应 → 从 stdin 读客户端
对探针的反应 → 落盘。测试断言落盘行。

覆盖：
1. ping → 回 {"result": {}}（spec MUST，内置处理）
2. 未注册方法 → -32601 Method not found
3. 注册 handler → params 进 / result 出（round-trip）
4. handler 抛异常 → -32603 Internal error
5. id=0（falsy id 陷阱：分发必须用 is not None，truthiness 会吞掉 id=0）
6. server 通知（有 method 无 id）不得触发任何回包 —— 探针后 server 读到的
   第一行必须是客户端的下一条真实请求（list_prompts），而非游离响应
"""

import json
import sys
import time
from pathlib import Path

import pytest

from mcp_client import MCPClient


def assert_fast_response(client: MCPClient, call, max_seconds: float = 2.0):
    """监听线程死亡时 list_* 会烧满 request_timeout；活着则毫秒级"""
    t0 = time.time()
    result = call()
    elapsed = time.time() - t0
    assert elapsed < max_seconds, (
        f"request took {elapsed:.2f}s — listener thread likely dead"
    )
    return result


def wait_for_file(path: Path, timeout: float = 3.0) -> str:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists():
            return path.read_text()
        time.sleep(0.02)
    raise AssertionError(f"server never wrote {path} within {timeout}s")


# 探针注入走 argv，脚本本身恒定 —— 模块级 compile() 语法防线一次覆盖全部测试
PROBE_SERVER = r"""
import sys, json, time
out_path, probe = sys.argv[1], json.loads(sys.argv[2])

def reply(msg, result):
    resp = {"jsonrpc": "2.0", "id": msg.get("id"), "result": result}
    sys.stdout.write(json.dumps(resp) + "\n"); sys.stdout.flush()

line = sys.stdin.readline()
msg = json.loads(line)
if msg.get("method") == "initialize":
    reply(msg, {"protocolVersion": "2024-11-05", "capabilities": {},
                "serverInfo": {"name": "fake", "version": "0"}})
sys.stdin.readline()  # notifications/initialized（无回包）

# tools/list：先发探针（server 主动请求/通知），再回响应
line = sys.stdin.readline()
msg = json.loads(line)
sys.stdout.write(json.dumps(probe) + "\n"); sys.stdout.flush()
reply(msg, {"tools": []})

# 读客户端的下一行：正确实现 = 客户端后续真实请求；错误实现 = 对通知的游离回包
line = sys.stdin.readline()
with open(out_path, "w") as f:
    f.write(line)
time.sleep(0.2)
"""


def make_server(out_path: Path, probe: dict) -> list:
    return [sys.executable, "-c", PROBE_SERVER, str(out_path), json.dumps(probe)]


def started_client(argv: list, **kw) -> MCPClient:
    client = MCPClient(argv, **kw)
    assert client.start(), "fake server failed to initialize"
    return client


def test_ping_gets_pong(tmp_path):
    out = tmp_path / "reply.json"
    client = started_client(make_server(out, {"jsonrpc": "2.0", "id": "srv-1",
                                              "method": "ping"}))
    try:
        assert_fast_response(client, client.list_tools) == []
        r = json.loads(wait_for_file(out))
        assert r["id"] == "srv-1"
        assert "result" in r and "error" not in r
    finally:
        client.stop()


def test_unknown_method_gets_32601(tmp_path):
    out = tmp_path / "reply.json"
    client = started_client(make_server(out, {"jsonrpc": "2.0", "id": "srv-2",
                                              "method": "sampling/createMessage",
                                              "params": {"messages": []}}))
    try:
        assert_fast_response(client, client.list_tools) == []
        r = json.loads(wait_for_file(out))
        assert r["id"] == "srv-2"
        assert r["error"]["code"] == -32601
        assert "sampling/createMessage" in r["error"]["message"]
    finally:
        client.stop()


def test_registered_handler_roundtrip(tmp_path):
    out = tmp_path / "reply.json"
    client = MCPClient(make_server(out, {"jsonrpc": "2.0", "id": "srv-3",
                                         "method": "sampling/createMessage",
                                         "params": {"messages": [{"role": "user",
                                                                  "content": "hi"}]}}))
    seen = {}

    def handler(params):
        seen.update(params)
        return {"role": "assistant", "model": "fake",
                "content": {"type": "text", "text": "pong"}}

    client.on_server_request("sampling/createMessage", handler)
    assert client.start()
    try:
        assert_fast_response(client, client.list_tools) == []
        assert "messages" in seen, "handler must receive server params"
        r = json.loads(wait_for_file(out))
        assert r["id"] == "srv-3"
        assert r["result"]["content"]["text"] == "pong"
        assert "error" not in r
    finally:
        client.stop()


def test_handler_exception_gets_32603(tmp_path):
    out = tmp_path / "reply.json"
    client = MCPClient(make_server(out, {"jsonrpc": "2.0", "id": "srv-4",
                                         "method": "sampling/createMessage",
                                         "params": {}}))
    def boom(params):
        raise ValueError("handler exploded")
    client.on_server_request("sampling/createMessage", boom)
    assert client.start()
    try:
        assert_fast_response(client, client.list_tools) == []
        r = json.loads(wait_for_file(out))
        assert r["error"]["code"] == -32603
        assert "handler exploded" in r["error"]["message"]
    finally:
        client.stop()


def test_falsy_id_zero_not_dropped(tmp_path):
    out = tmp_path / "reply.json"
    client = started_client(make_server(out, {"jsonrpc": "2.0", "id": 0,
                                              "method": "ping"}))
    try:
        assert_fast_response(client, client.list_tools) == []
        r = json.loads(wait_for_file(out))
        assert r["id"] == 0, "id=0 是 falsy 但必须原样回传（truthiness 分发陷阱）"
        assert "result" in r
    finally:
        client.stop()


def test_server_notification_gets_no_reply(tmp_path):
    out = tmp_path / "reply.json"
    # 探针是无 id 的通知；request_timeout 压短：第二条请求 server 不回，只做行源
    client = started_client(
        make_server(out, {"jsonrpc": "2.0", "method": "notifications/progress",
                          "params": {"progressToken": "t1", "progress": 1}}),
        request_timeout=1.5)
    try:
        assert_fast_response(client, client.list_tools) == []
        client.list_prompts()  # 供给 server 读的下一行；超时无响应无关断言
        nxt = json.loads(wait_for_file(out))
        assert nxt.get("method") == "prompts/list", (
            f"server 探针后读到的应是客户端下一条真实请求，却读到 {nxt} "
            "—— 通知被错误回了包，挤占了下一行"
        )
    finally:
        client.stop()


# 语法防线：所有内嵌 server 脚本必须可编译（占位符替换产物的非法 Python 会让
# server 启动即崩 → 红的原因归因错到被测对象头上）
compile(PROBE_SERVER, "PROBE_SERVER", "exec")
