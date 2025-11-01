# Week 2: Voice & Transcription Implementation ✅

**Status:** COMPLETE
**Date:** November 1, 2025

---

## Overview

Week 2 of the AI-powered wedding journal project implements real-time voice transcription using OpenAI Whisper API and a browser-based voice recorder component.

**New Features:**
- ✅ Audio file transcription using Whisper API
- ✅ Voice recorder component with Web Audio API
- ✅ Language detection (English, Tamil, Hindi)
- ✅ Language toggle UI
- ✅ Real-time transcription pipeline
- ✅ Integrated with existing journal entry flow

---

## Backend Changes

### 1. **Updated Dependencies** (`backend/pyproject.toml`)

Added AI/ML packages needed for Weeks 2-7:
```toml
anthropic = "^0.28.0"          # Claude API
openai = "^1.40.0"             # Whisper + Embeddings
langgraph = "^0.2.0"           # Agent orchestration
langchain = "^0.2.0"           # LLM utilities
langchain-core = "^0.2.0"      # Core utilities
langchain-anthropic = "^0.1.0" # Anthropic integration
langchain-openai = "^0.1.0"    # OpenAI integration
```

**Installation:**
```bash
cd backend
poetry lock
poetry install
```

### 2. **New Transcription Service** (`backend/app/services/transcription.py`)

Service for handling Whisper API transcription:

**Classes:**

#### `TranscriptionService`
- `transcribe_audio(audio_file, language, file_name)` - Transcribe audio bytes
  - **Inputs:**
    - `audio_file`: Raw audio bytes (webm, mp3, m4a, wav, etc.)
    - `language`: Optional language code ('en', 'ta', etc.). Auto-detect if None.
    - `file_name`: Original filename with extension
  - **Returns:** Dict with `text`, `language`, `confidence`
  - **Note:** Uses sync client in async executor (Whisper API doesn't support async)

#### `LanguageDetector`
- `detect_language(audio_file, text)` - Detect language from audio or text
  - From **audio**: Uses Whisper to detect language
  - From **text**: Uses script detection (Tamil script recognition)
  - **Returns:** Language code ('en', 'ta', etc.)

**Key Design Decisions:**
1. **Sync/Async Wrapper:** Whisper API is synchronous, so we use `asyncio.run_in_executor()` to run it in thread pool without blocking
2. **Confidence Score:** Whisper doesn't expose confidence, so we default to 0.95
3. **Language Detection:** Hybrid approach - Whisper for audio, script detection for text

### 3. **New Transcription Router** (`backend/app/routers/transcription.py`)

Handles transcription API endpoints:

#### `POST /api/transcription/transcribe`
```python
# Request
{
  "file": <audio file (multipart/form-data)>,
  "language": "en" # Optional
}

# Response
{
  "text": "Transcribed text here",
  "language": "en",
  "confidence": 0.95
}
```

**Features:**
- File validation (25MB limit from Whisper)
- Language auto-detection
- Error handling with detailed messages
- Async-safe execution

#### `POST /api/transcription/detect-language`
```python
# Request
{
  "text": "Sample text to detect language"
}

# Response
{
  "language": "en",
  "language_name": "English"
}
```

**Supported Languages:**
- `en` - English
- `ta` - Tamil
- `hi` - Hindi
- `kn` - Kannada
- `te` - Telugu
- `ml` - Malayalam

### 4. **Updated Main App** (`backend/app/main.py`)

Added transcription router:
```python
from app.routers import journal, tasks, user, transcription

app.include_router(transcription.router)
```

**New Endpoints:**
- `POST /api/transcription/transcribe` - Transcribe audio
- `POST /api/transcription/detect-language` - Detect text language

---

## Frontend Changes

### 1. **New Voice Recorder Component** (`frontend/src/components/VoiceRecorder.tsx`)

Complete voice recording UI with browser's Web Audio API:

**Features:**
- **Record Button:** Start/stop recording
- **Live Timer:** Shows recording duration (MM:SS format)
- **Visual Feedback:** Animated pulse indicator while recording
- **Language Selector:** Choose language before transcription
- **Submit Button:** Send audio to API after recording
- **Loading State:** Shows "Transcribing audio..." while processing
- **Error Handling:** User-friendly error messages

**Props:**
```typescript
interface VoiceRecorderProps {
  onTranscriptionComplete: (text: string, language: string) => void;
  isLoading?: boolean;
}
```

**Workflow:**
1. User clicks microphone icon to start recording
2. Browser requests microphone permission (first time only)
3. Audio chunks are collected while recording
4. User stops recording by clicking stop button
5. User selects language (optional, defaults to English)
6. User clicks upload button to submit
7. Component calls Whisper API via `/api/transcription/transcribe`
8. Calls `onTranscriptionComplete` callback with transcribed text
9. Recording state resets for next entry

**Technical Details:**
- Uses `MediaRecorder` API for audio capture
- Collects audio chunks in `Blob[]`
- Creates WebM format audio file
- Handles microphone permission errors gracefully
- Cleans up event listeners and intervals on unmount

### 2. **Updated Journal Input Component** (`frontend/src/components/JournalInput.tsx`)

Integrated voice recorder into main entry form:

**Changes:**
1. Import `VoiceRecorder` component
2. Add voice recorder above text area
3. Add `handleTranscriptionComplete` handler
   - Sets transcribed text in textarea
   - Clears error state
   - User can edit before submitting

**User Flow:**
```
Voice Recorder
     ↓
User speaks (or types text)
     ↓
Whisper transcription
     ↓
Text appears in textarea
     ↓
User edits if needed
     ↓
Click "Save Entry"
```

---

## API Testing

### Test Voice Transcription

**Using curl:**
```bash
# Record audio with ffmpeg or similar, then:
curl -X POST http://localhost:8000/api/transcription/transcribe \
  -F "file=@audio.webm" \
  -F "language=en"
```

**Response:**
```json
{
  "text": "We need to book the caterer soon",
  "language": "en",
  "confidence": 0.95
}
```

### Test Language Detection

**Using curl:**
```bash
curl -X POST http://localhost:8000/api/transcription/detect-language \
  -H "Content-Type: application/json" \
  -d '{"text": "நான் கல்யாணம் பற்றி சிந்திக்கிறேன்"}'
```

**Response:**
```json
{
  "language": "ta",
  "language_name": "Tamil"
}
```

### Full Journal Entry with Voice

**In browser:**
1. Open `http://localhost:3000`
2. Click microphone icon
3. Say: "We need to find a beach venue that's eco-friendly"
4. Click stop (red square)
5. Select language (English)
6. Click upload (blue arrow)
7. Wait for transcription
8. Text appears in textarea
9. Edit if needed
10. Click "Save Entry"
11. Entry saved to database with transcribed text

---

## Key Implementation Notes

### 1. **Async/Sync Bridge**
The Whisper API is synchronous, but our backend is async. Solution:
```python
import asyncio
loop = asyncio.get_event_loop()
transcript = await loop.run_in_executor(
    None,
    lambda: sync_client.audio.transcriptions.create(...)
)
```

### 2. **File Upload Handling**
Using FastAPI's `UploadFile` for streaming file uploads:
- No need to load entire file into memory first
- Automatic content-type detection
- Built-in validation support

### 3. **Language Detection Strategy**
- **For Audio:** Whisper's language detection is highly accurate
- **For Text:** Use script-based heuristic (Tamil Unicode range detection)
- **Fallback:** Default to English if detection fails

### 4. **Browser Audio API**
Modern Web Audio API used (no plugin required):
- `navigator.mediaDevices.getUserMedia()` - Request microphone
- `MediaRecorder` - Record audio stream
- `Blob` - Convert to file format
- Works on Chrome, Firefox, Safari, Edge

---

## Next Steps (Week 3)

The voice transcription pipeline is now complete. Next week:

1. **Intake Agent** - Extract entities from entries
   - Vendors, venues, costs, dates, people
   - Themes: budget, eco-friendly, stress
   - Auto-detect tasks
   - Sentiment analysis

2. **Integration** - Connect to journal entry creation
   - Process transcribed text through agent
   - Extract and store entities
   - Auto-log tasks

3. **Testing** - Validate extraction accuracy
   - Test with 20+ sample entries
   - Achieve >80% accuracy target

---

## Deployment

### Backend
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
# Server runs on http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive Swagger UI showing all endpoints including:
- `/api/transcription/transcribe`
- `/api/transcription/detect-language`

---

## File Structure

```
backend/
├── app/
│   ├── routers/
│   │   ├── transcription.py          [NEW] Transcription endpoints
│   │   ├── journal.py                [unchanged]
│   │   ├── tasks.py                  [unchanged]
│   │   └── user.py                   [unchanged]
│   ├── services/
│   │   ├── transcription.py          [NEW] Whisper API service
│   │   └── ...
│   └── main.py                       [UPDATED] Added transcription router
└── pyproject.toml                    [UPDATED] Added AI packages

frontend/
├── src/
│   └── components/
│       ├── VoiceRecorder.tsx         [NEW] Voice recorder component
│       └── JournalInput.tsx          [UPDATED] Integrated voice recorder
```

---

## Summary

**Week 2 Complete!** The wedding journal now supports:
- ✅ Voice recording (Web Audio API)
- ✅ Real-time transcription (Whisper API)
- ✅ Multi-language support (EN/TA/HI)
- ✅ Language detection (auto-detect or select)
- ✅ Seamless UI integration
- ✅ Error handling & validation

Users can now:
1. Speak journal entries instead of typing
2. Auto-transcription to text
3. Edit before saving
4. Switch between voice and text input

**Ready for Week 3:** Intake Agent implementation will add intelligence to extract meaning from transcribed entries!

---

## Quick Debugging

### Microphone Permission Denied
- Chrome/Firefox: Check browser permissions
- HTTPS required: May fail on `localhost` in some cases (use `localhost:3000` not `127.0.0.1:3000`)

### Transcription API Error
- Check `OPENAI_API_KEY` is set in `.env`
- Verify API key has transcription permissions
- Check file size < 25MB

### Language Not Detected
- Whisper defaults to English if unclear
- Manual selection fallback available
- Works best with 10+ seconds of audio

---

**Status:** Week 2 Implementation Complete ✅
**Ready to Proceed:** Week 3 - Intake Agent + Entity Extraction
