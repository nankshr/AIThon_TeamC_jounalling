# 🚀 START HERE - Wedding Journal MVP

**Everything is built and ready to run!** Follow these 5 simple steps.

## ⚡ Quick Start (5 minutes)

### Step 1: Configure Database (1 minute)

Edit `backend/.env`:

```bash
# Open backend/.env
# Replace these with your cloud PostgreSQL credentials:
DATABASE_URL=postgresql+asyncpg://username:password@cloud-host.example.com:5432/wedding_journal
```

That's it for now. API keys are optional for Phase 1.

### Step 2: Setup Backend (2 minutes)

```bash
cd backend
poetry install
poetry run alembic upgrade head
```

### Step 3: Run Backend

```bash
poetry run uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is ready!

### Step 4: Run Frontend

Open **a new terminal**:

```bash
cd frontend
npm install
npm run dev
```

You should see:
```
  ▲ Next.js 14.0.0
  - Local:        http://localhost:3000
```

✅ Frontend is ready!

### Step 5: Test It!

Open `http://localhost:3000` in your browser and:

1. **Create an entry:** "I'm so excited about the wedding planning!"
2. **Create a task:** "Call the caterer" with priority "High"
3. **Complete the task:** Click the circle icon

Done! ✨

---

## 📋 What Works Now

✅ Journal entries (create, view)
✅ Task management (create, complete, delete)
✅ User preferences (wedding date, budget)
✅ Beautiful UI with Tailwind CSS
✅ All data saved to your PostgreSQL

---

## 🐛 Quick Troubleshooting

**Backend won't start?**
```bash
# Check if port 8000 is free
lsof -i :8000

# Or use different port
poetry run uvicorn app.main:app --port 8001 --reload
```

**Frontend can't connect to API?**
- Verify backend is running on port 8000
- Check your `frontend/.env.local` has correct API URL
- Open browser console (F12) to see actual error

**Database connection error?**
- Verify `DATABASE_URL` in `backend/.env`
- Test connection: `psql $DATABASE_URL`
- Ask your cloud provider for connection help

---

## 📚 Full Documentation

For detailed info, see:
- **SETUP_GUIDE.md** - Complete step-by-step setup
- **VERIFICATION.md** - How to test everything
- **BUILD_SUMMARY.md** - What was built
- **CLAUDE.md** - For developers/Claude Code
- **README.md** - Project overview

---

## 🎯 Next: Phase 2 - AI Features

Once MVP works, we'll add:
- ✨ Voice transcription
- 🤖 Entity extraction (vendors, venues, costs)
- 🔍 Semantic search
- 💡 AI suggestions
- 🎯 Task auto-generation

---

## 📞 Support

If you get stuck:

1. Check SETUP_GUIDE.md "Troubleshooting" section
2. Check VERIFICATION.md for error details
3. Verify your PostgreSQL connection
4. Check browser console (F12) for frontend errors
5. Check terminal for backend errors

---

**That's it! You're ready to go!** 🎉

Start creating journal entries and tasks. Enjoy! 💐
