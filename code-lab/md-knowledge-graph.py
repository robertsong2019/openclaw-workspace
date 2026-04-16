#!/usr/bin/env python3
"""
Markdown Knowledge Graph Generator
Scans .md files, extracts headings, links, and tags, outputs a Mermaid diagram.

Usage:
  python3 md-knowledge-graph.py [directory] [--output graph.md] [--max-depth 3]
"""

import os
import re
import sys
import argparse
from collections import defaultdict
from pathlib import Path


def extract_frontmatter_tags(content: str) -> list[str]:
    """Extract tags from YAML frontmatter."""
    tags = []
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm = content[3:end]
            for line in fm.splitlines():
                line = line.strip()
                if line.startswith("- ") and "tag" in content[3:end].lower():
                    tags.append(line[2:].strip().strip('"\''))
    return tags


def extract_headings(content: str, max_depth: int = 3) -> list[tuple[int, str]]:
    """Extract markdown headings as (level, text)."""
    headings = []
    for line in content.splitlines():
        m = re.match(r'^(#{1,6})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            if level <= max_depth:
                headings.append((level, m.group(2).strip()))
    return headings


def extract_links(content: str) -> list[str]:
    """Extract [[wikilinks]] and [md](links) to local .md files."""
    links = set()
    # Wikilinks
    for m in re.finditer(r'\[\[([^\]]+)\]\]', content):
        links.add(m.group(1).split("|")[0].strip())
    # Markdown links to local .md
    for m in re.finditer(r'\[([^\]]*)\]\(([^)]+\.md)\)', content):
        links.add(Path(m.group(2)).stem)
    return list(links)


def sanitize_id(name: str) -> str:
    """Mermaid-safe node ID."""
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)[:50]


def scan_directory(directory: str) -> dict:
    """Scan directory for .md files and build graph data."""
    graph = {}
    for root, _, files in os.walk(directory):
        # Skip hidden dirs and node_modules
        dirs_to_skip = {'.git', 'node_modules', '.venv', '__pycache__'}
        root_path = Path(root)
        if any(p.startswith('.') for p in root_path.parts) and root_path != Path(directory):
            continue
        for f in files:
            if not f.endswith('.md'):
                continue
            fpath = Path(root) / f
            try:
                content = fpath.read_text(encoding='utf-8')
            except Exception:
                continue

            name = fpath.stem
            rel = fpath.relative_to(directory)

            headings = extract_headings(content)
            links = extract_links(content)
            tags = extract_frontmatter_tags(content)

            graph[name] = {
                'path': str(rel),
                'headings': headings,
                'links': links,
                'tags': tags,
                'size': len(content),
            }
    return graph


def render_mermaid(graph: dict, title: str = "Knowledge Graph") -> str:
    """Render graph data as Mermaid flowchart."""
    lines = [f"# {title}\n", "```mermaid", "flowchart LR"]

    # Group by directory
    groups = defaultdict(list)
    for name, data in graph.items():
        dir_name = str(Path(data['path']).parent) or "root"
        groups[dir_name].append(name)

    # Create subgraphs by directory
    for dir_name, members in sorted(groups.items()):
        safe_dir = sanitize_id(dir_name) or "root"
        lines.append(f"    subgraph {safe_dir}[{dir_name}]")
        for name in members:
            safe = sanitize_id(name)
            data = graph[name]
            # Show heading count as badge
            h_count = len(data['headings'])
            label = f"{name}<br/>({h_count} sections)"
            lines.append(f'        {safe}["{label}"]')
        lines.append("    end")

    # Add links as edges
    seen_edges = set()
    for name, data in graph.items():
        safe_from = sanitize_id(name)
        for link in data['links']:
            if link in graph:
                safe_to = sanitize_id(link)
                edge = (safe_from, safe_to)
                rev = (safe_to, safe_from)
                if edge not in seen_edges and rev not in seen_edges:
                    lines.append(f"    {safe_from} --> {safe_to}")
                    seen_edges.add(edge)

    lines.append("```")

    # Stats
    total_links = sum(len(d['links']) for d in graph.values())
    resolved = sum(1 for n, d in graph.items() for l in d['links'] if l in graph)
    lines.append(f"\n---\n📊 **{len(graph)} files** | **{total_links} links** ({resolved} resolved) | "
                 f"**{sum(len(d['headings']) for d in graph.values())} sections**")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Mermaid knowledge graph from markdown files")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--output", "-o", default=None, help="Output file (default: stdout)")
    parser.add_argument("--max-depth", type=int, default=3, help="Max heading depth to extract")
    args = parser.parse_args()

    graph = scan_directory(args.directory)
    if not graph:
        print("No markdown files found.", file=sys.stderr)
        sys.exit(1)

    mermaid = render_mermaid(graph)

    if args.output:
        Path(args.output).write_text(mermaid, encoding='utf-8')
        print(f"✅ Graph written to {args.output} ({len(graph)} nodes)")
    else:
        print(mermaid)


if __name__ == "__main__":
    main()
