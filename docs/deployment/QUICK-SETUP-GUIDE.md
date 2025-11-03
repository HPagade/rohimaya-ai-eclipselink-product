# 🚀 Quick Setup Guide for EclipseLink AI MVP

This guide will help you configure all required external services to run the MVP.

**Time to complete**: ~30-45 minutes
**Cost**: ~$0 for initial testing (all services have free tiers)

---

## ✅ Prerequisites

- GitHub/GitLab account
- Credit card (required for Azure, can use free credits)
- Terminal access with Node.js 18+ installed

---

## 📋 Setup Checklist

| Service | Purpose | Time | Status |
|---------|---------|------|--------|
| Supabase | PostgreSQL Database | 5 min | ⬜ |
| Azure OpenAI | Whisper + GPT-4 | 10 min | ⬜ |
| Cloudflare R2 | Voice Storage | 5 min | ⬜ |
| Upstash Redis | Job Queue | 5 min | ⬜ |
| Environment Setup | Configuration | 10 min | ⬜ |

---

## 1️⃣ Supabase (PostgreSQL Database)

### Setup Steps

1. **Sign up**: Go to https://supabase.com and create account
2. **Create project**:
   - Click "New Project"
   - Name: `eclipselink-mvp`
   - Database Password: Generate strong password (save it!)
   - Region: Choose closest to your users
   - Click "Create new project" (takes ~2 minutes)

3. **Get credentials**:
   - Go to Settings → Database
   - Copy **Connection String** (Connection pooling → URI)
   - Example: `postgresql://postgres.xxx:password@aws-0-us-east-1.pooler.supabase.com:5432/postgres`

4. **Get API keys**:
   - Go to Settings → API
   - Copy **Project URL** (e.g., `https://xxx.supabase.co`)
   - Copy **anon public** key
   - Copy **service_role** key (secret!)

### Environment Variables

```bash
DATABASE_URL=postgresql://postgres.xxx:[PASSWORD]@[HOST]:5432/postgres
SUPABASE_URL=https://[PROJECT-ID].supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Run Database Migrations

```bash
export DATABASE_URL="your-connection-string-here"
cd database
bash setup.sh
```

This creates all 15 tables, indexes, RLS policies, and triggers.

---

## 2️⃣ Azure OpenAI (Whisper + GPT-4)

### Setup Steps

1. **Sign up**: Go to https://portal.azure.com
   - Create free account ($200 credit for 30 days)

2. **Create Azure OpenAI resource**:
   - Search for "Azure OpenAI"
   - Click "Create"
   - Resource group: Create new (e.g., `eclipselink-rg`)
   - Region: **East US** (has best availability)
   - Name: `eclipselink-openai`
   - Pricing tier: Standard S0
   - Click "Review + create"

3. **Deploy models** (CRITICAL):
   - Go to your resource → Azure OpenAI Studio
   - Click "Deployments" → "Create new deployment"

   **Deploy Whisper:**
   - Model: `whisper`
   - Deployment name: `whisper` (exact name!)
   - Click "Create"

   **Deploy GPT-4:**
   - Model: `gpt-4` or `gpt-4-32k` (if available)
   - Deployment name: `gpt-4` (exact name!)
   - Click "Create"

4. **Get credentials**:
   - Go to resource → Keys and Endpoint
   - Copy **KEY 1**
   - Copy **Endpoint** (e.g., `https://eclipselink-openai.openai.azure.com/`)

### Environment Variables

```bash
AZURE_OPENAI_KEY=abc123def456...
AZURE_OPENAI_ENDPOINT=https://[YOUR-RESOURCE].openai.azure.com
AZURE_OPENAI_API_VERSION=2024-02-15-preview
WHISPER_DEPLOYMENT_NAME=whisper
GPT4_DEPLOYMENT_NAME=gpt-4
```

### Pricing

- **Whisper**: $0.006 per minute (~$0.02 per handoff for 3min audio)
- **GPT-4**: $0.03/1K input + $0.06/1K output (~$0.07 per handoff)
- **Total**: ~$0.09 per handoff
- **Free tier**: $200 credit = ~2,200 handoffs

---

## 3️⃣ Cloudflare R2 (Voice Storage)

### Setup Steps

1. **Sign up**: Go to https://dash.cloudflare.com
   - Create free account (no credit card for R2!)

2. **Create R2 bucket**:
   - Go to R2 Object Storage (left sidebar)
   - Click "Create bucket"
   - Name: `eclipselink-production`
   - Location: Automatic
   - Click "Create bucket"

3. **Create API token**:
   - Go to R2 → Manage R2 API Tokens
   - Click "Create API token"
   - Token name: `eclipselink-backend`
   - Permissions: Object Read & Write
   - Click "Create API token"
   - **SAVE** the Access Key ID and Secret Access Key!

4. **Get Account ID**:
   - Visible in R2 dashboard (top right)
   - Example: `abc123def456...`

### Environment Variables

```bash
R2_ACCOUNT_ID=your-account-id
R2_ACCESS_KEY_ID=your-access-key-id
R2_SECRET_ACCESS_KEY=your-secret-access-key
R2_BUCKET_NAME=eclipselink-production
R2_PUBLIC_URL=https://eclipselink-production.[YOUR-ACCOUNT-ID].r2.cloudflarestorage.com
```

### Pricing

- **Free tier**: 10 GB storage, 1 million Class A operations/month
- **Paid**: $0.015/GB/month (VERY cheap!)
- **Typical usage**: 100 handoffs/day × 2MB/audio = 6GB/month = $0.09/month

---

## 4️⃣ Upstash Redis (Job Queue)

### Setup Steps

1. **Sign up**: Go to https://console.upstash.com
   - Create free account

2. **Create Redis database**:
   - Click "Create database"
   - Name: `eclipselink-queue`
   - Type: Regional
   - Region: Choose closest to you
   - TLS: Enabled
   - Click "Create"

3. **Get credentials**:
   - Click on your database
   - Copy **Endpoint** (e.g., `us1-xxx.upstash.io`)
   - Copy **Password**
   - Note **Port** (usually 6379)

### Environment Variables

```bash
REDIS_HOST=us1-xxx.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
REDIS_URL=redis://default:[PASSWORD]@[ENDPOINT].upstash.io:6379
```

### Pricing

- **Free tier**: 10,000 commands/day
- **Typical usage**: 100 handoffs/day × 20 commands = 2,000 commands/day
- **Cost**: FREE for MVP testing

---

## 5️⃣ Environment Configuration

### Create .env Files

```bash
# Backend
cp .env.example apps/backend/.env

# Frontend
cp .env.example apps/frontend/.env.local
```

### Complete Backend .env

Edit `apps/backend/.env` with all credentials from above:

```bash
# Database (Supabase)
DATABASE_URL=postgresql://...
SUPABASE_URL=https://...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_KEY=...

# Azure OpenAI
AZURE_OPENAI_KEY=...
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_API_VERSION=2024-02-15-preview
WHISPER_DEPLOYMENT_NAME=whisper
GPT4_DEPLOYMENT_NAME=gpt-4

# Cloudflare R2
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=eclipselink-production
R2_PUBLIC_URL=https://...

# Redis (Upstash)
REDIS_HOST=...
REDIS_PORT=6379
REDIS_PASSWORD=...
REDIS_URL=redis://...

# JWT (Generate secure secret)
JWT_SECRET=$(openssl rand -base64 32)
JWT_EXPIRES_IN=1h
JWT_REFRESH_EXPIRES_IN=30d

# App Config
NODE_ENV=development
PORT=4000
FRONTEND_URL=http://localhost:3000
```

### Complete Frontend .env.local

Edit `apps/frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:4000
NEXT_PUBLIC_SUPABASE_URL=https://[PROJECT].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
```

---

## 6️⃣ Install Dependencies & Start

### Install

```bash
npm install
```

### Run Database Migrations

```bash
cd database
export DATABASE_URL="your-supabase-connection-string"
bash setup.sh
```

### Start Development

**Terminal 1 - Backend:**
```bash
cd apps/backend
npm run dev
```

**Terminal 2 - Workers:**
```bash
cd apps/backend
# Start both workers
npm run worker:transcription &
npm run worker:sbar &
```

**Terminal 3 - Frontend:**
```bash
cd apps/frontend
npm run dev
```

### Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:4000
- **API Health**: http://localhost:4000/health

---

## 🧪 Test the MVP

### Quick Test Flow

1. **Register**: http://localhost:3000/register
   - Email: test@hospital.com
   - Password: Test123!
   - First/Last Name
   - Role: Registered Nurse

2. **Create Handoff**:
   - POST http://localhost:4000/v1/handoffs
   - Body: `{ patientId, fromStaffId, handoffType: "shift_change" }`

3. **Upload Voice**:
   - POST http://localhost:4000/v1/voice/upload
   - Form data: audio file + handoffId

4. **Watch Processing**:
   - Check worker logs
   - GET http://localhost:4000/v1/voice/:id/status

5. **View SBAR**:
   - GET http://localhost:4000/v1/sbar/:handoffId

---

## 🐛 Troubleshooting

### Database connection fails
```bash
# Test connection
psql "$DATABASE_URL"

# Check .env file is loaded
echo $DATABASE_URL
```

### Azure OpenAI errors
- Verify deployment names match exactly (`whisper`, `gpt-4`)
- Check region has quota for models
- Verify API key is correct

### Redis connection fails
```bash
# Test Redis connection
redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD ping
```

### Workers not processing
- Check Redis connection
- Verify environment variables loaded
- Check worker logs for errors

---

## 📊 Monitoring

### Check Service Health

```bash
# Database
curl http://localhost:4000/health

# Check database tables
psql "$DATABASE_URL" -c "\dt"

# Check Redis queue
redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD KEYS "*"
```

### View Logs

```bash
# Backend logs
cd apps/backend && npm run dev

# Worker logs
cd apps/backend && npm run worker:transcription
```

---

## 💰 Cost Estimation

### Development (100 handoffs/day)

| Service | Monthly Cost |
|---------|--------------|
| Supabase | **FREE** (< 500MB) |
| Azure OpenAI | **$9** (100 × $0.09) |
| Cloudflare R2 | **$0.09** (6GB storage) |
| Upstash Redis | **FREE** (< 10K commands/day) |
| **TOTAL** | **~$9/month** |

### Production (1,000 handoffs/day)

| Service | Monthly Cost |
|---------|--------------|
| Supabase | **$25** (Pro plan) |
| Azure OpenAI | **$2,700** (1K × 30 × $0.09) |
| Cloudflare R2 | **$0.90** (60GB storage) |
| Upstash Redis | **$10** (Pay-as-you-go) |
| **TOTAL** | **~$2,736/month** |

**Note**: Azure OpenAI is 99% of production cost. Consider:
- Caching common transcriptions
- Batch processing
- Reserved capacity discounts

---

## ✅ Success Checklist

- [ ] Supabase project created and database migrated
- [ ] Azure OpenAI resource with Whisper + GPT-4 deployed
- [ ] Cloudflare R2 bucket created with API token
- [ ] Upstash Redis database created
- [ ] Environment variables configured in `.env` files
- [ ] `npm install` completed successfully
- [ ] Database migrations ran successfully
- [ ] Backend starts without errors
- [ ] Workers start and connect to Redis
- [ ] Frontend starts and connects to backend
- [ ] Can register user account
- [ ] Can create handoff
- [ ] Can upload voice recording
- [ ] Workers process transcription
- [ ] SBAR report generates successfully

---

## 🎉 Next Steps

Once setup is complete:

1. **Test Complete Flow**: Create handoff → Upload voice → View SBAR
2. **Create Test Patients**: Seed database with realistic patient data
3. **Implement SBAR Controller**: View and manage SBAR reports
4. **Add Patient Controller**: Search and view patient history
5. **Deploy to Staging**: Railway.app + Cloudflare Pages

---

## 📚 Additional Resources

- **Supabase Docs**: https://supabase.com/docs
- **Azure OpenAI Docs**: https://learn.microsoft.com/azure/ai-services/openai/
- **Cloudflare R2 Docs**: https://developers.cloudflare.com/r2/
- **Upstash Docs**: https://docs.upstash.com/redis
- **BullMQ Docs**: https://docs.bullmq.io/

---

**Questions?** Check the main README.md or create an issue in the repository.

**Need help?** All services have excellent support documentation and communities.

🚀 **Happy building!**
