-- =============================================
-- EclipseLink AI - Database Schema Migration
-- Migration: 002_audit_and_notifications
-- Description: Voice recordings, AI generations, SBAR, audit logs, notifications, EHR, sessions, and system tables
-- Date: 2025-01-24
-- =============================================

-- =============================================
-- ADDITIONAL CUSTOM TYPES
-- =============================================

-- Recording Status
CREATE TYPE recording_status AS ENUM (
  'uploading',
  'uploaded',
  'processing',
  'transcribed',
  'failed',
  'deleted'
);

-- Audio Format
CREATE TYPE audio_format AS ENUM ('webm', 'mp3', 'wav', 'ogg', 'm4a');

-- Generation Stage
CREATE TYPE generation_stage AS ENUM ('transcription', 'sbar_generation');

-- Generation Status
CREATE TYPE generation_status AS ENUM ('queued', 'processing', 'completed', 'failed');

-- Assignment Role
CREATE TYPE assignment_role AS ENUM (
  'giving',
  'receiving',
  'supervising',
  'cc',
  'reviewing'
);

-- Assignment Status
CREATE TYPE assignment_status AS ENUM (
  'pending',
  'notified',
  'viewed',
  'accepted',
  'declined',
  'completed'
);

-- Audit Action
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

-- Notification Type
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

-- Notification Priority
CREATE TYPE notification_priority AS ENUM ('low', 'normal', 'high', 'urgent');

-- EHR Type
CREATE TYPE ehr_type AS ENUM ('epic', 'cerner', 'meditech', 'allscripts', 'protouch', 'pointclickcare', 'wellsky', 'other');

-- EHR Protocol
CREATE TYPE ehr_protocol AS ENUM ('fhir_r4', 'hl7_v2', 'hl7_v3', 'rest', 'soap');

-- Connection Status
CREATE TYPE connection_status AS ENUM ('active', 'inactive', 'testing', 'error');

-- Sync Type
CREATE TYPE sync_type AS ENUM ('patient_import', 'patient_export', 'handoff_export', 'medication_sync', 'allergy_sync', 'vital_signs_sync');

-- Sync Status
CREATE TYPE sync_status AS ENUM ('started', 'in_progress', 'completed', 'failed', 'partial');

-- =============================================
-- TABLE: voice_recordings
-- =============================================

CREATE TABLE voice_recordings (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Foreign Keys
  handoff_id UUID NOT NULL REFERENCES handoffs(id) ON DELETE CASCADE,
  uploaded_by UUID NOT NULL REFERENCES staff(id) ON DELETE SET NULL,

  -- Recording Details
  status recording_status DEFAULT 'uploading',
  duration INTEGER NOT NULL,
  file_size BIGINT NOT NULL,
  audio_format audio_format NOT NULL,
  sample_rate INTEGER,
  bit_rate INTEGER,
  channels INTEGER DEFAULT 1,

  -- Storage
  file_path TEXT NOT NULL,
  file_url TEXT,
  file_url_expires_at TIMESTAMPTZ,

  -- Processing
  transcription_job_id VARCHAR(100),
  transcription_attempts INTEGER DEFAULT 0,
  last_transcription_error TEXT,

  -- Quality Metrics
  audio_quality_score DECIMAL(3, 2),
  silence_percentage DECIMAL(5, 2),
  noise_level DECIMAL(5, 2),

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

COMMENT ON TABLE voice_recordings IS 'Voice recording metadata (files stored in R2)';
COMMENT ON COLUMN voice_recordings.file_path IS 'Path in Cloudflare R2 bucket';

-- =============================================
-- TABLE: ai_generations
-- =============================================

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
  transcription_confidence DECIMAL(3, 2),
  transcription_language VARCHAR(10) DEFAULT 'en',
  transcription_word_count INTEGER,

  -- Azure OpenAI Details
  azure_request_id VARCHAR(100),
  model_name VARCHAR(50),
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
  processing_duration INTEGER,

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

  -- Cost Tracking
  estimated_cost DECIMAL(10, 4),

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

COMMENT ON TABLE ai_generations IS 'AI processing records for transcription and SBAR generation';

-- =============================================
-- TABLE: sbar_reports
-- =============================================

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
  completeness_score DECIMAL(3, 2),
  readability_score DECIMAL(3, 2),
  clinical_accuracy_score DECIMAL(3, 2),

  -- Export
  exported_formats JSONB DEFAULT '[]',
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

COMMENT ON TABLE sbar_reports IS 'Generated SBAR reports with version control';

-- =============================================
-- TABLE: handoff_assignments
-- =============================================

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
  notification_method VARCHAR(20),
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

COMMENT ON TABLE handoff_assignments IS 'Staff assignments to handoffs (many-to-many)';

-- =============================================
-- TABLE: audit_logs
-- =============================================

CREATE TABLE audit_logs (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Who
  user_id UUID REFERENCES staff(id),
  user_email VARCHAR(255),
  user_role user_role,

  -- What
  action audit_action NOT NULL,
  resource VARCHAR(50) NOT NULL,
  resource_id UUID,

  -- Details
  changes JSONB,
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
  phi_type VARCHAR(50),

  -- Security
  severity VARCHAR(20) DEFAULT 'info',
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

COMMENT ON TABLE audit_logs IS 'HIPAA-compliant audit trail (7-year retention)';

-- =============================================
-- TABLE: notifications
-- =============================================

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

COMMENT ON TABLE notifications IS 'In-app notifications for users';

-- =============================================
-- TABLE: ehr_connections
-- =============================================

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
  fhir_base_url TEXT,
  auth_type VARCHAR(50) NOT NULL,

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
  config JSONB,
  supported_resources JSONB,

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

COMMENT ON TABLE ehr_connections IS 'EHR integration configuration per facility';

-- =============================================
-- TABLE: ehr_sync_logs
-- =============================================

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

COMMENT ON TABLE ehr_sync_logs IS 'EHR synchronization audit trail';

-- =============================================
-- TABLE: user_sessions
-- =============================================

CREATE TABLE user_sessions (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Foreign Keys
  user_id UUID NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
  facility_id UUID REFERENCES facilities(id),

  -- Session Details
  token_hash VARCHAR(255) NOT NULL UNIQUE,
  refresh_token_hash VARCHAR(255) UNIQUE,

  -- Device Information
  device_name VARCHAR(100),
  device_type VARCHAR(50),
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
  logout_reason VARCHAR(50),

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

COMMENT ON TABLE user_sessions IS 'Active user sessions for JWT token management';

-- =============================================
-- TABLE: feature_flags
-- =============================================

CREATE TABLE feature_flags (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Feature Details
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  feature_key VARCHAR(100) UNIQUE NOT NULL,

  -- Status
  enabled BOOLEAN DEFAULT false,
  rollout_percentage INTEGER DEFAULT 0,

  -- Targeting
  target_facilities UUID[] DEFAULT '{}',
  target_roles user_role[] DEFAULT '{}',
  target_users UUID[] DEFAULT '{}',

  -- Environment
  environment VARCHAR(20) DEFAULT 'production',

  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_by UUID REFERENCES staff(id),
  updated_by UUID REFERENCES staff(id),

  -- Constraints
  CONSTRAINT valid_rollout CHECK (rollout_percentage >= 0 AND rollout_percentage <= 100)
);

-- Indexes
CREATE INDEX idx_feature_flags_key ON feature_flags(feature_key);
CREATE INDEX idx_feature_flags_enabled ON feature_flags(enabled) WHERE enabled = true;
CREATE INDEX idx_feature_flags_environment ON feature_flags(environment);

COMMENT ON TABLE feature_flags IS 'Feature toggles for gradual rollout';

-- =============================================
-- TABLE: system_settings
-- =============================================

CREATE TABLE system_settings (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Setting Details
  key VARCHAR(100) UNIQUE NOT NULL,
  value TEXT NOT NULL,
  category VARCHAR(50) DEFAULT 'general',
  description TEXT,

  -- Data Type
  value_type VARCHAR(20) DEFAULT 'string',

  -- Metadata
  is_sensitive BOOLEAN DEFAULT false,
  is_editable BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  updated_by UUID REFERENCES staff(id)
);

-- Indexes
CREATE INDEX idx_settings_key ON system_settings(key);
CREATE INDEX idx_settings_category ON system_settings(category);

COMMENT ON TABLE system_settings IS 'Application-wide configuration settings';

-- =============================================
-- Row-Level Security (RLS) Policies
-- =============================================

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

-- RLS Policies (facility isolation)
CREATE POLICY voice_recordings_facility_isolation ON voice_recordings
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM handoffs
      WHERE handoffs.id = voice_recordings.handoff_id
      AND handoffs.facility_id = current_setting('app.current_facility_id', true)::UUID
    )
  );

CREATE POLICY ai_generations_facility_isolation ON ai_generations
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM handoffs
      WHERE handoffs.id = ai_generations.handoff_id
      AND handoffs.facility_id = current_setting('app.current_facility_id', true)::UUID
    )
  );

CREATE POLICY sbar_reports_facility_isolation ON sbar_reports
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM handoffs
      WHERE handoffs.id = sbar_reports.handoff_id
      AND handoffs.facility_id = current_setting('app.current_facility_id', true)::UUID
    )
  );

CREATE POLICY handoff_assignments_facility_isolation ON handoff_assignments
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM handoffs
      WHERE handoffs.id = handoff_assignments.handoff_id
      AND handoffs.facility_id = current_setting('app.current_facility_id', true)::UUID
    )
  );

CREATE POLICY audit_logs_facility_isolation ON audit_logs
  FOR SELECT
  USING (facility_id = current_setting('app.current_facility_id', true)::UUID);

CREATE POLICY notifications_user_isolation ON notifications
  FOR ALL
  USING (user_id = current_setting('app.current_user_id', true)::UUID);

CREATE POLICY ehr_connections_facility_isolation ON ehr_connections
  FOR ALL
  USING (facility_id = current_setting('app.current_facility_id', true)::UUID);

CREATE POLICY ehr_sync_logs_facility_isolation ON ehr_sync_logs
  FOR ALL
  USING (facility_id = current_setting('app.current_facility_id', true)::UUID);

CREATE POLICY user_sessions_user_isolation ON user_sessions
  FOR ALL
  USING (user_id = current_setting('app.current_user_id', true)::UUID);

-- =============================================
-- Triggers for updated_at
-- =============================================

CREATE TRIGGER update_voice_recordings_updated_at BEFORE UPDATE ON voice_recordings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ai_generations_updated_at BEFORE UPDATE ON ai_generations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sbar_reports_updated_at BEFORE UPDATE ON sbar_reports
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_handoff_assignments_updated_at BEFORE UPDATE ON handoff_assignments
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ehr_connections_updated_at BEFORE UPDATE ON ehr_connections
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_feature_flags_updated_at BEFORE UPDATE ON feature_flags
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_settings_updated_at BEFORE UPDATE ON system_settings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
