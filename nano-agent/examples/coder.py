"""
代码生成代理示例
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nano_agent import Agent, tool


@tool
def write_file(filename: str, content: str) -> str:
    """写入文件

    Args:
        filename: 文件名
        content: 文件内容

    Returns:
        操作结果
    """
    # 在实际应用中，这里会真的写入文件
    return f"已创建文件: {filename} ({len(content)} 字符)"


@tool
def read_file(filename: str) -> str:
    """读取文件

    Args:
        filename: 文件名

    Returns:
        文件内容
    """
    # 模拟读取
    return f"# {filename}\n# 这是文件内容"


@tool
def validate_code(code: str, language: str = "python") -> str:
    """验证代码语法

    Args:
        code: 代码内容
        language: 编程语言

    Returns:
        验证结果
    """
    # 简单的语法检查
    if "def " in code or "class " in code:
        return "✅ 代码语法看起来正确"
    else:
        return "⚠️ 未检测到函数或类定义"


@tool
def generate_tests(function_name: str, code: str) -> str:
    """生成单元测试

    Args:
        function_name: 函数名
        code: 函数代码

    Returns:
        生成的测试代码
    """
    tests = f"""
def test_{function_name}():
    # TODO: 实现测试
    assert True
"""
    return tests.strip()


# 创建代理
coder = Agent(
    name="代码助手",
    instructions="""你是一个专业的编程助手，帮助用户：
1. 编写高质量的代码
2. 进行代码审查和优化
3. 生成单元测试
4. 提供编程建议

请主动调用工具来完成代码相关任务。代码应该清晰、可维护、符合最佳实践。""",
    tools=[write_file, read_file, validate_code, generate_tests],
    verbose=True
)


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Nano-Agent 示例: 代码助手")
    print("=" * 60)

    user_input = "帮我写一个 Python 函数来计算斐波那契数列，并生成测试"
    print(f"\n👤 用户: {user_input}\n")

    response = coder.run(user_input)

    print("\n" + "=" * 60)
    print("✅ 最终回复:")
    print("=" * 60)
    print(response)
