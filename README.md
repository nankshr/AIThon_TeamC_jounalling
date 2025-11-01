# AI-Powered Wedding Journal - MVP

A complete AI-powered wedding journal application for intelligent planning and journaling.

**Status:** ✅ 50% Complete (Weeks 2-3 Done, Weeks 4-8 Pending)
**Features:** Voice recording, Whisper transcription, GPT-4 entity extraction

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 16 with pgvector extension (cloud or local)

### Backend Setup

1. **Install Python dependencies:**
```bash
cd backend
poetry install
```

2. **Create and configure `.env`:**
```bash
# Edit .env with your database URL and API keys
```

Configure with your cloud PostgreSQL:
```
DATABASE_URL=postgresql+asyncpg://username:password@host:port/wedding_journal
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your-secret-key
DEBUG=True
```

**Note:** Only OPENAI_API_KEY is required (Anthropic is optional)

3. **Initialize database:**
```bash
poetry run alembic upgrade head
```

4. **Run backend:**
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Create `.env.local`:**
```bash
cp .env.local.example .env.local
# Default: NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Run frontend:**
```bash
npm run dev
```

Frontend runs on `http://localhost:3000`

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── routers/             # API endpoints
│   └── agents/              # AI agents (coming soon)
├── alembic/                 # Database migrations
└── tests/                   # Tests

frontend/
├── src/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   ├── lib/                 # Utilities & API client
│   └── styles/              # CSS
└── public/                  # Static files
```

## Key Features (MVP)

### Completed ✅
- ✅ Voice recording with playback
- ✅ Audio transcription (Whisper API)
- ✅ Entity extraction (vendors, venues, costs, dates, people)
- ✅ Task detection (explicit + implicit)
- ✅ Sentiment analysis (emotion + confidence)
- ✅ Multi-language support (English, Tamil, Hindi)
- ✅ Journal entry creation
- ✅ Task management
- ✅ User preferences tracking
- ✅ Timeline awareness (pre/post-wedding)

### Pending ⏳
- ⏳ Semantic search (RAG implementation)
- ⏳ Memory Agent (Week 4)
- ⏳ Insight Agent (Week 5)
- ⏳ Advanced search UI (Week 6)

## API Endpoints

### Transcription (Week 2)
- `POST /api/transcription/transcribe` - Audio to text
- `GET /api/transcription/detect-language` - Auto-detect language

### Entry Processing (Week 3)
- `POST /api/journal/entries` - Full processing (extract all data)
- `POST /api/journal/entries/{id}/extract-entities` - Extract entities only
- `POST /api/journal/entries/{id}/extract-tasks` - Extract tasks only
- `POST /api/journal/entries/{id}/analyze-sentiment` - Sentiment only

### Journal
- `POST /api/journal/entry` - Create entry
- `GET /api/journal/entries` - List entries
- `GET /api/journal/entry/{id}` - Get entry
- `POST /api/journal/search` - Search entries

### Tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/pending` - Get pending tasks
- `GET /api/tasks/history` - Get completed tasks
- `POST /api/tasks/{id}/complete` - Complete task
- `PUT /api/tasks/{id}` - Update task

### User
- `GET /api/user/preferences` - Get preferences
- `PUT /api/user/preferences` - Update preferences
- `GET /api/user/timeline` - Get timeline status

## Technology Stack

**Backend:**
- FastAPI (async)
- SQLAlchemy + asyncpg
- PostgreSQL 16 + pgvector
- Pydantic
- Alembic migrations

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Zustand (state management)
- Axios (HTTP client)

**Infrastructure:**
- Cloud PostgreSQL
- Local development servers

## Development

### Testing Backend
```bash
cd backend
poetry run pytest -v
```

### Linting
```bash
# Backend
poetry run black app/
poetry run ruff check app/
poetry run mypy app/

# Frontend
npm run lint
```

### Database Migrations
```bash
# Create new migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Rollback
poetry run alembic downgrade -1
```

## Configuration

### Environment Variables

**Backend (.env):**
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key (REQUIRED)
- `SECRET_KEY`: App secret key
- `DEBUG`: Debug mode (True/False)
- `ANTHROPIC_API_KEY`: (Optional - not currently used)

**Frontend (.env.local):**
- `NEXT_PUBLIC_API_URL`: Backend URL (default: http://localhost:8000)

## Next Steps

1. **Week 1-3:** Infrastructure, Voice & Intake Agent ✅ DONE
2. **Week 4:** Memory Agent (Semantic Search & RAG) - NEXT
3. **Week 5:** Insight Agent (Recommendations & Alerts)
4. **Week 6-7:** UI Polish & Search Interface
5. **Week 8:** Testing & Deployment

## Documentation

**Main Documentation (Root Level):**
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete project overview
- [PROJECT_TASKS.md](PROJECT_TASKS.md) - Task tracking (100+ items)
- [FEATURES_IMPLEMENTED.md](FEATURES_IMPLEMENTED.md) - What's working now
- [STATUS_DASHBOARD.md](STATUS_DASHBOARD.md) - Progress metrics
- [READY_TO_TEST_WEEK3.md](READY_TO_TEST_WEEK3.md) - Testing instructions

**Technical Details:**
- [WEEK_3_INTAKE_AGENT.md](WEEK_3_INTAKE_AGENT.md) - Week 3 implementation
- [WEEK_2_COMPLETION.md](WEEK_2_COMPLETION.md) - Week 2 implementation
- [CLAUDE.md](CLAUDE.md) - Developer guide

**Detailed Reference:**
- `additional_docs/` - 26 files with detailed documentation

## Support

For issues or questions, check the project documentation or GitHub issues.

## License

MIT License
