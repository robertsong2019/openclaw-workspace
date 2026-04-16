#!/usr/bin/env python3
"""
MindMap Generator v2 - 从文本生成 ASCII 思维导图
改进：更好的中文分词、树状辐射布局、权重可视化

用法: python mindmap2.py -t "你的文本内容"
     python mindmap2.py file.txt
     echo "文本" | python mindmap2.py
"""
import sys
import re
import math
from collections import Counter
from dataclasses import dataclass, field


STOP_WORDS = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一',
    '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着',
    '没有', '看', '好', '自己', '这', '他', '她', '它', '们', '那', '些',
    '什么', '怎么', '可以', '因为', '所以', '但是', '如果', '虽然', '而且',
    '或者', '以及', '还是', '已经', '正在', '应该', '需要', '能够', '这个',
    '那个', '这些', '那些', '其中', '通过', '进行', '使用', '关于', '对于',
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'need', 'to', 'of', 'in',
    'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through',
    'and', 'but', 'or', 'not', 'so', 'yet', 'if', 'when', 'where', 'how',
    'what', 'which', 'who', 'this', 'that', 'it', 'its', 'than', 'too',
    'very', 'just', 'also', 'then', 'there', 'here', 'all', 'each',
    'every', 'both', 'any', 'few', 'more', 'most', 'some', 'such', 'no',
    'only', 'own', 'same', 'other', 'about', 'up', 'out', 'off',
}


# 常见中文技术词汇（用于正向最大匹配）
COMMON_TERMS = {
    '人工智能', '机器学习', '深度学习', '神经网络', '自然语言处理', '计算机视觉',
    '强化学习', '数据科学', '前端开发', '后端开发', '微服务', '容器化',
    '云计算', '大数据', '区块链', '物联网', '边缘计算', '量子计算',
    '数字化转型', '敏捷开发', '持续集成', '持续部署', '代码审查',
    '设计模式', '面向对象', '函数式编程', '响应式编程', '并发编程',
    '分布式系统', '负载均衡', '高可用', '故障转移', '数据一致性',
    '关系数据库', '非关系数据库', '文档数据库', '图数据库',
    '搜索引擎', '推荐系统', '内容分发', '网络安全', '数据隐私',
    '用户体验', '交互设计', '信息架构', '可视化', '数据治理',
    '特征工程', '模型训练', '超参数', '损失函数', '激活函数',
    '卷积网络', '循环网络', '注意力机制', '生成对抗', '迁移学习',
    '联邦学习', '知识蒸馏', '模型压缩', '推理优化',
}

# 添加2-4字的技术词汇
for term in list(COMMON_TERMS):
    for length in range(2, min(len(term), 5)):
        pass  # 只匹配完整词


def segment_chinese(text: str) -> list[str]:
    """简易中文分词：正向最大匹配 + 常见词汇表"""
    tokens = []
    # 先按标点和空格分割
    segments = re.split(r'[，。！？、；：""''（）【】《》\s,.\-!?;:()\[\]{}<>/\\|@#$%^&*+=~`]', text)
    
    for seg in segments:
        if not seg:
            continue
        i = 0
        while i < len(seg):
            matched = False
            # 尝试匹配4字、3字、2字
            for length in [4, 3, 2]:
                if i + length <= len(seg):
                    candidate = seg[i:i+length]
                    if candidate in COMMON_TERMS or (length >= 2 and candidate not in STOP_WORDS and re.match(r'^[\u4e00-\u9fff]+$', candidate)):
                        # 检查是否是常见术语的一部分（优先长匹配）
                        longer_match = None
                        for l in [4, 3]:
                            if l > length and i + l <= len(seg) and seg[i:i+l] in COMMON_TERMS:
                                longer_match = seg[i:i+l]
                                break
                        if longer_match:
                            tokens.append(longer_match)
                            i += len(longer_match)
                        else:
                            tokens.append(candidate)
                            i += length
                        matched = True
                        break
            if not matched:
                if seg[i] not in STOP_WORDS and re.match(r'[\u4e00-\u9fff]', seg[i]):
                    # 单字跳过，除非特别重要
                    pass
                i += 1
    
    return tokens


def extract_keywords(text: str, top_n: int = 12) -> list[tuple[str, int]]:
    """提取关键词"""
    # 中文分词
    cn_tokens = segment_chinese(text)
    
    # 英文单词
    en_words = re.findall(r'[a-zA-Z][a-zA-Z0-9_\-.]{2,}', text)
    en_words = [w.lower() for w in en_words if w.lower() not in STOP_WORDS]
    
    all_tokens = cn_tokens + en_words
    filtered = [w for w in all_tokens if w not in STOP_WORDS and len(w) >= 2]
    
    counter = Counter(filtered)
    return counter.most_common(top_n)


@dataclass
class Branch:
    word: str
    weight: int
    children: list = field(default_factory=list)


def generate_tree_mindmap(keywords: list[tuple[str, int]], title: str = "主题") -> str:
    """生成树状思维导图，左右对称分布"""
    if not keywords:
        return "  (无关键词)\n"
    
    max_w = keywords[0][1]
    n = len(keywords)
    
    # 分配层级
    # 前1/3作为一级分支，中间1/3作为二级，其余作为三级
    tier1_count = max(2, (n + 2) // 4)
    
    branches = []
    for i in range(min(tier1_count, n)):
        branches.append(Branch(keywords[i][0], keywords[i][1]))
    
    # 分配二级
    idx = tier1_count
    for i, branch in enumerate(branches):
        if idx < n:
            branch.children.append(Branch(keywords[idx][0], keywords[idx][1]))
            idx += 1
        if idx < n and i < len(branches) // 2:
            branch.children.append(Branch(keywords[idx][0], keywords[idx][1]))
            idx += 1
    
    # 剩余分配为三级
    for branch in branches:
        for child in branch.children:
            if idx < n:
                child.children.append(Branch(keywords[idx][0], keywords[idx][1]))
                idx += 1
    
    # 左右分配分支
    mid = (len(branches) + 1) // 2
    left_branches = list(reversed(branches[:mid]))
    right_branches = branches[mid:]
    
    def weight_symbol(w):
        ratio = w / max_w
        if ratio > 0.7: return '◆'
        if ratio > 0.4: return '◇'
        return '·'
    
    def draw_branch_left(branch: Branch, prefix: str = "") -> list[str]:
        """从右向左画的分支"""
        sym = weight_symbol(branch.weight)
        lines = [f"{prefix}{sym} {branch.word}"]
        for i, child in enumerate(branch.children):
            connector = '╰' if i == len(branch.children) - 1 else '├'
            child_lines = draw_branch_left(child, prefix + (' ' if i == len(branch.children) - 1 else '│') + ' ')
            lines[0] = f"{prefix}{sym} {branch.word}"  # 主词
            # 重新组织：主词在上，子项在下
        return lines
    
    def format_right_branch(branch: Branch, indent: str = "") -> str:
        sym = weight_symbol(branch.weight)
        bar = '█' * max(1, int(branch.weight / max_w * 8))
        result = f"{indent}{sym} {branch.word} {bar}"
        for i, child in enumerate(branch.children):
            c_sym = weight_symbol(child.weight)
            c_bar = '░' * max(1, int(child.weight / max_w * 6))
            conn = '└' if i == len(branch.children) - 1 else '├'
            result += f"\n{indent}  {conn}─ {c_sym} {child.word} {c_bar}"
            for j, gc in enumerate(child.children):
                gc_sym = weight_symbol(gc.weight)
                gc_conn = '└' if j == len(child.children) - 1 else '├'
                result += f"\n{indent}  │   {gc_conn}─ {gc_sym} {gc.word}"
        return result
    
    def format_left_branch(branch: Branch, indent: str = "") -> str:
        sym = weight_symbol(branch.weight)
        bar = '█' * max(1, int(branch.weight / max_w * 8))
        result = f"{bar} {branch.word} {sym}{indent}"
        for i, child in enumerate(branch.children):
            c_sym = weight_symbol(child.weight)
            c_bar = '░' * max(1, int(child.weight / max_w * 6))
            conn = '└' if i == len(branch.children) - 1 else '├'
            result += f"\n{c_bar} {child.word} {c_sym} ─{conn}{indent}"
            for j, gc in enumerate(child.children):
                gc_sym = weight_symbol(gc.weight)
                gc_conn = '└' if j == len(child.children) - 1 else '├'
                result += f"\n  {gc.word} {gc_sym} ─{gc_conn}{indent}"
        return result
    
    # 组装
    lines = []
    w = 44
    lines.append("┌" + "─" * w + "┐")
    title_pad = w // 2 - len(title) // 2 - 1
    lines.append("│" + " " * title_pad + f"🧠 {title}" + " " * (w - title_pad - len(title) - 3) + "│")
    lines.append("├" + "─" * w + "┤")
    lines.append("│" + " " * w + "│")
    
    # 右侧分支
    for branch in right_branches:
        for line in format_right_branch(branch, "  ").split('\n'):
            lines.append("│  " + line.ljust(w - 2) + "│")
        lines.append("│" + " " * w + "│")
    
    # 中心
    center_line = f"│  {'─' * 3} ◉ {title} {'─' * 3}"
    lines.append(center_line + " " * max(0, w - len(center_line) + 1) + "│")
    lines.append("│" + " " * w + "│")
    
    # 左侧分支
    for branch in left_branches:
        for line in format_left_branch(branch, "  ").split('\n'):
            lines.append("│  " + line.ljust(w - 2) + "│")
        lines.append("│" + " " * w + "│")
    
    lines.append("└" + "─" * w + "┘")
    lines.append("")
    lines.append(f"  关键词统计: 共 {len(keywords)} 个 | ◆ 高频 ◇ 中频 · 低频")
    
    return '\n'.join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='ASCII MindMap Generator v2')
    parser.add_argument('file', nargs='?', help='输入文本文件')
    parser.add_argument('-t', '--text', help='直接输入文本')
    parser.add_argument('-n', '--top', type=int, default=12, help='提取前N个关键词')
    parser.add_argument('--title', default='主题', help='中心主题')
    args = parser.parse_args()
    
    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        text = """
        人工智能和机器学习正在改变我们的世界。深度学习作为机器学习的分支，
        推动了计算机视觉和自然语言处理的重大突破。神经网络是深度学习的核心，
        卷积网络和循环网络是两种重要的网络结构。强化学习在游戏和机器人领域
        取得了显著进展。数据科学结合统计学和计算机科学，为业务决策提供支持。
        Python是人工智能领域最流行的编程语言，拥有丰富的机器学习库。
        TensorFlow和PyTorch是两个主流的深度学习框架。
        """
        args.title = "AI技术生态"
    
    keywords = extract_keywords(text, args.top)
    print(generate_tree_mindmap(keywords, args.title))


if __name__ == '__main__':
    main()
