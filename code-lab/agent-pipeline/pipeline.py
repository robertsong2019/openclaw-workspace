#!/usr/bin/env python3
"""
Agent Pipeline Builder - 轻量级工具链引擎

类似 Unix pipe 的哲学：组合小型工具构建复杂工作流。
"""

import json
import yaml
import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ToolResult:
    """工具执行结果"""
    data: Any
    metadata: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        if 'timestamp' not in self.metadata:
            self.metadata['timestamp'] = datetime.now().isoformat()


class Tool:
    """工具基类"""
    name: str = "base.tool"
    description: str = "Base tool class"
    
    def process(self, input_data: Any, config: Dict) -> Any:
        """处理输入数据"""
        raise NotImplementedError
    
    def validate_config(self, config: Dict) -> bool:
        """验证配置"""
        return True


class ToolRegistry:
    """工具注册表"""
    _tools: Dict[str, Tool] = {}
    
    @classmethod
    def register(cls, tool: Tool):
        """注册工具"""
        cls._tools[tool.name] = tool
    
    @classmethod
    def get(cls, name: str) -> Optional[Tool]:
        """获取工具"""
        return cls._tools.get(name)
    
    @classmethod
    def list(cls) -> List[str]:
        """列出所有工具"""
        return list(cls._tools.keys())
    
    @classmethod
    def info(cls, name: str) -> Optional[Dict]:
        """获取工具信息"""
        tool = cls.get(name)
        if tool:
            return {
                "name": tool.name,
                "description": tool.description,
            }
        return None


class PipelineStep:
    """Pipeline 步骤"""
    def __init__(self, tool_name: str, config: Dict = None):
        self.tool_name = tool_name
        self.config = config or {}
        self.tool = ToolRegistry.get(tool_name)
        
        if not self.tool:
            raise ValueError(f"Tool not found: {tool_name}")
    
    def execute(self, input_data: Any, debug: bool = False) -> ToolResult:
        """执行步骤"""
        if debug:
            print(f"[DEBUG] Step: {self.tool_name}")
            print(f"[DEBUG] Config: {self.config}")
            print(f"[DEBUG] Input type: {type(input_data).__name__}")
        
        start_time = datetime.now()
        
        try:
            output = self.tool.process(input_data, self.config)
            elapsed = (datetime.now() - start_time).total_seconds()
            
            if debug:
                print(f"[DEBUG] Output type: {type(output).__name__}")
                print(f"[DEBUG] Elapsed: {elapsed:.3f}s")
            
            return ToolResult(
                data=output,
                metadata={
                    "tool": self.tool_name,
                    "elapsed_seconds": elapsed,
                    "success": True
                }
            )
        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            return ToolResult(
                data=None,
                metadata={
                    "tool": self.tool_name,
                    "elapsed_seconds": elapsed,
                    "success": False,
                    "error": str(e)
                }
            )


class Pipeline:
    """Pipeline 引擎"""
    
    def __init__(self, name: str = "unnamed", description: str = ""):
        self.name = name
        self.description = description
        self.steps: List[PipelineStep] = []
        self.debug = False
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'Pipeline':
        """从 YAML 文件创建 pipeline"""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        pipeline = cls(
            name=config.get('name', 'unnamed'),
            description=config.get('description', '')
        )
        
        for step_config in config.get('steps', []):
            step = PipelineStep(
                tool_name=step_config['tool'],
                config=step_config.get('config', {})
            )
            pipeline.add_step(step)
        
        return pipeline
    
    @classmethod
    def from_json(cls, json_path: str) -> 'Pipeline':
        """从 JSON 文件创建 pipeline"""
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        pipeline = cls(
            name=config.get('name', 'unnamed'),
            description=config.get('description', '')
        )
        
        for step_config in config.get('steps', []):
            step = PipelineStep(
                tool_name=step_config['tool'],
                config=step_config.get('config', {})
            )
            pipeline.add_step(step)
        
        return pipeline
    
    def add_step(self, step: PipelineStep):
        """添加步骤"""
        self.steps.append(step)
    
    def run(self, input_data: Any, debug: bool = False) -> ToolResult:
        """运行 pipeline"""
        self.debug = debug
        
        if debug:
            print(f"\n{'='*60}")
            print(f"Pipeline: {self.name}")
            print(f"Steps: {len(self.steps)}")
            print(f"{'='*60}\n")
        
        current_data = input_data
        results_metadata = []
        
        for i, step in enumerate(self.steps, 1):
            if debug:
                print(f"\n--- Step {i}/{len(self.steps)} ---")
            
            result = step.execute(current_data, debug=debug)
            results_metadata.append(result.metadata)
            
            if not result.metadata.get('success', False):
                # 步骤失败，停止执行
                return ToolResult(
                    data=None,
                    metadata={
                        "pipeline": self.name,
                        "steps_executed": i,
                        "total_steps": len(self.steps),
                        "success": False,
                        "error": result.metadata.get('error'),
                        "step_results": results_metadata
                    }
                )
            
            current_data = result.data
        
        if debug:
            print(f"\n{'='*60}")
            print("Pipeline completed successfully!")
            print(f"{'='*60}\n")
        
        return ToolResult(
            data=current_data,
            metadata={
                "pipeline": self.name,
                "steps_executed": len(self.steps),
                "total_steps": len(self.steps),
                "success": True,
                "step_results": results_metadata
            }
        )
    
    @staticmethod
    def register_tool(tool: Tool):
        """注册工具"""
        ToolRegistry.register(tool)


# ============================================================================
# 内置工具
# ============================================================================

class TextCleanTool(Tool):
    """文本清理工具"""
    name = "text.clean"
    description = "Clean text: lowercase, remove special chars, trim whitespace"
    
    def process(self, input_data: Any, config: Dict) -> str:
        text = str(input_data)
        
        # 小写
        if config.get('lowercase', False):
            text = text.lower()
        
        # 去除特殊字符
        if config.get('remove_special_chars', False):
            import re
            text = re.sub(r'[^a-zA-Z0-9\s\u4e00-\u9fff]', '', text)
        
        # 去除空白
        if config.get('trim_whitespace', True):
            text = ' '.join(text.split())
        
        return text


class TextTokenizeTool(Tool):
    """文本分词工具"""
    name = "text.tokenize"
    description = "Tokenize text into words or characters"
    
    def process(self, input_data: Any, config: Dict) -> List[str]:
        text = str(input_data)
        method = config.get('method', 'word')  # word, char, sentence
        
        if method == 'word':
            # 简单分词（按空格）
            return text.split()
        elif method == 'char':
            return list(text)
        elif method == 'sentence':
            import re
            return re.split(r'[.!?。！？]', text)
        else:
            raise ValueError(f"Unknown tokenize method: {method}")


class TextStatsTool(Tool):
    """文本统计工具"""
    name = "text.stats"
    description = "Calculate text statistics: length, word count, etc."
    
    def process(self, input_data: Any, config: Dict) -> Dict:
        text = str(input_data)
        
        stats = {
            'length': len(text),
            'char_count': len(text.replace(' ', '')),
            'word_count': len(text.split()),
            'line_count': len(text.split('\n')),
        }
        
        # 中文统计
        import re
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        stats['chinese_char_count'] = len(chinese_chars)
        
        output_format = config.get('output_format', 'dict')
        if output_format == 'json':
            return json.dumps(stats, ensure_ascii=False, indent=2)
        else:
            return stats


class DataFilterTool(Tool):
    """数据过滤工具"""
    name = "data.filter"
    description = "Filter data based on conditions"
    
    def process(self, input_data: Any, config: Dict) -> Any:
        # 移除空值
        if config.get('remove_empty', False):
            if isinstance(input_data, (list, tuple)):
                return [item for item in input_data if item]
            elif isinstance(input_data, dict):
                return {k: v for k, v in input_data.items() if v}
        
        # 最小长度
        min_length = config.get('min_length')
        if min_length and isinstance(input_data, (list, tuple, str)):
            if len(input_data) < min_length:
                return [] if isinstance(input_data, (list, tuple)) else ''
        
        return input_data


class DataTransformTool(Tool):
    """数据转换工具"""
    name = "data.transform"
    description = "Transform data format"
    
    def process(self, input_data: Any, config: Dict) -> Any:
        target_format = config.get('format', 'auto')
        
        if target_format == 'json':
            if isinstance(input_data, (dict, list)):
                return json.dumps(input_data, ensure_ascii=False, indent=2)
            else:
                return json.dumps(str(input_data), ensure_ascii=False)
        
        elif target_format == 'list':
            if isinstance(input_data, str):
                return input_data.split('\n')
            elif isinstance(input_data, dict):
                return list(input_data.items())
            else:
                return list(input_data)
        
        elif target_format == 'string':
            if isinstance(input_data, (dict, list)):
                return json.dumps(input_data, ensure_ascii=False, indent=2)
            else:
                return str(input_data)
        
        return input_data


class AgentExtractTool(Tool):
    """信息提取工具（基于正则）"""
    name = "agent.extract"
    description = "Extract information using regex patterns"
    
    def process(self, input_data: Any, config: Dict) -> Dict:
        import re
        text = str(input_data)
        patterns = config.get('patterns', [])
        
        results = {}
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                # 尝试获取命名组
                match = re.search(pattern, text)
                if match and match.groupdict():
                    results.update(match.groupdict())
                else:
                    results[f'match_{len(results)}'] = matches
        
        return results


class AgentClassifyTool(Tool):
    """文本分类工具（基于规则）"""
    name = "agent.classify"
    description = "Classify text using keyword rules"
    
    def process(self, input_data: Any, config: Dict) -> Dict:
        text = str(input_data).lower()
        rules = config.get('rules', {})
        
        scores = {}
        for category, keywords in rules.items():
            score = sum(1 for kw in keywords if kw.lower() in text)
            scores[category] = score
        
        # 找出最高分
        if scores:
            best_category = max(scores, key=scores.get)
            confidence = scores[best_category] / sum(scores.values()) if sum(scores.values()) > 0 else 0
        else:
            best_category = None
            confidence = 0
        
        return {
            'category': best_category,
            'confidence': confidence,
            'scores': scores
        }


class ListFilterTool(Tool):
    """列表元素过滤工具"""
    name = "list.filter"
    description = "Filter list elements by length or value"

    def process(self, input_data: Any, config: Dict) -> List:
        if not isinstance(input_data, list):
            return input_data

        result = input_data

        # 最小长度过滤
        min_length = config.get('min_length')
        if min_length is not None:
            result = [item for item in result if len(str(item)) >= min_length]

        # 最大长度过滤
        max_length = config.get('max_length')
        if max_length is not None:
            result = [item for item in result if len(str(item)) <= max_length]

        # 移除空值
        if config.get('remove_empty', False):
            result = [item for item in result if item]

        # 去重
        if config.get('unique', False):
            result = list(dict.fromkeys(result))  # 保持顺序

        return result


class ListMapTool(Tool):
    """列表元素映射工具"""
    name = "list.map"
    description = "Transform each item in a list"

    def process(self, input_data: Any, config: Dict) -> List:
        if not isinstance(input_data, list):
            return input_data

        operation = config.get('operation', 'identity')

        if operation == 'uppercase':
            return [str(item).upper() for item in input_data]
        elif operation == 'lowercase':
            return [str(item).lower() for item in input_data]
        elif operation == 'strip':
            return [str(item).strip() for item in input_data]
        elif operation == 'int':
            return [int(item) for item in input_data if str(item).strip().lstrip('-').isdigit()]
        elif operation == 'prefix':
            prefix = config.get('prefix', '')
            return [f"{prefix}{item}" for item in input_data]
        elif operation == 'suffix':
            suffix = config.get('suffix', '')
            return [f"{item}{suffix}" for item in input_data]
        else:
            return input_data


class ListJoinTool(Tool):
    """列表连接工具"""
    name = "list.join"
    description = "Join list items into a string"

    def process(self, input_data: Any, config: Dict) -> str:
        if not isinstance(input_data, list):
            return str(input_data)

        separator = config.get('separator', ' ')
        return separator.join(str(item) for item in input_data)


class AgentJSONExtractTool(Tool):
    """从 LLM 输出中提取 JSON"""
    name = "agent.json_extract"
    description = "Extract JSON from LLM responses"

    def process(self, input_data: Any, config: Dict) -> Any:
        text = str(input_data)

        # 尝试提取 ```json 代码块
        import re
        json_block = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
        if json_block:
            try:
                return json.loads(json_block.group(1))
            except json.JSONDecodeError:
                pass

        # 尝试找到 JSON 对象或数组
        json_patterns = [
            r'\{[\s\S]*\}',  # JSON 对象
            r'\[[\s\S]*\]',  # JSON 数组
        ]

        for pattern in json_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue

        # 尝试解析整个输入
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw": text, "error": "No valid JSON found"}


class AgentPromptTemplateTool(Tool):
    """简单的 Prompt 模板工具"""
    name = "agent.prompt_template"
    description = "Fill prompt templates with variables"

    def process(self, input_data: Any, config: Dict) -> str:
        template = config.get('template', str(input_data))
        variables = config.get('variables', {})

        # 支持两种变量格式: {var} 和 {{var}}
        result = template
        for key, value in variables.items():
            result = result.replace(f'{{{key}}}', str(value))
            result = result.replace(f'{{{{{key}}}}}', str(value))

        # 如果 input_data 是字典，也用它来填充
        if isinstance(input_data, dict):
            for key, value in input_data.items():
                result = result.replace(f'{{{key}}}', str(value))
                result = result.replace(f'{{{{{key}}}}}', str(value))

        return result


class ListTakeTool(Tool):
    """取列表前 N 个元素"""
    name = "list.take"
    description = "Take first N items from a list"

    def process(self, input_data: Any, config: Dict) -> List:
        if not isinstance(input_data, list):
            return input_data

        n = config.get('n', 10)
        return input_data[:n]


class ListSortTool(Tool):
    """排序列表"""
    name = "list.sort"
    description = "Sort a list"

    def process(self, input_data: Any, config: Dict) -> List:
        if not isinstance(input_data, list):
            return input_data

        reverse = config.get('reverse', False)
        key = config.get('key', None)

        try:
            if key:
                # 按指定键排序（如果元素是字典）
                return sorted(input_data, key=lambda x: x.get(key, ''), reverse=reverse)
            else:
                return sorted(input_data, reverse=reverse)
        except TypeError:
            # 混合类型，转为字符串排序
            return sorted(input_data, key=str, reverse=reverse)


# ============================================================================
# 网络工具
# ============================================================================

class HttpGetTool(Tool):
    """HTTP GET 请求工具（使用标准库 urllib）"""
    name = "http.get"
    description = "Fetch content from HTTP URL"

    def process(self, input_data: Any, config: Dict) -> Dict:
        from urllib.request import urlopen, Request
        from urllib.error import URLError, HTTPError
        import json as json_lib

        # URL 可以从输入或配置中获取
        url = config.get('url') or str(input_data).strip()
        if not url:
            return {"error": "No URL provided"}

        # 请求头
        headers = config.get('headers', {})
        # 默认 User-Agent
        if 'User-Agent' not in headers:
            headers['User-Agent'] = 'Agent-Pipeline/1.0'

        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=config.get('timeout', 10)) as response:
                content = response.read().decode('utf-8')
                content_type = response.getheader('Content-Type', '')

                result = {
                    'status': response.status,
                    'url': url,
                    'content_type': content_type,
                }

                # 尝试解析 JSON
                if 'application/json' in content_type:
                    try:
                        result['data'] = json_lib.loads(content)
                    except json_lib.JSONDecodeError:
                        result['raw'] = content
                else:
                    result['raw'] = content

                return result

        except HTTPError as e:
            return {
                'error': f'HTTP Error {e.code}: {e.reason}',
                'url': url,
                'status': e.code
            }
        except URLError as e:
            return {
                'error': f'URL Error: {e.reason}',
                'url': url
            }
        except Exception as e:
            return {
                'error': f'Request failed: {str(e)}',
                'url': url
            }


# ============================================================================
# 文本工具（扩展）
# ============================================================================

class TextExtractTool(Tool):
    """文本提取工具（多模式正则）"""
    name = "text.extract"
    description = "Extract text using regex patterns"

    def process(self, input_data: Any, config: Dict) -> List[Dict]:
        import re
        text = str(input_data)
        patterns = config.get('patterns', [])
        extract_all = config.get('all', False)

        results = []
        for i, pattern in enumerate(patterns):
            name = pattern.get('name', f'pattern_{i}')
            regex = pattern.get('regex', '')
            if not regex:
                continue

            matches = re.finditer(regex, text)
            if extract_all:
                # 提取所有匹配
                for match in matches:
                    if match.groupdict():
                        results.append({
                            'pattern': name,
                            'match': match.groupdict()
                        })
                    else:
                        results.append({
                            'pattern': name,
                            'match': match.group()
                        })
            else:
                # 只提取第一个
                match = re.search(regex, text)
                if match:
                    if match.groupdict():
                        results.append({
                            'pattern': name,
                            'match': match.groupdict()
                        })
                    else:
                        results.append({
                            'pattern': name,
                            'match': match.group()
                        })

        return results


class TextJsonTool(Tool):
    """JSON 解析与转换工具"""
    name = "text.json"
    description = "Parse or format JSON"

    def process(self, input_data: Any, config: Dict) -> Any:
        import json as json_lib

        action = config.get('action', 'parse')  # parse, format, stringify

        if action == 'parse':
            # 解析 JSON
            text = str(input_data).strip()
            try:
                return json_lib.loads(text)
            except json_lib.JSONDecodeError as e:
                return {"error": f"Invalid JSON: {str(e)}"}

        elif action == 'format':
            # 格式化 JSON（假设输入是 Python 对象）
            indent = config.get('indent', 2)
            try:
                return json_lib.dumps(input_data, ensure_ascii=False, indent=indent)
            except (TypeError, ValueError) as e:
                return {"error": f"Cannot format as JSON: {str(e)}"}

        elif action == 'stringify':
            # 转为 JSON 字符串
            compact = config.get('compact', False)
            try:
                if compact:
                    return json_lib.dumps(input_data, ensure_ascii=False, separators=(',', ':'))
                else:
                    return json_lib.dumps(input_data, ensure_ascii=False)
            except (TypeError, ValueError) as e:
                return {"error": f"Cannot stringify: {str(e)}"}

        return input_data


class TextSplitTool(Tool):
    """智能分词工具"""
    name = "text.split"
    description = "Split text by separator, regex, or length"

    def process(self, input_data: Any, config: Dict) -> List[str]:
        import re
        text = str(input_data)
        mode = config.get('mode', 'separator')  # separator, regex, length, lines

        if mode == 'separator':
            sep = config.get('separator', '\n')
            maxsplit = config.get('maxsplit', -1)
            return text.split(sep, maxsplit)

        elif mode == 'regex':
            pattern = config.get('pattern', r'\s+')
            return re.split(pattern, text)

        elif mode == 'length':
            chunk_size = config.get('chunk_size', 100)
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            return chunks

        elif mode == 'lines':
            return text.split('\n')

        return [text]


# ============================================================================
# 数据工具（扩展）
# ============================================================================

class DataFormatTool(Tool):
    """格式化输出工具"""
    name = "data.format"
    description = "Format data as table, JSON, or YAML"

    def process(self, input_data: Any, config: Dict) -> str:
        format_type = config.get('format', 'json')  # json, yaml, table, markdown

        if format_type == 'json':
            indent = config.get('indent', 2)
            import json as json_lib
            return json_lib.dumps(input_data, ensure_ascii=False, indent=indent)

        elif format_type == 'yaml':
            return yaml.dump(input_data, allow_unicode=True, default_flow_style=False)

        elif format_type == 'table':
            # 简单表格格式
            if not isinstance(input_data, list):
                return str(input_data)

            if not input_data:
                return ""

            # 假设是字典列表
            if isinstance(input_data[0], dict):
                headers = list(input_data[0].keys())
                rows = [[str(item.get(h, '')) for h in headers] for item in input_data]

                # 计算列宽
                col_widths = [max(len(str(h)), max(len(r[i]) for r in rows)) for i, h in enumerate(headers)]

                # 构建表格
                lines = []
                # 标题行
                header_line = ' | '.join(h.ljust(w) for h, w in zip(headers, col_widths))
                lines.append(header_line)
                lines.append('-+-'.join('-' * w for w in col_widths))
                # 数据行
                for row in rows:
                    lines.append(' | '.join(cell.ljust(w) for cell, w in zip(row, col_widths)))

                return '\n'.join(lines)
            else:
                return '\n'.join(str(item) for item in input_data)

        elif format_type == 'markdown':
            # Markdown 表格
            if not isinstance(input_data, list) or not input_data:
                return str(input_data)

            if isinstance(input_data[0], dict):
                headers = list(input_data[0].keys())
                lines = [
                    '| ' + ' | '.join(headers) + ' |',
                    '| ' + ' | '.join('---' for _ in headers) + ' |'
                ]
                for item in input_data:
                    lines.append('| ' + ' | '.join(str(item.get(h, '')) for h in headers) + ' |')
                return '\n'.join(lines)
            else:
                return '\n'.join(f'- {item}' for item in input_data)

        return str(input_data)


class DataGroupTool(Tool):
    """数据分组工具"""
    name = "data.group"
    description = "Group data by a field or key"

    def process(self, input_data: Any, config: Dict) -> Dict:
        if not isinstance(input_data, list):
            return {"error": "Input must be a list"}

        key = config.get('key')
        if not key:
            return {"error": "Group key not specified"}

        groups = {}
        for item in input_data:
            if isinstance(item, dict):
                group_value = item.get(key)
            else:
                group_value = item

            if group_value not in groups:
                groups[group_value] = []
            groups[group_value].append(item)

        return groups


class DataUniqueTool(Tool):
    """去重工具"""
    name = "data.unique"
    description = "Remove duplicates from data"

    def process(self, input_data: Any, config: Dict) -> Any:
        by_key = config.get('by_key', None)

        if by_key:
            # 按指定字段去重（字典列表）
            if isinstance(input_data, list):
                seen = set()
                result = []
                for item in input_data:
                    if isinstance(item, dict):
                        key_value = item.get(by_key)
                        if key_value not in seen:
                            seen.add(key_value)
                            result.append(item)
                    else:
                        if item not in seen:
                            seen.add(item)
                            result.append(item)
                return result
        else:
            # 简单去重
            if isinstance(input_data, list):
                return list(dict.fromkeys(input_data))  # 保持顺序
            elif isinstance(input_data, str):
                lines = input_data.split('\n')
                return '\n'.join(dict.fromkeys(lines))

        return input_data


# ============================================================================
# 文件工具
# ============================================================================

class FileReadTool(Tool):
    """文件读取工具"""
    name = "file.read"
    description = "Read file content"

    def process(self, input_data: Any, config: Dict) -> str:
        file_path = config.get('path') or str(input_data).strip()
        encoding = config.get('encoding', 'utf-8')

        if not file_path:
            return {"error": "File path not provided"}

        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except FileNotFoundError:
            return {"error": f"File not found: {file_path}"}
        except IOError as e:
            return {"error": f"Failed to read file: {str(e)}"}


class FileWriteTool(Tool):
    """文件写入工具"""
    name = "file.write"
    description = "Write content to file"

    def process(self, input_data: Any, config: Dict) -> Dict:
        file_path = config.get('path') or str(input_data.get('path', '')).strip()
        content = config.get('content') or input_data.get('content', str(input_data))
        encoding = config.get('encoding', 'utf-8')
        mode = config.get('mode', 'w')  # w = write, a = append

        if not file_path:
            return {"error": "File path not provided"}

        try:
            with open(file_path, mode, encoding=encoding) as f:
                f.write(content)
            return {"success": True, "path": file_path, "mode": mode}
        except IOError as e:
            return {"error": f"Failed to write file: {str(e)}"}


class FileLinesTool(Tool):
    """按行读取文件工具"""
    name = "file.lines"
    description = "Read file line by line"

    def process(self, input_data: Any, config: Dict) -> List[str]:
        file_path = config.get('path') or str(input_data).strip()
        encoding = config.get('encoding', 'utf-8')
        skip_empty = config.get('skip_empty', False)
        strip_whitespace = config.get('strip', True)

        if not file_path:
            return []

        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()

            if strip_whitespace:
                lines = [line.rstrip('\n\r') for line in lines]

            if skip_empty:
                lines = [line for line in lines if line]

            return lines

        except FileNotFoundError:
            return [{"error": f"File not found: {file_path}"}]
        except IOError as e:
            return [{"error": f"Failed to read file: {str(e)}"}]


# ============================================================================
# 系统工具
# ============================================================================

class EnvGetTool(Tool):
    """环境变量获取工具"""
    name = "env.get"
    description = "Get environment variable"

    def process(self, input_data: Any, config: Dict) -> str:
        import os

        # 变量名可以从输入或配置获取
        var_name = config.get('name') or str(input_data).strip()
        default = config.get('default', '')

        if not var_name:
            return {"error": "Variable name not provided"}

        return os.environ.get(var_name, default)


# ============================================================================
# 注册内置工具
# ============================================================================

def register_builtin_tools():
    """注册所有内置工具"""
    # 文本处理
    Pipeline.register_tool(TextCleanTool())
    Pipeline.register_tool(TextTokenizeTool())
    Pipeline.register_tool(TextStatsTool())
    Pipeline.register_tool(TextExtractTool())  # 新增
    Pipeline.register_tool(TextJsonTool())  # 新增
    Pipeline.register_tool(TextSplitTool())  # 新增

    # 数据处理
    Pipeline.register_tool(DataFilterTool())
    Pipeline.register_tool(DataTransformTool())
    Pipeline.register_tool(DataFormatTool())  # 新增
    Pipeline.register_tool(DataGroupTool())  # 新增
    Pipeline.register_tool(DataUniqueTool())  # 新增

    # 列表处理
    Pipeline.register_tool(ListFilterTool())
    Pipeline.register_tool(ListMapTool())
    Pipeline.register_tool(ListJoinTool())
    Pipeline.register_tool(ListTakeTool())
    Pipeline.register_tool(ListSortTool())

    # AI Agent 工具
    Pipeline.register_tool(AgentExtractTool())
    Pipeline.register_tool(AgentClassifyTool())
    Pipeline.register_tool(AgentJSONExtractTool())
    Pipeline.register_tool(AgentPromptTemplateTool())

    # 网络工具
    Pipeline.register_tool(HttpGetTool())  # 新增

    # 文件工具
    Pipeline.register_tool(FileReadTool())  # 新增
    Pipeline.register_tool(FileWriteTool())  # 新增
    Pipeline.register_tool(FileLinesTool())  # 新增

    # 系统工具
    Pipeline.register_tool(EnvGetTool())  # 新增


# ============================================================================
# CLI
# ============================================================================

def main():
    register_builtin_tools()
    
    parser = argparse.ArgumentParser(
        description="Agent Pipeline Builder - 组合工具构建工作流",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行 pipeline
  python pipeline.py run examples/basic.yaml
  
  # 使用调试模式
  python pipeline.py run examples/basic.yaml --debug
  
  # 列出所有工具
  python pipeline.py tools
  
  # 显示工具详情
  python pipeline.py info text.clean
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # run 命令
    run_parser = subparsers.add_parser('run', help='运行 pipeline')
    run_parser.add_argument('config', help='Pipeline 配置文件 (YAML/JSON)')
    run_parser.add_argument('--input', '-i', help='输入数据（默认从 stdin 读取）')
    run_parser.add_argument('--debug', '-d', action='store_true', help='调试模式')
    run_parser.add_argument('--output', '-o', help='输出文件（默认 stdout）')
    
    # tools 命令
    tools_parser = subparsers.add_parser('tools', help='列出所有工具')
    
    # info 命令
    info_parser = subparsers.add_parser('info', help='显示工具详情')
    info_parser.add_argument('tool_name', help='工具名称')
    
    # repl 命令
    repl_parser = subparsers.add_parser('repl', help='交互式构建 pipeline')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        # 运行 pipeline
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"Error: Config file not found: {args.config}", file=sys.stderr)
            sys.exit(1)
        
        # 创建 pipeline
        if config_path.suffix in ['.yaml', '.yml']:
            pipeline = Pipeline.from_yaml(str(config_path))
        else:
            pipeline = Pipeline.from_json(str(config_path))
        
        # 获取输入
        if args.input:
            input_data = args.input
        else:
            print("Enter input data (Ctrl+D to finish):", file=sys.stderr)
            input_data = sys.stdin.read().strip()
        
        # 运行
        result = pipeline.run(input_data, debug=args.debug)
        
        # 输出
        output_data = result.data
        if isinstance(output_data, (dict, list)):
            output_str = json.dumps(output_data, ensure_ascii=False, indent=2)
        else:
            output_str = str(output_data)
        
        if args.output:
            Path(args.output).write_text(output_str, encoding='utf-8')
            print(f"Output written to: {args.output}", file=sys.stderr)
        else:
            print(output_str)
        
        # 返回状态码
        sys.exit(0 if result.metadata.get('success', False) else 1)
    
    elif args.command == 'tools':
        # 列出工具
        print("Available tools:")
        print("-" * 60)
        for tool_name in sorted(ToolRegistry.list()):
            info = ToolRegistry.info(tool_name)
            print(f"{tool_name:25} - {info['description']}")
    
    elif args.command == 'info':
        # 显示工具详情
        info = ToolRegistry.info(args.tool_name)
        if info:
            print(f"Tool: {info['name']}")
            print(f"Description: {info['description']}")
        else:
            print(f"Tool not found: {args.tool_name}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'repl':
        # 交互式模式
        repl_mode()
    
    else:
        parser.print_help()


def repl_mode():
    """交互式 Pipeline 构建模式"""
    print("\n" + "=" * 60)
    print("  Agent Pipeline REPL - 交互式 Pipeline 构建")
    print("=" * 60)
    print("\n命令:")
    print("  add <tool> [config_json]  - 添加步骤")
    print("  run [input]               - 运行 pipeline")
    print("  steps                     - 显示当前步骤")
    print("  clear                     - 清空 pipeline")
    print("  tools                     - 列出可用工具")
    print("  help                      - 显示帮助")
    print("  quit / exit               - 退出")
    print("\n示例:")
    print("  add text.clean {\"lowercase\": true}")
    print("  add text.tokenize {\"method\": \"word\"}")
    print("  run \"Hello World\"")
    print("")

    pipeline = Pipeline(name="repl-pipeline")
    current_input = None

    while True:
        try:
            line = input("pipeline> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not line:
            continue

        parts = line.split(maxsplit=2)
        cmd = parts[0].lower()

        if cmd in ('quit', 'exit', 'q'):
            print("Goodbye!")
            break

        elif cmd == 'help':
            print("\n命令:")
            print("  add <tool> [config_json]  - 添加步骤")
            print("  run [input]               - 运行 pipeline")
            print("  steps                     - 显示当前步骤")
            print("  clear                     - 清空 pipeline")
            print("  tools                     - 列出可用工具")
            print("  help                      - 显示帮助")
            print("  quit / exit               - 退出")

        elif cmd == 'tools':
            print("\n可用工具:")
            for tool_name in sorted(ToolRegistry.list()):
                info = ToolRegistry.info(tool_name)
                print(f"  {tool_name:25} - {info['description']}")
            print()

        elif cmd == 'steps':
            if not pipeline.steps:
                print("Pipeline 为空，使用 'add <tool>' 添加步骤")
            else:
                print(f"\n当前 Pipeline ({len(pipeline.steps)} 步):")
                for i, step in enumerate(pipeline.steps, 1):
                    print(f"  {i}. {step.tool_name} {json.dumps(step.config, ensure_ascii=False)}")
                print()

        elif cmd == 'clear':
            pipeline = Pipeline(name="repl-pipeline")
            print("Pipeline 已清空")

        elif cmd == 'add':
            if len(parts) < 2:
                print("用法: add <tool> [config_json]")
                continue

            tool_name = parts[1]
            config = {}

            if len(parts) > 2:
                try:
                    config = json.loads(parts[2])
                except json.JSONDecodeError as e:
                    print(f"配置 JSON 解析失败: {e}")
                    continue

            try:
                step = PipelineStep(tool_name, config)
                pipeline.add_step(step)
                print(f"✓ 添加步骤: {tool_name}")
            except ValueError as e:
                print(f"错误: {e}")

        elif cmd == 'run':
            if not pipeline.steps:
                print("Pipeline 为空，先使用 'add' 添加步骤")
                continue

            input_data = parts[1] if len(parts) > 1 else current_input
            if input_data is None:
                print("请提供输入: run \"your input\"")
                continue

            print(f"\n运行 Pipeline...")
            result = pipeline.run(input_data, debug=False)

            if result.metadata.get('success'):
                output = result.data
                if isinstance(output, (dict, list)):
                    print(json.dumps(output, ensure_ascii=False, indent=2))
                else:
                    print(output)
            else:
                print(f"Pipeline 失败: {result.metadata.get('error')}")

        else:
            print(f"未知命令: {cmd}。输入 'help' 查看帮助。")


if __name__ == '__main__':
    main()
