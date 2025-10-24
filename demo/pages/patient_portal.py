"""Patient Portal for EclipseLink AI Demo"""
import streamlit as st
import sqlite3
from datetime import datetime

def show():
    """Show patient portal - patients view their own handoffs"""
    st.markdown("<div class='main-header'>🏥 My Health Portal</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>View your care information and updates</div>", unsafe_allow_html=True)

    # Patient portal welcome
    st.markdown("""
    <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1.5rem; color: white;'>
        <div style='text-align: center;'>
            <h3 style='margin: 0 0 0.5rem 0; color: white;'>Welcome to Your Health Portal</h3>
            <p style='margin: 0; opacity: 0.9;'>Access your medical information, care updates, and communicate with your care team</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Patient selection (in production, this would be auto-detected from login)
    conn = sqlite3.connect('demo_data.db', check_same_thread=False)
    c = conn.cursor()

    if 'patient_portal_id' not in st.session_state:
        st.session_state.patient_portal_id = 'P001234'

    c.execute('SELECT DISTINCT patient_id, patient_name FROM handoffs ORDER BY patient_name')
    patients = c.fetchall()

    if patients:
        patient_options = {f"{name}": pid for pid, name in patients}
        selected = st.selectbox(
            "👤 Logged in as:",
            options=list(patient_options.keys()),
            help="Demo: Select which patient view to see"
        )
        st.session_state.patient_portal_id = patient_options[selected]

    # Get patient details
    c.execute('''
        SELECT name, patient_id, date_of_birth, gender, blood_type, allergies, conditions, medications
        FROM patients
        WHERE patient_id = ?
    ''', (st.session_state.patient_portal_id,))
    patient_info = c.fetchone()

    # Tab navigation
    tab1, tab2, tab3, tab4 = st.tabs(["📋 My Care Updates", "👤 My Information", "💬 Messages", "📊 My Health Data"])

    with tab1:
        show_care_updates(conn, st.session_state.patient_portal_id)

    with tab2:
        show_patient_info(patient_info)

    with tab3:
        show_messages()

    with tab4:
        show_health_data(conn, st.session_state.patient_portal_id)

    conn.close()


def show_care_updates(conn, patient_id):
    """Show patient's handoffs and care updates"""
    st.markdown("### Recent Care Updates")

    c = conn.cursor()
    c.execute('''
        SELECT id, created_at, handoff_type, priority, from_staff, to_staff,
               sbar_situation, sbar_background, sbar_assessment, sbar_recommendation
        FROM handoffs
        WHERE patient_id = ? AND status = 'completed'
        ORDER BY created_at DESC
        LIMIT 10
    ''', (patient_id,))
    handoffs = c.fetchall()

    if not handoffs:
        st.info("No care updates available yet.")
        return

    for handoff in handoffs:
        (handoff_id, created_at, handoff_type, priority, from_staff, to_staff,
         situation, background, assessment, recommendation) = handoff

        timestamp = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        time_str = timestamp.strftime('%B %d, %Y at %I:%M %p')

        type_names = {
            'shift_change': '🔄 Care Team Change',
            'transfer': '🏥 Unit Transfer',
            'admission': '➡️ Hospital Admission',
            'discharge': '🏠 Discharge',
            'procedure': '🔬 Procedure'
        }
        type_display = type_names.get(handoff_type, handoff_type)

        with st.expander(f"{type_display} - {time_str}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Care Team:** {from_staff} → {to_staff}")
            with col2:
                priority_colors = {'routine': '🟢', 'urgent': '🟡', 'emergent': '🔴'}
                st.markdown(f"**Priority:** {priority_colors.get(priority, '⚪')} {priority.title()}")

            st.markdown("---")

            # Patient-friendly sections
            if situation:
                st.markdown("#### What's Happening")
                st.info(situation)

            if background:
                st.markdown("#### My Medical Background")
                st.success(background)

            if assessment:
                st.markdown("#### Current Status")
                st.warning(assessment)

            if recommendation:
                st.markdown("#### Care Plan")
                st.error(recommendation)

            # Actions
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📄 Download PDF", key=f"pdf_{handoff_id}", use_container_width=True):
                    st.success("✅ PDF downloaded to your device")
            with col2:
                if st.button("✉️ Email Copy", key=f"email_copy_{handoff_id}", use_container_width=True):
                    st.success("✅ Sent to your registered email")
            with col3:
                if st.button("❓ Ask Question", key=f"ask_{handoff_id}", use_container_width=True):
                    st.info("💬 Question submitted to care team")


def show_patient_info(patient_info):
    """Show patient's personal information"""
    if not patient_info:
        st.warning("Patient information not found.")
        return

    name, patient_id, dob, gender, blood_type, allergies, conditions, medications = patient_info

    st.markdown("### My Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        **Demographics**
        - Name: {name}
        - Patient ID: {patient_id}
        - Date of Birth: {dob}
        - Gender: {gender}
        - Blood Type: {blood_type}
        """)

    with col2:
        st.markdown(f"""
        **Contact Information**
        - Email: {name.lower().replace(' ', '.')}@email.com
        - Phone: (555) 123-4567
        - Address: 123 Main St, City, State
        """)

    st.markdown("---")

    # Allergies - Important!
    st.markdown("### ⚠️ My Allergies")
    if allergies:
        st.error(f"**{allergies}**\n\nPlease inform all healthcare providers about your allergies.")
    else:
        st.success("No known allergies on record")

    # Conditions
    st.markdown("### 🏥 My Medical Conditions")
    if conditions:
        for condition in conditions.split(','):
            st.markdown(f"- {condition.strip()}")
    else:
        st.info("No conditions on record")

    # Medications
    st.markdown("### 💊 My Current Medications")
    if medications:
        for med in medications.split(','):
            st.markdown(f"- {med.strip()}")
    else:
        st.info("No medications on record")

    # Edit button
    st.markdown("---")
    if st.button("✏️ Request Update to My Information", use_container_width=True):
        st.success("✅ Request sent to medical records department. They will contact you within 24 hours.")


def show_messages():
    """Show patient messages"""
    st.markdown("### 💬 My Messages")

    # Sample messages
    messages = [
        {
            'from': 'Dr. Sarah Johnson',
            'subject': 'Discharge Instructions',
            'date': 'Oct 24, 2025 2:30 PM',
            'message': 'Please remember to take your medications as prescribed. Follow up with your primary care doctor in 2 weeks. Call if you have any concerns.',
            'unread': True
        },
        {
            'from': 'RN Michael Chen',
            'subject': 'Lab Results Available',
            'date': 'Oct 23, 2025 10:15 AM',
            'message': 'Your recent lab results are now available. Your doctor will review them and contact you if any action is needed.',
            'unread': False
        },
        {
            'from': 'Pharmacy Department',
            'subject': 'Prescription Ready',
            'date': 'Oct 22, 2025 3:45 PM',
            'message': 'Your prescription is ready for pickup at the hospital pharmacy. Hours: 8 AM - 6 PM Monday-Friday.',
            'unread': False
        }
    ]

    for msg in messages:
        status = "🔴 New" if msg['unread'] else "✅ Read"
        with st.expander(f"{status} | **{msg['subject']}** - From: {msg['from']}", expanded=msg['unread']):
            st.markdown(f"**Date:** {msg['date']}")
            st.markdown("---")
            st.write(msg['message'])

            col1, col2 = st.columns(2)
            with col1:
                if st.button("↩️ Reply", key=f"reply_{msg['date']}", use_container_width=True):
                    st.info("Reply feature coming soon!")
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{msg['date']}", use_container_width=True):
                    st.warning("Message deleted")

    # Compose new message
    st.markdown("---")
    st.markdown("### ✉️ Send New Message")

    with st.form("new_message"):
        to = st.selectbox("To:", ["My Care Team", "Dr. Sarah Johnson", "RN Michael Chen", "Billing Department", "Medical Records"])
        subject = st.text_input("Subject:")
        message = st.text_area("Message:", height=150)

        if st.form_submit_button("Send Message", use_container_width=True):
            st.success("✅ Message sent! You'll receive a response within 24 hours.")


def show_health_data(conn, patient_id):
    """Show patient's health trends and data"""
    st.markdown("### 📊 My Health Trends")

    # Sample vital signs data
    import pandas as pd
    import plotly.express as px

    # Generate sample data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    data = {
        'Date': dates,
        'Blood Pressure (Systolic)': [130 + (i % 10) for i in range(30)],
        'Heart Rate': [75 + (i % 15) for i in range(30)],
        'Blood Glucose': [140 + (i % 20) for i in range(30)],
        'Weight (lbs)': [180 - (i * 0.5) for i in range(30)]
    }
    df = pd.DataFrame(data)

    # Blood pressure chart
    st.markdown("#### Blood Pressure Trend")
    fig = px.line(df, x='Date', y='Blood Pressure (Systolic)',
                  title='Your Blood Pressure Over Time',
                  labels={'Blood Pressure (Systolic)': 'Systolic BP (mmHg)'})
    fig.add_hline(y=120, line_dash="dash", line_color="green", annotation_text="Target: <120")
    fig.add_hline(y=140, line_dash="dash", line_color="red", annotation_text="High: >140")
    st.plotly_chart(fig, use_container_width=True)

    # Blood glucose chart
    st.markdown("#### Blood Glucose Trend")
    fig2 = px.line(df, x='Date', y='Blood Glucose',
                   title='Your Blood Glucose Over Time',
                   labels={'Blood Glucose': 'Glucose (mg/dL)'})
    fig2.add_hline(y=100, line_dash="dash", line_color="green", annotation_text="Target: 80-130")
    fig2.add_hline(y=180, line_dash="dash", line_color="red", annotation_text="High: >180")
    st.plotly_chart(fig2, use_container_width=True)

    # Health goals
    st.markdown("---")
    st.markdown("### 🎯 My Health Goals")

    goals = [
        {"goal": "Lower Blood Pressure", "target": "< 120/80", "progress": 75},
        {"goal": "Lose Weight", "target": "170 lbs", "progress": 60},
        {"goal": "Exercise 3x/week", "target": "150 min/week", "progress": 40},
        {"goal": "Improve HbA1c", "target": "< 7.0%", "progress": 85}
    ]

    for goal in goals:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{goal['goal']}** - Target: {goal['target']}")
            st.progress(goal['progress'] / 100)
        with col2:
            st.metric("Progress", f"{goal['progress']}%")

    # Upcoming appointments
    st.markdown("---")
    st.markdown("### 📅 Upcoming Appointments")

    appointments = [
        {"date": "Nov 5, 2025", "time": "10:00 AM", "provider": "Dr. Sarah Johnson", "type": "Follow-up"},
        {"date": "Nov 12, 2025", "time": "2:30 PM", "provider": "Endocrinology", "type": "Diabetes Management"},
    ]

    for appt in appointments:
        st.markdown(f"""
        <div style='background: #f8fafc; padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem; border-left: 4px solid #3b82f6;'>
            <strong>{appt['date']} at {appt['time']}</strong><br>
            {appt['provider']} - {appt['type']}
        </div>
        """, unsafe_allow_html=True)
