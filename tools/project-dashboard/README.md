# 📊 Project Dashboard Generator

> A lightweight CLI tool that scans all projects in a workspace and generates a unified health/status dashboard.

Perfect for AI agents and developers who need a quick overview of multiple projects.

## Features

- 🔍 **Multi-project scanning** - Detects all projects in a workspace
- 📊 **Health scoring** - 0-100 score based on docs, tests, git status, code quality
- 📝 **Multiple formats** - Markdown (human-readable) or JSON (machine-readable)
- ⚡ **Fast** - Pure Python, no external dependencies
- 🤖 **AI-friendly** - Designed for AI agent context generation

## What It Detects

| Category | Details |
|----------|---------|
| **Git Status** | Clean, dirty, untracked files |
| **Tests** | pytest, jest, mocha, unittest, cargo, go test |
| **Docs** | README, CHANGELOG, API docs, tutorials |
| **Code Quality** | TODO/FIXME counts |
| **Languages** | Python, JavaScript, TypeScript, Go, Rust, etc. |
| **Dependencies** | npm, pip, cargo, go modules |
| **Activity** | Last modified, file/line counts |

## Installation

```bash
# No installation needed - just run it!
python3 project_dashboard.py /path/to/workspace

# Or make it executable
chmod +x project_dashboard.py
./project_dashboard.py /path/to/workspace
```

## Quick Start

```bash
# Scan current directory
python3 project_dashboard.py .

# Scan a workspace
python3 project_dashboard.py ~/projects

# JSON output
python3 project_dashboard.py ~/projects -f json

# Save to file
python3 project_dashboard.py ~/projects -o DASHBOARD.md

# Only show healthy projects (score >= 50)
python3 project_dashboard.py ~/projects --min-health 50
```

## Example Output

```markdown
# 📊 Project Dashboard

_Generated: 2026-03-22 22:00_

**Total Projects**: 5

## Overview

| Metric | Value |
|--------|-------|
| Total Files | 1,234 |
| Total Lines | 45,678 |
| Projects with Tests | 4/5 |
| Projects with Docs | 5/5 |
| Avg Health Score | 78 |

## Projects

| Project | Language | Health | Git | Tests | Docs | TODOs | Files | Lines |
|---------|----------|--------|-----|-------|------|-------|-------|-------|
| agent-task-cli | TypeScript | 🟢 85 | ✅ | ✅ | 📚 | 3 | 156 | 4,321 |
| prompt-mgr | Python | 🟢 82 | ✅ | ✅ | 📚 | 5 | 89 | 2,456 |
| local-embedding | Python | 🟡 65 | ⚠️ | ❌ | 📚 | 12 | 45 | 1,234 |
```

## Health Score Calculation

| Factor | Points | Criteria |
|--------|--------|----------|
| Documentation | 30 | README (15), CHANGELOG (10), extra docs (5) |
| Testing | 25 | Has tests (25) |
| Git Status | 20 | Clean (20), untracked (10) |
| Code Quality | 15 | No TODOs (15), <10 (10), <50 (5) |
| Activity | 10 | Modified <7d ago (10), <30d (5) |

## Use Cases

### For AI Agents

```bash
# Generate context for AI assistants
python3 project_dashboard.py ~/workspace -o context/dashboard.md

# JSON for programmatic use
python3 project_dashboard.py ~/workspace -f json | jq '.projects[] | select(.health_score < 50)'
```

### For Developers

```bash
# Daily standup preparation
python3 project_dashboard.py ~/projects

# CI/CD integration
python3 project_dashboard.py . -f json --min-health 60 || echo "Low health score detected"

# Find projects needing attention
python3 project_dashboard.py ~/projects | grep "Needs Attention" -A 10
```

## AI Agent Integration

This tool is designed to work with AI agents like OpenClaw:

```python
# In an AI agent skill
from pathlib import Path
import json
import subprocess

def get_workspace_health(workspace_path):
    """Get health status of all projects."""
    result = subprocess.run(
        ['python3', 'project_dashboard.py', workspace_path, '-f', 'json'],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

# Use in agent context
health = get_workspace_health('/root/.openclaw/workspace')
low_health = [p for p in health['projects'] if p['health_score'] < 50]
if low_health:
    print(f"Projects needing attention: {[p['name'] for p in low_health]}")
```

## Extending

### Add Custom Checks

```python
# In project_dashboard.py, add to _analyze_project()

# Check for CI/CD config
project.has_ci = any(
    (path / f).exists() 
    for f in ['.github/workflows', '.gitlab-ci.yml', 'Jenkinsfile']
)

# Check for security files
project.has_security = (path / 'SECURITY.md').exists()
```

### Custom Output Formats

```python
def generate_html(self) -> str:
    """Generate HTML dashboard."""
    # Implement HTML generation
    pass
```

## Roadmap

- [ ] HTML output format
- [ ] CI/CD status detection
- [ ] Security file detection
- [ ] Dependency freshness check
- [ ] Historical tracking (compare with previous scans)
- [ ] Watch mode for continuous updates
- [ ] Integration with GitHub API for remote repos

## License

MIT

## Related Tools

- **context_gen.py** - Generate AI-ready context for single projects
- **memory_embedder.py** - Semantic search for memory files
- **prompt-mgr** - Manage AI prompt templates

---

Built for AI Agent development workflows 🤖
