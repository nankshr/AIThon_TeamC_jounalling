"""Initial schema setup

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "vector"')

    # user_preferences table
    op.create_table(
        'user_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('values', postgresql.ARRAY(sa.String()), nullable=False, server_default='{}'),
        sa.Column('budget_goal', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('wedding_date', sa.Date(), nullable=True),
        sa.Column('primary_language', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('suggestion_mode_default', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('post_wedding_mode', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

    # journal_entries table
    op.create_table(
        'journal_entries',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('raw_text', sa.Text(), nullable=False),
        sa.Column('language', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('themes', postgresql.ARRAY(sa.String()), nullable=False, server_default='{}'),
        sa.Column('sentiment', sa.String(length=50), nullable=True),
        sa.Column('embedding', sa.String, nullable=True),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('suggestion_mode_active', sa.String(length=10), nullable=False, server_default='default'),
        sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['user_preferences.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create vector index on journal_entries
    op.execute('CREATE INDEX idx_entries_embedding ON journal_entries USING ivfflat (embedding vector_cosine_ops)')

    # master_entities table
    op.create_table(
        'master_entities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('canonical_name', sa.Text(), nullable=False),
        sa.Column('first_mentioned', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('last_mentioned', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('mention_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('decision_made', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.PrimaryKeyConstraint('id')
    )

    # entities table
    op.create_table(
        'entities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entry_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_name', sa.Text(), nullable=False),
        sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('canonical_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['canonical_id'], ['master_entities.id'], ),
        sa.ForeignKeyConstraint(['entry_id'], ['journal_entries.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # tasks table
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entry_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('deadline', sa.Date(), nullable=True),
        sa.Column('priority', sa.String(length=20), nullable=False, server_default='medium'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('completed_at', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['entry_id'], ['journal_entries.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['user_preferences.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('tasks')
    op.drop_table('entities')
    op.drop_table('master_entities')
    op.drop_table('journal_entries')
    op.drop_table('user_preferences')
    op.execute('DROP EXTENSION IF EXISTS "vector"')
