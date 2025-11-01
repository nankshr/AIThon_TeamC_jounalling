"""Update embedding column to pgvector Vector type

Revision ID: 002
Revises: 001
Create Date: 2024-11-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade: Convert embedding column to pgvector type."""
    # Drop existing embedding column and recreate with Vector type
    op.execute('ALTER TABLE journal_entries DROP COLUMN embedding')
    op.execute('ALTER TABLE journal_entries ADD COLUMN embedding vector(1536)')


def downgrade() -> None:
    """Downgrade: Revert embedding column back to String."""
    op.execute('ALTER TABLE journal_entries DROP COLUMN embedding')
    op.execute('ALTER TABLE journal_entries ADD COLUMN embedding VARCHAR')
