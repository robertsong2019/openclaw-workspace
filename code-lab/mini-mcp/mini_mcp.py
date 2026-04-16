#!/usr/bin/env python3
"""
Mini-MCP: A lightweight tool registry & invocation framework.
Simulates core MCP (Model Context Protocol) concepts in ~150 lines.

Usage:
  python mini_mcp.py              # Start interactive REPL
  python mini_mcp.py --list       # List registered tools
  python mini_mcp.py --call <name> [json_args]  # Call a tool
"""

import json
import sys
import math
import datetime
import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class Tool:
    name: str
    description: str
    func: Callable
    parameters: dict = field(default_factory=dict)

    def invoke(self, **kwargs) -> Any:
        return self.func(**kwargs)

    def schema(self) -> dict:
        sig = inspect.signature(self.func)
        params = {}
        for pname, param in sig.parameters.items():
            ptype = "string"
            if param.annotation in (int, float):
                ptype = "number"
            elif param.annotation == bool:
                ptype = "boolean"
            elif param.annotation in (list, dict):
                ptype = "object"
            params[pname] = {
                "type": ptype,
                "description": self.parameters.get(pname, ""),
                "required": param.default is inspect.Parameter.empty,
            }
        return {
            "name": self.name,
            "description": self.description,
            "parameters": params,
        }


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, name: str, description: str = "", **param_descs):
        def decorator(func):
            self._tools[name] = Tool(
                name=name,
                description=description or func.__doc__ or "",
                func=func,
                parameters=param_descs,
            )
            return func
        return decorator

    def list_tools(self) -> list[dict]:
        return [t.schema() for t in self._tools.values()]

    def call(self, name: str, **kwargs) -> Any:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found. Available: {list(self._tools.keys())}")
        return self._tools[name].invoke(**kwargs)

    def interactive(self):
        print("🔧 Mini-MCP Tool Server")
        print(f"   {len(self._tools)} tools registered\n")
        self._print_help()
        while True:
            try:
                line = input("mcp> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Bye!")
                break
            if not line:
                continue
            parts = line.split(maxsplit=1)
            cmd = parts[0]
            if cmd in ("quit", "exit", "q"):
                print("👋 Bye!")
                break
            elif cmd == "help":
                self._print_help()
            elif cmd == "list":
                for s in self.list_tools():
                    print(f"  📌 {s['name']}: {s['description']}")
                    for pname, pinfo in s['parameters'].items():
                        req = " (required)" if pinfo['required'] else ""
                        print(f"      - {pname}: {pinfo['type']}{req}")
            elif cmd == "call":
                if len(parts) < 2:
                    print("Usage: call <tool_name> [json_args]")
                    continue
                call_parts = parts[1].split(maxsplit=1)
                tool_name = call_parts[0]
                args = json.loads(call_parts[1]) if len(call_parts) > 1 else {}
                try:
                    result = self.call(tool_name, **args)
                    print(f"  ✅ {json.dumps(result, indent=2, default=str, ensure_ascii=False)}")
                except Exception as e:
                    print(f"  ❌ {e}")
            elif cmd == "schema":
                if len(parts) > 1 and parts[1] in self._tools:
                    print(json.dumps(self._tools[parts[1]].schema(), indent=2))
                else:
                    print(f"Unknown tool. Available: {list(self._tools.keys())}")
            else:
                print(f"Unknown command: {cmd}. Type 'help'.")

    def _print_help(self):
        print("Commands: list | call <name> [json] | schema <name> | help | quit")


# --- Global registry ---
registry = ToolRegistry()


# --- Built-in tools ---
@registry.register("time", description="Get current date/time", timezone="IANA timezone string")
def get_time(timezone: str = "Asia/Shanghai") -> dict:
    """Return current time info."""
    import zoneinfo
    tz = zoneinfo.ZoneInfo(timezone)
    now = datetime.datetime.now(tz)
    return {
        "iso": now.isoformat(),
        "unix": int(now.timestamp()),
        "weekday": now.strftime("%A"),
        "formatted": now.strftime("%Y-%m-%d %H:%M:%S"),
    }


@registry.register("calc", description="Evaluate a math expression safely", expr="Math expression string")
def calculate(expr: str) -> dict:
    """Safe math evaluation."""
    allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
    allowed.update({"abs": abs, "round": round, "min": min, "max": max, "pow": pow})
    result = eval(expr, {"__builtins__": {}}, allowed)
    return {"expr": expr, "result": result, "type": type(result).__name__}


@registry.register("hash", description="Generate hash for a string", text="Input text", algorithm="md5|sha1|sha256")
def hash_text(text: str, algorithm: str = "sha256") -> dict:
    import hashlib
    h = hashlib.new(algorithm, text.encode())
    return {"input_length": len(text), "algorithm": algorithm, "hash": h.hexdigest()}


@registry.register("json_fmt", description="Format/validate JSON string", json_str="Raw JSON string")
def format_json(json_str: str) -> dict:
    parsed = json.loads(json_str)
    return {"valid": True, "formatted": json.dumps(parsed, indent=2, ensure_ascii=False), "keys": list(parsed.keys()) if isinstance(parsed, dict) else None}


@registry.register("color", description="Generate a random color palette", count="Number of colors (1-10)")
def color_palette(count: int = 5) -> dict:
    import random
    colors = []
    for _ in range(min(count, 10)):
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        colors.append({
            "hex": f"#{r:02x}{g:02x}{b:02x}",
            "rgb": f"rgb({r},{g},{b})",
            "luminance": round(0.299 * r + 0.587 * g + 0.114 * b, 1),
        })
    return {"count": len(colors), "colors": colors}


@registry.register("base64", description="Encode/decode base64", text="Input text", mode="encode|decode")
def base64_tool(text: str, mode: str = "encode") -> dict:
    import base64
    if mode == "encode":
        result = base64.b64encode(text.encode()).decode()
    else:
        result = base64.b64decode(text.encode()).decode()
    return {"mode": mode, "result": result}


@registry.register("stats", description="Compute basic statistics for a list of numbers", numbers="JSON array of numbers")
def compute_stats(numbers: list) -> dict:
    n = len(numbers)
    mean = sum(numbers) / n
    sorted_n = sorted(numbers)
    median = sorted_n[n // 2] if n % 2 else (sorted_n[n // 2 - 1] + sorted_n[n // 2]) / 2
    variance = sum((x - mean) ** 2 for x in numbers) / n
    return {
        "count": n,
        "mean": round(mean, 4),
        "median": round(median, 4),
        "stddev": round(math.sqrt(variance), 4),
        "min": min(numbers),
        "max": max(numbers),
    }


# --- CLI ---
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        registry.interactive()
    elif args[0] == "--list":
        for s in registry.list_tools():
            print(f"  {s['name']}: {s['description']}")
    elif args[0] == "--call" and len(args) >= 2:
        name = args[1]
        call_args = json.loads(args[2]) if len(args) > 2 else {}
        result = registry.call(name, **call_args)
        print(json.dumps(result, indent=2, default=str, ensure_ascii=False))
    else:
        print(__doc__)
