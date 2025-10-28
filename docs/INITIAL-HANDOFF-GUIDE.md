# Initial Handoff on Admission - Complete Guide

> **Purpose**: Explains how initial handoffs work in EclipseLink AI and what information is required for patient admission

---

## Table of Contents

1. [What is an Initial Handoff?](#what-is-an-initial-handoff)
2. [Initial vs Update Handoffs](#initial-vs-update-handoffs)
3. [Required Information for Admission](#required-information-for-admission)
4. [Medical Professional Roles](#medical-professional-roles)
5. [Workflow: Patient Admission](#workflow-patient-admission)
6. [Technical Implementation](#technical-implementation)
7. [Testing Initial Handoffs](#testing-initial-handoffs)

---

## What is an Initial Handoff?

An **initial handoff** is the **first clinical documentation** created when a patient is admitted to the hospital or transferred to a new unit. It establishes the **baseline** for all future handoffs.

### Key Characteristics

- **Comprehensive**: Contains complete patient history, current condition, care plan
- **Establishes Baseline**: All future handoffs are updates to this initial report
- **One per Admission**: Each hospital admission gets exactly ONE initial handoff
- **Flagged in Database**: `is_initial_handoff = true` in `handoffs` table

### Why Initial Handoffs are Different

| Aspect | Initial Handoff | Update Handoff |
|--------|----------------|----------------|
| **When** | Patient admission | Shift changes (every 8-12 hours) |
| **Content** | Complete patient history | Only what changed since last handoff |
| **Duration** | 5-10 minute voice recording | 1-3 minute voice recording |
| **SBAR Length** | 400-800 words | 100-200 words |
| **Processing Time** | 60-90 seconds | 30-45 seconds |
| **Cost** | ~$0.12 (more tokens) | ~$0.06 (fewer tokens) |

---

## Initial vs Update Handoffs

### Example: Diabetic Patient Admission

**Initial Handoff (Day 1 - 7:00 AM)**:
```
SITUATION:
60-year-old female presenting with hyperglycemic crisis. Blood glucose 320 mg/dL
on arrival. Patient alert and oriented x3, appears fatigued. Polyuria and
polydipsia x 3 days per patient report.

BACKGROUND:
Past medical history includes type 2 diabetes (diagnosed 10 years ago), essential
hypertension, and hyperlipidemia. Home medications: Metformin 1000mg BID,
Lisinopril 10mg daily, Atorvastatin 20mg daily. Known allergy to Penicillin
(rash). Patient lives at home with spouse, independent with ADLs. No recent
hospitalizations. Patient reports medication non-compliance x 1 week due to
running out of Metformin.

ASSESSMENT:
Current vital signs: Temperature 98.6°F, BP 145/92, HR 88, RR 18, SpO2 98% on
room air. Patient is hemodynamically stable but requires close glucose monitoring
and insulin therapy. Admission labs show HbA1c 11.2%, elevated ketones. Started
on insulin drip per protocol. Endocrinology consulted.

RECOMMENDATION:
Continue insulin drip, target glucose 120-180 mg/dL. Check glucose q1h. Monitor
for DKA signs. Patient education on medication compliance and glucose monitoring.
Discharge planning: home health referral, medication reconciliation, endocrinology
follow-up appointment scheduled for 2 weeks post-discharge.
```

**Update Handoff #1 (Day 1 - 7:00 PM, 12 hours later)**:
```
SITUATION:
Blood glucose improved to 145 mg/dL (down from 320). Patient continues to be
alert and oriented, no longer fatigued. Polyuria resolved, taking adequate PO fluids.

ASSESSMENT:
Glucose trending down nicely on current insulin protocol. Patient tolerating
regular diet. All vitals stable. Patient engaged in diabetes education session.

RECOMMENDATION:
Continue current insulin drip, transition to SubQ insulin overnight if glucose
remains stable. Continue q1h glucose checks. Plan for discharge tomorrow if
glucose stable on SubQ insulin.
```

**Update Handoff #2 (Day 2 - 7:00 AM, next morning)**:
```
SITUATION:
Blood glucose 110 mg/dL this morning, excellent control overnight. Patient reports
feeling much better, energy level improved.

ASSESSMENT:
Successfully transitioned to SubQ insulin overnight with stable glucose levels.
Patient passed diabetes education assessment, verbalizes understanding of
medication regimen and home glucose monitoring.

RECOMMENDATION:
Discharge today after morning rounds. Prescriptions: Metformin 1000mg BID,
Lisinopril 10mg daily, Atorvastatin 20mg daily, insulin pen with sliding scale.
Follow-up with endocrinology in 2 weeks (Nov 6). Patient received written
discharge instructions.
```

### How the System Knows It's an Update

**Database Tracking**:
```sql
-- Initial handoff
INSERT INTO handoffs (
  patient_id,
  is_initial_handoff,        -- TRUE
  previous_handoff_id         -- NULL (no previous handoff)
) VALUES ('patient-123', true, NULL);

-- Update handoff #1
INSERT INTO handoffs (
  patient_id,
  is_initial_handoff,        -- FALSE
  previous_handoff_id         -- Points to initial handoff
) VALUES ('patient-123', false, 'initial-handoff-id');

-- Update handoff #2
INSERT INTO handoffs (
  patient_id,
  is_initial_handoff,        -- FALSE
  previous_handoff_id         -- Points to update handoff #1
) VALUES ('patient-123', false, 'update-handoff-1-id');
```

**API Request**:
```typescript
// Creating initial handoff
POST /v1/handoffs
{
  "patientId": "patient-123",
  "fromStaffId": "nurse-456",
  "isInitialHandoff": true,      // ← Explicit flag
  "previousHandoffId": null       // ← No previous handoff
}

// Creating update handoff
POST /v1/handoffs
{
  "patientId": "patient-123",
  "fromStaffId": "nurse-789",
  "isInitialHandoff": false,      // ← Not initial
  "previousHandoffId": "handoff-abc"  // ← Link to previous
}
```

---

## Required Information for Admission

### Minimum Required Fields

When creating an **initial handoff** on patient admission, you must provide:

#### 1. Patient Demographics
```typescript
{
  "firstName": "Jane",
  "lastName": "Smith",
  "mrn": "MRN123456",              // Medical Record Number (unique)
  "dateOfBirth": "1963-05-15",
  "gender": "female",
  "bloodType": "O+",                // Optional but recommended
  "primaryLanguage": "English"      // Optional
}
```

#### 2. Admission Details
```typescript
{
  "admissionDate": "2025-10-28T07:30:00Z",
  "admissionSource": "emergency_department",  // or "direct_admission", "transfer"
  "chiefComplaint": "Hyperglycemic crisis",
  "admittingDiagnosis": "Type 2 diabetes with hyperglycemia"
}
```

#### 3. Staff Assignment
```typescript
{
  "fromStaffId": "admitting-nurse-id",   // Nurse creating the handoff
  "toStaffId": null,                      // Can be null initially, assigned later
  "handoffType": "admission",
  "priority": "routine"                   // or "urgent", "emergent"
}
```

#### 4. Clinical Information (via Voice Recording)

The nurse records a **5-10 minute voice memo** covering:

**SBAR Framework**:
- **Situation**: Current condition, vital signs, chief complaint
- **Background**: Medical history, medications, allergies, social history
- **Assessment**: Clinical findings, lab results, current trends
- **Recommendation**: Treatment plan, pending tasks, follow-ups

**What to Include**:
```
✅ Current vital signs (BP, HR, RR, Temp, SpO2)
✅ Chief complaint and presenting symptoms
✅ Past medical history (chronic conditions)
✅ Current medications (name, dose, frequency)
✅ Allergies (medication and food allergies)
✅ Social history (living situation, support system)
✅ Code status (Full Code, DNR, DNI)
✅ Treatment plan (orders, interventions)
✅ Pending tasks (labs, imaging, consults)
✅ Safety concerns (fall risk, isolation precautions)
```

---

## Medical Professional Roles

### All Supported Roles in System

The database supports **15 medical professional roles** plus **2 admin roles**:

```sql
CREATE TYPE user_role AS ENUM (
  -- Nursing Staff
  'registered_nurse',              -- RN (most common user)
  'licensed_practical_nurse',      -- LPN
  'certified_nursing_assistant',   -- CNA

  -- Advanced Practice
  'nurse_practitioner',            -- NP
  'physician_assistant',           -- PA

  -- Physicians
  'physician',                     -- MD/DO

  -- Allied Health Professionals
  'respiratory_therapist',         -- RT
  'physical_therapist',            -- PT
  'occupational_therapist',        -- OT
  'medical_assistant',             -- MA

  -- Emergency Services
  'emergency_medical_technician',  -- EMT/Paramedic

  -- Technical Specialists
  'radiologic_technician',         -- Radiology tech
  'surgical_technician',           -- Surgical tech
  'lab_technician',                -- Lab tech
  'pharmacy_technician',           -- Pharmacy tech

  -- Administrative
  'admin',                         -- Facility admin
  'super_admin'                    -- System admin
);
```

### Role Permissions

| Role | Can Create Handoff? | Can Accept Handoff? | Can Edit SBAR? | Can View All Patients? |
|------|---------------------|---------------------|----------------|------------------------|
| **Registered Nurse** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes (in their unit) |
| **LPN** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes (in their unit) |
| **CNA** | ⚠️ Limited | ✅ Yes | ❌ No | ⚠️ Assigned patients only |
| **Physician** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes (all patients) |
| **NP/PA** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes (in their service) |
| **Respiratory Therapist** | ⚠️ Limited | ✅ Yes | ⚠️ Assessment only | ⚠️ Assigned patients only |
| **Physical Therapist** | ⚠️ Limited | ❌ No | ⚠️ Assessment only | ⚠️ Assigned patients only |
| **Medical Assistant** | ⚠️ Limited | ❌ No | ❌ No | ⚠️ Assigned patients only |
| **Admin** | ❌ No | ❌ No | ❌ No | ✅ Yes (reporting only) |

### Most Common Use Cases

**1. Registered Nurse (RN)** - 80% of handoffs
- Creates initial handoff on admission
- Creates update handoffs at shift change
- Receives handoffs from previous shift
- Primary user of the system

**2. Physician** - 10% of handoffs
- Creates handoff when admitting patient
- Reviews handoffs created by nurses
- Adds clinical assessments to SBAR

**3. Nurse Practitioner (NP)** - 8% of handoffs
- Similar to RN but with prescribing authority
- Often manages their own patient panel
- Creates comprehensive handoffs

**4. Licensed Practical Nurse (LPN)** - 2% of handoffs
- Assists RNs with patient care
- Creates handoffs under RN supervision
- Limited to specific units (e.g., skilled nursing)

---

## Workflow: Patient Admission

### Step-by-Step Process

#### **Step 1: Patient Arrives**
```
Emergency Department → Admitting Nurse receives patient
```

#### **Step 2: Create Patient Record**
```typescript
POST /v1/patients
{
  "firstName": "Jane",
  "lastName": "Smith",
  "mrn": "MRN123456",
  "dateOfBirth": "1963-05-15",
  "gender": "female",
  "facilityId": "facility-abc"
}

Response:
{
  "success": true,
  "data": {
    "id": "patient-123",
    "mrn": "MRN123456",
    "status": "active"
  }
}
```

#### **Step 3: Create Initial Handoff**
```typescript
POST /v1/handoffs
{
  "patientId": "patient-123",
  "fromStaffId": "nurse-456",
  "toStaffId": null,                // Assigned later
  "facilityId": "facility-abc",
  "handoffType": "admission",
  "priority": "routine",
  "isInitialHandoff": true,         // ← Critical flag
  "previousHandoffId": null,
  "clinicalNotes": "Patient admitted from ED with hyperglycemic crisis"
}

Response:
{
  "success": true,
  "data": {
    "id": "handoff-abc",
    "status": "draft",
    "isInitialHandoff": true
  }
}
```

#### **Step 4: Record Voice Memo**
```typescript
// Nurse uses frontend to record 5-10 minute voice memo
POST /v1/voice/upload
Content-Type: multipart/form-data

{
  handoffId: "handoff-abc",
  audioFile: <binary data>,
  duration: 420,              // 7 minutes
  audioFormat: "webm"
}

Response:
{
  "success": true,
  "data": {
    "recordingId": "recording-xyz",
    "status": "uploaded",
    "transcriptionJobId": "job-123"  // Queued for processing
  }
}
```

#### **Step 5: AI Processing (Automatic)**
```
1. Transcription Worker picks up job from queue
2. Downloads audio from Cloudflare R2
3. Calls Azure Whisper API (30-45 seconds)
4. Saves transcription to database
5. Updates handoff status: draft → recording → transcribing

6. SBAR Generation Worker picks up next job
7. Fetches transcription from database
8. Calls GPT-4 with INITIAL handoff prompt
9. Generates comprehensive SBAR report
10. Saves SBAR to database (version 1, is_initial = true)
11. Updates handoff status: transcribing → generating → ready

Total time: 60-90 seconds
```

#### **Step 6: Nurse Reviews SBAR**
```typescript
GET /v1/sbar/handoff-abc

Response:
{
  "success": true,
  "data": {
    "id": "sbar-123",
    "handoffId": "handoff-abc",
    "version": 1,
    "isInitial": true,            // ← Indicates initial handoff
    "situation": "60-year-old female presenting with hyperglycemic crisis...",
    "background": "Past medical history includes type 2 diabetes...",
    "assessment": "Current vital signs: Temperature 98.6°F, BP 145/92...",
    "recommendation": "Continue insulin drip, target glucose 120-180 mg/dL...",
    "qualityMetrics": {
      "completenessScore": 0.95,
      "readabilityScore": 0.88,
      "adherenceToIPassFramework": true,
      "criticalInfoPresent": true
    }
  }
}
```

#### **Step 7: Optional Edits**
```typescript
// If nurse needs to correct/add information
PUT /v1/sbar/sbar-123
{
  "situation": "60-year-old female presenting with hyperglycemic crisis. Blood glucose 320 mg/dL on arrival (updated)...",
  "editSummary": "Added specific glucose value"
}

Response:
{
  "success": true,
  "data": {
    "id": "sbar-123",
    "version": 1,
    "editHistory": [
      {
        "editedAt": "2025-10-28T08:15:00Z",
        "editedBy": { "id": "nurse-456", "name": "Sarah Johnson" },
        "editSummary": "Added specific glucose value",
        "changes": [
          {
            "section": "situation",
            "previousValue": "...",
            "newValue": "..."
          }
        ]
      }
    ]
  }
}
```

#### **Step 8: Assign to Receiving Nurse**
```typescript
PUT /v1/handoffs/handoff-abc/assign
{
  "toStaffId": "nurse-789",
  "scheduledTime": "2025-10-28T19:00:00Z"  // Evening shift
}

Response:
{
  "success": true,
  "data": {
    "id": "handoff-abc",
    "status": "assigned",
    "toStaff": {
      "id": "nurse-789",
      "name": "Michael Chen",
      "role": "registered_nurse"
    },
    "scheduledTime": "2025-10-28T19:00:00Z"
  }
}
```

#### **Step 9: Next Shift Nurse Accepts**
```typescript
POST /v1/handoffs/handoff-abc/accept
{
  "notes": "Reviewed and accepted, ready to take over care"
}

Response:
{
  "success": true,
  "data": {
    "id": "handoff-abc",
    "status": "accepted",
    "acceptedAt": "2025-10-28T19:05:00Z"
  }
}
```

---

## Technical Implementation

### Database Schema for Initial Handoffs

**Handoffs Table**:
```sql
CREATE TABLE handoffs (
  id UUID PRIMARY KEY,
  patient_id UUID NOT NULL REFERENCES patients(id),
  facility_id UUID NOT NULL REFERENCES facilities(id),
  from_staff_id UUID NOT NULL REFERENCES staff(id),
  to_staff_id UUID REFERENCES staff(id),         -- NULL until assigned

  -- Initial handoff tracking
  is_initial_handoff BOOLEAN DEFAULT false,      -- TRUE for admission handoffs
  previous_handoff_id UUID REFERENCES handoffs(id),  -- NULL for initial, links for updates

  status handoff_status NOT NULL,                -- draft, recording, ready, etc.
  handoff_type TEXT NOT NULL,                    -- "admission", "shift_change", etc.
  priority handoff_priority NOT NULL,            -- routine, urgent, emergent

  clinical_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**SBAR Reports Table**:
```sql
CREATE TABLE sbar_reports (
  id UUID PRIMARY KEY,
  handoff_id UUID NOT NULL REFERENCES handoffs(id),
  patient_id UUID NOT NULL REFERENCES patients(id),
  facility_id UUID NOT NULL REFERENCES facilities(id),

  -- Version tracking
  version INTEGER NOT NULL,                      -- 1 for initial, 2, 3, 4... for updates
  previous_version_id UUID REFERENCES sbar_reports(id),  -- NULL for initial
  is_initial BOOLEAN DEFAULT false,              -- TRUE for initial handoff SBAR

  -- SBAR content
  situation TEXT NOT NULL,
  background TEXT NOT NULL,
  assessment TEXT NOT NULL,
  recommendation TEXT NOT NULL,

  -- Changes (only for update handoffs)
  changes_since_last_version JSONB,              -- NULL for initial

  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### AI Prompt Differences

**Initial Handoff Prompt**:
```typescript
function buildInitialSbarPrompt(transcriptionText: string) {
  return [
    { role: 'system', content: SBAR_SYSTEM_PROMPT },
    {
      role: 'user',
      content: `This is an INITIAL handoff (patient admission or first documentation).

TRANSCRIPTION:
${transcriptionText}

Generate a COMPLETE SBAR report with:
1. FULL patient history (past medical history, medications, allergies)
2. Complete assessment of current condition
3. Comprehensive treatment plan
4. All pending tasks and follow-ups

Be thorough - this establishes the baseline for all future handoffs.`
    }
  ];
}
```

**Update Handoff Prompt**:
```typescript
function buildUpdateSbarPrompt(transcriptionText: string, previousSbar: any) {
  return [
    { role: 'system', content: SBAR_SYSTEM_PROMPT },
    {
      role: 'user',
      content: `This is an UPDATE handoff (shift change).

PREVIOUS SBAR (Version ${previousSbar.version}):
Situation: ${previousSbar.situation}
Background: ${previousSbar.background}
Assessment: ${previousSbar.assessment}
Recommendation: ${previousSbar.recommendation}

NEW TRANSCRIPTION (only covers changes since last handoff):
${transcriptionText}

Generate an UPDATED SBAR that:
1. Incorporates new information from transcription
2. Maintains relevant context from previous version
3. Highlights what has CHANGED (vital signs, medications, status)
4. Removes obsolete information
5. Updates recommendations based on current status`
    }
  ];
}
```

### API Logic

**Creating Handoff**:
```typescript
// apps/backend/src/controllers/handoff.controller.ts
export async function createHandoff(req: Request, res: Response): Promise<void> {
  const { patientId, fromStaffId, toStaffId, isInitialHandoff, previousHandoffId } = req.body;

  // Validation: Initial handoffs should not have previous handoff
  if (isInitialHandoff && previousHandoffId) {
    throw new ValidationError('Initial handoffs cannot have a previous handoff');
  }

  // Validation: Update handoffs MUST have previous handoff
  if (!isInitialHandoff && !previousHandoffId) {
    throw new ValidationError('Update handoffs must reference a previous handoff');
  }

  // If this is initial handoff, verify no other initial handoff exists
  if (isInitialHandoff) {
    const existingInitial = await db.query(
      `SELECT id FROM handoffs
       WHERE patient_id = $1
       AND is_initial_handoff = true
       AND status NOT IN ('cancelled', 'failed')`,
      [patientId]
    );

    if (existingInitial.rows.length > 0) {
      throw new ValidationError('Patient already has an initial handoff. Use update handoff instead.');
    }
  }

  // Create handoff
  const result = await db.query(
    `INSERT INTO handoffs (
      patient_id, facility_id, from_staff_id, to_staff_id,
      is_initial_handoff, previous_handoff_id, status, handoff_type, priority
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    RETURNING *`,
    [
      patientId,
      req.user!.facilityId,
      fromStaffId,
      toStaffId,
      isInitialHandoff,
      previousHandoffId,
      'draft',
      req.body.handoffType || 'shift_change',
      req.body.priority || 'routine'
    ]
  );

  res.status(201).json({
    success: true,
    data: result.rows[0]
  });
}
```

---

## Testing Initial Handoffs

### Test Scenario: New Patient Admission

**Test Data**:
```typescript
// 1. Create test patient
const patient = await createTestPatient({
  firstName: 'Jane',
  lastName: 'Smith',
  mrn: 'TEST-' + Date.now(),
  dateOfBirth: '1963-05-15',
  gender: 'female'
});

// 2. Create initial handoff
const initialHandoff = await createHandoff({
  patientId: patient.id,
  fromStaffId: testNurse.id,
  isInitialHandoff: true,        // ← Mark as initial
  previousHandoffId: null,       // ← No previous handoff
  handoffType: 'admission',
  priority: 'routine'
});

expect(initialHandoff.status).toBe('draft');
expect(initialHandoff.isInitialHandoff).toBe(true);

// 3. Upload voice recording
const voiceRecording = await uploadTestAudio({
  handoffId: initialHandoff.id,
  audioFile: 'test-initial-handoff.webm',
  duration: 420  // 7 minutes
});

// 4. Wait for AI processing
await waitForHandoffStatus(initialHandoff.id, 'ready', 90000);  // 90 second timeout

// 5. Verify SBAR generated
const sbar = await getSbar(initialHandoff.id);
expect(sbar.version).toBe(1);
expect(sbar.isInitial).toBe(true);
expect(sbar.situation).toBeDefined();
expect(sbar.background).toBeDefined();
expect(sbar.assessment).toBeDefined();
expect(sbar.recommendation).toBeDefined();

// 6. Create update handoff (12 hours later)
const updateHandoff = await createHandoff({
  patientId: patient.id,
  fromStaffId: testNurse2.id,
  isInitialHandoff: false,       // ← Not initial
  previousHandoffId: initialHandoff.id,  // ← Link to initial
  handoffType: 'shift_change',
  priority: 'routine'
});

expect(updateHandoff.isInitialHandoff).toBe(false);
expect(updateHandoff.previousHandoffId).toBe(initialHandoff.id);

// 7. Upload update voice (shorter)
const updateRecording = await uploadTestAudio({
  handoffId: updateHandoff.id,
  audioFile: 'test-update-handoff.webm',
  duration: 120  // 2 minutes
});

// 8. Wait for update SBAR
await waitForHandoffStatus(updateHandoff.id, 'ready', 60000);

// 9. Verify update SBAR references previous
const updateSbar = await getSbar(updateHandoff.id);
expect(updateSbar.version).toBe(2);
expect(updateSbar.isInitial).toBe(false);
expect(updateSbar.previousVersionId).toBe(sbar.id);

// 10. Compare versions
const comparison = await compareSbar(sbar.id, updateSbar.id);
expect(comparison.changes.length).toBeGreaterThan(0);
expect(comparison.versionSpan).toBe(1);
```

### Common Test Cases

**Test 1: Cannot Create Duplicate Initial Handoffs**
```typescript
test('prevents duplicate initial handoffs for same patient', async () => {
  // Create first initial handoff
  const handoff1 = await createHandoff({
    patientId: patient.id,
    isInitialHandoff: true,
    previousHandoffId: null
  });

  // Try to create second initial handoff (should fail)
  await expect(
    createHandoff({
      patientId: patient.id,
      isInitialHandoff: true,
      previousHandoffId: null
    })
  ).rejects.toThrow('Patient already has an initial handoff');
});
```

**Test 2: Update Handoff Must Have Previous**
```typescript
test('requires previousHandoffId for update handoffs', async () => {
  await expect(
    createHandoff({
      patientId: patient.id,
      isInitialHandoff: false,
      previousHandoffId: null  // ← Missing!
    })
  ).rejects.toThrow('Update handoffs must reference a previous handoff');
});
```

**Test 3: Version History**
```typescript
test('tracks version history correctly', async () => {
  // Initial (v1)
  const h1 = await createHandoffWithSbar(patient.id, { isInitial: true });

  // Update 1 (v2)
  const h2 = await createHandoffWithSbar(patient.id, {
    isInitial: false,
    previousHandoffId: h1.id
  });

  // Update 2 (v3)
  const h3 = await createHandoffWithSbar(patient.id, {
    isInitial: false,
    previousHandoffId: h2.id
  });

  // Get version history
  const versions = await getSbarVersions(h3.id);

  expect(versions.totalVersions).toBe(3);
  expect(versions.versionTree.initial).toBe(h1.sbarId);
  expect(versions.versionTree.updates).toEqual([h2.sbarId, h3.sbarId]);
  expect(versions.versionTree.current).toBe(h3.sbarId);
});
```

---

## FAQ

**Q: What if the patient was admitted yesterday but we forgot to create the initial handoff?**

A: Create it now! The initial handoff establishes the baseline. You can create it at any time, but all future handoffs should reference it. The system doesn't enforce admission date matching.

**Q: Can a physician create the initial handoff instead of a nurse?**

A: Yes! Any staff member with appropriate permissions can create the initial handoff. In some workflows, the admitting physician creates it, and nurses create subsequent updates.

**Q: What if the patient is readmitted after being discharged?**

A: Create a NEW initial handoff. Each hospital admission gets its own initial handoff. The `is_initial_handoff` flag is per admission, not per patient lifetime.

**Q: Can we edit an initial handoff after it's created?**

A: Yes! Use `PUT /v1/sbar/:id` to edit any section. All edits are tracked in `edit_history` for audit purposes.

**Q: What's the maximum length for voice recordings?**

A: Technically unlimited, but we recommend:
- Initial handoffs: 5-10 minutes (optimal)
- Update handoffs: 1-3 minutes (optimal)
- Maximum: 15 minutes (Azure Whisper limit is 25 MB or ~2 hours)

**Q: Does the system detect if it should be an initial vs update handoff?**

A: No, the creating user must explicitly set `isInitialHandoff: true/false`. The system validates the flag matches the presence/absence of `previousHandoffId`.

---

## Summary

**Key Points**:
1. **Initial handoff** = first documentation on admission (comprehensive, 5-10 min)
2. **Update handoff** = subsequent shift changes (only changes, 1-3 min)
3. Flag: `is_initial_handoff = true` in database
4. Link: `previous_handoff_id` connects update to initial
5. All 17 medical roles can participate in handoffs (permissions vary)
6. One initial handoff per admission, unlimited updates
7. AI uses different prompts for initial vs update handoffs

**Workflow**:
```
Admission → Create Patient → Create Initial Handoff → Record Voice (5-10 min)
→ AI Processing (60-90 sec) → Review SBAR → Assign to Next Shift
→ Shift Change → Create Update Handoff → Record Voice (1-3 min)
→ AI Processing (30-45 sec) → Review Updated SBAR → Repeat
```

---

*For more information, see [EDUCATIONAL-GUIDE.md](./EDUCATIONAL-GUIDE.md) for full system architecture details.*
