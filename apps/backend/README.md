# EclipseLink AI - Backend API

Clinical handoff system with AI-powered voice transcription and SBAR report generation.

## Overview

This is the backend API for the EclipseLink AI platform, built with Express.js, TypeScript, and Azure OpenAI services. It provides RESTful endpoints for managing clinical handoffs, voice recordings, patient data, and AI-generated SBAR reports.

### Key Features

- **Authentication & Authorization**: JWT-based auth with role-based permissions (17 user roles)
- **Voice Recording Upload**: Multipart file upload with format validation (webm, mp3, wav, ogg, m4a)
- **Async Transcription**: BullMQ workers process voice recordings with Azure Whisper API
- **AI-Generated SBAR Reports**: GPT-4 generates structured clinical handoff reports following I-PASS framework
- **Initial vs Update Workflow**: Distinguishes between baseline handoffs and incremental updates
- **Quality Metrics**: Automatically calculates completeness, readability, and I-PASS adherence scores
- **Change Tracking**: Detects changes between SBAR versions (vital signs, medications, etc.)

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   Client    │─────▶│  Express API │─────▶│  PostgreSQL DB  │
│  (Frontend) │      │  (REST API)  │      │   (Supabase)    │
└─────────────┘      └──────────────┘      └─────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  BullMQ      │
                     │  Job Queues  │
                     └──────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
        ┌───────────────┐      ┌────────────────┐
        │ Transcription │      │ SBAR Generator │
        │    Worker     │─────▶│     Worker     │
        └───────────────┘      └────────────────┘
                │                       │
                ▼                       ▼
        ┌───────────────┐      ┌────────────────┐
        │ Azure Whisper │      │   Azure GPT-4  │
        │      API      │      │       API      │
        └───────────────┘      └────────────────┘
```

## Tech Stack

- **Runtime**: Node.js 20+
- **Language**: TypeScript 5.3+
- **Framework**: Express.js 4.18
- **Job Queue**: BullMQ 5.1 + Redis
- **AI Services**: Azure OpenAI (Whisper, GPT-4)
- **Database**: PostgreSQL (Supabase) - *planned*
- **File Storage**: Cloudflare R2 - *planned*
- **Validation**: Zod 3.22
- **Authentication**: JWT (jsonwebtoken)
- **Security**: Helmet, CORS, rate limiting

## Project Structure

```
apps/backend/
├── src/
│   ├── config/
│   │   └── queue.config.ts          # BullMQ queue setup
│   ├── controllers/
│   │   ├── auth.controller.ts       # Authentication endpoints
│   │   ├── handoff.controller.ts    # Handoff CRUD operations
│   │   ├── voice.controller.ts      # Voice upload & status polling
│   │   ├── patient.controller.ts    # Patient data & history
│   │   └── sbar.controller.ts       # SBAR reports & comparison
│   ├── middleware/
│   │   ├── auth.middleware.ts       # JWT authentication
│   │   ├── permissions.middleware.ts # Role-based access control
│   │   ├── error.middleware.ts      # Error handling
│   │   ├── rate-limit.middleware.ts # API rate limiting
│   │   └── upload.middleware.ts     # File upload (Multer)
│   ├── routes/
│   │   ├── auth.routes.ts
│   │   ├── handoff.routes.ts
│   │   ├── voice.routes.ts
│   │   ├── patient.routes.ts
│   │   └── sbar.routes.ts
│   ├── validators/
│   │   ├── auth.validator.ts        # Zod schemas for auth
│   │   ├── handoff.validator.ts
│   │   ├── voice.validator.ts
│   │   ├── patient.validator.ts
│   │   └── sbar.validator.ts
│   ├── workers/
│   │   ├── transcription.worker.ts  # Azure Whisper processing
│   │   └── sbar-generation.worker.ts # GPT-4 SBAR generation
│   ├── services/
│   │   └── azure-openai.service.ts  # Azure OpenAI client
│   ├── utils/
│   │   └── jwt.util.ts              # JWT token helpers
│   └── index.ts                     # Express app entry point
├── test-workflow.ts                 # End-to-end workflow test
├── package.json
└── tsconfig.json
```

## Getting Started

### Prerequisites

- Node.js 20+
- Redis (for BullMQ job queues)
- Azure OpenAI account with Whisper and GPT-4 deployments

### Environment Variables

Create a `.env` file in `apps/backend/`:

```env
# Server
PORT=4000
NODE_ENV=development
CORS_ORIGIN=http://localhost:3000

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_REFRESH_SECRET=your-refresh-secret-key

# Redis (for BullMQ)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_WHISPER_DEPLOYMENT=whisper-deployment-1
AZURE_OPENAI_GPT4_DEPLOYMENT=gpt4-deployment-1
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Database (TODO - Supabase)
# DATABASE_URL=postgresql://...
# SUPABASE_URL=https://...
# SUPABASE_ANON_KEY=...

# Cloudflare R2 (TODO)
# R2_ACCOUNT_ID=...
# R2_ACCESS_KEY_ID=...
# R2_SECRET_ACCESS_KEY=...
# R2_BUCKET_NAME=...
```

### Installation

```bash
# Install dependencies (from monorepo root)
npm install

# Or install backend only
cd apps/backend
npm install
```

### Running the Server

```bash
# Development mode (from monorepo root)
npm run dev:backend

# Or from backend directory
npm run dev

# Production build
npm run build
npm start
```

### Starting Redis

```bash
# Install Redis (macOS)
brew install redis
brew services start redis

# Or run manually
redis-server

# Verify Redis is running
redis-cli ping
# Should return: PONG
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/v1/auth/register` | Register new user | No |
| POST | `/v1/auth/login` | Login with email/password | No |
| POST | `/v1/auth/refresh` | Refresh access token | No |
| POST | `/v1/auth/logout` | Logout and invalidate tokens | Yes |
| GET | `/v1/auth/me` | Get current user profile | Yes |

### Handoffs

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/v1/handoffs` | Create handoff | `handoff:create` |
| GET | `/v1/handoffs` | List handoffs (filtered, paginated) | `handoff:read` |
| GET | `/v1/handoffs/:id` | Get handoff details | `handoff:read` |
| PUT | `/v1/handoffs/:id` | Update handoff | `handoff:update` |
| POST | `/v1/handoffs/:id/assign` | Assign to provider | `handoff:update` |
| POST | `/v1/handoffs/:id/complete` | Mark as completed | `handoff:update` |
| DELETE | `/v1/handoffs/:id` | Cancel/delete handoff | `handoff:delete` |

### Voice Recordings

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/v1/voice/upload` | Upload audio (multipart) | `voice:upload` |
| GET | `/v1/voice/:id` | Get recording details | `voice:read` |
| GET | `/v1/voice/:id/download` | Get presigned download URL | `voice:read` |
| GET | `/v1/voice/:id/status` | Poll transcription status | `voice:read` |
| DELETE | `/v1/voice/:id` | Delete recording | `voice:delete` |

### Patients

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/v1/patients` | List patients | `patient:read` |
| GET | `/v1/patients/:id` | Get patient details | `patient:read` |
| GET | `/v1/patients/:id/handoffs` | Get patient handoff history | `patient:read` |

### SBAR Reports

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/v1/sbar/:handoffId` | Get SBAR for handoff | `sbar:read` |
| GET | `/v1/sbar/:handoffId/versions` | Get all SBAR versions | `sbar:read` |
| GET | `/v1/sbar/:id/compare` | Compare SBAR versions | `sbar:read` |
| PUT | `/v1/sbar/:id` | Update SBAR (manual edit) | `sbar:update` |
| POST | `/v1/sbar/:id/export` | Export SBAR (PDF/DOC) | `sbar:read` |

## Complete Workflow

### 1. Upload Voice Recording

```bash
curl -X POST http://localhost:4000/v1/voice/upload \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "audio=@recording.webm" \
  -F "handoffId=h1234567-89ab-cdef-0123-456789abcdef" \
  -F "duration=185"
```

Response:
```json
{
  "success": true,
  "data": {
    "recordingId": "r1234567...",
    "transcriptionJobId": "job-abc123",
    "status": "uploaded",
    "estimatedProcessingTime": 30
  }
}
```

### 2. Poll Transcription Status

```bash
curl http://localhost:4000/v1/voice/r1234567/status \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response (processing):
```json
{
  "success": true,
  "data": {
    "status": "processing",
    "stage": "transcription",
    "progress": 45,
    "message": "Transcribing audio with Azure Whisper API..."
  }
}
```

Response (completed):
```json
{
  "success": true,
  "data": {
    "status": "transcribed",
    "stage": "completed",
    "progress": 100,
    "transcription": {
      "text": "Patient is a 60-year-old female...",
      "confidence": 0.96,
      "wordCount": 385
    },
    "nextStep": "sbar_generation"
  }
}
```

### 3. Get Generated SBAR Report

```bash
curl http://localhost:4000/v1/sbar/h1234567 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "sbar_abc123",
    "version": 4,
    "isInitial": false,
    "situation": "60yo female with T2DM. Blood glucose improved to 110 mg/dL...",
    "background": "PMH: T2DM x10yrs, HTN, hyperlipidemia...",
    "assessment": "VS: T 98.6°F, BP 130/85, HR 78...",
    "recommendation": "Continue insulin. Discharge tomorrow...",
    "qualityMetrics": {
      "completenessScore": 0.98,
      "readabilityScore": 0.92,
      "adherenceToIPassFramework": true
    },
    "changesSinceLastVersion": [
      {
        "section": "assessment",
        "field": "bloodGlucose",
        "previousValue": "145 mg/dL",
        "newValue": "110 mg/dL",
        "significance": "high"
      }
    ]
  }
}
```

## Testing the Workflow

Run the end-to-end workflow test:

```bash
# Make sure Redis is running first
redis-server

# In another terminal, run the test
npx ts-node test-workflow.ts
```

This will:
1. Queue a test transcription job
2. Workers process with Azure Whisper (or mock if no audio file)
3. Generate SBAR report with GPT-4
4. Display complete results with quality metrics

## Background Workers

The system uses BullMQ workers for async processing:

### Transcription Worker
- **Queue**: `transcription`
- **Concurrency**: 5 workers
- **Rate Limit**: 10 jobs/min
- **Timeout**: 60 seconds
- **Retries**: 3 attempts with exponential backoff

### SBAR Generation Worker
- **Queue**: `sbar-generation`
- **Concurrency**: 3 workers
- **Rate Limit**: 5 jobs/min
- **Timeout**: 120 seconds
- **Retries**: 3 attempts with exponential backoff

Workers start automatically when the Express app starts and shut down gracefully on SIGTERM/SIGINT.

## Current Status

### ✅ Implemented

- Complete Express API with all endpoints (stub controllers)
- JWT authentication & permissions middleware
- Request validation with Zod schemas
- Rate limiting (general, voice upload, auth)
- Error handling & standardized responses
- File upload with Multer (format & size validation)
- BullMQ queues and workers
- Azure Whisper transcription
- Azure GPT-4 SBAR generation with I-PASS framework
- Quality metrics calculation
- Change detection between SBAR versions
- Graceful shutdown

### 🚧 TODO (Database Integration)

All controllers currently return stub data with realistic response shapes. The next step is to integrate with PostgreSQL (Supabase):

- [ ] Database connection setup
- [ ] Replace all `// TODO: db.query()` with real database queries
- [ ] Implement Row-Level Security (RLS) policies
- [ ] Add database migrations
- [ ] Integrate Cloudflare R2 for file storage
- [ ] Add audit logging
- [ ] Implement EHR integration endpoints
- [ ] Add analytics endpoints
- [ ] Write unit and integration tests

## Development Notes

### Initial vs Update Handoff Workflow

The system distinguishes between two types of handoffs:

**Initial/Baseline Handoff** (`isInitialHandoff: true`):
- First handoff for a patient
- Generates complete SBAR from scratch
- No previous context
- Version 1

**Update Handoff** (`isInitialHandoff: false`):
- Subsequent handoffs for the same patient
- References `previousHandoffId` and `previousSbarId`
- GPT-4 receives previous SBAR as context
- Detects and highlights changes
- Increments version number

This distinction is critical for proper SBAR generation and change tracking.

### Rate Limiting

The API implements in-memory rate limiting:

- **General endpoints**: 100 requests/minute
- **Voice upload**: 10 uploads/minute
- **Auth endpoints**: 5 requests/15 minutes

For production, consider Redis-based rate limiting for distributed systems.

### Error Responses

All errors follow the Part 4D specification format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "additionalInfo": "..."
    }
  },
  "meta": {
    "requestId": "req_...",
    "timestamp": "2025-10-24T..."
  }
}
```

## Contributing

This is part of the EclipseLink AI monorepo. See the root README for contributing guidelines.

## License

Proprietary - EclipseLink AI Platform
