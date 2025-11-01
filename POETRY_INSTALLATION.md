# 🔧 Poetry Installation Guide for Windows (Administrator Mode)

## Problem
```
poetry : The term 'poetry' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

This means Poetry is not installed or not in your PATH.

---

## Solution: Install Poetry via Pip

### Step 1: Upgrade Pip (Required)

Open PowerShell as Administrator and run:

```powershell
python -m pip install --upgrade pip
```

Expected output:
```
Successfully installed pip-X.X.X
```

### Step 2: Install Poetry via Pip

```powershell
pip install poetry
```

This will:
- Download Poetry package
- Install it in your Python environment
- Make `poetry` command available system-wide

Expected output:
```
Successfully installed poetry-X.X.X
```

**Wait for it to complete - may take 1-2 minutes**

### Step 3: Verify Poetry Installation

```powershell
poetry --version
```

**Expected output:**
```
Poetry (version 1.7.x)
```

If you see this, Poetry is successfully installed! ✅

---

## Alternative: If Pip Installation Fails

### Option A: Use Python Module Directly

Instead of `poetry` commands, use:

```powershell
python -m poetry --version
python -m poetry install
python -m poetry run alembic upgrade head
python -m poetry run uvicorn app.main:app --reload
```

### Option B: Install via Official Installer

1. Download from: https://python-poetry.org/docs/
2. Run the official installer
3. Verify installation afterward

---

## Step 4: Configure Poetry (One-Time Setup)

After Poetry is installed, configure it to use local virtual environments:

```powershell
poetry config virtualenvs.in-project true
```

This creates `.venv` in your project folder instead of a global location.

---

## Step 5: Install Backend Dependencies

Navigate to backend folder and install:

```powershell
cd backend
poetry install
```

Expected output:
```
Installing dependencies from lock file
...
Installing the current project: wedding-journal-backend (0.1.0)
...
✓ Done
```

This creates a `.venv` folder in backend/ with all dependencies.

---

## Complete Setup Commands (Copy & Paste)

Run these commands one by one:

```powershell
# 1. Upgrade pip
python -m pip install --upgrade pip

# 2. Install poetry
pip install poetry

# 3. Verify poetry works
poetry --version

# 4. Configure poetry for local venv
poetry config virtualenvs.in-project true

# 5. Go to backend folder
cd backend

# 6. Install dependencies
poetry install

# 7. Initialize database
poetry run alembic upgrade head

# 8. Start backend server
poetry run uvicorn app.main:app --reload
```

---

## Troubleshooting

### Still Getting "poetry not recognized"

**Solution 1: Check PATH**
```powershell
# See where poetry was installed
pip show poetry
# Look for "Location: C:\Users\...\AppData\Python\Scripts"

# That path should be in your System PATH
# If not, add it manually:
$env:Path += ";C:\Users\YourUsername\AppData\Python\Scripts"
```

**Solution 2: Restart PowerShell**
```powershell
# Close PowerShell completely
# Open a NEW PowerShell window as Administrator
# Try again: poetry --version
```

**Solution 3: Use Python Module Method**
```powershell
# Use this instead of 'poetry' command:
python -m poetry install
python -m poetry run alembic upgrade head
```

### Installation Takes Too Long

This is normal - it's downloading and installing 40+ packages. Let it finish (may take 2-5 minutes).

### Disk Space Issue

```
ERROR: Could not install packages
```

Make sure you have at least 1GB free disk space.

### Permission Denied

```
ERROR: Permission denied
```

Make sure PowerShell is running as Administrator.

---

## Verify Installation is Complete

After running `poetry install`, you should have:

```
backend/
├── .venv/                 # Virtual environment (created)
├── .venv/lib/
├── .venv/Scripts/
├── pyproject.toml
├── poetry.lock
└── app/
```

Check that `.venv` folder exists:
```powershell
ls .venv
# Should list: Include, Lib, Scripts, pyvenv.cfg
```

---

## Next Steps After Poetry Installation

```powershell
# 1. Create .env file
cd backend
cp .env.example .env

# 2. Edit .env with your cloud PostgreSQL URL
# (Open with Notepad or Visual Studio Code)
# DATABASE_URL=postgresql+asyncpg://...

# 3. Run migrations
poetry run alembic upgrade head

# 4. Start backend
poetry run uvicorn app.main:app --reload

# Backend will be running on http://localhost:8000
```

---

## If Everything Works

You should see:
```
✓ Poetry installed successfully
✓ Dependencies installed in .venv
✓ Backend folder ready
✓ Can run: poetry run alembic upgrade head
✓ Can run: poetry run uvicorn ...
```

---

## Quick Reference

| Command | What it does |
|---------|------------|
| `poetry --version` | Check if poetry is installed |
| `poetry install` | Install dependencies from pyproject.toml |
| `poetry update` | Update dependencies |
| `poetry add <package>` | Add new dependency |
| `poetry run <command>` | Run command in poetry environment |
| `poetry env list` | List environments |
| `poetry cache clear . --all` | Clear poetry cache |

---

## Support

If you still have issues:

1. **Verify Python:** `python --version` (should be 3.11+)
2. **Verify Pip:** `pip --version`
3. **Try Module Method:** `python -m poetry --version`
4. **Restart Computer:** Sometimes PATH updates need reboot
5. **Check Admin Mode:** Ensure PowerShell is running as Administrator

---

**After Poetry is installed, follow ADMIN_SETUP.md for the complete backend setup!**
