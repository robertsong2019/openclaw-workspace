#!/usr/bin/env python3
"""
客户端健壮性测试（RED-first）

三个目标：
1. MCP 规范握手：initialize 响应后客户端必须发送 notifications/initialized
   （当前实现是 return 后的死代码，从未发出——不符合规范的 server 会拒绝后续请求）
2. stderr 管道死锁：server 往 stderr 写大量日志（MCP stdio server 的标准做法）时，
   64KB pipe 缓冲区填满 → server 阻塞 → 永远等不到响应
3. die-after-init：server 在 initialize 后立即退出的健壮性契约
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from mcp_client import MCPClient

DIR = Path(__file__).parent

INIT_OK = {
    "jsonrpc": "2.0",
    "id": "1",
    "result": {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "fake", "version": "0.0"},
    },
}


class FakeServerScript:
    """用 -c 内联脚本当 server，行为完全可控"""

    def __init__(self, script: str, env: dict | None = None):
        self.cmd = [sys.executable, "-c", script]
        self.extra_env = env or {}


# 脚本 1：记录是否收到 notifications/initialized（写标记文件）
RECORDER_SCRIPT = r"""
import sys, json, os
mark = os.environ["INIT_MARK_FILE"]
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        msg = json.loads(line)
    except Exception:
        continue
    m = msg.get("method")
    if m == "initialize":
        resp = dict(INIT_OK_PLACEHOLDER)
        resp["id"] = msg.get("id")
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()
    elif m == "notifications/initialized":
        with open(mark, "w") as f:
            f.write("ok")
    elif m == "tools/list":
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg.get("id"),
                                     "result": {"tools": []}}) + "\n")
        sys.stdout.flush()
""".replace("INIT_OK_PLACEHOLDER", json.dumps(INIT_OK))

# 脚本 2：启动时先向 stderr 写 200KB（填满 pipe 缓冲区）再服务请求
STDERR_FLOOD_SCRIPT = r"""
import sys, json
sys.stderr.write("x" * 200000)
sys.stderr.flush()
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
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg.get("id"),
                                     "result": {}}) + "\n")
        sys.stdout.flush()
""".replace("INIT_OK_PLACEHOLDER", json.dumps(INIT_OK))

# 脚本 3：initialize 后立即退出（模拟易死 server）
DIE_AFTER_INIT_SCRIPT = r"""
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
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()
        sys.exit(0)
""".replace("INIT_OK_PLACEHOLDER", json.dumps(INIT_OK))


def test_client_sends_initialized_notification_per_spec(tmp_path, monkeypatch):
    """规范握手：initialize 响应后必须发出 notifications/initialized 通知"""
    mark = tmp_path / "initialized_received"
    monkeypatch.setenv("INIT_MARK_FILE", str(mark))
    client = MCPClient(FakeServerScript(RECORDER_SCRIPT).cmd, request_timeout=3)
    try:
        assert client.start() is True
        client.list_tools()  # 触发后续请求
        deadline = time.time() + 2.0
        while time.time() < deadline and not mark.exists():
            time.sleep(0.02)
        assert mark.exists(), (
            "client never sent notifications/initialized after handshake "
            "(dead code after return in _initialize)"
        )
    finally:
        client.stop()


def test_stderr_flood_does_not_deadlock_client():
    """server 写 200KB stderr 不得让客户端死锁——这是 MCP stdio server 的标准日志通道"""
    client = MCPClient(FakeServerScript(STDERR_FLOOD_SCRIPT).cmd, request_timeout=3)
    try:
        assert client.start() is True, (
            "initialize deadlocked: server blocked writing stderr (pipe full) "
            "and client never drains it"
        )
    finally:
        client.stop()


def test_die_after_init_start_still_succeeds():
    """server 在 initialize 后立即退出：start() 必须仍返回 True（initialize 确实成功了），
    后续请求优雅返回空而不是抛异常"""
    client = MCPClient(FakeServerScript(DIE_AFTER_INIT_SCRIPT).cmd, request_timeout=3)
    try:
        assert client.start() is True
        assert client.list_tools() == []  # 不抛 BrokenPipeError
    finally:
        client.stop()
