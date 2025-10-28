-- Seed Data for EclipseLink AI
-- Run this after schema.sql to populate database with test data
--
-- Usage: psql -d eclipselink -f database/seed-data.sql

BEGIN;

-- Clear existing data (use CASCADE carefully!)
TRUNCATE TABLE audit_logs CASCADE;
TRUNCATE TABLE rewards_points CASCADE;
TRUNCATE TABLE handoffs CASCADE;
TRUNCATE TABLE patients CASCADE;
TRUNCATE TABLE users CASCADE;
TRUNCATE TABLE facilities CASCADE;

-- =============================================
-- 1. DEMO FACILITY
-- =============================================
INSERT INTO facilities (
    id,
    name,
    address,
    city,
    state,
    zip_code,
    phone,
    email,
    license_number,
    subscription_tier,
    subscription_status,
    subscription_expires_at,
    features
) VALUES (
    1,
    'Demo General Hospital',
    '123 Healthcare Blvd',
    'Portland',
    'Oregon',
    '97201',
    '503-555-1234',
    'admin@demohospital.com',
    'LIC-OR-2025-001',
    'trial',
    'active',
    NOW() + INTERVAL '30 days',
    '{"ehr_integration": false}'::jsonb
);

-- Reset sequence
SELECT setval('facilities_id_seq', 1, true);

-- =============================================
-- 2. DEMO USERS (Multiple Roles)
-- =============================================
-- Password for all demo users: "DemoPass2025!"
-- Hashed with bcrypt (cost 12)
-- In production, generate this with: bcrypt.hashpw("DemoPass2025!".encode(), bcrypt.gensalt(12))

INSERT INTO users (
    id,
    facility_id,
    email,
    password_hash,
    email_verified,
    first_name,
    last_name,
    phone,
    role,
    department,
    license_number,
    is_admin,
    is_active
) VALUES
-- 1. Registered Nurse (RN) - Primary demo user
(
    1,
    1,
    'nurse.sarah@demohospital.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LqH6PfQKtf6.kWZ8W', -- DemoPass2025!
    true,
    'Sarah',
    'Williams',
    '503-555-2001',
    'RN',
    'Medical-Surgical',
    'RN-OR-123456',
    false,
    true
),

-- 2. Doctor (MD)
(
    2,
    1,
    'dr.johnson@demohospital.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LqH6PfQKtf6.kWZ8W',
    true,
    'Michael',
    'Johnson',
    '503-555-2002',
    'MD',
    'Internal Medicine',
    'MD-OR-789012',
    false,
    true
),

-- 3. Physical Therapist (PT)
(
    3,
    1,
    'pt.chen@demohospital.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LqH6PfQKtf6.kWZ8W',
    true,
    'Lisa',
    'Chen',
    '503-555-2003',
    'PT',
    'Rehabilitation',
    'PT-OR-345678',
    false,
    true
),

-- 4. Licensed Practical Nurse (LPN)
(
    4,
    1,
    'lpn.davis@demohospital.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LqH6PfQKtf6.kWZ8W',
    true,
    'Emily',
    'Davis',
    '503-555-2004',
    'LPN',
    'Medical-Surgical',
    'LPN-OR-901234',
    false,
    true
),

-- 5. Admin User
(
    5,
    1,
    'admin@demohospital.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LqH6PfQKtf6.kWZ8W',
    true,
    'Hannah',
    'Admin',
    '503-555-2000',
    'RN',
    'Administration',
    'RN-OR-000001',
    true,
    true
);

-- Reset sequence
SELECT setval('users_id_seq', 5, true);

-- =============================================
-- 3. DEMO PATIENTS
-- =============================================
INSERT INTO patients (
    id,
    facility_id,
    mrn,
    first_name,
    last_name,
    date_of_birth,
    gender,
    phone,
    email,
    address,
    city,
    state,
    zip_code,
    emergency_contact_name,
    emergency_contact_phone,
    emergency_contact_relation,
    room_number,
    admission_date,
    primary_diagnosis,
    allergies,
    code_status,
    status
) VALUES
-- Patient 1: Pneumonia case (no baseline yet)
(
    1,
    1,
    'MRN-10234',
    'Sarah',
    'Johnson',
    '1958-03-15',
    'Female',
    '503-555-3001',
    'sarah.j@email.com',
    '456 Oak Street',
    'Portland',
    'OR',
    '97202',
    'John Johnson (Husband)',
    '503-555-3002',
    'Spouse',
    '302',
    '2025-10-26',
    'Community-acquired pneumonia',
    'Penicillin (rash)',
    'Full Code',
    'active'
),

-- Patient 2: Post-operative hip replacement (has baseline)
(
    2,
    1,
    'MRN-10235',
    'Michael',
    'Chen',
    '1945-07-22',
    'Male',
    '503-555-3003',
    'mchen@email.com',
    '789 Maple Ave',
    'Portland',
    'OR',
    '97203',
    'Jennifer Chen (Daughter)',
    '503-555-3004',
    'Daughter',
    '315',
    '2025-10-25',
    'Post-operative right hip arthroplasty',
    'NKDA (No Known Drug Allergies)',
    'Full Code',
    'active'
),

-- Patient 3: CHF exacerbation (has baseline)
(
    3,
    1,
    'MRN-10236',
    'Elizabeth',
    'Martinez',
    '1962-11-08',
    'Female',
    '503-555-3005',
    'e.martinez@email.com',
    '321 Birch Lane',
    'Portland',
    'OR',
    '97204',
    'Carlos Martinez (Son)',
    '503-555-3006',
    'Son',
    '218',
    '2025-10-24',
    'Congestive heart failure exacerbation',
    'Sulfa drugs (hives)',
    'DNR (Do Not Resuscitate)',
    'active'
),

-- Patient 4: Diabetic ketoacidosis (no baseline yet)
(
    4,
    1,
    'MRN-10237',
    'Robert',
    'Williams',
    '1970-05-30',
    'Male',
    '503-555-3007',
    'rwilliams@email.com',
    '654 Cedar Drive',
    'Portland',
    'OR',
    '97205',
    'Mary Williams (Wife)',
    '503-555-3008',
    'Spouse',
    '421',
    '2025-10-27',
    'Diabetic ketoacidosis (DKA)',
    'NKDA',
    'Full Code',
    'active'
),

-- Patient 5: Stroke recovery (has baseline)
(
    5,
    1,
    'MRN-10238',
    'Margaret',
    'Thompson',
    '1952-09-12',
    'Female',
    '503-555-3009',
    'mthompson@email.com',
    '987 Pine Street',
    'Portland',
    'OR',
    '97206',
    'David Thompson (Husband)',
    '503-555-3010',
    'Spouse',
    '112',
    '2025-10-23',
    'Ischemic stroke with left-sided weakness',
    'Aspirin (GI upset)',
    'Full Code',
    'active'
);

-- Reset sequence
SELECT setval('patients_id_seq', 5, true);

-- =============================================
-- 4. SAMPLE HANDOFFS (Baseline for some patients)
-- =============================================
INSERT INTO handoffs (
    id,
    facility_id,
    patient_id,
    created_by_user_id,
    is_baseline,
    baseline_handoff_id,
    audio_file_url,
    audio_duration_seconds,
    audio_file_size_bytes,
    transcript_text,
    transcript_confidence,
    transcribed_at,
    sbar_situation,
    sbar_background,
    sbar_assessment,
    sbar_recommendation,
    ai_processing_time_ms,
    ai_processed_at,
    has_critical_alert,
    status,
    created_at
) VALUES
-- Baseline for Patient 2 (Michael Chen - Hip replacement)
(
    1,
    1,
    2,
    1,
    true,
    NULL,
    '/uploads/handoffs/2025/10/27/handoff-001.webm',
    65,
    245000,
    'Patient is Michael Chen, 80-year-old male in room 315. Post-op day 2 from right total hip arthroplasty. Epidural removed this morning, transitioned to oral pain meds. Vitals stable - BP 132/78, heart rate 76, temp 98.4, oxygen saturation 96% on room air. Pain controlled at 3 out of 10. Physical therapy evaluated today, able to ambulate 20 feet with walker. No signs of infection at surgical site. Drain output minimal. Diet advanced to regular, tolerating well. Voiding without issues. Plan to continue PT twice daily, monitor for DVT signs, discharge planning started for home with home health.',
    0.94,
    NOW() - INTERVAL '2 days',
    'Michael Chen, 80-year-old male in Room 315, post-operative day 2 from right total hip arthroplasty. Currently stable on oral pain management.',
    'Admitted 10/25 for elective right hip replacement due to severe osteoarthritis. PMH includes hypertension (well-controlled), hyperlipidemia. No known drug allergies. Full code status. Surgery uncomplicated, epidural for post-op pain management removed this morning.',
    'Patient showing good recovery - vital signs stable (BP 132/78, HR 76, Temp 98.4°F, SpO2 96% RA). Pain well-controlled at 3/10 on oral medications. Surgical site clean, dry, intact with minimal drain output. PT evaluation successful with 20-foot ambulation using walker. No signs of DVT or infection. Tolerating regular diet, voiding independently.',
    'Continue current pain management regimen. Physical therapy twice daily with goal of independent transfers. Monitor for signs of DVT (calf tenderness, swelling) and surgical site infection. Continue anticoagulation prophylaxis. Discharge planning in progress for home with home health services. Target discharge in 2-3 days if continued progress.',
    5200,
    NOW() - INTERVAL '2 days',
    false,
    'completed',
    NOW() - INTERVAL '2 days'
),

-- Baseline for Patient 3 (Elizabeth Martinez - CHF)
(
    2,
    1,
    3,
    1,
    true,
    NULL,
    '/uploads/handoffs/2025/10/27/handoff-002.webm',
    58,
    220000,
    'Elizabeth Martinez, 63-year-old female in room 218. Admitted for CHF exacerbation 3 days ago. Has been on IV Lasix, good diuresis achieved with negative 2.5 liters over last 24 hours. Weight down 4 pounds from admission. Breathing improved significantly, oxygen weaned from 4 liters to 2 liters nasal cannula, saturating 93%. Vitals BP 118/72, heart rate 84 regular, temp 98.6. JVD resolved. Lung sounds still with mild crackles at bases but much improved. Edema 1+ in lower extremities, was 3+ on admission. Transitioned to PO Lasix this morning. Cardiology consulted, echo shows EF 35%. Medication optimization ongoing. Patient feeling much better, appetite returning. DNR status confirmed with family.',
    0.92,
    NOW() - INTERVAL '3 days',
    'Elizabeth Martinez, 63-year-old female in Room 218, admitted for CHF exacerbation. Currently improving on IV diuresis, transitioning to oral medications.',
    'Admitted 10/24 with shortness of breath, orthopnea, and lower extremity edema. History of heart failure (EF 35%), hypertension, diabetes type 2. Allergic to sulfa drugs (hives). DNR status per patient and family wishes. Home medications include carvedilol, lisinopril, metformin.',
    'Significant clinical improvement after 3 days of IV Lasix therapy. Net negative 2.5L fluid balance over 24 hours, weight decreased 4 lbs. Respiratory status improved - oxygen requirement decreased from 4L to 2L NC, SpO2 93%. Vital signs stable (BP 118/72, HR 84). Physical exam shows resolved JVD, improved lung sounds (mild bilateral crackles remain), and decreased edema (1+ from 3+). Recent echo confirms EF 35%. Patient reports feeling much better with improved appetite.',
    'Transition to oral Lasix today and monitor response. Continue medication optimization per cardiology recommendations. Daily weights and strict I&O monitoring. Continue oxygen at 2L NC, wean as tolerated with goal of room air. Low-sodium diet education. Case management for home health setup. Plan discharge in 2-3 days if stable on oral diuretics with follow-up in heart failure clinic within 1 week.',
    4800,
    NOW() - INTERVAL '3 days',
    false,
    'completed',
    NOW() - INTERVAL '3 days'
),

-- Baseline for Patient 5 (Margaret Thompson - Stroke)
(
    3,
    1,
    5,
    2,
    true,
    NULL,
    '/uploads/handoffs/2025/10/27/handoff-003.webm',
    72,
    280000,
    'Margaret Thompson, 73-year-old female in room 112. Admitted 5 days ago with acute ischemic stroke, left MCA territory. Received tPA within window. Currently has residual left-sided weakness, 3 out of 5 strength in left arm and leg. Speech normal, no aphasia. Alert and oriented times 3. Vitals stable, BP 138/82, heart rate 78 regular, temp 98.2, oxygen saturation 97% on room air. Neuro checks stable overnight. PT and OT evaluating daily, making slow but steady progress. Swallow study passed, on regular diet with supervision. Started on aspirin and statin for secondary prevention. MRI completed, no hemorrhagic conversion. Rehab facility screening in progress.',
    0.96,
    NOW() - INTERVAL '4 days',
    'Margaret Thompson, 73-year-old female in Room 112, day 5 post-ischemic stroke (left MCA). Currently stable with residual left-sided weakness, participating in therapy.',
    'Admitted 10/23 with sudden onset left-sided weakness and facial droop. CT negative for hemorrhage, MRI showed acute infarct in right MCA territory. Received IV tPA at 2.5 hours from symptom onset. Past medical history includes hypertension, atrial fibrillation (on aspirin, now discussing anticoagulation). Allergic to aspirin causes GI upset, tolerating current dose with food. Full code status.',
    'Patient neurologically stable with persistent but improving left hemiparesis (3/5 strength in left upper and lower extremities). Speech intact without aphasia. Cognition preserved, A&O x3. Vital signs within normal limits (BP 138/82, HR 78, Temp 98.2°F, SpO2 97% RA). Serial neuro checks unchanged overnight. Swallow evaluation passed, advancing diet as tolerated with supervision due to left-sided neglect. Physical and occupational therapy twice daily with gradual functional improvements. MRI confirmed no hemorrhagic transformation.',
    'Continue current stroke protocol with neuro checks every 4 hours. Maintain blood pressure 120-180 systolic per neurology. Continue aspirin 325mg and atorvastatin 80mg for secondary prevention; cardiology to evaluate need for anticoagulation given AFib history. Intensive PT/OT for mobility and ADL training. Consult case management for acute rehab placement - patient requires intensive therapy. Target transfer to rehab facility within 2-3 days. Family meeting scheduled tomorrow to discuss long-term care plan.',
    6100,
    NOW() - INTERVAL '4 days',
    false,
    'completed',
    NOW() - INTERVAL '4 days'
);

-- Reset sequence
SELECT setval('handoffs_id_seq', 3, true);

-- =============================================
-- 5. REWARDS POINTS FOR SAMPLE HANDOFFS
-- =============================================
INSERT INTO rewards_points (
    user_id,
    facility_id,
    points_earned,
    action_type,
    description,
    handoff_id,
    earned_at
) VALUES
(1, 1, 10, 'baseline_handoff', 'Created baseline handoff for Michael Chen', 1, NOW() - INTERVAL '2 days'),
(1, 1, 10, 'baseline_handoff', 'Created baseline handoff for Elizabeth Martinez', 2, NOW() - INTERVAL '3 days'),
(2, 1, 10, 'baseline_handoff', 'Created baseline handoff for Margaret Thompson', 3, NOW() - INTERVAL '4 days');

-- =============================================
-- VERIFICATION QUERIES
-- =============================================
-- Uncomment these to verify the seed data

-- SELECT 'Facilities:', COUNT(*) FROM facilities;
-- SELECT 'Users:', COUNT(*) FROM users;
-- SELECT 'Patients:', COUNT(*) FROM patients;
-- SELECT 'Handoffs:', COUNT(*) FROM handoffs;
-- SELECT 'Rewards:', SUM(points_earned) FROM rewards_points;

COMMIT;

-- Success message
SELECT 'Seed data loaded successfully!' AS status;
SELECT '5 users created (password: DemoPass2025!)' AS info;
SELECT 'Login as: nurse.sarah@demohospital.com' AS demo_user;
