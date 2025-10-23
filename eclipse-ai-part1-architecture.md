# EclipseLink AI™ - Part 1: System Architecture Overview

**Document Version:** 1.0  
**Last Updated:** October 23, 2025  
**Product:** EclipseLink AI™ Clinical Handoff System  
**Company:** Rohimaya Health AI  
**Founders:** Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [High-Level Architecture](#high-level-architecture)
3. [Technology Stack Recommendations](#technology-stack-recommendations)
4. [System Components](#system-components)
5. [Data Flow Architecture](#data-flow-architecture)
6. [Deployment Architecture](#deployment-architecture)
7. [Scalability & Performance](#scalability-performance)
8. [Integration Points](#integration-points)
9. [Security Architecture](#security-architecture)
10. [Monitoring & Observability](#monitoring-observability)

---

## 1. Executive Summary

### Product Overview
EclipseLink AI™ is a voice-enabled clinical handoff platform that transforms spoken patient reports into structured SBAR (Situation, Background, Assessment, Recommendation) documentation using advanced AI. The system serves 9,022,020 healthcare professionals across 15 disciplines in hospitals, clinics, and care facilities nationwide.

### Core Value Proposition
- **Voice-to-SBAR Conversion**: Transforms 3-5 minute voice recordings into comprehensive SBAR reports in under 30 seconds
- **EHR Integration**: Seamlessly connects with Epic, Cerner, MEDITECH, and other major EHR systems
- **Multi-Platform Access**: Progressive Web App (PWA) accessible on mobile, tablet, and desktop
- **HIPAA Compliant**: End-to-end encrypted with comprehensive audit trails

### Target Market
- **Total Addressable Market (TAM)**: $18.9 billion healthcare communication market
- **Primary Users**: RNs, MDs, LPNs, CNAs, MAs, NPs, PAs, RTs, PTs, OTs, EMTs, Radiologic Techs, Surgical Techs, Lab Techs, Pharmacy Techs
- **Facilities**: 6,090 hospitals, 87,000+ nursing homes, 13,000+ clinics in the US

---

## 2. High-Level Architecture

### Architecture Pattern
EclipseLink AI follows a **modern microservices architecture** with the following characteristics:

- **Frontend**: Progressive Web App (PWA) built with React/Next.js
- **Backend**: RESTful API services with serverless functions
- **AI Services**: Azure OpenAI integration (Whisper + GPT-4)
- **Database**: PostgreSQL with read replicas
- **Storage**: Object storage for voice recordings and documents
- **Cache**: Redis for session management and performance
- **Queue**: Message queue for async processing

### Architectural Diagram (Text-Based)

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Mobile  │  │  Tablet  │  │ Desktop  │  │   Kiosk  │       │
│  │   PWA    │  │   PWA    │  │   PWA    │  │   Mode   │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
└───────┼─────────────┼─────────────┼─────────────┼──────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
        ┌─────────────▼──────────────┐
        │   CLOUDFLARE CDN + WAF     │  (Global Edge Network)
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────┐
        │   API GATEWAY / LOAD       │
        │   BALANCER                 │
        │   (Cloudflare Workers)     │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────────────────────────────────┐
        │              BACKEND SERVICES LAYER                     │
        │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
        │  │ Auth Service │  │ API Service  │  │ Voice Service│ │
        │  │  (Supabase)  │  │  (Railway)   │  │  (Railway)   │ │
        │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
        └─────────┼──────────────────┼──────────────────┼─────────┘
                  │                  │                  │
        ┌─────────▼──────────────────▼──────────────────▼─────────┐
        │              INTEGRATION LAYER                           │
        │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
        │  │ Azure OpenAI │  │ EHR Connector│  │ Redis Cache  │ │
        │  │ (Whisper +   │  │ (Epic FHIR)  │  │ (Upstash)    │ │
        │  │  GPT-4)      │  │              │  │              │ │
        │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
        └─────────┼──────────────────┼──────────────────┼─────────┘
                  │                  │                  │
        ┌─────────▼──────────────────▼──────────────────▼─────────┐
        │              DATA LAYER                                  │
        │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
        │  │  PostgreSQL  │  │ Object Store │  │ Message Queue│ │
        │  │  (Supabase)  │  │ (Cloudflare  │  │ (BullMQ +    │ │
        │  │              │  │  R2)         │  │  Redis)      │ │
        │  └──────────────┘  └──────────────┘  └──────────────┘ │
        └──────────────────────────────────────────────────────────┘
                  │                  │                  │
        ┌─────────▼──────────────────▼──────────────────▼─────────┐
        │              EXTERNAL INTEGRATIONS                       │
        │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
        │  │   Epic EHR   │  │  Cerner EHR  │  │  MEDITECH    │ │
        │  │   (FHIR)     │  │   (FHIR)     │  │   (HL7)      │ │
        │  └──────────────┘  └──────────────┘  └──────────────┘ │
        └──────────────────────────────────────────────────────────┘
```

---

## 3. Technology Stack Recommendations

### Frontend Stack

#### Primary Framework: **Next.js 14+ (React 18+)**
- **Why**: Server-side rendering (SSR), static generation, API routes, excellent SEO
- **Features Needed**:
  - App Router (for modern routing)
  - Server Components (for performance)
  - API Routes (for BFF pattern)
  - Image optimization
  - PWA capabilities

#### UI Framework: **Tailwind CSS + shadcn/ui**
- **Why**: Utility-first CSS, component library, accessibility built-in
- **Components**:
  - shadcn/ui for base components (buttons, forms, modals)
  - Custom healthcare-specific components
  - Responsive design system

#### State Management: **Zustand + React Query**
- **Zustand**: Lightweight global state (user session, app settings)
- **React Query**: Server state management (API calls, caching)
- **Why**: Simple, performant, minimal boilerplate

#### Voice Recording: **MediaRecorder API + Web Audio API**
- **Native browser APIs** for audio capture
- **Fallback**: RecordRTC library for older browsers
- **Format**: WebM/Opus for best compression

#### PWA: **next-pwa**
- **Features**:
  - Offline capability
  - Install prompts
  - Background sync
  - Push notifications
  - Service workers

### Backend Stack

#### Primary Platform: **Railway.app**
- **Why**: 
  - Simple deployment from GitHub/GitLab
  - Automatic HTTPS
  - Environment management
  - Integrated PostgreSQL
  - Competitive pricing ($5-20/month per service)
  - Excellent for startups

#### API Framework: **Node.js + Express.js** OR **Next.js API Routes**
**Option A: Separate Backend (Railway)**
- Express.js with TypeScript
- Better for microservices
- More control over architecture

**Option B: Integrated Backend (Next.js API Routes)**
- Simpler deployment
- Unified codebase
- Better for monolith start

**Recommendation**: Start with Next.js API Routes, migrate to separate backend when scaling

#### Alternative Backend: **Python + FastAPI** (for AI-heavy operations)
- Better for Azure OpenAI integration
- Async support
- Type safety with Pydantic
- Deploy alongside Node.js services

### Database Stack

#### Primary Database: **Supabase (PostgreSQL)**
- **Why**:
  - Managed PostgreSQL
  - Built-in authentication
  - Real-time subscriptions
  - Row-level security (RLS)
  - Generous free tier
  - Built-in storage
  - RESTful APIs auto-generated

#### Features Needed:
- PostgreSQL 15+
- Row-Level Security (RLS) for HIPAA
- Point-in-time recovery
- Automated backups
- Read replicas (for scaling)

#### Alternative: **Neon** (Serverless Postgres)
- Serverless architecture
- Instant branching
- Scale-to-zero
- Cost-effective

### AI Services Stack

#### Speech-to-Text: **Azure OpenAI Whisper API**
- **Endpoint**: `https://YOUR-RESOURCE.openai.azure.com/openai/deployments/whisper/audio/transcriptions`
- **Model**: whisper-1
- **Features**:
  - Medical terminology recognition
  - Multi-language support
  - High accuracy (95%+ on medical terms)
  - HIPAA BAA available

#### Text Generation: **Azure OpenAI GPT-4**
- **Endpoint**: `https://YOUR-RESOURCE.openai.azure.com/openai/deployments/gpt-4/chat/completions`
- **Model**: gpt-4-32k (for long patient reports)
- **Features**:
  - SBAR structuring
  - Clinical intelligence
  - Context awareness
  - Consistent formatting

#### Configuration:
```javascript
const azureOpenAI = {
  apiKey: process.env.AZURE_OPENAI_KEY,
  apiVersion: "2024-02-15-preview",
  endpoint: process.env.AZURE_OPENAI_ENDPOINT,
  deployments: {
    whisper: "whisper-deployment-name",
    gpt4: "gpt-4-deployment-name"
  }
}
```

### Storage & Cache Stack

#### Object Storage: **Cloudflare R2**
- **Why**:
  - S3-compatible API
  - No egress fees
  - Global CDN
  - Cost-effective ($0.015/GB/month)
- **Usage**:
  - Voice recordings (.webm, .mp3)
  - Generated documents (.pdf, .docx)
  - Profile images

#### Cache: **Upstash Redis**
- **Why**:
  - Serverless Redis
  - Per-request pricing
  - Global replication
  - REST API
- **Usage**:
  - Session management
  - Rate limiting
  - API response caching
  - Real-time features

### Authentication Stack

#### Recommended: **Supabase Auth**
- **Why**:
  - Built into Supabase
  - JWT-based
  - MFA support
  - Social login options
  - Row-level security integration
  - HIPAA compliant configuration

#### Features:
- Email/password authentication
- Magic link login
- MFA (TOTP, SMS)
- OAuth providers (optional)
- Secure session management
- Automatic token refresh

#### Alternative: **Auth0**
- More enterprise features
- Better for complex SSO
- Higher cost

### Message Queue Stack

#### Recommended: **BullMQ + Upstash Redis**
- **Why**:
  - Robust job processing
  - Retries and error handling
  - Delayed jobs
  - Job prioritization
- **Usage**:
  - Voice transcription queue
  - SBAR generation queue
  - EHR sync jobs
  - Email notifications
  - Report generation

### Monitoring & Observability Stack

#### Application Monitoring: **Sentry**
- Error tracking
- Performance monitoring
- Release tracking
- Free tier: 5K events/month

#### Logging: **Better Stack (formerly Logtail)**
- Structured logging
- Real-time search
- Alerting
- Compliance logging (HIPAA audit trail)

#### Uptime Monitoring: **BetterUptime**
- Endpoint monitoring
- SSL monitoring
- Status page
- Incident management

#### Analytics: **PostHog** (self-hosted or cloud)
- Product analytics
- Feature flags
- Session recording
- Funnels and retention
- HIPAA-compliant configuration

---

## 4. System Components

### 4.1 Frontend Components

#### A. Progressive Web App (PWA)
**Technology**: Next.js 14 + next-pwa

**Key Features**:
- Installable on all devices
- Offline functionality
- Background sync
- Push notifications
- Auto-updates

**Structure**:
```
/app
  /(auth)
    /login
    /register
    /forgot-password
  /(dashboard)
    /dashboard
    /handoffs
      /new
      /[id]
    /patients
      /[id]
    /profile
    /settings
  /api
    /auth
    /handoffs
    /patients
    /voice
```

#### B. Voice Recording Interface
**Component**: `VoiceRecorder.tsx`

**Features**:
- One-tap recording start/stop
- Real-time waveform visualization
- Duration counter
- Pause/resume capability
- Audio preview before submission
- Offline recording with background sync

**Technical Implementation**:
```typescript
interface VoiceRecorderProps {
  onRecordingComplete: (blob: Blob, duration: number) => void;
  maxDuration?: number; // default 300 seconds (5 min)
  patientId: string;
}

// Uses MediaRecorder API
// Format: audio/webm;codecs=opus
// Bitrate: 32kbps (optimized for voice)
```

#### C. SBAR Display Interface
**Component**: `SBARDisplay.tsx`

**Sections**:
1. **Situation** (Patient identification, vital signs, chief complaint)
2. **Background** (Medical history, medications, allergies)
3. **Assessment** (Clinical findings, diagnosis, test results)
4. **Recommendation** (Interventions, orders, follow-up)

**Features**:
- Collapsible sections
- Edit capability (inline editing)
- Version history
- Export options (PDF, DOCX, copy to clipboard)
- Share to EHR button

#### D. Patient Dashboard
**Component**: `PatientDashboard.tsx`

**Features**:
- Patient list with search and filters
- Recent handoffs timeline
- Quick access to patient records
- Alerts and notifications
- Scheduled handoffs

#### E. Handoff History
**Component**: `HandoffHistory.tsx`

**Features**:
- Chronological list of all handoffs
- Filter by date, provider, patient, facility
- Search functionality
- Export bulk reports
- Analytics dashboard

### 4.2 Backend Services

#### A. Authentication Service
**Endpoint Base**: `/api/auth`

**Responsibilities**:
- User registration and login
- Token generation and validation
- Multi-factor authentication
- Password reset
- Session management
- Role-based access control (RBAC)

**Endpoints**:
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/refresh
POST   /api/auth/forgot-password
POST   /api/auth/reset-password
POST   /api/auth/verify-mfa
GET    /api/auth/me
```

#### B. Voice Processing Service
**Endpoint Base**: `/api/voice`

**Responsibilities**:
- Voice upload handling
- Audio format validation
- Storage in Cloudflare R2
- Queue job for transcription
- Progress tracking
- Error handling and retries

**Endpoints**:
```
POST   /api/voice/upload
GET    /api/voice/status/:jobId
DELETE /api/voice/:recordingId
GET    /api/voice/:recordingId/download
```

**Processing Flow**:
1. Client uploads voice file
2. Service validates format and size
3. Uploads to R2 storage
4. Creates transcription job in queue
5. Returns job ID to client
6. Client polls for status
7. On completion, transcription is stored

#### C. AI Processing Service
**Endpoint Base**: `/api/ai`

**Responsibilities**:
- Whisper API transcription
- GPT-4 SBAR generation
- Medical terminology validation
- Quality assurance checks
- Retry logic with exponential backoff

**Endpoints**:
```
POST   /api/ai/transcribe
POST   /api/ai/generate-sbar
POST   /api/ai/refine-sbar
GET    /api/ai/job/:jobId
```

**Whisper Integration**:
```typescript
async function transcribeAudio(audioBuffer: Buffer): Promise<string> {
  const formData = new FormData();
  formData.append('file', audioBuffer, 'recording.webm');
  formData.append('model', 'whisper-1');
  formData.append('language', 'en');
  formData.append('response_format', 'verbose_json');

  const response = await axios.post(
    `${AZURE_OPENAI_ENDPOINT}/openai/deployments/whisper/audio/transcriptions`,
    formData,
    {
      headers: {
        'api-key': AZURE_OPENAI_KEY,
        'Content-Type': 'multipart/form-data'
      },
      params: {
        'api-version': '2024-02-15-preview'
      }
    }
  );

  return response.data.text;
}
```

**GPT-4 SBAR Generation**:
```typescript
async function generateSBAR(transcription: string, patientContext: PatientContext): Promise<SBAR> {
  const prompt = `You are a clinical documentation assistant. Convert the following voice transcription into a structured SBAR format.

Patient Context:
- Name: ${patientContext.name}
- MRN: ${patientContext.mrn}
- Age: ${patientContext.age}
- Primary Diagnosis: ${patientContext.primaryDiagnosis}

Transcription:
${transcription}

Generate a comprehensive SBAR report following these guidelines:
- Situation: Current patient status, vital signs, chief complaint
- Background: Relevant medical history, current medications, allergies
- Assessment: Clinical findings, diagnosis, lab/test results
- Recommendation: Proposed interventions, orders, follow-up plans

Format the response as JSON with keys: situation, background, assessment, recommendation`;

  const response = await axios.post(
    `${AZURE_OPENAI_ENDPOINT}/openai/deployments/gpt-4/chat/completions`,
    {
      messages: [
        { role: 'system', content: 'You are an expert clinical documentation assistant.' },
        { role: 'user', content: prompt }
      ],
      temperature: 0.3,
      max_tokens: 2000,
      response_format: { type: 'json_object' }
    },
    {
      headers: {
        'api-key': AZURE_OPENAI_KEY,
        'Content-Type': 'application/json'
      },
      params: {
        'api-version': '2024-02-15-preview'
      }
    }
  );

  return JSON.parse(response.data.choices[0].message.content);
}
```

#### D. Handoff Service
**Endpoint Base**: `/api/handoffs`

**Responsibilities**:
- CRUD operations for handoffs
- Handoff status management
- Assignment to receiving provider
- Notification triggers
- Handoff validation
- Compliance tracking

**Endpoints**:
```
POST   /api/handoffs              (Create new handoff)
GET    /api/handoffs              (List handoffs with filters)
GET    /api/handoffs/:id          (Get handoff details)
PUT    /api/handoffs/:id          (Update handoff)
DELETE /api/handoffs/:id          (Delete handoff)
POST   /api/handoffs/:id/complete (Mark handoff complete)
POST   /api/handoffs/:id/assign   (Assign to provider)
GET    /api/handoffs/:id/history  (Version history)
```

#### E. Patient Service
**Endpoint Base**: `/api/patients`

**Responsibilities**:
- Patient demographics
- Medical history
- Medication list
- Allergy information
- Recent handoffs
- EHR synchronization

**Endpoints**:
```
POST   /api/patients              (Create patient record)
GET    /api/patients              (Search/list patients)
GET    /api/patients/:id          (Get patient details)
PUT    /api/patients/:id          (Update patient)
GET    /api/patients/:id/handoffs (Patient handoff history)
POST   /api/patients/:id/sync-ehr (Sync with EHR)
```

#### F. EHR Integration Service
**Endpoint Base**: `/api/ehr`

**Responsibilities**:
- FHIR API communication (Epic)
- HL7 message handling (MEDITECH)
- Patient data sync
- Handoff export to EHR
- Medication reconciliation
- Allergy cross-reference

**Endpoints**:
```
POST   /api/ehr/connect           (Initialize EHR connection)
GET    /api/ehr/patient/:mrn      (Fetch patient from EHR)
POST   /api/ehr/handoff/export    (Export handoff to EHR)
POST   /api/ehr/sync              (Full data sync)
GET    /api/ehr/status            (Connection status)
```

**Epic FHIR Integration Example**:
```typescript
async function fetchEpicPatient(mrn: string): Promise<EpicPatient> {
  // Epic FHIR R4 API
  const response = await axios.get(
    `${EPIC_FHIR_BASE_URL}/Patient`,
    {
      params: {
        identifier: `urn:oid:YOUR_FACILITY_OID|${mrn}`
      },
      headers: {
        'Authorization': `Bearer ${epicAccessToken}`,
        'Accept': 'application/fhir+json',
        'Epic-Client-ID': EPIC_CLIENT_ID
      }
    }
  );

  return transformFHIRToPatient(response.data);
}
```

### 4.3 Data Layer Components

#### A. PostgreSQL Database (Supabase)
**Configuration**:
```yaml
Database: PostgreSQL 15
Connection Pooling: Supavisor (PgBouncer)
Backups: Daily automated with 7-day retention
Encryption: AES-256 at rest
SSL: Required for all connections
```

**Tables**: (Detailed in Part 3: Database Schema)
- facilities
- staff
- patients
- handoffs
- voice_recordings
- ai_generations
- sbar_reports
- handoff_assignments
- audit_logs
- notifications
- ehr_connections
- ehr_sync_logs
- user_sessions
- feature_flags
- system_settings

#### B. Object Storage (Cloudflare R2)
**Buckets**:
```
eclipselink-voice-recordings/
  ├── 2025/
  │   ├── 10/
  │   │   ├── {facilityId}/
  │   │   │   ├── {recordingId}.webm
  │   │   │   └── {recordingId}.mp3

eclipselink-documents/
  ├── sbar-reports/
  │   ├── {handoffId}.pdf
  │   └── {handoffId}.docx
  ├── exports/
  │   └── bulk-export-{timestamp}.zip

eclipselink-user-uploads/
  ├── avatars/
  │   └── {userId}.jpg
```

**Access Control**:
- Pre-signed URLs for voice playback (15-minute expiry)
- Server-side encryption
- CORS configuration for frontend access

#### C. Cache Layer (Upstash Redis)
**Cache Strategy**:
```typescript
// Session cache
Key: `session:${userId}`
TTL: 24 hours
Value: { userId, facilityId, role, permissions }

// Patient cache
Key: `patient:${patientId}`
TTL: 1 hour
Value: { demographics, vitals, medications, allergies }

// API response cache
Key: `api:${endpoint}:${params}`
TTL: 5 minutes
Value: JSON response

// Rate limiting
Key: `ratelimit:${userId}:${action}`
TTL: 1 minute
Value: Request count
```

---

## 5. Data Flow Architecture

### 5.1 Voice-to-SBAR Data Flow

```
┌──────────────┐
│   Clinician  │
│  Records     │
│  Voice (3min)│
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  STEP 1: Voice Capture (Frontend)        │
│  - MediaRecorder API captures audio      │
│  - Format: audio/webm (Opus codec)       │
│  - Real-time waveform display            │
│  - Duration: 0-5 minutes                 │
└──────┬───────────────────────────────────┘
       │
       ▼ POST /api/voice/upload
┌──────────────────────────────────────────┐
│  STEP 2: Voice Upload (Backend)          │
│  - Validate audio format                 │
│  - Generate unique recordingId           │
│  - Upload to Cloudflare R2               │
│  - Create database record                │
│  - Return: { recordingId, uploadUrl }    │
└──────┬───────────────────────────────────┘
       │
       ▼ Queue Job
┌──────────────────────────────────────────┐
│  STEP 3: Transcription Queue (BullMQ)    │
│  - Job Type: "voice-transcription"       │
│  - Priority: HIGH                        │
│  - Retry: 3 attempts with backoff        │
│  - Payload: { recordingId, audioUrl }    │
└──────┬───────────────────────────────────┘
       │
       ▼ Process Job
┌──────────────────────────────────────────┐
│  STEP 4: Azure Whisper API               │
│  - Download audio from R2                │
│  - Call Whisper API                      │
│  - Model: whisper-1                      │
│  - Response: Full transcription text     │
│  - Processing Time: 15-30 seconds        │
└──────┬───────────────────────────────────┘
       │
       ▼ Store Transcription
┌──────────────────────────────────────────┐
│  STEP 5: Save Transcription (DB)         │
│  - Update voice_recordings table         │
│  - Create ai_generations record          │
│  - Status: "transcribed"                 │
└──────┬───────────────────────────────────┘
       │
       ▼ Queue SBAR Job
┌──────────────────────────────────────────┐
│  STEP 6: SBAR Generation Queue           │
│  - Job Type: "sbar-generation"           │
│  - Fetch patient context from DB         │
│  - Payload: { transcription, patient }   │
└──────┬───────────────────────────────────┘
       │
       ▼ Process Job
┌──────────────────────────────────────────┐
│  STEP 7: Azure GPT-4 API                 │
│  - Build prompt with context             │
│  - Call GPT-4 (gpt-4-32k)                │
│  - Parse JSON response                   │
│  - Validate SBAR structure               │
│  - Processing Time: 10-20 seconds        │
└──────┬───────────────────────────────────┘
       │
       ▼ Store SBAR
┌──────────────────────────────────────────┐
│  STEP 8: Save SBAR Report (DB)           │
│  - Create sbar_reports record            │
│  - Link to handoff                       │
│  - Update handoff status: "ready"        │
│  - Trigger notification                  │
└──────┬───────────────────────────────────┘
       │
       ▼ WebSocket/Polling
┌──────────────────────────────────────────┐
│  STEP 9: Notify Frontend                 │
│  - Push notification to clinician        │
│  - Update UI with completed SBAR         │
│  - Enable edit/review/export options     │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  STEP 10: Clinician Review & Approval    │
│  - Review generated SBAR                 │
│  - Edit if necessary                     │
│  - Approve and complete handoff          │
│  - Export to EHR (optional)              │
└──────────────────────────────────────────┘

Total Time: 30-60 seconds from upload to SBAR
```

### 5.2 EHR Integration Data Flow

```
┌──────────────┐
│  Clinician   │
│  Initiates   │
│  EHR Sync    │
└──────┬───────┘
       │
       ▼ POST /api/ehr/patient/:mrn
┌──────────────────────────────────────────┐
│  STEP 1: EHR Connection Validation       │
│  - Check active EHR connection           │
│  - Validate credentials/tokens           │
│  - Determine EHR type (Epic/Cerner/etc)  │
└──────┬───────────────────────────────────┘
       │
       ▼ Epic FHIR API
┌──────────────────────────────────────────┐
│  STEP 2: Fetch Patient from Epic         │
│  - FHIR R4 API call                      │
│  - Endpoint: GET /Patient?identifier=MRN │
│  - Auth: OAuth 2.0 Bearer token          │
│  - Response: FHIR Patient resource       │
└──────┬───────────────────────────────────┘
       │
       ▼ Transform Data
┌──────────────────────────────────────────┐
│  STEP 3: FHIR to Internal Model          │
│  - Parse FHIR Patient resource           │
│  - Map to internal patient schema        │
│  - Fetch related resources:              │
│    • MedicationStatement                 │
│    • AllergyIntolerance                  │
│    • Condition (diagnoses)               │
│    • Observation (vitals)                │
└──────┬───────────────────────────────────┘
       │
       ▼ Store Data
┌──────────────────────────────────────────┐
│  STEP 4: Update Internal Database        │
│  - Upsert patient record                 │
│  - Update medications                    │
│  - Update allergies                      │
│  - Update diagnoses                      │
│  - Log sync in ehr_sync_logs             │
└──────┬───────────────────────────────────┘
       │
       ▼ Return to Frontend
┌──────────────────────────────────────────┐
│  STEP 5: Display Synced Data             │
│  - Show patient demographics             │
│  - Display medication list               │
│  - Show allergy alerts                   │
│  - Ready for handoff creation            │
└──────────────────────────────────────────┘
```

### 5.3 Handoff Completion Data Flow

```
┌──────────────┐
│  Clinician   │
│  Completes   │
│  Handoff     │
└──────┬───────┘
       │
       ▼ POST /api/handoffs/:id/complete
┌──────────────────────────────────────────┐
│  STEP 1: Validate Handoff                │
│  - Check handoff exists                  │
│  - Verify clinician authorization        │
│  - Ensure SBAR is complete               │
│  - Validate receiving provider assigned  │
└──────┬───────────────────────────────────┘
       │
       ▼ Update Database
┌──────────────────────────────────────────┐
│  STEP 2: Update Handoff Status           │
│  - Set status: "completed"               │
│  - Set completed_at timestamp            │
│  - Log in audit_logs table               │
│  - Update handoff_assignments            │
└──────┬───────────────────────────────────┘
       │
       ▼ Notify Receiving Provider
┌──────────────────────────────────────────┐
│  STEP 3: Send Notifications              │
│  - Create notification record            │
│  - Send push notification (if enabled)   │
│  - Send email (if configured)            │
│  - Update notification badge count       │
└──────┬───────────────────────────────────┘
       │
       ▼ Optional EHR Export
┌──────────────────────────────────────────┐
│  STEP 4: Export to EHR (if enabled)      │
│  - Generate HL7 ADT message (MEDITECH)   │
│  - OR Create FHIR Communication (Epic)   │
│  - Send to EHR endpoint                  │
│  - Log export status                     │
└──────┬───────────────────────────────────┘
       │
       ▼ Analytics & Compliance
┌──────────────────────────────────────────┐
│  STEP 5: Log for Analytics               │
│  - Track handoff completion time         │
│  - Calculate processing metrics          │
│  - Joint Commission compliance tracking  │
│  - Quality improvement data              │
└──────────────────────────────────────────┘
```

---

## 6. Deployment Architecture

### 6.1 Recommended Deployment Strategy

**Overview**: Multi-region serverless architecture with global CDN

```
PRODUCTION ENVIRONMENT
├── Frontend: Cloudflare Pages (Global CDN)
├── Backend: Railway.app (US-East + US-West)
├── Database: Supabase (US-East, with read replica in US-West)
├── Storage: Cloudflare R2 (Global, multi-region)
├── Cache: Upstash Redis (Global, multi-region)
└── AI: Azure OpenAI (US-East)
```

### 6.2 Infrastructure Components

#### A. Frontend Deployment (Cloudflare Pages)

**Configuration**:
```yaml
Project: eclipselink-ai-frontend
Branch: main (production), develop (staging)
Build Command: npm run build
Output Directory: .next
Node Version: 18.x
Environment Variables:
  - NEXT_PUBLIC_API_URL
  - NEXT_PUBLIC_SUPABASE_URL
  - NEXT_PUBLIC_SUPABASE_ANON_KEY
  - NEXT_PUBLIC_POSTHOG_KEY
```

**Features**:
- Automatic deployments from Git push
- Preview deployments for PRs
- Global CDN (300+ locations)
- DDoS protection
- Web Application Firewall (WAF)
- SSL/TLS automatic
- IPv6 support

**Custom Domain**:
```
Production: app.eclipselink.ai
Staging: staging.eclipselink.ai
```

**Cloudflare Settings**:
```yaml
Always Use HTTPS: Enabled
Auto Minify: JS, CSS, HTML
Brotli Compression: Enabled
HTTP/2: Enabled
HTTP/3 (QUIC): Enabled
Early Hints: Enabled
```

#### B. Backend Deployment (Railway.app)

**Service Configuration**:

**Service 1: API Server**
```yaml
Name: eclipselink-api
Source: GitHub repo (backend/)
Build Command: npm run build
Start Command: npm run start
Region: us-east
Instance: Shared CPU, 512MB RAM (start), Auto-scale to 2GB
Environment Variables:
  - DATABASE_URL (from Railway PostgreSQL)
  - AZURE_OPENAI_KEY
  - AZURE_OPENAI_ENDPOINT
  - CLOUDFLARE_R2_ACCESS_KEY
  - CLOUDFLARE_R2_SECRET_KEY
  - REDIS_URL (Upstash)
  - SUPABASE_SERVICE_KEY
  - JWT_SECRET
  - SENTRY_DSN
Health Check: /api/health
```

**Service 2: Worker Service (Background Jobs)**
```yaml
Name: eclipselink-worker
Source: Same GitHub repo (workers/)
Start Command: npm run worker
Region: us-east
Instance: Shared CPU, 1GB RAM
Environment Variables: (same as API Server)
```

**Railway Advantages**:
- Automatic HTTPS
- Zero-downtime deployments
- Automatic rollbacks
- GitHub integration
- Environment variable management
- Built-in observability
- Simple pricing ($5/month base + usage)

**Alternative**: Vercel (for Next.js full-stack)
```yaml
Project: eclipselink-ai
Framework: Next.js
Build Command: npm run build
Output Directory: .next
Serverless Functions: Auto-detected
Edge Functions: Yes (for auth middleware)
Regions: Global edge network
```

#### C. Database Deployment (Supabase)

**Project Configuration**:
```yaml
Project: eclipselink-production
Region: us-east-1
Plan: Pro ($25/month)
Database: PostgreSQL 15
Instance: 2 vCPU, 4GB RAM
Storage: 8GB (expandable to 500GB)
Connection Limit: 60 (with Supavisor pooling)
```

**Features Enabled**:
- Row Level Security (RLS)
- Realtime subscriptions
- PostgREST API
- Storage buckets
- Auth (for internal use)
- Point-in-time recovery (7 days)

**Backup Strategy**:
```yaml
Automated Daily Backups: Enabled
Retention: 7 days
Manual Backups: Weekly (kept for 30 days)
Export Location: Cloudflare R2
```

**Read Replica** (for scaling):
```yaml
Region: us-west-2
Purpose: Read-only queries (analytics, reporting)
Lag: < 1 second
Failover: Manual
```

**Connection Pooling** (Supavisor):
```yaml
Mode: Transaction
Max Connections: 60
Pool Size: 15 per worker
Timeout: 30 seconds
```

#### D. Storage Deployment (Cloudflare R2)

**Bucket Configuration**:
```yaml
Bucket: eclipselink-production
Region: Auto (globally distributed)
Access: Private (pre-signed URLs only)
CORS: Configured for app.eclipselink.ai
Lifecycle Rules:
  - Voice recordings: Delete after 90 days
  - SBAR PDFs: Retain indefinitely
  - Temporary files: Delete after 7 days
```

**Access Configuration**:
```javascript
// R2 Client Setup
const r2Client = new S3Client({
  region: 'auto',
  endpoint: 'https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com',
  credentials: {
    accessKeyId: process.env.R2_ACCESS_KEY,
    secretAccessKey: process.env.R2_SECRET_KEY
  }
});

// Pre-signed URL generation (15 min expiry)
const getSignedUrl = (key: string) => {
  return getSignedUrl(r2Client, new GetObjectCommand({
    Bucket: 'eclipselink-production',
    Key: key
  }), {
    expiresIn: 900 // 15 minutes
  });
};
```

**Cost Estimate**:
```
Storage: 100GB @ $0.015/GB = $1.50/month
Class A Operations: 1M @ $4.50/million = $4.50/month
Class B Operations: 10M @ $0.36/million = $3.60/month
Egress: $0 (no egress fees!)
Total: ~$10/month
```

#### E. Cache Deployment (Upstash Redis)

**Configuration**:
```yaml
Database: eclipselink-cache
Region: Global (multi-region replication)
Type: Pay-as-you-go
Max Commands: 10,000/day (free tier), then $0.2/100K
Max Bandwidth: 200MB/day (free tier), then $0.2/GB
Persistence: Enabled
TLS: Required
Eviction: allkeys-lru
```

**Redis URL**:
```
redis://YOUR_USERNAME:YOUR_PASSWORD@global-evident-12345.upstash.io:6379
```

**Usage**:
```typescript
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_URL,
  token: process.env.UPSTASH_REDIS_TOKEN
});

// Session cache
await redis.setex(`session:${userId}`, 86400, JSON.stringify(session));

// Rate limiting
const count = await redis.incr(`ratelimit:${userId}:upload`);
await redis.expire(`ratelimit:${userId}:upload`, 60);
if (count > 10) throw new Error('Rate limit exceeded');
```

#### F. AI Services Deployment (Azure OpenAI)

**Resource Configuration**:
```yaml
Resource Name: eclipselink-openai
Region: East US
Pricing Tier: Standard
Deployment Name: eclipselink-prod
```

**Whisper Deployment**:
```yaml
Model: whisper
Version: Latest
Capacity: 10 requests/minute (adjustable)
Endpoint: https://eclipselink-openai.openai.azure.com/openai/deployments/whisper/audio/transcriptions
```

**GPT-4 Deployment**:
```yaml
Model: gpt-4-32k
Version: 0613
Capacity: 20 requests/minute (adjustable)
Endpoint: https://eclipselink-openai.openai.azure.com/openai/deployments/gpt-4/chat/completions
```

**Cost Estimate** (per 1,000 handoffs):
```
Whisper (5 min audio avg): $0.006/min × 5 × 1,000 = $30
GPT-4 (2K tokens avg): $0.03/1K tokens × 2 × 1,000 = $60
Total: ~$90 per 1,000 handoffs = $0.09 per handoff
```

**Rate Limiting Strategy**:
```typescript
const rateLimiter = new Bottleneck({
  maxConcurrent: 5,
  minTime: 100, // 100ms between requests
  reservoir: 20, // 20 tokens
  reservoirRefreshAmount: 20,
  reservoirRefreshInterval: 60 * 1000 // Refill every minute
});

const transcribe = rateLimiter.wrap(transcribeAudio);
```

### 6.3 Environment Configuration

#### Development Environment
```yaml
Frontend: localhost:3000 (Next.js dev server)
Backend: localhost:4000 (Express or Next.js API)
Database: Supabase local (via Docker) or Dev project
Redis: Local Redis (Docker) or Upstash free tier
Storage: Local filesystem or R2 dev bucket
AI: Azure OpenAI dev resource
```

#### Staging Environment
```yaml
Frontend: staging.eclipselink.ai (Cloudflare Pages)
Backend: Railway staging service
Database: Supabase staging project
Redis: Upstash staging database
Storage: R2 staging bucket
AI: Azure OpenAI staging deployment
```

#### Production Environment
```yaml
Frontend: app.eclipselink.ai (Cloudflare Pages)
Backend: Railway production service (multi-region)
Database: Supabase production (with read replica)
Redis: Upstash global (multi-region)
Storage: R2 production bucket (global)
AI: Azure OpenAI production (with redundancy)
```

### 6.4 CI/CD Pipeline

#### GitHub Actions Workflow (Recommended)

**File**: `.github/workflows/deploy.yml`

```yaml
name: Deploy EclipseLink AI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run test
      - run: npm run lint

  deploy-frontend:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: eclipselink-ai
          directory: .next
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}

  deploy-backend:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: eclipselink-api

  database-migrations:
    needs: [deploy-backend]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Migrations
        run: |
          npm install
          npm run migrate:production
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

#### GitLab CI/CD Pipeline

**File**: `.gitlab-ci.yml`

```yaml
stages:
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "18"

test:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run test
    - npm run lint
  only:
    - main
    - develop
    - merge_requests

build-frontend:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - .next/
    expire_in: 1 hour
  only:
    - main

deploy-frontend:
  stage: deploy
  image: node:${NODE_VERSION}
  script:
    - npm install -g wrangler
    - npx wrangler pages publish .next --project-name=eclipselink-ai
  environment:
    name: production
    url: https://app.eclipselink.ai
  only:
    - main

deploy-backend:
  stage: deploy
  image: curlimages/curl:latest
  script:
    - curl -X POST $RAILWAY_WEBHOOK_URL
  environment:
    name: production
  only:
    - main
```

---

## 7. Scalability & Performance

### 7.1 Performance Targets

**Response Times**:
- Voice upload: < 2 seconds
- Transcription: < 30 seconds (for 5-min audio)
- SBAR generation: < 20 seconds
- API responses: < 200ms (p95)
- Page load time: < 2 seconds (LCP)

**Throughput Targets**:
- Concurrent users: 1,000+ per facility
- Handoffs/day: 100,000+
- Voice uploads/minute: 500+
- API requests/second: 1,000+

### 7.2 Scalability Strategy

#### Horizontal Scaling
```yaml
Frontend: Auto-scaled via Cloudflare CDN (unlimited)
Backend: Railway auto-scaling (up to 10 instances)
Database: Vertical scaling + read replicas
Workers: Scale based on queue depth
Cache: Global replication (Upstash)
```

#### Database Scaling
```sql
-- Read replica for analytics queries
CREATE PUBLICATION eclipselink_replica FOR ALL TABLES;

-- Partitioning for large tables
CREATE TABLE handoffs_2025_10 PARTITION OF handoffs
  FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');

-- Indexes for performance
CREATE INDEX idx_handoffs_facility_date ON handoffs(facility_id, created_at DESC);
CREATE INDEX idx_handoffs_patient ON handoffs(patient_id);
CREATE INDEX idx_handoffs_status ON handoffs(status) WHERE status != 'completed';
```

#### Caching Strategy
```typescript
// 3-tier caching
// L1: In-memory (Node.js)
// L2: Redis (Upstash)
// L3: Database

const cache = {
  async get(key: string) {
    // L1: Memory
    if (memoryCache.has(key)) return memoryCache.get(key);
    
    // L2: Redis
    const redisValue = await redis.get(key);
    if (redisValue) {
      memoryCache.set(key, redisValue);
      return redisValue;
    }
    
    // L3: Database
    const dbValue = await db.query(key);
    await redis.setex(key, 3600, dbValue);
    memoryCache.set(key, dbValue);
    return dbValue;
  }
};
```

#### CDN & Asset Optimization
```typescript
// Next.js Image optimization
import Image from 'next/image';

<Image
  src="/logo.png"
  alt="EclipseLink AI"
  width={200}
  height={50}
  priority
  quality={85}
/>

// Code splitting
const SBARDisplay = dynamic(() => import('@/components/SBARDisplay'), {
  loading: () => <Skeleton />,
  ssr: false
});
```

### 7.3 Performance Monitoring

**Key Metrics**:
```typescript
// Application Performance Monitoring
const metrics = {
  // Response time
  'api.response_time': histogram,
  'voice.upload.duration': histogram,
  'ai.transcription.duration': histogram,
  'ai.sbar_generation.duration': histogram,
  
  // Throughput
  'api.requests_per_second': gauge,
  'handoffs.created_per_minute': gauge,
  
  // Errors
  'api.error_rate': counter,
  'ai.transcription.failures': counter,
  
  // Business metrics
  'handoffs.completed': counter,
  'users.active': gauge
};
```

**Alerting Rules** (BetterUptime):
```yaml
- name: High API Error Rate
  condition: error_rate > 1%
  duration: 5m
  action: alert_on_call

- name: Slow Transcription
  condition: transcription_duration > 60s
  duration: 10m
  action: alert_team

- name: Database Connection Issues
  condition: db_connection_errors > 10
  duration: 2m
  action: alert_critical
```

---

## 8. Integration Points

### 8.1 External Integrations

#### Epic EHR (FHIR R4)
```yaml
Protocol: FHIR R4
Authentication: OAuth 2.0
Endpoints:
  - Patient: GET /Patient?identifier={MRN}
  - Medication: GET /MedicationStatement?patient={id}
  - Allergy: GET /AllergyIntolerance?patient={id}
  - Condition: GET /Condition?patient={id}
Data Exchange: JSON
```

#### Cerner (FHIR R4)
```yaml
Protocol: FHIR R4
Authentication: OAuth 2.0
Endpoints: Similar to Epic
Differences:
  - Different OAuth flow
  - Some proprietary extensions
  - Different date formats
```

#### MEDITECH (HL7 v2)
```yaml
Protocol: HL7 v2.x messages
Authentication: VPN + credentials
Message Types:
  - ADT^A01 (Admit patient)
  - ADT^A08 (Update patient)
  - ORU^R01 (Observation results)
Data Exchange: Pipe-delimited text
```

#### Protouch, PointClickCare, WellSky
```yaml
Protocol: Custom REST APIs or HL7
Authentication: API keys or OAuth
Data Exchange: JSON or XML
Status: Integration templates prepared
```

### 8.2 Internal Integrations (Future)

#### PlumeDose AI (Medication Management)
```yaml
Direction: Bi-directional
Data Flow:
  - EclipseLink → PlumeDose: Medication orders from handoff
  - PlumeDose → EclipseLink: Medication administration records
Endpoint: /api/integrations/plumedose
```

#### Other Rohimaya Health AI Products
```yaml
Integration Bus: Shared API Gateway
Authentication: Internal JWT tokens
Data Format: JSON
Events: Webhook-based notifications
```

---

## 9. Security Architecture

### 9.1 Authentication & Authorization

**Authentication Flow**:
```
1. User enters credentials
2. Supabase Auth validates
3. JWT token issued (1-hour expiry)
4. Refresh token stored (30-day expiry)
5. All API calls include JWT in Authorization header
6. Backend validates JWT on each request
7. Role and permissions checked via database
```

**Role-Based Access Control (RBAC)**:
```sql
-- Roles
CREATE TYPE user_role AS ENUM (
  'nurse',
  'doctor',
  'physician_assistant',
  'therapist',
  'technician',
  'admin',
  'super_admin'
);

-- Permissions
CREATE TABLE permissions (
  id UUID PRIMARY KEY,
  role user_role NOT NULL,
  resource VARCHAR(50) NOT NULL,
  action VARCHAR(20) NOT NULL,
  UNIQUE(role, resource, action)
);

-- Examples
INSERT INTO permissions VALUES
  ('...', 'nurse', 'handoff', 'create'),
  ('...', 'nurse', 'handoff', 'read'),
  ('...', 'nurse', 'handoff', 'update'),
  ('...', 'doctor', 'handoff', 'delete'),
  ('...', 'admin', '*', '*');
```

### 9.2 Data Encryption

**At Rest**:
- Database: AES-256 encryption (Supabase)
- Storage: Server-side encryption (R2)
- Backups: Encrypted with separate key

**In Transit**:
- All connections: TLS 1.3
- Certificate: Automated via Cloudflare/Railway
- API calls: HTTPS only
- Websockets: WSS only

**Field-Level Encryption** (for PHI):
```typescript
import { createCipheriv, createDecipheriv } from 'crypto';

const encrypt = (text: string): string => {
  const cipher = createCipheriv('aes-256-gcm', encryptionKey, iv);
  const encrypted = Buffer.concat([cipher.update(text, 'utf8'), cipher.final()]);
  return encrypted.toString('base64');
};

const decrypt = (encrypted: string): string => {
  const decipher = createDecipheriv('aes-256-gcm', encryptionKey, iv);
  const decrypted = Buffer.concat([decipher.update(Buffer.from(encrypted, 'base64')), decipher.final()]);
  return decrypted.toString('utf8');
};

// Usage
const encryptedSSN = encrypt(patient.ssn);
await db.patients.update({ id, ssn: encryptedSSN });
```

### 9.3 HIPAA Compliance

**Required Controls**:
```yaml
Access Control:
  - Unique user IDs
  - Automatic logoff (15 minutes)
  - Encryption and decryption
  
Audit Controls:
  - All PHI access logged
  - Failed login attempts tracked
  - Administrative actions logged
  - Log retention: 7 years
  
Integrity Controls:
  - Checksums for data transfers
  - Digital signatures for documents
  - Version control
  
Transmission Security:
  - End-to-end encryption
  - Integrity checks
  - Secure protocols (TLS 1.3)
```

**Audit Logging**:
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES staff(id),
  action VARCHAR(50) NOT NULL,
  resource VARCHAR(50) NOT NULL,
  resource_id UUID,
  ip_address INET,
  user_agent TEXT,
  request_payload JSONB,
  response_status INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- All PHI access logged
CREATE FUNCTION log_phi_access() RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_logs (user_id, action, resource, resource_id)
  VALUES (current_user_id(), TG_OP, TG_TABLE_NAME, NEW.id);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Business Associate Agreements (BAA)**:
- Supabase: HIPAA BAA available
- Azure OpenAI: HIPAA BAA available
- Cloudflare: HIPAA BAA available (enterprise)
- Railway: Standard DPA (evaluate for HIPAA)

---

## 10. Monitoring & Observability

### 10.1 Application Monitoring (Sentry)

**Configuration**:
```typescript
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
  profilesSampleRate: 0.1,
  beforeSend(event, hint) {
    // Remove PHI from error logs
    if (event.request?.data) {
      event.request.data = sanitizePHI(event.request.data);
    }
    return event;
  }
});
```

**Error Tracking**:
- Frontend errors captured automatically
- Backend errors via SDK
- Performance monitoring
- Release tracking
- User feedback

### 10.2 Logging (Better Stack)

**Structured Logging**:
```typescript
import { createLogger } from '@logtail/node';

const logger = createLogger(process.env.LOGTAIL_TOKEN);

logger.info('Handoff created', {
  handoffId: handoff.id,
  facilityId: handoff.facility_id,
  userId: user.id,
  duration: processingTime
});

logger.error('Transcription failed', {
  error: error.message,
  recordingId: recording.id,
  attempt: retryCount
});
```

**Log Retention**:
```yaml
Application Logs: 30 days
Audit Logs: 7 years (HIPAA requirement)
Access Logs: 90 days
Error Logs: 1 year
```

### 10.3 Uptime Monitoring (BetterUptime)

**Monitored Endpoints**:
```yaml
- URL: https://app.eclipselink.ai
  Check Interval: 60 seconds
  Alert Threshold: 2 consecutive failures
  
- URL: https://api.eclipselink.ai/health
  Check Interval: 30 seconds
  Expected Status: 200
  Expected Body: {"status":"healthy"}
  
- URL: https://api.eclipselink.ai/api/voice/upload
  Method: POST
  Check Interval: 300 seconds (5 min)
  Headers: Authorization
```

**Status Page**:
```
Public URL: status.eclipselink.ai
Components:
  - Web Application
  - API Services
  - Voice Processing
  - AI Services (Transcription & SBAR)
  - EHR Integrations
```

### 10.4 Analytics (PostHog)

**Events Tracked**:
```typescript
posthog.capture('handoff_created', {
  facility_id: facilityId,
  user_role: userRole,
  voice_duration: duration,
  patient_type: patientType
});

posthog.capture('sbar_generated', {
  processing_time: time,
  quality_score: score
});

posthog.capture('ehr_sync_completed', {
  ehr_type: 'epic',
  sync_duration: duration,
  records_synced: count
});
```

**Funnels**:
```
Handoff Creation Funnel:
1. Voice recording started
2. Voice recording completed
3. Transcription initiated
4. SBAR generated
5. Handoff reviewed
6. Handoff completed
```

---

## Summary & Next Steps

### Architecture Highlights
✅ Modern microservices architecture  
✅ Scalable, serverless-first approach  
✅ HIPAA-compliant from the ground up  
✅ Cost-effective for startups ($50-100/month to start)  
✅ Global CDN for performance  
✅ Comprehensive monitoring & observability  

### Recommended Tech Stack Summary
- **Frontend**: Next.js 14 + Tailwind CSS + shadcn/ui (Cloudflare Pages)
- **Backend**: Node.js + Express OR Next.js API Routes (Railway)
- **Database**: Supabase (PostgreSQL with Auth & Storage)
- **AI**: Azure OpenAI (Whisper + GPT-4)
- **Storage**: Cloudflare R2
- **Cache**: Upstash Redis
- **Auth**: Supabase Auth
- **Queue**: BullMQ + Redis
- **Monitoring**: Sentry + Better Stack + BetterUptime + PostHog

### Next Documents in Series
✅ **Part 1: System Architecture Overview** (THIS DOCUMENT)  
⏳ Part 2: Repository Structure & Setup (GitLab + GitHub)  
⏳ Part 3: Database Schema & ERD  
⏳ Part 4: API Specifications  
⏳ Part 5: Azure OpenAI Integration  
⏳ Part 6: EHR Integration Architecture  
⏳ Part 7: Frontend Workflows & Wireframes  
⏳ Part 8: Security & HIPAA Compliance  
⏳ Part 9: Deployment & DevOps Guide  

---

**Ready to proceed to Part 2: Repository Structure & Setup?**

---

*EclipseLink AI™ is a product of Rohimaya Health AI*  
*© 2025 Rohimaya Health AI. All rights reserved.*
