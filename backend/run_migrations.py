#!/usr/bin/env python
"""Simple script to run migrations without async complications."""

import os
import sys
from sqlalchemy import create_engine
from app.config import settings
from app.models import Base

# Use regular PostgreSQL driver instead of asyncpg for migrations
db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")

print("Connecting to database...")

engine = create_engine(db_url, echo=False)

# Create all tables
Base.metadata.create_all(engine)
print("Tables created successfully")

# Try to create pgvector extension (may not be available)
try:
    with engine.connect() as conn:
        conn.execute(engine.text('CREATE EXTENSION IF NOT EXISTS "vector"'))
        conn.commit()
        print("pgvector extension created")
except Exception as e:
    print(f"Note: pgvector not available (this is okay for Phase 1)")

print("\nDatabase initialized!")
