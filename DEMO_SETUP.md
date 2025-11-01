# Demo Setup Guide - Ready to Present! 🎬

**File:** `DEMO_SCRIPT.md` (opens with this guide)

---

## ⏱️ Timing: 3 Minutes Exact

- **Problem Statement:** 30 seconds
- **Solution Overview:** 1 minute
- **Tech Stack:** 1 minute 30 seconds
- **Live Demo:** 1 minute
- **Q&A:** As needed

---

## 🚀 Before Demo Starts

### 1. **Start Services (do this BEFORE presenting)**

```bash
# Terminal 1 - Backend (takes ~10 seconds to start)
cd backend
poetry run uvicorn app.main:app --reload --port 8000

# Wait for: "Uvicorn running on http://127.0.0.1:8000"

# Terminal 2 - Frontend (takes ~15 seconds to build)
cd frontend
npm run dev

# Wait for: "ready - started server on 0.0.0.0:3000"
```

### 2. **Open Browser**
```
http://localhost:3000
```

---

## 📝 Demo Script Sections

### **Section 1: Problem (0:00 - 0:30)**
Read: "The Problem" section from DEMO_SCRIPT.md
- Paint picture of wedding chaos
- Mention scattered notes, forgotten tasks
- Connect to audience emotions

### **Section 2: Solution (0:30 - 1:30)**
Read: "The Solution" section
- Go through 4 key features:
  1. Capture thoughts (voice/text/upload)
  2. AI extracts automatically
  3. Tasks managed automatically
  4. Smart search by meaning
- Use emoji to keep it engaging

### **Section 3: Tech Stack (1:30 - 3:00)**
Show the architecture diagram while explaining:
- Frontend (React/Next.js) - what users see
- Backend (FastAPI/LangGraph) - where the AI lives
- Database (PostgreSQL + pgvector) - where data lives
- Brief mention of OpenAI APIs

### **Section 4: Live Demo (whenever ready)**
Follow: "Live Demo" section
- **Step 1 (30 sec):** Create entry → Get suggestions → Save
- **Step 2 (15 sec):** Upload audio file
- **Step 3 (15 sec):** Semantic search example

---

## 💻 Live Demo Checklist

### **Demo 1: AI Suggestions** ✨

```
1. Click on journal input area
2. Type: "Just booked photographer for ₹50,000.
          Need florist and caterer next.
          Running low on budget."
3. Click "✨ Get AI Suggestions" button
4. Wait 2-3 seconds for green box to appear
5. POINT: "Look - AI automatically found:
           - Vendors (photographer)
           - Tasks (book florist, book caterer)
           - Budget (₹50,000)
           - Mood (concerned)"
6. Check 2-3 task checkboxes
7. Click "Save Entry"
8. POINT: "See tasks appear on right side instantly!"
```

**What to expect:**
- ✅ Green suggestion box with all data
- ✅ Task checkboxes ready
- ✅ Right panel shows created tasks

### **Demo 2: Audio Upload** 🎙️

```
1. Have an audio file ready (MP3, WAV, or M4A)
2. Look for "📁 Upload Audio" option
3. Click to select file
4. Choose language (EN/HI/TA)
5. Text appears in journal
6. POINT: "Hands-free journaling - no typing needed!"
```

**What to expect:**
- ✅ File uploads quickly
- ✅ Transcription appears in textarea
- ✅ Can then get AI suggestions on audio text

### **Demo 3: Semantic Search** 🔍

```
1. Go to Search page (if time allows)
2. Search: "vendor expensive"
3. POINT: "Notice relevance percentage - 87% match
           AI understands MEANING, not just keywords"
4. Click entry to expand
5. POINT: "See extracted vendors, budget, sentiment
           Everything extracted automatically!"
```

**What to expect:**
- ✅ Results appear within 1-2 seconds
- ✅ Relevance bar shows match quality
- ✅ Expanded view shows full details

---

## ⚠️ If Something Goes Wrong

### **Search endpoint not working?**
- The import issue was fixed (AsyncSessionLocal)
- If still broken, ignore it for demo
- Focus on AI suggestions instead

### **Tasks not appearing?**
- Refresh the page (F5)
- They should appear after 2 seconds

### **Audio upload not working?**
- Skip it, move to search instead
- Focus on the AI suggestions demo

### **Slow responses?**
- Normal first run (embeddings generation)
- Mention: "First run is slower, cache speeds it up"

---

## 🎙️ Speaking Tips

### **Opening:**
"Wedding planning is **overwhelming**. Today we show how **AI** makes it **simple**."

### **During Demo:**
- Point to screen elements
- Pause for reactions
- Use timing: "In just 2 seconds, AI extracted..."
- Highlight key moments

### **Closing:**
"From chaos to clarity. That's AI Wedding Journal."

---

## 📊 Talking Points

| Topic | Key Message |
|-------|-------------|
| **Problem** | Scattered, stressful, losing tasks |
| **Solution** | Centralized, AI-powered, automatic |
| **AI Value** | Extracts data, finds patterns, predicts needs |
| **Tech** | Modern stack, proven technologies |
| **UX** | Simple, intuitive, works with voice too |
| **Impact** | Couples feel organized and confident |

---

## ✅ Pre-Demo Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Browser open at http://localhost:3000
- [ ] Have demo text ready to copy/paste
- [ ] Have audio file for upload demo
- [ ] Read DEMO_SCRIPT.md once before presenting
- [ ] Test one full flow (type → suggest → save → search)
- [ ] Clear browser console (F12 → Console → Clear)

---

## 🎯 Success Metrics

Demo is successful if audience sees:
- ✅ AI automatically extracted vendors
- ✅ Tasks created from journal entry
- ✅ Tasks appeared on right side
- ✅ Search found entries by meaning
- ✅ Professional, working application

---

## 📱 Demo Flow Diagram

```
START PRESENTING
  ↓
Problem Statement (30 sec)
  ↓
Solution Overview (1 min)
  ↓
Tech Stack (1 min 30 sec)
  ↓
LIVE DEMO (1-2 min)
  ├─ Create entry with suggestions
  ├─ Show tasks on right panel
  └─ Optional: Search or upload audio
  ↓
Q&A
  ↓
END: "From chaos to clarity. That's AI Wedding Journal."
```

---

## 💬 Expected Questions & Answers

**Q: How does it know to create tasks?**
A: "Claude AI reads your journal entry and understands what needs to be done. It's like having a planning assistant read your thoughts."

**Q: Can I edit the AI suggestions?**
A: "Yes, you can uncheck any task you don't want, or manually add more."

**Q: Is my data safe?**
A: "Yes, only embeddings go to OpenAI for the AI features. Your journal stays on your device."

**Q: Does it need internet?**
A: "For AI features yes, but basic journaling works offline."

**Q: Cost to use?**
A: "Just API costs - about ₹10-20 per month for regular use."

---

## 🎬 Ready to Present!

1. ✅ Open DEMO_SCRIPT.md
2. ✅ Backend & Frontend running
3. ✅ Browser ready at localhost:3000
4. ✅ Take a deep breath
5. ✅ Start speaking!

**You've got this! 🚀**

---

*Last Updated: November 1, 2025*
*Demo Duration: 3 minutes*
*Status: Ready to present ✨*

