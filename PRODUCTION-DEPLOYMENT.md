# 🚀 Production Deployment Guide - EclipseLink AI

Complete guide for deploying EclipseLink AI to production on various platforms.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Option 1: Railway + Vercel (Recommended)](#option-1-railway--vercel-recommended)
- [Option 2: Docker Self-Hosted](#option-2-docker-self-hosted)
- [Option 3: Kubernetes (Enterprise)](#option-3-kubernetes-enterprise)
- [Option 4: AWS (Complete)](#option-4-aws-complete)
- [Post-Deployment](#post-deployment)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)

---

## Overview

**Estimated Deployment Time:** 30-60 minutes  
**Monthly Cost:** $20-200 depending on platform  
**Skill Level Required:** Intermediate

---

## Prerequisites

### Required Accounts

1. ✅ **GitHub Account** - For code repository
2. ✅ **OpenAI API Key** - Get from https://platform.openai.com ($5 minimum credit)
3. ✅ **Anthropic API Key** - Get from https://console.anthropic.com ($5 minimum credit)

### Choose Your Database

- **Option A: Supabase** (Free tier, easiest)
- **Option B: Railway PostgreSQL** ($5/month)
- **Option C: Self-hosted PostgreSQL**

### Required Tools

```bash
# Check if you have these installed
node --version   # Should be v20+
npm --version    # Should be v9+
git --version    # Any recent version
```

---

## Option 1: Railway + Vercel (Recommended)

**Best for:** Small to medium deployments (0-1000 users)  
**Cost:** ~$20-50/month  
**Difficulty:** ⭐⭐ Easy

### Step 1: Deploy Database (Supabase)

```bash
# 1. Go to https://supabase.com
# 2. Click "New Project"
# 3. Fill in:
#    - Name: eclipselink-ai-prod
#    - Database Password: [Generate strong password]
#    - Region: [Closest to your users]
#    - Plan: Free (or Pro for $25/month)
# 4. Wait 2-3 minutes for project creation

# 5. Copy these values (Settings → API):
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# 6. Run database schema (SQL Editor → New query):
# Copy and paste contents of: database/schema.sql
# Click "Run"
```

### Step 2: Deploy Backend (Railway)

```bash
# 1. Go to https://railway.app
# 2. Click "New Project" → "Deploy from GitHub repo"
# 3. Select your forked repository
# 4. Click "Add variables" and add:

ENVIRONMENT=production
DEBUG=false
DATABASE_URL=${{Postgres.DATABASE_URL}}  # If using Railway Postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SECRET_KEY=[Generate with: openssl rand -hex 32]
OPENAI_API_KEY=sk-proj-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
CORS_ORIGINS='["https://your-app.vercel.app"]'

# 5. Set root directory: apps/backend
# 6. Railway will auto-detect and deploy
# 7. Copy your Railway URL: https://xxx.railway.app
```

### Step 3: Deploy Frontend (Vercel)

```bash
# Option A: Via Vercel Dashboard
# 1. Go to https://vercel.com
# 2. Click "New Project"
# 3. Import your GitHub repository
# 4. Configure:
#    - Framework: Vite
#    - Root Directory: apps/frontend
#    - Build Command: npm run build
#    - Output Directory: dist
# 5. Add Environment Variables:

VITE_API_URL=https://your-railway-app.railway.app/api
VITE_ENVIRONMENT=production

# 6. Deploy!
# 7. Your app will be live at: https://your-app.vercel.app

# Option B: Via Vercel CLI
cd apps/frontend
npm install -g vercel
vercel --prod
# Follow the prompts
```

### Step 4: Update CORS

Go back to Railway and update `CORS_ORIGINS`:

```bash
CORS_ORIGINS='["https://your-app.vercel.app"]'
```

Redeploy Railway backend.

### Step 5: Test Your Deployment

```bash
# Test backend health
curl https://your-railway-app.railway.app/health

# Test frontend
open https://your-app.vercel.app

# Test full flow:
# 1. Register a new user
# 2. Create a patient
# 3. Upload a test audio file
# 4. Verify SBAR generation works
```

**✅ Done! Your app is live!**

---

## Option 2: Docker Self-Hosted

**Best for:** On-premise deployments, hospitals with existing infrastructure  
**Cost:** Infrastructure costs only  
**Difficulty:** ⭐⭐⭐ Moderate

### Prerequisites

- Ubuntu 20.04+ or similar Linux server
- Docker & Docker Compose installed
- 4GB RAM minimum, 8GB recommended
- 50GB disk space

### Step 1: Prepare Server

```bash
# SSH into your server
ssh user@your-server.com

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

### Step 2: Clone Repository

```bash
# Clone the repository
git clone https://github.com/HPagade/rohimaya-ai-eclipselink-product.git
cd rohimaya-ai-eclipselink-product

# Create production environment file
cp .env.production.example .env.production

# Edit with your values
nano .env.production
```

### Step 3: Configure Environment

Edit `.env.production`:

```bash
# Required: Generate secure passwords
POSTGRES_PASSWORD=$(openssl rand -hex 32)
REDIS_PASSWORD=$(openssl rand -hex 32)
SECRET_KEY=$(openssl rand -hex 32)

# Add your API keys
OPENAI_API_KEY=sk-proj-xxx
ANTHROPIC_API_KEY=sk-ant-xxx

# Set your domain
CORS_ORIGINS='["https://yourdomain.com"]'
VITE_API_URL=https://api.yourdomain.com/api
```

### Step 4: Deploy with Docker Compose

```bash
# Validate configuration
docker compose -f docker-compose.prod.yml config

# Build images
docker compose -f docker-compose.prod.yml build

# Start services
docker compose -f docker-compose.prod.yml --env-file .env.production up -d

# View logs
docker compose -f docker-compose.prod.yml logs -f

# Check status
docker compose -f docker-compose.prod.yml ps
```

### Step 5: Setup Nginx Reverse Proxy (Optional but Recommended)

```bash
# Install Nginx
sudo apt install nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/eclipselink
```

```nginx
# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/eclipselink /etc/nginx/sites-enabled/

# Test Nginx config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com
```

**✅ Done! Your app is self-hosted!**

---

## Option 3: Kubernetes (Enterprise)

**Best for:** Large hospitals, multi-tenant deployments  
**Cost:** Infrastructure costs only  
**Difficulty:** ⭐⭐⭐⭐⭐ Advanced

### Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured
- Helm 3.x installed
- 16GB RAM minimum across cluster
- Persistent storage (NFS/SAN)

### Step 1: Create Namespace

```bash
kubectl create namespace eclipselink-prod
kubectl config set-context --current --namespace=eclipselink-prod
```

### Step 2: Create Secrets

```bash
# Create secrets for sensitive data
kubectl create secret generic eclipselink-secrets \
  --from-literal=postgres-password=$(openssl rand -hex 32) \
  --from-literal=redis-password=$(openssl rand -hex 32) \
  --from-literal=secret-key=$(openssl rand -hex 32) \
  --from-literal=openai-api-key='sk-proj-xxx' \
  --from-literal=anthropic-api-key='sk-ant-xxx' \
  -n eclipselink-prod
```

### Step 3: Deploy PostgreSQL

```yaml
# Save as postgres-deployment.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: "eclipselink"
        - name: POSTGRES_USER
          value: "eclipselink_user"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: eclipselink-secrets
              key: postgres-password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 50Gi
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  clusterIP: None
```

```bash
kubectl apply -f postgres-deployment.yaml
```

### Step 4: Deploy Redis, Backend, Frontend

Similar manifests for Redis, Backend, and Frontend services...

*(Full Kubernetes manifests would be quite long - create separate files for each service)*

### Step 5: Deploy Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: eclipselink-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - yourdomain.com
    - api.yourdomain.com
    secretName: eclipselink-tls
  rules:
  - host: yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 3000
  - host: api.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backend
            port:
              number: 4000
```

```bash
kubectl apply -f ingress.yaml
```

**✅ Done! Kubernetes deployment complete!**

---

## Option 4: AWS (Complete)

**Best for:** Enterprise deployments requiring AWS infrastructure  
**Cost:** ~$100-500/month depending on usage  
**Difficulty:** ⭐⭐⭐⭐ Advanced

### Architecture

- **Frontend:** S3 + CloudFront
- **Backend:** ECS Fargate or EC2
- **Database:** RDS PostgreSQL
- **Cache:** ElastiCache Redis
- **Storage:** S3 for audio files
- **Load Balancer:** Application Load Balancer

### Quick Deploy with CDK/Terraform

*(Full AWS deployment would require extensive IaC code - consider using AWS Copilot or CDK)*

```bash
# Using AWS Copilot (easiest for AWS)
brew install aws/tap/copilot-cli

# Initialize
copilot init

# Deploy
copilot deploy
```

---

## Post-Deployment

### 1. Verify Health Checks

```bash
# Backend health
curl https://your-api-url.com/health

# Detailed health (includes DB check)
curl https://your-api-url.com/api/health/detailed

# Expected response:
# {
#   "status": "healthy",
#   "checks": {
#     "database": "connected",
#     "ai_services": "configured"
#   }
# }
```

### 2. Create First Admin User

```bash
# Via API
curl -X POST https://your-api-url.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@yourhospital.com",
    "password": "SecurePassword123!",
    "user_type": "admin",
    "facility_id": "your-facility-id"
  }'
```

### 3. Test Complete Flow

1. ✅ Register user
2. ✅ Login
3. ✅ Create patient
4. ✅ Upload audio file
5. ✅ Verify SBAR generation
6. ✅ Check audit logs

### 4. Setup Monitoring

**Option A: Sentry (Recommended)**
```bash
# Add to environment variables
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
```

**Option B: CloudWatch/Datadog/New Relic**
- Configure based on your platform

---

## Monitoring & Maintenance

### Daily Checks

```bash
# Check service status
docker compose -f docker-compose.prod.yml ps

# Check logs for errors
docker compose -f docker-compose.prod.yml logs --tail=100 | grep ERROR

# Check disk space
df -h

# Check memory usage
free -m
```

### Weekly Checks

- Review error logs in Sentry
- Check API latency metrics
- Review AI API costs
- Check database size and growth
- Verify backups are working

### Monthly Tasks

- Update dependencies
- Review and rotate credentials
- Performance optimization
- Cost optimization review

### Backup Strategy

```bash
# Automated daily backups (add to crontab)
0 2 * * * docker exec eclipselink-postgres-prod pg_dump -U eclipselink_user eclipselink | gzip > /backups/eclipselink-$(date +\%Y\%m\%d).sql.gz

# Keep 30 days of backups
find /backups -name "eclipselink-*.sql.gz" -mtime +30 -delete
```

---

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
docker compose logs backend

# Common issues:
# 1. Database not ready - wait 30 seconds and restart
# 2. Missing environment variables - check .env.production
# 3. Port already in use - change BACKEND_PORT
```

### Frontend Won't Load

```bash
# Check if backend is accessible
curl https://your-api-url.com/health

# Check CORS settings
# Ensure CORS_ORIGINS includes your frontend URL

# Check browser console for errors
```

### Database Connection Failed

```bash
# Test database connection
docker exec -it eclipselink-postgres-prod psql -U eclipselink_user -d eclipselink

# If fails, check:
# 1. POSTGRES_PASSWORD is correct
# 2. Database container is running
# 3. Network connectivity
```

### AI Generation Fails

```bash
# Check API keys are valid
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check Anthropic key
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"

# Common issues:
# 1. API keys expired or invalid
# 2. Insufficient credits
# 3. Rate limiting
```

### High Costs

```bash
# Check AI API usage
# OpenAI Dashboard: https://platform.openai.com/usage
# Anthropic Dashboard: https://console.anthropic.com/settings/usage

# Optimize:
# 1. Implement caching for similar handoffs
# 2. Reduce audio file size before upload
# 3. Use shorter prompts
# 4. Implement rate limiting
```

---

## Security Checklist

Before going live:

- [ ] All secrets rotated from defaults
- [ ] SECRET_KEY generated with `openssl rand -hex 32`
- [ ] DEBUG=false in production
- [ ] HTTPS/TLS enabled
- [ ] CORS_ORIGINS restricted to your domains only
- [ ] Rate limiting enabled
- [ ] Backups configured and tested
- [ ] Monitoring/alerting setup
- [ ] Error tracking enabled (Sentry)
- [ ] Security headers configured
- [ ] Database credentials strong
- [ ] Regular security updates scheduled
- [ ] HIPAA compliance review completed
- [ ] Incident response plan documented

---

## Performance Optimization

### Backend

```python
# Increase workers for production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4000", "--workers", "4"]
```

### Database

```sql
-- Add indexes for common queries
CREATE INDEX idx_handoffs_facility_id ON handoffs(facility_id);
CREATE INDEX idx_handoffs_created_at ON handoffs(created_at DESC);
CREATE INDEX idx_patients_facility_id ON patients(facility_id);
```

### Frontend

- Enable CDN (CloudFlare/CloudFront)
- Optimize images
- Enable gzip compression (already in nginx.conf)
- Use production build (already configured)

---

## Cost Optimization

### Current Budget Breakdown

| Service | Cost/Month | Notes |
|---------|-----------|-------|
| Railway Backend | $20 | Can scale to $50 with usage |
| Vercel Frontend | $0-20 | Free tier sufficient for <100 users |
| Supabase DB | $0-25 | Free tier or Pro |
| OpenAI API | $20-50 | ~$0.006/minute audio |
| Anthropic API | $30-100 | ~$0.50/handoff |
| **Total** | **$70-215** | **Per 100-500 users** |

### Optimization Tips

1. **Cache AI responses** - Avoid re-processing similar handoffs
2. **Compress audio** - Reduce file sizes before uploading
3. **Use reserved capacity** - If predictable usage
4. **Monitor usage** - Set up alerts for unusual spikes

---

## Support

- 📖 **Documentation:** Check README.md and other docs
- 🐛 **Issues:** GitHub Issues
- 💬 **Questions:** support@rohimaya.ai
- 🏢 **Enterprise:** enterprise@rohimaya.ai

---

**✅ You're ready for production! Good luck! 🚀**
