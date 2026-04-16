# dep-guard 🔒

Lightweight dependency health & security scanner for Node.js and Python projects.

## Features

- 🔍 Detects outdated dependencies
- ⚠️ Flags known vulnerabilities (npm audit / pip audit)
- 📊 Generates health score (0-100)
- 📋 Multiple output formats (text, json, markdown)
- 🚀 Zero config — runs against package.json or requirements.txt

## Install

```bash
# Copy to PATH or run directly
chmod +x dep-guard.sh
./dep-guard.sh /path/to/project
```

## Usage

```bash
# Scan current directory
dep-guard.sh .

# Scan specific project
dep-guard.sh ~/projects/my-app

# JSON output
dep-guard.sh --format json ~/projects/my-app

# Markdown report
dep-guard.sh --format markdown ~/projects/my-app

# Only security check (skip outdated)
dep-guard.sh --security-only ~/projects/my-app

# CI mode: exit 1 if score < threshold
dep-guard.sh --min-score 70 ~/projects/my-app
```

## Health Score Calculation

| Factor | Weight |
|--------|--------|
| Vulnerabilities (high/critical) | 40% |
| Outdated major versions | 30% |
| Outdated minor/patch versions | 20% |
| Lock file present | 10% |

## Example Output

```
╔══════════════════════════════════════╗
║  dep-guard · Dependency Health Scan  ║
╠══════════════════════════════════════╣
║  Project: my-app                     ║
║  Type:    node                       ║
║  Score:   82/100 ✅                  ║
╠══════════════════════════════════════╣
║                                      ║
║  🔒 Security (0 issues)             ║
║  📦 Outdated (3 packages)            ║
║    • express 4.18 → 5.0 (major)     ║
║    • lodash 4.17.20 → 4.17.21       ║
║    • jest 29.0 → 29.7 (minor)       ║
║  🔐 Lockfile: package-lock.json ✓   ║
║                                      ║
╚══════════════════════════════════════╝
```
