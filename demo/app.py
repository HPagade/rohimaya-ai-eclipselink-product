import streamlit as st
import time
from datetime import datetime
import sqlite3
import os
from database import init_db, search_handoffs
from translations import LANGUAGES, get_text

# Page configuration
st.set_page_config(
    page_title="EclipseLink AI™ - Clinical Handoff Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'handoffs' not in st.session_state:
    st.session_state.handoffs = []
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
        margin: 0.5rem 0;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .handoff-card {
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        background: white;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .status-completed {
        background: #d1fae5;
        color: #065f46;
    }
    .status-active {
        background: #dbeafe;
        color: #1e40af;
    }
    .status-pending {
        background: #fef3c7;
        color: #92400e;
    }
    .sbar-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #3b82f6;
    }
    .sbar-title {
        font-weight: bold;
        color: #1e40af;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
conn = init_db()

def login_page():
    """Login page"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<div style='text-align: center; margin-top: 3rem;'>", unsafe_allow_html=True)
        st.markdown("⚡", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #1e40af;'>EclipseLink AI™</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>Clinical Handoff Platform</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("### Sign In")
            email = st.text_input("Email", placeholder="doctor@hospital.com")
            password = st.text_input("Password", type="password", placeholder="Enter password")

            col_a, col_b = st.columns(2)
            with col_a:
                login_btn = st.form_submit_button("Sign In", use_container_width=True)
            with col_b:
                demo_btn = st.form_submit_button("Try Demo", use_container_width=True, type="secondary")

            if login_btn or demo_btn:
                # Demo authentication - accept any credentials or demo mode
                st.session_state.authenticated = True
                st.session_state.user = {
                    'name': 'Dr. Sarah Johnson',
                    'role': 'Registered Nurse',
                    'email': email if email else 'demo@eclipselink.ai'
                }
                st.rerun()

        st.markdown("<p style='text-align: center; color: #64748b; margin-top: 2rem; font-size: 0.9rem;'>Demo Mode: Enter any credentials or click 'Try Demo'</p>", unsafe_allow_html=True)

def dashboard_page():
    """Main dashboard"""
    # Header
    st.markdown(f"<div class='main-header'>⚡ EclipseLink AI™</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Welcome back, {st.session_state.user['name']}</div>", unsafe_allow_html=True)

    # First-time user guided tour
    if 'tour_shown' not in st.session_state:
        st.session_state.tour_shown = True
        st.balloons()

        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 0.75rem; margin-bottom: 2rem; color: white;'>
            <h2 style='margin: 0 0 1rem 0; color: white;'>👋 Welcome to EclipseLink AI!</h2>
            <p style='font-size: 1.1rem; margin-bottom: 1rem;'>
                Let's take a quick tour of your new clinical handoff platform. Here's what you can do:
            </p>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem;'>
                <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem;'>
                    <strong>🎤 Voice Recording</strong><br>
                    <small>Record handoffs in 2 minutes vs 20 minutes manually</small>
                </div>
                <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem;'>
                    <strong>🤖 AI SBAR Generation</strong><br>
                    <small>Automatic structured reports with quality scoring</small>
                </div>
                <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem;'>
                    <strong>📊 Analytics Dashboard</strong><br>
                    <small>Track performance, trends, and quality metrics</small>
                </div>
                <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem;'>
                    <strong>👥 Patient Management</strong><br>
                    <small>Complete histories and handoff tracking</small>
                </div>
            </div>
            <p style='margin-top: 1.5rem; text-align: center; font-size: 0.9rem; opacity: 0.9;'>
                💡 Tip: Start by clicking "➕ New Handoff" in the sidebar to create your first AI-powered handoff!
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Stats
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM handoffs WHERE status='active'")
    active_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM handoffs WHERE status='completed'")
    completed_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM handoffs")
    total_count = c.fetchone()[0]

    # Calculate average time
    c.execute("SELECT AVG(recording_duration) FROM handoffs WHERE recording_duration IS NOT NULL")
    avg_duration = c.fetchone()[0] or 0
    avg_min = int(avg_duration // 60)
    avg_sec = int(avg_duration % 60)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class='stat-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
            <div class='stat-number'>{}</div>
            <div class='stat-label'>Active Handoffs</div>
        </div>
        """.format(active_count), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='stat-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
            <div class='stat-number'>{}</div>
            <div class='stat-label'>Completed Today</div>
        </div>
        """.format(completed_count), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='stat-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <div class='stat-number'>{}</div>
            <div class='stat-label'>Total Handoffs</div>
        </div>
        """.format(total_count), unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='stat-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
            <div class='stat-number'>{}:{:02d}</div>
            <div class='stat-label'>Avg Time (min)</div>
        </div>
        """.format(avg_min, avg_sec), unsafe_allow_html=True)

    st.markdown("---")

    # Search and Filter
    st.markdown("### 🔍 Search & Filter")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        search_query = st.text_input("Search", placeholder="Patient name, ID...", label_visibility="collapsed")

    with col2:
        handoff_type_filter = st.selectbox("Type", ["all", "shift_change", "transfer", "admission", "discharge", "procedure"])

    with col3:
        priority_filter = st.selectbox("Priority", ["all", "routine", "urgent", "emergent"])

    with col4:
        status_filter = st.selectbox("Status", ["all", "active", "pending", "completed"])

    with col5:
        c.execute("SELECT DISTINCT specialty FROM handoffs WHERE specialty IS NOT NULL")
        specialties = ['all'] + [s[0] for s in c.fetchall()]
        specialty_filter = st.selectbox("Specialty", specialties)

    # Get filtered handoffs
    handoffs = search_handoffs(conn,
                               query=search_query,
                               handoff_type=handoff_type_filter,
                               priority=priority_filter,
                               status=status_filter,
                               specialty=specialty_filter)

    st.markdown(f"### Handoffs ({len(handoffs)} found)")

    if handoffs:
        for handoff in handoffs:
            handoff_id = handoff[0]
            patient_name = handoff[1]
            patient_id = handoff[2]
            handoff_type = handoff[3]
            priority = handoff[4]
            status = handoff[5]
            created_at = handoff[6]
            from_staff = handoff[8] if len(handoff) > 8 else 'Unknown'
            specialty = handoff[10] if len(handoff) > 10 else 'General'

            status_class = f"status-{status}"
            status_text = status.replace('_', ' ').title()

            col_a, col_b, col_c = st.columns([3, 1, 1])
            with col_a:
                st.markdown(f"""
                <div class='handoff-card'>
                    <div style='display: flex; align-items: center; justify-content: space-between;'>
                        <div>
                            <strong>{patient_name}</strong> • {patient_id}
                            <br><small style='color: #64748b;'>{handoff_type.replace('_', ' ').title()} • {specialty} • {created_at}</small>
                            <br><small style='color: #94a3b8;'>From: {from_staff}</small>
                        </div>
                        <span class='status-badge {status_class}'>{status_text}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                if st.button("View", key=f"view_{handoff_id}", use_container_width=True):
                    st.session_state.selected_handoff = handoff_id
                    st.session_state.page = 'view_handoff'
                    st.rerun()
            with col_c:
                priority_color = {'routine': '🟢', 'urgent': '🟡', 'emergent': '🔴'}
                st.markdown(f"<div style='text-align: center; padding: 0.5rem;'>{priority_color.get(priority, '⚪')} {priority.title()}</div>", unsafe_allow_html=True)
    else:
        st.info("No handoffs found. Try adjusting your filters or create a new handoff.")

    if st.button("➕ Create New Handoff", type="primary", use_container_width=True):
        st.session_state.page = 'create_handoff'
        st.rerun()

def main():
    """Main app logic"""

    # Sidebar
    with st.sidebar:
        # Language selector
        if 'language' not in st.session_state:
            st.session_state.language = 'en'

        st.markdown("### 🌐 Language")
        selected_lang = st.selectbox(
            "Choose language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x],
            key="lang_selector",
            label_visibility="collapsed"
        )
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()

        st.markdown("---")
        st.markdown("### Navigation")

        if st.session_state.authenticated:
            st.markdown(f"**{st.session_state.user['name']}**")
            st.markdown(f"*{st.session_state.user['role']}*")
            st.markdown("---")

            # Main navigation buttons with visual feedback
            current_page = st.session_state.get('page', 'dashboard')

            if st.button("🏠 Dashboard", use_container_width=True, type="primary" if current_page == 'dashboard' else "secondary"):
                st.session_state.page = 'dashboard'
                st.rerun()

            if st.button("➕ New Handoff", use_container_width=True, type="primary" if current_page == 'create_handoff' else "secondary"):
                st.session_state.page = 'create_handoff'
                st.rerun()

            if st.button("👥 Patients", use_container_width=True, type="primary" if current_page == 'patients' else "secondary"):
                st.session_state.page = 'patients'
                st.rerun()

            if st.button("📊 Analytics", use_container_width=True, type="primary" if current_page == 'analytics' else "secondary"):
                st.session_state.page = 'analytics'
                st.rerun()

            if st.button("📝 Audit Trail", use_container_width=True, type="primary" if current_page == 'audit_trail' else "secondary"):
                st.session_state.page = 'audit_trail'
                st.rerun()

            st.markdown("---")
            st.markdown("**🚀 NEW FEATURES**")

            if st.button("🤖 AI Assistant", use_container_width=True, type="primary" if current_page == 'chatbot' else "secondary"):
                st.session_state.page = 'chatbot'
                st.rerun()

            if st.button("👨‍👩‍👧 Family Portal", use_container_width=True, type="primary" if current_page == 'family_portal' else "secondary"):
                st.session_state.page = 'family_portal'
                st.rerun()

            if st.button("🏥 Patient Portal", use_container_width=True, type="primary" if current_page == 'patient_portal' else "secondary"):
                st.session_state.page = 'patient_portal'
                st.rerun()

            st.markdown("---")

            # Quick stats in sidebar
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM handoffs WHERE status='active'")
            active_count = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM patients")
            patient_count = c.fetchone()[0]

            st.markdown(f"""
            **Quick Stats**
            - Active Handoffs: **{active_count}**
            - Total Patients: **{patient_count}**
            """)

            st.markdown("---")

            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.page = 'login'
                st.rerun()

        st.markdown("---")
        st.markdown("### About")
        st.info("**EclipseLink AI™**\n\nVoice-enabled clinical handoff platform with AI-powered SBAR generation.\n\n*Rohimaya Health AI*\n\n🔒 HIPAA Compliant")

    # Main content
    if not st.session_state.authenticated:
        login_page()
    else:
        page = st.session_state.get('page', 'dashboard')

        if page == 'dashboard':
            dashboard_page()
        elif page == 'create_handoff':
            from pages import create_handoff
            create_handoff.show()
        elif page == 'view_handoff':
            from pages import view_handoff
            view_handoff.show()
        elif page == 'patients':
            from pages import patients
            patients.show()
        elif page == 'analytics':
            from pages import analytics
            analytics.show()
        elif page == 'audit_trail':
            from pages import audit_trail
            audit_trail.show()
        elif page == 'chatbot':
            from pages import chatbot
            chatbot.show()
        elif page == 'family_portal':
            from pages import family_portal
            family_portal.show()
        elif page == 'patient_portal':
            from pages import patient_portal
            patient_portal.show()

if __name__ == "__main__":
    main()
