# EclipseLink AI™ - Part 5: Azure OpenAI Integration Guide

**Document Version:** 1.0  
**Last Updated:** October 23, 2025  
**Product:** EclipseLink AI™ Clinical Handoff System  
**Company:** Rohimaya Health AI  
**Founders:** Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO)

---

## Table of Contents

1. [Azure OpenAI Overview](#azure-openai-overview)
2. [Service Setup & Configuration](#service-setup-configuration)
3. [Whisper API Integration (Voice-to-Text)](#whisper-api-integration)
4. [GPT-4 Integration (SBAR Generation)](#gpt-4-integration)
5. [Prompt Engineering Strategies](#prompt-engineering-strategies)
6. [Error Handling & Retry Logic](#error-handling-retry-logic)
7. [Cost Optimization](#cost-optimization)
8. [Quality Monitoring](#quality-monitoring)
9. [Testing & Validation](#testing-validation)

---

## 1. Azure OpenAI Overview

### 1.1 Why Azure OpenAI?

**Key Benefits:**
- **Healthcare Compliance:** Microsoft's commitment to HIPAA/HITECH
- **Enterprise SLA:** 99.9% uptime guarantee
- **Data Privacy:** Customer data not used for training
- **Regional Deployment:** Deploy in US regions for data sovereignty
- **Business Associate Agreement (BAA):** Available for HIPAA compliance
- **Enterprise Support:** 24/7 technical support

**EclipseLink AI Uses:**
1. **Whisper API** - Voice-to-text transcription
2. **GPT-4** - SBAR report generation

### 1.2 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ECLIPSELINK AI BACKEND                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ 1. Voice Recording Upload
                      │
                      ▼
            ┌──────────────────┐
            │  Cloudflare R2   │
            │  Audio Storage   │
            └────────┬─────────┘
                     │
                     │ 2. Fetch Audio URL
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│                  AZURE OPENAI SERVICE                       │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              WHISPER API                              │ │
│  │  Model: whisper-1                                     │ │
│  │  Input: Audio file (webm, mp3, wav, m4a)            │ │
│  │  Output: Transcribed text with timestamps            │ │
│  │  Processing Time: ~10-30 seconds                     │ │
│  └────────────────────┬─────────────────────────────────┘ │
│                       │                                    │
│                       │ 3. Transcription Complete          │
│                       │                                    │
│                       ▼                                    │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              GPT-4 API                                │ │
│  │  Model: gpt-4 (or gpt-4-turbo)                       │ │
│  │  Input: Transcribed text + System Prompt             │ │
│  │         + Patient Context + Previous SBAR (if update) │ │
│  │  Output: Structured SBAR report (JSON)               │ │
│  │  Processing Time: ~15-45 seconds                     │ │
│  └────────────────────┬─────────────────────────────────┘ │
└────────────────────────┼────────────────────────────────────┘
                         │
                         │ 4. SBAR Generated
                         │
                         ▼
            ┌──────────────────────┐
            │   Supabase Database   │
            │   Store SBAR Report   │
            └──────────────────────┘
```

### 1.3 Service Costs (Estimated)

**Whisper API:**
- **Price:** $0.006 per minute of audio
- **Typical Duration:** 2-5 minutes per handoff
- **Cost per Handoff:** $0.012 - $0.030

**GPT-4 API:**
- **Price:** ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- **Typical Input:** 500-1500 tokens (transcription + context)
- **Typical Output:** 500-1000 tokens (SBAR)
- **Cost per Handoff:** $0.045 - $0.105

**Total AI Cost per Handoff:** $0.06 - $0.14

**Monthly Estimates (1000 handoffs/month):**
- AI Costs: $60 - $140/month
- Very affordable at seed stage!

---

## 2. Service Setup & Configuration

### 2.1 Azure OpenAI Resource Creation

**Step 1: Create Azure OpenAI Resource**

```bash
# Azure CLI commands
az login

# Create resource group
az group create \
  --name eclipselink-ai-rg \
  --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create \
  --name eclipselink-openai \
  --resource-group eclipselink-ai-rg \
  --kind OpenAI \
  --sku S0 \
  --location eastus \
  --yes
```

**Step 2: Deploy Models**

Via Azure Portal:
1. Navigate to Azure OpenAI Studio
2. Go to "Deployments"
3. Deploy Whisper-1 model
4. Deploy GPT-4 or GPT-4-Turbo model

**Model Deployment Names:**
- Whisper: `whisper-deployment-1`
- GPT-4: `gpt4-deployment-1`

### 2.2 Environment Configuration

**.env.local (Development):**
```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://eclipselink-openai.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Whisper Deployment
AZURE_OPENAI_WHISPER_DEPLOYMENT=whisper-deployment-1

# GPT-4 Deployment
AZURE_OPENAI_GPT4_DEPLOYMENT=gpt4-deployment-1

# Rate Limiting
AZURE_OPENAI_MAX_RETRIES=3
AZURE_OPENAI_TIMEOUT_MS=120000
```

**.env.production (Production):**
```bash
# Use Azure Key Vault for production secrets
AZURE_KEY_VAULT_URL=https://eclipselink-kv.vault.azure.net/
# Secrets retrieved at runtime
```

### 2.3 SDK Installation

**Backend Package.json:**
```json
{
  "dependencies": {
    "@azure/openai": "^1.0.0-beta.12",
    "openai": "^4.20.0",
    "form-data": "^4.0.0"
  }
}
```

**Install:**
```bash
npm install @azure/openai openai form-data
```

---

## 3. Whisper API Integration (Voice-to-Text)

### 3.1 Whisper Service Configuration

**Create Azure OpenAI Client:**

```typescript
// apps/backend/src/services/azure-openai.service.ts
import { OpenAIClient, AzureKeyCredential } from '@azure/openai';
import FormData from 'form-data';
import fs from 'fs';

export class AzureOpenAIService {
  private client: OpenAIClient;
  private whisperDeployment: string;
  private gpt4Deployment: string;
  
  constructor() {
    this.client = new OpenAIClient(
      process.env.AZURE_OPENAI_ENDPOINT!,
      new AzureKeyCredential(process.env.AZURE_OPENAI_API_KEY!)
    );
    
    this.whisperDeployment = process.env.AZURE_OPENAI_WHISPER_DEPLOYMENT!;
    this.gpt4Deployment = process.env.AZURE_OPENAI_GPT4_DEPLOYMENT!;
  }
  
  // Whisper transcription methods
  // GPT-4 generation methods
}
```

### 3.2 Audio Transcription Implementation

**Basic Transcription:**

```typescript
// apps/backend/src/services/azure-openai.service.ts

interface TranscriptionResult {
  text: string;
  duration: number;
  confidence: number;
  language: string;
  segments?: TranscriptionSegment[];
}

interface TranscriptionSegment {
  id: number;
  start: number;
  end: number;
  text: string;
}

async transcribeAudio(
  audioFilePath: string,
  options?: {
    language?: string;
    prompt?: string;
    temperature?: number;
  }
): Promise<TranscriptionResult> {
  const startTime = Date.now();
  
  try {
    // Read audio file
    const audioBuffer = fs.readFileSync(audioFilePath);
    
    // Call Whisper API
    const result = await this.client.getAudioTranscription(
      this.whisperDeployment,
      audioBuffer,
      {
        language: options?.language || 'en',
        prompt: options?.prompt,
        temperature: options?.temperature || 0,
        responseFormat: 'verbose_json' // Get detailed output with timestamps
      }
    );
    
    const duration = Date.now() - startTime;
    
    // Parse result
    return {
      text: result.text,
      duration: duration,
      confidence: this.calculateConfidence(result),
      language: result.language || 'en',
      segments: result.segments?.map((seg: any) => ({
        id: seg.id,
        start: seg.start,
        end: seg.end,
        text: seg.text
      }))
    };
    
  } catch (error) {
    console.error('Whisper transcription error:', error);
    throw new TranscriptionError(
      'Failed to transcribe audio',
      error
    );
  }
}

private calculateConfidence(result: any): number {
  // Whisper doesn't provide direct confidence scores
  // Estimate based on presence of [inaudible] markers and segment count
  if (!result.text) return 0;
  
  const hasInaudible = result.text.toLowerCase().includes('[inaudible]');
  const textLength = result.text.length;
  const segmentCount = result.segments?.length || 0;
  
  // Simple heuristic scoring
  let confidence = 0.85; // Base confidence
  
  if (hasInaudible) confidence -= 0.15;
  if (textLength < 100) confidence -= 0.10;
  if (segmentCount < 5) confidence -= 0.05;
  
  return Math.max(0.5, Math.min(1.0, confidence));
}
```

### 3.3 Audio Quality Validation

**Pre-transcription Validation:**

```typescript
// apps/backend/src/services/audio-validator.service.ts

interface AudioValidationResult {
  isValid: boolean;
  quality: 'excellent' | 'good' | 'acceptable' | 'poor';
  issues: string[];
  metadata: {
    duration: number;
    fileSize: number;
    format: string;
    sampleRate?: number;
    bitRate?: number;
  };
}

async validateAudio(filePath: string): Promise<AudioValidationResult> {
  const stats = fs.statSync(filePath);
  const issues: string[] = [];
  
  // Check file size
  const fileSize = stats.size;
  const maxSize = 10 * 1024 * 1024; // 10MB
  
  if (fileSize > maxSize) {
    issues.push(`File size ${fileSize} exceeds maximum ${maxSize}`);
    return {
      isValid: false,
      quality: 'poor',
      issues,
      metadata: { duration: 0, fileSize, format: 'unknown' }
    };
  }
  
  // Minimum size check (30 seconds at low quality ~ 100KB)
  if (fileSize < 100000) {
    issues.push('Audio file too short or corrupted');
  }
  
  // Use ffprobe for detailed audio analysis (optional)
  try {
    const metadata = await this.getAudioMetadata(filePath);
    
    // Check duration
    if (metadata.duration < 30) {
      issues.push('Recording duration less than 30 seconds');
    }
    
    if (metadata.duration > 600) {
      issues.push('Recording duration exceeds 10 minutes');
    }
    
    // Check sample rate (prefer 16kHz or higher)
    if (metadata.sampleRate && metadata.sampleRate < 16000) {
      issues.push('Low sample rate may affect transcription quality');
    }
    
    // Determine quality
    let quality: AudioValidationResult['quality'] = 'good';
    
    if (issues.length === 0 && metadata.sampleRate >= 44100) {
      quality = 'excellent';
    } else if (issues.length > 2) {
      quality = 'poor';
    } else if (issues.length > 0) {
      quality = 'acceptable';
    }
    
    return {
      isValid: issues.length < 3,
      quality,
      issues,
      metadata: {
        duration: metadata.duration,
        fileSize,
        format: metadata.format,
        sampleRate: metadata.sampleRate,
        bitRate: metadata.bitRate
      }
    };
    
  } catch (error) {
    console.error('Audio validation error:', error);
    return {
      isValid: false,
      quality: 'poor',
      issues: ['Unable to validate audio file'],
      metadata: { duration: 0, fileSize, format: 'unknown' }
    };
  }
}

private async getAudioMetadata(filePath: string): Promise<any> {
  // Use ffprobe or similar tool
  // For simplicity, returning mock data
  return {
    duration: 120, // seconds
    format: 'webm',
    sampleRate: 48000,
    bitRate: 128000
  };
}
```

### 3.4 Complete Transcription Workflow

**Voice Processing Service:**

```typescript
// apps/backend/src/services/voice-processing.service.ts

interface ProcessVoiceResult {
  recordingId: string;
  transcription: TranscriptionResult;
  processingTime: number;
  status: 'completed' | 'failed';
  error?: string;
}

async processVoiceRecording(
  recordingId: string,
  audioFilePath: string
): Promise<ProcessVoiceResult> {
  const startTime = Date.now();
  
  try {
    // Step 1: Update status to 'transcribing'
    await this.updateRecordingStatus(recordingId, 'transcribing');
    
    // Step 2: Validate audio quality
    const validation = await this.audioValidator.validateAudio(audioFilePath);
    
    if (!validation.isValid) {
      throw new Error(`Audio validation failed: ${validation.issues.join(', ')}`);
    }
    
    // Log audio quality
    await this.logAudioQuality(recordingId, validation);
    
    // Step 3: Transcribe with Whisper
    const transcription = await this.azureOpenAI.transcribeAudio(
      audioFilePath,
      {
        language: 'en',
        // Optional: Provide medical terminology hints
        prompt: 'This is a clinical handoff recording discussing patient care, medications, vital signs, and treatment plans.'
      }
    );
    
    // Step 4: Store transcription
    await this.storeTranscription(recordingId, transcription);
    
    // Step 5: Update status to 'transcribed'
    await this.updateRecordingStatus(recordingId, 'transcribed');
    
    const processingTime = Date.now() - startTime;
    
    // Log metrics
    await this.logProcessingMetrics(recordingId, {
      transcriptionDuration: processingTime,
      wordCount: transcription.text.split(' ').length,
      confidence: transcription.confidence
    });
    
    return {
      recordingId,
      transcription,
      processingTime,
      status: 'completed'
    };
    
  } catch (error) {
    console.error('Voice processing error:', error);
    
    // Update status to 'failed'
    await this.updateRecordingStatus(recordingId, 'failed', error.message);
    
    return {
      recordingId,
      transcription: null as any,
      processingTime: Date.now() - startTime,
      status: 'failed',
      error: error.message
    };
  }
}
```

---

## 4. GPT-4 Integration (SBAR Generation)

### 4.1 GPT-4 Configuration

**Base GPT-4 Service:**

```typescript
// apps/backend/src/services/gpt4.service.ts

interface GPT4CompletionOptions {
  temperature?: number;
  maxTokens?: number;
  topP?: number;
  frequencyPenalty?: number;
  presencePenalty?: number;
}

async generateCompletion(
  messages: Array<{ role: string; content: string }>,
  options: GPT4CompletionOptions = {}
): Promise<string> {
  try {
    const response = await this.client.getChatCompletions(
      this.gpt4Deployment,
      messages,
      {
        temperature: options.temperature ?? 0.7,
        maxTokens: options.maxTokens ?? 2000,
        topP: options.topP ?? 0.95,
        frequencyPenalty: options.frequencyPenalty ?? 0,
        presencePenalty: options.presencePenalty ?? 0
      }
    );
    
    if (!response.choices || response.choices.length === 0) {
      throw new Error('No completion generated');
    }
    
    return response.choices[0].message?.content || '';
    
  } catch (error) {
    console.error('GPT-4 completion error:', error);
    throw new GPT4Error('Failed to generate completion', error);
  }
}
```

### 4.2 SBAR Generation - Initial Handoff

**Initial Handoff System Prompt:**

```typescript
const INITIAL_HANDOFF_SYSTEM_PROMPT = `You are a clinical documentation specialist creating SBAR (Situation, Background, Assessment, Recommendation) reports for healthcare handoffs. You follow the I-PASS framework and Joint Commission standards.

Your task is to generate a comprehensive SBAR report from a clinical handoff transcription. This is an INITIAL handoff (admission or first documentation), so provide complete information in all sections.

OUTPUT FORMAT (JSON):
{
  "situation": "Current patient status, chief complaint, vital signs, and immediate concerns",
  "background": "Relevant medical history, medications, allergies, social history",
  "assessment": "Clinical findings, lab results, current condition assessment",
  "recommendation": "Treatment plan, follow-up needs, pending tasks",
  "currentStatus": "Brief status summary",
  "medications": [{"name": "...", "dose": "...", "frequency": "...", "route": "..."}],
  "allergies": [{"allergen": "...", "reaction": "...", "severity": "..."}],
  "vitalSigns": {"temperature": 0, "bpSystolic": 0, "bpDiastolic": 0, "heartRate": 0, "respiratoryRate": 0, "oxygenSaturation": 0},
  "pendingTasks": ["task 1", "task 2"]
}

GUIDELINES:
- Extract ALL relevant clinical information
- Use clear, professional medical language
- Include specific measurements with units
- Organize information logically
- Flag critical information
- Be thorough - this is the baseline for future updates
- Follow I-PASS framework: Illness severity, Patient summary, Action list, Situation awareness, Synthesis by receiver
- Ensure Joint Commission compliance
`;
```

**Initial Handoff Generation:**

```typescript
// apps/backend/src/services/sbar-generation.service.ts

interface GenerateSBARInput {
  transcription: string;
  patientContext: PatientContext;
  handoffType: string;
  isInitial: boolean;
  previousSBAR?: SBARReport;
}

interface PatientContext {
  id: string;
  firstName: string;
  lastName: string;
  mrn: string;
  dateOfBirth: string;
  gender: string;
  admissionDate?: string;
  roomNumber?: string;
  knownAllergies?: string[];
  knownMedications?: string[];
}

async generateInitialSBAR(
  input: GenerateSBARInput
): Promise<SBARReport> {
  const { transcription, patientContext } = input;
  
  // Build user message with context
  const userMessage = `
PATIENT INFORMATION:
- Name: ${patientContext.firstName} ${patientContext.lastName}
- MRN: ${patientContext.mrn}
- DOB: ${patientContext.dateOfBirth}
- Gender: ${patientContext.gender}
- Room: ${patientContext.roomNumber || 'Not assigned'}
${patientContext.knownAllergies?.length ? `- Known Allergies: ${patientContext.knownAllergies.join(', ')}` : ''}

HANDOFF TRANSCRIPTION:
${transcription}

Generate a comprehensive SBAR report from this initial clinical handoff.
`;

  try {
    const messages = [
      { role: 'system', content: INITIAL_HANDOFF_SYSTEM_PROMPT },
      { role: 'user', content: userMessage }
    ];
    
    const completion = await this.gpt4Service.generateCompletion(
      messages,
      {
        temperature: 0.3, // Lower for consistency
        maxTokens: 2500
      }
    );
    
    // Parse JSON response
    const sbarData = this.parseSBARResponse(completion);
    
    // Validate completeness
    const validation = this.validateSBAR(sbarData, true);
    
    if (!validation.isValid) {
      throw new Error(`SBAR validation failed: ${validation.errors.join(', ')}`);
    }
    
    return {
      ...sbarData,
      version: 1,
      isInitial: true,
      previousVersionId: null,
      completenessScore: validation.completenessScore,
      readabilityScore: this.calculateReadabilityScore(sbarData)
    };
    
  } catch (error) {
    console.error('Initial SBAR generation error:', error);
    throw new SBARGenerationError('Failed to generate initial SBAR', error);
  }
}
```

### 4.3 SBAR Generation - Update Handoff

**Update Handoff System Prompt:**

```typescript
const UPDATE_HANDOFF_SYSTEM_PROMPT = `You are a clinical documentation specialist updating SBAR (Situation, Background, Assessment, Recommendation) reports for healthcare handoffs.

Your task is to generate an UPDATED SBAR report that captures CHANGES since the previous handoff. You will receive:
1. The current handoff transcription (describing changes)
2. The previous SBAR report (baseline)

OUTPUT FORMAT (JSON):
{
  "situation": "Updated current status - highlight what has CHANGED",
  "background": "Use '[Stable - see v{N}]' if unchanged, otherwise update",
  "assessment": "Updated clinical findings - emphasize changes",
  "recommendation": "Updated care plan - note what's new or modified",
  "currentStatus": "Brief current status",
  "medications": [/* only if changed */],
  "allergies": [/* only if new allergies discovered */],
  "vitalSigns": {/* current vital signs */},
  "pendingTasks": [/* current pending tasks */],
  "changesSinceLastVersion": [
    {"section": "situation", "type": "update", "previousValue": "...", "newValue": "...", "field": "..."},
    {"section": "assessment", "type": "addition", "newValue": "...", "field": "..."}
  ]
}

GUIDELINES:
- Focus on CHANGES and UPDATES - don't repeat stable information
- Use "[Stable - see vN]" to reference unchanged sections
- Clearly document what has changed
- Maintain continuity with previous version
- Track specific changes in changesSinceLastVersion array
- Types of changes: "update", "addition", "removal", "unchanged"
`;
```

**Update Handoff Generation:**

```typescript
async generateUpdateSBAR(
  input: GenerateSBARInput
): Promise<SBARReport> {
  const { transcription, patientContext, previousSBAR } = input;
  
  if (!previousSBAR) {
    throw new Error('Previous SBAR required for update handoff');
  }
  
  // Build user message with context AND previous SBAR
  const userMessage = `
PATIENT INFORMATION:
- Name: ${patientContext.firstName} ${patientContext.lastName}
- MRN: ${patientContext.mrn}

PREVIOUS SBAR (Version ${previousSBAR.version}):
---
SITUATION: ${previousSBAR.situation}

BACKGROUND: ${previousSBAR.background}

ASSESSMENT: ${previousSBAR.assessment}

RECOMMENDATION: ${previousSBAR.recommendation}
---

CURRENT HANDOFF TRANSCRIPTION (describing changes):
${transcription}

Generate an updated SBAR report that captures the changes since the previous version.
Focus on what has changed - use "[Stable - see v${previousSBAR.version}]" for unchanged sections.
`;

  try {
    const messages = [
      { role: 'system', content: UPDATE_HANDOFF_SYSTEM_PROMPT },
      { role: 'user', content: userMessage }
    ];
    
    const completion = await this.gpt4Service.generateCompletion(
      messages,
      {
        temperature: 0.3,
        maxTokens: 2000
      }
    );
    
    // Parse JSON response
    const sbarData = this.parseSBARResponse(completion);
    
    // Merge stable sections from previous version
    const mergedSBAR = this.mergeWithPrevious(sbarData, previousSBAR);
    
    // Validate
    const validation = this.validateSBAR(mergedSBAR, false);
    
    if (!validation.isValid) {
      throw new Error(`SBAR validation failed: ${validation.errors.join(', ')}`);
    }
    
    return {
      ...mergedSBAR,
      version: previousSBAR.version + 1,
      isInitial: false,
      previousVersionId: previousSBAR.id,
      completenessScore: validation.completenessScore,
      readabilityScore: this.calculateReadabilityScore(mergedSBAR)
    };
    
  } catch (error) {
    console.error('Update SBAR generation error:', error);
    throw new SBARGenerationError('Failed to generate update SBAR', error);
  }
}

private mergeWithPrevious(
  currentSBAR: Partial<SBARReport>,
  previousSBAR: SBARReport
): SBARReport {
  // Replace "[Stable - see vN]" markers with actual content from previous version
  const merged = { ...currentSBAR };
  
  const stablePattern = /\[Stable - see v\d+\]/i;
  
  if (merged.situation && stablePattern.test(merged.situation)) {
    merged.situation = previousSBAR.situation;
  }
  
  if (merged.background && stablePattern.test(merged.background)) {
    merged.background = previousSBAR.background;
  }
  
  if (merged.assessment && stablePattern.test(merged.assessment)) {
    merged.assessment = previousSBAR.assessment;
  }
  
  if (merged.recommendation && stablePattern.test(merged.recommendation)) {
    merged.recommendation = previousSBAR.recommendation;
  }
  
  // Merge medications and allergies if not provided
  if (!merged.medications || merged.medications.length === 0) {
    merged.medications = previousSBAR.medications;
  }
  
  if (!merged.allergies || merged.allergies.length === 0) {
    merged.allergies = previousSBAR.allergies;
  }
  
  return merged as SBARReport;
}
```

### 4.4 Response Parsing & Validation

```typescript
private parseSBARResponse(completion: string): Partial<SBARReport> {
  try {
    // Extract JSON from potential markdown code blocks
    let jsonStr = completion.trim();
    
    // Remove markdown code blocks if present
    if (jsonStr.startsWith('```json')) {
      jsonStr = jsonStr.replace(/```json\n?/g, '').replace(/```\n?$/g, '');
    } else if (jsonStr.startsWith('```')) {
      jsonStr = jsonStr.replace(/```\n?/g, '');
    }
    
    const parsed = JSON.parse(jsonStr);
    
    return {
      situation: parsed.situation || '',
      background: parsed.background || '',
      assessment: parsed.assessment || '',
      recommendation: parsed.recommendation || '',
      currentStatus: parsed.currentStatus || '',
      medications: parsed.medications || [],
      allergies: parsed.allergies || [],
      vitalSigns: parsed.vitalSigns || null,
      pendingTasks: parsed.pendingTasks || [],
      changesSinceLastVersion: parsed.changesSinceLastVersion || []
    };
    
  } catch (error) {
    console.error('SBAR parsing error:', error);
    throw new Error('Failed to parse SBAR JSON response');
  }
}

interface SBARValidation {
  isValid: boolean;
  errors: string[];
  warnings: string[];
  completenessScore: number;
}

private validateSBAR(
  sbar: Partial<SBARReport>,
  isInitial: boolean
): SBARValidation {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  // Required fields
  if (!sbar.situation || sbar.situation.length < 20) {
    errors.push('Situation section too short or missing');
  }
  
  if (!sbar.background || sbar.background.length < 20) {
    if (isInitial) {
      errors.push('Background section too short or missing');
    } else {
      warnings.push('Background section may need more detail');
    }
  }
  
  if (!sbar.assessment || sbar.assessment.length < 20) {
    errors.push('Assessment section too short or missing');
  }
  
  if (!sbar.recommendation || sbar.recommendation.length < 20) {
    errors.push('Recommendation section too short or missing');
  }
  
  // Calculate completeness score
  let score = 0;
  const checks = [
    { field: 'situation', weight: 0.25, present: !!sbar.situation && sbar.situation.length >= 50 },
    { field: 'background', weight: 0.25, present: !!sbar.background && sbar.background.length >= 50 },
    { field: 'assessment', weight: 0.25, present: !!sbar.assessment && sbar.assessment.length >= 50 },
    { field: 'recommendation', weight: 0.25, present: !!sbar.recommendation && sbar.recommendation.length >= 50 },
    { field: 'vitalSigns', weight: 0.10, present: !!sbar.vitalSigns },
    { field: 'medications', weight: 0.05, present: !!sbar.medications && sbar.medications.length > 0 },
    { field: 'allergies', weight: 0.05, present: !!sbar.allergies && sbar.allergies.length > 0 }
  ];
  
  checks.forEach(check => {
    if (check.present) score += check.weight;
  });
  
  return {
    isValid: errors.length === 0,
    errors,
    warnings,
    completenessScore: Math.min(1.0, score)
  };
}

private calculateReadabilityScore(sbar: Partial<SBARReport>): number {
  // Simple readability scoring
  // Based on sentence length, word complexity, structure
  
  const allText = [
    sbar.situation,
    sbar.background,
    sbar.assessment,
    sbar.recommendation
  ].filter(Boolean).join(' ');
  
  const sentences = allText.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const avgSentenceLength = allText.split(' ').length / sentences.length;
  
  // Ideal sentence length: 15-20 words
  let score = 1.0;
  if (avgSentenceLength < 10) score -= 0.1;  // Too short
  if (avgSentenceLength > 30) score -= 0.2;  // Too long
  
  return Math.max(0.5, Math.min(1.0, score));
}
```

---

## 5. Prompt Engineering Strategies

### 5.1 Medical Terminology Optimization

**Whisper Prompt (Medical Context):**

```typescript
const MEDICAL_TERMINOLOGY_PROMPT = `
This is a clinical handoff recording. The conversation includes:
- Medical terminology (diagnoses, procedures, medications)
- Vital signs (blood pressure, heart rate, temperature, SpO2)
- Laboratory values (CBC, BMP, cultures)
- Medication names and dosages
- Body systems and anatomical terms
- Clinical abbreviations (PRN, PO, IV, IM, q4h, BID, TID)
`;

// Use when calling Whisper
const transcription = await azureOpenAI.transcribeAudio(audioPath, {
  language: 'en',
  prompt: MEDICAL_TERMINOLOGY_PROMPT,
  temperature: 0 // Deterministic output
});
```

### 5.2 Few-Shot Learning Examples

**GPT-4 with Examples:**

```typescript
const FEW_SHOT_EXAMPLES = `
EXAMPLE 1 (Initial Handoff):
Input Transcription: "This is 45-year-old male admitted yesterday with chest pain. Blood pressure 140 over 90, heart rate 88. EKG shows ST elevation. Started on aspirin, nitroglycerin. Troponin pending. Cardiology consulted."

Output SBAR:
{
  "situation": "45-year-old male admitted 24 hours ago with acute chest pain. Current vital signs: BP 140/90 mmHg, HR 88 bpm. EKG demonstrates ST segment elevation concerning for acute coronary syndrome.",
  "background": "No past medical history provided. No known allergies documented. Social history pending.",
  "assessment": "Acute ST-elevation myocardial infarction (STEMI). Patient hemodynamically stable. Troponin results pending. Cardiology consultation initiated.",
  "recommendation": "Continue aspirin 325mg daily and nitroglycerin sublingual PRN. Monitor cardiac enzymes q6h. Cardiology to evaluate for cardiac catheterization. Telemetry monitoring. NPO for potential procedure."
}

EXAMPLE 2 (Update Handoff - Changes Only):
Previous: "60yo female, glucose 320 mg/dL on admission..."
Current Transcription: "Glucose improved to 180. Started on insulin sliding scale. Tolerating regular diet."

Output SBAR:
{
  "situation": "Blood glucose improved significantly from 320 to 180 mg/dL",
  "background": "[Stable - see v1]",
  "assessment": "Responding well to insulin therapy. Blood glucose trending toward target range.",
  "recommendation": "Continue current insulin sliding scale. Monitor glucose AC and HS. Diabetes education in progress.",
  "changesSinceLastVersion": [
    {"section": "situation", "type": "update", "field": "bloodGlucose", "previousValue": "320 mg/dL", "newValue": "180 mg/dL"},
    {"section": "recommendation", "type": "addition", "field": "medications", "newValue": "Insulin sliding scale initiated"}
  ]
}
`;

// Inject examples into system prompt
const ENHANCED_SYSTEM_PROMPT = `${INITIAL_HANDOFF_SYSTEM_PROMPT}

${FEW_SHOT_EXAMPLES}

Now generate the SBAR for the following handoff:`;
```

### 5.3 I-PASS Framework Integration

```typescript
const IPASS_FRAMEWORK_PROMPT = `
Follow the I-PASS framework strictly:

I - ILLNESS SEVERITY
- Identify patient stability (stable, watcher, unstable)
- Note critical issues requiring immediate attention

P - PATIENT SUMMARY
- Brief overview: age, diagnosis, day of stay
- Key clinical data points

A - ACTION LIST
- Outstanding tasks and pending orders
- Required follow-ups and timeframes

S - SITUATION AWARENESS
- Contingency planning ("If-then" statements)
- Anticipatory guidance

S - SYNTHESIS BY RECEIVER
- Ensure information organized for easy comprehension
- Highlight handback communication needs

Incorporate these elements throughout your SBAR report.
`;
```

### 5.4 Quality Control Prompts

```typescript
const QUALITY_CONTROL_SUFFIX = `
QUALITY CHECKLIST:
✓ All vital signs included with units
✓ Medications with dose, route, frequency
✓ Allergies clearly documented
✓ Time-sensitive items flagged
✓ Clinical reasoning evident
✓ Clear action items
✓ Professional medical terminology
✓ Objective findings separated from assessment
✓ No ambiguous pronouns
✓ Specific measurements (not "normal" or "stable")

Review your SBAR against this checklist before finalizing.
`;

// Append to system prompt
const FINAL_SYSTEM_PROMPT = `${INITIAL_HANDOFF_SYSTEM_PROMPT}

${IPASS_FRAMEWORK_PROMPT}

${QUALITY_CONTROL_SUFFIX}`;
```

---

## 6. Error Handling & Retry Logic

### 6.1 Azure OpenAI Error Handling

```typescript
// apps/backend/src/services/azure-openai-resilience.service.ts

class AzureOpenAIResilientService {
  private maxRetries = 3;
  private baseDelay = 1000; // 1 second
  
  async transcribeWithRetry(
    audioPath: string,
    options?: any
  ): Promise<TranscriptionResult> {
    let lastError: Error | null = null;
    
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        return await this.azureOpenAI.transcribeAudio(audioPath, options);
      } catch (error) {
        lastError = error as Error;
        
        // Check if retryable
        if (!this.isRetryable(error)) {
          throw error;
        }
        
        // Log attempt
        console.warn(`Transcription attempt ${attempt} failed:`, error.message);
        
        // Calculate backoff delay
        if (attempt < this.maxRetries) {
          const delay = this.calculateBackoff(attempt, error);
          console.log(`Retrying in ${delay}ms...`);
          await this.sleep(delay);
        }
      }
    }
    
    throw new Error(
      `Transcription failed after ${this.maxRetries} attempts: ${lastError?.message}`
    );
  }
  
  async generateSBARWithRetry(
    input: GenerateSBARInput
  ): Promise<SBARReport> {
    let lastError: Error | null = null;
    
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        if (input.isInitial) {
          return await this.sbarService.generateInitialSBAR(input);
        } else {
          return await this.sbarService.generateUpdateSBAR(input);
        }
      } catch (error) {
        lastError = error as Error;
        
        if (!this.isRetryable(error)) {
          throw error;
        }
        
        console.warn(`SBAR generation attempt ${attempt} failed:`, error.message);
        
        if (attempt < this.maxRetries) {
          const delay = this.calculateBackoff(attempt, error);
          await this.sleep(delay);
        }
      }
    }
    
    throw new Error(
      `SBAR generation failed after ${this.maxRetries} attempts: ${lastError?.message}`
    );
  }
  
  private isRetryable(error: any): boolean {
    // Retry on rate limits
    if (error.status === 429 || error.code === 'rate_limit_exceeded') {
      return true;
    }
    
    // Retry on timeouts
    if (error.code === 'ETIMEDOUT' || error.code === 'timeout') {
      return true;
    }
    
    // Retry on service unavailable
    if (error.status === 503 || error.code === 'service_unavailable') {
      return true;
    }
    
    // Retry on connection errors
    if (error.code === 'ECONNRESET' || error.code === 'ECONNREFUSED') {
      return true;
    }
    
    // Don't retry on validation errors or bad requests
    if (error.status === 400 || error.status === 422) {
      return false;
    }
    
    // Don't retry on authentication errors
    if (error.status === 401 || error.status === 403) {
      return false;
    }
    
    // Default: retry on 5xx errors
    return error.status >= 500 && error.status < 600;
  }
  
  private calculateBackoff(attempt: number, error: any): number {
    // Check for Retry-After header (rate limiting)
    if (error.headers && error.headers['retry-after']) {
      const retryAfter = parseInt(error.headers['retry-after']);
      return retryAfter * 1000;
    }
    
    // Exponential backoff: 1s, 2s, 4s, 8s...
    const exponentialDelay = this.baseDelay * Math.pow(2, attempt - 1);
    
    // Add jitter (±20%)
    const jitter = exponentialDelay * (0.8 + Math.random() * 0.4);
    
    // Cap at 30 seconds
    return Math.min(jitter, 30000);
  }
  
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### 6.2 Circuit Breaker Pattern

```typescript
// apps/backend/src/services/circuit-breaker.service.ts

enum CircuitState {
  CLOSED = 'closed',      // Normal operation
  OPEN = 'open',          // Failing - reject requests
  HALF_OPEN = 'half_open' // Testing if recovered
}

class CircuitBreaker {
  private state: CircuitState = CircuitState.CLOSED;
  private failureCount = 0;
  private successCount = 0;
  private lastFailureTime: number | null = null;
  
  private readonly failureThreshold = 5;
  private readonly successThreshold = 2;
  private readonly timeout = 60000; // 1 minute
  
  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.OPEN) {
      if (this.shouldAttemptReset()) {
        this.state = CircuitState.HALF_OPEN;
        console.log('Circuit breaker: transitioning to HALF_OPEN');
      } else {
        throw new Error('Circuit breaker is OPEN - service unavailable');
      }
    }
    
    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  private onSuccess(): void {
    this.failureCount = 0;
    
    if (this.state === CircuitState.HALF_OPEN) {
      this.successCount++;
      
      if (this.successCount >= this.successThreshold) {
        this.state = CircuitState.CLOSED;
        this.successCount = 0;
        console.log('Circuit breaker: CLOSED - service recovered');
      }
    }
  }
  
  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    this.successCount = 0;
    
    if (this.failureCount >= this.failureThreshold) {
      this.state = CircuitState.OPEN;
      console.error('Circuit breaker: OPEN - too many failures');
    }
  }
  
  private shouldAttemptReset(): boolean {
    return (
      this.lastFailureTime !== null &&
      Date.now() - this.lastFailureTime >= this.timeout
    );
  }
  
  getState(): CircuitState {
    return this.state;
  }
}

// Usage
const azureOpenAICircuitBreaker = new CircuitBreaker();

async function transcribeWithCircuitBreaker(audioPath: string) {
  return azureOpenAICircuitBreaker.execute(() =>
    azureOpenAI.transcribeAudio(audioPath)
  );
}
```

---

## 7. Cost Optimization

### 7.1 Cost Tracking

```typescript
// apps/backend/src/services/cost-tracking.service.ts

interface AIOperationCost {
  service: 'whisper' | 'gpt4';
  tokensUsed?: number;
  audioDuration?: number;
  estimatedCost: number;
  timestamp: Date;
}

class CostTrackingService {
  // Pricing (as of Oct 2024)
  private readonly WHISPER_COST_PER_MINUTE = 0.006;
  private readonly GPT4_INPUT_COST_PER_1K = 0.03;
  private readonly GPT4_OUTPUT_COST_PER_1K = 0.06;
  
  async trackWhisperCost(audioDurationSeconds: number): Promise<number> {
    const minutes = audioDurationSeconds / 60;
    const cost = minutes * this.WHISPER_COST_PER_MINUTE;
    
    await this.logCost({
      service: 'whisper',
      audioDuration: audioDurationSeconds,
      estimatedCost: cost,
      timestamp: new Date()
    });
    
    return cost;
  }
  
  async trackGPT4Cost(
    inputTokens: number,
    outputTokens: number
  ): Promise<number> {
    const inputCost = (inputTokens / 1000) * this.GPT4_INPUT_COST_PER_1K;
    const outputCost = (outputTokens / 1000) * this.GPT4_OUTPUT_COST_PER_1K;
    const totalCost = inputCost + outputCost;
    
    await this.logCost({
      service: 'gpt4',
      tokensUsed: inputTokens + outputTokens,
      estimatedCost: totalCost,
      timestamp: new Date()
    });
    
    return totalCost;
  }
  
  async getMonthlySpend(): Promise<{whisper: number, gpt4: number, total: number}> {
    const startOfMonth = new Date();
    startOfMonth.setDate(1);
    startOfMonth.setHours(0, 0, 0, 0);
    
    const costs = await this.getCostsSince(startOfMonth);
    
    return {
      whisper: costs.filter(c => c.service === 'whisper')
        .reduce((sum, c) => sum + c.estimatedCost, 0),
      gpt4: costs.filter(c => c.service === 'gpt4')
        .reduce((sum, c) => sum + c.estimatedCost, 0),
      total: costs.reduce((sum, c) => sum + c.estimatedCost, 0)
    };
  }
  
  private async logCost(cost: AIOperationCost): Promise<void> {
    // Store in database
    await db.aiProcessingLogs.create({
      data: {
        service: cost.service,
        tokensUsed: cost.tokensUsed,
        audioDuration: cost.audioDuration,
        estimatedCost: cost.estimatedCost,
        timestamp: cost.timestamp
      }
    });
  }
  
  private async getCostsSince(date: Date): Promise<AIOperationCost[]> {
    return db.aiProcessingLogs.findMany({
      where: {
        timestamp: {
          gte: date
        }
      }
    });
  }
}
```

### 7.2 Token Optimization Strategies

```typescript
// Reduce input tokens for GPT-4
function optimizeTranscriptionForGPT4(transcription: string): string {
  // Remove excessive whitespace
  let optimized = transcription.replace(/\s+/g, ' ').trim();
  
  // Remove filler words (carefully - preserve medical meaning)
  const fillerWords = ['um', 'uh', 'you know', 'like', 'actually', 'basically'];
  fillerWords.forEach(filler => {
    const regex = new RegExp(`\\b${filler}\\b`, 'gi');
    optimized = optimized.replace(regex, '');
  });
  
  // Clean up multiple spaces again
  optimized = optimized.replace(/\s+/g, ' ').trim();
  
  return optimized;
}

// Token estimation
function estimateTokenCount(text: string): number {
  // Rough estimation: ~4 characters per token
  return Math.ceil(text.length / 4);
}

// Cost-aware generation
async function generateSBARWithCostTracking(input: GenerateSBARInput): Promise<{
  sbar: SBARReport;
  cost: number;
}> {
  // Optimize input
  const optimizedTranscription = optimizeTranscriptionForGPT4(input.transcription);
  
  // Estimate input tokens
  const inputTokens = estimateTokenCount(optimizedTranscription) + 
                      estimateTokenCount(JSON.stringify(input.patientContext));
  
  console.log(`Estimated input tokens: ${inputTokens}`);
  
  // Generate SBAR
  const sbar = await sbarService.generateInitialSBAR({
    ...input,
    transcription: optimizedTranscription
  });
  
  // Estimate output tokens
  const outputTokens = estimateTokenCount(JSON.stringify(sbar));
  
  // Track cost
  const cost = await costTracking.trackGPT4Cost(inputTokens, outputTokens);
  
  console.log(`GPT-4 cost for this handoff: $${cost.toFixed(4)}`);
  
  return { sbar, cost };
}
```

### 7.3 Caching Strategies

```typescript
// Cache patient context to reduce API calls
class PatientContextCache {
  private cache = new Map<string, PatientContext>();
  private ttl = 3600000; // 1 hour
  
  get(patientId: string): PatientContext | null {
    const cached = this.cache.get(patientId);
    if (!cached) return null;
    
    // Check if expired
    if (Date.now() - cached.cachedAt > this.ttl) {
      this.cache.delete(patientId);
      return null;
    }
    
    return cached;
  }
  
  set(patientId: string, context: PatientContext): void {
    this.cache.set(patientId, {
      ...context,
      cachedAt: Date.now()
    });
  }
}

// Use cache
const patientCache = new PatientContextCache();

async function getPatientContextForSBAR(patientId: string): Promise<PatientContext> {
  // Try cache first
  let context = patientCache.get(patientId);
  
  if (!context) {
    // Fetch from database
    context = await db.patients.findUnique({
      where: { id: patientId },
      select: {
        id: true,
        firstName: true,
        lastName: true,
        mrn: true,
        dateOfBirth: true,
        gender: true
      }
    });
    
    // Cache for future use
    patientCache.set(patientId, context);
  }
  
  return context;
}
```

---

## 8. Quality Monitoring

### 8.1 SBAR Quality Metrics

```typescript
interface SBARQualityMetrics {
  completenessScore: number;  // 0-1
  readabilityScore: number;   // 0-1
  ipassCompliance: boolean;
  jointCommissionCompliance: boolean;
  criticalInfoPresent: boolean;
  avgSectionLength: number;
  medicalTermAccuracy: number;
}

async function assessSBARQuality(sbar: SBARReport): Promise<SBARQualityMetrics> {
  return {
    completenessScore: calculateCompletenessScore(sbar),
    readabilityScore: calculateReadabilityScore(sbar),
    ipassCompliance: checkIPassCompliance(sbar),
    jointCommissionCompliance: checkJointCommissionCompliance(sbar),
    criticalInfoPresent: checkCriticalInfo(sbar),
    avgSectionLength: calculateAvgSectionLength(sbar),
    medicalTermAccuracy: await validateMedicalTerms(sbar)
  };
}

function checkIPassCompliance(sbar: SBARReport): boolean {
  // I-PASS elements:
  // I - Illness severity
  // P - Patient summary
  // A - Action list
  // S - Situation awareness
  // S - Synthesis
  
  const hasIllnessSeverity = /stable|unstable|watcher|critical/i.test(
    sbar.situation + sbar.assessment
  );
  
  const hasActionList = sbar.pendingTasks && sbar.pendingTasks.length > 0;
  
  const hasSituationAwareness = /if|contingency|anticipate/i.test(
    sbar.recommendation
  );
  
  return hasIllnessSeverity && hasActionList && hasSituationAwareness;
}

function checkJointCommissionCompliance(sbar: SBARReport): boolean {
  // Joint Commission requires:
  // - Patient identification
  // - Current condition
  // - Recent/anticipated changes
  // - Response to treatment
  // - Outstanding tasks
  
  const checks = [
    !!sbar.situation && sbar.situation.length >= 50,
    !!sbar.assessment && sbar.assessment.length >= 50,
    !!sbar.recommendation && sbar.recommendation.length >= 30,
    !!sbar.vitalSigns,
    !!sbar.medications && sbar.medications.length > 0
  ];
  
  return checks.filter(Boolean).length >= 4; // At least 4 of 5
}

function checkCriticalInfo(sbar: SBARReport): boolean {
  // Verify critical information is present
  const criticalElements = [
    !!sbar.allergies, // Allergies documented
    !!sbar.vitalSigns, // Vital signs included
    !!sbar.currentStatus, // Status summary
    sbar.situation.length >= 100, // Sufficient situation detail
    sbar.recommendation.length >= 50 // Clear recommendations
  ];
  
  return criticalElements.filter(Boolean).length >= 4;
}
```

### 8.2 Human Review Queue

```typescript
// Flag SBARs for human review based on quality scores
async function flagForReview(
  sbarId: string,
  metrics: SBARQualityMetrics
): Promise<void> {
  const shouldReview = (
    metrics.completenessScore < 0.7 ||
    metrics.readabilityScore < 0.6 ||
    !metrics.ipassCompliance ||
    !metrics.jointCommissionCompliance ||
    !metrics.criticalInfoPresent
  );
  
  if (shouldReview) {
    await db.sbarReports.update({
      where: { id: sbarId },
      data: {
        flaggedForReview: true,
        reviewReason: generateReviewReason(metrics)
      }
    });
    
    // Notify clinical admin
    await notifyReviewQueue(sbarId, metrics);
  }
}

function generateReviewReason(metrics: SBARQualityMetrics): string {
  const reasons: string[] = [];
  
  if (metrics.completenessScore < 0.7) {
    reasons.push('Low completeness score');
  }
  if (!metrics.ipassCompliance) {
    reasons.push('Missing I-PASS elements');
  }
  if (!metrics.criticalInfoPresent) {
    reasons.push('Missing critical information');
  }
  
  return reasons.join('; ');
}
```

---

## 9. Testing & Validation

### 9.1 Unit Tests

```typescript
// apps/backend/tests/azure-openai.service.test.ts

describe('AzureOpenAIService', () => {
  let service: AzureOpenAIService;
  
  beforeEach(() => {
    service = new AzureOpenAIService();
  });
  
  describe('transcribeAudio', () => {
    it('should successfully transcribe valid audio', async () => {
      const result = await service.transcribeAudio(
        './test-fixtures/sample-handoff.webm'
      );
      
      expect(result.text).toBeDefined();
      expect(result.text.length).toBeGreaterThan(100);
      expect(result.confidence).toBeGreaterThan(0.7);
      expect(result.language).toBe('en');
    });
    
    it('should handle poor audio quality', async () => {
      const result = await service.transcribeAudio(
        './test-fixtures/poor-quality.webm'
      );
      
      expect(result.confidence).toBeLessThan(0.6);
      // Should still return text, but may have [inaudible] markers
    });
  });
  
  describe('generateSBAR', () => {
    it('should generate complete initial SBAR', async () => {
      const transcription = `
        This is a 60-year-old female admitted yesterday with hyperglycemia.
        Blood glucose was 320 on admission. She has type 2 diabetes for 10 years.
        Current vital signs: blood pressure 140 over 90, heart rate 88.
        Started on insulin drip. Glucose is now 180. Continue monitoring.
      `;
      
      const sbar = await service.generateInitialSBAR({
        transcription,
        patientContext: mockPatientContext,
        handoffType: 'admission',
        isInitial: true
      });
      
      expect(sbar.situation).toBeDefined();
      expect(sbar.situation).toContain('60');
      expect(sbar.situation).toContain('hyperglycemia');
      expect(sbar.background).toBeDefined();
      expect(sbar.assessment).toBeDefined();
      expect(sbar.recommendation).toBeDefined();
      expect(sbar.vitalSigns).toBeDefined();
      expect(sbar.version).toBe(1);
      expect(sbar.isInitial).toBe(true);
    });
    
    it('should generate update SBAR with changes tracked', async () => {
      const updateTranscription = `
        Glucose improved to 145. Patient tolerating regular diet.
        Plan for discharge tomorrow.
      `;
      
      const sbar = await service.generateUpdateSBAR({
        transcription: updateTranscription,
        patientContext: mockPatientContext,
        handoffType: 'shift_change',
        isInitial: false,
        previousSBAR: mockPreviousSBAR
      });
      
      expect(sbar.version).toBe(mockPreviousSBAR.version + 1);
      expect(sbar.isInitial).toBe(false);
      expect(sbar.previousVersionId).toBe(mockPreviousSBAR.id);
      expect(sbar.changesSinceLastVersion).toBeDefined();
      expect(sbar.changesSinceLastVersion.length).toBeGreaterThan(0);
    });
  });
});
```

### 9.2 Integration Tests

```typescript
// apps/backend/tests/integration/handoff-workflow.test.ts

describe('Complete Handoff Workflow', () => {
  it('should process voice recording to completed SBAR', async () => {
    // 1. Upload voice recording
    const recording = await voiceService.uploadRecording({
      handoffId: testHandoffId,
      audioFile: fs.readFileSync('./test-fixtures/handoff.webm'),
      duration: 120
    });
    
    expect(recording.status).toBe('uploaded');
    
    // 2. Wait for transcription
    const transcriptionStatus = await voiceService.pollStatus(
      recording.id,
      { maxAttempts: 30 }
    );
    
    expect(transcriptionStatus.status).toBe('transcribed');
    expect(transcriptionStatus.transcription.text).toBeDefined();
    
    // 3. Wait for SBAR generation
    await sleep(5000); // Give time for SBAR generation
    
    const handoff = await handoffService.getHandoff(testHandoffId);
    
    expect(handoff.status).toBe('ready');
    expect(handoff.sbarId).toBeDefined();
    
    // 4. Verify SBAR quality
    const sbar = await sbarService.getSBAR(handoff.sbarId);
    
    expect(sbar.situation).toBeDefined();
    expect(sbar.background).toBeDefined();
    expect(sbar.assessment).toBeDefined();
    expect(sbar.recommendation).toBeDefined();
    expect(sbar.completenessScore).toBeGreaterThan(0.8);
  }, 60000); // 60 second timeout
});
```

---

## Summary

### ✅ Part 5 Complete!

**What Part 5 Covers:**

1. **Azure OpenAI Setup** - Complete service configuration
2. **Whisper Integration** - Voice-to-text with quality validation
3. **GPT-4 Integration** - SBAR generation with initial vs. update prompts
4. **Prompt Engineering** - Medical terminology, few-shot learning, I-PASS framework
5. **Error Handling** - Retry logic, circuit breakers, resilience patterns
6. **Cost Optimization** - Token reduction, caching, cost tracking (~$0.06-$0.14 per handoff)
7. **Quality Monitoring** - Completeness scoring, I-PASS compliance, review queue
8. **Testing** - Unit tests, integration tests, quality validation

### 🎯 Key Innovations:

**Two-Prompt System:**
- Initial handoff → Comprehensive SBAR generation
- Update handoff → Context-aware delta generation with change tracking

**Cost Efficiency:**
- ~$0.06-$0.14 per handoff (very affordable!)
- $60-$140/month for 1000 handoffs

**Quality Assurance:**
- I-PASS framework compliance
- Joint Commission standards
- Automated quality scoring
- Human review queue for low-quality SBARs

**Resilience:**
- Retry with exponential backoff
- Circuit breaker pattern
- Error classification
- Graceful degradation

---

## 📊 Complete Documentation Progress:

| Part | Document | Size | Status |
|------|----------|------|--------|
| 1 | System Architecture | 57KB | ✅ |
| 2 | Repository Structure | 61KB | ✅ |
| 3 | Database Schema | 62KB | ✅ |
| 4A-D | API Specifications | 147KB | ✅ |
| 5 | **Azure OpenAI Integration** | **38KB** | ✅ **NEW!** |
| **TOTAL** | **8 Documents** | **365KB** | **5 of 9 Parts (56%)** |

**Remaining:**
- Part 6: Deployment & DevOps Guide
- Part 7: Security & HIPAA Compliance
- Part 8: Testing Strategy
- Part 9: Product Roadmap & Scaling

---

**Ready for Part 6 (Deployment & DevOps)?** 🚀

---

*EclipseLink AI™ is a product of Rohimaya Health AI*  
*© 2025 Rohimaya Health AI. All rights reserved.*
