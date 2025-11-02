-- ============================================================================
-- EclipseLink AI - Pilot MVP Database Schema (SOLID Design)
-- PostgreSQL 15+ for 15-20 user pilot program
-- Single Responsibility: Each table has ONE clear purpose
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- TABLE 1: users
-- Single Responsibility: User authentication and profile management
-- ============================================================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Authentication (Single Responsibility: Identity)
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,

    -- Profile (Single Responsibility: User Information)
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    profession VARCHAR(50) NOT NULL DEFAULT 'RN',
    license_number VARCHAR(100),

    -- Authorization (Single Responsibility: Access Control)
    role VARCHAR(20) NOT NULL DEFAULT 'clinician', -- clinician, admin
    is_active BOOLEAN DEFAULT true,

    -- Security Metadata
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- Constraints
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT password_hash_length CHECK (LENGTH(password_hash) >= 60)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;

-- ============================================================================
-- TABLE 2: patients
-- Single Responsibility: Patient demographic and clinical data
-- ============================================================================
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Demographics
    mrn VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20),

    -- Clinical Status
    room_number VARCHAR(20),
    primary_diagnosis TEXT,
    code_status VARCHAR(50) DEFAULT 'Full Code',

    -- Admission Management
    admission_date TIMESTAMP,
    discharge_date TIMESTAMP,
    is_active BOOLEAN DEFAULT true,

    -- Audit Trail
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- Constraints
    CONSTRAINT valid_dob CHECK (date_of_birth <= CURRENT_DATE),
    CONSTRAINT valid_admission_dates CHECK (discharge_date IS NULL OR discharge_date >= admission_date)
);

CREATE INDEX idx_patients_mrn ON patients(mrn);
CREATE INDEX idx_patients_active ON patients(is_active) WHERE is_active = true;
CREATE INDEX idx_patients_room ON patients(room_number) WHERE room_number IS NOT NULL;

-- ============================================================================
-- TABLE 3: handoffs
-- Single Responsibility: Clinical handoff documentation
-- ============================================================================
CREATE TABLE handoffs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Relationships
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    created_by UUID NOT NULL REFERENCES users(id),

    -- Voice Recording Metadata
    audio_url TEXT,
    audio_duration_seconds INTEGER,
    audio_file_size_bytes INTEGER,

    -- AI Processing Results
    transcription TEXT,
    transcription_confidence DECIMAL(3,2),

    -- SBAR Components (JSONB for flexibility - Open/Closed Principle)
    sbar_situation JSONB,
    sbar_background JSONB,
    sbar_assessment JSONB,
    sbar_recommendation JSONB,

    -- Workflow Management
    shift_type VARCHAR(20), -- day, night, evening
    status VARCHAR(20) DEFAULT 'draft', -- draft, completed, archived

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,

    -- Constraints
    CONSTRAINT valid_confidence CHECK (
        transcription_confidence IS NULL OR
        (transcription_confidence >= 0 AND transcription_confidence <= 1)
    ),
    CONSTRAINT valid_duration CHECK (audio_duration_seconds IS NULL OR audio_duration_seconds > 0)
);

CREATE INDEX idx_handoffs_patient ON handoffs(patient_id);
CREATE INDEX idx_handoffs_created_by ON handoffs(created_by);
CREATE INDEX idx_handoffs_status ON handoffs(status);
CREATE INDEX idx_handoffs_created_at ON handoffs(created_at DESC);
CREATE INDEX idx_handoffs_shift ON handoffs(shift_type);

-- Full-text search support
CREATE INDEX idx_handoffs_transcription_fts ON handoffs
    USING gin(to_tsvector('english', COALESCE(transcription, '')));

-- ============================================================================
-- TABLE 4: audit_logs
-- Single Responsibility: HIPAA-compliant audit trail
-- ============================================================================
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Actor Information
    user_id UUID REFERENCES users(id),
    user_email VARCHAR(255) NOT NULL,
    user_ip_address VARCHAR(45),

    -- Action Details
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,

    -- Change Tracking
    changes JSONB,
    metadata JSONB,

    -- Timestamp
    created_at TIMESTAMP DEFAULT NOW(),

    -- Constraints
    CONSTRAINT valid_action CHECK (
        action IN ('create', 'read', 'update', 'delete', 'login', 'logout', 'export')
    )
);

CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_created_at ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_action ON audit_logs(action);

-- ============================================================================
-- TABLE 5: user_sessions
-- Single Responsibility: Session lifecycle management
-- ============================================================================
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Token Management
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    refresh_token_hash VARCHAR(255) UNIQUE,

    -- Security Context
    ip_address VARCHAR(45),
    user_agent TEXT,

    -- Lifecycle
    expires_at TIMESTAMP NOT NULL,
    last_activity_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    revoked_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,

    -- Constraints
    CONSTRAINT valid_expiry CHECK (expires_at > created_at)
);

CREATE INDEX idx_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_sessions_token ON user_sessions(token_hash);
CREATE INDEX idx_sessions_active ON user_sessions(is_active) WHERE is_active = true;
CREATE INDEX idx_sessions_expires ON user_sessions(expires_at);

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- Dependency Inversion: Generic update trigger
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patients_updated_at
    BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_handoffs_updated_at
    BEFORE UPDATE ON handoffs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- AUTOMATIC AUDIT LOGGING
-- Dependency Inversion: Generic audit trigger
-- ============================================================================
CREATE OR REPLACE FUNCTION log_audit_trail()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_logs (user_email, action, resource_type, resource_id, changes)
        VALUES (
            current_setting('app.current_user_email', true),
            'delete',
            TG_TABLE_NAME,
            OLD.id,
            row_to_json(OLD)
        );
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_logs (user_email, action, resource_type, resource_id, changes)
        VALUES (
            current_setting('app.current_user_email', true),
            'update',
            TG_TABLE_NAME,
            NEW.id,
            jsonb_build_object('old', row_to_json(OLD), 'new', row_to_json(NEW))
        );
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_logs (user_email, action, resource_type, resource_id, changes)
        VALUES (
            current_setting('app.current_user_email', true),
            'create',
            TG_TABLE_NAME,
            NEW.id,
            row_to_json(NEW)
        );
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Apply audit logging to critical tables
CREATE TRIGGER audit_patients
    AFTER INSERT OR UPDATE OR DELETE ON patients
    FOR EACH ROW EXECUTE FUNCTION log_audit_trail();

CREATE TRIGGER audit_handoffs
    AFTER INSERT OR UPDATE OR DELETE ON handoffs
    FOR EACH ROW EXECUTE FUNCTION log_audit_trail();

-- ============================================================================
-- VIEWS: Single Responsibility - Data Aggregation
-- ============================================================================

-- View: Active patients with handoff summary
CREATE VIEW v_active_patients AS
SELECT
    p.id,
    p.mrn,
    p.first_name,
    p.last_name,
    p.room_number,
    p.primary_diagnosis,
    p.admission_date,
    COUNT(h.id) as handoff_count,
    MAX(h.created_at) as last_handoff_at,
    u.first_name || ' ' || u.last_name as last_handoff_by
FROM patients p
LEFT JOIN handoffs h ON p.id = h.patient_id AND h.status = 'completed'
LEFT JOIN users u ON h.created_by = u.id
WHERE p.is_active = true
GROUP BY p.id, u.first_name, u.last_name;

-- View: User activity dashboard
CREATE VIEW v_user_activity AS
SELECT
    u.id,
    u.email,
    u.first_name,
    u.last_name,
    u.profession,
    u.role,
    COUNT(DISTINCT h.id) as handoffs_created,
    COUNT(DISTINCT h.patient_id) as patients_handled,
    MAX(h.created_at) as last_handoff_at,
    u.last_login_at,
    u.created_at as user_since
FROM users u
LEFT JOIN handoffs h ON u.id = h.created_by
WHERE u.is_active = true
GROUP BY u.id;

-- View: Daily handoff statistics
CREATE VIEW v_daily_handoff_stats AS
SELECT
    DATE(h.created_at) as date,
    COUNT(*) as total_handoffs,
    COUNT(DISTINCT h.patient_id) as unique_patients,
    COUNT(DISTINCT h.created_by) as active_clinicians,
    AVG(h.audio_duration_seconds) as avg_audio_duration,
    AVG(h.transcription_confidence) as avg_confidence,
    COUNT(*) FILTER (WHERE h.shift_type = 'day') as day_shift_handoffs,
    COUNT(*) FILTER (WHERE h.shift_type = 'night') as night_shift_handoffs,
    COUNT(*) FILTER (WHERE h.shift_type = 'evening') as evening_shift_handoffs
FROM handoffs h
WHERE h.status = 'completed'
GROUP BY DATE(h.created_at)
ORDER BY date DESC;

-- ============================================================================
-- ROW-LEVEL SECURITY (RLS)
-- Single Responsibility: Data access control
-- ============================================================================
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE handoffs ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;

-- Policy: All authenticated users can view patients (pilot - single facility)
CREATE POLICY "authenticated_users_view_patients"
    ON patients FOR SELECT
    USING (auth.role() = 'authenticated');

-- Policy: All authenticated users can create patients
CREATE POLICY "authenticated_users_create_patients"
    ON patients FOR INSERT
    WITH CHECK (auth.role() = 'authenticated');

-- Policy: Users can update any patient (pilot - collaborative environment)
CREATE POLICY "authenticated_users_update_patients"
    ON patients FOR UPDATE
    USING (auth.role() = 'authenticated');

-- Policy: All authenticated users can view handoffs
CREATE POLICY "authenticated_users_view_handoffs"
    ON handoffs FOR SELECT
    USING (auth.role() = 'authenticated');

-- Policy: Users can create handoffs
CREATE POLICY "authenticated_users_create_handoffs"
    ON handoffs FOR INSERT
    WITH CHECK (auth.role() = 'authenticated' AND created_by = auth.uid());

-- Policy: Users can update their own handoffs
CREATE POLICY "users_update_own_handoffs"
    ON handoffs FOR UPDATE
    USING (created_by = auth.uid());

-- Policy: Admins can view all audit logs
CREATE POLICY "admins_view_audit_logs"
    ON audit_logs FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Policy: Users can only view their own sessions
CREATE POLICY "users_view_own_sessions"
    ON user_sessions FOR SELECT
    USING (user_id = auth.uid());

-- ============================================================================
-- INITIAL SEED DATA
-- ============================================================================

-- Create admin user (password: Admin123!)
INSERT INTO users (email, password_hash, first_name, last_name, profession, role)
VALUES (
    'admin@eclipselink.local',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5zcJb7F3pJ/kS',
    'System',
    'Administrator',
    'Admin',
    'admin'
);

-- ============================================================================
-- END OF SCHEMA
-- Created with SOLID principles:
-- - Single Responsibility: Each table has one clear purpose
-- - Open/Closed: JSONB fields allow extension without modification
-- - Liskov Substitution: Consistent interface across all tables
-- - Interface Segregation: Minimal, focused views for specific needs
-- - Dependency Inversion: Generic triggers and functions
-- ============================================================================
