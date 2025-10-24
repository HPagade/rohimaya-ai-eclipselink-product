"""View Handoff Details for EclipseLink AI Demo"""
import streamlit as st
import sqlite3
from pdf_export import generate_sbar_pdf
import base64
from datetime import datetime
import plotly.graph_objects as go

def show():
    """View handoff details page"""

    if 'selected_handoff' not in st.session_state:
        st.error("No handoff selected")
        if st.button("⬅️ Back to Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return

    # Get handoff data
    conn = sqlite3.connect('demo_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM handoffs WHERE id=?", (st.session_state.selected_handoff,))
    handoff = c.fetchone()

    if not handoff:
        st.error("Handoff not found")
        return

    # Unpack all fields from new schema
    (handoff_id, patient_name, patient_id, handoff_type, priority, status, created_at, completed_at,
     from_staff, to_staff, specialty, sbar_situation, sbar_background, sbar_assessment,
     sbar_recommendation, recording_duration, transcription, quality_score,
     completeness_score, critical_elements_score) = handoff

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<div class='main-header'>Handoff #{handoff_id} Details</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitle'>{patient_name} • {patient_id}</div>", unsafe_allow_html=True)
    with col2:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

    # Handoff Information
    st.markdown("### 📋 Handoff Information")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Patient", patient_name)
        st.caption(f"ID: {patient_id}")
    with col2:
        st.metric("Type", handoff_type.replace('_', ' ').title())
        if specialty:
            st.caption(f"Specialty: {specialty}")
    with col3:
        priority_icons = {'routine': '🟢', 'urgent': '🟡', 'emergent': '🔴'}
        st.metric("Priority", f"{priority_icons.get(priority, '⚪')} {priority.title()}")
    with col4:
        status_emoji = {'completed': '✅', 'active': '⏳', 'pending': '⏸️'}
        st.metric("Status", f"{status_emoji.get(status, '')} {status.title()}")

    # Staff Information
    if from_staff or to_staff:
        col1, col2, col3 = st.columns(3)
        with col1:
            if from_staff:
                st.markdown(f"**From:** {from_staff}")
        with col2:
            if to_staff:
                st.markdown(f"**To:** {to_staff}")
        with col3:
            if recording_duration:
                minutes = int(recording_duration // 60)
                seconds = int(recording_duration % 60)
                st.markdown(f"**Duration:** {minutes}:{seconds:02d}")

    # SBAR Report
    if sbar_situation:
        st.markdown("---")
        st.markdown("### 📊 SBAR Report with Quality Metrics")

        # Quality scores visualization
        if quality_score and completeness_score and critical_elements_score:
            # Create gauge charts
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = quality_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Quality Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#3b82f6"},
                        'steps': [
                            {'range': [0, 60], 'color': "#fee2e2"},
                            {'range': [60, 80], 'color': "#fef3c7"},
                            {'range': [80, 100], 'color': "#d1fae5"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig.update_layout(height=200, margin=dict(t=40, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = completeness_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Completeness"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#10b981"},
                        'steps': [
                            {'range': [0, 60], 'color': "#fee2e2"},
                            {'range': [60, 80], 'color': "#fef3c7"},
                            {'range': [80, 100], 'color': "#d1fae5"}
                        ]
                    }
                ))
                fig.update_layout(height=200, margin=dict(t=40, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)

            with col3:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = critical_elements_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Critical Elements"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#f59e0b"},
                        'steps': [
                            {'range': [0, 60], 'color': "#fee2e2"},
                            {'range': [60, 80], 'color': "#fef3c7"},
                            {'range': [80, 100], 'color': "#d1fae5"}
                        ]
                    }
                ))
                fig.update_layout(height=200, margin=dict(t=40, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)

            with col4:
                # Overall grade
                avg_score = (quality_score + completeness_score + critical_elements_score) / 3
                if avg_score >= 90:
                    grade, color = "A", "#10b981"
                elif avg_score >= 80:
                    grade, color = "B", "#3b82f6"
                elif avg_score >= 70:
                    grade, color = "C", "#f59e0b"
                else:
                    grade, color = "D", "#ef4444"

                st.markdown(f"""
                <div style='text-align: center; padding: 2rem;'>
                    <div style='font-size: 4rem; font-weight: bold; color: {color};'>{grade}</div>
                    <div style='color: #64748b;'>Overall Grade</div>
                    <div style='font-size: 1.2rem; margin-top: 0.5rem;'>{avg_score:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

        else:
            # Fallback for old data without scores
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Quality Score", "Calculating...", "N/A")
            with col2:
                st.metric("Completeness Score", "Calculating...", "N/A")

        st.markdown("---")

        # Edit mode toggle
        if 'edit_mode' not in st.session_state:
            st.session_state.edit_mode = False

        col_a, col_b, col_c = st.columns([3, 1, 1])
        with col_b:
            if not st.session_state.edit_mode:
                if st.button("✏️ Edit SBAR", use_container_width=True):
                    st.session_state.edit_mode = True
                    st.session_state.edited_situation = sbar_situation
                    st.session_state.edited_background = sbar_background
                    st.session_state.edited_assessment = sbar_assessment
                    st.session_state.edited_recommendation = sbar_recommendation
                    st.rerun()
        with col_c:
            if st.session_state.edit_mode:
                if st.button("💾 Save Changes", type="primary", use_container_width=True):
                    # Save edits
                    c.execute('''
                        UPDATE handoffs
                        SET sbar_situation=?, sbar_background=?, sbar_assessment=?, sbar_recommendation=?
                        WHERE id=?
                    ''', (
                        st.session_state.edited_situation,
                        st.session_state.edited_background,
                        st.session_state.edited_assessment,
                        st.session_state.edited_recommendation,
                        handoff_id
                    ))
                    conn.commit()

                    # Log audit trail
                    c.execute('''
                        INSERT INTO audit_logs (handoff_id, action, user, timestamp, details)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (handoff_id, 'edited', st.session_state.user['name'],
                         datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                         f"SBAR report edited by {st.session_state.user['name']}"))
                    conn.commit()

                    st.session_state.edit_mode = False
                    st.success("✅ SBAR updated successfully!")
                    st.rerun()

        # Situation
        st.markdown("""
        <div class='sbar-section' style='border-left-color: #3b82f6;'>
            <div class='sbar-title'>📘 Situation</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.edit_mode:
            st.session_state.edited_situation = st.text_area(
                "Edit Situation",
                value=st.session_state.get('edited_situation', sbar_situation),
                key="edit_situation",
                height=100
            )
        else:
            st.markdown(f"<p>{sbar_situation}</p>", unsafe_allow_html=True)

        # Background
        st.markdown("""
        <div class='sbar-section' style='border-left-color: #10b981;'>
            <div class='sbar-title'>📗 Background</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.edit_mode:
            st.session_state.edited_background = st.text_area(
                "Edit Background",
                value=st.session_state.get('edited_background', sbar_background),
                key="edit_background",
                height=100
            )
        else:
            st.markdown(f"<p>{sbar_background}</p>", unsafe_allow_html=True)

        # Assessment
        st.markdown("""
        <div class='sbar-section' style='border-left-color: #f59e0b;'>
            <div class='sbar-title'>📙 Assessment</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.edit_mode:
            st.session_state.edited_assessment = st.text_area(
                "Edit Assessment",
                value=st.session_state.get('edited_assessment', sbar_assessment),
                key="edit_assessment",
                height=100
            )
        else:
            st.markdown(f"<p>{sbar_assessment}</p>", unsafe_allow_html=True)

        # Recommendation
        st.markdown("""
        <div class='sbar-section' style='border-left-color: #ef4444;'>
            <div class='sbar-title'>📕 Recommendation</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.edit_mode:
            st.session_state.edited_recommendation = st.text_area(
                "Edit Recommendation",
                value=st.session_state.get('edited_recommendation', sbar_recommendation),
                key="edit_recommendation",
                height=100
            )
        else:
            st.markdown(f"<p>{sbar_recommendation}</p>", unsafe_allow_html=True)

        # Transcription (if available)
        if transcription and not st.session_state.edit_mode:
            with st.expander("📝 View Original Transcription"):
                st.markdown(f"**Voice Transcription:**\n\n{transcription}")

        # Actions
        st.markdown("---")
        st.markdown("### 📤 Actions")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("📄 Export PDF", use_container_width=True):
                # Generate PDF
                handoff_data = {
                    'patient_name': patient_name,
                    'patient_id': patient_id,
                    'handoff_type': handoff_type,
                    'priority': priority,
                    'created_at': created_at,
                    'from_staff': from_staff,
                    'to_staff': to_staff,
                    'specialty': specialty,
                    'sbar_situation': sbar_situation,
                    'sbar_background': sbar_background,
                    'sbar_assessment': sbar_assessment,
                    'sbar_recommendation': sbar_recommendation,
                    'quality_score': quality_score,
                    'completeness_score': completeness_score,
                    'critical_elements_score': critical_elements_score
                }

                pdf_data = generate_sbar_pdf(handoff_data)

                # Create download button
                b64_pdf = base64.b64encode(pdf_data).decode()
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="handoff_{handoff_id}_{patient_id}.pdf">Download PDF</a>'

                st.success("✅ PDF generated!")
                st.markdown(href, unsafe_allow_html=True)

                # Log export
                c.execute('''
                    INSERT INTO audit_logs (handoff_id, action, user, timestamp, details)
                    VALUES (?, ?, ?, ?, ?)
                ''', (handoff_id, 'exported', st.session_state.user['name'],
                     datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     f"PDF exported by {st.session_state.user['name']}"))
                conn.commit()

        with col2:
            if st.button("📧 Email Report", use_container_width=True):
                st.info("📧 Email sent! (Demo - would send via SMTP in production)")

        with col3:
            if st.button("🔄 Create Follow-up", use_container_width=True):
                st.session_state.page = 'create_handoff'
                st.session_state.selected_patient = patient_id
                st.rerun()

        with col4:
            if status != 'completed':
                if st.button("✅ Mark Complete", type="primary", use_container_width=True):
                    c.execute("UPDATE handoffs SET status='completed', completed_at=? WHERE id=?",
                             (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), handoff_id))

                    # Log completion
                    c.execute('''
                        INSERT INTO audit_logs (handoff_id, action, user, timestamp, details)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (handoff_id, 'completed', st.session_state.user['name'],
                         datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                         f"Handoff completed by {st.session_state.user['name']}"))

                    conn.commit()
                    st.success("✅ Handoff marked as complete!")
                    st.balloons()
                    st.rerun()
            else:
                st.success("✅ Already Completed")

    else:
        st.info("⏳ SBAR report is being generated. Please check back in a moment.")

    # Audit Trail for this handoff
    st.markdown("---")
    st.markdown("### 📝 Activity Log")

    c.execute('''
        SELECT action, user, timestamp, details
        FROM audit_logs
        WHERE handoff_id = ?
        ORDER BY timestamp DESC
    ''', (handoff_id,))
    logs = c.fetchall()

    if logs:
        for log in logs:
            action, user, timestamp, details = log
            action_icons = {
                'created': '➕', 'voice_uploaded': '🎤', 'transcribed': '📝',
                'sbar_generated': '🤖', 'completed': '✅', 'viewed': '👁️',
                'edited': '✏️', 'exported': '📤'
            }
            icon = action_icons.get(action, '📌')

            st.markdown(f"""
            <div style='background: #f8fafc; padding: 0.75rem; margin: 0.25rem 0; border-radius: 0.5rem;'>
                {icon} <strong>{action.replace('_', ' ').title()}</strong> by {user}
                <br><small style='color: #64748b;'>{timestamp} • {details}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No activity logged for this handoff.")

    conn.close()
