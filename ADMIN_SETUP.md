# Administrator Setup Guide for Poetry

Since you're running Cursor in Administrator mode, here's the complete setup process.

## Step 1: Install Python (if needed)

### Verify Python Installation
```bash
python --version
python -m pip --version
```

Should show Python 3.11+

### If Python is not installed
- Download from python.org
- Run installer in Administrator mode
- Check "Add Python to PATH"
- Verify installation afterward

---

## Step 2: Install Poetry

### Option A: Pip Installation (Recommended for Admin Mode)
```bash
python -m pip install --upgrade pip
pip install poetry
```

### Option B: Direct Download
```bash
# Use pipx (if available)
pipx install poetry

# Or download from official source
# Visit: https://python-poetry.org/docs/
```

### Verify Installation
```bash
poetry --version
# Should output: Poetry (version 1.x.x)
```

---

## Step 3: Configure Poetry

### Set Python Virtual Environment in Project
```bash
cd backend

# Tell poetry to use a local venv in the project
poetry config virtualenvs.in-project true

# Verify configuration
poetry config --list
```

### Create Virtual Environment
```bash
# This creates .venv folder in backend/
poetry install
```

---

## Step 4: Backend Setup

### Step 4.1: Configure Environment
```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` with your cloud PostgreSQL:
```env
DATABASE_URL=postgresql+asyncpg://username:password@cloud-host.com:5432/wedding_journal
SECRET_KEY=your-secret-key
DEBUG=True
```

### Step 4.2: Install Dependencies
```bash
# In backend directory
poetry install
```

Expected output:
```
Installing dependencies from lock file

Package operations: 45 packages installed

Installing the current project: wedding-journal-backend (0.1.0)
```

### Step 4.3: Initialize Database
```bash
poetry run alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade base -> 001, initial schema
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002, initial schema
```

### Step 4.4: Run Backend Server
```bash
poetry run uvicorn app.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

## Step 5: Troubleshooting Administrator Issues

### Issue: Poetry Command Not Found

**Error:** `'poetry' is not recognized as an internal or external command`

**Solution:**
```bash
# Use Python module directly
python -m poetry install
python -m poetry run uvicorn app.main:app --reload

# Or check PATH
where poetry
# Should show a path like: C:\Users\...\AppData\Python\Scripts\poetry.cmd

# If not found, reinstall poetry
pip uninstall poetry
pip install poetry
```

### Issue: Permission Denied

**Error:** `PermissionError: [Errno 13] Permission denied`

**Solution:**
1. Run terminal as Administrator ✓ (you're already doing this)
2. Clear pip cache:
```bash
pip cache purge
poetry cache clear . --all
```

3. Reinstall:
```bash
pip uninstall poetry
pip install poetry --force-reinstall
```

### Issue: Cannot Install Dependencies

**Error:** `ERROR: Could not open requirements file`

**Solution:**
```bash
# Ensure you're in the backend directory
cd backend

# Check pyproject.toml exists
ls pyproject.toml

# Try installing with verbose output
poetry install -vvv
```

### Issue: Virtual Environment Issues

**Error:** `Poetry could not find a python environment`

**Solution:**
```bash
# Configure poetry to use system Python
poetry config virtualenvs.use-active-venv true

# Specify Python version
poetry env use python3.11

# Or remove and recreate venv
rm -rf .venv
poetry install
```

---

## Step 6: Frontend Setup (in separate terminal)

### 6.1 Install Node Dependencies
```bash
cd frontend
npm install
```

### 6.2 Run Development Server
```bash
npm run dev
```

Expected output:
```
  ▲ Next.js 14.0.0
  - Local:        http://localhost:3000
```

---

## Step 7: Verify Everything Works

### Test Backend Health
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

### Test Frontend
Open in browser: `http://localhost:3000`
- Should see Wedding Journal header
- Should see journal input form
- Should see task panel on right

### Test API Connection
In browser console (F12):
```javascript
fetch('http://localhost:8000/api/user/preferences')
  .then(r => r.json())
  .then(d => console.log(d))
```

Should return user preference object.

---

## Step 8: Common Admin Mode Issues & Fixes

### Issue: Network Access Blocked
**Error:** `Connection refused` when connecting to localhost

**Solution:**
- Windows Defender might block: Add Python to firewall exceptions
- Or temporarily disable Windows Defender for testing
- Restart after changes

### Issue: Database Connection Fails
**Error:** `could not connect to server`

**Solution:**
```bash
# Test your connection string directly
psql "postgresql://user:password@host:port/db"

# If it works, then check .env file has exact same string:
cat .env
# Verify DATABASE_URL line has no typos

# Also verify pgvector is installed:
psql -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### Issue: Port Already in Use
**Error:** `Address already in use: ('0.0.0.0', 8000)`

**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill it (replace PID with number from above)
taskkill /PID <PID> /F

# Or use different port
poetry run uvicorn app.main:app --port 8001 --reload
```

---

## Step 9: Development Workflow

### Running Both Backend & Frontend

**Terminal 1 (Backend):**
```bash
cd backend
poetry run uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

**Terminal 3 (Database/Optional):**
```bash
# Monitor database (if local PostgreSQL)
psql -h localhost -U username -d wedding_journal
SELECT COUNT(*) FROM journal_entries;
```

---

## Step 10: Quick Commands Reference

```bash
# Backend
cd backend
poetry install              # Install deps
poetry run alembic upgrade head  # Setup DB
poetry run uvicorn app.main:app --reload  # Start server
poetry run pytest          # Run tests
poetry run black app/      # Format code
poetry run ruff check app/ # Lint code

# Frontend
cd frontend
npm install                # Install deps
npm run dev               # Start dev server
npm run build             # Build for prod
npm run lint              # Check code

# Database
poetry run alembic current        # Check migrations
poetry run alembic downgrade base # Reset DB
```

---

## ✅ Success Checklist

After completing all steps:

- [ ] Poetry installed and working
- [ ] Backend dependencies installed
- [ ] Database migrations run successfully
- [ ] Backend server starts on port 8000
- [ ] Health check returns `{"status": "healthy"}`
- [ ] Frontend dependencies installed
- [ ] Frontend server starts on port 3000
- [ ] Can see journal UI in browser
- [ ] Can create a test journal entry
- [ ] Entry appears in list
- [ ] No errors in browser console
- [ ] No errors in backend terminal

---

## 🎯 Next After Setup

1. Create a test journal entry
2. Verify it appears in the UI
3. Check it in the database:
```sql
SELECT * FROM journal_entries ORDER BY created_at DESC LIMIT 1;
```
4. Create a test task
5. Complete the task
6. Verify full workflow works

---

**You're all set!** The MVP is ready for testing in Administrator mode. 🚀

If you hit any issues, check the specific troubleshooting section above or consult:
- BACKEND_SETUP.md for backend-specific issues
- VERIFICATION.md for testing procedures
- CLAUDE.md for general development info
