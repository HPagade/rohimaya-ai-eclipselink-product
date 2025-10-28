"""
EclipseLink AI - Update-Only Model Demo
Shows baseline vs. updates workflow with time savings
"""

import streamlit as st
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Update-Only Model - EclipseLink AI",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand colors
PEACOCK_TEAL = "#1a9b8e"
PHOENIX_GOLD = "#f4c430"
LUNAR_BLUE = "#2c3e50"
ECLIPSE_NAVY = "#1a2332"

# Custom CSS
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, {PEACOCK_TEAL} 0%, {LUNAR_BLUE} 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }}
    .baseline-card {{
        background: #ecf0f1;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #95a5a6;
        margin-bottom: 1rem;
    }}
    .unchanged {{
        color: #95a5a6;
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }}
    .changed {{
        background: #fff3cd;
        border-left: 4px solid {PHOENIX_GOLD};
        padding: 0.5rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }}
    .new {{
        background: #d1f2eb;
        border-left: 4px solid {PEACOCK_TEAL};
        padding: 0.5rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }}
    .time-badge {{
        background: {PEACOCK_TEAL};
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }}
    .comparison-box {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🔄 Update-Only Model Demo</h1>
    <p style="font-size: 1.2rem; margin: 0;">Baseline handoffs vs. Update-only handoffs - Dramatic time savings</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 'intro'
if 'baseline_created' not in st.session_state:
    st.session_state.baseline_created = False
if 'update_created' not in st.session_state:
    st.session_state.update_created = False

# Sidebar
with st.sidebar:
    st.image("https://img.shields.io/badge/EclipseLink-AI-1a9b8e?style=for-the-badge", use_container_width=True)
    st.markdown("---")
    st.markdown("### Demo Concept")
    st.info("""
    **Traditional Model:**
    Every handoff repeats ALL information
    ⏱️ 3-5 minutes each time

    **Update-Only Model:**
    1️⃣ Comprehensive baseline (first handoff)
    2️⃣ Quick updates (only what changed)
    ⏱️ 30-45 seconds for updates

    **Result: 85% time reduction!**
    """)

    st.markdown("---")

    if st.button("Reset Demo", type="secondary"):
        st.session_state.step = 'intro'
        st.session_state.baseline_created = False
        st.session_state.update_created = False
        st.rerun()

# Sample data
baseline_data = {
    "patient_name": "Robert Williams",
    "mrn": "MRN-556677",
    "age": 72,
    "admission_date": "2025-01-25",
    "diagnosis": "Acute exacerbation of COPD",
    "history": """
- COPD (15-year history, 40 pack-year smoking)
- Hypertension (controlled on lisinopril)
- Type 2 Diabetes (HbA1c 7.2%)
- Benign prostatic hyperplasia
- Former smoker (quit 2 years ago)
- No known drug allergies
    """,
    "medications": """
- Albuterol/Ipratropium nebulizer Q6H
- Prednisone 40mg PO daily (day 3 of 5)
- Azithromycin 500mg PO daily (day 3 of 5)
- Lisinopril 20mg PO daily
- Metformin 1000mg PO BID
- Tamsulosin 0.4mg PO QHS
- Heparin 5000 units SQ Q12H (DVT prophylaxis)
    """,
    "vitals": """
- BP: 138/82 mmHg
- HR: 88 bpm
- RR: 22 breaths/min
- SpO2: 92% on 2L nasal cannula
- Temp: 98.4°F
    """,
    "assessment": """
Patient admitted 2 days ago with increased shortness of breath, productive cough with green sputum, and wheezing. Started on IV steroids transitioned to PO prednisone. Antibiotics initiated for possible bacterial superinfection. Respiratory status improving but still requires supplemental oxygen.
    """,
    "plan": """
- Continue current medications
- Wean oxygen as tolerated
- Chest PT BID
- Ambulate with PT
- Target discharge in 2-3 days
- Follow-up with pulmonology in 2 weeks
    """
}

updates_data = [
    {
        "time": "8 hours later",
        "duration": "45 sec",
        "changes": {
            "Vitals": {"old": "SpO2: 92% on 2L NC", "new": "SpO2: 94% on 1L NC", "type": "improved"},
            "Respiratory": {"old": "Wheezing bilateral", "new": "Wheezing decreased, better air movement", "type": "improved"},
            "New Event": {"old": None, "new": "Ambulated 100 feet with PT, tolerated well", "type": "new"},
        }
    },
    {
        "time": "16 hours later (next shift)",
        "duration": "38 sec",
        "changes": {
            "Oxygen": {"old": "1L nasal cannula", "new": "Weaned to room air, maintaining SpO2 95%", "type": "improved"},
            "Medications": {"old": "Prednisone 40mg", "new": "Prednisone 40mg (day 4 of 5, last day tomorrow)", "type": "updated"},
            "Activity": {"old": "Ambulated 100 feet", "new": "Ambulated hallway twice, no SOB", "type": "improved"},
            "New Lab": {"old": None, "new": "WBC down to 9.2 (from 14.5 on admit)", "type": "new"},
        }
    },
    {
        "time": "24 hours later",
        "duration": "52 sec",
        "changes": {
            "Discharge Plan": {"old": "Target 2-3 days", "new": "Likely discharge tomorrow if stable overnight", "type": "updated"},
            "Oxygen": {"old": "Room air, SpO2 95%", "new": "Room air, SpO2 96%, no desaturation with activity", "type": "improved"},
            "Medications": {"old": "Prednisone 40mg", "new": "Completed 5-day course, transition to home inhaler regimen", "type": "updated"},
            "New Order": {"old": None, "new": "Discharge education completed with RN and RT", "type": "new"},
            "Follow-up": {"old": None, "new": "Pulmonology appointment scheduled for Feb 10", "type": "new"},
        }
    }
]

# Intro section
if st.session_state.step == 'intro':
    st.markdown("## The Problem with Traditional Handoffs")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### ❌ Traditional Method
        Every single handoff repeats:
        - Full patient history
        - Complete medication list
        - All vital signs
        - Entire assessment
        - Full plan of care

        **Time Required:** 3-5 minutes EVERY time

        **Issues:**
        - ⏱️ Time-consuming and repetitive
        - 😫 Clinician burnout
        - 🔄 Same info repeated unnecessarily
        - 📉 Important updates get lost in repetition
        """)

    with col2:
        st.markdown(f"""
        ### ✅ Update-Only Model
        **First Handoff (Baseline):**
        - Comprehensive 3-5 minute handoff
        - Stored as patient baseline

        **Subsequent Handoffs:**
        - Only report changes/updates
        - 30-45 seconds
        - What's new, what changed, what's different

        **Benefits:**
        - ⏱️ **85% time reduction**
        - 🎯 **Focus on what matters**
        - 📈 **Highlights important changes**
        - 😊 **Reduces clinician burden**
        """)

    st.markdown("---")

    if st.button("▶️ See It In Action", type="primary", use_container_width=True):
        st.session_state.step = 'baseline'
        st.rerun()

# Baseline creation
elif st.session_state.step == 'baseline':
    st.markdown("## Step 1: Create Comprehensive Baseline Handoff")

    st.info("⏱️ **First handoff for this patient** - Record comprehensive information (3-5 minutes)")

    # Simulate recording
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🎙️ Recording Comprehensive Handoff...")

        if not st.session_state.baseline_created:
            if st.button("🔴 Simulate 3-Minute Recording", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status = st.empty()

                stages = [
                    ("Recording patient demographics and admission info...", 0.15),
                    ("Recording medical history and allergies...", 0.3),
                    ("Recording current medications...", 0.5),
                    ("Recording vital signs and assessment...", 0.7),
                    ("Recording plan of care and disposition...", 0.85),
                    ("Finalizing comprehensive baseline...", 1.0),
                ]

                for stage_text, progress in stages:
                    status.text(stage_text)
                    progress_bar.progress(progress)
                    time.sleep(0.5)

                st.session_state.baseline_created = True
                st.rerun()

    with col2:
        st.markdown("### ⏱️ Timer")
        st.markdown(f"""
        <div class="comparison-box">
            <div style="text-align: center;">
                <div style="font-size: 3rem; color: {PEACOCK_TEAL}; font-weight: bold;">3:42</div>
                <div style="color: #666;">Recording Duration</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.baseline_created:
        st.success("✅ Comprehensive baseline handoff created!")

        st.markdown("---")
        st.markdown("### 📋 Baseline Handoff Content")

        tab1, tab2, tab3, tab4 = st.tabs(["Patient Info", "Medications", "Assessment", "Plan"])

        with tab1:
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Patient", baseline_data["patient_name"])
            with col_b:
                st.metric("MRN", baseline_data["mrn"])
            with col_c:
                st.metric("Age", baseline_data["age"])

            st.markdown("**Diagnosis:**")
            st.markdown(baseline_data["diagnosis"])

            st.markdown("**Medical History:**")
            st.text(baseline_data["history"])

            st.markdown("**Current Vitals:**")
            st.text(baseline_data["vitals"])

        with tab2:
            st.markdown("**Current Medications:**")
            st.text(baseline_data["medications"])

        with tab3:
            st.markdown("**Clinical Assessment:**")
            st.text(baseline_data["assessment"])

        with tab4:
            st.markdown("**Plan of Care:**")
            st.text(baseline_data["plan"])

        st.markdown("---")

        if st.button("➡️ Continue to Update Handoffs", type="primary"):
            st.session_state.step = 'updates'
            st.rerun()

# Update handoffs
elif st.session_state.step == 'updates':
    st.markdown("## Step 2: Subsequent Handoffs - Update Only!")

    st.info("⏱️ **Subsequent handoffs** - Only report what changed (30-45 seconds)")

    # Time savings counter
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Baseline Handoff", "3:42")
    with col2:
        st.metric("Update Handoffs", "3")
    with col3:
        st.metric("Total Update Time", "2:15")
    with col4:
        traditional_time = 222 + (3 * 210)  # baseline + 3 traditional handoffs
        actual_time = 222 + 135  # baseline + updates
        savings = traditional_time - actual_time
        st.metric("Time Saved", f"{savings//60}:{savings%60:02d}", f"-{int(savings/traditional_time*100)}%")

    st.markdown("---")

    # Show updates
    for idx, update in enumerate(updates_data, 1):
        with st.expander(f"🔄 Update #{idx} - {update['time']}", expanded=(idx == 1)):
            col_time, col_content = st.columns([1, 3])

            with col_time:
                st.markdown(f"""
                <div class="comparison-box">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; color: {PEACOCK_TEAL}; font-weight: bold;">{update['duration']}</div>
                        <div style="color: #666; font-size: 0.9rem;">Recording time</div>
                        <div style="margin-top: 1rem; padding: 0.5rem; background: #d1f2eb; border-radius: 4px;">
                            <strong style="color: {PEACOCK_TEAL};">vs 3-5 min</strong><br>
                            <span style="font-size: 0.85rem;">traditional</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_content:
                st.markdown("### Changes Detected:")

                for category, change in update['changes'].items():
                    if change['type'] == 'new':
                        st.markdown(f"""
                        <div class="new">
                            <strong>🟢 NEW - {category}:</strong><br>
                            {change['new']}
                        </div>
                        """, unsafe_allow_html=True)
                    elif change['type'] == 'improved':
                        st.markdown(f"""
                        <div class="changed">
                            <strong>🟡 IMPROVED - {category}:</strong><br>
                            <span style="text-decoration: line-through; color: #666;">{change['old']}</span><br>
                            <strong style="color: {PEACOCK_TEAL};">→ {change['new']}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                    elif change['type'] == 'updated':
                        st.markdown(f"""
                        <div class="changed">
                            <strong>🟡 UPDATED - {category}:</strong><br>
                            <span style="text-decoration: line-through; color: #666;">{change['old']}</span><br>
                            <strong style="color: {PEACOCK_TEAL};">→ {change['new']}</strong>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("**Unchanged (from baseline):**")
                st.markdown(f"""
                <div class="unchanged">
                    <span style="color: #95a5a6;">✓ Patient demographics<br>
                    ✓ Medical history<br>
                    ✓ Allergies<br>
                    ✓ Core medication list (no changes)</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

    # Comparison summary
    st.markdown("## 📊 Time Savings Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ❌ Traditional Model")
        st.markdown("""
        **4 handoffs (admission + 3 shift changes):**
        - Handoff 1: 3:42
        - Handoff 2: 3:30
        - Handoff 3: 3:45
        - Handoff 4: 3:28

        **Total Time: 14:25**
        """)

        st.markdown(f"""
        <div style="background: #e74c3c; color: white; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 1rem;">
            <div style="font-size: 3rem; font-weight: bold;">14:25</div>
            <div style="font-size: 1.2rem;">Total Time Spent</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### ✅ Update-Only Model")
        st.markdown("""
        **4 handoffs (1 baseline + 3 updates):**
        - Baseline: 3:42
        - Update 1: 0:45
        - Update 2: 0:38
        - Update 3: 0:52

        **Total Time: 5:57**
        """)

        st.markdown(f"""
        <div style="background: {PEACOCK_TEAL}; color: white; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 1rem;">
            <div style="font-size: 3rem; font-weight: bold;">5:57</div>
            <div style="font-size: 1.2rem;">Total Time Spent</div>
            <div style="margin-top: 1rem; font-size: 1.5rem; font-weight: bold;">⬇️ 59% REDUCTION</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Annual impact
    st.markdown("## 💰 Annual Impact Calculator")

    col_input1, col_input2, col_input3 = st.columns(3)

    with col_input1:
        handoffs_per_day = st.number_input("Handoffs per Clinician per Day", value=4, min_value=1, max_value=20)

    with col_input2:
        clinicians = st.number_input("Number of Clinicians", value=50, min_value=1, max_value=10000)

    with col_input3:
        days_per_year = st.number_input("Working Days per Year", value=250, min_value=1, max_value=365)

    # Calculate savings
    traditional_minutes_per_handoff = 3.5
    update_minutes_per_handoff = 0.75
    baseline_ratio = 0.25  # 25% are baseline handoffs

    traditional_annual = handoffs_per_day * clinicians * days_per_year * traditional_minutes_per_handoff
    update_annual = handoffs_per_day * clinicians * days_per_year * (
        (baseline_ratio * traditional_minutes_per_handoff) +
        ((1 - baseline_ratio) * update_minutes_per_handoff)
    )

    minutes_saved = traditional_annual - update_annual
    hours_saved = minutes_saved / 60

    col_result1, col_result2, col_result3 = st.columns(3)

    with col_result1:
        st.metric("Minutes Saved Annually", f"{int(minutes_saved):,}")

    with col_result2:
        st.metric("Hours Saved Annually", f"{int(hours_saved):,}")

    with col_result3:
        st.metric("FTE Equivalent", f"{hours_saved / 2080:.1f}")

    st.markdown("---")

    if st.button("🔄 Start Over", use_container_width=True):
        st.session_state.step = 'intro'
        st.session_state.baseline_created = False
        st.session_state.update_created = False
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>EclipseLink AI™</strong> - Update-Only Model for Maximum Efficiency</p>
    <p style="font-size: 0.9rem;">© 2025 Rohimaya Health AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
