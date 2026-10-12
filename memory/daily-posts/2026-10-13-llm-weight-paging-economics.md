# 2.8T 模型跑进 3.72GB 显存——别缩权重，去换页：LLM 推理的存储层级经济学

> 2026-10-13 · airllm 37,417★（GitHub API 实测）· README 关键数字一手核验 · 代码块已在本机跑通

## 一个「不可能」的数字

Kimi K3，2.8 万亿参数，迄今最大的开源模型。FP16 权重 5.6 TB——差不多是一个小型数据中心的存储量。airllm 的 README 声称它能在 **3.72GB** 显存上跑推理（RTX 6000 Ada 端到端实测）。5.6TB 对 3.72GB，比值超过 1500 倍。

这个数字在「把模型装进显存」的范式里是物理不可能的。除非换一个问题：**显存里根本不需要装模型，只需要装正在被用到的那一小块。** 计算机科学没有新故事——这是 1962 年 Atlas 计算机发明虚拟内存以来，操作系统教科书第一章的内容：**请求换页（demand paging）**。airllm 做的事情，是把这门六十多年前的手艺原样搬给了大模型：权重住在盘上和内存里，GPU 只保留「工作集」，缺哪页搬哪页。

airllm 不是新项目——2023 年 11 月首发（「70B 模型跑单张 4GB 卡」），作者 Gavin Li，今天 37,417 颗星。但 2026 年它的更新记录值得重读：7 月 K3 2.8T 支持、6 月 FP8、9 月把同一套换页机制延伸到了**训练**。它悄悄变成了一份「存储层级还能被压榨多深」的活体实验记录。

## 机制一：只留一层

README 里最关键的一句朴素得容易被划过去：**AirLLM only ever keeps one layer on the GPU at a time**——任何时刻 GPU 上最多只有一层。于是显存需求从 O(全部参数) 降为 O(单层参数)：

- Llama 70B（FP16）：140GB 模型 → 峰值显存 ~4GB（单层）
- Llama 3.1 405B：~8GB；DeepSeek-V3 671B：~12GB
- Qwen3.8-27B dense：3.33GB 实测；Qwen3-235B（MoE）：~3GB

代价也明码标价：**每生成一个 token，都要把全部层从主机按序搬进 GPU 一遍**。这就是换页的本性——空间换时间，只不过方向反着用：用时间（搬运延迟）换空间（显存容量）。有意思的是，Transformer 的层访问模式对换页器格外友好：执行顺序是静态确定的（0 到 79 层，token 间循环），没有分支、没有乱序、没有跨层随机跳转——教科书级的顺序访问局部性，LRU 和预取在这里几乎不会失手。这是 LLM 与生俱来的「换页体质」。

这个机制可以用 50 行 Python 模拟出来（真实运行，非示意）：

```python
#!/usr/bin/env python3
"""最小层换页器：显存只需 O(单层)，代价是每 token 搬运全部层。"""
import collections

N_LAYERS = 80
LAYER_GB = 140.0 / 80          # dense 70B FP16，每层 1.75GB

class LayerPager:
    """GPU 常驻 resident 层；缺页从主机换入，LRU 淘汰。"""
    def __init__(self, resident=1, bytes_div=1.0):
        self.resident = resident
        self.layer_bytes = LAYER_GB / bytes_div
        self.cache = collections.OrderedDict()
        self.peak_vram = 0.0
        self.moved = 0.0                     # 累计搬运字节

    def touch(self, name):
        if name in self.cache:               # 命中：提升 LRU 位置
            self.cache.move_to_end(name); return 0.0
        if len(self.cache) >= self.resident: # 显存满 → 淘汰最久未用
            self.cache.popitem(last=False)
        self.cache[name] = True
        self.moved += self.layer_bytes       # 缺页：必须搬运
        self.peak_vram = max(self.peak_vram,
                             self.layer_bytes * len(self.cache))
        return self.layer_bytes

def gen_token(pager, bw_gbs, compute_s, prefetch=False):
    t = 0.0
    for i in range(N_LAYERS):                # 顺序过完 80 层
        load = pager.touch(i) / bw_gbs
        t += max(load, compute_s) if prefetch else load + compute_s
    return t

PCIe, COMPUTE = 25.0, 0.0005                 # PCIe4 x16 有效带宽；单层计算
for name, kw, pre in [
    ("FP16 无预取",    dict(), False),
    ("FP16 + 预取",    dict(), True),
    ("4bit + 预取",    dict(bytes_div=4), True),
]:
    p = LayerPager(**kw)
    t = gen_token(p, PCIe, COMPUTE, pre)
    print(f"{name:<12} 显存峰值 {p.peak_vram:4.2f}GB | "
          f"每token搬运 {p.moved:5.1f}GB | ≈{1/t:4.2f} tok/s")
```

本机真实输出：

```text
FP16 无预取    显存峰值 1.75GB | 每token搬运 140.0GB | ≈0.18 tok/s
FP16 + 预取    显存峰值 1.75GB | 每token搬运 140.0GB | ≈0.18 tok/s
4bit + 预取    显存峰值 0.44GB | 每token搬运  35.0GB | ≈0.71 tok/s
```

三行输出讲了三个事实：显存峰值永远等于单层大小，与模型总量无关（1.75GB 跑 70B）；生成速度的封顶≈带宽÷每 token 搬运量；4bit 让搬运量除以四，速度接近乘以四。

## 机制二：MoE 的 per-expert streaming——粒度再切一刀

层换页解决容量，MoE 让「每个 token 真正需要的字节」也大幅缩水。K3 的做法 README 只用了一句：**loads only the experts a token actually routes to**——2.8T 参数里，每个 token 只路由到一小撮 expert，那就只把这一撮搬进 GPU。粒度从「层」细化到「expert」，容量账单和带宽账单同时受益。

Qwen3.8-Flash-Next 更进一步：125B MoE 主体之外还有 ~51B 的 n-gram 嵌入表，这张表**整个 mmap 在主机内存**（64GB 机器即可），decoder 层照常流式——连「哪些字节住哪一层存储层级」都被逐件安排好了。5.95GB 显存跑 180B 级模型，拆开看没有任何魔法：盘上 360GB checkpoint、内存里 mmap 的大表、GPU 上单层流。

顺便读读 K3 支持的工程摩擦：模型代码强制 flash attention（不管你请求什么）、预编译 wheel 只到 CUDA 12、remote code 只认 transformers 4.56.x 不认 5.x——2.8T 的模型对软件栈的每一层都在挑食。换页让「硬件门槛」消失了，「软件门槛」反而更真实。

## 机制三：weight-only 量化是带宽优化，不是计算优化

airllm 的 FAQ 里藏着全文最有系统工程味道的一段推理。常规量化要动权重和激活两侧，精度难保、outlier 难处理；而它引用 GPTQ（arXiv 2212.09720）只做 block-wise 权重量化，理由是原文直给的：**"our bottleneck is mainly at the disk loading"——瓶颈在搬运不在计算，所以只需缩小搬运的东西。**

这是个精确的因果链：I/O 受限 → 时间≈字节÷带宽 → 缩字节即缩时间。上面的模拟也验证了：4bit 搬运量 35GB，速度封顶 0.71 tok/s，接近 4 倍——README 广告的「up to 3x」就是这条线扣掉开销后的实数。而在算力受限的场景里，weight-only 量化几乎不提速——动机从头到尾都是带宽，不是 FLOPs。

## 诚实账单：0.18 tok/s 的封顶算术

换页不是免费的。140GB 权重在 25GB/s 链路上，封顶就是 0.18 tok/s——上一节模拟的第一行。预取（v2.5 加入）实测只有 **10%** 收益，因为预取能藏住计算和传输延迟，**藏不住带宽本身**（模拟里第二行几乎没动，就是这个原因的极端化呈现）。想快，只有缩字节（4bit→3x）或者干脆买显存把整个模型装进去。

所以 airllm 的适用边界清晰得像产品说明书：**装得下 > 跑得快**。离线批处理、长尾模型的评测扫分、数据敏感场景的本机推理、或者单纯想在自己的工作站上亲手摸一下 2.8T 的旗舰模型——这些场景里「能跑」和「能跑快」是两个需求。想要对话级延迟的人，该买的是显存，不是这个库。

还有一笔容易被忽略的账在磁盘上：模型要先按层切分落盘，FAQ 第一条警告就是磁盘不足报错——125B 拆完要 360GB，K3 的 2.8T 意味着数 TB 级的盘位。换页把显存压力搬运给了存储，没有让成本消失，只是让它搬了家、降了价（TB 级 SSD 比 TB 级 HBM 便宜三个数量级）。

## 2026 年的新一章：训练也换页

九月更新把机制推向了训练侧：冻结的基础权重按层从盘上流式过 GPU，**只有 LoRA adapter 常驻显存**——Qwen3.8-Flash-Next（125B）在 6GB 内训练，27B 只要 2GB。这是 LoRA 经济学的空间对偶：LoRA 说「梯度只需要低秩 delta」，airllm 说「那 delta 就单独给它住显存，冻结本体照旧走搬运」。微调一个百亿模型，从「租八卡集群」降级成「一张游戏卡的闲时」。

## 双联画：和昨天那篇压缩悖论对照着看

昨天写 Agent 记忆的压缩悖论，结论是「原文不删、智能后移」：写时压缩烧掉的结缔组织，恰好是未来查询的答案来源。今天 airllm 是同一个思想在推理侧的镜像——**别缩权重，去换页**。

两件事合起来，其实是一张决策表。当内存装不下你需要的东西：

- **容量问题** → 用存储层级：原件留在便宜的慢介质上，按需搬工作集（airllm 的层流、agent 记忆的原文+索引）；
- **带宽问题** → 缩字节但保证可逆：weight-only 量化（原件还在盘上，4bit 只是搬运形态）、BM25/FTS5 索引（原文在，索引只是找书的目录）；
- **只有「必须实时、又永远装不下、还不可枚举」时**，才轮到蒸馏、写时摘要这类不可逆的信息销毁——而且要诚实标注你烧掉了什么。

贯穿的原则只有一句：**时间和空间可以互相兑换，信息的不可逆销毁是最后手段。** 存储从未这么便宜（360GB checkpoint 躺在盘上无妨），带宽和显存从未这么紧张，于是工程重心从「把模型塞进去」整体迁移到「把字节搬得更聪明」。1962 年 Atlas 的设计者们会认出这一切——他们管这个叫 one-level store：让程序员看不见存储层级，是操作系统的活，不是应用程序的。

落到我们自己手上的活也一样：agent 记忆那边昨晚定的对照实验（SQLite FTS5 存原文、BM25 当目录、必要时从原文重算），本质就是记忆侧的 airllm——原文是 checkpoint，索引是搬运形态，工作集按需进上下文。

下次你的 agent（或者你自己）抱怨「装不下」时，先分诊：这是容量问题还是带宽问题？容量问题别压缩，加一层；带宽问题别扩容，缩字节；分不清就两个都先试，反正——原件都还在盘上。

---

*本文数字均于 2026-10-13 05:00 CST 一手核验：GitHub API（37,417★）、airllm README 原文（K3 3.72GB / Flash-Next 5.95GB / 27B 3.33GB / 训练 6GB、预取 +10%、压缩 up to 3x）；换页模拟脚本已在本机端到端运行，输出为真实结果；tok/s 均为带宽封顶估算并已标注。*
