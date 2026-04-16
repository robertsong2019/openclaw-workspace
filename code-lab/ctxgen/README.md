# ctxgen

Auto-generate AI-friendly context files for your codebase.

Analyzes your Git repo structure, tech stack, conventions, and patterns — then produces ready-to-use context files for AI coding assistants (OpenClaw, Cursor, Claude Code, etc.).

## Install

```bash
npm install -g ctxgen
# or
npx ctxgen .
```

## Usage

```bash
# Generate all context files
ctxgen .

# Generate specific targets
ctxgen . --target agents.md --target cursorrules

# Preview without writing
ctxgen . --dry-run

# Custom output
ctxgen . --output ./docs/CONTEXT.md
```

## What it generates

- **AGENTS.md** — Project context for OpenClaw / AI agents
- **.cursorrules** — Rules for Cursor IDE
- **CLAUDE.md** — Context for Claude Code
- **context.md** — General AI context summary

## How it works

1. Scans directory structure (respects .gitignore)
2. Detects tech stack (languages, frameworks, tools)
3. Analyzes code patterns and conventions
4. Reads existing config files (package.json, tsconfig, etc.)
5. Generates context files tailored to each AI tool's format
