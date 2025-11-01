"""User endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas import (
    UserPreferenceUpdateRequest,
    UserPreferenceResponse,
    TimelineStatusResponse,
)
from app.services import get_db
from app.services.user import UserService

router = APIRouter(prefix="/api/user", tags=["user"])

# For MVP, using a hardcoded user_id
DEFAULT_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


@router.get("/preferences", response_model=UserPreferenceResponse)
async def get_user_preferences(
    db: AsyncSession = Depends(get_db),
) -> UserPreferenceResponse:
    """Get user preferences."""
    # Ensure user exists
    await UserService.get_or_create_user(db, DEFAULT_USER_ID)
    await db.commit()

    user = await UserService.get_user(db, DEFAULT_USER_ID)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/preferences", response_model=UserPreferenceResponse)
async def update_user_preferences(
    request: UserPreferenceUpdateRequest,
    db: AsyncSession = Depends(get_db),
) -> UserPreferenceResponse:
    """Update user preferences."""
    # Ensure user exists
    await UserService.get_or_create_user(db, DEFAULT_USER_ID)
    await db.commit()

    user = await UserService.update_user(db, DEFAULT_USER_ID, request)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.commit()

    return user


@router.get("/timeline", response_model=TimelineStatusResponse)
async def get_timeline_status(
    db: AsyncSession = Depends(get_db),
) -> TimelineStatusResponse:
    """Get wedding timeline status."""
    # Ensure user exists
    await UserService.get_or_create_user(db, DEFAULT_USER_ID)
    await db.commit()

    return await UserService.get_timeline_status(db, DEFAULT_USER_ID)
