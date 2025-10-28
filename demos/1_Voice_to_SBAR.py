"""
EclipseLink AI - Voice-to-SBAR Interactive Demo
Demonstrates the core functionality of converting voice recordings to structured SBAR reports
"""

import streamlit as st
import time
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Voice-to-SBAR Demo - EclipseLink AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand colors
PEACOCK_TEAL = "#1a9b8e"
PHOENIX_GOLD = "#f4c430"
LUNAR_BLUE = "#2c3e50"
ECLIPSE_NAVY = "#1a2332"

# Custom CSS
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, {PEACOCK_TEAL} 0%, {LUNAR_BLUE} 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }}
    .sbar-section {{
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid {PEACOCK_TEAL};
        margin-bottom: 1rem;
    }}
    .metric-card {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }}
    .status-badge {{
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }}
    .status-processing {{
        background-color: {PHOENIX_GOLD};
        color: {ECLIPSE_NAVY};
    }}
    .status-completed {{
        background-color: {PEACOCK_TEAL};
        color: white;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎙️ Voice-to-SBAR Demo</h1>
    <p style="font-size: 1.2rem; margin: 0;">Transform voice recordings into structured SBAR reports in seconds</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'processing_stage' not in st.session_state:
    st.session_state.processing_stage = 'upload'
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'sbar_report' not in st.session_state:
    st.session_state.sbar_report = {}

# Sidebar - Demo Controls
with st.sidebar:
    st.image("https://img.shields.io/badge/EclipseLink-AI-1a9b8e?style=for-the-badge", use_container_width=True)
    st.markdown("---")
    st.markdown("### Demo Controls")

    demo_scenario = st.selectbox(
        "Select Scenario",
        ["Post-Surgery ICU Transfer", "Emergency Department Admission", "End of Shift Handoff", "Custom Recording"]
    )

    use_sample_data = st.checkbox("Use Sample Data", value=True, help="Use pre-populated sample data for quick demo")

    st.markdown("---")
    st.markdown("### About This Demo")
    st.info("""
    This interactive demo showcases EclipseLink AI's core feature:
    - Voice recording upload
    - Real-time transcription
    - AI-powered SBAR generation
    - Interactive editing
    """)

    if st.button("Reset Demo", type="secondary"):
        st.session_state.processing_stage = 'upload'
        st.session_state.transcript = ""
        st.session_state.sbar_report = {}
        st.rerun()

# Main content area
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Avg. Processing Time", "28 sec")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Transcription Accuracy", "97%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Time Saved vs Manual", "4.5 min")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Step 1: Voice Recording Upload
st.markdown("## Step 1: Voice Recording")

if st.session_state.processing_stage == 'upload':
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("### Upload or Record Audio")

        upload_method = st.radio(
            "Choose method:",
            ["Upload Audio File", "Record New Audio (Simulated)"],
            horizontal=True
        )

        if upload_method == "Upload Audio File":
            uploaded_file = st.file_uploader(
                "Choose an audio file",
                type=['mp3', 'wav', 'm4a', 'ogg'],
                help="Supported formats: MP3, WAV, M4A, OGG"
            )

            if uploaded_file:
                st.audio(uploaded_file)
                st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size/1024:.1f} KB)")
        else:
            st.info("🎤 Click the button below to simulate recording")
            if st.button("🔴 Start Recording (Simulated)", type="primary", use_container_width=True):
                with st.spinner("Recording... (3-5 minutes simulated)"):
                    time.sleep(2)
                st.success("Recording completed! Duration: 4:32")

        if st.button("▶️ Process Recording", type="primary", use_container_width=True, disabled=not (uploaded_file if upload_method == "Upload Audio File" else False)):
            st.session_state.processing_stage = 'transcribing'
            st.rerun()

    with col_right:
        st.markdown("### Recording Guidelines")
        st.markdown("""
        **For best results:**
        - 🎯 Speak clearly and at normal pace
        - 🔇 Minimize background noise
        - ⏱️ Typical duration: 3-5 minutes
        - 📋 Include patient details, situation, background, assessment, recommendations

        **Supported formats:**
        - MP3, WAV, M4A, OGG
        - Max size: 50 MB
        """)

# Step 2: Transcription
elif st.session_state.processing_stage == 'transcribing':
    st.markdown("## Step 2: Transcription")

    progress_bar = st.progress(0)
    status_text = st.empty()

    # Simulate transcription process
    stages = [
        ("Uploading to secure cloud storage...", 0.2),
        ("Processing audio with Azure OpenAI Whisper...", 0.5),
        ("Applying medical terminology corrections...", 0.8),
        ("Finalizing transcription...", 1.0)
    ]

    for stage_text, progress in stages:
        status_text.markdown(f'<span class="status-badge status-processing">⏳ {stage_text}</span>', unsafe_allow_html=True)
        progress_bar.progress(progress)
        time.sleep(1)

    # Sample transcript based on scenario
    transcripts = {
        "Post-Surgery ICU Transfer": """
This is a handoff for patient Sarah Johnson, 68-year-old female, medical record number
MRN-123456. She just came out of a four-hour coronary artery bypass graft surgery.

Situation: Post-op day zero CABG times four. She's currently stable but needs close
monitoring for the next 24 hours in the ICU.

Background: Patient has a history of coronary artery disease, hypertension, and type 2
diabetes. She was admitted three days ago with unstable angina. Cardiac catheterization
showed 90% stenosis in the LAD and significant disease in other vessels.

Assessment: Currently intubated and sedated on propofol at 20 mics per kig per minute.
Vital signs are stable - blood pressure 118 over 72, heart rate 78 and regular, oxygen
saturation 98% on 40% FiO2. Chest tubes are in place draining serosanguinous fluid,
about 150 mLs in the last hour. Labs drawn in the OR showed hemoglobin of 9.8, which
we're monitoring closely.

Recommendation: Continue current sedation, monitor chest tube output every hour, watch
for any signs of bleeding or cardiac tamponade. Plan to extubate in the morning if she
remains stable overnight. Cardiac enzymes and EKG scheduled for 6 AM. She has an
epidural for pain management once extubated.
""",
        "Emergency Department Admission": """
This is for Michael Chen, 45-year-old male, MRN-789012, presenting to the ED via EMS
with chest pain.

Situation: Patient called 911 for sudden onset chest pain that started 2 hours ago while
mowing the lawn. Pain is substernal, 8 out of 10, radiating to left arm and jaw.

Background: Past medical history significant for smoking one pack per day for 25 years,
family history of early MI - father had heart attack at age 50. No prior cardiac history
but has been hypertensive, not well controlled on medications.

Assessment: Currently chest pain is 6 out of 10 after morphine and nitro. EKG shows
ST elevations in leads two, three, and AVF consistent with inferior wall MI. Troponin
elevated at 2.4. Blood pressure initially 160 over 95, now 135 over 82. Heart rate 92,
regular rhythm. Already given aspirin, plavix loading dose, heparin bolus and drip started.

Recommendation: Activating cath lab now for emergent cardiac catheterization. Patient
and family aware and consented. Will need ICU bed post-procedure. Cardiology fellow
Dr. Williams is on the way.
""",
        "End of Shift Handoff": """
Quick handoff for my patients before end of shift.

First is room 412, Jennifer Martinez, 32-year-old female with preterm labor. She's 32
weeks pregnant, came in with contractions every 5 minutes. We've given her magnesium
sulfate and the contractions have spaced out to every 15 minutes. Fetal monitoring looks
good, baby's heart rate in the 140s. OB is aware and checking back in an hour.

Room 415, Robert Thompson, 72-year-old male with pneumonia. He's on day 2 of
ceftriaxone and azithromycin. Improving but still needs oxygen at 3 liters to keep sats
above 92. Got his morning breathing treatment. Chest X-ray this morning showed some
improvement. Should be ready to transition to oral antibiotics tomorrow if he continues
improving.

Room 418, Lisa Anderson, 58-year-old post-op cholecystectomy. Surgery was yesterday
morning, laparoscopic. Doing well, tolerating regular diet, pain controlled with oral meds.
Thinking she can discharge tomorrow morning if surgical team agrees on rounds.

That's all three. Let me know if you need anything else.
"""
    }

    st.session_state.transcript = transcripts.get(demo_scenario, transcripts["Post-Surgery ICU Transfer"])

    status_text.markdown(f'<span class="status-badge status-completed">✅ Transcription Complete!</span>', unsafe_allow_html=True)
    time.sleep(1)

    st.session_state.processing_stage = 'transcript_review'
    st.rerun()

# Step 3: Review Transcript
elif st.session_state.processing_stage == 'transcript_review':
    st.markdown("## Step 3: Review Transcript")

    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.markdown("### Generated Transcript")
        st.info("Review and edit the transcript before generating the SBAR report. The AI has already corrected common medical terminology.")

        edited_transcript = st.text_area(
            "Transcript",
            value=st.session_state.transcript,
            height=400,
            help="Edit any errors in the transcription"
        )

        st.session_state.transcript = edited_transcript

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("⬅️ Back to Upload", use_container_width=True):
                st.session_state.processing_stage = 'upload'
                st.rerun()
        with col_btn2:
            if st.button("Generate SBAR Report ➡️", type="primary", use_container_width=True):
                st.session_state.processing_stage = 'generating_sbar'
                st.rerun()

    with col_right:
        st.markdown("### Accuracy Metrics")
        st.metric("Word Accuracy", "97.3%", "2.1%")
        st.metric("Medical Terms", "142 detected")
        st.metric("Auto-corrections", "8 applied")

        st.markdown("### Common Corrections")
        st.markdown("""
        - ✅ "mics" → "mcg"
        - ✅ "times four" → "x4"
        - ✅ "cath lab" → "catheterization lab"
        - ✅ "sats" → "saturations"
        """)

# Step 4: Generate SBAR
elif st.session_state.processing_stage == 'generating_sbar':
    st.markdown("## Step 4: Generating SBAR Report")

    progress_bar = st.progress(0)
    status_text = st.empty()

    stages = [
        ("Analyzing transcript with GPT-4...", 0.25),
        ("Extracting clinical information...", 0.5),
        ("Structuring SBAR format...", 0.75),
        ("Finalizing report...", 1.0)
    ]

    for stage_text, progress in stages:
        status_text.markdown(f'<span class="status-badge status-processing">⏳ {stage_text}</span>', unsafe_allow_html=True)
        progress_bar.progress(progress)
        time.sleep(1)

    # Generate SBAR based on scenario
    sbar_reports = {
        "Post-Surgery ICU Transfer": {
            "patient_name": "Sarah Johnson",
            "mrn": "MRN-123456",
            "age": 68,
            "situation": """Post-operative day 0 status-post coronary artery bypass graft (CABG) x4. Patient transferred to ICU for close monitoring following 4-hour surgical procedure. Currently stable but requires intensive monitoring for the next 24 hours.""",
            "background": """68-year-old female with significant past medical history of:
• Coronary artery disease
• Hypertension
• Type 2 diabetes mellitus

Admitted 3 days ago with unstable angina. Cardiac catheterization revealed 90% stenosis in left anterior descending artery (LAD) with significant disease in additional vessels, necessitating surgical intervention.""",
            "assessment": """AIRWAY/BREATHING:
• Currently intubated and mechanically ventilated
• FiO2: 40%
• Oxygen saturation: 98%
• Sedation: Propofol 20 mcg/kg/min

CARDIOVASCULAR:
• Blood pressure: 118/72 mmHg
• Heart rate: 78 bpm, regular rhythm
• Chest tubes in place with serosanguinous drainage: 150 mL in past hour

LABORATORY:
• Hemoglobin: 9.8 g/dL (being monitored)
• Additional OR labs within normal parameters

PAIN MANAGEMENT:
• Epidural catheter in place for post-extubation pain control""",
            "recommendation": """IMMEDIATE ACTIONS:
• Continue current sedation regimen
• Monitor chest tube output hourly
• Watch for signs of bleeding or cardiac tamponade

PLANNED INTERVENTIONS:
• Extubation planned for tomorrow morning if patient remains stable
• Cardiac enzymes and 12-lead EKG scheduled for 0600
• Activate epidural for pain management post-extubation

MONITORING PARAMETERS:
• Vital signs every 15 minutes for first 4 hours, then hourly
• Chest tube output every hour
• Continuous cardiac monitoring
• Hourly neurological assessments once sedation lightened"""
        },
        "Emergency Department Admission": {
            "patient_name": "Michael Chen",
            "mrn": "MRN-789012",
            "age": 45,
            "situation": """45-year-old male presenting via EMS with acute chest pain consistent with ST-elevation myocardial infarction (STEMI). Symptom onset 2 hours ago during physical activity (lawn mowing). Currently experiencing substernal chest pain 6/10 (reduced from 8/10 after interventions).""",
            "background": """Significant cardiac risk factors:
• 25 pack-year smoking history (1 PPD x 25 years)
• Uncontrolled hypertension on medications
• Family history: Father with MI at age 50
• No prior cardiac history

Presenting symptoms: Substernal chest pain radiating to left arm and jaw, initially 8/10 severity.""",
            "assessment": """CARDIOVASCULAR:
• EKG: ST-elevations in leads II, III, AVF → Inferior wall MI
• Troponin: 2.4 (elevated)
• Blood pressure: 135/82 mmHg (initially 160/95 mmHg)
• Heart rate: 92 bpm, regular rhythm

CURRENT TREATMENT:
• Aspirin administered
• Plavix loading dose given
• Heparin bolus + continuous drip initiated
• Morphine for pain control
• Nitroglycerin administered
• Current pain level: 6/10

RESPONSE TO TREATMENT:
• Blood pressure improved with interventions
• Pain partially controlled
• Hemodynamically stable""",
            "recommendation": """URGENT INTERVENTIONS:
• Cath lab activated for emergent cardiac catheterization
• Patient and family consented and informed

CONSULTATIONS:
• Cardiology fellow Dr. Williams en route

POST-PROCEDURE PLANNING:
• ICU bed reserved for post-catheterization care
• Continue antiplatelet therapy
• Monitor for reperfusion arrhythmias

FAMILY COMMUNICATION:
• Family present and updated on plan
• Informed of STEMI diagnosis and emergent intervention"""
        }
    }

    default_sbar = sbar_reports.get(demo_scenario, sbar_reports["Post-Surgery ICU Transfer"])
    st.session_state.sbar_report = default_sbar

    status_text.markdown(f'<span class="status-badge status-completed">✅ SBAR Report Generated!</span>', unsafe_allow_html=True)
    time.sleep(1)

    st.session_state.processing_stage = 'sbar_review'
    st.rerun()

# Step 5: Review and Edit SBAR
elif st.session_state.processing_stage == 'sbar_review':
    st.markdown("## Step 5: Review & Edit SBAR Report")

    sbar = st.session_state.sbar_report

    # Patient Info Header
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Patient Name", value=sbar["patient_name"], key="patient_name")
    with col2:
        st.text_input("MRN", value=sbar["mrn"], key="mrn")
    with col3:
        st.number_input("Age", value=sbar["age"], key="age")
    with col4:
        st.selectbox("Gender", ["Female", "Male", "Other"], key="gender")

    st.markdown("---")

    # SBAR Sections
    st.markdown('<div class="sbar-section">', unsafe_allow_html=True)
    st.markdown("### 🔴 Situation")
    situation = st.text_area(
        "Current clinical situation and reason for communication",
        value=sbar["situation"],
        height=120,
        key="situation"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sbar-section">', unsafe_allow_html=True)
    st.markdown("### 📋 Background")
    background = st.text_area(
        "Relevant medical history and context",
        value=sbar["background"],
        height=150,
        key="background"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sbar-section">', unsafe_allow_html=True)
    st.markdown("### 🔍 Assessment")
    assessment = st.text_area(
        "Clinical findings and current status",
        value=sbar["assessment"],
        height=200,
        key="assessment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sbar-section">', unsafe_allow_html=True)
    st.markdown("### ✅ Recommendation")
    recommendation = st.text_area(
        "Suggested actions and interventions",
        value=sbar["recommendation"],
        height=200,
        key="recommendation"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Action buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("⬅️ Back to Transcript", use_container_width=True):
            st.session_state.processing_stage = 'transcript_review'
            st.rerun()

    with col2:
        if st.button("📄 Export to PDF", use_container_width=True):
            st.success("PDF exported successfully!")
            st.download_button(
                "⬇️ Download PDF",
                data="Sample SBAR Report PDF content",
                file_name=f"SBAR_{sbar['mrn']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )

    with col3:
        if st.button("🏥 Send to EHR", use_container_width=True):
            with st.spinner("Connecting to EHR system..."):
                time.sleep(2)
            st.success("SBAR report sent to EHR successfully!")

    with col4:
        if st.button("✅ Approve & Complete", type="primary", use_container_width=True):
            st.session_state.processing_stage = 'completed'
            st.rerun()

# Step 6: Completion
elif st.session_state.processing_stage == 'completed':
    st.markdown("## ✅ Handoff Complete!")

    st.success("🎉 SBAR report has been approved and saved to the system.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Time", "32 seconds", "-4.5 min vs manual")
    with col2:
        st.metric("Processing Steps", "5 completed")
    with col3:
        st.metric("Accuracy Score", "98.5%")

    st.markdown("---")

    st.markdown("### What's Next?")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        **Report has been:**
        - ✅ Saved to patient record
        - ✅ Logged in audit trail
        - ✅ Notifications sent to team
        - ✅ Available in EHR
        """)

    with col_b:
        st.markdown("""
        **You can now:**
        - 📱 View on mobile app
        - 📊 See analytics dashboard
        - 👥 Share with care team
        - 📋 Generate another handoff
        """)

    st.markdown("---")

    if st.button("🔄 Start New Handoff", type="primary", use_container_width=True):
        st.session_state.processing_stage = 'upload'
        st.session_state.transcript = ""
        st.session_state.sbar_report = {}
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>EclipseLink AI™</strong> - Transforming Clinical Handoffs with AI</p>
    <p style="font-size: 0.9rem;">© 2025 Rohimaya Health AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
