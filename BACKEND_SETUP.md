# Backend Setup & Testing Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.11+ installed
- ✅ Your cloud PostgreSQL connection details ready
- ✅ Poetry installed (or will install via pip)

## Step 1: Configure Environment Variables

### 1.1 Navigate to Backend Directory
```bash
cd backend
```

### 1.2 Create .env File
```bash
cp .env.example .env
```

### 1.3 Edit .env with Your Cloud PostgreSQL

Open `backend/.env` and configure with your cloud database details:

```env
# IMPORTANT: Replace with your actual cloud PostgreSQL connection
DATABASE_URL=postgresql+asyncpg://username:password@cloud-host.example.com:5432/wedding_journal

# API Keys (optional for Phase 1, required for AI features in Phase 2)
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256

# Environment
DEBUG=True
ENVIRONMENT=development
```

**Example Real Connection String:**
```
DATABASE_URL=postgresql+asyncpg://postgres:mypassword@db.example.com:5432/wedding_journal
```

## Step 2: Install Poetry & Dependencies

### 2.1 Install Poetry (if not already installed)
```bash
pip install poetry
```

Verify installation:
```bash
poetry --version
```

### 2.2 Install Backend Dependencies
```bash
cd backend
poetry install
```

This will:
- Install all Python packages from `pyproject.toml`
- Create a virtual environment
- Install FastAPI, SQLAlchemy, PostgreSQL driver, etc.

**Expected output:**
```
Installing dependencies from lock file
...
Installing the current project: wedding-journal-backend (0.1.0)
```

## Step 3: Initialize Database

### 3.1 Run Migrations
```bash
poetry run alembic upgrade head
```

This will:
- Create pgvector extension in your cloud database
- Create all 5 tables (user_preferences, journal_entries, entities, master_entities, tasks)
- Create vector indexes for semantic search

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade base -> 001, initial schema
```

### 3.2 Verify Database Tables

Connect to your cloud PostgreSQL and verify:
```sql
-- Connect to your database
psql -h your-host -U username -d wedding_journal

-- List tables
\dt

-- Should show:
-- public | entities              | table
-- public | journal_entries       | table
-- public | master_entities       | table
-- public | tasks                 | table
-- public | user_preferences      | table
```

## Step 4: Run Backend Server

### 4.1 Start Development Server
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Backend is now running on: `http://localhost:8000`

### 4.2 Access API Documentation
Open in browser: `http://localhost:8000/docs`

You should see:
- Swagger UI with all 13 API endpoints
- "Try it out" buttons for each endpoint
- Request/response schemas

## Step 5: Test Backend Endpoints

### 5.1 Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status": "healthy"}
```

### 5.2 Test User Preferences
```bash
curl http://localhost:8000/api/user/preferences
```

**Expected Response:**
```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "values": [],
  "budget_goal": null,
  "wedding_date": null,
  "primary_language": "en",
  "suggestion_mode_default": true,
  "post_wedding_mode": false,
  "created_at": "2024-11-01T..."
}
```

### 5.3 Create Journal Entry
```bash
curl -X POST http://localhost:8000/api/journal/entry \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Started planning the wedding! Looking at venues.",
    "language": "en",
    "suggestion_mode": true
  }'
```

**Expected Response:** Entry with ID and metadata

### 5.4 Get All Entries
```bash
curl http://localhost:8000/api/journal/entries
```

### 5.5 Create Task
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "action": "Call caterer for quote",
    "priority": "high",
    "deadline": "2024-01-15"
  }'
```

### 5.6 Get Pending Tasks
```bash
curl http://localhost:8000/api/tasks/pending
```

## Troubleshooting

### Poetry Not Found
**Error:** `poetry: command not found`

**Solution:**
```bash
# Install poetry
pip install poetry

# Or use Python module directly
python -m poetry install
python -m poetry run uvicorn app.main:app --reload
```

### Database Connection Error
**Error:** `could not connect to server`

**Solution:**
```bash
# Verify connection string
echo $DATABASE_URL

# Test connection directly
psql postgresql://username:password@host:port/wedding_journal

# Check if pgvector is installed
psql -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### Module Not Found
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Reinstall dependencies
poetry install --no-cache

# Or clear and reinstall
rm -rf .venv
poetry install
```

### Port 8000 Already in Use
**Error:** `Address already in use: ('0.0.0.0', 8000)`

**Solution:**
```bash
# Use different port
poetry run uvicorn app.main:app --port 8001 --reload

# Or find and kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

### Alembic Migration Fails
**Error:** `Target database is not up to date`

**Solution:**
```bash
# Check current migration
poetry run alembic current

# Reset to base
poetry run alembic downgrade base

# Apply fresh
poetry run alembic upgrade head
```

## Environment Variables Reference

| Variable | Required | Example | Purpose |
|----------|----------|---------|---------|
| `DATABASE_URL` | Yes | `postgresql+asyncpg://...` | Cloud PostgreSQL connection |
| `ANTHROPIC_API_KEY` | No (Phase 2) | `sk-ant-xxx` | Claude API for AI features |
| `OPENAI_API_KEY` | No (Phase 2) | `sk-xxx` | OpenAI for embeddings |
| `SECRET_KEY` | Yes | `random-string` | App security |
| `ALGORITHM` | No | `HS256` | JWT algorithm |
| `DEBUG` | No | `True` | Debug mode |
| `ENVIRONMENT` | No | `development` | Environment type |

## Quick Commands Reference

```bash
# Navigate to backend
cd backend

# Install dependencies
poetry install

# Run migrations
poetry run alembic upgrade head

# Start server
poetry run uvicorn app.main:app --reload

# Run tests
poetry run pytest

# Check code
poetry run mypy app/
poetry run black --check app/
poetry run ruff check app/

# Database
poetry run alembic downgrade base  # Reset
poetry run alembic current         # Check status
```

## Next Steps

After backend is working:

1. ✅ Start frontend: `npm run dev` (port 3000)
2. ✅ Open browser: `http://localhost:3000`
3. ✅ Test by creating entries and tasks
4. ✅ Verify data in cloud PostgreSQL
5. ✅ Move to Phase 2: AI Agents

## Support

If you encounter issues:

1. Check this troubleshooting section
2. Verify `.env` configuration
3. Check database connectivity
4. Review backend logs in terminal
5. Check browser console for frontend errors (F12)

---

**Backend is ready for testing!** 🚀

Once configured and running, the MVP will be complete and ready for Phase 2 (AI Features).
