"""User preference models."""

from datetime import date
from sqlalchemy import Column, String, Numeric, Date, Boolean, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base, TimestampMixin


class UserPreference(Base, TimestampMixin):
    """User preferences and settings."""

    __tablename__ = "user_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Preferences
    values = Column(ARRAY(String), default=list, nullable=False)  # e.g., ["budget-conscious", "eco-friendly"]
    budget_goal = Column(Numeric(12, 2), nullable=True)
    wedding_date = Column(Date, nullable=True)

    # Settings
    primary_language = Column(String(10), default="en", nullable=False)
    suggestion_mode_default = Column(Boolean, default=True, nullable=False)
    post_wedding_mode = Column(Boolean, default=False, nullable=False)

    # Metadata
    meta = Column(JSON, default=dict, nullable=False)

    def __repr__(self) -> str:
        return f"<UserPreference(id={self.id}, wedding_date={self.wedding_date})>"
