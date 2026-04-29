# agent-log Feature Backlog

## ✅ Existing Features
- `search` command: Search all logs for a keyword with colorized output
- `today` command: Show today's activity timeline
- `date` command: Show activity for a specific date
- `summary` command: Summarize last N days of activity (line counts)
- `cron` command: List all cron job runs
- `stats` command: Show workspace statistics (file counts, sizes)
- Colorized output for better readability
- Zero dependencies, single Bash script

## 🔲 Feature Backlog

### Search Enhancements
- [ ] **F1**: `search` with regex support — allow `-r` flag for regex patterns
- [ ] **F2**: `search` with file filtering — filter by date range or file type
- [ ] **F3**: `search` with export — save results to file (`-o results.txt`)

### Timeline & Summary
- [ ] **F4**: `summary` with keyword filtering — show only entries matching a pattern
- [ ] **F5**: `summary` with activity types — categorize by coding/research/planning
- [ ] **F6**: `trend` command — show activity trends over time (charts/graphs)

### Session Analysis
- [ ] **F7**: `sessions` command — list all session files with metadata
- [ ] **F8**: `session <id>` command — show detailed session transcript
- [ ] **F9**: `find` command — find sessions by agent/model/date

### Output Formats
- [ ] **F10**: JSON output mode — `-j` flag for structured output
- [ ] **F11**: CSV export — export stats/summary as CSV
- [ ] **F12**: Markdown export — format output as Markdown

### Utilities
- [ ] **F13**: `grep` wrapper — fast grep across all log files
- [ ] **F14**: `tail` wrapper — watch latest log files in real-time
- [ ] **F15**: `clean` command — remove old/empty log files (with confirmation)

### Testing & Quality
- [ ] **F16**: Unit tests for each command (Bats framework)
- [ ] **F17**: Integration tests with sample data
- [ ] **F18**: Performance benchmarks for large log sets

## Priorities
**Round 1 (Core UX):** F1, F4, F10 — Improve search and add JSON output
**Round 2 (Analysis):** F6, F7, F8 — Better session and trend analysis
**Round 3 (Quality):** F16, F17 — Add test coverage
