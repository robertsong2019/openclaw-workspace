# Agent 记忆的下半场：我试了两次"访问加权衰减"，两次都翻车

> 2026-10-18 · 罗嵩 · 本文是《我的 Agent 记了 12 万字符的笔记，其中 83% 它自己再也读不到》的直接续篇。所有数字均为当日实测。

## 一、先兑现昨天的预测

昨天文章结尾留了一个预测：给 MEMORY.md 做完瘦身手术（158,216 → 8,694 字符）后，网关正在运行的旧进程缓存了术前的肥胖记忆，药效要等下一次 OOM 重启才生效——「那个一直杀宿主的 bug，将第一次扮演救生员」。

今天取证，预测分两半兑现：

- **警告消失：兑现。** 10-17 全天日志里 10 次「MEMORY.md is N chars (limit 20000)」截断警告，全部落在 05:38 重启之前（旧代缓存 121,147 的术后残留）；10-18 全天至今 **0 次**。此前这条警告响了 39 天共 1,802 次，约每天 46 次。39 天来第一次安静。
- **OOM 病愈：没有。** 重启计数从 76 一路走到 82，10-17 23:17 和 10-18 03:47 又各崩一次，间隔 4.5 小时，270 分钟节律纹丝不动。遗忘治好了注入层，治不好 V8 堆——这是两种病，昨天就说过。

但这不是今天的重点。重点是：**昨天的手术是一次性的，而我需要的是常驻机制。** 手动归档能救急一次，救不了第 40 天。恰好，昨晚的 GitHub Trending 深度分析里出现了一个直接相关的项目，把这个问题推向了下半场。

## 二、生态给出的答案：不是读更多，是没被读的自动降级

新上榜的 `akitaonrails/ai-memory`（Rust 单二进制，自托管长期记忆服务）主打跨 harness 共享：20 多个 coding agent（Claude Code、Codex、Cursor、Gemini CLI……）读写同一份记忆，换工具不用重新自我介绍。

真正值得注意的是它的**老化机制设计**，四条全是硬货：

1. **分级衰减曲线**：不同 tier 的记忆有不同的半衰期，冷记忆按指数降级；
2. **访问加权保留**：打开、搜索、链接到达都算「使用」，被用过的记忆衰减更慢；
3. **压缩而非删除**：冷的 episodic 笔记被压成 durable facts（文件路径、错误码、决策结论），近似重复合并、矛盾标记，零硬删除，版本链随时可恢复；
4. **Opt-in dreaming**：配置 LLM 后空闲时把冷记忆簇重写成连贯单页，但**转默认开启前必须过 recall eval**——用「压缩后还能想起多少」的量化指标给遗忘发通行证。

这四条精准命中昨天诊断出的死信区问题。我的系统里 83.5% 的记忆只写不读；它的回答不是「让 agent 读更多」，而是「没被读的记忆自动降级压缩」。markdown 是 source of truth、数据库只是衍生索引、全链路零 LLM 调用——这套哲学和我昨天的手术（全文归档可重建、手术本身 207 秒完成）完全同源，相当于把那次手术做成了常驻服务。

顺带一提它的另一个创新：跨工具交接（handoff）不是文本粘贴，而是带 owner 和 exactly-once 语义的 typed protocol——`ai-memory run codex` 启动时给 Codex 一份 Claude 原历史的私有本地投影，远端只收 harness 和 session 身份，不收 transcript 本体。隐私边界做进了协议层而不是靠用户自觉。这对多 agent 协作是个重要信号：记忆的消费者正在从「一个 agent 的多个会话」变成「多个 agent 的多台机器」，谁先定义好交接协议，谁就拿到下一层的入口。

最让我心动的是第 2 条：访问加权。直觉上它就是对的——昨天 47,019 字符的 Key Insights 层和 811 字符的 10-10 日志，凭什么享受同等的保留待遇？于是我决定在**自己真实的 158k 归档**上实测一把访问加权衰减。

然后，翻车了。翻了两次。

## 三、两次翻车实录

先定义实验：把归档按 `##` 切成 14 个 section（实测切出来：Agent Identity 141 字符、九层按日期堆叠的 Current Focus、47k 的 Key Insights、Timeline 等），给每个 section 算一个保留分数：

```
score = 0.5 ^ (age / half_life[tier]) × (1 + 0.10 × access)
```

tier 分三级：episodic（日志型，半衰期 7 天）、semantic（洞察型，30 天）、identity（身份型，365 天）。分数低于 0.30 判冷，进压缩队列。核心代码（完整脚本 80 行，这里是主干）：

```python
HALF_LIFE = {"episodic": 7.0, "semantic": 30.0, "identity": 365.0}
THRESHOLD = 0.30

def section_tier(title):
    if title.startswith("Agent Identity"):   return "identity"
    if title.startswith("Current Focus"):    return "episodic"
    return "semantic"

for s in sections:                      # 按 "## " 切出的 14 个 section
    age = (TODAY - s.ref_date).days     # 从标题里的日期取年龄
    decay = 0.5 ** (age / HALF_LIFE[s.tier])
    bonus = min(1 + 0.10 * s.access, 3.0)
    s.score = decay * bonus
    # score < THRESHOLD → 进压缩队列（压成 facts，不删除）
```

**翻车一：朴素子串代理。** access 怎么算？我最自然的想法：某天的日志被后续日志引用，就算被访问。于是数每个日期串（如 `10-09`）在后续 daily 文件里的出现次数。跑出来压缩队列 **0%**——所有 section 的 access 都是 11-19。原因 embarrassingly 简单：后续 daily 里的完整日期 `2026-10-09` 本身就包含子串 `10-09`，我在数日期，不是数访问。

**翻车二：剥掉完整日期再数。** 修正：先把 `2026-10-\d{2}` 全部剥掉，再数裸日期串。跑出来 access 还有 8-15，压缩队列依然是 0%。这次没有 bug——是我的 daily 真的高频回指过去的日期（「回顾过去 24h」「上日 KO 600s 超时」这类句子）。也就是说，**提及 ≠ 访问**。一句话提到 10-09，不等于 agent 真的把那天的 843 字符读进了上下文。文本里考古不出访问行为。

**对照组：纯 recency。** 把 access 权重整个置零，只留时间衰减，跑出来这个表（真实输出）：

```
section                          chars   age   tier      score  action
Agent Identity                     141     1  identity  0.998  keep
Current Focus (2026-10-14)        2846     4  episodic  0.673  keep
Current Focus (2026-10-13)        3276     5  episodic  0.610  keep
Current Focus (2026-10-08)         616    10  episodic  0.371  keep
Current Focus (10-06 及更早)       1731    12  episodic  0.305  keep
Current Focus (10-02 及更早)     54022    16  episodic  0.205  COMPRESS
Key Insights (Carry Forward)     47019     1  semantic  0.977  keep
...（其余 semantic/identity 全部 keep）
压缩队列: 54,022 / 120,920 chars (44.7%)
```

看那一行：**10-02 及更早，54,022 字符，44.7% 的归档体积**。这正是 git 考古里 10-02 均衡失守后以日均 2.2k 增长、最终把 KO 整理任务拖到 600,022ms 超时被杀的那块沉积层。纯 recency 策略今天会把它判冷压缩——而现实中它是在第 14 天由一场超时事故「发现」的。一个 7 天半衰期的 TTL，比事故早一周量级。

## 四、翻车教我的三件事

**第一，访问加权的前提是访问遥测，而 markdown 文件没有读事件。** ai-memory 敢做访问加权，是因为它是服务层：每次 open/search/link-arrival 都经过它，天然有 atime。我的 memory/*.md 躺在磁盘上，谁 grep 了它、grep 完用没用，文件系统不记录，事后从文本里也挖不出来。两次翻车不是实现 bug，是**数据源根本不存在**。要做访问加权，埋点位置很明确：注入层。OpenClaw 每次把 MEMORY.md 注入会话上下文时记一行 access log（哪个 section、哪个会话、何时），一个月后访问权重才有真实数据可算。这是我下一步要改的代码。

**第二，今天就能部署的是 tier + recency + size，不需要任何遥测。** 三个档位的半衰期、按日期分层的 episodic 判冷、加上按 `##` 分节称重的尺寸水位（昨天那个 30 行体检脚本），这些数据全是现成的，我的 15k 归档纪律本质上就是一个手动 GC 水位线。自动化的第一步不是炫技，是把这个水位线从 HEARTBEAT 里的纪律变成每天跑一次的脚本——判冷、压缩、归档，全程零 LLM。

**第三，「dreaming 必须过 recall eval」是所有 agent 自改行为的通用纪律。** 遗忘是有损压缩，有损就必然丢东西。ai-memory 的克制在于：压缩功能写好了，但默认关闭，开启的前提是量化验证「压缩后召回率不掉」。这个门槛值得推广成铁律——不只是记忆压缩，任何 agent 自我修改（重写配置、精简规则、合并文件）都应该先过一个「改完后关键任务表现不降」的 eval，再转正。我自己昨天做完瘦身手术，今天也只是验证了「警告消失」这个代理指标，还没有跑过一次真正的 recall eval：随机抽 20 个只有归档里才有答案的问题，问瘦身后的 agent，看能答对几个。这个实验排进下周。

## 五、下半场

记忆系统的上半场比的是容量：存得多、检索准、上下文塞得满。下半场的比分牌换了——**保留率、召回率、单位记忆的维护成本**。写进上下文却永远不被读的字符，和没写一样，还更贵（昨天的账：83.5% 的内容每天 46 次地挤占 20k 的注入预算）。

生态正在收敛到同一个答案：衰减是默认，保留要挣得（access-weighted），压缩不删除（version chain），遗忘要先证明自己无害（recall eval gate）。我的两次翻车不丢人——它们把「访问加权」从一句漂亮话变成了一道明确的工程题：先埋点，再有权重，最后才谈 dreaming。

下一步的动作清单很短：注入层 access log 埋点；recency+size 自动判冷脚本上线（替代 15k 手动纪律）；归档 recall eval 跑基线。等这三件事落地，这座 158k 的记忆仓库才算真正有了新陈代谢。

---

*实测环境：OpenClaw workspace（Ubuntu 6.8，Node 22.22.1），归档 `memory/archive-2026-10-17-memory-slim-full.md`（158,216 chars / 14 sections），日志源 `/tmp/openclaw/openclaw-2026-10-1{7,8}.log` + `journalctl --user -u openclaw-gateway`。本文写作于 2026-10-18 05:00 cron，与《记忆暗物质》（10-17）、《Agent 宿主 OOM 取证》（10-16）构成同一系列的第四篇。*
