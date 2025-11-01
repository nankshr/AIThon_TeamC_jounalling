# Week 2 Testing Guide - Voice & Transcription

## Quick Start

### 1. Start Backend
```powershell
cd backend
poetry run uvicorn app.main:app --reload
```
Should output: `Uvicorn running on http://127.0.0.1:8000`

### 2. Start Frontend (new terminal)
```powershell
cd frontend
npm run dev
```
Should output: `http://localhost:3000`

### 3. Test in Browser
1. Open `http://localhost:3000`
2. Look for microphone icon in "New Journal Entry" section
3. Click microphone to start recording
4. Speak clearly (any language)
5. Click stop button (red square)
6. Select language if needed
7. Click upload button (blue arrow)
8. Wait 2-5 seconds for transcription
9. Transcribed text appears in textarea
10. Click "Save Entry"
11. Verify entry appears in list below

---

## Testing Scenarios

### Scenario 1: English Voice Entry
**Input:** Speak "We need to book a photographer for next month"
**Expected:**
- Text appears in textarea
- Language shows as "English"
- Can be saved to database

### Scenario 2: Tamil Voice Entry
**Input:** Speak in Tamil: "நான் பச்சை திருமண வேண்டுமென்று விரும்புகிறேன்"
**Expected:**
- Text appears in Tamil script
- Language auto-detected as Tamil
- Can be saved to database

### Scenario 3: Language Toggle
**Steps:**
1. Record English audio
2. Before uploading, select "Tamil" from language dropdown
3. Upload
**Expected:** Should attempt Tamil transcription (may fail since input is English)

### Scenario 4: Long Entry
**Input:** Record 30+ second entry
**Expected:**
- Timer shows MM:SS format
- Full text transcribed without truncation
- API handles >10KB text properly

---

## API Testing (curl/Postman)

### Test 1: Transcribe Audio File

**Get an audio file first:**
```bash
# Using ffmpeg to create a 5-second audio file
ffmpeg -f lavfi -i sine=f=1000:d=5 -q:a 9 -acodec libmp3lame output.mp3
```

**Upload and transcribe:**
```bash
curl -X POST http://localhost:8000/api/transcription/transcribe \
  -F "file=@output.mp3" \
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

### Test 2: Detect Language
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

### Test 3: API Documentation
Visit `http://localhost:8000/docs` to see:
- All endpoints with descriptions
- Try-it-out functionality
- Request/response schemas

---

## Error Testing

### Error 1: No Microphone Permission
**Steps:**
1. Deny microphone access when prompted
2. Click microphone button

**Expected:** Alert message "Unable to access microphone..."

### Error 2: No Audio Recorded
**Steps:**
1. Start recording
2. Immediately click stop
3. Click upload

**Expected:** Alert "No audio recorded"

### Error 3: Invalid API Key
**Steps:**
1. Change `OPENAI_API_KEY` in `.env` to invalid value
2. Try to upload audio

**Expected:** Error message "Transcription failed: API error"

### Error 4: File Too Large
**Steps:**
1. Try uploading a 30+ MB audio file

**Expected:** Error "Audio file too large (max 25MB)"

---

## Debugging

### Check API Connection
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

### Check Transcription Service
```bash
curl -X POST http://localhost:8000/api/transcription/detect-language \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}'
# Should return language detection
```

### Check Frontend Build
```bash
cd frontend
npm run build
# Should complete without errors
```

### Check Backend Logs
Look for:
- ✓ `Uvicorn running on http://127.0.0.1:8000`
- ✓ `Database initialized`
- ✓ No Python import errors
- ✓ CORS middleware configured

---

## Browser DevTools Checklist

### Console Tab
- No red errors
- No yellow warnings about CORS
- No API 404/500 errors

### Network Tab
1. Start recording
2. Stop and upload
3. Watch for request to `/api/transcription/transcribe`
4. Check response status = 200
5. Response body contains transcribed text

### Application Tab (Storage)
- Check local storage for any frontend state
- Verify no sensitive data exposed

---

## Performance Metrics

### Expected Timings
- **Recording Start:** <200ms
- **Microphone Permission:** <500ms (first time)
- **Audio Upload:** <2s (for 30-second audio)
- **Transcription:** 2-5 seconds (depending on audio length and API load)
- **Total Flow:** <10 seconds end-to-end

### Acceptable Ranges
- Recording buffer: Can record up to browser limit (typically 1+ hour)
- API timeout: 60 seconds (should complete in <5s)
- File size: Capped at 25MB by Whisper API

---

## Testing Checklist

- [ ] Microphone icon appears in UI
- [ ] Recording starts when icon clicked
- [ ] Timer counts up during recording
- [ ] Stop button works (turns red)
- [ ] Upload button appears after recording stops
- [ ] Language dropdown shows (EN/TA/HI)
- [ ] Submit triggers transcription
- [ ] Text appears in textarea
- [ ] Text can be edited
- [ ] Entry can be saved from textarea
- [ ] Multiple entries can be created
- [ ] Entries appear in history
- [ ] API documentation loads at /docs
- [ ] Transcription endpoint responds
- [ ] Language detection endpoint responds

---

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| "Microphone not found" | Permission denied | Check OS microphone settings |
| Empty transcription | Audio quality too low | Speak clearly, try again |
| API 401 error | Invalid API key | Check `OPENAI_API_KEY` in `.env` |
| API 500 error | Backend issue | Check backend logs, restart server |
| Text not appearing | Frontend bug | Check browser console, refresh page |
| Slow transcription | API overloaded | Normal during peak times, retry |

---

## Next Steps

Once Week 2 testing is complete:
1. Proceed to Week 3: Intake Agent
2. Agent will process transcribed text
3. Extract entities, tasks, sentiment
4. Store structured data

**Estimated Week 3 time:** 3-4 days for full implementation
