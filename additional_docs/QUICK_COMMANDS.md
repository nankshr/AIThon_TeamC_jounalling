# Quick Commands Reference

## 🚀 Start Development

### Terminal 1: Backend
```bash
cd backend
poetry run uvicorn app.main:app --reload
```
Backend runs on: http://localhost:8000

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:3000

---

## 🧪 Testing

### Test OpenAI Connection
```bash
cd backend
poetry run python test_openai_connection.py
```

### Test Intake Agent
```bash
cd backend
poetry run python test_intake_agent.py
```

---

## 📝 Documentation Files

### To Read First
```bash
# Overview
cat PROJECT_SUMMARY.md

# What's working
cat FEATURES_IMPLEMENTED.md

# Tasks & progress
cat PROJECT_TASKS.md

# Testing guide
cat READY_TO_TEST_WEEK3.md
```

### Status Checks
```bash
# Current progress
cat STATUS_DASHBOARD.md

# Implementation details
cat IMPLEMENTATION_SUMMARY.md

# Completion summary
cat COMPLETION_SUMMARY.md
```

---

## 🔍 Code Organization

### Backend Structure
```bash
backend/
├── app/agents/          # AI agents
│   └── intake.py       # Entity extraction
├── app/routers/        # API endpoints
│   ├── transcription.py
│   └── entries.py
├── app/services/       # Business logic
│   └── transcription.py
└── app/models/         # Database models
```

### Frontend Structure
```bash
frontend/
└── src/components/     # React components
    ├── VoiceRecorder.tsx   # Voice input
    └── JournalInput.tsx    # Entry form + AI
```

---

## 🎯 Common Tasks

### Install Dependencies
```bash
# Backend
cd backend && poetry install

# Frontend
cd frontend && npm install
```

### Update Dependencies
```bash
# Backend
cd backend && poetry lock && poetry install

# Frontend
cd frontend && npm install
```

### Database Migrations
```bash
cd backend
poetry run alembic upgrade head
```

### Code Quality (Backend)
```bash
cd backend
poetry run black app/
poetry run ruff check app/
poetry run mypy app/
```

### Code Quality (Frontend)
```bash
cd frontend
npm run lint
npm run build
```

---

## 📊 Project Status

### Current (50% Complete)
✅ Week 1-3: Infrastructure, Voice, AI Extraction

### Pending (50% Remaining)
⏳ Week 4-8: Memory Agent, Insights, UI, Testing, Deploy

### Documentation
- 14 files at root level
- 26 files in additional_docs/
- Total: 40 files, ~480KB

---

## 🔗 Key Files

### Essential
- PROJECT_SUMMARY.md - Overview
- PROJECT_TASKS.md - Tasks
- FEATURES_IMPLEMENTED.md - What works
- READY_TO_TEST_WEEK3.md - Testing

### Technical
- WEEK_3_INTAKE_AGENT.md - AI details
- WEEK_2_COMPLETION.md - Voice details
- CLAUDE.md - Developer guide

### Reference
- additional_docs/ - 26 archived files

---

## 💡 Tips

### Frontend Dev
- Press F12 for browser console
- Check Network tab for API calls
- Use React DevTools extension

### Backend Dev
- Check terminal for logs (uvicorn output)
- Use OpenAI API dashboard for usage tracking
- Test endpoints at http://localhost:8000/docs

### Database
- Use pgAdmin or psql to inspect data
- Check migrations with: poetry run alembic current

---

## ❌ Troubleshooting

### Backend won't start
```bash
# Check dependencies
cd backend && poetry install

# Check database connection
# Update DATABASE_URL in .env
```

### Transcription slow
```bash
# Check OpenAI status
# Wait up to 20 seconds (Whisper can be slow)
# Check API usage: https://platform.openai.com
```

### Frontend can't reach backend
```bash
# Check NEXT_PUBLIC_API_URL in frontend/.env.local
# Ensure backend is running on 8000
# Check browser console (F12) for CORS errors
```

### API returns 500 error
```bash
# Check backend logs (uvicorn terminal)
# Check API keys in .env
# Try restarting backend
```

---

## 📞 Next Steps

1. **Start:** `cd backend && poetry run uvicorn app.main:app --reload`
2. **In another terminal:** `cd frontend && npm run dev`
3. **Test:** Go to http://localhost:3000
4. **Read:** PROJECT_SUMMARY.md for overview
5. **Plan:** Check PROJECT_TASKS.md for next work

---

**Happy coding! 🚀**
