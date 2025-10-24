-- EclipseLink AI™ - Seed Data
-- Development/Testing Data Only
-- DO NOT use in production!

BEGIN;

-- Insert a test facility
INSERT INTO facilities (id, name, type, address, city, state, zip_code, phone, email)
VALUES
(
  '550e8400-e29b-41d4-a716-446655440001',
  'General Hospital',
  'hospital',
  '123 Medical Center Dr',
  'San Francisco',
  'CA',
  '94102',
  '(415) 555-0100',
  'admin@generalhospital.com'
);

-- Insert test users (password is 'password123' for all, hashed with bcrypt)
-- Note: In production, use strong unique passwords!
INSERT INTO users (id, email, password_hash, first_name, last_name, role, facility_id, phone, is_active, email_verified)
VALUES
(
  '550e8400-e29b-41d4-a716-446655440101',
  'nurse@example.com',
  '$2b$10$rKvVJZ9vC8aB9qY6jL/hJeEOhXfJZ7KHqPqQZpYZ6sJqZpYZ6sJqZ',
  'Sarah',
  'Johnson',
  'registered_nurse',
  '550e8400-e29b-41d4-a716-446655440001',
  '(415) 555-0101',
  true,
  true
),
(
  '550e8400-e29b-41d4-a716-446655440102',
  'doctor@example.com',
  '$2b$10$rKvVJZ9vC8aB9qY6jL/hJeEOhXfJZ7KHqPqQZpYZ6sJqZpYZ6sJqZ',
  'Michael',
  'Chen',
  'physician',
  '550e8400-e29b-41d4-a716-446655440001',
  '(415) 555-0102',
  true,
  true
),
(
  '550e8400-e29b-41d4-a716-446655440103',
  'admin@example.com',
  '$2b$10$rKvVJZ9vC8aB9qY6jL/hJeEOhXfJZ7KHqPqQZpYZ6sJqZpYZ6sJqZ',
  'Emily',
  'Rodriguez',
  'admin',
  '550e8400-e29b-41d4-a716-446655440001',
  '(415) 555-0103',
  true,
  true
);

-- Insert test patients
INSERT INTO patients (id, mrn, first_name, last_name, date_of_birth, gender, ssn_encrypted, phone, email, address, city, state, zip_code, facility_id)
VALUES
(
  '550e8400-e29b-41d4-a716-446655440201',
  'MRN001234',
  'John',
  'Smith',
  '1965-05-15',
  'male',
  NULL, -- Encrypted in real system
  '(415) 555-0201',
  'john.smith@email.com',
  '456 Patient St',
  'San Francisco',
  'CA',
  '94102',
  '550e8400-e29b-41d4-a716-446655440001'
),
(
  '550e8400-e29b-41d4-a716-446655440202',
  'MRN001235',
  'Jane',
  'Doe',
  '1972-08-22',
  'female',
  NULL,
  '(415) 555-0202',
  'jane.doe@email.com',
  '789 Health Ave',
  'San Francisco',
  'CA',
  '94103',
  '550e8400-e29b-41d4-a716-446655440001'
);

-- Insert a sample handoff
INSERT INTO handoffs (
  id,
  patient_id,
  from_staff_id,
  to_staff_id,
  facility_id,
  handoff_type,
  priority,
  status,
  scheduled_time,
  actual_time
)
VALUES
(
  '550e8400-e29b-41d4-a716-446655440301',
  '550e8400-e29b-41d4-a716-446655440201',
  '550e8400-e29b-41d4-a716-446655440101',
  '550e8400-e29b-41d4-a716-446655440102',
  '550e8400-e29b-41d4-a716-446655440001',
  'shift_change',
  'routine',
  'completed',
  NOW(),
  NOW()
);

-- Insert a sample SBAR report
INSERT INTO sbar_reports (
  id,
  handoff_id,
  patient_id,
  situation,
  background,
  assessment,
  recommendation,
  transcription_text,
  generated_by,
  completeness_score,
  quality_score,
  version,
  is_latest
)
VALUES
(
  '550e8400-e29b-41d4-a716-446655440401',
  '550e8400-e29b-41d4-a716-446655440301',
  '550e8400-e29b-41d4-a716-446655440201',
  'Patient is a 58-year-old male admitted for chest pain. Current vital signs are stable with BP 135/85, HR 78, SpO2 98% on room air.',
  'Patient has a history of hypertension and type 2 diabetes. He presented to the ER 6 hours ago with chest pain rated 7/10. EKG showed no acute ST changes. Troponin levels were normal. He received aspirin and nitroglycerin in the ER.',
  'Chest pain is likely non-cardiac in origin, possibly musculoskeletal. Patient reports pain improves with position changes. No radiation to arm or jaw. Cardiac workup negative so far. Continue monitoring.',
  'Continue telemetry monitoring overnight. Repeat troponin in 6 hours. Maintain current medications. Cardiology consult in the morning if symptoms persist. Patient is NPO after midnight for possible stress test tomorrow.',
  'This is a voice transcription of the clinical handoff...',
  'ai-generated',
  0.92,
  0.88,
  1,
  true
);

-- Insert sample voice recording metadata
INSERT INTO voice_recordings (
  id,
  handoff_id,
  file_path,
  file_size,
  duration,
  status,
  uploaded_by
)
VALUES
(
  '550e8400-e29b-41d4-a716-446655440501',
  '550e8400-e29b-41d4-a716-446655440301',
  'audio/2025/sample-handoff.webm',
  245678,
  182,
  'transcribed',
  '550e8400-e29b-41d4-a716-446655440101'
);

-- Create audit log entry
INSERT INTO audit_logs (
  id,
  user_id,
  action,
  resource_type,
  resource_id,
  patient_id,
  facility_id,
  ip_address,
  user_agent,
  result
)
VALUES
(
  gen_random_uuid(),
  '550e8400-e29b-41d4-a716-446655440101',
  'handoff_create',
  'handoff',
  '550e8400-e29b-41d4-a716-446655440301',
  '550e8400-e29b-41d4-a716-446655440201',
  '550e8400-e29b-41d4-a716-446655440001',
  '192.168.1.100',
  'Mozilla/5.0 (Test Browser)',
  'success'
);

COMMIT;

-- Display seed data summary
SELECT 'Seed data inserted successfully!' as message;
SELECT 'Test Users:' as info;
SELECT email, first_name, last_name, role FROM users;
SELECT '' as spacing;
SELECT 'Test Patients:' as info;
SELECT mrn, first_name, last_name FROM patients;
SELECT '' as spacing;
SELECT 'Login credentials (all users):' as info;
SELECT 'Password: password123' as note;
