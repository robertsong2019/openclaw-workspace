# skill-doctor 🩺

Diagnose and health-check OpenClaw Agent Skills.

```bash
npx skill-doctor ./my-skill
npx skill-doctor ./skills/*    # batch check
npx skill-doctor ./my-skill --fix  # auto-fix where possible
```

## Checks Performed

- **Structure**: Required files exist (SKILL.md, etc.)
- **SKILL.md**: Valid frontmatter, required fields, reasonable length
- **Scripts**: Referenced scripts exist and are executable
- **Security**: No suspicious patterns (eval, exec of user input, exfiltration)
- **Docs**: README present and non-trivial
- **Freshness**: No stale references, reasonable file sizes

## Output

- Clean summary table with pass/warn/fail per check
- Exit code 0 = all pass, 1 = warnings, 2 = failures

## Install

```bash
npm install -g skill-doctor
# or use directly
npx skill-doctor <path>
```
