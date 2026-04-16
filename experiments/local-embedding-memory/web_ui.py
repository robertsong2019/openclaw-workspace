#!/usr/bin/env python3
"""
Web UI for Local Embedding Memory Searcher
============================================

A simple web interface for semantic memory search.
Run: python web_ui.py --port 8080
Then open: http://localhost:8080
"""

import argparse
import json
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import subprocess
import sys

# HTML Template for the UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Memory Search</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #e0e0e0;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #00d9ff, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subtitle {
            color: #888;
            font-size: 1rem;
        }
        
        .search-box {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            backdrop-filter: blur(10px);
        }
        
        .search-input-wrapper {
            display: flex;
            gap: 12px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 16px 20px;
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            background: rgba(0, 0, 0, 0.3);
            color: #fff;
            font-size: 1.1rem;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #00d9ff;
        }
        
        input[type="text"]::placeholder {
            color: #666;
        }
        
        button {
            padding: 16px 32px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(90deg, #00d9ff, #00ff88);
            color: #1a1a2e;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 217, 255, 0.3);
        }
        
        .options {
            display: flex;
            gap: 20px;
            margin-top: 16px;
            color: #888;
            font-size: 0.9rem;
        }
        
        .options label {
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }
        
        input[type="checkbox"] {
            width: 18px;
            height: 18px;
            accent-color: #00d9ff;
        }
        
        input[type="number"] {
            width: 60px;
            padding: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            background: rgba(0, 0, 0, 0.3);
            color: #fff;
            text-align: center;
        }
        
        .results {
            margin-top: 24px;
        }
        
        .result-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            transition: border-color 0.3s, transform 0.2s;
        }
        
        .result-card:hover {
            border-color: rgba(0, 217, 255, 0.3);
            transform: translateX(4px);
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        
        .result-score {
            background: linear-gradient(90deg, #00d9ff, #00ff88);
            color: #1a1a2e;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
        }
        
        .result-source {
            color: #888;
            font-size: 0.85rem;
        }
        
        .result-section {
            color: #00d9ff;
            font-size: 0.9rem;
            margin-bottom: 8px;
        }
        
        .result-content {
            color: #ccc;
            line-height: 1.6;
            white-space: pre-wrap;
        }
        
        .stats {
            text-align: center;
            color: #666;
            padding: 20px;
        }
        
        .error {
            background: rgba(255, 0, 0, 0.1);
            border: 1px solid rgba(255, 0, 0, 0.3);
            color: #ff6b6b;
            padding: 16px;
            border-radius: 12px;
            text-align: center;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #888;
        }
        
        footer {
            text-align: center;
            margin-top: 40px;
            color: #555;
            font-size: 0.85rem;
        }
        
        footer a {
            color: #00d9ff;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🧠 Memory Search</h1>
            <p class="subtitle">Semantic search for your MEMORY.md files</p>
        </header>
        
        <div class="search-box">
            <form id="searchForm">
                <div class="search-input-wrapper">
                    <input type="text" id="query" name="query" placeholder="Search your memories..." value="{{QUERY}}">
                    <button type="submit">Search</button>
                </div>
                <div class="options">
                    <label>
                        <input type="checkbox" id="compare" name="compare" {{COMPARE_CHECKED}}>
                        Compare semantic vs text search
                    </label>
                    <label>
                        Top
                        <input type="number" id="topK" name="topK" value="{{TOP_K}}" min="1" max="20">
                        results
                    </label>
                </div>
            </form>
        </div>
        
        <div class="results" id="results">
            {{RESULTS}}
        </div>
        
        <footer>
            Powered by <a href="https://www.sbert.net/">sentence-transformers</a> |
            Part of <a href="#">Local Embedding Memory</a>
        </footer>
    </div>
</body>
</html>
"""


class MemorySearchHandler(SimpleHTTPRequestHandler):
    """Custom handler for memory search"""
    
    searcher = None
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/" or parsed.path == "":
            self.handle_home(parsed)
        elif parsed.path == "/api/search":
            self.handle_api_search(parsed)
        else:
            super().do_GET()
    
    def handle_home(self, parsed):
        """Handle home page with optional search results"""
        query = parse_qs(parsed.query).get("query", [""])[0]
        top_k = int(parse_qs(parsed.query).get("topK", ["5"])[0])
        compare = "compare" in parse_qs(parsed.query)
        
        results_html = ""
        
        if query:
            try:
                if compare:
                    results_html = self.render_compare_results(query, top_k)
                else:
                    results_html = self.render_results(query, top_k)
            except Exception as e:
                results_html = f'<div class="error">Error: {str(e)}</div>'
        else:
            results_html = '<div class="stats">Ready to search. Enter a query above.</div>'
        
        html = HTML_TEMPLATE.replace("{{QUERY}}", query)
        html = html.replace("{{TOP_K}}", str(top_k))
        html = html.replace("{{COMPARE_CHECKED}}", "checked" if compare else "")
        html = html.replace("{{RESULTS}}", results_html)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_api_search(self, parsed):
        """Handle API search request"""
        query = parse_qs(parsed.query).get("query", [""])[0]
        top_k = int(parse_qs(parsed.query).get("topK", ["5"])[0])
        
        if not query:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "No query provided"}).encode())
            return
        
        try:
            results = self.searcher.search(query, top_k)
            data = {
                "query": query,
                "results": [
                    {
                        "score": float(score),
                        "source": chunk.source,
                        "section": chunk.metadata.get("header", ""),
                        "content": chunk.content[:500]
                    }
                    for chunk, score in results
                ]
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data, indent=2).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def render_results(self, query: str, top_k: int) -> str:
        """Render search results as HTML"""
        results = self.searcher.search(query, top_k)
        
        if not results:
            return '<div class="stats">No results found.</div>'
        
        html = f'<div class="stats">Found {len(results)} results for "{query}"</div>'
        
        for i, (chunk, score) in enumerate(results, 1):
            html += f"""
            <div class="result-card">
                <div class="result-header">
                    <span class="result-source">{chunk.source}</span>
                    <span class="result-score">{score:.3f}</span>
                </div>
                {f'<div class="result-section">Section: {chunk.metadata.get("header")}</div>' if chunk.metadata.get("header") else ''}
                <div class="result-content">{chunk.content[:400]}...</div>
            </div>
            """
        
        return html
    
    def render_compare_results(self, query: str, top_k: int) -> str:
        """Render comparison between semantic and text search"""
        semantic_results = self.searcher.search(query, top_k)
        text_results = self.searcher.text_search(query, top_k)
        
        html = f'<div class="stats">Comparing semantic vs text search for "{query}"</div>'
        
        html += '<h3 style="color: #00d9ff; margin: 20px 0 10px;">🧠 Semantic Search</h3>'
        
        for chunk, score in semantic_results:
            html += f"""
            <div class="result-card">
                <div class="result-header">
                    <span class="result-source">{chunk.source}</span>
                    <span class="result-score">{score:.3f}</span>
                </div>
                {f'<div class="result-section">Section: {chunk.metadata.get("header")}</div>' if chunk.metadata.get("header") else ''}
                <div class="result-content">{chunk.content[:300]}...</div>
            </div>
            """
        
        html += '<h3 style="color: #00d9ff; margin: 20px 0 10px;">📝 Text Search</h3>'
        
        for chunk, score in text_results:
            html += f"""
            <div class="result-card">
                <div class="result-header">
                    <span class="result-source">{chunk.source}</span>
                    <span class="result-score">{score:.3f}</span>
                </div>
                {f'<div class="result-section">Section: {chunk.metadata.get("header")}</div>' if chunk.metadata.get("header") else ''}
                <div class="result-content">{chunk.content[:300]}...</div>
            </div>
            """
        
        return html
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def main():
    parser = argparse.ArgumentParser(description="Web UI for Memory Searcher")
    parser.add_argument("--port", type=int, default=8080, help="Port to run server on")
    parser.add_argument("--memory-dir", type=str, default="/root/.openclaw/workspace", help="Memory directory")
    parser.add_argument("--model", type=str, default="all-MiniLM-L6-v2", help="Embedding model")
    
    args = parser.parse_args()
    
    # Import and initialize searcher
    from memory_embedder import LocalMemorySearcher
    
    print(f"🧠 Initializing Memory Searcher...")
    print(f"   Memory dir: {args.memory_dir}")
    print(f"   Model: {args.model}")
    
    searcher = LocalMemorySearcher(
        memory_dir=Path(args.memory_dir),
        model_name=args.model
    )
    
    # Check if index exists
    if not searcher.index.load():
        print("⚠️  No index found. Please run: python memory_embedder.py --index")
        sys.exit(1)
    
    MemorySearchHandler.searcher = searcher
    
    server = HTTPServer(("0.0.0.0", args.port), MemorySearchHandler)
    
    print(f"\n✅ Web UI running at: http://localhost:{args.port}")
    print(f"   Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")


if __name__ == "__main__":
    main()
