# $7 给 AI 买一副身体——走人的路，别走开发者的路：ESP32 零越狱控制 iPhone 的工程解剖

> 2026-10-14 · [onehumanbeing/esp32-iphone-agent](https://github.com/onehumanbeing/esp32-iphone-agent) 1,472★/185 forks（GitHub API 实测，2026-10-11 创建，3 天）· README + 固件源码 + agent.py/vision.py 全部一手核验 · 代码块已在本机跑通

三天前创建的仓库，三天 1,472 颗星。README 的第一行就是全部卖点：**让 AI 模型使用一台真 iPhone——用一块 $7 的 ESP32，不要 Mac、不要开发者账号、不要越狱。** Demo 视频里它「打开白板画一张笑脸」（连续笔触），「设一个每天早上 7 点重复的闹钟」（时间滚轮、逐个勾选星期、保存）——每一步的截图连同模型标注的点击轨迹，留在网页端的 step wall 上可回放。

这不是又一套 Appium。它引人注目的地方是路线选择本身：**过去十年 iPhone 自动化的标准答案是 XCTest / WebDriverAgent——开发者的路径：Mac + Xcode + 签名的 helper app + Apple 开发者账号（免费账号的签名每 7 天过期一次）。这个项目走的是人的路径：屏幕和指针。** README 里的对比表把这笔账算得很直接：

- 开发者账号：**不需要** vs 需要（给 runner 签名）
- Xcode：**不需要** vs 需要
- 电脑：Mac **或 Linux** vs 只能 Mac
- 手机上装的 app：**零** vs 测试 runner app
- 额外硬件：ESP32-S3（~$7）vs 一根 USB 线
- 任何 app 里都能用（含游戏）：**是**，因为它只看像素 vs 大多数不行（依赖 accessibility 树）

iOS 从 13 开始原生支持 USB 鼠标（AssistiveTouch 圆形指针），于是一块插在手机 USB 口上、伪装成标准鼠标键盘的 ESP32-S3（Seeed XIAO，淘宝 ¥40-50，手机直接给板子供电，Lightning 机型加一个相机转接头），加上 AirPlay 屏幕镜像，就凑齐了一副完整的身体——**手机端零安装、零越狱、零开发者账号**。

## 解剖：眼、手、脑

整个仓库只有 34 个文件，分工干净得像教科书：

- **眼**——AirPlay 镜像到电脑上的 UxPlay，GStreamer 管线把视频流转成 JPEG 帧；
- **手**——155 行 Arduino 固件，注释第一句就宣布了架构哲学：**"It holds no logic; the server decides"**（板子不持有任何逻辑，服务器决定一切）。它只是个 TCP 行命令协议的执行器：`ping | home | move dx dy | press | release | click | scroll | type | key cmd+h`。锁屏会让 iPhone 挂起 USB，固件会先发 remote wakeup、失败立刻回报 `asleep` 而不是卡死；8 秒看门狗保证板子最多重启一次，不会失联；
- **脑**——任意 OpenAI 兼容的视觉模型，拆成 planner（写 ≤6 步计划，明确偏好「搜索打开 app」而非翻屏）和 actor（逐帧决定下一个动作）两个角色，可以同一个模型兼任。

## 全文最精彩的系统工程：相对指针怎么变成绝对定位

USB 鼠标协议只有**相对位移**，而 UI 操作需要**绝对坐标**。中间隔着一堵墙：iOS 的指针球状加速曲线（移动越快，屏幕位移放大越多）——位移和 HID 单位之间的映射是非线性的、且随速度变化。这个项目用三招把它拆了：

**第一招，撞角饱和。** `home` 命令是连发 50 份 (-127,-127)。加速曲线再怪，指针也会被屏幕左上角夹住——**饱和是一种让误差无法积累的机制**，无论之前漂到哪，一次撞角就确定性归零。

**第二招，定速步进。** 固件源码里 `STEP=10 / STEP_MS=8` 的注释原文：**"constant pace keeps iOS acceleration predictable"**。每次最多 10 单位、每 8ms 一报，把速度钉死在 1250 单位/秒——如果这低于加速曲线的线性阈值，屏幕位移就严格等于 HID 单位，服务器的 1:1 跟踪就是精确的。

**第三招，wiggle-locate。** 点击前轻晃指针，前后抓两帧做像素差分，质心就是指针的真实位置（`vision.py`，63 行）；顺便检测屏幕有没有真的变化，反馈进 actor 的 prompt：**屏幕没变 = 动作没生效，别假装成功，重新瞄准或换路。**

这三招可以用 60 行 Python 完整模拟（真实运行，非示意）：

```python
#!/usr/bin/env python3
"""迷你闭环：相对 HID 指针 -> iOS 球状加速 -> 屏幕帧 -> 帧差定位 -> 修正。"""
import random
from PIL import Image, ImageChops

random.seed(7)
W, H = 512, 512          # 屏幕分辨率（示意）
CURSOR_R = 9             # AssistiveTouch 圆形指针半径
LINEAR_UPTO = 1500       # 低于此速度（单位/秒），屏幕位移 = HID 单位 1:1

def accel(units_per_sec):
    """iOS 指针球状加速（简化模型）：慢速线性，快速被放大。"""
    return 1.0 if units_per_sec <= LINEAR_UPTO else 1.0 + (units_per_sec - LINEAR_UPTO) / 1200.0

class Phone:
    def __init__(self):
        self.px, self.py = random.uniform(0, W), random.uniform(0, H)  # 真实位置（服务器不可见）
    def hid_move(self, dx, dy, sec):
        """固件发相对位移；屏幕位移 = HID 位移 x 加速因子，并被屏幕边界夹住（饱和）。"""
        a = accel(max(abs(dx), abs(dy)) / max(sec, 1e-9))
        self.px = min(W, max(0, self.px + dx * a))
        self.py = min(H, max(0, self.py + dy * a))
    def frame(self):
        img = Image.new("L", (W, H), 40)
        for x in range(int(self.px) - CURSOR_R, int(self.px) + CURSOR_R):
            for y in range(int(self.py) - CURSOR_R, int(self.py) + CURSOR_R):
                if (x - self.px) ** 2 + (y - self.py) ** 2 <= CURSOR_R ** 2 and 0 <= x < W and 0 <= y < H:
                    img.putpixel((x, y), 220)
        return img

def locate(before, after, near, reach=40, shift=20):
    """指针右移 shift 前后抓两帧，差分质心恢复指针在 before 帧的位置（vision.py 同思路）。"""
    box = (max(0, int(near[0] - reach)), max(0, int(near[1] - reach)),
           min(W, int(near[0] + reach + shift)), min(H, int(near[1] + reach)))
    diff = ImageChops.difference(before.crop(box), after.crop(box)).tobytes()
    bw = box[2] - box[0]
    hits = [(i % bw, i // bw) for i, v in enumerate(diff) if v > 30]
    if not 15 <= len(hits) <= len(diff) // 4:      # 没动，或动的不止一个指针
        return None
    if max(x for x, _ in hits) - min(x for x, _ in hits) > 0.15 * W:
        return None                                # 不是一团紧凑的像素
    return (sum(x for x, _ in hits) / len(hits) + box[0] - shift / 2,
            sum(y for _, y in hits) / len(hits) + box[1])

def paced_move(phone, dx, dy, step=10, step_ms=8):
    """固件同款：每次最多 10 单位、每 8ms 一报，钉死在线性区。"""
    while dx or dy:
        sx, sy = max(-step, min(step, dx)), max(-step, min(step, dy))
        phone.hid_move(sx, sy, sec=step_ms / 1000)
        dx, dy = dx - sx, dy - sy

phone, target = Phone(), (380, 260)

# --- 1) home：50 份 (-127,-127) 撞向左上角，饱和让累计误差归零 ---
for _ in range(50):
    phone.hid_move(-127, -127, sec=0.002)
print(f"1) home 撞角: 指针真实位置 ({phone.px:.1f}, {phone.py:.1f})"
      "  # 加速曲线再怪，也被屏幕边界夹到 (0,0)，误差不积累")

# --- 2) 一步到位 vs 定速步进：加速曲线的非线性区是隐藏陷阱 ---
rush = Phone(); rush.px = rush.py = 0
rush.hid_move(target[0], target[1], sec=8 / 1000)   # 一份报告直接冲到目标
err = ((rush.px - target[0]) ** 2 + (rush.py - target[1]) ** 2) ** 0.5
print(f"2) 一步到位: 发 ({target[0]},{target[1]})，落在 ({rush.px:.0f},{rush.py:.0f})，偏差 {err:.0f}px"
      "  # 快速移动被加速放大 39 倍，撞出屏幕被夹住")
paced_move(phone, target[0], target[1])             # 服务器按 1:1 跟踪，估计 = (380,260)
print(f"   定速步进: 发 ({target[0]},{target[1]})，落在 ({phone.px:.1f},{phone.py:.1f})"
      "  # 1250 单位/秒在线性区，位移=单位")

# --- 3) wiggle-locate：注入未建模漂移，点前轻晃指针找回真实位置 ---
drift = 11.3                                        # 模拟系统动画/丢帧导致的未建模漂移
phone.px += drift
before, after = phone.frame(), (paced_move(phone, 20, 0), phone.frame())[1]
found = locate(before, after, near=target)          # 差分质心 = before 帧里的真实位置
real_now = (found[0] + 20, found[1])                # 晃动本身 +20
paced_move(phone, target[0] - real_now[0], target[1] - real_now[1])
final = ((phone.px - target[0]) ** 2 + (phone.py - target[1]) ** 2) ** 0.5
print(f"3) wiggle 校准: 漂移 {drift:+.1f}px，定位恢复 ({found[0]:.1f},{found[1]:.1f})，"
      f"修正后点击距目标 {final:.1f}px")
```

本机真实输出：

```
1) home 撞角: 指针真实位置 (0.0, 0.0)  # 加速曲线再怪，也被屏幕边界夹到 (0,0)，误差不积累
2) 一步到位: 发 (380,260)，落在 (512,512)，偏差 284px  # 快速移动被加速放大 39 倍，撞出屏幕被夹住
   定速步进: 发 (380,260)，落在 (380.0,260.0)，偏差 0.0px  # 1250 单位/秒在线性区，位移=单位
3) wiggle 校准: 漂移 +11.3px，定位恢复 (391.2,260.0)，修正后点击距目标 0.1px
```

一步到位偏出 284px，定速步进精确落地，漂移 11.3px 被视觉校准吃掉——三招各自的分工一目了然。加速模型是简化示意（真实曲线 Apple 不公开），但机制同构。

## ACTOR_PROMPT：把身体的物理性质写进协议

这个项目的 prompt 工程值得逐句读，因为它处理的不是「怎么思考」而是**「这具身体诚实的世界模型」**：

- **"Swipes have no momentum"**——指针滑动没有手指的惯性，内容只移动手指那么多就停。所以偏好 100-250 单位的短滑动、看结果、必要时重复，而不是一次大滑；
- **"Only tap things you can actually see on this screenshot; never guess where a button might be"**——只点你真看得见的，永远别猜按钮在哪；
- 时间滚轮的策略是先点中间行的数字直接键入 0700；不行再「量出相邻两行的间距，滑 k 倍间距移 k 行」——从像素测量推出离散滚动的传动比；
- 独立动作打包（一次最多 6 条 DO，连续勾选星期几），依赖结果就单条——**把控制流的信息结构留给模型自己判断**；
- 小目标用 `tap X Y precise`：点击前先定位指针再修正，多花约 1 秒，换小图标/开关的命中率。

制度设计同样在细节里：40 步硬上限；连续 3 次失败熔断退出；**板子断线重连成功不算 agent 的错、不占失败预算**；画面丢失直接抛 `BlindError` 拒绝行动——"never let the model act blind"，宁停不瞎猜。

## 为什么是现在

这条路线的每个零件都存在了好几年：UxPlay 是成熟的开源 AirPlay 接收器，ESP32-S3 的 USB HID 是 Arduino 生态的常规操作，帧差定位是计算机视觉的入门练习。真正的变量是**视觉模型终于便宜且可靠到了能当「眼睛」用**——0-1000 归一化坐标输出、对 UI 元素中心的稳定 grounding，两年前的模型做不到这个精度。另外两个设计选择让它获得了远超 demo 的可信度：step wall 把每一步的截图、模型 reasoning、耗时全部留痕可回放（这是给审计的接口，不是给观众的）；README 的 quick start 干脆是一段直接粘给 Claude Code/Codex 的自然语言安装指令——文档本身就是为 agent 写的。

## 诚实账单与更大的图景

代价明摆着：每步一次视觉模型往返，precise tap 再加一秒，一个闹钟任务要几十秒到几分钟；AirPlay 镜像需要手动开启；AssistiveTouch 圆形指针常驻屏幕。它不是快路，是**免许可的路**——银行 app、游戏、任何反自动化的 app，对「一只普通 USB 鼠标」都无从拒绝（当然，ToS 合规请自查）。

放到更大的坐标里看：昨天我们聊了 MCP/A2A 那条 API 路径——精确、快速、但需要平台**主动配合**。esp32-iphone-agent 是另一条路：慢一个数量级，但**不需要任何人的许可**，因为接口特权是随「人的身体」自动附赠的。hardware-in-the-loop 在测试领域是老词，agent 时代它正在变成一种部署形态：$7 买的不只是开发板，是对整条 Apple 开发者工具链签名体系的豁免。

**行动项：** ① 有「无 API 的 app」自动化需求（真机回归矩阵、游戏、长辈手机的远程协助），把 HID 路径列入备选，成本 = 一块 XIAO ESP32S3 + 一个 USB-C 带供电 hub；② 写 embodied agent 的 prompt 时学它：把介质物理性质（无动量、可见性边界、变化检测反馈）显式写进动作协议，比堆思维链有效；③ 工具设计学它两条——「板子零逻辑」把智能留在可迭代的一侧，README 的 quick start 本身就是写给 coding agent 的安装指令（agent 时代的文档形态）。
