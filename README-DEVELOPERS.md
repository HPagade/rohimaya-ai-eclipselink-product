# EclipseLink AI™ - Developer Documentation

> **Intelligent Clinical Handoff Platform - Technical Implementation Guide**

[![HIPAA Compliant](https://img.shields.io/badge/HIPAA-Compliant-green)](https://rohimaya.ai)
[![Joint Commission](https://img.shields.io/badge/Joint%20Commission-Aligned-blue)](https://rohimaya.ai)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-orange)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture](#architecture)
4. [Getting Started](#getting-started)
5. [Database Schema](#database-schema)
6. [API Documentation](#api-documentation)
7. [Authentication & Security](#authentication--security)
8. [EHR Integrations](#ehr-integrations)
9. [AI/ML Components](#aiml-components)
10. [Testing](#testing)
11. [Deployment](#deployment)
12. [Contributing](#contributing)

---

## 🎯 System Overview

**EclipseLink AI** is a voice-enabled clinical handoff platform that transforms unstructured voice recordings into standardized SBAR (Situation, Background, Assessment, Recommendation) format using Azure OpenAI. The system serves 15 healthcare professions with real-time translation, critical alert detection, and seamless EHR integration.

### Core Innovation: Update-Only Model™

- **Initial admission**: Comprehensive baseline (3-5 min voice recording)
- **Subsequent handoffs**: Only changes documented (30-45 sec)
- **AI comparison**: Automatically extracts updates vs baseline
- **Result**: 80% time reduction

### 15 Integrated Elements

1. Voice-to-SBAR AI (Azure Whisper + GPT-4)
2. Update-Only Model™ intelligence
3. Critical alert detection
4. Real-time translation (50+ languages)
5. AI chatbot (RAG-powered)
6. Family portal (plain-language summaries)
7. Multi-EHR integration
8. 15 profession-specific dashboards
9. Predictive analytics
10. Audit logging (7+ years, HIPAA-compliant)
11-15. Rohimaya ecosystem integration (PlumeDose, RiseGuard, etc.)

---

## 🛠️ Technology Stack

### Frontend
```
- Next.js 14 (App Router)
- React 18
- TypeScript 5
- Tailwind CSS 3
- Shadcn/ui components
- React Query (data fetching)
- Zustand (state management)
```

### Backend
```
- Next.js API Routes
- Node.js 20 LTS
- PostgreSQL 16
- Supabase (auth, real-time, storage)
- Redis (caching, sessions)
```

### AI/ML
```
- Azure OpenAI (GPT-4 Turbo, Whisper)
- Azure Cognitive Services (translation)
- Python 3.11 (ML microservices)
- LangChain (RAG chatbot)
- Pinecone (vector database)
```

### Infrastructure
```
- Cloudflare Pages (frontend hosting)
- Azure Kubernetes Service (AKS)
- Azure PostgreSQL Flexible Server
- Azure Storage (audio files, documents)
- Azure Monitor (observability)
- GitLab CI/CD
```

### EHR Integration
```
- Epic FHIR R4 API
- Cerner Millennium FHIR
- MEDITECH Expanse FHIR
- Protouch HL7 v2.8
- PointClickCare API
- WellSky API
```

---

## 🏗️ Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Clinical   │  │  Family    │  │   Admin    │            │
│  │  Web App   │  │  Portal    │  │  Dashboard │            │
│  │ (Next.js)  │  │ (Next.js)  │  │ (Next.js)  │            │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘            │
└─────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │
          │    Cloudflare Pages Hosting    │
          │                                  │
┌─────────▼──────────────────────────────────▼─────────────────┐
│                      API GATEWAY                              │
│           (Next.js API Routes + Rate Limiting)                │
└──┬─────────┬──────────┬──────────┬──────────┬──────────┬────┘
   │         │          │          │          │          │
   │         │          │          │          │          │
┌──▼────┐ ┌─▼─────┐ ┌─▼──────┐ ┌─▼──────┐ ┌─▼──────┐ ┌▼─────┐
│ Voice │ │ SBAR  │ │ Alert  │ │Family  │ │  EHR   │ │ AI   │
│Service│ │Service│ │Service │ │Service │ │Gateway │ │Chat  │
│       │ │       │ │        │ │        │ │        │ │      │
│Whisper│ │GPT-4  │ │Rules   │ │Simplify│ │HL7/    │ │RAG   │
│  API  │ │Turbo  │ │Engine  │ │Language│ │FHIR    │ │GPT-4 │
└───┬───┘ └───┬───┘ └───┬────┘ └───┬────┘ └───┬────┘ └──┬───┘
    │         │         │          │          │          │
    └─────────┴─────────┴──────────┴──────────┴──────────┘
                            │
                ┌───────────▼────────────┐
                │    PostgreSQL 16        │
                │  (Supabase Backend)     │
                │   - 15 Core Tables      │
                │   - Audit Logs          │
                │   - RLS Policies        │
                └────────────────────────┘
```

### Data Flow: Voice → SBAR

```
1. Clinician records voice → Upload to Azure Storage
2. Whisper API transcribes → Text returned
3. GPT-4 analyzes transcript → SBAR JSON generated
4. Alert Service scans SBAR → Critical alerts flagged
5. Update-Only Model compares to baseline → Delta extracted
6. Database stores finalized handoff → Real-time sync to dashboards
7. EHR Gateway pushes handoff → HL7/FHIR message sent
```

---

## 🚀 Getting Started

### Prerequisites

```bash
- Node.js 20 LTS
- PostgreSQL 16
- Git
- Azure subscription (OpenAI access)
- Supabase account
- GitLab account (CI/CD)
```

### Environment Variables

Create `.env.local`:

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Azure OpenAI
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4-turbo
AZURE_WHISPER_DEPLOYMENT_NAME=whisper

# Azure Storage (Audio Files)
AZURE_STORAGE_ACCOUNT_NAME=rohimayastorage
AZURE_STORAGE_ACCOUNT_KEY=your-storage-key
AZURE_STORAGE_CONTAINER_NAME=voice-recordings

# Redis (Session Management)
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=your-redis-password

# EHR Integrations
EPIC_CLIENT_ID=your-epic-client-id
EPIC_CLIENT_SECRET=your-epic-secret
EPIC_FHIR_BASE_URL=https://fhir.epic.com/interconnect-fhir-oauth/

CERNER_CLIENT_ID=your-cerner-client-id
CERNER_CLIENT_SECRET=your-cerner-secret
CERNER_FHIR_BASE_URL=https://fhir-myrecord.cerner.com/

# Application Settings
NODE_ENV=development
NEXT_PUBLIC_APP_URL=http://localhost:3000
JWT_SECRET=your-jwt-secret-min-32-chars

# Feature Flags
ENABLE_FAMILY_PORTAL=true
ENABLE_AI_CHATBOT=true
ENABLE_PREDICTIVE_ANALYTICS=false
```

### Installation

```bash
# Clone repository
git clone https://gitlab.com/rohimaya/eclipselink-ai.git
cd eclipselink-ai

# Install dependencies
npm install

# Set up database
npm run db:migrate
npm run db:seed

# Start development server
npm run dev
```

Access application at `http://localhost:3000`

### Project Structure

```
eclipselink-ai/
├── app/                    # Next.js app directory
│   ├── (auth)/            # Authentication routes
│   ├── (dashboard)/       # Protected dashboard routes
│   ├── api/               # API routes
│   └── layout.tsx         # Root layout
├── components/            # React components
│   ├── ui/               # Shadcn/ui components
│   ├── features/         # Feature-specific components
│   └── shared/           # Shared components
├── lib/                   # Utilities
│   ├── supabase/         # Supabase client
│   ├── azure/            # Azure OpenAI integration
│   ├── ehr/              # EHR integrations
│   └── utils/            # Helper functions
├── types/                 # TypeScript types
├── public/               # Static assets
├── prisma/               # Database schema
│   └── schema.prisma
├── tests/                # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── docs/                 # Documentation
    ├── api/              # API documentation
    ├── architecture/     # Architecture docs
    └── deployment/       # Deployment guides
```

---

## 🗄️ Database Schema

### Core Tables (15 Total)

#### 1. `users`
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  profession VARCHAR(50) NOT NULL, -- 'RN', 'MD', 'RT', 'PT', etc.
  license_number VARCHAR(100),
  facility_id UUID REFERENCES facilities(id),
  role VARCHAR(20) DEFAULT 'clinician', -- 'clinician', 'admin', 'super_admin'
  is_active BOOLEAN DEFAULT true,
  last_login TIMESTAMP,
  mfa_enabled BOOLEAN DEFAULT false,
  mfa_secret VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_facility ON users(facility_id);
CREATE INDEX idx_users_profession ON users(profession);
```

#### 2. `patients`
```sql
CREATE TABLE patients (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  mrn VARCHAR(50) UNIQUE NOT NULL, -- Medical Record Number
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  date_of_birth DATE NOT NULL,
  gender VARCHAR(20),
  preferred_language VARCHAR(50) DEFAULT 'en',
  facility_id UUID REFERENCES facilities(id),
  admission_date TIMESTAMP,
  discharge_date TIMESTAMP,
  room_number VARCHAR(20),
  primary_diagnosis TEXT,
  allergies TEXT[],
  code_status VARCHAR(50), -- 'Full Code', 'DNR', 'DNI', etc.
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_patients_mrn ON patients(mrn);
CREATE INDEX idx_patients_facility ON patients(facility_id);
CREATE INDEX idx_patients_active ON patients(is_active) WHERE is_active = true;
```

#### 3. `handoffs`
```sql
CREATE TABLE handoffs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  patient_id UUID REFERENCES patients(id) NOT NULL,
  from_user_id UUID REFERENCES users(id) NOT NULL,
  to_user_id UUID REFERENCES users(id),
  shift_type VARCHAR(20), -- 'day', 'night', 'swing'
  handoff_type VARCHAR(20), -- 'initial', 'update'
  
  -- Voice Recording
  audio_url TEXT,
  audio_duration_seconds INTEGER,
  transcription TEXT,
  
  -- SBAR Components (JSON)
  situation JSONB,
  background JSONB,
  assessment JSONB,
  recommendation JSONB,
  
  -- AI-Generated Fields
  critical_alerts JSONB[], -- Array of alert objects
  confidence_score DECIMAL(3,2), -- 0.00 to 1.00
  
  -- Metadata
  ehr_message_id VARCHAR(255), -- For HL7/FHIR tracking
  status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'completed', 'flagged'
  is_baseline BOOLEAN DEFAULT false,
  baseline_handoff_id UUID REFERENCES handoffs(id), -- Links to original baseline
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_handoffs_patient ON handoffs(patient_id);
CREATE INDEX idx_handoffs_from_user ON handoffs(from_user_id);
CREATE INDEX idx_handoffs_created ON handoffs(created_at DESC);
CREATE INDEX idx_handoffs_baseline ON handoffs(is_baseline) WHERE is_baseline = true;
```

#### 4. `critical_alerts`
```sql
CREATE TABLE critical_alerts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  handoff_id UUID REFERENCES handoffs(id) NOT NULL,
  alert_type VARCHAR(50) NOT NULL, -- 'medication', 'vital_sign', 'lab', 'fall_risk', etc.
  severity VARCHAR(20) NOT NULL, -- 'critical', 'high', 'medium', 'low'
  message TEXT NOT NULL,
  acknowledged BOOLEAN DEFAULT false,
  acknowledged_by UUID REFERENCES users(id),
  acknowledged_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alerts_handoff ON critical_alerts(handoff_id);
CREATE INDEX idx_alerts_severity ON critical_alerts(severity);
CREATE INDEX idx_alerts_unacknowledged ON critical_alerts(acknowledged) WHERE acknowledged = false;
```

#### 5. `family_access`
```sql
CREATE TABLE family_access (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  patient_id UUID REFERENCES patients(id) NOT NULL,
  family_email VARCHAR(255) NOT NULL,
  family_name VARCHAR(200),
  relationship VARCHAR(100), -- 'Spouse', 'Child', 'Parent', etc.
  access_code VARCHAR(10) UNIQUE NOT NULL, -- 6-digit PIN
  access_level VARCHAR(20) DEFAULT 'view', -- 'view', 'limited', 'full'
  is_active BOOLEAN DEFAULT true,
  last_access TIMESTAMP,
  expires_at TIMESTAMP, -- Optional expiration
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_family_patient ON family_access(patient_id);
CREATE INDEX idx_family_code ON family_access(access_code);
CREATE UNIQUE INDEX idx_family_unique ON family_access(patient_id, family_email);
```

### Additional Tables

6. `facilities` - Hospital/clinic information
7. `audit_logs` - Complete audit trail (7+ years)
8. `ai_training_feedback` - User corrections for model improvement
9. `ehr_sync_log` - EHR integration tracking
10. `translation_cache` - Cached translations for performance
11. `chatbot_conversations` - AI chatbot interaction logs
12. `rewards_points` - Phoenix & Peacock Honors integration
13. `predictive_analytics` - ML model predictions
14. `system_settings` - Application configuration
15. `notification_queue` - Async notification delivery

### Row-Level Security (RLS)

```sql
-- Clinicians can only see patients in their facility
CREATE POLICY "Clinicians see own facility patients"
  ON patients FOR SELECT
  USING (facility_id = (SELECT facility_id FROM users WHERE id = auth.uid()));

-- Handoffs viewable by sender, receiver, or same facility
CREATE POLICY "Handoff access control"
  ON handoffs FOR SELECT
  USING (
    from_user_id = auth.uid() 
    OR to_user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM users u
      JOIN patients p ON handoffs.patient_id = p.id
      WHERE u.id = auth.uid() AND u.facility_id = p.facility_id
    )
  );

-- Family members can only access their patient's info
CREATE POLICY "Family portal access"
  ON patients FOR SELECT
  USING (
    id IN (
      SELECT patient_id FROM family_access
      WHERE family_email = auth.email() AND is_active = true
    )
  );
```

---

## 🔌 API Documentation

### Authentication

All API requests require Bearer token authentication:

```bash
Authorization: Bearer <jwt_token>
```

### Base URL

```
Production: https://api.rohimaya.ai/v1
Development: http://localhost:3000/api
```

### Core Endpoints

#### 1. Voice Recording Upload

```http
POST /api/handoffs/voice-upload
Content-Type: multipart/form-data

Parameters:
- audio: File (required) - Audio file (WAV, MP3, M4A, max 25MB)
- patient_id: UUID (required)
- shift_type: String (required) - 'day', 'night', 'swing'
- handoff_type: String (required) - 'initial', 'update'

Response 201:
{
  "handoff_id": "uuid",
  "audio_url": "https://storage.azure.com/...",
  "transcription": "string",
  "processing_status": "completed",
  "confidence_score": 0.95
}
```

#### 2. Generate SBAR from Transcription

```http
POST /api/handoffs/generate-sbar
Content-Type: application/json

Body:
{
  "handoff_id": "uuid",
  "transcription": "string",
  "patient_id": "uuid"
}

Response 200:
{
  "handoff_id": "uuid",
  "sbar": {
    "situation": {
      "patient_name": "John Doe",
      "age": 45,
      "diagnosis": "Acute MI",
      "room": "ICU-204",
      "chief_complaint": "Chest pain"
    },
    "background": {
      "medical_history": ["HTN", "Diabetes Type 2"],
      "surgical_history": [],
      "allergies": ["Penicillin"],
      "medications": [...]
    },
    "assessment": {
      "vital_signs": {...},
      "labs": {...},
      "progress": "Stable, chest pain resolved"
    },
    "recommendation": {
      "pending_orders": [...],
      "follow_up": "Monitor troponin q6h",
      "escalation_needed": false
    }
  },
  "critical_alerts": [
    {
      "type": "medication",
      "severity": "high",
      "message": "Heparin drip rate outside protocol range"
    }
  ]
}
```

#### 3. Get Patient Handoffs

```http
GET /api/patients/:patient_id/handoffs
Query Parameters:
- limit: Number (default: 50)
- offset: Number (default: 0)
- shift_type: String (optional)
- start_date: ISO Date (optional)
- end_date: ISO Date (optional)

Response 200:
{
  "handoffs": [
    {
      "id": "uuid",
      "patient": {...},
      "from_user": {...},
      "to_user": {...},
      "shift_type": "day",
      "sbar": {...},
      "critical_alerts": [...],
      "created_at": "2025-10-23T10:30:00Z"
    }
  ],
  "total": 150,
  "has_more": true
}
```

#### 4. AI Chatbot Query

```http
POST /api/chatbot/query
Content-Type: application/json

Body:
{
  "question": "What are the patient's current medications?",
  "patient_id": "uuid",
  "context": "medication_review"
}

Response 200:
{
  "answer": "The patient is currently on...",
  "sources": [
    {
      "type": "handoff",
      "id": "uuid",
      "timestamp": "2025-10-23T08:00:00Z"
    }
  ],
  "confidence": 0.92,
  "follow_up_questions": [
    "Would you like to see recent vitals?",
    "Do you need lab results?"
  ]
}
```

#### 5. Real-Time Translation

```http
POST /api/translate
Content-Type: application/json

Body:
{
  "text": "Patient complains of chest pain",
  "target_language": "es", // ISO 639-1 code
  "source_language": "en" // Optional, auto-detect if not provided
}

Response 200:
{
  "original_text": "Patient complains of chest pain",
  "translated_text": "El paciente se queja de dolor en el pecho",
  "source_language": "en",
  "target_language": "es",
  "confidence": 0.98
}
```

#### 6. Family Portal Access

```http
POST /api/family/authenticate
Content-Type: application/json

Body:
{
  "patient_mrn": "string",
  "access_code": "string" // 6-digit PIN
}

Response 200:
{
  "access_token": "jwt_token",
  "patient": {
    "first_name": "John",
    "room_number": "204",
    "admission_date": "2025-10-20T00:00:00Z"
  },
  "latest_update": {
    "summary": "Your loved one is resting comfortably...",
    "condition": "Stable",
    "timestamp": "2025-10-23T10:00:00Z"
  }
}
```

### Error Responses

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Patient ID is required",
    "details": {...}
  },
  "request_id": "uuid"
}
```

#### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Malformed request |
| `UNAUTHORIZED` | 401 | Missing/invalid token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `AI_SERVICE_ERROR` | 503 | Azure OpenAI unavailable |

---

## 🔒 Authentication & Security

### Password Policy (NIST 2025 Compliant)

```typescript
const PASSWORD_REQUIREMENTS = {
  minLength: 12,
  maxLength: 16,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecialChars: true,
  expirationDays: 365, // Annual rotation
  historyCount: 5, // Cannot reuse last 5 passwords
  maxAttempts: 5, // Account lockout after 5 failures
  lockoutDurationMinutes: 30
};
```

### Multi-Factor Authentication (MFA)

```typescript
// Enable MFA
POST /api/auth/mfa/enable
Response: { qr_code: "data:image/png;base64,..." }

// Verify MFA
POST /api/auth/mfa/verify
Body: { code: "123456" }
Response: { verified: true }
```

### Session Management

- **Session timeout**: 15 minutes of inactivity
- **Token refresh**: Every 10 minutes (if active)
- **Redis-backed sessions**: Instant invalidation on logout

### Encryption

```typescript
// Data at rest
AES-256-GCM encryption for PHI

// Data in transit
TLS 1.3 with perfect forward secrecy

// Database encryption
PostgreSQL transparent data encryption (TDE)
```

### Audit Logging

```typescript
interface AuditLog {
  id: string;
  user_id: string;
  action: string; // 'create', 'read', 'update', 'delete'
  resource_type: string; // 'patient', 'handoff', etc.
  resource_id: string;
  ip_address: string;
  user_agent: string;
  changes?: Record<string, any>; // Before/after values
  timestamp: Date;
}

// Retention: 7+ years (HIPAA requirement)
// Immutable: Logs cannot be modified or deleted
```

---

## 🏥 EHR Integrations

### Epic FHIR R4

```typescript
// OAuth 2.0 Authentication
const epicAuth = {
  client_id: process.env.EPIC_CLIENT_ID,
  client_secret: process.env.EPIC_CLIENT_SECRET,
  token_url: 'https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token',
  scopes: ['Patient.read', 'Observation.read', 'MedicationRequest.read']
};

// Fetch patient data
async function fetchEpicPatient(mrn: string) {
  const response = await fetch(
    `${EPIC_FHIR_BASE_URL}/Patient?identifier=${mrn}`,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Accept': 'application/fhir+json'
      }
    }
  );
  return response.json();
}

// Push handoff as Communication resource
async function pushHandoffToEpic(handoff: Handoff) {
  const communication = {
    resourceType: 'Communication',
    status: 'completed',
    subject: { reference: `Patient/${handoff.patient_fhir_id}` },
    sender: { reference: `Practitioner/${handoff.from_user_fhir_id}` },
    recipient: [{ reference: `Practitioner/${handoff.to_user_fhir_id}` }],
    payload: [
      {
        contentString: JSON.stringify(handoff.sbar)
      }
    ],
    sent: new Date().toISOString()
  };

  return await fetch(`${EPIC_FHIR_BASE_URL}/Communication`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/fhir+json'
    },
    body: JSON.stringify(communication)
  });
}
```

### Protouch (HL7 v2.8)

```typescript
// Parse incoming ADT^A01 (Patient Admission)
import { HL7Parser } from 'hl7-standard';

async function parseProtouch ADT(message: string) {
  const parser = new HL7Parser();
  const parsed = parser.parse(message);

  return {
    mrn: parsed.segments.PID[3][0],
    firstName: parsed.segments.PID[5][1],
    lastName: parsed.segments.PID[5][0],
    dateOfBirth: parsed.segments.PID[7],
    room: parsed.segments.PV1[3][0],
    admissionDate: parsed.segments.PV1[44]
  };
}

// Send handoff as MDM^T02 (Medical Document)
async function sendHandoffToProtouch(handoff: Handoff) {
  const hl7Message = `
MSH|^~\\&|ECLIPSELINK|ROHIMAYA|PROTOUCH|${facilityId}|${timestamp}||MDM^T02|${messageId}|P|2.8
PID|1||${handoff.patient.mrn}||${handoff.patient.lastName}^${handoff.patient.firstName}
TXA|1||TEXT||${timestamp}||||||||||AV|||
OBX|1|TX|||${JSON.stringify(handoff.sbar)}
  `.trim();

  // Send via MLLP (Minimal Lower Layer Protocol)
  await sendMLLP(protouchHost, protouchPort, hl7Message);
}
```

### Integration Testing

```typescript
// Mock EHR responses for development
if (process.env.NODE_ENV === 'development') {
  app.use('/mock-epic', mockEpicServer);
  app.use('/mock-cerner', mockCernerServer);
}

// Integration tests
describe('Epic FHIR Integration', () => {
  it('should fetch patient by MRN', async () => {
    const patient = await fetchEpicPatient('E12345');
    expect(patient.resourceType).toBe('Patient');
  });

  it('should push handoff as Communication', async () => {
    const response = await pushHandoffToEpic(mockHandoff);
    expect(response.status).toBe(201);
  });
});
```

---

## 🤖 AI/ML Components

### Azure OpenAI Integration

```typescript
import { OpenAIClient, AzureKeyCredential } from '@azure/openai';

const client = new OpenAIClient(
  process.env.AZURE_OPENAI_ENDPOINT!,
  new AzureKeyCredential(process.env.AZURE_OPENAI_API_KEY!)
);

// Transcribe audio with Whisper
async function transcribeAudio(audioUrl: string): Promise<string> {
  const response = await client.getAudioTranscription(
    process.env.AZURE_WHISPER_DEPLOYMENT_NAME!,
    audioUrl,
    {
      language: 'en',
      temperature: 0.2, // Lower = more accurate
      prompt: 'Medical handoff with clinical terminology'
    }
  );
  return response.text;
}

// Generate SBAR with GPT-4 Turbo
async function generateSBAR(transcription: string, patientContext: any) {
  const systemPrompt = `You are a clinical AI assistant that converts nurse handoff transcriptions into structured SBAR format. Extract:
- Situation: Patient name, age, diagnosis, chief complaint, room number
- Background: Medical history, surgical history, allergies, current medications
- Assessment: Vital signs, labs, current condition, progress
- Recommendation: Pending orders, follow-up needed, escalation required

Identify critical alerts (medication errors, vital sign abnormalities, fall risks, lab criticals).

Return JSON only. Be precise with medical terminology.`;

  const response = await client.getChatCompletions(
    process.env.AZURE_OPENAI_DEPLOYMENT_NAME!,
    [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: `Patient context: ${JSON.stringify(patientContext)}\n\nTranscription: ${transcription}` }
    ],
    {
      temperature: 0.3,
      maxTokens: 2000,
      responseFormat: { type: 'json_object' }
    }
  );

  return JSON.parse(response.choices[0].message.content);
}
```

### RAG-Powered Chatbot

```typescript
import { Pinecone } from '@pinecone-database/pinecone';
import { OpenAIEmbeddings } from 'langchain/embeddings/openai';

const pinecone = new Pinecone({ apiKey: process.env.PINECONE_API_KEY! });
const index = pinecone.index('eclipselink-knowledge');

// Index handoff into vector database
async function indexHandoff(handoff: Handoff) {
  const embeddings = new OpenAIEmbeddings({
    azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY,
    azureOpenAIApiEndpoint: process.env.AZURE_OPENAI_ENDPOINT,
  });

  const text = `
    Patient: ${handoff.patient.first_name} ${handoff.patient.last_name}
    MRN: ${handoff.patient.mrn}
    SBAR: ${JSON.stringify(handoff.sbar)}
  `;

  const vector = await embeddings.embedQuery(text);

  await index.upsert([
    {
      id: handoff.id,
      values: vector,
      metadata: {
        patient_id: handoff.patient_id,
        created_at: handoff.created_at.toISOString(),
        shift_type: handoff.shift_type
      }
    }
  ]);
}

// Query chatbot with semantic search
async function queryChatbot(question: string, patientId: string) {
  const embeddings = new OpenAIEmbeddings({...});
  const queryVector = await embeddings.embedQuery(question);

  const results = await index.query({
    vector: queryVector,
    topK: 5,
    filter: { patient_id: patientId }
  });

  const context = results.matches
    .map(match => match.metadata)
    .join('\n\n');

  const response = await client.getChatCompletions(
    process.env.AZURE_OPENAI_DEPLOYMENT_NAME!,
    [
      { role: 'system', content: 'You are a helpful clinical AI assistant.' },
      { role: 'user', content: `Context: ${context}\n\nQuestion: ${question}` }
    ]
  );

  return response.choices[0].message.content;
}
```

### Critical Alert Detection

```typescript
interface AlertRule {
  type: string;
  condition: (sbar: any) => boolean;
  severity: 'critical' | 'high' | 'medium' | 'low';
  message: (sbar: any) => string;
}

const ALERT_RULES: AlertRule[] = [
  {
    type: 'vital_sign_critical',
    condition: (sbar) => {
      const hr = sbar.assessment?.vital_signs?.heart_rate;
      return hr && (hr < 40 || hr > 140);
    },
    severity: 'critical',
    message: (sbar) => `Heart rate ${sbar.assessment.vital_signs.heart_rate} outside safe range`
  },
  {
    type: 'medication_high_risk',
    condition: (sbar) => {
      const meds = sbar.background?.medications || [];
      const highRisk = ['heparin', 'insulin', 'warfarin'];
      return meds.some(med => 
        highRisk.some(hr => med.name.toLowerCase().includes(hr))
      );
    },
    severity: 'high',
    message: () => 'High-risk medication requires extra vigilance'
  },
  // ... 50+ more rules
];

function detectAlerts(sbar: any): CriticalAlert[] {
  return ALERT_RULES
    .filter(rule => rule.condition(sbar))
    .map(rule => ({
      type: rule.type,
      severity: rule.severity,
      message: rule.message(sbar)
    }));
}
```

---

## 🧪 Testing

### Unit Tests

```bash
npm run test:unit

# Watch mode
npm run test:unit:watch

# Coverage
npm run test:coverage
```

```typescript
// Example: SBAR generation test
describe('generateSBAR', () => {
  it('should extract patient name from transcription', async () => {
    const transcription = 'Patient John Doe, 45 year old male...';
    const sbar = await generateSBAR(transcription, {});
    
    expect(sbar.situation.patient_name).toBe('John Doe');
    expect(sbar.situation.age).toBe(45);
  });

  it('should detect critical alerts', async () => {
    const transcription = 'Heart rate 160, patient diaphoretic...';
    const sbar = await generateSBAR(transcription, {});
    const alerts = detectAlerts(sbar);
    
    expect(alerts).toHaveLength(1);
    expect(alerts[0].severity).toBe('critical');
  });
});
```

### Integration Tests

```bash
npm run test:integration
```

```typescript
// Example: API endpoint test
describe('POST /api/handoffs/voice-upload', () => {
  it('should process voice recording and generate SBAR', async () => {
    const response = await request(app)
      .post('/api/handoffs/voice-upload')
      .attach('audio', './tests/fixtures/sample-handoff.wav')
      .field('patient_id', testPatientId)
      .field('shift_type', 'day')
      .expect(201);

    expect(response.body).toHaveProperty('handoff_id');
    expect(response.body).toHaveProperty('sbar');
    expect(response.body.sbar).toHaveProperty('situation');
  });
});
```

### E2E Tests (Playwright)

```bash
npm run test:e2e
```

```typescript
// Example: Complete handoff workflow
test('clinician can create and view handoff', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.fill('[name="email"]', 'nurse@hospital.com');
  await page.fill('[name="password"]', 'Test123!');
  await page.click('[type="submit"]');

  // Navigate to patient
  await page.goto('/patients/123');
  
  // Record handoff
  await page.click('[data-testid="record-handoff"]');
  await page.click('[data-testid="start-recording"]');
  await page.waitForTimeout(5000);
  await page.click('[data-testid="stop-recording"]');

  // Verify SBAR generated
  await expect(page.locator('[data-testid="sbar-situation"]')).toBeVisible();
  await expect(page.locator('[data-testid="sbar-background"]')).toBeVisible();
});
```

---

## 🚀 Deployment

### Cloudflare Pages (Frontend)

```bash
# Install Wrangler CLI
npm install -g wrangler

# Build for production
npm run build

# Deploy to Cloudflare Pages
wrangler pages deploy .next --project-name eclipselink-ai

# Set environment variables
wrangler pages secret put NEXT_PUBLIC_SUPABASE_URL
wrangler pages secret put AZURE_OPENAI_API_KEY
```

### Azure Kubernetes Service (Backend)

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eclipselink-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: eclipselink-api
  template:
    metadata:
      labels:
        app: eclipselink-api
    spec:
      containers:
      - name: api
        image: rohimaya.azurecr.io/eclipselink-api:latest
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: connection-string
        - name: AZURE_OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: azure-credentials
              key: openai-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: eclipselink-api-service
spec:
  selector:
    app: eclipselink-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: LoadBalancer
```

```bash
# Deploy to AKS
az aks get-credentials --resource-group rohimaya --name eclipselink-cluster
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/ingress.yaml

# Scale deployment
kubectl scale deployment eclipselink-api --replicas=5

# Check status
kubectl get pods
kubectl logs -f deployment/eclipselink-api
```

### GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: rohimaya.azurecr.io/eclipselink-api

test:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm run test:unit
    - npm run test:integration
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD rohimaya.azurecr.io
    - docker build -t $DOCKER_IMAGE:$CI_COMMIT_SHA -t $DOCKER_IMAGE:latest .
    - docker push $DOCKER_IMAGE:$CI_COMMIT_SHA
    - docker push $DOCKER_IMAGE:latest
  only:
    - main

deploy:production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config set-cluster k8s --server="$KUBE_SERVER" --insecure-skip-tls-verify=true
    - kubectl config set-credentials admin --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=admin
    - kubectl config use-context default
    - kubectl set image deployment/eclipselink-api api=$DOCKER_IMAGE:$CI_COMMIT_SHA
    - kubectl rollout status deployment/eclipselink-api
  only:
    - main
  when: manual
```

### Database Migrations

```bash
# Run migrations
npm run db:migrate

# Rollback last migration
npm run db:migrate:rollback

# Generate migration
npm run db:migrate:make add_patient_preferences
```

---

## 🤝 Contributing

### Development Workflow

1. **Fork repository** on GitLab
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** with tests
4. **Run linter**: `npm run lint`
5. **Run tests**: `npm run test`
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open Merge Request** with description

### Code Style

```bash
# Format with Prettier
npm run format

# Lint with ESLint
npm run lint

# Type check
npm run type-check
```

### Commit Conventions

```
feat: Add voice recording upload
fix: Resolve SBAR generation timeout
docs: Update API documentation
test: Add handoff integration tests
chore: Update dependencies
refactor: Simplify alert detection logic
```

---

## 📞 Support

### Documentation
- [API Docs](https://docs.rohimaya.ai/eclipselink)
- [Architecture Diagrams](https://docs.rohimaya.ai/architecture)
- [Video Tutorials](https://www.youtube.com/rohimayahealth)

### Contact
- **Email:** developers@rohimaya.ai
- **Slack:** [Join Rohimaya Dev Community](https://rohimaya.slack.com)
- **GitLab Issues:** [Report Bug](https://gitlab.com/rohimaya/eclipselink-ai/issues)

### Office Hours
- **Weekly Dev Q&A:** Thursdays 2pm MT
- **Architecture Review:** Bi-weekly Tuesdays 10am MT

---

## 📄 License

Copyright © 2025 Rohimaya Health AI, LLC. All rights reserved.

This is proprietary software. Contact hello@rohimaya.ai for licensing.

---

**Built with ❤️ by the Rohimaya team in Westminster, Colorado**
