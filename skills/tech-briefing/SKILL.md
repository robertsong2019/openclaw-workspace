---
name: tech-briefing
description: "Generate daily tech briefings from GitHub Trending and Hacker News. Use when user asks for tech news, trending repos, daily digest, what's hot in tech, or briefing. Triggers on phrases like 'tech briefing', 'daily digest', 'trending repos', 'HN top stories', '技术简报', '今日热点'."
metadata:
  {
    "openclaw":
      {
        "emoji": "📡",
        "requires": { "bins": ["python3"] }
      }
  }
---

# Tech Briefing

Generate a structured daily tech digest aggregating **GitHub Trending** repos, **Hacker News** top stories, and **CN tech news** (OSChina + InfoQ 中文).

## Quick Start

```bash
# Full briefing (Markdown)
python3 {baseDir}/scripts/tech_briefing.py

# JSON output (for programmatic use)
python3 {baseDir}/scripts/tech_briefing.py --format json

# GitHub only, weekly, Python repos
python3 {baseDir}/scripts/tech_briefing.py --source github --since weekly --lang python

# HN only, top 5
python3 {baseDir}/scripts/tech_briefing.py --source hn --hn-limit 5

# CN sources only (OSChina + InfoQ)
python3 {baseDir}/scripts/tech_briefing.py --source cn --cn-limit 10
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--format` | `md` | Output: `md` or `json` |
| `--cn-limit` | `10` | Max CN news items per source |
| `--source` | `all` | `all`, `github`, `hn`, or `cn` |
| `--github-limit` | `10` | Max GitHub repos |
| `--hn-limit` | `10` | Max HN stories |
| `--lang` | _(all)_ | GitHub language filter (e.g. `python`, `rust`) |
| `--since` | `daily` | `daily`, `weekly`, or `monthly` |

## Workflow

1. Run the script to fetch data
2. Summarize highlights in natural language
3. Highlight repos or stories relevant to the user's interests (check USER.md / MEMORY.md)
4. Optionally compare with previous briefings for trend detection

## CN Sources

- **OSChina** (`oschina.net/news`): Page scraping, no API key needed
- **InfoQ 中文** (`infoq.cn`): Via Tavily search API (requires `TAVILY_API_KEY` env var)
- Use `--source cn` to fetch CN news only

## Notes

- GitHub + HN: No API key required (public endpoints)
- InfoQ CN requires `TAVILY_API_KEY` (InfoQ is SPA, no public API)
- Keep limits small (5-10) for token efficiency
- For heartbeat integration: add to HEARTBEAT.md as a periodic check
