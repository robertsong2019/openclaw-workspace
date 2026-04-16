# agent-memory-kit (amk)

CLI for managing and searching AI agent memory files, session logs, and workspace context.

## Install

```bash
cd tools/agent-memory-kit
npm install -g .
# or just: node cli.mjs <command>
```

## Commands

| Command | Description |
|---------|-------------|
| `amk search <query>` | Full-text search across all memory files |
| `amk summary` | Show recent memory summary (last 7 days) |
| `amk stats` | Memory statistics — file count, size, date range |
| `amk tags` | Extract top terms/topics from all memory files |
| `amk timeline` | Chronological activity timeline with headings |
| `amk merge <src> <dst>` | Merge one memory file into another |
| `amk prune <days> [--apply]` | List/remove files older than N days |
| `amk context [path]` | Generate a context snapshot for LLM prompts |

## Why?

AI agents accumulate memory files over time. This tool helps you:
- **Find things** — search across months of daily memory files
- **Understand patterns** — see what topics come up most via `tags`
- **Clean up** — prune old files safely
- **Build prompts** — `context` generates a ready-to-use context block

## Design

- Zero dependencies — pure Node.js
- Works with OpenClaw workspace structure (`memory/YYYY-MM-DD.md`, `MEMORY.md`)
- Safe by default — destructive operations require `--apply`
- Respects `OPENCLAW_WORKSPACE` env var for custom paths
