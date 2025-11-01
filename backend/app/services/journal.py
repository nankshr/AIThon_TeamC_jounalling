"""Journal entry service."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload
from uuid import UUID
from app.models import JournalEntry, Entity, Task as TaskModel, UserPreference
from app.schemas import JournalEntryCreateRequest, JournalEntryResponse
from typing import List, Optional
import uuid


class JournalService:
    """Service for journal entry operations."""

    @staticmethod
    async def create_entry(
        db: AsyncSession,
        user_id: UUID,
        request: JournalEntryCreateRequest,
    ) -> JournalEntryResponse:
        """Create a new journal entry."""
        entry = JournalEntry(
            id=uuid.uuid4(),
            user_id=user_id,
            raw_text=request.text,
            language=request.language,
            session_id=uuid.uuid4(),
            suggestion_mode_active="on" if request.suggestion_mode else "off",
            themes=[],
            metadata={}
        )

        db.add(entry)
        await db.flush()
        await db.refresh(entry, ["entities", "tasks"])

        return JournalEntryResponse(
            id=entry.id,
            raw_text=entry.raw_text,
            language=entry.language,
            themes=entry.themes,
            sentiment=entry.sentiment,
            created_at=entry.created_at,
            entities=[],
            tasks=[],
        )

    @staticmethod
    async def get_entries(
        db: AsyncSession,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[List[JournalEntryResponse], int]:
        """Get user's journal entries with pagination."""
        # Get total count
        count_stmt = select(func.count(JournalEntry.id)).where(JournalEntry.user_id == user_id)
        result = await db.execute(count_stmt)
        total = result.scalar()

        # Get entries
        stmt = (
            select(JournalEntry)
            .where(JournalEntry.user_id == user_id)
            .options(selectinload(JournalEntry.entities), selectinload(JournalEntry.tasks))
            .order_by(desc(JournalEntry.created_at))
            .limit(limit)
            .offset(offset)
        )

        result = await db.execute(stmt)
        entries = result.scalars().all()

        return [_entry_to_response(entry) for entry in entries], total

    @staticmethod
    async def get_entry(
        db: AsyncSession,
        entry_id: UUID,
        user_id: UUID,
    ) -> Optional[JournalEntryResponse]:
        """Get a single journal entry."""
        stmt = (
            select(JournalEntry)
            .where((JournalEntry.id == entry_id) & (JournalEntry.user_id == user_id))
            .options(selectinload(JournalEntry.entities), selectinload(JournalEntry.tasks))
        )

        result = await db.execute(stmt)
        entry = result.scalars().first()

        return _entry_to_response(entry) if entry else None

    @staticmethod
    async def get_user_entries_count(
        db: AsyncSession,
        user_id: UUID,
    ) -> int:
        """Get total count of user's entries."""
        stmt = select(func.count(JournalEntry.id)).where(JournalEntry.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalar() or 0


def _entry_to_response(entry: JournalEntry) -> JournalEntryResponse:
    """Convert JournalEntry model to response schema."""
    return JournalEntryResponse(
        id=entry.id,
        raw_text=entry.raw_text,
        language=entry.language,
        themes=entry.themes or [],
        sentiment=entry.sentiment,
        created_at=entry.created_at,
        entities=[
            {
                "entity_type": e.entity_type,
                "entity_name": e.entity_name,
                "confidence": e.confidence,
                "metadata": e.metadata,
            }
            for e in entry.entities
        ],
        tasks=[
            {
                "id": t.id,
                "action": t.action,
                "description": t.description,
                "deadline": t.deadline.isoformat() if t.deadline else None,
                "priority": t.priority.value,
                "status": t.status.value,
            }
            for t in entry.tasks
        ],
    )
