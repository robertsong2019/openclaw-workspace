#!/usr/bin/env python3
"""
示例Agent - 用于测试Edge Agent Dashboard
"""

import time
import random
import os
from datetime import datetime


def main():
    print("=" * 50)
    print("Example Agent Started!")
    print(f"PID: {os.getpid()}")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 50)

    count = 0
    while True:
        count += 1

        # 模拟正常日志
        print(f"[INFO] Processing cycle {count}")
        print(f"[INFO] CPU usage: {random.uniform(5, 30):.1f}%")
        print(f"[INFO] Memory: {random.uniform(100, 500):.1f}MB")

        # 模拟处理任务
        time.sleep(1)

        # 每10个周期输出一些调试信息
        if count % 10 == 0:
            print(f"[DEBUG] Completed {count} cycles")

        # 偶尔模拟警告
        if random.random() < 0.1:
            print(f"[WARN] High latency detected: {random.uniform(100, 500):.1f}ms")

        # 每30个周期输出摘要
        if count % 30 == 0:
            print(f"[SUMMARY] Processed {count} items successfully")

        # 永远运行（直到被Dashboard停止）
        if count >= 1000:
            # 重置计数器，避免整数溢出
            count = 0


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Agent stopped by user")
    except Exception as e:
        print(f"[ERROR] Agent crashed: {e}")
        raise
