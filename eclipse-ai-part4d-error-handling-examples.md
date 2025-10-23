# EclipseLink AI™ - Part 4D: Error Handling, Rate Limiting & Code Examples

**Document Version:** 1.0  
**Last Updated:** October 23, 2025  
**Product:** EclipseLink AI™ Clinical Handoff System  
**Company:** Rohimaya Health AI  
**Founders:** Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO)

---

## Table of Contents

1. [Error Handling](#error-handling)
2. [Rate Limiting](#rate-limiting)
3. [Webhooks](#webhooks)
4. [API Versioning](#api-versioning)
5. [Code Examples](#code-examples)
6. [Testing Guide](#testing-guide)
7. [Best Practices](#best-practices)

---

## 1. Error Handling

### 1.1 Standard Error Response Format

All errors follow a consistent structure:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      // Optional additional context
    }
  },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2025-10-24T08:00:00Z"
  }
}
```

### 1.2 HTTP Status Codes

| Status Code | Meaning | Usage |
|-------------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH request |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE (no response body) |
| 400 | Bad Request | Invalid request parameters or validation error |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Authenticated but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource or constraint violation |
| 422 | Unprocessable Entity | Validation error (semantic error) |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 502 | Bad Gateway | Upstream service (Azure AI) error |
| 503 | Service Unavailable | Service temporarily unavailable |
| 504 | Gateway Timeout | Upstream service timeout |

### 1.3 Error Codes Reference

#### Authentication Errors (AUTH_*)

**AUTH_REQUIRED**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "Authentication is required to access this resource"
  }
}
```

**AUTH_INVALID_TOKEN**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_INVALID_TOKEN",
    "message": "Invalid or expired authentication token",
    "details": {
      "reason": "Token expired at 2025-10-24T07:00:00Z"
    }
  }
}
```

**AUTH_INVALID_CREDENTIALS**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS",
    "message": "Invalid email or password",
    "details": {
      "remainingAttempts": 2,
      "lockoutAfter": 5
    }
  }
}
```

**AUTH_ACCOUNT_LOCKED**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_ACCOUNT_LOCKED",
    "message": "Account is locked due to too many failed login attempts",
    "details": {
      "lockedUntil": "2025-10-24T08:30:00Z",
      "lockedDurationMinutes": 30
    }
  }
}
```

**AUTH_EMAIL_NOT_VERIFIED**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_EMAIL_NOT_VERIFIED",
    "message": "Email address must be verified before login",
    "details": {
      "email": "john.doe@hospital.com",
      "verificationEmailSent": true
    }
  }
}
```

#### Authorization Errors (FORBIDDEN, INSUFFICIENT_PERMISSIONS)

**FORBIDDEN**
```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "You do not have permission to access this resource",
    "details": {
      "requiredPermission": "handoff:delete",
      "userPermissions": ["handoff:create", "handoff:read", "handoff:update"]
    }
  }
}
```

**INSUFFICIENT_PERMISSIONS**
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_PERMISSIONS",
    "message": "Insufficient permissions to perform this action",
    "details": {
      "action": "delete_handoff",
      "requiredRole": "admin",
      "currentRole": "registered_nurse"
    }
  }
}
```

#### Validation Errors (VALIDATION_ERROR, INVALID_INPUT, REQUIRED_FIELD)

**VALIDATION_ERROR**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Email is required",
        "code": "REQUIRED_FIELD",
        "value": null
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters",
        "code": "INVALID_INPUT",
        "value": "short"
      },
      {
        "field": "patientId",
        "message": "Invalid UUID format",
        "code": "INVALID_INPUT",
        "value": "not-a-uuid"
      }
    ]
  }
}
```

**INVALID_INPUT**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Invalid input value",
    "details": {
      "field": "priority",
      "value": "super_urgent",
      "allowedValues": ["routine", "urgent", "emergent"]
    }
  }
}
```

#### Resource Errors (NOT_FOUND, ALREADY_EXISTS, CONFLICT)

**NOT_FOUND**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found",
    "details": {
      "resource": "handoff",
      "id": "h1234567-89ab-cdef-0123-456789abcdef"
    }
  }
}
```

**ALREADY_EXISTS**
```json
{
  "success": false,
  "error": {
    "code": "ALREADY_EXISTS",
    "message": "A resource with this identifier already exists",
    "details": {
      "resource": "user",
      "conflictingField": "email",
      "conflictingValue": "john.doe@hospital.com"
    }
  }
}
```

**CONFLICT**
```json
{
  "success": false,
  "error": {
    "code": "CONFLICT",
    "message": "Operation conflicts with current resource state",
    "details": {
      "resource": "handoff",
      "currentState": "completed",
      "attemptedAction": "update",
      "reason": "Cannot update completed handoff"
    }
  }
}
```

#### State Transition Errors

**INVALID_STATE_TRANSITION**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_STATE_TRANSITION",
    "message": "Cannot transition handoff from current state to requested state",
    "details": {
      "currentStatus": "completed",
      "requestedStatus": "draft",
      "allowedTransitions": [],
      "reason": "Completed handoffs cannot be reopened"
    }
  }
}
```

#### File Upload Errors

**FILE_TOO_LARGE**
```json
{
  "success": false,
  "error": {
    "code": "FILE_TOO_LARGE",
    "message": "Uploaded file exceeds maximum allowed size",
    "details": {
      "maxSize": 10485760,
      "maxSizeFormatted": "10 MB",
      "actualSize": 15728640,
      "actualSizeFormatted": "15 MB"
    }
  }
}
```

**INVALID_FILE_FORMAT**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_FILE_FORMAT",
    "message": "Unsupported file format",
    "details": {
      "supportedFormats": ["audio/webm", "audio/mp3", "audio/wav", "audio/ogg", "audio/m4a"],
      "receivedFormat": "video/mp4"
    }
  }
}
```

#### Processing Errors

**TRANSCRIPTION_FAILED**
```json
{
  "success": false,
  "error": {
    "code": "TRANSCRIPTION_FAILED",
    "message": "Voice transcription failed",
    "details": {
      "recordingId": "v1234567-89ab-cdef-0123-456789abcdef",
      "reason": "Audio quality insufficient for accurate transcription",
      "audioQualityScore": 0.35,
      "minimumRequired": 0.50,
      "attemptNumber": 3,
      "maxAttempts": 3,
      "suggestion": "Please re-record in a quieter environment"
    }
  }
}
```

**SBAR_GENERATION_FAILED**
```json
{
  "success": false,
  "error": {
    "code": "SBAR_GENERATION_FAILED",
    "message": "SBAR report generation failed",
    "details": {
      "handoffId": "h1234567-89ab-cdef-0123-456789abcdef",
      "reason": "Insufficient clinical information in transcription",
      "transcriptionWordCount": 45,
      "minimumRequired": 100,
      "suggestion": "Provide more detailed patient assessment"
    }
  }
}
```

**EHR_SYNC_FAILED**
```json
{
  "success": false,
  "error": {
    "code": "EHR_SYNC_FAILED",
    "message": "EHR synchronization failed",
    "details": {
      "syncId": "sync_abc123",
      "ehrType": "epic",
      "reason": "Connection timeout",
      "retryable": true,
      "retryAfter": 300
    }
  }
}
```

#### Rate Limiting

**RATE_LIMIT_EXCEEDED**
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again later.",
    "details": {
      "limit": 100,
      "remaining": 0,
      "reset": 1698086400,
      "resetFormatted": "2025-10-24T08:00:00Z",
      "retryAfter": 60
    }
  }
}
```

#### Server Errors

**INTERNAL_ERROR**
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An internal server error occurred. Please try again later.",
    "details": {
      "requestId": "req_abc123",
      "timestamp": "2025-10-24T08:00:00Z",
      "supportContact": "support@eclipselink.ai"
    }
  }
}
```

**SERVICE_UNAVAILABLE**
```json
{
  "success": false,
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "Service is temporarily unavailable",
    "details": {
      "retryAfter": 300,
      "reason": "Scheduled maintenance",
      "estimatedResolution": "2025-10-24T09:00:00Z"
    }
  }
}
```

### 1.4 Error Handling Best Practices

**Client-Side Error Handling:**

```typescript
async function apiRequest(endpoint: string, options: RequestOptions) {
  try {
    const response = await fetch(endpoint, options);
    const data = await response.json();
    
    if (!response.ok) {
      // Handle specific error codes
      switch (data.error.code) {
        case 'AUTH_INVALID_TOKEN':
          // Try to refresh token
          await refreshAuthToken();
          // Retry request
          return apiRequest(endpoint, options);
          
        case 'RATE_LIMIT_EXCEEDED':
          // Wait and retry
          const retryAfter = data.error.details.retryAfter * 1000;
          await new Promise(resolve => setTimeout(resolve, retryAfter));
          return apiRequest(endpoint, options);
          
        case 'VALIDATION_ERROR':
          // Show validation errors to user
          showValidationErrors(data.error.details);
          throw new ValidationError(data.error);
          
        case 'NOT_FOUND':
          // Handle missing resource
          throw new NotFoundError(data.error);
          
        default:
          throw new APIError(data.error);
      }
    }
    
    return data;
  } catch (error) {
    // Handle network errors
    if (error instanceof TypeError) {
      throw new NetworkError('Network request failed');
    }
    throw error;
  }
}
```

---

## 2. Rate Limiting

### 2.1 Rate Limit Rules

EclipseLink AI implements rate limiting to ensure fair usage and system stability.

**Per User Limits:**

| Scope | Limit | Window |
|-------|-------|--------|
| General API | 100 requests | per minute |
| General API | 1,000 requests | per hour |
| General API | 10,000 requests | per day |
| Voice Upload | 10 uploads | per minute |
| Voice Upload | 100 uploads | per hour |
| EHR Sync | 1 sync per patient | per minute |
| EHR Sync | 60 syncs | per hour |

**Per Facility Limits:**

| Scope | Limit | Window |
|-------|-------|--------|
| Total API | 1,000 requests | per minute |
| Total API | 10,000 requests | per hour |
| Voice Upload | 100 uploads | per minute |
| EHR Sync | 500 syncs | per hour |

### 2.2 Rate Limit Headers

Every API response includes rate limit information:

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1698086400
X-RateLimit-Window: 60
```

**Header Descriptions:**
- `X-RateLimit-Limit` - Maximum requests allowed in window
- `X-RateLimit-Remaining` - Requests remaining in current window
- `X-RateLimit-Reset` - Unix timestamp when limit resets
- `X-RateLimit-Window` - Window duration in seconds

### 2.3 Rate Limit Response

When rate limit is exceeded:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 60
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1698086460

{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again in 60 seconds.",
    "details": {
      "limit": 100,
      "remaining": 0,
      "reset": 1698086460,
      "retryAfter": 60,
      "window": "per minute"
    }
  }
}
```

### 2.4 Rate Limit Handling

**Exponential Backoff Strategy:**

```typescript
async function apiRequestWithBackoff(
  endpoint: string,
  options: RequestOptions,
  maxRetries: number = 3
): Promise<Response> {
  let attempt = 0;
  
  while (attempt < maxRetries) {
    try {
      const response = await fetch(endpoint, options);
      
      if (response.status === 429) {
        const retryAfter = parseInt(response.headers.get('Retry-After') || '60');
        const backoffTime = Math.min(retryAfter * 1000 * Math.pow(2, attempt), 60000);
        
        console.log(`Rate limited. Retrying after ${backoffTime}ms...`);
        await new Promise(resolve => setTimeout(resolve, backoffTime));
        
        attempt++;
        continue;
      }
      
      return response;
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;
      
      const backoffTime = 1000 * Math.pow(2, attempt);
      await new Promise(resolve => setTimeout(resolve, backoffTime));
      attempt++;
    }
  }
  
  throw new Error('Max retries exceeded');
}
```

### 2.5 Rate Limit Monitoring

**Check Rate Limit Status:**

```typescript
async function checkRateLimitStatus(): Promise<RateLimitStatus> {
  const response = await fetch('https://api.eclipselink.ai/v1/handoffs', {
    method: 'HEAD',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  return {
    limit: parseInt(response.headers.get('X-RateLimit-Limit') || '0'),
    remaining: parseInt(response.headers.get('X-RateLimit-Remaining') || '0'),
    reset: parseInt(response.headers.get('X-RateLimit-Reset') || '0'),
    resetDate: new Date(parseInt(response.headers.get('X-RateLimit-Reset') || '0') * 1000)
  };
}
```

---

## 3. Webhooks

### 3.1 Webhook Overview

EclipseLink AI can send real-time notifications to your server when specific events occur.

**Benefits:**
- Real-time updates without polling
- Reduced API calls
- Event-driven architecture
- Lower latency

### 3.2 Webhook Events

**Handoff Events:**
- `handoff.created` - New handoff created
- `handoff.updated` - Handoff updated
- `handoff.status_changed` - Status changed
- `handoff.assigned` - Assigned to provider
- `handoff.completed` - Handoff completed
- `handoff.cancelled` - Handoff cancelled

**Voice Events:**
- `voice.uploaded` - Voice recording uploaded
- `voice.transcribing` - Transcription started
- `voice.transcribed` - Transcription completed
- `voice.transcription_failed` - Transcription failed

**SBAR Events:**
- `sbar.generating` - SBAR generation started
- `sbar.generated` - SBAR generated
- `sbar.updated` - SBAR manually edited
- `sbar.generation_failed` - Generation failed

**EHR Events:**
- `ehr.sync_started` - EHR sync initiated
- `ehr.sync_completed` - Sync completed successfully
- `ehr.sync_failed` - Sync failed

**Patient Events:**
- `patient.created` - New patient added
- `patient.updated` - Patient data updated
- `patient.discharged` - Patient discharged

### 3.3 Webhook Payload Structure

```json
{
  "event": "handoff.completed",
  "eventId": "evt_abc123xyz456",
  "timestamp": "2025-10-24T08:15:00.000Z",
  "apiVersion": "v1",
  "data": {
    "handoff": {
      "id": "h1234567-89ab-cdef-0123-456789abcdef",
      "patientId": "p1234567-89ab-cdef-0123-456789abcdef",
      "status": "completed",
      "fromStaffId": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
      "toStaffId": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
      "handoffType": "shift_change",
      "completedAt": "2025-10-24T08:15:00Z",
      "sbarId": "s1234567-89ab-cdef-0123-456789abcdef"
    }
  },
  "meta": {
    "facilityId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "environment": "production"
  }
}
```

### 3.4 Webhook Signature Verification

All webhook requests include a signature header for security verification:

**Signature Header:**
```http
X-EclipseLink-Signature: t=1698086400,v1=5257a869e7ecebeda32affa62cdca3fa51cad7e77a0e56ff536d0ce8e108d8bd
```

**Format:** `t={timestamp},v1={signature}`
- `t` - Unix timestamp when signature was created
- `v1` - HMAC-SHA256 signature of payload

**Verification Process:**

```typescript
import crypto from 'crypto';

function verifyWebhookSignature(
  payload: string,
  signatureHeader: string,
  webhookSecret: string
): boolean {
  // Parse signature header
  const elements = signatureHeader.split(',');
  const timestamp = elements[0].split('=')[1];
  const signature = elements[1].split('=')[1];
  
  // Prevent replay attacks (reject if > 5 minutes old)
  const currentTime = Math.floor(Date.now() / 1000);
  if (currentTime - parseInt(timestamp) > 300) {
    throw new Error('Webhook signature expired');
  }
  
  // Create signed payload
  const signedPayload = `${timestamp}.${payload}`;
  
  // Compute expected signature
  const expectedSignature = crypto
    .createHmac('sha256', webhookSecret)
    .update(signedPayload)
    .digest('hex');
  
  // Compare signatures (timing-safe)
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  );
}
```

**Express.js Example:**

```typescript
import express from 'express';

const app = express();

app.post('/webhooks/eclipselink', 
  express.raw({ type: 'application/json' }),
  (req, res) => {
    const signature = req.headers['x-eclipselink-signature'] as string;
    const payload = req.body.toString('utf8');
    
    try {
      // Verify signature
      const isValid = verifyWebhookSignature(
        payload,
        signature,
        process.env.WEBHOOK_SECRET!
      );
      
      if (!isValid) {
        return res.status(401).send('Invalid signature');
      }
      
      // Parse and process event
      const event = JSON.parse(payload);
      handleWebhookEvent(event);
      
      // Acknowledge receipt
      res.status(200).send({ received: true });
    } catch (error) {
      console.error('Webhook error:', error);
      res.status(400).send('Invalid webhook');
    }
  }
);

function handleWebhookEvent(event: WebhookEvent) {
  switch (event.event) {
    case 'handoff.completed':
      console.log('Handoff completed:', event.data.handoff.id);
      // Update internal systems
      break;
      
    case 'voice.transcribed':
      console.log('Transcription ready:', event.data.recording.id);
      // Notify staff
      break;
      
    case 'sbar.generated':
      console.log('SBAR generated:', event.data.sbar.id);
      // Export to EHR
      break;
      
    default:
      console.log('Unhandled event:', event.event);
  }
}
```

### 3.5 Webhook Configuration

**Register Webhook Endpoint (Future API):**

```http
POST /v1/webhooks
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "url": "https://your-server.com/webhooks/eclipselink",
  "events": [
    "handoff.completed",
    "voice.transcribed",
    "sbar.generated"
  ],
  "active": true,
  "description": "Production webhook endpoint"
}
```

### 3.6 Webhook Retry Logic

If your endpoint returns an error or timeout:

**Retry Schedule:**
- Immediate: 0 seconds
- Retry 1: 5 seconds
- Retry 2: 30 seconds
- Retry 3: 5 minutes
- Retry 4: 30 minutes
- Retry 5: 2 hours
- Retry 6: 6 hours

**After 6 failed attempts:** Webhook is marked as failing and must be manually re-enabled.

**Expected Response:**
- Status Code: 200, 201, or 204
- Response Time: < 10 seconds

---

## 4. API Versioning

### 4.1 Versioning Strategy

EclipseLink AI uses URL-based versioning:

```
https://api.eclipselink.ai/v1/handoffs
https://api.eclipselink.ai/v2/handoffs (future)
```

**Current Version:** v1  
**Latest Version:** v1  
**Supported Versions:** v1

### 4.2 Version Headers

**Request:**
```http
GET /v1/handoffs
Accept: application/json
Accept-Version: v1
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json
API-Version: v1
```

### 4.3 Deprecation Policy

When endpoints are deprecated:

**Deprecation Notice (6 months before sunset):**
```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 01 Jun 2026 00:00:00 GMT
Link: <https://docs.eclipselink.ai/api/migration/v2>; rel="sunset"
```

**Timeline:**
1. **Deprecation Announcement** - 6 months notice
2. **Migration Guide Published** - Migration documentation
3. **Warning Period** - Deprecation headers added
4. **Sunset Date** - Old version disabled
5. **Grace Period** - 30 days emergency access

---

## 5. Code Examples

### 5.1 Complete JavaScript/TypeScript Client

**API Client Setup:**

```typescript
// api-client.ts
import axios, { AxiosInstance, AxiosError } from 'axios';

interface APIConfig {
  baseURL: string;
  timeout?: number;
}

interface TokenStorage {
  accessToken: string | null;
  refreshToken: string | null;
}

class EclipseLinkAPI {
  private client: AxiosInstance;
  private tokens: TokenStorage = {
    accessToken: null,
    refreshToken: null
  };
  
  constructor(config: APIConfig) {
    this.client = axios.create({
      baseURL: config.baseURL || 'https://api.eclipselink.ai/v1',
      timeout: config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    // Request interceptor - add auth token
    this.client.interceptors.request.use(
      (config) => {
        if (this.tokens.accessToken) {
          config.headers.Authorization = `Bearer ${this.tokens.accessToken}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );
    
    // Response interceptor - handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;
        
        // Handle 401 - try to refresh token
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            await this.refreshAccessToken();
            return this.client(originalRequest);
          } catch (refreshError) {
            // Refresh failed - redirect to login
            this.handleAuthFailure();
            return Promise.reject(refreshError);
          }
        }
        
        // Handle 429 - rate limit
        if (error.response?.status === 429) {
          const retryAfter = error.response.headers['retry-after'] || 60;
          await this.delay(parseInt(retryAfter) * 1000);
          return this.client(originalRequest);
        }
        
        return Promise.reject(error);
      }
    );
  }
  
  // Authentication
  async login(email: string, password: string) {
    const response = await this.client.post('/auth/login', {
      email,
      password
    });
    
    this.tokens.accessToken = response.data.data.tokens.accessToken;
    this.tokens.refreshToken = response.data.data.tokens.refreshToken;
    
    // Store in localStorage
    localStorage.setItem('accessToken', this.tokens.accessToken);
    localStorage.setItem('refreshToken', this.tokens.refreshToken!);
    
    return response.data.data.user;
  }
  
  async refreshAccessToken() {
    if (!this.tokens.refreshToken) {
      throw new Error('No refresh token available');
    }
    
    const response = await this.client.post('/auth/refresh', {
      refreshToken: this.tokens.refreshToken
    });
    
    this.tokens.accessToken = response.data.data.accessToken;
    this.tokens.refreshToken = response.data.data.refreshToken;
    
    localStorage.setItem('accessToken', this.tokens.accessToken);
    localStorage.setItem('refreshToken', this.tokens.refreshToken!);
  }
  
  async logout() {
    try {
      await this.client.post('/auth/logout', {
        refreshToken: this.tokens.refreshToken
      });
    } finally {
      this.tokens.accessToken = null;
      this.tokens.refreshToken = null;
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    }
  }
  
  // Handoffs
  async createHandoff(data: CreateHandoffDTO) {
    const response = await this.client.post('/handoffs', data);
    return response.data.data;
  }
  
  async getHandoffs(params?: HandoffQueryParams) {
    const response = await this.client.get('/handoffs', { params });
    return response.data.data;
  }
  
  async getHandoff(handoffId: string) {
    const response = await this.client.get(`/handoffs/${handoffId}`);
    return response.data.data;
  }
  
  async updateHandoff(handoffId: string, data: Partial<Handoff>) {
    const response = await this.client.put(`/handoffs/${handoffId}`, data);
    return response.data.data;
  }
  
  async completeHandoff(handoffId: string, completionNotes: string) {
    const response = await this.client.post(`/handoffs/${handoffId}/complete`, {
      completionNotes
    });
    return response.data.data;
  }
  
  // Voice Recording
  async uploadVoiceRecording(
    handoffId: string,
    audioBlob: Blob,
    duration: number,
    onProgress?: (progress: number) => void
  ) {
    const formData = new FormData();
    formData.append('handoffId', handoffId);
    formData.append('audio', audioBlob, 'recording.webm');
    formData.append('duration', duration.toString());
    
    const response = await this.client.post('/voice/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      }
    });
    
    return response.data.data;
  }
  
  async getVoiceStatus(recordingId: string) {
    const response = await this.client.get(`/voice/${recordingId}/status`);
    return response.data.data;
  }
  
  async pollVoiceStatus(
    recordingId: string,
    onUpdate?: (status: VoiceStatus) => void
  ): Promise<VoiceStatus> {
    let attempts = 0;
    const maxAttempts = 60; // 5 minutes max
    
    const getDelay = (attempt: number): number => {
      if (attempt < 15) return 2000;      // 2s for first 30s
      if (attempt < 24) return 5000;      // 5s for next 45s
      if (attempt < 36) return 10000;     // 10s for next 2min
      return 15000;                        // 15s after that
    };
    
    while (attempts < maxAttempts) {
      const status = await this.getVoiceStatus(recordingId);
      
      if (onUpdate) {
        onUpdate(status);
      }
      
      if (status.status === 'transcribed' || status.status === 'failed') {
        return status;
      }
      
      attempts++;
      await this.delay(getDelay(attempts));
    }
    
    throw new Error('Voice processing timeout after 5 minutes');
  }
  
  // Patients
  async getPatients(params?: PatientQueryParams) {
    const response = await this.client.get('/patients', { params });
    return response.data.data;
  }
  
  async getPatient(patientId: string) {
    const response = await this.client.get(`/patients/${patientId}`);
    return response.data.data;
  }
  
  async getPatientHandoffs(patientId: string, params?: any) {
    const response = await this.client.get(
      `/patients/${patientId}/handoffs`,
      { params }
    );
    return response.data.data;
  }
  
  // SBAR
  async getSbar(handoffId: string) {
    const response = await this.client.get(`/sbar/${handoffId}`);
    return response.data.data;
  }
  
  async getSbarVersions(handoffId: string) {
    const response = await this.client.get(`/sbar/${handoffId}/versions`);
    return response.data.data;
  }
  
  async updateSbar(sbarId: string, data: UpdateSbarDTO) {
    const response = await this.client.put(`/sbar/${sbarId}`, data);
    return response.data.data;
  }
  
  async exportSbar(sbarId: string, format: 'pdf' | 'docx' | 'txt') {
    const response = await this.client.post(`/sbar/${sbarId}/export`, {
      format
    });
    return response.data.data;
  }
  
  // Utilities
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  private handleAuthFailure() {
    // Redirect to login or emit event
    window.location.href = '/login';
  }
  
  // Set tokens (for hydrating from localStorage)
  setTokens(accessToken: string, refreshToken: string) {
    this.tokens.accessToken = accessToken;
    this.tokens.refreshToken = refreshToken;
  }
}

// Export singleton instance
export const api = new EclipseLinkAPI({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://api.eclipselink.ai/v1'
});

// Hydrate tokens from localStorage on init
if (typeof window !== 'undefined') {
  const accessToken = localStorage.getItem('accessToken');
  const refreshToken = localStorage.getItem('refreshToken');
  if (accessToken && refreshToken) {
    api.setTokens(accessToken, refreshToken);
  }
}
```

**Usage Examples:**

```typescript
// Login
async function handleLogin(email: string, password: string) {
  try {
    const user = await api.login(email, password);
    console.log('Logged in as:', user.firstName, user.lastName);
  } catch (error) {
    console.error('Login failed:', error);
  }
}

// Create handoff with voice recording
async function createHandoffWithVoice(
  patientId: string,
  audioBlob: Blob,
  duration: number
) {
  try {
    // Step 1: Create handoff
    const handoff = await api.createHandoff({
      patientId,
      fromStaffId: currentUser.id,
      handoffType: 'shift_change',
      priority: 'routine',
      isInitialHandoff: false,
      previousHandoffId: latestHandoffId
    });
    
    console.log('Handoff created:', handoff.id);
    
    // Step 2: Upload voice recording
    const recording = await api.uploadVoiceRecording(
      handoff.id,
      audioBlob,
      duration,
      (progress) => console.log(`Upload: ${progress}%`)
    );
    
    console.log('Recording uploaded:', recording.recordingId);
    
    // Step 3: Poll for transcription and SBAR generation
    const finalStatus = await api.pollVoiceStatus(
      recording.recordingId,
      (status) => console.log('Status:', status.stage, status.progress + '%')
    );
    
    console.log('Processing complete!', finalStatus);
    
    // Step 4: Get complete handoff with SBAR
    const completeHandoff = await api.getHandoff(handoff.id);
    return completeHandoff;
    
  } catch (error) {
    console.error('Error creating handoff:', error);
    throw error;
  }
}

// Get handoffs with filtering
async function getMyHandoffs() {
  const result = await api.getHandoffs({
    toStaffId: currentUser.id,
    status: 'assigned',
    page: 1,
    limit: 20
  });
  
  console.log(`Found ${result.handoffs.length} handoffs`);
  return result.handoffs;
}
```

### 5.2 Python Client

```python
# eclipselink_client.py
import requests
from typing import Dict, Optional, List
from datetime import datetime
import time

class EclipseLinkAPI:
    def __init__(self, base_url: str = "https://api.eclipselink.ai/v1"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def _get_headers(self) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        headers.update(kwargs.pop('headers', {}))
        
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs
        )
        
        # Handle rate limiting
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limited. Retrying after {retry_after}s...")
            time.sleep(retry_after)
            return self._request(method, endpoint, **kwargs)
        
        # Handle token refresh
        if response.status_code == 401 and self.refresh_token:
            self._refresh_access_token()
            return self._request(method, endpoint, **kwargs)
        
        response.raise_for_status()
        return response.json()
    
    # Authentication
    def login(self, email: str, password: str) -> Dict:
        data = self._request('POST', '/auth/login', json={
            'email': email,
            'password': password
        })
        
        self.access_token = data['data']['tokens']['accessToken']
        self.refresh_token = data['data']['tokens']['refreshToken']
        
        return data['data']['user']
    
    def _refresh_access_token(self):
        data = self._request('POST', '/auth/refresh', json={
            'refreshToken': self.refresh_token
        })
        
        self.access_token = data['data']['accessToken']
        self.refresh_token = data['data']['refreshToken']
    
    def logout(self):
        try:
            self._request('POST', '/auth/logout', json={
                'refreshToken': self.refresh_token
            })
        finally:
            self.access_token = None
            self.refresh_token = None
    
    # Handoffs
    def create_handoff(self, handoff_data: Dict) -> Dict:
        return self._request('POST', '/handoffs', json=handoff_data)['data']
    
    def get_handoffs(self, **params) -> Dict:
        return self._request('GET', '/handoffs', params=params)['data']
    
    def get_handoff(self, handoff_id: str) -> Dict:
        return self._request('GET', f'/handoffs/{handoff_id}')['data']
    
    def update_handoff(self, handoff_id: str, updates: Dict) -> Dict:
        return self._request('PUT', f'/handoffs/{handoff_id}', json=updates)['data']
    
    def complete_handoff(self, handoff_id: str, completion_notes: str) -> Dict:
        return self._request('POST', f'/handoffs/{handoff_id}/complete', json={
            'completionNotes': completion_notes
        })['data']
    
    # Voice Recording
    def upload_voice_recording(
        self,
        handoff_id: str,
        audio_file_path: str,
        duration: int
    ) -> Dict:
        with open(audio_file_path, 'rb') as audio_file:
            files = {
                'audio': ('recording.webm', audio_file, 'audio/webm')
            }
            data = {
                'handoffId': handoff_id,
                'duration': str(duration)
            }
            
            # Special headers for multipart
            headers = {'Authorization': f'Bearer {self.access_token}'}
            
            response = requests.post(
                f'{self.base_url}/voice/upload',
                files=files,
                data=data,
                headers=headers
            )
            response.raise_for_status()
            return response.json()['data']
    
    def get_voice_status(self, recording_id: str) -> Dict:
        return self._request('GET', f'/voice/{recording_id}/status')['data']
    
    def poll_voice_status(
        self,
        recording_id: str,
        max_attempts: int = 60,
        callback = None
    ) -> Dict:
        """Poll voice processing status until complete or failed"""
        for attempt in range(max_attempts):
            status = self.get_voice_status(recording_id)
            
            if callback:
                callback(status)
            
            if status['status'] in ['transcribed', 'failed']:
                return status
            
            # Dynamic delay
            if attempt < 15:
                delay = 2
            elif attempt < 24:
                delay = 5
            elif attempt < 36:
                delay = 10
            else:
                delay = 15
            
            time.sleep(delay)
        
        raise TimeoutError('Voice processing timeout after 5 minutes')
    
    # Patients
    def get_patients(self, **params) -> Dict:
        return self._request('GET', '/patients', params=params)['data']
    
    def get_patient(self, patient_id: str) -> Dict:
        return self._request('GET', f'/patients/{patient_id}')['data']
    
    def get_patient_handoffs(self, patient_id: str, **params) -> Dict:
        return self._request(
            'GET',
            f'/patients/{patient_id}/handoffs',
            params=params
        )['data']
    
    # SBAR
    def get_sbar(self, handoff_id: str) -> Dict:
        return self._request('GET', f'/sbar/{handoff_id}')['data']
    
    def get_sbar_versions(self, handoff_id: str) -> Dict:
        return self._request('GET', f'/sbar/{handoff_id}/versions')['data']
    
    def update_sbar(self, sbar_id: str, updates: Dict) -> Dict:
        return self._request('PUT', f'/sbar/{sbar_id}', json=updates)['data']
    
    def export_sbar(self, sbar_id: str, format: str = 'pdf') -> Dict:
        return self._request('POST', f'/sbar/{sbar_id}/export', json={
            'format': format
        })['data']


# Usage example
if __name__ == '__main__':
    api = EclipseLinkAPI()
    
    # Login
    user = api.login('john.doe@hospital.com', 'SecurePass123!')
    print(f"Logged in as {user['firstName']} {user['lastName']}")
    
    # Get handoffs
    handoffs = api.get_handoffs(status='ready', page=1, limit=10)
    print(f"Found {len(handoffs['handoffs'])} handoffs")
    
    # Create handoff
    new_handoff = api.create_handoff({
        'patientId': 'p1234567-89ab-cdef-0123-456789abcdef',
        'fromStaffId': user['id'],
        'handoffType': 'shift_change',
        'priority': 'routine',
        'isInitialHandoff': False,
        'previousHandoffId': 'h1234567-89ab-cdef-0123-456789abcdef'
    })
    print(f"Created handoff: {new_handoff['id']}")
```

### 5.3 cURL Examples

**Login:**
```bash
curl -X POST https://api.eclipselink.ai/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@hospital.com",
    "password": "SecurePass123!"
  }'
```

**Create Handoff:**
```bash
curl -X POST https://api.eclipselink.ai/v1/handoffs \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patientId": "p1234567-89ab-cdef-0123-456789abcdef",
    "fromStaffId": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
    "handoffType": "shift_change",
    "priority": "routine",
    "isInitialHandoff": false,
    "previousHandoffId": "h1234567-89ab-cdef-0123-456789abcdef"
  }'
```

**Upload Voice Recording:**
```bash
curl -X POST https://api.eclipselink.ai/v1/voice/upload \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "handoffId=h1234567-89ab-cdef-0123-456789abcdef" \
  -F "duration=185" \
  -F "audio=@recording.webm"
```

**Get Handoffs with Filters:**
```bash
curl -X GET "https://api.eclipselink.ai/v1/handoffs?status=ready&priority=urgent&page=1&limit=20" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 6. Testing Guide

### 6.1 Test Environment

**Staging API:**
```
https://api-staging.eclipselink.ai/v1
```

**Test Credentials:**
```
Email: test.nurse@eclipselink-demo.com
Password: Demo123!
Role: registered_nurse

Email: test.doctor@eclipselink-demo.com
Password: Demo123!
Role: physician

Email: test.admin@eclipselink-demo.com
Password: Demo123!
Role: admin
```

### 6.2 Postman Collection

**Import URL:**
```
https://api.eclipselink.ai/postman/collection.json
```

**Environment Variables:**
```json
{
  "base_url": "https://api-staging.eclipselink.ai/v1",
  "access_token": "{{accessToken}}",
  "refresh_token": "{{refreshToken}}",
  "test_patient_id": "p-demo-001",
  "test_handoff_id": "h-demo-001"
}
```

### 6.3 Sample Test Data

**Test Patient IDs:**
- `p-demo-001` - Jane Smith (Type 2 Diabetes)
- `p-demo-002` - Robert Johnson (Pneumonia)
- `p-demo-003` - Mary Williams (Post-operative)

**Test Handoff IDs:**
- `h-demo-001` - Completed shift change
- `h-demo-002` - Active transfer
- `h-demo-003` - Pending admission

---

## 7. Best Practices

### 7.1 Authentication

✅ **DO:**
- Store tokens securely (HttpOnly cookies or encrypted storage)
- Implement automatic token refresh
- Handle 401 errors gracefully
- Clear tokens on logout

❌ **DON'T:**
- Store tokens in plain localStorage (use encryption)
- Embed tokens in URLs
- Share tokens between users
- Ignore token expiration

### 7.2 Error Handling

✅ **DO:**
- Check `success` field in responses
- Handle specific error codes
- Implement retry logic for transient errors
- Log errors with request IDs
- Show user-friendly error messages

❌ **DON'T:**
- Assume all 200 responses are successful
- Ignore error details
- Retry on 4xx errors (except 429)
- Expose technical errors to users

### 7.3 Rate Limiting

✅ **DO:**
- Monitor rate limit headers
- Implement exponential backoff
- Respect Retry-After header
- Cache responses when possible
- Use webhooks instead of polling

❌ **DON'T:**
- Ignore 429 responses
- Retry immediately
- Make unnecessary API calls
- Poll at fixed intervals

### 7.4 Voice Recording

✅ **DO:**
- Compress audio before upload
- Show upload progress
- Handle network interruptions
- Validate audio format
- Test audio quality

❌ **DON'T:**
- Upload uncompressed audio
- Exceed 10MB file size
- Upload without error handling
- Use unsupported formats

### 7.5 SBAR Management

✅ **DO:**
- Link update handoffs to previous
- Set isInitialHandoff correctly
- Track version history
- Review AI-generated content
- Save edits with summaries

❌ **DON'T:**
- Create initial handoffs repeatedly
- Ignore previousHandoffId
- Accept AI output without review
- Delete version history

---

## Summary

### ✅ Part 4D Complete!

**What Part 4D Covers:**

1. **Error Handling** - 20+ error codes with examples
2. **Rate Limiting** - Limits, headers, retry strategies
3. **Webhooks** - Real-time events with signature verification
4. **API Versioning** - Deprecation policy
5. **Code Examples** - Complete clients in TypeScript, Python, cURL
6. **Testing Guide** - Test environment, Postman, sample data
7. **Best Practices** - Authentication, errors, rate limits, SBAR

### 📊 Complete Part 4 Summary:

**Part 4A:** API Overview & Authentication (32KB)  
**Part 4B:** Handoff & Voice Endpoints (33KB)  
**Part 4C:** Patient, SBAR & EHR Endpoints (39KB)  
**Part 4D:** Error Handling & Code Examples (38KB)

**Total Part 4:** 142KB of comprehensive API documentation!

### 🎯 Key Takeaways:

1. **Initial vs Update Workflow** - Critical distinction for efficiency
2. **SBAR Versioning** - Complete audit trail and change tracking
3. **Comprehensive Error Handling** - 20+ error codes
4. **Production-Ready Code** - Complete clients with retry logic
5. **Rate Limiting** - Smart backoff strategies
6. **Webhooks** - Real-time updates with security

---

## 📦 All Documentation Complete:

1. ✅ **Part 1: System Architecture** (57KB)
2. ✅ **Part 2: Repository Structure** (61KB)
3. ✅ **Part 3: Database Schema** (62KB)
4. ✅ **Part 4A-D: API Specifications** (142KB)

**Total Documentation: 322KB** 🎉

**Ready to move to Part 5: Azure OpenAI Integration?**

---

*EclipseLink AI™ is a product of Rohimaya Health AI*  
*© 2025 Rohimaya Health AI. All rights reserved.*
