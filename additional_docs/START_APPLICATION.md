# Start the Application - Quick Guide

**Status:** ✅ Ready to Run
**Date:** November 1, 2025

---

## 🚀 Quick Start (Copy & Paste)

### Option A: Two Separate Terminals

**Terminal 1 - Backend:**
```bash
cd backend
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open **http://localhost:3000** in your browser.

---

### Option B: One Terminal (Sequential)

**Terminal 1:**
```bash
cd backend
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
cd ../frontend
npm run dev
```

---

## ✅ Verification Checklist

After starting both servers:

### Backend Verification
```
Open http://localhost:8000/docs
✅ Should see Swagger API documentation
✅ Try POST /api/journal/entries endpoint
✅ Try GET /docs works
```

### Frontend Verification
```
Open http://localhost:3000
✅ Should see journal entry form
✅ Should see "Record voice or type" section
✅ Should see textarea "What's on your mind?"
✅ Should see "Save Entry" button
```

---

## 🧪 Test AI Suggestions Feature

After both are running:

1. **Type in textarea:**
   ```
   Need to book photographer and florist.
   Wedding is June 15.
   Budget: $5000.
   ```

2. **Click "✨ Get AI Suggestions"**
   - Wait 2-5 seconds for AI processing
   - See green box with suggestions

3. **Verify:**
   - ✅ Green box appeared
   - ✅ Shows "✓ AI Analysis"
   - ✅ Shows "Tasks Identified: X"
   - ✅ Shows suggested tasks with full details
   - ✅ Tasks have checkboxes (checked by default)
   - ✅ Priority badges are colored (red/amber/blue)

4. **Click "Save Entry"**
   - ✅ Green box disappears
   - ✅ Form clears
   - ✅ Success message shows
   - ✅ Tasks created in database

5. **Check Console (F12)**
   - ✅ See `[Tasks] Creating X tasks:`
   - ✅ See `[Tasks] Successfully created task:`
   - ✅ No errors shown

---

## 📋 What Works

### ✅ Completed Features

1. **Voice Recording**
   - Click 🎤 to record
   - ⏹️ to stop
   - ▶️ to playback
   - 📤 to use transcription

2. **Text Entry**
   - Type or paste text
   - Multi-language support
   - Rich text support

3. **AI Suggestions** ← NEWLY FIXED ✨
   - Click "✨ Get AI Suggestions"
   - See analysis with full task details
   - Tasks have colored priority badges
   - Full task information shown:
     - Title
     - Description
     - Deadline
     - Status
     - Priority

4. **Task Creation** ← NEWLY FIXED ✨
   - Suggested tasks created when "Save Entry" clicked
   - Only checked tasks are created
   - Tasks appear in database
   - Success message shown

5. **Task Selection**
   - All tasks checked by default
   - Click checkbox to uncheck
   - Click card to toggle
   - Only checked tasks created

---

## 🔧 Environment Setup

### Backend (.env in backend/ folder)
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/wedding_journal
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here (if using Claude)
SECRET_KEY=your-secret-key
DEBUG=True
```

### Frontend (.env.local in frontend/ folder)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📊 Success Indicators

### Backend Running ✅
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Frontend Running ✅
```
Ready in Xs

▲ Local:        http://localhost:3000
▲ Environments: .env.local

> Local:        http://localhost:3000
```

### API Working ✅
```
✅ http://localhost:8000/docs loads (Swagger)
✅ http://localhost:8000/redoc loads (ReDoc)
```

### App Working ✅
```
✅ Journal form loads
✅ Textarea visible
✅ Buttons visible
✅ No console errors
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill it (or change port)
poetry run uvicorn app.main:app --port 8001

# Find what's using port 3000
lsof -i :3000

# Change port
npm run dev -- -p 3001
```

### Dependencies Missing
```bash
# Reinstall backend
cd backend
poetry install

# Reinstall frontend
cd frontend
npm install
```

### Database Connection Error
```bash
# Check if PostgreSQL is running
psql -h localhost -U postgres

# Create database if needed
createdb wedding_journal

# Run migrations
cd backend
poetry run alembic upgrade head
```

### API Connection Error
```
Error in frontend: "Failed to fetch..."

Solution:
1. Verify backend is running on port 8000
2. Check NEXT_PUBLIC_API_URL in .env.local
3. Verify CORS enabled in backend
4. Check firewall settings
```

### AI Features Not Working
```
Error: "Failed to extract data..."

Solution:
1. Check OPENAI_API_KEY is set
2. Check API key is valid and has credits
3. Check rate limits not exceeded
4. See backend logs for details
```

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| `TESTING_AI_SUGGESTIONS.md` | Complete test guide with all scenarios |
| `FIXES_SUMMARY.md` | What was fixed and how |
| `VISUAL_GUIDE.md` | UI mockups and screen layouts |
| `SUGGESTIONS_FIX.md` | Technical fix details |
| `VERIFY_TASK_FIX.md` | Quick verification steps |
| `RUN_COMPLETE_APP.md` | Full app documentation |

---

## 🎯 Next Steps

### Immediate (Right Now)
1. Start backend: `poetry run uvicorn app.main:app --reload`
2. Start frontend: `npm run dev`
3. Open http://localhost:3000
4. Follow `TESTING_AI_SUGGESTIONS.md`

### After Testing (Once Verified)
- [ ] Run all test scenarios
- [ ] Verify database has tasks
- [ ] Check console logs look correct
- [ ] Document any issues found
- [ ] Plan V2 enhancements

### Production Ready
- [ ] All tests pass
- [ ] No console errors
- [ ] Tasks created reliably
- [ ] Suggestions persist correctly
- [ ] UI looks good

---

## 💡 Pro Tips

1. **Open Console Early**
   - Press F12 while app loads
   - Watch `[Tasks]` logs
   - Catch errors immediately

2. **Use Two Monitors**
   - One for app
   - One for console
   - Easier debugging

3. **Keep Terminals Open**
   - Don't close during testing
   - Easy to see startup messages
   - Can spot errors immediately

4. **Test Multiple Entries**
   - Different text inputs
   - Different task counts
   - Different selections
   - Edge cases

5. **Check Network Tab**
   - F12 → Network
   - Watch API calls
   - See request/response bodies
   - Spot connection issues

---

## 📞 Getting Help

**If something doesn't work:**

1. Check console (F12) for error messages
2. Check backend terminal for log output
3. Check frontend terminal for build errors
4. Review `TESTING_AI_SUGGESTIONS.md`
5. Check connection between frontend and backend
6. Verify environment variables are set
7. Restart both backend and frontend
8. Clear browser cache (Ctrl+Shift+Delete)
9. Reinstall dependencies if needed

---

## ✨ Features Ready to Test

**AI Suggestions Feature** ← Main Focus
- ✅ Type text
- ✅ Click "Get AI Suggestions"
- ✅ See full task details in green box
- ✅ Suggestions persist until save
- ✅ Select/deselect tasks with checkboxes
- ✅ Click "Save Entry"
- ✅ Tasks created in database
- ✅ Success message shown
- ✅ Form clears

---

**Ready to Start! 🚀**

Run the commands above and start testing the AI Suggestions feature.

See `TESTING_AI_SUGGESTIONS.md` for comprehensive test scenarios.
