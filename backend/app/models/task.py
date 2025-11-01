"""Task models."""

from datetime import date
from sqlalchemy import Column, String, Text, ForeignKey, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from .base import Base, TimestampMixin


class TaskPriority(str, enum.Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, enum.Enum):
    """Task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task(Base, TimestampMixin):
    """Action item task."""

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_preferences.id"), nullable=False)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("journal_entries.id", ondelete="SET NULL"), nullable=True)

    # Task info
    action = Column(Text, nullable=False)
    description = Column(Text, nullable=True)

    # Scheduling
    deadline = Column(Date, nullable=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)

    # Completion
    completed_at = Column(String, nullable=True)  # ISO timestamp string

    # Relationships
    entry = relationship("JournalEntry", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, action={self.action}, status={self.status})>"
