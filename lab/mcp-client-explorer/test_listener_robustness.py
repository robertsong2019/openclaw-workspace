#!/usr/bin/env python3
"""
客户端监听线程健壮性 + stop/上下文管理器契约（RED-first）

目标缺口（09-15 覆盖率扫描，mcp_client.py 85.4%）：
1. RED：server stdout 打印"合法 JSON 但非 dict"的行（调试打印数组/字符串是真实世界
   常态）→ _listen_responses 的 response.get() 抛 AttributeError（只捕了
   JSONDecodeError）→ 监听线程静默死亡 → 之后所有请求永久超时（silent-hang 家族）
2. 纯文本/空行容错（已有处理逻辑，特性化测试）
3. start() Popen 异常路径（命令不存在 → False 而非崩溃）
4. stop() 杀伤升级（server 无视 SIGTERM → 必须 SIGKILL 收尾，不留僵尸）
5. with 上下文管理器（完全无测试）
6. list_resources/list_prompts 对 JSON-RPC error 响应 → [] 契约
"""

import json
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from mcp_client import MCPClient


def listener_alive(client: MCPClient) -> bool:
    """诊断：_listen_responses 线程是否还活着（线程死亡 = 之后所有请求永久超时）"""
    return any(
        t.is_alive() and getattr(t, "_target", None) == client._listen_responses
        for t in threading.enumerate()
    )


def assert_fast_response(client: MCPClient, call, max_seconds: float = 1.0):
    """红/绿可区分的 observable：list_* 成功与超时都返回 []（List[Tool] 契约），
    唯一行为差异是延迟——监听线程死了每次调用烧满 request_timeout，活着则毫秒级"""
    t0 = time.time()
    result = call()
    elapsed = time.time() - t0
    assert elapsed < max_seconds, (
        f"request took {elapsed:.2f}s (>= timeout) — listener thread likely dead; "
        f"alive={listener_alive(client)}"
    )
    return result

INIT_OK = {
    "jsonrpc": "2.0",
    "id": "1",
    "result": {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}, "prompts": {}},
        "serverInfo": {"name": "fake", "version": "0.0"},
    },
}


def make_server(script: str) -> list:
    return [sys.executable, "-c", script]


# （compile 语法防线在文件末尾所有脚本定义之后）


# 对每个请求：先打印一行"垃圾"（str(EXPR_PLACEHOLDER) 的结果），再给真实响应。
# EXPR 是在 server 进程内求值的 Python 表达式：
#   [1, 2, 3]                  -> str() 即合法 JSON 行（list 的 str == json.dumps）
#   json.dumps("...")          -> 合法 JSON 字符串行
#   "plain text"               -> 纯文本（非法 JSON，走 JSONDecodeError 路径）
# 若客户端监听线程被垃圾行杀死，真实响应将永远无人处理 → 请求超时返回 None
GARBAGE_THEN_SERVE = r"""
import sys, json
def serve(msg):
    resp = {"jsonrpc": "2.0", "id": msg.get("id"), "result": {}}
    if msg.get("method") == "tools/list":
        resp["result"] = {"tools": []}
    elif msg.get("method") == "prompts/list":
        resp["result"] = {"prompts": []}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        msg = json.loads(line)
    except Exception:
        continue
    if msg.get("method") == "initialize":
        resp = dict(INIT_OK_PLACEHOLDER)
        resp["id"] = msg.get("id")
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()
    else:
        sys.stdout.write(str(EXPR_PLACEHOLDER) + "\n")
        sys.stdout.flush()
        serve(msg)
""".replace("INIT_OK_PLACEHOLDER", json.dumps(INIT_OK))

# 纯文本垃圾 + 空行（JSONDecodeError / 空行跳过路径——已实现，特性化）
PLAIN_GARBAGE_THEN_SERVE = GARBAGE_THEN_SERVE.replace(
    "EXPR_PLACEHOLDER", '"this is not json at all"')

# 合法 JSON 但非 dict：数组（调试打印一个 list 的真实场景）
LIST_GARBAGE_THEN_SERVE = GARBAGE_THEN_SERVE.replace(
    "EXPR_PLACEHOLDER", "[1, 2, 3]")

# 合法 JSON 但非 dict：字符串（json.dumps 过的调试输出是合法 JSON 行）
STRING_GARBAGE_THEN_SERVE = GARBAGE_THEN_SERVE.replace(
    'EXPR_PLACEHOLDER', 'json.dumps("debug: state=" + "x" * 20)')

# error 响应专用 server：list 类请求一律回 JSON-RPC error
ALWAYS_ERROR_SCRIPT = r"""
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        msg = json.loads(line)
    except Exception:
        continue
    if msg.get("method") == "initialize":
        resp = dict(INIT_OK_PLACEHOLDER)
        resp["id"] = msg.get("id")
    else:
        resp = {"jsonrpc": "2.0", "id": msg.get("id"),
                "error": {"code": -32601, "message": "method not found"}}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()
""".replace("INIT_OK_PLACEHOLDER", json.dumps(INIT_OK))

# 无视 SIGTERM 的 server（terminate 杀不死，必须升级 SIGKILL）
SIGTERM_IGNORER = r"""
import sys, json, signal, time
signal.signal(signal.SIGTERM, lambda *a: None)
def serve(msg):
    resp = {"jsonrpc": "2.0", "id": msg.get("id"), "result": {}}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        msg = json.loads(line)
    except Exception:
        continue
    if msg.get("method") == "initialize":
        resp = dict(INIT_OK_PLACEHOLDER)
        resp["id"] = msg.get("id")
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()
    else:
        serve(msg)
""".replace("INIT_OK_PLACEHOLDER", json.dumps(INIT_OK))


# 生成的 server 脚本必须可编译——占位符替换后的语法防线
# （前科：占位符替换出非法 Python → server 崩溃/启动失败 → 红的原因归因错到被测对象头上）
for _s in (GARBAGE_THEN_SERVE, PLAIN_GARBAGE_THEN_SERVE, LIST_GARBAGE_THEN_SERVE,
           STRING_GARBAGE_THEN_SERVE, ALWAYS_ERROR_SCRIPT, SIGTERM_IGNORER):
    compile(_s, "<generated-server>", "exec")


def test_listener_survives_valid_json_list_line():
    """RED：server stdout 的合法 JSON 数组行不得杀死监听线程。

    旧行为：response.get("id") 对 list 抛 AttributeError（只捕 JSONDecodeError）
    → 线程死 → 同一请求的真实响应无人处理 → None，且之后所有请求永久超时。
    """
    client = MCPClient(make_server(LIST_GARBAGE_THEN_SERVE), request_timeout=2)
    try:
        assert client.start() is True
        tools = assert_fast_response(client, client.list_tools)
        assert tools == []
        assert listener_alive(client), "listener thread died on [1, 2, 3] stdout line"
        # 线程死后第二个请求也会永久超时——双保险断言
        prompts = assert_fast_response(client, client.list_prompts)
        assert prompts == []
    finally:
        client.stop()


def test_listener_survives_valid_json_string_line():
    """RED：合法 JSON 字符串行（json.dumps 过的调试输出）同样不得杀死线程"""
    client = MCPClient(make_server(STRING_GARBAGE_THEN_SERVE), request_timeout=2)
    try:
        assert client.start() is True
        assert assert_fast_response(client, client.list_tools) == []
        assert listener_alive(client), "listener thread died on JSON-string stdout line"
    finally:
        client.stop()


def test_listener_tolerates_plain_text_and_blank_lines():
    """特性化：纯文本垃圾（JSONDecodeError 路径）与空行（跳过路径）本就该容忍"""
    client = MCPClient(make_server(PLAIN_GARBAGE_THEN_SERVE), request_timeout=2)
    try:
        assert client.start() is True
        assert assert_fast_response(client, client.list_tools) == []
        assert listener_alive(client)
    finally:
        client.stop()


def test_list_methods_map_jsonrpc_error_to_empty_list():
    """契约：list_resources/list_prompts 收到 error 响应 → [] 而非 None/抛异常"""
    client = MCPClient(make_server(ALWAYS_ERROR_SCRIPT), request_timeout=2)
    try:
        assert client.start() is True
        assert client.list_resources() == []
        assert client.list_prompts() == []
    finally:
        client.stop()


def test_start_popen_failure_returns_false_cleanly():
    """契约：命令不存在 → start() 捕获异常返回 False，不崩溃，可安全 stop"""
    client = MCPClient(["/nonexistent/binary-xyz-0915"])
    try:
        assert client.start() is False
        assert client.process is None
        assert client._initialized is False
        client.stop()  # 幂等：失败后 stop 不炸
    finally:
        client.stop()


def test_stop_escalates_to_kill_when_server_ignores_sigterm():
    """契约：server 无视 SIGTERM → stop() 升级 SIGKILL 并收尸，不留僵尸进程"""
    client = MCPClient(make_server(SIGTERM_IGNORER), request_timeout=2)
    assert client.start() is True
    proc = client.process
    t0 = time.time()
    client.stop()
    elapsed = time.time() - t0
    assert proc.poll() is not None, (
        "server ignored SIGTERM and survived stop() — kill escalation missing, "
        "zombie process left behind"
    )
    assert elapsed < 8.0, f"stop() took {elapsed:.1f}s against SIGTERM-ignorer"


def test_context_manager_starts_and_stops():
    """特性化：with 成功路径——进入即已启动，退出即回收进程"""
    with MCPClient(make_server(PLAIN_GARBAGE_THEN_SERVE), request_timeout=2) as c:
        assert c.start() is True or c.process is not None
        assert c.process is not None
        assert c._initialized is True
    assert c.process is None
    assert c._initialized is False


def test_context_manager_swallows_start_failure():
    """特性化（含 API 味道标注）：with 块吞掉 start() 的 False——
    调用方拿到一个 process=None 的死客户端而非异常。
    当前契约如此记录；若未来改为 raise RuntimeError 属行为变更，此处需同步更新。
    """
    with MCPClient(["/nonexistent/binary-xyz-0915"]) as c:
        assert c.process is None
        assert c._initialized is False
