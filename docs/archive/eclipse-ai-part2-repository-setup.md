# EclipseLink AI™ - Part 2: Repository Structure & Setup

**Document Version:** 1.0  
**Last Updated:** October 23, 2025  
**Product:** EclipseLink AI™ Clinical Handoff System  
**Company:** Rohimaya Health AI  
**Founders:** Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO)

---

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Complete Folder Structure](#complete-folder-structure)
3. [GitHub Setup Guide](#github-setup-guide)
4. [GitLab Setup Guide](#gitlab-setup-guide)
5. [Configuration Files](#configuration-files)
6. [Environment Variables](#environment-variables)
7. [Package Dependencies](#package-dependencies)
8. [Git Workflow](#git-workflow)
9. [Claude Code Integration](#claude-code-integration)
10. [Initial Setup Commands](#initial-setup-commands)

---

## 1. Repository Overview

### Repository Strategy
EclipseLink AI uses a **monorepo structure** with clear separation between frontend, backend, and shared code.

### Repository Names
- **GitHub**: `eclipselink-ai`
- **GitLab**: `eclipselink-ai`

### Branch Strategy
```
main (production)
├── develop (staging)
├── feature/* (feature branches)
├── bugfix/* (bug fixes)
└── hotfix/* (emergency fixes)
```

### Repository Structure Philosophy
- **Monorepo**: All code in one repository for easier management
- **Clear Separation**: Frontend, backend, and shared code are separate
- **TypeScript**: Type safety across the entire stack
- **Documentation**: Inline and separate documentation
- **Scripts**: Automation for common tasks

---

## 2. Complete Folder Structure

```
eclipselink-ai/
├── .github/                          # GitHub-specific files
│   ├── workflows/                    # GitHub Actions CI/CD
│   │   ├── deploy-frontend.yml
│   │   ├── deploy-backend.yml
│   │   ├── test.yml
│   │   └── security-scan.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .gitlab/                          # GitLab-specific files
│   ├── merge_request_templates/
│   │   └── default.md
│   └── issue_templates/
│       ├── bug.md
│       └── feature.md
│
├── apps/                             # Application code
│   ├── frontend/                     # Next.js PWA
│   │   ├── public/                   # Static assets
│   │   │   ├── icons/
│   │   │   │   ├── icon-192x192.png
│   │   │   │   ├── icon-512x512.png
│   │   │   │   └── favicon.ico
│   │   │   ├── images/
│   │   │   │   ├── logo.svg
│   │   │   │   ├── logo-dark.svg
│   │   │   │   └── placeholder-avatar.png
│   │   │   └── manifest.json
│   │   │
│   │   ├── src/
│   │   │   ├── app/                  # Next.js 14 App Router
│   │   │   │   ├── (auth)/           # Auth layout group
│   │   │   │   │   ├── login/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── register/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── forgot-password/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── layout.tsx
│   │   │   │   │
│   │   │   │   ├── (dashboard)/      # Dashboard layout group
│   │   │   │   │   ├── dashboard/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── handoffs/
│   │   │   │   │   │   ├── page.tsx
│   │   │   │   │   │   ├── new/
│   │   │   │   │   │   │   └── page.tsx
│   │   │   │   │   │   └── [id]/
│   │   │   │   │   │       ├── page.tsx
│   │   │   │   │   │       └── edit/
│   │   │   │   │   │           └── page.tsx
│   │   │   │   │   ├── patients/
│   │   │   │   │   │   ├── page.tsx
│   │   │   │   │   │   └── [id]/
│   │   │   │   │   │       └── page.tsx
│   │   │   │   │   ├── profile/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── settings/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── analytics/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── layout.tsx
│   │   │   │   │
│   │   │   │   ├── api/              # API Routes (BFF pattern)
│   │   │   │   │   ├── auth/
│   │   │   │   │   │   ├── login/
│   │   │   │   │   │   │   └── route.ts
│   │   │   │   │   │   ├── register/
│   │   │   │   │   │   │   └── route.ts
│   │   │   │   │   │   ├── logout/
│   │   │   │   │   │   │   └── route.ts
│   │   │   │   │   │   └── me/
│   │   │   │   │   │       └── route.ts
│   │   │   │   │   ├── handoffs/
│   │   │   │   │   │   ├── route.ts
│   │   │   │   │   │   └── [id]/
│   │   │   │   │   │       └── route.ts
│   │   │   │   │   ├── voice/
│   │   │   │   │   │   ├── upload/
│   │   │   │   │   │   │   └── route.ts
│   │   │   │   │   │   └── [id]/
│   │   │   │   │   │       └── route.ts
│   │   │   │   │   └── patients/
│   │   │   │   │       ├── route.ts
│   │   │   │   │       └── [id]/
│   │   │   │   │           └── route.ts
│   │   │   │   │
│   │   │   │   ├── layout.tsx        # Root layout
│   │   │   │   ├── page.tsx          # Landing page
│   │   │   │   ├── error.tsx         # Error boundary
│   │   │   │   ├── loading.tsx       # Loading UI
│   │   │   │   ├── not-found.tsx     # 404 page
│   │   │   │   └── globals.css       # Global styles
│   │   │   │
│   │   │   ├── components/           # React components
│   │   │   │   ├── ui/               # shadcn/ui components
│   │   │   │   │   ├── button.tsx
│   │   │   │   │   ├── input.tsx
│   │   │   │   │   ├── card.tsx
│   │   │   │   │   ├── dialog.tsx
│   │   │   │   │   ├── dropdown-menu.tsx
│   │   │   │   │   ├── form.tsx
│   │   │   │   │   ├── label.tsx
│   │   │   │   │   ├── select.tsx
│   │   │   │   │   ├── table.tsx
│   │   │   │   │   ├── tabs.tsx
│   │   │   │   │   ├── toast.tsx
│   │   │   │   │   └── toaster.tsx
│   │   │   │   │
│   │   │   │   ├── auth/             # Authentication components
│   │   │   │   │   ├── LoginForm.tsx
│   │   │   │   │   ├── RegisterForm.tsx
│   │   │   │   │   ├── ForgotPasswordForm.tsx
│   │   │   │   │   └── AuthGuard.tsx
│   │   │   │   │
│   │   │   │   ├── handoff/          # Handoff components
│   │   │   │   │   ├── HandoffList.tsx
│   │   │   │   │   ├── HandoffCard.tsx
│   │   │   │   │   ├── HandoffDetails.tsx
│   │   │   │   │   ├── HandoffForm.tsx
│   │   │   │   │   ├── HandoffTimeline.tsx
│   │   │   │   │   └── HandoffFilters.tsx
│   │   │   │   │
│   │   │   │   ├── voice/            # Voice recording components
│   │   │   │   │   ├── VoiceRecorder.tsx
│   │   │   │   │   ├── VoicePlayer.tsx
│   │   │   │   │   ├── Waveform.tsx
│   │   │   │   │   └── RecordingControls.tsx
│   │   │   │   │
│   │   │   │   ├── sbar/             # SBAR components
│   │   │   │   │   ├── SBARDisplay.tsx
│   │   │   │   │   ├── SBAREditor.tsx
│   │   │   │   │   ├── SBARSection.tsx
│   │   │   │   │   ├── SBARExport.tsx
│   │   │   │   │   └── SBARValidation.tsx
│   │   │   │   │
│   │   │   │   ├── patient/          # Patient components
│   │   │   │   │   ├── PatientList.tsx
│   │   │   │   │   ├── PatientCard.tsx
│   │   │   │   │   ├── PatientDetails.tsx
│   │   │   │   │   ├── PatientSearch.tsx
│   │   │   │   │   ├── VitalSigns.tsx
│   │   │   │   │   ├── MedicationList.tsx
│   │   │   │   │   └── AllergyList.tsx
│   │   │   │   │
│   │   │   │   ├── layout/           # Layout components
│   │   │   │   │   ├── Header.tsx
│   │   │   │   │   ├── Sidebar.tsx
│   │   │   │   │   ├── Footer.tsx
│   │   │   │   │   ├── Navigation.tsx
│   │   │   │   │   └── UserMenu.tsx
│   │   │   │   │
│   │   │   │   ├── dashboard/        # Dashboard components
│   │   │   │   │   ├── DashboardStats.tsx
│   │   │   │   │   ├── RecentHandoffs.tsx
│   │   │   │   │   ├── UpcomingHandoffs.tsx
│   │   │   │   │   └── ActivityFeed.tsx
│   │   │   │   │
│   │   │   │   └── common/           # Common components
│   │   │   │       ├── LoadingSpinner.tsx
│   │   │   │       ├── ErrorMessage.tsx
│   │   │   │       ├── EmptyState.tsx
│   │   │   │       ├── Avatar.tsx
│   │   │   │       ├── Badge.tsx
│   │   │   │       ├── Skeleton.tsx
│   │   │   │       └── ConfirmDialog.tsx
│   │   │   │
│   │   │   ├── hooks/                # Custom React hooks
│   │   │   │   ├── useAuth.ts
│   │   │   │   ├── useHandoffs.ts
│   │   │   │   ├── usePatients.ts
│   │   │   │   ├── useVoiceRecorder.ts
│   │   │   │   ├── useWebSocket.ts
│   │   │   │   ├── useLocalStorage.ts
│   │   │   │   ├── useDebounce.ts
│   │   │   │   └── useMediaQuery.ts
│   │   │   │
│   │   │   ├── lib/                  # Utility libraries
│   │   │   │   ├── api.ts            # API client
│   │   │   │   ├── supabase.ts       # Supabase client
│   │   │   │   ├── utils.ts          # Utility functions
│   │   │   │   ├── constants.ts      # App constants
│   │   │   │   ├── validations.ts    # Form validations
│   │   │   │   └── audio.ts          # Audio processing
│   │   │   │
│   │   │   ├── stores/               # Zustand stores
│   │   │   │   ├── authStore.ts
│   │   │   │   ├── handoffStore.ts
│   │   │   │   ├── patientStore.ts
│   │   │   │   └── uiStore.ts
│   │   │   │
│   │   │   ├── types/                # TypeScript types
│   │   │   │   ├── index.ts
│   │   │   │   ├── auth.ts
│   │   │   │   ├── handoff.ts
│   │   │   │   ├── patient.ts
│   │   │   │   ├── sbar.ts
│   │   │   │   ├── staff.ts
│   │   │   │   ├── facility.ts
│   │   │   │   └── api.ts
│   │   │   │
│   │   │   └── styles/               # Additional styles
│   │   │       └── tailwind.css
│   │   │
│   │   ├── .env.local.example        # Environment variables template
│   │   ├── .eslintrc.json            # ESLint config
│   │   ├── .prettierrc               # Prettier config
│   │   ├── next.config.js            # Next.js config
│   │   ├── postcss.config.js         # PostCSS config
│   │   ├── tailwind.config.ts        # Tailwind config
│   │   ├── tsconfig.json             # TypeScript config
│   │   ├── package.json
│   │   └── README.md
│   │
│   └── backend/                      # Express.js API (optional standalone)
│       ├── src/
│       │   ├── config/               # Configuration
│       │   │   ├── database.ts
│       │   │   ├── redis.ts
│       │   │   ├── azure.ts
│       │   │   └── r2.ts
│       │   │
│       │   ├── controllers/          # Route controllers
│       │   │   ├── auth.controller.ts
│       │   │   ├── handoff.controller.ts
│       │   │   ├── patient.controller.ts
│       │   │   ├── voice.controller.ts
│       │   │   ├── ai.controller.ts
│       │   │   └── ehr.controller.ts
│       │   │
│       │   ├── services/             # Business logic
│       │   │   ├── auth.service.ts
│       │   │   ├── handoff.service.ts
│       │   │   ├── patient.service.ts
│       │   │   ├── voice.service.ts
│       │   │   ├── transcription.service.ts
│       │   │   ├── sbar.service.ts
│       │   │   ├── ehr.service.ts
│       │   │   ├── notification.service.ts
│       │   │   └── storage.service.ts
│       │   │
│       │   ├── models/               # Database models (if using ORM)
│       │   │   ├── facility.model.ts
│       │   │   ├── staff.model.ts
│       │   │   ├── patient.model.ts
│       │   │   ├── handoff.model.ts
│       │   │   └── index.ts
│       │   │
│       │   ├── middleware/           # Express middleware
│       │   │   ├── auth.middleware.ts
│       │   │   ├── error.middleware.ts
│       │   │   ├── validation.middleware.ts
│       │   │   ├── rateLimit.middleware.ts
│       │   │   ├── logging.middleware.ts
│       │   │   └── cors.middleware.ts
│       │   │
│       │   ├── routes/               # API routes
│       │   │   ├── auth.routes.ts
│       │   │   ├── handoff.routes.ts
│       │   │   ├── patient.routes.ts
│       │   │   ├── voice.routes.ts
│       │   │   ├── ai.routes.ts
│       │   │   ├── ehr.routes.ts
│       │   │   └── index.ts
│       │   │
│       │   ├── utils/                # Utility functions
│       │   │   ├── logger.ts
│       │   │   ├── validator.ts
│       │   │   ├── crypto.ts
│       │   │   ├── date.ts
│       │   │   └── response.ts
│       │   │
│       │   ├── types/                # TypeScript types
│       │   │   ├── index.d.ts
│       │   │   ├── express.d.ts
│       │   │   └── custom.d.ts
│       │   │
│       │   ├── workers/              # Background workers
│       │   │   ├── transcription.worker.ts
│       │   │   ├── sbar.worker.ts
│       │   │   ├── notification.worker.ts
│       │   │   └── ehr-sync.worker.ts
│       │   │
│       │   ├── app.ts                # Express app setup
│       │   └── server.ts             # Server entry point
│       │
│       ├── tests/                    # Backend tests
│       │   ├── unit/
│       │   ├── integration/
│       │   └── e2e/
│       │
│       ├── .env.example              # Environment variables template
│       ├── .eslintrc.json
│       ├── .prettierrc
│       ├── tsconfig.json
│       ├── package.json
│       └── README.md
│
├── packages/                         # Shared packages
│   ├── types/                        # Shared TypeScript types
│   │   ├── src/
│   │   │   ├── index.ts
│   │   │   ├── database.ts
│   │   │   ├── api.ts
│   │   │   └── common.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   ├── config/                       # Shared configuration
│   │   ├── src/
│   │   │   ├── index.ts
│   │   │   └── constants.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── utils/                        # Shared utilities
│       ├── src/
│       │   ├── index.ts
│       │   ├── validation.ts
│       │   └── formatting.ts
│       ├── package.json
│       └── tsconfig.json
│
├── database/                         # Database files
│   ├── migrations/                   # SQL migrations
│   │   ├── 001_initial_schema.sql
│   │   ├── 002_add_voice_recordings.sql
│   │   ├── 003_add_sbar_reports.sql
│   │   └── README.md
│   │
│   ├── seeds/                        # Seed data
│   │   ├── facilities.sql
│   │   ├── staff.sql
│   │   └── README.md
│   │
│   ├── functions/                    # Database functions
│   │   ├── audit_logging.sql
│   │   └── row_level_security.sql
│   │
│   └── schema.sql                    # Complete schema file
│
├── docs/                             # Documentation
│   ├── api/                          # API documentation
│   │   ├── authentication.md
│   │   ├── handoffs.md
│   │   ├── patients.md
│   │   ├── voice.md
│   │   └── ehr.md
│   │
│   ├── architecture/                 # Architecture docs
│   │   ├── system-overview.md
│   │   ├── data-flow.md
│   │   ├── security.md
│   │   └── deployment.md
│   │
│   ├── guides/                       # User guides
│   │   ├── getting-started.md
│   │   ├── development.md
│   │   ├── testing.md
│   │   └── deployment.md
│   │
│   └── README.md
│
├── scripts/                          # Automation scripts
│   ├── setup.sh                      # Initial setup
│   ├── migrate.sh                    # Run migrations
│   ├── seed.sh                       # Seed database
│   ├── deploy-frontend.sh            # Deploy frontend
│   ├── deploy-backend.sh             # Deploy backend
│   └── backup.sh                     # Backup database
│
├── .gitignore                        # Git ignore file
├── .gitlab-ci.yml                    # GitLab CI/CD
├── .prettierignore                   # Prettier ignore
├── README.md                         # Main README
├── LICENSE                           # License file
├── CONTRIBUTING.md                   # Contribution guidelines
├── CHANGELOG.md                      # Changelog
└── package.json                      # Root package.json (workspace)
```

---

## 3. GitHub Setup Guide

### 3.1 Create GitHub Repository

**Step 1: Create Repository on GitHub**
1. Go to https://github.com/new
2. Repository name: `eclipselink-ai`
3. Description: "EclipseLink AI™ - Voice-enabled clinical handoff platform with AI-powered SBAR generation"
4. Visibility: Private
5. Initialize with README: No (we'll create our own)
6. Add .gitignore: No (we'll create our own)
7. Choose license: MIT or Proprietary
8. Click "Create repository"

**Step 2: Clone Repository Locally**
```bash
# Clone the empty repository
git clone https://github.com/YOUR_USERNAME/eclipselink-ai.git
cd eclipselink-ai
```

### 3.2 Initial GitHub Setup Commands

```bash
# Initialize the repository structure
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p apps/frontend
mkdir -p apps/backend
mkdir -p packages/{types,config,utils}
mkdir -p database/{migrations,seeds,functions}
mkdir -p docs/{api,architecture,guides}
mkdir -p scripts

# Create initial README
cat > README.md << 'EOF'
# EclipseLink AI™

Voice-enabled clinical handoff platform with AI-powered SBAR generation.

## 🦚 About Rohimaya Health AI

EclipseLink AI™ is developed by Rohimaya Health AI, founded by Hannah Kraulik Pagade (CEO) and Prasad Pagade (CTO).

## 🚀 Quick Start

See [docs/guides/getting-started.md](docs/guides/getting-started.md) for setup instructions.

## 📁 Repository Structure

- `apps/frontend` - Next.js PWA
- `apps/backend` - Express.js API
- `packages/` - Shared packages
- `database/` - Database migrations and schema
- `docs/` - Documentation
- `scripts/` - Automation scripts

## 🛠️ Development

```bash
# Install dependencies
npm install

# Run frontend dev server
npm run dev:frontend

# Run backend dev server
npm run dev:backend

# Run tests
npm test
```

## 📝 License

Proprietary - © 2025 Rohimaya Health AI. All rights reserved.
EOF

# Create root package.json for workspace
cat > package.json << 'EOF'
{
  "name": "eclipselink-ai",
  "version": "1.0.0",
  "private": true,
  "description": "EclipseLink AI - Voice-enabled clinical handoff platform",
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev:frontend": "npm run dev --workspace=apps/frontend",
    "dev:backend": "npm run dev --workspace=apps/backend",
    "build:frontend": "npm run build --workspace=apps/frontend",
    "build:backend": "npm run build --workspace=apps/backend",
    "test": "npm run test --workspaces --if-present",
    "lint": "npm run lint --workspaces --if-present",
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,md}\"",
    "migrate": "bash scripts/migrate.sh",
    "seed": "bash scripts/seed.sh"
  },
  "devDependencies": {
    "prettier": "^3.0.0",
    "typescript": "^5.2.0"
  }
}
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/
.nyc_output/

# Next.js
.next/
out/
build/
dist/

# Production
*.log
logs/
*.pid
*.seed
*.pid.lock

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
.env*.local

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Temporary files
tmp/
temp/
*.tmp

# Build artifacts
*.tsbuildinfo

# Supabase
.supabase/

# Railway
.railway/

# Claude Code
.claude/
EOF

# Initial commit
git add .
git commit -m "Initial repository setup"
git push -u origin main

# Create develop branch
git checkout -b develop
git push -u origin develop
```

### 3.3 GitHub Actions Workflows

**File: `.github/workflows/test.yml`**
```yaml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test-frontend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./apps/frontend
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run type check
        run: npm run type-check
      
      - name: Run tests
        run: npm test

  test-backend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./apps/backend
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run type check
        run: npm run type-check
      
      - name: Run tests
        run: npm test
```

**File: `.github/workflows/deploy-frontend.yml`**
```yaml
name: Deploy Frontend

on:
  push:
    branches: [main]
    paths:
      - 'apps/frontend/**'
      - '.github/workflows/deploy-frontend.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./apps/frontend
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
        env:
          NEXT_PUBLIC_API_URL: ${{ secrets.API_URL }}
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
      
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: eclipselink-ai
          directory: .next
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

**File: `.github/workflows/deploy-backend.yml`**
```yaml
name: Deploy Backend

on:
  push:
    branches: [main]
    paths:
      - 'apps/backend/**'
      - 'packages/**'
      - '.github/workflows/deploy-backend.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: eclipselink-api
```

**File: `.github/workflows/security-scan.yml`**
```yaml
name: Security Scan

on:
  schedule:
    - cron: '0 0 * * 0' # Weekly on Sunday
  push:
    branches: [main]

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run npm audit
        run: npm audit --audit-level=moderate
      
      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### 3.4 GitHub Issue Templates

**File: `.github/ISSUE_TEMPLATE/bug_report.md`**
```markdown
---
name: Bug Report
about: Report a bug to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Screenshots
If applicable, add screenshots.

## Environment
- Device: [e.g., iPhone 12, Desktop]
- OS: [e.g., iOS 15, Windows 11]
- Browser: [e.g., Chrome 98, Safari 15]
- Version: [e.g., 1.0.0]

## Additional Context
Any other relevant information.
```

**File: `.github/ISSUE_TEMPLATE/feature_request.md`**
```markdown
---
name: Feature Request
about: Suggest a new feature
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## Feature Description
A clear and concise description of the feature.

## Problem It Solves
What problem does this feature solve?

## Proposed Solution
How should this feature work?

## Alternatives Considered
What other solutions have you considered?

## Additional Context
Any other relevant information, mockups, or examples.
```

### 3.5 GitHub Pull Request Template

**File: `.github/PULL_REQUEST_TEMPLATE.md`**
```markdown
## Description
Describe the changes in this PR.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Fixes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots here.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests passing
```

---

## 4. GitLab Setup Guide

### 4.1 Create GitLab Repository

**Step 1: Create Repository on GitLab**
1. Go to https://gitlab.com/projects/new
2. Project name: `eclipselink-ai`
3. Project description: "EclipseLink AI™ - Voice-enabled clinical handoff platform with AI-powered SBAR generation"
4. Visibility: Private
5. Initialize with README: No
6. Click "Create project"

**Step 2: Clone Repository Locally**
```bash
# Clone the empty repository
git clone https://gitlab.com/YOUR_USERNAME/eclipselink-ai.git
cd eclipselink-ai
```

### 4.2 Initial GitLab Setup Commands

```bash
# Use the same setup commands as GitHub (from section 3.2)
# Just replace the remote URL

# If you already set up GitHub, add GitLab as a second remote
git remote add gitlab https://gitlab.com/YOUR_USERNAME/eclipselink-ai.git

# Push to both remotes
git push origin main
git push gitlab main

git checkout -b develop
git push origin develop
git push gitlab develop
```

### 4.3 GitLab CI/CD Pipeline

**File: `.gitlab-ci.yml`**
```yaml
stages:
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "18"
  DOCKER_DRIVER: overlay2

# Cache configuration
.node_cache: &node_cache
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - node_modules/
      - .npm/

# Test Frontend
test:frontend:
  stage: test
  image: node:${NODE_VERSION}
  <<: *node_cache
  script:
    - cd apps/frontend
    - npm ci
    - npm run lint
    - npm run type-check
    - npm test
  only:
    - main
    - develop
    - merge_requests

# Test Backend
test:backend:
  stage: test
  image: node:${NODE_VERSION}
  <<: *node_cache
  script:
    - cd apps/backend
    - npm ci
    - npm run lint
    - npm run type-check
    - npm test
  only:
    - main
    - develop
    - merge_requests

# Build Frontend
build:frontend:
  stage: build
  image: node:${NODE_VERSION}
  <<: *node_cache
  script:
    - cd apps/frontend
    - npm ci
    - npm run build
  artifacts:
    paths:
      - apps/frontend/.next/
    expire_in: 1 hour
  only:
    - main

# Build Backend
build:backend:
  stage: build
  image: node:${NODE_VERSION}
  <<: *node_cache
  script:
    - cd apps/backend
    - npm ci
    - npm run build
  artifacts:
    paths:
      - apps/backend/dist/
    expire_in: 1 hour
  only:
    - main

# Deploy Frontend to Cloudflare Pages
deploy:frontend:
  stage: deploy
  image: node:${NODE_VERSION}
  dependencies:
    - build:frontend
  script:
    - npm install -g wrangler
    - cd apps/frontend
    - npx wrangler pages publish .next --project-name=eclipselink-ai
  environment:
    name: production
    url: https://app.eclipselink.ai
  only:
    - main

# Deploy Backend to Railway
deploy:backend:
  stage: deploy
  image: curlimages/curl:latest
  dependencies:
    - build:backend
  script:
    - curl -X POST $RAILWAY_WEBHOOK_URL
  environment:
    name: production
  only:
    - main

# Security Scanning
security:scan:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm audit --audit-level=moderate
  allow_failure: true
  only:
    - main
    - develop
    - merge_requests

# Database Migrations (manual job)
migrate:database:
  stage: deploy
  image: postgres:15
  script:
    - psql $DATABASE_URL -f database/schema.sql
  when: manual
  only:
    - main
```

### 4.4 GitLab Merge Request Template

**File: `.gitlab/merge_request_templates/default.md`**
```markdown
## Description
Describe the changes in this MR.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Closes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots here.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Pipeline passes
```

### 4.5 GitLab Issue Templates

**File: `.gitlab/issue_templates/bug.md`**
```markdown
## Bug Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- Device: [e.g., iPhone 12, Desktop]
- OS: [e.g., iOS 15, Windows 11]
- Browser: [e.g., Chrome 98, Safari 15]
- Version: [e.g., 1.0.0]

## Screenshots
If applicable, add screenshots.

/label ~bug
```

**File: `.gitlab/issue_templates/feature.md`**
```markdown
## Feature Description
A clear and concise description of the feature.

## Problem It Solves
What problem does this feature solve?

## Proposed Solution
How should this feature work?

## Alternatives Considered
What other solutions have you considered?

## Additional Context
Any other relevant information, mockups, or examples.

/label ~enhancement
```

---

## 5. Configuration Files

### 5.1 Frontend Configuration Files

**File: `apps/frontend/package.json`**
```json
{
  "name": "@eclipselink/frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,md}\""
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@supabase/supabase-js": "^2.38.0",
    "@tanstack/react-query": "^5.0.0",
    "zustand": "^4.4.0",
    "axios": "^1.6.0",
    "date-fns": "^2.30.0",
    "zod": "^3.22.0",
    "react-hook-form": "^7.48.0",
    "@hookform/resolvers": "^3.3.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "class-variance-authority": "^0.7.0",
    "lucide-react": "^0.292.0",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-toast": "^1.1.5",
    "sonner": "^1.2.0",
    "next-pwa": "^5.6.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.2.0",
    "eslint": "^8.54.0",
    "eslint-config-next": "^14.0.0",
    "prettier": "^3.1.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "@testing-library/react": "^14.1.0",
    "@testing-library/jest-dom": "^6.1.0",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0"
  }
}
```

**File: `apps/frontend/next.config.js`**
```javascript
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development'
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['eclipselink-production.r2.cloudflarestorage.com'],
    formats: ['image/avif', 'image/webp']
  },
  experimental: {
    serverActions: true
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
  }
};

module.exports = withPWA(nextConfig);
```

**File: `apps/frontend/tailwind.config.ts`**
```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: ['class'],
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}'
  ],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px'
      }
    },
    extend: {
      colors: {
        // Rohimaya brand colors
        'peacock-teal': '#1a9b8e',
        'phoenix-gold': '#f4c430',
        'lunar-blue': '#2c3e50',
        'moon-white': '#f8f9fa',
        'eclipse-navy': '#1a2332',
        'accent-copper': '#b87333',
        
        // shadcn/ui colors
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))'
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))'
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))'
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))'
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))'
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))'
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))'
        }
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)'
      },
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' }
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' }
        }
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out'
      }
    }
  },
  plugins: [require('tailwindcss-animate')]
};

export default config;
```

**File: `apps/frontend/tsconfig.json`**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/types/*": ["./src/types/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/stores/*": ["./src/stores/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**File: `apps/frontend/.eslintrc.json`**
```json
{
  "extends": ["next/core-web-vitals", "prettier"],
  "rules": {
    "no-console": ["warn", { "allow": ["warn", "error"] }],
    "prefer-const": "error",
    "@typescript-eslint/no-unused-vars": [
      "error",
      {
        "argsIgnorePattern": "^_",
        "varsIgnorePattern": "^_"
      }
    ]
  }
}
```

**File: `apps/frontend/.prettierrc`**
```json
{
  "semi": true,
  "trailingComma": "none",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

**File: `apps/frontend/.env.local.example`**
```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:4000
# NEXT_PUBLIC_API_URL=https://api.eclipselink.ai

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# PostHog Analytics (optional)
NEXT_PUBLIC_POSTHOG_KEY=your-posthog-key
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com

# Sentry (optional)
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn
SENTRY_AUTH_TOKEN=your-sentry-auth-token
```

### 5.2 Backend Configuration Files

**File: `apps/backend/package.json`**
```json
{
  "name": "@eclipselink/backend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js",
    "lint": "eslint src --ext .ts",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "migrate": "node -r dotenv/config scripts/migrate.js",
    "worker": "tsx src/workers/index.ts"
  },
  "dependencies": {
    "express": "^4.18.0",
    "cors": "^2.8.5",
    "helmet": "^7.1.0",
    "compression": "^1.7.4",
    "dotenv": "^16.3.0",
    "@supabase/supabase-js": "^2.38.0",
    "ioredis": "^5.3.0",
    "bullmq": "^5.0.0",
    "axios": "^1.6.0",
    "@aws-sdk/client-s3": "^3.450.0",
    "@aws-sdk/s3-request-presigner": "^3.450.0",
    "form-data": "^4.0.0",
    "multer": "^1.4.5-lts.1",
    "zod": "^3.22.0",
    "jsonwebtoken": "^9.0.2",
    "bcryptjs": "^2.4.3",
    "winston": "^3.11.0",
    "@logtail/node": "^0.4.0",
    "@sentry/node": "^7.85.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.0",
    "@types/cors": "^2.8.0",
    "@types/compression": "^1.7.0",
    "@types/multer": "^1.4.0",
    "@types/jsonwebtoken": "^9.0.0",
    "@types/bcryptjs": "^2.4.0",
    "@types/node": "^20.0.0",
    "typescript": "^5.2.0",
    "tsx": "^4.6.0",
    "eslint": "^8.54.0",
    "@typescript-eslint/parser": "^6.13.0",
    "@typescript-eslint/eslint-plugin": "^6.13.0",
    "prettier": "^3.1.0",
    "jest": "^29.7.0",
    "@types/jest": "^29.5.0",
    "ts-jest": "^29.1.0",
    "supertest": "^6.3.0",
    "@types/supertest": "^6.0.0"
  }
}
```

**File: `apps/backend/tsconfig.json`**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./src/*"],
      "@/config/*": ["./src/config/*"],
      "@/controllers/*": ["./src/controllers/*"],
      "@/services/*": ["./src/services/*"],
      "@/middleware/*": ["./src/middleware/*"],
      "@/utils/*": ["./src/utils/*"],
      "@/types/*": ["./src/types/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

**File: `apps/backend/.env.example`**
```env
# Server Configuration
NODE_ENV=development
PORT=4000
API_URL=http://localhost:4000

# Database (Supabase)
DATABASE_URL=postgresql://user:password@host:5432/database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key
SUPABASE_ANON_KEY=your-anon-key

# Redis (Upstash)
REDIS_URL=redis://username:password@host:6379

# Azure OpenAI
AZURE_OPENAI_KEY=your-azure-openai-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-02-15-preview
WHISPER_DEPLOYMENT_NAME=whisper
GPT4_DEPLOYMENT_NAME=gpt-4

# Cloudflare R2
R2_ACCOUNT_ID=your-account-id
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
R2_BUCKET_NAME=eclipselink-production
R2_PUBLIC_URL=https://your-bucket.r2.cloudflarestorage.com

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=1h
JWT_REFRESH_EXPIRES_IN=30d

# Encryption
ENCRYPTION_KEY=your-32-character-encryption-key

# Rate Limiting
RATE_LIMIT_WINDOW_MS=60000
RATE_LIMIT_MAX_REQUESTS=100

# Logging
LOG_LEVEL=info
LOGTAIL_TOKEN=your-logtail-token

# Monitoring
SENTRY_DSN=your-sentry-dsn

# EHR Integration (Epic)
EPIC_CLIENT_ID=your-epic-client-id
EPIC_CLIENT_SECRET=your-epic-client-secret
EPIC_FHIR_BASE_URL=https://fhir.epic.com/interconnect-fhir-oauth

# Email (optional - for notifications)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
SMTP_FROM=noreply@eclipselink.ai
```

---

## 6. Environment Variables

### 6.1 Environment Variable Management

**Best Practices:**
1. **Never commit `.env` files** to version control
2. Use `.env.example` as a template
3. Store production secrets in CI/CD platform (GitHub Secrets, GitLab CI/CD Variables)
4. Use different values for dev, staging, and production
5. Rotate secrets regularly

### 6.2 GitHub Secrets Setup

Navigate to: `Settings > Secrets and variables > Actions`

**Required Secrets:**
```
# Cloudflare
CLOUDFLARE_API_TOKEN
CLOUDFLARE_ACCOUNT_ID

# Railway
RAILWAY_TOKEN

# Supabase
SUPABASE_URL
SUPABASE_ANON_KEY
SUPABASE_SERVICE_KEY
DATABASE_URL

# Azure OpenAI
AZURE_OPENAI_KEY
AZURE_OPENAI_ENDPOINT

# Cloudflare R2
R2_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY

# Other
JWT_SECRET
ENCRYPTION_KEY
SENTRY_DSN
LOGTAIL_TOKEN
```

### 6.3 GitLab CI/CD Variables

Navigate to: `Settings > CI/CD > Variables`

Add the same secrets as GitHub, with protection enabled for production variables.

---

## 7. Package Dependencies

### 7.1 Frontend Dependencies Summary

**Core Framework:**
- Next.js 14 (React framework)
- React 18 (UI library)

**UI Components:**
- Tailwind CSS (styling)
- shadcn/ui (component library)
- Radix UI (accessible primitives)
- Lucide React (icons)

**State Management:**
- Zustand (global state)
- React Query (server state)

**Forms & Validation:**
- React Hook Form (forms)
- Zod (validation)

**Data Fetching:**
- Axios (HTTP client)
- Supabase JS (database client)

**PWA:**
- next-pwa (service worker)

### 7.2 Backend Dependencies Summary

**Core Framework:**
- Express.js (HTTP server)
- TypeScript (type safety)

**Database:**
- Supabase JS (PostgreSQL client)

**Cache & Queue:**
- ioredis (Redis client)
- BullMQ (job queue)

**Storage:**
- AWS SDK S3 (R2 client)

**AI Services:**
- Axios (HTTP client for Azure OpenAI)

**Security:**
- Helmet (security headers)
- CORS (cross-origin)
- jsonwebtoken (JWT)
- bcryptjs (password hashing)

**Logging:**
- Winston (logger)
- Logtail (log management)
- Sentry (error tracking)

---

## 8. Git Workflow

### 8.1 Branching Strategy (Git Flow)

```
main                    (production)
  │
  ├─ develop            (staging)
  │   │
  │   ├─ feature/voice-recorder
  │   ├─ feature/sbar-display
  │   ├─ feature/ehr-integration
  │   │
  │   ├─ bugfix/audio-quality
  │   └─ bugfix/session-timeout
  │
  └─ hotfix/security-patch
```

### 8.2 Commit Message Convention

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, missing semi colons, etc.
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```bash
git commit -m "feat(voice): add waveform visualization"
git commit -m "fix(auth): resolve token refresh issue"
git commit -m "docs(api): update handoff endpoints"
git commit -m "refactor(sbar): improve generation logic"
```

### 8.3 Common Git Commands

```bash
# Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/voice-recorder

# Make changes, commit
git add .
git commit -m "feat(voice): implement voice recorder component"

# Push to remote
git push origin feature/voice-recorder

# Create pull request on GitHub/GitLab
# After approval, merge to develop

# Update main from develop (for release)
git checkout main
git pull origin main
git merge develop
git push origin main
```

---

## 9. Claude Code Integration

### 9.1 What is Claude Code?

Claude Code is a command-line tool that allows developers to delegate coding tasks directly to Claude AI from the terminal. It's perfect for:
- Generating boilerplate code
- Creating components
- Writing tests
- Refactoring code
- Implementing features

### 9.2 Setting Up Claude Code with GitHub

**Step 1: Install Claude Code**
```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Or use npx (no installation)
npx @anthropic-ai/claude-code
```

**Step 2: Configure Claude Code**
```bash
# Initialize Claude Code in your project
cd eclipselink-ai
claude-code init

# This creates a .claude/ directory with configuration
```

**Step 3: Create `.claude/config.json`**
```json
{
  "projectName": "EclipseLink AI",
  "description": "Voice-enabled clinical handoff platform with AI-powered SBAR generation",
  "techStack": {
    "frontend": "Next.js 14, TypeScript, Tailwind CSS, shadcn/ui",
    "backend": "Express.js, TypeScript, Supabase, Redis",
    "ai": "Azure OpenAI (Whisper, GPT-4)",
    "database": "PostgreSQL (Supabase)",
    "storage": "Cloudflare R2",
    "cache": "Upstash Redis"
  },
  "conventions": {
    "commits": "Conventional Commits",
    "branching": "Git Flow",
    "typescript": "strict mode",
    "linting": "ESLint + Prettier"
  },
  "directories": {
    "frontend": "apps/frontend",
    "backend": "apps/backend",
    "shared": "packages",
    "database": "database",
    "docs": "docs"
  }
}
```

**Step 4: Create `.claude/context.md`** (Project Context for Claude)
```markdown
# EclipseLink AI - Project Context for Claude Code

## Product Overview
EclipseLink AI is a voice-enabled clinical handoff platform that transforms spoken patient reports into structured SBAR (Situation, Background, Assessment, Recommendation) documentation using advanced AI.

## Tech Stack
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, shadcn/ui, Zustand, React Query
- **Backend**: Express.js, TypeScript, Supabase, Redis (Upstash), BullMQ
- **AI**: Azure OpenAI (Whisper for speech-to-text, GPT-4 for SBAR generation)
- **Database**: PostgreSQL via Supabase
- **Storage**: Cloudflare R2 for voice recordings and documents
- **Deployment**: Cloudflare Pages (frontend), Railway (backend)

## Code Conventions
- Use TypeScript strict mode
- Follow ESLint + Prettier rules
- Use functional components with hooks (no class components)
- Use Tailwind CSS for styling (no CSS modules)
- Use shadcn/ui components when available
- Follow Conventional Commits format
- Write comprehensive JSDoc comments for functions

## File Organization
- Components go in `apps/frontend/src/components/`
- API routes in `apps/frontend/src/app/api/`
- Backend controllers in `apps/backend/src/controllers/`
- Backend services in `apps/backend/src/services/`
- Shared types in `packages/types/src/`

## Naming Conventions
- Components: PascalCase (VoiceRecorder.tsx)
- Files: camelCase for utilities, PascalCase for components
- Functions: camelCase (createHandoff, generateSBAR)
- Constants: UPPER_SNAKE_CASE (API_BASE_URL)
- Types/Interfaces: PascalCase (User, HandoffData)

## Testing
- Use Jest for unit tests
- Use React Testing Library for component tests
- Test files should be named `*.test.ts` or `*.test.tsx`
- Aim for >80% code coverage

## Documentation
- All public functions should have JSDoc comments
- Complex logic should have inline comments
- Update README.md when adding new features
- Keep API documentation up to date in `docs/api/`

## Brand Colors (Rohimaya Health AI)
```typescript
const colors = {
  peacockTeal: '#1a9b8e',
  phoenixGold: '#f4c430',
  lunarBlue: '#2c3e50',
  moonWhite: '#f8f9fa',
  eclipseNavy: '#1a2332',
  accentCopper: '#b87333'
};
```
```

### 9.3 Using Claude Code for Development

**Example 1: Generate a Component**
```bash
claude-code "Create a VoiceRecorder component in apps/frontend/src/components/voice/ with the following features:
- Record audio using MediaRecorder API
- Display waveform visualization
- Show duration counter
- Pause/resume functionality
- Upload to backend API
- TypeScript with proper types
- Use Tailwind CSS for styling
- Use shadcn/ui Button component"
```

**Example 2: Create API Route**
```bash
claude-code "Create a POST /api/voice/upload route in apps/frontend/src/app/api/voice/upload/route.ts that:
- Accepts multipart/form-data with audio file
- Validates file size (max 10MB) and format (webm/mp3)
- Uploads to Cloudflare R2
- Creates database record
- Queues transcription job
- Returns recordingId and status
- Includes error handling"
```

**Example 3: Implement Backend Service**
```bash
claude-code "Implement transcription.service.ts in apps/backend/src/services/ that:
- Fetches audio from R2
- Calls Azure OpenAI Whisper API
- Handles rate limiting with exponential backoff
- Stores transcription in database
- Updates job status in Redis
- Includes comprehensive error handling and logging"
```

**Example 4: Generate Tests**
```bash
claude-code "Create comprehensive Jest tests for the VoiceRecorder component including:
- Rendering tests
- Recording start/stop functionality
- Waveform visualization
- Error handling
- API integration mocks"
```

**Example 5: Refactor Code**
```bash
claude-code "Refactor apps/backend/src/services/sbar.service.ts to:
- Extract prompt engineering to separate module
- Add retry logic with exponential backoff
- Improve error messages
- Add comprehensive logging
- Optimize token usage"
```

### 9.4 Claude Code Best Practices

**1. Be Specific**
- Provide clear requirements
- Specify file paths
- Mention exact technologies
- Include constraints

**2. Reference Project Context**
- Claude Code reads `.claude/context.md`
- Mention conventions when needed
- Reference existing patterns

**3. Iterate**
```bash
# First pass
claude-code "Create a basic handoff list component"

# Refinement
claude-code "Add filtering, sorting, and pagination to HandoffList component"

# Enhancement
claude-code "Add real-time updates via WebSocket to HandoffList"
```

**4. Use for Repetitive Tasks**
- Generating CRUD endpoints
- Creating similar components
- Writing boilerplate
- Adding tests
- Documentation

**5. Review and Test**
- Always review generated code
- Run tests
- Check for security issues
- Verify against requirements

### 9.5 Claude Code Configuration File

**File: `.claude/tasks.json`** (Pre-defined tasks)
```json
{
  "tasks": [
    {
      "name": "create-component",
      "description": "Create a new React component with TypeScript",
      "template": "Create a {{componentName}} component in {{path}} with TypeScript, Tailwind CSS, and shadcn/ui components. Include proper types and JSDoc comments."
    },
    {
      "name": "create-api-route",
      "description": "Create a new Next.js API route",
      "template": "Create a {{method}} {{endpoint}} route in {{path}} with TypeScript, input validation using Zod, error handling, and proper types."
    },
    {
      "name": "create-service",
      "description": "Create a new backend service",
      "template": "Create {{serviceName}} service in apps/backend/src/services/ with TypeScript, comprehensive error handling, logging, and unit tests."
    },
    {
      "name": "add-tests",
      "description": "Add tests for existing code",
      "template": "Create comprehensive Jest tests for {{filePath}} including unit tests, integration tests, and edge cases."
    },
    {
      "name": "refactor",
      "description": "Refactor existing code",
      "template": "Refactor {{filePath}} to improve code quality, add types, optimize performance, and add comments."
    }
  ]
}
```

**Usage:**
```bash
# Run a pre-defined task
claude-code task create-component --componentName="PatientSearch" --path="apps/frontend/src/components/patient/"

# List all available tasks
claude-code task list
```

### 9.6 GitHub Integration with Claude Code

**Automated PR Review:**
```bash
# In GitHub Actions workflow
- name: Claude Code Review
  run: |
    npx @anthropic-ai/claude-code review \
      --pr=${{ github.event.pull_request.number }} \
      --check-types \
      --check-tests \
      --check-security
```

**Commit Message Generation:**
```bash
# Generate commit message from staged changes
git add .
claude-code generate-commit-message
git commit -F .claude/commit-message.txt
```

---

## 10. Initial Setup Commands

### 10.1 Complete Setup Script

**File: `scripts/setup.sh`**
```bash
#!/bin/bash

# EclipseLink AI - Complete Setup Script
# This script sets up the entire development environment

set -e  # Exit on error

echo "🦚 EclipseLink AI - Initial Setup"
echo "=================================="

# Check prerequisites
echo "📋 Checking prerequisites..."

command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Please install Node.js 18+"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git is required but not installed."; exit 1; }

echo "✅ Prerequisites met"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd apps/frontend
npm install
cd ../..

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd apps/backend
npm install
cd ../..

# Create environment files
echo ""
echo "⚙️  Setting up environment files..."

if [ ! -f apps/frontend/.env.local ]; then
    cp apps/frontend/.env.local.example apps/frontend/.env.local
    echo "✅ Created apps/frontend/.env.local (please update with your values)"
else
    echo "⏭️  apps/frontend/.env.local already exists"
fi

if [ ! -f apps/backend/.env ]; then
    cp apps/backend/.env.example apps/backend/.env
    echo "✅ Created apps/backend/.env (please update with your values)"
else
    echo "⏭️  apps/backend/.env already exists"
fi

# Initialize Supabase (if installed)
if command -v supabase >/dev/null 2>&1; then
    echo ""
    echo "🗄️  Initializing Supabase..."
    supabase init
    echo "✅ Supabase initialized"
else
    echo "⏭️  Supabase CLI not installed (optional for local development)"
fi

# Build packages
echo ""
echo "🔨 Building shared packages..."
npm run build --workspace=packages/types
npm run build --workspace=packages/config
npm run build --workspace=packages/utils
echo "✅ Packages built"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Update environment variables in:"
echo "   - apps/frontend/.env.local"
echo "   - apps/backend/.env"
echo "2. Run 'npm run dev:frontend' to start the frontend"
echo "3. Run 'npm run dev:backend' to start the backend"
echo "4. Visit http://localhost:3000"
echo ""
echo "🦚 Happy coding with EclipseLink AI!"
```

Make script executable:
```bash
chmod +x scripts/setup.sh
```

### 10.2 Step-by-Step Manual Setup

**For Hannah to run after cloning:**

```bash
# 1. Clone the repository (GitHub)
git clone https://github.com/YOUR_USERNAME/eclipselink-ai.git
cd eclipselink-ai

# OR clone from GitLab
git clone https://gitlab.com/YOUR_USERNAME/eclipselink-ai.git
cd eclipselink-ai

# 2. Run the setup script
bash scripts/setup.sh

# 3. Update environment variables
# Edit these files with your actual values:
# - apps/frontend/.env.local
# - apps/backend/.env

# 4. Start development servers
# In terminal 1:
npm run dev:frontend

# In terminal 2:
npm run dev:backend

# 5. Open browser
# Navigate to http://localhost:3000
```

### 10.3 Database Setup Commands

```bash
# Connect to Supabase (or local PostgreSQL)
psql $DATABASE_URL

# Run migrations
npm run migrate

# Seed initial data (optional)
npm run seed
```

### 10.4 Claude Code Quick Start

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Initialize in project
cd eclipselink-ai
claude-code init

# Start building with Claude Code
claude-code "Help me implement the VoiceRecorder component"
```

---

## Summary & Next Steps

### ✅ What We've Created

**Part 2 provides:**
1. ✅ Complete folder structure for monorepo
2. ✅ GitHub setup guide with Actions workflows
3. ✅ GitLab setup guide with CI/CD pipeline
4. ✅ All configuration files (package.json, tsconfig, etc.)
5. ✅ Environment variable templates
6. ✅ Git workflow and conventions
7. ✅ Claude Code integration guide
8. ✅ Automated setup scripts

### 📦 Ready to Use

You now have everything needed to:
- **Create the GitHub repository** and push code
- **Create the GitLab repository** (in parallel)
- **Use Claude Code** to generate components and features
- **Set up CI/CD** for automated testing and deployment
- **Start development** immediately

### 🚀 What's Next

**For immediate setup:**
1. Create GitHub/GitLab repositories
2. Run setup script
3. Update environment variables
4. Start developing with Claude Code

**Next documentation parts:**
- ✅ Part 1: System Architecture Overview
- ✅ Part 2: Repository Structure & Setup (THIS DOCUMENT)
- ⏳ Part 3: Database Schema & ERD
- ⏳ Part 4: API Specifications
- ⏳ Part 5: Azure OpenAI Integration
- ⏳ Part 6: EHR Integration Architecture
- ⏳ Part 7: Frontend Workflows & Wireframes
- ⏳ Part 8: Security & HIPAA Compliance
- ⏳ Part 9: Deployment & DevOps Guide

---

**Ready to proceed to Part 3: Database Schema & ERD?**

---

*EclipseLink AI™ is a product of Rohimaya Health AI*  
*© 2025 Rohimaya Health AI. All rights reserved.*
