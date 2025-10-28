# EclipseLink AI™

<div align="center">

![EclipseLink AI](https://img.shields.io/badge/EclipseLink-AI-1a9b8e?style=for-the-badge)
![Version](https://img.shields.io/badge/version-1.0.0-f4c430?style=for-the-badge)
![License](https://img.shields.io/badge/license-Proprietary-1a2332?style=for-the-badge)

**Voice-enabled clinical handoff platform for hospitals**

Transforming 3-5 minute voice recordings into structured SBAR reports in under 30 seconds

[Quick Start](#-quick-start) • [Features](#-features) • [Architecture](#-architecture) • [Support](#-support)

</div>

---

## 🦚 About

EclipseLink AI™ is a **HIPAA-compliant voice-enabled clinical handoff platform** that helps healthcare professionals create structured SBAR reports using AI.

**Key Benefits:**
- 📉 Reduce handoff time from 5 minutes to 30 seconds
- 🎯 Eliminate 80% of medical errors caused by poor handoffs
- ⏱️ Save clinicians 45-60 minutes per shift
- 🏆 Earn rewards points for using the system (Phoenix & Peacock Honors™)

**Built by:** Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO) at **Rohimaya Health AI**

---

## ✨ Features

### Core Features
- 🎙️ **Voice-to-SBAR Conversion** - Record voice, get structured SBAR reports in 30 seconds
- 📱 **Works Offline** - Record handoffs without internet, syncs when online
- 🚨 **Critical Alert Detection** - AI detects life-threatening information automatically
- ⚡ **Update-Only Model™** - 80% faster subsequent handoffs (30-45 sec vs 3-5 min)
- 🏥 **EHR Integration** - Works with Epic, Cerner, MEDITECH
- 👨‍👩‍👧‍👦 **Family Portal** - Plain-language updates for patient families
- 🤖 **AI Chatbot** - Ask questions about patients and handoffs
- 🌍 **50+ Languages** - Real-time translation for diverse populations
- 🏆 **Rewards Program** - Earn points for PTO, meals, spa days, more

### Deployment Options
- ☁️ **Cloud (HIPAA-compliant)** - For small hospitals and clinics
- 🏢 **On-Premise** - For large hospital systems with dedicated infrastructure
- 🔀 **Hybrid** - Mix and match based on your needs

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose ([Install](https://docs.docker.com/get-docker/))
- Node.js 18+ ([Install](https://nodejs.org/))
- Azure OpenAI account ([Apply](https://azure.microsoft.com/en-us/products/ai-services/openai-service))

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/HPagade/rohimaya-ai-eclipselink-product.git
cd rohimaya-ai-eclipselink-product

# Copy environment configuration
cp .env.example .env

# Edit .env with your Azure OpenAI credentials and other settings
nano .env  # or use your preferred editor
```

### 2. Start with Docker (Fastest)

```bash
# Start all services (database, backend, frontend, redis)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access the app:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:4000
- API Docs: http://localhost:4000/api/docs

### 3. Development Mode (Without Docker)

```bash
# Install dependencies
npm install

# Set up database (requires PostgreSQL running)
npm run db:setup

# Start development servers
npm run dev

# Or start separately
npm run dev:frontend  # Port 3000
npm run dev:backend   # Port 4000
```

---

## 👥 User Roles

EclipseLink AI serves **9+ million healthcare professionals** across 15 roles:

**Primary Users:**
- Registered Nurses (RN)
- Licensed Practical Nurses (LPN)
- Certified Nursing Assistants (CNA)
- Physicians (MD/DO)
- Nurse Practitioners (NP)
- Physician Assistants (PA)

**Specialized Users:**
- Respiratory Therapists (RT)
- Physical/Occupational Therapists (PT/OT)
- Pharmacists (PharmD)
- Social Workers (MSW/LCSW)
- Case Managers
- Medical Assistants (MA)
- Emergency Medical Technicians (EMT)
- Lab/Surgical/Radiologic Technicians
- System Administrators

Each role gets a tailored view with role-based permissions.

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Next.js 14 + React 18 (TypeScript)
- Tailwind CSS + shadcn/ui
- PWA (Progressive Web App) - works offline
- Zustand (state) + React Query (server state)

**Backend:**
- Express.js + TypeScript
- PostgreSQL 15+ (via Supabase)
- Redis (caching, queues)
- BullMQ (background jobs)

**AI Services:**
- Azure OpenAI Whisper (speech-to-text)
- Azure OpenAI GPT-4 (SBAR generation)

**Storage:**
- Cloudflare R2 (voice recordings)
- PostgreSQL (structured data)

**Deployment:**
- Cloud: Railway (backend) + Cloudflare Pages (frontend) + Supabase (database)
- On-Premise: Kubernetes + PostgreSQL HA + NFS/SAN storage

### Key Workflows

**1. New Handoff (Voice-to-SBAR)**
```
Clinician records voice (3-5 min)
  ↓
Upload to storage (2-5 sec)
  ↓
AI transcription via Whisper (15-30 sec)
  ↓
AI generates SBAR via GPT-4 (10-20 sec)
  ↓
Clinician reviews and approves
  ↓
Export to EHR (optional)
  ↓
Earn rewards points 🏆
```

**2. Update-Only Handoff (80% faster)**
```
Select existing patient
  ↓
Record only what changed (30-45 sec)
  ↓
AI merges update into existing SBAR
  ↓
Submit (total time: 60 sec vs 5 min!)
  ↓
Earn rewards points 🏆
```

---

## 📊 Database Schema

**15 Core Tables:**
1. `facilities` - Healthcare facilities
2. `staff` - Healthcare professionals
3. `patients` - Patient records (PHI)
4. `handoffs` - Clinical handoffs
5. `voice_recordings` - Audio metadata
6. `ai_generations` - AI processing jobs
7. `sbar_reports` - Generated SBAR reports
8. `handoff_assignments` - Staff assignments
9. `audit_logs` - HIPAA audit trail (7-year retention)
10. `notifications` - Real-time notifications
11. `ehr_connections` - EHR configurations
12. `ehr_sync_logs` - EHR sync history
13. `user_sessions` - JWT sessions
14. `feature_flags` - Feature toggles
15. `system_settings` - App configuration

**Security Features:**
- Row-Level Security (RLS) - facility-level isolation
- End-to-end encryption (AES-256 at rest, TLS 1.3 in transit)
- Comprehensive audit logging
- HIPAA-compliant by design

---

## 🛠️ Development Commands

```bash
# Development
npm run dev                # Start all services
npm run dev:frontend       # Frontend only (port 3000)
npm run dev:backend        # Backend only (port 4000)

# Building
npm run build              # Build for production
npm run build:frontend     # Build frontend only
npm run build:backend      # Build backend only

# Testing
npm test                   # Run all tests
npm run test:watch         # Watch mode
npm run test:coverage      # Coverage report

# Code Quality
npm run lint               # Run linter
npm run lint:fix           # Fix linting issues
npm run format             # Format with Prettier
npm run type-check         # TypeScript check

# Database
npm run db:setup           # Initialize database
npm run db:migrate         # Run migrations
npm run db:seed            # Seed test data
npm run db:reset           # Reset database (⚠️ deletes all data)

# Docker
docker-compose up -d       # Start all services
docker-compose down        # Stop services
docker-compose logs -f     # View logs
```

---

## 🔒 HIPAA Compliance

EclipseLink AI is built HIPAA-compliant from the ground up:

✅ **Technical Safeguards**
- End-to-end encryption (AES-256 at rest, TLS 1.3 in transit)
- Row-Level Security (RLS) for data isolation
- Comprehensive audit logging (7-year retention)
- Automatic session timeout
- Multi-factor authentication (MFA)
- Role-Based Access Control (RBAC)

✅ **Administrative Safeguards**
- Business Associate Agreements (BAA) with all vendors
- Security risk assessments
- Incident response procedures
- Regular security training
- Access reviews and monitoring

✅ **Physical Safeguards**
- On-premise: Customer-controlled data centers
- Cloud: SOC 2 Type II certified providers
- Encrypted backups with point-in-time recovery
- Disaster recovery procedures

---

## 🌐 Deployment

### Cloud Deployment (Small Hospitals)

**Services:**
- Frontend: Cloudflare Pages (CDN + hosting)
- Backend: Railway (auto-scaling Node.js)
- Database: Supabase (PostgreSQL 15+ with backups)
- Storage: Cloudflare R2 (S3-compatible)
- Cache: Upstash Redis (serverless)

**Cost:** ~$200-500/month for 50-200 users

### On-Premise Deployment (Large Hospitals)

**Requirements:**
- Kubernetes cluster (3+ nodes)
- PostgreSQL HA (primary + replica)
- Redis cluster (Sentinel mode)
- NFS/SAN storage for voice recordings
- VPN/private endpoint to Azure OpenAI

**Provided:**
- Kubernetes manifests
- Helm charts
- Deployment scripts
- Monitoring stack (Prometheus + Grafana)

**Cost:** Hospital infrastructure + Azure OpenAI API usage

---

## 🔗 Integration with Rohimaya Health AI Ecosystem

EclipseLink AI is part of the **Rohimaya Health AI** 8-product suite with **$50+ billion combined TAM**:

1. **EclipseLink AI™** - Clinical handoffs ($18.9B TAM) **← YOU ARE HERE**
2. **PlumeDose AI™** - Medication management ($8.4B TAM)
3. **RiseGuard AI™** - Fall prevention ($6.2B TAM)
4. **LunarBridge AI™** - Clinical trial matching ($3.8B TAM)
5. **FeatherSight AI™** - Lab intelligence ($5.1B TAM)
6. **PhoenixBreath AI™** - Respiratory monitoring ($2.9B TAM)
7. **WingStrength AI™** - PT/OT optimization ($4.6B TAM)
8. **Phoenix & Peacock Honors™** - Universal rewards program

**Cross-Product Integration Example:**
```
PlumeDose detects medication change
  ↓
RiseGuard recalculates fall risk
  ↓
EclipseLink adds alert to handoff automatically
  ↓
All staff notified in real-time
  ↓
Earn rewards points across all products
```

---

## 📚 Documentation

### Quick Links
- **[Wireframes & User Flows](WIREFRAMES.md)** - UI mockups and navigation flows
- **[Setup Guide](SETUP.md)** - Detailed installation instructions
- **[Developer Guide](README-DEVELOPERS.md)** - Development workflow and best practices
- **[User Guide](README-USERS.md)** - End-user documentation
- **[Changelog](CHANGELOG.md)** - Version history and changes

### Archived Documentation
Comprehensive technical documentation is available in `docs/archive/`:
- Architecture overview
- Database schema and ERD
- API documentation (auth, handoffs, SBAR, EHR)
- Security and HIPAA compliance
- Deployment and DevOps
- Testing strategy
- Scaling and roadmap

---

## 🤝 Support

### Getting Help
- 📖 **Documentation:** See links above
- 🐛 **Bug Reports:** GitHub/GitLab Issues
- 💬 **Questions:** support@rohimaya.ai
- 🏢 **Enterprise Support:** enterprise@rohimaya.ai

### Contact

**Rohimaya Health AI**

**Hannah Kraulik Pagade** - CEO
**Prasad Pagade** - CTO

📧 Email: info@rohimaya.ai
🌐 Website: https://rohimaya.ai
💼 LinkedIn: [Rohimaya Health AI](https://linkedin.com/company/rohimaya-health-ai)

---

## 📄 License

**Proprietary Software** - © 2025 Rohimaya Health AI. All rights reserved.

Unauthorized copying, modification, distribution, or use is strictly prohibited without express written permission.

For licensing inquiries: licensing@rohimaya.ai

---

<div align="center">

Made with ❤️ by Rohimaya Health AI

**EclipseLink AI™** - Transforming Clinical Handoffs with AI

*Improving Patient Safety, One Handoff at a Time*

</div>
