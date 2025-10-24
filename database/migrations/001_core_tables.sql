-- Migration 001: Core Tables (Handoffs, Voice Recordings, SBAR, etc.)
-- EclipseLink AI™ Database Migration

-- -----------------------------------------------------------------------------
-- Table: handoffs
-- -----------------------------------------------------------------------------
CREATE TABLE handoffs (
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

  -- Processing Times
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
  CONSTRAINT valid_quality_score CHECK (quality_score >= 0 AND quality_score <= 1)
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

COMMENT ON TABLE handoffs IS 'Clinical handoff records with SBAR generation tracking';

-- -----------------------------------------------------------------------------
-- Table: voice_recordings
-- -----------------------------------------------------------------------------
CREATE TABLE voice_recordings (
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

-- Indexes for voice_recordings
CREATE INDEX idx_voice_handoff ON voice_recordings(handoff_id);
CREATE INDEX idx_voice_uploaded_by ON voice_recordings(uploaded_by);
CREATE INDEX idx_voice_status ON voice_recordings(status);
CREATE INDEX idx_voice_uploaded ON voice_recordings(uploaded_at DESC);
CREATE INDEX idx_voice_processing ON voice_recordings(status)
  WHERE status IN ('uploading', 'uploaded', 'processing');

COMMENT ON TABLE voice_recordings IS 'Voice recording metadata (files stored in R2)';

-- -----------------------------------------------------------------------------
-- Table: ai_generations
-- -----------------------------------------------------------------------------
CREATE TABLE ai_generations (
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

  -- Token Usage
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
  CONSTRAINT valid_attempts CHECK (attempt_number <= max_attempts)
);

-- Indexes for ai_generations
CREATE INDEX idx_ai_recording ON ai_generations(voice_recording_id);
CREATE INDEX idx_ai_handoff ON ai_generations(handoff_id);
CREATE INDEX idx_ai_stage_status ON ai_generations(stage, status);
CREATE INDEX idx_ai_created ON ai_generations(created_at DESC);
CREATE INDEX idx_ai_failed ON ai_generations(status, attempt_number)
  WHERE status = 'failed';

COMMENT ON TABLE ai_generations IS 'AI processing records for transcription and SBAR generation';

-- -----------------------------------------------------------------------------
-- Table: sbar_reports
-- -----------------------------------------------------------------------------
CREATE TABLE sbar_reports (
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
  )
);

-- Indexes for sbar_reports
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

-- -----------------------------------------------------------------------------
-- Table: handoff_assignments
-- -----------------------------------------------------------------------------
CREATE TABLE handoff_assignments (
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

-- Indexes for handoff_assignments
CREATE INDEX idx_assignments_handoff ON handoff_assignments(handoff_id);
CREATE INDEX idx_assignments_staff ON handoff_assignments(staff_id);
CREATE INDEX idx_assignments_status ON handoff_assignments(status);
CREATE INDEX idx_assignments_staff_status ON handoff_assignments(staff_id, status)
  WHERE status IN ('pending', 'notified', 'viewed');

COMMENT ON TABLE handoff_assignments IS 'Staff assignments to handoffs (many-to-many)';
