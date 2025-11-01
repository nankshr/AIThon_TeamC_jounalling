# AI-Powered Wedding Journal - MVP

A complete AI-powered wedding journal application for intelligent planning and journaling.

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
cp .env.example .env
# Edit .env with your database URL and API keys
```

Configure with your cloud PostgreSQL:
```
DATABASE_URL=postgresql+asyncpg://username:password@host:port/wedding_journal
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your-secret-key
DEBUG=True
```

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

- ✅ Journal entry creation (text-based)
- ✅ Task management
- ✅ User preferences tracking
- ✅ Timeline awareness (pre/post-wedding)
- ⏳ AI entity extraction (coming next)
- ⏳ Semantic search (RAG implementation)
- ⏳ Voice transcription

## API Endpoints

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
- `ANTHROPIC_API_KEY`: Claude API key
- `OPENAI_API_KEY`: OpenAI key
- `SECRET_KEY`: App secret key
- `DEBUG`: Debug mode (True/False)

**Frontend (.env.local):**
- `NEXT_PUBLIC_API_URL`: Backend URL (default: http://localhost:8000)

## Next Steps

1. **Week 1-2:** Infrastructure & Voice ✅
2. **Week 3-5:** AI Agents (Entity extraction, RAG, Insights)
3. **Week 6-7:** UI Polish & Search
4. **Week 8:** Deployment

## Documentation

- [CLAUDE.md](CLAUDE.md) - Developer guide
- [PROJECT_PLAN.md](prd/PROJECT_PLAN.md) - Full project plan
- [QUICK_START_GUIDE.md](prd/QUICK_START_GUIDE.md) - Detailed setup

## Support

For issues or questions, check the project documentation or GitHub issues.

## License

MIT License
