#!/usr/bin/env python3
"""
Local Embedding Memory Searcher
===============================

An experimental tool for semantic memory search using local embeddings.
Inspired by Memori's SQL Native Memory Layer, but designed for Markdown-based memory systems.

Features:
- Uses sentence-transformers for local embeddings (no API calls!)
- Chunks memory files into semantic units
- Provides semantic search with relevance scores
- Compares semantic vs text search results

Usage:
    python memory_embedder.py --index    # Index all memory files
    python memory_embedder.py --search "query"  # Search memories
    python memory_embedder.py --compare "query" # Compare semantic vs text search
"""

import os
import json
import hashlib
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

# Try to import optional dependencies
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️  sentence-transformers not installed. Install with:")
    print("   pip install sentence-transformers numpy")


@dataclass
class MemoryChunk:
    """A semantic chunk of memory"""
    id: str
    source: str
    content: str
    embedding: Optional[list] = None
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source": self.source,
            "content": self.content,
            "embedding": self.embedding,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MemoryChunk":
        return cls(
            id=data["id"],
            source=data["source"],
            content=data["content"],
            embedding=data.get("embedding"),
            metadata=data.get("metadata", {})
        )


class MemoryChunker:
    """Splits memory files into semantic chunks"""
    
    def __init__(self, max_chunk_size: int = 500, overlap: int = 50):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def chunk_file(self, filepath: Path) -> list[MemoryChunk]:
        """Split a markdown file into semantic chunks"""
        content = filepath.read_text(encoding="utf-8")
        chunks = []
        
        # Split by headers first (## or ###)
        sections = self._split_by_headers(content)
        
        for i, section in enumerate(sections):
            # If section is small enough, keep as-is
            if len(section["content"]) <= self.max_chunk_size:
                chunk_id = self._generate_id(filepath.name, i, section["content"])
                chunks.append(MemoryChunk(
                    id=chunk_id,
                    source=str(filepath),
                    content=section["content"].strip(),
                    metadata={
                        "header": section.get("header", ""),
                        "level": section.get("level", 0),
                        "position": i
                    }
                ))
            else:
                # Split large sections by paragraphs with overlap
                sub_chunks = self._split_by_paragraphs(
                    section["content"], 
                    section.get("header", "")
                )
                for j, sub in enumerate(sub_chunks):
                    chunk_id = self._generate_id(filepath.name, f"{i}_{j}", sub)
                    chunks.append(MemoryChunk(
                        id=chunk_id,
                        source=str(filepath),
                        content=sub.strip(),
                        metadata={
                            "header": section.get("header", ""),
                            "level": section.get("level", 0),
                            "position": i,
                            "sub_position": j
                        }
                    ))
        
        return chunks
    
    def _split_by_headers(self, content: str) -> list[dict]:
        """Split content by markdown headers"""
        lines = content.split("\n")
        sections = []
        current = {"content": "", "header": "", "level": 0}
        
        for line in lines:
            # Check for headers
            if line.startswith("### "):
                if current["content"].strip():
                    sections.append(current)
                current = {"content": line + "\n", "header": line[4:].strip(), "level": 3}
            elif line.startswith("## "):
                if current["content"].strip():
                    sections.append(current)
                current = {"content": line + "\n", "header": line[3:].strip(), "level": 2}
            elif line.startswith("# "):
                if current["content"].strip():
                    sections.append(current)
                current = {"content": line + "\n", "header": line[2:].strip(), "level": 1}
            else:
                current["content"] += line + "\n"
        
        if current["content"].strip():
            sections.append(current)
        
        return sections
    
    def _split_by_paragraphs(self, content: str, header: str) -> list[str]:
        """Split content by paragraphs with overlap"""
        paragraphs = content.split("\n\n")
        chunks = []
        current = ""
        
        for para in paragraphs:
            if len(current) + len(para) <= self.max_chunk_size:
                current += para + "\n\n"
            else:
                if current.strip():
                    chunks.append(current.strip())
                current = para + "\n\n"
        
        if current.strip():
            chunks.append(current.strip())
        
        return chunks
    
    def _generate_id(self, filename: str, position, content: str) -> str:
        """Generate a unique ID for a chunk"""
        hash_input = f"{filename}:{position}:{content[:100]}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]


class LocalEmbeddingEngine:
    """Local embedding engine using sentence-transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize with a lightweight model.
        
        Models (sorted by size/speed):
        - all-MiniLM-L6-v2: Fast, good quality (80MB)
        - all-MiniLM-L12-v2: Better quality, slower (120MB)
        - paraphrase-MiniLM-L3-v2: Fastest, lower quality (60MB)
        """
        if not EMBEDDINGS_AVAILABLE:
            raise RuntimeError("sentence-transformers not installed")
        
        print(f"🔄 Loading model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        print(f"✅ Model loaded! Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
    
    def embed(self, texts: list[str]) -> np.ndarray:
        """Generate embeddings for a list of texts"""
        return self.model.encode(texts, show_progress_bar=len(texts) > 10)
    
    def embed_single(self, text: str) -> np.ndarray:
        """Generate embedding for a single text"""
        return self.model.encode(text)
    
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings"""
        return np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )


class MemoryIndex:
    """Index for storing and searching memory embeddings"""
    
    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.chunks: list[MemoryChunk] = []
        self.embeddings: Optional[np.ndarray] = None
        self.model_name: str = ""
        self.file_hashes: dict[str, str] = {}  # filepath -> content hash for incremental indexing
    
    def load(self) -> bool:
        """Load index from disk"""
        if not self.index_path.exists():
            return False
        
        data = json.loads(self.index_path.read_text())
        self.chunks = [MemoryChunk.from_dict(c) for c in data["chunks"]]
        self.model_name = data.get("model_name", "")
        self.file_hashes = data.get("file_hashes", {})
        
        if self.chunks and self.chunks[0].embedding:
            self.embeddings = np.array([c.embedding for c in self.chunks])
        
        print(f"📖 Loaded {len(self.chunks)} chunks from index")
        return True
    
    def save(self, model_name: str):
        """Save index to disk"""
        data = {
            "chunks": [c.to_dict() for c in self.chunks],
            "model_name": model_name,
            "indexed_at": datetime.now().isoformat(),
            "file_hashes": self.file_hashes
        }
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(data, indent=2))
        print(f"💾 Saved index to {self.index_path}")
    
    def add_chunks(self, chunks: list[MemoryChunk], embeddings: np.ndarray):
        """Add chunks with their embeddings"""
        for i, chunk in enumerate(chunks):
            chunk.embedding = embeddings[i].tolist()
        self.chunks.extend(chunks)
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> list[tuple[MemoryChunk, float]]:
        """Search for similar chunks"""
        if self.embeddings is None:
            return []
        
        # Calculate similarities
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top-k
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append((self.chunks[idx], float(similarities[idx])))
        
        return results


class LocalMemorySearcher:
    """Main class for local memory search"""
    
    def __init__(
        self,
        memory_dir: Path,
        index_path: Optional[Path] = None,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        self.memory_dir = Path(memory_dir)
        self.index_path = index_path or self.memory_dir / ".embedding_index.json"
        self.model_name = model_name
        
        self.chunker = MemoryChunker()
        self.index = MemoryIndex(self.index_path)
        self.engine: Optional[LocalEmbeddingEngine] = None
    
    def _init_engine(self):
        """Initialize embedding engine (lazy loading)"""
        if self.engine is None:
            self.engine = LocalEmbeddingEngine(self.model_name)
        return self.engine
    
    def index_memories(self, force: bool = False):
        """Index all memory files with incremental support"""
        # Load existing index
        existing_index = self.index.load()
        
        if not force and existing_index and self.index.model_name == self.model_name:
            # Check for incremental updates
            return self._incremental_index()
        elif existing_index and self.index.model_name != self.model_name:
            print(f"⚠️  Model changed from {self.index.model_name} to {self.model_name}")
        
        # Full reindex
        self._full_reindex()
    
    def _compute_file_hash(self, filepath: Path) -> str:
        """Compute hash of file content for change detection"""
        content = filepath.read_text(encoding="utf-8")
        return hashlib.md5(content.encode()).hexdigest()
    
    def _incremental_index(self):
        """Incrementally index only changed files"""
        # Find all memory files
        memory_files = list(self.memory_dir.glob("MEMORY.md"))
        memory_files.extend(self.memory_dir.glob("memory/*.md"))
        
        if not memory_files:
            print("❌ No memory files found!")
            return
        
        # Check which files need reindexing
        files_to_index = []
        unchanged_files = []
        
        for filepath in memory_files:
            current_hash = self._compute_file_hash(filepath)
            stored_hash = self.index.file_hashes.get(str(filepath))
            
            if stored_hash != current_hash:
                files_to_index.append(filepath)
            else:
                unchanged_files.append(filepath)
        
        if not files_to_index:
            print("✅ All files up to date. No changes detected.")
            return
        
        print(f"📚 Found {len(memory_files)} memory files:")
        print(f"   📝 {len(files_to_index)} files need reindexing")
        print(f"   ✅ {len(unchanged_files)} files unchanged")
        
        # Remove chunks from changed files
        changed_sources = {str(f) for f in files_to_index}
        self.index.chunks = [c for c in self.index.chunks if c.source not in changed_sources]
        
        # Chunk changed files
        new_chunks = []
        for filepath in files_to_index:
            chunks = self.chunker.chunk_file(filepath)
            new_chunks.extend(chunks)
            print(f"   📄 {filepath.name}: {len(chunks)} chunks")
        
        print(f"\n📊 New chunks to index: {len(new_chunks)}")
        
        if new_chunks:
            # Generate embeddings for new chunks only
            engine = self._init_engine()
            print("\n🔄 Generating embeddings for new chunks...")
            texts = [c.content for c in new_chunks]
            embeddings = engine.embed(texts)
            
            # Add to index
            self.index.add_chunks(new_chunks, embeddings)
            
            # Update embeddings array
            if self.index.chunks:
                all_embeddings = [c.embedding for c in self.index.chunks]
                self.index.embeddings = np.array(all_embeddings)
        
        # Update file hashes
        for filepath in files_to_index:
            self.index.file_hashes[str(filepath)] = self._compute_file_hash(filepath)
        
        # Save
        self.index.save(self.model_name)
        print(f"\n✅ Incremental indexing complete! {len(new_chunks)} new chunks indexed.")
        print(f"📊 Total chunks: {len(self.index.chunks)}")
    
    def _full_reindex(self):
        """Perform a full reindex of all files"""
        # Find all memory files
        memory_files = list(self.memory_dir.glob("MEMORY.md"))
        memory_files.extend(self.memory_dir.glob("memory/*.md"))
        
        if not memory_files:
            print("❌ No memory files found!")
            return
        
        print(f"📚 Found {len(memory_files)} memory files:")
        for f in memory_files:
            print(f"   - {f}")
        
        # Chunk all files
        all_chunks = []
        for filepath in memory_files:
            chunks = self.chunker.chunk_file(filepath)
            all_chunks.extend(chunks)
            print(f"   📄 {filepath.name}: {len(chunks)} chunks")
        
        print(f"\n📊 Total chunks: {len(all_chunks)}")
        
        # Generate embeddings
        engine = self._init_engine()
        print("\n🔄 Generating embeddings...")
        texts = [c.content for c in all_chunks]
        embeddings = engine.embed(texts)
        
        # Add to index
        self.index.chunks = []  # Clear existing
        self.index.file_hashes = {}  # Clear hashes
        self.index.add_chunks(all_chunks, embeddings)
        self.index.embeddings = embeddings
        
        # Update file hashes
        for filepath in memory_files:
            self.index.file_hashes[str(filepath)] = self._compute_file_hash(filepath)
        
        # Save
        self.index.save(self.model_name)
        print(f"\n✅ Indexing complete! {len(all_chunks)} chunks indexed.")
    
    def search(self, query: str, top_k: int = 5) -> list[tuple[MemoryChunk, float]]:
        """Search memories semantically"""
        if not self.index.load():
            print("❌ No index found. Run with --index first.")
            return []
        
        engine = self._init_engine()
        query_embedding = engine.embed_single(query)
        
        return self.index.search(query_embedding, top_k)
    
    def text_search(self, query: str, top_k: int = 5) -> list[tuple[MemoryChunk, float]]:
        """Simple text-based search (for comparison)"""
        if not self.index.load():
            return []
        
        query_lower = query.lower()
        results = []
        
        for chunk in self.index.chunks:
            # Simple TF scoring
            content_lower = chunk.content.lower()
            score = 0
            for word in query_lower.split():
                score += content_lower.count(word)
            
            if score > 0:
                # Normalize by content length
                score = score / (len(chunk.content) / 100)
                results.append((chunk, score))
        
        # Sort and return top-k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def compare_search(self, query: str, top_k: int = 5):
        """Compare semantic vs text search"""
        print(f"\n🔍 Query: '{query}'")
        print("=" * 60)
        
        # Semantic search
        print("\n🧠 Semantic Search Results:")
        print("-" * 40)
        semantic_results = self.search(query, top_k)
        for i, (chunk, score) in enumerate(semantic_results, 1):
            print(f"\n{i}. [{score:.3f}] {chunk.source}")
            if chunk.metadata.get("header"):
                print(f"   Section: {chunk.metadata['header']}")
            preview = chunk.content[:200].replace("\n", " ")
            print(f"   {preview}...")
        
        # Text search
        print("\n\n📝 Text Search Results:")
        print("-" * 40)
        text_results = self.text_search(query, top_k)
        for i, (chunk, score) in enumerate(text_results, 1):
            print(f"\n{i}. [{score:.3f}] {chunk.source}")
            if chunk.metadata.get("header"):
                print(f"   Section: {chunk.metadata['header']}")
            preview = chunk.content[:200].replace("\n", " ")
            print(f"   {preview}...")
        
        # Analysis
        print("\n\n📊 Comparison Analysis:")
        print("-" * 40)
        semantic_sources = {c.source for c, _ in semantic_results}
        text_sources = {c.source for c, _ in text_results}
        
        overlap = semantic_sources & text_sources
        unique_semantic = semantic_sources - text_sources
        unique_text = text_sources - semantic_sources
        
        print(f"Overlapping sources: {len(overlap)}")
        print(f"Unique to semantic: {len(unique_semantic)}")
        print(f"Unique to text: {len(unique_text)}")
        
        if unique_semantic:
            print(f"\n✨ Semantic search found unique results from:")
            for s in unique_semantic:
                print(f"   - {s}")


def main():
    parser = argparse.ArgumentParser(
        description="Local Embedding Memory Searcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Index all memory files
  python memory_embedder.py --index
  
  # Force reindex
  python memory_embedder.py --index --force
  
  # Search memories
  python memory_embedder.py --search "AI Agent architecture"
  
  # Compare semantic vs text search
  python memory_embedder.py --compare "memory system design"
        """
    )
    
    parser.add_argument("--index", action="store_true", help="Index memory files")
    parser.add_argument("--force", action="store_true", help="Force reindex")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--compare", type=str, help="Compare semantic vs text search")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    parser.add_argument(
        "--memory-dir", 
        type=str, 
        default="/root/.openclaw/workspace",
        help="Memory directory path"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="all-MiniLM-L6-v2",
        help="Embedding model name"
    )
    
    args = parser.parse_args()
    
    searcher = LocalMemorySearcher(
        memory_dir=Path(args.memory_dir),
        model_name=args.model
    )
    
    if args.index:
        searcher.index_memories(force=args.force)
    elif args.search:
        results = searcher.search(args.search, args.top_k)
        print(f"\n🔍 Results for: '{args.search}'")
        print("=" * 60)
        for i, (chunk, score) in enumerate(results, 1):
            print(f"\n{i}. [{score:.3f}] {chunk.source}")
            if chunk.metadata.get("header"):
                print(f"   Section: {chunk.metadata['header']}")
            print(f"   {chunk.content[:300]}...")
    elif args.compare:
        searcher.compare_search(args.compare, args.top_k)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
