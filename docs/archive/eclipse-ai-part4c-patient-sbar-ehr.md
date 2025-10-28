# EclipseLink AI™ - Part 4C: Patient, SBAR & EHR Integration Endpoints

**Document Version:** 1.0  
**Last Updated:** October 23, 2025  
**Product:** EclipseLink AI™ Clinical Handoff System  
**Company:** Rohimaya Health AI  
**Founders:** Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO)

---

## Table of Contents

1. [Handoff Workflow Patterns](#handoff-workflow-patterns)
2. [Patient Management Endpoints](#patient-management-endpoints)
3. [SBAR Report Endpoints](#sbar-report-endpoints)
4. [EHR Integration Endpoints](#ehr-integration-endpoints)
5. [Analytics & Reporting Endpoints](#analytics-reporting-endpoints)

---

## 1. Handoff Workflow Patterns

### 1.1 Initial vs. Update Handoffs - Critical Distinction

EclipseLink AI supports two distinct handoff patterns:

#### **Pattern A: Initial Handoff (Baseline)**
Used when:
- Patient is first admitted
- Product is newly implemented for an existing patient
- Complete patient assessment is needed
- No previous handoff exists

**Characteristics:**
- Full SBAR created from scratch
- Voice recording contains comprehensive patient assessment
- All sections (S.B.A.R.) fully populated
- Becomes the "baseline" for future updates

#### **Pattern B: Update Handoff (Delta)**
Used when:
- Shift changes
- Patient status changes
- Transfer between units
- Previous handoff exists

**Characteristics:**
- Links to previous handoff
- Voice recording focuses on "what's changed"
- AI appends/updates existing SBAR
- More efficient - no repetition of stable information
- Maintains version history

### 1.2 Workflow Comparison

```
┌─────────────────────────────────────────────────────────────┐
│                    INITIAL HANDOFF                          │
│                  (First Time Setup)                         │
└─────────────────────────────────────────────────────────────┘

1. Patient Admitted
   ↓
2. Nurse creates handoff (handoffType: "admission")
   ↓
3. System checks: Is there a previous handoff? NO
   ↓
4. Voice recording prompt: "Provide complete patient assessment"
   ↓
5. AI generates FULL SBAR:
   • Situation: Current status, vitals, chief complaint
   • Background: Medical history, medications, allergies
   • Assessment: Clinical findings, lab results
   • Recommendation: Treatment plan, follow-up
   ↓
6. SBAR Version 1 created
   ↓
7. Status: "ready" (baseline established)


┌─────────────────────────────────────────────────────────────┐
│                    UPDATE HANDOFF                           │
│                  (Subsequent Changes)                       │
└─────────────────────────────────────────────────────────────┘

1. Shift change OR status change
   ↓
2. Nurse creates handoff (previousHandoffId provided)
   ↓
3. System checks: Previous handoff exists? YES
   ↓
4. System retrieves latest SBAR (Version N)
   ↓
5. Voice recording prompt: "Describe changes since last handoff"
   ↓
6. AI processes UPDATE:
   • Identifies what changed
   • Keeps stable information
   • Updates only changed sections
   • Adds new information
   ↓
7. SBAR Version N+1 created
   ↓
8. Status: "ready" (update complete)
```

### 1.3 API Endpoint Design

The API intelligently handles both patterns through a **single unified endpoint** that detects context:

**Single Endpoint (Context-Aware):**
```http
POST /v1/handoffs
```

**Initial Handoff Request:**
```json
{
  "patientId": "p1234567-89ab-cdef-0123-456789abcdef",
  "fromStaffId": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "handoffType": "admission",
  "priority": "routine",
  "isInitialHandoff": true,  // Explicit flag
  "previousHandoffId": null  // No previous
}
```

**Update Handoff Request:**
```json
{
  "patientId": "p1234567-89ab-cdef-0123-456789abcdef",
  "fromStaffId": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
  "toStaffId": "c5d4e3f2-a1b2-3c4d-5e6f-7a8b9c0d1e2f",
  "handoffType": "shift_change",
  "priority": "routine",
  "isInitialHandoff": false,  // Explicit flag
  "previousHandoffId": "h1234567-89ab-cdef-0123-456789abcdef"  // Links to baseline
}
```

### 1.4 Backend Logic Flow

```typescript
// Backend pseudocode
async function createHandoff(data) {
  // Check if this is initial or update
  const isInitial = data.isInitialHandoff || !data.previousHandoffId;
  
  if (isInitial) {
    // INITIAL HANDOFF PATH
    return {
      aiPromptType: "initial_assessment",
      systemPrompt: "Generate a comprehensive SBAR from the complete patient assessment",
      sbarGeneration: "full",
      linkToPrevious: null
    };
  } else {
    // UPDATE HANDOFF PATH
    const previousHandoff = await getHandoff(data.previousHandoffId);
    const previousSbar = await getSbarReport(previousHandoff.sbarId);
    
    return {
      aiPromptType: "update_assessment",
      systemPrompt: "Generate SBAR updates based on changes since last handoff",
      sbarGeneration: "incremental",
      linkToPrevious: data.previousHandoffId,
      previousSbarContext: previousSbar
    };
  }
}
```

### 1.5 Voice Recording Prompts

**Initial Handoff (UI Prompt):**
```
Please provide a complete patient assessment including:
• Current condition and vital signs
• Medical history and diagnoses
• Current medications and allergies
• Recent events and interventions
• Assessment and plan of care
```

**Update Handoff (UI Prompt):**
```
Please describe changes since the last handoff:
• Changes in patient condition
• New vital signs or lab results
• Medication changes
• New events or interventions
• Updates to plan of care

(Stable information will be carried over automatically)
```

### 1.6 SBAR Versioning

Each SBAR update creates a new version while maintaining history:

```json
{
  "sbarReport": {
    "id": "s1234567-89ab-cdef-0123-456789abcdef",
    "handoffId": "h9876543-21ba-fedc-3210-fedcba987654",
    "version": 3,  // Current version
    "previousVersionId": "s2345678-90ab-cdef-0123-456789abcdef",
    "isLatest": true,
    "isInitial": false,
    
    "situation": "60yo female with T2DM, glucose improved to 110 mg/dL (was 145)",
    "background": "[Unchanged from v2]",  // Carried over
    "assessment": "Blood glucose now well-controlled with current regimen. Patient reports no symptoms.",
    "recommendation": "Continue current insulin dosing. Discharge planned for tomorrow AM.",
    
    "changesSinceLastVersion": [
      {
        "section": "situation",
        "type": "update",
        "previousValue": "glucose 145 mg/dL",
        "newValue": "glucose improved to 110 mg/dL"
      },
      {
        "section": "recommendation",
        "type": "update",
        "previousValue": "Consider discharge in 24 hours",
        "newValue": "Discharge planned for tomorrow AM"
      }
    ],
    
    "createdAt": "2025-10-24T07:10:00Z"
  }
}
```

---

## 2. Patient Management Endpoints

### 2.1 GET /v1/patients

List patients with search, filtering, and pagination.

**Endpoint:**
```
GET /v1/patients
```

**Authentication:** Required  
**Permission:** `patient:read`

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number (1-indexed) |
| limit | integer | 20 | Items per page (max 100) |
| search | string | - | Search by name, MRN, room |
| status | string | active | Filter by status |
| admissionDateStart | ISO 8601 | - | Filter by admission date (start) |
| admissionDateEnd | ISO 8601 | - | Filter by admission date (end) |
| department | string | - | Filter by department |
| hasInitialHandoff | boolean | - | Filter by handoff status |
| sortBy | string | lastName | Sort field |
| sortOrder | string | asc | Sort order (asc/desc) |

**Request:**
```http
GET /v1/patients?status=active&hasInitialHandoff=false&page=1&limit=20
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "patients": [
      {
        "id": "p1234567-89ab-cdef-0123-456789abcdef",
        "mrn": "MRN123456",
        "firstName": "Jane",
        "lastName": "Smith",
        "dateOfBirth": "1965-03-15",
        "age": 60,
        "gender": "female",
        "status": "active",
        "admissionDate": "2025-10-20T14:30:00Z",
        "roomNumber": "305",
        "department": "Medical/Surgical",
        "primaryDiagnosis": "Type 2 Diabetes Mellitus",
        "assignedProvider": {
          "id": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
          "firstName": "John",
          "lastName": "Doe",
          "role": "registered_nurse"
        },
        "handoffStatus": {
          "hasInitialHandoff": true,
          "totalHandoffs": 4,
          "latestHandoffId": "h9876543-21ba-fedc-3210-fedcba987654",
          "latestHandoffDate": "2025-10-24T07:00:00Z",
          "currentSbarVersion": 4
        },
        "acuityLevel": "moderate",
        "updatedAt": "2025-10-24T07:10:00Z"
      },
      {
        "id": "p2345678-90ab-cdef-0123-456789abcdef",
        "mrn": "MRN789012",
        "firstName": "Robert",
        "lastName": "Johnson",
        "dateOfBirth": "1980-07-22",
        "age": 45,
        "gender": "male",
        "status": "active",
        "admissionDate": "2025-10-24T06:00:00Z",
        "roomNumber": "412",
        "department": "Emergency Department",
        "primaryDiagnosis": "Community-Acquired Pneumonia",
        "assignedProvider": {
          "id": "c5d4e3f2-a1b2-3c4d-5e6f-7a8b9c0d1e2f",
          "firstName": "Emily",
          "lastName": "Brown",
          "role": "physician"
        },
        "handoffStatus": {
          "hasInitialHandoff": false,  // ⚠️ Needs initial handoff
          "totalHandoffs": 0,
          "latestHandoffId": null,
          "latestHandoffDate": null,
          "currentSbarVersion": 0
        },
        "acuityLevel": "high",
        "updatedAt": "2025-10-24T06:15:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 147,
      "totalPages": 8
    },
    "summary": {
      "totalPatients": 147,
      "needsInitialHandoff": 12,  // Patients without baseline
      "hasInitialHandoff": 135
    }
  }
}
```

---

### 2.2 GET /v1/patients/:id

Get detailed patient information.

**Endpoint:**
```
GET /v1/patients/{patientId}
```

**Authentication:** Required  
**Permission:** `patient:read`

**Request:**
```http
GET /v1/patients/p1234567-89ab-cdef-0123-456789abcdef
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "p1234567-89ab-cdef-0123-456789abcdef",
    "mrn": "MRN123456",
    "facilityId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    
    "demographics": {
      "firstName": "Jane",
      "lastName": "Smith",
      "middleName": "Marie",
      "dateOfBirth": "1965-03-15",
      "age": 60,
      "gender": "female",
      "race": "White",
      "ethnicity": "Not Hispanic or Latino",
      "maritalStatus": "Married",
      "preferredLanguage": "en"
    },
    
    "contact": {
      "phone": "+13035551234",
      "email": "jane.smith@email.com",
      "address": {
        "line1": "123 Main Street",
        "city": "Denver",
        "state": "CO",
        "zipCode": "80202"
      }
    },
    
    "emergencyContact": {
      "name": "John Smith",
      "relationship": "Spouse",
      "phone": "+13035555678"
    },
    
    "admission": {
      "admissionDate": "2025-10-20T14:30:00Z",
      "admissionType": "Emergency",
      "roomNumber": "305",
      "bedNumber": "A",
      "department": "Medical/Surgical",
      "expectedDischargeDate": "2025-10-25T00:00:00Z"
    },
    
    "clinical": {
      "status": "active",
      "acuityLevel": "moderate",
      "bloodType": "A+",
      "weight": 165,
      "weightUnit": "lbs",
      "height": 64,
      "heightUnit": "in"
    },
    
    "primaryDiagnosis": "Type 2 Diabetes Mellitus",
    "secondaryDiagnoses": [
      "Essential Hypertension",
      "Hyperlipidemia"
    ],
    
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
      "bpSystolic": 130,
      "bpDiastolic": 85,
      "heartRate": 78,
      "respiratoryRate": 16,
      "oxygenSaturation": 98,
      "recordedAt": "2025-10-24T06:00:00Z"
    },
    
    "handoffHistory": {
      "hasInitialHandoff": true,
      "initialHandoffId": "h1234567-89ab-cdef-0123-456789abcdef",
      "initialHandoffDate": "2025-10-20T15:00:00Z",
      "totalHandoffs": 4,
      "latestHandoffId": "h9876543-21ba-fedc-3210-fedcba987654",
      "latestHandoffDate": "2025-10-24T07:00:00Z",
      "currentSbarVersion": 4,
      "recentHandoffs": [
        {
          "id": "h9876543-21ba-fedc-3210-fedcba987654",
          "type": "shift_change",
          "isInitial": false,
          "sbarVersion": 4,
          "createdAt": "2025-10-24T07:00:00Z"
        },
        {
          "id": "h8765432-10ba-fedc-3210-fedcba987654",
          "type": "status_update",
          "isInitial": false,
          "sbarVersion": 3,
          "createdAt": "2025-10-23T19:00:00Z"
        },
        {
          "id": "h7654321-09ba-fedc-3210-fedcba987654",
          "type": "shift_change",
          "isInitial": false,
          "sbarVersion": 2,
          "createdAt": "2025-10-23T07:00:00Z"
        },
        {
          "id": "h1234567-89ab-cdef-0123-456789abcdef",
          "type": "admission",
          "isInitial": true,
          "sbarVersion": 1,
          "createdAt": "2025-10-20T15:00:00Z"
        }
      ]
    },
    
    "createdAt": "2025-10-20T14:30:00Z",
    "updatedAt": "2025-10-24T07:10:00Z"
  }
}
```

---

### 2.3 GET /v1/patients/:id/handoffs

Get patient's complete handoff history with SBAR evolution.

**Endpoint:**
```
GET /v1/patients/{patientId}/handoffs
```

**Authentication:** Required  
**Permission:** `patient:read`, `handoff:read`

**Query Parameters:**
- `includeInitial` (boolean, default: true) - Include initial handoff
- `includeUpdates` (boolean, default: true) - Include update handoffs
- `includeSbar` (boolean, default: false) - Include full SBAR in each handoff
- `limit` (integer, default: 10) - Number of handoffs to return

**Request:**
```http
GET /v1/patients/p1234567-89ab-cdef-0123-456789abcdef/handoffs?includeSbar=true&limit=5
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "patient": {
      "id": "p1234567-89ab-cdef-0123-456789abcdef",
      "name": "Jane Smith",
      "mrn": "MRN123456"
    },
    "handoffTimeline": [
      {
        "id": "h9876543-21ba-fedc-3210-fedcba987654",
        "handoffType": "shift_change",
        "isInitialHandoff": false,
        "previousHandoffId": "h8765432-10ba-fedc-3210-fedcba987654",
        "priority": "routine",
        "status": "completed",
        "fromStaff": {
          "name": "Sarah Johnson",
          "role": "registered_nurse"
        },
        "toStaff": {
          "name": "Michael Chen",
          "role": "registered_nurse"
        },
        "sbarReport": {
          "id": "s9876543-21ba-fedc-3210-fedcba987654",
          "version": 4,
          "isLatest": true,
          "situation": "60yo female with T2DM, glucose improved to 110 mg/dL",
          "background": "[Stable - see v1]",
          "assessment": "Blood glucose now well-controlled. No symptoms.",
          "recommendation": "Continue insulin. Discharge planned tomorrow.",
          "changesSinceLastVersion": [
            {
              "section": "situation",
              "change": "Glucose improved from 145 to 110 mg/dL"
            },
            {
              "section": "recommendation",
              "change": "Discharge date confirmed for tomorrow"
            }
          ]
        },
        "createdAt": "2025-10-24T07:00:00Z",
        "completedAt": "2025-10-24T07:15:00Z"
      },
      {
        "id": "h8765432-10ba-fedc-3210-fedcba987654",
        "handoffType": "status_update",
        "isInitialHandoff": false,
        "previousHandoffId": "h7654321-09ba-fedc-3210-fedcba987654",
        "priority": "routine",
        "status": "completed",
        "fromStaff": {
          "name": "John Doe",
          "role": "registered_nurse"
        },
        "sbarReport": {
          "id": "s8765432-10ba-fedc-3210-fedcba987654",
          "version": 3,
          "situation": "60yo female with T2DM, current glucose 145 mg/dL",
          "background": "[Stable - see v1]",
          "assessment": "Blood glucose trending downward with insulin regimen.",
          "recommendation": "Continue current insulin. Consider discharge in 24h.",
          "changesSinceLastVersion": [
            {
              "section": "assessment",
              "change": "Added note about glucose trending downward"
            }
          ]
        },
        "createdAt": "2025-10-23T19:00:00Z",
        "completedAt": "2025-10-23T19:10:00Z"
      },
      {
        "id": "h1234567-89ab-cdef-0123-456789abcdef",
        "handoffType": "admission",
        "isInitialHandoff": true,  // 🎯 INITIAL/BASELINE
        "previousHandoffId": null,
        "priority": "urgent",
        "status": "completed",
        "fromStaff": {
          "name": "John Doe",
          "role": "registered_nurse"
        },
        "sbarReport": {
          "id": "s1234567-89ab-cdef-0123-456789abcdef",
          "version": 1,
          "isInitial": true,
          "situation": "60yo female with T2DM admitted for hyperglycemia. Alert, oriented x3. Current glucose 320 mg/dL.",
          "background": "PMH: T2DM x10yrs, HTN, hyperlipidemia. Home meds: Metformin 1000mg BID, Lisinopril 10mg daily. Allergy: PCN (rash). Lives with spouse, independent ADLs.",
          "assessment": "VS: T 98.6°F, BP 145/90, HR 88, RR 18, SpO2 97% RA. Hyperglycemic crisis. Patient reports polyuria, polydipsia x 3 days. Last HbA1c 9.8%.",
          "recommendation": "Start insulin drip per protocol. Monitor glucose q1h. DM education. Endocrine consult requested. Admit to Med/Surg.",
          "changesSinceLastVersion": null  // No previous version
        },
        "createdAt": "2025-10-20T15:00:00Z",
        "completedAt": "2025-10-20T15:20:00Z"
      }
    ],
    "summary": {
      "totalHandoffs": 4,
      "initialHandoff": {
        "id": "h1234567-89ab-cdef-0123-456789abcdef",
        "date": "2025-10-20T15:00:00Z"
      },
      "updateHandoffs": 3,
      "currentSbarVersion": 4,
      "daysSinceAdmission": 4
    }
  }
}
```

---

## 3. SBAR Report Endpoints

### 3.1 GET /v1/sbar/:handoffId

Get SBAR report for a specific handoff.

**Endpoint:**
```
GET /v1/sbar/{handoffId}
```

**Authentication:** Required  
**Permission:** `sbar:read`

**Request:**
```http
GET /v1/sbar/h9876543-21ba-fedc-3210-fedcba987654
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "s9876543-21ba-fedc-3210-fedcba987654",
    "handoffId": "h9876543-21ba-fedc-3210-fedcba987654",
    "patientId": "p1234567-89ab-cdef-0123-456789abcdef",
    
    "version": 4,
    "previousVersionId": "s8765432-10ba-fedc-3210-fedcba987654",
    "isLatest": true,
    "isInitial": false,
    
    "situation": "60-year-old female with type 2 diabetes mellitus. Blood glucose improved to 110 mg/dL (down from 145 mg/dL). Patient alert and oriented x3. No acute distress.",
    
    "background": "Past medical history includes type 2 diabetes (10 years), essential hypertension, and hyperlipidemia. Home medications: Metformin 1000mg BID, Lisinopril 10mg daily. Known allergy to Penicillin (rash). Patient lives at home with spouse, independent with ADLs. Admitted 4 days ago for hyperglycemia (initial glucose 320 mg/dL).",
    
    "assessment": "Current vital signs: Temperature 98.6°F, BP 130/85, HR 78, RR 16, SpO2 98% on room air. Blood glucose now well-controlled with current insulin regimen. Patient reports no symptoms, decreased thirst, improved energy. Tolerating regular diet. Ambulating without assistance. No skin breakdown. Recent labs: HbA1c 8.2%.",
    
    "recommendation": "Continue current insulin sliding scale. Discharge education completed - patient verbalizes understanding of home glucose monitoring and medication regimen. Discharge planned for tomorrow morning. Follow-up appointment scheduled with endocrinology in 2 weeks (Nov 6). Continue home medications upon discharge. Patient received written discharge instructions.",
    
    "currentStatus": "Stable, improving, ready for discharge",
    
    "vitalSigns": {
      "temperature": 98.6,
      "bpSystolic": 130,
      "bpDiastolic": 85,
      "heartRate": 78,
      "respiratoryRate": 16,
      "oxygenSaturation": 98,
      "recordedAt": "2025-10-24T06:00:00Z"
    },
    
    "medications": [
      {
        "name": "Insulin sliding scale",
        "dose": "Per protocol",
        "frequency": "QID with meals and bedtime",
        "status": "active"
      },
      {
        "name": "Metformin",
        "dose": "1000mg",
        "frequency": "Twice daily",
        "status": "home_medication"
      },
      {
        "name": "Lisinopril",
        "dose": "10mg",
        "frequency": "Once daily",
        "status": "home_medication"
      }
    ],
    
    "allergies": [
      {
        "allergen": "Penicillin",
        "reaction": "Rash",
        "severity": "Moderate"
      }
    ],
    
    "pendingTasks": [
      "Final discharge teaching",
      "Arrange transportation home",
      "Provide written discharge instructions"
    ],
    
    "changesSinceLastVersion": [
      {
        "section": "situation",
        "type": "update",
        "field": "bloodGlucose",
        "previousValue": "145 mg/dL",
        "newValue": "110 mg/dL",
        "timestamp": "2025-10-24T07:00:00Z"
      },
      {
        "section": "recommendation",
        "type": "update",
        "field": "dischargeStatus",
        "previousValue": "Consider discharge in 24 hours",
        "newValue": "Discharge planned for tomorrow morning",
        "timestamp": "2025-10-24T07:00:00Z"
      },
      {
        "section": "recommendation",
        "type": "addition",
        "field": "followUpAppointment",
        "newValue": "Follow-up scheduled Nov 6 with endocrinology",
        "timestamp": "2025-10-24T07:00:00Z"
      }
    ],
    
    "qualityMetrics": {
      "completenessScore": 0.98,
      "readabilityScore": 0.92,
      "adherenceToIPassFramework": true,
      "jointCommissionCompliance": true
    },
    
    "aiGeneration": {
      "model": "gpt-4",
      "transcriptionSource": "v9876543-21ba-fedc-3210-fedcba987654",
      "generationType": "update",  // vs "initial"
      "processingDuration": 15,
      "confidenceScore": 0.96
    },
    
    "editHistory": [
      {
        "editedBy": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
        "editedAt": "2025-10-24T07:08:00Z",
        "section": "recommendation",
        "change": "Added specific follow-up date"
      }
    ],
    
    "createdAt": "2025-10-24T07:05:00Z",
    "updatedAt": "2025-10-24T07:08:00Z"
  }
}
```

---

### 3.2 GET /v1/sbar/:handoffId/versions

Get all SBAR versions for a patient's handoff chain.

**Endpoint:**
```
GET /v1/sbar/{handoffId}/versions
```

**Authentication:** Required  
**Permission:** `sbar:read`

**Query Parameters:**
- `includeChanges` (boolean, default: true) - Include change history

**Request:**
```http
GET /v1/sbar/h9876543-21ba-fedc-3210-fedcba987654/versions?includeChanges=true
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "patient": {
      "id": "p1234567-89ab-cdef-0123-456789abcdef",
      "name": "Jane Smith",
      "mrn": "MRN123456"
    },
    "versions": [
      {
        "version": 4,
        "id": "s9876543-21ba-fedc-3210-fedcba987654",
        "handoffId": "h9876543-21ba-fedc-3210-fedcba987654",
        "isLatest": true,
        "isInitial": false,
        "createdAt": "2025-10-24T07:05:00Z",
        "createdBy": "Sarah Johnson (RN)",
        "summary": "Glucose improved to 110, discharge tomorrow",
        "changeCount": 3
      },
      {
        "version": 3,
        "id": "s8765432-10ba-fedc-3210-fedcba987654",
        "handoffId": "h8765432-10ba-fedc-3210-fedcba987654",
        "isLatest": false,
        "isInitial": false,
        "createdAt": "2025-10-23T19:05:00Z",
        "createdBy": "John Doe (RN)",
        "summary": "Glucose trending down, considering discharge",
        "changeCount": 1
      },
      {
        "version": 2,
        "id": "s7654321-09ba-fedc-3210-fedcba987654",
        "handoffId": "h7654321-09ba-fedc-3210-fedcba987654",
        "isLatest": false,
        "isInitial": false,
        "createdAt": "2025-10-23T07:05:00Z",
        "createdBy": "Michael Chen (RN)",
        "summary": "Stable on insulin, education ongoing",
        "changeCount": 2
      },
      {
        "version": 1,
        "id": "s1234567-89ab-cdef-0123-456789abcdef",
        "handoffId": "h1234567-89ab-cdef-0123-456789abcdef",
        "isLatest": false,
        "isInitial": true,  // 🎯 BASELINE VERSION
        "createdAt": "2025-10-20T15:05:00Z",
        "createdBy": "John Doe (RN)",
        "summary": "Initial admission - hyperglycemia",
        "changeCount": null  // No changes (initial)
      }
    ],
    "versionTree": {
      "initial": "s1234567-89ab-cdef-0123-456789abcdef",
      "updates": [
        "s7654321-09ba-fedc-3210-fedcba987654",
        "s8765432-10ba-fedc-3210-fedcba987654",
        "s9876543-21ba-fedc-3210-fedcba987654"
      ],
      "current": "s9876543-21ba-fedc-3210-fedcba987654"
    },
    "totalVersions": 4,
    "daysSinceInitial": 4
  }
}
```

---

### 3.3 GET /v1/sbar/:id/compare

Compare two SBAR versions to see what changed.

**Endpoint:**
```
GET /v1/sbar/{sbarId}/compare?compareWith={otherSbarId}
```

**Authentication:** Required  
**Permission:** `sbar:read`

**Request:**
```http
GET /v1/sbar/s9876543-21ba-fedc-3210-fedcba987654/compare?compareWith=s1234567-89ab-cdef-0123-456789abcdef
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "comparison": {
      "fromVersion": {
        "id": "s1234567-89ab-cdef-0123-456789abcdef",
        "version": 1,
        "date": "2025-10-20T15:05:00Z"
      },
      "toVersion": {
        "id": "s9876543-21ba-fedc-3210-fedcba987654",
        "version": 4,
        "date": "2025-10-24T07:05:00Z"
      },
      "versionSpan": 3,
      "daysSpan": 4
    },
    "changes": [
      {
        "section": "situation",
        "field": "bloodGlucose",
        "changeType": "improved",
        "from": "320 mg/dL (hyperglycemic crisis)",
        "to": "110 mg/dL (well-controlled)",
        "significance": "high"
      },
      {
        "section": "situation",
        "field": "acuteDistress",
        "changeType": "resolved",
        "from": "Symptoms: polyuria, polydipsia x 3 days",
        "to": "No acute distress, no symptoms",
        "significance": "high"
      },
      {
        "section": "assessment",
        "field": "vitalSigns",
        "changeType": "improved",
        "from": "BP 145/90, HR 88",
        "to": "BP 130/85, HR 78",
        "significance": "medium"
      },
      {
        "section": "recommendation",
        "field": "treatmentPlan",
        "changeType": "updated",
        "from": "Start insulin drip, DM education, endocrine consult",
        "to": "Continue insulin, discharge tomorrow, follow-up Nov 6",
        "significance": "high"
      },
      {
        "section": "background",
        "field": "patientHistory",
        "changeType": "unchanged",
        "note": "Stable information carried forward",
        "significance": "low"
      }
    ],
    "summary": {
      "totalChanges": 6,
      "improvementTrend": "positive",
      "clinicalSignificance": "Patient shows significant improvement from admission to current state. Ready for discharge."
    }
  }
}
```

---

### 3.4 PUT /v1/sbar/:id

Edit SBAR report.

**Endpoint:**
```
PUT /v1/sbar/{sbarId}
```

**Authentication:** Required  
**Permission:** `sbar:update`

**Request:**
```http
PUT /v1/sbar/s9876543-21ba-fedc-3210-fedcba987654
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "recommendation": "Continue current insulin sliding scale. Discharge education completed - patient verbalizes understanding. Discharge planned for tomorrow morning 0900. Follow-up appointment scheduled with Dr. Martinez in endocrinology on November 6th at 10:00 AM. Continue home medications upon discharge.",
  "editSummary": "Added specific discharge time and physician name",
  "section": "recommendation"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "s9876543-21ba-fedc-3210-fedcba987654",
    "version": 4,
    "recommendation": "Continue current insulin sliding scale. Discharge education completed - patient verbalizes understanding. Discharge planned for tomorrow morning 0900. Follow-up appointment scheduled with Dr. Martinez in endocrinology on November 6th at 10:00 AM. Continue home medications upon discharge.",
    "editSummary": "Added specific discharge time and physician name",
    "editedBy": {
      "id": "b4c3d2e1-f5e6-4a7b-8c9d-0e1f2a3b4c5d",
      "name": "Sarah Johnson",
      "role": "registered_nurse"
    },
    "editedAt": "2025-10-24T07:20:00Z",
    "updatedAt": "2025-10-24T07:20:00Z"
  }
}
```

---

### 3.5 POST /v1/sbar/:id/export

Export SBAR report to various formats.

**Endpoint:**
```
POST /v1/sbar/{sbarId}/export
```

**Authentication:** Required  
**Permission:** `sbar:read`

**Request:**
```http
POST /v1/sbar/s9876543-21ba-fedc-3210-fedcba987654/export
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "format": "pdf",
  "includePatientPhoto": false,
  "includeVitalSigns": true,
  "includeChangeHistory": true,
  "includeAllVersions": false
}
```

**Supported Formats:**
- `pdf` - Formatted PDF document
- `docx` - Microsoft Word document
- `txt` - Plain text
- `json` - Structured JSON

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "exportId": "export_abc123",
    "format": "pdf",
    "downloadUrl": "https://eclipselink-production.r2.cloudflarestorage.com/exports/sbar-reports/s9876543_v4.pdf?signature=...",
    "expiresAt": "2025-10-24T08:20:00Z",
    "expiresIn": 3600,
    "fileSize": 245678,
    "fileName": "SBAR_Smith_Jane_MRN123456_v4.pdf"
  }
}
```

---

## 4. EHR Integration Endpoints

### 4.1 GET /v1/ehr/connections

List EHR connections for facility.

**Endpoint:**
```
GET /v1/ehr/connections
```

**Authentication:** Required  
**Permission:** `ehr:read`

**Request:**
```http
GET /v1/ehr/connections
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "connections": [
      {
        "id": "ehr_abc123",
        "facilityId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "ehrType": "epic",
        "ehrVersion": "2023",
        "protocol": "fhir_r4",
        "status": "active",
        "lastSuccessfulConnection": "2025-10-24T07:00:00Z",
        "lastSyncCompleted": "2025-10-24T07:05:00Z",
        "autoSyncEnabled": true,
        "syncFrequencyMinutes": 60,
        "supportedResources": [
          "Patient",
          "Observation",
          "MedicationStatement",
          "AllergyIntolerance",
          "Condition",
          "Encounter"
        ],
        "createdAt": "2025-01-15T10:00:00Z"
      }
    ]
  }
}
```

---

### 4.2 POST /v1/ehr/sync

Manually trigger EHR sync for a patient.

**Endpoint:**
```
POST /v1/ehr/sync
```

**Authentication:** Required  
**Permission:** `ehr:sync`

**Request:**
```http
POST /v1/ehr/sync
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "syncType": "patient_import",
  "patientId": "p1234567-89ab-cdef-0123-456789abcdef",
  "resources": ["Observation", "MedicationStatement", "AllergyIntolerance"]
}
```

**Sync Types:**
- `patient_import` - Import patient data from EHR
- `patient_export` - Export handoff data to EHR
- `full_sync` - Bidirectional sync

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "syncId": "sync_def456",
    "syncType": "patient_import",
    "patientId": "p1234567-89ab-cdef-0123-456789abcdef",
    "status": "in_progress",
    "resources": ["Observation", "MedicationStatement", "AllergyIntolerance"],
    "startedAt": "2025-10-24T07:25:00Z",
    "estimatedCompletionAt": "2025-10-24T07:26:00Z"
  }
}
```

---

### 4.3 GET /v1/ehr/sync/:syncId

Get EHR sync status and results.

**Endpoint:**
```
GET /v1/ehr/sync/{syncId}
```

**Authentication:** Required  
**Permission:** `ehr:read`

**Request:**
```http
GET /v1/ehr/sync/sync_def456
Authorization: Bearer {accessToken}
```

**Response (200 OK) - Completed:**
```json
{
  "success": true,
  "data": {
    "syncId": "sync_def456",
    "syncType": "patient_import",
    "patientId": "p1234567-89ab-cdef-0123-456789abcdef",
    "status": "completed",
    "resources": ["Observation", "MedicationStatement", "AllergyIntolerance"],
    "results": {
      "Observation": {
        "fetched": 48,
        "imported": 45,
        "skipped": 3,
        "errors": 0
      },
      "MedicationStatement": {
        "fetched": 12,
        "imported": 12,
        "skipped": 0,
        "errors": 0
      },
      "AllergyIntolerance": {
        "fetched": 2,
        "imported": 2,
        "skipped": 0,
        "errors": 0
      }
    },
    "summary": {
      "totalFetched": 62,
      "totalImported": 59,
      "totalSkipped": 3,
      "totalErrors": 0,
      "successRate": 0.95
    },
    "startedAt": "2025-10-24T07:25:00Z",
    "completedAt": "2025-10-24T07:25:52Z",
    "durationMs": 52000
  }
}
```

---

### 4.4 POST /v1/ehr/export-handoff

Export completed handoff to EHR.

**Endpoint:**
```
POST /v1/ehr/export-handoff
```

**Authentication:** Required  
**Permission:** `ehr:export`

**Request:**
```http
POST /v1/ehr/export-handoff
Authorization: Bearer {accessToken}
Content-Type: application/json

{
  "handoffId": "h9876543-21ba-fedc-3210-fedcba987654",
  "exportFormat": "fhir_communication",
  "includeVoiceRecording": false,
  "includeSbarAsPdf": true
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "exportId": "export_ghi789",
    "handoffId": "h9876543-21ba-fedc-3210-fedcba987654",
    "ehrConnectionId": "ehr_abc123",
    "status": "in_progress",
    "fhirResourceType": "Communication",
    "startedAt": "2025-10-24T07:30:00Z",
    "estimatedCompletionAt": "2025-10-24T07:30:30Z"
  }
}
```

---

## 5. Analytics & Reporting Endpoints

### 5.1 GET /v1/analytics/handoff-metrics

Get handoff performance metrics.

**Endpoint:**
```
GET /v1/analytics/handoff-metrics
```

**Authentication:** Required  
**Permission:** `analytics:read`

**Query Parameters:**
- `startDate` (ISO 8601, required)
- `endDate` (ISO 8601, required)
- `department` (string, optional)
- `handoffType` (string, optional)

**Request:**
```http
GET /v1/analytics/handoff-metrics?startDate=2025-10-01T00:00:00Z&endDate=2025-10-24T23:59:59Z&department=Medical/Surgical
Authorization: Bearer {accessToken}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "period": {
      "startDate": "2025-10-01T00:00:00Z",
      "endDate": "2025-10-24T23:59:59Z",
      "days": 24
    },
    "overview": {
      "totalHandoffs": 487,
      "initialHandoffs": 142,
      "updateHandoffs": 345,
      "completedHandoffs": 465,
      "averageHandoffsPerDay": 20.3,
      "averageHandoffsPerPatient": 3.4
    },
    "processingMetrics": {
      "averageRecordingDuration": 178,
      "averageTranscriptionDuration": 24,
      "averageSbarGenerationDuration": 19,
      "averageTotalProcessingTime": 43,
      "transcriptionSuccessRate": 0.982,
      "sbarQualityScore": 0.94
    },
    "handoffTypes": {
      "shift_change": {
        "count": 268,
        "percentage": 55.0
      },
      "admission": {
        "count": 142,
        "percentage": 29.2
      },
      "transfer": {
        "count": 52,
        "percentage": 10.7
      },
      "status_update": {
        "count": 25,
        "percentage": 5.1
      }
    },
    "priorityDistribution": {
      "routine": 412,
      "urgent": 68,
      "emergent": 7
    },
    "timeToCompletion": {
      "average": 12.5,
      "median": 10.0,
      "min": 3.0,
      "max": 45.0,
      "unit": "minutes"
    },
    "staffMetrics": {
      "totalStaff": 42,
      "averageHandoffsPerStaff": 11.6,
      "topPerformers": [
        {
          "staffId": "a3b2c1d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
          "name": "John Doe",
          "handoffCount": 28,
          "avgQuality": 0.96
        }
      ]
    }
  }
}
```

---

## Summary

### ✅ Part 4C Covers:

1. **Handoff Workflow Patterns** - Initial vs. Update handoffs
2. **Patient Endpoints** - 3 endpoints with handoff history tracking
3. **SBAR Endpoints** - 5 endpoints with version tracking and comparison
4. **EHR Integration** - 4 endpoints for sync and export
5. **Analytics** - Performance metrics and reporting

### 🎯 Key Workflow Features:

**Initial Handoff:**
- `isInitialHandoff: true`
- `previousHandoffId: null`
- Full SBAR generation
- Baseline establishment

**Update Handoff:**
- `isInitialHandoff: false`
- `previousHandoffId: "{uuid}"`
- Incremental SBAR updates
- Change tracking

### 📊 Endpoints Summary:

**Patient Endpoints (3):**
1. GET /v1/patients - List with handoff status
2. GET /v1/patients/:id - Full details
3. GET /v1/patients/:id/handoffs - Complete handoff timeline

**SBAR Endpoints (5):**
1. GET /v1/sbar/:handoffId - Get current SBAR
2. GET /v1/sbar/:handoffId/versions - Version history
3. GET /v1/sbar/:id/compare - Compare versions
4. PUT /v1/sbar/:id - Edit SBAR
5. POST /v1/sbar/:id/export - Export to PDF/DOCX

**EHR Endpoints (4):**
1. GET /v1/ehr/connections - List connections
2. POST /v1/ehr/sync - Manual sync
3. GET /v1/ehr/sync/:syncId - Sync status
4. POST /v1/ehr/export-handoff - Export to EHR

**Analytics (1):**
1. GET /v1/analytics/handoff-metrics - Performance metrics

---

**Next:** Part 4D will cover Error Handling, Rate Limiting, Webhooks, and Code Examples.

---

*EclipseLink AI™ is a product of Rohimaya Health AI*  
*© 2025 Rohimaya Health AI. All rights reserved.*
