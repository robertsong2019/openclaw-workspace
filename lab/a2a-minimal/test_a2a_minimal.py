"""a2a_minimal 测试套件 — unittest, 零依赖（与项目哲学一致）。

覆盖：TaskStore / AgentExecutor 单元测试 + HTTP E2E（discover、
message/send 多轮、tasks/get、tasks/cancel、错误路径）+ 健壮性
（malformed JSON 必须返回 JSON-RPC 错误而非断连）。

运行: python3 -m unittest test_a2a_minimal -v
"""

import json
import socket
import threading
import unittest
from http.server import HTTPServer
from urllib.request import Request, urlopen

from a2a_minimal import A2AClient, A2AHandler, AGENT_CARD, AgentExecutor, TaskStore


# ============================================================
# TaskStore 单元测试
# ============================================================

class TaskStoreTest(unittest.TestCase):
    def setUp(self):
        self.store = TaskStore()

    def test_create_defaults(self):
        task = self.store.create()
        self.assertEqual(task["status"], "submitted")
        self.assertEqual(task["messages"], [])
        self.assertEqual(task["artifacts"], [])
        self.assertTrue(task["id"])  # uuid 非空
        self.assertIn("createdAt", task)

    def test_create_explicit_id(self):
        task = self.store.create(task_id="t-1")
        self.assertEqual(task["id"], "t-1")
        self.assertIs(self.store.get("t-1"), task)

    def test_get_missing_returns_none(self):
        self.assertIsNone(self.store.get("no-such-task"))

    def test_update_status_existing(self):
        self.store.create(task_id="t-2")
        updated = self.store.update_status("t-2", "completed")
        self.assertEqual(updated["status"], "completed")
        self.assertEqual(self.store.get("t-2")["status"], "completed")

    def test_update_status_missing_returns_none(self):
        self.assertIsNone(self.store.update_status("ghost", "cancelled"))


# ============================================================
# AgentExecutor 单元测试
# ============================================================

class AgentExecutorTest(unittest.TestCase):
    def setUp(self):
        self.executor = AgentExecutor()

    def test_execute_echo_and_reverse(self):
        task = {"status": "submitted", "messages": [], "artifacts": []}
        results = self.executor.execute(task, [{"kind": "text", "text": "abc"}])
        self.assertEqual(task["status"], "completed")
        self.assertEqual(results, [
            {"kind": "text", "text": "Echo: abc"},
            {"kind": "text", "text": "Reverse: cba"},
        ])

    def test_execute_appends_incrementing_artifacts(self):
        task = {"status": "submitted", "messages": [], "artifacts": []}
        self.executor.execute(task, [{"kind": "text", "text": "a"}])
        self.executor.execute(task, [{"kind": "text", "text": "b"}])
        self.assertEqual([a["index"] for a in task["artifacts"]], [0, 1])
        self.assertEqual(len(task["artifacts"][1]["parts"]), 2)

    def test_execute_empty_parts_completes(self):
        task = {"status": "submitted", "messages": [], "artifacts": []}
        results = self.executor.execute(task, [])
        self.assertEqual(results, [])
        self.assertEqual(task["status"], "completed")

    def test_reverse_unicode_codepoints(self):
        task = {"status": "submitted", "messages": [], "artifacts": []}
        results = self.executor.execute(task, [{"kind": "text", "text": "你好"}])
        self.assertEqual(results[1]["text"], "Reverse: 好你")


# ============================================================
# HTTP E2E — 真实服务器（随机端口、后台线程）
# ============================================================

class ServerE2ETest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), A2AHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.port}"
        cls.client = A2AClient(cls.base)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        A2AHandler.store.tasks.clear()

    # ---- helpers ----

    def post_raw(self, payload: bytes):
        req = Request(f"{self.base}/", data=payload,
                      headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=3) as resp:
            return json.loads(resp.read())

    def rpc(self, method, params, req_id=1):
        return self.post_raw(json.dumps({
            "jsonrpc": "2.0", "method": method, "params": params, "id": req_id,
        }).encode())

    # ---- 发现 ----

    def test_discover_agent_card(self):
        card = self.client.discover()
        self.assertEqual(card["name"], "EchoAgent")
        self.assertEqual([s["id"] for s in card["skills"]], ["echo", "reverse"])
        self.assertIn("capabilities", card)

    def test_get_unknown_path_404(self):
        req = Request(f"{self.base}/nope")
        try:
            with urlopen(req, timeout=3) as resp:
                status, body = resp.status, json.loads(resp.read())
        except Exception as e:  # HTTPError 带 body
            status, body = e.code, json.loads(e.read())
        self.assertEqual(status, 404)
        self.assertIn("error", body)

    # ---- message/send 生命周期 ----

    def test_send_message_roundtrip(self):
        resp = self.client.send_message("hello")
        result = resp["result"]
        self.assertEqual(result["status"], "completed")
        texts = [p["text"] for a in result["artifacts"] for p in a["parts"]]
        self.assertEqual(texts, ["Echo: hello", "Reverse: olleh"])
        self.assertTrue(resp["id"])  # envelope id 回显非空

    def test_multi_turn_task_accumulates(self):
        tid = "task-multi"
        self.client.send_message("one", task_id=tid)
        self.client.send_message("two", task_id=tid)
        got = self.client.get_task(tid)["result"]
        self.assertEqual(len(got["messages"]), 2)
        self.assertEqual([a["index"] for a in got["artifacts"]], [0, 1])

    def test_get_task_unknown_error(self):
        resp = self.rpc("tasks/get", {"id": "ghost"}, req_id=7)
        self.assertEqual(resp["error"]["code"], -32602)
        self.assertEqual(resp["id"], 7)

    def test_cancel_task(self):
        # cancel 的真实使用场景是打断 in-flight 任务：直接 seed 一个
        # working 状态任务（同步 executor 下走 HTTP 的任务发出即完成，
        # 无法从外部观察到 working 窗口）。
        task = A2AHandler.store.create("task-c")
        task["status"] = "working"
        resp = self.client.cancel_task("task-c")
        self.assertEqual(resp["result"]["status"], "cancelled")
        got = self.client.get_task("task-c")["result"]
        self.assertEqual(got["status"], "cancelled")

    def test_cancel_unknown_error(self):
        resp = self.rpc("tasks/cancel", {"id": "ghost"}, req_id=8)
        self.assertEqual(resp["error"]["code"], -32602)

    def test_unknown_method_error(self):
        resp = self.rpc("math/add", {"a": 1, "b": 2}, req_id=9)
        self.assertEqual(resp["error"]["code"], -32601)
        self.assertIn("math/add", resp["error"]["message"])

    def test_agent_card_mutation_isolation(self):
        """AGENT_CARD 是模块级 dict：只读发现不应被请求改动。"""
        before = AGENT_CARD["name"]
        self.client.discover()
        self.assertEqual(AGENT_CARD["name"], before)


# ============================================================
# 健壮性 — malformed 请求必须得到 JSON-RPC 错误而非断连
# （red-verified: 修复前 4 类垃圾输入全部 RemoteDisconnected）
# ============================================================

class MalformedRequestTest(ServerE2ETest):
    def assert_rpc_error(self, payload, code):
        resp = self.post_raw(payload)
        self.assertIn("error", resp)
        self.assertEqual(resp["error"]["code"], code)
        self.assertIsNone(resp["id"])

    def test_invalid_json_parse_error(self):
        self.assert_rpc_error(b"{not json", -32700)

    def test_empty_body_parse_error(self):
        self.assert_rpc_error(b"", -32700)

    def test_non_dict_json_invalid_request(self):
        self.assert_rpc_error(b"[1,2,3]", -32600)

    def test_json_null_invalid_request(self):
        self.assert_rpc_error(b"null", -32600)

    def test_server_alive_after_garbage(self):
        self.post_raw(b"[1,2,3]")
        resp = self.rpc("tasks/get", {"id": "ghost"}, req_id=10)
        self.assertEqual(resp["error"]["code"], -32602)
        self.assertEqual(resp["id"], 10)

    # ---- Content-Length 头本身的垃圾（非整数/负数）----

    def send_raw_socket(self, payload: bytes, timeout=3.0) -> bytes:
        """绕过 http.client 自动补头，原样发送字节，收齐响应（连接关/超时/完整）。"""
        with socket.create_connection(("127.0.0.1", self.port), timeout=timeout) as s:
            s.sendall(payload)
            chunks = []
            while True:
                try:
                    data = s.recv(65536)
                except socket.timeout:
                    break
                if not data:
                    break
                chunks.append(data)
        return b"".join(chunks)

    def raw_post(self, headers: str, body: bytes = b"") -> dict:
        raw = self.send_raw_socket(
            f"POST / HTTP/1.1\r\nHost: t\r\nContent-Type: application/json\r\n"
            f"{headers}\r\n".encode() + body
        )
        self.assertTrue(raw, "服务器无响应（handler 崩溃断连或挂起）")
        head, _, body_raw = raw.partition(b"\r\n\r\n")
        self.assertIn(b"200 OK", head, head)
        return json.loads(body_raw)

    def test_content_length_non_integer_gets_error(self):
        resp = self.raw_post("Content-Length: abc\r\n")
        self.assertEqual(resp["error"]["code"], -32600)
        self.assertIsNone(resp["id"])

    def test_content_length_negative_gets_error_not_hang(self):
        resp = self.raw_post("Content-Length: -5\r\n")
        self.assertEqual(resp["error"]["code"], -32600)

    def test_server_alive_after_bad_header(self):
        self.raw_post("Content-Length: abc\r\n")
        resp = self.rpc("tasks/get", {"id": "ghost"}, req_id=11)
        self.assertEqual(resp["error"]["code"], -32602)
        self.assertEqual(resp["id"], 11)


# ============================================================
# 终态语义 — cancel 不得改写终态、cancelled 任务不得被复活
# （red-verified: 修复前 cancel 已完成任务"成功"改写状态、
#   已取消任务再收消息被静默复活为 completed）
# ============================================================


class RequestShapeHardeningTest(ServerE2ETest):
    """垃圾输入防御家族的更深层：params 非对象、message/parts 形状错误
    必须回 -32602 而非 AttributeError 崩 handler；Content-Length 必须有
    上界（无界 read = 阻塞 DoS）。"""

    def test_params_non_dict_gets_error_not_crash(self):
        resp = self.post_raw(json.dumps({"jsonrpc": "2.0",
                                         "method": "message/send",
                                         "params": "garbage", "id": 1}).encode())
        self.assertEqual(resp["error"]["code"], -32602)
        self.assertEqual(self.client.discover()["name"], "EchoAgent")

    def test_message_non_dict_gets_error_not_crash(self):
        resp = self.rpc("message/send", {"message": "just a string"}, req_id=2)
        self.assertEqual(resp["error"]["code"], -32602)

    def test_parts_non_list_gets_error_not_crash(self):
        resp = self.rpc("message/send",
                        {"message": {"role": "user", "parts": "not-a-list"}},
                        req_id=3)
        self.assertEqual(resp["error"]["code"], -32602)

    def test_part_non_dict_skipped_not_crash(self):
        resp = self.rpc("message/send",
                        {"message": {"role": "user",
                                     "parts": [123, {"kind": "text", "text": "hi"}]}},
                        req_id=4)
        self.assertEqual(resp["result"]["status"], "completed")
        texts = [p["text"] for a in resp["result"]["artifacts"] for p in a["parts"]]
        self.assertEqual(texts, ["Echo: hi", "Reverse: ih"])

    def test_oversized_content_length_rejected_immediately(self):
        sock = socket.create_connection(("127.0.0.1", self.port), timeout=3)
        sock.sendall(
            f"POST / HTTP/1.1\r\nHost: t\r\nContent-Type: application/json\r\n"
            f"Content-Length: {2 * 1024 * 1024}\r\n\r\n".encode())
        sock.settimeout(3)
        data = b""
        try:
            while b"too large" not in data and len(data) < 65536:
                chunk = sock.recv(65536)
                if not chunk:
                    break
                data += chunk
        except socket.timeout:
            pass
        sock.close()
        self.assertIn("-32600", data.decode())
        self.assertIn("too large", data.decode())


class TerminalStateTest(ServerE2ETest):
    def seed_working(self, tid):
        task = A2AHandler.store.create(tid)
        task["status"] = "working"
        return task

    def test_cancel_completed_task_rejected(self):
        self.client.send_message("done work", task_id="t-done")  # 同步执行 → completed
        resp = self.client.cancel_task("t-done")
        self.assertEqual(resp["error"]["code"], -32602)
        self.assertIn("completed", resp["error"]["message"])
        got = self.client.get_task("t-done")["result"]
        self.assertEqual(got["status"], "completed")  # 状态未被改写

    def test_double_cancel_rejected(self):
        self.seed_working("t-c")
        first = self.client.cancel_task("t-c")
        self.assertEqual(first["result"]["status"], "cancelled")
        second = self.client.cancel_task("t-c")
        self.assertEqual(second["error"]["code"], -32602)

    def test_cancelled_task_rejects_send_no_resurrection(self):
        self.seed_working("t-x")
        self.client.cancel_task("t-x")
        resp = self.client.send_message("sneak back", task_id="t-x")
        self.assertEqual(resp["error"]["code"], -32602)
        got = self.client.get_task("t-x")["result"]
        self.assertEqual(got["status"], "cancelled")
        self.assertEqual(len(got["messages"]), 0)  # 消息未入历史
        self.assertEqual(got["artifacts"], [])  # 未产生新产物

    def test_completed_task_still_accepts_multiturn(self):
        # completed 非终态封锁面：多轮续聊是已 pin 的行为，保持不变
        self.client.send_message("one", task_id="t-m")
        resp = self.client.send_message("two", task_id="t-m")
        self.assertEqual(resp["result"]["status"], "completed")


if __name__ == "__main__":
    unittest.main()
