# Verification Guide - MVP Testing

Use this guide to verify that the complete MVP is working correctly.

## Prerequisites
- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:3000`
- PostgreSQL accessible from your machine

## Quick Tests

### 1. Backend Health Check

**Test:** Verify backend is responding

```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{"status": "healthy"}
```

### 2. API Documentation

**Test:** Access interactive API docs

**URL:** `http://localhost:8000/docs`

**Expected:** Swagger UI showing all 13 endpoints

---

## API Testing (curl)

### Create Journal Entry

```bash
curl -X POST http://localhost:8000/api/journal/entry \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Met with the caterer today. They quoted 2500 per plate.",
    "language": "en",
    "suggestion_mode": true
  }'
```

**Expected Response:**
```json
{
  "id": "uuid-string",
  "raw_text": "Met with the caterer...",
  "language": "en",
  "themes": [],
  "sentiment": null,
  "created_at": "2024-01-01T10:00:00",
  "entities": [],
  "tasks": []
}
```

### Get All Entries

```bash
curl http://localhost:8000/api/journal/entries
```

**Expected Response:**
```json
{
  "total": 1,
  "entries": [
    {
      "id": "uuid",
      "raw_text": "Met with the caterer...",
      ...
    }
  ]
}
```

### Get Single Entry

```bash
# Replace with actual entry ID
curl http://localhost:8000/api/journal/entry/00000000-0000-0000-0000-000000000001
```

**Expected:** Entry details or 404 if not found

### Create Task

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "action": "Call caterer for final headcount",
    "priority": "high",
    "deadline": "2024-01-15"
  }'
```

**Expected Response:**
```json
{
  "id": "uuid",
  "action": "Call caterer for final headcount",
  "priority": "high",
  "status": "pending",
  "deadline": "2024-01-15",
  ...
}
```

### Get Pending Tasks

```bash
curl http://localhost:8000/api/tasks/pending
```

**Expected Response:**
```json
{
  "total": 1,
  "pending_count": 1,
  "completed_count": 0,
  "tasks": [...]
}
```

### Complete Task

```bash
# Replace with actual task ID
curl -X POST http://localhost:8000/api/tasks/00000000-0000-0000-0000-000000000001/complete
```

**Expected Response:**
```json
{
  "id": "uuid",
  "action": "...",
  "status": "completed",
  "completed_at": "2024-01-01T10:00:00",
  ...
}
```

### Get User Preferences

```bash
curl http://localhost:8000/api/user/preferences
```

**Expected Response:**
```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "values": [],
  "budget_goal": null,
  "wedding_date": null,
  "primary_language": "en",
  "suggestion_mode_default": true,
  "post_wedding_mode": false,
  "created_at": "2024-01-01T10:00:00"
}
```

### Update User Preferences

```bash
curl -X PUT http://localhost:8000/api/user/preferences \
  -H "Content-Type: application/json" \
  -d '{
    "wedding_date": "2024-06-15",
    "budget_goal": 100000,
    "values": ["eco-friendly", "budget-conscious"],
    "primary_language": "en"
  }'
```

**Expected Response:** Updated preferences

### Get Timeline Status

```bash
curl http://localhost:8000/api/user/timeline
```

**Expected Response:**
```json
{
  "wedding_date": "2024-06-15",
  "days_until_wedding": 166,
  "timeline_mode": "planning",
  "is_post_wedding": false,
  "post_wedding_days": null
}
```

---

## Frontend Testing

### 1. Home Page (`http://localhost:3000`)

**Visual Checks:**
- [ ] Header with Wedding Journal logo appears
- [ ] Navigation links (Journal, Search) visible
- [ ] Journal input area with textarea visible
- [ ] Task panel on right side visible
- [ ] Tailwind styling applied (gradient background)

**Functional Checks:**
- [ ] Can type in journal textarea
- [ ] Can see "AI suggestions enabled" text
- [ ] Can see "Save Entry" button
- [ ] Task panel shows "No pending tasks" initially

### 2. Create Journal Entry

**Steps:**
1. Type text in journal input: "Planning the venue for our wedding."
2. Click "Save Entry" button

**Expected:**
- [ ] Entry appears in "Recent Entries" section below
- [ ] Entry shows date, text, and any extracted themes
- [ ] Textarea clears after successful save

### 3. Create Task

**Steps:**
1. Click "+" icon in Task panel
2. Type action: "Book the venue"
3. Select priority: "High"
4. Click "Add"

**Expected:**
- [ ] Task appears in task list
- [ ] Task shows action, priority, and status
- [ ] Task count updates

### 4. Complete Task

**Steps:**
1. Hover over a task
2. Click the circle icon on the left

**Expected:**
- [ ] Task disappears from pending list
- [ ] Success notification (if implemented)

### 5. Search Page (`http://localhost:3000/search`)

**Visual Checks:**
- [ ] Search form visible with input and button
- [ ] "No searches yet" message visible initially
- [ ] Navigation working

**Functional Checks:**
- [ ] Can type in search input
- [ ] Can click search button
- [ ] Shows appropriate results or "No results found"

---

## Database Verification

### Connect to PostgreSQL

```bash
# Replace with your credentials
psql -h your-host -U username -d wedding_journal
```

### Check Tables Exist

```sql
-- List all tables
\dt

-- Should show:
-- user_preferences
-- journal_entries
-- master_entities
-- entities
-- tasks
```

### Check Sample Data

```sql
-- Count entries
SELECT COUNT(*) as entry_count FROM journal_entries;

-- List recent entries
SELECT id, raw_text, created_at FROM journal_entries ORDER BY created_at DESC LIMIT 5;

-- Count tasks
SELECT COUNT(*) as task_count FROM tasks;

-- Check user preferences
SELECT * FROM user_preferences;
```

### Verify pgvector

```sql
-- Check pgvector extension
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Should return: (vector extension exists)
```

---

## Error Troubleshooting

### Backend Errors

#### "Cannot connect to database"
```bash
# Verify connection string in .env
# Test direct connection:
psql $DATABASE_URL

# Check if pgvector is available:
psql $DATABASE_URL -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

#### "Module not found"
```bash
cd backend
poetry install --no-cache
poetry show  # List installed packages
```

#### "Port 8000 already in use"
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>

# Or use different port:
poetry run uvicorn app.main:app --port 8001 --reload
```

### Frontend Errors

#### "Failed to connect to API"
- Check backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Open browser console (F12) for actual error

#### "CORS error"
- Backend has CORS enabled for all origins
- Verify backend `/docs` is accessible

#### "Module not found"
```bash
cd frontend
npm install
npm cache clean --force
npm install
```

### Database Errors

#### "pgvector extension not available"
```sql
-- In your PostgreSQL:
CREATE EXTENSION IF NOT EXISTS vector;
```

#### "Tables don't exist"
```bash
cd backend
poetry run alembic downgrade base
poetry run alembic upgrade head
```

#### "Permission denied"
- Verify user has CREATE TABLE permissions
- Check connection string credentials

---

## Performance Testing

### Expected Response Times (MVP)
- Journal entry creation: < 500ms
- Get entries list: < 200ms
- Get user preferences: < 100ms
- Task operations: < 300ms

### Load Test Simple Query
```bash
# Create 10 entries quickly
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/journal/entry \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"Entry number $i\", \"language\": \"en\", \"suggestion_mode\": true}"
done

# Check retrieval time
time curl http://localhost:8000/api/journal/entries
```

---

## Checklist for MVP Verification

**Backend:**
- [ ] Health check responds
- [ ] API docs load at /docs
- [ ] Can create journal entry
- [ ] Can list entries
- [ ] Can get single entry
- [ ] Can create task
- [ ] Can complete task
- [ ] Can get/update preferences
- [ ] Can get timeline status

**Frontend:**
- [ ] Home page loads
- [ ] Can create journal entry
- [ ] Entry appears in list
- [ ] Can create task
- [ ] Can complete task
- [ ] Search page loads
- [ ] Navigation works
- [ ] UI looks good (Tailwind)

**Database:**
- [ ] All 5 tables exist
- [ ] pgvector extension available
- [ ] Vector index on journal_entries
- [ ] Data persists correctly
- [ ] Can query entries and tasks

**Integration:**
- [ ] Frontend connects to backend
- [ ] Created entries show in frontend
- [ ] API responses match schemas
- [ ] No CORS errors
- [ ] No console errors

---

## Success Criteria

✅ **MVP is working if:**

1. Backend API responds to all 13 endpoints
2. Frontend renders without errors
3. Can create and retrieve journal entries
4. Can manage tasks (create, complete)
5. Database persists all data
6. Frontend-Backend integration works
7. No critical errors in console
8. Response times are acceptable (< 1s)

---

## Next Steps After Verification

Once MVP is verified:

1. **Commit to git** with a meaningful message
2. **Document any issues** found during testing
3. **Prepare for Phase 2** - AI agents implementation
4. **Plan entity extraction** agent for Week 3
5. **Review and optimize** code if needed

---

**You now have a fully working MVP!** 🎉

Proceed to Phase 2: AI Agents when ready.
