#!/usr/bin/env python3
"""
Tests for Agent Pipeline Builder
"""

import sys
import os
import json
import tempfile

sys.path.insert(0, '.')

from pipeline import (Pipeline, PipelineStep, Tool, ToolResult, ToolRegistry,
                      register_builtin_tools)


# ============================================================================
# Helper: flaky tool for retry testing
# ============================================================================

class FlakyTool(Tool):
    """A tool that fails N times before succeeding"""
    name = "test.flaky"
    description = "Fails N times then succeeds"

    def __init__(self, fail_count=2):
        self.fail_count = fail_count
        self.call_count = 0

    def process(self, input_data, config):
        self.call_count += 1
        if self.call_count <= self.fail_count:
            raise RuntimeError(f"Flaky failure #{self.call_count}")
        return f"success after {self.call_count} attempts"


class FailTool(Tool):
    """Always fails"""
    name = "test.fail"
    description = "Always fails"

    def process(self, input_data, config):
        raise RuntimeError("Always fails")


class EchoTool(Tool):
    """Echoes input with optional prefix"""
    name = "test.echo"
    description = "Echo input"

    def process(self, input_data, config):
        prefix = config.get('prefix', '')
        return f"{prefix}{input_data}"


def register_test_tools():
    """Register test-only tools"""
    Pipeline.register_tool(FlakyTool())
    Pipeline.register_tool(FailTool())
    Pipeline.register_tool(EchoTool())


# ============================================================================
# Original tests (refactored to use assertions)
# ============================================================================

class TestToolRegistration:
    def test_builtin_tools(self):
        register_builtin_tools()
        tools = ToolRegistry.list()
        assert 'text.clean' in tools
        assert 'text.tokenize' in tools
        assert 'agent.classify' in tools
        assert 'text.stats' in tools
        assert 'data.filter' in tools
        assert 'data.transform' in tools
        assert 'list.filter' in tools
        assert 'list.map' in tools
        assert 'list.join' in tools

    def test_tool_info(self):
        register_builtin_tools()
        info = ToolRegistry.info('text.clean')
        assert info is not None
        assert info['name'] == 'text.clean'
        assert info['description']

    def test_unknown_tool_info(self):
        register_builtin_tools()
        assert ToolRegistry.info('nonexistent') is None


class TestBasicPipeline:
    def test_basic_pipeline(self):
        register_builtin_tools()
        pipeline = Pipeline(name="test")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True}))
        pipeline.add_step(PipelineStep('text.stats', {}))
        result = pipeline.run("Hello World")
        assert result.metadata['success'] is True
        assert 'length' in result.data

    def test_chain_example(self):
        register_builtin_tools()
        pipeline = Pipeline(name="chain-test")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True}))
        pipeline.add_step(PipelineStep('text.tokenize', {'method': 'word'}))
        pipeline.add_step(PipelineStep('list.filter', {'min_length': 4}))
        result = pipeline.run("The Quick Brown Fox")
        assert result.metadata['success'] is True
        assert len(result.data) == 2
        assert 'quick' in result.data
        assert 'brown' in result.data

    def test_empty_pipeline(self):
        register_builtin_tools()
        pipeline = Pipeline(name="empty")
        result = pipeline.run("hello")
        assert result.metadata['success'] is True
        assert result.data == "hello"

    def test_pipeline_metadata(self):
        register_builtin_tools()
        pipeline = Pipeline(name="meta-test", description="test desc")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True}))
        result = pipeline.run("HELLO")
        assert result.metadata['pipeline'] == 'meta-test'
        assert result.metadata['steps_executed'] == 1
        assert result.metadata['total_steps'] == 1

    def test_step_failure_stops_pipeline(self):
        register_builtin_tools()
        register_test_tools()
        pipeline = Pipeline(name="fail-test")
        pipeline.add_step(PipelineStep('test.fail', {}))
        pipeline.add_step(PipelineStep('text.clean', {}))
        result = pipeline.run("hello")
        assert result.metadata['success'] is False
        assert result.metadata['steps_executed'] == 1


class TestContinueOnError:
    def test_continue_on_error(self):
        register_builtin_tools()
        register_test_tools()
        pipeline = Pipeline(name="continue-test")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True}))
        pipeline.add_step(PipelineStep('test.fail', {}, continue_on_error=True))
        pipeline.add_step(PipelineStep('text.stats', {}))
        result = pipeline.run("Hello World")
        # Pipeline succeeds because failing step has continue_on_error
        assert result.metadata['success'] is True
        # Data should be from step 1 (cleaned text), not step 2 (failed)
        assert 'length' in result.data

    def test_continue_preserves_data(self):
        register_builtin_tools()
        register_test_tools()
        pipeline = Pipeline(name="preserve-test")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True}))
        pipeline.add_step(PipelineStep('test.fail', {}, continue_on_error=True))
        result = pipeline.run("HELLO WORLD")
        assert result.data == "hello world"


class TestRetry:
    def test_retry_succeeds_after_failures(self):
        register_builtin_tools()
        register_test_tools()
        flaky = ToolRegistry.get('test.flaky')
        flaky.call_count = 0  # reset
        pipeline = Pipeline(name="retry-test")
        pipeline.add_step(PipelineStep('test.flaky', {}, retry=3))
        result = pipeline.run("test")
        assert result.metadata['success'] is True
        assert result.metadata['step_results'][0]['attempts'] == 3  # 2 fails + 1 success

    def test_retry_exhausted(self):
        register_builtin_tools()
        register_test_tools()
        pipeline = Pipeline(name="retry-exhaust")
        pipeline.add_step(PipelineStep('test.fail', {}, retry=2))
        result = pipeline.run("test")
        assert result.metadata['success'] is False
        assert result.metadata['step_results'][0]['attempts'] == 3  # 1 + 2 retries


class TestPipelineValidate:
    def test_valid_pipeline(self):
        register_builtin_tools()
        pipeline = Pipeline(name="valid")
        pipeline.add_step(PipelineStep('text.clean', {}))
        v = pipeline.validate()
        assert v['valid'] is True
        assert v['step_count'] == 1

    def test_empty_pipeline_invalid(self):
        register_builtin_tools()
        pipeline = Pipeline(name="empty")
        v = pipeline.validate()
        assert v['valid'] is False
        assert "no steps" in v['issues'][0].lower()

    def test_duplicate_tool_warning(self):
        register_builtin_tools()
        pipeline = Pipeline(name="dupes")
        pipeline.add_step(PipelineStep('text.clean', {}))
        pipeline.add_step(PipelineStep('text.clean', {}))
        v = pipeline.validate()
        assert v['valid'] is True
        assert len(v['warnings']) >= 1


class TestPipelineSerialization:
    def test_to_dict(self):
        register_builtin_tools()
        pipeline = Pipeline(name="ser", description="test")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True}, retry=2))
        d = pipeline.to_dict()
        assert d['name'] == 'ser'
        assert d['description'] == 'test'
        assert len(d['steps']) == 1
        assert d['steps'][0]['tool'] == 'text.clean'
        assert d['steps'][0]['retry'] == 2

    def test_roundtrip_dict(self):
        register_builtin_tools()
        pipeline = Pipeline(name="roundtrip")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True}))
        pipeline.add_step(PipelineStep('text.tokenize', {'method': 'word'}))
        d = pipeline.to_dict()
        p2 = Pipeline.from_dict(d)
        assert p2.name == 'roundtrip'
        assert len(p2.steps) == 2
        result = p2.run("Hello World")
        assert result.metadata['success'] is True

    def test_to_json(self):
        register_builtin_tools()
        pipeline = Pipeline(name="json-test")
        pipeline.add_step(PipelineStep('text.clean', {}))
        j = pipeline.to_json()
        parsed = json.loads(j)
        assert parsed['name'] == 'json-test'

    def test_from_json_file(self):
        register_builtin_tools()
        pipeline = Pipeline(name="file-test")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True}))
        pipeline.add_step(PipelineStep('text.stats', {}))

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(pipeline.to_json())
            f.flush()
            path = f.name

        try:
            p2 = Pipeline.from_json(path)
            result = p2.run("HELLO")
            assert result.metadata['success'] is True
            assert result.data['length'] > 0
        finally:
            os.unlink(path)


# ============================================================================
# Tool-specific tests
# ============================================================================

class TestTextCleanTool:
    def test_lowercase(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.clean')
        assert tool.process("HELLO World", {'lowercase': True}) == "hello world"

    def test_remove_special(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.clean')
        assert tool.process("Hello, World! 123", {'remove_special_chars': True}) == "Hello World 123"

    def test_trim_whitespace(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.clean')
        assert tool.process("  hello   world  ", {'trim_whitespace': True}) == "hello world"

    def test_chinese_preserved(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.clean')
        result = tool.process("你好世界! Test", {'remove_special_chars': True})
        assert "你好世界" in result


class TestTextTokenizeTool:
    def test_word(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.tokenize')
        assert tool.process("hello world test", {'method': 'word'}) == ['hello', 'world', 'test']

    def test_char(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.tokenize')
        assert tool.process("abc", {'method': 'char'}) == ['a', 'b', 'c']

    def test_sentence(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.tokenize')
        result = tool.process("Hello. World! How are you?", {'method': 'sentence'})
        assert len(result) >= 2

    def test_invalid_method(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.tokenize')
        try:
            tool.process("test", {'method': 'invalid'})
            assert False, "Should have raised"
        except ValueError:
            pass


class TestTextStatsTool:
    def test_basic_stats(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.stats')
        result = tool.process("Hello World 你好", {})
        assert result['length'] > 0
        assert result['word_count'] >= 2
        assert result['chinese_char_count'] == 2

    def test_json_output(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.stats')
        result = tool.process("test", {'output_format': 'json'})
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert 'length' in parsed


class TestDataFilterTool:
    def test_remove_empty_list(self):
        register_builtin_tools()
        tool = ToolRegistry.get('data.filter')
        assert tool.process(["a", "", "b", None], {'remove_empty': True}) == ["a", "b"]

    def test_remove_empty_dict(self):
        register_builtin_tools()
        tool = ToolRegistry.get('data.filter')
        result = tool.process({"a": 1, "b": None, "c": ""}, {'remove_empty': True})
        assert "a" in result
        assert "b" not in result


class TestDataTransformTool:
    def test_to_json(self):
        register_builtin_tools()
        tool = ToolRegistry.get('data.transform')
        result = tool.process({"key": "val"}, {'format': 'json'})
        assert isinstance(result, str)
        assert "key" in result

    def test_to_list_string(self):
        register_builtin_tools()
        tool = ToolRegistry.get('data.transform')
        result = tool.process("a\nb\nc", {'format': 'list'})
        assert result == ["a", "b", "c"]


class TestListTools:
    def test_list_filter_min_length(self):
        register_builtin_tools()
        tool = ToolRegistry.get('list.filter')
        result = tool.process(["ab", "abcde", "a"], {'min_length': 3})
        assert result == ["abcde"]

    def test_list_filter_unique(self):
        register_builtin_tools()
        tool = ToolRegistry.get('list.filter')
        result = tool.process(["a", "b", "a", "c"], {'unique': True})
        assert result == ["a", "b", "c"]

    def test_list_map_uppercase(self):
        register_builtin_tools()
        tool = ToolRegistry.get('list.map')
        assert tool.process(["a", "b"], {'operation': 'uppercase'}) == ["A", "B"]

    def test_list_map_prefix(self):
        register_builtin_tools()
        tool = ToolRegistry.get('list.map')
        assert tool.process(["a", "b"], {'operation': 'prefix', 'prefix': '>'}) == [">a", ">b"]

    def test_list_join(self):
        register_builtin_tools()
        tool = ToolRegistry.get('list.join')
        assert tool.process(["a", "b", "c"], {'separator': ','}) == "a,b,c"

    def test_list_take(self):
        register_builtin_tools()
        tool = ToolRegistry.get('list.take')
        assert tool.process([1, 2, 3, 4, 5], {'n': 3}) == [1, 2, 3]

    def test_list_sort(self):
        register_builtin_tools()
        tool = ToolRegistry.get('list.sort')
        assert tool.process([3, 1, 2], {}) == [1, 2, 3]

    def test_list_sort_reverse(self):
        register_builtin_tools()
        tool = ToolRegistry.get('list.sort')
        assert tool.process([1, 2, 3], {'reverse': True}) == [3, 2, 1]


class TestAgentTools:
    def test_classify(self):
        register_builtin_tools()
        tool = ToolRegistry.get('agent.classify')
        result = tool.process("bug causes crash", {
            'rules': {'bug': ['bug', 'crash'], 'feature': ['add', 'new']}
        })
        assert result['category'] == 'bug'
        assert result['confidence'] > 0

    def test_json_extract_codeblock(self):
        register_builtin_tools()
        tool = ToolRegistry.get('agent.json_extract')
        result = tool.process('```json\n{"key": "val"}\n```', {})
        assert result == {"key": "val"}

    def test_json_extract_inline(self):
        register_builtin_tools()
        tool = ToolRegistry.get('agent.json_extract')
        result = tool.process('result: {"key": "val"}', {})
        assert result == {"key": "val"}

    def test_prompt_template(self):
        register_builtin_tools()
        tool = ToolRegistry.get('agent.prompt_template')
        result = tool.process("", {
            'template': 'Hello {name}!',
            'variables': {'name': 'World'}
        })
        assert result == "Hello World!"

    def test_extract(self):
        register_builtin_tools()
        tool = ToolRegistry.get('agent.extract')
        result = tool.process("email: test@example.com and test2@example.com", {
            'patterns': [r'[\w.]+@[\w.]+']
        })
        assert len(result) >= 1


class TestTextSplitTool:
    def test_split_separator(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.split')
        assert tool.process("a,b,c", {'mode': 'separator', 'separator': ','}) == ["a", "b", "c"]

    def test_split_length(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.split')
        result = tool.process("abcdef", {'mode': 'length', 'chunk_size': 2})
        assert result == ["ab", "cd", "ef"]


class TestTextJsonTool:
    def test_parse(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.json')
        result = tool.process('{"a": 1}', {'action': 'parse'})
        assert result == {"a": 1}

    def test_format(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.json')
        result = tool.process({"a": 1}, {'action': 'format'})
        assert isinstance(result, str)
        assert '"a"' in result

    def test_stringify_compact(self):
        register_builtin_tools()
        tool = ToolRegistry.get('text.json')
        result = tool.process({"a": 1}, {'action': 'stringify', 'compact': True})
        assert result == '{"a":1}'


class TestDataFormatTool:
    def test_markdown_table(self):
        register_builtin_tools()
        tool = ToolRegistry.get('data.format')
        result = tool.process(
            [{"name": "Alice", "age": "30"}],
            {'format': 'markdown'}
        )
        assert "| name |" in result
        assert "| Alice |" in result

    def test_yaml_format(self):
        register_builtin_tools()
        tool = ToolRegistry.get('data.format')
        result = tool.process({"key": "val"}, {'format': 'yaml'})
        assert "key: val" in result


class TestDataGroupTool:
    def test_group_by(self):
        register_builtin_tools()
        tool = ToolRegistry.get('data.group')
        result = tool.process(
            [{"type": "a", "v": 1}, {"type": "b", "v": 2}, {"type": "a", "v": 3}],
            {'key': 'type'}
        )
        assert len(result['a']) == 2
        assert len(result['b']) == 1


class TestDataUniqueTool:
    def test_unique_list(self):
        register_builtin_tools()
        tool = ToolRegistry.get('data.unique')
        assert tool.process([1, 2, 2, 3], {}) == [1, 2, 3]

    def test_unique_by_key(self):
        register_builtin_tools()
        tool = ToolRegistry.get('data.unique')
        result = tool.process(
            [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}, {"id": 1, "v": "c"}],
            {'by_key': 'id'}
        )
        assert len(result) == 2


class TestRunBatch:
    def test_batch_basic(self):
        register_builtin_tools()
        pipeline = Pipeline(name="batch")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True}))
        results = pipeline.run_batch(["HELLO", "WORLD", "TEST"])
        assert len(results) == 3
        assert all(r.metadata['success'] for r in results)
        assert results[0].data == "hello"
        assert results[1].data == "world"

    def test_batch_with_failure(self):
        register_builtin_tools()
        register_test_tools()
        pipeline = Pipeline(name="batch-fail")
        pipeline.add_step(PipelineStep('test.fail', {}))
        results = pipeline.run_batch(["a", "b"])
        assert all(not r.metadata['success'] for r in results)


class TestConditionalSteps:
    def test_condition_true(self):
        register_builtin_tools()
        pipeline = Pipeline(name="cond-true")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True},
                                       condition=lambda data: isinstance(data, str)))
        result = pipeline.run("HELLO")
        assert result.metadata['success'] is True
        assert result.data == "hello"

    def test_condition_false_skips(self):
        register_builtin_tools()
        pipeline = Pipeline(name="cond-false")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True},
                                       condition=lambda data: False))
        pipeline.add_step(PipelineStep('text.stats', {}))
        result = pipeline.run("HELLO")
        assert result.metadata['success'] is True
        assert result.metadata['step_results'][0].get('skipped') is True
        # stats should run on original "HELLO"
        assert result.data['length'] == 5

    def test_condition_type_check(self):
        register_builtin_tools()
        pipeline = Pipeline(name="type-check")
        pipeline.add_step(PipelineStep('text.clean', {'lowercase': True}))
        # Only tokenize if result is still a string
        pipeline.add_step(PipelineStep('text.tokenize', {'method': 'word'},
                                       condition=lambda data: isinstance(data, str)))
        result = pipeline.run("Hello World")
        assert result.metadata['success'] is True
        assert isinstance(result.data, list)


class TestInsertRemoveStep:
    def test_insert_step(self):
        register_builtin_tools()
        pipeline = Pipeline(name="insert")
        pipeline.add_step(PipelineStep('text.clean', {}))
        pipeline.add_step(PipelineStep('text.stats', {}))
        pipeline.insert_step(1, PipelineStep('text.tokenize', {}))
        assert len(pipeline.steps) == 3
        assert pipeline.steps[1].tool_name == 'text.tokenize'

    def test_remove_step(self):
        register_builtin_tools()
        pipeline = Pipeline(name="remove")
        pipeline.add_step(PipelineStep('text.clean', {}))
        pipeline.add_step(PipelineStep('text.tokenize', {}))
        removed = pipeline.remove_step(0)
        assert removed.tool_name == 'text.clean'
        assert len(pipeline.steps) == 1

    def test_remove_out_of_range(self):
        register_builtin_tools()
        pipeline = Pipeline(name="oob")
        try:
            pipeline.remove_step(0)
            assert False, "Should raise"
        except IndexError:
            pass


class TestPipelineMerge:
    def test_merge_two_pipelines(self):
        register_builtin_tools()
        p1 = Pipeline(name="clean")
        p1.add_step(PipelineStep('text.clean', {'lowercase': True}))
        p2 = Pipeline(name="stats")
        p2.add_step(PipelineStep('text.stats', {}))
        merged = p1.merge(p2)
        assert merged.step_count == 2
        assert 'clean' in merged.name and 'stats' in merged.name
        result = merged.run("HELLO WORLD")
        assert result.metadata['success'] is True
        assert result.data['length'] > 0

    def test_merge_with_separator(self):
        register_builtin_tools()
        p1 = Pipeline(name="a")
        p1.add_step(PipelineStep('text.clean', {'lowercase': True}))
        p2 = Pipeline(name="b")
        p2.add_step(PipelineStep('text.stats', {}))
        sep = PipelineStep('text.tokenize', {'method': 'word'})
        merged = p1.merge(p2, separator=sep)
        assert merged.step_count == 3
        assert merged.steps[1].tool_name == 'text.tokenize'

    def test_step_count(self):
        register_builtin_tools()
        pipeline = Pipeline(name="count")
        assert pipeline.step_count == 0
        pipeline.add_step(PipelineStep('text.clean', {}))
        assert pipeline.step_count == 1


# ============================================================================
# Run all tests
# ============================================================================

if __name__ == '__main__':
    import pytest
    sys.exit(pytest.main([__file__, '-v', '--tb=short']))
