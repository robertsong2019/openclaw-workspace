# prompt-template-manager (ptm)

Store, catalog, and render prompt templates with `{{variable}}` substitution.

## Commands

```bash
ptm list                          # List all templates
ptm show <name>                   # Display a template
ptm add <name> [content]          # Add new template
ptm render <name> key=val ...     # Render with variables
ptm export <name> key=val ...     # Output rendered (pipe-friendly)
```

## Bundled Templates

- **code-review** — Structured code review prompt
- **bug-investigation** — Root cause analysis prompt  
- **skill-design** — OpenClaw skill design prompt

## Add Your Own

Drop `.md` files into `templates/` with `{{variable}}` placeholders:

```markdown
# Analyze {{type}}
Examine this {{type}} for {{goal}}:
{{content}}
```

Then: `ptm render analyze type=API goal="security issues" content="..."`

## Design

- Zero dependencies
- Templates are plain Markdown — version control friendly
- `export` outputs raw text for piping to other tools
