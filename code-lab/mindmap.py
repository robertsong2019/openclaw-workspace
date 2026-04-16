#!/usr/bin/env python3
"""
MindMap Generator - 从文本生成 ASCII 思维导图
用法: echo "你的文本" | python mindmap.py
     python mindmap.py file.txt
     python mindmap.py -t "你的主题和关键词"
"""
import sys
import re
import math
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

# 简单的中文停用词
STOP_WORDS = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一',
    '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着',
    '没有', '看', '好', '自己', '这', '他', '她', '它', '们', '那', '些',
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'need', 'dare', 'ought',
    'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
    'as', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'between', 'out', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'and', 'but', 'or', 'nor', 'not', 'so', 'yet', 'both',
    'either', 'neither', 'each', 'every', 'all', 'any', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'only', 'own', 'same', 'than',
    'too', 'very', 'just', 'because', 'if', 'when', 'where', 'how', 'what',
    'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'it', 'its',
}

BORDER_STYLES = {
    'round':  ('╭', '╮', '╰', '╯', '│', '─'),
    'square': ('┌', '┐', '└', '┘', '│', '─'),
    'star':   ('✦', '✦', '✦', '✦', '║', '═'),
}


@dataclass
class Node:
    word: str
    weight: int
    x: int = 0
    y: int = 0
    children: list = field(default_factory=list)
    angle: float = 0


def extract_keywords(text: str, top_n: int = 12) -> list[tuple[str, int]]:
    """提取关键词及其权重"""
    # 分离中英文
    # 中文：逐字/词（简单按2-4字切分）
    cn_pattern = re.compile(r'[\u4e00-\u9fff]{2,4}')
    en_pattern = re.compile(r'[a-zA-Z][a-zA-Z0-9_\-]{2,}')
    
    cn_words = cn_pattern.findall(text)
    en_words = en_pattern.findall(text)
    
    # 也提取单个重要中文字
    cn_singles = re.findall(r'[\u4e00-\u9fff]', text)
    
    all_words = cn_words + [w.lower() for w in en_words]
    
    # 过滤停用词
    filtered = [w for w in all_words if w not in STOP_WORDS and len(w) >= 2]
    
    counter = Counter(filtered)
    return counter.most_common(top_n)


def make_box(text: str, style: str = 'round', padding: int = 1) -> list[str]:
    """围绕文本创建边框"""
    tl, tr, bl, br, v, h = BORDER_STYLES.get(style, BORDER_STYLES['round'])
    pad = ' ' * padding
    width = len(text) + padding * 2
    
    top = tl + h * width + tr
    mid = v + pad + text + pad + v
    bot = bl + h * width + br
    
    return [top, mid, bot]


def generate_ascii_mindmap(keywords: list[tuple[str, int]], title: str = "MindMap") -> str:
    """生成 ASCII 思维导图"""
    if not keywords:
        return "  (无关键词可展示)\n"
    
    # 中心节点
    center = title[:16] if title else "●"
    
    # 构建层级：中心 → 主分支 → 子分支
    max_weight = keywords[0][1] if keywords else 1
    
    # 分成主分支和子分支
    main_branches = []
    sub_branches = []
    
    for i, (word, weight) in enumerate(keywords):
        node = Node(word, weight)
        if i < len(keywords) // 2 + 1:
            main_branches.append(node)
        else:
            sub_branches.append(node)
    
    # 分配子分支到主分支
    for i, sub in enumerate(sub_branches):
        parent_idx = i % len(main_branches)
        main_branches[parent_idx].children.append(sub)
    
    # 计算布局
    lines = []
    n = len(main_branches)
    
    # 上半部分和下半部分
    top_branches = main_branches[:n//2 + n%2]
    bot_branches = main_branches[n//2 + n%2:]
    
    # 左右分配
    left_top = top_branches[:len(top_branches)//2]
    right_top = top_branches[len(top_branches)//2:]
    left_bot = bot_branches[:len(bot_branches)//2]
    right_bot = bot_branches[len(bot_branches)//2:]
    
    # 生成中心盒子
    center_box = make_box(f" 🧠 {center} ", 'star')
    center_h = len(center_box)
    center_w = len(center_box[0])
    
    # 收集所有输出行
    output_parts = []
    
    # 画上半部分
    for branch in (left_top + right_top):
        weight_ratio = branch.weight / max_weight
        symbol = '●' if weight_ratio > 0.7 else ('○' if weight_ratio > 0.4 else '·')
        line = f"  {symbol} {branch.word} ({branch.weight})"
        
        for child in branch.children:
            child_sym = '→' if child.weight / max_weight > 0.3 else '↳'
            line += f"\n    {child_sym} {child.word} ({child.weight})"
        
        output_parts.append(('top', 'left' if branch in left_top else 'right', line))
    
    # 中心
    output_parts.append(('center', '', '\n'.join(center_box)))
    
    # 画下半部分
    for branch in (left_bot + right_bot):
        weight_ratio = branch.weight / max_weight
        symbol = '●' if weight_ratio > 0.7 else ('○' if weight_ratio > 0.4 else '·')
        line = f"  {symbol} {branch.word} ({branch.weight})"
        
        for child in branch.children:
            child_sym = '→' if child.weight / max_weight > 0.3 else '↳'
            line += f"\n    {child_sym} {child.word} ({child.weight})"
        
        output_parts.append(('bot', 'left' if branch in left_bot else 'right', line))
    
    # 组装最终输出
    result = []
    result.append("╔══════════════════════════════════════╗")
    result.append("║        🗺️  ASCII MindMap Gen          ║")
    result.append("╚══════════════════════════════════════╝")
    result.append("")
    
    # 左右布局
    top_lines = []
    bot_lines = []
    
    for pos, side, text in output_parts:
        if pos == 'top':
            top_lines.append(text)
        elif pos == 'bot':
            bot_lines.append(text)
    
    left_top_lines = []
    right_top_lines = []
    
    # 简单顺序输出
    for pos, side, text in output_parts:
        if pos == 'center':
            result.append(text)
            result.append("")
        else:
            for line in text.split('\n'):
                if pos == 'top':
                    result.append("    " + line)
                else:
                    result.append("    " + line)
    
    # 加权重图例
    result.append("")
    result.append("  图例: ● 高频  ○ 中频  · 低频")
    result.append(f"  关键词数: {sum(1 + len(b.children) for _, b in [(0, nb) for nb in main_branches])}")
    
    return '\n'.join(result)


def generate_radial_mindmap(keywords: list[tuple[str, int]], title: str = "MindMap") -> str:
    """生成径向布局的 ASCII 思维导图"""
    if not keywords:
        return "  (无关键词可展示)\n"
    
    max_weight = keywords[0][1]
    n = len(keywords)
    
    # 径向角度分配
    angle_step = 2 * math.pi / max(n, 1)
    radius = 10  # 字符为单位的半径
    
    # 画布
    width, height = 60, 30
    canvas = [[' '] * width for _ in range(height)]
    cx, cy = width // 2, height // 2
    
    # 中心
    center_text = title[:6] if title else "●"
    for i, ch in enumerate(center_text):
        if cx - len(center_text)//2 + i < width:
            canvas[cy][cx - len(center_text)//2 + i] = ch
    
    # 放置关键词
    positions = []
    for i, (word, weight) in enumerate(keywords):
        angle = angle_step * i - math.pi / 2
        # 终端字符宽高比约 2:1
        x = int(cx + radius * math.cos(angle))
        y = int(cy + radius * math.sin(angle) * 0.5)
        
        x = max(0, min(width - len(word) - 1, x))
        y = max(0, min(height - 1, y))
        
        positions.append((x, y, word, weight))
        
        # 画连接线（简化：画点）
        steps = max(abs(x - cx), abs(y - cy))
        if steps > 0:
            for s in range(1, steps):
                lx = int(cx + (x - cx) * s / steps)
                ly = int(cy + (y - cy) * s / steps)
                if 0 <= lx < width and 0 <= ly < height and canvas[ly][lx] == ' ':
                    canvas[ly][lx] = '·'
        
        # 放置文字
        for j, ch in enumerate(word):
            if x + j < width and 0 <= y < height:
                canvas[y][x + j] = ch
    
    # 渲染
    lines = []
    lines.append("┌" + "─" * width + "┐")
    for row in canvas:
        lines.append("│" + ''.join(row) + "│")
    lines.append("└" + "─" * width + "┘")
    
    # 下方列出关键词
    lines.append("")
    legend_items = []
    for word, weight in keywords:
        ratio = weight / max_weight
        bar = '█' * int(ratio * 10)
        legend_items.append(f"  {word:<12} {bar} {weight}")
    
    lines.append('\n'.join(legend_items))
    
    return '\n'.join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='ASCII MindMap Generator')
    parser.add_argument('file', nargs='?', help='输入文本文件')
    parser.add_argument('-t', '--text', help='直接输入文本')
    parser.add_argument('-n', '--top', type=int, default=10, help='提取前N个关键词')
    parser.add_argument('-r', '--radial', action='store_true', help='使用径向布局')
    parser.add_argument('--title', default='主题', help='中心主题文字')
    args = parser.parse_args()
    
    # 读取文本
    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        # Demo mode
        text = """
        人工智能 机器学习 深度学习 神经网络 自然语言处理
        计算机视觉 强化学习 数据科学 算法 代码编程
        Python JavaScript TypeScript 开发框架 前端开发
        后端架构 数据库 云计算 微服务 容器化部署
        人工智能改变世界，机器学习是核心驱动力
        深度学习推动计算机视觉和自然语言处理突破
        """
        args.title = "AI技术"
    
    keywords = extract_keywords(text, args.top)
    
    if args.radial:
        print(generate_radial_mindmap(keywords, args.title))
    else:
        print(generate_ascii_mindmap(keywords, args.title))


if __name__ == '__main__':
    main()
