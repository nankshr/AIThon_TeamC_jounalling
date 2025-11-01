"""User service."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import date as dateclass, datetime
from app.models import UserPreference
from app.schemas import UserPreferenceUpdateRequest, UserPreferenceResponse, TimelineStatusResponse
from typing import Optional
import uuid


class UserService:
    """Service for user preference operations."""

    @staticmethod
    async def get_or_create_user(
        db: AsyncSession,
        user_id: Optional[UUID] = None,
    ) -> UserPreference:
        """Get or create user preference."""
        if not user_id:
            user_id = uuid.uuid4()

        stmt = select(UserPreference).where(UserPreference.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            user = UserPreference(
                id=user_id,
                values=[],
                primary_language="en",
                suggestion_mode_default=True,
                post_wedding_mode=False,
                metadata={},
            )
            db.add(user)
            await db.flush()

        return user

    @staticmethod
    async def get_user(
        db: AsyncSession,
        user_id: UUID,
    ) -> Optional[UserPreferenceResponse]:
        """Get user preferences."""
        stmt = select(UserPreference).where(UserPreference.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            return None

        return UserPreferenceResponse(
            id=user.id,
            values=user.values,
            budget_goal=float(user.budget_goal) if user.budget_goal else None,
            wedding_date=user.wedding_date,
            primary_language=user.primary_language,
            suggestion_mode_default=user.suggestion_mode_default,
            post_wedding_mode=user.post_wedding_mode,
            created_at=user.created_at,
        )

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: UUID,
        request: UserPreferenceUpdateRequest,
    ) -> Optional[UserPreferenceResponse]:
        """Update user preferences."""
        stmt = select(UserPreference).where(UserPreference.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            return None

        if request.values is not None:
            user.values = request.values
        if request.budget_goal is not None:
            user.budget_goal = request.budget_goal
        if request.wedding_date is not None:
            user.wedding_date = dateclass.fromisoformat(request.wedding_date)
        if request.primary_language is not None:
            user.primary_language = request.primary_language
        if request.suggestion_mode_default is not None:
            user.suggestion_mode_default = request.suggestion_mode_default
        if request.post_wedding_mode is not None:
            user.post_wedding_mode = request.post_wedding_mode

        user.updated_at = datetime.utcnow()

        await db.flush()
        await db.refresh(user)

        return UserPreferenceResponse(
            id=user.id,
            values=user.values,
            budget_goal=float(user.budget_goal) if user.budget_goal else None,
            wedding_date=user.wedding_date,
            primary_language=user.primary_language,
            suggestion_mode_default=user.suggestion_mode_default,
            post_wedding_mode=user.post_wedding_mode,
            created_at=user.created_at,
        )

    @staticmethod
    async def get_timeline_status(
        db: AsyncSession,
        user_id: UUID,
    ) -> TimelineStatusResponse:
        """Get timeline status for user."""
        stmt = select(UserPreference).where(UserPreference.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            return TimelineStatusResponse(
                wedding_date=None,
                days_until_wedding=None,
                timeline_mode="planning",
                is_post_wedding=False,
                post_wedding_days=None,
            )

        wedding_date = user.wedding_date
        today = dateclass.today()

        if not wedding_date:
            return TimelineStatusResponse(
                wedding_date=None,
                days_until_wedding=None,
                timeline_mode="planning",
                is_post_wedding=False,
                post_wedding_days=None,
            )

        days_diff = (wedding_date - today).days

        if days_diff > 0:
            timeline_mode = "planning"
            is_post_wedding = False
            post_wedding_days = None
        elif days_diff == 0:
            timeline_mode = "wedding_day"
            is_post_wedding = False
            post_wedding_days = None
        else:
            timeline_mode = "post_wedding"
            is_post_wedding = True
            post_wedding_days = abs(days_diff)

        return TimelineStatusResponse(
            wedding_date=wedding_date,
            days_until_wedding=days_diff if days_diff > 0 else None,
            timeline_mode=timeline_mode,
            is_post_wedding=is_post_wedding,
            post_wedding_days=post_wedding_days,
        )
