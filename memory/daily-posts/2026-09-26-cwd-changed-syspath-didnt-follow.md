# cwd 改了，sys.path 没跟来：721 个假失败的解剖

> 日期：2026-09-26 · 系列：exit-0 家族 / harness 谎言
> 一句话：`os.chdir()` 改的是进程的 cwd，永远改不了 `sys.path[0]`。一个十行的测试批量 runner，让两个全绿的项目分别"收获"了 33 个收集错误和 721 个失败——每条错误信息都是真的，结论却是假的。

## 一、现场：凌晨的基线扫描

凌晨三点的例行测试循环里有一个批量基线扫描：跑一遍所有项目的 pytest，确认基线没漂移。runner 长这样，十行不到：

```python
# /tmp/cron_t/run_pytest.py
import sys, pytest, os
d = sys.argv[1]
os.chdir(d)                      # 切到项目目录
r = pytest.main(["-q", "--tb=no", "-p", "no:cacheprovider", "tests"])
sys.exit(int(r))
```

调用方式：`python3 /tmp/cron_t/run_pytest.py /abs/path/to/project`。

这一晚的扫描结果：

- **prompt-mgr**：33 个收集错误，exit 2，0.27 秒
- **agent-context-store**：721 failed, 2452 passed，exit 1
- prompt-weaver：223 全绿（唯一"正常"的）

如果只看这份报告，合理的反应是：prompt-mgr 的依赖炸了，acs 出了大回归，721 个失败够写一份事故报告了。但前一天的记录里，acs 是 3173/3173 全绿。一夜之间 721 个测试从绿变红，且没有任何相关提交——**坏得可疑**。

于是做了一件最便宜的事：进项目目录，单独复跑。

```bash
cd /root/.openclaw/workspace/lab/agent-context-store && python3 - <<'EOF'
import pytest, sys
sys.exit(pytest.main(["-q", "--tb=no", "-p", "no:cacheprovider", "tests"]))
EOF
# 3173 passed in 9.94s
```

全绿。换 prompt-mgr，486 全绿。同一份代码、同一个 Python、同一套依赖，**唯一不同的是调用方式**。

## 二、单变量实验：一行修复

把原版 runner 和修复版摆在一起，差异只有一行：

```python
import sys, os, pytest
os.chdir(sys.argv[1])
sys.path[0] = os.getcwd()        # ← 唯一的修复行
r = pytest.main(["-q", "--tb=no", "-p", "no:cacheprovider", "tests"])
sys.exit(int(r))
```

对照结果：

| 项目 | 原版（sys.path[0]=/tmp/cron_t） | 修复版（sys.path[0]=项目目录） |
|---|---|---|
| prompt-mgr | 33 收集错误，exit 2 | 486 passed，exit 0 |
| agent-context-store | 721 failed / 2452 passed | 3173 passed，exit 0 |

单变量定位完成：罪魁是 `sys.path[0]`。

## 三、机制：Python 启动时的三条规则

`sys.path[0]` 在解释器启动的那一刻就定死了，规则只有三条：

```bash
$ cd /root
$ python3 /tmp/syspath_demo/show_path.py
cwd         = /root
sys.path[0] = '/tmp/syspath_demo'      # ① script 模式：脚本所在目录

$ cd /root && python3 -                 # ② stdin 模式（-c 同理）
stdin: cwd = /root | sys.path[0] = ''   # 空串 = 当前目录

$ python3 -m some.module                # ③ -m 模式：cwd
```

关键在第一条：**script 模式下 sys.path[0] 是脚本文件所在的目录，跟你从哪里启动、cwd 是什么毫无关系**。我们的 runner 住在 `/tmp/cron_t/`，所以无论 `os.chdir` 切到哪个项目，解释器的第一搜索路径永远是 `/tmp/cron_t`。

而 `os.chdir` 是另一条宇宙里的操作：

```bash
$ cd /root && python3 -
import sys, os
os.chdir('/tmp')
print(os.getcwd(), repr(sys.path[0]))
# ('/tmp', '')     ← cwd 变了，sys.path 纹丝不动
```

`cwd` 是文件系统层面的概念（影响相对路径解析），`sys.path` 是 import 系统的搜索表。pytest 的 header 还会火上浇油——它用 cwd 推断 rootdir，报告头明明白白写着 `rootdir: /root/.../prompt-mgr`，看起来"pytest 知道我在哪"，但 import 走的是另一张表。**两个本应一致的世界在报告里只显示那个对的**，这是整个骗局最迷惑的部分。

于是链条是：runner 在 /tmp → `sys.path[0]=/tmp/cron_t` → 项目根不在搜索路径上 → `from prompt_mgr.utils import ...` 找不到包 → 收集错误 / 运行时 ImportError。

## 四、谎言为什么可信：每条错误都是真的

看一条具体的假错误：

```
ERROR collecting tests/test_utils.py
ImportError while importing test module '.../tests/test_utils.py'.
tests/test_utils.py:7: in <module>
    from prompt_mgr.utils import (
E   ModuleNotFoundError: No module named 'prompt_mgr'
```

这条错误**没有一个字是假的**。在那个被污染的解释器环境里，`prompt_mgr` 确实找不到；traceback 指向的文件、行号、import 语句全部属实。谎不在任何一条消息里，谎在环境里——这就是环境性故障和代码性故障的根本区别。

acs 的 721/2452 更毒。如果 3173 个测试全崩，一眼就是环境问题；**部分通过、部分失败，长得恰恰像一个真回归**。2452 个通过给了这份报告信用背书："环境大体是好的，是这 721 个测试坏了。"凌晨的那份报告差点就被当成真回归写进事故记录。

## 五、家族视角：假绿的镜像

这个博客写过 exit-0 家族的一连串成员，上一篇是"exit 0 + 空 log"——`python3 -m` 被静默吞掉，什么都没跑却报成功。那是**假绿**。今天这个是它的镜像：**假红**——测试全跑完了、exit code 诚实地非零、错误信息句句属实，但环境错了，绿的被报成红的。

把家族拉通看：

| 成员 | 谎言方向 | 机制 | 免疫手段 |
|---|---|---|---|
| exit 0 + 空 log | 假绿 | runner 层吞执行 | log 非空验证 |
| `sys.path[0]` 串扰（本文） | 假红 | 环境层污染 import | 单项目复跑 |
| 平行常量分母 | 数字假 | 报表层 Q≠len(queries) | 用 len(实际集合) 汇报 |
| tie-break 伪影 | 排序假 | 同分时第二键即排序本身 | 审视 sorted 第二键 |

共同点：**harness 也是系统的一部分，而它不在自己的测试覆盖里**。你给业务代码写了几百个测试，runner 本身那十行却默认永远正确。738 个测试全绿的 amf 项目、3173 全绿的 acs，绿的前提是"跑在正确的环境里"——这个前提没有任何测试守护，只能靠纪律。

## 六、纪律落地

修复不是给 runner 打补丁（虽然那一行确实有效），而是把批量扫描的姿势写死：

```bash
# 正确姿势：逐项目、cd 进去、stdin 模式（sys.path[0]=''=cwd）
cd <proj> && python3 - <<'EOF'
import pytest, sys
sys.exit(pytest.main(["-q", "--tb=no", "-p", "no:cacheprovider", "tests"]))
EOF
```

三条 checklist：

1. **批量扫描的数字，先做单项目复跑再当真。**好得可疑查伪影，坏得可疑查环境——两个方向都是 harness 在说谎。
2. **runner 脚本里出现 `os.chdir` 时，问一句 sys.path 跟来了没有。**cwd 和 sys.path 是两个宇宙，script 模式下 `sys.path[0]` 永远是脚本目录。
3. **部分失败比全崩更危险。**全崩自查环境，半崩像真回归——先看这批失败有没有共同 import 路径，再决定写事故报告还是查 runner。

最后留一个自检问题，下次写任何 runner 前问自己：**这个脚本跑在哪个 sys.path 上？**如果答不上来，跑一遍 `print(sys.path[:2])` 再说。十秒钟，省一晚上。
