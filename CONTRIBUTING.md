# Contributing to OpenClaw Workspace

感谢你有兴趣为这个工作区做出贡献！🎉

## 📋 目录

- [行为准则](#行为准则)
- [我能如何贡献](#我能如何贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交信息规范](#提交信息规范)
- [文档贡献](#文档贡献)
- [问题报告](#问题报告)

## 行为准则

### 我们的承诺

- 尊重所有贡献者
- 接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

- 使用性化的语言或图像
- 捣乱、侮辱/贬损评论以及人身或政治攻击
- 公开或私下的骚扰
- 未经明确许可，发布他人的私人信息

## 我能如何贡献

### 🐛 报告 Bug

在 `memory/` 目录中创建一个文件记录 Bug：

```bash
# 创建 Bug 报告
cat > memory/bug-reports/YYYY-MM-DD-bug-title.md << EOF
# Bug 报告: [简短描述]

## 描述
清晰简洁地描述这个 bug。

## 复现步骤
1. 去 '...'
2. 点击 '...'
3. 滚动到 '...'
4. 看到错误

## 预期行为
描述你期望发生什么。

## 实际行为
描述实际发生了什么。

## 环境信息
- 项目: [例如 agent-task-cli]
- 版本: [例如 1.0.0]
- Node.js/Python 版本: 
- 操作系统: 

## 截图/日志
如果适用，添加截图或日志帮助解释问题。

## 附加信息
添加任何其他关于问题的信息。
EOF
```

### 💡 建议新功能

在 `memory/feature-requests/` 中创建文件：

```bash
cat > memory/feature-requests/YYYY-MM-DD-feature-title.md << EOF
# 功能请求: [简短描述]

## 这是否与某个问题相关？
清晰简洁地描述问题所在。

## 你希望什么解决方案？
清晰简洁地描述你想要发生什么。

## 描述你考虑过的替代方案
清晰简洁地描述你考虑过的任何替代方案或功能。

## 附加信息
添加关于功能请求的任何其他信息或截图。
EOF
```

### 📝 改进文档

文档改进包括：

1. **修复错误** - 错别字、错误信息、过期链接
2. **添加示例** - 更多使用场景、代码示例
3. **改进清晰度** - 重写不清楚的部分
4. **翻译** - 添加英文版本

参见 [DOCUMENTATION-GUIDE.md](DOCUMENTATION-GUIDE.md) 了解文档标准。

### 🔧 贡献代码

#### 准备工作

1. **Fork 并克隆**（如果在外部仓库）
   ```bash
   git clone https://github.com/your-username/workspace.git
   cd workspace
   ```

2. **安装依赖**
   ```bash
   # Node.js 项目
   cd projects/agent-task-cli
   npm install
   
   # Python 项目
   cd experiments/local-embedding-memory
   pip install -r requirements.txt
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/my-new-feature
   # 或
   git checkout -b fix/my-bug-fix
   ```

## 开发流程

### 1. 代码变更

```bash
# 进行代码修改
# ...

# 运行测试
npm test  # Node.js 项目
pytest    # Python 项目

# 运行 lint
npm run lint
```

### 2. 提交变更

```bash
git add .
git commit -m "feat: add new feature"
```

### 3. 推送并创建 PR

```bash
git push origin feature/my-new-feature
# 然后在 GitHub 上创建 Pull Request
```

## 代码规范

### JavaScript/TypeScript

```javascript
// 使用 const/let，不用 var
const myVar = 'value';

// 使用箭头函数
const myFunc = () => {
  return 'value';
};

// 使用模板字符串
const message = `Hello ${name}`;

// 使用 async/await
async function fetchData() {
  const response = await fetch(url);
  return response.json();
}
```

### Python

```python
# 遵循 PEP 8
def my_function(arg1, arg2):
    """函数文档字符串"""
    return arg1 + arg2

# 使用类型提示
def greet(name: str) -> str:
    return f"Hello {name}"

# 使用 f-strings
message = f"Hello {name}"
```

### 通用原则

- **DRY** (Don't Repeat Yourself) - 不要重复代码
- **KISS** (Keep It Simple, Stupid) - 保持简单
- **YAGNI** (You Aren't Gonna Need It) - 不要过度设计
- **单一职责原则** - 每个函数只做一件事
- **有意义的命名** - 变量和函数名要有意义

## 提交信息规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档变更
- `style`: 代码格式（不影响代码运行的变动）
- `refactor`: 重构（既不是新增功能，也不是修改 bug）
- `perf`: 性能优化
- `test`: 增加测试
- `chore`: 构建过程或辅助工具的变动
- `revert`: 回退

### 示例

```bash
# 新功能
git commit -m "feat: add support for custom patterns"

# Bug 修复
git commit -m "fix: resolve memory leak in search function"

# 文档
git commit -m "docs: update installation guide"

# 重构
git commit -m "refactor: simplify orchestrator logic"

# 破坏性变更
git commit -m "feat!: change API interface

BREAKING CHANGE: The function signature has changed from (a, b) to ({a, b})"
```

## 文档贡献

### 文档结构

```
项目/
├── README.md        # 项目概览
├── TUTORIAL.md      # 教程
├── API.md           # API 参考
├── CHANGELOG.md     # 变更日志
└── CONTRIBUTING.md  # 贡献指南
```

### 文档标准

1. **清晰简洁** - 避免冗长的句子
2. **提供示例** - 代码示例胜过千言万语
3. **解释"为什么"** - 不仅说明做什么，还要说明为什么
4. **包含故障排除** - 帮助用户解决常见问题
5. **保持更新** - 更新最后修改日期

参见 [DOCUMENTATION-GUIDE.md](DOCUMENTATION-GUIDE.md) 了解更多。

## 问题报告

### 报告前检查

- [ ] 搜索现有问题
- [ ] 检查文档
- [ ] 尝试最新版本

### 报告模板

参见 [报告 Bug](#-报告-bug) 部分。

## 开发环境设置

### Node.js 项目

```bash
cd projects/agent-task-cli
npm install
npm test
npm run lint
```

### Python 项目

```bash
cd experiments/local-embedding-memory
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest
```

## 测试规范

### 单元测试

- 每个公共函数都应有测试
- 测试覆盖率 > 80%
- 使用描述性的测试名称

```javascript
describe('MyComponent', () => {
  it('should render correctly', () => {
    // 测试代码
  });
});
```

### 集成测试

- 测试组件之间的交互
- 使用真实的依赖（如果可能）
- 测试关键路径

## 发布流程

1. 更新 `CHANGELOG.md`
2. 更新版本号
3. 运行所有测试
4. 创建 git tag
5. 发布到 npm/PyPI（如适用）

## 获取帮助

- 📖 查看文档: [GETTING-STARTED.md](GETTING-STARTED.md)
- 💬 在 `memory/` 中提问
- 🐛 报告问题: 创建 Bug 报告文件

## 许可证

通过贡献代码，你同意你的贡献将按照 MIT 许可证进行许可。

---

**感谢你的贡献！** ❤️

*最后更新: 2026-03-25*
