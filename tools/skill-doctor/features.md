# skill-doctor Features

## Core (v1.0.0) ✅
- [x] SKILL.md existence & size check
- [x] SKILL.md description detection
- [x] README.md existence check
- [x] Oversized files detection (>500KB)
- [x] Suspicious patterns detection (eval, injection, pipe-to-shell)
- [x] Script references validation
- [x] node_modules / .gitignore check
- [x] package.json validation
- [x] CLI interface with exit codes (0=pass, 1=warn, 2=fail)
- [x] Multiple directory support

## Planned
- [x] **JSON output** (`--json`) — machine-readable output for CI integration ✅ 2026-05-09
- [ ] **Custom checks** — load additional checks from `.skill-doctor.js`
- [ ] **Auto-fix** (`--fix`) — auto-fix simple issues (add .gitignore, etc.)
