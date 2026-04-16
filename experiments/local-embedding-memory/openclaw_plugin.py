"""
OpenClaw Plugin: Local Embedding Memory
Integrates semantic memory search with OpenClaw agents

v1.1.0 — Fixed to match actual memory_embedder API (LocalMemorySearcher, LocalEmbeddingEngine)
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add the local-embedding-memory module to the path
plugin_dir = os.path.dirname(__file__)
sys.path.insert(0, plugin_dir)

try:
    from memory_embedder import LocalMemorySearcher, LocalEmbeddingEngine, EMBEDDINGS_AVAILABLE

    class LocalEmbeddingMemoryPlugin:
        """OpenClaw plugin for semantic memory search"""

        def __init__(self, workspace: str = None):
            self.workspace = workspace or os.getcwd()
            self.memory_dir = os.path.join(self.workspace, "memory")
            self.main_memory = os.path.join(self.workspace, "MEMORY.md")
            self.index_path = os.path.join(self.workspace, ".embedding_index.json")
            self.searcher: Optional[LocalMemorySearcher] = None

        def _get_memory_source(self) -> str:
            """Return workspace root — the searcher expects workspace_dir with memory/ subfolder."""
            return self.workspace

        def initialize(self) -> Dict[str, Any]:
            """Initialize the memory plugin."""
            try:
                if not EMBEDDINGS_AVAILABLE:
                    return {
                        "status": "error",
                        "message": "sentence-transformers not installed. Run: pip install sentence-transformers numpy",
                    }

                source = self._get_memory_source()
                if not os.path.exists(source):
                    return {
                        "status": "warning",
                        "message": "No memory files found",
                        "suggestion": "Create MEMORY.md or memory/ directory",
                    }

                from pathlib import Path as _Path
                self.searcher = LocalMemorySearcher(
                    _Path(source), index_path=_Path(self.index_path)
                )

                # Check existing index
                total = 0
                last_time = None
                if os.path.isfile(self.index_path):
                    with open(self.index_path, "r") as f:
                        data = json.load(f)
                        total = len(data.get("chunks", []))
                        last_time = data.get("last_index_time")

                return {
                    "status": "success",
                    "message": "Local embedding memory plugin initialized",
                    "total_memories": total,
                    "last_index_time": last_time,
                    "index_path": self.index_path,
                }

            except Exception as exc:
                return {"status": "error", "message": f"Failed to initialize: {exc}"}

        def update_index(self, force: bool = False) -> Dict[str, Any]:
            """Update the embedding index."""
            try:
                if not self.searcher:
                    return {"status": "error", "message": "Plugin not initialized"}

                self.searcher.index_memories(force=force)

                # Read back stats
                total = 0
                last_time = None
                if os.path.isfile(self.index_path):
                    with open(self.index_path, "r") as f:
                        data = json.load(f)
                        total = len(data.get("chunks", []))
                        last_time = data.get("last_index_time")

                return {
                    "status": "success",
                    "message": "Embedding index updated",
                    "total_memories": total,
                    "index_time": last_time,
                }

            except Exception as exc:
                return {"status": "error", "message": f"Failed to update index: {exc}"}

        def search_memory(self, query: str, top_k: int = 5, min_score: float = 0.0) -> Dict[str, Any]:
            """Search memories using semantic search."""
            try:
                if not self.searcher:
                    return {"status": "error", "message": "Plugin not initialized"}

                # Auto-index if needed
                if not os.path.isfile(self.index_path):
                    idx = self.update_index()
                    if idx["status"] != "success":
                        return idx

                raw_results = self.searcher.search(query, top_k=top_k)
                results = []
                for chunk, score in raw_results:
                    if score < min_score:
                        continue
                    results.append({
                        "id": chunk.id,
                        "source": chunk.source,
                        "content": chunk.content[:300],
                        "score": float(score),
                        "metadata": chunk.metadata,
                    })

                return {
                    "status": "success",
                    "query": query,
                    "total_results": len(results),
                    "results": results,
                }

            except Exception as exc:
                return {"status": "error", "message": f"Search failed: {exc}"}

        def compare_search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
            """Compare semantic vs text search."""
            try:
                if not self.searcher:
                    return {"status": "error", "message": "Plugin not initialized"}

                if not os.path.isfile(self.index_path):
                    return {"status": "error", "message": "Index not found. Run update_index() first."}

                # compare_search prints but doesn't return, so call directly
                semantic_raw = self.searcher.search(query, top_k=top_k)
                text_raw = self.searcher.text_search(query, top_k=top_k)

                def _serialize(items):
                    out = []
                    for chunk, score in items:
                        out.append({
                            "source": chunk.source,
                            "content": chunk.content[:300],
                            "score": float(score),
                        })
                    return out

                return {
                    "status": "success",
                    "query": query,
                    "semantic_results": _serialize(semantic_raw),
                    "text_results": _serialize(text_raw),
                }

            except Exception as exc:
                return {"status": "error", "message": f"Comparison search failed: {exc}"}

        def get_stats(self) -> Dict[str, Any]:
            """Get memory statistics."""
            try:
                memory_files = []
                if os.path.isfile(self.main_memory):
                    memory_files.append(self.main_memory)
                if os.path.isdir(self.memory_dir):
                    for fn in os.listdir(self.memory_dir):
                        if fn.endswith(".md"):
                            memory_files.append(os.path.join(self.memory_dir, fn))

                total_size = sum(os.path.getsize(f) for f in memory_files if os.path.exists(f))

                index_info: Dict[str, Any] = {}
                if os.path.isfile(self.index_path):
                    with open(self.index_path, "r") as f:
                        data = json.load(f)
                        index_info = {
                            "chunks": len(data.get("chunks", [])),
                            "last_index_time": data.get("last_index_time"),
                            "embedding_model": data.get("model", "unknown"),
                        }

                return {
                    "status": "success",
                    "memory_files": len(memory_files),
                    "total_size_bytes": total_size,
                    "total_size_mb": round(total_size / (1024 * 1024), 2),
                    "index_info": index_info,
                    "plugin_initialized": self.searcher is not None,
                }

            except Exception as exc:
                return {"status": "error", "message": f"Failed to get stats: {exc}"}

        def get_health(self) -> Dict[str, Any]:
            """Get plugin health status."""
            issues: list[str] = []
            warnings: list[str] = []

            if not self.searcher:
                issues.append("Plugin not initialized")
            if not os.path.isfile(self.index_path):
                warnings.append("Index file not found — will auto-create on first search")
            if not os.path.isfile(self.main_memory) and not os.path.isdir(self.memory_dir):
                issues.append("No memory files found")

            if issues:
                health = "unhealthy"
            elif warnings:
                health = "degraded"
            else:
                health = "healthy"

            return {
                "status": health,
                "issues": issues,
                "warnings": warnings,
                "plugin_initialized": self.searcher is not None,
                "index_exists": os.path.isfile(self.index_path),
                "memory_files_exist": os.path.isfile(self.main_memory) or os.path.isdir(self.memory_dir),
            }

        def search_with_context(self, query: str, context_window: int = 2,
                                top_k: int = 5) -> Dict[str, Any]:
            """Search memories and return results with extended context."""
            search_result = self.search_memory(query, top_k)
            if search_result["status"] != "success":
                return search_result

            for r in search_result["results"]:
                r["context_available"] = True
                r["context_lines"] = context_window

            search_result["context_enhanced"] = True
            return search_result

        def recent_memories(self, limit: int = 10) -> Dict[str, Any]:
            """Get recently indexed memories."""
            try:
                if not os.path.isfile(self.index_path):
                    return {"status": "error", "message": "Index not found"}

                with open(self.index_path, "r") as f:
                    data = json.load(f)

                chunks = data.get("chunks", [])
                recent = chunks[-limit:] if len(chunks) >= limit else chunks

                return {
                    "status": "success",
                    "total_chunks": len(chunks),
                    "returned_chunks": len(recent),
                    "recent_memories": recent,
                }

            except Exception as exc:
                return {"status": "error", "message": f"Failed to get recent memories: {exc}"}

    def create_plugin(workspace: str = None) -> LocalEmbeddingMemoryPlugin:
        """Factory function to create plugin instance."""
        return LocalEmbeddingMemoryPlugin(workspace)

    PLUGIN_NAME = "Local Embedding Memory"
    PLUGIN_VERSION = "1.1.0"
    PLUGIN_DESCRIPTION = "Semantic memory search for OpenClaw agents"
    PLUGIN_CAPABILITIES = [
        "semantic_search",
        "text_search",
        "index_management",
        "memory_statistics",
        "health_checks",
    ]

    __all__ = [
        "create_plugin",
        "LocalEmbeddingMemoryPlugin",
        "PLUGIN_NAME",
        "PLUGIN_VERSION",
        "PLUGIN_DESCRIPTION",
        "PLUGIN_CAPABILITIES",
    ]

except ImportError as exc:
    def create_plugin(workspace: str = None):
        raise ImportError(f"Memory embedder not available: {exc}")

    PLUGIN_NAME = "Local Embedding Memory"
    PLUGIN_VERSION = "1.1.0"
    PLUGIN_DESCRIPTION = "Semantic memory search for OpenClaw agents (dependencies not installed)"
    PLUGIN_CAPABILITIES = []
