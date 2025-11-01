# Testing the Suggestions Fix

**Date:** November 1, 2025
**Component:** JournalInput.tsx
**Status:** Ready for testing

---

## Quick Start

### 1. Start Backend
```bash
cd backend
poetry run uvicorn app.main:app --reload
```
Backend: http://localhost:8000

### 2. Start Frontend
```bash
cd frontend
npm run dev
```
Frontend: http://localhost:3000

### 3. Open Browser
```
http://localhost:3000
```

---

## Test Case 1: Suggestions Persist Until Save

### Steps:
1. **Navigate** to the journal page
2. **Type** some text in the journal textarea:
   ```
   Need to book photographer and florist.
   Wedding budget is $5000.
   Wedding date is June 15, 2025.
   ```
3. **Click** "✨ Get AI Suggestions" button
4. **Wait** for "Processing with AI..." to finish (2-5 seconds)
5. **Observe** green suggestion box appears with:
   - Vendors Found: 0
   - Tasks Identified: 2
   - Mood: (should detect sentiment)
   - Timeline: pre-wedding

### Expected Results:
✅ Green suggestion box visible
✅ AI analysis complete message shown
✅ Suggested Tasks listed:
   - "Book photographer" (high priority)
   - "Book florist" (high priority)
✅ Extracted Information shows dates

### Continue Test:
6. **Add more text** to the textarea (don't click anything)
   ```
   Also need to send invitations.
   ```
7. **Observe** suggestions stay visible - they don't disappear
8. **Verify** green box is still there

### Final Step:
9. **Click** "Save Entry" button
10. **Observe** green suggestion box disappears
11. **Verify** form clears completely
12. **Ready** for next entry

---

## Test Case 2: Tasks Are Created with Suggestions

### Steps:
1. **Type** text with action items:
   ```
   Meet with caterer Mamma's Kitchen ($2000).
   Also need to book venue by next week.
   Partner wants eco-friendly flowers.
   ```

2. **Click** "✨ Get AI Suggestions"

3. **Wait** for processing (see "Processing with AI..." spinner)

4. **See** green suggestion box with:
   - Suggested Tasks section showing checkboxes
   - Example tasks:
     ☑ Book venue (high)
     ☑ Confirm catering (medium)
     ☑ Choose eco-friendly flowers (medium)

### Verify Checkboxes:
5. **All tasks should be checked by default** ✅

6. **Uncheck ONE task** (e.g., "Choose eco-friendly flowers")
   - Click the checkbox to uncheck it

7. **Verify visual feedback** - checkbox is now unchecked

### Save and Verify:
8. **Click** "Save Entry"

9. **Wait** for save (button shows "Saving...")

10. **Check Task List** (should be visible on page)

11. **Verify Tasks Created:**
    - ✅ "Book venue" appears in task list (CHECKED = created)
    - ✅ "Confirm catering" appears in task list (CHECKED = created)
    - ❌ "Choose eco-friendly flowers" does NOT appear (UNCHECKED = not created)

### Result:
✅ Only checked tasks were created
✅ Unchecked tasks were ignored
✅ Tasks appear in task list with correct data
✅ Form cleared after save

---

## Test Case 3: No Suggestions Shown if No Tasks

### Steps:
1. **Type** simple text with no action items:
   ```
   Wedding planning is going well.
   I'm happy with my choices.
   ```

2. **Click** "✨ Get AI Suggestions"

3. **Wait** for AI processing

4. **Observe** green suggestion box appears but:
   - **Suggested Tasks section is empty** (no tasks listed)
   - Shows extracted information (dates, sentiments)
   - Vendors/Costs might be empty too

5. **Click** "Save Entry"

6. **Verify** NO tasks are created

### Result:
✅ No tasks created for entries without action items
✅ AI correctly identifies when there are no tasks
✅ Still shows analysis (mood, timeline) even without tasks

---

## Test Case 4: Multiple Entries in Sequence

### Steps:
1. **Entry 1** - Create with tasks:
   ```
   Book photographer ASAP!
   Budget: $1500
   ```
   - Click "Get AI Suggestions"
   - Keep all tasks checked
   - Click "Save Entry"
   - Verify tasks appear in task list

2. **Entry 2** - Create with different tasks:
   ```
   Finalize menu with caterer.
   Need to decide on colors too.
   ```
   - Click "Get AI Suggestions"
   - See new suggestions appear
   - Uncheck "Decide on colors"
   - Click "Save Entry"
   - Verify only "Finalize menu" task created

3. **Entry 3** - Dismiss before saving:
   ```
   Just thinking about the day!
   ```
   - Click "Get AI Suggestions"
   - See suggestions
   - Click "Dismiss suggestions" link (not Save Entry)
   - Verify green box disappears
   - Entry NOT created (text still in textarea)
   - Click "Save Entry" without suggestions shown
   - Verify entry created with no tasks

### Result:
✅ Each entry can have independent suggestions
✅ Dismiss doesn't save entry
✅ Multiple entries create multiple tasks correctly

---

## Test Case 5: Error Scenarios

### Scenario 1: Empty Entry
1. **Don't type anything**
2. **Click** "✨ Get AI Suggestions"
3. **Expected:** Error message "Please enter some text"

### Scenario 2: Network Error Simulation
1. **Type text**
2. **Disconnect network** (or stop backend)
3. **Click** "✨ Get AI Suggestions"
4. **Expected:** Error message appears (check console)
5. **Reconnect network**
6. **Try again** - should work

### Scenario 3: Processing Timeout
1. **Type text**
2. **Click** "✨ Get AI Suggestions"
3. **Wait** more than 10 seconds
4. **Expected:** Processing completes or error shown
5. **Verify** UI recovers gracefully

---

## Debugging Checklist

### If Suggestions Don't Appear:
- [ ] Check browser console (F12) for errors
- [ ] Verify backend is running: http://localhost:8000/docs
- [ ] Check API response in Network tab
- [ ] Verify `NEXT_PUBLIC_API_URL` is set correctly
- [ ] Check that /api/journal/entries endpoint responds

### If Tasks Don't Get Created:
- [ ] Check that checkboxes are being checked
- [ ] Verify task checkboxes have correct IDs (task-0, task-1, etc.)
- [ ] Check browser console for fetch errors
- [ ] Verify /api/tasks endpoint exists and works
- [ ] Check backend logs for task creation errors

### If Suggestions Disappear Too Early:
- [ ] Verify `showSuggestions` state is not being reset
- [ ] Check that `setExtractedData(null)` only happens after Save Entry
- [ ] Verify click handlers on buttons are correct

---

## Console Output to Expect

### Successful Suggestion Extraction:
```
Sending journal entry to Intake Agent for processing...
Intake Agent result: {success: true, data: {...}}
Extracted entities: {...}
Extracted tasks: {...}
Sentiment: {...}
```

### Successful Task Creation:
```
Creating tasks: [
  {title: "Book photographer", priority: "high"},
  {title: "Send invitations", priority: "high"}
]
Created 2 tasks
```

### After Save Entry:
```
Form cleared and suggestions dismissed
```

---

## Performance Metrics

| Action | Expected Time |
|--------|---|
| Get AI Suggestions | 2-5 seconds |
| Save Entry with 2 tasks | 1-2 seconds |
| Task creation API call | <500ms per task |
| Form clear and reset | <100ms |

---

## Visual Checklist

### "Get AI Suggestions" Button
- [ ] Appears only when text is entered
- [ ] Disappears after clicking (replaced by suggestions)
- [ ] Has ✨ emoji
- [ ] Text: "Get AI Suggestions"
- [ ] Blue background when hoverable
- [ ] Gray when disabled

### Suggestion Box (Green)
- [ ] Green background (#F0FDF4)
- [ ] Green border (#86EFAC)
- [ ] Header: "✓ AI Analysis"
- [ ] Summary grid with 2-4 stats
- [ ] Suggested Tasks with checkboxes
- [ ] Extracted Information section
- [ ] "Dismiss suggestions" button at bottom

### Task Checkboxes
- [ ] All checked by default
- [ ] Can be unchecked by clicking
- [ ] Show task title
- [ ] Show priority in parentheses (high/medium/low)
- [ ] Text is clickable too

### Save Entry Button
- [ ] Shows "Saving..." while processing
- [ ] Disabled during submission
- [ ] Re-enabled after save
- [ ] Clears form after success

---

## Success Criteria

✅ **All Tests Pass:**
- Suggestions persist until save
- Only checked tasks are created
- Form clears after save
- Multiple entries work independently
- Error handling works gracefully
- Console shows no errors

✅ **Performance Acceptable:**
- Get suggestions: <5 seconds
- Save entry: <2 seconds
- No UI freezing

✅ **User Experience:**
- Clear visual hierarchy
- Intuitive workflow
- Informative feedback messages
- Easy to dismiss suggestions

---

## Submission Checklist

Before considering this fix complete:

- [ ] Tested all 5 test cases
- [ ] All tests pass
- [ ] No console errors
- [ ] Tasks appear in task list
- [ ] Suggestions persist correctly
- [ ] Form clears after save
- [ ] Multiple entries work
- [ ] Visual design matches mockups

---

## Support

If issues occur:
1. **Check console** (F12 → Console tab)
2. **Check Network tab** for failed requests
3. **Verify backend is running** and responding
4. **Try hard refresh** (Ctrl+Shift+R)
5. **Check backend logs** for error messages

---

**Status: READY FOR TESTING** ✅
**Next Step: Run through all test cases above**
