#!/usr/bin/env python3
"""校验 JSON 文件合法性并打印指定字段的值；非法 JSON / 缺 key 时非零退出。"""
import json
import sys

with open(sys.argv[1]) as fh:
    data = json.load(fh)
print(data[sys.argv[2]])
