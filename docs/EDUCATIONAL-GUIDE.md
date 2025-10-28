# EclipseLink AI - Full Stack Educational Guide

> **Audience**: Full-stack engineers and AI/ML developers learning production system architecture
>
> **Purpose**: Comprehensive explanation of architectural decisions, technologies, and implementation patterns

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Fundamentals](#architecture-fundamentals)
3. [Technology Stack Deep Dive](#technology-stack-deep-dive)
4. [Database Design Patterns](#database-design-patterns)
5. [Backend Architecture](#backend-architecture)
6. [AI/ML Integration](#aiml-integration)
7. [Worker Pattern & Job Queues](#worker-pattern--job-queues)
8. [Frontend Architecture](#frontend-architecture)
9. [Security & HIPAA Compliance](#security--hipaa-compliance)
10. [Deployment Architecture](#deployment-architecture)
11. [Testing & Quality Assurance](#testing--quality-assurance)
12. [Common Pitfalls & Best Practices](#common-pitfalls--best-practices)

---

## System Overview

### What is EclipseLink AI?

EclipseLink AI is a **clinical handoff automation system** that transforms voice recordings into structured SBAR (Situation, Background, Assessment, Recommendation) reports for hospital staff.

**Core Value Proposition**:
- **85% time reduction** in handoff documentation (from 15 minutes to 2-3 minutes)
- **Cost**: ~$0.09 per handoff (Whisper $0.02 + GPT-4 $0.07)
- **Processing Time**: 45-90 seconds from voice upload to structured report
- **Update-Only Model**: Initial baseline + lightweight updates (not starting from scratch each shift)

### The Problem It Solves

**Traditional Clinical Handoffs**:
- 15-20 minutes of manual documentation per patient
- 30-40 patients per shift = 7.5-13 hours of documentation
- Information gets lost between shifts
- Inconsistent format across staff
- High cognitive load on already-tired staff

**EclipseLink Solution**:
- Nurse records 2-3 minute voice memo
- AI automatically transcribes (Azure Whisper)
- AI generates structured SBAR report (GPT-4)
- Nurse reviews/edits if needed
- Next shift nurse receives complete, structured handoff

---

## Architecture Fundamentals

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                              │
│  Nurse's Browser (Next.js 14 Frontend - Cloudflare Pages)      │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS/REST API
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER                                   │
│  Express.js Backend (TypeScript - Railway)                      │
│  - Authentication (JWT)                                          │
│  - Request validation                                            │
│  - Business logic                                                │
│  - Database queries                                              │
└───────┬──────────────┬─────────────┬───────────────┬────────────┘
        │              │             │               │
        ↓              ↓             ↓               ↓
┌──────────────┐ ┌──────────┐ ┌─────────────┐ ┌──────────────┐
│  PostgreSQL  │ │    R2    │ │   Redis     │ │ Azure OpenAI │
│  (Supabase)  │ │(Cloudflare│ │  (Upstash)  │ │  - Whisper   │
│              │ │  Storage) │ │             │ │  - GPT-4     │
│ - Patients   │ │ - Voice   │ │ - BullMQ    │ │              │
│ - Handoffs   │ │   files   │ │ - Job queue │ │              │
│ - SBAR       │ │           │ │             │ │              │
└──────────────┘ └──────────┘ └─────────────┘ └──────────────┘
        ↑                            ↑               ↑
        │                            │               │
        └────────────────────────────┴───────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                    WORKER LAYER                                  │
│  Background Job Processors (Node.js - Railway)                  │
│  - Transcription Worker (Azure Whisper API calls)               │
│  - SBAR Generation Worker (GPT-4 API calls)                     │
└─────────────────────────────────────────────────────────────────┘
```

### Why This Architecture?

**1. Separation of Concerns**
- **Frontend**: Pure UI/UX, no business logic
- **Backend API**: Business logic, validation, orchestration
- **Workers**: Long-running AI tasks (can take 30-60 seconds)
- **Database**: Single source of truth

**2. Scalability**
- Workers can be scaled independently (add more worker processes)
- API can be scaled horizontally (add more server instances)
- Database handles concurrency via connection pooling

**3. Reliability**
- If worker crashes, job stays in queue (BullMQ persistence)
- Retry logic with exponential backoff
- Failed jobs go to dead-letter queue for investigation

**4. Cost Efficiency**
- Workers only consume resources when processing
- Cloudflare R2 cheaper than AWS S3 ($0.015/GB vs $0.023/GB)
- Serverless database (Supabase) scales to zero

---

## Technology Stack Deep Dive

### Frontend: Next.js 14 + React 18

**Why Next.js?**
```typescript
// 1. App Router (app/ directory) - Modern React architecture
app/
  layout.tsx          // Root layout (shared across all pages)
  page.tsx            // Home page
  dashboard/
    page.tsx          // Dashboard page
    layout.tsx        // Dashboard-specific layout
  handoffs/
    [id]/             // Dynamic route (handoff details)
      page.tsx
```

**Benefits**:
- **Server Components**: Reduce JavaScript bundle size (only interactive parts are client-side)
- **Built-in Routing**: File-system based, no react-router needed
- **API Routes**: Can build API endpoints in Next.js (we use separate Express backend instead)
- **Automatic Code Splitting**: Each page loads only its required code

**Example Server vs Client Components**:
```typescript
// Server Component (default) - Runs on server, no JS sent to client
export default async function HandoffsList() {
  const handoffs = await fetch('https://api.example.com/handoffs');
  return <div>{handoffs.map(h => <HandoffCard key={h.id} handoff={h} />)}</div>;
}

// Client Component - Interactive, runs in browser
'use client'
export default function VoiceRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  // ... interactive logic
}
```

**React 18 Features**:
- **Concurrent Rendering**: UI stays responsive during heavy operations
- **Suspense**: Loading states handled declaratively
- **Automatic Batching**: Multiple state updates batched into single render

**Styling: Tailwind CSS + shadcn/ui**
```typescript
// Tailwind: Utility-first CSS (no writing CSS files)
<button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg">
  Start Recording
</button>

// shadcn/ui: Pre-built, accessible components
import { Button } from "@/components/ui/button"
<Button variant="primary" size="lg">Start Recording</Button>
```

**Why Tailwind over traditional CSS?**
- No naming conflicts (no class name collisions)
- Responsive design built-in: `md:text-lg` (medium screens and up)
- Consistent spacing: `p-4` always means 1rem padding
- Tree-shaking: Unused styles automatically removed

---

### Backend: Express.js + TypeScript

**Why Express?**
- **Mature ecosystem**: 14+ years, battle-tested
- **Middleware pattern**: Easy to add authentication, logging, validation
- **RESTful APIs**: Standard HTTP methods (GET, POST, PUT, DELETE)
- **TypeScript**: Catch errors at compile time, not runtime

**Project Structure**:
```
apps/backend/src/
├── config/              # Configuration (database, env vars)
│   ├── database.config.ts
│   └── env.config.ts
├── controllers/         # Request handlers (business logic)
│   ├── handoff.controller.ts
│   ├── voice.controller.ts
│   └── sbar.controller.ts
├── middleware/          # Request interceptors
│   ├── auth.middleware.ts      # JWT validation
│   ├── error.middleware.ts     # Error handling
│   └── validation.middleware.ts
├── services/            # External integrations
│   ├── storage.service.ts      # Cloudflare R2
│   └── azure-openai.service.ts # AI APIs
├── workers/             # Background job processors
│   ├── transcription.worker.ts
│   └── sbar-generation.worker.ts
├── routes/              # API route definitions
│   └── v1/
│       ├── handoff.routes.ts
│       └── sbar.routes.ts
└── types/               # TypeScript type definitions
    └── database.types.ts
```

**Controller Pattern Example**:
```typescript
// apps/backend/src/controllers/handoff.controller.ts
export async function createHandoff(req: Request, res: Response): Promise<void> {
  // 1. Extract data from request
  const { patientId, fromStaffId, toStaffId } = req.body;

  // 2. Validate business rules
  if (!patientId) {
    throw new ValidationError('patientId is required');
  }

  // 3. Database operations
  const patient = await db.query('SELECT * FROM patients WHERE id = $1', [patientId]);
  if (!patient.rows.length) {
    throw new NotFoundError('patient', patientId);
  }

  // 4. Create handoff
  const handoff = await db.query(
    'INSERT INTO handoffs (patient_id, from_staff_id, to_staff_id) VALUES ($1, $2, $3) RETURNING *',
    [patientId, fromStaffId, toStaffId]
  );

  // 5. Return response
  res.status(201).json({
    success: true,
    data: handoff.rows[0]
  });
}
```

**Why Controllers?**
- **Separation of Concerns**: Routes define URLs, controllers define logic
- **Testability**: Can test controllers without spinning up HTTP server
- **Reusability**: Same logic can be used in multiple routes

**Middleware Pattern**:
```typescript
// Authentication middleware
app.use('/v1/handoffs', authMiddleware, handoffRoutes);

// How authMiddleware works:
export async function authMiddleware(req: Request, res: Response, next: NextFunction) {
  // 1. Extract JWT token from header
  const token = req.headers.authorization?.split(' ')[1];

  // 2. Verify token
  const decoded = jwt.verify(token, process.env.JWT_SECRET);

  // 3. Attach user info to request
  req.user = decoded;

  // 4. Continue to next middleware/controller
  next();
}
```

**Benefits**:
- Run code before every request (auth, logging, validation)
- Chain multiple middleware functions
- Early exit if validation fails (don't hit controller)

---

### Database: PostgreSQL (via Supabase)

**Why PostgreSQL?**
- **ACID Compliance**: Atomicity, Consistency, Isolation, Durability (critical for healthcare)
- **JSONB Support**: Store complex data (edit history, changes) without extra tables
- **Full-Text Search**: Search patient records efficiently
- **Row-Level Security (RLS)**: Database-level access control (HIPAA requirement)

**Schema Design Philosophy**:

**1. Normalization** (Avoid data duplication)
```sql
-- BAD: Duplicate patient data in every handoff
CREATE TABLE handoffs (
  id UUID PRIMARY KEY,
  patient_first_name TEXT,  -- Duplicated!
  patient_last_name TEXT,   -- Duplicated!
  patient_mrn TEXT          -- Duplicated!
);

-- GOOD: Reference patient by ID
CREATE TABLE handoffs (
  id UUID PRIMARY KEY,
  patient_id UUID REFERENCES patients(id)  -- Single source of truth
);
```

**2. Foreign Keys** (Enforce relationships)
```sql
CREATE TABLE handoffs (
  patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE RESTRICT,
  -- If you try to delete a patient with active handoffs, PostgreSQL will reject it
);
```

**3. Indexes** (Speed up queries)
```sql
-- Without index: Full table scan (slow for large tables)
SELECT * FROM handoffs WHERE patient_id = 'abc-123';  -- Scans every row

-- With index: Direct lookup (O(log n) instead of O(n))
CREATE INDEX idx_handoffs_patient_id ON handoffs(patient_id);
```

**4. JSONB for Flexible Data**
```sql
-- edit_history column stores array of edits
{
  "edit_history": [
    {
      "editedAt": "2025-10-28T10:30:00Z",
      "editedBy": { "id": "user-123", "name": "Dr. Smith" },
      "changes": [
        {"section": "situation", "previousValue": "...", "newValue": "..."}
      ]
    }
  ]
}

-- Query JSONB data
SELECT * FROM sbar_reports
WHERE edit_history @> '[{"editedBy": {"id": "user-123"}}]';
```

**5. Enums for Type Safety**
```sql
-- BAD: String column (typos allowed)
CREATE TABLE handoffs (status TEXT);  -- "complted" (typo!) gets inserted

-- GOOD: Enum (only valid values allowed)
CREATE TYPE handoff_status AS ENUM ('draft', 'ready', 'completed');
CREATE TABLE handoffs (status handoff_status);  -- Typos rejected at insert
```

**Example: Complex Query with JOINs**
```sql
-- Fetch handoff with patient, from_staff, to_staff details in ONE query
SELECT
  h.*,
  p.first_name as patient_first_name,
  p.last_name as patient_last_name,
  p.mrn,
  fs.first_name as from_staff_first_name,
  fs.last_name as from_staff_last_name,
  ts.first_name as to_staff_first_name,
  ts.last_name as to_staff_last_name
FROM handoffs h
LEFT JOIN patients p ON h.patient_id = p.id
LEFT JOIN staff fs ON h.from_staff_id = fs.id
LEFT JOIN staff ts ON h.to_staff_id = ts.id
WHERE h.id = $1;

-- Why this is efficient:
-- 1. Single database round-trip (vs 4 separate queries)
-- 2. PostgreSQL optimizes the JOIN execution plan
-- 3. Indexes on foreign keys make JOINs fast
```

---

## Backend Architecture

### RESTful API Design

**REST Principles**:
1. **Resources**: Nouns (handoffs, patients, sbar)
2. **HTTP Methods**: Verbs (GET, POST, PUT, DELETE)
3. **Stateless**: Each request contains all needed info (JWT token)
4. **Standard Status Codes**: 200 OK, 201 Created, 404 Not Found, 500 Server Error

**URL Structure**:
```
GET    /v1/handoffs              # List all handoffs
POST   /v1/handoffs              # Create new handoff
GET    /v1/handoffs/:id          # Get specific handoff
PUT    /v1/handoffs/:id          # Update handoff
DELETE /v1/handoffs/:id          # Delete handoff

GET    /v1/sbar/:handoffId       # Get SBAR for handoff
GET    /v1/sbar/:handoffId/versions  # Get version history
GET    /v1/sbar/:id/compare?compareWith=xyz  # Compare versions
PUT    /v1/sbar/:id              # Edit SBAR
POST   /v1/sbar/:id/export       # Export to PDF/DOCX
```

**Why `/v1/`?**
- **API Versioning**: When breaking changes needed, create `/v2/` (old clients keep working)
- **Clear Deprecation Path**: Announce v1 deprecation, give clients time to migrate

**Request/Response Format**:
```typescript
// Standard success response
{
  "success": true,
  "data": { /* actual data */ },
  "meta": {
    "requestId": "req_12345",
    "timestamp": "2025-10-28T10:30:00Z"
  }
}

// Standard error response
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Handoff with ID abc-123 not found",
    "details": { "handoffId": "abc-123" }
  },
  "meta": {
    "requestId": "req_12345",
    "timestamp": "2025-10-28T10:30:00Z"
  }
}
```

**Why consistent format?**
- Frontend can handle all responses the same way
- Easy to add global error handling
- Debugging easier with requestId

---

### Service Layer Pattern

**What is a Service?**
A service encapsulates interaction with external systems (databases, APIs, storage).

**Example: Storage Service**
```typescript
// apps/backend/src/services/storage.service.ts
export class StorageService {
  private client: S3Client;  // Cloudflare R2 is S3-compatible

  async uploadFile(options: UploadOptions): Promise<UploadResult> {
    // 1. Generate unique file key
    const fileKey = this.generateFileKey(options.fileName, facilityId, handoffId);

    // 2. Upload to R2
    await this.client.send(new PutObjectCommand({
      Bucket: this.bucketName,
      Key: fileKey,
      Body: options.fileBuffer,
      ContentType: options.contentType
    }));

    // 3. Return result
    return { fileKey, fileUrl, fileSize };
  }

  async getPresignedUrl(fileKey: string): Promise<string> {
    // Generate temporary URL (expires in 1 hour)
    return await getSignedUrl(this.client, new GetObjectCommand({
      Bucket: this.bucketName,
      Key: fileKey
    }), { expiresIn: 3600 });
  }
}
```

**Why Services?**
- **Testability**: Mock external systems in tests
- **Reusability**: Use storage service in multiple controllers
- **Encapsulation**: Controller doesn't know R2 implementation details

**Controller using Service**:
```typescript
// Controller doesn't know about S3Client, PutObjectCommand, etc.
const storageService = new StorageService();
const uploadResult = await storageService.uploadFile({
  fileName: 'recording.webm',
  fileBuffer: req.file.buffer,
  contentType: 'audio/webm'
});
```

---

### Error Handling Strategy

**Custom Error Classes**:
```typescript
// apps/backend/src/middleware/error.middleware.ts
export class NotFoundError extends Error {
  constructor(resource: string, id: string) {
    super(`${resource} with ID ${id} not found`);
    this.name = 'NotFoundError';
  }
}

export class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

// Usage in controller:
if (!patient) {
  throw new NotFoundError('patient', patientId);
}
```

**Global Error Handler Middleware**:
```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  // Log error for debugging
  console.error(err);

  // Determine HTTP status code
  let statusCode = 500;
  if (err instanceof NotFoundError) statusCode = 404;
  if (err instanceof ValidationError) statusCode = 400;

  // Return standardized error response
  res.status(statusCode).json({
    success: false,
    error: {
      code: err.name,
      message: err.message
    }
  });
});
```

**Benefits**:
- No try-catch in every controller function
- Consistent error responses
- Easy to add error tracking (Sentry, Datadog)

---

## AI/ML Integration

### Azure OpenAI Service

**Why Azure OpenAI vs OpenAI directly?**
- **Enterprise SLA**: 99.9% uptime guarantee
- **HIPAA Compliance**: BAA (Business Associate Agreement) available
- **Data Residency**: Keep PHI in specific regions
- **Microsoft Support**: Enterprise support contracts

**Architecture**:
```typescript
// apps/backend/src/services/azure-openai.service.ts
export class AzureOpenAIService {
  private client: OpenAIClient;

  constructor() {
    this.client = new OpenAIClient(
      `https://${process.env.AZURE_OPENAI_ENDPOINT}.openai.azure.com`,
      new AzureKeyCredential(process.env.AZURE_OPENAI_KEY)
    );
  }

  // Transcription (Whisper model)
  async transcribeAudio(audioFilePath: string): Promise<TranscriptionResult> {
    const audioStream = fs.createReadStream(audioFilePath);

    const result = await this.client.getAudioTranscription(
      process.env.AZURE_OPENAI_WHISPER_DEPLOYMENT,  // "whisper"
      audioStream,
      {
        language: 'en',
        temperature: 0,  // Deterministic output
        response_format: 'verbose_json'  // Include timestamps, confidence
      }
    );

    return {
      text: result.text,
      duration: result.duration,
      confidence: this.calculateConfidence(result),
      language: result.language
    };
  }

  // Text Generation (GPT-4 model)
  async generateCompletion(messages: ChatMessage[]): Promise<CompletionResult> {
    const result = await this.client.getChatCompletions(
      process.env.AZURE_OPENAI_GPT4_DEPLOYMENT,  // "gpt-4"
      messages,
      {
        temperature: 0.3,  // Slightly creative but mostly factual
        max_tokens: 2000,   // Limit response length
        top_p: 0.9,        // Nucleus sampling
        response_format: { type: 'json_object' }  // Force JSON output
      }
    );

    return {
      content: result.choices[0].message.content,
      finishReason: result.choices[0].finish_reason,
      usage: result.usage  // Token counts for billing
    };
  }
}
```

### Prompt Engineering for SBAR

**System Prompt** (Defines AI behavior):
```typescript
const SBAR_SYSTEM_PROMPT = `You are an expert clinical documentation AI assistant specialized in generating structured SBAR reports.

Your task:
1. Analyze the provided clinical voice transcription
2. Extract key information
3. Generate a structured SBAR report following I-PASS framework

SBAR Structure:
- **Situation**: Current patient status, chief complaint, vital signs
- **Background**: Medical history, medications, allergies, admission reason
- **Assessment**: Clinical assessment, trends, lab results
- **Recommendation**: Care plan, pending tasks, follow-ups

Guidelines:
- Use clear, concise medical terminology
- Include all critical information (allergies, vitals, medications)
- Prioritize patient safety
- Flag any concerning findings
- Maintain professional tone

Output Format: JSON
{
  "situation": "...",
  "background": "...",
  "assessment": "...",
  "recommendation": "..."
}`;
```

**Why This Prompt Works**:
1. **Role Definition**: "expert clinical documentation AI" sets context
2. **Task Clarity**: Explicit steps (analyze → extract → generate)
3. **Structure**: Clear SBAR framework
4. **Guidelines**: Tone, terminology, priorities
5. **Output Format**: Forces structured JSON response

**Initial vs Update Prompts**:
```typescript
// Initial handoff: Full detail required
function buildInitialSbarPrompt(transcriptionText: string) {
  return [
    { role: 'system', content: SBAR_SYSTEM_PROMPT },
    {
      role: 'user',
      content: `This is an INITIAL handoff (patient admission or first documentation).

TRANSCRIPTION:
${transcriptionText}

Generate a complete SBAR report with full patient history, current status, and care plan.`
    }
  ];
}

// Update handoff: Focus on changes
function buildUpdateSbarPrompt(transcriptionText: string, previousSbar: any) {
  return [
    { role: 'system', content: SBAR_SYSTEM_PROMPT },
    {
      role: 'user',
      content: `This is an UPDATE handoff.

PREVIOUS SBAR (Version ${previousSbar.version}):
Situation: ${previousSbar.situation}
Background: ${previousSbar.background}
Assessment: ${previousSbar.assessment}
Recommendation: ${previousSbar.recommendation}

NEW TRANSCRIPTION:
${transcriptionText}

Generate an UPDATED SBAR that:
1. Incorporates new information from transcription
2. Maintains relevant context from previous version
3. Highlights what has CHANGED since last handoff
4. Updates recommendations based on current status`
    }
  ];
}
```

**Why Update Prompts are Different**:
- Context window limit (GPT-4 has ~8k tokens)
- Nurse only records changes, not entire patient history
- Faster processing (less tokens = lower cost)
- Better quality (AI sees progression over time)

---

### Quality Metrics

**Automated Quality Scoring**:
```typescript
function calculateQualityMetrics(sbar: SbarReport) {
  // Completeness: Are key elements present?
  const hasVitals = /\d+\/\d+|HR|BP|temp|O2 sat|SpO2/i.test(
    sbar.situation + sbar.assessment
  );
  const hasMedications = /medication|drug|dose|mg|ml/i.test(sbar.background);
  const hasAllergies = /allergy|allergies|allergic|NKDA/i.test(sbar.background);
  const hasTasks = /follow.?up|monitor|continue|discharge|pending/i.test(
    sbar.recommendation
  );

  const completenessScore = [hasVitals, hasMedications, hasAllergies, hasTasks]
    .filter(Boolean).length / 4;

  // Readability: Average sentence length (8-20 words is ideal)
  const sentences = sbar.situation.split(/[.!?]+/);
  const avgSentenceLength = sentences.reduce((sum, s) =>
    sum + s.trim().split(/\s+/).length, 0
  ) / sentences.length;
  const readabilityScore = avgSentenceLength >= 8 && avgSentenceLength <= 20
    ? 1.0
    : Math.max(0, 1 - Math.abs(avgSentenceLength - 14) / 20);

  // I-PASS Framework adherence
  const adherenceToIPassFramework =
    hasVitals && hasMedications && hasAllergies && hasTasks;

  // Critical info present
  const criticalInfoPresent = hasVitals && hasAllergies;

  return {
    completenessScore,
    readabilityScore,
    adherenceToIPassFramework,
    criticalInfoPresent
  };
}
```

**Why Automated Metrics?**
- Flag low-quality reports for human review
- Track AI model performance over time
- Identify areas for prompt engineering improvement
- Justify 85% time savings claim

---

## Worker Pattern & Job Queues

### Why Background Workers?

**The Problem**:
```typescript
// BAD: Synchronous API call
app.post('/v1/voice/upload', async (req, res) => {
  const file = req.file;

  // Upload to R2 (3 seconds)
  await storageService.upload(file);

  // Transcribe with Whisper (30 seconds) ⚠️ USER WAITS 30+ SECONDS!
  const transcription = await azureService.transcribe(file);

  // Generate SBAR with GPT-4 (15 seconds) ⚠️ USER WAITS 45+ SECONDS TOTAL!
  const sbar = await azureService.generateSbar(transcription);

  res.json({ success: true });
});
```

**The Solution**:
```typescript
// GOOD: Queue job, return immediately
app.post('/v1/voice/upload', async (req, res) => {
  const file = req.file;

  // Upload to R2 (3 seconds)
  const uploadResult = await storageService.upload(file);

  // Queue transcription job (instant)
  await transcriptionQueue.add('transcribe', {
    filePath: uploadResult.fileKey,
    handoffId: req.body.handoffId
  });

  // Return immediately (3 seconds total)
  res.json({ success: true, message: 'Processing in background' });
});
```

**Benefits**:
- API responds in 3 seconds instead of 45 seconds
- Worker handles AI calls asynchronously
- If worker crashes, job stays in queue (processed when worker restarts)
- Can scale workers independently of API

---

### BullMQ Architecture

**BullMQ** is a Node.js job queue built on Redis.

**Components**:
```
┌─────────────┐
│   Producer  │ (API endpoint)
│   (API)     │ Adds jobs to queue
└──────┬──────┘
       │
       ↓
┌─────────────┐
│    Redis    │ Stores job data
│    Queue    │ - Job payload
│   (Upstash) │ - Job status
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Consumer  │ (Worker process)
│   (Worker)  │ Processes jobs
└─────────────┘
```

**Queue Configuration**:
```typescript
// apps/backend/src/config/queue.config.ts
const connection = {
  host: process.env.REDIS_HOST,
  port: parseInt(process.env.REDIS_PORT),
  password: process.env.REDIS_PASSWORD,
  tls: {} // Required for Upstash
};

export const transcriptionQueue = new Queue('transcription', {
  connection,
  defaultJobOptions: {
    attempts: 3,              // Retry failed jobs 3 times
    backoff: {
      type: 'exponential',    // 5s, 10s, 20s delays
      delay: 5000
    },
    removeOnComplete: {
      age: 86400,             // Keep completed jobs for 24 hours
      count: 1000             // Keep last 1000 completed jobs
    },
    removeOnFail: false       // Keep failed jobs for debugging
  }
});
```

**Worker Implementation**:
```typescript
// apps/backend/src/workers/transcription.worker.ts
export const transcriptionWorker = new Worker(
  'transcription',
  async (job: Job<TranscriptionJobData>) => {
    const { recordingId, filePath, handoffId } = job.data;

    // Update database: status = 'processing'
    await db.query(
      'UPDATE voice_recordings SET status = $1 WHERE id = $2',
      ['processing', recordingId]
    );

    // Download file from R2
    const audioBuffer = await storageService.downloadFile(filePath);

    // Transcribe with Azure Whisper
    const transcription = await azureOpenAIService.transcribeAudio(audioBuffer);

    // Save transcription to database
    await db.query(
      'UPDATE voice_recordings SET transcription_text = $1, status = $2 WHERE id = $3',
      [transcription.text, 'transcribed', recordingId]
    );

    // Queue SBAR generation job
    await sbarGenerationQueue.add('generate-sbar', {
      handoffId,
      transcriptionText: transcription.text
    });

    // Return success
    return { success: true, transcription: transcription.text };
  },
  {
    connection,
    concurrency: 5  // Process 5 jobs in parallel
  }
);

// Event handlers
transcriptionWorker.on('completed', (job, result) => {
  console.log(`✅ Job ${job.id} completed:`, result);
});

transcriptionWorker.on('failed', (job, error) => {
  console.error(`❌ Job ${job?.id} failed:`, error);
});
```

**Why BullMQ?**
- **Persistence**: Jobs survive Redis restarts (persisted to disk)
- **Retry Logic**: Automatic exponential backoff
- **Priority Queues**: Urgent handoffs processed first
- **Rate Limiting**: Respect Azure OpenAI rate limits
- **Monitoring**: BullMQ UI shows job status in real-time

---

### Job Lifecycle

```
1. Job Created
   ↓
2. Job Queued (waiting in Redis)
   ↓
3. Job Active (worker picks it up)
   ↓
4. Job Processing (worker executes async function)
   ↓
   ├─→ 5a. Job Completed (success)
   │   └─→ Removed after 24 hours
   │
   └─→ 5b. Job Failed (error thrown)
       └─→ 6. Job Waiting (retry in 5s, 10s, 20s)
           └─→ After 3 attempts: Job Failed (permanently)
               └─→ Move to Dead Letter Queue for investigation
```

**Monitoring Jobs**:
```typescript
// Get job status
const job = await transcriptionQueue.getJob(jobId);
console.log(job.state);  // 'waiting', 'active', 'completed', 'failed'

// Get queue metrics
const waiting = await transcriptionQueue.getWaitingCount();
const active = await transcriptionQueue.getActiveCount();
const failed = await transcriptionQueue.getFailedCount();
```

---

## Security & HIPAA Compliance

### HIPAA Requirements

**HIPAA** (Health Insurance Portability and Accountability Act) requires:
1. **Access Controls**: Only authorized users can view PHI (Protected Health Information)
2. **Audit Trails**: Log all access to patient data
3. **Data Encryption**: Encrypt data in transit and at rest
4. **Data Isolation**: Facility A cannot see Facility B's data
5. **Business Associate Agreements (BAA)**: All vendors must sign BAA

### Facility Isolation

**Row-Level Security (RLS)**:
```sql
-- Every table has facility_id
CREATE TABLE handoffs (
  id UUID PRIMARY KEY,
  facility_id UUID NOT NULL REFERENCES facilities(id),
  patient_id UUID NOT NULL,
  -- ...
);

-- RLS Policy: Users can only see their facility's data
CREATE POLICY facility_isolation ON handoffs
  FOR ALL
  USING (facility_id = current_setting('app.facility_id')::UUID);

-- Enable RLS
ALTER TABLE handoffs ENABLE ROW LEVEL SECURITY;
```

**How it works**:
```typescript
// 1. User authenticates, JWT contains facilityId
const token = jwt.sign({ userId: 'user-123', facilityId: 'facility-abc' }, SECRET);

// 2. Middleware extracts facilityId from JWT
req.user = { userId: 'user-123', facilityId: 'facility-abc' };

// 3. Every database query includes facility_id
await db.query(
  'SELECT * FROM handoffs WHERE facility_id = $1 AND id = $2',
  [req.user.facilityId, handoffId]
);

// User from facility-abc CANNOT query facility-xyz's data
// PostgreSQL RLS enforces this at database level (even if SQL is wrong)
```

### Authentication & Authorization

**JWT (JSON Web Token)**:
```typescript
// Login endpoint generates JWT
app.post('/v1/auth/login', async (req, res) => {
  const { email, password } = req.body;

  // Verify credentials
  const user = await db.query('SELECT * FROM staff WHERE email = $1', [email]);
  const isValid = await bcrypt.compare(password, user.password_hash);

  if (!isValid) {
    throw new UnauthorizedError('Invalid credentials');
  }

  // Generate JWT
  const token = jwt.sign(
    {
      userId: user.id,
      facilityId: user.facility_id,
      role: user.role
    },
    process.env.JWT_SECRET,
    { expiresIn: '8h' }  // Token expires after 8 hours
  );

  res.json({ success: true, token });
});
```

**JWT Structure**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJ1c2VyLTEyMyIsImZhY2lsaXR5SWQiOiJmYWNpbGl0eS1hYmMiLCJyb2xlIjoicmVnaXN0ZXJlZF9udXJzZSIsImlhdCI6MTYzMjc2MDAwMCwiZXhwIjoxNjMyNzg4ODAwfQ.abc123def456...

Header    Payload                                          Signature
(base64)  (base64)                                         (HMAC-SHA256)
```

**Authentication Middleware**:
```typescript
export async function authMiddleware(req: Request, res: Response, next: NextFunction) {
  try {
    // Extract token
    const authHeader = req.headers.authorization;
    if (!authHeader?.startsWith('Bearer ')) {
      throw new UnauthorizedError('No token provided');
    }

    const token = authHeader.split(' ')[1];

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET) as JWTPayload;

    // Attach to request
    req.user = {
      userId: decoded.userId,
      facilityId: decoded.facilityId,
      role: decoded.role
    };

    next();
  } catch (error) {
    throw new UnauthorizedError('Invalid token');
  }
}
```

### Audit Logging

**Every database operation is logged**:
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES staff(id),
  facility_id UUID NOT NULL REFERENCES facilities(id),
  action audit_action NOT NULL,  -- 'create', 'read', 'update', 'delete', 'export'
  resource_type TEXT NOT NULL,   -- 'handoff', 'sbar_report', 'patient'
  resource_id UUID,
  changes JSONB,                 -- Before/after values for updates
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Automatic Audit Logging**:
```typescript
// Middleware logs every request
app.use(async (req: Request, res: Response, next: NextFunction) => {
  const startTime = Date.now();

  // Continue request
  next();

  // After response sent, log to audit table
  res.on('finish', async () => {
    await db.query(
      `INSERT INTO audit_logs (user_id, facility_id, action, resource_type, ip_address, user_agent)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [
        req.user?.userId,
        req.user?.facilityId,
        req.method,
        req.path.split('/')[2],  // Extract resource from /v1/handoffs/123
        req.ip,
        req.headers['user-agent']
      ]
    );
  });
});
```

---

## Deployment Architecture

### Development vs Production

**Development Environment**:
- Local PostgreSQL or Supabase free tier
- Mock Azure OpenAI (return test transcriptions)
- Local R2 emulator or test bucket
- Redis via Docker

**Production Environment**:
- Supabase (PostgreSQL) - managed, automatic backups
- Cloudflare R2 - production bucket with lifecycle policies
- Upstash Redis - managed Redis with global replication
- Azure OpenAI - production deployment with rate limits

### Railway Deployment

**Why Railway?**
- **Simple Deployment**: Git push to deploy
- **Environment Variables**: Secure secret management
- **Auto-scaling**: Scales based on CPU/memory usage
- **Monitoring**: Built-in logs, metrics, alerts
- **Cost**: $5/month for hobby projects, scales to enterprise

**railway.json**:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm install && npm run build"
  },
  "deploy": {
    "startCommand": "npm run start",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

**Deployment Process**:
```bash
# 1. Link Railway project
railway link

# 2. Set environment variables
railway variables set DATABASE_URL=postgresql://...
railway variables set AZURE_OPENAI_KEY=...

# 3. Deploy
git push railway main

# Railway automatically:
# - Installs dependencies (npm install)
# - Builds TypeScript (npm run build)
# - Starts server (npm run start)
# - Monitors health (restarts if crashed)
```

### Cloudflare Pages (Frontend)

**Why Cloudflare Pages?**
- **Edge Network**: Serve from 200+ data centers worldwide
- **Automatic HTTPS**: Free SSL certificates
- **CDN**: Automatic caching of static assets
- **Preview Deployments**: Every Git branch gets its own URL
- **Cost**: Free for unlimited sites

**Deployment**:
```bash
# 1. Build Next.js app
cd apps/frontend
npm run build

# 2. Deploy to Cloudflare Pages
npx wrangler pages deploy out/

# Cloudflare automatically:
# - Uploads all files to CDN
# - Invalidates cache for changed files
# - Assigns URL (e.g., https://eclipselink.pages.dev)
```

---

## Testing & Quality Assurance

### Testing Strategy

**1. Unit Tests** (Test individual functions)
```typescript
// apps/backend/src/services/__tests__/storage.service.test.ts
import { StorageService } from '../storage.service';

describe('StorageService', () => {
  let storageService: StorageService;

  beforeEach(() => {
    storageService = new StorageService();
  });

  test('generateFileKey creates unique keys', () => {
    const key1 = storageService.generateFileKey('test.webm', 'facility-1', 'handoff-1');
    const key2 = storageService.generateFileKey('test.webm', 'facility-1', 'handoff-1');

    expect(key1).not.toBe(key2);  // Different due to timestamp/random
    expect(key1).toContain('facility-1');
    expect(key1).toContain('handoff-1');
  });
});
```

**2. Integration Tests** (Test API endpoints)
```typescript
// apps/backend/src/controllers/__tests__/handoff.controller.test.ts
import request from 'supertest';
import app from '../../app';

describe('POST /v1/handoffs', () => {
  test('creates handoff with valid data', async () => {
    const response = await request(app)
      .post('/v1/handoffs')
      .set('Authorization', `Bearer ${testToken}`)
      .send({
        patientId: 'patient-123',
        fromStaffId: 'staff-1',
        toStaffId: 'staff-2'
      });

    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data.patient_id).toBe('patient-123');
  });

  test('returns 400 for missing patientId', async () => {
    const response = await request(app)
      .post('/v1/handoffs')
      .set('Authorization', `Bearer ${testToken}`)
      .send({
        fromStaffId: 'staff-1',
        toStaffId: 'staff-2'
      });

    expect(response.status).toBe(400);
    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

**3. End-to-End Tests** (Test full workflows)
```typescript
// tests/e2e/handoff-workflow.test.ts
describe('Complete handoff workflow', () => {
  test('nurse uploads voice → transcription → SBAR generation', async () => {
    // 1. Upload voice recording
    const uploadResponse = await uploadVoiceRecording('test-audio.webm');
    expect(uploadResponse.status).toBe(201);

    // 2. Wait for transcription (poll job status)
    const jobId = uploadResponse.body.data.jobId;
    await waitForJobCompletion(jobId, 60000);  // 60 second timeout

    // 3. Verify SBAR generated
    const sbarResponse = await getSbar(uploadResponse.body.data.handoffId);
    expect(sbarResponse.body.data.situation).toBeDefined();
    expect(sbarResponse.body.data.background).toBeDefined();
  });
});
```

---

## Common Pitfalls & Best Practices

### 1. Database Connection Pooling

**PROBLEM**:
```typescript
// BAD: New connection for every query
async function getHandoff(id: string) {
  const client = new Client({ connectionString: process.env.DATABASE_URL });
  await client.connect();  // Slow! Opens TCP connection
  const result = await client.query('SELECT * FROM handoffs WHERE id = $1', [id]);
  await client.end();
  return result.rows[0];
}
```

**SOLUTION**:
```typescript
// GOOD: Connection pool (reuse connections)
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,  // Maximum 20 connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

async function getHandoff(id: string) {
  const result = await pool.query('SELECT * FROM handoffs WHERE id = $1', [id]);
  return result.rows[0];
}
```

### 2. SQL Injection Prevention

**PROBLEM**:
```typescript
// BAD: String concatenation (SQL injection vulnerable!)
const result = await db.query(
  `SELECT * FROM handoffs WHERE id = '${handoffId}'`
);
// Attacker sends: handoffId = "'; DROP TABLE handoffs; --"
// Executes: SELECT * FROM handoffs WHERE id = ''; DROP TABLE handoffs; --'
```

**SOLUTION**:
```typescript
// GOOD: Parameterized queries (PostgreSQL handles escaping)
const result = await db.query(
  'SELECT * FROM handoffs WHERE id = $1',
  [handoffId]
);
```

### 3. Error Handling in Async Functions

**PROBLEM**:
```typescript
// BAD: Unhandled promise rejection (crashes server)
app.post('/v1/handoffs', async (req, res) => {
  const handoff = await createHandoff(req.body);  // If this throws, server crashes!
  res.json({ success: true, data: handoff });
});
```

**SOLUTION**:
```typescript
// GOOD: Global error handler
app.post('/v1/handoffs', async (req, res, next) => {
  try {
    const handoff = await createHandoff(req.body);
    res.json({ success: true, data: handoff });
  } catch (error) {
    next(error);  // Pass to error middleware
  }
});

// Or use express-async-errors package (auto-wraps async functions)
import 'express-async-errors';

app.post('/v1/handoffs', async (req, res) => {
  const handoff = await createHandoff(req.body);  // Errors automatically caught
  res.json({ success: true, data: handoff });
});
```

### 4. Race Conditions in Workers

**PROBLEM**:
```typescript
// BAD: Two workers process same job simultaneously
const job = await queue.getNextJob();
await processJob(job);  // If this takes 10 seconds, another worker might grab same job!
await job.complete();
```

**SOLUTION**:
```typescript
// GOOD: BullMQ handles locking automatically
const worker = new Worker('transcription', async (job) => {
  // BullMQ ensures only ONE worker processes this job
  // Job is locked until worker completes or crashes
  await processJob(job);
});
```

### 5. Memory Leaks in File Uploads

**PROBLEM**:
```typescript
// BAD: Load entire file into memory
app.post('/v1/voice/upload', async (req, res) => {
  const fileBuffer = req.file.buffer;  // 50 MB file = 50 MB memory usage!
  await uploadToR2(fileBuffer);
});
// With 100 concurrent uploads = 5 GB memory usage!
```

**SOLUTION**:
```typescript
// GOOD: Stream file directly to R2
app.post('/v1/voice/upload', async (req, res) => {
  const fileStream = req.file.stream;  // Stream chunks (64 KB at a time)
  await uploadToR2Stream(fileStream);
});
// 100 concurrent uploads = ~6.4 MB memory usage
```

---

## Summary: Key Takeaways

### Architecture Decisions

1. **Monorepo**: Shared types between frontend/backend, easier refactoring
2. **TypeScript**: Catch errors at compile time, self-documenting code
3. **PostgreSQL**: ACID compliance, JSONB for flexible data, full-text search
4. **Worker Pattern**: Long AI tasks don't block API responses
5. **Service Layer**: Encapsulate external systems, easy to mock in tests

### AI/ML Best Practices

1. **Prompt Engineering**: Clear role, task, structure, guidelines, output format
2. **Context Management**: Initial vs update prompts (save tokens, improve quality)
3. **Quality Metrics**: Automated scoring flags low-quality reports
4. **Error Handling**: Retry logic, fallbacks, graceful degradation

### Security Principles

1. **Facility Isolation**: Row-Level Security at database level
2. **JWT Authentication**: Stateless, includes user context (facilityId, role)
3. **Audit Logging**: Every action logged for HIPAA compliance
4. **Parameterized Queries**: Prevent SQL injection

### Deployment Strategy

1. **Railway**: Simple Git-based deployment, auto-scaling
2. **Cloudflare Pages**: Edge network, automatic HTTPS, preview deployments
3. **Environment Variables**: Never commit secrets to Git
4. **Monitoring**: Logs, metrics, alerts for production issues

---

## Further Learning Resources

### Full-Stack Development
- **Next.js Docs**: https://nextjs.org/docs
- **Express.js Guide**: https://expressjs.com/en/guide/routing.html
- **PostgreSQL Tutorial**: https://www.postgresql.org/docs/current/tutorial.html
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook/

### AI/ML Integration
- **OpenAI Cookbook**: https://cookbook.openai.com/
- **Prompt Engineering Guide**: https://www.promptingguide.ai/
- **Azure OpenAI Docs**: https://learn.microsoft.com/en-us/azure/ai-services/openai/

### System Design
- **Designing Data-Intensive Applications** (Book by Martin Kleppmann)
- **System Design Primer**: https://github.com/donnemartin/system-design-primer

### Healthcare Tech
- **HIPAA Compliance Guide**: https://www.hhs.gov/hipaa/for-professionals/
- **SBAR Framework**: https://www.jointcommission.org/

---

**Questions to Test Your Understanding**:

1. Why do we use background workers instead of processing AI tasks in API endpoints?
2. What's the difference between an initial handoff prompt and an update handoff prompt?
3. How does Row-Level Security (RLS) prevent cross-facility data access?
4. Why is connection pooling important for database performance?
5. What happens if a worker crashes while processing a job?

**Next Steps**:
1. Set up local development environment
2. Deploy MVP to staging (Railway + Cloudflare Pages)
3. Add test data and walk through complete workflow
4. Monitor job queue and AI quality metrics
5. Plan v2 features based on user feedback

---

*This guide is a living document. As you implement features and encounter challenges, add your learnings here!*
