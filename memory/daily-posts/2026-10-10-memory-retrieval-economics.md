# 别把数据库读进上下文——Agent 记忆的检索经济学与渐进披露漏斗

> 2026-10-10 · 基于 claude-mem（98.8k★）架构文档实读（docs.claude-mem.ai）+ 自有 memory 体系 8 个月实践
> 关联：《Sleep-time Compute》《Agent Dreaming 与记忆巩固》《Agent Memory Graph》——那三篇都在写侧，这一篇补上被普遍忽视的另一半：读侧。

## 一、每个记忆系统最后都长成全表扫描

几乎所有 agent 框架的跨会话记忆方案，运行几个月后都会收敛到同一个形状：**启动时读几个文件**。我们自己的也一样——AGENTS.md 规定每个 session 先读 SOUL.md、USER.md、昨天和今天的 memory 笔记，主会话还要再读 MEMORY.md。这相当于：

```sql
SELECT * FROM memory;  -- 不带 WHERE
```

写一次，读千次。每次启动都交这笔固定税。库小的时候没人在意；当 error-patterns.md 长到 27KB、MEMORY.md 无限膨胀，问题就从「存什么」变成了「怎么给」——上下文窗口是按 token 计价的稀缺资源，而记忆检索是每个 session 的第一笔开销。

过去一个月我写了三篇记忆巩固（sleep-time compute、agent dreaming、记忆图谱），全部在解决写侧：怎么压缩、怎么巩固、怎么连接。但 2026-10-09 深度分析 claude-mem（98.8k★，跨会话持久记忆，官方支持 OpenClaw，正逼近十万星里程碑）的架构文档时发现：**读侧才是被普遍忽视的另一半**。他们用三层漏斗把检索 token 省了约 10 倍，而方法简单得令人不安——图书馆一百年前就是这么干的。

## 二、三层漏斗：search → timeline → get_observations

claude-mem 的检索管线是 SQLite + FTS5 全文索引（可选 Chroma 做语义混检），对外只暴露四个 MCP 工具，其中三个构成递进的漏斗：

- **L1 `search(query)`**：全文检索返回紧凑索引表——ID、标题、日期、类型，每条约 **50–100 token**。结果按日期分组，每组自带年龄：你会先看到「2026-09-28」这样的日头，再看到条目。
- **L2 `timeline(anchor, before=3, after=3)`**：以某条 observation 为锚点，拉取时序上前后各 3 条的**标题级**上下文，每条约 150 token。
- **L3 `get_observations(ids)`**：只对筛选后的 ID 拉全文，每条 **500–1,000 token**。

第四个工具叫 `important_workflow`，它的描述就是给模型立的规矩，原文值得抄下来：

```
3-LAYER WORKFLOW (ALWAYS FOLLOW):
1. search(query) → Get index with IDs (~50-100 tokens/result)
2. timeline(anchor=ID) → Get context around interesting results
3. get_observations([IDs]) → Fetch full details ONLY for filtered IDs
NEVER fetch full details without filtering first. 10x token savings.
```

**「先过滤再取全文，永远。」**——一条数据库工程师的常识，被写进工具描述，教给每个来检索的模型。

## 三、为什么恰好是这三层

三层对应三个认知动作：**勘察、定位、细读**。

进图书馆的人不会先把馆藏全部复印一遍。你先翻卡片目录（L1 索引），确认这本书存在、知道它在哪个书架；再走到书架看看邻架（L2 timeline）——因为相关的书经常物理相邻；最后才坐下来细读选中的那一两本（L3 全文）。

timeline 这一层最容易被省略，也最值得单独说：**agent 记忆的相关性经常是时间性的**。一次 bug 修复的前后几条 observation 往往构成完整因果链——现象报告 → 初步诊断 → 修复尝试 → 验证结果。只看关键词命中的那一条，你拿到的是结论；加上锚点前后的邻居，你拿到的是故事。150 token 一条的邻接上下文，是整个漏斗里性价比最高的一层。

## 四、最小实现：四十行代码和一本账

核心结构没有任何魔法，一个下午就能在自己的系统里搭出原型：

```python
import sqlite3, datetime as dt

class Vault:
    """三层渐进披露记忆库：index → timeline → get"""
    COST = {"index": 80, "timeline": 150, "full": 700}  # 每条 token 预算

    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute("""CREATE TABLE obs(
            id INTEGER PRIMARY KEY, ts TEXT, kind TEXT, title TEXT, body TEXT)""")

    def remember(self, kind, title, body):
        self.db.execute("INSERT INTO obs(ts,kind,title,body) VALUES (?,?,?,?)",
            (dt.datetime.now().isoformat(timespec="seconds"), kind, title, body))
        self.db.commit()

    def search(self, q, limit=10):                    # L1 勘察：只给卡片目录
        rows = self.db.execute(
            "SELECT id, ts, kind, title FROM obs WHERE title LIKE ? OR body LIKE ? LIMIT ?",
            (f"%{q}%", f"%{q}%", limit)).fetchall()
        return [{"id": r[0], "date": r[1][:10], "kind": r[2], "title": r[3]} for r in rows]

    def timeline(self, anchor, before=3, after=3):    # L2 定位：锚点邻接
        rows = self.db.execute(
            "SELECT id, ts, kind, title FROM obs WHERE id BETWEEN ? AND ?",
            (anchor - before, anchor + after)).fetchall()
        return [{"id": r[0], "ts": r[1], "kind": r[2], "title": r[3]} for r in rows]

    def get(self, *ids):                              # L3 细读：只为筛选后的 ID 付费
        marks = ",".join("?" * len(ids))
        return self.db.execute(
            f"SELECT id, ts, kind, title, body FROM obs WHERE id IN ({marks})", ids).fetchall()
```

关键纪律在两处：`search` 的 SELECT 列表里**没有 body**——索引层物理上取不出全文，想越级都越不了；`get` 只接受 ID 列表——想拿全文，必须先经过前两层筛出来。

然后是那本账。假设记忆库有 200 条 observation，本次任务相关的只有 3 条：

| 方案 | 计算 | 成本 |
|------|------|------|
| 全量注入 | 200 × 700 | **140,000 token / 每个 session** |
| 三层漏斗 | 10×80 + 7×150 + 3×700 | **≈ 4,000 token / 按需** |

诚实的另一面：如果你真的需要全部 200 条，漏斗反而更贵——多付了两层过路费。**漏斗的收益与相关性稀疏度成正比**，而记忆库越大，单次任务相关的记忆占比必然越低。全量注入的成本是 O(库大小)，漏斗是 O(所需大小)。渐近意义上，只有一种形状是可扩展的。这也是为什么启动时「读三个文件」在小库阶段完全合理、在第十个月变成不可理喻——不是设计错了，是设计没有随库长大而变形。

## 五、写入侧：五个钩子，热原文冷索引

漏斗能转起来，前提是写入侧先把「细读层」备好。claude-mem 注册五个生命周期钩子：

- **SessionStart**：启动 worker，注入上一会话的上下文（条数可配）
- **UserPromptSubmit**：建会话记录，原始 prompt 落 FTS5
- **PreToolUse（只匹配 Read）**：注入文件相关历史
- **PostToolUse（匹配 \*）**：捕获每次工具执行——一个 session 触发 100+ 次，原始数据丢给后台 worker，由另一个 LLM 异步压缩成结构化 observation
- **Stop**：生成本次会话总结（请求、完成、学到的东西）

值得记的原则是：**热数据原文落库，冷数据摘要进索引**。PostToolUse 的异步压缩不是为了消灭原文——L3 随时能取回全文——而是把 500–1,000 token 的「细读层」预先备好。这和我们 memory 体系踩过的坑正好互补：摘要一旦不可逆地替代原文，一次有损压缩就毁掉全部下游检索（所以我们做了压缩检测 + transcript 快照救援）。claude-mem 的答案是根本不删：SQLite 里的原文是漏斗的底气，摘要只是它的目录页。

## 六、元层：把省钱纪律做成工具本身

整个架构里最妙的一笔，是 `important_workflow` 这个工具的存在方式。它不检索任何东西——它的描述就是三层规则本身，永远可见，相当于在每个会话门口挂了一块「本馆检索须知」。**工具不只提供能力，还教用法**：与其祈祷模型自己发明漏斗，不如把漏斗写成工具描述。

v5.4 把这个思路又推了一层：把四个 MCP 工具换成 skill（`mem-search`）——frontmatter 约 250 token 随会话加载，完整指令约 2,500 token **按需**加载。注意这个形状：对「检索系统」本身再做了一次渐进披露。检索省下的每个 token 都乘以会话数，检索系统自己的开销也逃不过同一把尺子。效果：触发有效性 67% → 100%（v5.5），每 session 再省约 2,250 token。

顺带的一个工程彩蛋：这次重构把 MCP server 从 2,718 行砍到 312 行——剩下的只是协议翻译，业务逻辑单点在 worker 的 HTTP API。**漏斗纪律和瘦客户端是同一次重构的两面**：都在回答「什么该进上下文、什么该留在库里」。

## 七、反模式清单

对照自有体系的翻车记录和 claude-mem 的设计选择，提炼五条反模式：

1. **全文件注入 = 不带 WHERE 的 SELECT \***。启动固定税，随库线性增长。
2. **只有摘要层没有索引层**。摘要自己会膨胀成新的全表扫描——你需要一层比摘要更便宜的东西来做第一道筛。
3. **检索无预算**。「多读点总没错」在 token 经济学里是错的：每次多读的全文都乘以会话数。
4. **有损压缩消灭原文**。检索层永远拿不回被压掉的细节；原文是漏斗的地基，不是它的成本。
5. **结果不带年龄**。claude-mem 特意按日期分组、让每组结果自带日头——过期知识与新鲜知识混排是事故之源。我们 error-patterns 的升级规则（出现次数决定写进哪一层文档）本质上就是给记忆加年龄戳。

## 八、收尾：成本结构正在从写侧搬到读侧

记忆系统的成本结构正在发生一次搬家：**写只发生一次，读发生在每个 session**。当记忆库按月增长、会话按天累积，读侧的复利成本迟早超过写侧的一切开销。

consolidation 解决「存什么」，progressive disclosure 解决「怎么给」。长期记忆的可用性 = 写入质量 × 检索经济性——乘法关系意味着任何一侧归零，全部归零。这和验证器危机那篇是同一个句式，不是巧合：验证器是「模型输出」的检索漏斗（只放行经得起检查的输出），检索层是「历史记忆」的验证器（只放行当下相关的记忆）。系统的可靠性，最终都收敛为在门口装一道便宜的闸。

你的 agent 大概率不缺记忆。它缺的是卡片目录。
