"""Pydantic schemas for task endpoints."""

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class TaskCreateRequest(BaseModel):
    """Request to create a task."""
    action: str = Field(..., description="Task action")
    description: Optional[str] = None
    deadline: Optional[str] = None  # ISO date string
    priority: str = Field(default="medium")


class TaskUpdateRequest(BaseModel):
    """Request to update a task."""
    action: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class TaskResponse(BaseModel):
    """Response with task details."""
    id: UUID
    action: str
    description: Optional[str]
    deadline: Optional[str]
    priority: str
    status: str
    completed_at: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TasksListResponse(BaseModel):
    """Response with list of tasks."""
    total: int
    pending_count: int
    completed_count: int
    tasks: List[TaskResponse]


class TaskCompleteRequest(BaseModel):
    """Request to mark task as complete."""
    completed_at: Optional[str] = Field(None, description="ISO timestamp of completion")
