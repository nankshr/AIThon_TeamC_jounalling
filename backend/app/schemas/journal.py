"""Pydantic schemas for journal endpoints."""

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class EntitySchema(BaseModel):
    """Schema for extracted entity."""
    entity_type: str = Field(..., description="Type of entity (vendor, venue, cost, etc.)")
    entity_name: str = Field(..., description="Name of the entity")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: dict = Field(default_factory=dict)

    class Config:
        from_attributes = True


class TaskSchema(BaseModel):
    """Schema for task."""
    id: Optional[UUID] = None
    action: str
    description: Optional[str] = None
    deadline: Optional[str] = None
    priority: str = "medium"
    status: str = "pending"

    class Config:
        from_attributes = True


class JournalEntryCreateRequest(BaseModel):
    """Request to create a journal entry."""
    text: str = Field(..., description="Journal entry text")
    language: str = Field(default="en", description="Language code")
    suggestion_mode: Optional[bool] = Field(default=True, description="Enable AI suggestions")


class JournalEntryResponse(BaseModel):
    """Response with journal entry and AI analysis."""
    id: UUID
    raw_text: str
    language: str
    themes: List[str] = Field(default_factory=list)
    sentiment: Optional[str] = None
    created_at: datetime
    entities: List[EntitySchema] = Field(default_factory=list)
    tasks: List[TaskSchema] = Field(default_factory=list)
    suggestions: Optional[dict] = None
    contradictions: Optional[List[str]] = None

    class Config:
        from_attributes = True


class JournalEntriesListResponse(BaseModel):
    """Response with list of journal entries."""
    total: int
    entries: List[JournalEntryResponse]


class JournalSearchRequest(BaseModel):
    """Request for semantic search."""
    query: str = Field(..., description="Search query")
    limit: int = Field(default=10, ge=1, le=50)
    search_type: str = Field(default="hybrid", description="Type of search: 'semantic', 'keyword', or 'hybrid'")


class JournalSearchResponse(BaseModel):
    """Response from search."""
    query: str
    results: List[JournalEntryResponse]
    total_results: int
