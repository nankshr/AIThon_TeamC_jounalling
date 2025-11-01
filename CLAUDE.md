# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-powered wedding journal application that helps users plan weddings through intelligent journaling with AI insights. The app captures voice/text entries, extracts structured data (vendors, venues, costs, tasks), provides semantic search, detects contradictions, and generates AI-powered suggestions.

**Timeline:** 8-week MVP development on Coolify (self-hosted)

## Technology Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI (async)
- **Database:** PostgreSQL 16 + pgvector extension
- **ORM:** SQLAlchemy (async)
- **Agent Orchestration:** LangGraph + LangChain
- **APIs:** Anthropic Claude 3.5 Sonnet, OpenAI Whisper, OpenAI Embeddings

### Frontend
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Zustand

### Infrastructure
- **Hosting:** Coolify (self-hosted)
- **Containerization:** Docker + Docker Compose
- **SSL/HTTPS:** Automatic via Coolify/Caddy

## Architecture

### Multi-Agent Workflow

```
User Input (Voice/Text)
    ↓
[Transcription] → Whisper API (audio → text)
    ↓
[Intake Agent] → Extract entities, themes, tasks
    ↓
[Memory Agent] → Semantic search (RAG)
    ↓
[Insight Agent] → Detect contradictions, generate insights
    ↓
[Task Manager] → Auto-log tasks, retrieve reminders
    ↓
Response (with suggestions, reminders, insights)
```

### Key Components

- **Intake Agent:** Extracts vendors, venues, costs, dates, people, themes (budget, eco-friendly, stress), tasks (explicit + implicit), sentiment
- **Memory Agent:** Hybrid search combining semantic (vector), keyword (full-text), and entity-based search with time decay
- **Insight Agent:** Detects contradictions (budget >20% over, deadline pressure <30 days with >5 tasks), generates next steps
- **Task Manager:** Auto-logs tasks from entries, manages priorities/deadlines, provides reminders
- **Orchestrator:** LangGraph workflow connecting all agents with state management

## Key Development Commands

### Backend

```bash
# Installation and setup
cd backend
poetry install                                    # Install dependencies
cp .env.example .env                             # Create env file
poetry run alembic upgrade head                  # Run migrations
poetry run uvicorn app.main:app --reload         # Run dev server (http://localhost:8000)

# Testing
poetry run pytest                                 # Run all tests
poetry run pytest tests/test_agents.py -v       # Run specific test file
poetry run pytest -k test_entity_extraction     # Run specific test

# Code quality
poetry run mypy app/                             # Type checking
poetry run black app/                            # Format code
poetry run ruff check app/                       # Lint code
```

### Frontend

```bash
# Installation and setup
cd frontend
npm install                                      # Install dependencies
cp .env.local.example .env.local                # Create env file
npm run dev                                      # Run dev server (http://localhost:3000)

# Testing and linting
npm run lint                                     # Run ESLint
npm run test                                     # Run tests (when configured)

# Production
npm run build                                    # Build for production
npm start                                        # Start production server
```

### Docker

```bash
# Build and run all services
docker compose build
docker compose up                                # Runs on http://localhost:3000

# Run single service
docker compose up backend                        # Just backend
docker compose up frontend                       # Just frontend
```

### Database

```bash
# Connect to PostgreSQL
psql -h localhost -U postgres -d wedding_journal

# Create migration
cd backend && poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Rollback last migration
poetry run alembic downgrade -1
```

## Directory Structure

```
wedding-journal/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── config.py              # Environment config
│   │   ├── models/                # SQLAlchemy ORM models
│   │   │   ├── journal.py         # JournalEntry model
│   │   │   ├── entities.py        # Entity & MasterEntity models
│   │   │   └── tasks.py           # Task model
│   │   ├── schemas/               # Pydantic schemas (request/response)
│   │   ├── services/              # Business logic
│   │   │   ├── transcription.py   # Whisper API
│   │   │   ├── embeddings.py      # OpenAI embeddings
│   │   │   ├── search.py          # Hybrid search
│   │   │   ├── entity_manager.py  # Entity deduplication
│   │   │   └── database.py        # DB utilities
│   │   ├── agents/                # LangGraph agents
│   │   │   ├── prompts.py         # Claude prompts
│   │   │   ├── intake.py          # Entity extraction agent
│   │   │   ├── memory.py          # RAG/search agent
│   │   │   ├── insight.py         # Contradiction detection agent
│   │   │   ├── task_manager.py    # Task management agent
│   │   │   └── orchestrator.py    # LangGraph workflow
│   │   └── routers/               # API route handlers
│   ├── alembic/                   # Database migrations
│   ├── tests/                     # Unit & integration tests
│   ├── pyproject.toml             # Poetry dependencies
│   ├── .env.example              # Environment template
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx          # Main journaling page
│   │   │   ├── search/page.tsx   # Search interface
│   │   │   └── layout.tsx        # Root layout
│   │   ├── components/
│   │   │   ├── JournalInput.tsx   # Text entry
│   │   │   ├── VoiceRecorder.tsx  # Voice recording
│   │   │   ├── SuggestionToggle.tsx
│   │   │   ├── JournalingSidebar.tsx
│   │   │   ├── TaskReview.tsx
│   │   │   └── SearchInterface.tsx
│   │   ├── hooks/
│   │   │   └── useVoiceRecorder.ts
│   │   └── lib/
│   │       └── api.ts            # API client
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── Dockerfile
│
├── prd/
│   ├── PROJECT_PLAN.md           # Detailed 8-week plan
│   ├── QUICK_START_GUIDE.md      # Setup commands
│   └── PROGRESS_CHECKLIST.md     # Week-by-week tracking
│
└── docker-compose.yml
```

## Database Schema

**Key Tables:**
- `user_preferences` - User settings, budget goal, wedding date
- `journal_entries` - Text entries with embeddings (pgvector)
- `entities` - Extracted data (vendors, venues, costs, dates, people)
- `master_entities` - Deduplicated entities with decision tracking
- `tasks` - Auto-logged action items with deadline and priority

**Vector Index:**
```sql
CREATE INDEX idx_entries_embedding ON journal_entries
USING ivfflat (embedding vector_cosine_ops);
```

## API Endpoints

**Journal:**
- `POST /api/journal/entry` - Create entry (triggers multi-agent workflow)
- `GET /api/journal/entries` - List all entries
- `GET /api/journal/entry/{id}` - Get specific entry
- `POST /api/journal/search` - Semantic search

**Tasks:**
- `GET /api/tasks/pending` - Get pending tasks
- `POST /api/tasks/{id}/complete` - Mark task complete
- `GET /api/tasks/history` - Task history

**User:**
- `GET /api/user/preferences` - Get preferences
- `PUT /api/user/preferences` - Update preferences
- `GET /api/user/timeline` - Timeline status (pre/post-wedding)

**Transcription:**
- `POST /api/transcription/transcribe` - Convert audio to text

## Environment Variables

**Backend (.env):**
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/wedding_journal
ANTHROPIC_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
SECRET_KEY=<random-string>
DEBUG=True/False
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing Strategy

- **Unit tests:** Test agents, services, and utilities in isolation
- **Integration tests:** Test API endpoints with database
- **E2E tests:** Test critical user flows (voice → extraction → search)
- **Manual testing:** Voice transcription quality varies by language/accent

**Test samples in `backend/tests/fixtures.py`:**
- 20+ wedding journal entries for testing entity extraction
- Various languages (English, Tamil)
- Cost formats (₹, $, decimal variations)
- Entity deduplication scenarios

## Development Workflow

- **Main branch:** Production-ready code
- **Feature branches:** `feature/name` from main
- **Commit messages:** `feat: add feature`, `fix: bug`, `refactor: improve`
- **Code style:**
  - Backend: Type hints, docstrings, Black formatting
  - Frontend: Full TypeScript, ESLint + Prettier
- **Pre-commit hooks:** Black, Ruff, mypy (backend); ESLint (frontend)

## Cost Tracking

**Monthly API costs (estimated):**
- Anthropic Claude: $20-40 (adjust model to Haiku for cost reduction)
- OpenAI Whisper: $10-20
- OpenAI Embeddings: $2-5
- Total: ~$32-65/month

Monitor usage via:
- Anthropic dashboard: console.anthropic.com
- OpenAI dashboard: platform.openai.com

## Deployment (Week 8)

1. **Docker setup:** Dockerfiles for backend/frontend already defined in prd/PROJECT_PLAN.md
2. **Database:** PostgreSQL 16 with pgvector extension (Docker or Coolify managed)
3. **Coolify deployment:**
   - Connect GitHub repo
   - Set environment variables
   - Enable automatic deploys
   - SSL handled automatically via Caddy
4. **Backups:** Configure PostgreSQL backups in Coolify

## Success Metrics (MVP)

After 4 weeks of real usage:
- **Engagement:** ≥3 journal entries/week
- **Accuracy:** 80%+ entity extraction, 70%+ task detection
- **Utility:** User acts on ≥40% of suggestions, uses search ≥1x/week
- **Value:** User feels "more organized", at least 1 decision made easier

## Quick Debugging

**Database connection fails:**
```bash
docker ps | grep pgvector
docker restart <container-id>
psql -h localhost -U postgres -d wedding_journal
```

**API connection fails (frontend):**
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS configuration in backend
- Verify backend is running on expected port

**Entity extraction low accuracy:**
- Check prompt in `app/agents/prompts.py`
- Verify entity examples in test fixtures
- Review Claude API output with `langchain.debug = True`

**Vector search not working:**
```bash
# Verify pgvector installed
psql -d wedding_journal -c "CREATE EXTENSION vector;"
# Check embeddings cached correctly
SELECT COUNT(*) FROM journal_entries WHERE embedding IS NOT NULL;
```

## Important Project Details

- **Language support:** MVP for English & Tamil (expandable)
- **Multi-user:** Currently single-user, add auth in V2
- **Timeline modes:** Pre-wedding (urgency) vs Post-wedding (reflection)
- **Contradiction thresholds:** Budget >20% over, deadline <30 days with >5 critical tasks
- **Embedding model:** OpenAI text-embedding-3-small (1536 dimensions)
- **Vector index type:** IVFFlat (good balance of speed/accuracy for pgvector)

## Useful Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Next.js Docs](https://nextjs.org/docs)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [PostgreSQL pgvector](https://github.com/pgvector/pgvector)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
