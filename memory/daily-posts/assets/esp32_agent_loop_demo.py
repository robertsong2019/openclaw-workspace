#!/usr/bin/env python3
"""迷你闭环：相对 HID 指针 -> iOS 球状加速 -> 屏幕帧 -> 帧差定位 -> 修正。
模拟 esp32-iphone-agent 的三层机制：
  1) home 撞角：饱和让累计误差归零
  2) 定速步进：躲开加速曲线的非线性区（对比一步到位）
  3) wiggle-locate：帧差找到指针真实位置，闭合残差
"""
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
        self.px, self.py = random.uniform(0, W), random.uniform(0, H)  # 指针真实位置（服务器不可见）
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
est_err = ((phone.px - target[0]) ** 2 + (phone.py - target[1]) ** 2) ** 0.5
print(f"   定速步进: 发 ({target[0]},{target[1]})，落在 ({phone.px:.1f},{phone.py:.1f})，偏差 {est_err:.1f}px"
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
