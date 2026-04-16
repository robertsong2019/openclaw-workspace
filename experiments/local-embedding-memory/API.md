# API Reference - Local Embedding Memory Searcher

> Complete API documentation for the semantic memory search library

## Table of Contents

- [Core Classes](#core-classes)
  - [MemoryEmbedder](#memoryembedder)
  - [MemoryIndex](#memoryindex)
  - [SearchResult](#searchresult)
- [Command-Line Interface](#command-line-interface)
- [Web API](#web-api)
- [Data Structures](#data-structures)

---

## Core Classes

### MemoryEmbedder

The main class for indexing and searching memory files.

#### Constructor

```python
from memory_embedder import MemoryEmbedder

embedder = MemoryEmbedder(
    memory_dir="../memory",          # Path to memory directory
    model_name="all-MiniLM-L6-v2",   # Embedding model
    index_file=".embedding_index.json"  # Index file path
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `memory_dir` | str | `"../memory"` | Directory containing MEMORY.md and daily files |
| `model_name` | str | `"all-MiniLM-L6-v2"` | Sentence-transformers model name |
| `index_file` | str | `".embedding_index.json"` | Path to store/load index |

---

#### Methods

##### `build_index(incremental=True)`

Build or update the embedding index.

```python
# Incremental index (only changed files)
embedder.build_index(incremental=True)

# Full reindex
embedder.build_index(incremental=False)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `incremental` | bool | `True` | If True, only reindex modified files |

**Returns:**

- `dict`: Statistics about the indexing process

```python
{
    "total_files": 10,
    "indexed_files": 3,
    "skipped_files": 7,
    "total_chunks": 45,
    "new_chunks": 12,
    "indexing_time": 2.34
}
```

**Example:**

```python
embedder = MemoryEmbedder(memory_dir="../memory")

# First time indexing
stats = embedder.build_index(incremental=False)
print(f"Indexed {stats['total_chunks']} chunks from {stats['total_files']} files")

# Later, after updating some files
stats = embedder.build_index(incremental=True)
print(f"Updated {stats['indexed_files']} files, skipped {stats['skipped_files']}")
```

---

##### `search(query, top_k=5)`

Perform semantic search on indexed memories.

```python
results = embedder.search(
    query="AI Agent memory patterns",
    top_k=5
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | str | *required* | Search query |
| `top_k` | int | `5` | Number of results to return |

**Returns:**

- `List[SearchResult]`: List of search results (see [SearchResult](#searchresult))

**Example:**

```python
results = embedder.search("interesting AI projects", top_k=3)

for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"File: {result.file_path}")
    print(f"Section: {result.section}")
    print(f"Preview: {result.content[:100]}...")
    print()
```

---

##### `text_search(query, top_k=5)`

Perform simple text-based search (for comparison).

```python
results = embedder.text_search(
    query="AI Agent",
    top_k=5
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | str | *required* | Search query |
| `top_k` | int | `5` | Number of results to return |

**Returns:**

- `List[SearchResult]`: List of search results

**Difference from `search()`:**

- Uses TF-IDF text matching instead of semantic embeddings
- Faster but less intelligent
- Good for finding exact keyword matches

---

##### `compare_search(query, top_k=5)`

Compare semantic vs text search side-by-side.

```python
comparison = embedder.compare_search(
    query="AI Agent memory",
    top_k=5
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | str | *required* | Search query |
| `top_k` | int | `5` | Number of results per method |

**Returns:**

- `dict`: Comparison results

```python
{
    "query": "AI Agent memory",
    "semantic": [SearchResult, ...],
    "text": [SearchResult, ...],
    "overlap": 3  # Number of results that appear in both
}
```

**Example:**

```python
comparison = embedder.compare_search("machine learning", top_k=5)

print("🧠 Semantic Search:")
for result in comparison["semantic"][:3]:
    print(f"  - {result.file_path}: {result.section}")

print("\n📄 Text Search:")
for result in comparison["text"][:3]:
    print(f"  - {result.file_path}: {result.section}")

print(f"\nOverlap: {comparison['overlap']} results match")
```

---

##### `load_index()` / `save_index()`

Manually load or save the index.

```python
# Load existing index
index = embedder.load_index()
print(f"Loaded {len(index.chunks)} chunks")

# Save index (usually done automatically)
embedder.save_index()
```

**Note:** `build_index()` automatically saves the index. These methods are for manual control.

---

### MemoryIndex

Data structure representing the embedding index.

```python
@dataclass
class MemoryIndex:
    chunks: List[MemoryChunk]      # All indexed chunks
    embeddings: np.ndarray         # Embedding vectors (N x 384)
    file_hashes: Dict[str, str]    # File path -> MD5 hash
    model_name: str                # Model used for embeddings
    created_at: str                # ISO timestamp
    updated_at: str                # ISO timestamp
```

**Usage:**

```python
index = embedder.load_index()

print(f"Total chunks: {len(index.chunks)}")
print(f"Embedding dimensions: {index.embeddings.shape[1]}")
print(f"Last updated: {index.updated_at}")
```

---

### SearchResult

Represents a single search result.

```python
@dataclass
class SearchResult:
    score: float          # Similarity score (0-1)
    file_path: str        # Source file
    section: str          # Section header
    content: str          # Chunk content
    chunk_id: int         # Chunk index
```

**Usage:**

```python
result = embedder.search("AI Agent", top_k=1)[0]

print(f"Score: {result.score:.3f}")      # 0.847
print(f"File: {result.file_path}")       # "MEMORY.md"
print(f"Section: {result.section}")      # "Memory Systems"
print(f"Content: {result.content}")      # Full chunk text
```

---

### MemoryChunk

Represents a single chunk of memory.

```python
@dataclass
class MemoryChunk:
    chunk_id: int         # Unique identifier
    file_path: str        # Source file
    section: str          # Section header
    content: str          # Chunk text
    start_line: int       # Starting line in file
    end_line: int         # Ending line in file
```

---

## Command-Line Interface

### Indexing

```bash
# Incremental index (only changed files)
python memory_embedder.py --index

# Full reindex
python memory_embedder.py --index --force
```

### Searching

```bash
# Semantic search
python memory_embedder.py --search "AI Agent memory patterns"

# Text search
python memory_embedder.py --search "AI Agent" --mode text

# Compare semantic vs text
python memory_embedder.py --compare "machine learning"
```

### Options

| Flag | Description |
|------|-------------|
| `--index` | Build/update the index |
| `--force` | Force full reindex (with `--index`) |
| `--search QUERY` | Search memories |
| `--compare QUERY` | Compare semantic vs text search |
| `--mode MODE` | Search mode: `semantic` (default) or `text` |
| `--top-k N` | Number of results (default: 5) |
| `--memory-dir DIR` | Memory directory path |
| `--model NAME` | Embedding model name |

---

## Web API

### Start Server

```bash
python web_ui.py --port 8080
```

### Endpoints

#### `GET /`

Web UI homepage with search interface.

**Response:** HTML page

---

#### `GET /api/search`

JSON API for search.

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | *required* | Search query |
| `mode` | string | `"semantic"` | Search mode: `semantic`, `text`, or `compare` |
| `top_k` | int | `5` | Number of results |

**Example Request:**

```bash
curl "http://localhost:8080/api/search?q=AI+Agent&mode=semantic&top_k=5"
```

**Response:**

```json
{
  "query": "AI Agent",
  "mode": "semantic",
  "results": [
    {
      "score": 0.847,
      "file_path": "MEMORY.md",
      "section": "Memory Systems",
      "content": "AI Agents need persistent memory...",
      "chunk_id": 12
    },
    ...
  ]
}
```

**Example: Compare Mode**

```bash
curl "http://localhost:8080/api/search?q=machine+learning&mode=compare&top_k=3"
```

```json
{
  "query": "machine learning",
  "mode": "compare",
  "semantic": [...],
  "text": [...],
  "overlap": 2
}
```

---

## Data Structures

### Index File Format

The `.embedding_index.json` file stores:

```json
{
  "chunks": [
    {
      "chunk_id": 0,
      "file_path": "MEMORY.md",
      "section": "Memory Systems",
      "content": "AI Agents need persistent memory...",
      "start_line": 45,
      "end_line": 67
    }
  ],
  "embeddings": [[0.123, 0.456, ...], ...],
  "file_hashes": {
    "MEMORY.md": "a1b2c3d4e5f6...",
    "memory/2026-03-21.md": "f6e5d4c3b2a1..."
  },
  "model_name": "all-MiniLM-L6-v2",
  "created_at": "2026-03-22T00:00:00Z",
  "updated_at": "2026-03-22T01:00:00Z"
}
```

**Notes:**

- `embeddings` is a 2D array (N x 384 for all-MiniLM-L6-v2)
- `file_hashes` enables incremental indexing
- Index file can be version controlled (but add to `.gitignore` for large indexes)

---

## Advanced Usage

### Custom Chunking

```python
from memory_embedder import MemoryEmbedder, ChunkConfig

config = ChunkConfig(
    min_chunk_size=100,    # Minimum characters per chunk
    max_chunk_size=1000,   # Maximum characters per chunk
    overlap_sentences=2    # Sentence overlap between chunks
)

embedder = MemoryEmbedder(
    memory_dir="../memory",
    chunk_config=config
)
```

### Custom Similarity Metric

```python
from scipy.spatial.distance import cosine, euclidean

# Default: cosine similarity
results = embedder.search("query")

# Custom: euclidean distance
embedder.distance_metric = "euclidean"
results = embedder.search("query")
```

### Batch Search

```python
queries = [
    "AI Agent patterns",
    "memory systems",
    "edge computing"
]

results = embedder.batch_search(queries, top_k=3)

for query, query_results in zip(queries, results):
    print(f"\nQuery: {query}")
    for result in query_results:
        print(f"  - {result.file_path}: {result.score:.3f}")
```

### Export to Memori Format

```python
# Export index for Memori integration
embedder.export_to_memori(output_dir="./memori_export")

# Creates:
# memori_export/
# ├── schema.sql
# ├── chunks.csv
# └── embeddings.npy
```

---

## Error Handling

```python
from memory_embedder import MemoryEmbedder, IndexNotFoundError

try:
    embedder = MemoryEmbedder(memory_dir="../memory")
    results = embedder.search("query")
except IndexNotFoundError:
    print("Index not found. Run with --index first.")
except Exception as e:
    print(f"Error: {e}")
```

---

## Performance

### Benchmarks

**Indexing (all-MiniLM-L6-v2 on CPU):**

| Files | Chunks | Time | Index Size |
|-------|--------|------|------------|
| 10 | 50 | 2s | 150KB |
| 50 | 250 | 10s | 750KB |
| 100 | 500 | 20s | 1.5MB |
| 500 | 2500 | 100s | 7.5MB |

**Incremental Indexing (1 file changed):**

| Total Files | Time | Speedup |
|-------------|------|---------|
| 10 | 0.2s | 10x |
| 50 | 0.2s | 50x |
| 100 | 0.2s | 100x |

**Search (single query):**

| Chunks | Time |
|--------|------|
| 50 | 5ms |
| 250 | 10ms |
| 500 | 20ms |
| 2500 | 50ms |

### Memory Usage

- Model: ~80MB (all-MiniLM-L6-v2)
- Index (500 chunks): ~1.5MB
- Peak RAM: ~100MB

---

## Troubleshooting

### Model Download Issues

If model download fails:

```python
# Option 1: Use offline model
embedder = MemoryEmbedder(model_name="/path/to/local/model")

# Option 2: Download manually
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
model.save("/path/to/local/model")
```

### Slow Indexing

- Use smaller model: `paraphrase-MiniLM-L3-v2` (60MB)
- Reduce chunk size
- Use incremental indexing

### Poor Search Results

- Try different models
- Increase `top_k`
- Use compare mode to debug
- Check chunk boundaries

---

## Version History

- **v1.1.0** (2026-03-22): Added incremental indexing and Web UI
- **v1.0.0** (2026-03-20): Initial release with semantic search

---

**Next:** [TUTORIAL.md](TUTORIAL.md) - Step-by-step guide with examples

**Questions?** Open an issue or check the [README](README.md)
