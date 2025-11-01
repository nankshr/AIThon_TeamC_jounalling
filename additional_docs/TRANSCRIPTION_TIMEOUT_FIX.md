# Transcription Timeout - Debugging & Solutions

**Date:** November 1, 2025
**Issue:** "Transcribing audio... This may take 5-10 seconds" shows for too long
**Status:** Investigating & enhancing logging

---

## ✅ Good News

OpenAI API connection is **working perfectly**:
- ✅ API key is valid
- ✅ Connection successful
- ✅ Whisper-1 model available
- ✅ 99 models accessible

---

## 📋 What Changed

Added detailed logging to track the transcription flow:

### 1. **Backend Logging** (app/routers/transcription.py)
Now logs:
- `[INFO] Received transcription request`
- `[INFO] Audio file size: XXX bytes`
- `[INFO] Calling TranscriptionService.transcribe_audio...`
- `[INFO] Transcription successful: {text: "..."}`
- `[ERROR] Transcription endpoint error: ...` (if fails)

### 2. **Service Logging** (app/services/transcription.py)
Now logs:
- `[INFO] Starting Whisper API call with language: en`
- `[INFO] Whisper API response: {text: "..."}`
- `[ERROR] Whisper API error: ...` (if fails)

---

## 🔍 How to Debug

### Step 1: Check Backend Logs
When you upload audio, look at the backend terminal for:

**Good flow:**
```
INFO: Received transcription request - file: audio.webm, language: en
INFO: Audio file size: 152924 bytes
INFO: Calling TranscriptionService.transcribe_audio...
INFO: Starting Whisper API call with language: en
INFO: Whisper API response: {text: "...", language: "en"}
INFO: Transcription successful: {text: "...", ...}
INFO: POST /api/transcription/transcribe HTTP/1.1" 200
```

**If stuck:**
```
INFO: Received transcription request...
INFO: Audio file size: XXX bytes
INFO: Calling TranscriptionService.transcribe_audio...
[NOTHING AFTER THIS FOR LONG TIME]
```

### Step 2: Check Browser Console (F12)
You should see:
```javascript
Sending audio to API: {size: 152924, type: 'audio/webm', language: 'en'}
[Wait 5-10 seconds]
API response status: 200
Transcription result: {text: "...", language: "en", confidence: 0.95}
```

### Step 3: Identify the Issue

**If backend logs stop at "Calling TranscriptionService...":**
- Whisper API is hanging
- Possible causes:
  - Network timeout
  - API overloaded
  - Audio file corrupted
  - Language parameter issue

**If you see error in logs:**
```
ERROR: Whisper API error: ...
```
- Check the full error message
- Note the specific error type

---

## 🚀 Restart with Enhanced Logging

### 1. Kill Current Backend
```bash
Ctrl+C in backend terminal
```

### 2. Restart Backend
```bash
cd backend
poetry run uvicorn app.main:app --reload
```

Should show:
```
INFO:     Application startup complete
```

### 3. Test Again
1. Record voice
2. Click upload
3. **Watch backend logs** - you'll see each step
4. Check browser console too

---

## 📊 Expected Timeline

### Successful flow:
```
Upload clicked (t=0s)
  ↓
Backend receives (t=0.5s) - "Received transcription request"
  ↓
File read (t=0.7s) - "Audio file size: XXX"
  ↓
Whisper API call (t=1s) - "Starting Whisper API call"
  ↓
Whisper processing (t=1-8s) - No log output (waiting for API)
  ↓
Result received (t=8s) - "Whisper API response:"
  ↓
Response sent (t=8.2s) - HTTP 200
  ↓
Text appears (t=8.5s) - Shows in textarea
```

**Total: ~8-10 seconds** (normal for Whisper API)

---

## 🐛 Possible Issues & Solutions

### Issue 1: Browser shows "Transcribing..." but nothing happens for >30s

**Possible cause:** Whisper API is slow or hanging

**Solution:**
1. Check backend logs (see if "Starting Whisper API call" appears)
2. Wait up to 2 minutes (Whisper can be slow sometimes)
3. If >2 minutes, kill request and try again

### Issue 2: Backend logs show error

**Example error:**
```
ERROR: Whisper API error: Invalid API key
```

**Solution:**
1. Check OPENAI_API_KEY in .env
2. Run: `poetry run python test_openai_connection.py`
3. If test fails, update API key
4. Restart backend

### Issue 3: Audio file appears empty

**Backend log:**
```
INFO: Audio file size: 0 bytes
ERROR: Empty audio file
```

**Solution:**
1. Check microphone is working
2. Make sure you actually spoke
3. Try recording longer (5+ seconds)
4. Try different browser

### Issue 4: Network timeout error

**Backend log:**
```
ERROR: Whisper API error: Connection timeout
```

**Solution:**
1. Check internet connection
2. Try again (API might be temporarily slow)
3. Use shorter audio (under 30 seconds)
4. Check OpenAI API status: https://status.openai.com/

---

## 🧪 Test the Transcription Directly

Create a test with ffmpeg (if you have it):

```bash
# Generate test audio (requires ffmpeg installed)
ffmpeg -f lavfi -i sine=f=1000:d=5 test_audio.webm

# Then test the API directly:
curl -X POST http://localhost:8000/api/transcription/transcribe \
  -F "file=@test_audio.webm" \
  -F "language=en" \
  -v
```

---

## 📝 What to Check

Before saying "it's slow", verify:

1. **Backend is running?**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status": "healthy"}
   ```

2. **OpenAI API working?**
   ```bash
   cd backend
   poetry run python test_openai_connection.py
   # Should show: [OK] All tests passed
   ```

3. **Network is working?**
   ```bash
   ping 8.8.8.8
   # Should show responses
   ```

4. **Audio is being captured?**
   - Record 5+ seconds
   - Click play
   - Hear yourself
   - If no sound, microphone issue (not API)

---

## 📋 Logging Locations

### Backend Logs
```
Terminal running: poetry run uvicorn app.main:app --reload
Look for INFO/ERROR messages
```

### Browser Console Logs
```
Press F12
Click "Console" tab
Look for messages starting with: Sending audio..., API response...
```

### Application Logs (advanced)
```
Check: backend/logs/ (if configured)
Or: tail -f backend/logs/app.log
```

---

## ⏱️ Timing Expectations

| Operation | Time | Notes |
|-----------|------|-------|
| File upload | <1s | Frontend → Backend |
| File read | <1s | Backend reads file |
| API request | <1s | Backend → OpenAI |
| Whisper processing | 3-8s | Depends on audio length |
| Response | <1s | OpenAI → Backend → Frontend |
| **Total** | **5-10s** | Normal timing |

If taking >20s, something is slow or stuck.

---

## 🎯 Next Steps

### Immediate:
1. Note current behavior (does it hang or complete slowly?)
2. Check backend logs when you test
3. Share any error messages

### After restart:
1. Hard refresh browser (Ctrl+Shift+R)
2. Record 5-second test audio
3. Check both backend logs and browser console
4. Note timing at each step

### If still slow:
1. Run `test_openai_connection.py` to verify API
2. Try smaller audio (3 seconds)
3. Try different browser
4. Check your internet speed

---

## 📞 Quick Reference

**Test OpenAI connection:**
```bash
cd backend && poetry run python test_openai_connection.py
```

**Check backend logs:**
```
Look at terminal running uvicorn
Filter for: INFO, ERROR, WARNING
```

**Check browser logs:**
```
Press F12 → Console tab
Look for: "Sending audio", "API response", "Transcription error"
```

**Restart everything:**
```bash
Ctrl+C (stop backend)
Ctrl+C (stop frontend)
cd backend && poetry run uvicorn app.main:app --reload
cd frontend && npm run dev
Browser: Ctrl+Shift+R (hard refresh)
```

---

## Summary

**What was added:**
- ✅ Detailed logging at every step
- ✅ Better error messages
- ✅ Test script to verify OpenAI connection
- ✅ Timing information

**What you do:**
1. Restart backend (gets new logging)
2. Record and upload audio
3. Check backend logs for each step
4. See where it's slow or stuck
5. Use this guide to diagnose

**Expected result:**
You'll see exactly where the time is being spent, making it easy to fix!

---

**Ready to test?** Restart backend with enhanced logging and try again! 🚀
