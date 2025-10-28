"""
EclipseLink AI - Demo Suite Home Page
Interactive demonstration suite for EclipseLink AI platform
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="EclipseLink AI - Interactive Demos",
    page_icon="🦚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand colors
PEACOCK_TEAL = "#1a9b8e"
PHOENIX_GOLD = "#f4c430"
LUNAR_BLUE = "#2c3e50"
ECLIPSE_NAVY = "#1a2332"
MOON_WHITE = "#f8f9fa"
ACCENT_COPPER = "#b87333"

# Custom CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    * {{
        font-family: 'Inter', sans-serif;
    }}

    .main-header {{
        background: linear-gradient(135deg, {PEACOCK_TEAL} 0%, {LUNAR_BLUE} 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}

    .hero-title {{
        font-size: 3rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
        line-height: 1.2;
    }}

    .hero-subtitle {{
        font-size: 1.3rem;
        margin: 0;
        opacity: 0.95;
    }}

    .demo-card {{
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-top: 5px solid {PEACOCK_TEAL};
        height: 100%;
        transition: transform 0.3s, box-shadow 0.3s;
    }}

    .demo-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }}

    .feature-card {{
        background: {MOON_WHITE};
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid {PEACOCK_TEAL};
        margin-bottom: 1rem;
    }}

    .stat-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}

    .stat-number {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {PEACOCK_TEAL};
        margin: 0;
    }}

    .stat-label {{
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }}

    .brand-badge {{
        background: linear-gradient(135deg, {PEACOCK_TEAL}, {LUNAR_BLUE});
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🦚</div>
        <h2 style="color: {PEACOCK_TEAL}; margin: 0;">EclipseLink AI</h2>
        <p style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">Interactive Demo Suite</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Navigate Demos")
    st.info("""
    Use the sidebar navigation above to explore:

    🎙️ **Voice-to-SBAR Demo**
    Experience the core feature

    📊 **Clinical Dashboard**
    See real-time management

    🚨 **Critical Alert Detection**
    See AI flag critical values

    🔄 **Update-Only Model**
    Baseline vs updates workflow

    👨‍👩‍👧‍👦 **Family Portal**
    Plain-language for families

    💬 **AI Chatbot**
    Query patient data instantly

    🌐 **Multi-Language Translation**
    50+ language support
    """)

    st.markdown("---")

    st.markdown("### About EclipseLink AI")
    st.markdown("""
    Voice-enabled clinical handoff platform with AI-powered SBAR generation.

    **Transform** 3-5 minute voice recordings into comprehensive SBAR reports in under 30 seconds.
    """)

    st.markdown("---")

    st.markdown("### Contact Us")
    st.markdown("""
    📧 **Email:** sales@rohimaya.ai

    🌐 **Website:** eclipselink.ai

    📞 **Phone:** 1-800-ECLIPSE
    """)

# Main Header
st.markdown(f"""
<div class="main-header">
    <div class="brand-badge">DEMO SUITE</div>
    <h1 class="hero-title">Welcome to EclipseLink AI™</h1>
    <p class="hero-subtitle">Voice-enabled clinical handoff platform with AI-powered SBAR generation</p>
    <p style="margin-top: 1.5rem; font-size: 1.1rem;">
        Transforming 3-5 minute voice recordings into comprehensive SBAR reports in under 30 seconds
    </p>
</div>
""", unsafe_allow_html=True)

# Key Stats
st.markdown("### Platform Impact")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">30s</div>
        <div class="stat-label">Average Processing Time</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">97%</div>
        <div class="stat-label">Transcription Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">4.5 min</div>
        <div class="stat-label">Time Saved per Handoff</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">9M+</div>
        <div class="stat-label">Target Healthcare Professionals</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Demo Cards
st.markdown("### Explore Our Interactive Demos")

st.markdown("#### Core Product Features")
col_demo1, col_demo2 = st.columns(2)

with col_demo1:
    st.markdown(f"""
    <div class="demo-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎙️</div>
        <h3 style="color: {PEACOCK_TEAL}; margin-top: 0;">Voice-to-SBAR Demo</h3>
        <p style="color: #666; line-height: 1.6;">
            Experience our core feature end-to-end. Upload or simulate a voice recording,
            watch real-time transcription, and see AI generate structured SBAR reports.
        </p>
        <ul style="color: #666; line-height: 1.8;">
            <li>Multiple clinical scenarios</li>
            <li>Real-time processing simulation</li>
            <li>Interactive SBAR editing</li>
            <li>EHR export preview</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_demo2:
    st.markdown(f"""
    <div class="demo-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
        <h3 style="color: {PEACOCK_TEAL}; margin-top: 0;">Clinical Dashboard</h3>
        <p style="color: #666; line-height: 1.6;">
            Explore the management interface used by healthcare facilities. View active
            handoffs, analytics, team performance, and system alerts.
        </p>
        <ul style="color: #666; line-height: 1.8;">
            <li>Real-time handoff tracking</li>
            <li>Analytics & insights</li>
            <li>Team activity monitoring</li>
            <li>System notifications</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("#### Advanced Features")
col_demo4, col_demo5, col_demo6 = st.columns(3)

with col_demo4:
    st.markdown(f"""
    <div class="demo-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🚨</div>
        <h3 style="color: {PEACOCK_TEAL}; margin-top: 0;">Critical Alert Detection</h3>
        <p style="color: #666; line-height: 1.6;">
            See how AI automatically identifies and flags critical values in patient handoffs.
            Real-time detection of abnormal vitals, labs, and high-risk medications.
        </p>
        <ul style="color: #666; line-height: 1.8;">
            <li>Critical vital sign alerts</li>
            <li>Abnormal lab value detection</li>
            <li>High-risk medication flags</li>
            <li>Multi-severity alert system</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_demo5:
    st.markdown(f"""
    <div class="demo-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔄</div>
        <h3 style="color: {PEACOCK_TEAL}; margin-top: 0;">Update-Only Model</h3>
        <p style="color: #666; line-height: 1.6;">
            Experience the baseline vs updates workflow. Create comprehensive baseline handoffs
            once, then quick 30-second updates for subsequent handoffs.
        </p>
        <ul style="color: #666; line-height: 1.8;">
            <li>Comprehensive baseline creation</li>
            <li>Quick update-only handoffs</li>
            <li>Visual change tracking</li>
            <li>85% time reduction</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_demo6:
    st.markdown(f"""
    <div class="demo-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">👨‍👩‍👧‍👦</div>
        <h3 style="color: {PEACOCK_TEAL}; margin-top: 0;">Family Portal</h3>
        <p style="color: #666; line-height: 1.6;">
            See how clinical updates are translated to plain language for patient families.
            Medical jargon automatically converted to easy-to-understand updates.
        </p>
        <ul style="color: #666; line-height: 1.8;">
            <li>Medical → plain language</li>
            <li>Side-by-side comparison</li>
            <li>Privacy controls</li>
            <li>Mobile-responsive design</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

col_demo7, col_demo8, col_demo9 = st.columns(3)

with col_demo7:
    st.markdown(f"""
    <div class="demo-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
        <h3 style="color: {PEACOCK_TEAL}; margin-top: 0;">AI Chatbot</h3>
        <p style="color: #666; line-height: 1.6;">
            Ask questions about patient data in natural language and get instant answers.
            Query medications, labs, vitals, procedures, and more using conversational AI.
        </p>
        <ul style="color: #666; line-height: 1.8;">
            <li>Natural language queries</li>
            <li>Instant patient data answers</li>
            <li>Source citations</li>
            <li>Quick query templates</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_demo8:
    st.markdown(f"""
    <div class="demo-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🌐</div>
        <h3 style="color: {PEACOCK_TEAL}; margin-top: 0;">Multi-Language Translation</h3>
        <p style="color: #666; line-height: 1.6;">
            Experience real-time translation to 50+ languages. Clinical handoffs automatically
            translated for diverse healthcare teams and international family members.
        </p>
        <ul style="color: #666; line-height: 1.8;">
            <li>50+ languages supported</li>
            <li>Real-time translation</li>
            <li>Medical terminology accuracy</li>
            <li>Cultural sensitivity</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_demo9:
    st.markdown(f"""
    <div class="demo-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
        <h3 style="color: {PEACOCK_TEAL}; margin-top: 0;">More Coming Soon</h3>
        <p style="color: #666; line-height: 1.6;">
            We're continuously adding new demos to showcase EclipseLink AI's capabilities.
            Check back soon for EHR integration, offline mode, and ecosystem demos.
        </p>
        <ul style="color: #666; line-height: 1.8;">
            <li>EHR integration flow</li>
            <li>Offline mode & sync</li>
            <li>Team collaboration</li>
            <li>HIPAA audit logs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Key Features
st.markdown("### Key Platform Features")

col_feat1, col_feat2 = st.columns(2)

with col_feat1:
    st.markdown(f"""
    <div class="feature-card">
        <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">🎙️ Voice-to-SBAR Conversion</h4>
        <ul style="line-height: 1.8; margin: 0;">
            <li><strong>Record</strong> via mobile, tablet, or desktop</li>
            <li><strong>Transcribe</strong> with 97%+ medical term accuracy (Azure OpenAI Whisper)</li>
            <li><strong>Generate</strong> structured SBAR reports with GPT-4 in under 30 seconds</li>
            <li><strong>Edit</strong> and approve with inline editing interface</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="feature-card">
        <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">🏥 EHR Integration</h4>
        <ul style="line-height: 1.8; margin: 0;">
            <li><strong>Seamless connectivity</strong> with Epic, Cerner, MEDITECH</li>
            <li><strong>FHIR R4</strong> and <strong>HL7 v2</strong> protocol support</li>
            <li><strong>Bi-directional sync</strong> of patient data</li>
            <li><strong>One-click export</strong> to EHR systems</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="feature-card">
        <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">📱 Multi-Platform Access</h4>
        <ul style="line-height: 1.8; margin: 0;">
            <li><strong>Progressive Web App (PWA)</strong> - Install on any device</li>
            <li><strong>Offline capability</strong> - Record without internet</li>
            <li><strong>Real-time sync</strong> across all devices</li>
            <li><strong>Responsive design</strong> optimized for all screens</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_feat2:
    st.markdown(f"""
    <div class="feature-card">
        <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">🔒 HIPAA Compliance</h4>
        <ul style="line-height: 1.8; margin: 0;">
            <li><strong>End-to-end encryption</strong> - AES-256 at rest, TLS 1.3 in transit</li>
            <li><strong>Row-Level Security</strong> - Database-level data isolation</li>
            <li><strong>Comprehensive audit logs</strong> - 7-year retention</li>
            <li><strong>PHI access tracking</strong> - Every access logged</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="feature-card">
        <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">🤖 AI-Powered Intelligence</h4>
        <ul style="line-height: 1.8; margin: 0;">
            <li><strong>Azure OpenAI Whisper</strong> for speech-to-text</li>
            <li><strong>GPT-4-32k</strong> for SBAR generation</li>
            <li><strong>Medical terminology</strong> auto-correction</li>
            <li><strong>Context-aware</strong> clinical information extraction</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="feature-card">
        <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">📊 Analytics & Insights</h4>
        <ul style="line-height: 1.8; margin: 0;">
            <li><strong>Real-time dashboards</strong> for facility management</li>
            <li><strong>Performance metrics</strong> by department and staff</li>
            <li><strong>Quality indicators</strong> and compliance tracking</li>
            <li><strong>Custom reports</strong> and data exports</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Target Users
st.markdown("### Target Healthcare Professionals")

st.markdown(f"""
<div style="background: {MOON_WHITE}; padding: 2rem; border-radius: 10px;">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
        <div>
            <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">Nursing Staff</h4>
            <ul style="line-height: 1.8; color: #666;">
                <li>Registered Nurses (RN)</li>
                <li>Licensed Practical Nurses (LPN)</li>
                <li>Certified Nursing Assistants (CNA)</li>
                <li>Nurse Practitioners (NP)</li>
            </ul>
        </div>
        <div>
            <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">Physicians</h4>
            <ul style="line-height: 1.8; color: #666;">
                <li>Medical Doctors (MD)</li>
                <li>Doctors of Osteopathy (DO)</li>
                <li>Physician Assistants (PA)</li>
                <li>Resident Physicians</li>
            </ul>
        </div>
        <div>
            <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">Allied Health</h4>
            <ul style="line-height: 1.8; color: #666;">
                <li>Respiratory Therapists (RT)</li>
                <li>Physical Therapists (PT)</li>
                <li>Occupational Therapists (OT)</li>
                <li>Medical Assistants (MA)</li>
            </ul>
        </div>
        <div>
            <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">Emergency Services</h4>
            <ul style="line-height: 1.8; color: #666;">
                <li>Emergency Medical Technicians (EMT)</li>
                <li>Paramedics</li>
                <li>Emergency Department Staff</li>
                <li>Critical Care Staff</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Market Opportunity
st.markdown("### Market Opportunity")

col_market1, col_market2, col_market3 = st.columns(3)

with col_market1:
    st.markdown(f"""
    <div class="stat-card" style="padding: 2rem;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">👥</div>
        <div class="stat-number">9M+</div>
        <div class="stat-label" style="font-size: 1rem; margin-top: 1rem;">
            Healthcare Professionals in US
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_market2:
    st.markdown(f"""
    <div class="stat-card" style="padding: 2rem;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">🏥</div>
        <div class="stat-number">106K+</div>
        <div class="stat-label" style="font-size: 1rem; margin-top: 1rem;">
            Target Facilities<br>(Hospitals, Nursing Homes, Clinics)
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_market3:
    st.markdown(f"""
    <div class="stat-card" style="padding: 2rem;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">💵</div>
        <div class="stat-number">$18.9B</div>
        <div class="stat-label" style="font-size: 1rem; margin-top: 1rem;">
            Total Addressable Market (TAM)
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Call to Action
st.markdown(f"""
<div style="background: linear-gradient(135deg, {PEACOCK_TEAL} 0%, {LUNAR_BLUE} 100%); padding: 3rem 2rem; border-radius: 15px; text-align: center; color: white;">
    <h2 style="margin: 0 0 1rem 0;">Ready to Transform Your Clinical Handoffs?</h2>
    <p style="font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.95;">
        Explore our interactive demos to see how EclipseLink AI can save time, reduce errors, and improve patient outcomes at your facility.
    </p>
    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
        <div style="background: white; color: {PEACOCK_TEAL}; padding: 1rem 2rem; border-radius: 8px; font-weight: 600; cursor: pointer;">
            📧 Schedule a Live Demo
        </div>
        <div style="background: rgba(255,255,255,0.2); color: white; padding: 1rem 2rem; border-radius: 8px; font-weight: 600; cursor: pointer; border: 2px solid white;">
            📞 Contact Sales
        </div>
        <div style="background: rgba(255,255,255,0.2); color: white; padding: 1rem 2rem; border-radius: 8px; font-weight: 600; cursor: pointer; border: 2px solid white;">
            📄 Download Brochure
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 2rem;">
    <h3 style="color: {PEACOCK_TEAL}; margin-bottom: 1rem;">About Rohimaya Health AI</h3>
    <p style="line-height: 1.8; max-width: 800px; margin: 0 auto;">
        EclipseLink AI™ is the flagship product of <strong>Rohimaya Health AI</strong>, a healthcare technology
        company dedicated to improving clinical communication and patient safety through AI-powered solutions.
    </p>
    <p style="margin-top: 1.5rem;">
        <strong>Founded by:</strong> Hannah Kraulik Pagade (CEO) • Prasad Pagade (CTO)
    </p>
    <p style="margin-top: 1rem;">
        📧 info@rohimaya.ai • 🌐 rohimaya.ai • 🦚 EclipseLink AI™
    </p>
    <p style="font-size: 0.9rem; margin-top: 2rem; color: #999;">
        © 2025 Rohimaya Health AI. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
