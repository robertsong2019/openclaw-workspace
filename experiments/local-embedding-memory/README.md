# Local Embedding Memory Searcher

> 🧠 Semantic search for your MEMORY.md files using local embeddings

## What is this?

An experimental tool that brings **semantic search** to Markdown-based memory systems (like OpenClaw's MEMORY.md pattern). Instead of simple keyword matching, it understands the **meaning** of your queries.

### Why?

- **Better search**: Find relevant memories even without exact keyword matches
- **No API calls**: Uses local embeddings (sentence-transformers) - completely offline
- **Fast**: Lightweight model (80MB) runs on CPU
- **Compare**: See how semantic search differs from text search

## Installation

```bash
pip install sentence-transformers numpy
```

## Quick Start

```bash
# Index your memories
python memory_embedder.py --index

# Incremental index (only changed files)
python memory_embedder.py --index

# Search
python memory_embedder.py --search "AI Agent memory patterns"

# Compare semantic vs text search
python memory_embedder.py --compare "interesting projects"

# Interactive demo
python interactive_demo.py

# Web UI
python web_ui.py --port 8080
```

## How it works

1. **Chunking**: Splits MEMORY.md and memory/*.md into semantic chunks
2. **Embedding**: Generates vector embeddings using sentence-transformers
3. **Indexing**: Stores embeddings in a local JSON index
4. **Search**: Finds similar chunks using cosine similarity

## Example Output

```
🔍 Query: 'AI Agent memory architecture'
============================================================

🧠 Semantic Search Results:
----------------------------------------

1. [0.847] MEMORY.md
   Section: Memory Systems
   💬 AI Agents need persistent memory to maintain context across sessions...
   
2. [0.823] memory/2026-03-21.md
   Section: Memori - SQL Native Memory Layer
   💬 Memori uses SQL as a memory layer for AI, providing automatic enhancement...

3. [0.801] MEMORY.md
   Section: Lessons Learned
   💬 Structured memory beats raw context - 67% cost reduction vs full context...
```

## Architecture

```
memory/
├── MEMORY.md              # Main memory file
├── 2026-03-21.md          # Daily notes
├── 2026-03-20.md
└── .embedding_index.json  # Generated index (with file hashes)

experiments/local-embedding-memory/
├── memory_embedder.py     # Core library (with incremental indexing)
├── interactive_demo.py    # Interactive CLI
├── web_ui.py              # Web interface ✨ NEW
└── README.md
```

## Key Features

### Incremental Indexing

- Only reindexes files that have changed
- Uses content hashes for change detection
- Saves time and resources on large memory sets
- Preserves existing embeddings for unchanged files

### Semantic Chunking

- Splits by headers (##, ###)
- Respects content boundaries
- Maintains context with overlap

### Multiple Search Modes

1. **Semantic Search**: Understands meaning
2. **Text Search**: Simple keyword matching
3. **Compare Mode**: Side-by-side comparison

### Web UI

```bash
# Start the web server
python web_ui.py --port 8080

# Then open http://localhost:8080 in your browser
```

Features:
- Clean, modern dark theme
- Real-time semantic search
- Side-by-side comparison mode
- REST API endpoint at `/api/search`

### Model Options

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| all-MiniLM-L6-v2 | 80MB | ⚡⚡⚡ | ⭐⭐⭐ |
| all-MiniLM-L12-v2 | 120MB | ⚡⚡ | ⭐⭐⭐⭐ |
| paraphrase-MiniLM-L3-v2 | 60MB | ⚡⚡⚡⚡ | ⭐⭐ |

## Use Cases

- **Personal Knowledge Management**: Search your notes semantically
- **AI Agent Memory**: Enhance agent memory retrieval
- **Research Notes**: Find related concepts across files
- **Journaling**: Discover connections in daily entries

## Comparison with Memori

| Feature | Local Embedding Memory | Memori |
|---------|------------------------|--------|
| Storage | JSON file | SQL database |
| Setup | Zero config | Requires setup |
| API | None | Optional |
| Multi-tenant | No | Yes |
| Auto-enhancement | No | Yes |
| OpenClaw plugin | No | Yes |

## Future Ideas

- [x] Add incremental indexing ✅
- [ ] Support more embedding models
- [ ] Add clustering to find themes
- [ ] Export to Memori format
- [x] Web UI for exploration ✅

## Inspiration

- [Memori](https://github.com/MemoriLabs/Memori) - SQL Native Memory Layer
- [sentence-transformers](https://www.sbert.net/) - Embedding models
- OpenClaw's MEMORY.md pattern

---

*Part of the Code Lab experiments series - exploring AI Agent tools and embedded AI.*
