-- ============================================================================
-- EclipseLink AI - Database Schema
-- PostgreSQL 15+ (Supabase compatible)
-- ============================================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- TABLE 1: facilities
-- ============================================================================

CREATE TABLE facilities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    phone VARCHAR(20),
    email VARCHAR(255),
    license_number VARCHAR(100) UNIQUE,
    subscription_tier VARCHAR(50) DEFAULT 'trial',
    subscription_status VARCHAR(50) DEFAULT 'active',
    subscription_expires_at TIMESTAMP WITH TIME ZONE,
    features JSONB DEFAULT '{"ehr_integration": false}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_facilities_license ON facilities(license_number);
CREATE INDEX idx_facilities_status ON facilities(subscription_status);

-- ============================================================================
-- TABLE 2: users (15 clinical roles)
-- ============================================================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(255),
    email_verification_expires_at TIMESTAMP WITH TIME ZONE,
    reset_password_token VARCHAR(255),
    reset_password_expires_at TIMESTAMP WITH TIME ZONE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    profile_photo_url TEXT,
    role VARCHAR(50) NOT NULL,
    department VARCHAR(100),
    license_number VARCHAR(100),
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP WITH TIME ZONE,
    last_login_ip VARCHAR(45),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_facility ON users(facility_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active);

-- ============================================================================
-- TABLE 3: patients
-- ============================================================================

CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
    mrn VARCHAR(50) NOT NULL,
    ehr_patient_id VARCHAR(100),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    emergency_contact_name VARCHAR(200),
    emergency_contact_phone VARCHAR(20),
    emergency_contact_relation VARCHAR(50),
    room_number VARCHAR(20),
    admission_date DATE,
    discharge_date DATE,
    primary_diagnosis TEXT,
    allergies TEXT,
    code_status VARCHAR(50),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(facility_id, mrn)
);

CREATE INDEX idx_patients_facility ON patients(facility_id);
CREATE INDEX idx_patients_mrn ON patients(mrn);
CREATE INDEX idx_patients_status ON patients(status);
CREATE INDEX idx_patients_room ON patients(room_number);

-- ============================================================================
-- TABLE 4: handoffs (Update-Only Model™)
-- ============================================================================

CREATE TABLE handoffs (
    id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    created_by_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_baseline BOOLEAN DEFAULT FALSE,
    baseline_handoff_id INTEGER REFERENCES handoffs(id),
    audio_file_url TEXT NOT NULL,
    audio_duration_seconds INTEGER,
    audio_file_size_bytes INTEGER,
    transcript_text TEXT,
    transcript_confidence DECIMAL(3,2),
    transcribed_at TIMESTAMP WITH TIME ZONE,
    sbar_situation TEXT,
    sbar_background TEXT,
    sbar_assessment TEXT,
    sbar_recommendation TEXT,
    ai_processing_time_ms INTEGER,
    ai_processed_at TIMESTAMP WITH TIME ZONE,
    changes_detected JSONB,
    changes_summary TEXT,
    has_critical_alert BOOLEAN DEFAULT FALSE,
    critical_alert_type VARCHAR(100),
    critical_alert_confidence DECIMAL(3,2),
    critical_alert_notified_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'draft',
    reviewed_by_user_id INTEGER REFERENCES users(id),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_handoffs_facility ON handoffs(facility_id);
CREATE INDEX idx_handoffs_patient ON handoffs(patient_id);
CREATE INDEX idx_handoffs_creator ON handoffs(created_by_user_id);
CREATE INDEX idx_handoffs_baseline ON handoffs(baseline_handoff_id);
CREATE INDEX idx_handoffs_status ON handoffs(status);
CREATE INDEX idx_handoffs_critical ON handoffs(has_critical_alert);
CREATE INDEX idx_handoffs_created_at ON handoffs(created_at DESC);

-- ============================================================================
-- TABLE 5: handoff_changes (tracks detailed changes)
-- ============================================================================

CREATE TABLE handoff_changes (
    id SERIAL PRIMARY KEY,
    handoff_id INTEGER NOT NULL REFERENCES handoffs(id) ON DELETE CASCADE,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_type VARCHAR(50),
    severity VARCHAR(20),
    ai_confidence DECIMAL(3,2),
    ai_explanation TEXT,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_changes_handoff ON handoff_changes(handoff_id);
CREATE INDEX idx_changes_severity ON handoff_changes(severity);

-- ============================================================================
-- TABLE 6: rewards_points (gamification)
-- ============================================================================

CREATE TABLE rewards_points (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    facility_id INTEGER NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
    points_earned INTEGER NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    description TEXT,
    handoff_id INTEGER REFERENCES handoffs(id) ON DELETE SET NULL,
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_rewards_user ON rewards_points(user_id);
CREATE INDEX idx_rewards_facility ON rewards_points(facility_id);
CREATE INDEX idx_rewards_earned_at ON rewards_points(earned_at DESC);

-- ============================================================================
-- TABLE 7: audit_logs (HIPAA 7-year retention)
-- ============================================================================

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id INTEGER,
    ip_address VARCHAR(45),
    user_agent TEXT,
    request_method VARCHAR(10),
    request_path TEXT,
    old_values JSONB,
    new_values JSONB,
    is_suspicious BOOLEAN DEFAULT FALSE,
    suspicious_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
) PARTITION BY RANGE (created_at);

CREATE TABLE audit_logs_2024 PARTITION OF audit_logs
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
CREATE TABLE audit_logs_2025 PARTITION OF audit_logs
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
CREATE TABLE audit_logs_2026 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX idx_audit_facility ON audit_logs(facility_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_created_at ON audit_logs(created_at DESC);

-- ============================================================================
-- TABLE 8: handoff_assignments
-- ============================================================================

CREATE TABLE handoff_assignments (
    id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assigned_by_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    shift VARCHAR(20),
    assignment_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_assignments_facility ON handoff_assignments(facility_id);
CREATE INDEX idx_assignments_patient ON handoff_assignments(patient_id);
CREATE INDEX idx_assignments_user ON handoff_assignments(user_id);
CREATE INDEX idx_assignments_active ON handoff_assignments(is_active);
CREATE INDEX idx_assignments_date ON handoff_assignments(assignment_date DESC);

-- ============================================================================
-- TABLE 9: notifications
-- ============================================================================

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal',
    handoff_id INTEGER REFERENCES handoffs(id) ON DELETE CASCADE,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);

-- ============================================================================
-- TABLE 10: ehr_connections
-- ============================================================================

CREATE TABLE ehr_connections (
    id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
    ehr_system VARCHAR(50) NOT NULL,
    ehr_environment VARCHAR(20) DEFAULT 'production',
    api_endpoint TEXT NOT NULL,
    client_id TEXT,
    client_secret TEXT,
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP WITH TIME ZONE,
    fhir_version VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP WITH TIME ZONE,
    last_sync_status VARCHAR(50),
    last_sync_error TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_ehr_facility ON ehr_connections(facility_id);
CREATE INDEX idx_ehr_active ON ehr_connections(is_active);

-- ============================================================================
-- TABLE 11: ehr_sync_logs
-- ============================================================================

CREATE TABLE ehr_sync_logs (
    id SERIAL PRIMARY KEY,
    ehr_connection_id INTEGER NOT NULL REFERENCES ehr_connections(id) ON DELETE CASCADE,
    sync_type VARCHAR(50) NOT NULL,
    records_processed INTEGER DEFAULT 0,
    records_succeeded INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'in_progress',
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_sync_logs_connection ON ehr_sync_logs(ehr_connection_id);
CREATE INDEX idx_sync_logs_status ON ehr_sync_logs(status);
CREATE INDEX idx_sync_logs_started_at ON ehr_sync_logs(started_at DESC);

-- ============================================================================
-- TABLE 12: critical_alerts
-- ============================================================================

CREATE TABLE critical_alerts (
    id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
    handoff_id INTEGER NOT NULL REFERENCES handoffs(id) ON DELETE CASCADE,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    detected_by_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    ai_confidence DECIMAL(3,2),
    alert_message TEXT NOT NULL,
    recommended_actions TEXT,
    notified_users INTEGER[],
    notification_method VARCHAR(50),
    notified_at TIMESTAMP WITH TIME ZONE,
    acknowledged_by_user_id INTEGER REFERENCES users(id),
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    action_taken TEXT,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_alerts_facility ON critical_alerts(facility_id);
CREATE INDEX idx_alerts_handoff ON critical_alerts(handoff_id);
CREATE INDEX idx_alerts_patient ON critical_alerts(patient_id);
CREATE INDEX idx_alerts_severity ON critical_alerts(severity);
CREATE INDEX idx_alerts_unresolved ON critical_alerts(resolved_at) WHERE resolved_at IS NULL;

-- ============================================================================
-- VIEWS
-- ============================================================================

CREATE VIEW v_user_leaderboard AS
SELECT
    u.id,
    u.facility_id,
    u.first_name,
    u.last_name,
    u.role,
    COALESCE(SUM(rp.points_earned), 0) as total_points,
    COUNT(h.id) as total_handoffs,
    COUNT(CASE WHEN h.is_baseline THEN 1 END) as baseline_handoffs,
    COUNT(CASE WHEN NOT h.is_baseline THEN 1 END) as update_handoffs
FROM users u
LEFT JOIN rewards_points rp ON u.id = rp.user_id
LEFT JOIN handoffs h ON u.id = h.created_by_user_id
WHERE u.deleted_at IS NULL
GROUP BY u.id, u.facility_id, u.first_name, u.last_name, u.role;

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_facilities_updated_at BEFORE UPDATE ON facilities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_handoffs_updated_at BEFORE UPDATE ON handoffs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ehr_connections_updated_at BEFORE UPDATE ON ehr_connections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- ROW LEVEL SECURITY (Enable for Supabase)
-- ============================================================================

ALTER TABLE facilities ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE handoffs ENABLE ROW LEVEL SECURITY;
ALTER TABLE handoff_changes ENABLE ROW LEVEL SECURITY;
ALTER TABLE rewards_points ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE handoff_assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE ehr_connections ENABLE ROW LEVEL SECURITY;
ALTER TABLE ehr_sync_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE critical_alerts ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- SEED DATA (Demo facility for development)
-- ============================================================================

INSERT INTO facilities (name, address, city, state, zip_code, phone, email, license_number, subscription_tier)
VALUES ('Demo General Hospital', '123 Healthcare Blvd', 'Medical City', 'CA', '90210', '555-0100', 'admin@demohospital.com', 'LIC-DGH-2024', 'premium');

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
