#!/usr/bin/env python3
"""
Test suite for Project Dashboard Generator
"""

import json
import subprocess
import sys
from pathlib import Path


def run_dashboard(*args):
    """Run dashboard with args and return output."""
    script_dir = Path(__file__).parent.parent  # Go up to project-dashboard/
    cmd = ['python3', str(script_dir / 'project_dashboard.py')] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def test_basic_scan():
    """Test basic workspace scan."""
    print("✓ Testing basic scan...")
    code, out, err = run_dashboard('projects/')
    assert code == 0, f"Failed: {err}"
    assert '# 📊 Project Dashboard' in out
    assert 'agent-task-cli' in out
    print("  ✓ Basic scan works")


def test_json_output():
    """Test JSON output format."""
    print("✓ Testing JSON output...")
    code, out, err = run_dashboard('projects/', '-f', 'json')
    assert code == 0, f"Failed: {err}"
    
    data = json.loads(out)
    assert 'summary' in data
    assert 'projects' in data
    assert len(data['projects']) > 0
    print("  ✓ JSON output works")


def test_health_filter():
    """Test minimum health score filter."""
    print("✓ Testing health score filter...")
    code, out, err = run_dashboard('projects/', '--min-health', '70')
    assert code == 0, f"Failed: {err}"
    
    # Should only show high-health projects
    code2, out2, err2 = run_dashboard('projects/', '-f', 'json', '--min-health', '70')
    data = json.loads(out2)
    
    for project in data['projects']:
        assert project['health_score'] >= 70, f"Low health project included: {project['name']}"
    print("  ✓ Health filter works")


def test_file_output():
    """Test output to file."""
    print("✓ Testing file output...")
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        output_path = f.name
    
    try:
        code, out, err = run_dashboard('projects/', '-o', output_path)
        assert code == 0, f"Failed: {err}"
        
        content = Path(output_path).read_text()
        assert '# 📊 Project Dashboard' in content
        print("  ✓ File output works")
    finally:
        Path(output_path).unlink(missing_ok=True)


def test_health_score_calculation():
    """Test health score calculation logic."""
    print("✓ Testing health score calculation...")
    code, out, err = run_dashboard('projects/', '-f', 'json')
    data = json.loads(out)
    
    for project in data['projects']:
        score = project['health_score']
        assert 0 <= score <= 100, f"Invalid score: {score}"
        
        # Verify score components
        has_docs = project['has_docs']
        has_tests = project['has_tests']
        
        # Projects with docs and tests should have decent scores
        if has_docs and has_tests and project['git_status'] == 'clean':
            assert score >= 60, f"Healthy project has low score: {project['name']} ({score})"
    
    print("  ✓ Health score calculation works")


def main():
    """Run all tests."""
    print("\n🧪 Running Project Dashboard Tests\n")
    print("=" * 50)
    
    tests = [
        test_basic_scan,
        test_json_output,
        test_health_filter,
        test_file_output,
        test_health_score_calculation,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"  ✗ Failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed += 1
    
    print("=" * 50)
    if failed == 0:
        print(f"\n✅ All {len(tests)} tests passed!\n")
        return 0
    else:
        print(f"\n❌ {failed}/{len(tests)} tests failed\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
