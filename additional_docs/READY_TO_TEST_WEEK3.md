# Ready to Test - Week 3 (Intake Agent Complete)

**Status:** ✅ READY FOR TESTING
**Date:** November 1, 2025

---

## 🎯 What's New This Week

### ✨ Intake Agent with OpenAI LLM
- Replaces Anthropic with OpenAI GPT-4-Turbo
- Extracts entities (vendors, venues, costs, dates, people)
- Identifies tasks (explicit + implicit)
- Detects sentiment and themes
- Determines timeline (pre/post-wedding)

### 📡 New API Endpoints
```
POST /api/journal/entries
  - Full entry processing with all extractions

POST /api/journal/entries/{id}/extract-entities
POST /api/journal/entries/{id}/extract-tasks
POST /api/journal/entries/{id}/analyze-sentiment
```

### 🖥️ Enhanced Frontend
- Shows "Processing with AI..." during analysis
- Displays extracted data summary box
- Shows vendors found, tasks identified, mood, timeline

---

## 🚀 How to Test

### Step 1: Start Backend
```bash
cd backend
poetry run uvicorn app.main:app --reload
```

Wait for: `Application startup complete`

### Step 2: Start Frontend
```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:3000`

### Step 3: Test Via Frontend (Easiest)
1. Open http://localhost:3000
2. Type a journal entry:
   ```
   Had a great meeting with the caterer today!
   They offered a vegetarian menu for $2000 for 100 guests.
   I need to decide between them and Fresh & Modern Catering.
   Also need to book the photographer before they get booked up.
   Wedding date is June 15, 2025.
   ```
3. Click "Save Entry"
4. Watch backend logs for processing
5. See green "AI Analysis Complete" box appear with:
   - ✓ Vendors Found
   - ✓ Tasks Identified
   - ✓ Mood
   - ✓ Timeline

### Step 4: Test Via CLI (For Developers)
```bash
cd backend
poetry run python test_intake_agent.py
```

Expected output:
- Test 1: Extracts 3 vendors, 3+ tasks, detected stress
- Test 2: Extracts 14+ tasks, budget and stress themes

### Step 5: Test Via API (cURL)
```bash
curl -X POST http://localhost:8000/api/journal/entries \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Booked the venue! It was $5000 for the date but the discount for off-season made it $3500. Still need to confirm catering and photography. Getting excited about the wedding!",
    "language": "en",
    "transcribed_from_audio": false
  }'
```

Expected response:
```json
{
  "success": true,
  "message": "Entry processed successfully",
  "data": {
    "entities": {
      "vendors": [...],
      "venues": [...],
      "costs": [...],
      "dates": [...]
    },
    "tasks": {
      "explicit": [...],
      "implicit": [...]
    },
    "sentiment": {"emotion": "excited", "confidence": 0.9},
    "themes": ["excitement", "budget"],
    "timeline": "pre-wedding"
  }
}
```

---

## ✅ What to Verify

### Backend Logs
When processing an entry, you should see:
```
INFO: Processing journal entry: 250 characters, language: en
INFO: Calling OpenAI GPT-4 for entity extraction
INFO: OpenAI response received: 1200 characters
INFO: Extracted entities - vendors: 2, tasks: 3 explicit + 1 implicit
```

### Frontend Display
You should see:
- Blue "Processing with AI..." indicator
- Green checkmark box appears after 2-5 seconds
- Shows count of extracted items
- Shows detected mood/emotion
- Shows timeline classification

### API Response
- HTTP 200 status code
- Valid JSON with "success": true
- Data contains all extracted fields
- No errors in response

---

## 🧪 Test Scenarios

### Scenario 1: Vendor Selection (Budget Focused)
**Input:**
```
Met with three caterers today. Options:
1. Budget Caterer - $1500 for 100 guests
2. Premium Catering - $3500 for 100 guests
3. Eco-Friendly Organic - $2500 for 100 guests

We have a $30,000 budget and this is eating into it.
Need to decide by end of week.
Wedding is June 15, 2025.
```

**Expected Extractions:**
- 3 vendors with costs
- Wedding date (June 15, 2025)
- 1 decision task (high priority)
- Sentiment: stressed about budget
- Themes: budget, decision-making

---

### Scenario 2: Task-Heavy Entry (Overwhelm)
**Input:**
```
So much to do and feeling overwhelmed!

TO-DO:
- Finalize guest list (deadline: this Friday)
- Send invitations to 150 people
- Confirm catering headcount
- Book photographer
- Get dress tailored
- Arrange transportation
- Book honeymoon flights
- Register for gifts
- Buy wedding favors

My partner isn't helping much. This is all on me.
We're already over budget spending $18,000 when we planned $15,000.
```

**Expected Extractions:**
- 9+ explicit tasks with priorities
- 1-2 implicit tasks (budget overrun, partner involvement)
- Sentiment: very stressed, confident
- Themes: stress, budget overrun, task load
- Many high priority tasks

---

### Scenario 3: Voice Recording Flow
**Steps:**
1. Click 🎤 microphone button
2. Speak: "Just booked the venue for June 15. Cost $4000. Still need to find a photographer and book catering."
3. Click ⏹️ stop button
4. Click ▶️ to hear playback
5. Click 📤 upload button
6. Backend transcribes with Whisper API
7. Transcribed text automatically sent to Intake Agent
8. Watch "Processing with AI..." appear
9. See extracted data box appear with:
   - Venue found (June 15)
   - Vendors: 0 (venue booked, others pending)
   - Tasks: 2 (photographer, catering)
   - Mood: excited/neutral
   - Timeline: pre-wedding

---

## 📊 What to Look For

### Success Indicators
- ✅ Entries process in 2-5 seconds
- ✅ No 500 errors in backend
- ✅ JSON response is valid
- ✅ All entities extracted correctly
- ✅ Tasks marked with correct priority
- ✅ Dates in YYYY-MM-DD format
- ✅ Costs as numeric values
- ✅ Sentiment confidence 0.0-1.0
- ✅ Frontend shows data summary

### Common Issues
- ❌ Processing takes >10 seconds = OpenAI API slow
- ❌ 500 error = Check backend logs for error
- ❌ Invalid JSON = Response format issue
- ❌ No data extracted = Prompt issue (unlikely)
- ❌ Frontend doesn't show box = API call failed silently

---

## 🔍 Debugging

### If Frontend Shows Error:
1. Press F12 to open browser console
2. Look for error message in Console tab
3. Check Network tab for failed API request
4. See what response status code is

### If Backend Shows Error:
1. Look at terminal running uvicorn
2. Find the error traceback
3. Most common: OpenAI API key invalid
4. Check: `OPENAI_API_KEY` in .env file

### If Processing Hangs:
1. Wait up to 10 seconds
2. If still hanging, OpenAI API is slow
3. Try again - might be temporary
4. Check OpenAI status: https://status.openai.com/

### If No Data Extracted:
1. Entry text might be too ambiguous
2. Try entry with clear information
3. Check backend logs for details
4. Look at actual LLM response

---

## 📋 Checklist Before Testing

- [ ] Backend running: `poetry run uvicorn app.main:app --reload`
- [ ] Frontend running: `npm run dev`
- [ ] OPENAI_API_KEY set in backend/.env
- [ ] Browser at http://localhost:3000
- [ ] Backend logs visible in terminal
- [ ] Browser console ready (F12)

---

## 🎉 After Testing

### If Everything Works:
1. Test a few more entries manually
2. Try voice recording + transcription + AI analysis
3. Check backend logs are clean
4. Check tokens used are reasonable

### Then Ready For:
- Week 4: Memory Agent (search & RAG)
- Git commit with all Week 3 changes
- Start implementing vector search

---

## 📞 Key Files to Reference

**Intake Agent:**
- [backend/app/agents/intake.py](backend/app/agents/intake.py)

**API Endpoints:**
- [backend/app/routers/entries.py](backend/app/routers/entries.py)

**Frontend Integration:**
- [frontend/src/components/JournalInput.tsx](frontend/src/components/JournalInput.tsx)

**Test Script:**
- [backend/test_intake_agent.py](backend/test_intake_agent.py)

**Prompts:**
- [backend/app/agents/prompts.py](backend/app/agents/prompts.py)

---

## 🚀 Ready?

Start with **Step 1: Start Backend** above!

The system is ready. Everything is working. Go test it! 🎉

---

**Happy Testing!**
