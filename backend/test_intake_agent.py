#!/usr/bin/env python3
"""Test script for Intake Agent with OpenAI LLM."""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.agents.intake import IntakeAgent


async def main():
    """Test the Intake Agent with sample journal entries."""

    print("=" * 70)
    print("Intake Agent Test - OpenAI LLM")
    print("=" * 70)

    # Sample journal entry 1: Vendor selection
    sample_entry_1 = """
    Had a great meeting with three potential caterers today!

    1. Mamma's Kitchen - $3000 for 100 guests, they specialize in Indian cuisine,
       very enthusiastic but a bit pricey
    2. Fresh & Modern Catering - $2000 for 100 guests, modern menu, good reviews,
       need to confirm their vegetarian options
    3. Local Farm to Table - $2500 for 100 guests, eco-friendly approach which
       we love! They're available on our date.

    Still need to decide which one. Also need to book the photographer soon because
    the popular ones are getting booked. Feeling stressed about budget - our total
    is $30,000 and we're already spending $20,000. Need to talk to Mom about this.

    Wedding date is June 15, 2025.
    """

    print("\n[Test 1] Vendor Selection Entry")
    print("-" * 70)
    print("Input:", sample_entry_1[:100] + "...")

    result_1 = await IntakeAgent.process_entry(sample_entry_1, language="en")

    if result_1["success"]:
        print("\n[OK] Processing successful!")
        data = result_1["data"]

        print("\n[ENTITIES] Extracted Entities:")
        print(f"  Vendors: {len(data.get('entities', {}).get('vendors', []))} found")
        for vendor in data.get("entities", {}).get("vendors", []):
            print(
                f"    - {vendor.get('name')}: {vendor.get('category')} "
                f"(${vendor.get('cost')}, {vendor.get('status')})"
            )

        print(f"\n[DATES] Dates: {len(data.get('entities', {}).get('dates', []))} found")
        for date in data.get("entities", {}).get("dates", []):
            print(f"    - {date.get('event')}: {date.get('date')}")

        print(f"\n[COSTS] Costs: {len(data.get('entities', {}).get('costs', []))} found")
        for cost in data.get("entities", {}).get("costs", []):
            print(
                f"    - {cost.get('category')}: {cost.get('amount')} {cost.get('currency')}"
            )

        print("\n[TASKS] Tasks:")
        explicit = data.get("tasks", {}).get("explicit", [])
        implicit = data.get("tasks", {}).get("implicit", [])
        print(f"  Explicit: {len(explicit)} tasks")
        for task in explicit[:3]:
            print(f"    - {task.get('task')} (priority: {task.get('priority')})")
        print(f"  Implicit: {len(implicit)} tasks")
        for task in implicit[:2]:
            print(f"    - {task.get('task')} ({task.get('reason')})")

        print("\n[SENTIMENT]", data.get("sentiment"))
        print("[TIMELINE]", data.get("timeline"))
        print("[SUMMARY]", data.get("summary"))

        print(f"\n[TOKENS] Tokens used: {result_1.get('tokens_used')}")

    else:
        print(f"\n[ERROR] Processing failed: {result_1.get('error')}")

    # Sample journal entry 2: Task-heavy entry
    sample_entry_2 = """
    So much to do! I'm getting overwhelmed. Here's what I still need to handle:

    BEFORE THE WEDDING (June 15):
    - Finalize guest list (deadline: this week!)
    - Send invitations (we're already 2 weeks behind)
    - Confirm catering (need final headcount by June 1)
    - Book photographer (keep calling, no answer)
    - Get wedding dress tailored (already have it but needs alterations)
    - Arrange transportation for guests from the airport
    - Book honeymoon flights to Europe
    - Register for gifts on Amazon
    - Break in wedding shoes (can't walk in these!)
    - Practice wedding vows with my partner
    - Coordinate with florist about decorations
    - Schedule pre-wedding photoshoot
    - Get hair and makeup trial done
    - Brief the wedding party about their responsibilities

    I'm so stressed. Why is wedding planning this hard? My partner keeps saying
    "don't worry, it'll be fine" but I'm the one doing all the work!

    Budget concerns: we've already spent $18,000 and haven't paid for venue yet.
    That's over budget already and we haven't even gotten to the reception!
    """

    print("\n" + "=" * 70)
    print("\n[Test 2] Task-Heavy Entry")
    print("-" * 70)
    print("Input:", sample_entry_2[:100] + "...")

    result_2 = await IntakeAgent.process_entry(sample_entry_2, language="en")

    if result_2["success"]:
        print("\n[OK] Processing successful!")
        data = result_2["data"]

        print("\n[TASKS] Tasks Extracted:")
        explicit = data.get("tasks", {}).get("explicit", [])
        implicit = data.get("tasks", {}).get("implicit", [])

        print(f"  Explicit Tasks: {len(explicit)}")
        for task in explicit[:5]:
            deadline = (
                f" (deadline: {task.get('deadline')})"
                if task.get("deadline")
                else ""
            )
            print(
                f"    - {task.get('task')} - {task.get('priority')}{deadline}"
            )
        if len(explicit) > 5:
            print(f"    ... and {len(explicit) - 5} more")

        print(f"\n  Implicit Tasks: {len(implicit)}")
        for task in implicit[:3]:
            print(f"    - {task.get('task')}")
            print(f"      Reason: {task.get('reason')}")

        print("\n[THEMES] Themes:", data.get("themes", []))
        print("[SENTIMENT]", data.get("sentiment"))

        print(f"\n[TOKENS] Tokens used: {result_2.get('tokens_used')}")

    else:
        print(f"\n[ERROR] Processing failed: {result_2.get('error')}")

    print("\n" + "=" * 70)
    print("[OK] Intake Agent tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
