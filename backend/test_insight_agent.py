"""Test script for Insight Agent (recommendations and alerts)."""

import asyncio
from app.agents.insight import InsightAgent

# Sample entries for testing
SAMPLE_ENTRIES = [
    {
        "id": "entry-1",
        "text": "Met with caterers. Budget is $8000 total.",
        "date": "2024-10-20",
        "entities": {
            "vendors": [
                {"name": "Mamma's Kitchen", "category": "catering", "status": "pending"}
            ],
            "costs": [{"amount": 8000, "category": "total budget"}],
            "dates": [{"event": "wedding", "date": "2025-06-15"}],
        },
        "tasks": {
            "explicit": [
                {"title": "Book caterer", "status": "pending", "priority": "high"},
                {"title": "Confirm menu", "status": "pending", "priority": "medium"},
            ]
        },
        "sentiment": {"emotion": "excited", "confidence": 0.85},
        "themes": ["budget", "catering"],
    },
    {
        "id": "entry-2",
        "text": "Booked venue and photographer. Spent so far: $5200.",
        "date": "2024-10-25",
        "entities": {
            "vendors": [
                {"name": "Garden Venue", "category": "venue", "status": "booked"},
                {"name": "Photo Pro", "category": "photography", "status": "booked"},
            ],
            "costs": [
                {"amount": 4000, "category": "venue"},
                {"amount": 1200, "category": "photography"},
            ],
            "dates": [{"event": "wedding", "date": "2025-06-15"}],
        },
        "tasks": {
            "explicit": [
                {"title": "Book caterer", "status": "pending", "priority": "high"},
                {"title": "Confirm menu", "status": "pending", "priority": "medium"},
                {
                    "title": "Finalize guest list",
                    "status": "pending",
                    "priority": "high",
                },
                {"title": "Send invitations", "status": "pending", "priority": "high"},
            ]
        },
        "sentiment": {"emotion": "happy", "confidence": 0.9},
        "themes": ["budget", "progress", "excitement"],
    },
    {
        "id": "entry-3",
        "text": "Florist quoted $800, decorator quoted $1500. Feeling budget pressure.",
        "date": "2024-11-01",
        "entities": {
            "vendors": [
                {"name": "Bloom Flowers", "category": "flowers", "status": "pending"},
                {
                    "name": "Decoration Co",
                    "category": "decoration",
                    "status": "pending",
                },
            ],
            "costs": [
                {"amount": 800, "category": "flowers"},
                {"amount": 1500, "category": "decoration"},
            ],
            "dates": [{"event": "wedding", "date": "2025-06-15"}],
        },
        "tasks": {
            "explicit": [
                {"title": "Choose florist", "status": "pending", "priority": "high"},
                {"title": "Choose decorator", "status": "pending", "priority": "high"},
                {"title": "Book caterer", "status": "pending", "priority": "high"},
                {"title": "Confirm menu", "status": "pending", "priority": "medium"},
                {
                    "title": "Finalize guest list",
                    "status": "pending",
                    "priority": "high",
                },
                {"title": "Send invitations", "status": "pending", "priority": "high"},
                {
                    "title": "Arrange transportation",
                    "status": "pending",
                    "priority": "medium",
                },
            ]
        },
        "sentiment": {"emotion": "stressed", "confidence": 0.88},
        "themes": ["budget", "stress", "timeline"],
    },
]


async def test_detect_contradictions():
    """Test contradiction detection."""
    print("[INFO] Testing Insight Agent - Contradiction Detection")
    print("-" * 60)

    try:
        contradictions = await InsightAgent.detect_contradictions(SAMPLE_ENTRIES)

        print(f"[PASS] Contradiction detection completed")
        print(f"Contradictions found: {len(contradictions)}\n")

        if not contradictions:
            print("[INFO] No contradictions detected")
        else:
            for i, contradiction in enumerate(contradictions, 1):
                print(f"Contradiction {i}:")
                print(f"  Type: {contradiction['type']}")
                print(f"  Severity: {contradiction['severity']}")
                print(f"  Description: {contradiction['description']}")
                print()

    except Exception as e:
        print(f"[ERROR] Contradiction detection failed: {str(e)}")
        import traceback

        traceback.print_exc()


async def test_generate_insights():
    """Test insight generation."""
    print("[INFO] Testing Insight Agent - Generate Insights")
    print("-" * 60)

    try:
        insights = await InsightAgent.generate_insights(SAMPLE_ENTRIES)

        print(f"[PASS] Insight generation completed\n")

        # Print patterns
        if insights.get("patterns"):
            print("Patterns Detected:")
            for pattern in insights["patterns"]:
                print(f"  - {pattern['description']}")
            print()

        # Print sentiment trend
        if insights.get("sentiment_trend"):
            trend = insights["sentiment_trend"]
            print(f"Sentiment Trend:")
            print(f"  Dominant Emotion: {trend['dominant_emotion']}")
            print(f"  Count: {trend['count']}")
            print(f"  Trend: {trend['trend_description']}")
            print()

        # Print budget status
        if insights.get("budget_status"):
            budget = insights["budget_status"]
            print(f"Budget Status:")
            print(f"  Total Spent: ${budget['total_spent']:.2f}")
            print(f"  Largest Category: {budget['largest_category']} (${budget['largest_amount']:.2f})")
            print()

        # Print task summary
        if insights.get("task_summary"):
            tasks = insights["task_summary"]
            print(f"Task Summary:")
            print(f"  Total Tasks: {tasks['total_tasks']}")
            print(f"  Completed: {tasks['completed']}")
            print(f"  Pending: {tasks['pending']}")
            print(f"  Completion Rate: {tasks['completion_rate']:.1f}%")
            print(f"  High Priority: {tasks['high_priority']}")
            print()

        # Print recommendations
        if insights.get("recommendations"):
            print("Recommendations:")
            for i, rec in enumerate(insights["recommendations"], 1):
                print(f"  {i}. {rec.get('message', 'Unknown recommendation')}")
            print()

        # Print alerts
        if insights.get("alerts"):
            print("Alerts:")
            for i, alert in enumerate(insights["alerts"], 1):
                print(f"  {i}. [{alert['severity'].upper()}] {alert['message']}")
            print()

    except Exception as e:
        print(f"[ERROR] Insight generation failed: {str(e)}")
        import traceback

        traceback.print_exc()


async def test_get_next_steps():
    """Test next steps generation."""
    print("[INFO] Testing Insight Agent - Generate Next Steps")
    print("-" * 60)

    try:
        next_steps = await InsightAgent.get_next_steps(SAMPLE_ENTRIES)

        print(f"[PASS] Next steps generation completed")
        print(f"Next steps: {len(next_steps)}\n")

        if not next_steps:
            print("[INFO] No next steps generated")
        else:
            for i, step in enumerate(next_steps, 1):
                print(f"Step {i}:")
                print(f"  Priority: {step['priority'].upper()}")
                print(f"  Action: {step['action']}")
                if step.get("deadline"):
                    print(f"  Deadline: {step['deadline']}")
                if step.get("reason"):
                    print(f"  Reason: {step['reason']}")
                print()

    except Exception as e:
        print(f"[ERROR] Next steps generation failed: {str(e)}")
        import traceback

        traceback.print_exc()


async def main():
    """Run all Insight Agent tests."""
    print("=" * 60)
    print("WEDDING JOURNAL - INSIGHT AGENT TEST SUITE")
    print("=" * 60)
    print()

    await test_detect_contradictions()
    print()

    await test_generate_insights()
    print()

    await test_get_next_steps()
    print()

    print("=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
