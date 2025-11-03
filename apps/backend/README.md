# EclipseLink AI Backend

## ⚠️ IMPORTANT: ARCHITECTURE CLARIFICATION

This repository contains **TWO backend implementations**. Please read carefully to understand which one to use.

---

## 🟢 CURRENT PRODUCTION ARCHITECTURE (USE THIS)

**Supabase Edge Functions + PostgreSQL**
- **Technology:** Deno/TypeScript serverless functions
- **Location:** Documented in `COMPLETE-DEPLOYMENT-GUIDE.md` (root directory)
- **Deployment:** `supabase functions deploy`
- **Status:** ✅ **Production Ready** - Use this for deployment

### Key Features:
- Serverless Edge Functions (Deno runtime)
- Built-in authentication via Supabase Auth
- Real-time subscriptions via WebSocket
- Row-Level Security (RLS) for data isolation
- $0 hosting cost (Supabase free tier)

### Edge Functions:
1. **process-handoff** - Transcribes audio with Whisper, generates SBAR with Claude
2. **generate-qr-code** - Creates QR codes for family access
3. **validate-family-access** - Token-based authentication for families

### Files to Deploy:
```bash
# Create functions
supabase functions new process-handoff
supabase functions new generate-qr-code

# Deploy
supabase functions deploy process-handoff
supabase functions deploy generate-qr-code
```

**See:** `COMPLETE-DEPLOYMENT-GUIDE.md` for full deployment instructions

---

## 🔵 REFERENCE IMPLEMENTATION (DO NOT DEPLOY)

**FastAPI + Python Backend**
- **Technology:** Python/FastAPI
- **Location:** `apps/backend/app/` directory
- **Status:** 🟡 **Reference Only** - Demonstrates SOLID design principles

### Purpose:
This FastAPI implementation was created to demonstrate:
- ✅ SOLID design principles in Python
- ✅ Clean architecture patterns
- ✅ Type-safe Pydantic models
- ✅ Dependency Inversion with service providers
- ✅ Comprehensive business logic implementation

### Key Files (Reference):
- `app/models.py` - Pydantic models (30+ models)
- `app/services/ai_service.py` - AI integration with Whisper + Claude
- `app/services/auth_service.py` - JWT authentication
- `app/core/config.py` - Configuration management
- `app/api/` - RESTful API endpoints

### Why Not Used in Production?
While this FastAPI backend is well-architected, we chose Supabase Edge Functions for production because:
- **Cost:** $0/month vs. $50-200/month for FastAPI hosting
- **Scalability:** Serverless auto-scaling vs. manual server management
- **Simplicity:** Integrated auth/database vs. separate services
- **Speed:** Edge deployment (250ms cold start) vs. container deployment

---

## 📖 Which One Should I Use?

| Scenario | Use This |
|----------|----------|
| **Deploying to production** | ✅ Supabase Edge Functions |
| **Running 15-user pilot** | ✅ Supabase Edge Functions |
| **Learning SOLID principles** | 🔵 FastAPI (reference) |
| **Understanding business logic** | 🔵 FastAPI (reference) |
| **Cost optimization** | ✅ Supabase Edge Functions |
| **Quick deployment (30 min)** | ✅ Supabase Edge Functions |

---

## 🚀 Quick Start (Production)

### 1. Set Up Supabase
```bash
# Install Supabase CLI
brew install supabase/tap/supabase  # macOS
# OR
scoop install supabase  # Windows

# Login and link project
supabase login
supabase link --project-ref YOUR_PROJECT_REF
```

### 2. Deploy Database Schema
```bash
# In Supabase Dashboard → SQL Editor, run:
# 1. database/schema-creative-production.sql
# 2. database/SCHEMA-FIXES.sql
```

### 3. Deploy Edge Functions
```bash
# Set environment variables
supabase secrets set OPENAI_API_KEY=sk-xxx
supabase secrets set ANTHROPIC_API_KEY=sk-ant-xxx

# Deploy functions
supabase functions deploy process-handoff
supabase functions deploy generate-qr-code
```

### 4. Deploy Frontend
```bash
cd apps/frontend
vercel --prod
```

**Full instructions:** See `COMPLETE-DEPLOYMENT-GUIDE.md`

---

## 🔧 Development

### Testing Edge Functions Locally
```bash
# Start local Supabase
supabase start

# Serve function locally
supabase functions serve process-handoff

# Test with curl
curl -i --location --request POST 'http://localhost:54321/functions/v1/process-handoff' \
  --header 'Authorization: Bearer YOUR_ANON_KEY' \
  --header 'Content-Type: application/json' \
  --data '{"handoff_id":"uuid-here"}'
```

### Testing FastAPI (Reference)
```bash
cd apps/backend

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload

# Visit: http://localhost:8000/docs
```

---

## 📚 Documentation

- **Production Architecture:** `COMPLETE-DEPLOYMENT-GUIDE.md`
- **Database Schema:** `database/schema-creative-production.sql`
- **Schema Fixes:** `database/SCHEMA-FIXES.sql`
- **Error Report:** `ERROR-REPORT-AND-FIXES.md`
- **Implementation Guide:** `IMPLEMENTATION-COMPLETE.md`
- **Creative Features:** `CREATIVE-PRODUCTION-GUIDE.md`

---

## 💡 Architecture Decision

**Decision Date:** October 2024
**Decision:** Use Supabase Edge Functions over FastAPI for production

**Reasoning:**
1. **Cost:** $21/month total vs. $200+/month with FastAPI
2. **Speed:** 30-minute deployment vs. 2-3 hours
3. **Maintenance:** Serverless (no servers to manage)
4. **Scaling:** Automatic vs. manual infrastructure
5. **Integration:** Built-in auth, storage, database, real-time

**Trade-offs Accepted:**
- Less Python code (Deno/TypeScript instead)
- Vendor lock-in to Supabase (mitigated by PostgreSQL compatibility)
- Cold start latency (250ms - acceptable for healthcare use case)

**Reference Implementation Kept Because:**
- Demonstrates SOLID principles for team learning
- Shows clean architecture patterns
- Provides business logic reference
- Useful for interviews/code reviews

---

## 🤝 Contributing

When contributing to backend logic:
1. **Update Edge Functions** for production changes
2. **Update FastAPI reference** to maintain consistency
3. **Document both** to show architectural evolution
4. **Test Edge Functions** before deploying

---

## 📞 Questions?

- **Deployment issues:** See `ERROR-REPORT-AND-FIXES.md`
- **Architecture questions:** See `CREATIVE-PRODUCTION-GUIDE.md`
- **Testing procedures:** See `COMPLETE-DEPLOYMENT-GUIDE.md` Phase 4

---

**Last Updated:** November 2024
**Status:** Production Ready (Supabase), Reference Only (FastAPI)
**Deployment Readiness:** 77% (after applying SCHEMA-FIXES.sql)
