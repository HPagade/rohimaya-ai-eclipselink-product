# EclipseLink AI - Local Development Setup

Complete guide to get EclipseLink AI running on your local machine.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Backend Setup (Python FastAPI)](#backend-setup)
4. [Frontend Setup (React + Vite)](#frontend-setup)
5. [Testing the System](#testing-the-system)
6. [Adding Real API Keys](#adding-real-api-keys)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Make sure you have these installed:

### Required Software
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
  ```bash
  python3 --version  # Should show 3.11 or higher
  ```

- **Node.js 20+** ([Download](https://nodejs.org/))
  ```bash
  node --version  # Should show v20.x or higher
  npm --version
  ```

- **PostgreSQL 15+** ([Download](https://www.postgresql.org/download/))
  ```bash
  psql --version  # Should show 15.x or higher
  ```

- **Git** (already installed if you cloned this repo)

### Optional but Recommended
- **pgAdmin** - GUI for PostgreSQL database management
- **Postman** or **Insomnia** - For testing API endpoints
- **VS Code** - Recommended code editor

---

## Database Setup

### Step 1: Start PostgreSQL
Make sure PostgreSQL is running:

```bash
# macOS (if installed via Homebrew)
brew services start postgresql@15

# Linux
sudo systemctl start postgresql

# Windows
# Start PostgreSQL from Services or pgAdmin
```

### Step 2: Create Database
```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# Inside psql prompt:
CREATE DATABASE eclipselink;
CREATE USER eclipselink_user WITH PASSWORD 'dev_password_2025';
GRANT ALL PRIVILEGES ON DATABASE eclipselink TO eclipselink_user;

# Exit psql
\q
```

### Step 3: Run Schema SQL
```bash
# From project root directory
psql -U eclipselink_user -d eclipselink -f database/schema.sql
```

You should see output like:
```
CREATE TABLE
CREATE TABLE
...
Schema created successfully!
```

### Step 4: Load Seed Data
```bash
psql -U eclipselink_user -d eclipselink -f database/seed-data.sql
```

You should see:
```
Seed data loaded successfully!
5 users created (password: DemoPass2025!)
Login as: nurse.sarah@demohospital.com
```

### Step 5: Verify Database
```bash
psql -U eclipselink_user -d eclipselink -c "SELECT COUNT(*) FROM patients;"
```

Should show: `5` patients

---

## Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd apps/backend
```

### Step 2: Create Python Virtual Environment
```bash
# Create venv
python3 -m venv venv

# Activate venv
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- FastAPI, Uvicorn (web server)
- SQLAlchemy, psycopg2 (database)
- Pydantic (validation)
- python-multipart (file uploads)
- OpenAI, Anthropic SDKs (for AI, optional for now)
- And more...

### Step 4: Configure Environment Variables
Create `.env` file in `apps/backend/`:

```bash
# Copy from example
cp .env.example .env

# Edit .env with your values
nano .env  # or use any text editor
```

**Minimum configuration for testing with MOCKS:**
```env
# Database
DATABASE_URL=postgresql://eclipselink_user:dev_password_2025@localhost:5432/eclipselink

# Server
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development

# JWT Secret (generate with: openssl rand -hex 32)
JWT_SECRET_KEY=your-secret-key-here-generate-a-real-one

# AI Keys - Leave as placeholders to use MOCKS
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

> **Note**: With placeholder API keys, the system will use **mock AI responses**. This is perfect for testing! See [Adding Real API Keys](#adding-real-api-keys) when you're ready.

### Step 5: Run Database Migrations
```bash
# From apps/backend with venv activated
alembic upgrade head
```

### Step 6: Start Backend Server
```bash
# From apps/backend with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
⚠️  OpenAI API key not configured - using MOCK transcription
⚠️  Anthropic API key not configured - using MOCK SBAR generation
✓ Database connected successfully
```

**Test it**: Open http://localhost:8000/docs in your browser. You should see the FastAPI interactive API documentation (Swagger UI).

---

## Frontend Setup

Open a **new terminal** (keep backend running in the first terminal).

### Step 1: Navigate to Frontend Directory
```bash
cd apps/frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

This will install:
- React 18, React Router
- Vite (build tool)
- TailwindCSS (styling)
- Zustand (state management)
- Axios (HTTP client)
- And more...

### Step 3: Configure Environment Variables
Create `.env` file in `apps/frontend/`:

```bash
# Copy from example (if it exists)
cp .env.example .env || touch .env

# Edit .env
nano .env
```

**Configuration:**
```env
VITE_API_URL=http://localhost:8000/api
VITE_ENVIRONMENT=development
```

### Step 4: Start Frontend Dev Server
```bash
npm run dev
```

You should see:
```
  VITE v5.4.21  ready in 450 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Test it**: Open http://localhost:5173 in your browser. You should see the EclipseLink AI login page!

---

## Testing the System

Now you have both backend (port 8000) and frontend (port 5173) running!

### Test 1: Login
1. Go to http://localhost:5173/login
2. **Email**: `nurse.sarah@demohospital.com`
3. **Password**: `DemoPass2025!`
4. Click "Sign In"

You should be redirected to the dashboard!

### Test 2: View Patients
- Navigate to "Patients" from the dashboard
- You should see 5 demo patients (Sarah Johnson, Michael Chen, etc.)

### Test 3: Create Handoff (The Big Test!)

1. Click **"Create Handoff"** from dashboard
2. **Select Patient**: Click on "Sarah Johnson" (she has no baseline yet, so you'll get 10 points!)
3. **Record Voice**:
   - Click "Start Recording"
   - Grant microphone permission when prompted
   - Speak for 10-20 seconds (anything works - it's using mock AI)
   - Click "Stop & Save"

4. **Watch Processing**:
   - You'll see animated progress: "Uploading... Transcribing... Generating SBAR..."
   - This uses **MOCK AI** so it will complete in ~5 seconds

5. **View Results**:
   - See the AI-generated SBAR (4 sections)
   - See the transcript
   - See points earned (+10 for baseline!)
   - Export or print the handoff

### Test 4: Create Update Handoff
1. Go back to "Create Handoff"
2. Select **Michael Chen** (he already has a baseline from seed data)
3. Notice the badge says "Update (5 pts)" instead of "Baseline (10 pts)"
4. Record another voice note
5. This time you'll earn 5 points instead of 10!

### Test 5: Check API Directly
- Open http://localhost:8000/docs
- Click on **GET /api/patients**
- Click "Try it out" → "Execute"
- You should see JSON with all 5 patients

---

## Adding Real API Keys

When you're ready to use **real AI** instead of mocks:

### Step 1: Get API Keys

**OpenAI (for Whisper transcription):**
1. Go to https://platform.openai.com/api-keys
2. Create account or login
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

**Anthropic (for Claude SBAR generation):**
1. Go to https://console.anthropic.com/
2. Create account or login
3. Go to "API Keys" section
4. Create new key
5. Copy the key (starts with `sk-ant-...`)

### Step 2: Update Backend .env
Edit `apps/backend/.env`:

```env
# Replace placeholder values
OPENAI_API_KEY=sk-proj-your-real-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-real-anthropic-key-here
```

### Step 3: Restart Backend
```bash
# Stop backend (Ctrl+C in backend terminal)
# Start it again:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Now you should see:
```
✓ OpenAI Whisper API configured
✓ Anthropic Claude API configured
```

### Cost Estimates
- **Whisper**: ~$0.006 per minute of audio ($0.36 for 60 recordings)
- **Claude Sonnet**: ~$0.003 per request ($0.18 for 60 SBARs)
- **Total**: ~$0.009 per handoff = **$0.54 for 60 handoffs**

Monthly cost for moderate usage: **~$10-20/month** (well under your $100 budget!)

---

## Troubleshooting

### Database Connection Errors

**Error**: `psycopg2.OperationalError: could not connect to server`

**Fix**:
```bash
# Make sure PostgreSQL is running
brew services list | grep postgresql  # macOS
sudo systemctl status postgresql      # Linux

# Check if database exists
psql -U postgres -l | grep eclipselink
```

### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Fix**:
```bash
# Make sure venv is activated
source venv/bin/activate  # You should see (venv) in prompt

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Build Errors

**Error**: `Cannot find module '@/components/...'`

**Fix**:
```bash
# Delete node_modules and reinstall
cd apps/frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors in Browser

**Error**: `Access to fetch at 'http://localhost:8000' blocked by CORS policy`

**Fix**: Make sure `apps/backend/.env` has:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

Then restart backend server.

### Microphone Permission Denied

**Error**: "Unable to access microphone. Please grant permission."

**Fix**:
1. **Chrome/Edge**: Click the lock icon in address bar → Site settings → Microphone → Allow
2. **Firefox**: Click the shield icon → Permissions → Microphone → Allow
3. **Safari**: Safari menu → Settings for This Website → Microphone → Allow

### Port Already in Use

**Error**: `ERROR:    [Errno 48] Address already in use`

**Fix**:
```bash
# Backend (port 8000)
lsof -ti:8000 | xargs kill -9

# Frontend (port 5173)
lsof -ti:5173 | xargs kill -9
```

### Mock AI Not Working

**Symptom**: Processing hangs or errors out even with placeholder keys

**Fix**: Check backend logs. Mock AI has built-in delays:
- Transcription: 2 seconds
- SBAR generation: 3 seconds

If it's taking longer, there may be a real error. Check terminal for stack traces.

---

## Next Steps

Congratulations! You now have EclipseLink AI running locally with:
- ✅ PostgreSQL database with seed data
- ✅ FastAPI backend with mock AI
- ✅ React frontend with voice recording
- ✅ Complete handoff flow working end-to-end

**What to explore next:**
1. Read `docs/learning/DAY-2-AI-INTEGRATION-GUIDE.md` to understand how the AI works
2. Try creating multiple handoffs to see the points system
3. Add real API keys when ready to test actual AI
4. Customize the SBAR prompt in `apps/backend/app/services/ai_service.py`

**Questions?** Check the learning guides in `docs/learning/` or review the code comments!

---

## Quick Reference

### Start Everything (After Initial Setup)

```bash
# Terminal 1: Database
brew services start postgresql@15

# Terminal 2: Backend
cd apps/backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 3: Frontend
cd apps/frontend
npm run dev
```

Then open http://localhost:5173 and login with:
- **Email**: nurse.sarah@demohospital.com
- **Password**: DemoPass2025!

### Stop Everything

```bash
# Stop backend: Ctrl+C in Terminal 2
# Stop frontend: Ctrl+C in Terminal 3
# Stop database (optional):
brew services stop postgresql@15
```

---

**Happy coding!** 🚀
