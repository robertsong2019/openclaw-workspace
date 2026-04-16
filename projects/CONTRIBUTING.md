# 贡献指南

感谢你对本工作区项目的兴趣！以下是参与贡献的方式。

## 通用规则

### 代码风格

- **Bash 脚本**: 使用 `shellcheck` 检查，遵循 [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- **Node.js**: ESM (`import`/`export`)，单文件优先，零依赖优先
- **Python**: PEP 8，类型注解，标准库优先

### 提交规范

```
<type>: <简短描述>

[可选的详细说明]
```

类型：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`

### 文档要求

- 每个项目必须有 `README.md`（包含：概述、快速开始、用法）
- API 变更需同步更新文档
- 新功能需附带使用示例

## 贡献流程

1. **Fork 或创建分支** — 不直接 push 到 main
2. **小步提交** — 每个提交做好一件事
3. **测试** — 确保现有测试通过，新功能有测试
4. **文档** — 更新 README 和 CHANGELOG
5. **PR 描述** — 说明做了什么、为什么、如何验证

## 项目结构

```
projects/
├── agent-log/            # 日志搜索 CLI (Bash)
├── agent-memory-graph/   # 知识图谱记忆 (Python)
├── agent-memory-service/ # 三层记忆服务 (Node.js)
├── agent-task-cli/       # 多 Agent 编排 CLI (Node.js)
├── askill/               # Skill 工具
├── context-forge/        # AI 上下文生成器 (Node.js)
├── mission-control/      # 监控仪表板 (HTML/JS)
└── prompt-mgr/           # Prompt 管理 CLI (Node.js)
```

## 设计原则

- **零依赖优先** — 能用标准库就用标准库
- **单文件优先** — 工具类项目尽量保持单文件
- **Unix 哲学** — 做好一件事，可组合
- **文档即代码** — README 和代码同等重要

## 问题反馈

- GitHub Issues 或直接联系维护者
- Bug 报告请包含：复现步骤、期望行为、实际行为

---

_MIT License_
