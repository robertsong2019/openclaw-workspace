#!/usr/bin/env python3
"""Tech Briefing Generator — aggregates GitHub Trending + HN into a daily digest."""

import json
import urllib.request
import urllib.error
import sys
import argparse
from datetime import datetime, timezone

def fetch_json(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def fetch_text(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode()

def get_github_trending(lang="", since="daily", limit=10):
    """Fetch GitHub trending repos via GitHub Search API (recently pushed, high stars)."""
    try:
        # Use date range based on 'since' param
        from datetime import timedelta
        since_days = {"daily": 1, "weekly": 7, "monthly": 30}.get(since, 1)
        pushed_after = (datetime.now(timezone.utc) - timedelta(days=since_days)).strftime("%Y-%m-%d")
        
        # Find recently created repos sorted by stars (true "trending")
        q = f"created:>{pushed_after} stars:>10"
        if lang:
            q += f" language:{lang}"
        url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page={limit}"
        data = fetch_json(url, timeout=10)
        repos = []
        for r in data.get("items", [])[:limit]:
            repos.append({
                "name": r.get("full_name", ""),
                "desc": (r.get("description", "") or "")[:120],
                "stars": r.get("stargazers_count", 0),
                "today_stars": 0,
                "lang": r.get("language", ""),
                "url": r.get("html_url", ""),
            })
        return repos
    except Exception as e:
        return [{"error": str(e)}]

def get_hn_top(limit=10):
    """Fetch top HN stories via Algolia API."""
    try:
        url = f"https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage={limit}"
        data = fetch_json(url, timeout=10)
        stories = []
        for h in data.get("hits", [])[:limit]:
            stories.append({
                "title": h.get("title", ""),
                "points": h.get("points", 0),
                "comments": h.get("num_comments", 0),
                "url": h.get("url", "") or f"https://news.ycombinator.com/item?id={h.get('objectID','')}",
                "hn_url": f"https://news.ycombinator.com/item?id={h.get('objectID','')}",
            })
        return stories
    except Exception as e:
        return [{"error": str(e)}]

def format_md(github_repos, hn_stories, date_str):
    lines = [f"# 📡 Tech Briefing — {date_str}\n"]
    
    if github_repos and "error" not in github_repos[0]:
        lines.append("## 🔥 GitHub Trending\n")
        for i, r in enumerate(github_repos, 1):
            star_info = f"⭐ {r['stars']:,}"
            if r.get("today_stars"):
                star_info += f" (+{r['today_stars']:,} today)"
            lang = f" [{r['lang']}]" if r.get("lang") else ""
            lines.append(f"**{i}. [{r['name']}]({r['url']})**{lang} — {star_info}")
            if r.get("desc"):
                lines.append(f"   {r['desc']}")
            lines.append("")
    elif github_repos:
        lines.append(f"## 🔥 GitHub Trending\n⚠️ {github_repos[0].get('error', 'fetch failed')}\n")

    if hn_stories and "error" not in hn_stories[0]:
        lines.append("## 📰 Hacker News Top\n")
        for i, s in enumerate(hn_stories, 1):
            lines.append(f"**{i}. [{s['title']}]({s['url']})** — {s['points']} pts, {s['comments']} comments")
            lines.append(f"   [HN讨论]({s['hn_url']})")
            lines.append("")
    elif hn_stories:
        lines.append(f"## 📰 Hacker News Top\n⚠️ {hn_stories[0].get('error', 'fetch failed')}\n")

    return "\n".join(lines)

def format_json(github_repos, hn_stories, date_str):
    return json.dumps({
        "date": date_str,
        "github_trending": github_repos,
        "hn_top": hn_stories,
    }, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Tech Briefing Generator")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--github-limit", type=int, default=10)
    parser.add_argument("--hn-limit", type=int, default=10)
    parser.add_argument("--lang", default="", help="GitHub language filter")
    parser.add_argument("--since", default="daily", choices=["daily", "weekly", "monthly"])
    parser.add_argument("--source", choices=["all", "github", "hn"], default="all")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    gh = get_github_trending(lang=args.lang, since=args.since, limit=args.github_limit) \
        if args.source in ("all", "github") else []
    hn = get_hn_top(limit=args.hn_limit) \
        if args.source in ("all", "hn") else []

    if args.format == "json":
        print(format_json(gh, hn, date_str))
    else:
        print(format_md(gh, hn, date_str))

if __name__ == "__main__":
    main()
