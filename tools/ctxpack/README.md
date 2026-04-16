# ctxpack

Generate optimized context files for AI coding agents.

Analyzes your project structure, identifies key files, and produces a well-structured context file (AGENTS.md, CLAUDE.md, .cursorrules, etc.) that helps AI agents understand your codebase.

## Features

- **Smart scanning** — Respects `.gitignore`, skips node_modules, dist, build dirs
- **Auto-detection** — Identifies project type (Node, Python, Rust, Go, etc.)
- **Key file extraction** — Finds entry points, configs, schemas, tests
- **Token-aware** — Estimates token count and warns on oversized output
- **Multiple formats** — Output as AGENTS.md, CLAUDE.md, .cursorrules, or custom
- **Diff mode** — Update existing context files, only changing what's needed

## Usage

```bash
# Generate context for current project
python3 ctxpack.py /path/to/project

# Specify output format
python3 ctxpack.py /path/to/project --format claude

# Custom output file
python3 ctxpack.py /path/to/project -o CONTEXT.md

# Include specific patterns
python3 ctxpack.py /path/to/project --include "*.schema.ts" "*.config.js"

# Set max tokens (default: 8000)
python3 ctxpack.py /path/to/project --max-tokens 4000
```

## How It Works

1. Scans directory tree (respecting gitignore)
2. Detects project type and frameworks
3. Identifies key files (entry, config, schemas, tests)
4. Reads and summarizes each key file
5. Generates structured context markdown
6. Estimates token usage

## Output Sections

- **Project Overview** — Type, framework, language
- **Architecture** — Directory structure, key modules
- **Key Files** — Important files with descriptions
- **Patterns & Conventions** — Detected coding patterns
- **Build & Test** — How to build, test, run
- **Dependencies** — Key dependencies and their roles
