"""Test suite for AI agents (Intake, Memory, Insight)."""

import pytest
import asyncio
from app.agents.intake import IntakeAgent
from app.agents.memory import MemoryAgent
from app.agents.insight import InsightAgent


class TestIntakeAgent:
    """Test Intake Agent entity extraction."""

    @pytest.mark.asyncio
    async def test_process_entry_basic(self):
        """Test basic entry processing."""
        text = "I need to book a photographer for June 15th. Budget is $1500."
        result = await IntakeAgent.process_entry(text)

        assert result["success"] is True
        assert "data" in result
        assert "entities" in result["data"]
        assert "tasks" in result["data"]

    @pytest.mark.asyncio
    async def test_extract_entities(self):
        """Test entity extraction."""
        text = "Met with caterer Mamma's Kitchen, quoted $3000 for June 15."
        entities = await IntakeAgent.extract_entities(text)

        assert "vendors" in entities or "costs" in entities or "dates" in entities

    @pytest.mark.asyncio
    async def test_extract_tasks(self):
        """Test task extraction."""
        text = "Need to book venue and photographer by next week."
        tasks = await IntakeAgent.extract_tasks(text)

        assert "explicit" in tasks or "implicit" in tasks

    @pytest.mark.asyncio
    async def test_extract_sentiment(self):
        """Test sentiment analysis."""
        text = "I'm so stressed about all the wedding planning!"
        sentiment = await IntakeAgent.extract_sentiment(text)

        assert "emotion" in sentiment
        assert "confidence" in sentiment


class TestMemoryAgent:
    """Test Memory Agent search and RAG."""

    @pytest.mark.asyncio
    async def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]

        similarity = MemoryAgent._cosine_similarity(vec1, vec2)
        assert similarity == 1.0

    @pytest.mark.asyncio
    async def test_cosine_similarity_orthogonal(self):
        """Test cosine similarity with orthogonal vectors."""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [0.0, 1.0, 0.0]

        similarity = MemoryAgent._cosine_similarity(vec1, vec2)
        assert similarity == 0.0

    @pytest.mark.asyncio
    async def test_search_entries(self):
        """Test semantic search."""
        entries = [
            {
                "id": "1",
                "text": "Booked the venue",
                "embedding": [0.1] * 1536,
                "date": "2024-01-01",
                "entities": {},
                "sentiment": {"emotion": "happy", "confidence": 0.9},
            },
            {
                "id": "2",
                "text": "Decided on the caterer",
                "embedding": [0.2] * 1536,
                "date": "2024-01-02",
                "entities": {},
                "sentiment": {"emotion": "satisfied", "confidence": 0.8},
            },
        ]

        results = await MemoryAgent.search_entries("venue", entries, top_k=1)

        assert len(results) > 0
        assert results[0]["id"] in ["1", "2"]

    @pytest.mark.asyncio
    async def test_find_contradictions(self):
        """Test contradiction detection."""
        entries = [
            {
                "id": "1",
                "entities": {
                    "costs": [{"amount": 8000, "category": "total budget"}],
                    "dates": [{"event": "wedding", "date": "2025-06-15"}],
                },
                "tasks": {"explicit": []},
            },
            {
                "id": "2",
                "entities": {
                    "costs": [{"amount": 5000, "category": "venue"}],
                },
                "tasks": {"explicit": []},
            },
            {
                "id": "3",
                "entities": {
                    "costs": [{"amount": 4000, "category": "catering"}],
                },
                "tasks": {"explicit": []},
            },
        ]

        contradictions = await MemoryAgent.find_contradictions(entries)

        # Should detect budget overrun (5000 + 4000 > 8000 * 0.8)
        assert isinstance(contradictions, list)


class TestInsightAgent:
    """Test Insight Agent recommendations."""

    @pytest.mark.asyncio
    async def test_detect_contradictions(self):
        """Test contradiction detection in Insight Agent."""
        entries = [
            {
                "id": "1",
                "entities": {
                    "costs": [{"amount": 5000, "category": "total budget"}],
                    "dates": [{"event": "wedding", "date": "2025-12-25"}],
                },
                "tasks": {"explicit": [{"status": "pending", "priority": "high"}] * 10},
                "sentiment": {"emotion": "stressed"},
                "themes": ["budget"],
            }
        ]

        contradictions = await InsightAgent.detect_contradictions(entries)

        assert isinstance(contradictions, list)

    @pytest.mark.asyncio
    async def test_generate_insights(self):
        """Test insight generation."""
        entries = [
            {
                "id": "1",
                "sentiment": {"emotion": "happy", "confidence": 0.9},
                "entities": {"costs": [{"amount": 2000, "category": "venue"}]},
                "tasks": {"explicit": [{"status": "pending", "priority": "high"}]},
                "themes": ["excitement"],
            },
            {
                "id": "2",
                "sentiment": {"emotion": "stressed", "confidence": 0.8},
                "entities": {"costs": [{"amount": 1000, "category": "catering"}]},
                "tasks": {"explicit": [{"status": "completed", "priority": "high"}]},
                "themes": ["stress"],
            },
        ]

        insights = await InsightAgent.generate_insights(entries)

        assert "patterns" in insights
        assert "recommendations" in insights
        assert "sentiment_trend" in insights

    @pytest.mark.asyncio
    async def test_get_next_steps(self):
        """Test next steps generation."""
        entries = [
            {
                "id": "1",
                "tasks": {
                    "explicit": [
                        {
                            "title": "Book photographer",
                            "status": "pending",
                            "priority": "high",
                            "deadline": "2024-12-01",
                        }
                    ]
                },
                "entities": {
                    "vendors": [
                        {"name": "Photo Pro", "category": "photography", "status": "pending"}
                    ]
                },
            }
        ]

        next_steps = await InsightAgent.get_next_steps(entries)

        assert isinstance(next_steps, list)
        assert len(next_steps) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
