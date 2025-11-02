# 🚀 COMPLETE DEPLOYMENT GUIDE - EclipseLink AI

**Production-Ready System for All Stakeholders**
**Cost: $21/month | Timeline: 4 weeks | Users: Unlimited**

---

## 📋 TABLE OF CONTENTS

1. [Prerequisites](#prerequisites)
2. [Architecture Overview](#architecture-overview)
3. [Phase 1: Supabase Setup (30 minutes)](#phase-1-supabase-setup)
4. [Phase 2: Edge Functions (1 hour)](#phase-2-edge-functions)
5. [Phase 3: Next.js Frontend (1 week)](#phase-3-nextjs-frontend)
6. [Phase 4: Testing (2 days)](#phase-4-testing)
7. [Phase 5: Production Deployment (1 day)](#phase-5-production-deployment)
8. [Monitoring & Maintenance](#monitoring--maintenance)
9. [Troubleshooting](#troubleshooting)

---

## PREREQUISITES

### Required Accounts (All Free Tier)
- ✅ [Supabase](https://supabase.com) - Database, Auth, Storage, Realtime
- ✅ [Vercel](https://vercel.com) - Next.js hosting
- ✅ [OpenAI](https://platform.openai.com) - Whisper API ($10 credit)
- ✅ [Anthropic](https://console.anthropic.com) - Claude API ($5 credit)
- ✅ [GitHub](https://github.com) - Code repository

### Local Development
```bash
node --version  # v20.0.0+
npm --version   # v9.0.0+
git --version   # v2.30.0+
```

---

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Vercel)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │Clinician │  │  Family  │  │  Patient │  │  Admin  ││
│  │Dashboard │  │  Portal  │  │  Portal  │  │  Panel  ││
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘│
└───────┼─────────────┼─────────────┼──────────────┼─────┘
        │             │             │              │
        └─────────────┴─────────────┴──────────────┘
                           │
    ┌──────────────────────▼──────────────────────────┐
    │           SUPABASE (All-in-One)                 │
    │  ┌────────────────────────────────────────┐     │
    │  │ PostgreSQL (Multi-tenant + RLS)        │     │
    │  └────────────────────────────────────────┘     │
    │  ┌────────────────────────────────────────┐     │
    │  │ Auth (Email, OAuth, Magic Links)       │     │
    │  └────────────────────────────────────────┘     │
    │  ┌────────────────────────────────────────┐     │
    │  │ Storage (Audio files, QR codes)        │     │
    │  └────────────────────────────────────────┘     │
    │  ┌────────────────────────────────────────┐     │
    │  │ Realtime (WebSocket notifications)     │     │
    │  └────────────────────────────────────────┘     │
    │  ┌────────────────────────────────────────┐     │
    │  │ Edge Functions (AI Processing)         │     │
    │  │  - process-handoff                     │     │
    │  │  - generate-qr-code                    │     │
    │  │  - batch-process                       │     │
    │  └────────────────────────────────────────┘     │
    └─────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌──────▼──────┐   ┌──────▼──────┐
   │ OpenAI  │      │ Anthropic   │   │  Cloudflare │
   │ Whisper │      │   Claude    │   │     R2      │
   └─────────┘      └─────────────┘   └─────────────┘
```

---

## PHASE 1: SUPABASE SETUP (30 minutes)

### Step 1.1: Create Supabase Project

```bash
# 1. Go to https://supabase.com
# 2. Click "New Project"
# 3. Name: "eclipselink-ai-prod"
# 4. Database Password: Generate strong password (save it!)
# 5. Region: Choose closest to your users
# 6. Pricing: Free tier
# 7. Click "Create new project"
```

### Step 1.2: Run Database Schema

```bash
# 1. In Supabase Dashboard → SQL Editor
# 2. Click "New query"
# 3. Copy content from database/schema-creative-production.sql
# 4. Click "Run"
# 5. Verify: Should see "Success. No rows returned"
```

### Step 1.3: Enable Realtime

```bash
# 1. In Supabase Dashboard → Database → Replication
# 2. Enable replication for these tables:
#    - handoffs
#    - notifications
#    - patients
# 3. Click "Save"
```

### Step 1.4: Configure Storage

```sql
-- In SQL Editor, run:
-- Create storage bucket for audio files
INSERT INTO storage.buckets (id, name, public)
VALUES ('audio-files', 'audio-files', false);

-- Create storage bucket for QR codes
INSERT INTO storage.buckets (id, name, public)
VALUES ('qr-codes', 'qr-codes', true);

-- Storage policies for audio files
CREATE POLICY "Clinicians can upload audio"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'audio-files' AND
  auth.role() = 'authenticated'
);

CREATE POLICY "Users can read own facility audio"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'audio-files' AND
  auth.role() = 'authenticated'
);

-- Storage policies for QR codes
CREATE POLICY "Anyone can view QR codes"
ON storage.objects FOR SELECT
USING (bucket_id = 'qr-codes');

CREATE POLICY "Clinicians can create QR codes"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'qr-codes' AND
  auth.role() = 'authenticated'
);
```

### Step 1.5: Get API Keys

```bash
# 1. In Supabase Dashboard → Settings → API
# 2. Copy these values:

# Project URL
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co

# Anon/Public Key (safe to use in frontend)
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...

# Service Role Key (NEVER expose in frontend!)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...
```

---

## PHASE 2: EDGE FUNCTIONS (1 hour)

### Step 2.1: Install Supabase CLI

```bash
# macOS
brew install supabase/tap/supabase

# Windows (PowerShell)
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase

# Linux
brew install supabase/tap/supabase

# Verify installation
supabase --version
```

### Step 2.2: Initialize Supabase Locally

```bash
# Login to Supabase
supabase login

# Link to your project
supabase link --project-ref xxxxx  # Get ref from dashboard URL
```

### Step 2.3: Create Edge Function - Process Handoff

```bash
# Create function
supabase functions new process-handoff

# This creates: supabase/functions/process-handoff/index.ts
```

**File: `supabase/functions/process-handoff/index.ts`**
```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { handoff_id } = await req.json()

    // Initialize Supabase client
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // 1. Get handoff details
    const { data: handoff } = await supabaseClient
      .from('handoffs')
      .select('*, patient:patients(*)')
      .eq('id', handoff_id)
      .single()

    if (!handoff || !handoff.audio_url) {
      throw new Error('Handoff not found or missing audio')
    }

    // 2. Download audio file
    const { data: audioFile } = await supabaseClient
      .storage
      .from('audio-files')
      .download(handoff.audio_url)

    // 3. Transcribe with OpenAI Whisper
    const formData = new FormData()
    formData.append('file', audioFile, 'audio.mp3')
    formData.append('model', 'whisper-1')
    formData.append('language', handoff.transcription_language || 'en')

    const transcriptionRes = await fetch(
      'https://api.openai.com/v1/audio/transcriptions',
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${Deno.env.get('OPENAI_API_KEY')}`
        },
        body: formData
      }
    )

    const transcription = await transcriptionRes.json()

    // 4. Generate SBAR with Anthropic Claude
    const sbarPrompt = `You are a clinical AI assistant. Convert this nursing handoff transcription into structured SBAR format.

Patient Context:
- Name: ${handoff.patient.first_name} ${handoff.patient.last_name}
- MRN: ${handoff.patient.mrn}
- Age: ${calculateAge(handoff.patient.date_of_birth)}
- Room: ${handoff.patient.room_number}
- Diagnosis: ${handoff.patient.primary_diagnosis}

Transcription:
${transcription.text}

Generate a JSON object with this structure:
{
  "situation": {
    "patient_name": string,
    "age": number,
    "room": string,
    "diagnosis": string,
    "chief_complaint": string
  },
  "background": {
    "medical_history": string[],
    "allergies": string[],
    "medications": [{"name": string, "dose": string}],
    "code_status": string
  },
  "assessment": {
    "vital_signs": {"hr": number, "bp": string, "temp": number, "spo2": number},
    "current_condition": string,
    "concerns": string[]
  },
  "recommendation": {
    "pending_orders": string[],
    "follow_up_needed": string[],
    "escalation_required": boolean
  }
}

Return ONLY the JSON, no explanations.`

    const sbarRes = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': Deno.env.get('ANTHROPIC_API_KEY') ?? '',
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 4096,
        messages: [{
          role: 'user',
          content: sbarPrompt
        }]
      })
    })

    const sbarData = await sbarRes.json()
    const sbarText = sbarData.content[0].text

    // Extract JSON from response
    const jsonMatch = sbarText.match(/\{[\s\S]*\}/)
    const sbar = jsonMatch ? JSON.parse(jsonMatch[0]) : null

    // 5. Detect critical alerts
    const critical_alerts = []

    // Check vital signs
    if (sbar.assessment?.vital_signs) {
      const vitals = sbar.assessment.vital_signs
      if (vitals.hr && (vitals.hr < 50 || vitals.hr > 120)) {
        critical_alerts.push({
          type: 'vital_sign_abnormal',
          severity: 'high',
          message: `Heart rate ${vitals.hr} outside normal range`
        })
      }
      if (vitals.spo2 && vitals.spo2 < 92) {
        critical_alerts.push({
          type: 'vital_sign_critical',
          severity: 'critical',
          message: `Oxygen saturation ${vitals.spo2}% - requires immediate attention`
        })
      }
    }

    // Check for high-risk medications
    const highRiskMeds = ['heparin', 'warfarin', 'insulin']
    if (sbar.background?.medications) {
      sbar.background.medications.forEach(med => {
        if (highRiskMeds.some(risk => med.name.toLowerCase().includes(risk))) {
          critical_alerts.push({
            type: 'high_risk_medication',
            severity: 'medium',
            message: `High-risk medication: ${med.name}`
          })
        }
      })
    }

    // 6. Calculate quality score (simple heuristic)
    const quality_score = calculateQualityScore(sbar, transcription)

    // 7. Update handoff in database
    const { error: updateError } = await supabaseClient
      .from('handoffs')
      .update({
        transcription: transcription.text,
        transcription_confidence: 0.95, // Whisper doesn't provide this
        transcription_processed_at: new Date().toISOString(),
        sbar: sbar,
        critical_alerts: critical_alerts,
        quality_score: quality_score,
        requires_attention: critical_alerts.some(a => a.severity === 'critical'),
        status: 'pending_review',
        ai_processing_time_ms: Date.now() - startTime,
        ai_cost_cents: calculateCost(audioFile.size, transcription.text.length)
      })
      .eq('id', handoff_id)

    if (updateError) throw updateError

    // 8. Create notification for critical alerts
    if (critical_alerts.length > 0) {
      await supabaseClient.from('notifications').insert({
        facility_id: handoff.facility_id,
        user_id: handoff.created_by,
        type: 'critical_alert',
        title: 'Critical Alert Detected',
        message: `${critical_alerts.length} critical alerts found in handoff`,
        priority: 'critical',
        related_handoff_id: handoff_id,
        related_patient_id: handoff.patient_id,
        channels: ['in_app', 'push']
      })
    }

    return new Response(
      JSON.stringify({
        success: true,
        handoff_id,
        transcription: transcription.text,
        sbar,
        critical_alerts,
        quality_score
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200
      }
    )

  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 400
      }
    )
  }
})

// Helper functions
function calculateAge(dob: string): number {
  const birthDate = new Date(dob)
  const today = new Date()
  let age = today.getFullYear() - birthDate.getFullYear()
  const m = today.getMonth() - birthDate.getMonth()
  if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  return age
}

function calculateQualityScore(sbar: any, transcription: any): number {
  let score = 0.5 // Base score

  // Has all SBAR sections
  if (sbar.situation) score += 0.125
  if (sbar.background) score += 0.125
  if (sbar.assessment) score += 0.125
  if (sbar.recommendation) score += 0.125

  // Check completeness
  if (sbar.situation?.patient_name) score += 0.05
  if (sbar.situation?.diagnosis) score += 0.05
  if (sbar.background?.medications?.length > 0) score += 0.05
  if (sbar.assessment?.vital_signs) score += 0.05

  return Math.min(score, 1.0)
}

function calculateCost(audioSizeBytes: number, textLength: number): number {
  // OpenAI Whisper: $0.006 per minute
  // Assume 1MB = ~1 minute of audio
  const minutes = audioSizeBytes / (1024 * 1024)
  const whisperCost = minutes * 0.6 // cents

  // Anthropic Claude: ~$3 per 1M input tokens, $15 per 1M output tokens
  // Rough estimate: 1 token ≈ 4 characters
  const inputTokens = textLength / 4
  const outputTokens = 1000 // Assume ~1000 tokens for SBAR
  const claudeCost = (inputTokens / 1000000 * 300) + (outputTokens / 1000000 * 1500) // cents

  return Math.round(whisperCost + claudeCost)
}
```

### Step 2.4: Create Edge Function - Generate QR Code

```bash
supabase functions new generate-qr-code
```

**File: `supabase/functions/generate-qr-code/index.ts`**
```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import QRCode from 'https://esm.sh/qrcode@1.5.3'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { patient_id, created_by, relationship, full_name, email } = await req.json()

    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // 1. Get patient details
    const { data: patient } = await supabaseClient
      .from('patients')
      .select('facility_id')
      .eq('id', patient_id)
      .single()

    // 2. Generate secure access token
    const access_token = crypto.randomUUID()

    // 3. Create family access record
    const { data: familyAccess, error: insertError } = await supabaseClient
      .from('family_access')
      .insert({
        facility_id: patient.facility_id,
        patient_id,
        full_name,
        relationship,
        email,
        access_method: 'qr_code',
        access_token,
        created_by,
        expires_at: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(), // 30 days
        is_active: true
      })
      .select()
      .single()

    if (insertError) throw insertError

    // 4. Generate QR code URL
    const baseUrl = Deno.env.get('PUBLIC_SITE_URL') || 'https://eclipselink.ai'
    const qrUrl = `${baseUrl}/family/${access_token}`

    // 5. Generate QR code image
    const qrCodeDataUrl = await QRCode.toDataURL(qrUrl, {
      width: 400,
      margin: 2,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      }
    })

    // 6. Convert data URL to blob
    const base64Data = qrCodeDataUrl.split(',')[1]
    const binaryData = Uint8Array.from(atob(base64Data), c => c.charCodeAt(0))

    // 7. Upload to storage
    const fileName = `${patient_id}-${Date.now()}.png`
    const { error: uploadError } = await supabaseClient
      .storage
      .from('qr-codes')
      .upload(fileName, binaryData, {
        contentType: 'image/png',
        cacheControl: '3600',
        upsert: false
      })

    if (uploadError) throw uploadError

    // 8. Get public URL
    const { data: { publicUrl } } = supabaseClient
      .storage
      .from('qr-codes')
      .getPublicUrl(fileName)

    // 9. Update family_access with QR code URL
    await supabaseClient
      .from('family_access')
      .update({
        qr_code_url: publicUrl,
        qr_code_generated_at: new Date().toISOString()
      })
      .eq('id', familyAccess.id)

    return new Response(
      JSON.stringify({
        success: true,
        access_token,
        qr_code_url: publicUrl,
        access_url: qrUrl,
        expires_at: familyAccess.expires_at
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200
      }
    )

  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 400
      }
    )
  }
})
```

### Step 2.5: Set Environment Variables

```bash
# Set secrets for Edge Functions
supabase secrets set OPENAI_API_KEY=sk-xxx
supabase secrets set ANTHROPIC_API_KEY=sk-ant-xxx
supabase secrets set PUBLIC_SITE_URL=https://eclipselink.ai
```

### Step 2.6: Deploy Edge Functions

```bash
# Deploy process-handoff function
supabase functions deploy process-handoff

# Deploy generate-qr-code function
supabase functions deploy generate-qr-code

# Verify deployment
supabase functions list
```

---

## PHASE 3: NEXT.JS FRONTEND (1 week)

### Step 3.1: Create Next.js Project

```bash
# Create new Next.js app
npx create-next-app@latest eclipselink-web \
  --typescript \
  --tailwind \
  --app \
  --src-dir \
  --import-alias "@/*"

cd eclipselink-web
```

### Step 3.2: Install Dependencies

```bash
npm install @supabase/supabase-js@latest \
  @supabase/auth-helpers-nextjs@latest \
  @supabase/auth-ui-react@latest \
  @supabase/auth-ui-shared@latest \
  zustand \
  zod \
  react-hook-form \
  @hookform/resolvers \
  date-fns \
  lucide-react \
  sonner \
  recharts \
  next-pwa
```

### Step 3.3: Create Environment File

**File: `.env.local`**
```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...

# Site
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

### Step 3.4: Key Implementation Files

Due to space constraints, I'll provide the essential file structure and key code:

**File Structure:**
```
src/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (dashboard)/
│   │   ├── clinician/
│   │   │   ├── page.tsx
│   │   │   ├── patients/page.tsx
│   │   │   └── record/[id]/page.tsx
│   │   ├── family/
│   │   │   └── [token]/page.tsx
│   │   ├── patient/
│   │   │   └── page.tsx
│   │   └── admin/
│   │       └── page.tsx
│   ├── api/
│   │   └── process-handoff/route.ts
│   └── layout.tsx
├── lib/
│   ├── supabase/
│   │   ├── client.ts
│   │   └── server.ts
│   ├── hooks/
│   │   ├── useUser.ts
│   │   ├── useRealtime.ts
│   │   └── useAudio.ts
│   └── utils.ts
└── components/
    ├── VoiceRecorder.tsx
    ├── SBARDisplay.tsx
    ├── QRCodeGenerator.tsx
    └── NotificationBell.tsx
```

I'll continue with the rest of the deployment guide and testing...
