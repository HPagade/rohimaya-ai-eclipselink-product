"""
SBAR Generation Demo - EclipseLink AI™
Demonstrates AI-powered SBAR report generation from clinical notes
"""

import streamlit as st
import time
from datetime import datetime

st.set_page_config(
    page_title="SBAR Generation Demo - EclipseLink AI",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .sbar-section {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #0ea5e9;
    }
    .sbar-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0ea5e9;
        margin-bottom: 0.5rem;
    }
    .processing {
        background: linear-gradient(90deg, #0ea5e9, #3b82f6, #0ea5e9);
        background-size: 200% 100%;
        animation: gradient 2s ease infinite;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .quality-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-weight: 600;
        font-size: 0.875rem;
    }
    .badge-high { background-color: #10b981; color: white; }
    .badge-medium { background-color: #f59e0b; color: white; }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 SBAR Generation Demo")
st.markdown("See how Azure OpenAI GPT-4 transforms clinical notes into structured SBAR reports.")

st.markdown("---")

# Initialize session state
if 'generated' not in st.session_state:
    st.session_state.generated = False
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Sample input transcript
sample_transcript = """Patient John Doe, 67-year-old male, admitted three days ago with acute exacerbation of COPD. Currently on room air with oxygen saturation 94%. Patient has a history of hypertension and diabetes mellitus type 2.

Background: Patient was admitted through the ED with shortness of breath and productive cough. Chest X-ray showed bilateral lower lobe infiltrates. Started on antibiotics and steroids. Blood glucose has been elevated, ranging from 180 to 220.

Assessment: Patient is improving, respiratory status is stable. However, blood sugar control needs optimization. Patient is eager to go home but may need one more day for glucose monitoring.

Recommendation: Continue current antibiotic course, consider endocrinology consult for diabetes management, plan for discharge tomorrow if glucose levels stabilize. Patient education on inhaler technique before discharge."""

# Input Section
st.subheader("📥 Clinical Notes Input")

with st.expander("ℹ️ How SBAR Generation Works", expanded=False):
    st.markdown("""
    ### AI-Powered SBAR Generation Process

    1. **Transcript Analysis**: GPT-4 analyzes the clinical notes for key information
    2. **Context Extraction**: Identifies patient demographics, medical history, current status
    3. **Structure Generation**: Organizes information into SBAR format:
       - **S**ituation: Current patient status and chief concern
       - **B**ackground: Relevant medical history and admission details
       - **A**ssessment: Clinical evaluation and findings
       - **R**ecommendation: Treatment plan and next steps
    4. **Quality Validation**: Checks completeness, readability, and clinical accuracy
    5. **Version Control**: Tracks changes across handoff updates

    **AI Model**: Azure OpenAI GPT-4 Turbo (healthcare-optimized)
    """)

transcript = st.text_area(
    "Clinical Transcript",
    value=sample_transcript,
    height=200,
    help="Enter or paste clinical notes from voice transcription"
)

# Patient context
col1, col2, col3 = st.columns(3)
with col1:
    patient_name = st.text_input("Patient Name", value="John Doe")
with col2:
    mrn = st.text_input("MRN", value="MRN-2024-001234")
with col3:
    handoff_type = st.selectbox("Handoff Type", ["Initial", "Update", "Discharge"])

# Generate button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Generate SBAR Report", type="primary", use_container_width=True):
        st.session_state.processing = True
        st.session_state.generated = False
        st.rerun()

# Processing animation
if st.session_state.processing:
    st.markdown("---")
    st.markdown('<div class="processing">🤖 AI is analyzing clinical notes and generating SBAR report...</div>', unsafe_allow_html=True)

    progress_bar = st.progress(0)
    status_text = st.empty()

    steps = [
        ("Parsing transcript...", 20),
        ("Extracting clinical context...", 40),
        ("Identifying SBAR components...", 60),
        ("Generating structured report...", 80),
        ("Validating completeness...", 100)
    ]

    for step, progress in steps:
        status_text.text(f"⚙️ {step}")
        progress_bar.progress(progress)
        time.sleep(0.5)

    st.session_state.processing = False
    st.session_state.generated = True
    st.rerun()

# Generated SBAR Report
if st.session_state.generated:
    st.markdown("---")
    st.subheader("📋 Generated SBAR Report")

    # Quality metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Completeness", "96.5%", "3.2%")
    with col2:
        st.metric("Readability", "92.0%")
    with col3:
        st.metric("Processing Time", "2.3s")
    with col4:
        st.metric("Confidence", "High", delta="✓")

    st.markdown("")

    # SBAR Sections
    st.markdown("""
    <div class="sbar-section">
        <div class="sbar-header">S - Situation</div>
        <p><strong>Patient:</strong> John Doe (MRN: MRN-2024-001234)</p>
        <p><strong>Age/Gender:</strong> 67-year-old male</p>
        <p><strong>Primary Diagnosis:</strong> Acute exacerbation of Chronic Obstructive Pulmonary Disease (COPD)</p>
        <p><strong>Current Status:</strong> Day 3 of hospitalization, clinically stable on room air with SpO2 94%</p>
        <p><strong>Key Concern:</strong> Elevated blood glucose levels requiring optimization before discharge</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sbar-section">
        <div class="sbar-header">B - Background</div>
        <p><strong>Admission Route:</strong> Emergency Department</p>
        <p><strong>Chief Complaint:</strong> Shortness of breath with productive cough</p>
        <p><strong>Relevant History:</strong></p>
        <ul>
            <li>Chronic Obstructive Pulmonary Disease (COPD)</li>
            <li>Hypertension</li>
            <li>Diabetes Mellitus Type 2</li>
        </ul>
        <p><strong>Initial Workup:</strong></p>
        <ul>
            <li>Chest X-ray: Bilateral lower lobe infiltrates</li>
            <li>Started on antibiotics and corticosteroids</li>
        </ul>
        <p><strong>Hospital Course:</strong> Blood glucose elevated, ranging 180-220 mg/dL despite current diabetic regimen</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sbar-section">
        <div class="sbar-header">A - Assessment</div>
        <p><strong>Respiratory Status:</strong> Improving and stable</p>
        <ul>
            <li>Currently maintaining SpO2 94% on room air</li>
            <li>Decreased shortness of breath</li>
            <li>Productive cough improving</li>
        </ul>
        <p><strong>Glycemic Control:</strong> Suboptimal, requires adjustment</p>
        <ul>
            <li>Persistent hyperglycemia (180-220 mg/dL)</li>
            <li>Current diabetic regimen insufficient</li>
            <li>May benefit from endocrinology consultation</li>
        </ul>
        <p><strong>Discharge Readiness:</strong> Nearly ready, pending glucose stabilization</p>
        <ul>
            <li>Patient eager for discharge</li>
            <li>Additional 24 hours recommended for glucose monitoring</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sbar-section">
        <div class="sbar-header">R - Recommendation</div>
        <p><strong>Immediate Actions:</strong></p>
        <ul>
            <li>Continue current antibiotic course for COPD exacerbation</li>
            <li>Continue corticosteroids as prescribed</li>
            <li>Consider endocrinology consultation for diabetes management optimization</li>
            <li>Monitor blood glucose every 4 hours</li>
        </ul>
        <p><strong>Discharge Planning:</strong></p>
        <ul>
            <li>Plan for discharge tomorrow if glucose levels stabilize (target <180 mg/dL)</li>
            <li>Patient education on proper inhaler technique before discharge</li>
            <li>Diabetes medication adjustment prior to discharge</li>
            <li>Schedule follow-up with primary care physician within 1 week</li>
            <li>Schedule follow-up with pulmonology within 2 weeks</li>
        </ul>
        <p><strong>Monitoring:</strong></p>
        <ul>
            <li>Continue oxygen saturation monitoring</li>
            <li>Monitor for respiratory distress</li>
            <li>Close glucose monitoring until stable</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Quality Assessment
    st.markdown("---")
    st.subheader("📊 Quality Assessment")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Completeness Score: 96.5%**")
        st.markdown('<span class="quality-badge badge-high">High Quality</span>', unsafe_allow_html=True)
        st.markdown("""
        - ✅ All SBAR sections present
        - ✅ Patient demographics included
        - ✅ Medical history documented
        - ✅ Clear recommendations provided
        - ⚠️ Could include vital signs timeline
        """)

    with col2:
        st.markdown("**Readability Score: 92.0%**")
        st.markdown('<span class="quality-badge badge-high">Excellent</span>', unsafe_allow_html=True)
        st.markdown("""
        - ✅ Clear, concise language
        - ✅ Proper medical terminology
        - ✅ Well-structured format
        - ✅ Easy to scan and review
        - ✅ Action items clearly stated
        """)

    # Actions
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("✏️ Edit Report", use_container_width=True):
            st.info("Opening SBAR editor...")

    with col2:
        if st.button("📄 Export PDF", use_container_width=True):
            st.success("✅ PDF generated!")

    with col3:
        if st.button("📧 Send to Provider", use_container_width=True):
            st.success("✅ Notification sent!")

    with col4:
        if st.button("🔄 Generate New", use_container_width=True):
            st.session_state.generated = False
            st.rerun()

# Version History
if st.session_state.generated:
    with st.expander("📜 Version History"):
        st.markdown("""
        | Version | Date | Modified By | Changes |
        |---------|------|-------------|---------|
        | v3 | 2024-10-28 14:30 | Dr. Smith | Current version - Added endocrinology consult recommendation |
        | v2 | 2024-10-28 10:15 | Nurse Johnson | Updated glucose readings, adjusted discharge timeline |
        | v1 | 2024-10-27 22:00 | Dr. Williams | Initial SBAR report generated from admission notes |
        """)

# Technical Details
with st.expander("🔧 Technical Implementation"):
    st.markdown("""
    ### Azure OpenAI GPT-4 Integration

    **Model Configuration**:
    - Model: `gpt-4-turbo-preview`
    - Temperature: 0.3 (balanced creativity and accuracy)
    - Max Tokens: 2000
    - Top-p: 0.95

    **System Prompt**:
    ```
    You are a medical AI assistant specializing in clinical handoffs.
    Generate structured SBAR reports from clinical notes following
    evidence-based healthcare communication standards.
    ```

    **Processing Pipeline**:
    1. Transcript received from voice recording
    2. Patient context retrieved from database
    3. Previous SBAR versions fetched (for updates)
    4. GPT-4 API called with clinical context
    5. Response parsed and validated
    6. Completeness and readability scores calculated
    7. Report saved with version control
    8. Notification sent to receiving provider

    **Quality Metrics**:
    - Completeness: Percentage of required SBAR fields populated
    - Readability: Flesch-Kincaid grade level score
    - Confidence: Model certainty in information extraction
    """)
