# EclipseLink AI™ - Part 4A: API Overview & Authentication

**Document Version:** 1.0  
**Last Updated:** October 23, 2025  
**Product:** EclipseLink AI™ Clinical Handoff System  
**Company:** Rohimaya Health AI  
**Founders:** Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO)

---

## Table of Contents

1. [API Overview](#api-overview)
2. [Base URLs & Architecture](#base-urls-architecture)
3. [Authentication Flow](#authentication-flow)
4. [Authentication Endpoints](#authentication-endpoints)
5. [JWT Token Structure](#jwt-token-structure)
6. [Role-Based Access Control](#role-based-access-control)
7. [Common Headers](#common-headers)

---

## 1. API Overview

### 1.1 Introduction

EclipseLink AI provides a comprehensive RESTful API for managing clinical handoffs, voice recordings, patient data, and EHR integrations. The API follows industry best practices for security, performance, and developer experience.

**Key Features:**
- RESTful design principles
- JWT-based authentication
- HIPAA-compliant security
- Rate limiting & throttling
- Comprehensive error handling
- Real-time webhooks
- Detailed documentation

### 1.2 API Design Principles

**RESTful Architecture:**
- Resource-based URLs (`/handoffs`, `/patients`)
- Standard HTTP methods (GET, POST, PUT, DELETE)
- Stateless communication
- HATEOAS principles where applicable

**JSON-First:**
- All requests accept `application/json`
- All responses return `application/json`
- ISO 8601 date formats
- Consistent naming conventions (camelCase)

**Security-First:**
- HTTPS only (TLS 1.3)
- JWT authentication with refresh tokens
- Row-level security (RLS)
- CORS configuration
- Rate limiting per user/facility
- Input validation with Zod schemas

**Developer-Friendly:**
- Predictable error responses
- Detailed error messages
- Comprehensive documentation
- Code examples in multiple languages
- Postman collection available

---

## 2. Base URLs & Architecture

### 2.1 Base URLs

**Production:**
```
https://api.eclipselink.ai/v1
```

**Staging:**
```
https://api-staging.eclipselink.ai/v1
```

**Development:**
```
http://localhost:4000/v1
```

### 2.2 API Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                   CLIENT APPLICATIONS                         │
│  (Web Frontend, Mobile Apps, Third-Party Integrations)       │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ HTTPS (TLS 1.3)
                         │ Authorization: Bearer {token}
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                  CLOUDFLARE CDN + WAF                         │
│  • Global Edge Network (300+ locations)                      │
│  • DDoS Protection                                           │
│  • SSL/TLS Termination                                       │
│  • Rate Limiting (Layer 7)                                   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    API GATEWAY LAYER                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Express.js Middleware Stack                           │ │
│  │  1. Request Logging (Winston + Logtail)                │ │
│  │  2. CORS Handling                                       │ │
│  │  3. JWT Verification                                    │ │
│  │  4. Role-Based Access Control (RBAC)                   │ │
│  │  5. Request Validation (Zod)                           │ │
│  │  6. Rate Limiting (Redis)                              │ │
│  │  7. Error Handling                                      │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
           ┌─────────────┼─────────────┬─────────────┐
           │             │             │             │
           ▼             ▼             ▼             ▼
    ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
    │   Auth    │ │  Handoff  │ │  Patient  │ │   Voice   │
    │  Routes   │ │  Routes   │ │  Routes   │ │  Routes   │
    └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
          │             │             │             │
          └─────────────┼─────────────┼─────────────┘
                        │             │
                        ▼             ▼
              ┌──────────────────────────────┐
              │      SERVICE LAYER           │
              │  (Business Logic & Data)     │
              └──────────────┬───────────────┘
                             │
           ┌─────────────────┼─────────────────┬──────────────┐
           │                 │                 │              │
           ▼                 ▼                 ▼              ▼
    ┌──────────┐      ┌──────────┐     ┌──────────┐   ┌──────────┐
    │ Supabase │      │  Upstash │     │  Azure   │   │Cloudflare│
    │(PostgreSQL)│      │  Redis   │     │  OpenAI  │   │    R2    │
    └──────────┘      └──────────┘     └──────────┘   └──────────┘
```

### 2.3 Request Flow

**Typical API Request:**

```
1. Client makes HTTPS request
   ↓
2. Cloudflare CDN receives request
   ↓
3. SSL/TLS termination & DDoS check
   ↓
4. Forward to API Gateway (Railway)
   ↓
5. Express middleware processes request:
   - Parse request body
   - Verify JWT token
   - Check user permissions
   - Validate input data
   - Check rate limits
   ↓
6. Route to appropriate controller
   ↓
7. Controller calls service layer
   ↓
8. Service layer:
   - Queries database (Supabase)
   - Calls external APIs (Azure OpenAI)
   - Updates cache (Redis)
   ↓
9. Format response
   ↓
10. Return JSON response to client
```

---

## 3. Authentication Flow

### 3.1 JWT-Based Authentication

EclipseLink AI uses **JSON Web Tokens (JWT)** for stateless authentication. The flow includes both access tokens (short-lived, 1 hour) and refresh tokens (long-lived, 30 days).

### 3.2 Complete Authentication Flow

```
┌────────────┐                                    ┌────────────┐
│   Client   │                                    │   Server   │
└─────┬──────┘                                    └─────┬──────┘
      │                                                 │
      │  1. POST /v1/auth/login                        │
      │     { email, password }                        │
      │────────────────────────────────────────────────>│
      │                                                 │
      │                                                 │ 2. Verify credentials
      │                                                 │    with Supabase Auth
      │                                                 │
      │                                                 │ 3. Generate tokens:
      │                                                 │    - Access token (1hr)
      │                                                 │    - Refresh token (30d)
      │                                                 │
      │                                                 │ 4. Store session in DB
      │                                                 │    (user_sessions table)
      │                                                 │
      │  5. 200 OK                                     │
      │     { accessToken, refreshToken, user }        │
      │<────────────────────────────────────────────────│
      │                                                 │
      │  6. Store tokens in secure storage             │
      │     (HttpOnly cookies or localStorage)          │
      │                                                 │
      │                                                 │
      │  ════════════════════════════════════════════  │
      │        AUTHENTICATED API REQUESTS               │
      │  ════════════════════════════════════════════  │
      │                                                 │
      │  7. GET /v1/handoffs                           │
      │     Authorization: Bearer {accessToken}         │
      │────────────────────────────────────────────────>│
      │                                                 │
      │                                                 │ 8. Verify JWT signature
      │                                                 │
      │                                                 │ 9. Check expiration
      │                                                 │
      │                                                 │ 10. Extract user info
      │                                                 │     from token payload
      │                                                 │
      │                                                 │ 11. Check permissions
      │                                                 │     (RBAC)
      │                                                 │
      │                                                 │ 12. Query data with
      │                                                 │     RLS policies
      │                                                 │
      │  13. 200 OK                                    │
      │      { handoffs: [...] }                       │
      │<────────────────────────────────────────────────│
      │                                                 │
      │                                                 │
      │  ════════════════════════════════════════════  │
      │         TOKEN REFRESH (after 1 hour)           │
      │  ════════════════════════════════════════════  │
      │                                                 │
      │  14. GET /v1/handoffs                          │
      │      Authorization: Bearer {expiredToken}       │
      │────────────────────────────────────────────────>│
      │                                                 │
      │                                                 │ 15. Token expired!
      │                                                 │
      │  16. 401 Unauthorized                          │
      │      { error: "AUTH_INVALID_TOKEN" }           │
      │<────────────────────────────────────────────────│
      │                                                 │
      │  17. POST /v1/auth/refresh                     │
      │      { refreshToken }                          │
      │────────────────────────────────────────────────>│
      │                                                 │
      │                                                 │ 18. Verify refresh token
      │                                                 │
      │                                                 │ 19. Check session in DB
      │                                                 │
      │                                                 │ 20. Generate new tokens
      │                                                 │
      │  21. 200 OK                                    │
      │      { accessToken, refreshToken }             │
      │<────────────────────────────────────────────────│
      │                                                 │
      │  22. Store new tokens                          │
      │                                                 │
      │  23. Retry original request with new token     │
      │      GET /v1/handoffs                          │
      │      Authorization: Bearer {newAccessToken}     │
      │────────────────────────────────────────────────>│
      │                                                 │
      │  24. 200 OK                                    │
      │      { handoffs: [...] }                       │
      │<────────────────────────────────────────────────│
      │                                                 │
```

### 3.3 Token Lifecycle

**Access Token:**
- **Expires:** 1 hour
- **Purpose:** Authenticate API requests
- **Storage:** Memory or secure storage
- **Claims:** userId, facilityId, role, permissions

**Refresh Token:**
- **Expires:** 30 days
- **Purpose:** Obtain new access tokens
- **Storage:** Secure HttpOnly cookie (preferred) or encrypted storage
- **Rotation:** New refresh token issued on each refresh

---

## 4. Authentication Endpoints

### 4.1 POST /v1/auth/register

Register a new user account.

**Request:**
```http
POST /v1/auth/register
Content-Type: application/json

{
  "email": "john.doe@hospital.com",
  "password": "SecurePass123!",
  "firstName": "John",
  "lastName": "Doe",
  "role": "registered_nurse",
  "facilityId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "licenseNumber": "RN123456",
  "licenseState": "CO"
}
```

**Validation Rules:**
- `email`: Valid email format, unique
- `password`: Min 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special char
- `firstName`: Required, 2-100 characters
- `lastName`: Required, 2-100 characters
- `role`: Valid role enum
- `facilityId`: Valid UUID, facility must exist
- `licenseNumber`: Required for clinical roles
- `licenseState`: Valid 2-letter state code

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
      "email": "john.doe@hospital.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "registered_nurse",
      "facilityId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "facility": {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "name": "City General Hospital",
        "type": "hospital"
      },
      "isActive": true,
      "emailVerified": false,
      "createdAt": "2025-10-23T22:30:00.000Z"
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJhM2IyYzFkNC1lNWY2LTRhN2ItOGM5ZC0wZTFmMmEzYjRjNWQiLCJmYWNpbGl0eUlkIjoiZjQ3YWMxMGItNThjYy00MzcyLWE1NjctMGUwMmIyYzNkNDc5Iiwicm9sZSI6InJlZ2lzdGVyZWRfbnVyc2UiLCJwZXJtaXNzaW9ucyI6WyJoYW5kb2ZmOmNyZWF0ZSIsImhhbmRvZmY6cmVhZCIsImhhbmRvZmY6dXBkYXRlIiwicGF0aWVudDpyZWFkIiwidm9pY2U6dXBsb2FkIl0sImlhdCI6MTY5ODA4NjQwMCwiZXhwIjoxNjk4MDkwMDAwLCJpc3MiOiJlY2xpcHNlbGluay1hcGkiLCJhdWQiOiJlY2xpcHNlbGluay1mcm9udGVuZCJ9.signature",
      "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJhM2IyYzFkNC1lNWY2LTRhN2ItOGM5ZC0wZTFmMmEzYjRjNWQiLCJ0b2tlbklkIjoidG9rZW5fYWJjMTIzIiwiaWF0IjoxNjk4MDg2NDAwLCJleHAiOjE3MDA2Nzg0MDAsImlzcyI6ImVjbGlwc2VsaW5rLWFwaSIsImF1ZCI6ImVjbGlwc2VsaW5rLWZyb250ZW5kIn0.signature",
      "expiresIn": 3600,
      "tokenType": "Bearer"
    }
  },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2025-10-23T22:30:00.000Z"
  }
}
```

**Error Responses:**

**400 Bad Request - Validation Error:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "password",
        "message": "Password must contain at least one uppercase letter",
        "code": "INVALID_INPUT"
      }
    ]
  }
}
```

**409 Conflict - Email Already Exists:**
```json
{
  "success": false,
  "error": {
    "code": "ALREADY_EXISTS",
    "message": "A user with this email already exists"
  }
}
```

---

### 4.2 POST /v1/auth/login

Authenticate user and receive JWT tokens.

**Request:**
```http
POST /v1/auth/login
Content-Type: application/json

{
  "email": "john.doe@hospital.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
      "email": "john.doe@hospital.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "registered_nurse",
      "facilityId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "facility": {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "name": "City General Hospital",
        "type": "hospital"
      },
      "department": "Emergency Department",
      "isActive": true,
      "emailVerified": true,
      "mfaEnabled": false,
      "lastLoginAt": "2025-10-23T22:30:00.000Z"
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expiresIn": 3600,
      "tokenType": "Bearer"
    }
  }
}
```

**Error Responses:**

**401 Unauthorized - Invalid Credentials:**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

**403 Forbidden - Account Locked:**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_ACCOUNT_LOCKED",
    "message": "Account is locked due to too many failed login attempts. Try again in 30 minutes.",
    "details": {
      "lockedUntil": "2025-10-23T23:00:00.000Z"
    }
  }
}
```

---

### 4.3 POST /v1/auth/refresh

Refresh access token using refresh token.

**Request:**
```http
POST /v1/auth/refresh
Content-Type: application/json

{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 3600,
    "tokenType": "Bearer"
  }
}
```

**Error Responses:**

**401 Unauthorized - Invalid Refresh Token:**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_INVALID_TOKEN",
    "message": "Invalid or expired refresh token"
  }
}
```

---

### 4.4 POST /v1/auth/logout

Invalidate current session and tokens.

**Request:**
```http
POST /v1/auth/logout
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

**Implementation Notes:**
- Invalidates both access and refresh tokens
- Removes session from `user_sessions` table
- Blacklists tokens in Redis (optional for extra security)

---

### 4.5 POST /v1/auth/forgot-password

Request password reset email.

**Request:**
```http
POST /v1/auth/forgot-password
Content-Type: application/json

{
  "email": "john.doe@hospital.com"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "If an account exists with this email, a password reset link has been sent."
}
```

**Implementation Notes:**
- Always returns success (prevents email enumeration)
- Sends email with reset link valid for 1 hour
- Reset token stored in database with expiration

---

### 4.6 POST /v1/auth/reset-password

Reset password with token from email.

**Request:**
```http
POST /v1/auth/reset-password
Content-Type: application/json

{
  "token": "reset_abc123xyz456",
  "password": "NewSecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

**Error Responses:**

**400 Bad Request - Invalid Token:**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Invalid or expired password reset token"
  }
}
```

---

### 4.7 POST /v1/auth/verify-email

Verify email address with token.

**Request:**
```http
POST /v1/auth/verify-email
Content-Type: application/json

{
  "token": "verify_abc123xyz456"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Email verified successfully"
}
```

---

### 4.8 GET /v1/auth/me

Get current authenticated user information.

**Request:**
```http
GET /v1/auth/me
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
    "email": "john.doe@hospital.com",
    "firstName": "John",
    "lastName": "Doe",
    "preferredName": "Johnny",
    "role": "registered_nurse",
    "title": "Emergency Department RN",
    "department": "Emergency Department",
    "facilityId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "facility": {
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "name": "City General Hospital",
      "type": "hospital",
      "address": {
        "city": "Denver",
        "state": "CO"
      }
    },
    "licenseNumber": "RN123456",
    "licenseState": "CO",
    "phone": "+13035551234",
    "avatarUrl": "https://eclipselink-production.r2.cloudflarestorage.com/avatars/a3b2c1d4.jpg",
    "preferences": {
      "language": "en",
      "timezone": "America/Denver",
      "notifications": {
        "email": true,
        "push": true,
        "sms": false
      }
    },
    "isActive": true,
    "emailVerified": true,
    "mfaEnabled": false,
    "lastLoginAt": "2025-10-23T22:30:00.000Z",
    "createdAt": "2025-01-15T10:00:00.000Z"
  }
}
```

---

### 4.9 PUT /v1/auth/me

Update current user profile.

**Request:**
```http
PUT /v1/auth/me
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "preferredName": "Johnny",
  "phone": "+13035551234",
  "preferences": {
    "notifications": {
      "email": true,
      "push": true,
      "sms": true
    }
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
    "preferredName": "Johnny",
    "phone": "+13035551234",
    "preferences": {
      "notifications": {
        "email": true,
        "push": true,
        "sms": true
      }
    },
    "updatedAt": "2025-10-23T22:35:00.000Z"
  }
}
```

---

### 4.10 POST /v1/auth/change-password

Change password for authenticated user.

**Request:**
```http
POST /v1/auth/change-password
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "currentPassword": "SecurePass123!",
  "newPassword": "NewSecurePass456!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

**Error Responses:**

**401 Unauthorized - Wrong Current Password:**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS",
    "message": "Current password is incorrect"
  }
}
```

---

## 5. JWT Token Structure

### 5.1 Access Token Payload

```json
{
  "userId": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "facilityId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "role": "registered_nurse",
  "permissions": [
    "handoff:create",
    "handoff:read",
    "handoff:update",
    "patient:read",
    "voice:upload",
    "sbar:read",
    "sbar:update"
  ],
  "iat": 1698086400,
  "exp": 1698090000,
  "iss": "eclipselink-api",
  "aud": "eclipselink-frontend"
}
```

**Claims Explained:**
- `userId`: User's unique identifier
- `facilityId`: User's facility (for data isolation)
- `role`: User's role for RBAC
- `permissions`: Array of specific permissions
- `iat`: Issued at (Unix timestamp)
- `exp`: Expires at (Unix timestamp)
- `iss`: Issuer (our API)
- `aud`: Audience (our frontend)

### 5.2 Refresh Token Payload

```json
{
  "userId": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "tokenId": "token_abc123",
  "type": "refresh",
  "iat": 1698086400,
  "exp": 1700678400,
  "iss": "eclipselink-api",
  "aud": "eclipselink-frontend"
}
```

**Claims Explained:**
- `tokenId`: Unique token identifier (for revocation)
- `type`: Token type (refresh)
- Longer expiration (30 days)

### 5.3 Token Verification

**Backend (Node.js):**
```typescript
import jwt from 'jsonwebtoken';

interface JWTPayload {
  userId: string;
  facilityId: string;
  role: string;
  permissions: string[];
}

function verifyAccessToken(token: string): JWTPayload {
  try {
    const decoded = jwt.verify(
      token,
      process.env.JWT_SECRET as string,
      {
        issuer: 'eclipselink-api',
        audience: 'eclipselink-frontend'
      }
    ) as JWTPayload;
    
    return decoded;
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      throw new Error('AUTH_INVALID_TOKEN');
    }
    throw new Error('AUTH_INVALID_TOKEN');
  }
}
```

---

## 6. Role-Based Access Control (RBAC)

### 6.1 Roles & Permissions Matrix

| Role | Handoff | Patient | Voice | SBAR | Staff | Facility | Settings |
|------|---------|---------|-------|------|-------|----------|----------|
| **registered_nurse** | create, read, update | read | upload | read, update | read (self) | read | read |
| **licensed_practical_nurse** | create, read, update | read | upload | read, update | read (self) | read | read |
| **certified_nursing_assistant** | read | read | upload | read | read (self) | read | read |
| **physician** | create, read, update, delete | create, read, update | upload | create, read, update, approve | read | read | read |
| **nurse_practitioner** | create, read, update, delete | create, read, update | upload | create, read, update, approve | read | read | read |
| **physician_assistant** | create, read, update | read, update | upload | read, update, approve | read | read | read |
| **admin** | all | all | all | all | all | read, update | all |
| **super_admin** | all | all | all | all | all | all | all |

### 6.2 Permission Format

**Pattern:** `resource:action`

**Examples:**
- `handoff:create` - Create handoffs
- `handoff:read` - Read handoffs
- `handoff:update` - Update handoffs
- `handoff:delete` - Delete handoffs
- `patient:read` - Read patient data
- `patient:update` - Update patient data
- `*:*` - All permissions (super_admin)

### 6.3 Permission Check Middleware

```typescript
import { Request, Response, NextFunction } from 'express';

function requirePermission(permission: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = req.user; // Set by auth middleware
    
    if (!user) {
      return res.status(401).json({
        success: false,
        error: {
          code: 'AUTH_REQUIRED',
          message: 'Authentication required'
        }
      });
    }
    
    // Super admin has all permissions
    if (user.role === 'super_admin') {
      return next();
    }
    
    // Check if user has specific permission
    const hasPermission = user.permissions.includes(permission) || 
                         user.permissions.includes('*:*');
    
    if (!hasPermission) {
      return res.status(403).json({
        success: false,
        error: {
          code: 'FORBIDDEN',
          message: 'You do not have permission to perform this action'
        }
      });
    }
    
    next();
  };
}

// Usage in routes
router.post('/handoffs', 
  authenticateJWT,
  requirePermission('handoff:create'),
  createHandoff
);
```

---

## 7. Common Headers

### 7.1 Required Request Headers

**For All Authenticated Requests:**
```http
Authorization: Bearer {accessToken}
Content-Type: application/json
Accept: application/json
```

**Optional Request Headers:**
```http
X-Client-Version: 1.0.0
X-Request-ID: {uuid}
X-Device-ID: {device_identifier}
Accept-Language: en-US
```

### 7.2 Standard Response Headers

**All Responses Include:**
```http
Content-Type: application/json; charset=utf-8
X-Request-ID: {uuid}
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1698086400
X-Response-Time: 145ms
```

**CORS Headers:**
```http
Access-Control-Allow-Origin: https://app.eclipselink.ai
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type, X-Request-ID
Access-Control-Max-Age: 86400
```

**Security Headers:**
```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
```

---

## Summary

### ✅ Part 4A Covers:

1. **API Overview** - Architecture, design principles, base URLs
2. **Authentication Flow** - Complete JWT authentication lifecycle
3. **Auth Endpoints** - 10 authentication endpoints with examples
4. **JWT Structure** - Token payload details and verification
5. **RBAC** - Complete role-based access control matrix
6. **Headers** - Standard request/response headers

### 📊 Authentication Endpoints Summary:

1. POST /v1/auth/register
2. POST /v1/auth/login
3. POST /v1/auth/refresh
4. POST /v1/auth/logout
5. POST /v1/auth/forgot-password
6. POST /v1/auth/reset-password
7. POST /v1/auth/verify-email
8. GET /v1/auth/me
9. PUT /v1/auth/me
10. POST /v1/auth/change-password

### 🔐 Security Features:

- JWT with 1-hour access tokens
- 30-day refresh tokens with rotation
- Password requirements enforced
- Account lockout after failed attempts
- Email verification
- HTTPS only
- CORS protection
- Rate limiting

---

**Next:** Part 4B will cover Handoff & Voice Recording endpoints.

---

*EclipseLink AI™ is a product of Rohimaya Health AI*  
*© 2025 Rohimaya Health AI. All rights reserved.*
