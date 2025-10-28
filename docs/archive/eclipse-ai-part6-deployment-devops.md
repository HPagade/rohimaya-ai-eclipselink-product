# EclipseLink AI™ - Part 6: Deployment & DevOps Guide

**Document Version:** 1.0  
**Last Updated:** October 23, 2025  
**Product:** EclipseLink AI™ Clinical Handoff System  
**Company:** Rohimaya Health AI  
**Founders:** Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO)

---

## Table of Contents

1. [Infrastructure Overview](#infrastructure-overview)
2. [Environment Configuration](#environment-configuration)
3. [Railway Deployment](#railway-deployment)
4. [Cloudflare Setup](#cloudflare-setup)
5. [Database Management](#database-management)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [Monitoring & Logging](#monitoring-logging)
8. [Backup & Disaster Recovery](#backup-disaster-recovery)
9. [Scaling Strategy](#scaling-strategy)

---

## 1. Infrastructure Overview

### 1.1 Production Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLOUDFLARE                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │     CDN      │  │   DNS/SSL    │  │   R2 Storage         │ │
│  │  (Global)    │  │  (Managed)   │  │   (Audio Files)      │ │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘ │
└─────────┼──────────────────┼──────────────────────┼─────────────┘
          │                  │                      │
          │ HTTPS            │ Domain              │ S3 API
          │                  │                      │
          ▼                  ▼                      │
┌──────────────────────────────────────────┐        │
│           RAILWAY.APP                     │        │
│  ┌────────────────────────────────────┐  │        │
│  │     Next.js Application            │  │        │
│  │  (Frontend + API Routes)           │  │        │
│  │  - Port 3000                       │  │        │
│  │  - Auto-scaling                    │  │        │
│  │  - Zero-downtime deploys           │  │        │
│  └────────────┬───────────────────────┘  │        │
│               │                           │        │
│               │ Database Connection       │        │
│               │                           │        │
│  ┌────────────▼───────────────────────┐  │        │
│  │     Supabase PostgreSQL            │◄─┼────────┘
│  │  (Hosted Database)                 │  │
│  │  - Connection pooling              │  │
│  │  - Automated backups               │  │
│  │  - Point-in-time recovery          │  │
│  └────────────────────────────────────┘  │
└───────────────────────────────────────────┘
          │
          │ Logs
          ▼
┌──────────────────────┐
│   Logtail/Better     │
│   Stack (Logging)    │
└──────────────────────┘

EXTERNAL SERVICES:
┌─────────────────┐     ┌─────────────────┐
│  Azure OpenAI   │     │   Upstash Redis │
│  (Whisper/GPT-4)│     │   (Caching)     │
└─────────────────┘     └─────────────────┘
```

### 1.2 Infrastructure Components

**Hosting & Compute:**
- **Railway** - Application hosting, auto-scaling
- **Supabase** - PostgreSQL database (hosted)
- **Upstash Redis** - Caching layer

**CDN & Storage:**
- **Cloudflare CDN** - Global edge network
- **Cloudflare R2** - Audio file storage (S3-compatible)
- **Cloudflare DNS** - Domain management

**AI Services:**
- **Azure OpenAI** - Whisper & GPT-4 APIs

**Monitoring:**
- **Logtail/Better Stack** - Log aggregation
- **Railway Metrics** - Application metrics
- **Supabase Dashboard** - Database metrics

### 1.3 Cost Breakdown (Monthly Estimates)

| Service | Tier | Cost | Notes |
|---------|------|------|-------|
| Railway | Hobby | $5-20 | Based on usage |
| Supabase | Pro | $25 | Database + Auth + Storage |
| Cloudflare R2 | Pay-as-you-go | $5-15 | Storage + requests |
| Cloudflare CDN | Free | $0 | Sufficient for seed stage |
| Azure OpenAI | Pay-per-use | $60-140 | 1000 handoffs/month |
| Upstash Redis | Free/Paid | $0-10 | 10K requests/day free |
| Logtail | Free/Paid | $0-15 | 1GB/month free |
| **Total** | | **$95-225/month** | Very affordable for seed stage |

---

## 2. Environment Configuration

### 2.1 Environment Strategy

**Three Environments:**
1. **Development** - Local machines
2. **Staging** - Pre-production testing
3. **Production** - Live system

### 2.2 Environment Variables

**.env.development:**
```bash
# Application
NODE_ENV=development
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:3000/api

# Supabase (Development Project)
NEXT_PUBLIC_SUPABASE_URL=https://your-dev-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_dev_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_dev_service_role_key

# Database (Direct Connection)
DATABASE_URL=postgresql://postgres:password@localhost:54322/postgres

# Azure OpenAI (Development)
AZURE_OPENAI_API_KEY=dev_api_key
AZURE_OPENAI_ENDPOINT=https://eclipselink-dev-openai.openai.azure.com/
AZURE_OPENAI_WHISPER_DEPLOYMENT=whisper-dev
AZURE_OPENAI_GPT4_DEPLOYMENT=gpt4-dev

# Cloudflare R2 (Development Bucket)
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=dev_access_key
R2_SECRET_ACCESS_KEY=dev_secret_key
R2_BUCKET_NAME=eclipselink-audio-dev
R2_PUBLIC_URL=https://dev-audio.eclipselink.ai

# Redis (Local or Upstash Free)
REDIS_URL=redis://localhost:6379
# OR
UPSTASH_REDIS_REST_URL=https://your-redis.upstash.io
UPSTASH_REDIS_REST_TOKEN=your_token

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_change_in_production
JWT_EXPIRES_IN=1h
REFRESH_TOKEN_SECRET=your_refresh_token_secret
REFRESH_TOKEN_EXPIRES_IN=30d

# Logging
LOG_LEVEL=debug
LOGTAIL_SOURCE_TOKEN=your_dev_token

# Feature Flags
ENABLE_EHR_SYNC=false
ENABLE_WEBHOOKS=false
```

**.env.staging:**
```bash
# Application
NODE_ENV=staging
NEXT_PUBLIC_APP_URL=https://staging.eclipselink.ai
NEXT_PUBLIC_API_URL=https://staging.eclipselink.ai/api

# Supabase (Staging Project)
NEXT_PUBLIC_SUPABASE_URL=https://staging-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=staging_anon_key
SUPABASE_SERVICE_ROLE_KEY=staging_service_role_key

# Database (Connection Pooler)
DATABASE_URL=postgresql://postgres.staging:password@aws-0-us-east-1.pooler.supabase.com:5432/postgres

# Azure OpenAI (Staging)
AZURE_OPENAI_API_KEY=staging_api_key
AZURE_OPENAI_ENDPOINT=https://eclipselink-staging-openai.openai.azure.com/
AZURE_OPENAI_WHISPER_DEPLOYMENT=whisper-staging
AZURE_OPENAI_GPT4_DEPLOYMENT=gpt4-staging

# Cloudflare R2 (Staging Bucket)
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=staging_access_key
R2_SECRET_ACCESS_KEY=staging_secret_key
R2_BUCKET_NAME=eclipselink-audio-staging
R2_PUBLIC_URL=https://staging-audio.eclipselink.ai

# Redis (Upstash Staging)
UPSTASH_REDIS_REST_URL=https://staging-redis.upstash.io
UPSTASH_REDIS_REST_TOKEN=staging_token

# JWT Configuration
JWT_SECRET=staging_jwt_secret_use_secure_random_string
JWT_EXPIRES_IN=1h
REFRESH_TOKEN_SECRET=staging_refresh_token_secret
REFRESH_TOKEN_EXPIRES_IN=30d

# Logging
LOG_LEVEL=info
LOGTAIL_SOURCE_TOKEN=staging_logtail_token

# Feature Flags
ENABLE_EHR_SYNC=true
ENABLE_WEBHOOKS=true
```

**.env.production:**
```bash
# Application
NODE_ENV=production
NEXT_PUBLIC_APP_URL=https://app.eclipselink.ai
NEXT_PUBLIC_API_URL=https://app.eclipselink.ai/api

# Supabase (Production Project)
NEXT_PUBLIC_SUPABASE_URL=https://prod-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=prod_anon_key
SUPABASE_SERVICE_ROLE_KEY=prod_service_role_key

# Database (Connection Pooler with SSL)
DATABASE_URL=postgresql://postgres.prod:password@aws-0-us-east-1.pooler.supabase.com:5432/postgres?sslmode=require

# Azure OpenAI (Production)
AZURE_OPENAI_API_KEY=prod_api_key
AZURE_OPENAI_ENDPOINT=https://eclipselink-prod-openai.openai.azure.com/
AZURE_OPENAI_WHISPER_DEPLOYMENT=whisper-prod
AZURE_OPENAI_GPT4_DEPLOYMENT=gpt4-prod

# Cloudflare R2 (Production Bucket)
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=prod_access_key
R2_SECRET_ACCESS_KEY=prod_secret_key
R2_BUCKET_NAME=eclipselink-audio-prod
R2_PUBLIC_URL=https://audio.eclipselink.ai

# Redis (Upstash Production)
UPSTASH_REDIS_REST_URL=https://prod-redis.upstash.io
UPSTASH_REDIS_REST_TOKEN=prod_token

# JWT Configuration (Use Azure Key Vault or secure secret manager)
JWT_SECRET=production_jwt_secret_64_char_minimum_secure_random
JWT_EXPIRES_IN=1h
REFRESH_TOKEN_SECRET=production_refresh_token_secret_64_char_minimum
REFRESH_TOKEN_EXPIRES_IN=30d

# Logging
LOG_LEVEL=warn
LOGTAIL_SOURCE_TOKEN=prod_logtail_token

# Feature Flags
ENABLE_EHR_SYNC=true
ENABLE_WEBHOOKS=true
ENABLE_ANALYTICS=true

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_MAX_REQUESTS=100
RATE_LIMIT_WINDOW_MS=60000

# Security
CORS_ORIGIN=https://app.eclipselink.ai
HELMET_ENABLED=true
```

### 2.3 Secret Management

**Development:**
- Store in `.env.local` (gitignored)

**Staging/Production:**
- Use Railway's encrypted environment variables
- Consider Azure Key Vault for sensitive secrets

**Secret Rotation:**
```bash
# Rotate JWT secrets every 90 days
# Rotate API keys every 180 days
# Rotate database passwords every 365 days
```

---

## 3. Railway Deployment

### 3.1 Railway Project Setup

**Step 1: Create Railway Project**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to existing project or create new
railway init
```

**Step 2: Configure railway.json**

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm run build"
  },
  "deploy": {
    "startCommand": "npm run start",
    "healthcheckPath": "/api/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

**Step 3: Configure nixpacks.toml**

```toml
# nixpacks.toml
[phases.setup]
nixPkgs = ['nodejs_20', 'python3']

[phases.install]
cmds = [
  'npm ci --legacy-peer-deps'
]

[phases.build]
cmds = [
  'npm run build'
]

[start]
cmd = 'npm run start'
```

### 3.2 Railway Service Configuration

**Service Settings:**

```yaml
Name: eclipselink-ai-prod
Region: us-west1
Plan: Hobby ($5/month base)

Build:
  - Root Directory: /
  - Builder: Nixpacks
  - Build Command: npm run build
  
Deploy:
  - Start Command: npm run start
  - Port: 3000
  - Health Check: /api/health
  - Health Check Timeout: 100s
  
Resources:
  - Memory: 512MB (auto-scale to 2GB)
  - CPU: Shared (auto-scale)
  - Disk: 1GB
```

**Scaling Configuration:**

```yaml
# Auto-scaling rules
Horizontal Scaling:
  - Min Instances: 1
  - Max Instances: 3
  - Scale up at: 70% CPU or 80% Memory
  - Scale down at: 30% CPU or 40% Memory
  - Cool down: 5 minutes

Vertical Scaling:
  - Start: 512MB RAM
  - Scale to: 2GB RAM max
  - Based on memory pressure
```

### 3.3 Custom Domains

**Configure Custom Domain:**

1. Go to Railway Project → Settings → Domains
2. Add custom domain: `app.eclipselink.ai`
3. Railway provides CNAME target
4. Configure in Cloudflare DNS (see section 4)

**SSL/TLS:**
- Railway automatically provisions SSL certificates
- Let's Encrypt certificates
- Auto-renewal

### 3.4 Deployment Commands

**Deploy from CLI:**

```bash
# Deploy current branch
railway up

# Deploy specific environment
railway up --environment production

# Deploy with specific service
railway up --service eclipselink-ai

# Rollback to previous deployment
railway rollback

# View logs
railway logs

# Open deployed URL
railway open
```

**Deploy from Git:**

```bash
# Railway auto-deploys on git push
git push origin main

# Manual trigger from Railway dashboard
# Settings → Deployments → Deploy
```

### 3.5 Health Check Endpoint

**Create Health Check:**

```typescript
// apps/web/src/app/api/health/route.ts

import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

export async function GET() {
  const checks = {
    timestamp: new Date().toISOString(),
    status: 'healthy',
    version: process.env.APP_VERSION || '1.0.0',
    checks: {
      database: 'unknown',
      redis: 'unknown',
      storage: 'unknown'
    }
  };

  try {
    // Check database connection
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    );
    
    const { error: dbError } = await supabase
      .from('users')
      .select('count')
      .limit(1)
      .single();
    
    checks.checks.database = dbError ? 'unhealthy' : 'healthy';
    
    // Check Redis (if configured)
    if (process.env.UPSTASH_REDIS_REST_URL) {
      // Simple ping to Redis
      checks.checks.redis = 'healthy'; // Implement actual check
    }
    
    // Check R2 Storage access
    checks.checks.storage = 'healthy'; // Implement actual check
    
    // Overall status
    const allHealthy = Object.values(checks.checks).every(
      status => status === 'healthy'
    );
    
    checks.status = allHealthy ? 'healthy' : 'degraded';
    
    return NextResponse.json(checks, {
      status: allHealthy ? 200 : 503
    });
    
  } catch (error) {
    return NextResponse.json(
      {
        ...checks,
        status: 'unhealthy',
        error: error.message
      },
      { status: 503 }
    );
  }
}
```

---

## 4. Cloudflare Setup

### 4.1 DNS Configuration

**Add DNS Records:**

```dns
# Main application
app.eclipselink.ai      CNAME   your-app.railway.app   (Proxied ☁️)

# API subdomain (if needed)
api.eclipselink.ai      CNAME   your-app.railway.app   (Proxied ☁️)

# Audio CDN
audio.eclipselink.ai    CNAME   your-bucket.r2.dev     (Proxied ☁️)

# Staging
staging.eclipselink.ai  CNAME   staging-app.railway.app (Proxied ☁️)

# Root domain redirect
eclipselink.ai          A       192.0.2.1              (Proxied ☁️)
www.eclipselink.ai      CNAME   eclipselink.ai         (Proxied ☁️)
```

### 4.2 Cloudflare R2 Storage Setup

**Create R2 Bucket:**

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create production bucket
wrangler r2 bucket create eclipselink-audio-prod

# Create staging bucket
wrangler r2 bucket create eclipselink-audio-staging

# List buckets
wrangler r2 bucket list
```

**Configure CORS:**

```json
// r2-cors-config.json
[
  {
    "AllowedOrigins": ["https://app.eclipselink.ai"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
    "AllowedHeaders": ["*"],
    "ExposeHeaders": ["ETag"],
    "MaxAgeSeconds": 3600
  }
]
```

**Apply CORS:**

```bash
wrangler r2 bucket cors put eclipselink-audio-prod --cors-file r2-cors-config.json
```

**Custom Domain for R2:**

1. Cloudflare Dashboard → R2 → Bucket Settings
2. Add custom domain: `audio.eclipselink.ai`
3. Cloudflare auto-configures DNS

### 4.3 R2 Integration Code

**R2 Client Setup:**

```typescript
// apps/backend/src/services/r2-storage.service.ts

import { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

export class R2StorageService {
  private client: S3Client;
  private bucketName: string;
  private publicUrl: string;
  
  constructor() {
    this.client = new S3Client({
      region: 'auto',
      endpoint: `https://${process.env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
      credentials: {
        accessKeyId: process.env.R2_ACCESS_KEY_ID!,
        secretAccessKey: process.env.R2_SECRET_ACCESS_KEY!
      }
    });
    
    this.bucketName = process.env.R2_BUCKET_NAME!;
    this.publicUrl = process.env.R2_PUBLIC_URL!;
  }
  
  async uploadAudio(
    file: Buffer,
    fileName: string,
    contentType: string
  ): Promise<string> {
    const key = `audio/${new Date().getFullYear()}/${fileName}`;
    
    await this.client.send(
      new PutObjectCommand({
        Bucket: this.bucketName,
        Key: key,
        Body: file,
        ContentType: contentType,
        CacheControl: 'max-age=31536000', // 1 year
        Metadata: {
          uploadedAt: new Date().toISOString()
        }
      })
    );
    
    return `${this.publicUrl}/${key}`;
  }
  
  async getPresignedDownloadUrl(key: string, expiresIn: number = 3600): Promise<string> {
    const command = new GetObjectCommand({
      Bucket: this.bucketName,
      Key: key
    });
    
    return getSignedUrl(this.client, command, { expiresIn });
  }
  
  async deleteAudio(key: string): Promise<void> {
    await this.client.send(
      new DeleteObjectCommand({
        Bucket: this.bucketName,
        Key: key
      })
    );
  }
}
```

### 4.4 CDN & Caching Configuration

**Cloudflare Page Rules:**

```
1. Cache Audio Files
   URL: audio.eclipselink.ai/*
   Settings:
   - Browser Cache TTL: 1 year
   - Edge Cache TTL: 1 month
   - Cache Level: Everything

2. Cache Static Assets
   URL: app.eclipselink.ai/_next/static/*
   Settings:
   - Browser Cache TTL: 1 year
   - Edge Cache TTL: 1 month

3. Bypass API Cache
   URL: app.eclipselink.ai/api/*
   Settings:
   - Cache Level: Bypass
```

**Security Headers:**

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

**Cloudflare Workers (Optional - Rate Limiting):**

```typescript
// cloudflare-worker-rate-limit.ts

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const ip = request.headers.get('CF-Connecting-IP');
    const key = `rate_limit:${ip}`;
    
    // Get current count
    const count = await env.KV.get(key);
    const current = count ? parseInt(count) : 0;
    
    // Check limit (100 requests per minute)
    if (current >= 100) {
      return new Response('Rate limit exceeded', {
        status: 429,
        headers: {
          'Retry-After': '60',
          'X-RateLimit-Limit': '100',
          'X-RateLimit-Remaining': '0'
        }
      });
    }
    
    // Increment counter
    await env.KV.put(key, (current + 1).toString(), {
      expirationTtl: 60 // 1 minute
    });
    
    // Forward request
    return fetch(request);
  }
};
```

---

## 5. Database Management

### 5.1 Supabase Setup

**Production Database Configuration:**

```yaml
Project: eclipselink-prod
Region: US East (Ohio)
Plan: Pro ($25/month)

Compute:
  - Dedicated CPU
  - 2GB RAM
  - 10GB Database size
  
Connection Pooling:
  - Mode: Transaction
  - Pool Size: 15
  - Connection Limit: 100
  
Backups:
  - Daily automated backups
  - 7-day retention
  - Point-in-time recovery (PITR)
```

### 5.2 Database Migrations

**Migration Strategy:**

```bash
# Create migration
npx supabase migration new add_handoff_version_tracking

# Apply migration to local
npx supabase db reset

# Apply migration to staging
npx supabase db push --db-url $STAGING_DATABASE_URL

# Apply migration to production
npx supabase db push --db-url $PROD_DATABASE_URL
```

**Migration Example:**

```sql
-- migrations/20251023_add_sbar_versioning.sql

BEGIN;

-- Add version tracking to sbar_reports
ALTER TABLE sbar_reports
ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1,
ADD COLUMN IF NOT EXISTS previous_version_id UUID REFERENCES sbar_reports(id),
ADD COLUMN IF NOT EXISTS is_latest BOOLEAN NOT NULL DEFAULT true,
ADD COLUMN IF NOT EXISTS changes_since_last_version JSONB;

-- Create index for version queries
CREATE INDEX IF NOT EXISTS idx_sbar_reports_version 
ON sbar_reports(handoff_id, version DESC);

-- Create index for latest versions
CREATE INDEX IF NOT EXISTS idx_sbar_reports_latest 
ON sbar_reports(handoff_id) 
WHERE is_latest = true;

-- Function to update is_latest flag
CREATE OR REPLACE FUNCTION update_sbar_latest_flag()
RETURNS TRIGGER AS $$
BEGIN
  -- Set all previous versions to not latest
  UPDATE sbar_reports
  SET is_latest = false
  WHERE handoff_id = NEW.handoff_id
    AND id != NEW.id;
  
  -- Ensure new version is latest
  NEW.is_latest := true;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to maintain is_latest flag
CREATE TRIGGER trigger_update_sbar_latest
BEFORE INSERT ON sbar_reports
FOR EACH ROW
EXECUTE FUNCTION update_sbar_latest_flag();

COMMIT;
```

### 5.3 Database Performance Optimization

**Connection Pooling:**

```typescript
// lib/db.ts
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
  ssl: process.env.NODE_ENV === 'production' ? {
    rejectUnauthorized: false
  } : false
});

export default pool;
```

**Query Optimization:**

```sql
-- Add missing indexes for common queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_handoffs_patient_created 
ON handoffs(patient_id, created_at DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_handoffs_staff_status 
ON handoffs(from_staff_id, status) 
WHERE status IN ('assigned', 'ready');

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_voice_recordings_status 
ON voice_recordings(status, created_at DESC) 
WHERE status != 'completed';

-- Analyze tables for query planner
ANALYZE handoffs;
ANALYZE sbar_reports;
ANALYZE voice_recordings;
```

### 5.4 Backup Strategy

**Automated Backups (Supabase):**
- Daily full backups at 2 AM UTC
- 7-day retention (Pro plan)
- Point-in-time recovery available

**Manual Backup:**

```bash
# Backup production database
pg_dump $PROD_DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup to S3/R2
pg_dump $PROD_DATABASE_URL | \
  gzip | \
  aws s3 cp - s3://eclipselink-backups/db_$(date +%Y%m%d).sql.gz

# Restore from backup
psql $DATABASE_URL < backup_20251023_020000.sql
```

**Backup Testing:**

```bash
# Monthly: Restore backup to staging and verify
pg_restore -d $STAGING_DATABASE_URL backup_latest.sql
# Run verification queries
psql $STAGING_DATABASE_URL -c "SELECT COUNT(*) FROM handoffs;"
psql $STAGING_DATABASE_URL -c "SELECT COUNT(*) FROM sbar_reports;"
```

---

## 6. CI/CD Pipeline

### 6.1 GitLab CI/CD Configuration

**.gitlab-ci.yml:**

```yaml
# .gitlab-ci.yml

stages:
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "20.x"

# Test stage
test:
  stage: test
  image: node:20
  cache:
    paths:
      - node_modules/
      - .next/cache/
  script:
    - npm ci
    - npm run lint
    - npm run type-check
    - npm run test
  only:
    - merge_requests
    - develop
    - main

# Build stage (verify build succeeds)
build:
  stage: build
  image: node:20
  cache:
    paths:
      - node_modules/
      - .next/cache/
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - .next/
    expire_in: 1 hour
  only:
    - develop
    - main

# Deploy to staging
deploy_staging:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
  script:
    - echo "Deploying to Railway staging..."
    - |
      curl -X POST \
        -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"environmentId": "'$RAILWAY_STAGING_ENV_ID'"}' \
        https://backboard.railway.app/graphql/v2
  environment:
    name: staging
    url: https://staging.eclipselink.ai
  only:
    - develop

# Deploy to production (manual approval required)
deploy_production:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
  script:
    - echo "Deploying to Railway production..."
    - |
      curl -X POST \
        -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"environmentId": "'$RAILWAY_PROD_ENV_ID'"}' \
        https://backboard.railway.app/graphql/v2
  environment:
    name: production
    url: https://app.eclipselink.ai
  when: manual
  only:
    - main
```

### 6.2 Pre-deployment Checks

**Pre-commit Hook (.husky/pre-commit):**

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

echo "🔍 Running pre-commit checks..."

# Run linter
npm run lint || {
  echo "❌ Linting failed. Fix errors before committing."
  exit 1
}

# Run type checking
npm run type-check || {
  echo "❌ Type checking failed. Fix TypeScript errors."
  exit 1
}

# Run tests
npm run test || {
  echo "❌ Tests failed. Fix failing tests before committing."
  exit 1
}

echo "✅ All pre-commit checks passed!"
```

**Pre-push Hook (.husky/pre-push):**

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

echo "🚀 Running pre-push checks..."

# Run full test suite
npm run test:coverage || {
  echo "❌ Test coverage below threshold."
  exit 1
}

# Check for console.logs in production code
if grep -r "console.log" apps/web/src --exclude-dir=node_modules; then
  echo "⚠️  Warning: console.log statements found in code"
  echo "Remove them or use proper logging before pushing to production"
fi

echo "✅ All pre-push checks passed!"
```

### 6.3 Deployment Verification

**Post-deployment Smoke Tests:**

```typescript
// scripts/smoke-test.ts

import axios from 'axios';

const STAGING_URL = 'https://staging.eclipselink.ai';
const PROD_URL = 'https://app.eclipselink.ai';

async function runSmokeTests(baseUrl: string) {
  console.log(`🧪 Running smoke tests against ${baseUrl}...`);
  
  const tests = [
    {
      name: 'Health check',
      test: async () => {
        const response = await axios.get(`${baseUrl}/api/health`);
        return response.status === 200 && response.data.status === 'healthy';
      }
    },
    {
      name: 'Authentication endpoint',
      test: async () => {
        const response = await axios.post(
          `${baseUrl}/api/v1/auth/login`,
          {
            email: 'test@example.com',
            password: 'invalid'
          },
          { validateStatus: () => true }
        );
        // Should return 401 for invalid credentials
        return response.status === 401;
      }
    },
    {
      name: 'API documentation',
      test: async () => {
        const response = await axios.get(`${baseUrl}/api/docs`);
        return response.status === 200;
      }
    }
  ];
  
  let passed = 0;
  let failed = 0;
  
  for (const test of tests) {
    try {
      const result = await test.test();
      if (result) {
        console.log(`  ✅ ${test.name}`);
        passed++;
      } else {
        console.log(`  ❌ ${test.name} - assertion failed`);
        failed++;
      }
    } catch (error) {
      console.log(`  ❌ ${test.name} - ${error.message}`);
      failed++;
    }
  }
  
  console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);
  
  if (failed > 0) {
    process.exit(1);
  }
}

// Run smoke tests
const environment = process.argv[2] || 'staging';
const url = environment === 'production' ? PROD_URL : STAGING_URL;

runSmokeTests(url).catch(error => {
  console.error('Smoke tests failed:', error);
  process.exit(1);
});
```

---

## 7. Monitoring & Logging

### 7.1 Logtail/Better Stack Setup

**Install Logtail:**

```bash
npm install @logtail/node @logtail/winston
```

**Configure Winston Logger:**

```typescript
// lib/logger.ts

import winston from 'winston';
import { Logtail } from '@logtail/node';
import { LogtailTransport } from '@logtail/winston';

const logtail = new Logtail(process.env.LOGTAIL_SOURCE_TOKEN!);

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'eclipselink-api',
    environment: process.env.NODE_ENV
  },
  transports: [
    // Console transport for local development
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    // Logtail transport for production
    new LogtailTransport(logtail)
  ]
});

export default logger;
```

**Usage in Application:**

```typescript
import logger from '@/lib/logger';

// Info logging
logger.info('Handoff created', {
  handoffId: 'h123',
  patientId: 'p456',
  staffId: 's789'
});

// Error logging
logger.error('SBAR generation failed', {
  handoffId: 'h123',
  error: error.message,
  stack: error.stack
});

// Warn logging
logger.warn('Low SBAR quality score', {
  sbarId: 's123',
  completenessScore: 0.65
});
```

### 7.2 Application Metrics

**Custom Metrics Service:**

```typescript
// services/metrics.service.ts

interface MetricData {
  name: string;
  value: number;
  tags?: Record<string, string>;
  timestamp?: Date;
}

class MetricsService {
  async track(metric: MetricData): Promise<void> {
    // Send to metrics backend (Railway metrics, or custom)
    logger.info('metric', {
      metric: metric.name,
      value: metric.value,
      tags: metric.tags,
      timestamp: metric.timestamp || new Date()
    });
    
    // Also store in database for historical analysis
    await db.metrics.create({
      data: {
        name: metric.name,
        value: metric.value,
        tags: metric.tags,
        timestamp: metric.timestamp || new Date()
      }
    });
  }
  
  async trackHandoffCreated(handoffId: string): Promise<void> {
    await this.track({
      name: 'handoff.created',
      value: 1,
      tags: { handoffId }
    });
  }
  
  async trackTranscriptionDuration(duration: number): Promise<void> {
    await this.track({
      name: 'transcription.duration',
      value: duration,
      tags: { unit: 'ms' }
    });
  }
  
  async trackSBARGenerationDuration(duration: number): Promise<void> {
    await this.track({
      name: 'sbar.generation.duration',
      value: duration,
      tags: { unit: 'ms' }
    });
  }
  
  async trackSBARQuality(score: number): Promise<void> {
    await this.track({
      name: 'sbar.quality_score',
      value: score,
      tags: { metric: 'completeness' }
    });
  }
}

export const metrics = new MetricsService();
```

### 7.3 Error Tracking

**Sentry Integration (Optional):**

```bash
npm install @sentry/nextjs
```

```typescript
// sentry.client.config.ts

import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
  beforeSend(event) {
    // Filter out sensitive data
    if (event.request) {
      delete event.request.cookies;
      delete event.request.headers;
    }
    return event;
  }
});
```

### 7.4 Alerts & Notifications

**Logtail Alerts:**

1. High error rate: > 10 errors/minute
2. SBAR generation failures: > 5 failures/hour
3. Database connection failures
4. Low health check score

**Slack Integration:**

```typescript
// lib/notifications.ts

import axios from 'axios';

export async function sendSlackAlert(
  message: string,
  severity: 'info' | 'warning' | 'critical'
): Promise<void> {
  const colors = {
    info: '#36a64f',
    warning: '#ff9900',
    critical: '#ff0000'
  };
  
  await axios.post(process.env.SLACK_WEBHOOK_URL!, {
    attachments: [
      {
        color: colors[severity],
        title: 'EclipseLink AI Alert',
        text: message,
        ts: Math.floor(Date.now() / 1000)
      }
    ]
  });
}
```

---

## 8. Backup & Disaster Recovery

### 8.1 Backup Schedule

**Daily Backups:**
- Database: 2 AM UTC (automated by Supabase)
- R2 Storage: Versioning enabled (30-day retention)
- Configuration: Weekly snapshots to Git

**Weekly Backups:**
- Full system snapshot
- Export to separate storage location
- Test restore procedure

**Monthly Backups:**
- Long-term archive
- Compliance documentation
- Security audit logs

### 8.2 Disaster Recovery Plan

**Recovery Time Objective (RTO):** 4 hours  
**Recovery Point Objective (RPO):** 24 hours

**Disaster Scenarios:**

**Scenario 1: Database Failure**
```bash
# 1. Identify issue
railway logs --service database

# 2. Restore from latest backup
supabase db restore --backup-id latest

# 3. Verify data integrity
psql $DATABASE_URL -c "SELECT COUNT(*) FROM handoffs;"

# 4. Resume application
railway up
```

**Scenario 2: Application Failure**
```bash
# 1. Rollback to previous deployment
railway rollback

# 2. If rollback fails, redeploy from Git
git checkout <last-known-good-commit>
railway up

# 3. Monitor health
railway logs --tail
```

**Scenario 3: Complete Infrastructure Failure**
```bash
# 1. Deploy to backup Railway account
railway link --project backup-eclipselink

# 2. Restore database from backup
pg_restore -d $NEW_DATABASE_URL backup_latest.sql

# 3. Update DNS to point to new deployment
# Update Cloudflare DNS records

# 4. Verify and monitor
./scripts/smoke-test.ts production
```

### 8.3 Data Retention Policy

**Production Data:**
- Active handoffs: Indefinite
- Completed handoffs: 7 years (HIPAA requirement)
- Audio recordings: 7 years (HIPAA requirement)
- SBAR reports: 7 years (HIPAA requirement)
- Audit logs: 7 years (HIPAA requirement)

**Development/Staging Data:**
- Cleared every 90 days
- No real PHI in staging/dev

---

## 9. Scaling Strategy

### 9.1 Current Capacity

**Baseline (Seed Stage):**
- Concurrent users: 50-100
- Handoffs/day: 100-200
- Database size: < 10GB
- Audio storage: < 50GB

**Railway Scaling:**
- Horizontal: 1-3 instances
- Vertical: 512MB-2GB RAM

### 9.2 Scaling Triggers

**Scale Up When:**
- CPU usage > 70% for 5 minutes
- Memory usage > 80% for 5 minutes
- Request latency > 2 seconds (p95)
- Database connections > 80% of pool

**Scale Down When:**
- CPU usage < 30% for 10 minutes
- Memory usage < 40% for 10 minutes
- Off-peak hours (2 AM - 6 AM)

### 9.3 Performance Optimization

**Database Query Optimization:**
```sql
-- Materialized view for dashboard stats
CREATE MATERIALIZED VIEW handoff_stats AS
SELECT 
  DATE(created_at) as date,
  status,
  COUNT(*) as count,
  AVG(EXTRACT(EPOCH FROM (updated_at - created_at))) as avg_duration
FROM handoffs
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at), status;

-- Refresh nightly
CREATE INDEX ON handoff_stats (date DESC);

-- Refresh command (in cron job)
REFRESH MATERIALIZED VIEW CONCURRENTLY handoff_stats;
```

**Caching Strategy:**

```typescript
// lib/cache.ts
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!
});

export async function getCachedOrFetch<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl: number = 3600
): Promise<T> {
  // Try cache first
  const cached = await redis.get(key);
  if (cached) {
    return cached as T;
  }
  
  // Fetch and cache
  const data = await fetcher();
  await redis.setex(key, ttl, JSON.stringify(data));
  
  return data;
}

// Usage
const patient = await getCachedOrFetch(
  `patient:${patientId}`,
  () => db.patients.findUnique({ where: { id: patientId } }),
  3600 // 1 hour TTL
);
```

### 9.4 Future Scaling Considerations

**Beyond Railway (Series A+):**
- **AWS ECS/Fargate** - Container orchestration
- **AWS RDS Aurora** - Managed PostgreSQL with read replicas
- **CloudFront + S3** - Global CDN for static assets
- **ElastiCache** - Redis clusters
- **Multi-region deployment** - US East, US West, EU

**Estimated Costs (1M handoffs/month):**
- Compute: $500-1000/month
- Database: $200-400/month
- Storage: $100-200/month
- AI Services: $600-1400/month
- **Total: $1,400-3,000/month**

---

## Summary

### ✅ Part 6 Complete!

**What Part 6 Covers:**

1. **Infrastructure Overview** - Complete architecture diagram
2. **Environment Configuration** - Dev, staging, production env vars
3. **Railway Deployment** - Configuration, scaling, health checks
4. **Cloudflare Setup** - DNS, R2 storage, CDN, caching
5. **Database Management** - Migrations, backups, optimization
6. **CI/CD Pipeline** - GitLab CI/CD, automated testing, deployments
7. **Monitoring & Logging** - Logtail, metrics, alerts
8. **Backup & Disaster Recovery** - RTO/RPO, recovery procedures
9. **Scaling Strategy** - Current capacity, triggers, future plans

### 🎯 Key Takeaways:

**Cost-Effective Infrastructure:**
- $95-225/month for seed stage
- Railway: $5-20/month (auto-scaling)
- Supabase: $25/month (Pro plan)
- Azure OpenAI: $60-140/month (1000 handoffs)

**Production-Ready DevOps:**
- Automated CI/CD with GitLab
- Zero-downtime deployments
- Health checks and monitoring
- 4-hour disaster recovery

**Scalability:**
- Current: 100-200 handoffs/day
- Future: 1M+ handoffs/month
- Clear scaling path to Series A

---

## 📊 Complete Documentation Progress:

| Part | Document | Size | Status |
|------|----------|------|--------|
| 1 | System Architecture | 57KB | ✅ |
| 2 | Repository Structure | 61KB | ✅ |
| 3 | Database Schema | 62KB | ✅ |
| 4A-D | API Specifications | 147KB | ✅ |
| 5 | Azure OpenAI Integration | 54KB | ✅ |
| 6 | **Deployment & DevOps** | **42KB** | ✅ **NEW!** |
| **TOTAL** | **9 Documents** | **423KB** | **6 of 9 Parts (67%)** |

**Remaining:**
- Part 7: Security & HIPAA Compliance
- Part 8: Testing Strategy
- Part 9: Product Roadmap & Scaling

---

**Ready for Part 7 (Security & HIPAA Compliance)?** 🔒

---

*EclipseLink AI™ is a product of Rohimaya Health AI*  
*© 2025 Rohimaya Health AI. All rights reserved.*
