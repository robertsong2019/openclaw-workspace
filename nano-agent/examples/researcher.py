"""
研究助理代理示例
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nano_agent import Agent, tool


@tool
def search_papers(topic: str, max_results: int = 5) -> str:
    """搜索学术论文

    Args:
        topic: 研究主题
        max_results: 最大结果数

    Returns:
        论文列表
    """
    # 模拟搜索结果
    papers = [
        {
            "title": f"Advances in {topic}",
            "authors": "Smith et al.",
            "year": 2024,
            "citations": 42
        },
        {
            "title": f"A Survey of {topic}",
            "authors": "Johnson & Lee",
            "year": 2023,
            "citations": 128
        },
        {
            "title": f"{topic}: Methods and Applications",
            "authors": "Chen et al.",
            "year": 2025,
            "citations": 15
        }
    ]

    result = f"找到 {len(papers)} 篇相关论文:\n\n"
    for i, paper in enumerate(papers[:max_results], 1):
        result += f"{i}. {paper['title']}\n"
        result += f"   作者: {paper['authors']} | 年份: {paper['year']} | 引用: {paper['citations']}\n"

    return result


@tool
def summarize_paper(paper_title: str) -> str:
    """总结论文内容

    Args:
        paper_title: 论文标题

    Returns:
        论文摘要
    """
    return f"""
## {paper_title} - 摘要

### 主要贡献
- 提出了新的方法
- 在多个数据集上进行了实验
- 达到了最先进的性能

### 关键发现
1. 方法 X 比方法 Y 快 2 倍
2. 准确率提升了 15%
3. 计算成本降低了一半

### 未来方向
- 扩展到更大规模的数据集
- 优化内存使用
- 应用到实际问题中
""".strip()


@tool
def extract_key_concepts(paper_title: str) -> str:
    """提取论文关键概念

    Args:
        paper_title: 论文标题

    Returns:
        关键概念列表
    """
    concepts = [
        "深度学习",
        "神经网络",
        "优化算法",
        "特征提取",
        "模型评估"
    ]
    return f"关键概念: {', '.join(concepts)}"


# 创建代理
researcher = Agent(
    name="研究助理",
    instructions="""你是一个专业的研究助理，帮助用户：
1. 搜索和筛选学术论文
2. 总结和提炼关键信息
3. 提取核心概念和方法
4. 提供研究建议和方向

请主动调用工具来完成研究任务。回答应该准确、简洁、有洞察力。""",
    tools=[search_papers, summarize_paper, extract_key_concepts],
    verbose=True
)


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Nano-Agent 示例: 研究助理")
    print("=" * 60)

    user_input = "帮我研究一下 TinyML 和边缘计算的最新进展"
    print(f"\n👤 用户: {user_input}\n")

    response = researcher.run(user_input)

    print("\n" + "=" * 60)
    print("✅ 最终回复:")
    print("=" * 60)
    print(response)
