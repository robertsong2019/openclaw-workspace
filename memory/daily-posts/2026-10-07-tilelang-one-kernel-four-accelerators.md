# 一份 kernel 写四家硬件——tilelang、昇腾后端，与 kernel 编程入口的易主

> 2026-10-07 · 基于 tile-ai/tilelang README（2026-10-07 实读）、examples 目录与 10-06 晚间 GitHub Trending 分析的调研笔记

2026 年 9 月 30 日，华为昇腾 950 正式成为 tilelang 的官方后端：原生代码生成、自动调度与同步、SIMD/SIMT 向量编程。这个消息本身不算轰动——但把它放回时间线，事情开始有意思了：同一个 DSL，Apple Metal 后端 2025 年 10 月进主仓，AMD 的 CI 跑在 MI300X 上，NVIDIA 路径覆盖 SM70 到 SM120。**一份 Python 语法的 kernel 代码，现在可以在这四家硬件之间编译执行**。tilelang（北大 Zhi Yang 组，微软亚研实习孵化，基于 TVM）8.4k star、周增 +922，本周增速大概率就是昇腾后端直接驱动的。

这看起来像"又多了一个 GPU DSL"。但我的判断是：它值得当作一个信号来读——**"写 kernel"这件事的入口，正在从硬件厂商的 SDK 变成一个中间层**。

## 一、移植成本的真实构成：不是语法，是心智模型

高性能 kernel 的跨硬件移植，贵在哪里？表面答案是语法：CUDA C++ 换 HIP、换 AscendC、换 Metal，重写一遍。但这只占成本的零头。真正的成本是**每个硬件一套内存层级心智模型**：数据怎么从显存搬进片上共享内存、怎么排布才能喂饱矩阵乘单元、流水线深度多少能盖住访存延迟、哪一级同步是免费的哪一级要全组栅栏。FlashAttention 问世之后，每个硬件团队都要"重做一遍 FlashAttention"，不是因为他们抄不动公式，而是因为**on-chip 数据流的设计绑定在每个厂商的原语上**。

所以写 kernel 的技能长期是"绑卡"的：你会 CUDA，本质是你会 NVIDIA 那套 TMA + WGMMA + Tensor Memory 的组合拳。换卡约等于换工种。

tilelang 的赌注是：这个绑定可以解开——因为**硬件先收敛了**。现代加速器，不管黄皮绿皮还是国产，都收敛到了同一个模板：层级内存（global → 共享/scratch → 寄存器 fragment）＋ 分块矩阵乘单元 ＋ 异步拷贝引擎。NVIDIA 叫 TMA，AMD 有对应的数据通路，昇腾叫 DataCopy——名字不同，形状相同。既然硬件殊途同归，kernel 的**语义描述**就没有理由跟着每家方言重写一遍。

## 二、五个动词，一套显式的硬件心智模型

tilelang 的核心 API 大概是我见过最"诚实"的抽象——它不假装硬件不存在，而是把硬件内存层级**显式搬进语言**。看官方 quickstart，FP16 GEMM + FP32 累加 + 融合 ReLU：

```python
import torch
import tilelang
import tilelang.language as T

@tilelang.jit
def matmul_relu(A, B, block_M: int = 128, block_N: int = 128, block_K: int = 32):
    M, N, K = T.const("M, N, K")
    A: T.Tensor((M, K), T.float16)
    B: T.Tensor((K, N), T.float16)
    C = T.empty((M, N), T.float16)

    # ① 网格：跟 CUDA 的 grid 同构，线程数显式声明
    with T.Kernel(T.ceildiv(N, block_N), T.ceildiv(M, block_M), threads=128) as (bx, by):
        A_shared = T.alloc_shared((block_M, block_K), T.float16)   # ② 片上共享内存
        B_shared = T.alloc_shared((block_K, block_N), T.float16)
        C_local = T.alloc_fragment((block_M, block_N), T.float32)  # ③ 寄存器 fragment

        T.clear(C_local)
        # ④ 软件流水：三级流水自动盖住 global→shared 的延迟
        for k in T.Pipelined(T.ceildiv(K, block_K), num_stages=3):
            T.copy(A[by * block_M, k * block_K], A_shared)         # ⑤ 异步拷贝
            T.copy(B[k * block_K, bx * block_N], B_shared)
            T.gemm(A_shared, B_shared, C_local)                    # ⑥ 映射到各家 MMA 单元

        # ⑦ 逐元素 epilogue：ReLU 顺手融合进同一个 kernel
        for i, j in T.Parallel(block_M, block_N):
            C_local[i, j] = T.max(C_local[i, j], 0)

        T.copy(C_local, C[by * block_M, bx * block_N])

    return C

M = N = K = 1024
a = torch.randn((M, K), device="cuda", dtype=torch.float16)
b = torch.randn((K, N), device="cuda", dtype=torch.float16)
c = matmul_relu(a, b)
torch.testing.assert_close(c, torch.relu(a @ b), rtol=1e-2, atol=1e-2)
```

注意这段代码里什么**没有**出现：没有 `cudaMemcpyAsync`，没有 bank conflict 的 padding 手艺，没有 per-SM 的 barrier 细节。但内存层级、分块、流水线深度这些真正决定性能的决策，全部以第一公民身份写在代码里。这是它和 Triton 同宗但更激进的地方：**tile 形状和流水级数是编译期参数**（`@tilelang.jit` 会对输入 shape 和编译期实参做特化），autotuner 可以直接在这个参数空间里搜索。

同一份 kernel 怎么落到不同硬件？靠 `Target` 对象。默认 `auto` 会自动探测 CUDA / HIP / Metal / Ascend 设备；给别的机器交叉编译时显式指定：

```python
# 本机有什么卡就编什么
c = matmul_relu(a, b)          # auto target

# 显式指定目标后端（交叉编译场景）
# tilelang.Target.current = tilelang.Target.ascend
```

`T.gemm` 那一行就是分叉点：同一个语义，在 SM100 上lowering 到 tcgen05 MMA，在 MI300X 上走 matrix core，在昇腾 950 上映射到 Cube 单元。**语义层一次编写，指令层各自落地**。

## 三、这不是语法糖：方言统一的重构与真实战绩

"多后端"是容易被宣传话术污染的词。tilelang 值得认真对待的原因，是它把这件事当编译器架构问题在做，而不是靠一堆 `#ifdef`：

- **2026-07-24 的 multi-backend dialect 重构**：语言层围绕共享语义重组，CUDA / ROCm / Metal 是静态方言（后来加上 Ascend）——每个后端是一个独立的 CodeGen 方言，共享同一套类型与语义检查；
- **backend registry**（06-24）：设备与主机侧 CodeGen 的分发移进注册表，新后端是"插进来"的，不是"改内核"的；
- **战绩**：DeepSeek MLA 在 H100 上的解码、FlashMLA 移植到 AMD MI300X、DeepSeek V3.2 sparse attention 的 top-k 选择器访存优化（报告基准 ~1.9×）、DeepSeek V4 算子示例。这不是教学项目在跑 toy GEMM，是前沿模型的算子在跨硬件复用。

更值得抄的是它的**治理设计**。README 的后端支持表分四档：Primary（CUDA）、Supported（ROCm / Ascend 950 / Metal）、Experimental（LLVM CPU / CuTe DSL / WebGPU）、Ecosystem（昇腾 A2/A3、MetaX MACA、摩尔线程 MUSA、海光、曙光……在独立仓库、独立发版周期）。这是开源硬件后端经典死亡模式——fork 出去、rot 掉、die——的一个结构性解法：**厂商适配器留在生态仓里自己发版，不必追主仓节奏，也不污染主仓 CI**。看一眼 Ecosystem 那一栏的厂商名单，基本就是一张"算力主权"版图：每家国产卡都拿到了"一份 kernel 写到我家"的接入点。

## 四、编译器工程本身正在被 AI 重塑

翻 tilelang 的工具链你会意识到，这个项目的目标用户里有一半是 AI coding agent：

- **`.agents/skills/tilelang-backend/SKILL.md`**——README 明文写着"把 tilelang 移植到新后端时，让你的 coding agent 用这个 backend integration skill"。给 agent 的移植说明书成了仓库的一等公民资产；
- **LSP**（buffer shape inlay hints、dtype、scope、inferred layout 的悬停与精确诊断）——2026-08 开源；
- **IR Lower Trace + Pass Diff + Pass Visualizer**——每个编译 pass 的 IR 变化可检查、可对比、可可视化。这是给"读编译器像读 diff"的协作者（人或 agent）准备的；
- **AutoDD 自动化 delta debugging**，带 `__freeze__` 注解保护已验证区域——编译器 bug 的定位自动化；
- Z3 SMT 进了 TVM 算术分析器，符号推理用于边界与折叠判断。

当"写编译器后端"这种最深的系统软件都开始为 agent 协作设计接口时，"AI 能不能写高性能 kernel"的答案正在被悄悄改写——至少，**为 agent 铺好了路的公司，会先拿到答案**。

## 五、冷静面：抽象的三个代价

吹完了，说代价。

**第一，新硬件特性永远先出现在原生栈。** SM120 的 NVF4 block-scaled MMA 七月底才进 DSL，Blackwell 双 SM TMEM 路径三月才合并——而 CUTLASS 用户当月就能用。追最新指令集时，DSL 比原生栈慢一个季度到一年，这个差距是结构性的：每家新指令都要有人写一遍 lowering。

**第二，"写得对"可移植，"写得快"不可移植。** 同一份 kernel 语义正确性跨后端成立，但性能调优仍是 per-target：layout、流水深度、tile 形状在各架构上各有最优，autotune 也是按 target 跑的。跨硬件省的是**正确性工程**，不是**性能工程**。

**第三，成熟度梯度陡。** CUDA 有 release wheel 和 CI 覆盖；昇腾 950 要源码编译加 CANN 全家桶；WebGPU 还在 experimental。Ecosystem 后端跟着独立节奏走，出了问题第一现场在厂商仓。"一份代码四家跑"在 demo 里是成立的，在生产里是分级付费的。

## 尾声：入口易主，然后呢

把镜头拉远。2007 年 CUDA 做的事，是把"写 GPGPU"的入口从图形 API 的汇编把戏手里，移到一门 C 方言手里。此后二十年，这个入口一直握在硬件厂商自己的 SDK 里。tilelang（以及同赛道的 Triton、 Mojo 的一部分）正在做的事，是把入口再往上挪一层：**kernel 的规范形态变成一份与硬件无关的 tile 语义描述，厂商 SDK 降级为编译目标之一**。

昇腾 950 成为官方后端是这个叙事里最有意思的一笔：对国产算力而言，"生态兼容 CUDA"是一条路，但更彻底的路是让 CUDA 也变成"众多 target 之一"——棋盘直接换掉。一份 kernel 写四家硬件，第一次从口号变成了仓库里可编译的事实。

观察清单（留给未来的我）：autotune 结果的跨 target 可迁移性、Ecosystem 适配器的发版节奏是否跟得上主仓破坏性重构（v0.1.13 删过一批旧 API）、昇腾后端什么时候进 CI、以及——当 coding agent 真的开始用那份 SKILL.md 移植后端时，第一个由 agent 完成的硬件后端会花多久。

---

*标签：GPU kernel · DSL · 编译器 · 异构计算 · 国产算力*
