import streamlit as st
import sqlite3
from datetime import datetime
import time

def show():
    """Create handoff page"""
    st.markdown("<div class='main-header'>Create New Handoff</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Record a clinical handoff using voice</div>", unsafe_allow_html=True)

    # Get database connection
    conn = sqlite3.connect('demo_data.db', check_same_thread=False)

    # Initialize step if not exists
    if 'handoff_step' not in st.session_state:
        st.session_state.handoff_step = 1

    # Step indicator
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**{'✅' if st.session_state.handoff_step > 1 else '1️⃣'} Basic Information**")
    with col2:
        st.markdown(f"**{'✅' if st.session_state.handoff_step > 2 else '2️⃣' if st.session_state.handoff_step == 2 else '⚪'} Voice Recording**")
    with col3:
        st.markdown(f"**{'3️⃣' if st.session_state.handoff_step == 3 else '⚪'} Processing**")

    st.markdown("---")

    # Step 1: Basic Information
    if st.session_state.handoff_step == 1:
        with st.form("handoff_basic_info"):
            st.markdown("### Handoff Details")

            col1, col2 = st.columns(2)
            with col1:
                patient_name = st.text_input("Patient Name *", placeholder="John Smith")
                patient_id = st.text_input("Patient ID *", placeholder="P001234")

            with col2:
                handoff_type = st.selectbox("Handoff Type",
                    ["shift_change", "transfer", "admission", "discharge", "procedure"])
                priority = st.selectbox("Priority", ["routine", "urgent", "emergent"])

            to_staff = st.text_input("Receiving Staff", placeholder="Dr. Jane Doe")
            notes = st.text_area("Additional Notes (Optional)", placeholder="Any special considerations...")

            if st.form_submit_button("Continue to Recording ➡️", type="primary", use_container_width=True):
                if patient_name and patient_id:
                    st.session_state.handoff_data = {
                        'patient_name': patient_name,
                        'patient_id': patient_id,
                        'handoff_type': handoff_type,
                        'priority': priority,
                        'to_staff': to_staff,
                        'notes': notes
                    }
                    st.session_state.handoff_step = 2
                    st.rerun()
                else:
                    st.error("Please fill in all required fields")

    # Step 2: Voice Recording
    elif st.session_state.handoff_step == 2:
        st.markdown("### Record Your Handoff")

        st.info("**SBAR Format Reminder:**\n- **S**ituation - What is happening?\n- **B**ackground - Clinical context?\n- **A**ssessment - What's the problem?\n- **R**ecommendation - What should be done?")

        # Voice recording simulation
        st.markdown("#### 🎤 Voice Recorder")

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if 'recording' not in st.session_state:
                st.session_state.recording = False
                st.session_state.recording_time = 0

            if not st.session_state.recording:
                if st.button("🎤 Start Recording", type="primary", use_container_width=True):
                    st.session_state.recording = True
                    st.session_state.recording_start = time.time()
                    st.rerun()
            else:
                elapsed = int(time.time() - st.session_state.recording_start)
                st.markdown(f"<div style='text-align: center; font-size: 2rem; font-weight: bold; color: #ef4444;'>⏺ Recording: {elapsed // 60}:{elapsed % 60:02d}</div>", unsafe_allow_html=True)

                if st.button("⏹ Stop Recording", type="secondary", use_container_width=True):
                    st.session_state.recording = False
                    st.session_state.recording_time = elapsed
                    st.success(f"✅ Recording completed! Duration: {elapsed // 60}:{elapsed % 60:02d}")

        # Alternative: Text input for demo
        st.markdown("---")
        st.markdown("#### 📝 Or Enter Text (Demo Mode)")

        handoff_text = st.text_area(
            "Handoff Details",
            placeholder="Example: This is a 60-year-old male patient with type 2 diabetes...",
            height=200,
            help="In demo mode, you can type the handoff details instead of recording"
        )

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state.handoff_step = 1
                st.rerun()

        with col_b:
            if st.button("Generate SBAR ➡️", type="primary", use_container_width=True):
                if handoff_text or st.session_state.get('recording_time', 0) > 0:
                    st.session_state.handoff_text = handoff_text
                    st.session_state.handoff_step = 3
                    st.rerun()
                else:
                    st.error("Please record audio or enter text")

    # Step 3: Processing & Results
    elif st.session_state.handoff_step == 3:
        st.markdown("### Processing Your Handoff")

        # Show processing animation
        with st.spinner(""):
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Simulate processing
            steps = [
                ("Uploading voice recording...", 20),
                ("Transcribing audio with Azure Whisper...", 50),
                ("Generating SBAR with GPT-4...", 80),
                ("Finalizing report...", 100)
            ]

            for step_text, progress in steps:
                status_text.markdown(f"**{step_text}**")
                progress_bar.progress(progress)
                time.sleep(0.5)

        st.success("✅ SBAR Report Generated Successfully!")

        # Generate mock SBAR based on the data
        handoff_data = st.session_state.handoff_data

        # Generate realistic SBAR content
        sbar = generate_sample_sbar(
            handoff_data['patient_name'],
            handoff_data['patient_id'],
            st.session_state.handoff_text
        )

        # Save to database
        c = conn.cursor()
        c.execute('''
            INSERT INTO handoffs (patient_name, patient_id, handoff_type, priority, status,
                                created_at, sbar_situation, sbar_background, sbar_assessment,
                                sbar_recommendation, recording_duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            handoff_data['patient_name'],
            handoff_data['patient_id'],
            handoff_data['handoff_type'],
            handoff_data['priority'],
            'completed',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            sbar['situation'],
            sbar['background'],
            sbar['assessment'],
            sbar['recommendation'],
            st.session_state.get('recording_time', 120)
        ))
        conn.commit()
        handoff_id = c.lastrowid

        # Display SBAR
        st.markdown("### 📋 SBAR Report")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Completeness Score", "95%", "High Quality")
        with col2:
            st.metric("Quality Score", "92%", "Excellent")

        # Situation
        st.markdown("""
        <div class='sbar-section' style='border-left-color: #3b82f6;'>
            <div class='sbar-title'>📘 Situation</div>
            <p>{}</p>
        </div>
        """.format(sbar['situation']), unsafe_allow_html=True)

        # Background
        st.markdown("""
        <div class='sbar-section' style='border-left-color: #10b981;'>
            <div class='sbar-title'>📗 Background</div>
            <p>{}</p>
        </div>
        """.format(sbar['background']), unsafe_allow_html=True)

        # Assessment
        st.markdown("""
        <div class='sbar-section' style='border-left-color: #f59e0b;'>
            <div class='sbar-title'>📙 Assessment</div>
            <p>{}</p>
        </div>
        """.format(sbar['assessment']), unsafe_allow_html=True)

        # Recommendation
        st.markdown("""
        <div class='sbar-section' style='border-left-color: #ef4444;'>
            <div class='sbar-title'>📕 Recommendation</div>
            <p>{}</p>
        </div>
        """.format(sbar['recommendation']), unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Edit SBAR", use_container_width=True):
                st.session_state.selected_handoff = handoff_id
                st.session_state.page = 'view_handoff'
                st.session_state.handoff_step = 1
                st.rerun()

        with col2:
            if st.button("✅ Complete Handoff", type="primary", use_container_width=True):
                st.balloons()
                st.success("🎉 Handoff completed successfully!")
                time.sleep(1)
                st.session_state.handoff_step = 1
                st.session_state.page = 'dashboard'
                st.rerun()

def generate_sample_sbar(patient_name, patient_id, user_input=""):
    """Generate sample SBAR content"""

    # If user provided input, try to extract key info
    if user_input:
        # Simple AI-like processing (in production, use Azure OpenAI)
        situation = f"Patient {patient_name} (ID: {patient_id}). {user_input[:200]}"
    else:
        situation = f"60-year-old patient {patient_name} (ID: {patient_id}) with stable vital signs. Alert and oriented x3. Current blood glucose 145 mg/dL."

    background = f"Past medical history includes type 2 diabetes (10 years), hypertension, and hyperlipidemia. Home medications include Metformin 1000mg BID and Lisinopril 10mg daily. Known allergy to Penicillin (rash). Patient lives at home with spouse, independent with ADLs."

    assessment = "Current vital signs: Temperature 98.6°F, BP 130/85, HR 78, RR 16, SpO2 98% on room air. Blood glucose trending downward with current insulin regimen. No acute distress noted. Patient reports decreased thirst and improved energy levels. Recent labs show HbA1c 8.2%."

    recommendation = "Continue current insulin sliding scale. Diabetes education completed - patient verbalizes understanding. Consider discharge in 24 hours if blood glucose remains stable. Follow-up appointment with endocrinology in 2 weeks. Continue home medications upon discharge."

    return {
        'situation': situation,
        'background': background,
        'assessment': assessment,
        'recommendation': recommendation
    }
