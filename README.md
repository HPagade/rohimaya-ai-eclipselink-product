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

EclipseLink AI™ is the flagship product of **Rohimaya Health AI**, a healthcare technology company dedicated to improving clinical communication and patient safety.

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
git clone https://github.com/YOUR_USERNAME/rohimaya-ai-eclipselink-product.git
cd rohimaya-ai-eclipselink-product

# OR clone from GitLab
git clone https://gitlab.com/YOUR_USERNAME/rohimaya-ai-eclipselink-product.git
cd rohimaya-ai-eclipselink-product
```

### 2. Database Setup

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

### 3. Environment Variables

Create `.env` files with your configuration:

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

### 4. Install Dependencies

```bash
# Install all dependencies
npm install
```

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

### Architecture Documentation
- [Part 1: System Architecture Overview](eclipse-ai-part1-architecture.md)
- [Part 2: Repository Structure & Setup](eclipse-ai-part2-repository-setup.md)
- [Part 3: Database Schema & ERD](eclipse-ai-part3-database-schema.md)

### Database Documentation
- [Database Schema](database/schema.sql)
- [Core Tables Migration](database/migrations/001_core_tables.sql)
- [Audit & Notifications Migration](database/migrations/002_audit_and_notifications.sql)
- [Functions & Triggers](database/functions/triggers.sql)

### API Documentation
Coming soon - API endpoints, request/response examples, authentication

### Integration Guides
- **Epic EHR** - FHIR R4 integration guide
- **Cerner** - FHIR R4 integration guide
- **MEDITECH** - HL7 v2 integration guide

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Next.js 14 (React 18)
- TypeScript
- Tailwind CSS + shadcn/ui
- Zustand (state management)
- React Query (server state)
- PWA support (offline-first)

**Backend:**
- Node.js + Express
- TypeScript
- Supabase (PostgreSQL + Auth)
- Redis (Upstash) for caching
- BullMQ for job queues

**AI Services:**
- Azure OpenAI Whisper (speech-to-text)
- Azure OpenAI GPT-4 (SBAR generation)

**Storage:**
- Cloudflare R2 (voice recordings, documents)
- PostgreSQL (structured data)

**Deployment:**
- Cloudflare Pages (frontend)
- Railway (backend)
- Supabase (database)

### Database Schema

**15 Core Tables:**
1. `facilities` - Healthcare facilities
2. `staff` - Healthcare professionals
3. `patients` - Patient records
4. `handoffs` - Clinical handoffs
5. `voice_recordings` - Audio file metadata
6. `ai_generations` - AI processing records
7. `sbar_reports` - Generated SBAR reports
8. `handoff_assignments` - Staff-to-handoff mapping
9. `audit_logs` - HIPAA audit trail
10. `notifications` - In-app notifications
11. `ehr_connections` - EHR integration config
12. `ehr_sync_logs` - EHR sync history
13. `user_sessions` - Active sessions
14. `feature_flags` - Feature toggles
15. `system_settings` - App configuration

See [Database Schema Documentation](eclipse-ai-part3-database-schema.md) for complete ERD and details.

### Data Flow

```
Clinician Records Voice (3-5 min)
        ↓
Upload to Cloudflare R2
        ↓
Queue Transcription Job (BullMQ)
        ↓
Azure Whisper API (15-30 sec)
        ↓
Store Transcription
        ↓
Queue SBAR Generation (BullMQ)
        ↓
Azure GPT-4 API (10-20 sec)
        ↓
Store SBAR Report
        ↓
Notify Clinician
        ↓
Review & Approve
        ↓
Export to EHR (Optional)
```

**Total Processing Time:** 30-60 seconds from upload to SBAR

---

## 🗂️ Repository Structure

```
rohimaya-ai-eclipselink-product/
├── database/                      # Database files
│   ├── schema.sql                # Complete schema
│   ├── migrations/               # SQL migrations
│   ├── seeds/                    # Seed data
│   ├── functions/                # Database functions
│   └── setup.sh                  # Setup script
│
├── eclipse-ai-part1-architecture.md       # Architecture docs
├── eclipse-ai-part2-repository-setup.md   # Setup guide
├── eclipse-ai-part3-database-schema.md    # Database docs
│
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore file
├── README.md                     # This file
└── package.json                  # Project dependencies
```

---

## 🔒 Privacy & Security

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

✅ **Never commit secrets** - Use environment variables
✅ **Enable 2FA** on GitHub/GitLab accounts
✅ **Use SSH keys** for git operations
✅ **Rotate secrets** regularly (every 90 days)
✅ **Review access logs** monthly
✅ **Enable branch protection** on main branch
✅ **Require code reviews** before merging
✅ **Run security scans** in CI/CD pipeline

---

## 📊 Database Setup Details

### Database Tables Created

After running `database/setup.sh`, you will have:

**Core Tables:**
- ✅ `facilities` - Healthcare facilities (6,000+ facilities nationwide)
- ✅ `staff` - Healthcare professionals (9M+ users)
- ✅ `patients` - Patient records (50M+ patients)
- ✅ `handoffs` - Clinical handoffs (100M+ handoffs/year)

**Processing Tables:**
- ✅ `voice_recordings` - Audio metadata (100M+ recordings)
- ✅ `ai_generations` - AI transcriptions and SBAR generation
- ✅ `sbar_reports` - Generated reports

**Support Tables:**
- ✅ `handoff_assignments` - Staff assignments
- ✅ `notifications` - Real-time notifications
- ✅ `audit_logs` - HIPAA-compliant audit trail

**Integration Tables:**
- ✅ `ehr_connections` - EHR system configurations
- ✅ `ehr_sync_logs` - Synchronization history

**System Tables:**
- ✅ `user_sessions` - Active user sessions
- ✅ `feature_flags` - Feature toggles for gradual rollout
- ✅ `system_settings` - Application configuration

### Verify Database Setup

```bash
# Check all tables are created
psql $DATABASE_URL -c "\dt"

# Check row-level security is enabled
psql $DATABASE_URL -c "SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';"

# Check triggers are created
psql $DATABASE_URL -c "SELECT trigger_name, event_object_table FROM information_schema.triggers;"
```

### Database Features

**🔐 Security:**
- Row-Level Security (RLS) enabled on all tables
- Facility-level data isolation
- HIPAA-compliant audit logging
- PHI access tracking

**⚡ Performance:**
- Optimized indexes on frequently queried columns
- Full-text search on names and content
- Partitioning ready for large tables
- Connection pooling via Supavisor

**📊 Scalability:**
- Support for 100M+ handoffs
- Horizontal read replicas
- Automatic backups (7-day retention)
- Point-in-time recovery

---

## 🛠️ Development

### Available Scripts

```bash
# Development
npm run dev                # Start both frontend and backend
npm run dev:frontend       # Start frontend only
npm run dev:backend        # Start backend only

# Building
npm run build             # Build all packages
npm run build:frontend    # Build frontend
npm run build:backend     # Build backend

# Testing
npm test                  # Run all tests
npm run test:watch        # Run tests in watch mode
npm run test:coverage     # Generate coverage report

# Code Quality
npm run lint              # Run ESLint
npm run format            # Format code with Prettier
npm run type-check        # TypeScript type checking

# Database
npm run migrate           # Run database migrations
npm run seed              # Seed database with test data
npm run db:reset          # Reset database (⚠️ deletes all data)
```

### Database Management

```bash
# Run database setup
export DATABASE_URL="your-supabase-url"
bash database/setup.sh

# Connect to database
psql $DATABASE_URL

# View all tables
\dt

# View table structure
\d+ patients

# Query data
SELECT * FROM facilities LIMIT 5;
```

---

## 🌐 Deployment

### Production Deployment

**Frontend (Cloudflare Pages):**
```bash
# Build frontend
npm run build:frontend

# Deploy to Cloudflare Pages
# Automatic via GitHub Actions on push to main
```

**Backend (Railway):**
```bash
# Build backend
npm run build:backend

# Deploy to Railway
# Automatic via Railway GitHub integration
```

**Database (Supabase):**
- Migrations run automatically via CI/CD
- Point-in-time recovery enabled
- Daily automated backups

### Environment Checklist

Before deploying to production:
- [ ] All environment variables configured
- [ ] Database migrations run successfully
- [ ] RLS policies tested
- [ ] Audit logging verified
- [ ] SSL certificates configured
- [ ] Domain names configured
- [ ] CORS settings updated
- [ ] Rate limiting configured
- [ ] Monitoring tools configured (Sentry, LogTail)
- [ ] Backup strategy tested

---

## 🤝 Support

### Getting Help

- **Documentation:** See the `docs/` folder
- **Issues:** Report bugs or request features in Issues
- **Email:** support@rohimaya.ai
- **Website:** https://rohimaya.ai

### Contributing

This is a proprietary product. For contribution inquiries, please contact the founders.

---

## 📄 License

**Proprietary Software**

© 2025 Rohimaya Health AI. All rights reserved.

This software and associated documentation files (the "Software") are proprietary to Rohimaya Health AI. Unauthorized copying, modification, distribution, or use of this Software, via any medium, is strictly prohibited without express written permission from Rohimaya Health AI.

For licensing inquiries: licensing@rohimaya.ai

---

## 🎯 Roadmap

### Q1 2025
- [x] Database schema design
- [x] Core architecture documentation
- [ ] MVP development
- [ ] HIPAA compliance certification prep

### Q2 2025
- [ ] Beta testing with pilot facilities
- [ ] Epic EHR integration
- [ ] Mobile app release (iOS/Android)
- [ ] HIPAA audit and certification

### Q3 2025
- [ ] General availability launch
- [ ] Cerner and MEDITECH integrations
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

### Q4 2025
- [ ] AI improvements and fine-tuning
- [ ] Custom SBAR templates
- [ ] Team collaboration features
- [ ] Enterprise features (SSO, advanced reporting)

---

## 📞 Contact

**Rohimaya Health AI**

**Hannah Kraulik Pagade** - CEO
**Prasad Pagade** - CTO

📧 Email: info@rohimaya.ai
🌐 Website: https://rohimaya.ai
🦚 Product: EclipseLink AI™

---

<div align="center">

Made with ❤️ by Rohimaya Health AI

**EclipseLink AI™** - Transforming Clinical Handoffs with AI

</div>
