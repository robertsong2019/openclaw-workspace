#!/usr/bin/env python3
"""
tools/call 与 prompts/get 的 arguments 形状门（RED-first 2026-09-26）

缺口：_handle_request 顶部已有 params 非 dict → -32602 门，但 method 层的
arguments 形状不一致：
- tools/call: arguments=list/str/int → args["op"] TypeError 被捕获 → -32603
  "list indices must be integers"（Internal error 语义 + 内部异常消息泄漏；
  参数形状错是 -32602 Invalid params，-32603 留给真正的工具执行失败）
- prompts/get: arguments 非 dict → args.get() AttributeError → -32602 但消息
  泄漏 "'str' object has no attribute 'get'"

统一为 -32602 "Invalid params: expected object"（与顶部 params 门同语义）。
既有 pin test_null_arguments_still_responds 只断言 error 存在，null 归入
-32602 门不与其冲突（不静默的意图保留）。
"""

import json
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

DIR = Path(__file__).parent
SERVER_CMD = [sys.executable, "mcp_server.py"]


class RawServer:
    """与 mcp_server.py 子进程按 JSON-RPC 行协议通信（复用 explorer 套件模式）"""

    def __init__(self):
        self.p = subprocess.Popen(
            SERVER_CMD,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=DIR,
        )
        self._buf = []
        self._lock = threading.Lock()
        self._t = threading.Thread(target=self._read, daemon=True)
        self._t.start()

    def _read(self):
        for line in self.p.stdout:
            line = line.strip()
            if not line:
                continue
            with self._lock:
                self._buf.append(json.loads(line))

    def send(self, obj):
        self.p.stdin.write(json.dumps(obj) + "\n")
        self.p.stdin.flush()

    def recv(self, timeout=2.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            with self._lock:
                if self._buf:
                    return self._buf.pop(0)
            time.sleep(0.01)
        return None

    def request(self, obj, timeout=2.0):
        self.send(obj)
        return self.recv(timeout)

    def close(self):
        try:
            self.p.stdin.close()
        except Exception:
            pass
        self.p.terminate()
        try:
            self.p.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.p.kill()


@pytest.fixture
def server():
    s = RawServer()
    yield s
    s.close()


BAD_ARGUMENTS = [["not", "a", "dict"], "text-string", 42]


def test_tools_call_list_arguments_gets_32602(server):
    """arguments=list → -32602（旧实现 TypeError 捕获 → -32603 内部错误语义）"""
    for bad in BAD_ARGUMENTS:
        server.send({"jsonrpc": "2.0", "id": f"tc-{id(bad)}", "method": "tools/call",
                     "params": {"name": "calculate", "arguments": bad}})
        resp = server.recv(timeout=1.5)
        assert resp is not None, f"silent hang for arguments={bad!r}"
        assert resp["error"]["code"] == -32602, f"arguments={bad!r}"


def test_tools_call_bad_arguments_no_internal_leak(server):
    """-32602 门消息必须是校验消息，不得泄漏内部异常文本"""
    server.send({"jsonrpc": "2.0", "id": "tc-leak", "method": "tools/call",
                 "params": {"name": "reverse_string", "arguments": ["abc"]}})
    resp = server.recv(timeout=1.5)
    assert resp is not None
    assert resp["error"]["code"] == -32602
    assert "indices" not in resp["error"]["message"]


def test_prompts_get_bad_arguments_clean_32602(server):
    """prompts/get arguments=list/str/int → -32602 且消息不泄漏 AttributeError 文本"""
    for bad in BAD_ARGUMENTS:
        server.send({"jsonrpc": "2.0", "id": f"pg-{id(bad)}", "method": "prompts/get",
                     "params": {"name": "code_review", "arguments": bad}})
        resp = server.recv(timeout=1.5)
        assert resp is not None, f"silent hang for arguments={bad!r}"
        assert resp["error"]["code"] == -32602, f"arguments={bad!r}"
        assert "attribute" not in resp["error"]["message"]


def test_null_arguments_still_gets_error_response(server):
    """既有 pin 语义保留：arguments=null 仍回错误包（现归 -32602 门），不静默"""
    server.send({"jsonrpc": "2.0", "id": "null-1", "method": "tools/call",
                 "params": {"name": "calculate", "arguments": None}})
    resp = server.recv(timeout=1.5)
    assert resp is not None
    assert "error" in resp


def test_good_arguments_unaffected(server):
    """合法 arguments 行为零变化（门只挡形状错）"""
    server.send({"jsonrpc": "2.0", "id": "ok-1", "method": "tools/call",
                 "params": {"name": "calculate",
                            "arguments": {"operation": "add", "a": 2, "b": 3}}})
    resp = server.recv(timeout=1.5)
    assert resp is not None
    assert "error" not in resp
    assert json.loads(resp["result"]["content"][0]["text"]) == 5
