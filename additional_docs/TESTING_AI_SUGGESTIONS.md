# Testing AI Suggestions Feature - Complete Guide

**Status:** ✅ Ready for Testing
**Date:** November 1, 2025
**Feature:** AI Suggestions Persistence & Task Creation

---

## Quick Start (3 Steps)

### Step 1: Start Backend
```bash
cd backend
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
✅ Backend runs on **http://localhost:8000**

### Step 2: Start Frontend (New Terminal)
```bash
cd frontend
npm run dev
```
✅ Frontend runs on **http://localhost:3000**

### Step 3: Open Browser
Navigate to **http://localhost:3000** and you're ready to test!

---

## What Was Fixed

### Issue 1: Suggestions Disappearing ✅ FIXED
**Before:** Suggestions appeared briefly then disappeared immediately
**After:** Suggestions persist in a green box until you click "Save Entry" or "Dismiss suggestions"

### Issue 2: Tasks Not Created ✅ FIXED
**Before:** Suggested tasks appeared but weren't saved to database
**After:** All checked tasks are created in the database when you click "Save Entry"

### Issue 3: Task Details Not Showing ✅ FIXED
**Before:** Only showed task title and priority "(high)"
**After:** Shows complete task details:
- Task title (bold)
- Priority badge (colored: red/amber/blue)
- Description text
- Deadline with 📅 emoji
- Status indicator

---

## Test Scenario 1: Basic Functionality (5 minutes)

### What This Tests
- Suggestions appear and persist
- "Get AI Suggestions" button works
- Tasks show full details
- Tasks are created in database

### Steps

1. **Type Entry**
   ```
   Need to book photographer and florist.
   Wedding is June 15.
   Budget is $5000.
   ```

2. **Click "✨ Get AI Suggestions" Button**
   - Wait 2-5 seconds for AI processing
   - See "⏳ Processing with AI..." spinner
   - Green box appears with AI Analysis

3. **Verify Suggestions Appear** ✅
   - Look for green box with "✓ AI Analysis"
   - See "Tasks Identified: 2"
   - See "Mood: (emotion)"
   - See "Timeline: (type)"

4. **Verify Task Details Show** ✅
   - Each task has:
     ```
     ☑ Book photographer [HIGH]
       Hire professional photographer for wedding
       📅 Due: 2025-06-15
       Status: pending
     ```
   - Priority badge is **colored**:
     - **RED** for HIGH priority
     - **AMBER** for MEDIUM priority
     - **BLUE** for LOW priority

5. **Click "Save Entry"**
   - Green box disappears
   - Form clears
   - Success message appears: "Created 2 task(s) successfully!"

6. **Verify Tasks Created** ✅
   - Tasks appear in task list (if visible on page)
   - Both tasks show in database
   - Check browser console (F12) for logs:
     ```
     [Tasks] Creating 2 tasks:
     [Tasks] Successfully created task: Book photographer
     [Tasks] Successfully created task: Book florist
     [Tasks] Successfully created 2 tasks
     ```

### Expected Results
```
✅ Green suggestions box appeared
✅ Suggestions stayed visible for 5+ seconds
✅ All task details visible (not just priority)
✅ Task checkboxes visible and checked
✅ "Save Entry" button worked
✅ 2 tasks created in database
✅ Form cleared after save
✅ Success message showed
```

---

## Test Scenario 2: Selective Task Creation (5 minutes)

### What This Tests
- Users can uncheck tasks
- Only checked tasks are created
- Unchecked tasks are ignored

### Steps

1. **Type Entry**
   ```
   Book florist. Buy decorations. Call caterer.
   ```

2. **Click "✨ Get AI Suggestions"**
   - Wait for suggestions to appear
   - See 3 tasks listed with checkboxes
   - All tasks are ☑ checked by default

3. **Uncheck Second Task**
   - Click checkbox for middle task to uncheck it
   - See checkbox change from ☑ to ☐
   - Other tasks stay ☑ checked

4. **Click "Save Entry"**
   - Suggestions disappear
   - Form clears

5. **Verify Correct Tasks Created** ✅
   ```
   ✅ Task 1: Created (was checked)
   ✅ Task 2: NOT created (was unchecked)
   ✅ Task 3: Created (was checked)
   ```

6. **Check Console Logs**
   ```
   [Tasks] Creating 2 tasks:
   [Tasks] Successfully created task: [Task 1]
   [Tasks] Successfully created task: [Task 3]
   [Tasks] Successfully created 2 tasks
   ```

### Expected Results
```
✅ Checkboxes toggle correctly
✅ Only 2 out of 3 tasks created
✅ Correct tasks created (not second one)
✅ Console shows exactly 2 creations
✅ Success message shows "Created 2 task(s)"
```

---

## Test Scenario 3: No Tasks Scenario (3 minutes)

### What This Tests
- App handles entries with no action items
- Suggestions still show other info
- No tasks created if none identified

### Steps

1. **Type Entry**
   ```
   The wedding planning is going smoothly.
   I'm really happy with all our decisions so far.
   Everything is on track.
   ```

2. **Click "✨ Get AI Suggestions"**
   - Green box appears
   - "Tasks Identified: 0" shown
   - No tasks listed (empty section)
   - Mood and timeline still shown

3. **Click "Save Entry"**
   - No tasks created
   - Entry saved

4. **Check Console**
   ```
   [Tasks] No tasks in extracted data
   ```

### Expected Results
```
✅ Suggestions shown even without tasks
✅ Green box displays sentiment/timeline
✅ No task section or empty task section
✅ No tasks created
✅ Console shows "No tasks"
```

---

## Test Scenario 4: Dismiss Without Saving (3 minutes)

### What This Tests
- "Dismiss suggestions" closes the box
- Entry is NOT saved when dismissing
- Can continue editing text

### Steps

1. **Type Entry**
   ```
   Need to book photographer.
   ```

2. **Click "✨ Get AI Suggestions"**
   - Green box appears
   - See "Dismiss suggestions" link at bottom

3. **Click "Dismiss suggestions"** (NOT "Save Entry")
   - Green box disappears
   - **Text stays in textarea** (not cleared!)
   - No entry created
   - No tasks created

4. **Add More Text**
   ```
   Also need to book florist.
   ```

5. **Click "✨ Get AI Suggestions" Again**
   - Updated suggestions appear
   - Shows both tasks now

6. **Click "Save Entry"**
   - Both tasks created
   - Entry saved

### Expected Results
```
✅ "Dismiss suggestions" link appears
✅ Dismissing removes green box
✅ Text remains in textarea (not saved)
✅ Can edit and get new suggestions
✅ Both tasks created on final save
```

---

## Test Scenario 5: Error Handling (3 minutes)

### What This Tests
- App handles errors gracefully
- Users see error messages
- App recovers from failures

### Steps

1. **Empty Entry Test**
   - Don't type anything
   - Click "✨ Get AI Suggestions"
   - Should see error: "Please enter some text"

2. **Network Error Simulation**
   - Stop backend (Ctrl+C in backend terminal)
   - Type text
   - Click "✨ Get AI Suggestions"
   - Should see error about connection
   - Check console (F12)
   - Restart backend
   - Try again - should work

3. **Server Recovery**
   - Restart backend
   - Type text
   - Click "✨ Get AI Suggestions"
   - Should work normally again

### Expected Results
```
✅ Error message shown for empty entry
✅ Connection error handled gracefully
✅ No crash or freeze
✅ Works again after reconnecting
✅ No stuck states
```

---

## Browser Console Monitoring

Open **F12** → **Console** tab to monitor logs.

### Successful Extraction
```
Sending journal entry to Intake Agent for processing...
Intake Agent result: {success: true, data: {...}}
Extracted entities: {vendors: [...], dates: [...]}
Extracted tasks: {explicit: [...]}
Sentiment: {emotion: "excited", confidence: 0.85}
```

### Successful Task Creation
```
[Tasks] Creating 2 tasks: [
  {title: "Book photographer", priority: "high", ...},
  {title: "Book florist", priority: "high", ...}
]
[Tasks] Creating task: Book photographer
[Tasks] Successfully created task: Book photographer
[Tasks] Creating task: Book florist
[Tasks] Successfully created task: Book florist
[Tasks] Successfully created 2 tasks
```

### Form Clear
```
Form cleared and suggestions dismissed
```

---

## Visual Checklist

### "Get AI Suggestions" Button
- [ ] Appears when text is entered
- [ ] Shows ✨ emoji
- [ ] Has blue styling
- [ ] Disabled while processing
- [ ] Disappears after clicking (replaced by suggestions)

### Processing Indicator
- [ ] Shows "⏳ Processing with AI..." while working
- [ ] Has spinning icon
- [ ] Appears for 2-5 seconds
- [ ] Disappears when done

### Suggestion Box (Green)
- [ ] Light green background
- [ ] Green border
- [ ] Has "✓ AI Analysis" header
- [ ] Shows 2x2 grid of stats:
  - [ ] Vendors Found
  - [ ] Tasks Identified
  - [ ] Mood
  - [ ] Timeline

### Task Cards
- [ ] Each task in separate card
- [ ] Checkbox on left (checked by default)
- [ ] Task title (bold)
- [ ] Priority badge (colored):
  - [ ] RED for HIGH
  - [ ] AMBER for MEDIUM
  - [ ] BLUE for LOW
- [ ] Description text visible
- [ ] 📅 Deadline shown
- [ ] Status shown
- [ ] Card clickable to toggle checkbox

### Extracted Information Section
- [ ] Shows vendors list
- [ ] Shows total costs
- [ ] Shows extracted dates
- [ ] All text visible and readable

### Dismiss Link
- [ ] Text says "Dismiss suggestions"
- [ ] Located at bottom of green box
- [ ] Clickable and works

### Success Message
- [ ] Shows "Created X task(s) successfully!"
- [ ] Appears for ~3 seconds
- [ ] Auto-dismisses
- [ ] Shows in message area

---

## Common Issues & Solutions

### Issue: "Get AI Suggestions" button doesn't appear
**Solution:**
- Type some text first
- Button appears only when text exists
- Check that `text.trim().length > 0`

### Issue: Suggestions disappear too fast
**Solution:**
- Check that you're not accidentally clicking elsewhere
- Look for green box - it should stay for 10+ seconds
- Only disappears on "Save Entry" or "Dismiss suggestions"

### Issue: Tasks don't appear as created
**Solution:**
1. Check browser console (F12)
2. Look for `[Tasks]` prefix logs
3. Verify checkboxes were checked (default is checked)
4. Check if tasks appear in task list
5. Verify API endpoint `/api/tasks` exists and works
6. Check backend logs for creation errors

### Issue: Task details not showing
**Solution:**
- Ensure backend is returning full task data
- Check console to see what data is received
- Verify `task.description`, `task.deadline`, `task.status` exist
- May need to add more fields to AI prompt

### Issue: Backend connection fails
**Solution:**
1. Verify backend is running: `poetry run uvicorn app.main:app --reload`
2. Check port 8000 is available
3. Verify `NEXT_PUBLIC_API_URL=http://localhost:8000` in frontend
4. Check CORS settings in backend

### Issue: OpenAI API error
**Solution:**
1. Verify `OPENAI_API_KEY` is set in backend `.env`
2. Check API key is valid
3. Verify account has credits
4. Check rate limits

---

## Performance Expectations

| Action | Time |
|--------|------|
| Click "Get AI Suggestions" | <200ms |
| AI Processing | 2-5 seconds |
| Show Suggestions | <100ms |
| Click "Save Entry" | <500ms |
| Create each task | 100-300ms |
| Form clear | <100ms |
| Total workflow | 3-7 seconds |

---

## Success Criteria

All these must pass for the feature to be complete:

- [ ] Suggestions appear in green box
- [ ] Suggestions persist for 10+ seconds
- [ ] Full task details visible (not just priority)
- [ ] Task checkboxes work (can toggle)
- [ ] Default: all tasks checked
- [ ] "Save Entry" creates only checked tasks
- [ ] Tasks appear in database/task list
- [ ] Form clears after save
- [ ] Success message shows (3 seconds)
- [ ] Dismiss button works
- [ ] No console errors
- [ ] Error handling works
- [ ] Multiple entries work independently
- [ ] UI matches design (colors, spacing, typography)

---

## Next Steps After Testing

1. **If All Tests Pass** ✅
   - Feature is production-ready
   - User can start using AI suggestions
   - Document any edge cases found
   - Plan for V2 enhancements

2. **If Issues Found** 🔧
   - Document exact steps to reproduce
   - Check console logs
   - Review code changes
   - Fix and retest

3. **Enhancements for V2** 📋
   - Edit task details before creating
   - "Select All" / "Deselect All" buttons
   - Drag to reorder tasks
   - Save task templates
   - Due date picker instead of text
   - Task history/tracking

---

## Support

**Questions or issues?**
1. Check console logs (F12)
2. Review this guide
3. Check backend logs
4. Verify environment setup
5. Restart both backend and frontend

**Success indicators:**
- Backend: `INFO: Uvicorn running on http://0.0.0.0:8000`
- Frontend: `▲ Local: http://localhost:3000`
- Browser: App loads without errors

---

**Status: READY FOR TESTING** ✅

Start the backend and frontend, then follow the test scenarios above!
