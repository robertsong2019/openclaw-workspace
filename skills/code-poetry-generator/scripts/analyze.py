#!/usr/bin/env python3
"""
Python AST Analyzer - Extracts structural information from Python code.
Supports stdin input or file path argument. Outputs JSON.
"""

import ast
import json
import sys
from pathlib import Path


class CodeAnalyzer(ast.NodeVisitor):
    """AST visitor that extracts code structure metrics."""

    def __init__(self):
        self.functions = []
        self.classes = []
        self.loops = 0
        self.conditionals = 0
        self.max_depth = 0
        self.current_depth = 0
        self.variables = set()
        self.decorators = set()
        self.imports = []
        self.line_count = 0

    def visit_FunctionDef(self, node):
        """Extract function information."""
        func_info = {
            'name': node.name,
            'line': node.lineno,
            'args': [arg.arg for arg in node.args.args],
            'decorators': [self._get_decorator_name(d) for d in node.decorator_list]
        }
        self.functions.append(func_info)
        self.decorators.update(func_info['decorators'])

        # Visit function body with increased depth
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_AsyncFunctionDef(self, node):
        """Handle async functions the same way."""
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        """Extract class information."""
        class_info = {
            'name': node.name,
            'line': node.lineno,
            'bases': [self._get_name(base) for base in node.bases],
            'decorators': [self._get_decorator_name(d) for d in node.decorator_list]
        }
        self.classes.append(class_info)
        self.decorators.update(class_info['decorators'])

        # Visit class body with increased depth
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_For(self, node):
        """Count for loops."""
        self.loops += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_While(self, node):
        """Count while loops."""
        self.loops += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_If(self, node):
        """Count if statements (conditionals)."""
        self.conditionals += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_Name(self, node):
        """Extract variable names (assignments)."""
        # This is a simplified approach - we're capturing all Name nodes
        # In practice, you'd want to track Store vs Load contexts
        if isinstance(node.ctx, ast.Store):
            self.variables.add(node.id)
        self.generic_visit(node)

    def visit_Import(self, node):
        """Extract import statements."""
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Extract from...import statements."""
        module = node.module or ''
        for alias in node.names:
            self.imports.append(f"{module}.{alias.name}")
        self.generic_visit(node)

    def _get_decorator_name(self, node):
        """Get the name of a decorator."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        elif isinstance(node, ast.Attribute):
            return self._get_name(node)
        return str(type(node).__name__)

    def _get_name(self, node):
        """Get the name from a node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)

    def get_analysis(self, source_lines):
        """Return the analysis results as a dictionary."""
        return {
            'functions': self.functions,
            'classes': self.classes,
            'loops': self.loops,
            'conditionals': self.conditionals,
            'max_nesting_depth': self.max_depth,
            'variables': sorted(list(self.variables)),
            'decorators': sorted(list(self.decorators)),
            'imports': self.imports,
            'line_count': len(source_lines)
        }


def analyze_code(source_code):
    """
    Analyze Python source code and return structural metrics.

    Args:
        source_code: String containing Python source code

    Returns:
        Dictionary with analysis results or error information
    """
    try:
        tree = ast.parse(source_code)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        source_lines = source_code.split('\n')
        return analyzer.get_analysis(source_lines)
    except SyntaxError as e:
        return {
            'error': True,
            'error_type': 'SyntaxError',
            'message': str(e),
            'line': e.lineno,
            'offset': e.offset
        }
    except Exception as e:
        return {
            'error': True,
            'error_type': type(e).__name__,
            'message': str(e)
        }


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) > 1:
        # Read from file
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(json.dumps({'error': True, 'message': f'File not found: {sys.argv[1]}'}))
            sys.exit(1)
        source_code = file_path.read_text(encoding='utf-8')
    else:
        # Read from stdin
        source_code = sys.stdin.read()

    if not source_code.strip():
        print(json.dumps({'error': True, 'message': 'No code provided'}))
        sys.exit(1)

    result = analyze_code(source_code)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
