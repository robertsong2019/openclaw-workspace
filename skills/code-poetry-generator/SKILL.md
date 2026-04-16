# Code Poetry Generator

Turn code into poetry, and poetry into code.

## Description

Transform code snippets into creative poems (haiku, sonnet, or free verse) that reflect the code's logic, structure, and intent. Reverse the process: turn poems into working code. Supports English and Chinese output.

## Activation

Activate when the user:
- Wants to turn code into a poem or haiku
- Wants to generate code inspired by a poem
- Mentions "code poetry", "code haiku", "code sonnet"
- Asks to "poeticize" or "versify" code
- Asks to "code-ify" a poem
- Uses phrases like "write a poem about this code", "turn this code into a haiku"

## Usage

### Code → Poetry

```
# From a file
Use code-poetry-generator: turn src/main.py into a haiku in Chinese

# From pasted code
Here's my code:
```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```
Write a sonnet about it.
```

### Poetry → Code

```
Take this poem and generate Python code that embodies it:
"Two roads diverged in a yellow wood..."
```

### CLI

```bash
# Haiku from file
bin/code-poetry --from-code main.py --mode haiku --lang en

# Sonnet from stdin
cat app.js | bin/code-poetry --from-code - --mode sonnet --lang zh

# Poem to code
bin/code-poetry --from-poem "Roses are red, loops are true" --lang en
```

## Modes

| Mode | Description |
|------|-------------|
| `haiku` | 5-7-5 syllable structure, compresses code essence |
| `sonnet` | Shakespearean sonnet: 14 lines, ABAB CDCD EFEF GG |
| `free` | Free verse, no formal constraints |

## Languages

- **Python**: Full AST analysis via `scripts/analyze.py`
- **JS/TS**: Regex-based structural analysis
- **Go, Rust, C, Java, etc.**: Heuristic analysis + LLM interpretation
- **Any text**: The LLM will do its best with any code or pseudocode

## How It Works

1. If Python code or a file is provided, run `scripts/analyze.py` to extract structural metrics (functions, loops, conditionals, depth, variable names)
2. Feed the analysis + raw code to the LLM with mode/language instructions
3. For poem→code, analyze the poem's structure and themes, then generate matching code

## Implementation Status

✅ **Fully Implemented** (2026-04-11)

### Completed Components

1. **scripts/analyze.py** - Python AST Analyzer
   - Extracts functions, classes, loops, conditionals
   - Tracks nesting depth, variables, decorators, imports
   - Counts lines of code
   - Handles syntax errors gracefully
   - Supports stdin input or file path argument
   - Outputs JSON format

2. **bin/code-poetry** - CLI Tool
   - `--from-code FILE|stdin`: Analyze code and generate poetry prompt
   - `--from-poem TEXT`: Generate code from poem prompt
   - `--mode haiku|sonnet|free`: Select poetry mode (default: free)
   - `--lang en|zh`: Select output language (default: en)
   - Outputs structured JSON prompts for LLM consumption
   - Automatically runs AST analysis for Python files

3. **tests/test_analyze.py** - Test Suite
   - 12 unit tests covering all major functionality
   - Tests: basic functions, classes, nesting, syntax errors, variables, imports
   - Passes with pytest: `python -m pytest tests/ -v`

4. **requirements.txt** - Dependencies
   - No external dependencies (Python 3 standard library only)

### Testing

Run tests:
```bash
cd ~/.openclaw/workspace/skills/code-poetry-generator
python3 -m pytest tests/ -v
```

Test CLI:
```bash
# Code to poetry
echo 'def hello(): print("Hi")' | bin/code-poetry --from-code - --mode haiku --lang en

# Poem to code
bin/code-poetry --from-poem "Two roads diverged" --lang zh
```

## Notes

- The `bin/code-poetry` CLI outputs a structured prompt — pipe it to the agent or use it standalone
- Multilingual: `--lang zh` for Chinese, `--lang en` for English
- For best results with sonnet mode, provide substantial code (20+ lines)
