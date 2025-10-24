import streamlit as st
import sqlite3

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

    handoff_id, patient_name, patient_id, handoff_type, priority, status, created_at, \
    sbar_situation, sbar_background, sbar_assessment, sbar_recommendation, recording_duration = handoff

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<div class='main-header'>Handoff Details</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitle'>ID: {handoff_id} • Created: {created_at}</div>", unsafe_allow_html=True)
    with col2:
        if st.button("⬅️ Back to Dashboard", use_container_width=True):
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
    with col3:
        st.metric("Priority", priority.title())
    with col4:
        status_emoji = {'completed': '✅', 'active': '⏳', 'pending': '⏸️'}
        st.metric("Status", status.title(), status_emoji.get(status, ''))

    # SBAR Report
    if sbar_situation:
        st.markdown("---")
        st.markdown("### 📊 SBAR Report")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Completeness Score", "95%", "High Quality")
        with col2:
            st.metric("Quality Score", "92%", "Excellent")

        # Edit mode toggle
        if 'edit_mode' not in st.session_state:
            st.session_state.edit_mode = False

        col_a, col_b = st.columns([4, 1])
        with col_b:
            if not st.session_state.edit_mode:
                if st.button("✏️ Edit", use_container_width=True):
                    st.session_state.edit_mode = True
                    st.rerun()
            else:
                if st.button("💾 Save", type="primary", use_container_width=True):
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

        # Actions
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📄 Export PDF", use_container_width=True):
                st.info("PDF export functionality - coming soon!")

        with col2:
            if st.button("📧 Email Report", use_container_width=True):
                st.info("Email functionality - coming soon!")

        with col3:
            if st.button("✅ Mark Complete", type="primary", use_container_width=True):
                c.execute("UPDATE handoffs SET status='completed' WHERE id=?", (handoff_id,))
                conn.commit()
                st.success("✅ Handoff marked as complete!")
                time.sleep(1)
                st.rerun()

    else:
        st.info("⏳ SBAR report is being generated. Please check back in a moment.")
