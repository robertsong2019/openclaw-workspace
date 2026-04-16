"""Demo: Agent Memory Graph in action."""
from memory_graph import MemoryGraph
import json

mg = MemoryGraph("demo_memory.db")

# ── Build a knowledge graph about an AI agent ecosystem ──

mg.add_entity("罗嵩", "person", {"role": "developer", "github": "robertsong2019"})
mg.add_entity("Catalyst", "agent", {"emoji": "🧪", "personality": "sharp & fast"})
mg.add_entity("OpenClaw", "platform", {"type": "agent runtime"})
mg.add_entity("Python", "language", {"version": "3.12"})
mg.add_entity("Memory Graph", "project", {"status": "experimental", "language": "Python"})

mg.relate("罗嵩", "created", "Catalyst")
mg.relate("Catalyst", "runs_on", "OpenClaw")
mg.relate("Catalyst", "serves", "罗嵩")
mg.relate("Catalyst", "built", "Memory Graph")
mg.relate("Memory Graph", "written_in", "Python")
mg.relate("罗嵩", "develops", "OpenClaw")

# ── Query demos ──

print("📊 Graph Stats:")
print(json.dumps(mg.stats(), indent=2, ensure_ascii=False))

print("\n🔍 All persons:")
for e in mg.query(entity_type="person"):
    print(f"  {e.name} ({e.type}): {e.properties}")

print("\n🔗 Relations from Catalyst:")
for r in mg.get_relations("Catalyst"):
    print(f"  {r.source} --[{r.verb}]--> {r.target}")

print("\n🌐 Context around 'Catalyst' (depth=2):")
ctx = mg.context("Catalyst", depth=2)
print(f"  Entities: {[e.name for e in ctx['entities']]}")
print(f"  Relations: {[(r.source, r.verb, r.target) for r in ctx['relations']]}")

print("\n📉 Decay simulation:")
result = mg.decay(max_age_days=0.001)  # aggressive decay for demo
print(f"  Removed: {result}")

print("\n📊 Stats after decay:")
print(json.dumps(mg.stats(), indent=2, ensure_ascii=False))

mg.close()
print("\n✅ Demo complete!")
