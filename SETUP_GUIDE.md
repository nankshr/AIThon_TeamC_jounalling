# Setup Guide - Wedding Journal MVP

Complete step-by-step guide to run the MVP locally with your cloud PostgreSQL database.

## What's Been Built

✅ **Backend (FastAPI)**
- Complete database models (User, JournalEntry, Entity, Task)
- Database migrations (Alembic)
- API endpoints (Journal, Tasks, User)
- Services layer for business logic
- Async SQLAlchemy with PostgreSQL support

✅ **Frontend (Next.js)**
- Pages: Home (/) and Search (/search)
- Components: Header, JournalInput, JournalList, TaskPanel
- API client with Zustand state management
- Tailwind CSS styling

✅ **Configuration**
- Environment templates
- Database schema with pgvector support
- TypeScript/Python setup

## Prerequisites

Before you start, make sure you have:

- **Python 3.11+** installed
- **Node.js 20+** installed
- **PostgreSQL 16** database with **pgvector** extension (on your cloud)
- Your cloud PostgreSQL **connection string** ready
- **API Keys** (optional for now - needed for AI features later):
  - Anthropic API key
  - OpenAI API key

## Step 1: Clone/Setup Repository

If you haven't already:

```bash
# Navigate to your project directory
cd d:/ClaudeCodeWorkspace/AIThon_TeamC_jounalling

# Verify git is initialized
git status
```

## Step 2: Backend Setup

### 2.1 Install Python Dependencies

```bash
cd backend

# Install poetry (if not already installed)
pip install poetry

# Install dependencies
poetry install
```

### 2.2 Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your cloud PostgreSQL connection
# Use your actual cloud database credentials
```

**Example `.backend/.env`:**
```
DATABASE_URL=postgresql+asyncpg://username:password@cloud-host.example.com:5432/wedding_journal
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
DEBUG=True
ENVIRONMENT=development
```

### 2.3 Initialize Database

```bash
# Run migrations (creates all tables)
poetry run alembic upgrade head
```

This will:
- Create pgvector extension in your cloud database
- Create all required tables (user_preferences, journal_entries, entities, master_entities, tasks)
- Create indexes for vector search

### 2.4 Run Backend Server

```bash
# Start FastAPI development server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Backend is now ready at:**
- Application: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## Step 3: Frontend Setup

### 3.1 Install Dependencies

Open a **new terminal** and navigate to frontend:

```bash
cd frontend
npm install
```

### 3.2 Configure Environment

```bash
# Copy the example file
cp .env.local.example .env.local
```

**Keep default or update if needed:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3.3 Run Frontend Server

```bash
npm run dev
```

You should see output like:
```
  ▲ Next.js 14.0.0
  - Local:        http://localhost:3000
```

**Frontend is now ready at:** `http://localhost:3000`

## Step 4: Test the Application

### 4.1 Test Backend Health

```bash
curl http://localhost:8000/health
```

Should return:
```json
{"status": "healthy"}
```

### 4.2 Create Test Entry

```bash
curl -X POST http://localhost:8000/api/journal/entry \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Started planning the wedding today! Looking at venues.",
    "language": "en",
    "suggestion_mode": true
  }'
```

Should return entry with ID and metadata.

### 4.3 Get Entries

```bash
curl http://localhost:8000/api/journal/entries
```

Should return list with your test entry.

### 4.4 Test Frontend

Open `http://localhost:3000` in your browser. You should see:

- Wedding Journal header
- Journal input area
- Task panel on the right
- Ability to create entries and tasks

## Step 5: Verify Database

### Connect to your cloud PostgreSQL

```bash
psql -h your-cloud-host -U username -d wedding_journal

# List tables
\dt

# Check user_preferences table
SELECT * FROM user_preferences;

# Check journal_entries table
SELECT COUNT(*) FROM journal_entries;
```

## What Works Now (MVP)

✅ **Journal Entries**
- Create new journal entries
- View all entries
- Entries are stored in PostgreSQL
- Timestamps tracked

✅ **Task Management**
- Create tasks
- Mark tasks as complete
- View pending tasks
- Priority levels
- Task history

✅ **User Preferences**
- Get/update user preferences
- Wedding date tracking
- Language preferences
- Timeline awareness (pre/post-wedding)

✅ **UI/UX**
- Beautiful Tailwind-styled interface
- Responsive design
- State management with Zustand
- Smooth interactions

## What's Not Implemented Yet

⏳ **AI Features** (Next Phase)
- [ ] Voice transcription (Whisper API)
- [ ] Entity extraction (Claude)
- [ ] Semantic search (pgvector)
- [ ] Contradiction detection
- [ ] Task auto-generation

## Troubleshooting

### Backend won't start

**Error: "Cannot connect to database"**
```bash
# Verify connection string
# Check if pgvector extension is enabled in cloud DB:
psql -c "CREATE EXTENSION IF NOT EXISTS vector"

# Verify migrations:
poetry run alembic current
```

**Error: "Module not found"**
```bash
# Reinstall dependencies
poetry install --no-cache
```

### Frontend shows API errors

**Error: "Failed to connect to API"**
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check browser console (F12) for actual error

**Error: "CORS error"**
- Backend has CORS enabled for development
- Verify backend is accessible from frontend

### Database issues

**pgvector not available**
```sql
-- In your cloud PostgreSQL:
CREATE EXTENSION IF NOT EXISTS vector;
```

**Tables not created**
```bash
# Re-run migrations
poetry run alembic downgrade base
poetry run alembic upgrade head
```

## File Structure Created

```
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── routers/
│   ├── alembic/
│   ├── pyproject.toml
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   └── styles/
│   ├── package.json
│   ├── tsconfig.json
│   └── .env.local.example
│
├── README.md
├── CLAUDE.md
├── SETUP_GUIDE.md
└── .gitignore
```

## Next Steps

### Phase 2: AI Agents

1. **Entity Extraction** (Week 3)
   - Implement intake agent
   - Extract vendors, venues, costs, dates
   - Entity deduplication

2. **Semantic Search** (Week 4)
   - Vector embeddings with OpenAI
   - Hybrid search (semantic + keyword)
   - Entity-based search

3. **Insights** (Week 5)
   - Contradiction detection
   - Task auto-generation
   - Next steps suggestions

### Quick Commands Reference

```bash
# Backend
cd backend
poetry install          # Install dependencies
poetry run uvicorn app.main:app --reload  # Run server
poetry run alembic upgrade head           # Apply migrations
poetry run pytest                         # Run tests

# Frontend
cd frontend
npm install            # Install dependencies
npm run dev            # Run dev server
npm run build          # Build for production
npm run lint           # Check code

# Database
poetry run alembic current           # Check current migration
poetry run alembic downgrade base    # Reset to base
poetry run alembic upgrade head      # Apply all migrations
```

## Support

Check these files for more information:
- **CLAUDE.md** - Development guidelines
- **prd/PROJECT_PLAN.md** - Full project specifications
- **prd/QUICK_START_GUIDE.md** - Additional setup details

---

**You're all set! The MVP is ready to run.** 🎉

Start with creating some journal entries and tasks to test the application. Next, we'll implement the AI features!
