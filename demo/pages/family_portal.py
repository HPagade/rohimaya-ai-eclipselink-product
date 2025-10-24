"""Family Communication Portal for EclipseLink AI Demo"""
import streamlit as st
import sqlite3
from datetime import datetime

def show():
    """Show family communication portal"""
    st.markdown("<div class='main-header'>👨‍👩‍👧 Family Communication Portal</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Stay informed about your loved one's care</div>", unsafe_allow_html=True)

    # Family portal info banner
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1.5rem; color: white;'>
        <div style='text-align: center;'>
            <h3 style='margin: 0 0 0.5rem 0; color: white;'>Welcome to Your Family Portal</h3>
            <p style='margin: 0; opacity: 0.9;'>Access your loved one's care updates in easy-to-understand language</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Family access simulation
    if 'family_patient_id' not in st.session_state:
        st.session_state.family_patient_id = 'P001234'  # Default to John Smith

    # Patient selection (family members typically only see one patient)
    conn = sqlite3.connect('demo_data.db', check_same_thread=False)
    c = conn.cursor()

    c.execute('SELECT DISTINCT patient_id, patient_name FROM handoffs ORDER BY created_at DESC')
    patients = c.fetchall()

    if patients:
        patient_options = {f"{name} ({pid})": pid for pid, name in patients}
        selected = st.selectbox(
            "👤 Select Family Member",
            options=list(patient_options.keys()),
            help="In production, you would only see your authorized family member"
        )
        st.session_state.family_patient_id = patient_options[selected]

    # Get handoffs for this patient
    c.execute('''
        SELECT id, created_at, handoff_type, priority, status,
               sbar_situation, sbar_background, sbar_assessment, sbar_recommendation,
               from_staff, to_staff
        FROM handoffs
        WHERE patient_id = ? AND status = 'completed'
        ORDER BY created_at DESC
    ''', (st.session_state.family_patient_id,))
    handoffs = c.fetchall()

    if not handoffs:
        st.info("No care updates available yet for this family member.")
        conn.close()
        return

    # Care timeline
    st.markdown("### 📅 Care Timeline")

    st.markdown("""
    <div style='background: #e0f2fe; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border-left: 4px solid #0284c7;'>
        <strong>ℹ️ About Care Updates</strong><br>
        <small>These updates are written by your loved one's care team. We've translated them into easy-to-understand language.</small>
    </div>
    """, unsafe_allow_html=True)

    for handoff in handoffs:
        (handoff_id, created_at, handoff_type, priority, status,
         situation, background, assessment, recommendation,
         from_staff, to_staff) = handoff

        # Create expandable card for each handoff
        timestamp = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        time_str = timestamp.strftime('%B %d, %Y at %I:%M %p')

        # Priority icon
        priority_icons = {
            'routine': '🟢 Routine',
            'urgent': '🟡 Needs Attention',
            'emergent': '🔴 Urgent'
        }
        priority_display = priority_icons.get(priority, priority)

        # Handoff type in plain language
        type_translation = {
            'shift_change': 'Care Team Change',
            'transfer': 'Moving to Different Unit',
            'admission': 'Hospital Admission',
            'discharge': 'Going Home',
            'procedure': 'Medical Procedure'
        }
        type_display = type_translation.get(handoff_type, handoff_type)

        with st.expander(f"**{type_display}** - {time_str} ({priority_display})", expanded=False):

            # Translation toggle
            col1, col2 = st.columns([3, 1])
            with col2:
                translate_mode = st.checkbox("📖 Simple Language", value=True, key=f"translate_{handoff_id}")

            if translate_mode and situation:
                st.markdown("### What's Happening")
                translated_situation = translate_to_family_language(situation)
                st.markdown(f"<div style='background: #f0f9ff; padding: 1rem; border-radius: 0.5rem;'>{translated_situation}</div>", unsafe_allow_html=True)

                st.markdown("### Medical History")
                translated_background = translate_to_family_language(background)
                st.markdown(f"<div style='background: #f0fdf4; padding: 1rem; border-radius: 0.5rem;'>{translated_background}</div>", unsafe_allow_html=True)

                st.markdown("### Current Status")
                translated_assessment = translate_to_family_language(assessment)
                st.markdown(f"<div style='background: #fffbeb; padding: 1rem; border-radius: 0.5rem;'>{translated_assessment}</div>", unsafe_allow_html=True)

                st.markdown("### Care Plan")
                translated_recommendation = translate_to_family_language(recommendation)
                st.markdown(f"<div style='background: #fef2f2; padding: 1rem; border-radius: 0.5rem;'>{translated_recommendation}</div>", unsafe_allow_html=True)

            else:
                # Show medical version
                st.markdown("### 📘 Situation")
                st.write(situation)
                st.markdown("### 📗 Background")
                st.write(background)
                st.markdown("### 📙 Assessment")
                st.write(assessment)
                st.markdown("### 📕 Recommendation")
                st.write(recommendation)

            # Care team info
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if from_staff:
                    st.markdown(f"**Previous Nurse/Doctor:** {from_staff}")
            with col2:
                if to_staff:
                    st.markdown(f"**Current Nurse/Doctor:** {to_staff}")

            # Action buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📧 Email to Family", key=f"email_{handoff_id}", use_container_width=True):
                    st.success("✅ Email sent to authorized family members!")
            with col2:
                if st.button("💬 Ask a Question", key=f"question_{handoff_id}", use_container_width=True):
                    st.info("📱 Your care team will respond within 2 hours")
            with col3:
                if st.button("🔔 Request Call", key=f"call_{handoff_id}", use_container_width=True):
                    st.success("✅ Nurse will call you within 30 minutes")

    # Family features
    st.markdown("---")
    st.markdown("### 📱 Family Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='background: #f8fafc; padding: 1.5rem; border-radius: 0.5rem; text-align: center; border: 1px solid #e2e8f0;'>
            <div style='font-size: 2rem;'>📞</div>
            <strong>Contact Nurse</strong><br>
            <small style='color: #64748b;'>Speak directly with care team</small><br>
            <button style='margin-top: 0.5rem; padding: 0.5rem 1rem; background: #3b82f6; color: white; border: none; border-radius: 0.25rem; cursor: pointer;'>Call Now</button>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background: #f8fafc; padding: 1.5rem; border-radius: 0.5rem; text-align: center; border: 1px solid #e2e8f0;'>
            <div style='font-size: 2rem;'>🔔</div>
            <strong>SMS Updates</strong><br>
            <small style='color: #64748b;'>Get text notifications</small><br>
            <button style='margin-top: 0.5rem; padding: 0.5rem 1rem; background: #10b981; color: white; border: none; border-radius: 0.25rem; cursor: pointer;'>Enable SMS</button>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='background: #f8fafc; padding: 1.5rem; border-radius: 0.5rem; text-align: center; border: 1px solid #e2e8f0;'>
            <div style='font-size: 2rem;'>🌐</div>
            <strong>Translate</strong><br>
            <small style='color: #64748b;'>50+ languages</small><br>
            <button style='margin-top: 0.5rem; padding: 0.5rem 1rem; background: #f59e0b; color: white; border: none; border-radius: 0.25rem; cursor: pointer;'>Change Language</button>
        </div>
        """, unsafe_allow_html=True)

    # Educational resources
    st.markdown("---")
    st.markdown("### 📚 Helpful Resources")

    with st.expander("Understanding Medical Terms"):
        st.markdown("""
        **Common Terms Explained:**
        - **Vital Signs:** Heart rate, blood pressure, temperature, oxygen level
        - **PRN:** "As needed" - medication taken when necessary
        - **BID:** Twice per day
        - **NPO:** Nothing by mouth (no food or drink)
        - **Code Status:** Patient preferences for life-saving measures
        """)

    with st.expander("Patient Rights"):
        st.markdown("""
        **Your Rights as a Family Member:**
        - Receive updates about your loved one's condition
        - Ask questions and get clear answers
        - Participate in care planning when appropriate
        - Access medical records (with patient permission)
        - File concerns or complaints
        """)

    with st.expander("Visiting Information"):
        st.markdown("""
        **Visiting Guidelines:**
        - **Visiting Hours:** 8 AM - 8 PM daily
        - **Number of Visitors:** Maximum 2 at a time
        - **Children:** Must be supervised at all times
        - **Safety:** Please sanitize hands before and after visit
        """)

    # Privacy notice
    st.markdown("---")
    st.info("""
    **🔒 Privacy & Security**

    Your access to this portal is secure and HIPAA-compliant. Only authorized family members can view this information.
    All communication is encrypted and logged for security purposes.
    """)

    conn.close()


def translate_to_family_language(medical_text):
    """
    Translate medical jargon to family-friendly language
    In production, this would use GPT-4 with a prompt to simplify medical language
    """
    if not medical_text:
        return "No information available."

    # Simple translation mappings (in production, use AI)
    translations = {
        'acute exacerbation': 'sudden worsening',
        'CHF': 'heart failure',
        'T2DM': 'type 2 diabetes',
        'T1DM': 'type 1 diabetes',
        'hypertension': 'high blood pressure',
        'hyperlipidemia': 'high cholesterol',
        'bilateral': 'on both sides',
        'unilateral': 'on one side',
        'alert and oriented x3': 'awake and aware',
        'oriented times three': 'knows who they are, where they are, and what time it is',
        'ADLs': 'daily activities like eating and bathing',
        'VS': 'vital signs (heart rate, blood pressure, etc.)',
        'BP': 'blood pressure',
        'HR': 'heart rate',
        'RR': 'breathing rate',
        'SpO2': 'oxygen level',
        'RA': 'room air (no oxygen support)',
        'IV': 'through a vein',
        'PO': 'by mouth',
        'PRN': 'as needed',
        'BID': 'twice a day',
        'TID': 'three times a day',
        'QID': 'four times a day',
        'mg': 'milligrams',
        'mcg': 'micrograms',
        'discharge': 'going home from the hospital',
        'admission': 'coming into the hospital',
    }

    family_text = medical_text
    for medical, family in translations.items():
        family_text = family_text.replace(medical, f"{family}")

    # Add friendly prefix
    family_friendly = f"👉 {family_text}"

    return family_friendly
