# session-archiver 📦

Archive, search, and export OpenClaw agent session histories.

## Features

- **Archive** live or completed sessions to local JSON store
- **Full-text search** across all archived sessions (supports Chinese text)
- **Export** to Markdown, HTML, or JSON
- **Statistics** — disk usage, message counts, date ranges
- **Auto-clean** — remove archives older than N days

## Install

```bash
cd tools/session-archiver
npm install
npm link  # optional, makes `session-archiver` available globally
```

## Usage

```bash
# Archive a specific session
session-archiver archive --id abc123 --label "Debug session"

# Archive all live sessions
session-archiver archive --all

# List archives
session-archiver list
session-archiver list --json

# Search
session-archiver search "部署失败"
session-archiver search "API error" --limit 5

# Export
session-archiver export abc123 --format markdown
session-archiver export abc123 --format html --output session.html

# Stats
session-archiver stats

# Clean old archives
session-archiver clean --days 90 --dry-run
session-archiver clean --days 90
```

## Architecture

```
bin/cli.js          — CLI entry point (Commander.js)
lib/archive.js      — Core: storage, search, export, stats, clean
lib/openclaw-api.js — OpenClaw gateway integration
lib/archive.test.js — Node.js built-in test runner
```

## Storage

Archives stored at `~/.openclaw/session-archives/<id>.json`. Override with `SESSION_ARCHIVE_DIR` env var.

Each archive contains: metadata, full message history, and a pre-built inverted index for fast search.

## Design Principles

- **Zero dependencies** — only Node.js built-ins (chalk optional for colors)
- **Offline-first** — all data local, no network required for search/export
- **Portable formats** — export to universal formats (MD/HTML/JSON)
- **Testable** — built-in tests using Node.js test runner
