"""Journal endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas import (
    JournalEntryCreateRequest,
    JournalEntryResponse,
    JournalEntriesListResponse,
    JournalSearchRequest,
    JournalSearchResponse,
)
from app.services import JournalService, get_db
from app.services.user import UserService

router = APIRouter(prefix="/api/journal", tags=["journal"])

# For MVP, using a hardcoded user_id
DEFAULT_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


@router.post("/entry", response_model=JournalEntryResponse)
async def create_journal_entry(
    request: JournalEntryCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> JournalEntryResponse:
    """Create a new journal entry with AI analysis."""
    # Ensure user exists
    await UserService.get_or_create_user(db, DEFAULT_USER_ID)
    await db.commit()

    # Create entry
    response = await JournalService.create_entry(db, DEFAULT_USER_ID, request)
    await db.commit()

    return response


@router.get("/entries", response_model=JournalEntriesListResponse)
async def list_journal_entries(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> JournalEntriesListResponse:
    """List all journal entries for the user."""
    entries, total = await JournalService.get_entries(db, DEFAULT_USER_ID, limit, offset)
    return JournalEntriesListResponse(total=total, entries=entries)


@router.get("/entry/{entry_id}", response_model=JournalEntryResponse)
async def get_journal_entry(
    entry_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> JournalEntryResponse:
    """Get a specific journal entry."""
    entry = await JournalService.get_entry(db, entry_id, DEFAULT_USER_ID)

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    return entry


@router.post("/search", response_model=JournalSearchResponse)
async def search_journal(
    request: JournalSearchRequest,
    db: AsyncSession = Depends(get_db),
) -> JournalSearchResponse:
    """Search journal entries (semantic search coming soon)."""
    # For MVP, return empty results
    # Will implement semantic search with embeddings in next phase
    return JournalSearchResponse(
        query=request.query,
        results=[],
        total_results=0,
    )
