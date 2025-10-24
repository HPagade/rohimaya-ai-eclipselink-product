-- =============================================
-- EclipseLink AI - Database Schema Migration
-- Migration: 001_core_tables
-- Description: Core tables for facilities, staff, patients, and handoffs
-- Date: 2025-01-24
-- =============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =============================================
-- CUSTOM TYPES
-- =============================================

-- Facility Types
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

-- User Roles
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

-- Employment Status
CREATE TYPE employment_status AS ENUM (
  'full_time',
  'part_time',
  'per_diem',
  'contract',
  'inactive'
);

-- Gender
CREATE TYPE gender AS ENUM ('male', 'female', 'other', 'unknown');

-- Blood Type
CREATE TYPE blood_type AS ENUM ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'unknown');

-- Patient Status
CREATE TYPE patient_status AS ENUM ('active', 'discharged', 'deceased', 'transferred');

-- Handoff Status
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

-- Handoff Priority
CREATE TYPE handoff_priority AS ENUM ('routine', 'urgent', 'emergent');

-- =============================================
-- TABLE: facilities
-- =============================================

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

-- Indexes for facilities
CREATE INDEX idx_facilities_name ON facilities USING gin(to_tsvector('english', name));
CREATE INDEX idx_facilities_type ON facilities(facility_type);
CREATE INDEX idx_facilities_location ON facilities(state, city);
CREATE INDEX idx_facilities_active ON facilities(is_active) WHERE is_active = true;
CREATE INDEX idx_facilities_subscription ON facilities(subscription_tier, subscription_status);

-- Comments
COMMENT ON TABLE facilities IS 'Healthcare facilities using EclipseLink AI';
COMMENT ON COLUMN facilities.primary_ehr IS 'Primary EHR system (Epic, Cerner, MEDITECH, etc.)';
COMMENT ON COLUMN facilities.subscription_tier IS 'free, basic, professional, enterprise';

-- =============================================
-- TABLE: staff
-- =============================================

CREATE TABLE staff (
  -- Primary Key
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

-- Comments
COMMENT ON TABLE staff IS 'Healthcare professionals using EclipseLink AI';
COMMENT ON COLUMN staff.auth_id IS 'References Supabase auth.users.id';
COMMENT ON COLUMN staff.npi_number IS 'National Provider Identifier (10 digits)';
COMMENT ON COLUMN staff.dea_number IS 'Drug Enforcement Administration number';

-- =============================================
-- TABLE: patients
-- =============================================

CREATE TABLE patients (
  -- Primary Key
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
  CONSTRAINT valid_admission CHECK (admission_date <= COALESCE(discharge_date, NOW())),
  CONSTRAINT valid_status_dates CHECK (
    (status = 'discharged' AND discharge_date IS NOT NULL) OR
    (status != 'discharged' AND discharge_date IS NULL) OR
    (status = 'deceased')
  )
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

-- Comments
COMMENT ON TABLE patients IS 'Patient demographic and medical information (PHI)';
COMMENT ON COLUMN patients.mrn IS 'Medical Record Number - unique per facility';
COMMENT ON COLUMN patients.ssn_encrypted IS 'Encrypted Social Security Number';
COMMENT ON COLUMN patients.allergies IS 'Array of allergy objects';
COMMENT ON COLUMN patients.medications IS 'Array of current medication objects';
COMMENT ON COLUMN patients.vital_signs IS 'Latest vital signs snapshot';

-- =============================================
-- TABLE: handoffs
-- =============================================

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

  -- Clinical Context
  location VARCHAR(100),
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
  recording_duration INTEGER,
  transcription_duration INTEGER,
  sbar_generation_duration INTEGER,
  total_processing_time INTEGER GENERATED ALWAYS AS (
    COALESCE(transcription_duration, 0) + COALESCE(sbar_generation_duration, 0)
  ) STORED,

  -- Notes
  clinical_notes TEXT,
  internal_notes TEXT,

  -- Quality Metrics
  quality_score DECIMAL(3, 2),
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

-- Indexes for handoffs
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

-- =============================================
-- Row-Level Security (RLS) Policies
-- =============================================

-- Enable RLS on all tables
ALTER TABLE facilities ENABLE ROW LEVEL SECURITY;
ALTER TABLE staff ENABLE ROW LEVEL SECURITY;
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE handoffs ENABLE ROW LEVEL SECURITY;

-- RLS Policies for facilities (users can only see their own facility)
CREATE POLICY facility_isolation_policy ON facilities
  FOR ALL
  USING (id = current_setting('app.current_facility_id', true)::UUID);

-- RLS Policies for staff (users can only see staff in their facility)
CREATE POLICY staff_facility_isolation ON staff
  FOR ALL
  USING (facility_id = current_setting('app.current_facility_id', true)::UUID);

-- RLS Policies for patients (users can only see patients in their facility)
CREATE POLICY patients_facility_isolation ON patients
  FOR ALL
  USING (facility_id = current_setting('app.current_facility_id', true)::UUID);

-- RLS Policies for handoffs (users can only see handoffs in their facility)
CREATE POLICY handoffs_facility_isolation ON handoffs
  FOR ALL
  USING (facility_id = current_setting('app.current_facility_id', true)::UUID);

-- =============================================
-- Triggers for updated_at
-- =============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_facilities_updated_at BEFORE UPDATE ON facilities
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_staff_updated_at BEFORE UPDATE ON staff
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_handoffs_updated_at BEFORE UPDATE ON handoffs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
