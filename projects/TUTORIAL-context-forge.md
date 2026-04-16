# Tutorial: 用 context-forge 让 AI 编码助手真正理解你的项目

> **适合**: 任何使用 Cursor / Claude Code / Copilot / Codex 的开发者
> **难度**: 初级
> **时间**: 10 分钟

---

## 你有没有遇到过这些问题？

- Cursor 总是生成不符合你项目风格的代码？
- Claude Code 不知道你的项目用什么测试框架？
- 每次开新对话都要重复解释项目结构？

**根本原因**: AI 编码助手不知道你的项目上下文。它们需要一份"项目说明书"。

`context-forge` 就是自动生成这份说明书的工具。

---

## 概念：什么是"上下文文件"？

AI 编码助手通过读取项目中的特定文件来理解项目：

| 文件 | 谁读它 | 里面有什么 |
|------|--------|-----------|
| `AGENTS.md` | OpenClaw, Claude Code | 项目约定、构建步骤、代码风格 |
| `.cursorrules` | Cursor | 编辑器规则和上下文 |
| `.github/copilot-instructions.md` | GitHub Copilot | PR/代码审查指南 |
| `.claude/CLAUDE.md` | Claude Code | 详细项目指令 |

手动写这些文件很烦，而且容易过时。**context-forge 自动生成它们。**

---

## Step 1: 安装

```bash
# 确保你有 Node.js (v18+)
node --version

# 下载单文件（零依赖）
cp context-forge.mjs /usr/local/bin/context-forge
chmod +x /usr/local/bin/context-forge
```

就这样。不需要 `npm install`，不需要任何依赖。

---

## Step 2: 预览（不写文件）

在运行之前，先看看它会生成什么：

```bash
context-forge /path/to/your-project --dry-run
```

你会看到类似这样的输出：

```markdown
## AGENTS.md

# Project: my-app

## Overview
Node.js (ESM) project with TypeScript.

## Dependencies
- express (production)
- jest (development)

## Scripts
- `npm test` — Run tests with Jest
- `npm start` — Start server

## Conventions
- Language: TypeScript
- Entry points: src/index.ts
```

**这时候没有任何文件被修改。** 安全地预览。

---

## Step 3: 正式生成

确认预览内容没问题后：

```bash
context-forge /path/to/your-project
```

这会在项目目录下生成 4 个上下文文件。

---

## Step 4: 添加你的定制内容

自动生成的内容是基础。你可以在此基础上添加项目特有的规则：

```bash
context-forge /path/to/your-project --update
```

**关键**: `--update` 模式会保留你手动添加的内容。原理是使用标记：

```markdown
<!-- context-forge:start -->
这部分是自动生成的，会被更新
<!-- context-forge:end -->

这部分是你手动写的，更新时会被保留
```

---

## 实战案例：给一个 Express 项目生成上下文

```bash
# 1. 克隆或进入项目
cd ~/my-express-app

# 2. 预览
context-forge . --dry-run

# 3. 生成
context-forge .

# 4. 检查生成的 AGENTS.md
cat AGENTS.md

# 5. 在标记外添加你的规则
# 例如：禁止使用 var，必须用 async/await 等

# 6. 下次更新时保留你的修改
context-forge . --update
```

---

## 它是怎么工作的？

简单三步：

1. **检测项目类型** — 扫描 `package.json`、`pyproject.toml`、`Cargo.toml` 等
2. **分析结构** — 读取目录结构、入口文件、依赖关系
3. **生成文件** — 根据模板为每个 AI 工具生成对应格式

支持的检测：
- **语言**: JavaScript, TypeScript, Python, Go, Rust, Ruby, Java, Kotlin, Swift, Zig, Vue, Svelte
- **包管理**: npm/pnpm/yarn, pip/poetry, cargo, go modules
- **框架**: 自动从依赖中推断（express, fastapi, react, next.js 等）

---

## 只生成特定文件

不需要所有文件？只生成你用的：

```bash
# 只生成 AGENTS.md（给 Claude Code 用）
context-forge . --only agents

# 只生成 .cursorrules（给 Cursor 用）
context-forge . --only cursor

# 只生成 Copilot 指令
context-forge . --only copilot
```

---

## 扩展和定制

`context-forge.mjs` 是一个单文件，可以自由修改：

- **添加新的项目检测器** — 写一个返回 `{ type, language, framework }` 的函数
- **添加新的输出模板** — 为新的 AI 工具添加生成函数
- **修改标记格式** — 改 `MARKER_START`/`MARKER_END` 常量

---

## 总结

| 场景 | 命令 |
|------|------|
| 首次使用 | `context-forge .` |
| 预览不写入 | `context-forge . --dry-run` |
| 更新保留手动内容 | `context-forge . --update` |
| 只生成 Cursor 规则 | `context-forge . --only cursor` |

**核心思路**: 让 AI 工具自动读取项目上下文 → 生成的代码质量显著提升 → 省去每次对话重复解释的麻烦。

---

_基于 [context-forge](./context-forge/) 项目_
