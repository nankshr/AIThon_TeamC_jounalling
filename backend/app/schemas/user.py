"""Pydantic schemas for user endpoints."""

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date


class UserPreferenceUpdateRequest(BaseModel):
    """Request to update user preferences."""
    values: Optional[List[str]] = Field(None, description="User values/preferences")
    budget_goal: Optional[float] = Field(None, ge=0)
    wedding_date: Optional[str] = Field(None, description="ISO date string")
    primary_language: Optional[str] = Field(None)
    suggestion_mode_default: Optional[bool] = None
    post_wedding_mode: Optional[bool] = None


class UserPreferenceResponse(BaseModel):
    """Response with user preferences."""
    id: UUID
    values: List[str]
    budget_goal: Optional[float]
    wedding_date: Optional[date]
    primary_language: str
    suggestion_mode_default: bool
    post_wedding_mode: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TimelineStatusResponse(BaseModel):
    """Response with timeline status."""
    wedding_date: Optional[date]
    days_until_wedding: Optional[int]
    timeline_mode: str  # "planning", "wedding_day", "post_wedding"
    is_post_wedding: bool
    post_wedding_days: Optional[int]
