#!/usr/bin/env python3
"""
Interactive Memory Explorer
===========================

An interactive CLI for exploring memory embeddings.
Demonstrates the power of semantic search vs traditional text search.

Usage:
    python interactive_demo.py
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from memory_embedder import (
    LocalMemorySearcher,
    MemoryChunk,
    EMBEDDINGS_AVAILABLE
)


def print_header(title: str):
    """Print a styled header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def print_chunk(chunk: MemoryChunk, score: float, index: int, max_len: int = 150):
    """Print a chunk with styling"""
    header = chunk.metadata.get("header", "")
    source = Path(chunk.source).name
    
    print(f"\n{index}. 📄 {source}")
    if header:
        print(f"   📍 Section: {header}")
    print(f"   🎯 Score: {score:.4f}")
    
    # Truncate content nicely
    content = chunk.content.strip()
    if len(content) > max_len:
        content = content[:max_len].rsplit(" ", 1)[0] + "..."
    
    # Highlight first line
    lines = content.split("\n")
    print(f"   💬 {lines[0][:80]}")
    if len(lines) > 1:
        print(f"      {lines[1][:70]}...")


def interactive_search(searcher: LocalMemorySearcher):
    """Interactive search mode"""
    print_header("🔍 Interactive Memory Search")
    print("Type your query and press Enter. Type 'quit' to exit.\n")
    print("Tips:")
    print("  - Use natural language: 'How do I handle memory?")
    print("  - Ask questions: 'What did I learn about AI agents?")
    print("  - Find concepts: 'Edge AI deployment strategies'")
    print()
    
    while True:
        try:
            query = input("\n🔎 Query: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Goodbye!")
            break
        
        if query.lower() in ("quit", "exit", "q"):
            print("👋 Goodbye!")
            break
        
        if not query:
            continue
        
        print("\n🧠 Searching...")
        results = searcher.search(query, top_k=5)
        
        if not results:
            print("❌ No results found. Try a different query.")
            continue
        
        print(f"\n✨ Found {len(results)} results:\n")
        print("-" * 50)
        
        for i, (chunk, score) in enumerate(results, 1):
            print_chunk(chunk, score, i)


def compare_mode(searcher: LocalMemorySearcher):
    """Compare semantic vs text search"""
    print_header("⚖️  Semantic vs Text Search Comparison")
    print("See how semantic understanding differs from keyword matching.\n")
    
    test_queries = [
        "AI Agent memory architecture",
        "how to organize code for agents",
        "Edge AI on Raspberry Pi",
        "mistakes I made in the past",
        "interesting projects I explored"
    ]
    
    print("Try one of these example queries, or type your own:")
    for i, q in enumerate(test_queries, 1):
        print(f"  {i}. {q}")
    print()
    
    while True:
        try:
            query = input("\n🔎 Query (or 'quit'): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Goodbye!")
            break
        
        if query.lower() in ("quit", "exit", "q"):
            break
        
        if not query:
            continue
        
        # Get results
        semantic = searcher.search(query, top_k=3)
        text = searcher.text_search(query, top_k=3)
        
        print("\n" + "=" * 60)
        print("🧠 SEMANTIC SEARCH")
        print("=" * 60)
        if semantic:
            for i, (chunk, score) in enumerate(semantic, 1):
                print_chunk(chunk, score, i, max_len=120)
        else:
            print("No results")
        
        print("\n" + "=" * 60)
        print("📝 TEXT SEARCH (keyword matching)")
        print("=" * 60)
        if text:
            for i, (chunk, score) in enumerate(text, 1):
                print_chunk(chunk, score, i, max_len=120)
        else:
            print("No results")
        
        # Show differences
        semantic_ids = {c.id for c, _ in semantic}
        text_ids = {c.id for c, _ in text}
        overlap = semantic_ids & text_ids
        
        print("\n" + "-" * 60)
        print(f"📊 Overlap: {len(overlap)}/{len(semantic)} results in common")
        if len(overlap) < len(semantic):
            print("✨ Semantic search found unique results!")


def explore_chunks(searcher: LocalMemorySearcher):
    """Explore indexed chunks"""
    print_header("📚 Memory Explorer")
    
    if not searcher.index.load():
        print("❌ No index found. Run --index first.")
        return
    
    chunks = searcher.index.chunks
    
    # Group by source
    sources = {}
    for chunk in chunks:
        source = Path(chunk.source).name
        if source not in sources:
            sources[source] = []
        sources[source].append(chunk)
    
    print(f"📊 Index Statistics:\n")
    print(f"   Total chunks: {len(chunks)}")
    print(f"   Files indexed: {len(sources)}")
    print(f"   Model: {searcher.index.model_name}")
    print()
    
    print("📁 Files:\n")
    for source, file_chunks in sorted(sources.items()):
        print(f"   📄 {source}")
        print(f"      Chunks: {len(file_chunks)}")
        
        # Show headers
        headers = set()
        for c in file_chunks:
            h = c.metadata.get("header")
            if h:
                headers.add(h)
        
        if headers:
            print(f"      Sections: {', '.join(list(headers)[:5])}")
        print()


def similarity_finder(searcher: LocalMemorySearcher):
    """Find similar chunks"""
    print_header("🔗 Similar Chunk Finder")
    print("Find chunks that are semantically similar to each other.\n")
    
    if not searcher.index.load():
        print("❌ No index found.")
        return
    
    # Get random sample and find most similar pairs
    import random
    
    chunks = searcher.index.chunks
    if len(chunks) < 2:
        print("Not enough chunks to compare.")
        return
    
    print("🔍 Finding interesting connections in your memory...\n")
    
    # Sample some chunks and find their most similar neighbors
    sample_size = min(5, len(chunks))
    samples = random.sample(chunks, sample_size)
    
    for sample in samples:
        print(f"\n📄 Sample: {Path(sample.source).name}")
        if sample.metadata.get("header"):
            print(f"   Section: {sample.metadata['header']}")
        print(f"   Content: {sample.content[:100]}...")
        
        # Find similar
        results = searcher.search(sample.content[:200], top_k=3)
        
        print(f"\n   🔗 Most similar chunks:")
        for i, (chunk, score) in enumerate(results, 1):
            if chunk.id == sample.id:
                continue  # Skip self
            print(f"   {i}. [{score:.3f}] {Path(chunk.source).name}")
            if chunk.metadata.get("header"):
                print(f"      Section: {chunk.metadata['header']}")


def main():
    if not EMBEDDINGS_AVAILABLE:
        print("❌ Required packages not installed.")
        print("\nInstall with:")
        print("   pip install sentence-transformers numpy")
        return 1
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        🧠 Local Embedding Memory Explorer 🧠              ║
    ║                                                           ║
    ║        Semantic search for your MEMORY.md files           ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    memory_dir = Path("/root/.openclaw/workspace")
    index_path = memory_dir / ".embedding_index.json"
    
    # Check if index exists
    if not index_path.exists():
        print("⚠️  No index found. Let's create one first!\n")
        searcher = LocalMemorySearcher(memory_dir=memory_dir)
        searcher.index_memories()
        print("\n✅ Index created! Starting explorer...\n")
    else:
        searcher = LocalMemorySearcher(memory_dir=memory_dir)
    
    # Main menu
    while True:
        print("\n" + "-" * 50)
        print("📋 Menu:\n")
        print("   1. 🔍 Interactive Search")
        print("   2. ⚖️  Compare Semantic vs Text Search")
        print("   3. 📚 Explore Indexed Chunks")
        print("   4. 🔗 Find Similar Chunks")
        print("   5. 🔄 Reindex Memories")
        print("   6. ❌ Exit")
        print()
        
        try:
            choice = input("Select (1-6): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break
        
        if choice == "1":
            interactive_search(searcher)
        elif choice == "2":
            compare_mode(searcher)
        elif choice == "3":
            explore_chunks(searcher)
        elif choice == "4":
            similarity_finder(searcher)
        elif choice == "5":
            searcher.index_memories(force=True)
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
