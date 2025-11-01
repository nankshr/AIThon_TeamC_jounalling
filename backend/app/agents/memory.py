"""Memory Agent - Semantic search and RAG using vector embeddings."""

import logging
from typing import Optional
from app.services.embeddings import EmbeddingsService

logger = logging.getLogger(__name__)


class MemoryAgent:
    """Agent for semantic search and retrieval-augmented generation."""

    @staticmethod
    async def search_entries(
        query: str,
        entries: list[dict],
        top_k: int = 5,
    ) -> list[dict]:
        """
        Search journal entries using semantic similarity.

        Args:
            query: Search query text
            entries: List of journal entries with embeddings
            top_k: Number of top results to return

        Returns:
            List of matching entries ranked by relevance
        """
        try:
            logger.info(f"Searching {len(entries)} entries for: {query}")

            # Generate embedding for query
            query_embedding = await EmbeddingsService.embed_text(query)

            # Calculate similarity scores using cosine similarity
            results = []
            for entry in entries:
                if "embedding" not in entry:
                    logger.warning(f"Entry {entry.get('id')} missing embedding, skipping")
                    continue

                similarity = MemoryAgent._cosine_similarity(
                    query_embedding, entry["embedding"]
                )

                results.append(
                    {
                        "id": entry.get("id"),
                        "text": entry.get("text", "")[:200],  # Preview
                        "date": entry.get("date"),
                        "relevance_score": similarity,
                        "full_text": entry.get("text"),
                        "entities": entry.get("entities", {}),
                        "sentiment": entry.get("sentiment"),
                    }
                )

            # Sort by relevance and return top_k
            results.sort(key=lambda x: x["relevance_score"], reverse=True)
            results = results[:top_k]

            logger.info(f"Found {len(results)} relevant entries")
            return results

        except Exception as e:
            logger.error(f"Search failed: {str(e)}", exc_info=True)
            raise

    @staticmethod
    async def find_contradictions(entries: list[dict]) -> list[dict]:
        """
        Detect contradictions across journal entries.

        Args:
            entries: List of journal entries with extracted data

        Returns:
            List of detected contradictions
        """
        try:
            logger.info(f"Analyzing {len(entries)} entries for contradictions")

            contradictions = []

            # Check budget contradictions
            total_budget = None
            current_spending = 0

            for entry in entries:
                costs = entry.get("entities", {}).get("costs", [])
                for cost in costs:
                    amount = cost.get("amount", 0)
                    category = cost.get("category", "")

                    if category == "total budget":
                        total_budget = amount
                    else:
                        current_spending += amount

            if total_budget and current_spending > total_budget * 1.2:  # >20% over
                contradictions.append(
                    {
                        "type": "budget_overrun",
                        "severity": "high",
                        "description": f"Budget overrun: Spent ${current_spending} of ${total_budget} (${current_spending - total_budget} over)",
                        "budget": total_budget,
                        "spent": current_spending,
                    }
                )

            # Check timeline pressure
            pending_tasks = 0
            days_to_wedding = None

            for entry in entries:
                tasks = entry.get("tasks", {}).get("explicit", [])
                pending_tasks += len([t for t in tasks if t.get("status") == "pending"])

                dates = entry.get("entities", {}).get("dates", [])
                for date_obj in dates:
                    if date_obj.get("event") == "wedding":
                        # Would need date calculation here
                        pass

            if pending_tasks > 5 and days_to_wedding and days_to_wedding < 30:
                contradictions.append(
                    {
                        "type": "timeline_pressure",
                        "severity": "high",
                        "description": f"Timeline pressure: {pending_tasks} tasks pending with <30 days to wedding",
                        "pending_tasks": pending_tasks,
                        "days_remaining": days_to_wedding,
                    }
                )

            # Check vendor conflicts (same vendor booked multiple times)
            vendors_seen = {}
            for entry in entries:
                vendors = entry.get("entities", {}).get("vendors", [])
                for vendor in vendors:
                    vendor_name = vendor.get("name", "").lower()
                    if vendor_name in vendors_seen:
                        if vendor.get("status") == "booked":
                            contradictions.append(
                                {
                                    "type": "vendor_conflict",
                                    "severity": "medium",
                                    "description": f"Vendor booked multiple times: {vendor.get('name')}",
                                    "vendor": vendor.get("name"),
                                    "entries": [vendors_seen[vendor_name], entry.get("id")],
                                }
                            )
                    else:
                        vendors_seen[vendor_name] = entry.get("id")

            logger.info(f"Found {len(contradictions)} contradictions")
            return contradictions

        except Exception as e:
            logger.error(f"Contradiction detection failed: {str(e)}", exc_info=True)
            raise

    @staticmethod
    async def retrieve_context(
        query: str,
        entries: list[dict],
        num_context: int = 3,
    ) -> str:
        """
        Retrieve context from similar entries for RAG.

        Args:
            query: Current query/entry
            entries: List of historical entries
            num_context: Number of context entries to retrieve

        Returns:
            Formatted context string for LLM
        """
        try:
            logger.info(f"Retrieving context for: {query}")

            # Search for similar entries
            similar = await MemoryAgent.search_entries(
                query, entries, top_k=num_context
            )

            # Format as context
            context_parts = []
            for i, entry in enumerate(similar, 1):
                score = f"{entry['relevance_score']:.2%}"
                context_parts.append(
                    f"[Similar Entry {i} - Relevance: {score}]\n"
                    f"Date: {entry.get('date')}\n"
                    f"Text: {entry['text']}\n"
                    f"Sentiment: {entry.get('sentiment', {}).get('emotion', 'unknown')}\n"
                )

            context = "\n".join(context_parts)
            logger.info(f"Retrieved {len(similar)} context entries")

            return context

        except Exception as e:
            logger.error(f"Context retrieval failed: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def _cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity score (0-1)
        """
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)
