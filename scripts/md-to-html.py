#!/usr/bin/env python3
"""
Markdown to HTML converter for blog posts
Uses the blog's HTML template structure
"""

import markdown
import sys
from pathlib import Path
from datetime import datetime

# HTML template for blog posts
TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Robert's Blog</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Syne:wght@700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-600: hsl(250, 70%, 60%);
            --primary-700: hsl(250, 70%, 50%);
            --gray-50: hsl(220, 15%, 98%);
            --gray-100: hsl(220, 15%, 96%);
            --gray-200: hsl(220, 15%, 92%);
            --gray-300: hsl(220, 15%, 85%);
            --gray-400: hsl(220, 10%, 70%);
            --gray-500: hsl(220, 10%, 50%);
            --gray-600: hsl(220, 15%, 35%);
            --gray-700: hsl(220, 20%, 25%);
            --gray-800: hsl(220, 25%, 15%);
            --gray-900: hsl(220, 30%, 10%);
            --text-xs: 0.64rem;
            --text-sm: 0.8rem;
            --text-base: 1rem;
            --text-lg: 1.25rem;
            --text-xl: 1.563rem;
            --text-2xl: 1.953rem;
            --text-3xl: 2.441rem;
            --text-4xl: 3.052rem;
            --space-1: 0.25rem;
            --space-2: 0.5rem;
            --space-3: 0.75rem;
            --space-4: 1rem;
            --space-6: 1.5rem;
            --space-8: 2rem;
            --space-12: 3rem;
            --space-16: 4rem;
            --radius-sm: 0.375rem;
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
            --radius-xl: 1rem;
            --color-primary: var(--primary-600);
            --color-primary-hover: var(--primary-700);
            --color-text-primary: var(--gray-800);
            --color-text-secondary: var(--gray-600);
            --color-text-muted: var(--gray-500);
            --surface-0: var(--gray-50);
            --surface-1: white;
            --surface-2: var(--gray-50);
            --surface-3: var(--gray-100);
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
            --card-bg: var(--surface-1);
            --card-radius: var(--radius-lg);
            --card-padding: var(--space-8);
            --transition-fast: 150ms ease-out;
            --transition-base: 250ms ease-out;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: var(--text-base);
            line-height: 1.6;
            background: var(--surface-0);
            min-height: 100vh;
            padding: var(--space-8) var(--space-4);
            color: var(--color-text-primary);
            -webkit-font-smoothing: antialiased;
        }}
        .container {{ max-width: 48rem; margin: 0 auto; }}
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Syne', 'Outfit', sans-serif;
            font-weight: 800;
            line-height: 1.2;
            letter-spacing: -0.02em;
            color: var(--color-text-primary);
        }}
        h1 {{ font-size: clamp(var(--text-3xl), 1.5rem + 3vw, var(--text-4xl)); margin-bottom: var(--space-2); }}
        h2 {{ font-size: var(--text-2xl); margin: var(--space-8) 0 var(--space-4); display: flex; align-items: center; gap: var(--space-2); }}
        h3 {{ font-size: var(--text-xl); margin: var(--space-6) 0 var(--space-3); }}
        h4 {{ font-size: var(--text-lg); margin: var(--space-4) 0 var(--space-2); }}
        .subtitle {{ font-size: var(--text-lg); color: var(--color-text-secondary); margin-bottom: var(--space-6); font-weight: 500; }}
        .date {{ font-size: var(--text-sm); color: var(--color-text-muted); margin-bottom: var(--space-6); }}
        p {{ margin-bottom: var(--space-4); color: var(--color-text-secondary); line-height: 1.8; }}
        .card {{
            background: var(--card-bg);
            border-radius: var(--card-radius);
            box-shadow: var(--shadow-md);
            padding: var(--card-padding);
            margin-bottom: var(--space-8);
            border: 1px solid var(--gray-200);
        }}
        a {{ color: var(--color-primary); text-decoration: none; transition: color var(--transition-fast); }}
        a:hover {{ color: var(--color-primary-hover); text-decoration: underline; }}
        code {{
            background: var(--surface-3);
            padding: 0.2em 0.4em;
            border-radius: var(--radius-sm);
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: var(--text-sm);
        }}
        pre {{
            background: var(--gray-900);
            color: var(--gray-100);
            padding: var(--space-4);
            border-radius: var(--radius-md);
            overflow-x: auto;
            margin: var(--space-4) 0;
        }}
        pre code {{
            background: none;
            padding: 0;
            color: inherit;
            font-size: var(--text-sm);
        }}
        ul, ol {{ margin: var(--space-4) 0; padding-left: var(--space-6); }}
        li {{ margin-bottom: var(--space-2); color: var(--color-text-secondary); }}
        blockquote {{
            border-left: 4px solid var(--color-primary);
            padding-left: var(--space-4);
            margin: var(--space-4) 0;
            color: var(--color-text-muted);
            font-style: italic;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: var(--space-4) 0;
        }}
        th, td {{
            padding: var(--space-2) var(--space-3);
            text-align: left;
            border-bottom: 1px solid var(--gray-200);
        }}
        th {{
            font-weight: 600;
            color: var(--color-text-primary);
            background: var(--surface-2);
        }}
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: var(--space-2);
            margin-bottom: var(--space-6);
            font-size: var(--text-sm);
            color: var(--color-text-muted);
        }}
        .back-link:hover {{ color: var(--color-primary); }}
        .tags {{
            display: flex;
            gap: var(--space-2);
            flex-wrap: wrap;
            margin-top: var(--space-6);
        }}
        .tag {{
            background: var(--gray-100);
            color: var(--gray-700);
            padding: var(--space-1) var(--space-3);
            border-radius: var(--radius-md);
            font-size: var(--text-xs);
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../essays.html" class="back-link">← 返回随笔列表</a>
        <div class="card">
            <h1>{title}</h1>
            <div class="date">{date}</div>
            <div class="content">
{content}
            </div>
        </div>
    </div>
</body>
</html>'''

def convert_file(md_path: Path, output_dir: Path):
    """Convert a markdown file to HTML"""
    # Read markdown
    md_content = md_path.read_text(encoding='utf-8')
    
    # Extract title (first h1)
    lines = md_content.split('\n')
    title = lines[0].lstrip('#').strip() if lines else md_path.stem
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc']
    )
    
    # Extract date from filename (2026-03-21-...)
    date_str = md_path.stem[:10]
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y年%m月%d日')
    except:
        date = date_str
    
    # Generate output filename
    output_name = md_path.stem[11:] + '.html'  # Remove date prefix
    output_path = output_dir / output_name
    
    # Fill template
    html = TEMPLATE.format(
        title=title,
        date=date,
        content=html_content
    )
    
    # Write output
    output_path.write_text(html, encoding='utf-8')
    print(f"✅ Converted: {md_path.name} → {output_name}")
    return output_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python md-to-html.py <markdown-file> [output-dir] [--output <filename>]")
        sys.exit(1)
    
    md_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else Path.cwd()
    output_name = None
    
    # Parse --output argument
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_name = sys.argv[idx + 1]
    
    if not md_path.exists():
        print(f"❌ File not found: {md_path}")
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if output_name:
        # Custom output filename
        md_content = md_path.read_text(encoding='utf-8')
        lines = md_content.split('\n')
        title = lines[0].lstrip('#').strip() if lines else md_path.stem
        
        html_content = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'toc']
        )
        
        date_str = md_path.stem[:10]
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y年%m月%d日')
        except:
            date = date_str
        
        output_path = output_dir / output_name
        html = TEMPLATE.format(
            title=title,
            date=date,
            content=html_content
        )
        
        output_path.write_text(html, encoding='utf-8')
        print(f"✅ Converted: {md_path.name} → {output_name}")
    else:
        convert_file(md_path, output_dir)

if __name__ == '__main__':
    main()
