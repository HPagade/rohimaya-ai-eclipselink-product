# EclipseLink AI™

<div align="center">

**Voice-enabled clinical handoff platform with AI-powered SBAR generation**

[![License](https://img.shields.io/badge/license-Proprietary-blue.svg)](LICENSE)
[![Node Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue.svg)](https://www.typescriptlang.org)

</div>

---

## 🦚 About Rohimaya Health AI

EclipseLink AI™ is the flagship product of **Rohimaya Health AI**, a healthtech startup revolutionizing clinical communication and patient handoffs.

**Founded by:**
- **Hannah Kraulik Pagade** - CEO
- **Prasad Pagade** - CTO

---

## 📖 Product Overview

EclipseLink AI transforms the way healthcare professionals conduct patient handoffs. Using advanced AI, it converts 3-5 minute voice recordings into structured SBAR (Situation, Background, Assessment, Recommendation) reports in under 30 seconds.

### Core Features

✅ **Voice-to-SBAR Conversion** - AI-powered transcription and structuring
✅ **EHR Integration** - Seamless connection with Epic, Cerner, MEDITECH
✅ **Multi-Platform Access** - Progressive Web App (mobile, tablet, desktop)
✅ **HIPAA Compliant** - End-to-end encryption with audit trails
✅ **Real-time Processing** - Fast transcription and report generation
✅ **Multi-facility Support** - Scalable across hospitals and clinics

### Target Market

**Total Addressable Market (TAM):** $18.9 billion healthcare communication market

**Primary Users:**
- Registered Nurses (RN)
- Physicians (MD/DO)
- Nurse Practitioners (NP)
- Physician Assistants (PA)
- Licensed Practical Nurses (LPN)
- Certified Nursing Assistants (CNA)
- Medical Assistants (MA)
- Allied Health Professionals (RT, PT, OT, EMT)
- Medical Technicians (Radiologic, Surgical, Lab, Pharmacy)

**Facilities:**
- 6,090 hospitals
- 87,000+ nursing homes
- 13,000+ clinics in the US

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 14 with App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Components:** shadcn/ui + Radix UI
- **State Management:** Zustand + React Query
- **PWA:** next-pwa

### Backend
- **Framework:** Express.js
- **Language:** TypeScript
- **Database:** PostgreSQL (Supabase)
- **Cache/Queue:** Redis (Upstash) + BullMQ
- **Storage:** Cloudflare R2
- **AI Services:** Azure OpenAI (Whisper + GPT-4)

### Deployment
- **Frontend:** Cloudflare Pages
- **Backend:** Railway
- **CI/CD:** GitHub Actions / GitLab CI

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ ([Download](https://nodejs.org))
- **npm** 9+
- **Git** ([Download](https://git-scm.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/HPagade/rohimaya-ai-eclipselink-product.git
cd rohimaya-ai-eclipselink-product

# Run the setup script
bash scripts/setup.sh

# Update environment variables
# Edit these files with your actual values:
# - apps/frontend/.env.local
# - apps/backend/.env
```

### Development

```bash
# Terminal 1: Run frontend
npm run dev:frontend

# Terminal 2: Run backend
npm run dev:backend

# Open browser
# Navigate to http://localhost:3000
```

### Build for Production

```bash
# Build frontend
npm run build:frontend

# Build backend
npm run build:backend
```

### Testing

```bash
# Run all tests
npm test

# Run linter
npm run lint

# Format code
npm run format
```

---

## 📁 Repository Structure

```
eclipselink-ai/
├── apps/
│   ├── frontend/          # Next.js PWA
│   └── backend/           # Express.js API
├── packages/              # Shared packages
│   ├── types/            # TypeScript types
│   ├── config/           # Shared configuration
│   └── utils/            # Shared utilities
├── database/              # Database files
│   ├── migrations/       # SQL migrations
│   ├── seeds/            # Seed data
│   └── functions/        # Database functions
├── docs/                  # Documentation
│   ├── api/              # API documentation
│   ├── architecture/     # Architecture docs
│   └── guides/           # User guides
├── scripts/               # Automation scripts
├── .github/               # GitHub workflows
├── .gitlab/               # GitLab CI/CD
└── .claude/               # Claude Code integration
```

---

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

### Architecture & Setup
- **[System Architecture Overview](docs/architecture/system-overview.md)** - Complete system architecture
- **[Repository Setup Guide](docs/guides/repository-setup.md)** - Detailed setup instructions

### Coming Soon
- Database Schema & ERD
- API Specifications
- Azure OpenAI Integration
- EHR Integration Architecture
- Frontend Workflows & Wireframes
- Security & HIPAA Compliance
- Deployment & DevOps Guide

---

## 🧑‍💻 Development Workflow

### Git Workflow (Git Flow)

```
main                    (production)
├── develop             (staging)
│   ├── feature/*      (new features)
│   ├── bugfix/*       (bug fixes)
│   └── hotfix/*       (emergency fixes)
```

### Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format
<type>(<scope>): <subject>

# Examples
git commit -m "feat(voice): add waveform visualization"
git commit -m "fix(auth): resolve token refresh issue"
git commit -m "docs(api): update handoff endpoints"
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Guidelines

- Use TypeScript strict mode
- Follow ESLint + Prettier rules
- Write comprehensive tests (>80% coverage)
- Add JSDoc comments for public functions
- Update documentation when adding features

---

## 🔐 Security & Compliance

EclipseLink AI is built with security and HIPAA compliance at its core:

- **End-to-end encryption** for all data in transit and at rest
- **Role-based access control (RBAC)** for user permissions
- **Comprehensive audit logging** for all PHI access
- **Business Associate Agreements (BAA)** with all third-party services
- **Regular security audits** and penetration testing

For more details, see our [Security Documentation](docs/architecture/system-overview.md#security-architecture).

---

## 🚢 Deployment

### Production Environments

- **Frontend:** [app.eclipselink.ai](https://app.eclipselink.ai) (Cloudflare Pages)
- **Backend API:** [api.eclipselink.ai](https://api.eclipselink.ai) (Railway)
- **Database:** Supabase (PostgreSQL)
- **Storage:** Cloudflare R2

### CI/CD Pipeline

Automated testing and deployment via:
- **GitHub Actions** (for GitHub repository)
- **GitLab CI** (for GitLab repository)

---

## 📊 Roadmap

### Phase 1: MVP (Current)
- [x] Repository structure
- [x] Documentation (Parts 1-2)
- [ ] Core frontend components
- [ ] Backend API implementation
- [ ] Azure OpenAI integration
- [ ] Basic EHR integration (Epic)

### Phase 2: Beta Launch
- [ ] Full EHR support (Cerner, MEDITECH)
- [ ] Advanced analytics dashboard
- [ ] Multi-facility management
- [ ] Mobile app optimization

### Phase 3: Scale
- [ ] Enterprise features
- [ ] Integration with PlumeDose AI
- [ ] International expansion
- [ ] Advanced AI features

---

## 📄 License

Proprietary - © 2025 Rohimaya Health AI. All rights reserved.

This software is the exclusive property of Rohimaya Health AI. Unauthorized copying, modification, distribution, or use is strictly prohibited.

---

## 📞 Contact

**Rohimaya Health AI**

- **Website:** [rohimaya.ai](https://rohimaya.ai) *(coming soon)*
- **Email:** contact@rohimaya.ai
- **Support:** support@eclipselink.ai

---

## 🙏 Acknowledgments

Special thanks to:
- Azure OpenAI team for AI services
- Supabase for database infrastructure
- Cloudflare for edge network and storage
- Railway for backend hosting
- The open-source community

---

<div align="center">

**Built with ❤️ by Rohimaya Health AI**

*Transforming Healthcare Communication, One Handoff at a Time*

</div>
