# 🎉 AI-Powered Wedding Journal - Project Plan

**Version:** 1.0  
**Last Updated:** November 1, 2025  
**Timeline:** 8 Weeks  
**Target:** Self-hosted MVP on Coolify

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Phase-by-Phase Breakdown](#phase-by-phase-breakdown)
- [Success Metrics](#success-metrics)
- [Future Roadmap](#future-roadmap)

---

## Project Overview

### Problem Statement
Wedding planning is overwhelming with scattered information, conflicting priorities (budget vs. desires), and forgotten tasks. Traditional journaling lacks intelligence to surface patterns, contradictions, or actionable insights.

### Solution
An AI-powered private journal that:
- Captures multilingual voice/text entries (English & Tamil)
- Automatically extracts themes, entities (vendors, venues, costs, dates)
- Provides real-time, context-aware suggestions (toggle mode)
- Tracks tasks and reminds users at each session
- Detects major contradictions with stated values (budget, eco-friendly)
- Uses semantic search to recall past discussions
- Adapts based on timeline (pre vs. post-wedding)

### Core Features (MVP)
✅ **Multi-turn conversational journaling** (voice + text)  
✅ **Real-time voice transcription** (English & Tamil)  
✅ **Auto-entity extraction** (vendors, venues, dates, costs)  
✅ **Theme classification** (budget concerns, eco-friendly, stress, etc.)  
✅ **Task management** (auto-log + review interface)  
✅ **Semantic search** (RAG-powered: "What did I say about venues?")  
✅ **Contradiction detection** (only major: budget blowout, deadline pressure)  
✅ **Timeline awareness** (wedding date tracking, post-wedding mode)  
✅ **Multi-agent orchestration** (LangGraph)

---

## Tech Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI (async)
- **Agent Orchestration:** LangGraph + LangChain
- **Database:** PostgreSQL 16 + pgvector
- **ORM:** SQLAlchemy (async)

### AI & ML
- **LLM:** Claude 3.5 Sonnet (Anthropic)
- **Voice:** Whisper API (OpenAI)
- **Embeddings:** OpenAI text-embedding-3-small
- **Vector Search:** pgvector

### Frontend
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Voice:** Web Audio API

### Infrastructure
- **Hosting:** Self-hosted on Coolify
- **Containers:** Docker + Docker Compose
- **SSL:** Automatic via Coolify/Caddy

---

## System Architecture

### Multi-Agent Workflow

```
User Input (Voice/Text)
    ↓
[Transcription] → Whisper API
    ↓
[Intake Agent] → Extract entities, themes, tasks
    ↓
[Memory Agent] → RAG search (semantic + keyword)
    ↓
[Insight Agent] → Detect contradictions, suggest next steps
    ↓
[Task Manager] → Auto-log tasks, retrieve reminders
    ↓
[Response Synthesizer] → Generate natural response
    ↓
User Response (with suggestions, reminders, insights)
```

---

## Phase-by-Phase Breakdown

## Phase 1: Foundation (Weeks 1-2)

### Week 1: Infrastructure Setup

**Goal:** Project structure, database, API skeleton

#### Tasks:
- [ ] Initialize Python + Next.js projects
- [ ] Setup PostgreSQL with pgvector
- [ ] Create database schema
- [ ] Build FastAPI skeleton
- [ ] Create basic Next.js UI
- [ ] Setup Docker development environment

**Deliverables:**
- Clean project structure
- Working database with migrations
- API endpoints (stubs)
- Functional UI that connects to backend

---

### Week 2: Voice & Transcription

**Goal:** Real-time voice transcription (English & Tamil)

#### Tasks:
- [ ] Integrate Whisper API
- [ ] Build voice recorder component
- [ ] Implement real-time transcription
- [ ] Add language detection
- [ ] Test with English and Tamil samples

**Deliverables:**
- Working voice-to-text pipeline
- UI with voice recording capability
- Language toggle (EN/TA)

---

## Phase 2: Core Intelligence (Weeks 3-5)

### Week 3: Intake Agent + Entity Extraction

**Goal:** Extract structured data from journal entries

#### Tasks:
- [ ] Design Claude prompts for entity extraction
- [ ] Build intake agent
- [ ] Implement entity deduplication (fuzzy matching)
- [ ] Create entity linking system
- [ ] Test with 20+ sample entries
- [ ] Validate >80% accuracy

**Key Components:**
- **Entities:** Vendors, venues, costs, dates, people
- **Themes:** Budget, eco-friendly, stress, timeline pressure
- **Tasks:** Explicit + implicit action items
- **Sentiment:** Emotional tone analysis

**Deliverables:**
- Intake agent with high accuracy
- Entity deduplication system
- Master entity records

---

### Week 4: Memory Agent + RAG

**Goal:** Semantic search across past entries

#### Tasks:
- [ ] Setup OpenAI embeddings
- [ ] Implement vector similarity search (pgvector)
- [ ] Build keyword search (PostgreSQL full-text)
- [ ] Create hybrid search (semantic + keyword + time-weighted)
- [ ] Add entity-based search
- [ ] Test retrieval quality

**Search Types:**
1. **Semantic:** "Tell me about budget-friendly options"
2. **Keyword:** "Green Caterers"
3. **Entity:** "All entries mentioning Beach Resort"
4. **Hybrid:** Combined with time decay

**Deliverables:**
- Production-ready RAG system
- Hybrid search with >90% relevance
- Entity history retrieval

---

### Week 5: Insight Agent + Task Manager

**Goal:** Generate insights and manage tasks

#### Tasks:
- [ ] Implement contradiction detection
  - Budget blowout (>20% over goal)
  - Deadline pressure (<30 days, >5 critical tasks)
  - Eco-conflicts (major violations only)
- [ ] Build next-steps generation (Claude)
- [ ] Create task auto-logging system
- [ ] Implement task reminders
- [ ] Add task completion handler

**Deliverables:**
- Contradiction detection (major only)
- AI-generated next steps
- Complete task management system

---

## Phase 3: User Experience (Weeks 6-7)

### Week 6: UI Polish + Real-Time Suggestions

**Goal:** Polished interface with toggle suggestions

#### Tasks:
- [ ] Build LangGraph orchestrator (connect all agents)
- [ ] Create suggestion toggle UI
- [ ] Implement non-intrusive sidebar for suggestions
- [ ] Build task review interface
- [ ] Add session greeting with reminders
- [ ] Implement loading states and animations

**UI Components:**
- **Suggestion Toggle:** User controls when to see AI insights
- **Sidebar:** Shows contradictions, next steps, insights
- **Task Review:** Auto-logged tasks with completion checkboxes
- **Greeting:** Context-aware based on timeline and pending tasks

**Deliverables:**
- Complete LangGraph workflow
- Polished, non-intrusive UI
- Real-time suggestion system

---

### Week 7: Semantic Search Interface + Timeline

**Goal:** Search functionality and timeline awareness

#### Tasks:
- [ ] Build search interface
  - Natural language queries
  - Entity-based filtering
  - Date range filtering
- [ ] Implement timeline awareness
  - Wedding date tracking
  - Pre-wedding mode (urgency levels)
  - Post-wedding mode (reflective questions)
- [ ] Create post-wedding prompts
- [ ] Add entry list/history view

**Timeline Modes:**
1. **Planning:** Days until wedding, urgency indicators
2. **Wedding Day:** Special greeting
3. **Post-Wedding (Day 1):** "How did it go?"
4. **Post-Wedding (Ongoing):** Reflective journaling

**Deliverables:**
- Full semantic search interface
- Timeline-aware system
- Post-wedding reflection mode

---

## Phase 4: Deployment (Week 8)

### Week 8: Deployment to Coolify

**Goal:** Production deployment

#### Tasks:
- [ ] Create Dockerfiles (backend + frontend)
- [ ] Write docker-compose.yml
- [ ] Setup environment variables securely
- [ ] Configure Coolify deployment
- [ ] Setup PostgreSQL on Coolify
- [ ] Deploy backend + frontend
- [ ] Configure SSL/HTTPS (automatic via Caddy)
- [ ] Setup database backups
- [ ] Add monitoring/logging (Sentry optional)
- [ ] Test production deployment
- [ ] Document deployment process

**Security Checklist:**
- [ ] HTTPS enabled
- [ ] API rate limiting
- [ ] Environment variables secured
- [ ] Database backups automated
- [ ] Error logging configured

**Deliverables:**
- Production-ready application on Coolify
- Deployment documentation
- Monitoring setup

---

## Detailed Technical Implementation

### Database Schema

```sql
-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- User preferences
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY,
    values TEXT[] DEFAULT '{}',
    budget_goal DECIMAL(10, 2),
    wedding_date DATE,
    primary_language VARCHAR(10) DEFAULT 'en',
    suggestion_mode_default BOOLEAN DEFAULT TRUE,
    post_wedding_mode BOOLEAN DEFAULT FALSE
);

-- Journal entries
CREATE TABLE journal_entries (
    id UUID PRIMARY KEY,
    session_id UUID NOT NULL,
    user_id UUID REFERENCES user_preferences(id),
    created_at TIMESTAMP DEFAULT NOW(),
    raw_text TEXT NOT NULL,
    language VARCHAR(10) NOT NULL,
    themes TEXT[],
    sentiment VARCHAR(50),
    embedding vector(1536),  -- pgvector
    suggestion_mode_active BOOLEAN DEFAULT FALSE
);

-- Entities (extracted)
CREATE TABLE entities (
    id UUID PRIMARY KEY,
    entry_id UUID REFERENCES journal_entries(id) ON DELETE CASCADE,
    entity_type VARCHAR(50) NOT NULL,
    entity_name TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    canonical_id UUID,  -- Links to master entity
    confidence FLOAT DEFAULT 1.0
);

-- Master entities (deduplicated)
CREATE TABLE master_entities (
    id UUID PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    canonical_name TEXT NOT NULL,
    first_mentioned TIMESTAMP,
    last_mentioned TIMESTAMP,
    mention_count INT DEFAULT 1,
    decision_made BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}'
);

-- Tasks
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES user_preferences(id),
    entry_id UUID REFERENCES journal_entries(id),
    action TEXT NOT NULL,
    deadline DATE,
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'pending',
    completed_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_entries_embedding ON journal_entries 
USING ivfflat (embedding vector_cosine_ops);
```

---

### API Endpoints

#### Journal
- `POST /api/journal/entry` - Create new entry
- `GET /api/journal/entries` - List all entries
- `GET /api/journal/entry/{id}` - Get specific entry
- `POST /api/journal/search` - Semantic search

#### Transcription
- `POST /api/transcription/transcribe` - Transcribe audio

#### Tasks
- `GET /api/tasks/pending` - Get pending tasks
- `POST /api/tasks/{id}/complete` - Mark task complete
- `GET /api/tasks/history` - Task history

#### User
- `GET /api/user/preferences` - Get user preferences
- `PUT /api/user/preferences` - Update preferences
- `GET /api/user/timeline` - Timeline status

---

### Docker Deployment

**Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: wedding_journal
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  backend:
    build: ./backend
    depends_on:
      - db
    environment:
      DATABASE_URL: ${DATABASE_URL}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
  
  frontend:
    build: ./frontend
    depends_on:
      - backend
    environment:
      NEXT_PUBLIC_API_URL: ${API_URL}

volumes:
  postgres_data:
```

---

## Cost Estimates

### Monthly Operating Costs

| Service | Cost |
|---------|------|
| Coolify hosting | Self-hosted (server cost only) |
| Anthropic Claude API | $20-40 |
| OpenAI Whisper API | $10-20 |
| OpenAI Embeddings | $2-5 |
| **Total** | **$32-65/month** |

**Cost Optimization:**
- Cache embeddings (don't regenerate)
- Use Claude Haiku for simple tasks
- Limit voice transcription length
- Consider Gemini Flash as cheaper alternative

---

## Success Metrics

### After 4 Weeks of Usage:

1. **Engagement:** ≥3 journal entries per week
2. **Accuracy:** 
   - 80%+ entity extraction accuracy
   - 70%+ task auto-detection accuracy
3. **Utility:**
   - User acts on ≥40% of AI suggestions
   - Uses semantic search ≥1x per week
4. **Value:**
   - User reports feeling "more organized"
   - At least 1 decision made easier due to AI insights

---

## Future Roadmap

### V2 Features (Post-MVP)
- 📱 Mobile app (React Native)
- 🗣️ More languages (Hindi, Kannada, Telugu, Malayalam)
- 📸 Photo uploads (venue pics, vendor samples)
- 🤝 Shared journaling (partner can add entries)
- 📊 Budget visualization dashboard
- 🔗 Vendor directory integration
- ✉️ Email parsing (auto-capture vendor quotes)
- 📅 Calendar integration (auto-add deadlines)

### V3 (Full Product)
- 🎯 AI wedding planning assistant (not just journaling)
- 🌍 Public vendor reviews (aggregated, anonymized)
- 🤖 Proactive reminders (SMS/WhatsApp)
- 📋 Template workflows (traditional, destination, eco-weddings)
- 💰 Budget optimization suggestions
- 🎨 Vendor matching (AI-powered recommendations)

---

## Development Guidelines

### Code Quality
- Write type hints for all Python functions
- Use TypeScript for all frontend code
- Add docstrings to all functions
- Write unit tests for critical paths
- Use ESLint + Prettier for formatting

### Git Workflow
- `main` branch for production
- `develop` branch for integration
- Feature branches: `feature/entity-extraction`
- Commit messages: `feat: add entity deduplication`

### Testing Strategy
- Unit tests for agents
- Integration tests for API endpoints
- End-to-end tests for critical user flows
- Manual testing for voice transcription quality

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 16
- Docker & Docker Compose
- API keys: Anthropic, OpenAI

### Quick Start

```bash
# Clone repo
git clone https://github.com/yourusername/wedding-journal.git
cd wedding-journal

# Backend setup
cd backend
poetry install
cp .env.example .env
# Edit .env with your API keys
alembic upgrade head
poetry run uvicorn app.main:app --reload

# Frontend setup (new terminal)
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local
npm run dev

# Visit http://localhost:3000
```

### Deployment to Coolify

1. Push code to GitHub
2. Create new app in Coolify
3. Connect GitHub repo
4. Set environment variables in Coolify
5. Deploy!

---

## Support & Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Anthropic API Docs](https://docs.anthropic.com/)

### Community
- GitHub Issues for bugs
- Discussions for feature requests

---

## License

MIT License - see LICENSE file

---

**Happy Building! 🎉**

Remember: This is YOUR wedding journal. Make it personal, make it helpful, and most importantly - make it reduce stress, not add to it.

Good luck with your wedding planning journey! 💐
