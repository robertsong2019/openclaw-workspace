#!/usr/bin/env python3
"""
MindMap v4 - ASCII 思维导图生成器
基于词典的正向最大匹配分词 + 对称树状布局

用法: python mindmap4.py              # Demo
     python mindmap4.py -t "文本"
     python mindmap4.py file.txt
"""
import sys, re, math, unicodedata
import jieba
from collections import Counter


# === 词典 ===
# 技术/通用词汇表（用于分词）
DICT = {
    # AI/技术
    '人工智能', '机器学习', '深度学习', '神经网络', '自然语言处理', '计算机视觉',
    '强化学习', '数据科学', '前端开发', '后端开发', '微服务', '容器化',
    '云计算', '大数据', '区块链', '物联网', '边缘计算', '量子计算',
    '大语言模型', '生成对抗网络', '卷积神经网络', '循环神经网络',
    '注意力机制', '迁移学习', '联邦学习', '知识蒸馏', '模型压缩',
    '特征工程', '模型训练', '超参数', '损失函数', '激活函数',
    '数据治理', '数据挖掘', '数据分析', '数据可视化',
    '推荐系统', '搜索引擎', '内容分发', '网络安全', '数据隐私',
    '分布式系统', '负载均衡', '高可用', '故障转移',
    '敏捷开发', '持续集成', '持续部署', '代码审查',
    '设计模式', '面向对象', '函数式编程', '响应式编程',
    '用户体验', '交互设计', '信息架构',
    '编程语言', '开源项目', '技术架构',
    # 通用高频词组
    '改变世界', '生活方式', '重要分支', '重大突破', '技术核心',
    '显著进展', '业务决策', '数据支持', '应用场景', '新一轮',
    '游戏AI', '机器人',
}

STOP = {
    # 代词
    '我', '你', '他', '她', '它', '我们', '你们', '他们', '她们', '它们', '这', '那', '这些', '那些',
    # 助词/虚词
    '的', '了', '在', '是', '和', '就', '不', '都', '一', '上', '也', '很', '到', '说', '要', '去',
    '会', '着', '没有', '好', '们', '些', '什么', '怎么', '可以', '因为', '所以', '但是',
    '如果', '虽然', '而且', '或者', '以及', '还是', '已经', '正在', '应该', '需要', '能够',
    '这个', '那个', '其中', '通过', '进行', '使用', '关于', '对于', '作为', '为', '从', '把',
    '被', '让', '给', '向', '与', '对', '及', '等', '之', '中', '下', '里', '后', '前', '时',
    '年', '月', '日', '个', '种', '最', '更', '其', '两',
    # 动词（非技术动作）
    '改变', '推动', '取得', '作出', '作出', '产生', '提供', '实现', '获得', '保持',
    '建立', '形成', '开展', '完成', '达到', '发生', '出现', '存在', '属于',
    # 形容词（通用）
    '深刻', '重大', '显著', '广泛', '重要', '关键', '主要', '基本', '核心',
    '主流', '流行', '常见', '相关', '不同', '各种', '多种', '一定', '许多',
    # 方式/状态
    '正在', '已经', '仍然', '始终', '一直', '始终', '逐渐', '不断',
    # 逻辑
    '并且', '并且', '或是', '也就是', '即', '以及', '与此同时', '此时',
    # 英文
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can', 'need',
    'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'and',
    'but', 'or', 'not', 'so', 'yet', 'if', 'when', 'where', 'how', 'what',
    'which', 'who', 'this', 'that', 'it', 'its', 'than', 'too', 'very', 'just',
    'with', 'for', 'from', 'are', 'also', 'all', 'more', 'other', 'new', 'use',
}


def segment(text: str) -> list[str]:
    """使用 jieba 分词 + 优先长词"""
    # 添加自定义词典（技术词汇优先）
    for term in [
        '人工智能', '机器学习', '深度学习', '神经网络',
        '自然语言处理', '计算机视觉', '强化学习',
        '卷积神经网络', '循环神经网络', '注意力机制',
        '大语言模型', '生成对抗网络', '迁移学习',
        '联邦学习', '知识蒸馏', '模型压缩',
        '特征工程', '模型训练', '超参数',
        '损失函数', '激活函数', '数据治理',
    ]:
        jieba.add_word(term, freq=1000)  # 高频优先
    
    # jieba 分词
    words = jieba.lcut(text, HMM=False)  # 关闭新词发现，用词典
    
    # 过滤：保留中文词、英文词，去除停用词和单字
    tokens = []
    for w in words:
        # 去除空白和标点
        w = w.strip()
        if len(w) < 2:
            continue
        # 去除纯标点
        if re.match(r'^[^\w\u4e00-\u9fff]+$', w):
            continue
        # 去除停用词
        if w in STOP or w.lower() in STOP:
            continue
        tokens.append(w if w.isascii() or w[0].isascii() else w)
    
    return tokens


def extract(text: str, n: int = 12) -> list[tuple[str, int]]:
    tokens = segment(text)
    return Counter(tokens).most_common(n)


def display_width(s: str) -> int:
    """计算字符串的显示宽度（中文占2）"""
    w = 0
    for ch in s:
        if unicodedata.east_asian_width(ch) in ('W', 'F'):
            w += 2
        else:
            w += 1
    return w


def pad_right(s: str, width: int) -> str:
    """右填充到指定显示宽度"""
    dw = display_width(s)
    return s + ' ' * max(0, width - dw)


def tree_map(kws: list[tuple[str, int]], title: str) -> str:
    if not kws:
        return "  (无关键词)\n"
    
    max_w = kws[0][1]
    n = len(kws)
    
    # 层级分配
    n1 = max(2, (n + 2) // 3)  # 主分支数
    n2 = n - n1                 # 子分支数
    
    branches = []
    for i in range(n1):
        children = []
        # 给第i个主分支分配子节点
        for j in range(n2):
            if j % n1 == i % n1:
                child_idx = n1 + j
                if child_idx < n:
                    children.append(kws[child_idx])
        branches.append({'word': kws[i][0], 'weight': kws[i][1], 'children': children})
    
    # 分左右
    mid = (len(branches) + 1) // 2
    left = list(reversed(branches[:mid]))
    right = branches[mid:]
    
    def sym(w):
        r = w / max_w
        return '◆' if r > 0.7 else ('◇' if r > 0.4 else '○')
    
    def bar(w, char='█', maxlen=10):
        return char * max(1, round(w / max_w * maxlen))
    
    # 计算布局宽度
    max_word_w = max((display_width(w) for w, _ in kws), default=4)
    branch_w = max_word_w + 20  # sym + word + bar + count
    box_w = max(50, branch_w + 12)
    
    lines = []
    
    # === Header ===
    lines.append('╭' + '─' * box_w + '╮')
    title_disp = f'🧠 {title}'
    title_pad = (box_w - display_width(title_disp)) // 2
    lines.append('│' + ' ' * title_pad + title_disp + ' ' * (box_w - title_pad - display_width(title_disp)) + '│')
    lines.append('├' + '─' * box_w + '┤')
    
    # === Right branches ===
    for b in right:
        s, w = sym(b['weight']), b['weight']
        line = f'│      {s} {b["word"]} {bar(w)} ({w})'
        lines.append(pad_right(line, box_w) + '│')
        for i, (cw, cc) in enumerate(b['children']):
            conn = '└──' if i == len(b['children']) - 1 else '├──'
            cs = sym(cc)
            line = f'│      │  {conn} {cs} {cw} {bar(cc, "░", 8)} ({cc})'
            lines.append(pad_right(line, box_w) + '│')
        lines.append('│' + ' ' * box_w + '│')
    
    # === Center ===
    center = f'│         ─── ◉ {title} ───'
    lines.append(pad_right(center, box_w) + '│')
    lines.append('│' + ' ' * box_w + '│')
    
    # === Left branches (mirrored) ===
    for b in left:
        s, w = sym(b['weight']), b['weight']
        line = f'│      {bar(w)} {b["word"]} {s} ({w})'
        lines.append(pad_right(line, box_w) + '│')
        for i, (cw, cc) in enumerate(b['children']):
            conn = '┘' if i == len(b['children']) - 1 else '┤'
            cs = sym(cc)
            line = f'│      └── {bar(cc, "░", 8)} {cw} {cs} ({cc})'
            lines.append(pad_right(line, box_w) + '│')
        lines.append('│' + ' ' * box_w + '│')
    
    lines.append('╰' + '─' * box_w + '╯')
    lines.append('')
    lines.append(f'  词频: ◆ 高频(>70%)  ◇ 中频(40-70%)  ○ 低频(<40%)  |  {len(kws)} 个关键词')
    
    return '\n'.join(lines)


def main():
    import argparse
    p = argparse.ArgumentParser(description='MindMap v4')
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
        a.title = 'AI技术生态'
    
    kws = extract(text, a.top)
    print(tree_map(kws, a.title))


if __name__ == '__main__':
    main()
