# 🚀 Quick Start Guide - Wedding Journal

**Get up and running in 30 minutes!**

---

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.11 or higher
- [ ] Node.js 20 or higher  
- [ ] PostgreSQL 16
- [ ] Docker & Docker Compose
- [ ] Git
- [ ] **API Keys:**
  - [ ] Anthropic API key (get from: https://console.anthropic.com/)
  - [ ] OpenAI API key (get from: https://platform.openai.com/)
- [ ] Coolify server access (for deployment)

---

## Local Development Setup

### Step 1: Clone and Setup Project Structure

```bash
# Create project directory
mkdir wedding-journal
cd wedding-journal

# Initialize backend
mkdir backend frontend
cd backend
poetry init -n
cd ..
```

### Step 2: Backend Setup (10 minutes)

```bash
cd backend

# Install dependencies
poetry add fastapi uvicorn sqlalchemy asyncpg alembic
poetry add langchain langgraph anthropic openai pgvector
poetry add pydantic pydantic-settings python-multipart

# Create .env file
cat > .env << 'ENVFILE'
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/wedding_journal
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
DEBUG=True
ENVFILE

# Start PostgreSQL with pgvector
docker run -d \
  --name wedding-journal-db \
  -e POSTGRES_DB=wedding_journal \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# Setup database (after creating models and migrations)
poetry run alembic upgrade head

# Run backend
poetry run uvicorn app.main:app --reload
# Backend runs on http://localhost:8000
```

### Step 3: Frontend Setup (5 minutes)

```bash
cd ../frontend

# Create Next.js app
npx create-next-app@latest . --typescript --tailwind --app

# Install dependencies
npm install axios zustand

# Create .env.local
cat > .env.local << 'ENVFILE'
NEXT_PUBLIC_API_URL=http://localhost:8000
ENVFILE

# Run frontend
npm run dev
# Frontend runs on http://localhost:3000
```

---

## Phase-by-Phase Quick Reference

### Week 1-2: Foundation
**Focus:** Infrastructure + Voice Transcription

**Key Files to Create:**
```
backend/
  app/
    main.py                 # FastAPI app
    config.py              # Settings
    models/                # SQLAlchemy models
      journal.py
      entities.py
      tasks.py
    schemas/               # Pydantic schemas
      journal.py
    services/
      transcription.py     # Whisper API
      database.py
  alembic/                 # Migrations
  tests/
frontend/
  src/
    app/page.tsx          # Main page
    components/
      JournalInput.tsx
      VoiceRecorder.tsx
    lib/api.ts            # API client
```

**Test Voice Transcription:**
```bash
# Upload audio file
curl -X POST http://localhost:8000/api/transcription/transcribe \
  -F "audio=@test_audio.wav"
```

---

### Week 3-5: Core Intelligence
**Focus:** Agents + RAG

**Key Files to Create:**
```
backend/
  app/
    agents/
      prompts.py          # Claude prompts
      intake.py           # Entity extraction
      memory.py           # RAG search
      insight.py          # Contradictions
      task_manager.py     # Task management
      orchestrator.py     # LangGraph workflow
    services/
      embeddings.py       # OpenAI embeddings
      search.py           # Hybrid search
      entity_manager.py   # Deduplication
```

**Test Entity Extraction:**
```python
# Create test_agents.py
from app.agents.intake import intake_agent

async def test():
    state = JournalState(
        user_input="Met with Green Caterers today. Quoted ₹600 per plate for 200 guests.",
        language="en"
    )
    result = await intake_agent(state)
    print(f"Vendors: {result.entities['vendors']}")
    print(f"Costs: {result.entities['costs']}")
```

---

### Week 6-7: UX Polish
**Focus:** UI + Search

**Key Components:**
```
frontend/
  src/
    components/
      SuggestionToggle.tsx
      JournalingSidebar.tsx
      TaskReview.tsx
      SearchInterface.tsx
    hooks/
      useVoiceRecorder.ts
```

**Test Search:**
```bash
curl -X POST http://localhost:8000/api/journal/search \
  -H "Content-Type: application/json" \
  -d '{"query": "what did I say about venues?"}'
```

---

### Week 8: Deployment
**Focus:** Coolify Deployment

**Docker Setup:**
```bash
# Create Dockerfiles (see PROJECT_PLAN.md)
# Build images
docker compose build

# Test locally
docker compose up

# Push to GitHub
git add .
git commit -m "feat: complete MVP"
git push origin main
```

**Coolify Deployment:**
1. Login to Coolify
2. Create New Resource → Docker Compose
3. Connect GitHub repo
4. Set environment variables:
   - `DATABASE_URL`
   - `ANTHROPIC_API_KEY`
   - `OPENAI_API_KEY`
   - `SECRET_KEY`
5. Deploy!

---

## Common Commands

### Backend
```bash
# Run backend
poetry run uvicorn app.main:app --reload

# Create migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Run tests
poetry run pytest

# Check types
poetry run mypy app/
```

### Frontend
```bash
# Dev server
npm run dev

# Build
npm run build

# Start production
npm start

# Lint
npm run lint
```

### Database
```bash
# Connect to DB
psql -h localhost -U postgres -d wedding_journal

# View tables
\dt

# Query entries
SELECT id, raw_text, created_at FROM journal_entries;

# Vector search test
SELECT raw_text, 
       1 - (embedding <=> '[0.1, 0.2, ...]'::vector) AS similarity 
FROM journal_entries 
ORDER BY similarity DESC 
LIMIT 5;
```

---

## Troubleshooting

### "Module not found" errors
```bash
# Backend
cd backend
poetry install

# Frontend
cd frontend
npm install
```

### Database connection fails
```bash
# Check if PostgreSQL is running
docker ps | grep pgvector

# Restart if needed
docker restart wedding-journal-db

# Check connection
psql -h localhost -U postgres -d wedding_journal
```

### Whisper API fails
- Check OpenAI API key in `.env`
- Verify API credits/quota
- Test with small audio file first

### Claude API fails  
- Check Anthropic API key in `.env`
- Verify API credits
- Check rate limits (50 requests/min)

### pgvector not working
```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify
SELECT * FROM pg_extension WHERE extname = 'vector';
```

---

## Development Tips

### 1. Test Incrementally
Don't build everything at once! Test each component:
- Week 1: Test database, test API endpoints
- Week 3: Test entity extraction with 10 sample entries
- Week 4: Test search with known queries
- Week 6: Test full workflow end-to-end

### 2. Use Sample Data
Create `backend/tests/fixtures.py`:
```python
SAMPLE_ENTRIES = [
    {
        "text": "Visited Beach Resort today. Beautiful! ₹2,50,000 for 200 guests.",
        "expected_venues": ["Beach Resort"],
        "expected_costs": [250000]
    },
    # Add 20+ more
]
```

### 3. Monitor API Costs
```python
# Track LLM usage
async def log_llm_usage(model, tokens_in, tokens_out):
    cost = calculate_cost(tokens_in, tokens_out)
    print(f"[Cost] {model}: ${cost:.4f}")
    # Save to database
```

### 4. Debug LangGraph
```python
# Enable verbose logging
import langchain
langchain.debug = True

# Check state at each node
workflow.add_node("debug", lambda s: print(s) or s)
```

---

## API Testing with curl

### Create Entry
```bash
curl -X POST http://localhost:8000/api/journal/entry \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Spoke to Green Caterers. ₹600 per plate. Need to decide by Friday.",
    "language": "en",
    "suggestion_mode": true
  }'
```

### Search
```bash
curl -X POST http://localhost:8000/api/journal/search \
  -H "Content-Type: application/json" \
  -d '{"query": "caterers"}'
```

### Get Pending Tasks
```bash
curl http://localhost:8000/api/tasks/pending
```

---

## Performance Benchmarks

Target response times:
- **Text entry:** <2 seconds
- **Voice transcription:** <5 seconds  
- **Search query:** <1 second
- **Full workflow:** <10 seconds

If slower, check:
- Database query optimization
- RAG retrieval limit (reduce from 10 to 5)
- Claude API timeout settings
- Embedding cache hit rate

---

## Security Checklist

Before deploying:
- [ ] All API keys in environment variables (not hardcoded)
- [ ] HTTPS enabled (Coolify handles this)
- [ ] CORS properly configured
- [ ] Rate limiting on API endpoints
- [ ] Input validation on all endpoints
- [ ] Database backups automated
- [ ] Error logging configured
- [ ] No sensitive data in logs

---

## Next Steps After MVP

1. **Collect Usage Data**
   - How often user journals
   - Which suggestions are acted on
   - Search query patterns

2. **Gather Feedback**
   - What's most helpful?
   - What's missing?
   - What's confusing?

3. **Iterate**
   - Fix bugs
   - Improve accuracy
   - Add requested features

4. **Scale**
   - Multi-user support
   - Mobile app
   - More languages

---

## Resources

### Documentation
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [LangGraph Intro](https://langchain-ai.github.io/langgraph/)
- [Next.js Learn](https://nextjs.org/learn)
- [pgvector Guide](https://github.com/pgvector/pgvector)

### Example Code
- See `PROJECT_PLAN.md` for complete code examples
- Check `backend/tests/` for test patterns
- Review `frontend/src/components/` for UI patterns

### Getting Help
- GitHub Issues for bugs
- GitHub Discussions for questions
- Anthropic Discord for Claude API help
- Stack Overflow for general coding questions

---

**You've got this! Start with Week 1 and build incrementally. 🚀**

Remember: 
- Test early, test often
- Don't optimize prematurely  
- User feedback > perfect code
- Ship the MVP, then iterate!

Good luck! 🎉
