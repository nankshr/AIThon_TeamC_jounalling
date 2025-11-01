# Voice Transcription Troubleshooting Guide

**Updated:** November 1, 2025

If transcription is not showing up, follow these steps to diagnose the issue.

---

## 🔍 Step 1: Check Browser Console

**Press:** `F12` (or right-click → Inspect → Console tab)

Look for messages like:
```
Sending audio to API: {size: 12345, type: 'audio/webm', language: 'en'}
API response status: 200
Transcription result: {text: "...", language: "en", confidence: 0.95}
```

### If You See These:
✅ **Good** - Voice is working, text should appear
❌ **Not seeing** - Continue to Step 2

### Common Console Errors:

**Error 1: "Unable to access microphone"**
- Click "Allow" when browser asks for microphone permission
- Check OS microphone settings
- Try different browser (Chrome, Firefox, Safari)

**Error 2: "Transcription failed: API error"**
- Check backend is running: Open `http://localhost:8000/health`
- Backend logs show error? Continue to Step 3

**Error 3: "CORS error" or "Network error"**
- Backend not running
- Wrong backend URL
- See Step 3

---

## 🔍 Step 2: Check Voice Playback

After you stop recording:

1. **Do you see the blue playback panel?**
   - ✅ YES → Go to Step 4
   - ❌ NO → Recording failed
     - Speak louder
     - Check microphone in OS settings
     - Try different browser

2. **Click the play button (▶️)**
   - ✅ Can hear audio → Recording worked!
   - ❌ No audio → Microphone issue

3. **Check recording duration**
   - Should show: "0:XX seconds" where XX > 0
   - If 0:00 → Nothing was recorded

---

## 🔍 Step 3: Check Backend Connection

### Test 1: Health Check
Open in browser: **http://localhost:8000/health**

**Expected:**
```json
{"status": "healthy"}
```

**Not working?**
- Backend not running?
- Wrong port?
- See "Start Backend" below

### Test 2: API Docs
Open in browser: **http://localhost:8000/docs**

Look for:
- `POST /api/transcription/transcribe` ✅
- `POST /api/transcription/detect-language` ✅

**Not there?**
- Restart backend
- Check imports in main.py

### Test 3: Direct API Test
Open browser console and paste:
```javascript
fetch('/api/transcription/detect-language', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: 'Hello world'})
})
.then(r => r.json())
.then(d => console.log('API works:', d))
.catch(e => console.log('API failed:', e))
```

**Expected output:** `API works: {language: 'en', language_name: 'English'}`

**Getting error?** → Go to Step 4

---

## 🔍 Step 4: Check Backend Logs

Look at the terminal where backend is running:

### Good Signs ✅
```
INFO: Application startup complete
INFO: Started server process [XXXX]
```

### Bad Signs ❌
```
ERROR: ...
Exception: ...
ModuleNotFoundError: ...
```

### Check These Logs When You Upload Audio:

**Good:**
```
POST /api/transcription/transcribe HTTP/1.1" 200
```

**Bad:**
```
POST /api/transcription/transcribe HTTP/1.1" 500
POST /api/transcription/transcribe HTTP/1.1" 404
```

---

## 🔍 Step 5: Check OpenAI API Key

### Test in Backend Terminal:

```bash
cd backend

# Check .env file exists and has key
cat .env | grep OPENAI_API_KEY

# Should show: OPENAI_API_KEY=sk-proj-...
```

**Key missing?** → Add it to `.env` and restart backend

### Test API Key Works:

```bash
poetry run python -c "
from openai import OpenAI
client = OpenAI()
print('API key valid!' if client.api_key else 'No API key')
"
```

**Shows error?** → API key is invalid

---

## 🚀 Fix Common Issues

### Issue 1: "Transcription failed: API error"

**Most likely cause:** OPENAI_API_KEY is invalid

**Fix:**
1. Get new key from https://platform.openai.com/api-keys
2. Update `backend/.env`:
   ```
   OPENAI_API_KEY=sk-proj-YOUR_NEW_KEY_HERE
   ```
3. Restart backend:
   ```bash
   # Stop current: Ctrl+C
   # Then restart:
   poetry run uvicorn app.main:app --reload
   ```

### Issue 2: "CORS error" or "Failed to fetch"

**Most likely cause:** Backend not running or wrong URL

**Fix:**
1. Check backend running:
   ```bash
   # Open new terminal
   curl http://localhost:8000/health
   # Should return: {"status":"healthy"}
   ```

2. If not running:
   ```bash
   cd backend
   poetry run uvicorn app.main:app --reload
   ```

3. If still failing, check frontend URL:
   ```bash
   # In browser console, verify:
   fetch('/api/transcription/detect-language', ...)
   # Should NOT show CORS error
   ```

### Issue 3: No Playback or Empty Recording

**Most likely cause:** Microphone not working or audio not captured

**Fix:**
1. Check microphone works elsewhere:
   - Open Discord, Teams, or zoom
   - Try recording voice

2. Check microphone permissions:
   - Chrome: Settings → Privacy → Microphone → Allow localhost:3000
   - Firefox: Check allow/block list
   - System: Windows/Mac settings

3. Try different browser

### Issue 4: Transcription Takes Too Long (>30 seconds)

**Possible causes:**
- API overload
- Large audio file
- Slow internet

**Wait 30+ seconds** - Whisper API can take time

---

## 📋 Complete Debugging Checklist

- [ ] Browser console (F12) shows no red errors
- [ ] Can hear audio playback after recording
- [ ] Recording shows duration > 0 seconds
- [ ] Backend running (http://localhost:8000/health works)
- [ ] API endpoints exist (http://localhost:8000/docs)
- [ ] OPENAI_API_KEY set in .env
- [ ] API key is valid (not expired)
- [ ] Microphone permissions granted
- [ ] Correct browser (Chrome, Firefox, Safari, Edge)
- [ ] Frontend running on localhost:3000

If all checked, but still not working → See "Advanced Debugging" below

---

## 🔧 Advanced Debugging

### Enable Detailed Logging

**Frontend (add to console):**
```javascript
localStorage.debug = '*'
```

**Backend (add to main.py):**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Recording + Transcription Manually

```bash
# Terminal 1: Backend
cd backend
poetry run uvicorn app.main:app --reload --log-level debug

# Terminal 2: Create test audio
ffmpeg -f lavfi -i sine=f=1000:d=5 audio.webm

# Terminal 3: Upload to API
curl -X POST http://localhost:8000/api/transcription/transcribe \
  -F "file=@audio.webm" \
  -F "language=en" \
  -v
```

**Expected response:**
```json
{
  "text": "...",
  "language": "en",
  "confidence": 0.95
}
```

### Check Backend Dependency Issues

```bash
cd backend

# Verify imports work
poetry run python -c "from app.services.transcription import TranscriptionService; print('OK')"
poetry run python -c "from app.routers.transcription import router; print('OK')"

# Should print: OK (twice)
```

---

## 🆘 Still Not Working?

### Gather Debug Info:

1. **Browser console output** (Screenshot)
2. **Backend terminal logs** (Screenshot)
3. **Steps you followed**
4. **Error message** (exact text)
5. **Microphone test result** (works in other apps?)

### Restart Everything:

```bash
# Terminal 1: Kill backend (Ctrl+C)
# Then restart:
cd backend
poetry install  # Reinstall if needed
poetry run uvicorn app.main:app --reload

# Terminal 2: Kill frontend (Ctrl+C)
# Then restart:
cd frontend
npm install  # Reinstall if needed
npm run dev

# Browser: Hard refresh (Ctrl+Shift+R)
```

### Nuclear Option:

```bash
# Backend
cd backend
rm -rf .venv
poetry install
poetry run uvicorn app.main:app --reload

# Frontend
cd frontend
rm -rf node_modules .next
npm install
npm run dev
```

---

## 📱 Testing on Different Devices

### Desktop / Laptop
- ✅ Chrome / Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge

### Mobile
- ⚠️ May require HTTPS
- ⚠️ Different microphone permissions
- ⚠️ Can work but testing easier on desktop

---

## 📊 Expected Timings

| Step | Time | Status |
|------|------|--------|
| Recording | Variable | Ongoing |
| Stop & show playback | <100ms | Instant |
| Click upload | Immediate | Instant |
| Send to API | 1-2 seconds | Watch console |
| Whisper processing | 2-5 seconds | "Transcribing..." shown |
| Return text | Immediate | Text appears |
| **Total** | **<10 seconds** | Normal |

If taking >20 seconds → API slow or network issue

---

## 🎯 What Each UI Element Means

### During Recording:
```
🎤 (red) - Click to stop
"Recording... 0:15" - You're recording (15 seconds)
Three animated dots - Audio is being captured
```

### After Recording (Blue Panel):
```
▶️ - Click to play audio
⏮️ - Click to reset and re-record
💾 (green) - Click to upload and transcribe
"0:15 / 0:15" - Playback position / Total duration
```

### While Transcribing:
```
💾 (spinning) - Uploading and processing
"Transcribing audio... may take 5-10 seconds" - Waiting for API
```

### After Transcription:
```
Text appears in textarea below voice recorder
User can edit text
Click "Save Entry" to save to database
```

---

## 🔗 Resources

- **OpenAI API Status:** https://status.openai.com/
- **Browser Compatibility:** Check https://caniuse.com/mediarecorder
- **Whisper API Docs:** https://platform.openai.com/docs/api-reference/audio

---

## 💡 Quick Fixes Summary

| Problem | Solution |
|---------|----------|
| No sound playback | Microphone not working, check OS settings |
| "Transcription failed" | Invalid OPENAI_API_KEY, update .env |
| "CORS error" | Backend not running, start it |
| Recording shows 0:00 | Didn't speak loud enough or microphone disabled |
| Text doesn't appear | Check browser console (F12) for errors |
| API takes >30s | Normal, Whisper can be slow, wait it out |

---

**Still stuck?** Check the console logs and restart both backend and frontend. Most issues resolve with:

```bash
# Terminal 1
cd backend && poetry run uvicorn app.main:app --reload

# Terminal 2
cd frontend && npm run dev

# Browser: F12 to check console, hard refresh (Ctrl+Shift+R)
```

Good luck! 🎤
