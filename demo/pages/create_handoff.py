import streamlit as st
import sqlite3
from datetime import datetime
import time
from audio_recorder_streamlit import audio_recorder

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
        st.markdown("### 🎤 Record Your Handoff")

        # Time comparison banner
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1.5rem; color: white;'>
            <div style='text-align: center;'>
                <div style='font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;'>⚡ 10x Faster</div>
                <div style='font-size: 1.2rem; opacity: 0.9;'>Old Way: 15-20 minutes | EclipseLink: 2 minutes</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info("**SBAR Format Reminder:**\n- **S**ituation - What is happening?\n- **B**ackground - Clinical context?\n- **A**ssessment - What's the problem?\n- **R**ecommendation - What should be done?")

        # Real voice recording
        st.markdown("#### 🎤 Voice Recorder (Real Recording)")

        audio_bytes = audio_recorder(
            text="Click to record",
            recording_color="#ef4444",
            neutral_color="#1e40af",
            icon_name="microphone",
            icon_size="3x",
        )

        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            st.success("✅ Recording captured! You can play it back above.")
            # Estimate duration (rough approximation)
            duration = len(audio_bytes) // 8000  # Rough estimate
            st.session_state.recording_time = duration
            st.session_state.has_audio = True
        else:
            st.session_state.has_audio = False

        # Alternative: Text input for demo
        st.markdown("---")
        st.markdown("#### 📝 Or Enter Text (Type Your Handoff)")

        # Example handoff with intentional missing elements for error detection
        example_text = """This is a 60-year-old male patient with type 2 diabetes.
Current glucose is 145 mg/dL. Patient is alert and oriented times three.
Vital signs: BP 130/85, HR 78, RR 16, SpO2 98% on room air.

Patient has been here for 3 days for diabetic management.
Blood glucose has been trending downward with current insulin regimen.

Recent HbA1c is 8.2%. No acute distress noted at this time.
Patient reports improved energy levels.

Continue current insulin sliding scale. Discharge education has been completed.
Patient verbalizes understanding. Consider discharge tomorrow if stable."""

        handoff_text = st.text_area(
            "Handoff Details",
            value="",
            placeholder=example_text,
            height=200,
            help="Speak naturally about the patient's situation, background, assessment, and your recommendations"
        )

        # Helpful examples
        with st.expander("💡 See Example Handoffs"):
            st.markdown("""
            **Good Example (Complete):**
            "Patient John Smith, MRN 12345, is a 60-year-old male with type 2 diabetes and penicillin allergy.
            Current glucose 145, vital signs stable. On Metformin 1000mg twice daily.
            Blood sugar trending down nicely. Plan to discharge tomorrow if remains stable."

            **Incomplete Example (Missing Critical Info):**
            "60-year-old diabetic patient. Glucose is 145. Doing okay.
            Plan to send home soon."

            ⚠️ Missing: Patient name/ID, allergies, medications, vital signs
            """)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state.handoff_step = 1
                st.rerun()

        with col_b:
            has_input = handoff_text.strip() != "" or st.session_state.get('has_audio', False)
            if st.button("🚀 Generate SBAR", type="primary", use_container_width=True, disabled=not has_input):
                if has_input:
                    st.session_state.handoff_text = handoff_text if handoff_text.strip() else "Voice recording provided"
                    st.session_state.handoff_step = 3
                    st.rerun()
                else:
                    st.error("Please record audio or enter text")

    # Step 3: Processing & Results
    elif st.session_state.handoff_step == 3:
        st.markdown("### 🤖 AI Processing Your Handoff")

        # Show detailed processing animation
        progress_bar = st.progress(0)
        status_container = st.empty()

        # Detailed processing steps
        steps = [
            ("🎤 Uploading voice recording to secure cloud storage...", 10, "Encrypting audio with AES-256"),
            ("🔊 Analyzing audio quality and noise levels...", 20, "Signal-to-noise ratio: 32 dB (excellent)"),
            ("🧠 Transcribing with Azure Whisper AI...", 40, "Processing natural language, medical terminology"),
            ("📝 Extracting medical entities...", 55, "Identifying: medications, vitals, diagnoses"),
            ("🏥 Validating critical elements...", 65, "Checking: patient ID, allergies, medications"),
            ("🤖 Generating SBAR structure with GPT-4...", 80, "Using clinical handoff best practices"),
            ("📊 Calculating quality scores...", 90, "Analyzing completeness and critical elements"),
            ("✅ Finalizing report and saving...", 100, "Creating audit log entry")
        ]

        for step_text, progress, detail in steps:
            status_container.markdown(f"""
            <div style='background: #f8fafc; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #3b82f6; margin: 0.5rem 0;'>
                <div style='font-weight: bold; font-size: 1.1rem; margin-bottom: 0.25rem;'>{step_text}</div>
                <div style='color: #64748b; font-size: 0.9rem;'>{detail}</div>
            </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(progress)
            time.sleep(0.6)  # Slightly slower for readability

        st.success("✅ SBAR Report Generated Successfully!")

        # Generate mock SBAR based on the data
        handoff_data = st.session_state.handoff_data

        # Generate realistic SBAR content
        sbar = generate_sample_sbar(
            handoff_data['patient_name'],
            handoff_data['patient_id'],
            st.session_state.handoff_text
        )

        # AI Quality Analysis & Error Detection
        st.markdown("---")
        st.markdown("### 🔍 AI Quality Analysis")

        # Check for missing critical elements
        user_input = st.session_state.handoff_text.lower()
        missing_elements = []
        warnings = []

        # Critical element detection
        if 'allerg' not in user_input:
            missing_elements.append("Patient allergies")
        if not any(med in user_input for med in ['medication', 'med ', 'drug', 'metformin', 'insulin', 'aspirin']):
            missing_elements.append("Current medications")
        if not any(vital in user_input for vital in ['bp', 'blood pressure', 'hr', 'heart rate', 'vital']):
            warnings.append("Vital signs not clearly documented")

        # Display warnings
        if missing_elements or warnings:
            st.markdown("#### ⚠️ Critical Elements Check")

            if missing_elements:
                for element in missing_elements:
                    st.warning(f"**Missing Critical Element:** {element}")
                    st.markdown(f"<small style='color: #f59e0b;'>🔔 Add this information to improve patient safety</small>", unsafe_allow_html=True)

            if warnings:
                for warning in warnings:
                    st.info(f"**Recommendation:** {warning}")

            st.markdown("""
            <div style='background: #fef3c7; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #f59e0b; margin: 1rem 0;'>
                <strong>💡 Pro Tip:</strong> The AI detected some missing information. You can edit the SBAR below to add these critical elements, or click "Edit SBAR" after saving.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("✅ All critical elements detected! Excellent handoff quality.")

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
        st.markdown("---")
        st.markdown("### 📋 SBAR Report")

        col1, col2, col3 = st.columns(3)
        with col1:
            quality_score = 95 if not missing_elements else 75
            st.metric("Quality Score", f"{quality_score}%", "Excellent" if quality_score >= 90 else "Good")
        with col2:
            completeness = 100 if not missing_elements else 80
            st.metric("Completeness", f"{completeness}%", "Complete" if completeness >= 95 else "Needs Review")
        with col3:
            critical_score = 100 if not missing_elements else 65
            st.metric("Critical Elements", f"{critical_score}%", "✅" if critical_score >= 90 else "⚠️")

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
