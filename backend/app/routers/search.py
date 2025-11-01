"""API endpoints for semantic search and RAG retrieval."""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from app.agents.memory import MemoryAgent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["search"])


class SearchRequest(BaseModel):
    """Request schema for search."""

    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    """Individual search result."""

    id: str
    text: str
    date: Optional[str] = None
    relevance_score: float
    full_text: str
    entities: dict[str, Any]
    sentiment: Optional[dict[str, Any]] = None


class SearchResponse(BaseModel):
    """Response schema for search."""

    success: bool
    message: str
    results: list[SearchResult] = []
    count: int = 0
    error: Optional[str] = None


class ContradictionDetectRequest(BaseModel):
    """Request schema for contradiction detection."""

    entries: list[dict[str, Any]]


class ContradictionResponse(BaseModel):
    """Response schema for contradiction detection."""

    success: bool
    message: str
    contradictions: list[dict[str, Any]] = []
    error: Optional[str] = None


class ContextRetrievalRequest(BaseModel):
    """Request schema for context retrieval."""

    query: str
    entries: list[dict[str, Any]]
    num_context: int = 3


class ContextRetrievalResponse(BaseModel):
    """Response schema for context retrieval."""

    success: bool
    message: str
    context: str = ""
    error: Optional[str] = None


@router.post("/search", response_model=SearchResponse)
async def search_entries(request: SearchRequest) -> SearchResponse:
    """
    Search for similar journal entries using semantic similarity (RAG pattern).

    This endpoint:
    1. Takes a search query
    2. Retrieves all journal entries from database
    3. Generates embedding for the query
    4. Compares against stored entry embeddings using cosine similarity
    5. Returns top-k similar entries with relevance scores, entities, and sentiment

    Args:
        request: SearchRequest with query and top_k

    Returns:
        List of matching entries ranked by relevance with full details
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        logger.info(f"Searching for: {request.query[:100]}... (top_k={request.top_k})")

        # Import database session
        from app.services.database import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            from app.models.journal import JournalEntry

            # Get all journal entries with embeddings
            stmt = select(JournalEntry).where(JournalEntry.embedding.isnot(None))
            result = await session.execute(stmt)
            entries = result.scalars().all()

            logger.info(f"Found {len(entries)} entries with embeddings in database")

            if not entries:
                logger.info("No entries found with embeddings")
                return SearchResponse(
                    success=True,
                    message="Search completed successfully",
                    results=[],
                    count=0,
                )

            # Convert entries to dict format for MemoryAgent
            entries_data = []
            for entry in entries:
                entry_dict = {
                    "id": str(entry.id),
                    "text": entry.raw_text,
                    "date": entry.created_at.isoformat() if entry.created_at else None,
                    "embedding": entry.embedding,
                    "entities": entry.meta.get("entities", {}) if entry.meta else {},
                    "sentiment": entry.meta.get("sentiment", {}) if entry.meta else {},
                    "themes": entry.themes,
                }
                entries_data.append(entry_dict)

            # Search using MemoryAgent
            search_results = await MemoryAgent.search_entries(
                request.query,
                entries_data,
                top_k=request.top_k
            )

            logger.info(f"Found {len(search_results)} matching entries")

            # Convert to SearchResult format
            results = [
                SearchResult(
                    id=r["id"],
                    text=r["text"][:200],  # Preview
                    date=r.get("date"),
                    relevance_score=r["relevance_score"],
                    full_text=r["full_text"],
                    entities=r.get("entities", {}),
                    sentiment=r.get("sentiment"),
                )
                for r in search_results
            ]

            return SearchResponse(
                success=True,
                message="Search completed successfully",
                results=results,
                count=len(results),
            )

    except HTTPException as e:
        logger.warning(f"HTTP error in search: {e.detail}")
        return SearchResponse(
            success=False,
            message="Invalid request",
            error=str(e.detail),
        )
    except Exception as e:
        logger.error(f"Error searching entries: {str(e)}", exc_info=True)
        return SearchResponse(
            success=False,
            message="Search failed",
            error=str(e),
        )


@router.post("/search/contradictions", response_model=ContradictionResponse)
async def detect_contradictions(
    request: ContradictionDetectRequest,
) -> ContradictionResponse:
    """
    Detect contradictions across journal entries.

    This endpoint detects:
    - Budget overruns (spending >20% over budget)
    - Timeline pressure (<30 days with >5 pending tasks)
    - Vendor conflicts (same vendor booked multiple times)

    Args:
        request: ContradictionDetectRequest with list of entries

    Returns:
        List of detected contradictions with severity levels
    """
    try:
        if not request.entries:
            raise HTTPException(status_code=400, detail="Entries list cannot be empty")

        logger.info(f"Detecting contradictions in {len(request.entries)} entries")

        # Call Memory Agent to detect contradictions
        contradictions = await MemoryAgent.find_contradictions(request.entries)

        logger.info(f"Found {len(contradictions)} contradictions")

        return ContradictionResponse(
            success=True,
            message="Contradiction detection completed",
            contradictions=contradictions,
        )

    except HTTPException as e:
        logger.warning(f"HTTP error in contradiction detection: {e.detail}")
        return ContradictionResponse(
            success=False,
            message="Invalid request",
            error=str(e.detail),
        )
    except Exception as e:
        logger.error(f"Error detecting contradictions: {str(e)}", exc_info=True)
        return ContradictionResponse(
            success=False,
            message="Contradiction detection failed",
            error=str(e),
        )


@router.post("/search/context", response_model=ContextRetrievalResponse)
async def retrieve_context(request: ContextRetrievalRequest) -> ContextRetrievalResponse:
    """
    Retrieve context from similar entries for RAG (Retrieval-Augmented Generation).

    This endpoint:
    1. Takes a query/new entry
    2. Retrieves top N similar historical entries
    3. Formats them as context for LLM processing

    Args:
        request: ContextRetrievalRequest with query and entries

    Returns:
        Formatted context string for LLM
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        logger.info(f"Retrieving context for: {request.query[:100]}...")

        # Call Memory Agent to retrieve context
        context = await MemoryAgent.retrieve_context(
            request.query, request.entries, num_context=request.num_context
        )

        logger.info(f"Retrieved context ({len(context)} chars)")

        return ContextRetrievalResponse(
            success=True,
            message="Context retrieval successful",
            context=context,
        )

    except HTTPException as e:
        logger.warning(f"HTTP error in context retrieval: {e.detail}")
        return ContextRetrievalResponse(
            success=False,
            message="Invalid request",
            error=str(e.detail),
        )
    except Exception as e:
        logger.error(f"Error retrieving context: {str(e)}", exc_info=True)
        return ContextRetrievalResponse(
            success=False,
            message="Context retrieval failed",
            error=str(e),
        )
