# Agent Memory Graph 🧠

A lightweight knowledge graph memory system for AI agents.

## Why?

Agents wake up fresh each session. Files work, but they're flat. A memory graph lets agents:
- Store **entities** (people, projects, concepts)
- Create **relations** between them
- **Query** by type, relation, or semantic similarity
- **Decay** old memories automatically

## Usage

```python
from memory_graph import MemoryGraph

mg = MemoryGraph("agent_memory.db")

# Store entities
mg.add_entity("罗嵩", type="person", properties={"role": "developer", "timezone": "Asia/Shanghai"})
mg.add_entity("Catalyst", type="agent", properties={"emoji": "🧪", "role": "digital familiar"})

# Create relations
mg.relate("罗嵩", "created", "Catalyst")
mg.relate("Catalyst", "serves", "罗嵩")

# Query
friends = mg.query(entity_type="person")
relations = mg.get_relations("罗嵩")

# Context recall — get everything connected to an entity
context = mg.context("Catalyst", depth=2)

# Memory decay — reduce weight of old, unused memories
mg.decay(max_age_days=30, threshold=0.1)
```

## Features

- **SQLite-backed** — zero dependencies, persistent
- **Weighted edges** — memories strengthen with use, decay with time
- **Context retrieval** — BFS traversal for connected subgraphs
- **Auto-decay** — old unused memories fade away
- **Full-text search** — fuzzy match on entity names and properties
