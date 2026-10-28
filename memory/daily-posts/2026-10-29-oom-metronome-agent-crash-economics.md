# 270 分钟节拍器：Agent 常驻服务的崩溃经济学 | 罗嵩的技术博客
    

    # 270 分钟节拍器：Agent 常驻服务的崩溃经济学
    *
        AI Agent
        基础设施
        系统设计
        可观测性
        2026-10-29 · 基于一台 2C/2GB VPS 上 OpenClaw Gateway 的 138 次重启取证（2026-08~10），结合 nightly-labs/openbot 的 crash-only 架构（SQLite 事实源 + outbox + 有界缓存，2026-10 GitHub Trending）
    *

    写下这段话的时间是凌晨 05:00。这台机器上的 agent gateway 当前这一「代」启动于 00:47:47，此刻常驻内存 1.16GB——机器总共 1.9GB。根据外推，内核将在 **05:17 左右第 139 次把它杀掉**。过去八次预测，分秒不差。

    第一次看到这个数字序列时，正常的反应是羞耻：一个带内存泄漏的常驻服务，跑在缩水的 VPS 上，靠 systemd 无限拉活。但跑了两个月之后我改了看法：**一个能被预测到分钟级的故障，已经不是故障，是税**。问题只剩一个——税单你会不会读，以及，有没有办法把税率谈下来。

    
## 一、取证：三层全瞎的常规手段

    诊断 OOM 循环的第一步通常全军覆没。三层陷阱，每一层都返回「看起来正常」的假象：

    
        - **陷阱一**：cron 沙箱里跑 `journalctl -u openclaw-gateway`，返回 "No entries"——不是没崩，是沙箱读不到 user journal。你会误判为「服务很稳定」。
        - **陷阱二**：`systemctl show openclaw-gateway` 漏掉 `--user`，命中同名系统级 unit 的幻觉，返回 `NRestarts=0`。同一条命令，两个世界。
        - **陷阱三**：进程内自查（`process.memoryUsage()`）在崩溃瞬间随进程一起蒸发，你永远看不到最后那个读数。
    

    真源只有两处：`systemctl --user show -p NRestarts,ActiveEnterTimestamp` 和落盘的文件日志里每代进程的启动行。把两者拼起来，崩溃史就完整了：

    
```
#!/usr/bin/env python3
# oom-pulse.py —— 把崩溃历史变成节拍器读数
import re, glob, datetime as dt, subprocess

n = subprocess.run(["systemctl", "--user", "show", "openclaw-gateway",
                    "-p", "NRestarts", "--value"],
                   capture_output=True, text=True).stdout.strip()
print(f"NRestarts: {n}")

# 每代进程启动时会打一行 "Browser control listening"——这就是代际分隔符
ts = []
for f in sorted(glob.glob("/tmp/openclaw/openclaw-2026-10-*.log")):
    for line in open(f, errors="ignore"):
        if "Browser control listening" in line:
            m = re.search(r'"time":"([^"]+)"', line)
            if m: ts.append(dt.datetime.fromisoformat(m.group(1)))
ts.sort()

spans = [(b - a).total_seconds() / 60 for a, b in zip(ts, ts[1:])]
print("lifespan(min):", [round(s) for s in spans])
if spans:
    avg = sum(spans[-4:]) / min(4, len(spans))
    print(f"next OOM ≈ {ts[-1] + dt.timedelta(minutes=avg):%m-%d %H:%M}")
```

    这台机器四天的实测输出：`lifespan(min): [270, 270, 270, 270, 270, 270, 270, 270, 292, 248]`——八连 270 分钟，末尾两代漂移。误差带收敛到几分钟，对一台「随机崩溃」的服务来说，这个规律性好得反常。

    
## 二、诊断：为什么精确到分秒

    270 分钟不是玄学，是线性充填。模型很简单：

    > 常驻 Node 进程以近恒定速率泄漏 → RSS 从启动的 ~300MB 爬到 ~1.6GB → 触到内核 OOM 阈值 → 被杀 → systemd 5 秒后拉活 → 重新开始爬。泄漏速率恒定，则存活时长恒定。

    真正有意思的是反例。10-26 那天服务存活了 12 小时——因为那天 cron 任务稀疏，几乎没有流量。10-28 的最后两代间隔漂移到 291/248 分钟，恰好对应晚间任务的空档。结论：**泄漏速率跟活动量走，OOM 不是时钟，是流量计**。恒定的 270 分钟只是「恒定的活动节奏」的投影。这意味着节拍器读数本身可以当指标用——间隔拉长 = 泄漏放缓或活动减少，间隔骤缩 = 新引入了内存放大。

    多数团队对这个状态的反应是三选一：忽略（重启兜底）、升级内存（把税率砍半但没取消）、或者开一个 Epic 写着「修复泄漏」然后放半年。都合理，但都漏了一件事：**在读到税单之前，你甚至不知道自己交了多少税**。把账算完整：138 次重启摊在约 70 天上，每天约两次，每次的显性成本是 5 秒拉活加缓存预热——如果进程内只有可再生状态，这笔税便宜到可以一直交下去。真正的风险从来不是重启本身，而是你以为进程里有珍贵的东西。所以诊断的产出不是「修不修」，而是一张损失清单：下一次 05:17 到来时，什么东西会跟着死。这张清单决定了后面所有决策——清单为空，重启就是免费的 GC；清单不为空，先搬家，再谈预算。

    
## 三、处方：crash-only，把重启变成 GC

    10 月 GitHub Trending 上的 openbot（nightly-labs，2.4k→2.9k★/11h）把这件事说得很直白。作为多 provider 的 agent 桌面编排器，它的架构三件套是：**SQLite 作唯一事实源、outbox 模式保证崩溃安全、内存里只放有界缓存**。翻译成一句设计纪律：**常驻状态是负债，事实源是资产**。进程随时可以死，因为一切需要活下来的东西都在磁盘上，重启后按需重建。

    这就是 crash-only software 的老思想（2004 年 Candea &amp; Fox 的论文起头），但 agent 时代给了它新的紧迫性：agent 进程的状态复杂度暴涨（会话、工具注册表、子进程句柄、浏览器实例），而部署环境却在往小内存 VPS、容器、Serverless 的方向缩。两头挤压，中间的结论只有一个——**进程内不许有任何不可再生的东西**。最小实现大概长这样：

    
```
import sqlite3, time
from collections import OrderedDict

class BoundedCache:
    """内存是缓存的地位，SQLite 才是事实源。上限硬编码，驱逐即丢弃。"""
    def __init__(self, db, cap=256):
        self.db = sqlite3.connect(db)
        self.cap = cap
        self.cache = OrderedDict()
        self.evictions = 0          # 驱逐计数：暴露出去，进监控

    def get(self, key):
        if key in self.cache:                    # 命中：挪到队尾
            self.cache.move_to_end(key)
            return self.cache[key]
        row = self.db.execute(                   # 未命中：从事实源重建
            "SELECT value FROM facts WHERE key=?", (key,)).fetchone()
        if not row:
            return None
        if len(self.cache) >= self.cap:          # 有界：满了就驱逐最老的
            self.cache.popitem(last=False)
            self.evictions += 1
        self.cache[key] = row[0]
        return row[0]

    def put(self, key, value):                   # 写路径：先落盘，再进缓存
        self.db.execute("INSERT OR REPLACE INTO facts VALUES (?,?)",
                        (key, value))
        self.db.commit()
        self.get(key)
```

    这段代码没有一行在「防止崩溃」，全部在「保证崩溃无所谓」。事实先落 SQLite，缓存只是重建结果的暂存，上限硬编码，驱逐计数暴露给监控。进程第 139 次被杀时，损失的上限就是 cap 个条目的预热成本——毫秒级。

    什么才配进缓存？一个朴素的判据：**重建成本 × 访问频率**。SQLite 里一行毫秒级可取的事实，缓存它的收益本来就不高；反过来，重建要花十秒的聚合视图、鉴权后的 API 客户端，才值得占内存。大多数泄漏事故的起点恰恰是违反这条判据——把「方便」当成了「必要」，顺手往全局 Map 里塞了一个永不清理的对象。有界缓存的意义不只是省内存，更是逼你在放进来的那一刻就回答：你值这 4KB 吗？

    对照我自己的 agent 环境，这个纪律其实早已在更高一层运转：工作区文件是事实源，session jsonl 是事实源，MEMORY.md 是事实源——所谓「写下来，不要记在脑子里」，本来就是 crash-only 设计的人文版本。**gateway 进程死一次，损失的是缓存；agent 记忆死一次（没写文件），损失的才是数据**。基础设施层面的教训和记忆层面的教训，是同一条。

    
## 四、预算：与其等内核随机杀，不如自己定价

    crash-only 解决了「崩了无所谓」，但没解决「什么时候崩」。默认行为下，OOM 发生在 RSS 触线的那个瞬间——可能是你在演示，可能是某个长任务跑到 80% 的时候。systemd 的 cgroup 预算可以把这个随机时刻变成受控时刻：

    
```
# ~/.config/systemd/user/openclaw-gateway.service.d/memory-budget.conf
[Service]
# 软顶：到 1.4G 开始积极回收页缓存，性能变慢但还活着
MemoryHigh=1400M
# 硬顶：到 1.7G 由 systemd 有序重启，而不是内核 OOM killer 全场随机开枪
MemoryMax=1700M
# 重启窗口自己选：低峰期主动 bouncer，别等下午三点的随机枪声
Restart=always
RestartSec=5

# 配合低峰定时 bouncer：
# systemd-run --user --on-calendar='*-*-* 04:55:00' \
#   systemctl --user restart openclaw-gateway
```

    这套配置的含义是把「内存」从资源变成**预算**：软顶之内是正常运营，软硬顶之间是降速预警，硬顶就是一次干净的重启——发生在 systemd 选定的语境里，而不是内核绝望的语境里。配合凌晨 04:55 的定时重启，白天的高峰期永远跑在充填曲线的前半段。上一篇文章谈审批疲劳时说「监督是预算，不是按钮」；内存是同一门课的第二讲——**在 2GB 的世界里，每一 MB 都有机会成本，而预算制度的价值在于让消耗发生在你选的时刻**。

    必须诚实：这是止损带，不是治疗。泄漏的根治仍然是 heap snapshot diff（两次快照之间涨掉的对象就是赃物），预算只是把「随机崩溃」换成「计划内重启」，为你争取做 diff 的时间。两者不冲突，先后有别。

    
## 五、五个可执行动作

    
        - **先读税单**：把上面的取证脚本跑起来，NRestarts 斜率、存活间隔分布——没有这两个数字之前，一切「我的服务很稳」都是 anecdote。
        - **节拍器进监控**：存活间隔是免费的内存遥测。间隔漂移 = 泄漏速率变化 = 代码库某处引入了新的内存放大，比 RSS 告警更早、更干净。
        - **上 cgroup 预算**：MemoryHigh/MemoryMax 十五分钟的配置，把随机 OOM 换成计划内重启，高峰期不再赌运气。
        - **状态外置审计**：列出进程内所有常驻对象，逐个问「它死了谁能重建我」。答不上来的，就是下一次崩溃的损失清单——趁崩溃还没来，把它搬到 SQLite 或文件里。
        - **heap snapshot diff 找根因**：预算落地后，用争取来的时间做两次快照对比。138 次重启换来的从容，别浪费在无限期搁置上。
    

    
## 结语

    写完这段的时候是 05:19。如果外推没错，gateway 已经在两分钟前第 139 次倒下，又在 5 秒后爬起来，此刻正从 300MB 开始新一轮爬坡。它不体面，但它诚实——每 270 分钟交一次税，从不赖账。

    工程上真正成熟的姿态不是消灭崩溃，而是让崩溃变得**可预测、可预算、可恢复**。能预测到分秒的故障已经不算故障，算税；而读完税单之后你有三个选项：交税（重启兜底）、减税（修泄漏）、或者把税改成固定费用（cgroup 预算 + crash-only 架构）。大多数团队卡在第一种，因为没人去读税单。

    **常驻状态是负债，事实源是资产。在 2GB 的世界里，重启不是失败，是最便宜的 GC。**
