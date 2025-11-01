# AI Suggestions Fix - Journal Input Component

**Issue Fixed:** November 1, 2025
**Component:** `frontend/src/components/JournalInput.tsx`

---

## Problems Fixed

### 1. AI Suggestions Disappearing
**Issue:** Suggestions appeared but disappeared after clicking "Save Entry"

**Root Cause:** The `extractedData` state was being cleared immediately after save, removing the suggestions UI

**Solution:**
- Added `showSuggestions` state to control visibility independently
- Extracted data persists until user clicks "Dismiss suggestions" or saves entry
- Added "✨ Get AI Suggestions" button to trigger extraction
- Suggestions now stay visible between extraction and save

### 2. Tasks Not Being Created
**Issue:** Suggested tasks appeared in UI but weren't saved to database

**Root Cause:** The task creation API call was commented out and never executed

**Solution:**
- Added checkbox UI for each suggested task (5 tasks max shown)
- All tasks checked by default
- When user clicks "Save Entry", only checked tasks are created
- Tasks are sent to `/api/tasks` endpoint with proper format:
  - `title` (required)
  - `description`
  - `priority` (high, medium, low)
  - `status` (pending)
  - `deadline`

---

## New User Flow

### Step 1: Type or Record Entry
User enters text via keyboard or voice recording

### Step 2: Get AI Suggestions (NEW)
- Click "✨ Get AI Suggestions" button
- AI analyzes text and extracts:
  - **Vendors, Costs, Dates** (Extracted Information)
  - **Suggested Tasks** with checkboxes
  - **Sentiment** (Mood)
  - **Timeline** (pre/post-wedding)

### Step 3: Review & Select Tasks
- See all suggested tasks with priority levels
- Uncheck any tasks you don't want to create
- All tasks checked by default
- Can dismiss suggestions with "Dismiss suggestions" link

### Step 4: Save Entry
- Click "Save Entry"
- Journal entry is created
- All checked tasks are created in database
- Form clears, suggestions disappear
- Ready for next entry

---

## Code Changes

### State Variables Added
```typescript
const [showSuggestions, setShowSuggestions] = useState(false)
```

### New Function: `handleExtractData`
- Called when user clicks "✨ Get AI Suggestions"
- Sends entry text to `/api/journal/entries`
- Sets `extractedData` and `showSuggestions = true`
- Shows processing indicator while AI analyzes

### Updated Function: `handleSubmit`
- Still saves journal entry
- Now retrieves checked tasks from UI
- Creates tasks via `/api/tasks` API
- Only sends checked tasks to database

### New UI Components
1. **"Get AI Suggestions" Button**
   - Shows when text entered and suggestions not yet shown
   - Disabled during processing

2. **Suggestions Box** (Green background)
   - Summary stats (vendors, tasks, mood, timeline)
   - **Suggested Tasks List** with checkboxes
   - Extracted Information summary
   - "Dismiss suggestions" button

3. **Task Checkboxes**
   - Each task has checkbox (checked by default)
   - Shows task title and priority
   - Up to 5 tasks shown
   - User can uncheck to skip creation

---

## API Integration

### Create Tasks Endpoint
```
POST /api/tasks
Body: {
  title: string (required),
  description: string,
  priority: "high" | "medium" | "low",
  status: "pending",
  deadline: string (optional, ISO date)
}
```

**Triggered By:** Checking tasks in suggestions and clicking "Save Entry"

---

## Data Flow Diagram

```
User Types/Records Entry
        ↓
   [Get AI Suggestions Button]
        ↓
   Fetch /api/journal/entries (Intake Agent)
        ↓
   Display Suggestions:
   - Vendors, Costs, Dates
   - Mood, Timeline
   - Suggested Tasks (with checkboxes)
        ↓
   User Reviews & Selects Tasks
        ↓
   [Save Entry Button]
        ↓
   Create Entry + Create Tasks
        ↓
   Clear Form & Suggestions
        ↓
   Ready for Next Entry
```

---

## User Experience Improvements

✅ **Persistent Suggestions** - Visible until dismissed or entry saved
✅ **Task Selection** - User can choose which tasks to create
✅ **Visual Feedback** - Green box with AI analysis results
✅ **Clear Action Items** - "Get AI Suggestions" button is explicit
✅ **Task Tracking** - Suggested tasks now appear in task list
✅ **Two-Phase Flow** - Separate extraction and saving steps

---

## Technical Details

### Checkbox State Management
```typescript
const checkedTasks = extractedData.tasks.explicit.filter((_: any, idx: number) => {
  const checkbox = document.getElementById(`task-${idx}`) as HTMLInputElement
  return checkbox?.checked
})
```

### Task Creation
```typescript
await Promise.all(
  checkedTasks.map((task: any) =>
    fetch(`${API_URL}/api/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: task.title,
        description: task.description || '',
        priority: task.priority || 'medium',
        status: 'pending',
        deadline: task.deadline,
      }),
    })
  )
)
```

---

## Testing the Fix

### Test 1: Suggestions Visibility
1. Type text in journal entry
2. Click "✨ Get AI Suggestions"
3. See green suggestion box appear
4. **Verify:** Suggestions stay visible
5. Type more text - suggestions remain
6. Click "Save Entry"
7. **Verify:** Suggestions disappear after save

### Test 2: Task Creation
1. Type text with action items (e.g., "Need to book photographer")
2. Click "✨ Get AI Suggestions"
3. See "Suggested Tasks" list with checkboxes
4. **Verify:** Tasks are checked by default
5. Uncheck one task
6. Click "Save Entry"
7. **Verify:** Checked tasks appear in Task List
8. **Verify:** Unchecked task is NOT created

### Test 3: Empty Suggestions
1. Type text with no action items
2. Click "✨ Get AI Suggestions"
3. **Verify:** "Suggested Tasks" section is empty
4. See only extracted information (vendors, costs, dates)
5. Click "Save Entry"
6. **Verify:** No tasks created, entry saved

---

## Future Enhancements

- [ ] Persist checkbox state if user dismisses and re-shows suggestions
- [ ] Edit task details (title, priority, deadline) before creating
- [ ] Bulk task operations (check/uncheck all)
- [ ] Task templates for common wedding planning items
- [ ] Drag-and-drop to reorder tasks
- [ ] Due date picker instead of text field

---

## Summary

The AI Suggestions feature now works correctly:
1. **Persistent Display** - Suggestions stay visible until explicitly dismissed
2. **Task Creation** - All checked tasks are created in database
3. **User Control** - Users can select which suggestions to accept
4. **Clear Flow** - "Get AI Suggestions" button makes the feature discoverable

The component now properly implements a two-phase workflow:
- Phase 1: Extract and suggest (separate from save)
- Phase 2: Save entry and create selected tasks

Status: **READY FOR TESTING** ✅
