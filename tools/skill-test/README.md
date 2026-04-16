# skill-test

Lightweight validator & tester for OpenClaw skills.

## Install

```bash
# Symlink to PATH
ln -s /path/to/skill-test/skill-test /usr/local/bin/skill-test
```

## Usage

```bash
# Test current directory
skill-test .

# Test a specific skill
skill-test ~/.openclaw/workspace/skills/github-trending

# Auto-fix issues (permissions, etc.)
skill-test . --fix

# Verbose output
skill-test . --verbose
```

## What It Checks

| Check | Description |
|-------|-------------|
| SKILL.md exists | Every skill must have one |
| H1 title | Clear name for the skill |
| Trigger/description | Agents need to know when to activate |
| Length | Too short = useless, too long = token waste |
| Dangerous commands | rm -rf, dd, mkfs patterns |
| Pipe-to-shell | curl|sh security risks |
| File references | Referenced files should exist |
| Script permissions | .sh files should be executable |
| Shellcheck | Lint scripts if shellcheck is available |
| Hardcoded secrets | API keys, private keys |
| Usage examples | Help discoverability |

## Exit Codes

- `0` — All checks pass (warnings ok)
- `1` — One or more failures detected
