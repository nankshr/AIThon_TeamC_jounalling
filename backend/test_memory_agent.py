"""Test script for Memory Agent (semantic search and RAG)."""

import asyncio
from app.agents.memory import MemoryAgent

# Sample entries with embeddings (mock data)
SAMPLE_ENTRIES = [
    {
        "id": "entry-1",
        "text": "Met with three caterers today. Mamma's Kitchen quoted $3000, Fresh & Modern quoted $2000, and Farm to Table quoted $2500. Wedding is June 15th.",
        "date": "2024-10-20",
        "embedding": [0.1] * 1536,  # Mock embedding
        "entities": {
            "vendors": [
                {
                    "name": "Mamma's Kitchen",
                    "category": "catering",
                    "cost": 3000,
                    "status": "pending",
                }
            ],
            "costs": [
                {"amount": 3000, "category": "catering"},
                {"amount": 2000, "category": "catering"},
                {"amount": 2500, "category": "catering"},
            ],
            "dates": [{"event": "wedding", "date": "2025-06-15"}],
        },
        "sentiment": {"emotion": "excited", "confidence": 0.85},
    },
    {
        "id": "entry-2",
        "text": "Booked the venue! It's perfect - beautiful garden, can fit 150 guests. Cost is $4000 for June 15. Now need to book photographer and florist.",
        "date": "2024-10-22",
        "embedding": [0.15] * 1536,  # Mock embedding
        "entities": {
            "vendors": [
                {"name": "Garden Venue", "category": "venue", "cost": 4000, "status": "booked"}
            ],
            "costs": [{"amount": 4000, "category": "venue"}],
            "dates": [{"event": "wedding", "date": "2025-06-15"}],
        },
        "sentiment": {"emotion": "happy", "confidence": 0.9},
    },
    {
        "id": "entry-3",
        "text": "Budget is becoming a concern. Total costs so far: $9500. Wedding budget is only $8000. Need to cut costs somewhere.",
        "date": "2024-10-25",
        "embedding": [0.2] * 1536,  # Mock embedding
        "entities": {
            "costs": [{"amount": 8000, "category": "total budget"}],
        },
        "sentiment": {"emotion": "stressed", "confidence": 0.88},
    },
    {
        "id": "entry-4",
        "text": "Only 2 months left! So much to do: book photographer, florist, finalize guest list, send invitations, choose menu, arrange transportation. Feeling overwhelmed.",
        "date": "2024-11-01",
        "embedding": [0.25] * 1536,  # Mock embedding
        "entities": {
            "dates": [{"event": "wedding", "date": "2025-06-15"}],
        },
        "tasks": {
            "explicit": [
                {"title": "Book photographer", "status": "pending", "priority": "high"},
                {"title": "Book florist", "status": "pending", "priority": "high"},
                {
                    "title": "Finalize guest list",
                    "status": "pending",
                    "priority": "medium",
                },
                {
                    "title": "Send invitations",
                    "status": "pending",
                    "priority": "high",
                },
                {"title": "Choose menu", "status": "pending", "priority": "medium"},
                {
                    "title": "Arrange transportation",
                    "status": "pending",
                    "priority": "low",
                },
            ]
        },
        "sentiment": {"emotion": "anxious", "confidence": 0.92},
    },
]


async def test_search():
    """Test semantic search functionality."""
    print("[INFO] Testing Memory Agent - Semantic Search")
    print("-" * 60)

    query = "finding caterers and comparing prices"

    try:
        results = await MemoryAgent.search_entries(query, SAMPLE_ENTRIES, top_k=3)

        print(f"[PASS] Search completed successfully")
        print(f"Query: {query}")
        print(f"Results: {len(results)} entries found\n")

        for i, result in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"  ID: {result['id']}")
            print(
                f"  Relevance Score: {result['relevance_score']:.2%}"
            )
            print(f"  Text: {result['text'][:80]}...")
            print(f"  Date: {result['date']}")
            print()

    except Exception as e:
        print(f"[ERROR] Search failed: {str(e)}")


async def test_contradictions():
    """Test contradiction detection."""
    print("[INFO] Testing Memory Agent - Contradiction Detection")
    print("-" * 60)

    try:
        contradictions = await MemoryAgent.find_contradictions(SAMPLE_ENTRIES)

        print(f"[PASS] Contradiction detection completed")
        print(f"Contradictions found: {len(contradictions)}\n")

        for i, contradiction in enumerate(contradictions, 1):
            print(f"Contradiction {i}:")
            print(f"  Type: {contradiction['type']}")
            print(f"  Severity: {contradiction['severity']}")
            print(f"  Description: {contradiction['description']}")
            print()

    except Exception as e:
        print(f"[ERROR] Contradiction detection failed: {str(e)}")


async def test_context_retrieval():
    """Test context retrieval for RAG."""
    print("[INFO] Testing Memory Agent - Context Retrieval for RAG")
    print("-" * 60)

    query = "What vendors have I been looking at for the wedding?"

    try:
        context = await MemoryAgent.retrieve_context(
            query, SAMPLE_ENTRIES, num_context=2
        )

        print(f"[PASS] Context retrieval completed")
        print(f"Query: {query}")
        print(f"Context length: {len(context)} characters\n")
        print("Context:\n")
        print(context)
        print()

    except Exception as e:
        print(f"[ERROR] Context retrieval failed: {str(e)}")


async def main():
    """Run all Memory Agent tests."""
    print("=" * 60)
    print("WEDDING JOURNAL - MEMORY AGENT TEST SUITE")
    print("=" * 60)
    print()

    await test_search()
    print()

    await test_contradictions()
    print()

    await test_context_retrieval()
    print()

    print("=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
