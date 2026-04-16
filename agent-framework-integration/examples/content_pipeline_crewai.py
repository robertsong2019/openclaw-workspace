#!/usr/bin/env python3
"""
Content Creation Pipeline using CrewAI-style Orchestration

This example demonstrates a content creation workflow where:
1. Researcher agent finds trending topics
2. Writer agent creates articles
3. Editor agent reviews and polishes

Uses the OpenClaw CrewAI adapter.

Author: Catalyst
Date: 2026-04-13
"""

import asyncio
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from crewai.adapter import (
    OpenClawCrew,
    OpenClawAgentConfig,
    create_agent
)


async def main():
    print("="*70)
    print("Content Creation Pipeline - CrewAI-style Orchestration")
    print("="*70)
    print()

    # Create specialized agents
    researcher = OpenClawAgentConfig(
        name="Researcher",
        agent_type="codex",
        pty=True
    )

    writer = OpenClawAgentConfig(
        name="Writer",
        agent_type="claude"
    )

    editor = OpenClawAgentConfig(
        name="Editor",
        agent_type="pi"
    )

    # Create the crew
    crew = OpenClawCrew(
        name="Content Production Team",
        description="Research, write, and edit technical articles",
        verbose=True,
        max_rpm=5  # Conservative rate limit
    )

    # Define the workflow tasks
    crew.add_task(
        task_id="trend_research",
        description="Research the top 5 emerging AI trends for 2026. For each trend, provide: name, description, key players, and potential impact. Format as JSON.",
        agent_config=researcher,
        expected_output="JSON with 5 trend entries",
        output_file="output/trends.json"
    )

    crew.add_task(
        task_id="article_outline",
        description="Based on the research findings, create a detailed article outline. Include: catchy title, introduction structure, section headings, and conclusion points.",
        agent_config=writer,
        expected_output="Detailed article outline",
        depends_on=["trend_research"],
        output_file="output/outline.md"
    )

    crew.add_task(
        task_id="article_draft",
        description="Write a comprehensive 1500-word article following the outline. Make it engaging and accessible while maintaining technical accuracy. Include examples and data points.",
        agent_config=writer,
        expected_output="1500-word article in Markdown",
        depends_on=["article_outline"],
        output_file="output/draft.md"
    )

    crew.add_task(
        task_id="article_review",
        description="Review the article for: clarity, flow, accuracy, and engagement. Provide specific feedback and suggestions for improvement. Rate each section out of 10.",
        agent_config=editor,
        expected_output="Detailed review with scores and feedback",
        depends_on=["article_draft"],
        output_file="output/review.json"
    )

    crew.add_task(
        task_id="final_polish",
        description="Incorporate the editor's feedback and create the final polished version of the article. Ensure all issues are addressed and the article is publication-ready.",
        agent_config=writer,
        expected_output="Final publication-ready article",
        depends_on=["article_review"],
        output_file="output/final_article.md"
    )

    # Execute the crew
    print("\n" + "─"*70)
    print("Starting Content Production Pipeline")
    print("─"*70 + "\n")

    result = await crew.kickoff(
        inputs={"topic": "AI trends 2026"},
        process="sequential"  # Tasks execute in dependency order
    )

    # Display results
    print("\n" + "="*70)
    print("PIPELINE EXECUTION COMPLETE")
    print("="*70)

    print(f"\nStatus: {result['status'].upper()}")
    print(f"Total Time: {result['total_time']:.2f} seconds")
    print(f"\nTask Summary:")

    for task_id, task_result in result['tasks'].items():
        status_emoji = {
            "completed": "✅",
            "failed": "❌",
            "running": "⏳",
            "pending": "⏸️"
        }.get(task_result['status'], "❓")

        print(f"\n  {status_emoji} {task_id}")
        print(f"     Status: {task_result['status']}")
        print(f"     Duration: {task_result['duration']:.2f}s")

        if task_result['status'] == 'completed':
            # Show snippet of result
            result_text = task_result.get('result', '')
            if result_text:
                snippet = result_text[:200].replace('\n', ' ')
                print(f"     Output: {snippet}...")

    # Print output files
    print("\n" + "─"*70)
    print("Generated Files:")
    print("─"*70)

    output_files = [
        "output/trends.json",
        "output/outline.md",
        "output/draft.md",
        "output/review.json",
        "output/final_article.md"
    ]

    for filepath in output_files:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  ✓ {filepath} ({size} bytes)")
        else:
            print(f"  ✗ {filepath} (not found)")

    print("\n" + "="*70)
    print("Next Steps:")
    print("="*70)
    print("1. Review the final article in output/final_article.md")
    print("2. Check the editor's feedback in output/review.json")
    print("3. Make manual adjustments if needed")
    print("="*70 + "\n")

    return result


if __name__ == "__main__":
    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Run the pipeline
    result = asyncio.run(main())

    # Exit with appropriate code
    sys.exit(0 if result['status'] == 'completed' else 1)
