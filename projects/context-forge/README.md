# context-forge 🔨

> Analyze your codebase and generate optimal context files for AI coding agents.

## Why

AI coding assistants (Cursor, Copilot, Claude Code, Codex) work better when they understand your project. But writing good context files (`AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`) is tedious and gets outdated.

**context-forge** scans your repo and generates these files automatically — so your AI tools always have up-to-date project context.

## Quick Start

```bash
# Install
cp context-forge.mjs /usr/local/bin/context-forge

# Run on your project
context-forge /path/to/my-project

# Preview what it would generate (no files written)
context-forge /path/to/my-project --dry-run
```

## Features

- 🔍 **Auto-detects** project type (Node.js, Python, Go, Rust, etc.)
- 📦 **Extracts** dependencies, scripts, entry points from `package.json`/`pyproject.toml`/`Cargo.toml`
- 🏗️ **Maps** directory structure and architecture patterns
- 📝 **Generates** context files for multiple AI tools
- 🔄 **Updates** existing files (preserves manual additions in marked sections)
- ⚡ **Zero deps** — single file, runs with Node.js

## Usage

```bash
# Generate all context files
context-forge /path/to/project

# Generate specific file only
context-forge /path/to/project --only agents

# Preview without writing
context-forge /path/to/project --dry-run

# Update existing (preserve manual sections)
context-forge /path/to/project --update
```

## Generated Files

| File | Target Agent | Purpose |
|------|-------------|---------|
| `AGENTS.md` | OpenClaw, Claude Code | Project context, conventions, build steps |
| `.cursorrules` | Cursor | Editor-specific rules and context |
| `.github/copilot-instructions.md` | GitHub Copilot | PR/code review guidelines |
| `.claude/CLAUDE.md` | Claude Code | Detailed project instructions |

## How It Works

```
context-forge scans:
  ├── package.json / pyproject.toml / Cargo.toml  → deps, scripts, entry points
  ├── Directory structure                          → architecture patterns
  ├── Git history (optional)                       → naming conventions, recent changes
  └── Existing context files                       → preserve manual additions

Then generates:
  └── Context files with project summary, conventions, and AI instructions
```

### Update Mode

When you use `--update`, context-forge preserves any content you've manually added between `<!-- context-forge:start -->` and `<!-- context-forge:end -->` markers, while refreshing the auto-generated sections.

## Extending

`context-forge.mjs` is a single ESM file. Key extension points:

- **New project detectors** — add a function that returns `{ type, language, framework }` from project files
- **New output templates** — add a generator function for new AI tool formats
- **Custom markers** — modify `MARKER_START`/`MARKER_END` constants

## License

MIT
