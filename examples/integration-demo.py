#!/usr/bin/env python3
"""
AI Agent Toolkit Integration Example

This script demonstrates how the various AI agent tools work together:
1. Context Generator - Creates AI-ready project summaries
2. Project Dashboard - Tracks project health and status
3. Memory Embedder - Provides semantic search for memories
4. Agent Task CLI - Orchestrates multi-agent tasks

Use case: Setting up a new AI agent project with full context awareness
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools/project-dashboard'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'experiments/local-embedding-memory'))

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def run_command(cmd, cwd=None):
    """Run a shell command and return output"""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr, result.returncode

def example_1_project_context():
    """Example 1: Generate context for a new AI agent project"""
    print_section("Example 1: Generate Project Context for AI Agent")
    
    workspace = Path(__file__).parent.parent
    
    # Simulate generating context for agent-task-cli project
    project_path = workspace / 'projects/agent-task-cli'
    
    print(f"📁 Analyzing project: {project_path.name}")
    print(f"🎯 Purpose: Create AI-ready context for onboarding new AI assistants\n")
    
    # In a real scenario, this would call context_gen.py
    context = {
        'project': project_path.name,
        'language': 'JavaScript/TypeScript',
        'purpose': 'Multi-agent task orchestration CLI',
        'key_files': [
            'src/index.js - Main entry point',
            'src/orchestrator.js - Task orchestration logic',
            'src/patterns/ - Different orchestration patterns',
            'bin/agent-task.js - CLI executable'
        ],
        'dependencies': ['commander', 'chalk', 'ora', 'js-yaml', 'uuid'],
        'entry_points': ['bin/agent-task.js'],
        'ai_onboarding_prompt': f"""
This is a {project_path.name} project - a CLI tool for orchestrating multi-agent tasks.

Key capabilities:
- Multiple orchestration patterns (Work Crew, Supervisor, Pipeline, Council, Auto-Routing)
- YAML/JSON task definition
- Real-time monitoring
- Export results in JSON/Markdown

When helping with this project:
1. Check src/patterns/ for orchestration implementations
2. Look at examples/ for usage patterns
3. Run tests with: npm test
4. Execute with: ./bin/agent-task.js run <task-file>
"""
    }
    
    print("✅ Generated context:")
    print(json.dumps(context, indent=2))
    
    return context

def example_2_project_health():
    """Example 2: Check project health using dashboard"""
    print_section("Example 2: Project Health Dashboard")
    
    workspace = Path(__file__).parent.parent
    
    print("📊 Scanning workspace for project health...\n")
    
    # Run dashboard tool
    stdout, stderr, code = run_command(
        'python3 tools/project-dashboard/project_dashboard.py projects -f json',
        cwd=workspace
    )
    
    if code == 0:
        data = json.loads(stdout)
        
        summary = data.get('summary', {})
        print(f"Total Projects: {summary.get('total_projects', len(data.get('projects', [])))}")
        print(f"Average Health: {summary.get('avg_health', 'N/A')}\n")
        
        print("Project Health Scores:")
        for project in data.get('projects', []):
            health_emoji = '🟢' if project['health_score'] >= 70 else '🟡' if project['health_score'] >= 50 else '🔴'
            print(f"  {health_emoji} {project['name']}: {project['health_score']}/100")
            print(f"     Language: {project['language']}")
            print(f"     Tests: {'✅' if project['has_tests'] else '❌'}")
            print(f"     Docs: {'✅' if project['has_docs'] else '❌'}")
            print()
        
        # Identify projects needing attention
        needs_attention = [p for p in data.get('projects', []) if p['health_score'] < 70]
        if needs_attention:
            print("⚠️  Projects needing attention:")
            for p in needs_attention:
                print(f"   - {p['name']} (health: {p['health_score']})")
    
    return data if code == 0 else None

def example_3_semantic_memory_search():
    """Example 3: Search memories semantically"""
    print_section("Example 3: Semantic Memory Search")
    
    workspace = Path(__file__).parent.parent
    memory_dir = workspace / 'memory'
    
    print(f"🧠 Searching memories in: {memory_dir}")
    print("🔍 Query: 'AI agent architecture patterns'\n")
    
    # In a real scenario, this would use memory_embedder.py
    # For demo, we'll simulate semantic search results
    
    mock_results = [
        {
            'file': 'memory/2026-03-21.md',
            'section': 'AI Agent 架构设计',
            'relevance': 0.89,
            'preview': 'Based on Anthropic "Building Effective AI Agents" - workflows vs agents...'
        },
        {
            'file': 'memory/2026-03-22.md',
            'section': 'Project Context Generator',
            'relevance': 0.82,
            'preview': 'AI-ready context summaries for agent onboarding...'
        },
        {
            'file': 'memory/2026-03-22-dashboard-tool.md',
            'section': 'Project Dashboard Generator',
            'relevance': 0.76,
            'preview': 'Multi-project health tracking for AI agent development...'
        }
    ]
    
    print("Top Semantic Search Results:\n")
    for i, result in enumerate(mock_results, 1):
        print(f"{i}. [{result['relevance']:.2f}] {result['file']}")
        print(f"   Section: {result['section']}")
        print(f"   Preview: {result['preview'][:100]}...")
        print()
    
    return mock_results

def example_4_integrated_workflow():
    """Example 4: Complete integrated workflow"""
    print_section("Example 4: Integrated AI Agent Development Workflow")
    
    print("Scenario: Starting work on a new AI agent feature\n")
    
    workflow_steps = [
        {
            'step': 1,
            'tool': 'Project Dashboard',
            'action': 'Check current project health',
            'output': 'Identify prompt-mgr (85/100) and agent-task-cli (65/100) as active projects'
        },
        {
            'step': 2,
            'tool': 'Context Generator',
            'action': 'Generate context for target project',
            'output': 'Create AI-ready summary of agent-task-cli for assistant onboarding'
        },
        {
            'step': 3,
            'tool': 'Memory Embedder',
            'action': 'Search for relevant past work',
            'output': 'Find memories about multi-agent patterns and orchestration'
        },
        {
            'step': 4,
            'tool': 'Agent Task CLI',
            'action': 'Orchestrate multi-agent implementation',
            'output': 'Use Work Crew pattern to get multiple perspectives on feature design'
        },
        {
            'step': 5,
            'tool': 'Dashboard (re-scan)',
            'action': 'Verify improvements',
            'output': 'Confirm health score improved after adding tests and docs'
        }
    ]
    
    print("Integrated Workflow Steps:\n")
    for step in workflow_steps:
        print(f"Step {step['step']}: {step['tool']}")
        print(f"  Action: {step['action']}")
        print(f"  Output: {step['output']}")
        print()
    
    return workflow_steps

def example_5_rapid_prototyping():
    """Example 5: Rapid prototyping with the toolkit"""
    print_section("Example 5: Rapid AI Agent Prototyping")
    
    print("Goal: Quickly prototype a new AI agent feature\n")
    
    prototype_workflow = {
        'name': 'Agent Memory Plugin',
        'estimated_time': '2 hours',
        'steps': [
            {
                'phase': 'Setup (15 min)',
                'tools': ['Context Generator'],
                'tasks': [
                    'Generate context for local-embedding-memory project',
                    'Understand current API and architecture',
                    'Identify integration points'
                ]
            },
            {
                'phase': 'Design (30 min)',
                'tools': ['Memory Embedder', 'Agent Task CLI'],
                'tasks': [
                    'Search memories for similar plugin patterns',
                    'Use Council pattern to get design feedback',
                    'Define plugin interface'
                ]
            },
            {
                'phase': 'Implementation (60 min)',
                'tools': ['Context Generator', 'Memory Embedder'],
                'tasks': [
                    'Implement plugin following generated context',
                    'Reference semantic search results for patterns',
                    'Add tests and documentation'
                ]
            },
            {
                'phase': 'Validation (15 min)',
                'tools': ['Project Dashboard'],
                'tasks': [
                    'Run health check on updated project',
                    'Verify test coverage',
                    'Confirm documentation complete'
                ]
            }
        ]
    }
    
    print(f"Prototype: {prototype_workflow['name']}")
    print(f"Estimated Time: {prototype_workflow['estimated_time']}\n")
    
    for step in prototype_workflow['steps']:
        print(f"{step['phase']}:")
        print(f"  Tools: {', '.join(step['tools'])}")
        print(f"  Tasks:")
        for task in step['tasks']:
            print(f"    - {task}")
        print()
    
    return prototype_workflow

def main():
    """Run all integration examples"""
    print("\n" + "="*70)
    print("  AI AGENT TOOLKIT - INTEGRATION DEMONSTRATION")
    print("="*70)
    print("\nThis demo shows how AI agent development tools work together")
    print("for rapid prototyping and embedded AI applications.\n")
    
    # Run all examples
    context = example_1_project_context()
    health = example_2_project_health()
    memories = example_3_semantic_memory_search()
    workflow = example_4_integrated_workflow()
    prototype = example_5_rapid_prototyping()
    
    # Summary
    print_section("Summary")
    
    print("✅ Demonstrated 5 integration scenarios:")
    print("   1. Project context generation for AI onboarding")
    print("   2. Multi-project health monitoring")
    print("   3. Semantic memory search for knowledge retrieval")
    print("   4. Integrated development workflow")
    print("   5. Rapid prototyping process\n")
    
    print("🎯 Key Benefits:")
    print("   • Faster AI agent onboarding with auto-generated context")
    print("   • Proactive project health tracking")
    print("   • Semantic knowledge retrieval vs. keyword search")
    print("   • Structured multi-agent coordination")
    print("   • Rapid prototyping with integrated toolchain\n")
    
    print("💡 Next Steps:")
    print("   1. Try each tool individually")
    print("   2. Integrate into your AI agent development workflow")
    print("   3. Customize for your specific use cases")
    print("   4. Extend with additional patterns and features\n")
    
    print("="*70)
    print("  For more information, see:")
    print("  - tools/project-dashboard/README.md")
    print("  - experiments/local-embedding-memory/README.md")
    print("  - projects/agent-task-cli/README.md")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
