-- Database Functions and Triggers
-- EclipseLink AI™

-- =============================================================================
-- TRIGGER FUNCTIONS
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Function: Update updated_at timestamp
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
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

CREATE TRIGGER update_sbar_reports_updated_at
  BEFORE UPDATE ON sbar_reports
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_handoff_assignments_updated_at
  BEFORE UPDATE ON handoff_assignments
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ehr_connections_updated_at
  BEFORE UPDATE ON ehr_connections
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_settings_updated_at
  BEFORE UPDATE ON system_settings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_feature_flags_updated_at
  BEFORE UPDATE ON feature_flags
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ai_generations_updated_at
  BEFORE UPDATE ON ai_generations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- -----------------------------------------------------------------------------
-- Function: Audit logging for PHI tables
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION log_table_changes()
RETURNS TRIGGER AS $$
DECLARE
  user_id_val UUID;
  user_email_val VARCHAR(255);
  user_role_val user_role;
BEGIN
  -- Get current user info from Supabase auth context
  -- Note: This assumes Supabase auth.uid() is available
  -- Adjust based on your auth implementation
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
    changes,
    phi_accessed
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
    END,
    TG_TABLE_NAME IN ('patients', 'handoffs', 'sbar_reports')
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

CREATE TRIGGER audit_sbar_reports_changes
  AFTER INSERT OR UPDATE OR DELETE ON sbar_reports
  FOR EACH ROW EXECUTE FUNCTION log_table_changes();

CREATE TRIGGER audit_staff_changes
  AFTER INSERT OR UPDATE OR DELETE ON staff
  FOR EACH ROW EXECUTE FUNCTION log_table_changes();

-- =============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- =============================================================================

-- Enable RLS on all tables
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

-- Facility-Level Isolation
CREATE POLICY staff_facility_isolation ON staff
  FOR ALL
  USING (
    facility_id = (
      SELECT facility_id FROM staff
      WHERE auth_id = auth.uid()
    )
  );

CREATE POLICY patients_facility_isolation ON patients
  FOR ALL
  USING (
    facility_id = (
      SELECT facility_id FROM staff
      WHERE auth_id = auth.uid()
    )
  );

CREATE POLICY handoffs_facility_isolation ON handoffs
  FOR ALL
  USING (
    facility_id = (
      SELECT facility_id FROM staff
      WHERE auth_id = auth.uid()
    )
  );

-- Admin full access policy
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

-- Audit logs read policy
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

-- Audit logs are insert-only
CREATE POLICY audit_logs_insert ON audit_logs
  FOR INSERT
  WITH CHECK (true);

-- Notifications policy
CREATE POLICY notifications_user_access ON notifications
  FOR ALL
  USING (user_id = (SELECT id FROM staff WHERE auth_id = auth.uid()));

-- Sessions policy
CREATE POLICY sessions_user_access ON user_sessions
  FOR ALL
  USING (user_id = (SELECT id FROM staff WHERE auth_id = auth.uid()));

COMMENT ON POLICY staff_facility_isolation ON staff IS 'Staff can only see data from their facility';
COMMENT ON POLICY patients_facility_isolation ON patients IS 'Patients scoped to facility';
COMMENT ON POLICY handoffs_facility_isolation ON handoffs IS 'Handoffs scoped to facility';
