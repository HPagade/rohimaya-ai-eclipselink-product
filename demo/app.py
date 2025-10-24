import streamlit as st
import time
from datetime import datetime
import sqlite3
import os

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

def init_db():
    """Initialize SQLite database for demo"""
    conn = sqlite3.connect('demo_data.db', check_same_thread=False)
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS handoffs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            patient_id TEXT,
            handoff_type TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT,
            sbar_situation TEXT,
            sbar_background TEXT,
            sbar_assessment TEXT,
            sbar_recommendation TEXT,
            recording_duration INTEGER
        )
    ''')

    # Insert sample data if empty
    c.execute('SELECT COUNT(*) FROM handoffs')
    if c.fetchone()[0] == 0:
        sample_data = [
            ('John Smith', 'P001234', 'shift_change', 'routine', 'completed',
             '2025-10-24 08:30:00',
             '60-year-old male with type 2 diabetes. Current glucose 145 mg/dL. Alert and oriented x3.',
             'History of T2DM (10 years), hypertension. Home meds: Metformin 1000mg BID, Lisinopril 10mg daily. Known PCN allergy.',
             'Vital signs stable: BP 130/85, HR 78, RR 16, SpO2 98% RA. Blood glucose trending down with insulin regimen.',
             'Continue insulin sliding scale. Discharge education completed. Follow-up with endocrinology in 2 weeks.',
             185),
            ('Jane Doe', 'P001235', 'transfer', 'urgent', 'active',
             '2025-10-24 10:15:00', None, None, None, None, None),
        ]
        c.executemany('''
            INSERT INTO handoffs (patient_name, patient_id, handoff_type, priority, status,
                                created_at, sbar_situation, sbar_background, sbar_assessment,
                                sbar_recommendation, recording_duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_data)

    conn.commit()
    return conn

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

    # Stats
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM handoffs WHERE status='active'")
    active_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM handoffs WHERE status='completed'")
    completed_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM handoffs")
    total_count = c.fetchone()[0]

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
            <div class='stat-number'>2.3</div>
            <div class='stat-label'>Avg Time (min)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Recent Handoffs")

    # Get recent handoffs
    c.execute("SELECT * FROM handoffs ORDER BY created_at DESC LIMIT 10")
    handoffs = c.fetchall()

    if handoffs:
        for handoff in handoffs:
            handoff_id, patient_name, patient_id, handoff_type, priority, status, created_at, *_ = handoff

            status_class = f"status-{status}"
            status_text = status.replace('_', ' ').title()

            col_a, col_b, col_c = st.columns([3, 1, 1])
            with col_a:
                st.markdown(f"""
                <div class='handoff-card'>
                    <div style='display: flex; align-items: center; justify-content: space-between;'>
                        <div>
                            <strong>{patient_name}</strong> • {patient_id}
                            <br><small style='color: #64748b;'>{handoff_type.replace('_', ' ').title()} • {created_at}</small>
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
        st.info("No handoffs yet. Create your first handoff to get started!")

    if st.button("➕ Create New Handoff", type="primary", use_container_width=True):
        st.session_state.page = 'create_handoff'
        st.rerun()

def main():
    """Main app logic"""

    # Sidebar
    with st.sidebar:
        st.markdown("### Navigation")

        if st.session_state.authenticated:
            st.markdown(f"**{st.session_state.user['name']}**")
            st.markdown(f"*{st.session_state.user['role']}*")
            st.markdown("---")

            if st.button("🏠 Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()

            if st.button("➕ New Handoff", use_container_width=True):
                st.session_state.page = 'create_handoff'
                st.rerun()

            if st.button("📋 All Handoffs", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()

            st.markdown("---")

            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.page = 'login'
                st.rerun()

        st.markdown("---")
        st.markdown("### About")
        st.info("**EclipseLink AI™**\n\nVoice-enabled clinical handoff platform with AI-powered SBAR generation.\n\n*Rohimaya Health AI*")

    # Main content
    if not st.session_state.authenticated:
        login_page()
    else:
        page = st.session_state.get('page', 'dashboard')

        if page == 'dashboard':
            dashboard_page()
        elif page == 'create_handoff':
            # Import create handoff page
            from pages import create_handoff
            create_handoff.show()
        elif page == 'view_handoff':
            # Import view handoff page
            from pages import view_handoff
            view_handoff.show()

if __name__ == "__main__":
    main()
