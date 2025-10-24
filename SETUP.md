# EclipseLink AI™ - Complete Setup Guide

Welcome to EclipseLink AI™! This guide will help you get the complete application running locally.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18.0.0 or higher)
- **npm** (v9.0.0 or higher)
- **PostgreSQL** (v14 or higher) OR a Supabase account
- **Redis** (v6 or higher) OR an Upstash Redis account
- **Azure OpenAI** account with Whisper and GPT-4 deployments
- **Cloudflare** account for R2 storage

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/HPagade/rohimaya-ai-eclipselink-product.git
cd rohimaya-ai-eclipselink-product
```

### 2. Install Dependencies

```bash
npm install
```

This will install dependencies for the entire monorepo (frontend, backend, and shared packages).

### 3. Set Up the Database

#### Option A: Using Local PostgreSQL

```bash
# Create the database
createdb eclipselink_dev

# Run the schema migration
psql eclipselink_dev < database/schema.sql

# Seed with test data
psql eclipselink_dev < database/seed.sql
```

#### Option B: Using Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Copy your database connection string
3. Run the migrations:
   ```bash
   psql "your-supabase-connection-string" < database/schema.sql
   psql "your-supabase-connection-string" < database/seed.sql
   ```

### 4. Configure Environment Variables

#### Backend Configuration

```bash
cd apps/backend
cp .env.example .env
```

Edit `apps/backend/.env` with your values:

```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/eclipselink_dev

# JWT Secrets (generate secure random strings)
JWT_SECRET=$(openssl rand -base64 32)
REFRESH_TOKEN_SECRET=$(openssl rand -base64 32)

# Azure OpenAI (from your Azure portal)
AZURE_OPENAI_API_KEY=your_actual_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_WHISPER_DEPLOYMENT=your-whisper-deployment
AZURE_OPENAI_GPT4_DEPLOYMENT=your-gpt4-deployment

# Cloudflare R2 (from Cloudflare dashboard)
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=eclipselink-audio-dev
R2_PUBLIC_URL=https://your-bucket.r2.dev

# Redis (local or Upstash)
REDIS_HOST=localhost
REDIS_PORT=6379
```

#### Frontend Configuration

```bash
cd ../frontend
cp .env.example .env.local
```

Edit `apps/frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:4000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 5. Start Redis

#### Local Redis

```bash
redis-server
```

#### OR use Upstash Redis (recommended for development)

1. Create a free Redis database at [upstash.com](https://upstash.com)
2. Add to `apps/backend/.env`:
   ```bash
   UPSTASH_REDIS_REST_URL=https://your-redis.upstash.io
   UPSTASH_REDIS_REST_TOKEN=your_token
   ```

### 6. Start the Application

From the root directory:

```bash
# Start both frontend and backend
npm run dev
```

OR start them separately:

```bash
# Terminal 1 - Backend
npm run dev:backend

# Terminal 2 - Frontend
npm run dev:frontend
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:4000

### 7. Access the Application

**Test Credentials** (from seed data):

- **Nurse**: `nurse@example.com` / `password123`
- **Doctor**: `doctor@example.com` / `password123`
- **Admin**: `admin@example.com` / `password123`

## 📁 Project Structure

```
eclipselink-ai/
├── apps/
│   ├── backend/          # Express.js API server
│   │   ├── src/
│   │   │   ├── controllers/   # API route handlers
│   │   │   ├── services/      # Business logic
│   │   │   ├── middleware/    # Auth, validation, etc.
│   │   │   ├── workers/       # BullMQ background workers
│   │   │   └── routes/        # API routes
│   │   └── package.json
│   └── frontend/         # Next.js 14 application
│       ├── src/
│       │   ├── app/           # Next.js app directory
│       │   ├── components/    # React components
│       │   ├── lib/           # Utilities & API client
│       │   └── stores/        # Zustand state management
│       └── package.json
├── database/
│   ├── schema.sql        # Database schema
│   ├── seed.sql          # Test data
│   └── migrations/       # Database migrations
├── packages/
│   └── types/            # Shared TypeScript types
└── package.json          # Root package.json
```

## 🔧 Development Workflow

### Running Tests

```bash
# Run all tests
npm test

# Run backend tests
npm run test:backend

# Run frontend tests
npm run test:frontend

# Run with coverage
npm run test:coverage
```

### Linting & Formatting

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format
```

### Building for Production

```bash
# Build all workspaces
npm run build

# Build backend only
npm run build:backend

# Build frontend only
npm run build:frontend
```

## 🎯 Core Features

### 1. Voice Recording

The voice recorder component (`src/components/handoffs/voice-recorder.tsx`) provides:
- Real-time recording with pause/resume
- Auto-stop at max duration (10 minutes)
- Audio playback preview
- WebM format output

### 2. SBAR Generation

The AI-powered SBAR generation:
1. Uploads voice recording to Cloudflare R2
2. Transcribes audio using Azure OpenAI Whisper
3. Generates structured SBAR report using GPT-4
4. Provides quality and completeness scores

### 3. Handoff Workflow

Complete handoff lifecycle:
- Create handoff with basic info
- Record voice details
- Automatic SBAR generation
- Review and edit SBAR
- Complete handoff

## 🔐 Security

- **Authentication**: JWT-based with refresh tokens
- **Encryption**: AES-256-GCM for sensitive data
- **HTTPS**: Enforced in production
- **Rate Limiting**: Prevents abuse
- **Audit Logging**: All PHI access logged
- **HIPAA Compliance**: See `eclipse-ai-part7-security-hipaa.md`

## 🚨 Troubleshooting

### "Cannot connect to database"

- Verify PostgreSQL is running: `pg_isready`
- Check DATABASE_URL in `.env`
- Ensure database exists: `psql -l`

### "Redis connection failed"

- Check if Redis is running: `redis-cli ping`
- Verify REDIS_HOST and REDIS_PORT in `.env`

### "Azure OpenAI API error"

- Verify API key in Azure portal
- Check deployment names are correct
- Ensure quota is not exceeded

### "Voice upload fails"

- Verify Cloudflare R2 credentials
- Check bucket exists and is accessible
- Ensure CORS is configured correctly

### "Port already in use"

```bash
# Find process using port 4000
lsof -i :4000

# Kill the process
kill -9 <PID>
```

## 📖 Documentation

Comprehensive documentation available:

1. **Part 1**: System Architecture (`eclipse-ai-part1-architecture.md`)
2. **Part 2**: Repository Structure (`eclipse-ai-part2-repository-setup.md`)
3. **Part 3**: Database Schema (`eclipse-ai-part3-database-schema.md`)
4. **Part 4**: API Specifications (`eclipse-ai-part4a-api-auth.md`, etc.)
5. **Part 5**: Azure OpenAI Integration (`eclipse-ai-part5-azure-openai.md`)
6. **Part 6**: Deployment & DevOps (`eclipse-ai-part6-deployment-devops.md`)
7. **Part 7**: Security & HIPAA (`eclipse-ai-part7-security-hipaa.md`)
8. **Part 8**: Testing Strategy (`eclipse-ai-part8-testing-strategy.md`)
9. **Part 9**: Roadmap & Scaling (`eclipse-ai-part9-roadmap-scaling.md`)

## 🤝 Support

For issues or questions:
- Create an issue in this repository
- Contact: admin@rohimaya.com

## 📄 License

PROPRIETARY - © 2025 Rohimaya Health AI. All rights reserved.

---

**EclipseLink AI™** - Voice-enabled clinical handoff platform with AI-powered SBAR generation

Built with ❤️ by Rohimaya Health AI
Founders: Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO)
