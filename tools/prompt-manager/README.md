# Prompt Template Manager (ptm)

A CLI tool for managing AI prompt templates — store, version, test, and compose prompts.

## Features
- Store prompts with metadata (model, temperature, tags)
- Version history with diff
- Variable interpolation (`{{variable}}`)
- Compose multi-step agent prompts from templates
- Test prompts with dry-run variable substitution
- Import/export JSON bundles

## Usage
```bash
ptm add <name> <template>     # Add a new template
ptm get <name>                # View a template
ptm list [--tag <tag>]        # List templates
ptm render <name> -k key=val  # Render with variables
ptm compose <t1> <t2> ...    # Compose multiple templates
ptm history <name>            # View version history
ptm export                    # Export all as JSON
ptm import <file>             # Import from JSON
```
