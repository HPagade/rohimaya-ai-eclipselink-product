"""Database initialization and management for EclipseLink AI Demo"""
import sqlite3
from datetime import datetime, timedelta
import random

def init_db():
    """Initialize comprehensive SQLite database with rich sample data"""
    conn = sqlite3.connect('demo_data.db', check_same_thread=False)
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE,
            name TEXT,
            date_of_birth TEXT,
            gender TEXT,
            blood_type TEXT,
            allergies TEXT,
            conditions TEXT,
            medications TEXT,
            emergency_contact TEXT,
            insurance TEXT,
            created_at TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS handoffs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            patient_id TEXT,
            handoff_type TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT,
            completed_at TEXT,
            from_staff TEXT,
            to_staff TEXT,
            specialty TEXT,
            sbar_situation TEXT,
            sbar_background TEXT,
            sbar_assessment TEXT,
            sbar_recommendation TEXT,
            recording_duration INTEGER,
            transcription TEXT,
            quality_score INTEGER,
            completeness_score INTEGER,
            critical_elements_score INTEGER
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            handoff_id INTEGER,
            action TEXT,
            user TEXT,
            timestamp TEXT,
            details TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            role TEXT,
            specialty TEXT,
            department TEXT,
            phone TEXT,
            created_at TEXT
        )
    ''')

    # Check if data already exists
    c.execute('SELECT COUNT(*) FROM patients')
    if c.fetchone()[0] == 0:
        # Insert sample patients
        patients = [
            ('P001234', 'John Smith', '1963-05-15', 'Male', 'O+',
             'Penicillin (rash)', 'Type 2 Diabetes, Hypertension, Hyperlipidemia',
             'Metformin 1000mg BID, Lisinopril 10mg daily, Atorvastatin 40mg daily',
             'Mary Smith (Wife): 555-0101', 'Blue Cross PPO',
             (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d %H:%M:%S')),

            ('P001235', 'Jane Doe', '1978-09-22', 'Female', 'A+',
             'Sulfa drugs (anaphylaxis)', 'Asthma, GERD',
             'Albuterol inhaler PRN, Omeprazole 20mg daily',
             'Robert Doe (Husband): 555-0102', 'Aetna HMO',
             (datetime.now() - timedelta(days=150)).strftime('%Y-%m-%d %H:%M:%S')),

            ('P001236', 'Robert Johnson', '1955-12-03', 'Male', 'B-',
             'None known', 'CHF, COPD, Chronic kidney disease Stage 3',
             'Furosemide 40mg daily, Carvedilol 12.5mg BID, Tiotropium inhaler daily',
             'Alice Johnson (Daughter): 555-0103', 'Medicare',
             (datetime.now() - timedelta(days=200)).strftime('%Y-%m-%d %H:%M:%S')),

            ('P001237', 'Maria Garcia', '1990-03-18', 'Female', 'AB+',
             'Latex', 'Type 1 Diabetes, Hypothyroidism',
             'Insulin pump, Levothyroxine 100mcg daily',
             'Carlos Garcia (Father): 555-0104', 'United Healthcare',
             (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d %H:%M:%S')),

            ('P001238', 'William Chen', '1945-07-30', 'Male', 'A-',
             'Aspirin (GI bleeding)', 'Atrial fibrillation, Stroke history, Dementia',
             'Apixaban 5mg BID, Metoprolol 50mg BID, Donepezil 10mg daily',
             'Linda Chen (Wife): 555-0105', 'Medicare + Medicaid',
             (datetime.now() - timedelta(days=250)).strftime('%Y-%m-%d %H:%M:%S')),

            ('P001239', 'Sarah Williams', '1982-11-12', 'Female', 'O-',
             'Iodine', 'Post-surgical (appendectomy), Anxiety',
             'Citalopram 20mg daily, PRN pain meds',
             'Michael Williams (Husband): 555-0106', 'Cigna PPO',
             (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S')),

            ('P001240', 'David Brown', '1968-04-25', 'Male', 'B+',
             'Shellfish', 'CAD s/p stent, Hyperlipidemia',
             'Aspirin 81mg daily, Clopidogrel 75mg daily, Atorvastatin 80mg daily',
             'Jennifer Brown (Wife): 555-0107', 'Blue Shield HMO',
             (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d %H:%M:%S')),

            ('P001241', 'Lisa Anderson', '1995-08-08', 'Female', 'A+',
             'None known', 'Sickle cell disease, Asthma',
             'Hydroxyurea 500mg daily, Folic acid 1mg daily, Albuterol PRN',
             'Patricia Anderson (Mother): 555-0108', 'Medicaid',
             (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d %H:%M:%S')),

            ('P001242', 'James Martinez', '1952-02-14', 'Male', 'O+',
             'Morphine', 'Prostate cancer, Hypertension',
             'Enzalutamide 160mg daily, Amlodipine 10mg daily',
             'Rosa Martinez (Wife): 555-0109', 'VA Healthcare',
             (datetime.now() - timedelta(days=300)).strftime('%Y-%m-%d %H:%M:%S')),

            ('P001243', 'Emily Taylor', '2005-06-20', 'Female', 'AB-',
             'Tree nuts (anaphylaxis)', 'Type 1 Diabetes, Celiac disease',
             'Insulin pump, Vitamin D 2000IU daily',
             'Karen Taylor (Mother): 555-0110', 'Blue Cross PPO',
             (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')),
        ]

        c.executemany('''
            INSERT INTO patients (patient_id, name, date_of_birth, gender, blood_type,
                                allergies, conditions, medications, emergency_contact, insurance, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', patients)

        # Insert sample users
        users = [
            ('Dr. Sarah Johnson', 'sarah.johnson@hospital.com', 'Physician', 'Emergency Medicine', 'Emergency Department', '555-1001', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('RN Michael Chen', 'michael.chen@hospital.com', 'Registered Nurse', 'Critical Care', 'ICU', '555-1002', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('Dr. David Kim', 'david.kim@hospital.com', 'Physician', 'Internal Medicine', 'General Medicine', '555-1003', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('RN Jennifer Lopez', 'jennifer.lopez@hospital.com', 'Registered Nurse', 'Medical-Surgical', 'Floor 3', '555-1004', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('Dr. Emily Roberts', 'emily.roberts@hospital.com', 'Physician', 'Cardiology', 'Cardiac Unit', '555-1005', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('RN Robert Taylor', 'robert.taylor@hospital.com', 'Registered Nurse', 'Emergency', 'Emergency Department', '555-1006', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ]

        c.executemany('''
            INSERT INTO users (name, email, role, specialty, department, phone, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', users)

        # Insert comprehensive sample handoffs with timestamps spread over past 30 days
        handoffs = [
            # Completed handoffs with full SBAR
            ('John Smith', 'P001234', 'shift_change', 'routine', 'completed',
             (datetime.now() - timedelta(days=2, hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=2, hours=7, minutes=45)).strftime('%Y-%m-%d %H:%M:%S'),
             'Dr. Sarah Johnson', 'RN Michael Chen', 'Endocrinology',
             '60-year-old male with type 2 diabetes. Current glucose 145 mg/dL. Alert and oriented x3. Patient reports improved energy levels and decreased thirst.',
             'History of T2DM (10 years), hypertension, hyperlipidemia. Home meds: Metformin 1000mg BID, Lisinopril 10mg daily, Atorvastatin 40mg daily. Known PCN allergy (rash). Lives at home with spouse, independent ADLs.',
             'Vital signs stable: BP 130/85, HR 78, RR 16, SpO2 98% RA, Temp 98.6°F. Blood glucose trending down with insulin regimen. Recent HbA1c 8.2%. No acute distress. Last BG check at 1400: 140 mg/dL.',
             'Continue insulin sliding scale. Discharge education completed - patient verbalizes understanding. Discharge planning for tomorrow if glucose remains stable. Follow-up with endocrinology in 2 weeks. Continue home meds upon discharge.',
             185, 'Patient handoff for John Smith...', 92, 95, 90),

            ('Jane Doe', 'P001235', 'transfer', 'urgent', 'completed',
             (datetime.now() - timedelta(days=1, hours=14)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=1, hours=13, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
             'RN Jennifer Lopez', 'Dr. David Kim', 'Pulmonology',
             '45-year-old female with acute asthma exacerbation. Currently on continuous albuterol nebulizer. Oxygen saturation 94% on 2L NC. Breathing labored but improved from admission.',
             'Known asthmatic with GERD. Recent URI symptoms x 3 days. Sulfa allergy (anaphylaxis). Home meds: Albuterol PRN, Omeprazole 20mg daily. No recent hospitalizations. Works as teacher, high stress.',
             'VS: BP 135/88, HR 102, RR 24, SpO2 94% on 2L, Temp 99.1°F. Mild wheezing bilaterally, decreased air movement lower lobes. Peak flow 60% of predicted. Last albuterol 30 min ago. CXR shows hyperinflation, no infiltrates.',
             'Transfer to ICU for closer monitoring. Continue continuous nebulizers. Start IV methylprednisolone 125mg q6h. Magnesium sulfate 2g IV if no improvement. Consider BiPAP if respiratory distress worsens. Pulmonology consult placed.',
             142, 'Emergency transfer for respiratory distress...', 88, 92, 85),

            ('Robert Johnson', 'P001236', 'admission', 'urgent', 'completed',
             (datetime.now() - timedelta(days=3, hours=20)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=3, hours=19, minutes=15)).strftime('%Y-%m-%d %H:%M:%S'),
             'Dr. Emily Roberts', 'RN Michael Chen', 'Cardiology',
             '68-year-old male with CHF exacerbation. Presenting with increasing shortness of breath and lower extremity edema over past week. Weight gain of 8 pounds. Currently dyspneic at rest.',
             'History of CHF (EF 30%), COPD, CKD Stage 3. Home meds: Furosemide 40mg daily, Carvedilol 12.5mg BID, Tiotropium daily. Non-compliant with low-sodium diet per patient admission. No IV drug use. Lives alone, daughter checks on him.',
             'VS: BP 150/95, HR 95, RR 28, SpO2 88% on RA, 93% on 4L NC, Temp 98.2°F. JVD present, crackles bilateral lung bases, 3+ pitting edema bilateral lower extremities. BNP 1250, Creatinine 2.1 (baseline 1.8). CXR shows pulmonary edema.',
             'Admit to telemetry. IV Furosemide 80mg bolus then 40mg IV q12h. Strict I&O, daily weights. Fluid restriction 1.5L/day. Cardiac diet. May need BiPAP if work of breathing increases. Cardiology consult in AM. Nephrology aware given CKD.',
             210, 'CHF exacerbation admission...', 94, 96, 92),

            ('Maria Garcia', 'P001237', 'procedure', 'routine', 'completed',
             (datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(hours=4, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
             'RN Robert Taylor', 'Dr. Sarah Johnson', 'Endocrinology',
             '34-year-old female with T1DM scheduled for insulin pump site change. Patient brought her own supplies. Currently in procedure room, NPO x 2 hours, last BG 158 at 0800.',
             'T1DM since age 12, on insulin pump therapy for 8 years. Hypothyroidism on Levothyroxine. Latex allergy - using non-latex gloves. A1C last month 7.1%, well-controlled. Works as accountant, very compliant with care.',
             'VS stable: BP 118/72, HR 70, RR 14, SpO2 99% RA, Temp 98.4°F. BG 158 (target 80-180). Patient alert, anxious about procedure. Old pump site shows no signs of infection. New site selected on left abdomen, prepped and ready.',
             'Proceed with pump site change using patient\'s supplies. Monitor BG closely post-procedure. Patient to bolus for correction if BG >180. Resume normal diet after procedure. Patient education reinforced. F/U in diabetes clinic in 3 months.',
             95, 'Pre-procedure handoff for pump change...', 90, 93, 88),

            ('William Chen', 'P001238', 'shift_change', 'urgent', 'completed',
             (datetime.now() - timedelta(days=1, hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=1, hours=1, minutes=45)).strftime('%Y-%m-%d %H:%M:%S'),
             'RN Jennifer Lopez', 'RN Robert Taylor', 'Neurology',
             '78-year-old male with history of stroke and dementia. New onset confusion and agitation this shift. Pulled out IV x 2. Family at bedside concerned about change in mental status.',
             'Stroke 2 years ago, vascular dementia, AFib on anticoagulation. Aspirin allergy (GI bleeding). Lives in memory care facility. Baseline: oriented to person only, requires assistance with ADLs. Meds: Apixaban, Metoprolol, Donepezil.',
             'VS: BP 165/92, HR 88 irregular, RR 18, SpO2 96% RA, Temp 100.2°F. Increased agitation, more confused than baseline. UA sent - pending. No focal neuro deficits noted. Fall risk - bed alarm on, 1:1 sitter in place.',
             'Monitor for UTI (common cause of delirium in elderly). Hold Apixaban pending family discussion about goals of care. Avoid restraints - use redirection and reorientation. Consider Tylenol for low-grade fever. Neurology aware. Update family if condition changes.',
             167, 'Change in mental status...', 87, 90, 84),

            ('Sarah Williams', 'P001239', 'discharge', 'routine', 'completed',
             (datetime.now() - timedelta(hours=10)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(hours=9, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
             'Dr. David Kim', 'RN Jennifer Lopez', 'General Surgery',
             '42-year-old female POD #3 from laparoscopic appendectomy. Doing well, tolerating regular diet, pain controlled with oral meds. Ambulating without assistance. Ready for discharge home.',
             'Post-op from uncomplicated appendectomy. History of anxiety on Citalopram. Iodine allergy. Married, works as graphic designer from home. Strong support system. No surgical history prior to this admission.',
             'VS stable: BP 122/78, HR 72, RR 14, SpO2 99% RA, Temp 98.6°F. Incisions clean, dry, intact - no erythema or drainage. Abdomen soft, non-tender. Bowel sounds present. Pain 2/10 with oral meds. Ambulating well.',
             'Discharge home with husband present. Scripts: Ibuprofen 600mg q6h PRN, Percocet 5/325 1-2 tabs q4h PRN breakthrough pain. Wound care instructions provided and understood. F/U with surgeon in 1 week. Return precautions reviewed.',
             132, 'Discharge planning complete...', 95, 97, 93),

            ('David Brown', 'P001240', 'transfer', 'emergent', 'completed',
             (datetime.now() - timedelta(days=1, hours=6)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=1, hours=5, minutes=40)).strftime('%Y-%m-%d %H:%M:%S'),
             'Dr. Sarah Johnson', 'Dr. Emily Roberts', 'Cardiology',
             '55-year-old male with chest pain x 1 hour. Troponin elevated at 0.8. EKG shows ST depression in lateral leads. Currently on heparin drip, pain improved with nitroglycerin. STEMI alert called.',
             'CAD s/p stent to LAD 2 years ago. On dual antiplatelet therapy. Hyperlipidemia. Shellfish allergy. Current meds: Aspirin 81mg, Clopidogrel 75mg, Atorvastatin 80mg. Non-smoker. Works in construction.',
             'VS: BP 155/90, HR 95, RR 18, SpO2 97% on 2L, Temp 98.6°F. Chest pain 8/10 on arrival, now 3/10 after NTG. Troponin 0.8 (0.05), trending. EKG shows ST depression V4-V6. Cardiology at bedside. Cath lab activated.',
             'Emergent transfer to cath lab for cardiac catheterization. Continue heparin, aspirin, clopidogrel held. Pre-cath checklist complete. Consent signed. Wife notified and en route. NPO. Anticipate possible stent placement.',
             156, 'STEMI activation...', 96, 98, 95),

            # Active/Pending handoffs
            ('Lisa Anderson', 'P001241', 'admission', 'urgent', 'active',
             (datetime.now() - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S'),
             None,
             'Dr. Sarah Johnson', 'RN Michael Chen', 'Hematology',
             None, None, None, None, None, None, None, None, None),

            ('James Martinez', 'P001242', 'shift_change', 'routine', 'active',
             (datetime.now() - timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
             None,
             'RN Jennifer Lopez', 'RN Robert Taylor', 'Oncology',
             None, None, None, None, None, None, None, None, None),

            ('Emily Taylor', 'P001243', 'procedure', 'routine', 'pending',
             (datetime.now() - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S'),
             None,
             'RN Robert Taylor', 'Dr. David Kim', 'Endocrinology',
             None, None, None, None, None, None, None, None, None),

            # Additional completed handoffs for analytics (past 30 days)
            ('John Smith', 'P001234', 'shift_change', 'routine', 'completed',
             (datetime.now() - timedelta(days=5, hours=12)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=5, hours=11, minutes=45)).strftime('%Y-%m-%d %H:%M:%S'),
             'RN Michael Chen', 'Dr. Sarah Johnson', 'Endocrinology',
             'Follow-up on glucose control...', 'Continued management...', 'Improving trend...', 'Maintain current regimen...', 178, 'Follow-up handoff...', 90, 92, 88),

            ('Jane Doe', 'P001235', 'shift_change', 'routine', 'completed',
             (datetime.now() - timedelta(days=7, hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=7, hours=7, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
             'RN Robert Taylor', 'RN Jennifer Lopez', 'Pulmonology',
             'Patient stable post-ICU transfer...', 'Recovering from asthma exacerbation...', 'Respiratory status improved...', 'Prepare for discharge in 48h...', 145, 'Stable handoff...', 88, 90, 86),

            ('Robert Johnson', 'P001236', 'shift_change', 'routine', 'completed',
             (datetime.now() - timedelta(days=10, hours=20)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=10, hours=19, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
             'Dr. Emily Roberts', 'Dr. David Kim', 'Cardiology',
             'CHF patient showing improvement...', 'Volume overload resolving...', 'Diuresis effective...', 'Transition to PO diuretics...', 190, 'CHF follow-up...', 91, 93, 89),

            ('David Brown', 'P001240', 'discharge', 'routine', 'completed',
             (datetime.now() - timedelta(days=12, hours=14)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=12, hours=13, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
             'Dr. Emily Roberts', 'RN Jennifer Lopez', 'Cardiology',
             'Post-cath discharge, stent placed successfully...', 'New stent to RCA...', 'Patient stable, chest pain resolved...', 'Dual antiplatelet therapy, cardiac rehab referral...', 125, 'Post-procedure discharge...', 94, 96, 92),

            ('Sarah Williams', 'P001239', 'admission', 'emergent', 'completed',
             (datetime.now() - timedelta(days=15, hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=15, hours=2, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
             'Dr. Sarah Johnson', 'Dr. David Kim', 'General Surgery',
             'Acute appendicitis, emergent surgery needed...', 'Previously healthy, sudden onset RLQ pain...', 'CT confirms appendicitis, no perforation...', 'Emergent appendectomy, surgery consult at bedside...', 98, 'Emergency admission...', 89, 91, 87),

            ('Maria Garcia', 'P001237', 'shift_change', 'routine', 'completed',
             (datetime.now() - timedelta(days=18, hours=16)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=18, hours=15, minutes=45)).strftime('%Y-%m-%d %H:%M:%S'),
             'RN Jennifer Lopez', 'RN Michael Chen', 'Endocrinology',
             'T1DM patient, pump functioning well...', 'Excellent glucose control...', 'No concerns, patient independent...', 'Continue current pump settings...', 110, 'Routine handoff...', 92, 94, 90),

            ('William Chen', 'P001238', 'admission', 'urgent', 'completed',
             (datetime.now() - timedelta(days=20, hours=22)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=20, hours=21, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
             'Dr. Sarah Johnson', 'Dr. David Kim', 'Neurology',
             'Altered mental status from memory care facility...', 'Baseline dementia, acute change...', 'Likely UTI, awaiting culture...', 'Antibiotics, IV fluids, monitor closely...', 175, 'Confusion admission...', 86, 88, 83),

            ('Lisa Anderson', 'P001241', 'transfer', 'emergent', 'completed',
             (datetime.now() - timedelta(days=22, hours=4)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=22, hours=3, minutes=45)).strftime('%Y-%m-%d %H:%M:%S'),
             'Dr. Sarah Johnson', 'Dr. David Kim', 'Hematology',
             'Sickle cell crisis, severe pain...', 'Known SCD, multiple previous crises...', 'Pain 10/10, requiring IV opioids...', 'Admit for pain management, hydration, heme consult...', 145, 'Sickle cell crisis...', 90, 92, 88),

            ('James Martinez', 'P001242', 'procedure', 'routine', 'completed',
             (datetime.now() - timedelta(days=25, hours=10)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=25, hours=9, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
             'Dr. David Kim', 'Dr. Emily Roberts', 'Oncology',
             'Pre-op for prostate biopsy...', 'Prostate cancer surveillance...', 'PSA rising, concerning for recurrence...', 'Proceed with biopsy, oncology following...', 130, 'Pre-procedure...', 91, 93, 89),

            ('Emily Taylor', 'P001243', 'admission', 'urgent', 'completed',
             (datetime.now() - timedelta(days=28, hours=18)).strftime('%Y-%m-%d %H:%M:%S'),
             (datetime.now() - timedelta(days=28, hours=17, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
             'Dr. Sarah Johnson', 'RN Michael Chen', 'Endocrinology',
             'DKA, blood sugar >500...', 'T1DM, pump malfunction suspected...', 'Ketones present, pH 7.25...', 'DKA protocol, insulin drip, close monitoring...', 165, 'DKA admission...', 88, 90, 85),
        ]

        c.executemany('''
            INSERT INTO handoffs (patient_name, patient_id, handoff_type, priority, status,
                                created_at, completed_at, from_staff, to_staff, specialty,
                                sbar_situation, sbar_background, sbar_assessment, sbar_recommendation,
                                recording_duration, transcription, quality_score, completeness_score, critical_elements_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', handoffs)

        # Insert audit logs for completed handoffs
        c.execute('SELECT id, patient_name, created_at, completed_at FROM handoffs WHERE status="completed"')
        completed_handoffs = c.fetchall()

        audit_entries = []
        for handoff in completed_handoffs:
            handoff_id, patient_name, created_at, completed_at = handoff
            created_dt = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            completed_dt = datetime.strptime(completed_at, '%Y-%m-%d %H:%M:%S') if completed_at else created_dt

            # Created
            audit_entries.append((handoff_id, 'created', 'System', created_at, f'Handoff created for {patient_name}'))
            # Voice uploaded
            audit_entries.append((handoff_id, 'voice_uploaded', 'User', (created_dt + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'), 'Voice recording uploaded'))
            # Transcribed
            audit_entries.append((handoff_id, 'transcribed', 'AI Worker', (created_dt + timedelta(minutes=3)).strftime('%Y-%m-%d %H:%M:%S'), 'Audio transcribed'))
            # SBAR generated
            audit_entries.append((handoff_id, 'sbar_generated', 'AI Worker', (created_dt + timedelta(minutes=4)).strftime('%Y-%m-%d %H:%M:%S'), 'SBAR report generated'))
            # Completed
            audit_entries.append((handoff_id, 'completed', 'User', completed_at, 'Handoff completed'))

        c.executemany('''
            INSERT INTO audit_logs (handoff_id, action, user, timestamp, details)
            VALUES (?, ?, ?, ?, ?)
        ''', audit_entries)

    conn.commit()
    return conn


def get_analytics_data(conn):
    """Get analytics data for dashboard"""
    c = conn.cursor()

    # Handoffs by type
    c.execute('''
        SELECT handoff_type, COUNT(*) as count
        FROM handoffs
        WHERE status = 'completed'
        GROUP BY handoff_type
        ORDER BY count DESC
    ''')
    handoffs_by_type = c.fetchall()

    # Handoffs by priority
    c.execute('''
        SELECT priority, COUNT(*) as count
        FROM handoffs
        WHERE status = 'completed'
        GROUP BY priority
    ''')
    handoffs_by_priority = c.fetchall()

    # Handoffs by specialty
    c.execute('''
        SELECT specialty, COUNT(*) as count
        FROM handoffs
        WHERE status = 'completed' AND specialty IS NOT NULL
        GROUP BY specialty
        ORDER BY count DESC
        LIMIT 10
    ''')
    handoffs_by_specialty = c.fetchall()

    # Daily handoffs (last 30 days)
    c.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM handoffs
        WHERE created_at >= date('now', '-30 days')
        GROUP BY DATE(created_at)
        ORDER BY date
    ''')
    daily_handoffs = c.fetchall()

    # Average quality scores
    c.execute('''
        SELECT
            AVG(quality_score) as avg_quality,
            AVG(completeness_score) as avg_completeness,
            AVG(critical_elements_score) as avg_critical
        FROM handoffs
        WHERE status = 'completed' AND quality_score IS NOT NULL
    ''')
    avg_scores = c.fetchone()

    # Average duration
    c.execute('''
        SELECT AVG(recording_duration) as avg_duration
        FROM handoffs
        WHERE status = 'completed' AND recording_duration IS NOT NULL
    ''')
    avg_duration = c.fetchone()[0]

    return {
        'handoffs_by_type': handoffs_by_type,
        'handoffs_by_priority': handoffs_by_priority,
        'handoffs_by_specialty': handoffs_by_specialty,
        'daily_handoffs': daily_handoffs,
        'avg_quality': avg_scores[0] if avg_scores[0] else 0,
        'avg_completeness': avg_scores[1] if avg_scores[1] else 0,
        'avg_critical': avg_scores[2] if avg_scores[2] else 0,
        'avg_duration': avg_duration if avg_duration else 0
    }


def search_handoffs(conn, query='', handoff_type='all', priority='all', status='all', specialty='all'):
    """Search and filter handoffs"""
    c = conn.cursor()

    sql = 'SELECT * FROM handoffs WHERE 1=1'
    params = []

    if query:
        sql += ' AND (patient_name LIKE ? OR patient_id LIKE ? OR from_staff LIKE ? OR to_staff LIKE ?)'
        search_term = f'%{query}%'
        params.extend([search_term, search_term, search_term, search_term])

    if handoff_type != 'all':
        sql += ' AND handoff_type = ?'
        params.append(handoff_type)

    if priority != 'all':
        sql += ' AND priority = ?'
        params.append(priority)

    if status != 'all':
        sql += ' AND status = ?'
        params.append(status)

    if specialty != 'all':
        sql += ' AND specialty = ?'
        params.append(specialty)

    sql += ' ORDER BY created_at DESC'

    c.execute(sql, params)
    return c.fetchall()
