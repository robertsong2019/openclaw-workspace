#!/usr/bin/env python3
"""
MindMap v3 - 从文本生成美观的 ASCII 思维导图
核心改进：基于逆频率的关键词提取 + 对称树状布局

用法: python mindmap3.py                    # Demo模式
     python mindmap3.py -t "文本内容"
     python mindmap3.py file.txt
     echo "文本" | python mindmap3.py
"""
import sys, re, math
from collections import Counter

STOP = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一',
    '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看',
    '好', '自己', '这', '他', '她', '它', '们', '那', '些', '什么', '怎么',
    '可以', '因为', '所以', '但是', '如果', '虽然', '而且', '或者', '以及',
    '还是', '已经', '正在', '应该', '需要', '能够', '这个', '那个', '这些',
    '那些', '其中', '通过', '进行', '使用', '关于', '对于', '作为', '为',
    '从', '把', '被', '让', '给', '向', '与', '对', '及', '等', '之',
    '中', '下', '里', '后', '前', '时', '年', '月', '日', '个', '种',
    'the','a','an','is','are','was','were','be','been','being','have','has',
    'had','do','does','did','will','would','could','should','may','might',
    'can','need','to','of','in','for','on','with','at','by','from','as',
    'and','but','or','not','so','yet','if','when','where','how','what',
    'which','who','this','that','it','its','than','too','very','just',
}


def extract(text: str, n: int = 15) -> list[tuple[str, int]]:
    """关键词提取：按标点断句，滑动窗口提取 n-gram"""
    # 按标点分割成短语
    phrases = re.split(r'[，。！？、；：\u201c\u201d\u2018\u2019（）【】《》\s,.\-!?;:()\[\]{}|/\\]+', text)
    phrases = [p.strip() for p in phrases if len(p.strip()) >= 2]
    
    # 从每个短语提取 2-4 字的中文 n-gram
    cn_ngrams = Counter()
    for phrase in phrases:
        cn_chars = re.findall(r'[\u4e00-\u9fff]+', phrase)
        for segment in cn_chars:
            for length in [4, 3, 2]:
                for i in range(len(segment) - length + 1):
                    gram = segment[i:i+length]
                    if gram not in STOP:
                        cn_ngrams[gram] += 1
            # 也计单字频率用于惩罚
            for ch in segment:
                if ch in STOP:
                    cn_ngrams[ch] += 0  # 不计数但确保在字典中
    
    # 英文单词
    en_words = Counter()
    for w in re.findall(r'[a-zA-Z][a-zA-Z0-9_\-.]{2,}', text):
        wl = w.lower()
        if wl not in STOP and len(wl) >= 3:
            en_words[wl] += 1
    
    # 合并并排序
    all_tokens = Counter()
    for gram, count in cn_ngrams.items():
        if len(gram) >= 2 and gram not in STOP:
            # 惩罚：如果3字或4字词包含在更高频的2字词中，降权
            all_tokens[gram] = count
    for w, c in en_words.items():
        all_tokens[w] = c
    
    # 去除冗余：如果短词是长词的子串且频率相同，保留长词
    items = sorted(all_tokens.items(), key=lambda x: (-x[1], -len(x[0])))
    result = []
    seen_parts = set()
    for word, count in items:
        # 检查是否已被包含
        skip = False
        for existing in seen_parts:
            if word in existing and count == all_tokens.get(existing, 0):
                skip = True
                break
        if not skip:
            result.append((word, count))
            seen_parts.add(word)
    
    return result[:n]


def tree_mindmap(kws: list[tuple[str, int]], title: str) -> str:
    """生成对称树状思维导图"""
    if not kws:
        return "  (未提取到关键词)\n"
    
    max_w = kws[0][1]
    n = len(kws)
    
    # 构建层级结构
    # Level 0: 中心
    # Level 1: 前 N/3 个关键词（主分支）
    # Level 2: 中间 N/3（子分支）
    # Level 3: 剩余（叶子）
    
    l1_count = max(2, (n + 2) // 3)
    l2_count = max(0, (n - l1_count + 1) // 2)
    
    l1 = kws[:l1_count]
    l2 = kws[l1_count:l1_count + l2_count]
    l3 = kws[l1_count + l2_count:]
    
    # 分配子节点
    branches = []
    for i, (w, c) in enumerate(l1):
        children = []
        # 给每个主分支分配 l2 节点
        l2_per = max(1, len(l2) // len(l1))
        start = i * l2_per
        for j in range(start, min(start + l2_per + (1 if i == len(l1)-1 else 0), len(l2))):
            child_word, child_count = l2[j]
            grandchildren = []
            # 给每个 l2 分配 l3
            if l3:
                l3_per = max(0, len(l3) // max(1, len(l2)))
                l3_start = j * l3_per if j < len(l2) else len(l3)
                for k in range(l3_start, min(l3_start + l3_per, len(l3))):
                    grandchildren.append((l3[k][0], l3[k][1]))
            children.append((child_word, child_count, grandchildren))
        branches.append((w, c, children))
    
    # 左右分配
    mid = (len(branches) + 1) // 2
    left = list(reversed(branches[:mid]))
    right = branches[mid:]
    
    def sym(weight):
        r = weight / max_w
        return '◆' if r > 0.7 else ('◇' if r > 0.4 else '○')
    
    def bar(weight, full='█', max_len=10):
        return full * max(1, int(weight / max_w * max_len))
    
    # 计算最大行宽
    max_word_len = max(len(w) for w, _, _ in kws) if kws else 6
    col_w = max_word_len + 16  # 符号 + 词 + bar + 数字
    
    lines = []
    
    # Header
    box_w = col_w * 2 + 8
    lines.append("╭" + "─" * box_w + "╮")
    pad = box_w // 2 - len(title) // 2 - 2
    lines.append("│" + " " * pad + f"🧠 {title}" + " " * (box_w - pad - len(title) - 3) + "│")
    lines.append("├" + "─" * box_w + "┤")
    
    def pad_line(content, width=box_w):
        # 去除ANSI等控制字符计算长度
        clean = re.sub(r'\x1b\[[0-9;]*m', '', content)
        actual = len(clean)
        # 中文字符占2宽度
        display_w = sum(2 if ord(c) > 127 else 1 for c in clean)
        padding = width - display_w
        if padding < 0:
            padding = 0
        return content + " " * padding + "│"
    
    # 右侧分支
    for word, count, children in right:
        s = sym(count)
        b = bar(count)
        lines.append(pad_line(f"│     {s} {word} {b} ({count})"))
        for i, (cw, cc, gc) in enumerate(children):
            conn = '└──' if i == len(children) - 1 else '├──'
            cs = sym(cc)
            cb = bar(cc, '░', 8)
            lines.append(pad_line(f"│     │  {conn} {cs} {cw} {cb} ({cc})"))
            for j, (gw, gc_count) in enumerate(gc):
                gc_conn = '└──' if j == len(gc) - 1 else '├──'
                gs = sym(gc_count)
                lines.append(pad_line(f"│     │     │  {gc_conn} {gs} {gw} ({gc_count})"))
        lines.append("│" + " " * box_w + "│")
    
    # Center
    lines.append(pad_line(f"│          ─── ◉ {title} ───"))
    lines.append("│" + " " * box_w + "│")
    
    # 左侧分支（镜像）
    for word, count, children in left:
        s = sym(count)
        b = bar(count)
        lines.append(pad_line(f"│     {b} {word} {s} ({count})"))
        for i, (cw, cc, gc) in enumerate(children):
            conn = '┘' if i == len(children) - 1 else '┤'
            cs = sym(cc)
            cb = bar(cc, '░', 8)
            lines.append(pad_line(f"│     {conn}── {cb} {cw} {cs} ({cc})  "))
            for j, (gw, gc_count) in enumerate(gc):
                gc_conn = '┘' if j == len(gc) - 1 else '┤'
                gs = sym(gc_count)
                lines.append(pad_line(f"│        {gc_conn}── {gw} {gs} ({gc_count})  "))
        lines.append("│" + " " * box_w + "│")
    
    lines.append("╰" + "─" * box_w + "╯")
    lines.append("")
    lines.append(f"  词频图例: ◆ 高频 (>70%)  ◇ 中频 (40-70%)  ○ 低频 (<40%)")
    lines.append(f"  共提取 {len(kws)} 个关键词，最高频次 {max_w}")
    
    return '\n'.join(lines)


def main():
    import argparse
    p = argparse.ArgumentParser(description='MindMap v3')
    p.add_argument('file', nargs='?')
    p.add_argument('-t', '--text')
    p.add_argument('-n', '--top', type=int, default=12)
    p.add_argument('--title', default='主题')
    a = p.parse_args()
    
    if a.text:
        text = a.text
    elif a.file:
        text = open(a.file, encoding='utf-8').read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        text = ("人工智能和机器学习正在深刻改变我们的世界和生活方式。"
                "深度学习作为机器学习的重要分支，推动了计算机视觉和"
                "自然语言处理领域的重大突破。神经网络是深度学习的技术核心，"
                "卷积神经网络和循环神经网络是两种关键的网络架构。"
                "强化学习在游戏AI和机器人控制领域取得了显著进展。"
                "数据科学结合统计学和计算机科学为业务决策提供数据支持。"
                "Python是人工智能研究和应用中最流行的编程语言。"
                "TensorFlow和PyTorch是目前最主流的深度学习框架。"
                "大语言模型如GPT系列正在引领新一轮人工智能革命。"
                "人工智能应用场景越来越广泛，从医疗到教育到金融。")
        a.title = "AI技术生态"
    
    kws = extract(text, a.top)
    print(tree_mindmap(kws, a.title))


if __name__ == '__main__':
    main()
