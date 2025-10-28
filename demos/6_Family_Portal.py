"""
EclipseLink AI - Family Portal Demo
Plain-language updates for patient families
"""

import streamlit as st
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Family Portal - EclipseLink AI",
    page_icon="👨‍👩‍👧‍👦",
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
    .clinician-view {{
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid {LUNAR_BLUE};
        margin-bottom: 1rem;
    }}
    .family-view {{
        background: #e8f8f5;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid {PEACOCK_TEAL};
        margin-bottom: 1rem;
    }}
    .medical-term {{
        background: #fff3cd;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }}
    .plain-language {{
        background: #d1f2eb;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: bold;
    }}
    .translation-arrow {{
        color: {PEACOCK_TEAL};
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
    }}
    .update-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }}
    .privacy-badge {{
        background: #e74c3c;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
    }}
    .shared-badge {{
        background: {PEACOCK_TEAL};
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>👨‍👩‍👧‍👦 Family Portal Demo</h1>
    <p style="font-size: 1.2rem; margin: 0;">Translating medical jargon into plain language for families</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = "Sarah Johnson"
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "side_by_side"

# Sidebar
with st.sidebar:
    st.image("https://img.shields.io/badge/EclipseLink-AI-1a9b8e?style=for-the-badge", use_container_width=True)
    st.markdown("---")
    st.markdown("### Select Patient")

    patient = st.selectbox(
        "Patient",
        ["Sarah Johnson - Post-Op CABG", "Michael Chen - Heart Attack", "Emma Rodriguez - Diabetes"]
    )

    st.session_state.selected_patient = patient.split(" - ")[0]

    st.markdown("---")
    st.markdown("### View Mode")

    view_mode = st.radio(
        "Display",
        ["Side-by-Side Comparison", "Family View Only", "Translation Examples"],
        index=0
    )

    if view_mode == "Side-by-Side Comparison":
        st.session_state.view_mode = "side_by_side"
    elif view_mode == "Family View Only":
        st.session_state.view_mode = "family_only"
    else:
        st.session_state.view_mode = "examples"

    st.markdown("---")
    st.markdown("### Privacy Controls")
    st.info("""
    **Family Portal respects privacy:**
    - ✅ Vital signs & progress
    - ✅ Procedures & tests
    - ✅ General condition
    - ❌ Specific lab values
    - ❌ Sensitive diagnoses (psych, substance use)
    - ❌ Detailed medication doses
    """)

# Patient data
patients_data = {
    "Sarah Johnson": {
        "mrn": "MRN-123456",
        "age": 68,
        "admission": "Post-op CABG x4",
        "updates": [
            {
                "time": "2 hours ago",
                "clinician": """Patient is hemodynamically stable post-op day 0 CABG x4. Currently intubated and sedated on propofol 20 mcg/kg/min. Vital signs: BP 118/72, HR 78, SpO2 98% on FiO2 40%. Chest tubes draining serosanguinous fluid, 150 mL last hour. Plan to extubate in AM if remains stable overnight.""",
                "family": """Sarah is doing well after her heart bypass surgery today. She is resting comfortably on a breathing machine with medicine to help her sleep peacefully. Her heart and blood pressure are normal and stable. The tubes in her chest are draining fluid as expected. If she continues to do well tonight, we plan to remove the breathing tube in the morning.""",
                "translations": {
                    "hemodynamically stable": "heart and blood pressure are normal and stable",
                    "post-op day 0 CABG x4": "after her heart bypass surgery today",
                    "intubated and sedated": "resting comfortably on a breathing machine with sleep medicine",
                    "propofol 20 mcg/kg/min": "[HIDDEN - specific doses not shared with family]",
                    "BP 118/72, HR 78, SpO2 98%": "her vital signs are normal",
                    "FiO2 40%": "moderate oxygen support",
                    "chest tubes draining serosanguinous fluid": "tubes in her chest are draining fluid as expected",
                    "extubate in AM": "remove the breathing tube in the morning"
                },
                "privacy": "shared"
            },
            {
                "time": "6 hours ago",
                "clinician": """Patient tolerated extubation well. Now on 2L nasal cannula, SpO2 95%. Pain controlled with epidural. Hemoglobin stable at 10.2. Cardiac enzymes trending down appropriately. Ambulated to chair with PT. Continuing DVT prophylaxis with heparin 5000 units SQ Q12H.""",
                "family": """Sarah is breathing on her own now with a little extra oxygen through a small nose tube. Her pain is well-managed. Her blood levels are stable and her heart markers are improving as expected. She was able to sit in a chair with help from the physical therapist today. She's receiving medicine to prevent blood clots.""",
                "translations": {
                    "tolerated extubation well": "breathing on her own now",
                    "2L nasal cannula": "small nose tube with a little extra oxygen",
                    "SpO2 95%": "oxygen levels are good",
                    "epidural": "special pain medicine",
                    "Hemoglobin stable at 10.2": "[HIDDEN - specific lab values not shared]",
                    "Cardiac enzymes trending down": "heart markers are improving as expected",
                    "Ambulated to chair with PT": "able to sit in a chair with help from physical therapist",
                    "DVT prophylaxis with heparin": "medicine to prevent blood clots",
                    "5000 units SQ Q12H": "[HIDDEN - specific doses not shared]"
                },
                "privacy": "shared"
            }
        ]
    },
    "Michael Chen": {
        "mrn": "MRN-789012",
        "age": 45,
        "admission": "STEMI (Heart Attack)",
        "updates": [
            {
                "time": "3 hours ago",
                "clinician": """Patient status post emergent cardiac catheterization with successful PCI to RCA. Door-to-balloon time 62 minutes. Single drug-eluting stent placed. TIMI 3 flow restored. Currently on aspirin 81mg, ticagrelor 90mg BID, atorvastatin 80mg. Troponin peaked at 12.4, now trending down. Patient asymptomatic, no chest pain. Telemetry monitoring shows normal sinus rhythm. Plan for echo in AM and discharge tomorrow if stable.""",
                "family": """Michael had an emergency heart procedure where doctors opened his blocked artery and placed a small mesh tube (stent) to keep it open. The procedure was successful and blood flow is back to normal. He's taking medicines to prevent blood clots and protect his heart. His heart markers are improving and he has no chest pain. His heart rhythm is normal. We're planning an ultrasound of his heart tomorrow morning, and if everything looks good, he may go home tomorrow.""",
                "translations": {
                    "status post emergent cardiac catheterization": "had an emergency heart procedure",
                    "successful PCI to RCA": "opened his blocked artery",
                    "Door-to-balloon time 62 minutes": "[Technical detail - not relevant to family]",
                    "drug-eluting stent": "small mesh tube (stent) to keep it open",
                    "TIMI 3 flow restored": "blood flow is back to normal",
                    "aspirin 81mg, ticagrelor 90mg BID, atorvastatin 80mg": "medicines to prevent blood clots and protect his heart",
                    "Troponin peaked at 12.4": "[HIDDEN - specific lab values]",
                    "asymptomatic": "has no chest pain",
                    "Telemetry monitoring shows normal sinus rhythm": "heart rhythm is normal",
                    "echo": "ultrasound of his heart"
                },
                "privacy": "shared"
            },
            {
                "time": "1 day ago",
                "clinician": """Patient admitted via EMS with acute inferior STEMI. Presented with 9/10 substernal chest pain radiating to left arm. EKG with ST elevations in II, III, AVF. Initial troponin 2.4. Started on dual antiplatelet therapy and heparin drip. Cath lab activated.""",
                "family": """Michael was brought in by ambulance with severe chest pain going down his left arm. Tests showed he was having a heart attack affecting the bottom part of his heart. He was given medicines immediately to prevent blood clots, and the heart catheterization team was called in right away.""",
                "translations": {
                    "admitted via EMS": "brought in by ambulance",
                    "acute inferior STEMI": "heart attack affecting the bottom part of his heart",
                    "9/10 substernal chest pain radiating to left arm": "severe chest pain going down his left arm",
                    "EKG with ST elevations in II, III, AVF": "tests showed he was having a heart attack",
                    "Initial troponin 2.4": "[HIDDEN - specific lab values]",
                    "dual antiplatelet therapy": "medicines to prevent blood clots",
                    "heparin drip": "blood thinner through IV",
                    "Cath lab activated": "heart catheterization team was called in"
                },
                "privacy": "shared"
            }
        ]
    },
    "Emma Rodriguez": {
        "mrn": "MRN-334455",
        "age": 8,
        "admission": "Diabetic Ketoacidosis (DKA)",
        "updates": [
            {
                "time": "4 hours ago",
                "clinician": """Pediatric patient with DKA now improving. pH increased from 7.08 to 7.28. Anion gap closed from 28 to 14. Glucose down to 220 on insulin drip at 0.08 U/kg/hr. Tolerating PO fluids. Alert and oriented. Transition to SQ insulin planned for tomorrow. Diabetes education ongoing with parents.""",
                "family": """Emma is doing much better! Her body's acid levels have improved significantly, and her blood sugar is coming down to a safer range with the insulin medicine. She's able to drink fluids and is alert and talking. Tomorrow, we plan to switch from IV insulin to insulin shots. Our diabetes nurse has been teaching you and your family how to manage her diabetes at home.""",
                "translations": {
                    "Pediatric patient with DKA": "Emma's diabetic ketoacidosis",
                    "pH increased from 7.08 to 7.28": "her body's acid levels have improved significantly",
                    "Anion gap closed from 28 to 14": "[Technical detail - simplified to 'improving']",
                    "Glucose down to 220 on insulin drip": "blood sugar is coming down to a safer range with insulin medicine",
                    "0.08 U/kg/hr": "[HIDDEN - specific doses]",
                    "Tolerating PO fluids": "able to drink fluids",
                    "Alert and oriented": "alert and talking",
                    "Transition to SQ insulin": "switch from IV insulin to insulin shots",
                    "Diabetes education ongoing": "diabetes nurse has been teaching you"
                },
                "privacy": "shared"
            }
        ]
    }
}

# Main content
selected_patient_name = st.session_state.selected_patient
patient_data = patients_data[selected_patient_name]

# Patient header
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Patient", selected_patient_name)
with col2:
    st.metric("MRN", patient_data["mrn"])
with col3:
    st.metric("Age", patient_data["age"])
with col4:
    st.metric("Admission", patient_data["admission"])

st.markdown("---")

# View modes
if st.session_state.view_mode == "side_by_side":
    st.markdown("## Side-by-Side Comparison")
    st.info("Compare how the same clinical information is presented to clinicians vs. families")

    for update in patient_data["updates"]:
        st.markdown(f"### Update from {update['time']}")

        col_clinician, col_arrow, col_family = st.columns([5, 1, 5])

        with col_clinician:
            st.markdown("#### 👨‍⚕️ Clinician View")
            st.markdown(f"""
            <div class="clinician-view">
                <strong>Medical Documentation:</strong><br><br>
                {update['clinician']}
            </div>
            """, unsafe_allow_html=True)

        with col_arrow:
            st.markdown("""
            <div class="translation-arrow">
                ➡️<br>
                <span style="font-size: 0.8rem; color: #666;">AI Translation</span>
            </div>
            """, unsafe_allow_html=True)

        with col_family:
            st.markdown("#### 👨‍👩‍👧‍👦 Family Portal View")
            st.markdown(f"""
            <div class="family-view">
                <strong>Plain Language Update:</strong><br><br>
                {update['family']}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

elif st.session_state.view_mode == "family_only":
    st.markdown("## 👨‍👩‍👧‍👦 Family Portal View")
    st.success("This is what family members see when they log in to the Family Portal")

    # Mobile-like interface
    st.markdown(f"""
    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); padding: 1.5rem;">
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, {PEACOCK_TEAL}, {LUNAR_BLUE}); border-radius: 10px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0;">Updates for {selected_patient_name}</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
    """, unsafe_allow_html=True)

    for update in patient_data["updates"]:
        st.markdown(f"""
        <div class="update-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div style="font-weight: bold; color: {PEACOCK_TEAL};">📋 {update['time']}</div>
                <span class="shared-badge">✓ SHARED</span>
            </div>
            <div style="line-height: 1.8; color: #333;">
                {update['family']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Family portal features
    st.markdown("### Family Portal Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **📱 Mobile Access**
        - iOS & Android apps
        - Responsive web design
        - Real-time notifications
        - Secure login
        """)

    with col2:
        st.markdown("""
        **🔒 Privacy & Security**
        - HIPAA compliant
        - Patient consent required
        - Granular sharing controls
        - Audit trail of all access
        """)

    with col3:
        st.markdown("""
        **🌐 Language Options**
        - Translate to 50+ languages
        - Cultural sensitivity
        - Reading level adjustment
        - Text-to-speech support
        """)

elif st.session_state.view_mode == "examples":
    st.markdown("## 📚 Translation Examples")
    st.info("See how EclipseLink AI translates medical terminology into plain language")

    # Show translation dictionary
    all_translations = {}
    for update in patient_data["updates"]:
        all_translations.update(update["translations"])

    st.markdown("### Medical Term → Plain Language")

    for medical, plain in all_translations.items():
        if "[HIDDEN" not in plain:
            col1, col2, col3 = st.columns([2, 1, 2])

            with col1:
                st.markdown(f"""
                <div class="medical-term">
                    {medical}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div style="text-align: center; color: {PEACOCK_TEAL}; font-size: 1.5rem;">
                    →
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="plain-language">
                    {plain}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
        else:
            # Show privacy-filtered items
            st.markdown(f"""
            <div style="background: #ffe6e6; padding: 0.75rem; border-radius: 8px; border-left: 4px solid #e74c3c; margin-bottom: 0.5rem;">
                <strong style="color: #c0392b;">🔒 Privacy Filtered:</strong> {medical}<br>
                <span style="font-size: 0.9rem; color: #666;">{plain}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Common medical terms reference
    st.markdown("### 📖 Common Medical Terms Reference")

    reference_terms = {
        "Vitals & Measurements": {
            "BP (Blood Pressure)": "How hard the heart is pumping blood",
            "HR (Heart Rate)": "How fast the heart is beating",
            "SpO2": "Oxygen level in the blood",
            "Temperature": "Body temperature",
            "Respiratory rate": "How fast you're breathing"
        },
        "Procedures": {
            "Intubation": "Putting in a breathing tube",
            "Extubation": "Removing the breathing tube",
            "Catheterization": "Inserting a small tube for treatment or testing",
            "Biopsy": "Taking a small tissue sample for testing",
            "MRI/CT scan": "Special pictures of the inside of the body"
        },
        "Medications": {
            "Antibiotic": "Medicine to fight infection",
            "Analgesic": "Pain medicine",
            "Anticoagulant": "Blood thinner to prevent clots",
            "Diuretic": "Medicine to remove excess fluid (water pill)",
            "IV": "Medicine given through a vein"
        },
        "Conditions": {
            "Hypertension": "High blood pressure",
            "Tachycardia": "Fast heart rate",
            "Hypoxia": "Low oxygen levels",
            "Edema": "Swelling from fluid buildup",
            "Arrhythmia": "Irregular heartbeat"
        }
    }

    for category, terms in reference_terms.items():
        with st.expander(f"📚 {category}"):
            for medical, plain in terms.items():
                st.markdown(f"**{medical}:** {plain}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>EclipseLink AI™</strong> - Bridging the Communication Gap Between Clinicians and Families</p>
    <p style="font-size: 0.9rem;">© 2025 Rohimaya Health AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
