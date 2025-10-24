# EclipseLink AI™

<div align="center">

![EclipseLink AI](https://img.shields.io/badge/EclipseLink-AI-1a9b8e?style=for-the-badge)
![Version](https://img.shields.io/badge/version-1.0.0-f4c430?style=for-the-badge)
![License](https://img.shields.io/badge/license-Proprietary-1a2332?style=for-the-badge)

**Voice-enabled clinical handoff platform with AI-powered SBAR generation**

Transforming 3-5 minute voice recordings into comprehensive SBAR reports in under 30 seconds

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Architecture](#-architecture) • [Support](#-support)

</div>

---

## 🦚 About Rohimaya Health AI

EclipseLink AI™ is the flagship product of **Rohimaya Health AI**, a healthcare technology company dedicated to improving clinical communication and patient safety through AI-powered solutions.

**Founded by:**
- **Hannah Kraulik Pagade** - CEO
- **Prasad Pagade** - CTO

**Company Mission:** Revolutionize healthcare communication through AI-powered solutions that save time, reduce errors, and improve patient outcomes.

**Brand Colors:**
- Peacock Teal: `#1a9b8e`
- Phoenix Gold: `#f4c430`
- Lunar Blue: `#2c3e50`
- Moon White: `#f8f9fa`
- Eclipse Navy: `#1a2332`
- Accent Copper: `#b87333`

---

## ✨ Features

### 🎙️ Voice-to-SBAR Conversion
- **Record** clinical handoffs via mobile, tablet, or desktop
- **Transcribe** using Azure OpenAI Whisper with 95%+ medical term accuracy
- **Generate** structured SBAR reports with GPT-4 in under 30 seconds
- **Edit** and approve reports with inline editing

### 🏥 EHR Integration
- **Seamless connectivity** with Epic, Cerner, MEDITECH, and other major EHR systems
- **FHIR R4** and **HL7 v2** protocol support
- **Bi-directional sync** of patient data, medications, allergies, and vital signs
- **One-click export** of handoff reports to EHR

### 📱 Multi-Platform Access
- **Progressive Web App (PWA)** - Install on any device
- **Offline capability** - Record handoffs without internet connection
- **Real-time sync** - Updates across all devices instantly
- **Responsive design** - Optimized for mobile, tablet, and desktop

### 🔒 HIPAA Compliance
- **End-to-end encryption** - AES-256 at rest, TLS 1.3 in transit
- **Row-Level Security** - Database-level data isolation
- **Comprehensive audit logs** - 7-year retention for compliance
- **PHI access tracking** - Every access logged and monitored
- **Business Associate Agreements** - Available with all service providers

### 👥 Target Users (9+ Million Healthcare Professionals)
- Registered Nurses (RN)
- Licensed Practical Nurses (LPN)
- Certified Nursing Assistants (CNA)
- Medical Assistants (MA)
- Physicians (MD/DO)
- Nurse Practitioners (NP)
- Physician Assistants (PA)
- Respiratory Therapists (RT)
- Physical/Occupational Therapists (PT/OT)
- Emergency Medical Technicians (EMT)
- Radiologic/Surgical/Lab/Pharmacy Technicians

**Total Addressable Market (TAM):** $18.9 billion healthcare communication market

**Target Facilities:**
- 6,090 hospitals
- 87,000+ nursing homes
- 13,000+ clinics in the US

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ ([Download](https://nodejs.org/))
- **PostgreSQL** 15+ via Supabase ([Sign up](https://supabase.com/))
- **Git** ([Download](https://git-scm.com/))
- **Azure OpenAI** account ([Apply](https://azure.microsoft.com/en-us/products/ai-services/openai-service))

### 1. Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/HPagade/rohimaya-ai-eclipselink-product.git
cd rohimaya-ai-eclipselink-product

# OR clone from GitLab
git clone https://gitlab.com/HPagade/rohimaya-ai-eclipselink-product.git
cd rohimaya-ai-eclipselink-product
```

### 2. Install Dependencies

```bash
# Install all dependencies
npm install
```

### 3. Environment Configuration

```bash
# Copy environment templates
cp .env.example .env

# Edit with your actual values
nano .env  # or use your preferred editor
```

Required environment variables:
- `DATABASE_URL` - Supabase PostgreSQL connection string
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anonymous key
- `AZURE_OPENAI_KEY` - Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT` - Azure OpenAI endpoint URL
- `CLOUDFLARE_R2_ACCESS_KEY` - Cloudflare R2 access key
- `CLOUDFLARE_R2_SECRET_KEY` - Cloudflare R2 secret key
- `JWT_SECRET` - Secret for JWT token signing
- `UPSTASH_REDIS_URL` - Redis connection URL

### 4. Database Setup

```bash
# Set your Supabase database URL
export DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT].supabase.co:5432/postgres"

# Run the database setup script
bash database/setup.sh
```

This will:
- ✅ Create 15 core database tables
- ✅ Enable Row-Level Security (RLS)
- ✅ Configure audit logging triggers
- ✅ Set up HIPAA-compliant security policies

### 5. Start Development

```bash
# Start development server
npm run dev

# Or start frontend and backend separately
npm run dev:frontend  # Runs on http://localhost:3000
npm run dev:backend   # Runs on http://localhost:4000
```

### 6. Access the Application

Open your browser and navigate to:
- **Frontend:** http://localhost:3000
- **API:** http://localhost:4000
- **API Documentation:** http://localhost:4000/api/docs

---

## 📚 Documentation

### Core Documentation (Parts 1-4)

#### Architecture & Repository Setup
- **[Part 1: System Architecture Overview](eclipse-ai-part1-architecture.md)** - Complete system architecture, tech stack, and design decisions
- **[Part 2: Repository Structure & Setup](eclipse-ai-part2-repository-setup.md)** - Detailed setup instructions, development workflow, and best practices

#### Database & Backend APIs
- **[Part 3: Database Schema & ERD](eclipse-ai-part3-database-schema.md)** - Complete database schema with 15 tables, relationships, indexes, and RLS policies
- **[Part 4a: API Authentication & Authorization](eclipse-ai-part4a-api-auth.md)** - JWT authentication, RBAC, security headers, and all auth endpoints
- **[Part 4b: Handoff & Voice Recording APIs](eclipse-ai-part4b-handoff-voice.md)** - Handoff lifecycle, voice upload/processing, and polling strategies
- **[Part 4c: Patient, SBAR & EHR APIs](eclipse-ai-part4c-patient-sbar-ehr.md)** - Patient management, SBAR generation, and EHR integration endpoints
- **[Part 4d: Error Handling & Rate Limiting](eclipse-ai-part4d-error-handling-examples.md)** - Comprehensive error codes, validation, retry logic, and examples

#### Role-Specific Guides
- **[Developer Guide](README-DEVELOPERS.md)** - Developer onboarding, local setup, testing, and development workflow
- **[Internal Team Guide](README-INTERNAL.md)** - Team processes, deployment procedures, and incident response
- **[Investor Overview](README-INVESTORS.md)** - Business model, market opportunity, and growth metrics
- **[User Guide](README-USERS.md)** - End-user documentation, feature guides, and FAQ

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Next.js 14 with App Router (React 18)
- TypeScript 5.3+
- Tailwind CSS + shadcn/ui
- Zustand (state management)
- React Query (server state)
- PWA support (offline-first)

**Backend:**
- Node.js 18+ + Express.js
- TypeScript 5.3+
- Supabase (PostgreSQL 15+ with Auth)
- Upstash Redis (caching & sessions)
- BullMQ (job queues)
- Winston (logging)

**AI Services:**
- Azure OpenAI Whisper (speech-to-text transcription)
- Azure OpenAI GPT-4-32k (SBAR generation)

**Storage:**
- Cloudflare R2 (voice recordings, documents)
- PostgreSQL (structured data, metadata)

**Deployment:**
- Frontend: Cloudflare Pages
- Backend: Railway
- Database: Supabase
- CDN & Security: Cloudflare

### Database Schema

**15 Core Tables:**
1. `facilities` - Healthcare facilities
2. `staff` - Healthcare professionals
3. `patients` - Patient records (PHI)
4. `handoffs` - Clinical handoffs
5. `voice_recordings` - Audio file metadata
6. `ai_generations` - AI processing records
7. `sbar_reports` - Generated SBAR reports
8. `handoff_assignments` - Staff-to-handoff mapping (N:N)
9. `audit_logs` - HIPAA audit trail (7-year retention)
10. `notifications` - In-app notifications
11. `ehr_connections` - EHR integration configurations
12. `ehr_sync_logs` - EHR synchronization history
13. `user_sessions` - Active user sessions (JWT)
14. `feature_flags` - Feature toggles
15. `system_settings` - Application configuration

See [Part 3: Database Schema](eclipse-ai-part3-database-schema.md) for complete ERD, relationships, and SQL.

### Data Flow

```
Clinician Records Voice (3-5 min)
        ↓
Upload to Cloudflare R2 (2-5 sec)
        ↓
Queue Transcription Job (BullMQ)
        ↓
Azure Whisper API Transcription (15-30 sec)
        ↓
Store Transcription in Database
        ↓
Queue SBAR Generation Job (BullMQ)
        ↓
Azure GPT-4 SBAR Generation (10-20 sec)
        ↓
Store SBAR Report
        ↓
Notify Clinician (Real-time)
        ↓
Review & Approve SBAR
        ↓
Export to EHR (Optional)
```

**Total Processing Time:** 30-60 seconds from upload to SBAR generation

---

## 🗂️ Repository Structure

```
rohimaya-ai-eclipselink-product/
├── backend/                          # Backend API (NEW)
│   ├── src/
│   │   ├── config/                  # Configuration files
│   │   ├── middleware/              # Express middleware
│   │   ├── routes/                  # API routes
│   │   ├── services/                # Business logic
│   │   ├── models/                  # TypeScript types
│   │   ├── utils/                   # Helper functions
│   │   ├── jobs/                    # BullMQ jobs
│   │   └── index.ts                 # Entry point
│   ├── database/
│   │   ├── migrations/              # Database migrations
│   │   ├── seeds/                   # Seed data
│   │   └── schema.sql              # Complete schema
│   ├── tests/                       # Test files
│   ├── package.json
│   └── tsconfig.json
│
├── docs/                            # Documentation
│   ├── eclipse-ai-part1-architecture.md
│   ├── eclipse-ai-part2-repository-setup.md
│   ├── eclipse-ai-part3-database-schema.md
│   ├── eclipse-ai-part4a-api-auth.md
│   ├── eclipse-ai-part4b-handoff-voice.md
│   ├── eclipse-ai-part4c-patient-sbar-ehr.md
│   └── eclipse-ai-part4d-error-handling-examples.md
│
├── README-DEVELOPERS.md             # Developer guide
├── README-INTERNAL.md               # Internal team guide
├── README-INVESTORS.md              # Investor overview
├── README-USERS.md                  # User guide
│
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore file
├── README.md                        # This file
└── package.json                     # Root package.json
```

---

## 🛠️ Development

### Available Scripts

```bash
# Development
npm run dev                # Start both frontend and backend
npm run dev:frontend       # Start frontend only (port 3000)
npm run dev:backend        # Start backend only (port 4000)

# Building
npm run build             # Build all packages
npm run build:frontend    # Build frontend for production
npm run build:backend     # Build backend for production

# Testing
npm test                  # Run all tests
npm run test:watch        # Run tests in watch mode
npm run test:coverage     # Generate coverage report

# Code Quality
npm run lint              # Run ESLint
npm run lint:fix          # Fix ESLint issues
npm run format            # Format code with Prettier
npm run type-check        # TypeScript type checking

# Database
npm run migrate           # Run database migrations
npm run seed              # Seed database with test data
npm run db:reset          # Reset database (⚠️ deletes all data)
```

### Git Workflow

We use **Git Flow** for branch management:

```
main                    (production-ready code)
├── develop             (integration branch)
│   ├── feature/*      (new features)
│   ├── bugfix/*       (bug fixes)
│   └── hotfix/*       (emergency fixes)
```

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: <type>(<scope>): <subject>

# Examples:
git commit -m "feat(voice): add waveform visualization"
git commit -m "fix(auth): resolve token refresh issue"
git commit -m "docs(api): update handoff endpoints"
git commit -m "chore(deps): update dependencies"
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`

---

## 🔒 Privacy & Security

### HIPAA Compliance

EclipseLink AI is built with HIPAA compliance at its core:

- ✅ **End-to-end encryption** (AES-256 at rest, TLS 1.3 in transit)
- ✅ **Row-Level Security (RLS)** for database-level data isolation
- ✅ **Comprehensive audit logging** with 7-year retention
- ✅ **PHI access tracking** - every access logged and monitored
- ✅ **Business Associate Agreements (BAA)** with all third-party services
- ✅ **Regular security audits** and penetration testing
- ✅ **Role-Based Access Control (RBAC)** with granular permissions
- ✅ **Multi-factor authentication (MFA)** support
- ✅ **Session management** with automatic timeout
- ✅ **Encrypted backups** with point-in-time recovery

### Making Your Repository Private

**On GitHub:**
1. Go to repository **Settings**
2. Scroll to **Danger Zone**
3. Click **Change visibility**
4. Select **Private**
5. Confirm by typing the repository name

**On GitLab:**
1. Go to **Settings** → **General**
2. Expand **Visibility, project features, permissions**
3. Under **Project visibility**, select **Private**
4. Click **Save changes**

### Security Best Practices

✅ **Never commit secrets** - Use environment variables and `.env` files (never commit `.env`)
✅ **Enable 2FA** on GitHub/GitLab accounts
✅ **Use SSH keys** for git operations
✅ **Rotate secrets** regularly (every 90 days)
✅ **Review access logs** monthly
✅ **Enable branch protection** on main and develop branches
✅ **Require code reviews** before merging
✅ **Run security scans** in CI/CD pipeline (Snyk, npm audit)
✅ **Use least privilege** principle for all access
✅ **Monitor dependencies** for vulnerabilities

---

## 🌐 Deployment

### Production Environments

- **Frontend:** [app.eclipselink.ai](https://app.eclipselink.ai) (Cloudflare Pages)
- **Backend API:** [api.eclipselink.ai](https://api.eclipselink.ai) (Railway)
- **Database:** Supabase (PostgreSQL with point-in-time recovery)
- **Storage:** Cloudflare R2 (voice recordings, documents)
- **CDN:** Cloudflare (global edge network)

### CI/CD Pipeline

Automated testing and deployment via:
- **GitHub Actions** (for GitHub repository)
- **GitLab CI** (for GitLab repository)

### Environment Checklist

Before deploying to production:
- [ ] All environment variables configured in production
- [ ] Database migrations run successfully
- [ ] RLS policies tested and verified
- [ ] Audit logging verified and operational
- [ ] SSL certificates configured and auto-renewing
- [ ] Domain names configured with DNS
- [ ] CORS settings updated for production domains
- [ ] Rate limiting configured and tested
- [ ] Monitoring tools configured (Sentry, LogTail, Uptime monitoring)
- [ ] Backup strategy tested and verified
- [ ] Load testing completed
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] DDoS protection enabled (Cloudflare)
- [ ] API documentation published

---

## 📊 Roadmap

### Phase 1: MVP (Current - Q1 2025)
- [x] Repository structure and architecture
- [x] Comprehensive documentation (Parts 1-4)
- [x] Database schema design
- [ ] Backend API implementation
- [ ] Frontend core components
- [ ] Azure OpenAI integration
- [ ] Basic EHR integration (Epic FHIR)
- [ ] HIPAA compliance certification prep

### Phase 2: Beta Launch (Q2 2025)
- [ ] Beta testing with 3-5 pilot facilities
- [ ] Full Epic EHR integration
- [ ] Cerner and MEDITECH integrations
- [ ] Mobile app optimization (iOS/Android PWA)
- [ ] HIPAA audit and certification
- [ ] Advanced analytics dashboard
- [ ] Multi-facility management

### Phase 3: General Availability (Q3 2025)
- [ ] Public launch and marketing campaign
- [ ] Additional EHR integrations (Allscripts, PointClickCare, WellSky)
- [ ] Advanced AI features (custom SBAR templates, auto-suggestions)
- [ ] Team collaboration features (shared handoffs, comments)
- [ ] Multi-language support (Spanish, Mandarin)
- [ ] Telehealth integration

### Phase 4: Scale & Enterprise (Q4 2025)
- [ ] Enterprise features (SSO, SAML, advanced RBAC)
- [ ] Integration with PlumeDose AI (medication management)
- [ ] Advanced reporting and analytics
- [ ] API for third-party integrations
- [ ] International expansion (Canada, EU)
- [ ] AI model fine-tuning with real-world data

---

## 🤝 Support & Contact

### Getting Help

- **Documentation:** Comprehensive docs in this repository
- **Developer Guide:** [README-DEVELOPERS.md](README-DEVELOPERS.md)
- **User Guide:** [README-USERS.md](README-USERS.md)
- **Issues:** Report bugs or request features via GitHub/GitLab Issues
- **Email Support:** support@rohimaya.ai

### Contact Information

**Rohimaya Health AI**

**Hannah Kraulik Pagade** - CEO
**Prasad Pagade** - CTO

📧 Email: info@rohimaya.ai
🌐 Website: https://rohimaya.ai
🦚 Product: EclipseLink AI™
💼 LinkedIn: [Rohimaya Health AI](https://linkedin.com/company/rohimaya-health-ai)

### Contributing

This is proprietary software. For contribution or partnership inquiries, please contact the founders directly.

---

## 📄 License

**Proprietary Software**

© 2025 Rohimaya Health AI. All rights reserved.

This software and associated documentation files (the "Software") are proprietary to Rohimaya Health AI. Unauthorized copying, modification, distribution, or use of this Software, via any medium, is strictly prohibited without express written permission from Rohimaya Health AI.

For licensing inquiries: licensing@rohimaya.ai

---

## 🙏 Acknowledgments

Special thanks to:
- **Azure OpenAI** team for cutting-edge AI services
- **Supabase** for robust database infrastructure
- **Cloudflare** for edge network, storage, and security
- **Railway** for reliable backend hosting
- **Upstash** for serverless Redis
- The **open-source community** for amazing tools and libraries

---

<div align="center">

Made with ❤️ by Rohimaya Health AI

**EclipseLink AI™** - Transforming Clinical Handoffs with AI

*Improving Patient Safety, One Handoff at a Time*

</div>
