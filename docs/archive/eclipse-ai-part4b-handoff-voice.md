# EclipseLink AI™ - Part 4B: Handoff & Voice Recording Endpoints

**Document Version:** 1.0  
**Last Updated:** October 23, 2025  
**Product:** EclipseLink AI™ Clinical Handoff System  
**Company:** Rohimaya Health AI  
**Founders:** Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO)

---

## Table of Contents

1. [Handoff Endpoints Overview](#handoff-endpoints-overview)
2. [Handoff Management Endpoints](#handoff-management-endpoints)
3. [Voice Recording Endpoints](#voice-recording-endpoints)
4. [Real-Time Status Polling](#real-time-status-polling)
5. [Batch Operations](#batch-operations)

---

## 1. Handoff Endpoints Overview

### 1.1 Handoff Lifecycle States

```
┌─────────┐
│  draft  │ ──> User creates handoff
└────┬────┘
     │
     ▼
┌─────────────┐
│  recording  │ ──> Voice recording in progress
└─────┬───────┘
      │
      ▼
┌──────────────┐
│ transcribing │ ──> Azure Whisper processing audio
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  generating  │ ──> GPT-4 generating SBAR
└──────┬───────┘
       │
       ▼
┌─────────┐
│  ready  │ ──> SBAR complete, ready for review
└────┬────┘
     │
     ├──> ┌──────────┐
     │    │ assigned │ ──> Assigned to receiving provider
     │    └────┬─────┘
     │         │
     │         ▼
     │    ┌──────────┐
     │    │ accepted │ ──> Provider accepted handoff
     │    └────┬─────┘
     │         │
     ▼         ▼
┌───────────┐
│ completed │ ──> Handoff finalized
└───────────┘

     OR
     
┌───────────┐
│ cancelled │ ──> Handoff cancelled
└───────────┘

     OR
     
┌─────────┐
│ failed  │ ──> AI processing failed
└─────────┘
```

### 1.2 Handoff Resource Structure

```typescript
interface Handoff {
  id: string;
  patientId: string;
  facilityId: string;
  fromStaffId: string;
  toStaffId?: string;
  status: HandoffStatus;
  priority: 'routine' | 'urgent' | 'emergent';
  handoffType: string;
  location?: string;
  scheduledTime?: string;
  actualTime?: string;
  clinicalNotes?: string;
  
  // Processing metadata
  voiceRecordingStartedAt?: string;
  voiceRecordingCompletedAt?: string;
  transcriptionStartedAt?: string;
  transcriptionCompletedAt?: string;
  sbarGenerationStartedAt?: string;
  sbarGenerationCompletedAt?: string;
  
  // Duration metrics
  recordingDuration?: number;
  transcriptionDuration?: number;
  sbarGenerationDuration?: number;
  totalProcessingTime?: number;
  
  // Quality metrics
  qualityScore?: number;
  
  // Flags
  isCritical: boolean;
  requiresFollowup: boolean;
  flaggedForReview: boolean;
  
  // EHR export
  exportedToEhr: boolean;
  exportCompletedAt?: string;
  
  // Timestamps
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
}
```

---

## 2. Handoff Management Endpoints

### 2.1 POST /v1/handoffs

Create a new handoff.

**Endpoint:**
```
POST /v1/handoffs
```

**Authentication:** Required  
**Permission:** `handoff:create`

**Request:**
```http
POST /v1/handoffs
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "patientId": "p1234567-89ab-cdef-0123-456789abcdef",
  "fromStaffId": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "toStaffId": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
  "handoffType": "shift_change",
  "priority": "routine",
  "scheduledTime": "2025-10-24T07:00:00Z",
  "location": "Room 305",
  "clinicalNotes": "Patient stable, continue current treatment plan",
  "isCritical": false,
  "requiresFollowup": true
}
```

**Request Body Schema:**
```typescript
{
  patientId: string;           // Required, valid UUID
  fromStaffId: string;         // Required, valid UUID
  toStaffId?: string;          // Optional, valid UUID
  handoffType: string;         // Required: shift_change, transfer, admission, discharge, procedure
  priority: string;            // Optional (default: routine): routine, urgent, emergent
  scheduledTime?: string;      // Optional, ISO 8601 datetime
  location?: string;           // Optional, max 100 chars
  clinicalNotes?: string;      // Optional, max 5000 chars
  isCritical?: boolean;        // Optional (default: false)
  requiresFollowup?: boolean;  // Optional (default: false)
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "h1234567-89ab-cdef-0123-456789abcdef",
    "patientId": "p1234567-89ab-cdef-0123-456789abcdef",
    "patient": {
      "id": "p1234567-89ab-cdef-0123-456789abcdef",
      "firstName": "Jane",
      "lastName": "Smith",
      "mrn": "MRN123456",
      "dateOfBirth": "1965-03-15",
      "roomNumber": "305"
    },
    "facilityId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "fromStaffId": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
    "fromStaff": {
      "id": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
      "firstName": "John",
      "lastName": "Doe",
      "role": "registered_nurse"
    },
    "toStaffId": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
    "toStaff": {
      "id": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
      "firstName": "Sarah",
      "lastName": "Johnson",
      "role": "registered_nurse"
    },
    "status": "draft",
    "handoffType": "shift_change",
    "priority": "routine",
    "scheduledTime": "2025-10-24T07:00:00Z",
    "location": "Room 305",
    "clinicalNotes": "Patient stable, continue current treatment plan",
    "isCritical": false,
    "requiresFollowup": true,
    "exportedToEhr": false,
    "createdAt": "2025-10-23T22:30:00Z",
    "updatedAt": "2025-10-23T22:30:00Z"
  },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2025-10-23T22:30:00Z"
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
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "patientId",
        "message": "Patient ID is required",
        "code": "REQUIRED_FIELD"
      },
      {
        "field": "handoffType",
        "message": "Invalid handoff type",
        "code": "INVALID_INPUT"
      }
    ]
  }
}
```

**404 Not Found - Patient Not Found:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Patient not found",
    "details": {
      "resource": "patient",
      "id": "p1234567-89ab-cdef-0123-456789abcdef"
    }
  }
}
```

---

### 2.2 GET /v1/handoffs

List handoffs with filtering, sorting, and pagination.

**Endpoint:**
```
GET /v1/handoffs
```

**Authentication:** Required  
**Permission:** `handoff:read`

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number (1-indexed) |
| limit | integer | 20 | Items per page (max 100) |
| status | string | all | Filter by status |
| priority | string | all | Filter by priority |
| handoffType | string | all | Filter by type |
| fromStaffId | UUID | - | Filter by giving provider |
| toStaffId | UUID | - | Filter by receiving provider |
| patientId | UUID | - | Filter by patient |
| startDate | ISO 8601 | - | Filter by created date (start) |
| endDate | ISO 8601 | - | Filter by created date (end) |
| search | string | - | Search by patient name/MRN |
| sortBy | string | createdAt | Sort field |
| sortOrder | string | desc | Sort order (asc/desc) |
| includeSbar | boolean | false | Include SBAR in response |

**Request Examples:**

**Get all ready handoffs:**
```http
GET /v1/handoffs?status=ready&page=1&limit=20
Authorization: Bearer {accessToken}
```

**Get urgent handoffs for specific provider:**
```http
GET /v1/handoffs?priority=urgent&toStaffId=b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d&status=assigned
Authorization: Bearer {accessToken}
```

**Search handoffs by patient:**
```http
GET /v1/handoffs?search=Smith&page=1&limit=20
Authorization: Bearer {accessToken}
```

**Get handoffs within date range:**
```http
GET /v1/handoffs?startDate=2025-10-20T00:00:00Z&endDate=2025-10-24T00:00:00Z
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "handoffs": [
      {
        "id": "h1234567-89ab-cdef-0123-456789abcdef",
        "patient": {
          "id": "p1234567-89ab-cdef-0123-456789abcdef",
          "firstName": "Jane",
          "lastName": "Smith",
          "mrn": "MRN123456",
          "dateOfBirth": "1965-03-15",
          "roomNumber": "305"
        },
        "fromStaff": {
          "id": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
          "firstName": "John",
          "lastName": "Doe",
          "role": "registered_nurse",
          "department": "Emergency Department"
        },
        "toStaff": {
          "id": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
          "firstName": "Sarah",
          "lastName": "Johnson",
          "role": "registered_nurse",
          "department": "Medical/Surgical"
        },
        "status": "ready",
        "priority": "urgent",
        "handoffType": "shift_change",
        "scheduledTime": "2025-10-24T07:00:00Z",
        "location": "Room 305",
        "hasSbar": true,
        "hasVoiceRecording": true,
        "processingComplete": true,
        "totalProcessingTime": 40,
        "qualityScore": 0.95,
        "isCritical": false,
        "requiresFollowup": true,
        "createdAt": "2025-10-23T22:30:00Z",
        "updatedAt": "2025-10-23T22:35:00Z"
      },
      {
        "id": "h2345678-90ab-cdef-0123-456789abcdef",
        "patient": {
          "id": "p2345678-90ab-cdef-0123-456789abcdef",
          "firstName": "Robert",
          "lastName": "Johnson",
          "mrn": "MRN789012",
          "dateOfBirth": "1980-07-22",
          "roomNumber": "412"
        },
        "fromStaff": {
          "id": "c5d4e3f2-a1b2-3c4d-5e6f-7a8b9c0d1e2f",
          "firstName": "Emily",
          "lastName": "Brown",
          "role": "physician"
        },
        "toStaff": null,
        "status": "generating",
        "priority": "routine",
        "handoffType": "transfer",
        "scheduledTime": "2025-10-24T09:00:00Z",
        "location": "Room 412",
        "hasSbar": false,
        "hasVoiceRecording": true,
        "processingComplete": false,
        "isCritical": false,
        "requiresFollowup": false,
        "createdAt": "2025-10-23T22:40:00Z",
        "updatedAt": "2025-10-23T22:42:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "totalPages": 3,
      "hasNextPage": true,
      "hasPrevPage": false,
      "nextPage": 2,
      "prevPage": null
    },
    "summary": {
      "totalHandoffs": 45,
      "statusBreakdown": {
        "draft": 2,
        "recording": 1,
        "transcribing": 3,
        "generating": 5,
        "ready": 18,
        "assigned": 10,
        "accepted": 4,
        "completed": 2
      },
      "priorityBreakdown": {
        "routine": 35,
        "urgent": 8,
        "emergent": 2
      }
    }
  },
  "meta": {
    "requestId": "req_abc124",
    "timestamp": "2025-10-23T22:45:00Z"
  }
}
```

---

### 2.3 GET /v1/handoffs/:id

Get detailed handoff information by ID.

**Endpoint:**
```
GET /v1/handoffs/{handoffId}
```

**Authentication:** Required  
**Permission:** `handoff:read`

**Request:**
```http
GET /v1/handoffs/h1234567-89ab-cdef-0123-456789abcdef
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "h1234567-89ab-cdef-0123-456789abcdef",
    
    "patient": {
      "id": "p1234567-89ab-cdef-0123-456789abcdef",
      "firstName": "Jane",
      "lastName": "Smith",
      "mrn": "MRN123456",
      "dateOfBirth": "1965-03-15",
      "gender": "female",
      "roomNumber": "305",
      "bedNumber": "A",
      "primaryDiagnosis": "Type 2 Diabetes Mellitus",
      "chiefComplaint": "Hyperglycemia",
      "allergies": [
        {
          "allergen": "Penicillin",
          "reaction": "Rash",
          "severity": "Moderate"
        }
      ],
      "medications": [
        {
          "name": "Metformin",
          "dose": "1000mg",
          "frequency": "Twice daily",
          "route": "Oral"
        },
        {
          "name": "Lisinopril",
          "dose": "10mg",
          "frequency": "Once daily",
          "route": "Oral"
        }
      ],
      "vitalSigns": {
        "temperature": 98.6,
        "temperatureUnit": "F",
        "bpSystolic": 130,
        "bpDiastolic": 85,
        "heartRate": 78,
        "respiratoryRate": 16,
        "oxygenSaturation": 98,
        "recordedAt": "2025-10-23T20:00:00Z"
      },
      "admissionDate": "2025-10-20T14:30:00Z",
      "status": "active"
    },
    
    "fromStaff": {
      "id": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
      "firstName": "John",
      "lastName": "Doe",
      "role": "registered_nurse",
      "department": "Emergency Department",
      "phone": "+13035551234",
      "email": "john.doe@hospital.com"
    },
    
    "toStaff": {
      "id": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
      "firstName": "Sarah",
      "lastName": "Johnson",
      "role": "registered_nurse",
      "department": "Medical/Surgical",
      "phone": "+13035555678",
      "email": "sarah.johnson@hospital.com"
    },
    
    "status": "ready",
    "priority": "urgent",
    "handoffType": "transfer",
    "scheduledTime": "2025-10-24T07:00:00Z",
    "actualTime": null,
    "location": "Room 305",
    "clinicalNotes": "Patient stable, continue current treatment plan",
    
    "voiceRecording": {
      "id": "v1234567-89ab-cdef-0123-456789abcdef",
      "duration": 185,
      "fileSize": 2048000,
      "audioFormat": "webm",
      "status": "transcribed",
      "uploadedAt": "2025-10-23T22:32:00Z",
      "processedAt": "2025-10-23T22:33:15Z"
    },
    
    "aiGeneration": {
      "transcription": {
        "id": "ai_trans_abc123",
        "text": "Patient is a 60-year-old female with type 2 diabetes admitted three days ago for hyperglycemia. Current blood glucose is 145 milligrams per deciliter...",
        "confidence": 0.96,
        "wordCount": 385,
        "processingDuration": 22
      },
      "sbarGeneration": {
        "id": "ai_sbar_def456",
        "processingDuration": 18,
        "qualityScore": 0.95
      }
    },
    
    "sbarReport": {
      "id": "s1234567-89ab-cdef-0123-456789abcdef",
      "situation": "60-year-old female with type 2 diabetes admitted 3 days ago for hyperglycemia. Patient is alert and oriented x3. Current blood glucose 145 mg/dL.",
      "background": "Past medical history includes type 2 diabetes (10 years), hypertension, and hyperlipidemia. Home medications include Metformin 1000mg BID and Lisinopril 10mg daily. Known allergy to Penicillin (rash). Patient lives at home with spouse, independent with ADLs.",
      "assessment": "Current vital signs: T 98.6°F, BP 130/85, HR 78, RR 16, SpO2 98% on room air. Blood glucose trending downward with current insulin regimen. No acute distress noted. Patient reports decreased thirst and improved energy levels. Last HbA1c 8.2% from admission labs.",
      "recommendation": "Continue current insulin sliding scale. Diabetes education completed - patient verbalizes understanding. Consider discharge in 24 hours if blood glucose remains stable. Follow-up appointment with endocrinology in 2 weeks. Continue home medications upon discharge.",
      "version": 1,
      "isLatest": true,
      "completenessScore": 0.95,
      "readabilityScore": 0.88,
      "createdAt": "2025-10-23T22:33:30Z"
    },
    
    "assignments": [
      {
        "staffId": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
        "role": "giving",
        "status": "completed",
        "completedAt": "2025-10-23T22:35:00Z"
      },
      {
        "staffId": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
        "role": "receiving",
        "status": "pending",
        "notifiedAt": "2025-10-23T22:35:00Z"
      }
    ],
    
    "processingTimes": {
      "voiceRecordingStartedAt": "2025-10-23T22:30:00Z",
      "voiceRecordingCompletedAt": "2025-10-23T22:32:30Z",
      "transcriptionStartedAt": "2025-10-23T22:32:35Z",
      "transcriptionCompletedAt": "2025-10-23T22:33:00Z",
      "sbarGenerationStartedAt": "2025-10-23T22:33:05Z",
      "sbarGenerationCompletedAt": "2025-10-23T22:33:30Z",
      "recordingDuration": 185,
      "transcriptionDuration": 22,
      "sbarGenerationDuration": 18,
      "totalProcessingTime": 40
    },
    
    "qualityScore": 0.95,
    "isCritical": false,
    "requiresFollowup": true,
    "flaggedForReview": false,
    
    "exportedToEhr": false,
    "exportAttemptedAt": null,
    "exportCompletedAt": null,
    
    "version": 1,
    "createdAt": "2025-10-23T22:30:00Z",
    "updatedAt": "2025-10-23T22:35:00Z",
    "completedAt": null
  },
  "meta": {
    "requestId": "req_abc125",
    "timestamp": "2025-10-23T22:45:00Z"
  }
}
```

**Error Responses:**

**404 Not Found:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Handoff not found",
    "details": {
      "resource": "handoff",
      "id": "h1234567-89ab-cdef-0123-456789abcdef"
    }
  }
}
```

---

### 2.4 PUT /v1/handoffs/:id

Update handoff information.

**Endpoint:**
```
PUT /v1/handoffs/{handoffId}
```

**Authentication:** Required  
**Permission:** `handoff:update`

**Request:**
```http
PUT /v1/handoffs/h1234567-89ab-cdef-0123-456789abcdef
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "status": "assigned",
  "toStaffId": "c5d4e3f2-a1b2-3c4d-5e6f-7a8b9c0d1e2f",
  "priority": "urgent",
  "clinicalNotes": "Updated notes: Patient requesting pain medication. Blood glucose stable at 145 mg/dL.",
  "requiresFollowup": true
}
```

**Updatable Fields:**
- `status` - Update handoff status
- `toStaffId` - Assign to different provider
- `priority` - Change priority level
- `scheduledTime` - Update scheduled time
- `location` - Update location
- `clinicalNotes` - Add/update clinical notes
- `isCritical` - Mark as critical
- `requiresFollowup` - Set followup flag

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "h1234567-89ab-cdef-0123-456789abcdef",
    "status": "assigned",
    "toStaffId": "c5d4e3f2-a1b2-3c4d-5e6f-7a8b9c0d1e2f",
    "toStaff": {
      "id": "c5d4e3f2-a1b2-3c4d-5e6f-7a8b9c0d1e2f",
      "firstName": "Emily",
      "lastName": "Brown",
      "role": "physician"
    },
    "priority": "urgent",
    "clinicalNotes": "Updated notes: Patient requesting pain medication. Blood glucose stable at 145 mg/dL.",
    "requiresFollowup": true,
    "updatedAt": "2025-10-23T22:50:00Z"
  }
}
```

**Error Responses:**

**400 Bad Request - Invalid Status Transition:**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_STATE_TRANSITION",
    "message": "Cannot transition from 'completed' to 'draft'",
    "details": {
      "currentStatus": "completed",
      "requestedStatus": "draft",
      "allowedTransitions": []
    }
  }
}
```

---

### 2.5 POST /v1/handoffs/:id/assign

Assign handoff to a provider.

**Endpoint:**
```
POST /v1/handoffs/{handoffId}/assign
```

**Authentication:** Required  
**Permission:** `handoff:update`

**Request:**
```http
POST /v1/handoffs/h1234567-89ab-cdef-0123-456789abcdef/assign
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "toStaffId": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
  "notifyProvider": true,
  "notificationMethod": "push",
  "message": "Urgent: Patient transfer to Med/Surg floor"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "handoff": {
      "id": "h1234567-89ab-cdef-0123-456789abcdef",
      "status": "assigned",
      "toStaffId": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d"
    },
    "assignment": {
      "id": "assign_abc123",
      "staffId": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
      "role": "receiving",
      "status": "notified",
      "notifiedAt": "2025-10-23T22:52:00Z",
      "notificationMethod": "push"
    },
    "notification": {
      "id": "notif_def456",
      "sent": true,
      "sentAt": "2025-10-23T22:52:00Z"
    }
  }
}
```

---

### 2.6 POST /v1/handoffs/:id/complete

Mark handoff as completed.

**Endpoint:**
```
POST /v1/handoffs/{handoffId}/complete
```

**Authentication:** Required  
**Permission:** `handoff:update`

**Request:**
```http
POST /v1/handoffs/h1234567-89ab-cdef-0123-456789abcdef/complete
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "completionNotes": "Handoff completed successfully. Receiving nurse briefed on patient status and current medications. All questions answered.",
  "actualTime": "2025-10-24T07:15:00Z"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "h1234567-89ab-cdef-0123-456789abcdef",
    "status": "completed",
    "completedAt": "2025-10-24T07:15:00Z",
    "actualTime": "2025-10-24T07:15:00Z",
    "completionNotes": "Handoff completed successfully. Receiving nurse briefed on patient status and current medications. All questions answered.",
    "updatedAt": "2025-10-24T07:15:00Z"
  }
}
```

---

### 2.7 DELETE /v1/handoffs/:id

Cancel or delete a handoff.

**Endpoint:**
```
DELETE /v1/handoffs/{handoffId}
```

**Authentication:** Required  
**Permission:** `handoff:delete`

**Request:**
```http
DELETE /v1/handoffs/h1234567-89ab-cdef-0123-456789abcdef
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "cancellationReason": "Patient discharged before handoff could be completed"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Handoff cancelled successfully",
  "data": {
    "id": "h1234567-89ab-cdef-0123-456789abcdef",
    "status": "cancelled",
    "cancelledAt": "2025-10-23T23:00:00Z",
    "cancellationReason": "Patient discharged before handoff could be completed"
  }
}
```

---

## 3. Voice Recording Endpoints

### 3.1 POST /v1/voice/upload

Upload voice recording for transcription.

**Endpoint:**
```
POST /v1/voice/upload
```

**Authentication:** Required  
**Permission:** `voice:upload`

**Request (multipart/form-data):**
```http
POST /v1/voice/upload
Authorization: Bearer {accessToken}
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="handoffId"

h1234567-89ab-cdef-0123-456789abcdef
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="audio"; filename="recording.webm"
Content-Type: audio/webm

[binary audio data]
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="duration"

185
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

**Form Fields:**
- `handoffId` (required) - UUID of associated handoff
- `audio` (required) - Audio file (max 10MB)
- `duration` (required) - Recording duration in seconds

**Accepted Audio Formats:**
- `audio/webm` (preferred)
- `audio/mp3`
- `audio/wav`
- `audio/ogg`
- `audio/m4a`

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "recordingId": "v1234567-89ab-cdef-0123-456789abcdef",
    "handoffId": "h1234567-89ab-cdef-0123-456789abcdef",
    "duration": 185,
    "fileSize": 2048000,
    "audioFormat": "webm",
    "status": "uploaded",
    "filePath": "2025/10/f47ac10b-58cc-4372-a567-0e02b2c3d479/v1234567-89ab-cdef-0123-456789abcdef.webm",
    "transcriptionJobId": "job_abc123",
    "estimatedProcessingTime": 30,
    "uploadedAt": "2025-10-23T22:32:00Z",
    "message": "Voice recording uploaded successfully. Transcription will begin shortly."
  }
}
```

**Error Responses:**

**400 Bad Request - File Too Large:**
```json
{
  "success": false,
  "error": {
    "code": "FILE_TOO_LARGE",
    "message": "Audio file exceeds maximum size of 10MB",
    "details": {
      "maxSize": 10485760,
      "actualSize": 15728640
    }
  }
}
```

**400 Bad Request - Invalid Format:**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_FILE_FORMAT",
    "message": "Unsupported audio format",
    "details": {
      "supportedFormats": ["audio/webm", "audio/mp3", "audio/wav", "audio/ogg", "audio/m4a"],
      "receivedFormat": "video/mp4"
    }
  }
}
```

---

### 3.2 GET /v1/voice/:id

Get voice recording details.

**Endpoint:**
```
GET /v1/voice/{recordingId}
```

**Authentication:** Required  
**Permission:** `voice:read`

**Request:**
```http
GET /v1/voice/v1234567-89ab-cdef-0123-456789abcdef
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "v1234567-89ab-cdef-0123-456789abcdef",
    "handoffId": "h1234567-89ab-cdef-0123-456789abcdef",
    "uploadedBy": {
      "id": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
      "firstName": "John",
      "lastName": "Doe"
    },
    "duration": 185,
    "fileSize": 2048000,
    "audioFormat": "webm",
    "sampleRate": 48000,
    "bitRate": 128,
    "channels": 1,
    "status": "transcribed",
    "filePath": "2025/10/f47ac10b-58cc-4372-a567-0e02b2c3d479/v1234567-89ab-cdef-0123-456789abcdef.webm",
    "fileUrl": "https://eclipselink-production.r2.cloudflarestorage.com/2025/10/f47ac10b-58cc-4372-a567-0e02b2c3d479/v1234567-89ab-cdef-0123-456789abcdef.webm?X-Amz-Signature=...",
    "fileUrlExpiresAt": "2025-10-23T23:02:00Z",
    "transcriptionJobId": "job_abc123",
    "transcriptionAttempts": 1,
    "audioQualityScore": 0.92,
    "silencePercentage": 5.3,
    "noiseLevel": 12.5,
    "recordedAt": "2025-10-23T22:30:00Z",
    "uploadedAt": "2025-10-23T22:32:00Z",
    "processedAt": "2025-10-23T22:33:15Z",
    "createdAt": "2025-10-23T22:32:00Z"
  }
}
```

---

### 3.3 GET /v1/voice/:id/download

Get presigned URL for audio download.

**Endpoint:**
```
GET /v1/voice/{recordingId}/download
```

**Authentication:** Required  
**Permission:** `voice:read`

**Request:**
```http
GET /v1/voice/v1234567-89ab-cdef-0123-456789abcdef/download
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "downloadUrl": "https://eclipselink-production.r2.cloudflarestorage.com/2025/10/f47ac10b-58cc-4372-a567-0e02b2c3d479/v1234567-89ab-cdef-0123-456789abcdef.webm?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...&X-Amz-Date=20251023T223000Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature=...",
    "expiresAt": "2025-10-23T23:02:00Z",
    "expiresIn": 900,
    "fileName": "recording-v1234567.webm",
    "fileSize": 2048000,
    "contentType": "audio/webm"
  }
}
```

**Usage Note:** The presigned URL is valid for 15 minutes. Use it to download or stream the audio file.

---

### 3.4 GET /v1/voice/:id/status

Get transcription/processing status.

**Endpoint:**
```
GET /v1/voice/{recordingId}/status
```

**Authentication:** Required  
**Permission:** `voice:read`

**Request:**
```http
GET /v1/voice/v1234567-89ab-cdef-0123-456789abcdef/status
Authorization: Bearer {accessToken}
```

**Response (200 OK) - Processing:**
```json
{
  "success": true,
  "data": {
    "recordingId": "v1234567-89ab-cdef-0123-456789abcdef",
    "status": "processing",
    "stage": "transcription",
    "progress": 45,
    "transcriptionJobId": "job_abc123",
    "startedAt": "2025-10-23T22:32:30Z",
    "estimatedCompletionAt": "2025-10-23T22:33:00Z",
    "message": "Transcribing audio with Azure Whisper API..."
  }
}
```

**Response (200 OK) - Completed:**
```json
{
  "success": true,
  "data": {
    "recordingId": "v1234567-89ab-cdef-0123-456789abcdef",
    "status": "transcribed",
    "stage": "completed",
    "progress": 100,
    "transcriptionJobId": "job_abc123",
    "startedAt": "2025-10-23T22:32:30Z",
    "completedAt": "2025-10-23T22:33:15Z",
    "processingDuration": 45,
    "transcription": {
      "text": "Patient is a 60-year-old female with type 2 diabetes admitted three days ago for hyperglycemia...",
      "confidence": 0.96,
      "wordCount": 385,
      "language": "en"
    },
    "nextStep": "sbar_generation",
    "message": "Transcription completed successfully. SBAR generation in progress..."
  }
}
```

**Response (200 OK) - Failed:**
```json
{
  "success": true,
  "data": {
    "recordingId": "v1234567-89ab-cdef-0123-456789abcdef",
    "status": "failed",
    "stage": "transcription",
    "progress": 0,
    "transcriptionJobId": "job_abc123",
    "startedAt": "2025-10-23T22:32:30Z",
    "failedAt": "2025-10-23T22:32:45Z",
    "attemptNumber": 3,
    "maxAttempts": 3,
    "error": {
      "code": "TRANSCRIPTION_FAILED",
      "message": "Audio quality insufficient for transcription",
      "details": {
        "audioQualityScore": 0.35,
        "minimumRequired": 0.50
      }
    },
    "retryAvailable": false,
    "message": "Transcription failed after 3 attempts. Please re-record with better audio quality."
  }
}
```

---

### 3.5 DELETE /v1/voice/:id

Delete voice recording.

**Endpoint:**
```
DELETE /v1/voice/{recordingId}
```

**Authentication:** Required  
**Permission:** `voice:delete`

**Request:**
```http
DELETE /v1/voice/v1234567-89ab-cdef-0123-456789abcdef
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Voice recording deleted successfully",
  "data": {
    "recordingId": "v1234567-89ab-cdef-0123-456789abcdef",
    "deletedAt": "2025-10-23T23:05:00Z"
  }
}
```

---

## 4. Real-Time Status Polling

### 4.1 Polling Strategy

For real-time updates on voice processing, implement exponential backoff polling:

**Polling Intervals:**
```
Initial: 2 seconds
After 30s: 5 seconds
After 60s: 10 seconds
After 120s: 15 seconds
Maximum: 5 minutes
```

**JavaScript Example:**
```typescript
async function pollVoiceStatus(recordingId: string): Promise<VoiceStatus> {
  let attempts = 0;
  const maxAttempts = 60; // 5 minutes max
  
  const getDelay = (attempt: number): number => {
    if (attempt < 15) return 2000;      // 2s for first 30s
    if (attempt < 24) return 5000;      // 5s for next 45s
    if (attempt < 36) return 10000;     // 10s for next 2min
    return 15000;                        // 15s after that
  };
  
  while (attempts < maxAttempts) {
    const response = await api.get(`/voice/${recordingId}/status`);
    const status = response.data.data;
    
    if (status.status === 'transcribed' || status.status === 'failed') {
      return status;
    }
    
    attempts++;
    await new Promise(resolve => setTimeout(resolve, getDelay(attempts)));
  }
  
  throw new Error('Polling timeout after 5 minutes');
}
```

### 4.2 WebSocket Alternative (Future)

For real-time updates without polling, WebSocket support is planned:

```typescript
// Future implementation
const ws = new WebSocket('wss://api.eclipselink.ai/v1/ws');

ws.on('connect', () => {
  ws.send(JSON.stringify({
    type: 'subscribe',
    channel: `voice:${recordingId}:status`
  }));
});

ws.on('message', (data) => {
  const update = JSON.parse(data);
  console.log('Status update:', update);
});
```

---

## 5. Batch Operations

### 5.1 GET /v1/handoffs/batch

Get multiple handoffs by IDs.

**Endpoint:**
```
GET /v1/handoffs/batch?ids={id1},{id2},{id3}
```

**Authentication:** Required  
**Permission:** `handoff:read`

**Request:**
```http
GET /v1/handoffs/batch?ids=h1234567-89ab-cdef-0123-456789abcdef,h2345678-90ab-cdef-0123-456789abcdef,h3456789-01ab-cdef-0123-456789abcdef
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "handoffs": [
      { "id": "h1234567-89ab-cdef-0123-456789abcdef", /* ... */ },
      { "id": "h2345678-90ab-cdef-0123-456789abcdef", /* ... */ },
      { "id": "h3456789-01ab-cdef-0123-456789abcdef", /* ... */ }
    ],
    "notFound": []
  }
}
```

---

## Summary

### ✅ Part 4B Covers:

1. **Handoff Lifecycle** - Complete state machine and transitions
2. **Handoff Endpoints** - 7 endpoints for full CRUD operations
3. **Voice Endpoints** - 5 endpoints for upload, status, and download
4. **Polling Strategy** - Efficient real-time status updates
5. **Batch Operations** - Multi-resource queries

### 📊 Endpoints Summary:

**Handoff Endpoints (7):**
1. POST /v1/handoffs - Create handoff
2. GET /v1/handoffs - List with filters
3. GET /v1/handoffs/:id - Get details
4. PUT /v1/handoffs/:id - Update
5. POST /v1/handoffs/:id/assign - Assign to provider
6. POST /v1/handoffs/:id/complete - Complete handoff
7. DELETE /v1/handoffs/:id - Cancel/delete

**Voice Recording Endpoints (5):**
1. POST /v1/voice/upload - Upload audio
2. GET /v1/voice/:id - Get recording details
3. GET /v1/voice/:id/download - Get presigned URL
4. GET /v1/voice/:id/status - Poll processing status
5. DELETE /v1/voice/:id - Delete recording

---

**Next:** Part 4C will cover Patient & SBAR endpoints.

---

*EclipseLink AI™ is a product of Rohimaya Health AI*  
*© 2025 Rohimaya Health AI. All rights reserved.*
