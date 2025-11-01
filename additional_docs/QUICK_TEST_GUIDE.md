# Quick Test Guide - Week 2 Voice Transcription

**Last Updated:** November 1, 2025
**Status:** Ready to Test

---

## ⚡ 5-Minute Quick Start

### Terminal 1: Start Backend
```bash
cd backend
poetry run uvicorn app.main:app --reload
```

Wait for:
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2: Start Frontend
```bash
cd frontend
npm run dev
```

Wait for:
```
▲ Next.js 14.1.0
Local:        http://localhost:3000
```

### Browser: Test Voice Transcription
1. Go to `http://localhost:3000`
2. See journal entry form with voice recorder
3. Click **🎤** microphone button
4. Speak clearly for 5+ seconds:
   - *"Hello, this is a test of the transcription system"*
5. Click **⏹️** stop button
6. See playback controls appear
7. Click **▶️** play to hear your voice
8. Click **📤** upload button
9. Wait 5-10 seconds (see "Transcribing audio..." message)
10. ✅ Text appears in textarea below

---

## 🔍 What to Check

### ✅ Frontend (Browser)
- Voice recorder shows properly
- Recording timer increments
- Play/pause buttons work
- Playback time shows progress
- Text appears after upload

### ✅ Backend (Terminal)
Watch for these logs (in order):
```
INFO: Received transcription request - file: audio.webm, language: en
INFO: Audio file size: XXXXX bytes
INFO: Calling TranscriptionService.transcribe_audio...
INFO: Starting Whisper API call with language: en
INFO: Whisper API response: {...}
INFO: Transcription successful: XX characters
```

### ✅ Browser Console (F12)
Should see:
```javascript
Sending audio to API: {size: ..., type: 'audio/webm', language: 'en'}
API response status: 200
Transcription result: {text: "...", language: "en", confidence: 0.95}
```

---

## ⚠️ If Something Goes Wrong

### Problem: No microphone permission
- **Fix:** Allow microphone access in browser, reload page

### Problem: Recording but no text appears
- **Check:** Backend logs for error messages
- **Try:** Record longer (5+ seconds), speak louder

### Problem: "Unexpected token '<'" error
- **Cause:** Frontend calling wrong backend port
- **Fix:** Verify `NEXT_PUBLIC_API_URL=http://localhost:8000` in [frontend/.env.local](frontend/.env.local)

### Problem: API connection error
- **Test:** `cd backend && poetry run python test_openai_connection.py`
- **Check:** OPENAI_API_KEY in [backend/.env](backend/.env)

### Problem: "'Transcription' object is not subscriptable"
- **Status:** Already fixed in code
- **Check:** [backend/app/services/transcription.py:52-62](backend/app/services/transcription.py#L52-L62)

---

## 📋 Test Scenarios

### Test 1: English Transcription (5 min)
- Record: "Testing the wedding journal application with voice transcription"
- Expected: Text appears with English detected
- Check: Backend logs show successful transcription

### Test 2: Language Selection (5 min)
- Record in Tamil or Hindi
- Select language from dropdown before upload
- Expected: Text appears in correct language

### Test 3: Playback Before Upload (3 min)
- Record audio
- Click play to hear recording
- Click pause
- Verify playback progress shows
- Click reset and record again

### Test 4: Error Handling (3 min)
- Start recording but don't speak
- Click stop and upload
- Expected: Error message "No text was transcribed"

### Test 5: Long Audio (10 min)
- Record 60+ seconds of continuous speech
- Upload
- Expected: Transcription still works (may take 15-20 seconds)

---

## 🎯 Success Criteria

✅ Test passes if:
1. Recording works (can start/stop)
2. Playback works (can hear recording)
3. Upload completes without error
4. Text appears in textarea
5. Backend logs show all steps completed
6. No 500 errors in browser console

---

## 📊 Expected Timing

| Step | Duration |
|------|----------|
| Start recording | <1s |
| Stop recording | <1s |
| Create audio blob | <1s |
| Upload to backend | 1-2s |
| Whisper API processes | 3-8s |
| Text displays | <1s |
| **Total** | **5-10s** |

If taking >30 seconds, something may be slow or stuck.

---

## 🚀 Next Steps After Testing

If voice transcription works:

### ✅ All systems go!
1. Create git commit
2. Start Week 3: Intake Agent (entity extraction)

### ⚠️ If having issues
1. Check QUICK_TEST_GUIDE.md troubleshooting section
2. Review logs in TRANSCRIPTION_TIMEOUT_FIX.md
3. Run OpenAI connection test: `poetry run python test_openai_connection.py`

---

## 📞 Quick Reference

**Check if backend is running:**
```bash
curl http://localhost:8000/health
# Should return 404 (no health endpoint yet) or app starts
```

**Check if frontend is running:**
```bash
curl http://localhost:3000
# Should return HTML
```

**Verify OpenAI API:**
```bash
cd backend && poetry run python test_openai_connection.py
# Should show: [OK] All tests passed!
```

**View backend logs:**
- Scroll up in Terminal 1 running uvicorn
- Look for INFO/ERROR messages

**View frontend logs:**
- Press F12 in browser
- Click "Console" tab
- Look for "Sending audio...", "API response", "Transcription result"

---

**Ready to test? Start with Terminal 1 above! 🎤**
