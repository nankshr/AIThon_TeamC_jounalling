# AI Wedding Journal - Demo Script (3 Minutes)

---

## 🎯 THE PROBLEM (30 seconds)

Wedding planning is **overwhelming and chaotic**:
- Hundreds of vendor decisions to make
- Budget tracking scattered across notes
- Tasks get lost in emails and WhatsApp
- Timeline pressure with countless deadlines
- Need to remember vendor details, costs, dates

**Result:** Couples feel disorganized and stressed 😰

---

## ✅ THE SOLUTION (1 minute)

**AI-Powered Wedding Journal** - A smart journaling app that:

### 1️⃣ **Capture Your Thoughts**
- Record voice or type entries freely
- Upload audio files directly
- Works while thinking or discussing

### 2️⃣ **AI Extracts Insights Automatically**
- **Vendors** - Photographers, caterers, florists automatically detected
- **Costs** - Budget amounts extracted and calculated
- **Tasks** - Suggested action items created automatically
- **Timeline** - Important dates identified
- **Mood** - Sentiment analysis shows stress levels

### 3️⃣ **Intelligent Task Management**
- AI-generated tasks from journal entries
- Checkboxes to select which to create
- Automatic deadline tracking
- Priority levels (Low → Critical)
- Right-side panel shows all pending tasks

### 4️⃣ **Smart Search (RAG)**
- Find entries by meaning, not just keywords
- Search: "vendor expensive" → finds cost concerns
- Relevance scoring (0-100% match)
- See extracted data per entry

---

## 🏗️ HOW IT'S BUILT (1.5 minutes)

### **Architecture: 3-Tier Stack**

```
┌─────────────────────────────────────┐
│   FRONTEND (React/Next.js)          │
│  - Journal Input & Voice Recording  │
│  - Audio Upload (MP3, WAV, etc)    │
│  - AI Suggestions Display           │
│  - Task Panel & Search              │
└─────────────────────────────────────┘
             ↕ API Calls
┌─────────────────────────────────────┐
│   BACKEND (FastAPI/LangGraph)       │
│  - Intake Agent → Extract entities  │
│  - Memory Agent → Semantic search   │
│  - Task Manager → Auto-create tasks │
│  - Whisper API → Audio transcription│
└─────────────────────────────────────┘
             ↕ SQL Queries
┌─────────────────────────────────────┐
│   DATABASE (PostgreSQL + pgvector)  │
│  - Journal Entries (with embeddings)│
│  - Tasks with priorities/deadlines  │
│  - Extracted entities (vendors...)  │
│  - Vector storage for search        │
└─────────────────────────────────────┘
```

### **Tech Stack**

**Frontend:**
- React 18 + Next.js 14 (App Router)
- TypeScript for type safety
- Tailwind CSS for styling
- Zustand for state management

**Backend:**
- FastAPI (async Python)
- LangGraph for agent orchestration
- LangChain for LLM integration
- SQLAlchemy ORM (async)

**AI/ML:**
- OpenAI Claude (entity extraction)
- OpenAI Whisper (audio transcription)
- OpenAI Embeddings (semantic search)

**Database:**
- PostgreSQL 16
- pgvector extension (vector search)
- Async connections for performance

---

## 🎬 LIVE DEMO (1 minute)

### **Demo Flow:**

**Step 1: Create Entry with Suggestions** ✨
```
Type: "Photographer costs ₹50,000. Need florist and caterer."
↓
Click "✨ Get AI Suggestions"
↓
Green box shows:
  - Vendors Found: 1 (Photographer)
  - Tasks Identified: 2 (Book florist, Book caterer)
  - Total Budget: ₹50,000
  - Mood: Concerned
↓
Check tasks → Click "Save Entry"
↓
Tasks APPEAR on right side! ✅
```

**Step 2: Upload Audio** 🎙️
```
Click "📁 Upload Audio"
↓
Select MP3 file
↓
Choose language (EN/HI/TA)
↓
Text appears in journal
```

**Step 3: Search with AI** 🔍
```
Go to Search page
↓
Search: "vendor expensive"
↓
Results ranked by relevance (87% match)
↓
Click to expand → See extracted data
```

---

## 💡 KEY INSIGHTS

| Feature | Benefit |
|---------|---------|
| **Voice Input** | Hands-free journaling while planning |
| **AI Extraction** | No manual data entry needed |
| **Auto Tasks** | Never forget an action item |
| **Semantic Search** | Find entries by meaning |
| **Budget Tracking** | Automatic cost calculations |
| **Mood Analysis** | Know your stress levels |

---

## 🚀 IMPACT

**Before AI Journal:**
- 🔴 Lost in spreadsheets
- 🔴 Tasks scattered everywhere
- 🔴 Budget unclear
- 🔴 Feeling overwhelmed

**After AI Journal:**
- 🟢 Centralized journal
- 🟢 Tasks auto-organized
- 🟢 Budget automatically calculated
- 🟢 Organized and confident ✨

---

## ❓ QUICK Q&A

**Q: Is my data private?**
A: Yes, local first. Embeddings go to OpenAI for AI, nothing else shared.

**Q: What if AI extracts wrong data?**
A: Users see suggestions and can edit/uncheck before saving.

**Q: Works without internet?**
A: Journaling works offline, search needs internet for embeddings.

**Q: Cost to use?**
A: Just API costs (~$0.50/month for typical usage).

---

## 🎯 SUMMARY

**Problem:** Wedding planning is chaotic and stressful

**Solution:** AI Wedding Journal - Your intelligent wedding planning assistant

**How It Works:**
- Record/upload/type entries
- AI extracts vendors, tasks, costs, dates
- Smart search finds entries by meaning
- Task panel keeps everything organized

**Built With:** React + FastAPI + OpenAI + PostgreSQL + pgvector

**Result:** Organized, stress-free wedding planning 💍✨

---

**Let's start the demo! 🎬**

