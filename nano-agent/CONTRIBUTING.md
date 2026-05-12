# Contributing to Nano-Agent

感谢你关注 Nano-Agent！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题
- 使用清晰的标题描述问题
- 包含复现步骤和 Python 版本
- 如果可能，提供修复建议

### 提交代码
1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/your-feature`)
3. 提交修改 (`git commit -m 'Add your feature'`)
4. 推送并开启 Pull Request

## 开发环境

```bash
# 克隆后进入项目
cd nano-agent

# 安装依赖（核心零依赖，以下为开发工具）
pip install pytest black mypy

# 运行测试
python -m pytest tests/ -v

# 格式化代码
black src/ tests/
```

## 项目结构

```
nano-agent/
├── src/nano_agent/    # 核心代码
│   ├── agent.py       # Agent 类 — 推理循环
│   ├── tools.py       # @tool 装饰器和 Tool 类
│   ├── memory.py      # Memory 记忆管理
│   └── llm.py         # LLM 后端接口
├── examples/          # 示例程序
├── tests/             # 测试
├── TUTORIAL.md        # 教程
├── API.md             # API 参考
└── ARCHITECTURE.md    # 架构设计
```

## 代码规范

- **保持极简** — 核心代码 <500 行是硬约束，新功能优先考虑放在扩展中
- **零依赖** — 核心模块不引入第三方库；可选功能在 requirements.txt 中标注
- **类型注解** — 所有公开函数使用 type hints
- **docstring** — 公开 API 使用 Google 风格 docstring
- **测试** — 新功能需附带测试（`tests/` 目录）

## 设计原则

1. **极简主义**: 核心 <500 行，每多一行都需要理由
2. **零依赖**: 纯标准库即可运行
3. **可组合**: 每个组件独立可用，通过接口组合
4. **可读性**: 30 分钟内可理解全部核心代码

## 添加新功能

### 添加工具
```python
# 在你的项目中定义，不需要改框架
from nano_agent import Agent, tool

@tool
def my_tool(param: str) -> str:
    """工具描述（LLM 会看到）"""
    return result
```

### 添加 LLM 后端
继承 `LLMBackend` 并实现 `complete()` 方法：

```python
from nano_agent.llm import LLMBackend

class MyBackend(LLMBackend):
    def complete(self, messages, tools=None):
        # 调用你的 LLM API
        return response
```

### 扩展 Memory
继承 `Memory` 类或实现相同接口：

```python
from nano_agent.memory import Memory

class PersistentMemory(Memory):
    def __init__(self, path):
        super().__init__()
        self.path = path
        # 加载持久化数据...
```

## 许可证

通过贡献代码，你同意你的贡献将在 MIT 许可证下发布。
