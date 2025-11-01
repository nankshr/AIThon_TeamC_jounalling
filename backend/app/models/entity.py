"""Entity and entity management models."""

from sqlalchemy import Column, String, Text, ForeignKey, JSON, Float, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .base import Base, TimestampMixin


class Entity(Base, TimestampMixin):
    """Extracted entity from journal entry."""

    __tablename__ = "entities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("journal_entries.id", ondelete="CASCADE"), nullable=False)

    # Entity info
    entity_type = Column(String(50), nullable=False)  # e.g., "vendor", "venue", "cost", "date", "person"
    entity_name = Column(Text, nullable=False)

    # Metadata and confidence
    meta = Column(JSON, default=dict, nullable=False)
    confidence = Column(Float, default=1.0, nullable=False)

    # Link to deduplicated master entity
    canonical_id = Column(UUID(as_uuid=True), ForeignKey("master_entities.id"), nullable=True)

    # Relationships
    entry = relationship("JournalEntry", back_populates="entities")
    master_entity = relationship("MasterEntity", back_populates="entities")

    def __repr__(self) -> str:
        return f"<Entity(id={self.id}, type={self.entity_type}, name={self.entity_name})>"


class MasterEntity(Base):
    """Deduplicated entity record (single source of truth)."""

    __tablename__ = "master_entities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Entity info
    entity_type = Column(String(50), nullable=False)
    canonical_name = Column(Text, nullable=False)

    # Tracking
    first_mentioned = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_mentioned = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    mention_count = Column(Integer, default=1, nullable=False)

    # Decision tracking
    decision_made = Column(Boolean, default=False, nullable=False)

    # Metadata
    meta = Column(JSON, default=dict, nullable=False)

    # Relationships
    entities = relationship("Entity", back_populates="master_entity", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<MasterEntity(id={self.id}, type={self.entity_type}, name={self.canonical_name})>"
