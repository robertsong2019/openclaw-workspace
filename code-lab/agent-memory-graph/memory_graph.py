"""
Agent Memory Graph — A lightweight knowledge graph for AI agent memory.

Zero external dependencies (stdlib + sqlite3 only).
"""

import sqlite3
import json
import time
import math
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Entity:
    name: str
    type: str = "thing"
    properties: dict = field(default_factory=dict)
    weight: float = 1.0
    created_at: float = field(default_factory=time.time)
    accessed_at: float = field(default_factory=time.time)
    access_count: int = 0


@dataclass
class Relation:
    source: str
    verb: str
    target: str
    weight: float = 1.0
    created_at: float = field(default_factory=time.time)
    properties: dict = field(default_factory=dict)


class MemoryGraph:
    """SQLite-backed knowledge graph with decay and context retrieval."""

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                name TEXT PRIMARY KEY,
                type TEXT NOT NULL DEFAULT 'thing',
                properties TEXT DEFAULT '{}',
                weight REAL DEFAULT 1.0,
                created_at REAL,
                accessed_at REAL,
                access_count INTEGER DEFAULT 0
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                verb TEXT NOT NULL,
                target TEXT NOT NULL,
                weight REAL DEFAULT 1.0,
                created_at REAL,
                properties TEXT DEFAULT '{}',
                UNIQUE(source, verb, target),
                FOREIGN KEY(source) REFERENCES entities(name),
                FOREIGN KEY(target) REFERENCES entities(name)
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_relations_source ON relations(source)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type)
        """)
        self.conn.commit()

    # ── Entity Operations ──────────────────────────────────

    def add_entity(self, name: str, type: str = "thing", properties: dict = None) -> Entity:
        """Add or update an entity."""
        props = json.dumps(properties or {})
        now = time.time()
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO entities (name, type, properties, weight, created_at, accessed_at, access_count)
            VALUES (?, ?, ?, 1.0, ?, ?, 0)
            ON CONFLICT(name) DO UPDATE SET
                type = excluded.type,
                properties = excluded.properties,
                accessed_at = excluded.accessed_at,
                access_count = access_count + 1
        """, (name, type, props, now, now))
        self.conn.commit()
        return Entity(name=name, type=type, properties=properties or {})

    def get_entity(self, name: str) -> Optional[Entity]:
        """Retrieve an entity and bump its access count."""
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE entities SET accessed_at = ?, access_count = access_count + 1
            WHERE name = ? RETURNING *
        """, (time.time(), name))
        row = cur.fetchone()
        self.conn.commit()
        if not row:
            return None
        return Entity(
            name=row["name"], type=row["type"],
            properties=json.loads(row["properties"]),
            weight=row["weight"], created_at=row["created_at"],
            accessed_at=row["accessed_at"], access_count=row["access_count"]
        )

    def query(self, entity_type: str = None, search: str = None) -> list[Entity]:
        """Query entities by type and/or name search."""
        cur = self.conn.cursor()
        sql = "SELECT * FROM entities WHERE 1=1"
        params = []
        if entity_type:
            sql += " AND type = ?"
            params.append(entity_type)
        if search:
            sql += " AND name LIKE ?"
            params.append(f"%{search}%")
        sql += " ORDER BY weight DESC, accessed_at DESC"
        cur.execute(sql, params)
        return [
            Entity(
                name=r["name"], type=r["type"],
                properties=json.loads(r["properties"]),
                weight=r["weight"], created_at=r["created_at"],
                accessed_at=r["accessed_at"], access_count=r["access_count"]
            )
            for r in cur.fetchall()
        ]

    # ── Relation Operations ────────────────────────────────

    def relate(self, source: str, verb: str, target: str, properties: dict = None) -> Relation:
        """Create a relation between two entities."""
        now = time.time()
        props = json.dumps(properties or {})
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO relations (source, verb, target, weight, created_at, properties)
            VALUES (?, ?, ?, 1.0, ?, ?)
            ON CONFLICT(source, verb, target) DO UPDATE SET
                weight = weight + 0.1,
                properties = excluded.properties
        """, (source, verb, target, now, props))
        self.conn.commit()
        return Relation(source=source, verb=verb, target=target, properties=properties or {})

    def get_relations(self, entity: str, direction: str = "outgoing") -> list[Relation]:
        """Get relations for an entity. direction: 'outgoing', 'incoming', or 'both'."""
        cur = self.conn.cursor()
        if direction in ("outgoing", "both"):
            cur.execute("""
                SELECT source, verb, target, weight, properties FROM relations WHERE source = ?
                ORDER BY weight DESC
            """, (entity,))
            rows = cur.fetchall()
        if direction in ("incoming", "both"):
            cur.execute("""
                SELECT source, verb, target, weight, properties FROM relations WHERE target = ?
                ORDER BY weight DESC
            """, (entity,))
            rows = (rows if direction == "both" else []) + cur.fetchall()

        return [
            Relation(
                source=r["source"], verb=r["verb"], target=r["target"],
                weight=r["weight"], properties=json.loads(r["properties"])
            )
            for r in rows
        ]

    # ── Context Retrieval (BFS) ────────────────────────────

    def context(self, entity: str, depth: int = 2, min_weight: float = 0.2) -> dict:
        """
        Retrieve the connected subgraph around an entity via BFS.

        Returns a dict with 'entities' and 'relations' forming the context neighborhood.
        """
        visited_entities = set()
        visited_relations = set()
        result_entities = []
        result_relations = []
        queue = [(entity, 0)]

        while queue:
            current, d = queue.pop(0)
            if current in visited_entities or d > depth:
                continue
            visited_entities.add(current)

            ent = self.get_entity(current)
            if not ent or ent.weight < min_weight:
                continue
            result_entities.append(ent)

            if d < depth:
                for rel in self.get_relations(current, "both"):
                    rel_key = (rel.source, rel.verb, rel.target)
                    if rel_key not in visited_relations and rel.weight >= min_weight:
                        visited_relations.add(rel_key)
                        result_relations.append(rel)
                        neighbor = rel.target if rel.source == current else rel.source
                        if neighbor not in visited_entities:
                            queue.append((neighbor, d + 1))

        return {"entities": result_entities, "relations": result_relations}

    # ── Memory Decay ───────────────────────────────────────

    def decay(self, max_age_days: float = 30, threshold: float = 0.1, decay_rate: float = 0.95):
        """
        Decay memory weights based on age. Remove memories below threshold.

        Uses exponential decay: weight *= decay_rate for each day since last access.
        """
        now = time.time()
        cur = self.conn.cursor()

        # Decay entities
        cur.execute("SELECT name, weight, accessed_at FROM entities")
        to_delete = []
        for row in cur.fetchall():
            age_days = (now - row["accessed_at"]) / 86400
            new_weight = row["weight"] * (decay_rate ** age_days)
            if new_weight < threshold:
                to_delete.append(row["name"])
            else:
                cur.execute("UPDATE entities SET weight = ? WHERE name = ?",
                            (new_weight, row["name"]))

        # Delete decayed entities and their relations
        for name in to_delete:
            cur.execute("DELETE FROM relations WHERE source = ? OR target = ?", (name, name))
            cur.execute("DELETE FROM entities WHERE name = ?", (name,))

        # Decay relations
        cur.execute("SELECT id, weight, created_at FROM relations")
        rel_to_delete = []
        for row in cur.fetchall():
            age_days = (now - row["created_at"]) / 86400
            new_weight = row["weight"] * (decay_rate ** age_days)
            if new_weight < threshold:
                rel_to_delete.append(row["id"])
            else:
                cur.execute("UPDATE relations SET weight = ? WHERE id = ?",
                            (new_weight, row["id"]))

        for rid in rel_to_delete:
            cur.execute("DELETE FROM relations WHERE id = ?", (rid,))

        self.conn.commit()
        return {
            "decayed_entities": len(to_delete),
            "decayed_relations": len(rel_to_delete)
        }

    # ── Export / Import ────────────────────────────────────

    def export_graph(self) -> dict:
        """Export entire graph as a JSON-serializable dict."""
        entities = self.query()
        cur = self.conn.cursor()
        cur.execute("SELECT source, verb, target, weight, properties FROM relations")
        relations = [
            {
                "source": r["source"], "verb": r["verb"], "target": r["target"],
                "weight": r["weight"], "properties": json.loads(r["properties"])
            }
            for r in cur.fetchall()
        ]
        return {
            "entities": [asdict(e) for e in entities],
            "relations": relations
        }

    def stats(self) -> dict:
        """Quick graph statistics."""
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) as n FROM entities")
        entity_count = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) as n FROM relations")
        relation_count = cur.fetchone()["n"]
        cur.execute("SELECT DISTINCT type FROM entities")
        types = [r["type"] for r in cur.fetchall()]
        cur.execute("SELECT DISTINCT verb FROM relations")
        verbs = [r["verb"] for r in cur.fetchall()]
        return {
            "entities": entity_count,
            "relations": relation_count,
            "entity_types": types,
            "relation_verbs": verbs
        }

    def close(self):
        self.conn.close()
