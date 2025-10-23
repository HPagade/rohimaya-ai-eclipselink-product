-- EclipseLink AI™ - Complete Database Schema
-- Product: EclipseLink AI™ Clinical Handoff System
-- Company: Rohimaya Health AI
-- PostgreSQL 15+ via Supabase

-- =============================================================================
-- 1. CUSTOM TYPES (ENUMS)
-- =============================================================================

-- Facility types
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

-- User roles
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

-- Employment status
CREATE TYPE employment_status AS ENUM (
  'full_time',
  'part_time',
  'per_diem',
  'contract',
  'inactive'
);

-- Patient demographics
CREATE TYPE gender AS ENUM ('male', 'female', 'other', 'unknown');
CREATE TYPE blood_type AS ENUM ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'unknown');
CREATE TYPE patient_status AS ENUM ('active', 'discharged', 'deceased', 'transferred');

-- Handoff types
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

-- Voice recording types
CREATE TYPE recording_status AS ENUM (
  'uploading',
  'uploaded',
  'processing',
  'transcribed',
  'failed',
  'deleted'
);

CREATE TYPE audio_format AS ENUM ('webm', 'mp3', 'wav', 'ogg', 'm4a');

-- AI generation types
CREATE TYPE generation_stage AS ENUM ('transcription', 'sbar_generation');
CREATE TYPE generation_status AS ENUM ('queued', 'processing', 'completed', 'failed');

-- Assignment types
CREATE TYPE assignment_role AS ENUM (
  'giving',
  'receiving',
  'supervising',
  'cc',
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

-- Audit types
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

-- Notification types
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

-- EHR types
CREATE TYPE ehr_type AS ENUM ('epic', 'cerner', 'meditech', 'allscripts', 'protouch', 'pointclickcare', 'wellsky', 'other');
CREATE TYPE ehr_protocol AS ENUM ('fhir_r4', 'hl7_v2', 'hl7_v3', 'rest', 'soap');
CREATE TYPE connection_status AS ENUM ('active', 'inactive', 'testing', 'error');

-- Sync types
CREATE TYPE sync_type AS ENUM ('patient_import', 'patient_export', 'handoff_export', 'medication_sync', 'allergy_sync', 'vital_signs_sync');
CREATE TYPE sync_status AS ENUM ('started', 'in_progress', 'completed', 'failed', 'partial');

-- Settings types
CREATE TYPE setting_category AS ENUM ('general', 'security', 'ai', 'ehr', 'notifications', 'billing');

-- =============================================================================
-- 2. CORE TABLES
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Table: facilities
-- -----------------------------------------------------------------------------
CREATE TABLE facilities (
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

-- Indexes for facilities
CREATE INDEX idx_facilities_name ON facilities USING gin(to_tsvector('english', name));
CREATE INDEX idx_facilities_type ON facilities(facility_type);
CREATE INDEX idx_facilities_location ON facilities(state, city);
CREATE INDEX idx_facilities_active ON facilities(is_active) WHERE is_active = true;
CREATE INDEX idx_facilities_subscription ON facilities(subscription_tier, subscription_status);

COMMENT ON TABLE facilities IS 'Healthcare facilities using EclipseLink AI';
COMMENT ON COLUMN facilities.primary_ehr IS 'Primary EHR system (Epic, Cerner, MEDITECH, etc.)';
COMMENT ON COLUMN facilities.subscription_tier IS 'free, basic, professional, enterprise';

-- -----------------------------------------------------------------------------
-- Table: staff
-- -----------------------------------------------------------------------------
CREATE TABLE staff (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Foreign Keys
  facility_id UUID NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,

  -- Authentication (synced with Supabase Auth)
  auth_id UUID UNIQUE,
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

-- Indexes for staff
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

COMMENT ON TABLE staff IS 'Healthcare professionals using EclipseLink AI';
COMMENT ON COLUMN staff.auth_id IS 'References Supabase auth.users.id';
COMMENT ON COLUMN staff.npi_number IS 'National Provider Identifier (10 digits)';

-- -----------------------------------------------------------------------------
-- Table: patients
-- -----------------------------------------------------------------------------
CREATE TABLE patients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Foreign Keys
  facility_id UUID NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,

  -- Patient Identifiers (PHI)
  mrn VARCHAR(50) NOT NULL,
  ssn_encrypted TEXT,
  external_id VARCHAR(100),

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

  -- Current Medications (stored as JSONB array)
  medications JSONB DEFAULT '[]',

  -- Vital Signs (latest)
  vital_signs JSONB,
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
  CONSTRAINT valid_admission CHECK (admission_date <= COALESCE(discharge_date, NOW()))
);

-- Indexes for patients
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

COMMENT ON TABLE patients IS 'Patient demographic and medical information (PHI)';
COMMENT ON COLUMN patients.mrn IS 'Medical Record Number - unique per facility';
COMMENT ON COLUMN patients.ssn_encrypted IS 'Encrypted Social Security Number';

-- =============================================================================
-- Continue with remaining tables in next part...
-- =============================================================================
