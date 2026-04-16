#!/usr/bin/env python3
"""
Tests for Agent Pipeline Builder
"""

import sys
sys.path.insert(0, '.')

from pipeline import Pipeline, Tool, ToolRegistry, register_builtin_tools


def test_tool_registration():
    """测试工具注册"""
    register_builtin_tools()
    
    tools = ToolRegistry.list()
    assert 'text.clean' in tools
    assert 'text.tokenize' in tools
    assert 'agent.classify' in tools
    print("✓ Tool registration test passed")


def test_basic_pipeline():
    """测试基础 pipeline"""
    register_builtin_tools()
    
    pipeline = Pipeline(name="test")
    from pipeline import PipelineStep
    
    # 添加步骤
    step1 = PipelineStep('text.clean', {'lowercase': True})
    step2 = PipelineStep('text.stats', {})
    
    pipeline.add_step(step1)
    pipeline.add_step(step2)
    
    # 运行
    result = pipeline.run("Hello World")
    
    assert result.metadata['success'] == True
    assert 'length' in result.data
    print("✓ Basic pipeline test passed")


def test_text_clean():
    """测试文本清理"""
    register_builtin_tools()
    
    tool = ToolRegistry.get('text.clean')
    
    # 测试小写
    result = tool.process("HELLO World", {'lowercase': True})
    assert result == "hello world"
    
    # 测试去特殊字符
    result = tool.process("Hello, World! 123", {'remove_special_chars': True})
    assert result == "Hello World 123"
    
    print("✓ Text clean test passed")


def test_text_tokenize():
    """测试分词"""
    register_builtin_tools()
    
    tool = ToolRegistry.get('text.tokenize')
    
    # 单词分词
    result = tool.process("hello world test", {'method': 'word'})
    assert result == ['hello', 'world', 'test']
    
    # 字符分词
    result = tool.process("abc", {'method': 'char'})
    assert result == ['a', 'b', 'c']
    
    print("✓ Text tokenize test passed")


def test_agent_classify():
    """测试分类"""
    register_builtin_tools()
    
    tool = ToolRegistry.get('agent.classify')
    
    result = tool.process(
        "I found a bug that causes crash",
        {'rules': {
            'bug': ['bug', 'crash', 'error'],
            'feature': ['add', 'new', 'feature']
        }}
    )
    
    assert result['category'] == 'bug'
    assert result['scores']['bug'] > 0
    print("✓ Agent classify test passed")


def test_yaml_pipeline():
    """测试从 YAML 创建 pipeline"""
    register_builtin_tools()
    
    pipeline = Pipeline.from_yaml('examples/basic.yaml')
    
    assert pipeline.name == 'basic-text-processing'
    assert len(pipeline.steps) == 2
    
    print("✓ YAML pipeline test passed")


def test_chain_example():
    """测试链式处理示例"""
    register_builtin_tools()
    
    # 创建 pipeline
    pipeline = Pipeline(name="chain-test")
    from pipeline import PipelineStep
    
    pipeline.add_step(PipelineStep('text.clean', {'lowercase': True}))
    pipeline.add_step(PipelineStep('text.tokenize', {'method': 'word'}))
    # 使用 list.filter 过滤列表元素（min_length=4 会过滤掉 "the" 和 "fox"）
    pipeline.add_step(PipelineStep('list.filter', {'min_length': 4}))
    
    result = pipeline.run("The Quick Brown Fox")
    
    assert result.metadata['success'] == True
    # 应该过滤掉 "the" 和 "fox" (长度 < 4)，保留 "quick" 和 "brown"
    assert len(result.data) == 2
    assert 'quick' in result.data
    assert 'brown' in result.data
    print("✓ Chain example test passed")


if __name__ == '__main__':
    print("Running tests...\n")
    
    test_tool_registration()
    test_basic_pipeline()
    test_text_clean()
    test_text_tokenize()
    test_agent_classify()
    test_yaml_pipeline()
    test_chain_example()
    
    print("\n✅ All tests passed!")
