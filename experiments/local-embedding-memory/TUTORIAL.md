# Tutorial - Local Embedding Memory Searcher

> From zero to semantic search in 10 minutes

## Table of Contents

- [Introduction](#introduction)
- [Part 1: Quick Start](#part-1-quick-start-5-minutes)
- [Part 2: Understanding Semantic Search](#part-2-understanding-semantic-search)
- [Part 3: Advanced Features](#part-3-advanced-features)
- [Part 4: Real-World Use Cases](#part-4-real-world-use-cases)
- [Part 5: Integration](#part-5-integration)
- [Troubleshooting](#troubleshooting)

---

## Introduction

### What is Local Embedding Memory Searcher?

It's a tool that brings **semantic search** to your Markdown notes. Unlike traditional search that matches exact keywords, semantic search understands the **meaning** of your query.

**Example:**

- **Query:** "How do I handle AI memory?"
- **Traditional search:** Looks for "handle", "AI", "memory" keywords
- **Semantic search:** Finds sections about "persistent storage", "context management", "memory patterns" - even if those exact words aren't in the query

### Why Local?

- ✅ **No API calls** - runs completely offline
- ✅ **No subscription** - free forever
- ✅ **Privacy** - your data stays on your machine
- ✅ **Fast** - milliseconds, not seconds
- ✅ **Lightweight** - 80MB model runs on CPU

### What You'll Learn

By the end of this tutorial, you'll know how to:

1. Set up semantic search for your notes
2. Index and search your memories
3. Use incremental indexing for efficiency
4. Integrate with your workflow
5. Understand how embeddings work

---

## Part 1: Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
# Clone or navigate to the project
cd experiments/local-embedding-memory

# Install required packages
pip install sentence-transformers numpy
```

**What gets installed:**

- `sentence-transformers`: Embedding model library
- `numpy`: Vector math operations

### Step 2: Prepare Your Memory Files

The tool expects a `memory/` directory with Markdown files:

```
your-project/
├── memory/
│   ├── MEMORY.md           # Main memory file
│   ├── 2026-03-21.md       # Daily notes
│   ├── 2026-03-20.md
│   └── ...
└── experiments/
    └── local-embedding-memory/
        ├── memory_embedder.py
        ├── interactive_demo.py
        └── web_ui.py
```

**Don't have memory files?** Create a sample:

```bash
mkdir -p ../memory
cat > ../memory/MEMORY.md << 'EOF'
# MEMORY.md

## AI Agents

AI Agents are autonomous systems that can perceive, reason, and act.

### Key Components
- **Perception**: Understanding the environment
- **Reasoning**: Making decisions
- **Action**: Executing tasks

## Memory Systems

Memory is crucial for AI Agents. Without it, they forget everything after each session.

### Types of Memory
- **Episodic**: Events and experiences
- **Semantic**: Facts and concepts
- **Procedural**: Skills and procedures

## Projects

### agent-role-orchestrator
Multi-agent orchestration with role-based patterns.

### holographic-memory-viz
3D visualization of memory embeddings.
EOF
```

### Step 3: Index Your Memories

```bash
# First-time indexing
python memory_embedder.py --index
```

**What happens:**

1. Reads all `.md` files in `../memory/`
2. Splits content into semantic chunks
3. Generates embeddings (vectors) for each chunk
4. Saves index to `.embedding_index.json`

**Output:**

```
🧠 Indexing memories...
📂 Found 4 Markdown files
✂️  Created 12 chunks
🔢 Generated embeddings (all-MiniLM-L6-v2)
💾 Saved index to .embedding_index.json
⏱️  Time: 2.34 seconds
```

### Step 4: Search Your Memories

```bash
# Semantic search
python memory_embedder.py --search "autonomous AI systems"

# Text search (for comparison)
python memory_embedder.py --search "autonomous AI systems" --mode text

# Compare both
python memory_embedder.py --compare "autonomous AI systems"
```

**Example Output:**

```
🔍 Query: 'autonomous AI systems'
============================================================

🧠 Semantic Search Results:
----------------------------------------

1. [0.891] MEMORY.md
   Section: AI Agents
   💬 AI Agents are autonomous systems that can perceive, reason, and act...
   
2. [0.823] MEMORY.md
   Section: Memory Systems
   💬 Memory is crucial for AI Agents. Without it, they forget everything...

3. [0.756] MEMORY.md
   Section: Projects
   💬 Multi-agent orchestration with role-based patterns...
```

**🎉 Congratulations!** You've just performed semantic search on your notes.

---

## Part 2: Understanding Semantic Search

### How Embeddings Work

**Embeddings** are numerical representations of text that capture meaning.

```
Text: "AI Agents are autonomous systems"
      ↓
Embedding: [0.123, -0.456, 0.789, ..., 0.234]  (384 dimensions)
```

**Key insight:** Similar concepts have similar embeddings.

```python
# Conceptual example
"dog"     → [0.9, 0.1, 0.3]
"puppy"   → [0.85, 0.15, 0.35]  # Very similar!
"cat"     → [0.2, 0.8, 0.5]      # Less similar
"computer" → [0.1, 0.2, 0.9]     # Not similar
```

### Semantic vs Text Search

Let's see the difference with an example:

**Your memory contains:**

```markdown
## Machine Learning
I've been exploring neural networks for pattern recognition.
```

**Query:** "artificial intelligence algorithms"

**Text Search Result:**

```
❌ No results found
Reason: Doesn't contain "artificial intelligence" or "algorithms"
```

**Semantic Search Result:**

```
✅ Found: Machine Learning section
Reason: "machine learning", "neural networks", "pattern recognition"
        are semantically related to "artificial intelligence algorithms"
```

### Try It Yourself

```bash
# Query that uses different words
python memory_embedder.py --search "storing information for later use"

# This will find sections about "memory", "storage", "persistence"
# even if those exact words aren't in the query
```

### Chunking Strategy

The tool splits your files into **semantic chunks**:

```markdown
## Section A
Content about topic A...

### Subsection A.1
More details about A...

## Section B
Content about topic B...
```

Becomes:

```
Chunk 1: "Section A\nContent about topic A..."
Chunk 2: "Subsection A.1\nMore details about A..."
Chunk 3: "Section B\nContent about topic B..."
```

**Why?** Smaller chunks = more precise search results.

---

## Part 3: Advanced Features

### Feature 1: Incremental Indexing

When you update your memory files, you don't need to reindex everything.

```bash
# Edit a file
echo "New content" >> ../memory/MEMORY.md

# Incremental index (only reindexes changed files)
python memory_embedder.py --index
```

**Output:**

```
🧠 Checking for changes...
📝 Modified: MEMORY.md
✅ Unchanged: 2026-03-21.md, 2026-03-20.md
⚡ Indexed 1 file, skipped 3 files
⏱️  Time: 0.21 seconds (vs 2.34 seconds for full reindex)
```

**How it works:**

1. Computes MD5 hash of each file
2. Compares with hashes stored in index
3. Only reindexes files with different hashes
4. Preserves embeddings for unchanged files

**When to use full reindex:**

```bash
# Change embedding model
python memory_embedder.py --index --force

# Corrupted index
python memory_embedder.py --index --force

# Major file restructuring
python memory_embedder.py --index --force
```

### Feature 2: Web UI

Launch a web interface for exploring your memories:

```bash
# Start web server
python web_ui.py --port 8080
```

**Then open:** http://localhost:8080

**Features:**

- 🔍 Real-time semantic search
- 📊 Side-by-side comparison mode
- 🎨 Clean, dark theme
- 📱 Mobile-friendly

**API Access:**

```bash
# Search via API
curl "http://localhost:8080/api/search?q=AI+Agent&top_k=5"

# Response
{
  "query": "AI Agent",
  "results": [
    {
      "score": 0.891,
      "file_path": "MEMORY.md",
      "section": "AI Agents",
      "content": "..."
    }
  ]
}
```

### Feature 3: Interactive Demo

```bash
python interactive_demo.py
```

**Features:**

- Interactive query loop
- Real-time feedback
- Result exploration
- Search history

### Feature 4: Batch Search

Search multiple queries at once:

```python
from memory_embedder import MemoryEmbedder

embedder = MemoryEmbedder(memory_dir="../memory")
embedder.build_index()

queries = [
    "AI memory patterns",
    "project documentation",
    "edge computing"
]

for query in queries:
    results = embedder.search(query, top_k=3)
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    for result in results:
        print(f"  [{result.score:.3f}] {result.file_path}: {result.section}")
```

### Feature 5: Custom Models

Try different embedding models:

```python
# Faster, smaller model
embedder = MemoryEmbedder(
    memory_dir="../memory",
    model_name="paraphrase-MiniLM-L3-v2"  # 60MB
)

# More accurate, larger model
embedder = MemoryEmbedder(
    memory_dir="../memory",
    model_name="all-MiniLM-L12-v2"  # 120MB
)

# Domain-specific model (if you have one)
embedder = MemoryEmbedder(
    memory_dir="../memory",
    model_name="/path/to/your/custom/model"
)
```

**Model comparison:**

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| paraphrase-MiniLM-L3-v2 | 60MB | ⚡⚡⚡⚡ | ⭐⭐ | Quick prototypes |
| all-MiniLM-L6-v2 | 80MB | ⚡⚡⚡ | ⭐⭐⭐ | General use |
| all-MiniLM-L12-v2 | 120MB | ⚡⚡ | ⭐⭐⭐⭐ | Higher accuracy |

**Note:** Changing models requires full reindex.

---

## Part 4: Real-World Use Cases

### Use Case 1: Personal Knowledge Management

**Scenario:** You maintain a personal knowledge base with 100+ Markdown files.

```bash
# Initial setup
python memory_embedder.py --index

# Search across all files
python memory_embedder.py --search "database optimization techniques"

# Daily workflow: update notes, then incremental index
python memory_embedder.py --index  # Fast, only reindexes changed files
```

**Benefits:**

- Find related concepts across files
- Discover connections you forgot
- No more "Where did I write about X?"

### Use Case 2: AI Agent Memory Enhancement

**Scenario:** You're building an AI agent with persistent memory.

```python
from memory_embedder import MemoryEmbedder

class EnhancedAgent:
    def __init__(self):
        self.memory = MemoryEmbedder(memory_dir="./agent_memory")
        self.memory.build_index()
    
    def recall(self, query):
        """Recall relevant memories"""
        results = self.memory.search(query, top_k=5)
        context = "\n".join([r.content for r in results])
        return context
    
    def learn(self, experience):
        """Store new experience"""
        with open("./agent_memory/experiences.md", "a") as f:
            f.write(f"\n\n## {experience['timestamp']}\n{experience['content']}\n")
        
        # Incremental index
        self.memory.build_index()

# Usage
agent = EnhancedAgent()

# Recall relevant context
context = agent.recall("previous API errors")
print(context)

# Learn from new experience
agent.learn({
    "timestamp": "2026-03-22 04:00",
    "content": "Discovered that rate limiting occurs at 100 req/min"
})
```

**Benefits:**

- Agent has persistent, searchable memory
- Incremental updates are fast
- Semantic recall finds related experiences

### Use Case 3: Research Note Organization

**Scenario:** You're a researcher with notes on multiple topics.

```bash
# Index all research notes
python memory_embedder.py --index

# Find related work across topics
python memory_embedder.py --search "optimization algorithms"

# Compare with traditional search to see what you might have missed
python memory_embedder.py --compare "optimization algorithms"
```

**Benefits:**

- Discover related work across different topics
- Find citations you forgot about
- Semantic connections reveal new insights

### Use Case 4: Daily Journal Analysis

**Scenario:** You keep a daily journal and want to find patterns.

```bash
# Structure your journal
journal/
├── 2026-01-01.md
├── 2026-01-02.md
├── ...
└── 2026-03-22.md

# Index all entries
python memory_embedder.py --index

# Find entries about specific themes
python memory_embedder.py --search "productive days"
python memory_embedder.py --search "challenging situations"
python memory_embedder.py --search "learning experiences"
```

**Benefits:**

- Find patterns in your journal
- Recall specific events
- Self-reflection made easier

### Use Case 5: Documentation Search

**Scenario:** You maintain extensive project documentation.

```bash
# Index documentation
python memory_embedder.py --memory-dir ./docs --index

# Developers can search semantically
python memory_embedder.py --search "how to handle errors"
python memory_embedder.py --search "authentication flow"

# Web UI for team access
python web_ui.py --port 8080
```

**Benefits:**

- Developers find answers faster
- No exact keyword needed
- Discovers related documentation

---

## Part 5: Integration

### Integration 1: VS Code Extension

Create a VS Code extension that searches your notes:

```javascript
// extension.js
const { exec } = require('child_process');

function searchMemory(query) {
    return new Promise((resolve) => {
        exec(
            `python /path/to/memory_embedder.py --search "${query}" --top-k 5`,
            (error, stdout) => {
                resolve(stdout);
            }
        );
    });
}

exports.searchMemory = searchMemory;
```

### Integration 2: Obsidian Plugin

If you use Obsidian for note-taking:

```javascript
// main.js
class SemanticSearchPlugin {
    async onload() {
        this.addCommand({
            id: 'semantic-search',
            name: 'Semantic Search',
            callback: () => this.showSearchModal()
        });
    }
    
    async showSearchModal() {
        const query = await this.prompt('Search query:');
        const results = await fetch(`http://localhost:8080/api/search?q=${query}`);
        this.displayResults(results);
    }
}
```

### Integration 3: GitHub Actions

Automatically index and search in CI/CD:

```yaml
# .github/workflows/search-docs.yml
name: Search Documentation

on:
  issue_comment:
    types: [created]

jobs:
  search:
    if: contains(github.event.comment.body, '/search')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install sentence-transformers numpy
      
      - name: Search
        run: |
          QUERY="${{ github.event.comment.body }}"
          QUERY="${QUERY/\/search /}"
          python experiments/local-embedding-memory/memory_embedder.py --search "$QUERY" > results.txt
      
      - name: Comment
        uses: actions/github-script@v5
        with:
          script: |
            const fs = require('fs');
            const results = fs.readFileSync('results.txt', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '```\n' + results + '\n```'
            });
```

### Integration 4: API Server

Deploy as a standalone API server:

```python
# server.py
from flask import Flask, request, jsonify
from memory_embedder import MemoryEmbedder

app = Flask(__name__)
embedder = MemoryEmbedder(memory_dir="../memory")
embedder.build_index()

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    top_k = int(request.args.get('top_k', 5))
    results = embedder.search(query, top_k)
    return jsonify({
        'query': query,
        'results': [
            {
                'score': r.score,
                'file': r.file_path,
                'section': r.section,
                'content': r.content
            }
            for r in results
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Deploy:**

```bash
pip install flask
python server.py
```

**Use:**

```bash
curl "http://localhost:5000/search?q=AI+Agent&top_k=3"
```

---

## Troubleshooting

### Problem 1: "Index not found"

**Error:**

```
❌ Error: Index file not found. Run with --index first.
```

**Solution:**

```bash
python memory_embedder.py --index
```

### Problem 2: Slow indexing

**Cause:** Large files or slow CPU.

**Solutions:**

```bash
# Use smaller model
python memory_embedder.py --model paraphrase-MiniLM-L3-v2 --index --force

# Use incremental indexing
python memory_embedder.py --index  # Only changed files
```

### Problem 3: Poor search results

**Cause:** Wrong model or small dataset.

**Solutions:**

```bash
# Try more accurate model
python memory_embedder.py --model all-MiniLM-L12-v2 --index --force

# Increase top_k
python memory_embedder.py --search "query" --top-k 10

# Use compare mode to debug
python memory_embedder.py --compare "query"
```

### Problem 4: Memory errors

**Cause:** Large index doesn't fit in RAM.

**Solutions:**

- Reduce chunk size
- Use smaller model
- Split into multiple indexes

### Problem 5: Model download fails

**Cause:** Network issues or firewall.

**Solution:**

```python
# Download manually
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
model.save("/local/path/model")

# Use local model
embedder = MemoryEmbedder(model_name="/local/path/model")
```

---

## Best Practices

### 1. Structure Your Memory Files

```markdown
# MEMORY.md

## Topic A
Content about topic A...

### Subtopic A.1
Details about A.1...

## Topic B
Content about topic B...
```

**Why:** Better chunking = better search results.

### 2. Use Incremental Indexing

```bash
# After editing files
python memory_embedder.py --index  # Fast!
```

**Why:** 10-100x faster than full reindex.

### 3. Regular Backups

```bash
# Backup your index
cp .embedding_index.json .embedding_index.backup.json

# Or commit to git
git add .embedding_index.json
git commit -m "Update index"
```

### 4. Experiment with Models

```bash
# Test different models
python memory_embedder.py --model paraphrase-MiniLM-L3-v2 --index --force
python memory_embedder.py --search "test query"

python memory_embedder.py --model all-MiniLM-L12-v2 --index --force
python memory_embedder.py --search "test query"
```

**Why:** Different models work better for different domains.

### 5. Use Web UI for Exploration

```bash
python web_ui.py --port 8080
```

**Why:** Visual exploration helps you understand what's in your memory.

---

## Summary

You've learned:

✅ How to set up semantic search for your notes  
✅ The difference between semantic and text search  
✅ Incremental indexing for efficiency  
✅ Real-world use cases and integrations  
✅ Troubleshooting common issues  

**Next Steps:**

- [ ] Index your own memory files
- [ ] Try different search queries
- [ ] Set up incremental indexing workflow
- [ ] Integrate with your tools (Obsidian, VS Code, etc.)
- [ ] Share your use cases!

---

## Additional Resources

- [API Reference](API.md) - Complete API documentation
- [README](README.md) - Project overview
- [sentence-transformers docs](https://www.sbert.net/) - Embedding models
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent framework

---

**Questions? Feedback?**

Open an issue or reach out! This is an experimental project, and your feedback helps improve it.

---

*Last updated: 2026-03-22*  
*Tutorial version: 1.0*
