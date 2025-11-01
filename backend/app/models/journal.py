"""Journal entry models."""

from sqlalchemy import Column, String, Text, ForeignKey, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base, TimestampMixin


class JournalEntry(Base, TimestampMixin):
    """Journal entry with embeddings and metadata."""

    __tablename__ = "journal_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_preferences.id"), nullable=False)

    # Content
    raw_text = Column(Text, nullable=False)
    language = Column(String(10), default="en", nullable=False)

    # Analysis
    themes = Column(ARRAY(String), default=list, nullable=False)  # e.g., ["budget", "stress", "timeline"]
    sentiment = Column(String(50), nullable=True)  # e.g., "positive", "negative", "neutral"

    # Vector embedding (1536 dimensions for OpenAI text-embedding-3-small)
    embedding = Column(String, nullable=True)

    # Session tracking
    session_id = Column(UUID(as_uuid=True), nullable=True)

    # UI state
    suggestion_mode_active = Column(String(10), default="default", nullable=False)  # "on", "off", "default"

    # Metadata
    meta = Column(JSON, default=dict, nullable=False)

    # Relationships
    entities = relationship("Entity", back_populates="entry", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="entry", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<JournalEntry(id={self.id}, language={self.language}, themes={self.themes})>"
