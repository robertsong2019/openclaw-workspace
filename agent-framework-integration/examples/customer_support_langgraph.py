#!/usr/bin/env python3
"""
Customer Support Triage System using LangGraph-style Orchestration

This example demonstrates a customer support workflow where:
1. Classify the issue type
2. Route to appropriate specialist
3. Resolve or escalate as needed
4. Follow up with customer

Uses the OpenClaw LangGraph adapter with state management and conditional routing.

Author: Catalyst
Date: 2026-04-13
"""

import asyncio
import json
import sys
import os
from typing import TypedDict, Literal

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from langgraph.adapter import (
    StateGraph,
    create_openclaw_node,
    START,
    END
)


# Define state types
class SupportState(TypedDict, total=False):
    customer_id: str
    issue_description: str
    issue_type: Literal["technical", "billing", "feature", "other"]
    classification_confidence: float
    resolution: str
    escalation_needed: bool
    follow_up_sent: bool
    done: bool
    step: int
    messages: list


async def main():
    print("="*70)
    print("Customer Support Triage System - LangGraph-style Orchestration")
    print("="*70)
    print()

    # Build the state graph
    graph = StateGraph(SupportState)

    # Node 1: Classify the issue
    def classify_issue(state: SupportState) -> dict:
        """Classify the customer issue"""
        issue = state.get("issue_description", "").lower()

        # Simple classification logic
        if any(word in issue for word in ["bug", "error", "crash", "not working", "broken"]):
            issue_type = "technical"
            confidence = 0.9
        elif any(word in issue for word in ["bill", "charge", "payment", "refund", "cost"]):
            issue_type = "billing"
            confidence = 0.95
        elif any(word in issue for word in ["feature", "request", "add", "new", "would like"]):
            issue_type = "feature"
            confidence = 0.85
        else:
            issue_type = "other"
            confidence = 0.6

        print(f"\n🔍 Classified issue as: {issue_type} (confidence: {confidence})")

        return {
            "issue_type": issue_type,
            "classification_confidence": confidence
        }

    # Node 2: Technical support
    technical_node = create_openclaw_node(
        name="technical_support",
        prompt_template="Help with this technical issue: {task}. Provide step-by-step troubleshooting.",
        agent_type="codex"
    )

    # Node 3: Billing support
    billing_node = create_openclaw_node(
        name="billing_support",
        prompt_template="Handle this billing inquiry: {task}. Check account status and explain charges.",
        agent_type="claude"
    )

    # Node 4: Feature request handler
    feature_node = create_openclaw_node(
        name="feature_handler",
        prompt_template="Process this feature request: {task}. Summarize the request and assess feasibility.",
        agent_type="pi"
    )

    # Node 5: General support
    general_node = create_openclaw_node(
        name="general_support",
        prompt_template="Help with this inquiry: {task}. Provide helpful and friendly assistance.",
        agent_type="claude"
    )

    # Node 6: Determine if escalation is needed
    def check_escalation(state: SupportState) -> dict:
        """Check if issue needs escalation"""
        # Check for escalation indicators
        messages = state.get("messages", [])

        # If resolution is empty or too short, might need escalation
        resolution = state.get("resolution", "")
        needs_escalation = len(resolution) < 50 or "escalate" in resolution.lower()

        print(f"\n⚠️  Escalation check: {'NEEDED' if needs_escalation else 'NOT NEEDED'}")

        return {"escalation_needed": needs_escalation}

    # Node 7: Escalate to senior support
    escalation_node = create_openclaw_node(
        name="escalation",
        prompt_template="ESCALATION NEEDED. Handle this complex issue that requires senior support: {task}",
        agent_type="codex"
    )

    # Node 8: Send follow-up
    def send_follow_up(state: SupportState) -> dict:
        """Send follow-up message to customer"""
        print("\n📧 Sending follow-up email to customer...")

        # In real implementation, this would send an actual email
        follow_up_message = f"""
Thank you for contacting support.

Your issue ({state.get('issue_type')}) has been processed.
Resolution: {state.get('resolution', 'See above')[:100]}...

If you need further assistance, please reply to this email.

Best regards,
Support Team
"""

        print("✓ Follow-up sent")
        print(f"\nMessage preview:\n{follow_up_message[:200]}...")

        return {"follow_up_sent": True}

    # Add all nodes to the graph
    graph.add_node("classify", classify_issue)
    graph.add_node("technical", technical_node)
    graph.add_node("billing", billing_node)
    graph.add_node("feature", feature_node)
    graph.add_node("general", general_node)
    graph.add_node("check_escalation", check_escalation)
    graph.add_node("escalation", escalation_node)
    graph.add_node("follow_up", send_follow_up)

    # Build the workflow edges

    # Start with classification
    graph.add_edge(START, "classify")

    # Route based on issue type
    def route_by_issue_type(state: SupportState) -> str:
        return state.get("issue_type", "general")

    graph.add_conditional_edges(
        "classify",
        route_by_issue_type,
        {
            "technical": "technical",
            "billing": "billing",
            "feature": "feature",
            "other": "general"
        }
    )

    # After handling, check if escalation is needed
    graph.add_edge("technical", "check_escalation")
    graph.add_edge("billing", "check_escalation")
    graph.add_edge("feature", "check_escalation")
    graph.add_edge("general", "check_escalation")

    # Route based on escalation decision
    def route_by_escalation(state: SupportState) -> str:
        return "escalation" if state.get("escalation_needed") else "follow_up"

    graph.add_conditional_edges(
        "check_escalation",
        route_by_escalation,
        {
            "escalation": "escalation",
            "follow_up": "follow_up"
        }
    )

    # Escalation goes to follow-up after resolution
    graph.add_edge("escalation", "follow_up")

    # End at follow-up
    graph.add_edge("follow_up", END)

    # Compile the graph
    compiled = graph.compile()

    # Test cases
    test_cases = [
        {
            "name": "Technical Issue",
            "state": {
                "customer_id": "CUST-001",
                "issue_description": "My app keeps crashing when I try to upload images. Error: 'Unexpected token < in JSON'",
                "messages": [],
                "step": 0
            }
        },
        {
            "name": "Billing Issue",
            "state": {
                "customer_id": "CUST-002",
                "issue_description": "I was charged $99 but I only have the basic plan which should be $29",
                "messages": [],
                "step": 0
            }
        },
        {
            "name": "Feature Request",
            "state": {
                "customer_id": "CUST-003",
                "issue_description": "I would like to request dark mode support for the mobile app",
                "messages": [],
                "step": 0
            }
        }
    ]

    # Run test cases
    for i, test_case in enumerate(test_cases, 1):
        print("\n" + "="*70)
        print(f"TEST CASE {i}/{len(test_cases)}: {test_case['name']}")
        print("="*70)
        print(f"Customer: {test_case['state']['customer_id']}")
        print(f"Issue: {test_case['state']['issue_description']}")
        print("-"*70)

        result = await compiled.invoke(test_case['state'])

        print("\n" + "─"*70)
        print("RESULT SUMMARY")
        print("─"*70)
        print(f"Issue Type: {result.get('issue_type', 'N/A')}")
        print(f"Classification Confidence: {result.get('classification_confidence', 0):.2f}")
        print(f"Escalation Needed: {'Yes' if result.get('escalation_needed') else 'No'}")
        print(f"Follow-up Sent: {'Yes' if result.get('follow_up_sent') else 'No'}")
        print(f"Total Steps: {result.get('step', 0)}")

        # Show resolution snippet
        resolution = result.get("resolution", "")
        if resolution:
            print(f"\nResolution Preview:")
            print(f"  {resolution[:200]}...")

        # Show messages
        messages = result.get("messages", [])
        if messages:
            print(f"\nAgent Messages ({len(messages)}):")
            for j, msg in enumerate(messages[-3:], 1):  # Show last 3 messages
                print(f"  {j}. {msg[:100]}...")

        print()

    print("="*70)
    print("All test cases completed!")
    print("="*70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Conditional routing based on issue type")
    print("  ✓ Different agents for different issue types")
    print("  ✓ Escalation logic with conditional edges")
    print("  ✓ State management across the workflow")
    print("  ✓ Follow-up automation")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
