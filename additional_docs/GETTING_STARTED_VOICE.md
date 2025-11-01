# Getting Started with Voice & Transcription

**Quick start guide for testing Week 2 implementation**

---

## Prerequisites ✅

- [x] Backend dependencies installed (`poetry install`)
- [x] Frontend dependencies installed (`npm install`)
- [x] .env files configured with API keys
- [x] PostgreSQL database connection working
- [x] Database tables created

---

## Step 1: Start Backend Server

```powershell
cd backend
poetry run uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [XXXX]
Starting up application...
Database initialized
INFO:     Application startup complete
```

✅ Backend is ready when you see "Application startup complete"

---

## Step 2: Start Frontend Server (New Terminal)

```powershell
cd frontend
npm run dev
```

**Expected Output:**
```
- Local:        http://localhost:3000
- Environments: .env
```

✅ Frontend is ready when you see the local URL

---

## Step 3: Open Browser

Navigate to: **http://localhost:3000**

You should see:
- Wedding Journal header
- "New Journal Entry" form
- 🎤 Microphone icon (NEW - Week 2!)
- Text area for journal entry
- Save Entry button

---

## Step 4: Test Voice Recording

### Option A: Simple Test

1. **Click the microphone icon** 🎤
   - Wait for microphone permission prompt
   - Click "Allow" to grant permission

2. **Speak clearly**
   - Say something like: "We need to find a photographer"
   - Recording timer shows MM:SS format
   - You'll see animated dots while recording

3. **Click the stop button** ⏹️ (red square)
   - Recording stops
   - Upload button appears

4. **Select language** (optional)
   - Defaults to English
   - Can select Tamil, Hindi, etc.

5. **Click upload button** 📤 (blue arrow)
   - Loading indicator appears
   - "Transcribing audio..." message shows
   - Wait 2-5 seconds for API response

6. **Text appears in textarea**
   - Transcribed text is now in the form
   - Edit if needed
   - Click "Save Entry" to save

### Option B: Full Workflow Test

1. Record: "We need to find an eco-friendly caterer for the reception"
2. Stop recording
3. Select language: English
4. Upload
5. Verify transcription is accurate
6. Edit text if needed
7. Click "Save Entry"
8. Verify entry appears in the list below
9. Entry should have transcribed text in database

---

## Step 5: Verify API Endpoints

Open another terminal and test endpoints directly:

### Test Transcription Endpoint

```bash
# Create a test audio file (requires ffmpeg)
ffmpeg -f lavfi -i sine=f=1000:d=5 -q:a 9 -acodec libmp3lame test_audio.mp3

# Upload and transcribe
curl -X POST http://localhost:8000/api/transcription/transcribe \
  -F "file=@test_audio.mp3" \
  -F "language=en"
```

**Expected Response:**
```json
{
  "text": "...",
  "language": "en",
  "confidence": 0.95
}
```

### Test Language Detection

```bash
curl -X POST http://localhost:8000/api/transcription/detect-language \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you today?"}'
```

**Expected Response:**
```json
{
  "language": "en",
  "language_name": "English"
}
```

---

## Step 6: View API Documentation

Open: **http://localhost:8000/docs**

You should see:
- All API endpoints listed
- 2 new transcription endpoints:
  - POST /api/transcription/transcribe
  - POST /api/transcription/detect-language
- Try-it-out functionality
- Request/response schemas

---

## Troubleshooting

### Issue: "Microphone not found" Error

**Solution:**
1. Check OS microphone settings
2. Ensure browser has microphone permission
3. Try a different browser (Chrome, Firefox, Edge, Safari)
4. Restart browser and try again

### Issue: Empty Transcription

**Possible Causes:**
- Audio quality too low (speak clearly)
- Whisper couldn't understand (try again)
- API error (check backend logs)

**Solution:**
1. Verify OPENAI_API_KEY is set in .env
2. Check backend logs for errors
3. Try with clearer audio
4. Check OpenAI account has API credits

### Issue: API Connection Failed

**Solution:**
1. Verify backend is running: `http://localhost:8000/health`
2. Check CORS is enabled (it is by default)
3. Verify OPENAI_API_KEY in .env
4. Restart backend server

### Issue: Frontend Won't Start

**Solution:**
```bash
cd frontend
rm -r node_modules .next
npm install
npm run dev
```

### Issue: Backend Import Error

**Solution:**
```bash
cd backend
poetry install
# Or if that fails:
poetry lock
poetry install --no-root
```

---

## Testing Checklist

- [ ] Backend server starts without errors
- [ ] Frontend loads at localhost:3000
- [ ] Microphone icon visible in UI
- [ ] Can click microphone to start recording
- [ ] Timer counts up while recording
- [ ] Can click stop button
- [ ] Language selector appears
- [ ] Can click upload button
- [ ] Transcription starts
- [ ] Text appears in textarea within 5 seconds
- [ ] Can edit transcribed text
- [ ] Can click "Save Entry"
- [ ] Entry appears in list below
- [ ] Can test second entry
- [ ] API documentation loads at /docs
- [ ] Endpoints accessible (curl tests work)

---

## Multi-Language Testing

### English Test
**Speak:** "We're having the wedding on June 15th at the beach"
**Expected:** Text in English

### Tamil Test
**Speak:** "நான் ஒரு பச்சை திருமணம் விரும்புகிறேன்" (or English with "ta" selected)
**Expected:** Tamil text or auto-detected as Tamil

### Language Toggle Test
1. Record English audio
2. Select "Tamil" language
3. Upload
4. Observe behavior (might fail or produce unexpected result)
5. Reset and try with proper language

---

## Performance Notes

### Expected Timings
- Recording start: <200ms
- Upload: 1-3 seconds (depending on audio length)
- Transcription: 2-5 seconds
- Total: <10 seconds end-to-end

### Normal Variations
- First API call might be slightly slower
- Longer audio takes longer to transcribe
- API response time varies (depends on OpenAI load)

---

## Database Verification

### Check Entries in Database

```bash
# Connect to PostgreSQL
psql -h 69.62.84.73 -U postgres -d wedding_journal

# Query entries
SELECT id, raw_text, language, created_at FROM journal_entries ORDER BY created_at DESC LIMIT 5;
```

You should see your transcribed entries with:
- UUID id
- raw_text (transcribed content)
- language (detected or selected)
- created_at timestamp

---

## Next Steps

### When Ready for Week 3 (Intake Agent)
1. Verify voice input is working consistently
2. Test with 5-10 different entries
3. Confirm entries are saved to database
4. Proceed to Week 3 intake agent implementation

### What Week 3 Will Do
- Process transcribed text with Claude
- Extract entities (vendors, venues, costs, dates)
- Auto-detect themes and tasks
- Analyze sentiment
- Store structured data in database

---

## Quick Reference Commands

**Start Everything:**
```bash
# Terminal 1: Backend
cd backend && poetry run uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Tests (optional)
curl http://localhost:8000/health
```

**View Logs:**
```bash
# Backend logs appear in Terminal 1
# Check for: "Application startup complete"

# Frontend logs appear in Terminal 2
# Check for: "http://localhost:3000"
```

**API Documentation:**
```
http://localhost:8000/docs
```

**Database Connection:**
```bash
psql -h 69.62.84.73 -U postgres -d wedding_journal
```

---

## Need Help?

Check these files:
- `WEEK2_IMPLEMENTATION.md` - Technical details
- `TESTING_WEEK2.md` - Detailed test cases
- `IMPLEMENTATION_STATUS.md` - Project status
- `WEEK2_SUMMARY.md` - Complete summary

---

**You're all set!** Try recording a voice entry now. 🎤

When ready, proceed to Week 3: Intake Agent implementation.
