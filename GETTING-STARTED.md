# Getting Started with EclipseLink AI Development

**A beginner-friendly guide to deploying and working with EclipseLink AI**

Welcome! This guide will walk you through everything you need to get EclipseLink AI up and running.

---

## 📋 Pre-Development Checklist

Before you start coding or deploying, make sure you understand the project:

### Understanding the Project
- [ ] Read [README.md](README.md) - Understand what EclipseLink AI does
- [ ] Review [docs/products/ALL-PRODUCTS-OVERVIEW.md](docs/products/ALL-PRODUCTS-OVERVIEW.md) - See the full product ecosystem
- [ ] Read [README-USERS.md](README-USERS.md) - Understand the user perspective
- [ ] Check [docs/products/ECLIPSELINK-AI-MVP-DEVELOPMENT-BRIEF.md](docs/products/ECLIPSELINK-AI-MVP-DEVELOPMENT-BRIEF.md) - Deep dive into MVP

### Healthcare Context
- [ ] Understand SBAR (Situation, Background, Assessment, Recommendation) format
- [ ] Learn about clinical handoffs and why they matter
- [ ] Review HIPAA compliance basics
- [ ] Understand the 15 healthcare roles this serves

---

## 🛠️ Your Development Environment Setup

### Step 1: Install Required Software

#### 1.1 Core Tools (Required)
- [ ] **Git** - Version control
  ```bash
  # Check if installed
  git --version
  # Should show: git version 2.x.x or higher
  ```
  - Not installed? Download from [git-scm.com](https://git-scm.com/)

- [ ] **Node.js 18+** and **npm** - JavaScript runtime
  ```bash
  # Check if installed
  node --version
  npm --version
  # Should show: v18.x.x or higher
  ```
  - Not installed? Download from [nodejs.org](https://nodejs.org/)

- [ ] **Docker & Docker Compose** - Container platform (easiest deployment)
  ```bash
  # Check if installed
  docker --version
  docker-compose --version
  ```
  - Not installed? Download from [docker.com](https://docs.docker.com/get-docker/)

#### 1.2 Development Tools (Recommended)
- [ ] **Visual Studio Code** - Code editor
  - Download from [code.visualstudio.com](https://code.visualstudio.com/)
  - Install extensions:
    - ESLint
    - Prettier
    - TypeScript
    - Python (if working with backend)

- [ ] **Python 3.9+** - For backend API (if not using Docker)
  ```bash
  python3 --version
  # Should show: Python 3.9.x or higher
  ```

- [ ] **PostgreSQL 15+** - Database (if not using Docker)
  - Download from [postgresql.org](https://www.postgresql.org/download/)

---

## 🚀 Step 2: Clone and Initial Setup

### 2.1 Clone the Repository
```bash
# Navigate to where you want the project
cd ~/Projects  # or wherever you keep code

# Clone the repository (use the actual repository name)
git clone https://github.com/HPagade/[REPOSITORY-NAME].git

# Navigate into the project
cd [REPOSITORY-NAME]

# Check that you're on the right branch
git branch
```

### 2.2 Explore the Structure
- [ ] Open the project in VS Code
- [ ] Browse through the main directories:
  - `apps/frontend/` - Next.js frontend application
  - `apps/backend/` - Python FastAPI backend
  - `database/` - Database schemas and migrations
  - `docs/` - All documentation
  - `k8s/` - Kubernetes deployment configs
  - `website/` - Marketing website

---

## 🔑 Step 3: Configure Environment Variables

### 3.1 Copy Environment Templates
```bash
# Copy the example environment file
cp .env.example .env

# For production deployment (later)
cp .env.production.example .env.production
```

### 3.2 Get Required API Keys

#### Azure OpenAI (Required for AI features)
- [ ] Create Azure account at [azure.microsoft.com](https://azure.microsoft.com/)
- [ ] Request access to Azure OpenAI Service
- [ ] Create OpenAI resource in Azure Portal
- [ ] Get your API key and endpoint
- [ ] Add to `.env`:
  ```bash
  AZURE_OPENAI_API_KEY=your-key-here
  AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
  ```

#### Database Setup
- [ ] Choose deployment option:
  - **Option A: Use Docker** (easiest) - No manual setup needed
  - **Option B: Use Supabase** (cloud database)
    - Create account at [supabase.com](https://supabase.com)
    - Create new project
    - Get connection string
    - Add to `.env`
  - **Option C: Local PostgreSQL** - Install PostgreSQL locally

### 3.3 Edit Environment Variables
```bash
# Edit the .env file with your preferred editor
nano .env
# or
code .env
```

Required variables:
- [ ] `AZURE_OPENAI_API_KEY` - Your Azure OpenAI key
- [ ] `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint
- [ ] `DATABASE_URL` - Database connection string
- [ ] `SECRET_KEY` - Generate with: `openssl rand -hex 32`
- [ ] `JWT_SECRET` - Generate with: `openssl rand -hex 32`

---

## 🐳 Step 4: Choose Your Deployment Path

### Option A: Docker Deployment (Recommended for Beginners)

#### 4.1 Start Everything with Docker
```bash
# Start all services (database, backend, frontend, redis)
docker-compose up -d

# Check that all containers are running
docker-compose ps

# View logs to check for errors
docker-compose logs -f
```

#### 4.2 Verify It's Working
- [ ] Frontend running: Open [http://localhost:3000](http://localhost:3000)
- [ ] Backend running: Open [http://localhost:4000/api/docs](http://localhost:4000/api/docs)
- [ ] No error messages in logs

#### 4.3 Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove all data (reset everything)
docker-compose down -v
```

### Option B: Manual Development Setup

#### 4.1 Install Dependencies
```bash
# Install Node.js dependencies
npm install

# Install frontend dependencies
cd apps/frontend
npm install
cd ../..

# Install backend dependencies (if using Python locally)
cd apps/backend
pip install -r requirements.txt
cd ../..
```

#### 4.2 Setup Database
```bash
# Run database migrations
npm run db:setup
npm run db:migrate

# Optional: Seed test data
npm run db:seed
```

#### 4.3 Start Development Servers
```bash
# Terminal 1: Start backend
npm run dev:backend

# Terminal 2: Start frontend
npm run dev:frontend

# Or start both together
npm run dev
```

---

## ✅ Step 5: Verify Your Setup

### 5.1 Check the Frontend
- [ ] Open [http://localhost:3000](http://localhost:3000)
- [ ] Can you see the EclipseLink AI login page?
- [ ] Are the styles loading correctly?
- [ ] Check browser console for errors (F12)

### 5.2 Check the Backend
- [ ] Open [http://localhost:4000/api/docs](http://localhost:4000/api/docs)
- [ ] Can you see the Swagger API documentation?
- [ ] Try the `/health` endpoint - should return `{"status": "healthy"}`

### 5.3 Check Database Connection
```bash
# If using Docker
docker-compose exec postgres psql -U eclipselink -d eclipselink_db -c "\dt"
# Should show list of tables

# If using local PostgreSQL
psql -U your_user -d eclipselink_db -c "\dt"
```

---

## 📖 Step 6: Learn the Codebase

### 6.1 Frontend (Next.js + React)
Start here: `apps/frontend/src/`
- [ ] `pages/` - Page components and routing
- [ ] `components/` - Reusable UI components
- [ ] `lib/` - Utility functions and API clients
- [ ] `styles/` - CSS and Tailwind styles

Key files to understand:
- [ ] `pages/index.tsx` - Landing page
- [ ] `pages/dashboard.tsx` - Main dashboard
- [ ] `pages/handoffs/new.tsx` - Create new handoff

### 6.2 Backend (Python + FastAPI)
Start here: `apps/backend/app/`
- [ ] `main.py` - Application entry point
- [ ] `routers/` - API endpoint definitions
- [ ] `services/` - Business logic
- [ ] `models.py` - Database models

Key files to understand:
- [ ] `routers/handoffs.py` - Handoff endpoints
- [ ] `services/ai_service.py` - AI integration
- [ ] `database.py` - Database connection

### 6.3 Database Schema
- [ ] Review `database/schema.sql` - Full database structure
- [ ] Check `database/migrations/` - Database version history

---

## 🧪 Step 7: Make Your First Change

### 7.1 Create a Test Branch
```bash
# Create a new branch for testing
git checkout -b test/my-first-change

# Check that you're on the new branch
git branch
```

### 7.2 Make a Simple Change
Try changing the welcome message:
```bash
# Edit the file
code apps/frontend/src/pages/index.tsx

# Find the welcome text and change it
# Save the file

# If dev server is running, check localhost:3000 to see your change
```

### 7.3 Test Your Change
- [ ] Does the frontend still load?
- [ ] Do you see your change?
- [ ] Are there any console errors?

### 7.4 Commit Your Change
```bash
# Check what changed
git status

# Stage your changes
git add apps/frontend/src/pages/index.tsx

# Commit with a message
git commit -m "test: Update welcome message"

# Switch back to main branch
git checkout main

# Delete test branch (if you want)
git branch -D test/my-first-change
```

---

## 🚀 Step 8: Deploy to Production (When Ready)

### 8.1 Pre-Deployment Checklist
Before deploying to production:
- [ ] Read [docs/deployment/PRODUCTION-DEPLOYMENT.md](docs/deployment/PRODUCTION-DEPLOYMENT.md)
- [ ] Complete [docs/security/SECURITY-CHECKLIST.md](docs/security/SECURITY-CHECKLIST.md)
- [ ] Test thoroughly in development
- [ ] Prepare production environment variables
- [ ] Choose deployment platform (Railway, Vercel, K8s, Docker)

### 8.2 Deployment Options

#### Cloud Deployment (Easiest)
- [ ] **Frontend**: Deploy to Vercel or Cloudflare Pages
- [ ] **Backend**: Deploy to Railway or Heroku
- [ ] **Database**: Use Supabase or Railway PostgreSQL
- [ ] Follow guide: [docs/deployment/QUICK-SETUP-GUIDE.md](docs/deployment/QUICK-SETUP-GUIDE.md)

#### Docker Deployment (On-Premise)
- [ ] Prepare production server
- [ ] Configure `docker-compose.prod.yml`
- [ ] Set up SSL certificates
- [ ] Follow guide: [docs/deployment/PRODUCTION-DEPLOYMENT.md](docs/deployment/PRODUCTION-DEPLOYMENT.md)

#### Kubernetes (Enterprise)
- [ ] Set up Kubernetes cluster
- [ ] Configure secrets
- [ ] Deploy with manifests in `k8s/`
- [ ] Follow guide: [k8s/README.md](k8s/README.md)

---

## 📚 Step 9: Understand the Full Ecosystem

### 9.1 The 8 Products
- [ ] Read [docs/products/ALL-PRODUCTS-OVERVIEW.md](docs/products/ALL-PRODUCTS-OVERVIEW.md)
- [ ] Understand how they integrate together
- [ ] See the roadmap for future products

### 9.2 The Rewards Program
- [ ] Learn about Phoenix & Peacock Honors™
- [ ] Understand the gamification strategy
- [ ] See how it drives adoption

### 9.3 Business Context
- [ ] Review target market (9M+ healthcare professionals)
- [ ] Understand pricing strategy
- [ ] Learn about regulatory compliance (HIPAA)

---

## 🆘 Step 10: Get Help When Stuck

### Common Issues and Solutions

**"Docker won't start"**
- Check Docker Desktop is running
- Try: `docker system prune` to clean up
- Restart Docker Desktop

**"Port already in use"**
- Something else is using port 3000 or 4000
- Stop other services or change ports in docker-compose.yml

**"Database connection failed"**
- Check DATABASE_URL in .env
- Verify database is running: `docker-compose ps`
- Check logs: `docker-compose logs postgres`

**"Azure OpenAI errors"**
- Verify your API key is correct
- Check your Azure subscription has OpenAI access
- Ensure endpoint URL is correct

### Getting Support
- [ ] **Documentation**: Check [docs/DOCUMENTATION-INDEX.md](docs/DOCUMENTATION-INDEX.md)
- [ ] **GitHub Issues**: Search existing issues or create new one
- [ ] **Email Support**: support@rohimaya.ai
- [ ] **Community**: (Coming soon - Discord/Slack)

---

## 🎯 Next Steps

### For Developers
1. [ ] Read [docs/development/README-DEVELOPERS.md](docs/development/README-DEVELOPERS.md)
2. [ ] Review [docs/development/CONTRIBUTING.md](docs/development/CONTRIBUTING.md)
3. [ ] Pick an issue to work on
4. [ ] Submit your first PR!

### For Deployers
1. [ ] Complete production deployment
2. [ ] Set up monitoring and alerts
3. [ ] Configure backups
4. [ ] Train end users

### For Product Managers
1. [ ] Review [docs/products/WIREFRAMES.md](docs/products/WIREFRAMES.md)
2. [ ] Understand user workflows
3. [ ] Plan feature priorities
4. [ ] Gather user feedback

---

## 🎓 Learning Resources

### Healthcare Technology
- [ ] SBAR Format: [Wikipedia](https://en.wikipedia.org/wiki/SBAR)
- [ ] Clinical Handoffs: [Joint Commission](https://www.jointcommission.org/)
- [ ] HIPAA Basics: [HHS.gov](https://www.hhs.gov/hipaa/)

### Technical Stack
- [ ] Next.js: [nextjs.org/learn](https://nextjs.org/learn)
- [ ] React: [react.dev/learn](https://react.dev/learn)
- [ ] FastAPI: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- [ ] PostgreSQL: [postgresql.org/docs](https://www.postgresql.org/docs/)
- [ ] Docker: [docker.com/get-started](https://docs.docker.com/get-started/)

---

## ✅ Final Checklist

Before considering yourself "set up and ready":

### Technical Setup
- [ ] All services start without errors
- [ ] Frontend loads and displays correctly
- [ ] Backend API responds to requests
- [ ] Database is connected and seeded
- [ ] Environment variables are configured

### Knowledge
- [ ] Understand what EclipseLink AI does
- [ ] Know the codebase structure
- [ ] Can make and test a simple change
- [ ] Know where to find documentation
- [ ] Know how to get help

### Ready for Next Steps
- [ ] Have decided: development, deployment, or both?
- [ ] Have read relevant guides for your path
- [ ] Have access to required services (Azure, etc.)
- [ ] Know your first task or issue to work on

---

## 🎉 You're Ready!

Congratulations! You've completed the getting started guide. You now have:
- ✅ A working development environment
- ✅ Understanding of the project
- ✅ Knowledge of where to find information
- ✅ Ability to make changes and test them

**Welcome to the Rohimaya Health AI team!** 🦚🔥

---

**Questions?** Contact support@rohimaya.ai

**Found a bug in this guide?** Please let us know!

---

**Last Updated:** November 2025  
**Version:** 1.0.0
