#!/usr/bin/env python3
"""Tech Briefing Generator — aggregates GitHub Trending + HN + CN sources into a daily digest."""

import json
import urllib.request
import urllib.error
import urllib.parse
import re
import sys
import argparse
from datetime import datetime, timezone

def fetch_json(url, timeout=15, headers=None):
    hdrs = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def fetch_text(url, timeout=15, headers=None):
    hdrs = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode()

def get_github_trending(lang="", since="daily", limit=10):
    """Fetch GitHub trending repos by scraping github.com/trending page."""
    try:
        since_param = {"daily": "", "weekly": "?since=weekly", "monthly": "?since=monthly"}.get(since, "")
        lang_param = f"&l={lang}" if lang else ""
        sep = "&" if "?" in since_param and lang_param else ""
        if not since_param and lang_param:
            url = f"https://github.com/trending?l={lang}"
        else:
            url = f"https://github.com/trending{since_param}{sep}{lang_param}"
        html = fetch_text(url, timeout=15)
        repos = []
        # Parse trending repo rows
        # Pattern: <h2 class="h3 lh-condensed"><a href="/owner/repo">
        repo_pattern = re.compile(
            r'<h2[^>]*class="h3[^"]*"[^>]*>.*?'
            r'<a\s+href="(/[^"]+?)"[^>]*>\s*'
            r'(?:<span[^>]*>\s*)?([^<]+?)\s*(?:</span>)?\s*'
            r'(?:/\s*(?:<span[^>]*>\s*)?([^<]+?)\s*(?:</span>)?)?\s*'
            r'</a>', re.DOTALL)
        # Simpler: find all /owner/repo links in h2
        for m in re.finditer(r'<article.*?</article>', html, re.DOTALL):
            block = m.group(0)
            # Repo name
            name_m = re.search(r'<h2[^>]*>.*?<a\s+href="(/[^"]+)"', block, re.DOTALL)
            if not name_m:
                continue
            repo_path = name_m.group(1).strip().split('/stargazers')[0].split('/forks')[0]
            name = repo_path.lstrip('/')
            # Description
            desc_m = re.search(r'<p[^>]*class="[^"]*color-fg-muted[^"]*"[^>]*>(.*?)</p>', block, re.DOTALL)
            desc = desc_m.group(1).strip()[:120] if desc_m else ""
            desc = re.sub(r'<[^>]+>', '', desc).strip()
            # Language
            lang_m = re.search(r'itemprop="programmingLanguage">(.*?)<', block)
            repo_lang = lang_m.group(1).strip() if lang_m else ""
            # Stars today
            today_m = re.search(r'([\d,]+)\s*stars\s*(?:this\s*)?(?:today|week|month)', block)
            today_stars = int(today_m.group(1).replace(',', '')) if today_m else 0
            # Total stars
            stars_m = re.search(r'href="/[^/]+/[^/]+/stargazers"[^>]*>\s*([\d,]+)\s*<', block)
            stars = int(stars_m.group(1).replace(',', '')) if stars_m else 0
            repos.append({
                "name": name,
                "desc": desc,
                "stars": stars,
                "today_stars": today_stars,
                "lang": repo_lang,
                "url": f"https://github.com{repo_path}",
            })
            if len(repos) >= limit:
                break
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

def get_oschina_news(limit=10):
    """Fetch OSCHINA news via RSS feed (has title + description)."""
    try:
        xml = fetch_text("https://www.oschina.net/news/rss", timeout=15)
        articles = []
        for m in re.finditer(
            r'<item>\s*<title><!\[CDATA\[([^\]]*?)\]\]></title>\s*'
            r'<link><!\[CDATA\[([^\]]*?)\]\]></link>.*?'
            r'<description><!\[CDATA\[([^\]]*?)\]\]></description>',
            xml, re.DOTALL
        ):
            title = m.group(1).strip()
            url = m.group(2).strip()
            desc = m.group(3).strip()[:200]
            # Unescape HTML entities
            desc = desc.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            articles.append({"title": title, "url": url, "snippet": desc})
            if len(articles) >= limit:
                break
        return articles
    except Exception as e:
        return [{"error": str(e)}]

def get_cn_news_via_search(limit=10):
    """Fetch CN tech news via Tavily search (for SPA sites like InfoQ)."""
    try:
        import os
        api_key = os.environ.get("TAVILY_API_KEY", "")
        if not api_key:
            return [{"error": "TAVILY_API_KEY not set"}]
        url = "https://api.tavily.com/search"
        payload = json.dumps({
            "api_key": api_key,
            "query": "最新技术资讯 AI 开发者",
            "include_domains": ["infoq.cn"],
            "max_results": limit,
            "search_depth": "basic",
            "topic": "news",
        }).encode()
        req = urllib.request.Request(url, data=payload,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
        articles = []
        for res in data.get("results", []):
            articles.append({
                "title": res.get("title", ""),
                "url": res.get("url", ""),
                "snippet": (res.get("content", "") or "")[:150],
            })
        return articles[:limit]
    except Exception as e:
        return [{"error": str(e)}]

def format_md(github_repos, hn_stories, cn_articles, date_str):
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

    if cn_articles and "error" not in cn_articles[0]:
        lines.append("## 🇨🇳 国内技术资讯\n")
        for i, a in enumerate(cn_articles, 1):
            snippet = f"\n   {a['snippet']}" if a.get("snippet") else ""
            lines.append(f"**{i}. [{a['title']}]({a['url']})**{snippet}")
            lines.append("")
    elif cn_articles:
        lines.append(f"## 🇨🇳 国内技术资讯\n⚠️ {cn_articles[0].get('error', 'fetch failed')}\n")

    return "\n".join(lines)

def format_json(github_repos, hn_stories, cn_articles, date_str):
    return json.dumps({
        "date": date_str,
        "github_trending": github_repos,
        "hn_top": hn_stories,
        "cn_news": cn_articles,
    }, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Tech Briefing Generator")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--github-limit", type=int, default=10)
    parser.add_argument("--hn-limit", type=int, default=10)
    parser.add_argument("--lang", default="", help="GitHub language filter")
    parser.add_argument("--since", default="daily", choices=["daily", "weekly", "monthly"])
    parser.add_argument("--cn-limit", type=int, default=10, help="CN news limit")
    parser.add_argument("--source", choices=["all", "github", "hn", "cn"], default="all")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    gh = get_github_trending(lang=args.lang, since=args.since, limit=args.github_limit) \
        if args.source in ("all", "github") else []
    hn = get_hn_top(limit=args.hn_limit) \
        if args.source in ("all", "hn") else []

    # CN sources: OSChina (page scrape) + InfoQ (Tavily search)
    cn = []
    if args.source in ("all", "cn"):
        osc = get_oschina_news(limit=args.cn_limit)
        if osc and "error" not in osc[0]:
            cn.extend(osc)
        infoq = get_cn_news_via_search(limit=args.cn_limit)
        if infoq and "error" not in infoq[0]:
            cn.extend(infoq)

    if args.format == "json":
        print(format_json(gh, hn, cn, date_str))
    else:
        print(format_md(gh, hn, cn, date_str))

if __name__ == "__main__":
    main()
