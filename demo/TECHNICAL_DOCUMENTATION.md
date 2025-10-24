# EclipseLink AI™ — Technical Documentation
## For Development Team, DevOps, and Technical Stakeholders

**Version:** 1.0.0
**Last Updated:** October 24, 2025
**Rohimaya Health AI**

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Technology Stack](#2-technology-stack)
3. [Database Schema](#3-database-schema)
4. [API Documentation](#4-api-documentation)
5. [AI/ML Pipeline](#5-aiml-pipeline)
6. [Security & Compliance](#6-security--compliance)
7. [Deployment & Infrastructure](#7-deployment--infrastructure)
8. [Development Workflow](#8-development-workflow)
9. [Testing Strategy](#9-testing-strategy)
10. [Monitoring & Observability](#10-monitoring--observability)
11. [Roadmap & Future Work](#11-roadmap--future-work)

---

## 1. System Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Client Apps   │
│  (Web, Mobile)  │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────────────┐
│   Load Balancer (ALB)   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Frontend (Next.js 14)  │
│  - SSR/SSG             │
│  - React 18            │
│  - API Routes          │
└────────┬────────────────┘
         │ REST/WebSocket
         ▼
┌─────────────────────────┐
│  Backend API (Express)  │
│  - JWT Auth            │
│  - Rate Limiting       │
│  - Request Validation  │
└────┬───────────────┬────┘
     │               │
     ▼               ▼
┌─────────────┐ ┌──────────────┐
│ PostgreSQL  │ │ Redis Cache  │
│  (Primary)  │ │ & Queue      │
└─────────────┘ └──────────────┘
     │
     ▼
┌─────────────────────────┐
│  BullMQ Workers         │
│  - Voice Processing     │
│  - SBAR Generation      │
│  - Quality Scoring      │
└────┬────────────────────┘
     │
     ▼
┌─────────────────────────┐
│  External Services      │
│  - Azure OpenAI         │
│  - Cloudflare R2        │
│  - SendGrid (Email)     │
└─────────────────────────┘
```

### Component Breakdown

#### Frontend (apps/frontend)
- **Framework:** Next.js 14 with App Router
- **UI Library:** React 18 + Tailwind CSS + Radix UI
- **State Management:** Zustand + React Query
- **Responsibilities:**
  - User authentication and session management
  - Voice recording (MediaRecorder API)
  - Real-time UI updates
  - SBAR report viewing/editing
  - Analytics dashboards

#### Backend API (apps/backend)
- **Framework:** Express.js + TypeScript
- **Database ORM:** Prisma
- **Responsibilities:**
  - RESTful API endpoints
  - JWT authentication + refresh tokens
  - File upload handling
  - WebSocket connections (real-time updates)
  - Job queue management

#### Worker Services (apps/workers)
- **Queue:** BullMQ (Redis-backed)
- **Workers:**
  1. **Voice Processor:** Uploads audio to R2, sends to Azure Whisper
  2. **SBAR Generator:** Takes transcription, generates SBAR via GPT-4
  3. **Quality Scorer:** Evaluates completeness and critical elements
  4. **Notification Worker:** Sends emails, push notifications

---

## 2. Technology Stack

### Frontend
| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Framework** | Next.js | 14.0+ | React framework with SSR/SSG |
| **Language** | TypeScript | 5.0+ | Type-safe JavaScript |
| **UI Library** | React | 18.2+ | Component library |
| **Styling** | Tailwind CSS | 3.4+ | Utility-first CSS |
| **Components** | Radix UI | Latest | Accessible UI primitives |
| **State** | Zustand | 4.4+ | Lightweight state management |
| **Data Fetching** | React Query | 5.0+ | Server state management |
| **HTTP Client** | Axios | 1.6+ | Promise-based HTTP client |
| **Forms** | React Hook Form | 7.48+ | Form validation |
| **Charts** | Recharts | 2.9+ | Data visualization |

### Backend
| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Runtime** | Node.js | 20 LTS | JavaScript runtime |
| **Framework** | Express.js | 4.18+ | Web application framework |
| **Language** | TypeScript | 5.0+ | Type-safe JavaScript |
| **Database** | PostgreSQL | 15+ | Relational database |
| **ORM** | Prisma | 5.6+ | Database ORM |
| **Cache/Queue** | Redis | 7.2+ | In-memory data store |
| **Queue** | BullMQ | 5.0+ | Job queue system |
| **Auth** | jsonwebtoken | 9.0+ | JWT implementation |
| **Validation** | Zod | 3.22+ | Schema validation |
| **File Upload** | Multer | 1.4+ | Multipart form data |

### AI/ML & Cloud Services
| Service | Provider | Purpose |
|---------|----------|---------|
| **Speech-to-Text** | Azure Whisper (OpenAI) | Voice transcription |
| **NLP/Generation** | Azure GPT-4 | SBAR generation |
| **Object Storage** | Cloudflare R2 | Audio file storage |
| **Email** | SendGrid | Transactional emails |
| **SMS** | Twilio | SMS notifications |
| **Hosting** | Azure Kubernetes Service | Container orchestration |
| **CDN** | Cloudflare | Content delivery |

### DevOps & Infrastructure
| Category | Technology | Purpose |
|----------|------------|---------|
| **Containerization** | Docker | Application containers |
| **Orchestration** | Kubernetes | Container orchestration |
| **CI/CD** | GitHub Actions | Automated pipelines |
| **Monitoring** | Datadog | APM and logging |
| **Error Tracking** | Sentry | Error monitoring |
| **Secrets** | Azure Key Vault | Secret management |

---

## 3. Database Schema

### Core Tables

#### users
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  role VARCHAR(50) NOT NULL, -- 'nurse', 'physician', 'admin'
  specialty VARCHAR(100),
  department VARCHAR(100),
  phone VARCHAR(20),
  is_active BOOLEAN DEFAULT true,
  last_login_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

#### patients
```sql
CREATE TABLE patients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mrn VARCHAR(50) UNIQUE NOT NULL, -- Medical Record Number
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  date_of_birth DATE NOT NULL,
  gender VARCHAR(20),
  blood_type VARCHAR(5),
  allergies TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_patients_mrn ON patients(mrn);
CREATE INDEX idx_patients_last_name ON patients(last_name);
```

#### handoffs
```sql
CREATE TABLE handoffs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  from_user_id UUID NOT NULL REFERENCES users(id),
  to_user_id UUID REFERENCES users(id),

  handoff_type VARCHAR(50) NOT NULL, -- 'shift_change', 'transfer', 'admission', 'discharge', 'procedure'
  priority VARCHAR(20) NOT NULL, -- 'routine', 'urgent', 'emergent'
  status VARCHAR(20) NOT NULL DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'

  voice_recording_id UUID REFERENCES voice_recordings(id),
  transcription TEXT,

  sbar_situation TEXT,
  sbar_background TEXT,
  sbar_assessment TEXT,
  sbar_recommendation TEXT,

  quality_score INTEGER, -- 0-100
  completeness_score INTEGER, -- 0-100
  critical_elements_score INTEGER, -- 0-100

  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_handoffs_patient ON handoffs(patient_id);
CREATE INDEX idx_handoffs_from_user ON handoffs(from_user_id);
CREATE INDEX idx_handoffs_status ON handoffs(status);
CREATE INDEX idx_handoffs_created_at ON handoffs(created_at DESC);
```

#### voice_recordings
```sql
CREATE TABLE voice_recordings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  handoff_id UUID NOT NULL REFERENCES handoffs(id),
  user_id UUID NOT NULL REFERENCES users(id),

  file_path VARCHAR(500) NOT NULL, -- R2 object key
  file_size INTEGER NOT NULL, -- bytes
  duration INTEGER NOT NULL, -- seconds
  mime_type VARCHAR(50) NOT NULL,

  transcription_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
  transcription_text TEXT,
  transcription_confidence FLOAT, -- 0-1

  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_voice_handoff ON voice_recordings(handoff_id);
CREATE INDEX idx_voice_status ON voice_recordings(transcription_status);
```

#### audit_logs
```sql
CREATE TABLE audit_logs (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  handoff_id UUID REFERENCES handoffs(id),

  action VARCHAR(50) NOT NULL, -- 'created', 'viewed', 'edited', 'exported', 'deleted'
  resource_type VARCHAR(50) NOT NULL, -- 'handoff', 'patient', 'user'
  resource_id UUID,

  ip_address INET,
  user_agent TEXT,
  metadata JSONB,

  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_handoff ON audit_logs(handoff_id, created_at DESC);
CREATE INDEX idx_audit_action ON audit_logs(action, created_at DESC);
```

### Prisma Schema

See `apps/backend/prisma/schema.prisma` for the complete Prisma schema definition.

---

## 4. API Documentation

### Authentication

#### POST /api/v1/auth/register
Register a new user account.

**Request:**
```json
{
  "email": "nurse@hospital.com",
  "password": "SecurePass123!",
  "firstName": "Jane",
  "lastName": "Doe",
  "role": "nurse",
  "specialty": "Emergency Medicine",
  "department": "Emergency Department"
}
```

**Response (201):**
```json
{
  "user": {
    "id": "uuid",
    "email": "nurse@hospital.com",
    "firstName": "Jane",
    "lastName": "Doe",
    "role": "nurse"
  },
  "accessToken": "jwt-token",
  "refreshToken": "jwt-refresh-token"
}
```

#### POST /api/v1/auth/login
Authenticate and receive access/refresh tokens.

**Request:**
```json
{
  "email": "nurse@hospital.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "user": { /* user object */ },
  "accessToken": "jwt-token",
  "refreshToken": "jwt-refresh-token"
}
```

### Handoffs

#### POST /api/v1/handoffs
Create a new handoff.

**Request:**
```json
{
  "patientId": "uuid",
  "toUserId": "uuid",
  "handoffType": "shift_change",
  "priority": "routine"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "patientId": "uuid",
  "fromUserId": "uuid",
  "toUserId": "uuid",
  "handoffType": "shift_change",
  "priority": "routine",
  "status": "pending",
  "createdAt": "2025-10-24T10:30:00Z"
}
```

#### POST /api/v1/handoffs/:id/voice
Upload voice recording for a handoff.

**Request:** Multipart form data
- `audio`: Audio file (webm, mp3, wav)

**Response (200):**
```json
{
  "voiceRecordingId": "uuid",
  "status": "processing",
  "estimatedTime": 30
}
```

#### GET /api/v1/handoffs/:id
Get handoff details including SBAR report.

**Response (200):**
```json
{
  "id": "uuid",
  "patient": { /* patient object */ },
  "fromUser": { /* user object */ },
  "toUser": { /* user object */ },
  "handoffType": "shift_change",
  "priority": "routine",
  "status": "completed",
  "transcription": "Patient handoff for...",
  "sbar": {
    "situation": "...",
    "background": "...",
    "assessment": "...",
    "recommendation": "..."
  },
  "qualityScore": 92,
  "completenessScore": 95,
  "criticalElementsScore": 90,
  "createdAt": "2025-10-24T10:30:00Z",
  "completedAt": "2025-10-24T10:35:00Z"
}
```

#### GET /api/v1/handoffs
List handoffs with filtering and pagination.

**Query Parameters:**
- `status`: Filter by status (pending, completed, etc.)
- `fromUserId`: Filter by sender
- `patientId`: Filter by patient
- `startDate`, `endDate`: Date range
- `page`, `limit`: Pagination

**Response (200):**
```json
{
  "handoffs": [ /* array of handoff objects */ ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

### Voice Processing

#### GET /api/v1/voice/:id/status
Check transcription status.

**Response (200):**
```json
{
  "id": "uuid",
  "status": "completed",
  "transcription": "Patient handoff for...",
  "confidence": 0.95,
  "duration": 85
}
```

### Export

#### GET /api/v1/handoffs/:id/export/pdf
Export handoff as PDF.

**Response:** PDF file (application/pdf)

---

## 5. AI/ML Pipeline

### Voice Processing Pipeline

```
Audio Upload → R2 Storage → Azure Whisper → Transcription → SBAR Generation → Quality Scoring
```

### Step 1: Audio Upload
- **Input:** Audio file (webm, mp3, wav)
- **Process:**
  1. Validate file format and size (< 50MB)
  2. Upload to Cloudflare R2 with unique key
  3. Create `voice_recordings` record
  4. Enqueue transcription job

### Step 2: Transcription (Azure Whisper)
- **Worker:** `voice-processor-worker`
- **Process:**
  1. Download audio from R2
  2. Send to Azure OpenAI Whisper API
  3. Receive transcription text + confidence score
  4. Update `voice_recordings` table
  5. Enqueue SBAR generation job

**Azure Whisper Config:**
```typescript
const response = await openai.audio.transcriptions.create({
  file: audioStream,
  model: "whisper-1",
  language: "en",
  response_format: "verbose_json",
  prompt: "Medical handoff for patient..." // Context priming
});
```

### Step 3: SBAR Generation (GPT-4)
- **Worker:** `sbar-generator-worker`
- **Process:**
  1. Take transcription text
  2. Send to GPT-4 with SBAR prompt template
  3. Parse JSON response into 4 SBAR sections
  4. Update `handoffs` table
  5. Enqueue quality scoring job

**GPT-4 Prompt Template:**
```
You are a medical assistant helping to generate SBAR reports from clinical handoffs.

Transcription:
{transcription}

Generate a structured SBAR report in JSON format:
{
  "situation": "...",
  "background": "...",
  "assessment": "...",
  "recommendation": "..."
}

Guidelines:
- Situation: Current patient status, chief complaint, vital signs
- Background: Medical history, medications, allergies
- Assessment: Clinical evaluation, test results, trends
- Recommendation: Treatment plan, follow-up, concerns
```

### Step 4: Quality Scoring
- **Worker:** `quality-scorer-worker`
- **Scoring Criteria:**
  1. **Completeness Score** (0-100)
     - Are all 4 SBAR sections present?
     - Minimum word count per section?
  2. **Critical Elements Score** (0-100)
     - Patient identifier (name, MRN)
     - Allergies mentioned
     - Current medications listed
     - Vital signs included
     - Diagnosis/reason for admission
     - Treatment plan
  3. **Quality Score** (0-100)
     - Overall average of above
     - GPT-4 evaluation of clarity and completeness

---

## 6. Security & Compliance

### HIPAA Compliance

#### Administrative Safeguards
- ✅ Security Management Process
- ✅ Assigned Security Responsibility (CISO role)
- ✅ Workforce Security (background checks, NDA)
- ✅ Information Access Management (RBAC)
- ✅ Security Awareness Training
- ✅ Security Incident Procedures
- ✅ Contingency Plan (backup & disaster recovery)

#### Physical Safeguards
- ✅ Facility Access Controls (Azure datacenters)
- ✅ Workstation Security (encrypted laptops, VPN)
- ✅ Device and Media Controls (encrypted storage)

#### Technical Safeguards
- ✅ **Access Control:** JWT-based authentication, MFA optional
- ✅ **Audit Controls:** All PHI access logged (see `audit_logs` table)
- ✅ **Integrity:** Database checksums, file integrity monitoring
- ✅ **Transmission Security:** TLS 1.3 for all connections

### Encryption

#### Data at Rest
- **Database:** PostgreSQL with pgcrypto extension
- **File Storage:** Cloudflare R2 with AES-256 encryption
- **Backups:** Encrypted with Azure Storage Service Encryption

#### Data in Transit
- **HTTPS:** TLS 1.3 with strong cipher suites
- **API Calls:** All external API calls over HTTPS
- **WebSockets:** WSS (WebSocket Secure)

### Authentication & Authorization

#### JWT Strategy
- **Access Token:** Short-lived (15 minutes), contains user ID + role
- **Refresh Token:** Long-lived (7 days), stored in httpOnly cookie
- **Token Rotation:** Refresh tokens rotated on use

#### Role-Based Access Control (RBAC)
| Role | Permissions |
|------|-------------|
| **Nurse** | Create handoffs, view own handoffs, view patients |
| **Physician** | Create handoffs, view all handoffs, view/edit patients |
| **Admin** | All permissions + user management + system settings |

### Data Retention
- **Active Handoffs:** Retained indefinitely
- **Audit Logs:** Retained for 7 years (HIPAA requirement)
- **Voice Recordings:** Retained for 30 days, then deleted from R2

---

## 7. Deployment & Infrastructure

### Environment Setup

#### Development
```bash
# Clone repo
git clone https://github.com/rohimaya/eclipselink-ai.git
cd eclipselink-ai

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with local credentials

# Start database
docker-compose up -d postgres redis

# Run migrations
npm run migrate

# Start dev servers
npm run dev # Turborepo starts all apps
```

#### Staging
- **Hosting:** Azure Kubernetes Service (AKS)
- **Domain:** staging.eclipselink.ai
- **Database:** Azure Database for PostgreSQL (Flexible Server)
- **CI/CD:** GitHub Actions on push to `staging` branch

#### Production
- **Hosting:** Azure Kubernetes Service (AKS) with multi-region
- **Domain:** app.eclipselink.ai
- **Database:** Azure Database for PostgreSQL (High Availability)
- **CI/CD:** GitHub Actions on push to `main` branch (manual approval)

### Kubernetes Configuration

**Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eclipselink-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: eclipselink-backend
  template:
    metadata:
      labels:
        app: eclipselink-backend
    spec:
      containers:
      - name: backend
        image: eclipselink/backend:latest
        ports:
        - containerPort: 4000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: eclipselink-secrets
              key: database-url
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
            port: 4000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 4000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### CI/CD Pipeline

**GitHub Actions Workflow:**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
      - run: npm run lint

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: eclipselink/backend:${{ github.sha }},eclipselink/backend:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG }}
      - run: kubectl set image deployment/eclipselink-backend backend=eclipselink/backend:${{ github.sha }}
      - run: kubectl rollout status deployment/eclipselink-backend
```

---

## 8. Development Workflow

### Git Workflow
- **Main Branch:** `main` (production)
- **Staging Branch:** `staging` (pre-production)
- **Feature Branches:** `feature/[ticket-id]-description`
- **Bugfix Branches:** `bugfix/[ticket-id]-description`
- **Hotfix Branches:** `hotfix/[ticket-id]-description`

### Pull Request Process
1. Create feature branch from `main`
2. Implement feature with tests
3. Run `npm run lint` and `npm test` locally
4. Push branch and open PR
5. Automated checks run (tests, lint, build)
6. Code review by 2+ team members
7. Merge to `staging` for QA testing
8. After QA approval, merge to `main` for production

### Code Style
- **ESLint:** Airbnb config with TypeScript overrides
- **Prettier:** Auto-formatting on save
- **Commit Messages:** Conventional Commits format
  - `feat:` New feature
  - `fix:` Bug fix
  - `docs:` Documentation
  - `refactor:` Code refactoring
  - `test:` Add tests
  - `chore:` Tooling/dependencies

---

## 9. Testing Strategy

### Unit Tests
- **Framework:** Jest + React Testing Library
- **Coverage Target:** 80%+ for critical paths
- **Location:** `*.test.ts` files co-located with source

**Example:**
```typescript
describe('SBARGenerator', () => {
  it('should generate valid SBAR from transcription', async () => {
    const transcription = "Patient is a 60-year-old male...";
    const sbar = await generateSBAR(transcription);

    expect(sbar.situation).toBeDefined();
    expect(sbar.background).toBeDefined();
    expect(sbar.assessment).toBeDefined();
    expect(sbar.recommendation).toBeDefined();
  });
});
```

### Integration Tests
- **Framework:** Jest + Supertest
- **Database:** In-memory PostgreSQL (pg-mem)
- **Location:** `apps/backend/tests/integration`

**Example:**
```typescript
describe('POST /api/v1/handoffs', () => {
  it('should create a new handoff', async () => {
    const response = await request(app)
      .post('/api/v1/handoffs')
      .set('Authorization', `Bearer ${accessToken}`)
      .send({
        patientId: patientId,
        toUserId: userId,
        handoffType: 'shift_change',
        priority: 'routine'
      })
      .expect(201);

    expect(response.body.id).toBeDefined();
    expect(response.body.status).toBe('pending');
  });
});
```

### E2E Tests
- **Framework:** Playwright
- **Location:** `apps/frontend/tests/e2e`
- **Coverage:** Critical user flows

**Example:**
```typescript
test('complete handoff flow', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.fill('[name=email]', 'nurse@hospital.com');
  await page.fill('[name=password]', 'password123');
  await page.click('button[type=submit]');

  // Create handoff
  await page.click('text=New Handoff');
  await page.selectOption('[name=patient]', patientId);
  // ... rest of flow

  // Verify SBAR generated
  await page.waitForSelector('text=SBAR Report');
  expect(await page.textContent('[data-testid=situation]')).toContain('Patient');
});
```

---

## 10. Monitoring & Observability

### Application Performance Monitoring (APM)
- **Tool:** Datadog APM
- **Metrics:**
  - Request rate (requests/second)
  - Response time (p50, p95, p99)
  - Error rate (%)
  - Apdex score

### Logging
- **Tool:** Datadog Logs
- **Log Levels:** ERROR, WARN, INFO, DEBUG
- **Structured Logging:** JSON format with context

**Example:**
```typescript
logger.info('Handoff created', {
  handoffId: handoff.id,
  userId: user.id,
  patientId: patient.id,
  duration: Date.now() - startTime
});
```

### Error Tracking
- **Tool:** Sentry
- **Integration:** Automatic error capture + source maps
- **Alerting:** Slack notifications for production errors

### Custom Dashboards
- **Handoff Volume:** Handoffs created per hour/day
- **AI Performance:** Transcription accuracy, SBAR generation time
- **User Activity:** Active users, handoffs per user
- **System Health:** Database connections, queue depth, API latency

---

## 11. Roadmap & Future Work

### Q1 2026
- [ ] Mobile apps (iOS + Android) using React Native
- [ ] Offline mode for voice recording
- [ ] Spanish language support
- [ ] FHIR integration with Epic/Cerner

### Q2 2026
- [ ] Real-time collaboration (multiple users editing same handoff)
- [ ] Voice commands ("Hey EclipseLink, create a new handoff")
- [ ] Custom SBAR templates per specialty
- [ ] Advanced analytics and reporting

### Q3 2026
- [ ] AI-powered suggestions ("Did you mention allergies?")
- [ ] Predictive quality scoring (before completion)
- [ ] Integration with nurse call systems
- [ ] Telemedicine handoff support

### Q4 2026
- [ ] Global expansion (multi-language, multi-region)
- [ ] SOC 2 Type II certification
- [ ] FDA 510(k) clearance (if needed for clinical decision support)
- [ ] Enterprise SSO (SAML, OIDC)

---

## Appendix A: Environment Variables

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/eclipselink

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRES_IN=15m
REFRESH_TOKEN_EXPIRES_IN=7d

# Azure OpenAI
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_WHISPER=whisper-1
AZURE_OPENAI_DEPLOYMENT_GPT4=gpt-4

# Cloudflare R2
R2_ACCOUNT_ID=your-account-id
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
R2_BUCKET_NAME=eclipselink-audio

# Email
SENDGRID_API_KEY=your-sendgrid-key
FROM_EMAIL=noreply@eclipselink.ai

# App
NODE_ENV=development
PORT=4000
CORS_ORIGIN=http://localhost:3000
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:4000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:4000
NEXT_PUBLIC_APP_NAME=EclipseLink AI
```

---

## Appendix B: Useful Commands

```bash
# Development
npm run dev              # Start all apps in dev mode
npm run build            # Build all apps for production
npm run test             # Run all tests
npm run lint             # Run ESLint on all code
npm run format           # Format code with Prettier

# Database
npm run migrate          # Run Prisma migrations
npm run seed             # Seed database with test data
npm run db:studio        # Open Prisma Studio (DB GUI)

# Docker
docker-compose up -d     # Start local dependencies
docker-compose down      # Stop local dependencies
docker-compose logs -f   # View logs

# Production
npm run start            # Start production servers
npm run logs             # View production logs
kubectl get pods         # Check Kubernetes pods
kubectl logs <pod-name>  # View pod logs
```

---

## Contact & Support

**For Development Questions:**
- Slack: #eng-eclipselink
- Email: dev@rohimaya.ai

**For Production Issues:**
- PagerDuty: On-call rotation
- Slack: #incidents

**Documentation Updates:**
- Submit PR to update this document
- Tag @tech-lead for review

---

*Last Updated: October 24, 2025*
*Version: 1.0.0*
*© 2025 Rohimaya Health AI. All rights reserved.*
