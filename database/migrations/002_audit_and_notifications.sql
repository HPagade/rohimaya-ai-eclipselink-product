-- Migration 002: Audit Logs, Notifications, and Supporting Tables
-- EclipseLink AI™ Database Migration

-- -----------------------------------------------------------------------------
-- Table: audit_logs
-- -----------------------------------------------------------------------------
CREATE TABLE audit_logs (
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

-- Indexes for audit_logs
CREATE INDEX idx_audit_user ON audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_action ON audit_logs(action, created_at DESC);
CREATE INDEX idx_audit_resource ON audit_logs(resource, resource_id);
CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_phi ON audit_logs(phi_accessed) WHERE phi_accessed = true;
CREATE INDEX idx_audit_flagged ON audit_logs(flagged) WHERE flagged = true;
CREATE INDEX idx_audit_facility ON audit_logs(facility_id, created_at DESC);
CREATE INDEX idx_audit_ip ON audit_logs(ip_address, created_at DESC);

COMMENT ON TABLE audit_logs IS 'HIPAA-compliant audit trail (7-year retention)';
COMMENT ON COLUMN audit_logs.phi_accessed IS 'True if action accessed Protected Health Information';

-- -----------------------------------------------------------------------------
-- Table: notifications
-- -----------------------------------------------------------------------------
CREATE TABLE notifications (
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

-- Indexes for notifications
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
COMMENT ON COLUMN notifications.expires_at IS 'Notification auto-dismissed after this time';

-- -----------------------------------------------------------------------------
-- Table: ehr_connections
-- -----------------------------------------------------------------------------
CREATE TABLE ehr_connections (
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

-- Indexes for ehr_connections
CREATE INDEX idx_ehr_facility ON ehr_connections(facility_id);
CREATE INDEX idx_ehr_type ON ehr_connections(ehr_type);
CREATE INDEX idx_ehr_status ON ehr_connections(status);
CREATE INDEX idx_ehr_active ON ehr_connections(facility_id, is_active) WHERE is_active = true;

COMMENT ON TABLE ehr_connections IS 'EHR integration configuration per facility';
COMMENT ON COLUMN ehr_connections.client_id_encrypted IS 'Encrypted with facility-specific key';

-- -----------------------------------------------------------------------------
-- Table: ehr_sync_logs
-- -----------------------------------------------------------------------------
CREATE TABLE ehr_sync_logs (
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
  )
);

-- Indexes for ehr_sync_logs
CREATE INDEX idx_sync_connection ON ehr_sync_logs(connection_id);
CREATE INDEX idx_sync_facility ON ehr_sync_logs(facility_id, started_at DESC);
CREATE INDEX idx_sync_type ON ehr_sync_logs(sync_type);
CREATE INDEX idx_sync_status ON ehr_sync_logs(status);
CREATE INDEX idx_sync_patient ON ehr_sync_logs(patient_id);
CREATE INDEX idx_sync_handoff ON ehr_sync_logs(handoff_id);
CREATE INDEX idx_sync_started ON ehr_sync_logs(started_at DESC);
CREATE INDEX idx_sync_failed ON ehr_sync_logs(status) WHERE status = 'failed';

COMMENT ON TABLE ehr_sync_logs IS 'EHR synchronization audit trail';
COMMENT ON COLUMN ehr_sync_logs.duration_ms IS 'Sync duration in milliseconds';

-- -----------------------------------------------------------------------------
-- Table: user_sessions
-- -----------------------------------------------------------------------------
CREATE TABLE user_sessions (
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

-- Indexes for user_sessions
CREATE INDEX idx_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_sessions_token ON user_sessions(token_hash);
CREATE INDEX idx_sessions_active ON user_sessions(user_id, is_active) WHERE is_active = true;
CREATE INDEX idx_sessions_expires ON user_sessions(expires_at) WHERE is_active = true;
CREATE INDEX idx_sessions_facility ON user_sessions(facility_id, is_active);

COMMENT ON TABLE user_sessions IS 'Active user sessions for JWT token management';
COMMENT ON COLUMN user_sessions.token_hash IS 'SHA-256 hash of JWT access token';

-- -----------------------------------------------------------------------------
-- Table: feature_flags
-- -----------------------------------------------------------------------------
CREATE TABLE feature_flags (
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

-- Indexes for feature_flags
CREATE INDEX idx_flags_enabled ON feature_flags(enabled) WHERE enabled = true;
CREATE INDEX idx_flags_key ON feature_flags(feature_key);
CREATE INDEX idx_flags_environment ON feature_flags(environment, enabled);

COMMENT ON TABLE feature_flags IS 'Feature toggles for gradual rollout';
COMMENT ON COLUMN feature_flags.rollout_percentage IS 'Percentage of users to enable feature for (0-100)';

-- -----------------------------------------------------------------------------
-- Table: system_settings
-- -----------------------------------------------------------------------------
CREATE TABLE system_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Setting Details
  key VARCHAR(100) UNIQUE NOT NULL,
  value TEXT NOT NULL,
  value_type VARCHAR(20) DEFAULT 'string',
  category setting_category NOT NULL,

  -- Description
  label VARCHAR(255) NOT NULL,
  description TEXT,

  -- Validation
  validation_regex VARCHAR(255),
  allowed_values TEXT[],

  -- Access Control
  is_public BOOLEAN DEFAULT false,
  requires_restart BOOLEAN DEFAULT false,

  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  updated_by UUID REFERENCES staff(id),

  -- Constraints
  CONSTRAINT valid_value_type CHECK (value_type IN ('string', 'integer', 'float', 'boolean', 'json'))
);

-- Indexes for system_settings
CREATE INDEX idx_settings_key ON system_settings(key);
CREATE INDEX idx_settings_category ON system_settings(category);
CREATE INDEX idx_settings_public ON system_settings(is_public) WHERE is_public = true;

COMMENT ON TABLE system_settings IS 'Application-wide configuration settings';
COMMENT ON COLUMN system_settings.is_public IS 'If true, frontend can access via API';
