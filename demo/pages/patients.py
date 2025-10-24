"""Patient Management for EclipseLink AI Demo"""
import streamlit as st
import sqlite3
from datetime import datetime

def show():
    """Show patient management page"""
    st.markdown("<div class='main-header'>👥 Patient Management</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Manage patient records and view handoff history</div>", unsafe_allow_html=True)

    # Get database connection
    conn = sqlite3.connect('demo_data.db', check_same_thread=False)
    c = conn.cursor()

    # Search bar
    search_query = st.text_input("🔍 Search patients", placeholder="Search by name, ID, or condition...")

    # Get patients
    if search_query:
        c.execute('''
            SELECT * FROM patients
            WHERE name LIKE ? OR patient_id LIKE ? OR conditions LIKE ?
            ORDER BY name
        ''', (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
    else:
        c.execute('SELECT * FROM patients ORDER BY name')

    patients = c.fetchall()

    st.markdown(f"### All Patients ({len(patients)} total)")

    if patients:
        # Display patients as cards
        for patient in patients:
            patient_id_pk, patient_id, name, dob, gender, blood_type, allergies, conditions, medications, emergency, insurance, created_at = patient

            # Get handoff count for this patient
            c.execute('SELECT COUNT(*) FROM handoffs WHERE patient_id = ?', (patient_id,))
            handoff_count = c.fetchone()[0]

            # Calculate age
            if dob:
                birth_date = datetime.strptime(dob, '%Y-%m-%d')
                age = (datetime.now() - birth_date).days // 365
            else:
                age = 'Unknown'

            # Create patient card
            with st.expander(f"**{name}** • {patient_id} • {age} y/o {gender}", expanded=False):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"""
                    **Demographics:**
                    - **DOB:** {dob}
                    - **Gender:** {gender}
                    - **Blood Type:** {blood_type}

                    **Insurance:**
                    - {insurance}

                    **Emergency Contact:**
                    - {emergency}
                    """)

                with col2:
                    st.markdown(f"""
                    **Allergies:**
                    <div style='background: #fef2f2; padding: 0.5rem; border-radius: 0.5rem; border-left: 4px solid #ef4444; margin: 0.5rem 0;'>
                        ⚠️ {allergies}
                    </div>

                    **Conditions:**
                    {conditions}

                    **Current Medications:**
                    {medications}
                    """, unsafe_allow_html=True)

                st.markdown("---")

                # Show patient's handoff history
                st.markdown(f"**Handoff History** ({handoff_count} total)")

                c.execute('''
                    SELECT id, handoff_type, priority, status, created_at, from_staff, to_staff
                    FROM handoffs
                    WHERE patient_id = ?
                    ORDER BY created_at DESC
                    LIMIT 5
                ''', (patient_id,))
                patient_handoffs = c.fetchall()

                if patient_handoffs:
                    for handoff in patient_handoffs:
                        h_id, h_type, h_priority, h_status, h_created, h_from, h_to = handoff

                        status_colors = {
                            'completed': '#10b981',
                            'active': '#3b82f6',
                            'pending': '#f59e0b'
                        }
                        priority_icons = {
                            'routine': '🟢',
                            'urgent': '🟡',
                            'emergent': '🔴'
                        }

                        col_a, col_b, col_c = st.columns([3, 1, 1])
                        with col_a:
                            st.markdown(f"""
                            <div style='background: #f8fafc; padding: 0.75rem; margin: 0.25rem 0; border-radius: 0.5rem; border-left: 4px solid {status_colors.get(h_status, "#64748b")};'>
                                <strong>{h_type.replace('_', ' ').title()}</strong> {priority_icons.get(h_priority, '⚪')}
                                <br><small style='color: #64748b;'>{h_from} → {h_to} • {h_created}</small>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_b:
                            if st.button("View", key=f"view_patient_handoff_{h_id}", use_container_width=True):
                                st.session_state.selected_handoff = h_id
                                st.session_state.page = 'view_handoff'
                                st.rerun()
                        with col_c:
                            st.markdown(f"<div style='text-align: center; padding: 0.5rem;'>{h_status}</div>", unsafe_allow_html=True)

                    if handoff_count > 5:
                        st.info(f"Showing 5 most recent. {handoff_count - 5} more handoffs in history.")
                else:
                    st.info("No handoffs for this patient yet.")

                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📋 New Handoff", key=f"new_handoff_{patient_id}", use_container_width=True):
                        st.session_state.selected_patient = patient_id
                        st.session_state.page = 'create_handoff'
                        st.rerun()
                with col2:
                    if st.button("📝 Edit Patient", key=f"edit_{patient_id}", use_container_width=True):
                        st.info("Edit functionality (Demo)")
                with col3:
                    if st.button("📊 Patient Report", key=f"report_{patient_id}", use_container_width=True):
                        st.info("Report generation (Demo)")

    else:
        st.info("No patients found. Try a different search term.")

    # Add new patient button
    st.markdown("---")
    if st.button("➕ Add New Patient", type="primary", use_container_width=True):
        show_add_patient_modal(conn)

    conn.close()


def show_add_patient_modal(conn):
    """Show add patient form"""
    st.markdown("### Add New Patient")

    with st.form("add_patient_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Patient Name *", placeholder="John Doe")
            patient_id = st.text_input("Patient ID *", placeholder="P001XXX")
            dob = st.date_input("Date of Birth *")
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
            blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])

        with col2:
            allergies = st.text_area("Allergies", placeholder="List any known allergies...")
            conditions = st.text_area("Medical Conditions", placeholder="List chronic conditions...")
            medications = st.text_area("Current Medications", placeholder="List current medications...")
            emergency_contact = st.text_input("Emergency Contact", placeholder="Name: Phone")
            insurance = st.text_input("Insurance", placeholder="Insurance provider and plan")

        submit = st.form_submit_button("Add Patient", type="primary", use_container_width=True)

        if submit:
            if name and patient_id and dob:
                c = conn.cursor()
                try:
                    c.execute('''
                        INSERT INTO patients (patient_id, name, date_of_birth, gender, blood_type,
                                            allergies, conditions, medications, emergency_contact, insurance, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (patient_id, name, dob.strftime('%Y-%m-%d'), gender, blood_type,
                         allergies, conditions, medications, emergency_contact, insurance,
                         datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    conn.commit()
                    st.success(f"✅ Patient {name} ({patient_id}) added successfully!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Patient ID {patient_id} already exists. Please use a unique ID.")
            else:
                st.error("Please fill in all required fields (*)")
