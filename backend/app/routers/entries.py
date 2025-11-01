"""API endpoints for journal entries."""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from app.agents.intake import IntakeAgent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/journal", tags=["journal"])


class JournalEntryCreate(BaseModel):
    """Request schema for creating a journal entry."""

    text: str
    language: str = "en"
    transcribed_from_audio: bool = False


class JournalEntryResponse(BaseModel):
    """Response schema for journal entry."""

    id: str
    text: str
    language: str
    entities: dict[str, Any]
    tasks: dict[str, Any]
    themes: list[str]
    sentiment: dict[str, Any]
    timeline: str
    summary: str


class EntryProcessingResponse(BaseModel):
    """Response for entry processing."""

    success: bool
    message: str
    data: Optional[dict[str, Any]] = None
    error: Optional[str] = None


@router.post("/entries", response_model=EntryProcessingResponse)
async def create_journal_entry(entry: JournalEntryCreate) -> EntryProcessingResponse:
    """
    Create a new journal entry and extract entities/tasks using Intake Agent.

    This endpoint:
    1. Accepts transcribed or typed journal entry
    2. Processes text with Intake Agent to extract:
       - Entities (vendors, venues, costs, dates, people)
       - Tasks (explicit and implicit)
       - Themes (budget, stress, etc.)
       - Sentiment (mood/emotion)
       - Timeline (pre/post-wedding)
    3. Returns structured data

    Args:
        entry: JournalEntryCreate with text and language

    Returns:
        Processing result with extracted data or error
    """
    try:
        if not entry.text or not entry.text.strip():
            raise HTTPException(status_code=400, detail="Entry text cannot be empty")

        logger.info(f"Creating journal entry: {len(entry.text)} chars, language: {entry.language}")

        # Process entry with Intake Agent
        logger.info("Calling Intake Agent to extract entities and tasks")
        result = await IntakeAgent.process_entry(entry.text, language=entry.language)

        if not result["success"]:
            logger.error(f"Intake Agent failed: {result.get('error')}")
            return EntryProcessingResponse(
                success=False,
                message="Failed to process entry",
                error=result.get("error"),
            )

        data = result["data"]
        logger.info(f"Successfully processed entry: {len(data)} top-level fields")

        # Return the extracted data
        return EntryProcessingResponse(
            success=True,
            message="Entry processed successfully",
            data={
                "entities": data.get("entities", {}),
                "tasks": data.get("tasks", {}),
                "themes": data.get("themes", []),
                "sentiment": data.get("sentiment", {}),
                "timeline": data.get("timeline", "pre-wedding"),
                "summary": data.get("summary", ""),
                "transcribed_from_audio": entry.transcribed_from_audio,
            },
        )

    except HTTPException as e:
        logger.warning(f"HTTP error in entry creation: {e.detail}")
        return EntryProcessingResponse(
            success=False,
            message="Invalid request",
            error=str(e.detail),
        )
    except Exception as e:
        logger.error(f"Error creating journal entry: {str(e)}", exc_info=True)
        return EntryProcessingResponse(
            success=False,
            message="Internal server error",
            error=str(e),
        )


@router.post("/entries/{entry_id}/extract-entities")
async def extract_entities(entry_id: str, entry: JournalEntryCreate):
    """
    Extract entities from an existing or new entry.

    Args:
        entry_id: ID of the entry (for reference)
        entry: Entry content to extract from

    Returns:
        Extracted entities
    """
    try:
        logger.info(f"Extracting entities from entry {entry_id}")
        entities = await IntakeAgent.extract_entities(entry.text)
        return {
            "success": True,
            "entry_id": entry_id,
            "entities": entities,
        }
    except Exception as e:
        logger.error(f"Error extracting entities: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }


@router.post("/entries/{entry_id}/extract-tasks")
async def extract_tasks(entry_id: str, entry: JournalEntryCreate):
    """
    Extract tasks from an existing or new entry.

    Args:
        entry_id: ID of the entry (for reference)
        entry: Entry content to extract from

    Returns:
        Extracted tasks
    """
    try:
        logger.info(f"Extracting tasks from entry {entry_id}")
        tasks = await IntakeAgent.extract_tasks(entry.text)
        return {
            "success": True,
            "entry_id": entry_id,
            "tasks": tasks,
        }
    except Exception as e:
        logger.error(f"Error extracting tasks: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }


@router.post("/entries/{entry_id}/analyze-sentiment")
async def analyze_sentiment(entry_id: str, entry: JournalEntryCreate):
    """
    Analyze sentiment/emotion from an entry.

    Args:
        entry_id: ID of the entry (for reference)
        entry: Entry content to analyze

    Returns:
        Sentiment analysis
    """
    try:
        logger.info(f"Analyzing sentiment for entry {entry_id}")
        sentiment = await IntakeAgent.extract_sentiment(entry.text)
        return {
            "success": True,
            "entry_id": entry_id,
            "sentiment": sentiment,
        }
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }
