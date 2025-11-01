# Search Feature - Quick Start

**Feature:** Semantic search across journal entries
**Status:** Ready to use
**Time to test:** 2 minutes

---

## Quick Start (30 seconds)

### 1. Start Services
```bash
# Terminal 1 - Backend
cd backend
poetry run uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 2. Create a Test Entry
- Open http://localhost:3000
- Write: "We called the photographer today. Very expensive but has great reviews."
- Click "✨ Get AI Suggestions"
- Click "Save Entry"

### 3. Search Your Entry
- Click "Search" in navigation
- Type: "photographer cost"
- Should find the entry!

---

## How to Use

### Search Page (http://localhost:3000/search)

**Step 1: Enter Query**
```
Search entries... (e.g., 'vendors', 'budget concerns', 'timeline')
```

**Step 2: Hit Enter or Click Search**
- Results appear ranked by relevance
- Green bar shows match percentage (0-100%)
- Sentiment badge shows mood (positive/negative/neutral)

**Step 3: Expand for Details**
- Click any result to see full entry
- View extracted entities (vendors, costs, dates)
- See mood analysis with confidence

---

## What It Finds

### ✅ Semantic Meaning (Not Just Keywords)
Search for... | Finds entries about...
---|---
"vendor issues" | Problems with photographers, caterers, florists
"budget concerns" | Spending too much, cost overruns, expensive items
"timeline pressure" | "Running out of time", "deadline stress", "rush"
"mood swings" | Emotional ups and downs, feeling overwhelmed

### ✅ Natural Language
- "I'm worried about costs" → finds budget entries
- "Vendor is expensive" → finds price concerns
- "Time is running out" → finds timeline entries

---

## Examples

### Example 1: Vendor Search

**Search:** "vendor"

**Results:**
```
🏢 Photographer booking (87% match)
   Mood: Positive
   Vendors: ABC Photography
   Budget: ₹50,000

🏢 Catering issue (72% match)
   Mood: Negative
   Vendors: XYZ Catering
   Budget: ₹1,00,000
```

### Example 2: Budget Search

**Search:** "expensive"

**Results:**
```
💰 Guest count increase (95% match)
   Vendors mentioned: 5
   Total budget: ₹5,00,000
   Budget overrun noted

💰 Venue too costly (81% match)
   Mood: Concerned
   Budget: ₹2,00,000
```

---

## Result Cards Explained

### Header (Always Visible)

```
📅 01 Nov 2025  ━━━━━━━━━━━━━━━━  87% match
We called photographer...          💭 Positive
```

- **Date** - When entry was created
- **Bar** - Relevance percentage (thickness shows score)
- **Text** - Preview of entry
- **Mood** - Sentiment badge

### Details (Click to Expand)

```
📝 Full Entry
Complete text of the journal entry...

💭 Mood Analysis
Positive confidence: 92%

🔍 Extracted Information
🏢 Vendors: ABC Photography
💰 Budget: ₹50,000
📅 Key Dates: 15 Nov 2025
```

---

## Search Tips

### ✅ Good Searches
- "vendor" - Generic term, finds all vendor entries
- "photographer" - Specific vendor type
- "budget concerns" - Specific topic
- "timeline" - Important dates/urgency
- "expensive" - Cost-related

### ❌ Bad Searches
- "xyz" - Random letters
- "the" - Too generic, low relevance
- "" - Empty search
- "2025-11-01" - Dates don't work well (yet)

### 🎯 Best Practices
1. Use 1-3 words for best results
2. Use natural language phrasing
3. Try different words if first search fails
4. Expand results to see extracted data
5. Look at sentiment badges to understand context

---

## Understanding Relevance Score

**Green Bar Meaning:**

```
0-30%   │ Low relevance (loosely related)
30-60%  │ Medium relevance (related topic)
60-80%  │ High relevance (very similar)
80-100% │ Exact match (directly answers query)
```

**How It's Calculated:**
- Compares semantic meaning of search query vs entry
- Uses AI embeddings to understand concepts
- Not just keyword matching
- Shows how well entry answers your search

---

## Sentiment Badges

### Positive Entry
```
💭 Positive (92% confidence)
```
Green badge. Entry expresses happy, satisfied feelings.

### Negative Entry
```
💭 Negative (87% confidence)
```
Red badge. Entry expresses worried, frustrated feelings.

### Neutral Entry
```
💭 Neutral (78% confidence)
```
Gray badge. Entry is factual, balanced tone.

---

## Common Scenarios

### Scenario 1: Find Vendor Issues
```
Search: "vendor problems"
↓
Results sorted by relevance
↓
Expand entries to see which vendors
↓
Check budget impact in extracted data
```

### Scenario 2: Check Budget Status
```
Search: "budget"
↓
See all budget-related entries
↓
Sentiment badge shows stress level
↓
Expand to see total costs
```

### Scenario 3: Timeline Analysis
```
Search: "timeline" or "deadline"
↓
Find time-sensitive entries
↓
Check dates in extracted data
↓
Assess urgency from sentiment
```

---

## FAQs

**Q: Why isn't my entry showing up?**
A: The search uses semantic meaning. Try different words that describe the concept, not exact phrases.

**Q: What if I get no results?**
A: Either you don't have entries about that topic, or try rephrasing. The search understands concepts.

**Q: How does it rank results?**
A: By how similar the entry's meaning is to your search query. Higher % = better match.

**Q: Can I search by date?**
A: Not yet. But you can see dates in expanded entry details.

**Q: Can I filter by sentiment?**
A: Not yet, but sentiment badge shows in each result.

**Q: Is my data private?**
A: All searches happen locally. No data sent to external services (except embeddings API).

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Submit search |
| Click card | Expand/collapse details |
| Esc | Dismiss expanded view (coming soon) |

---

## Troubleshooting

**No results appearing?**
1. Check if backend is running (`http://localhost:8000/docs`)
2. Verify entries exist (check main journal page)
3. Try simpler search terms

**Search is slow?**
1. Normal on first search (embeddings generation)
2. Subsequent searches should be faster
3. Check internet connection

**Entries not showing?**
1. Entries need embeddings to be searchable
2. New entries might take a moment to embed
3. Try creating an entry, wait 5 seconds, then search

---

## Next Steps

1. **Create entries** with various topics
2. **Experiment with searches** - try different phrasings
3. **Expand results** to see extracted information
4. **Check sentiment badges** to understand context
5. **Note patterns** - what searches work best?

---

## Need Help?

- Check SEMANTIC_SEARCH.md for technical details
- See QUICK_REFERENCE.md for API info
- Check START_APPLICATION.md for setup

---

**Happy searching!** 🔍

Use semantic search to explore your wedding planning journey and find insights you didn't know you had.

