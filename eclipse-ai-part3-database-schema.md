# EclipseLink AI™ - Part 3: Database Schema & ERD

**Document Version:** 1.0  
**Last Updated:** October 23, 2025  
**Product:** EclipseLink AI™ Clinical Handoff System  
**Company:** Rohimaya Health AI  
**Founders:** Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO)

---

## Table of Contents

1. [Database Overview](#database-overview)
2. [Entity Relationship Diagram](#entity-relationship-diagram)
3. [Complete Table Definitions](#complete-table-definitions)
4. [Relationships & Foreign Keys](#relationships-foreign-keys)
5. [Indexes & Performance](#indexes-performance)
6. [Row-Level Security (RLS)](#row-level-security)
7. [Database Functions](#database-functions)
8. [Triggers & Automation](#triggers-automation)
9. [Views & Materialized Views](#views-materialized-views)
10. [Migration Scripts](#migration-scripts)
11. [Seed Data](#seed-data)
12. [Backup & Recovery](#backup-recovery)

---

## 1. Database Overview

### 1.1 Database Platform
**PostgreSQL 15+** via **Supabase**

**Key Features:**
- ACID compliance
- Row-Level Security (RLS) for HIPAA compliance
- Real-time subscriptions
- PostgREST API auto-generation
- Built-in authentication
- Point-in-time recovery
- Automated backups

### 1.2 Database Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  (Next.js Frontend + Express Backend + Supabase Client)     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    SUPABASE LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   PostgREST  │  │  Realtime    │  │   Auth       │     │
│  │   (REST API) │  │  (WebSocket) │  │   (JWT)      │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 POSTGRESQL DATABASE                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Core Tables (15 tables)                             │  │
│  │  - facilities, staff, patients, handoffs             │  │
│  │  - voice_recordings, ai_generations, sbar_reports    │  │
│  │  - handoff_assignments, audit_logs, notifications    │  │
│  │  - ehr_connections, ehr_sync_logs, user_sessions     │  │
│  │  - feature_flags, system_settings                    │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Security Layer                                       │  │
│  │  - Row-Level Security (RLS) policies                 │  │
│  │  - Encryption at rest (AES-256)                      │  │
│  │  - Audit logging triggers                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Database Schema Summary

**15 Core Tables:**

| Table | Purpose | Rows (Est.) | Growth Rate |
|-------|---------|-------------|-------------|
| facilities | Healthcare facilities | 6,000 | Low |
| staff | Healthcare professionals | 9,022,000 | Medium |
| patients | Patient records | 50M+ | High |
| handoffs | Clinical handoffs | 100M+ | Very High |
| voice_recordings | Audio files metadata | 100M+ | Very High |
| ai_generations | AI processing records | 100M+ | Very High |
| sbar_reports | Generated SBAR reports | 100M+ | Very High |
| handoff_assignments | Handoff-to-provider mapping | 100M+ | Very High |
| audit_logs | HIPAA audit trail | 500M+ | Very High |
| notifications | In-app notifications | 200M+ | Very High |
| ehr_connections | EHR integration configs | 10,000 | Low |
| ehr_sync_logs | EHR sync history | 10M+ | High |
| user_sessions | Active user sessions | 500,000 | Medium |
| feature_flags | Feature toggles | 100 | Low |
| system_settings | App configuration | 50 | Low |

### 1.4 Storage Requirements

**Initial (Year 1):**
- Database: ~100 GB
- Voice recordings (R2): ~5 TB
- SBAR documents (R2): ~50 GB

**Projected (Year 3):**
- Database: ~500 GB
- Voice recordings (R2): ~20 TB
- SBAR documents (R2): ~200 GB

---

## 2. Entity Relationship Diagram

### 2.1 High-Level ERD (Text-Based)

```
┌─────────────────┐
│   facilities    │
│─────────────────│
│ id (PK)         │
│ name            │
│ type            │
│ address         │
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐          ┌─────────────────┐
│      staff      │          │    patients     │
│─────────────────│          │─────────────────│
│ id (PK)         │          │ id (PK)         │
│ facility_id (FK)│          │ facility_id (FK)│
│ email           │          │ mrn             │
│ role            │          │ name            │
│ license_number  │          │ dob             │
└────────┬────────┘          └────────┬────────┘
         │                            │
         │                            │
         │ N:N (via handoff_         │ 1:N
         │      assignments)          │
         │                            │
         └──────────┬─────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │      handoffs        │
         │──────────────────────│
         │ id (PK)              │
         │ patient_id (FK)      │
         │ facility_id (FK)     │
         │ from_staff_id (FK)   │
         │ to_staff_id (FK)     │
         │ status               │
         │ created_at           │
         └──────────┬───────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        │ 1:1       │ 1:1       │ 1:N
        │           │           │
        ▼           ▼           ▼
┌───────────────┐ ┌──────────────┐ ┌──────────────────┐
│voice_recordings│ │sbar_reports  │ │handoff_assignments│
│───────────────│ │──────────────│ │──────────────────│
│ id (PK)       │ │ id (PK)      │ │ id (PK)          │
│ handoff_id(FK)│ │ handoff_id   │ │ handoff_id (FK)  │
│ duration      │ │ situation    │ │ staff_id (FK)    │
│ file_path     │ │ background   │ │ role             │
└───────┬───────┘ │ assessment   │ └──────────────────┘
        │         │ recommendation│
        │ 1:1     └──────────────┘
        │
        ▼
┌───────────────────┐
│  ai_generations   │
│───────────────────│
│ id (PK)           │
│ recording_id (FK) │
│ transcription     │
│ processing_time   │
└───────────────────┘

┌─────────────────┐     ┌──────────────────┐
│  audit_logs     │     │  notifications   │
│─────────────────│     │──────────────────│
│ id (PK)         │     │ id (PK)          │
│ user_id (FK)    │     │ user_id (FK)     │
│ action          │     │ handoff_id (FK)  │
│ resource        │     │ type             │
│ timestamp       │     │ read             │
└─────────────────┘     └──────────────────┘

┌──────────────────┐     ┌──────────────────┐
│ ehr_connections  │     │  ehr_sync_logs   │
│──────────────────│     │──────────────────│
│ id (PK)          │     │ id (PK)          │
│ facility_id (FK) │     │ connection_id(FK)│
│ ehr_type         │     │ sync_type        │
│ credentials      │     │ status           │
└──────────────────┘     └──────────────────┘

┌──────────────────┐     ┌──────────────────┐
│  user_sessions   │     │  feature_flags   │
│──────────────────│     │──────────────────│
│ id (PK)          │     │ id (PK)          │
│ user_id (FK)     │     │ name             │
│ token            │     │ enabled          │
│ expires_at       │     │ rollout_percent  │
└──────────────────┘     └──────────────────┘

┌──────────────────┐
│ system_settings  │
│──────────────────│
│ id (PK)          │
│ key              │
│ value            │
│ category         │
└──────────────────┘
```

### 2.2 Core Relationships

**1. Facilities → Staff (1:N)**
- One facility has many staff members
- Each staff member belongs to one facility

**2. Facilities → Patients (1:N)**
- One facility has many patients
- Each patient belongs to one facility

**3. Patients → Handoffs (1:N)**
- One patient can have many handoffs
- Each handoff belongs to one patient

**4. Staff ⟷ Handoffs (N:N via handoff_assignments)**
- Multiple staff can be involved in one handoff
- Each staff member can be involved in multiple handoffs

**5. Handoffs → Voice Recordings (1:1)**
- Each handoff has one voice recording
- Each voice recording belongs to one handoff

**6. Voice Recordings → AI Generations (1:1)**
- Each recording has one AI generation record
- Each AI generation belongs to one recording

**7. Handoffs → SBAR Reports (1:1)**
- Each handoff has one SBAR report
- Each SBAR report belongs to one handoff

---

## 3. Complete Table Definitions

### 3.1 Table: facilities

**Purpose:** Store healthcare facility information

```sql
CREATE TYPE facility_type AS ENUM (
  'hospital',
  'clinic',
  'nursing_home',
  'assisted_living',
  'home_health',
  'ambulatory_care',
  'rehabilitation',
  'mental_health'
);

CREATE TABLE facilities (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Basic Information
  name VARCHAR(255) NOT NULL,
  facility_type facility_type NOT NULL,
  license_number VARCHAR(100),
  
  -- Contact Information
  email VARCHAR(255),
  phone VARCHAR(20),
  fax VARCHAR(20),
  website VARCHAR(255),
  
  -- Address
  address_line1 VARCHAR(255) NOT NULL,
  address_line2 VARCHAR(255),
  city VARCHAR(100) NOT NULL,
  state VARCHAR(2) NOT NULL,
  zip_code VARCHAR(10) NOT NULL,
  country VARCHAR(2) DEFAULT 'US',
  
  -- Geolocation
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  timezone VARCHAR(50) DEFAULT 'America/New_York',
  
  -- Capacity & Statistics
  bed_count INTEGER,
  staff_count INTEGER,
  annual_admissions INTEGER,
  
  -- EHR Information
  primary_ehr VARCHAR(50),
  ehr_version VARCHAR(20),
  
  -- Subscription & Billing
  subscription_tier VARCHAR(20) DEFAULT 'free',
  subscription_status VARCHAR(20) DEFAULT 'active',
  trial_ends_at TIMESTAMPTZ,
  billing_email VARCHAR(255),
  
  -- Metadata
  is_active BOOLEAN DEFAULT true,
  onboarded_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_by UUID,
  updated_by UUID,
  
  -- Constraints
  CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
  CONSTRAINT valid_phone CHECK (phone ~* '^\+?[1-9]\d{1,14}$'),
  CONSTRAINT valid_state CHECK (state ~* '^[A-Z]{2}$'),
  CONSTRAINT positive_bed_count CHECK (bed_count > 0),
  CONSTRAINT positive_staff_count CHECK (staff_count > 0)
);

-- Indexes
CREATE INDEX idx_facilities_name ON facilities USING gin(to_tsvector('english', name));
CREATE INDEX idx_facilities_type ON facilities(facility_type);
CREATE INDEX idx_facilities_location ON facilities(state, city);
CREATE INDEX idx_facilities_active ON facilities(is_active) WHERE is_active = true;
CREATE INDEX idx_facilities_subscription ON facilities(subscription_tier, subscription_status);

-- Comments
COMMENT ON TABLE facilities IS 'Healthcare facilities using EclipseLink AI';
COMMENT ON COLUMN facilities.primary_ehr IS 'Primary EHR system (Epic, Cerner, MEDITECH, etc.)';
COMMENT ON COLUMN facilities.subscription_tier IS 'free, basic, professional, enterprise';
```

### 3.2 Table: staff

**Purpose:** Store healthcare professional information

```sql
CREATE TYPE user_role AS ENUM (
  'registered_nurse',
  'licensed_practical_nurse',
  'certified_nursing_assistant',
  'medical_assistant',
  'physician',
  'nurse_practitioner',
  'physician_assistant',
  'respiratory_therapist',
  'physical_therapist',
  'occupational_therapist',
  'emergency_medical_technician',
  'radiologic_technician',
  'surgical_technician',
  'lab_technician',
  'pharmacy_technician',
  'admin',
  'super_admin'
);

CREATE TYPE employment_status AS ENUM (
  'full_time',
  'part_time',
  'per_diem',
  'contract',
  'inactive'
);

CREATE TABLE staff (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  facility_id UUID NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
  
  -- Authentication (synced with Supabase Auth)
  auth_id UUID UNIQUE, -- References auth.users.id
  email VARCHAR(255) UNIQUE NOT NULL,
  email_verified BOOLEAN DEFAULT false,
  
  -- Personal Information
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  middle_name VARCHAR(100),
  preferred_name VARCHAR(100),
  suffix VARCHAR(10),
  
  -- Professional Information
  role user_role NOT NULL,
  title VARCHAR(100),
  department VARCHAR(100),
  specialty VARCHAR(100),
  license_number VARCHAR(100),
  license_state VARCHAR(2),
  license_expiry DATE,
  npi_number VARCHAR(10),
  dea_number VARCHAR(20),
  
  -- Contact Information
  phone VARCHAR(20),
  mobile VARCHAR(20),
  emergency_contact_name VARCHAR(200),
  emergency_contact_phone VARCHAR(20),
  
  -- Employment
  employment_status employment_status DEFAULT 'full_time',
  hire_date DATE,
  termination_date DATE,
  
  -- Preferences
  preferred_language VARCHAR(10) DEFAULT 'en',
  timezone VARCHAR(50) DEFAULT 'America/New_York',
  notification_preferences JSONB DEFAULT '{"email": true, "push": true, "sms": false}',
  
  -- Profile
  avatar_url TEXT,
  bio TEXT,
  
  -- Security
  last_login_at TIMESTAMPTZ,
  last_login_ip INET,
  failed_login_attempts INTEGER DEFAULT 0,
  locked_until TIMESTAMPTZ,
  mfa_enabled BOOLEAN DEFAULT false,
  mfa_secret TEXT,
  
  -- Metadata
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_by UUID,
  updated_by UUID,
  
  -- Constraints
  CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
  CONSTRAINT valid_phone CHECK (phone ~* '^\+?[1-9]\d{1,14}$'),
  CONSTRAINT valid_mobile CHECK (mobile ~* '^\+?[1-9]\d{1,14}$'),
  CONSTRAINT valid_npi CHECK (npi_number ~* '^\d{10}$' OR npi_number IS NULL),
  CONSTRAINT valid_license_state CHECK (license_state ~* '^[A-Z]{2}$' OR license_state IS NULL),
  CONSTRAINT employment_dates CHECK (termination_date IS NULL OR termination_date >= hire_date)
);

-- Indexes
CREATE INDEX idx_staff_facility ON staff(facility_id);
CREATE INDEX idx_staff_auth ON staff(auth_id);
CREATE INDEX idx_staff_email ON staff(email);
CREATE INDEX idx_staff_role ON staff(role);
CREATE INDEX idx_staff_name ON staff(last_name, first_name);
CREATE INDEX idx_staff_active ON staff(facility_id, is_active) WHERE is_active = true;
CREATE INDEX idx_staff_department ON staff(facility_id, department);
CREATE INDEX idx_staff_search ON staff USING gin(
  to_tsvector('english', 
    coalesce(first_name, '') || ' ' || 
    coalesce(last_name, '') || ' ' || 
    coalesce(email, '')
  )
);

-- Comments
COMMENT ON TABLE staff IS 'Healthcare professionals using EclipseLink AI';
COMMENT ON COLUMN staff.auth_id IS 'References Supabase auth.users.id';
COMMENT ON COLUMN staff.npi_number IS 'National Provider Identifier (10 digits)';
COMMENT ON COLUMN staff.dea_number IS 'Drug Enforcement Administration number';
```

### 3.3 Table: patients

**Purpose:** Store patient demographic and medical information

```sql
CREATE TYPE gender AS ENUM ('male', 'female', 'other', 'unknown');
CREATE TYPE blood_type AS ENUM ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'unknown');
CREATE TYPE patient_status AS ENUM ('active', 'discharged', 'deceased', 'transferred');

CREATE TABLE patients (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  facility_id UUID NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
  
  -- Patient Identifiers (PHI)
  mrn VARCHAR(50) NOT NULL, -- Medical Record Number
  ssn_encrypted TEXT, -- Encrypted SSN
  external_id VARCHAR(100), -- EHR patient ID
  
  -- Personal Information (PHI)
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  middle_name VARCHAR(100),
  preferred_name VARCHAR(100),
  suffix VARCHAR(10),
  
  -- Demographics
  date_of_birth DATE NOT NULL,
  gender gender NOT NULL,
  race VARCHAR(50),
  ethnicity VARCHAR(50),
  preferred_language VARCHAR(10) DEFAULT 'en',
  
  -- Contact Information (PHI)
  phone VARCHAR(20),
  email VARCHAR(255),
  address_line1 VARCHAR(255),
  address_line2 VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(2),
  zip_code VARCHAR(10),
  country VARCHAR(2) DEFAULT 'US',
  
  -- Emergency Contact (PHI)
  emergency_contact_name VARCHAR(200),
  emergency_contact_relationship VARCHAR(50),
  emergency_contact_phone VARCHAR(20),
  
  -- Medical Information
  blood_type blood_type DEFAULT 'unknown',
  primary_diagnosis TEXT,
  chief_complaint TEXT,
  
  -- Allergies (stored as JSONB array)
  allergies JSONB DEFAULT '[]',
  -- Example: [{"allergen": "Penicillin", "reaction": "Rash", "severity": "Moderate"}]
  
  -- Current Medications (stored as JSONB array)
  medications JSONB DEFAULT '[]',
  -- Example: [{"name": "Lisinopril", "dose": "10mg", "frequency": "Daily"}]
  
  -- Vital Signs (latest)
  vital_signs JSONB,
  -- Example: {"temperature": 98.6, "bp_systolic": 120, "bp_diastolic": 80, "heart_rate": 72}
  vital_signs_updated_at TIMESTAMPTZ,
  
  -- Admission Information
  admission_date TIMESTAMPTZ,
  discharge_date TIMESTAMPTZ,
  length_of_stay INTEGER GENERATED ALWAYS AS (
    CASE 
      WHEN discharge_date IS NOT NULL 
      THEN EXTRACT(DAY FROM discharge_date - admission_date)
      ELSE NULL
    END
  ) STORED,
  room_number VARCHAR(20),
  bed_number VARCHAR(20),
  
  -- Insurance Information (PHI)
  insurance_provider VARCHAR(100),
  insurance_policy_number VARCHAR(100),
  insurance_group_number VARCHAR(100),
  
  -- Status
  status patient_status DEFAULT 'active',
  
  -- EHR Sync
  last_synced_at TIMESTAMPTZ,
  sync_status VARCHAR(20),
  
  -- Metadata
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_by UUID REFERENCES staff(id),
  updated_by UUID REFERENCES staff(id),
  
  -- Constraints
  CONSTRAINT unique_mrn_per_facility UNIQUE(facility_id, mrn),
  CONSTRAINT valid_phone CHECK (phone ~* '^\+?[1-9]\d{1,14}$' OR phone IS NULL),
  CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' OR email IS NULL),
  CONSTRAINT valid_dob CHECK (date_of_birth <= CURRENT_DATE),
  CONSTRAINT valid_admission CHECK (admission_date <= COALESCE(discharge_date, NOW())),
  CONSTRAINT valid_status_dates CHECK (
    (status = 'discharged' AND discharge_date IS NOT NULL) OR
    (status != 'discharged' AND discharge_date IS NULL) OR
    (status = 'deceased')
  )
);

-- Indexes
CREATE INDEX idx_patients_facility ON patients(facility_id);
CREATE INDEX idx_patients_mrn ON patients(facility_id, mrn);
CREATE INDEX idx_patients_external_id ON patients(external_id);
CREATE INDEX idx_patients_name ON patients(last_name, first_name);
CREATE INDEX idx_patients_dob ON patients(date_of_birth);
CREATE INDEX idx_patients_status ON patients(status) WHERE status = 'active';
CREATE INDEX idx_patients_admission ON patients(admission_date) WHERE status = 'active';
CREATE INDEX idx_patients_search ON patients USING gin(
  to_tsvector('english', 
    coalesce(first_name, '') || ' ' || 
    coalesce(last_name, '') || ' ' || 
    coalesce(mrn, '')
  )
);

-- Comments
COMMENT ON TABLE patients IS 'Patient demographic and medical information (PHI)';
COMMENT ON COLUMN patients.mrn IS 'Medical Record Number - unique per facility';
COMMENT ON COLUMN patients.ssn_encrypted IS 'Encrypted Social Security Number';
COMMENT ON COLUMN patients.allergies IS 'Array of allergy objects';
COMMENT ON COLUMN patients.medications IS 'Array of current medication objects';
COMMENT ON COLUMN patients.vital_signs IS 'Latest vital signs snapshot';
```

### 3.4 Table: handoffs

**Purpose:** Store clinical handoff records

```sql
CREATE TYPE handoff_status AS ENUM (
  'draft',
  'recording',
  'transcribing',
  'generating',
  'ready',
  'assigned',
  'accepted',
  'completed',
  'cancelled',
  'failed'
);

CREATE TYPE handoff_priority AS ENUM ('routine', 'urgent', 'emergent');

CREATE TABLE handoffs (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
  facility_id UUID NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
  from_staff_id UUID NOT NULL REFERENCES staff(id) ON DELETE SET NULL,
  to_staff_id UUID REFERENCES staff(id) ON DELETE SET NULL,
  
  -- Handoff Details
  status handoff_status DEFAULT 'draft',
  priority handoff_priority DEFAULT 'routine',
  handoff_type VARCHAR(50) DEFAULT 'shift_change',
  -- Types: shift_change, transfer, admission, discharge, procedure
  
  -- Clinical Context
  location VARCHAR(100), -- Current location (room, unit)
  scheduled_time TIMESTAMPTZ,
  actual_time TIMESTAMPTZ,
  
  -- Processing Times (for analytics)
  voice_recording_started_at TIMESTAMPTZ,
  voice_recording_completed_at TIMESTAMPTZ,
  transcription_started_at TIMESTAMPTZ,
  transcription_completed_at TIMESTAMPTZ,
  sbar_generation_started_at TIMESTAMPTZ,
  sbar_generation_completed_at TIMESTAMPTZ,
  
  -- Calculated Durations
  recording_duration INTEGER, -- seconds
  transcription_duration INTEGER, -- seconds
  sbar_generation_duration INTEGER, -- seconds
  total_processing_time INTEGER GENERATED ALWAYS AS (
    COALESCE(transcription_duration, 0) + COALESCE(sbar_generation_duration, 0)
  ) STORED,
  
  -- Notes
  clinical_notes TEXT,
  internal_notes TEXT, -- Staff-only notes
  
  -- Quality Metrics
  quality_score DECIMAL(3, 2), -- 0.00 to 1.00
  reviewed_by UUID REFERENCES staff(id),
  reviewed_at TIMESTAMPTZ,
  review_comments TEXT,
  
  -- Flags
  is_critical BOOLEAN DEFAULT false,
  requires_followup BOOLEAN DEFAULT false,
  flagged_for_review BOOLEAN DEFAULT false,
  
  -- EHR Export
  exported_to_ehr BOOLEAN DEFAULT false,
  export_attempted_at TIMESTAMPTZ,
  export_completed_at TIMESTAMPTZ,
  export_error TEXT,
  
  -- Metadata
  version INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  cancelled_at TIMESTAMPTZ,
  cancelled_by UUID REFERENCES staff(id),
  cancellation_reason TEXT,
  
  -- Constraints
  CONSTRAINT valid_staff CHECK (from_staff_id != to_staff_id OR to_staff_id IS NULL),
  CONSTRAINT valid_times CHECK (
    actual_time IS NULL OR 
    actual_time >= voice_recording_started_at
  ),
  CONSTRAINT valid_quality_score CHECK (quality_score >= 0 AND quality_score <= 1),
  CONSTRAINT completed_has_time CHECK (
    (status = 'completed' AND completed_at IS NOT NULL) OR
    (status != 'completed' AND completed_at IS NULL)
  ),
  CONSTRAINT cancelled_has_reason CHECK (
    (status = 'cancelled' AND cancellation_reason IS NOT NULL) OR
    (status != 'cancelled')
  )
);

-- Indexes
CREATE INDEX idx_handoffs_patient ON handoffs(patient_id);
CREATE INDEX idx_handoffs_facility ON handoffs(facility_id);
CREATE INDEX idx_handoffs_from_staff ON handoffs(from_staff_id);
CREATE INDEX idx_handoffs_to_staff ON handoffs(to_staff_id);
CREATE INDEX idx_handoffs_status ON handoffs(status);
CREATE INDEX idx_handoffs_priority ON handoffs(priority) WHERE priority IN ('urgent', 'emergent');
CREATE INDEX idx_handoffs_created ON handoffs(created_at DESC);
CREATE INDEX idx_handoffs_facility_created ON handoffs(facility_id, created_at DESC);
CREATE INDEX idx_handoffs_facility_status ON handoffs(facility_id, status);
CREATE INDEX idx_handoffs_active ON handoffs(facility_id, status) 
  WHERE status NOT IN ('completed', 'cancelled');
CREATE INDEX idx_handoffs_scheduled ON handoffs(scheduled_time) 
  WHERE status NOT IN ('completed', 'cancelled');
CREATE INDEX idx_handoffs_review ON handoffs(facility_id, flagged_for_review) 
  WHERE flagged_for_review = true;

-- Comments
COMMENT ON TABLE handoffs IS 'Clinical handoff records with SBAR generation tracking';
COMMENT ON COLUMN handoffs.handoff_type IS 'shift_change, transfer, admission, discharge, procedure';
COMMENT ON COLUMN handoffs.quality_score IS 'AI-generated quality score (0.00-1.00)';
COMMENT ON COLUMN handoffs.total_processing_time IS 'Computed: transcription + SBAR generation time';
```

### 3.5 Table: voice_recordings

**Purpose:** Store voice recording metadata

```sql
CREATE TYPE recording_status AS ENUM (
  'uploading',
  'uploaded',
  'processing',
  'transcribed',
  'failed',
  'deleted'
);

CREATE TYPE audio_format AS ENUM ('webm', 'mp3', 'wav', 'ogg', 'm4a');

CREATE TABLE voice_recordings (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  handoff_id UUID NOT NULL REFERENCES handoffs(id) ON DELETE CASCADE,
  uploaded_by UUID NOT NULL REFERENCES staff(id) ON DELETE SET NULL,
  
  -- Recording Details
  status recording_status DEFAULT 'uploading',
  duration INTEGER NOT NULL, -- seconds
  file_size BIGINT NOT NULL, -- bytes
  audio_format audio_format NOT NULL,
  sample_rate INTEGER, -- Hz (e.g., 48000)
  bit_rate INTEGER, -- kbps (e.g., 128)
  channels INTEGER DEFAULT 1, -- mono or stereo
  
  -- Storage
  file_path TEXT NOT NULL, -- R2 path
  file_url TEXT, -- Pre-signed URL (temporary)
  file_url_expires_at TIMESTAMPTZ,
  
  -- Processing
  transcription_job_id VARCHAR(100), -- BullMQ job ID
  transcription_attempts INTEGER DEFAULT 0,
  last_transcription_error TEXT,
  
  -- Quality Metrics
  audio_quality_score DECIMAL(3, 2), -- 0.00 to 1.00
  silence_percentage DECIMAL(5, 2), -- Percentage of silence
  noise_level DECIMAL(5, 2), -- Background noise level
  
  -- Metadata
  recorded_at TIMESTAMPTZ,
  uploaded_at TIMESTAMPTZ DEFAULT NOW(),
  processed_at TIMESTAMPTZ,
  deleted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Constraints
  CONSTRAINT positive_duration CHECK (duration > 0),
  CONSTRAINT positive_file_size CHECK (file_size > 0),
  CONSTRAINT valid_quality_score CHECK (
    audio_quality_score IS NULL OR 
    (audio_quality_score >= 0 AND audio_quality_score <= 1)
  ),
  CONSTRAINT valid_silence CHECK (
    silence_percentage IS NULL OR 
    (silence_percentage >= 0 AND silence_percentage <= 100)
  )
);

-- Indexes
CREATE INDEX idx_voice_handoff ON voice_recordings(handoff_id);
CREATE INDEX idx_voice_uploaded_by ON voice_recordings(uploaded_by);
CREATE INDEX idx_voice_status ON voice_recordings(status);
CREATE INDEX idx_voice_uploaded ON voice_recordings(uploaded_at DESC);
CREATE INDEX idx_voice_processing ON voice_recordings(status) 
  WHERE status IN ('uploading', 'uploaded', 'processing');
CREATE INDEX idx_voice_failed ON voice_recordings(status, transcription_attempts) 
  WHERE status = 'failed';

-- Comments
COMMENT ON TABLE voice_recordings IS 'Voice recording metadata (files stored in R2)';
COMMENT ON COLUMN voice_recordings.file_path IS 'Path in Cloudflare R2 bucket';
COMMENT ON COLUMN voice_recordings.audio_quality_score IS 'Computed audio quality (0.00-1.00)';
```

### 3.6 Table: ai_generations

**Purpose:** Store AI processing records (transcription + SBAR generation)

```sql
CREATE TYPE generation_stage AS ENUM ('transcription', 'sbar_generation');
CREATE TYPE generation_status AS ENUM ('queued', 'processing', 'completed', 'failed');

CREATE TABLE ai_generations (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  voice_recording_id UUID NOT NULL REFERENCES voice_recordings(id) ON DELETE CASCADE,
  handoff_id UUID NOT NULL REFERENCES handoffs(id) ON DELETE CASCADE,
  
  -- Processing Stage
  stage generation_stage NOT NULL,
  status generation_status DEFAULT 'queued',
  
  -- Transcription
  transcription TEXT,
  transcription_confidence DECIMAL(3, 2), -- 0.00 to 1.00
  transcription_language VARCHAR(10) DEFAULT 'en',
  transcription_word_count INTEGER,
  
  -- Azure OpenAI Details
  azure_request_id VARCHAR(100),
  model_name VARCHAR(50), -- whisper-1, gpt-4-32k
  deployment_name VARCHAR(100),
  
  -- Token Usage (for GPT-4)
  prompt_tokens INTEGER,
  completion_tokens INTEGER,
  total_tokens INTEGER GENERATED ALWAYS AS (
    COALESCE(prompt_tokens, 0) + COALESCE(completion_tokens, 0)
  ) STORED,
  
  -- Processing Times
  processing_started_at TIMESTAMPTZ,
  processing_completed_at TIMESTAMPTZ,
  processing_duration INTEGER, -- milliseconds
  
  -- Retry Logic
  attempt_number INTEGER DEFAULT 1,
  max_attempts INTEGER DEFAULT 3,
  retry_after TIMESTAMPTZ,
  
  -- Error Handling
  error_code VARCHAR(50),
  error_message TEXT,
  error_stack TEXT,
  
  -- Quality Metrics
  quality_score DECIMAL(3, 2),
  flagged_for_review BOOLEAN DEFAULT false,
  review_notes TEXT,
  
  -- Cost Tracking (approximate)
  estimated_cost DECIMAL(10, 4), -- USD
  
  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Constraints
  CONSTRAINT valid_confidence CHECK (
    transcription_confidence IS NULL OR 
    (transcription_confidence >= 0 AND transcription_confidence <= 1)
  ),
  CONSTRAINT valid_quality_score CHECK (
    quality_score IS NULL OR 
    (quality_score >= 0 AND quality_score <= 1)
  ),
  CONSTRAINT valid_attempts CHECK (attempt_number <= max_attempts),
  CONSTRAINT completed_has_duration CHECK (
    (status = 'completed' AND processing_duration IS NOT NULL) OR
    (status != 'completed')
  )
);

-- Indexes
CREATE INDEX idx_ai_recording ON ai_generations(voice_recording_id);
CREATE INDEX idx_ai_handoff ON ai_generations(handoff_id);
CREATE INDEX idx_ai_stage_status ON ai_generations(stage, status);
CREATE INDEX idx_ai_created ON ai_generations(created_at DESC);
CREATE INDEX idx_ai_failed ON ai_generations(status, attempt_number) 
  WHERE status = 'failed';
CREATE INDEX idx_ai_review ON ai_generations(flagged_for_review) 
  WHERE flagged_for_review = true;

-- Comments
COMMENT ON TABLE ai_generations IS 'AI processing records for transcription and SBAR generation';
COMMENT ON COLUMN ai_generations.transcription_confidence IS 'Whisper API confidence score (0.00-1.00)';
COMMENT ON COLUMN ai_generations.estimated_cost IS 'Approximate Azure OpenAI API cost in USD';
```

### 3.7 Table: sbar_reports

**Purpose:** Store generated SBAR reports

```sql
CREATE TABLE sbar_reports (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  handoff_id UUID NOT NULL UNIQUE REFERENCES handoffs(id) ON DELETE CASCADE,
  generated_by_ai UUID REFERENCES ai_generations(id),
  
  -- SBAR Content
  situation TEXT NOT NULL,
  background TEXT NOT NULL,
  assessment TEXT NOT NULL,
  recommendation TEXT NOT NULL,
  
  -- Additional Sections
  current_status TEXT,
  vital_signs JSONB,
  medications JSONB,
  allergies JSONB,
  recent_labs JSONB,
  pending_tasks JSONB,
  
  -- Formatting
  formatted_html TEXT,
  formatted_markdown TEXT,
  
  -- Version Control
  version INTEGER DEFAULT 1,
  is_latest BOOLEAN DEFAULT true,
  previous_version_id UUID REFERENCES sbar_reports(id),
  
  -- Editing History
  edited_by UUID REFERENCES staff(id),
  edited_at TIMESTAMPTZ,
  edit_summary TEXT,
  
  -- Approval
  approved_by UUID REFERENCES staff(id),
  approved_at TIMESTAMPTZ,
  approval_notes TEXT,
  
  -- Quality Metrics
  completeness_score DECIMAL(3, 2), -- 0.00 to 1.00
  readability_score DECIMAL(3, 2), -- 0.00 to 1.00
  clinical_accuracy_score DECIMAL(3, 2), -- 0.00 to 1.00 (manual review)
  
  -- Export
  exported_formats JSONB DEFAULT '[]', -- ['pdf', 'docx', 'ehr']
  last_exported_at TIMESTAMPTZ,
  
  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Constraints
  CONSTRAINT valid_completeness CHECK (
    completeness_score IS NULL OR 
    (completeness_score >= 0 AND completeness_score <= 1)
  ),
  CONSTRAINT valid_readability CHECK (
    readability_score IS NULL OR 
    (readability_score >= 0 AND readability_score <= 1)
  ),
  CONSTRAINT valid_clinical_accuracy CHECK (
    clinical_accuracy_score IS NULL OR 
    (clinical_accuracy_score >= 0 AND clinical_accuracy_score <= 1)
  ),
  CONSTRAINT approved_has_approver CHECK (
    (approved_at IS NOT NULL AND approved_by IS NOT NULL) OR
    (approved_at IS NULL AND approved_by IS NULL)
  )
);

-- Indexes
CREATE INDEX idx_sbar_handoff ON sbar_reports(handoff_id);
CREATE INDEX idx_sbar_generated_by ON sbar_reports(generated_by_ai);
CREATE INDEX idx_sbar_latest ON sbar_reports(handoff_id, is_latest) WHERE is_latest = true;
CREATE INDEX idx_sbar_approved ON sbar_reports(approved_by, approved_at);
CREATE INDEX idx_sbar_created ON sbar_reports(created_at DESC);
CREATE INDEX idx_sbar_search ON sbar_reports USING gin(
  to_tsvector('english', 
    coalesce(situation, '') || ' ' || 
    coalesce(background, '') || ' ' || 
    coalesce(assessment, '') || ' ' || 
    coalesce(recommendation, '')
  )
);

-- Comments
COMMENT ON TABLE sbar_reports IS 'Generated SBAR reports with version control';
COMMENT ON COLUMN sbar_reports.is_latest IS 'True if this is the most recent version';
COMMENT ON COLUMN sbar_reports.completeness_score IS 'AI-assessed completeness (0.00-1.00)';
```

### 3.8 Table: handoff_assignments

**Purpose:** Track staff assignments to handoffs (N:N relationship)

```sql
CREATE TYPE assignment_role AS ENUM (
  'giving',
  'receiving',
  'supervising',
  'cc', -- Carbon copy
  'reviewing'
);

CREATE TYPE assignment_status AS ENUM (
  'pending',
  'notified',
  'viewed',
  'accepted',
  'declined',
  'completed'
);

CREATE TABLE handoff_assignments (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  handoff_id UUID NOT NULL REFERENCES handoffs(id) ON DELETE CASCADE,
  staff_id UUID NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
  assigned_by UUID REFERENCES staff(id),
  
  -- Assignment Details
  role assignment_role NOT NULL,
  status assignment_status DEFAULT 'pending',
  
  -- Notifications
  notified_at TIMESTAMPTZ,
  notification_method VARCHAR(20), -- email, push, sms
  viewed_at TIMESTAMPTZ,
  
  -- Response
  responded_at TIMESTAMPTZ,
  response_notes TEXT,
  
  -- Completion
  completed_at TIMESTAMPTZ,
  completion_notes TEXT,
  
  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Constraints
  CONSTRAINT unique_handoff_staff_role UNIQUE(handoff_id, staff_id, role),
  CONSTRAINT valid_response_time CHECK (
    responded_at IS NULL OR responded_at >= notified_at
  ),
  CONSTRAINT valid_completion_time CHECK (
    completed_at IS NULL OR completed_at >= responded_at
  )
);

-- Indexes
CREATE INDEX idx_assignments_handoff ON handoff_assignments(handoff_id);
CREATE INDEX idx_assignments_staff ON handoff_assignments(staff_id);
CREATE INDEX idx_assignments_status ON handoff_assignments(status);
CREATE INDEX idx_assignments_staff_status ON handoff_assignments(staff_id, status) 
  WHERE status IN ('pending', 'notified', 'viewed');
CREATE INDEX idx_assignments_pending ON handoff_assignments(staff_id, status, created_at DESC) 
  WHERE status = 'pending';

-- Comments
COMMENT ON TABLE handoff_assignments IS 'Staff assignments to handoffs (many-to-many)';
COMMENT ON COLUMN handoff_assignments.role IS 'Staff role in handoff: giving, receiving, supervising, cc, reviewing';
```

### 3.9 Table: audit_logs

**Purpose:** HIPAA-compliant audit trail

```sql
CREATE TYPE audit_action AS ENUM (
  'create',
  'read',
  'update',
  'delete',
  'export',
  'print',
  'share',
  'login',
  'logout',
  'failed_login',
  'password_change',
  'permission_change'
);

CREATE TABLE audit_logs (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Who
  user_id UUID REFERENCES staff(id),
  user_email VARCHAR(255),
  user_role user_role,
  
  -- What
  action audit_action NOT NULL,
  resource VARCHAR(50) NOT NULL, -- table name: patients, handoffs, etc.
  resource_id UUID,
  
  -- Details
  changes JSONB, -- Before/after values
  request_payload JSONB,
  response_status INTEGER,
  
  -- Where
  ip_address INET,
  user_agent TEXT,
  facility_id UUID REFERENCES facilities(id),
  
  -- When
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  
  -- PHI Access Tracking
  phi_accessed BOOLEAN DEFAULT false,
  phi_type VARCHAR(50), -- patient_demographics, medical_records, etc.
  
  -- Security
  severity VARCHAR(20) DEFAULT 'info', -- info, warning, error, critical
  flagged BOOLEAN DEFAULT false,
  flag_reason TEXT
);

-- Indexes
CREATE INDEX idx_audit_user ON audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_action ON audit_logs(action, created_at DESC);
CREATE INDEX idx_audit_resource ON audit_logs(resource, resource_id);
CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_phi ON audit_logs(phi_accessed) WHERE phi_accessed = true;
CREATE INDEX idx_audit_flagged ON audit_logs(flagged) WHERE flagged = true;
CREATE INDEX idx_audit_facility ON audit_logs(facility_id, created_at DESC);
CREATE INDEX idx_audit_ip ON audit_logs(ip_address, created_at DESC);

-- Partitioning by month (for performance)
-- This would be set up separately during deployment

-- Comments
COMMENT ON TABLE audit_logs IS 'HIPAA-compliant audit trail (7-year retention)';
COMMENT ON COLUMN audit_logs.phi_accessed IS 'True if action accessed Protected Health Information';
COMMENT ON COLUMN audit_logs.changes IS 'JSON object with before/after values';
```

### 3.10 Table: notifications

**Purpose:** In-app notifications

```sql
CREATE TYPE notification_type AS ENUM (
  'handoff_assigned',
  'handoff_completed',
  'handoff_cancelled',
  'sbar_ready',
  'ehr_sync_success',
  'ehr_sync_failed',
  'system_alert',
  'mention',
  'reminder'
);

CREATE TYPE notification_priority AS ENUM ('low', 'normal', 'high', 'urgent');

CREATE TABLE notifications (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  user_id UUID NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
  handoff_id UUID REFERENCES handoffs(id) ON DELETE CASCADE,
  
  -- Notification Details
  type notification_type NOT NULL,
  priority notification_priority DEFAULT 'normal',
  title VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  
  -- Action
  action_url TEXT,
  action_text VARCHAR(50),
  
  -- Status
  is_read BOOLEAN DEFAULT false,
  read_at TIMESTAMPTZ,
  
  -- Delivery
  sent_via_email BOOLEAN DEFAULT false,
  sent_via_push BOOLEAN DEFAULT false,
  sent_via_sms BOOLEAN DEFAULT false,
  email_sent_at TIMESTAMPTZ,
  push_sent_at TIMESTAMPTZ,
  sms_sent_at TIMESTAMPTZ,
  
  -- Metadata
  metadata JSONB,
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Constraints
  CONSTRAINT valid_read_time CHECK (
    (is_read = true AND read_at IS NOT NULL) OR
    (is_read = false AND read_at IS NULL)
  )
);

-- Indexes
CREATE INDEX idx_notifications_user ON notifications(user_id, created_at DESC);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read) 
  WHERE is_read = false;
CREATE INDEX idx_notifications_handoff ON notifications(handoff_id);
CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_priority ON notifications(priority, created_at DESC) 
  WHERE priority IN ('high', 'urgent');
CREATE INDEX idx_notifications_expires ON notifications(expires_at) 
  WHERE expires_at IS NOT NULL AND is_read = false;

-- Comments
COMMENT ON TABLE notifications IS 'In-app notifications for users';
COMMENT ON COLUMN notifications.expires_at IS 'Notification auto-dismissed after this time';
```

### 3.11 Table: ehr_connections

**Purpose:** EHR integration configuration

```sql
CREATE TYPE ehr_type AS ENUM ('epic', 'cerner', 'meditech', 'allscripts', 'protouch', 'pointclickcare', 'wellsky', 'other');
CREATE TYPE ehr_protocol AS ENUM ('fhir_r4', 'hl7_v2', 'hl7_v3', 'rest', 'soap');
CREATE TYPE connection_status AS ENUM ('active', 'inactive', 'testing', 'error');

CREATE TABLE ehr_connections (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  facility_id UUID NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
  
  -- EHR Details
  ehr_type ehr_type NOT NULL,
  ehr_version VARCHAR(50),
  protocol ehr_protocol NOT NULL,
  
  -- Connection
  base_url TEXT NOT NULL,
  fhir_base_url TEXT, -- For FHIR endpoints
  auth_type VARCHAR(50) NOT NULL, -- oauth2, basic, api_key
  
  -- Credentials (encrypted)
  client_id_encrypted TEXT,
  client_secret_encrypted TEXT,
  api_key_encrypted TEXT,
  username_encrypted TEXT,
  password_encrypted TEXT,
  
  -- OAuth Tokens
  access_token_encrypted TEXT,
  refresh_token_encrypted TEXT,
  token_expires_at TIMESTAMPTZ,
  
  -- Configuration
  config JSONB, -- Additional configuration
  supported_resources JSONB, -- List of FHIR resources or HL7 message types
  
  -- Status
  status connection_status DEFAULT 'inactive',
  last_test_at TIMESTAMPTZ,
  last_test_result TEXT,
  last_successful_connection TIMESTAMPTZ,
  
  -- Sync Settings
  auto_sync_enabled BOOLEAN DEFAULT false,
  sync_frequency_minutes INTEGER DEFAULT 60,
  last_sync_at TIMESTAMPTZ,
  
  -- Metadata
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_by UUID REFERENCES staff(id),
  
  -- Constraints
  CONSTRAINT valid_sync_frequency CHECK (sync_frequency_minutes > 0),
  CONSTRAINT valid_base_url CHECK (base_url ~* '^https?://.*')
);

-- Indexes
CREATE INDEX idx_ehr_facility ON ehr_connections(facility_id);
CREATE INDEX idx_ehr_type ON ehr_connections(ehr_type);
CREATE INDEX idx_ehr_status ON ehr_connections(status);
CREATE INDEX idx_ehr_active ON ehr_connections(facility_id, is_active) WHERE is_active = true;

-- Comments
COMMENT ON TABLE ehr_connections IS 'EHR integration configuration per facility';
COMMENT ON COLUMN ehr_connections.client_id_encrypted IS 'Encrypted with facility-specific key';
COMMENT ON COLUMN ehr_connections.supported_resources IS 'Array of FHIR resources: ["Patient", "Observation", etc.]';
```

### 3.12 Table: ehr_sync_logs

**Purpose:** EHR synchronization history

```sql
CREATE TYPE sync_type AS ENUM ('patient_import', 'patient_export', 'handoff_export', 'medication_sync', 'allergy_sync', 'vital_signs_sync');
CREATE TYPE sync_status AS ENUM ('started', 'in_progress', 'completed', 'failed', 'partial');

CREATE TABLE ehr_sync_logs (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  connection_id UUID NOT NULL REFERENCES ehr_connections(id) ON DELETE CASCADE,
  facility_id UUID NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
  initiated_by UUID REFERENCES staff(id),
  
  -- Sync Details
  sync_type sync_type NOT NULL,
  status sync_status DEFAULT 'started',
  
  -- Scope
  patient_id UUID REFERENCES patients(id),
  handoff_id UUID REFERENCES handoffs(id),
  
  -- Results
  records_processed INTEGER DEFAULT 0,
  records_succeeded INTEGER DEFAULT 0,
  records_failed INTEGER DEFAULT 0,
  
  -- Timing
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  duration_ms INTEGER,
  
  -- Error Handling
  error_code VARCHAR(50),
  error_message TEXT,
  error_details JSONB,
  
  -- Request/Response
  request_payload JSONB,
  response_payload JSONB,
  
  -- Metadata
  metadata JSONB,
  
  -- Constraints
  CONSTRAINT valid_counts CHECK (
    records_succeeded + records_failed <= records_processed
  ),
  CONSTRAINT completed_has_time CHECK (
    (status = 'completed' AND completed_at IS NOT NULL) OR
    (status != 'completed')
  )
);

-- Indexes
CREATE INDEX idx_sync_connection ON ehr_sync_logs(connection_id);
CREATE INDEX idx_sync_facility ON ehr_sync_logs(facility_id, started_at DESC);
CREATE INDEX idx_sync_type ON ehr_sync_logs(sync_type);
CREATE INDEX idx_sync_status ON ehr_sync_logs(status);
CREATE INDEX idx_sync_patient ON ehr_sync_logs(patient_id);
CREATE INDEX idx_sync_handoff ON ehr_sync_logs(handoff_id);
CREATE INDEX idx_sync_started ON ehr_sync_logs(started_at DESC);
CREATE INDEX idx_sync_failed ON ehr_sync_logs(status) WHERE status = 'failed';

-- Comments
COMMENT ON TABLE ehr_sync_logs IS 'EHR synchronization audit trail';
COMMENT ON COLUMN ehr_sync_logs.duration_ms IS 'Sync duration in milliseconds';
```

### 3.13 Table: user_sessions

**Purpose:** Track active user sessions

```sql
CREATE TABLE user_sessions (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  user_id UUID NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
  facility_id UUID REFERENCES facilities(id),
  
  -- Session Details
  token_hash VARCHAR(255) NOT NULL UNIQUE, -- Hashed JWT token
  refresh_token_hash VARCHAR(255) UNIQUE,
  
  -- Device Information
  device_name VARCHAR(100),
  device_type VARCHAR(50), -- mobile, tablet, desktop
  os VARCHAR(50),
  browser VARCHAR(50),
  user_agent TEXT,
  
  -- Location
  ip_address INET,
  country VARCHAR(2),
  city VARCHAR(100),
  
  -- Status
  is_active BOOLEAN DEFAULT true,
  last_activity_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Expiry
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ NOT NULL,
  
  -- Logout
  logged_out_at TIMESTAMPTZ,
  logout_reason VARCHAR(50), -- manual, timeout, forced
  
  -- Constraints
  CONSTRAINT valid_expiry CHECK (expires_at > created_at),
  CONSTRAINT logged_out_inactive CHECK (
    (logged_out_at IS NOT NULL AND is_active = false) OR
    (logged_out_at IS NULL)
  )
);

-- Indexes
CREATE INDEX idx_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_sessions_token ON user_sessions(token_hash);
CREATE INDEX idx_sessions_active ON user_sessions(user_id, is_active) WHERE is_active = true;
CREATE INDEX idx_sessions_expires ON user_sessions(expires_at) WHERE is_active = true;
CREATE INDEX idx_sessions_facility ON user_sessions(facility_id, is_active);

-- Comments
COMMENT ON TABLE user_sessions IS 'Active user sessions for JWT token management';
COMMENT ON COLUMN user_sessions.token_hash IS 'SHA-256 hash of JWT access token';
```

### 3.14 Table: feature_flags

**Purpose:** Feature toggle management

```sql
CREATE TABLE feature_flags (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Feature Details
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  feature_key VARCHAR(100) UNIQUE NOT NULL,
  
  -- Status
  enabled BOOLEAN DEFAULT false,
  rollout_percentage INTEGER DEFAULT 0, -- 0-100
  
  -- Targeting
  target_facilities UUID[] DEFAULT '{}',
  target_roles user_role[] DEFAULT '{}',
  target_users UUID[] DEFAULT '{}',
  
  -- Environment
  environment VARCHAR(20) DEFAULT 'production', -- development, staging, production
  
  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_by UUID REFERENCES staff(id),
  updated_by UUID REFERENCES staff(id),
  
  -- Constraints
  CONSTRAINT valid_rollout CHECK (rollout_percentage >= 0 AND rollout_percentage <= 100)
);

-- Indexes
CREATE INDEX idx_flags_enabled ON feature_flags(enabled) WHERE enabled = true;
CREATE INDEX idx_flags_key ON feature_flags(feature_key);
CREATE INDEX idx_flags_environment ON feature_flags(environment, enabled);

-- Comments
COMMENT ON TABLE feature_flags IS 'Feature toggles for gradual rollout';
COMMENT ON COLUMN feature_flags.rollout_percentage IS 'Percentage of users to enable feature for (0-100)';
```

### 3.15 Table: system_settings

**Purpose:** Application configuration

```sql
CREATE TYPE setting_category AS ENUM ('general', 'security', 'ai', 'ehr', 'notifications', 'billing');

CREATE TABLE system_settings (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Setting Details
  key VARCHAR(100) UNIQUE NOT NULL,
  value TEXT NOT NULL,
  value_type VARCHAR(20) DEFAULT 'string', -- string, integer, float, boolean, json
  category setting_category NOT NULL,
  
  -- Description
  label VARCHAR(255) NOT NULL,
  description TEXT,
  
  -- Validation
  validation_regex VARCHAR(255),
  allowed_values TEXT[], -- For enum-like settings
  
  -- Access Control
  is_public BOOLEAN DEFAULT false, -- Can frontend access this?
  requires_restart BOOLEAN DEFAULT false,
  
  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  updated_by UUID REFERENCES staff(id),
  
  -- Constraints
  CONSTRAINT valid_value_type CHECK (value_type IN ('string', 'integer', 'float', 'boolean', 'json'))
);

-- Indexes
CREATE INDEX idx_settings_key ON system_settings(key);
CREATE INDEX idx_settings_category ON system_settings(category);
CREATE INDEX idx_settings_public ON system_settings(is_public) WHERE is_public = true;

-- Comments
COMMENT ON TABLE system_settings IS 'Application-wide configuration settings';
COMMENT ON COLUMN system_settings.is_public IS 'If true, frontend can access via API';
```

---

## 4. Relationships & Foreign Keys

### 4.1 Relationship Summary

```sql
-- 1. Facilities → Staff (1:N)
ALTER TABLE staff ADD CONSTRAINT fk_staff_facility 
  FOREIGN KEY (facility_id) REFERENCES facilities(id) ON DELETE CASCADE;

-- 2. Facilities → Patients (1:N)
ALTER TABLE patients ADD CONSTRAINT fk_patients_facility 
  FOREIGN KEY (facility_id) REFERENCES facilities(id) ON DELETE CASCADE;

-- 3. Patients → Handoffs (1:N)
ALTER TABLE handoffs ADD CONSTRAINT fk_handoffs_patient 
  FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE;

-- 4. Facilities → Handoffs (1:N)
ALTER TABLE handoffs ADD CONSTRAINT fk_handoffs_facility 
  FOREIGN KEY (facility_id) REFERENCES facilities(id) ON DELETE CASCADE;

-- 5. Staff → Handoffs (giving) (N:1)
ALTER TABLE handoffs ADD CONSTRAINT fk_handoffs_from_staff 
  FOREIGN KEY (from_staff_id) REFERENCES staff(id) ON DELETE SET NULL;

-- 6. Staff → Handoffs (receiving) (N:1)
ALTER TABLE handoffs ADD CONSTRAINT fk_handoffs_to_staff 
  FOREIGN KEY (to_staff_id) REFERENCES staff(id) ON DELETE SET NULL;

-- 7. Handoffs → Voice Recordings (1:1)
ALTER TABLE voice_recordings ADD CONSTRAINT fk_voice_handoff 
  FOREIGN KEY (handoff_id) REFERENCES handoffs(id) ON DELETE CASCADE;

-- 8. Voice Recordings → AI Generations (1:1)
ALTER TABLE ai_generations ADD CONSTRAINT fk_ai_recording 
  FOREIGN KEY (voice_recording_id) REFERENCES voice_recordings(id) ON DELETE CASCADE;

-- 9. Handoffs → AI Generations (1:N)
ALTER TABLE ai_generations ADD CONSTRAINT fk_ai_handoff 
  FOREIGN KEY (handoff_id) REFERENCES handoffs(id) ON DELETE CASCADE;

-- 10. Handoffs → SBAR Reports (1:1)
ALTER TABLE sbar_reports ADD CONSTRAINT fk_sbar_handoff 
  FOREIGN KEY (handoff_id) REFERENCES handoffs(id) ON DELETE CASCADE;

-- 11. Handoffs ⟷ Staff (N:N via handoff_assignments)
ALTER TABLE handoff_assignments ADD CONSTRAINT fk_assignments_handoff 
  FOREIGN KEY (handoff_id) REFERENCES handoffs(id) ON DELETE CASCADE;
ALTER TABLE handoff_assignments ADD CONSTRAINT fk_assignments_staff 
  FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE CASCADE;

-- 12. Staff → Audit Logs (N:1)
ALTER TABLE audit_logs ADD CONSTRAINT fk_audit_user 
  FOREIGN KEY (user_id) REFERENCES staff(id) ON DELETE SET NULL;

-- 13. Staff → Notifications (1:N)
ALTER TABLE notifications ADD CONSTRAINT fk_notifications_user 
  FOREIGN KEY (user_id) REFERENCES staff(id) ON DELETE CASCADE;

-- 14. Handoffs → Notifications (1:N)
ALTER TABLE notifications ADD CONSTRAINT fk_notifications_handoff 
  FOREIGN KEY (handoff_id) REFERENCES handoffs(id) ON DELETE CASCADE;

-- 15. Facilities → EHR Connections (1:N)
ALTER TABLE ehr_connections ADD CONSTRAINT fk_ehr_facility 
  FOREIGN KEY (facility_id) REFERENCES facilities(id) ON DELETE CASCADE;

-- 16. EHR Connections → EHR Sync Logs (1:N)
ALTER TABLE ehr_sync_logs ADD CONSTRAINT fk_sync_connection 
  FOREIGN KEY (connection_id) REFERENCES ehr_connections(id) ON DELETE CASCADE;

-- 17. Staff → User Sessions (1:N)
ALTER TABLE user_sessions ADD CONSTRAINT fk_sessions_user 
  FOREIGN KEY (user_id) REFERENCES staff(id) ON DELETE CASCADE;
```

### 4.2 Cascade Behavior

**ON DELETE CASCADE:**
- Deleting a facility removes all staff, patients, handoffs
- Deleting a patient removes all their handoffs
- Deleting a handoff removes voice recordings, AI generations, SBAR reports

**ON DELETE SET NULL:**
- Deleting a staff member doesn't delete handoffs, just nullifies the reference
- Allows historical records to persist

---

## 5. Indexes & Performance

### 5.1 Index Strategy

**Primary Indexes (automatically created):**
- Primary keys (B-tree)
- Unique constraints (B-tree)

**Query-Optimized Indexes:**
- Foreign keys (for joins)
- Frequently filtered columns (status, dates)
- Sort columns (created_at DESC)

**Full-Text Search Indexes:**
- GIN indexes on tsvector for text search
- Used for searching names, MRNs, SBAR content

**Partial Indexes:**
- WHERE clauses to index only relevant rows
- Saves space and improves performance

### 5.2 Index Maintenance

```sql
-- Rebuild indexes (run monthly)
REINDEX DATABASE your_database_name;

-- Analyze tables for query planning
ANALYZE facilities;
ANALYZE staff;
ANALYZE patients;
ANALYZE handoffs;
ANALYZE voice_recordings;
ANALYZE ai_generations;
ANALYZE sbar_reports;

-- Check index usage
SELECT 
  schemaname,
  tablename,
  indexname,
  idx_scan as index_scans,
  idx_tup_read as tuples_read,
  idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT 
  schemaname,
  tablename,
  indexname
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE '%_pkey';
```

---

## 6. Row-Level Security (RLS)

### 6.1 Enable RLS on All Tables

```sql
-- Enable RLS
ALTER TABLE facilities ENABLE ROW LEVEL SECURITY;
ALTER TABLE staff ENABLE ROW LEVEL SECURITY;
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE handoffs ENABLE ROW LEVEL SECURITY;
ALTER TABLE voice_recordings ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_generations ENABLE ROW LEVEL SECURITY;
ALTER TABLE sbar_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE handoff_assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE ehr_connections ENABLE ROW LEVEL SECURITY;
ALTER TABLE ehr_sync_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE feature_flags ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_settings ENABLE ROW LEVEL SECURITY;
```

### 6.2 RLS Policies

**Facility-Level Isolation:**
```sql
-- Staff can only see data from their facility
CREATE POLICY staff_facility_isolation ON staff
  FOR ALL
  USING (
    facility_id = (
      SELECT facility_id FROM staff 
      WHERE auth_id = auth.uid()
    )
  );

-- Patients scoped to facility
CREATE POLICY patients_facility_isolation ON patients
  FOR ALL
  USING (
    facility_id = (
      SELECT facility_id FROM staff 
      WHERE auth_id = auth.uid()
    )
  );

-- Handoffs scoped to facility
CREATE POLICY handoffs_facility_isolation ON handoffs
  FOR ALL
  USING (
    facility_id = (
      SELECT facility_id FROM staff 
      WHERE auth_id = auth.uid()
    )
  );
```

**Role-Based Access:**
```sql
-- Admins can see everything in their facility
CREATE POLICY admin_full_access ON handoffs
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM staff
      WHERE auth_id = auth.uid()
        AND facility_id = handoffs.facility_id
        AND role IN ('admin', 'super_admin')
    )
  );

-- Staff can see handoffs they're involved in
CREATE POLICY staff_assigned_handoffs ON handoffs
  FOR SELECT
  USING (
    from_staff_id = (SELECT id FROM staff WHERE auth_id = auth.uid())
    OR to_staff_id = (SELECT id FROM staff WHERE auth_id = auth.uid())
    OR EXISTS (
      SELECT 1 FROM handoff_assignments
      WHERE handoff_id = handoffs.id
        AND staff_id = (SELECT id FROM staff WHERE auth_id = auth.uid())
    )
  );
```

**Audit Logs (Read-Only for Non-Admins):**
```sql
CREATE POLICY audit_logs_read ON audit_logs
  FOR SELECT
  USING (
    user_id = (SELECT id FROM staff WHERE auth_id = auth.uid())
    OR EXISTS (
      SELECT 1 FROM staff
      WHERE auth_id = auth.uid()
        AND role IN ('admin', 'super_admin')
    )
  );

-- Audit logs are insert-only (no updates/deletes)
CREATE POLICY audit_logs_insert ON audit_logs
  FOR INSERT
  WITH CHECK (true);
```

---

## 7. Database Functions

### 7.1 Trigger Functions

**Update updated_at timestamp:**
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables
CREATE TRIGGER update_facilities_updated_at
  BEFORE UPDATE ON facilities
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_staff_updated_at
  BEFORE UPDATE ON staff
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patients_updated_at
  BEFORE UPDATE ON patients
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_handoffs_updated_at
  BEFORE UPDATE ON handoffs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Apply to remaining tables...
```

**Audit logging function:**
```sql
CREATE OR REPLACE FUNCTION log_table_changes()
RETURNS TRIGGER AS $$
DECLARE
  user_id_val UUID;
  user_email_val VARCHAR(255);
  user_role_val user_role;
BEGIN
  -- Get current user info
  SELECT id, email, role INTO user_id_val, user_email_val, user_role_val
  FROM staff
  WHERE auth_id = auth.uid();

  -- Insert audit log
  INSERT INTO audit_logs (
    user_id,
    user_email,
    user_role,
    action,
    resource,
    resource_id,
    changes
  ) VALUES (
    user_id_val,
    user_email_val,
    user_role_val,
    TG_OP,
    TG_TABLE_NAME,
    COALESCE(NEW.id, OLD.id),
    CASE
      WHEN TG_OP = 'DELETE' THEN to_jsonb(OLD)
      WHEN TG_OP = 'UPDATE' THEN jsonb_build_object(
        'before', to_jsonb(OLD),
        'after', to_jsonb(NEW)
      )
      ELSE to_jsonb(NEW)
    END
  );

  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Apply to PHI tables
CREATE TRIGGER audit_patients_changes
  AFTER INSERT OR UPDATE OR DELETE ON patients
  FOR EACH ROW EXECUTE FUNCTION log_table_changes();

CREATE TRIGGER audit_handoffs_changes
  AFTER INSERT OR UPDATE OR DELETE ON handoffs
  FOR EACH ROW EXECUTE FUNCTION log_table_changes();
```

---

**[File continues with sections 8-12: Triggers, Views, Migrations, Seed Data, and Backup/Recovery...]**

Would you like me to continue with the remaining sections, or shall we move to Part 4?

---

*EclipseLink AI™ is a product of Rohimaya Health AI*  
*© 2025 Rohimaya Health AI. All rights reserved.*
