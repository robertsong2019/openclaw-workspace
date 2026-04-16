#!/usr/bin/env python3
"""
Example: AI Agent Integration with Project Dashboard

This script demonstrates how AI agents can use the project dashboard
to understand workspace status and make decisions.
"""

import json
import subprocess
from pathlib import Path


def get_dashboard_json(workspace_path: str) -> dict:
    """Get project dashboard as JSON."""
    script_dir = Path(__file__).parent
    result = subprocess.run(
        ['python3', str(script_dir / 'project_dashboard.py'), 
         workspace_path, '-f', 'json'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Dashboard generation failed: {result.stderr}")
    
    return json.loads(result.stdout)


def generate_ai_context(dashboard: dict) -> str:
    """Generate AI-friendly context string."""
    lines = [
        f"Workspace has {dashboard['summary']['total_projects']} projects.",
        f"Average health score: {dashboard['summary']['avg_health_score']}/100.",
        f"{dashboard['summary']['with_tests']}/{dashboard['summary']['total_projects']} have tests.",
        f"{dashboard['summary']['with_docs']}/{dashboard['summary']['total_projects']} have documentation.",
    ]
    
    # Find projects needing attention
    low_health = [p for p in dashboard['projects'] if p['health_score'] < 50]
    if low_health:
        lines.append(f"\nProjects needing attention: {', '.join(p['name'] for p in low_health)}")
        for p in low_health:
            issues = []
            if not p['has_tests']:
                issues.append('no tests')
            if not p['has_docs']:
                issues.append('no docs')
            if p['git_status'] == 'dirty':
                issues.append('uncommitted changes')
            lines.append(f"  - {p['name']}: {', '.join(issues)}")
    
    return " ".join(lines)


def suggest_actions(dashboard: dict) -> list[str]:
    """Suggest actions based on dashboard analysis."""
    suggestions = []
    
    for project in dashboard['projects']:
        if project['health_score'] < 50:
            if not project['has_tests']:
                suggestions.append(f"Add tests to {project['name']} (currently 0% test coverage)")
            if not project['has_docs']:
                suggestions.append(f"Add README.md to {project['name']}")
            if project['git_status'] == 'dirty':
                suggestions.append(f"Commit or stash changes in {project['name']}")
        
        if project['todo_count'] > 10:
            suggestions.append(f"Address {project['todo_count']} TODOs in {project['name']}")
    
    return suggestions


def main():
    """Demo AI agent workflow."""
    workspace = input("Enter workspace path (or press Enter for current): ").strip() or "."
    
    print("\n🔍 Scanning workspace...")
    dashboard = get_dashboard_json(workspace)
    
    print("\n📊 Dashboard Summary:")
    print(f"  Projects: {dashboard['summary']['total_projects']}")
    print(f"  Total files: {dashboard['summary']['total_files']:,}")
    print(f"  Total lines: {dashboard['summary']['total_lines']:,}")
    print(f"  Avg health: {dashboard['summary']['avg_health_score']}/100")
    
    print("\n🤖 AI Context:")
    print(generate_ai_context(dashboard))
    
    print("\n💡 Suggested Actions:")
    suggestions = suggest_actions(dashboard)
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    else:
        print("  All projects are healthy! ✨")
    
    # Save dashboard for later use
    output_file = Path(workspace) / "dashboard-data.json"
    with open(output_file, 'w') as f:
        json.dump(dashboard, f, indent=2)
    print(f"\n💾 Dashboard saved to {output_file}")


if __name__ == "__main__":
    main()
