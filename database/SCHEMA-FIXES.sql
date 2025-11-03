-- ============================================================================
-- CRITICAL FIXES FOR schema-creative-production.sql
-- Apply these fixes AFTER running the main schema
-- ============================================================================

-- ============================================================================
-- FIX #1: Correct RLS Policies for Supabase Auth
-- ============================================================================

-- Drop incorrect policies
DROP POLICY IF EXISTS "authenticated_users_view_patients" ON patients;
DROP POLICY IF EXISTS "authenticated_users_create_patients" ON patients;
DROP POLICY IF EXISTS "authenticated_users_update_patients" ON patients;
DROP POLICY IF EXISTS "clinicians_all_patients" ON patients;
DROP POLICY IF EXISTS "families_own_patient" ON patients;

DROP POLICY IF EXISTS "clinicians_all_handoffs" ON handoffs;
DROP POLICY IF EXISTS "families_patient_handoffs" ON handoffs;
DROP POLICY IF EXISTS "authenticated_users_view_handoffs" ON handoffs;
DROP POLICY IF EXISTS "authenticated_users_create_handoffs" ON handoffs;
DROP POLICY IF EXISTS "users_update_own_handoffs" ON handoffs;

-- CORRECTED POLICIES FOR PATIENTS

-- Clinicians can view all patients in their facility
CREATE POLICY "clinicians_view_facility_patients" ON patients
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.facility_id = patients.facility_id
            AND users.user_type = 'clinician'
            AND users.is_active = true
        )
    );

-- Clinicians can create patients
CREATE POLICY "clinicians_create_patients" ON patients
    FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.facility_id = patients.facility_id
            AND users.user_type = 'clinician'
            AND users.is_active = true
        )
    );

-- Clinicians can update patients in their facility
CREATE POLICY "clinicians_update_patients" ON patients
    FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.facility_id = patients.facility_id
            AND users.user_type = 'clinician'
            AND users.is_active = true
        )
    );

-- Families can view their linked patient (if they have a user account)
CREATE POLICY "families_view_linked_patient" ON patients
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.user_type = 'family'
            AND users.patient_id = patients.id
            AND users.is_active = true
        )
    );

-- Patients can view their own record
CREATE POLICY "patients_view_own_record" ON patients
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.user_type = 'patient'
            AND users.id = patients.user_id
        )
    );

-- CORRECTED POLICIES FOR HANDOFFS

-- Clinicians can view all handoffs in their facility
CREATE POLICY "clinicians_view_facility_handoffs" ON handoffs
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.facility_id = handoffs.facility_id
            AND users.user_type = 'clinician'
            AND users.is_active = true
        )
    );

-- Clinicians can create handoffs
CREATE POLICY "clinicians_create_handoffs" ON handoffs
    FOR INSERT
    WITH CHECK (
        auth.uid() = created_by AND
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.user_type = 'clinician'
            AND users.is_active = true
        )
    );

-- Clinicians can update their own handoffs
CREATE POLICY "clinicians_update_own_handoffs" ON handoffs
    FOR UPDATE
    USING (
        created_by = auth.uid() AND
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.user_type = 'clinician'
        )
    );

-- Families can view handoffs for their patient (if they have user account)
CREATE POLICY "families_view_patient_handoffs" ON handoffs
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.user_type = 'family'
            AND users.patient_id = handoffs.patient_id
            AND users.is_active = true
        )
    );

-- CORRECTED POLICIES FOR FAMILY_ACCESS

DROP POLICY IF EXISTS "clinicians_manage_family_access" ON family_access;
DROP POLICY IF EXISTS "families_own_access" ON family_access;

-- Clinicians can manage family access for their facility's patients
CREATE POLICY "clinicians_manage_family_access" ON family_access
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.facility_id = family_access.facility_id
            AND users.user_type = 'clinician'
            AND users.is_active = true
        )
    );

-- Families can view their own access records
CREATE POLICY "families_view_own_access" ON family_access
    FOR SELECT
    USING (
        user_id = auth.uid() OR
        -- Allow service role for token-based access
        auth.role() = 'service_role'
    );

-- CORRECTED POLICIES FOR NOTIFICATIONS

DROP POLICY IF EXISTS "users_own_notifications" ON notifications;

-- Users can view their own notifications
CREATE POLICY "users_view_own_notifications" ON notifications
    FOR SELECT
    USING (user_id = auth.uid());

-- System can create notifications (service role)
CREATE POLICY "system_create_notifications" ON notifications
    FOR INSERT
    WITH CHECK (auth.role() = 'service_role' OR auth.uid() = user_id);

-- CORRECTED POLICIES FOR FACILITIES

DROP POLICY IF EXISTS "users_own_facility" ON facilities;

-- Users can view their facility
CREATE POLICY "users_view_own_facility" ON facilities
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.facility_id = facilities.id
        )
    );

-- Admins can update their facility
CREATE POLICY "admins_update_facility" ON facilities
    FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE users.id = auth.uid()
            AND users.facility_id = facilities.id
            AND users.role = 'admin'
        )
    );

-- CORRECTED POLICIES FOR USERS

DROP POLICY IF EXISTS "users_same_facility" ON users;

-- Users can view users in their facility
CREATE POLICY "users_view_facility_users" ON users
    FOR SELECT
    USING (
        facility_id = (
            SELECT facility_id FROM users WHERE id = auth.uid()
        )
    );

-- Users can update their own profile
CREATE POLICY "users_update_own_profile" ON users
    FOR UPDATE
    USING (id = auth.uid());

-- Admins can manage users in their facility
CREATE POLICY "admins_manage_facility_users" ON users
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users admin
            WHERE admin.id = auth.uid()
            AND admin.facility_id = users.facility_id
            AND admin.role = 'admin'
        )
    );

-- ============================================================================
-- FIX #2: Add Missing Indexes
-- ============================================================================

-- Index for similar handoff lookups (caching)
CREATE INDEX IF NOT EXISTS idx_handoffs_similar
ON handoffs(similar_handoff_id)
WHERE similar_handoff_id IS NOT NULL;

-- Index for family access token lookups (QR code scanning)
CREATE INDEX IF NOT EXISTS idx_family_access_token
ON family_access(access_token)
WHERE is_active = true;

-- Index for notification queries
CREATE INDEX IF NOT EXISTS idx_notifications_unread_user
ON notifications(user_id, created_at DESC)
WHERE is_read = false;

-- Index for audit log security queries
CREATE INDEX IF NOT EXISTS idx_audit_security_level
ON audit_logs(security_level, created_at DESC)
WHERE security_level IN ('sensitive', 'critical');

-- Index for AI cache lookups
CREATE INDEX IF NOT EXISTS idx_ai_cache_lookup
ON ai_cache(cache_key, cache_type)
WHERE expires_at IS NULL OR expires_at > NOW();

-- ============================================================================
-- FIX #3: Add Missing Constraints
-- ============================================================================

-- Email format validation for family_access
ALTER TABLE family_access
ADD CONSTRAINT family_email_format
CHECK (email IS NULL OR email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Phone format validation (basic)
ALTER TABLE users
ADD CONSTRAINT user_phone_format
CHECK (phone IS NULL OR phone ~ '^\+?[0-9]{10,15}$');

ALTER TABLE family_access
ADD CONSTRAINT family_phone_format
CHECK (phone IS NULL OR phone ~ '^\+?[0-9]{10,15}$');

-- Audio file size limit (25MB max for Whisper)
ALTER TABLE handoffs
ADD CONSTRAINT audio_size_limit
CHECK (audio_file_size_bytes IS NULL OR audio_file_size_bytes <= 26214400);

-- Access token length (must be UUID)
ALTER TABLE family_access
ADD CONSTRAINT access_token_format
CHECK (access_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$');

-- PIN must be 6 digits
ALTER TABLE family_access
ADD CONSTRAINT access_pin_format
CHECK (access_pin IS NULL OR access_pin ~ '^[0-9]{6}$');

-- ============================================================================
-- FIX #4: Add Proper Timestamp Types (Use TIMESTAMPTZ)
-- ============================================================================

-- Note: This requires table recreation if you want to change existing columns
-- For new deployments, update the main schema to use TIMESTAMPTZ
-- For existing deployments, this is a migration:

-- Example migration (don't run if using the fixed schema):
-- ALTER TABLE facilities ALTER COLUMN created_at TYPE TIMESTAMPTZ;
-- ALTER TABLE facilities ALTER COLUMN updated_at TYPE TIMESTAMPTZ;
-- (Repeat for all timestamp columns)

-- ============================================================================
-- FIX #5: Add Function for Token-Based Family Access
-- ============================================================================

-- Function to validate family access token (for API routes)
CREATE OR REPLACE FUNCTION validate_family_access_token(token_input TEXT)
RETURNS TABLE(
    access_id UUID,
    patient_id UUID,
    facility_id UUID,
    is_valid BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        fa.id,
        fa.patient_id,
        fa.facility_id,
        (fa.is_active AND
         (fa.expires_at IS NULL OR fa.expires_at > NOW()) AND
         (fa.max_uses IS NULL OR fa.use_count < fa.max_uses)) AS is_valid
    FROM family_access fa
    WHERE fa.access_token = token_input;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to record family access usage
CREATE OR REPLACE FUNCTION record_family_access(
    token_input TEXT,
    ip_addr TEXT DEFAULT NULL
)
RETURNS BOOLEAN AS $$
DECLARE
    access_valid BOOLEAN;
BEGIN
    -- Check if token is valid
    SELECT is_valid INTO access_valid
    FROM validate_family_access_token(token_input);

    IF NOT access_valid THEN
        RETURN FALSE;
    END IF;

    -- Update usage
    UPDATE family_access
    SET
        use_count = use_count + 1,
        last_accessed_at = NOW(),
        last_accessed_ip = ip_addr
    WHERE access_token = token_input;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- FIX #6: Add View for Family Portal (Token-based Access)
-- ============================================================================

-- View for family portal data (doesn't require auth.uid())
CREATE OR REPLACE VIEW v_family_portal_access AS
SELECT
    fa.access_token,
    fa.patient_id,
    fa.facility_id,
    fa.is_active,
    fa.expires_at,
    p.first_name || ' ' || p.last_name AS patient_name,
    p.room_number,
    p.unit,
    f.name AS facility_name
FROM family_access fa
JOIN patients p ON fa.patient_id = p.id
JOIN facilities f ON fa.facility_id = f.id
WHERE fa.is_active = true
AND (fa.expires_at IS NULL OR fa.expires_at > NOW());

-- ============================================================================
-- FIX #7: Update Auto-Audit Function to Handle NULL user_email
-- ============================================================================

DROP FUNCTION IF EXISTS log_audit_trail() CASCADE;

CREATE OR REPLACE FUNCTION log_audit_trail()
RETURNS TRIGGER AS $$
DECLARE
    current_user_email TEXT;
BEGIN
    -- Get user email, default to 'system' if not set
    BEGIN
        current_user_email := current_setting('app.current_user_email', true);
    EXCEPTION WHEN OTHERS THEN
        current_user_email := 'system';
    END;

    IF current_user_email IS NULL OR current_user_email = '' THEN
        current_user_email := 'system';
    END IF;

    IF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_logs (
            facility_id, user_email, action, resource_type, resource_id, changes
        ) VALUES (
            OLD.facility_id,
            current_user_email,
            'delete',
            TG_TABLE_NAME,
            OLD.id,
            row_to_json(OLD)
        );
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_logs (
            facility_id, user_email, action, resource_type, resource_id, changes
        ) VALUES (
            NEW.facility_id,
            current_user_email,
            'update',
            TG_TABLE_NAME,
            NEW.id,
            jsonb_build_object('old', row_to_json(OLD), 'new', row_to_json(NEW))
        );
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_logs (
            facility_id, user_email, action, resource_type, resource_id, changes
        ) VALUES (
            NEW.facility_id,
            current_user_email,
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

-- Re-create triggers
DROP TRIGGER IF EXISTS audit_patients ON patients;
DROP TRIGGER IF EXISTS audit_handoffs ON handoffs;
DROP TRIGGER IF EXISTS audit_family_access ON family_access;

CREATE TRIGGER audit_patients
    AFTER INSERT OR UPDATE OR DELETE ON patients
    FOR EACH ROW EXECUTE FUNCTION log_audit_trail();

CREATE TRIGGER audit_handoffs
    AFTER INSERT OR UPDATE OR DELETE ON handoffs
    FOR EACH ROW EXECUTE FUNCTION log_audit_trail();

CREATE TRIGGER audit_family_access
    AFTER INSERT OR UPDATE OR DELETE ON family_access
    FOR EACH ROW EXECUTE FUNCTION log_audit_trail();

-- ============================================================================
-- FIX #8: Add Cleanup Job for Expired Tokens
-- ============================================================================

-- Function to clean up expired family access tokens
CREATE OR REPLACE FUNCTION cleanup_expired_family_access()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    WITH deleted AS (
        UPDATE family_access
        SET is_active = false
        WHERE is_active = true
        AND expires_at < NOW()
        RETURNING *
    )
    SELECT COUNT(*) INTO deleted_count FROM deleted;

    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Schedule cleanup (requires pg_cron extension)
-- Run daily at 2 AM
-- SELECT cron.schedule(
--     'cleanup-expired-tokens',
--     '0 2 * * *',
--     'SELECT cleanup_expired_family_access()'
-- );

-- ============================================================================
-- END OF FIXES
-- These fixes should be applied AFTER the main schema
-- OR integrated into the main schema for new deployments
-- ============================================================================
