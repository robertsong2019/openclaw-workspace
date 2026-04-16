#!/usr/bin/env python3
"""
Unit tests for the Python AST analyzer.
"""

import ast
import json
import sys
import unittest
from pathlib import Path

# Add the scripts directory to the path
scripts_dir = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(scripts_dir))

from analyze import CodeAnalyzer, analyze_code


class TestBasicFunctionAnalysis(unittest.TestCase):
    """Test basic function analysis."""

    def test_simple_function(self):
        """Test analysis of a simple function."""
        code = """
def greet(name):
    return f"Hello, {name}!"
"""
        result = analyze_code(code)

        self.assertFalse(result.get('error'))
        self.assertEqual(len(result['functions']), 1)
        self.assertEqual(result['functions'][0]['name'], 'greet')
        self.assertEqual(result['functions'][0]['args'], ['name'])
        self.assertEqual(result['loops'], 0)
        self.assertGreater(result['line_count'], 0)

    def test_function_with_decorator(self):
        """Test function with decorator."""
        code = """
@staticmethod
def helper():
    pass
"""
        result = analyze_code(code)

        self.assertFalse(result.get('error'))
        self.assertEqual(len(result['functions']), 1)
        self.assertIn('staticmethod', result['decorators'])


class TestClassAndMethodAnalysis(unittest.TestCase):
    """Test class and method analysis."""

    def test_simple_class(self):
        """Test analysis of a simple class."""
        code = """
class Calculator:
    def add(self, a, b):
        return a + b
"""
        result = analyze_code(code)

        self.assertFalse(result.get('error'))
        self.assertEqual(len(result['classes']), 1)
        self.assertEqual(result['classes'][0]['name'], 'Calculator')
        self.assertEqual(len(result['functions']), 1)
        self.assertEqual(result['functions'][0]['name'], 'add')

    def test_class_with_inheritance(self):
        """Test class with base classes."""
        code = """
class Dog(Animal):
    def bark(self):
        return "Woof!"
"""
        result = analyze_code(code)

        self.assertFalse(result.get('error'))
        self.assertEqual(len(result['classes']), 1)
        self.assertEqual(result['classes'][0]['name'], 'Dog')
        self.assertIn('Animal', result['classes'][0]['bases'])


class TestNestedStructures(unittest.TestCase):
    """Test nested code structures."""

    def test_nested_loops(self):
        """Test analysis of nested loops."""
        code = """
def matrix_multiply(A, B):
    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            sum_val = 0
            for k in range(len(B)):
                sum_val += A[i][k] * B[k][j]
            row.append(sum_val)
        result.append(row)
    return result
"""
        result = analyze_code(code)

        self.assertFalse(result.get('error'))
        self.assertEqual(result['loops'], 3)
        self.assertGreater(result['max_nesting_depth'], 1)

    def test_nested_conditionals(self):
        """Test analysis of nested conditionals."""
        code = """
def categorize(x):
    if x > 0:
        if x < 10:
            return "small"
        else:
            return "large"
    else:
        return "negative"
"""
        result = analyze_code(code)

        self.assertFalse(result.get('error'))
        self.assertGreaterEqual(result['conditionals'], 2)
        self.assertGreater(result['max_nesting_depth'], 1)


class TestSyntaxErrorHandling(unittest.TestCase):
    """Test handling of syntax errors."""

    def test_invalid_syntax(self):
        """Test analysis of invalid Python code."""
        code = """
def broken(
    # Missing closing parenthesis
    return 1
"""
        result = analyze_code(code)

        self.assertTrue(result.get('error'))
        self.assertEqual(result['error_type'], 'SyntaxError')
        self.assertIn('message', result)

    def test_empty_code(self):
        """Test analysis of empty code."""
        result = analyze_code("")

        # Empty code is valid Python, just has no structure
        self.assertFalse(result.get('error'))
        self.assertEqual(result['line_count'], 1)


class TestVariableAndImportTracking(unittest.TestCase):
    """Test variable and import tracking."""

    def test_variable_detection(self):
        """Test variable name extraction."""
        code = """
def process():
    x = 1
    y = 2
    result = x + y
    return result
"""
        result = analyze_code(code)

        self.assertFalse(result.get('error'))
        # Should detect variables assigned to
        self.assertIn('x', result['variables'])
        self.assertIn('y', result['variables'])
        self.assertIn('result', result['variables'])

    def test_import_tracking(self):
        """Test import statement tracking."""
        code = """
import os
import sys
from pathlib import Path
from typing import List, Dict
"""
        result = analyze_code(code)

        self.assertFalse(result.get('error'))
        self.assertIn('os', result['imports'])
        self.assertIn('sys', result['imports'])
        self.assertIn('pathlib.Path', result['imports'])
        self.assertIn('typing.List', result['imports'])


class TestCLIBasicFunctionality(unittest.TestCase):
    """Test basic CLI functionality."""

    def test_analyzer_script_exists(self):
        """Test that the analyzer script can be imported."""
        from analyze import analyze_code
        self.assertTrue(callable(analyze_code))

    def test_fibonacci_analysis(self):
        """Test analysis of a well-known algorithm."""
        code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""
        result = analyze_code(code)

        self.assertFalse(result.get('error'))
        self.assertEqual(len(result['functions']), 1)
        self.assertEqual(result['functions'][0]['name'], 'fibonacci')
        self.assertGreater(result['conditionals'], 0)


if __name__ == '__main__':
    unittest.main()
