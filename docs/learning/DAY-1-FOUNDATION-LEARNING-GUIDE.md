# 📚 DAY 1: FOUNDATION - LEARNING GUIDE
**EclipseLink AI MVP Development**
**Date:** October 28, 2025
**Focus:** Backend setup, Frontend setup, Authentication, Database

---

## 🎯 TODAY'S LEARNING OBJECTIVES

By the end of today, you will understand:
1. ✅ Why we chose Python FastAPI over Node.js/Express
2. ✅ How FastAPI async works for AI API calls
3. ✅ Why React + Vite instead of Next.js
4. ✅ How Supabase Auth works (no custom JWT needed)
5. ✅ PostgreSQL schema design for healthcare data
6. ✅ Docker Compose for local development
7. ✅ HIPAA-compliant security basics

---

## 🏗️ ARCHITECTURE DECISIONS

### Decision 1: Python FastAPI (Backend)

**What we chose:** Python 3.11 + FastAPI 0.104

**Why we chose it:**
1. **Learning alignment:** You're pursuing Master's in AI/ML - Python is the AI language
2. **Async support:** FastAPI is built on async/await (crucial for OpenAI/Anthropic API calls)
3. **Auto-documentation:** FastAPI generates Swagger UI automatically at `/docs`
4. **Type safety:** Pydantic models catch bugs before runtime
5. **Fast enough:** Despite "Python is slow" myths, FastAPI is 2nd fastest web framework (behind Go)

**Alternatives we considered:**
- ❌ **Node.js + Express:** Faster initially but you want Python experience for AI/ML career
- ❌ **Django:** Too heavy for API-only backend (includes templating, ORM bloat)
- ❌ **Flask:** Older framework, lacks modern async support, no auto-docs

**Cost:** Free (open source)

**Key concepts you'll learn:**
```python
# Async/await for non-blocking AI API calls
async def process_handoff(audio_url: str):
    # This won't block other requests while waiting for AI
    transcript = await transcribe_with_whisper(audio_url)
    sbar = await generate_sbar_with_claude(transcript)
    return sbar

# Pydantic models for request validation
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr  # Validates email format automatically
    password: str    # Will add constraints (12-16 chars, etc.)
    role: UserRole   # Enum ensures valid role

    class Config:
        # This makes FastAPI generate better docs
        schema_extra = {
            "example": {
                "email": "sarah.rn@hospital.com",
                "password": "SecurePass2025!",
                "role": "RN"
            }
        }
```

### Decision 2: React + Vite (Frontend)

**What we chose:** React 18 + TypeScript + Vite

**Why we chose it:**
1. **React:** Industry standard (good for job applications, huge community)
2. **TypeScript:** Catches bugs before they reach users (type safety)
3. **Vite:** 10-20× faster than Create React App (instant hot reload)
4. **Bundle size:** Smaller than Next.js (faster loading for mobile clinicians)

**Why NOT Next.js:**
- ✅ Next.js is amazing for SEO/marketing sites
- ❌ EclipseLink is a web app (logged-in users), not a public website
- ❌ Next.js server components add complexity we don't need
- ❌ Larger bundle size (slower on hospital WiFi)
- ✅ Vite is simpler and perfect for SPAs (Single Page Applications)

**Key concepts you'll learn:**
```typescript
// React component with TypeScript
interface VoiceRecorderProps {
  patientId: string;
  onRecordingComplete: (audioBlob: Blob) => void;
  maxDuration?: number; // Optional, defaults to 300 seconds
}

const VoiceRecorder: React.FC<VoiceRecorderProps> = ({
  patientId,
  onRecordingComplete,
  maxDuration = 300
}) => {
  // TypeScript ensures you pass correct prop types
  // IDE autocomplete shows all available props
  return <div>...</div>
}

// Vite environment variables
console.log(import.meta.env.VITE_API_URL); // http://localhost:4000
// Note: Vite uses VITE_ prefix (not REACT_APP_ like CRA)
```

### Decision 3: Supabase (Database + Auth + Storage)

**What we chose:** Supabase (managed PostgreSQL + Auth + Storage)

**Why we chose it:**
1. **All-in-one:** Database, Auth, Storage in one service (less to manage)
2. **Free tier:** 50,000 users, 1GB storage, 2GB bandwidth (perfect for MVP)
3. **PostgreSQL:** Industry-standard relational database (HIPAA-friendly)
4. **Row-Level Security (RLS):** Built-in multi-tenancy (facility A can't see facility B's data)
5. **No custom auth code:** Email verification, password reset, JWT tokens all handled

**Alternatives we considered:**
- ❌ **AWS RDS + Cognito:** More powerful but $50+/month minimum, complex setup
- ❌ **Self-hosted PostgreSQL:** Free but requires DevOps knowledge
- ❌ **Firebase:** Great but NoSQL (healthcare needs relational data)

**Key concepts you'll learn:**
```sql
-- Row-Level Security (RLS) for HIPAA multi-tenancy
CREATE POLICY "Users can only access their facility's data"
ON handoffs
FOR SELECT
USING (
  facility_id = (
    SELECT facility_id
    FROM staff
    WHERE id = auth.uid()  -- Supabase magic: auth.uid() = current logged-in user
  )
);

-- This prevents cross-facility data leaks automatically!
-- Hospital A nurse can NEVER query Hospital B's handoffs
```

### Decision 4: Docker Compose (Development Environment)

**What we chose:** Docker + Docker Compose

**Why we chose it:**
1. **Consistency:** "Works on my machine" = "Works on everyone's machine"
2. **One command:** `docker-compose up` starts entire stack (backend, frontend, db, redis)
3. **Isolation:** Each project has its own environment (no Python version conflicts)
4. **Production-like:** Develop in same environment you'll deploy to

**Key concepts you'll learn:**
```yaml
# docker-compose.yml
version: '3.9'

services:
  backend:
    build: ./backend
    ports:
      - "4000:4000"  # localhost:4000 → container:4000
    environment:
      - DATABASE_URL=${DATABASE_URL}  # From .env file
    depends_on:
      - db  # Wait for database to start first

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:4000

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=changeme_dev_only
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Persist data

volumes:
  postgres_data:  # Named volume (survives container restart)
```

---

## 🔐 AUTHENTICATION ARCHITECTURE

### How Supabase Auth Works

```
┌────────────────────────────────────────────┐
│  User registers via React form             │
│  (email, password, role, facility)         │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│  Frontend: supabase.auth.signUp()          │
│  → Sends to Supabase Auth API              │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│  Supabase Auth Service:                    │
│  1. Hashes password (bcrypt)               │
│  2. Creates user in auth.users table       │
│  3. Sends verification email               │
│  4. Returns JWT token + refresh token      │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│  Frontend: Stores tokens in localStorage   │
│  Adds JWT to Authorization header:         │
│  Authorization: Bearer eyJhbGc...          │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│  Backend: Verifies JWT on each request     │
│  from supabase import create_client        │
│  user = supabase.auth.get_user(token)      │
│  if not user: return 401 Unauthorized      │
└────────────────────────────────────────────┘
```

**Key security features:**
- ✅ Passwords never stored in plain text (bcrypt hashed)
- ✅ JWT tokens expire after 1 hour (must refresh)
- ✅ Refresh tokens stored securely (HTTP-only cookies)
- ✅ Email verification required (prevents fake accounts)
- ✅ Rate limiting built-in (prevents brute force attacks)

### NIST 2025 Password Policy

**New password requirements** (changed from old 8+ char rules):
```python
from pydantic import validator

class UserCreate(BaseModel):
    password: str

    @validator('password')
    def validate_password(cls, v):
        # Length: 12-16 characters (NIST 2025 standard)
        if len(v) < 12 or len(v) > 16:
            raise ValueError('Password must be 12-16 characters')

        # Complexity: Mix of character types
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v)

        if not (has_upper and has_lower and has_digit and has_special):
            raise ValueError('Password must include uppercase, lowercase, number, and special character')

        # Check against common passwords (would load from file)
        COMMON_PASSWORDS = ['password123', 'admin123', ...]
        if v.lower() in COMMON_PASSWORDS:
            raise ValueError('Password is too common')

        return v
```

**Why these requirements:**
- 12-16 chars: Long enough to be secure, short enough to remember
- Complexity: Prevents simple dictionary attacks
- No common passwords: Prevents credential stuffing attacks
- Annual rotation: Reminders to update password yearly

---

## 🗄️ DATABASE SCHEMA DESIGN

### 12 Core Tables

**1. facilities** - Multi-tenancy foundation
```sql
CREATE TABLE facilities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  address TEXT,
  timezone VARCHAR(50) DEFAULT 'America/New_York',
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Example:
-- { id: "abc", name: "Memorial Hospital", timezone: "America/Denver" }
```

**2. users** - All 15 clinical roles
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  role user_role NOT NULL,  -- ENUM: RN, LPN, CNA, MD, etc.
  facility_id UUID REFERENCES facilities(id),
  is_active BOOLEAN DEFAULT true,
  email_verified BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_login_at TIMESTAMPTZ
);

-- Row-Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view users in their facility"
ON users FOR SELECT
USING (facility_id = (SELECT facility_id FROM users WHERE id = auth.uid()));
```

**3. patients** - Protected Health Information (PHI)
```sql
CREATE TABLE patients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mrn VARCHAR(50) NOT NULL,  -- Medical Record Number
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  date_of_birth DATE,
  room_number VARCHAR(20),
  admission_date DATE,
  primary_diagnosis TEXT,
  allergies TEXT[],  -- Array: ['Penicillin', 'Latex']
  primary_nurse_id UUID REFERENCES users(id),
  facility_id UUID REFERENCES facilities(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(mrn, facility_id)  -- MRN unique within facility
);

-- RLS: Only assigned staff can view patient
CREATE POLICY "Staff can view assigned patients"
ON patients FOR SELECT
USING (
  primary_nurse_id = auth.uid() OR
  facility_id = (SELECT facility_id FROM users WHERE id = auth.uid() AND role IN ('MD', 'Charge_Nurse', 'Admin'))
);
```

**4. handoffs** - Core product data
```sql
CREATE TABLE handoffs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,
  created_by_user_id UUID REFERENCES users(id),
  facility_id UUID REFERENCES facilities(id),

  -- Handoff type
  handoff_type VARCHAR(50) DEFAULT 'shift_change',
  is_baseline BOOLEAN DEFAULT false,
  baseline_handoff_id UUID REFERENCES handoffs(id),  -- NULL if this IS baseline

  -- Audio
  audio_url TEXT,
  audio_duration_seconds INTEGER,

  -- AI Processing
  transcript TEXT,
  sbar_situation TEXT,
  sbar_background TEXT,
  sbar_assessment TEXT,
  sbar_recommendation TEXT,

  -- Quality Metrics
  completeness_score INTEGER CHECK (completeness_score BETWEEN 0 AND 100),
  clarity_score INTEGER CHECK (clarity_score BETWEEN 0 AND 100),

  -- Status
  status VARCHAR(20) DEFAULT 'processing',  -- processing, completed, failed
  processing_started_at TIMESTAMPTZ,
  processing_completed_at TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX idx_handoffs_patient ON handoffs(patient_id, created_at DESC);
CREATE INDEX idx_handoffs_baseline ON handoffs(patient_id) WHERE is_baseline = true;
```

**5. handoff_changes** - Update-Only Model™ tracking
```sql
CREATE TABLE handoff_changes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  handoff_id UUID REFERENCES handoffs(id) ON DELETE CASCADE,
  field_name VARCHAR(100) NOT NULL,  -- 'pain_level', 'mobility', etc.
  old_value TEXT,
  new_value TEXT,
  change_type VARCHAR(20),  -- 'improvement', 'decline', 'stable', 'new'
  severity VARCHAR(20),  -- 'critical', 'warning', 'info'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Example:
-- { field: 'pain_level', old: '8/10', new: '4/10', type: 'improvement', severity: 'info' }
```

**6. rewards_points** - Phoenix & Peacock Honors™
```sql
CREATE TABLE rewards_points (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  points_earned INTEGER NOT NULL,
  activity_type VARCHAR(50) NOT NULL,  -- 'handoff_completed', 'update_only_used', etc.
  related_handoff_id UUID REFERENCES handoffs(id),
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Calculate total points
CREATE VIEW user_total_points AS
SELECT
  user_id,
  SUM(points_earned) as total_points,
  CASE
    WHEN SUM(points_earned) < 500 THEN 'Bronze'
    WHEN SUM(points_earned) < 2000 THEN 'Silver'
    WHEN SUM(points_earned) < 5000 THEN 'Gold'
    ELSE 'Platinum'
  END as tier
FROM rewards_points
GROUP BY user_id;
```

**7. audit_logs** - HIPAA compliance (7-year retention)
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  action VARCHAR(50) NOT NULL,  -- 'created', 'viewed', 'updated', 'deleted'
  resource_type VARCHAR(50) NOT NULL,  -- 'handoff', 'patient', 'user'
  resource_id UUID,
  ip_address INET,
  user_agent TEXT,
  request_payload JSONB,
  response_status INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Partition by year for efficient 7-year retention
CREATE TABLE audit_logs_2025 PARTITION OF audit_logs
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

**8-12. Additional tables** (same pattern):
- `handoff_assignments` - Who is assigned to receive handoff
- `notifications` - In-app notifications
- `ehr_connections` - EHR configuration (Epic, Cerner, etc.)
- `ehr_sync_logs` - EHR sync history
- `critical_alerts` - Detected critical alerts

---

## 🛠️ DEVELOPMENT WORKFLOW

### 1. Local Development Loop

```bash
# Terminal 1: Start all services
docker-compose up

# Terminal 2: Watch backend logs
docker-compose logs -f backend

# Terminal 3: Watch frontend logs
docker-compose logs -f frontend

# Make code changes → Auto-reloads!
# FastAPI: Uvicorn watches for file changes
# React: Vite HMR (Hot Module Replacement)
```

### 2. Database Migrations

```bash
# Generate migration from schema changes
alembic revision --autogenerate -m "Add handoff_changes table"

# Review generated migration
cat backend/alembic/versions/abc123_add_handoff_changes.py

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### 3. API Testing

```bash
# FastAPI auto-generates API docs
open http://localhost:4000/docs  # Swagger UI
open http://localhost:4000/redoc  # ReDoc

# Try API endpoints interactively in Swagger
# No Postman needed!
```

---

## 🔒 SECURITY CHECKLIST (HIPAA)

### What we implement today:

✅ **Authentication:**
- Email/password with secure hashing (bcrypt via Supabase)
- JWT tokens with expiration (1 hour)
- Refresh tokens (30 days)
- Email verification required

✅ **Authorization:**
- Role-Based Access Control (RBAC)
- Row-Level Security (RLS) in database
- Permission checks on every API endpoint

✅ **Input Validation:**
- Pydantic models validate all inputs
- SQL injection impossible (parameterized queries)
- XSS prevention (React escapes by default)

✅ **Audit Logging:**
- Log all data access (who viewed what, when)
- Log all mutations (create, update, delete)
- 7-year retention (HIPAA requirement)

✅ **Encryption:**
- HTTPS in production (TLS 1.3)
- Database encryption at rest (Supabase automatic)
- JWT tokens signed with secret key

### What we'll add later:

⏳ **MFA (Multi-Factor Authentication)** - Phase 2
⏳ **Session timeout** - 15 minutes of inactivity
⏳ **IP whitelisting** - Restrict access to hospital networks
⏳ **Penetration testing** - Before production launch

---

## 📦 PROJECT STRUCTURE

```
eclipselink-ai/
├── backend/                  # Python FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── config.py         # Settings (from .env)
│   │   ├── database.py       # Database connection
│   │   ├── auth.py           # Supabase auth wrapper
│   │   ├── models/           # Pydantic models (request/response)
│   │   ├── routes/           # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── handoffs.py
│   │   │   ├── patients.py
│   │   │   └── users.py
│   │   ├── services/         # Business logic
│   │   │   ├── whisper.py    # OpenAI transcription
│   │   │   ├── claude.py     # Anthropic SBAR generation
│   │   │   └── rewards.py    # Points calculation
│   │   └── utils/            # Helper functions
│   ├── alembic/              # Database migrations
│   ├── tests/                # Pytest tests
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                 # React + Vite
│   ├── src/
│   │   ├── main.tsx          # React entry point
│   │   ├── App.tsx           # Root component
│   │   ├── components/       # Reusable UI components
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   ├── handoffs/
│   │   │   └── shared/
│   │   ├── pages/            # Page components (routes)
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   └── HandoffDetail.tsx
│   │   ├── hooks/            # Custom React hooks
│   │   ├── services/         # API client
│   │   │   └── api.ts
│   │   ├── store/            # State management (Zustand)
│   │   ├── types/            # TypeScript types
│   │   └── styles/           # CSS (Tailwind)
│   ├── public/               # Static assets
│   │   ├── rohimaya-logo-circle.png
│   │   └── rohimaya-banner.png
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .env.example
│
├── database/
│   ├── schema.sql            # Complete database schema
│   ├── seed-data.sql         # Sample data for demo
│   └── migrations/           # SQL migrations
│
├── docs/
│   ├── learning/             # Educational docs (this!)
│   └── architecture/         # Diagrams, ADRs
│
├── docker-compose.yml        # Orchestrates all services
└── README.md                 # Setup instructions
```

---

## 🎓 KEY TAKEAWAYS

### 1. Async is Essential for AI APIs
```python
# ❌ BAD: Synchronous (blocks other requests)
def process_handoff(audio_url):
    transcript = requests.post(whisper_api, audio_url)  # Waits 20 seconds
    sbar = requests.post(claude_api, transcript)  # Waits 15 seconds
    return sbar  # Total: 35 seconds of blocking

# ✅ GOOD: Asynchronous (non-blocking)
async def process_handoff(audio_url):
    transcript = await async_whisper_call(audio_url)  # Other requests run meanwhile
    sbar = await async_claude_call(transcript)
    return sbar
```

### 2. TypeScript Catches Bugs Early
```typescript
// ❌ JavaScript: No error until runtime
const user = { name: "Sarah", role: "RN" };
console.log(user.roleee);  // undefined (typo not caught)

// ✅ TypeScript: Error at compile time
interface User {
  name: string;
  role: string;
}
const user: User = { name: "Sarah", role: "RN" };
console.log(user.roleee);  // TS Error: Property 'roleee' does not exist
```

### 3. RLS is Multi-Tenancy Magic
```sql
-- Without RLS: You must remember to filter everywhere
SELECT * FROM patients WHERE facility_id = current_user_facility; -- Easy to forget!

-- With RLS: Database enforces automatically
SELECT * FROM patients;  -- Only returns patients from YOUR facility
-- Even if you forget to filter, RLS protects you
```

---

## 📚 RESOURCES FOR DEEPER LEARNING

**FastAPI:**
- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/
- Async Guide: https://fastapi.tiangolo.com/async/

**React + Vite:**
- React Docs: https://react.dev/
- Vite Guide: https://vitejs.dev/guide/
- TypeScript Handbook: https://www.typescriptlang.org/docs/

**Supabase:**
- Supabase Docs: https://supabase.com/docs
- Row-Level Security: https://supabase.com/docs/guides/auth/row-level-security
- Auth Guide: https://supabase.com/docs/guides/auth

**HIPAA Compliance:**
- HIPAA Security Rule: https://www.hhs.gov/hipaa/for-professionals/security/
- Audit Log Requirements: https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/

---

## ✅ SUCCESS CRITERIA FOR TODAY

By end of Day 1, you should be able to:
1. ✅ Run `docker-compose up` and see all services start
2. ✅ Open http://localhost:4000/docs and see API documentation
3. ✅ Open http://localhost:3000 and see login page
4. ✅ Register a new user (RN role) and receive verification email
5. ✅ Login and land on empty dashboard
6. ✅ See audit log entry for login action
7. ✅ Understand WHY we made each technology choice

---

**Next:** Day 2 - Voice Recording & AI Integration

*Keep this document open as reference while building! 📖*
