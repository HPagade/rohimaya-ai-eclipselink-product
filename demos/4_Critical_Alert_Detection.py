"""
EclipseLink AI - Critical Alert Detection Demo
Shows how AI automatically flags critical values in handoffs
"""

import streamlit as st
import time
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Critical Alert Detection - EclipseLink AI",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand colors
PEACOCK_TEAL = "#1a9b8e"
PHOENIX_GOLD = "#f4c430"
LUNAR_BLUE = "#2c3e50"
ECLIPSE_NAVY = "#1a2332"
ALERT_RED = "#e74c3c"
ALERT_YELLOW = "#f39c12"
ALERT_GREEN = "#2ecc71"

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
    .alert-critical {{
        background-color: {ALERT_RED};
        color: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 6px solid #c0392b;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
    }}
    .alert-warning {{
        background-color: {ALERT_YELLOW};
        color: {ECLIPSE_NAVY};
        padding: 1rem;
        border-radius: 8px;
        border-left: 6px solid #e67e22;
        margin-bottom: 1rem;
    }}
    .alert-normal {{
        background-color: #ecf0f1;
        color: {ECLIPSE_NAVY};
        padding: 1rem;
        border-radius: 8px;
        border-left: 6px solid {PEACOCK_TEAL};
        margin-bottom: 1rem;
    }}
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    .vital-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }}
    .critical-badge {{
        background-color: {ALERT_RED};
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }}
    .warning-badge {{
        background-color: {ALERT_YELLOW};
        color: {ECLIPSE_NAVY};
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }}
    .normal-badge {{
        background-color: {ALERT_GREEN};
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚨 Critical Alert Detection Demo</h1>
    <p style="font-size: 1.2rem; margin: 0;">AI automatically identifies and flags critical values in patient handoffs</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Sidebar
with st.sidebar:
    st.image("https://img.shields.io/badge/EclipseLink-AI-1a9b8e?style=for-the-badge", use_container_width=True)
    st.markdown("---")
    st.markdown("### Demo Controls")

    scenario = st.selectbox(
        "Select Patient Scenario",
        ["ICU - Septic Shock", "Cardiac - STEMI", "Trauma - Major Hemorrhage", "Pediatric - Critical Labs"]
    )

    st.markdown("---")
    st.markdown("### About This Demo")
    st.info("""
    This demo shows how EclipseLink AI:
    - Detects critical vital signs
    - Flags abnormal lab values
    - Identifies high-risk medications
    - Alerts for code status changes
    - Monitors fall risk
    """)

    if st.button("Reset Demo", type="secondary"):
        st.session_state.analyzed = False
        st.session_state.alerts = []
        st.rerun()

# Sample data for different scenarios
scenarios = {
    "ICU - Septic Shock": {
        "transcript": """This is a handoff for Marcus Thompson, 58-year-old male, MRN-445566, admitted to ICU
with septic shock secondary to pneumonia. Patient became hypotensive overnight with systolic BP
dropping to 68 over 40. Started on norepinephrine at 15 micrograms per minute. Heart rate is
tachycardic at 142 beats per minute. Temperature spiked to 103.8 degrees Fahrenheit. Oxygen
saturation is 88% on 100% FiO2 via ventilator. Most recent lactate came back at 5.2. White blood
cell count is critically elevated at 24,000. Platelets dropped to 45,000. INR is 2.8. Patient is
on heparin drip for DVT prophylaxis. Potassium came back at 6.2, we've given kayexalate. Blood
cultures pending. Started broad spectrum antibiotics - vancomycin and piperacillin-tazobactam.
Patient is sedated on propofol and fentanyl. Family aware of critical status, full code status.""",
        "patient_name": "Marcus Thompson",
        "mrn": "MRN-445566",
        "age": 58,
        "vitals": {
            "BP": {"value": "68/40", "normal": "90-140/60-90", "status": "critical"},
            "HR": {"value": "142", "normal": "60-100", "status": "critical"},
            "Temp": {"value": "103.8°F", "normal": "97-99°F", "status": "critical"},
            "SpO2": {"value": "88%", "normal": ">92%", "status": "critical"},
        },
        "labs": {
            "Lactate": {"value": "5.2", "normal": "<2.0", "unit": "mmol/L", "status": "critical"},
            "WBC": {"value": "24,000", "normal": "4,000-11,000", "unit": "/μL", "status": "critical"},
            "Platelets": {"value": "45,000", "normal": "150,000-400,000", "unit": "/μL", "status": "critical"},
            "K+": {"value": "6.2", "normal": "3.5-5.0", "unit": "mEq/L", "status": "critical"},
            "INR": {"value": "2.8", "normal": "0.8-1.2", "unit": "", "status": "warning"},
        },
        "medications": [
            {"name": "Norepinephrine", "dose": "15 mcg/min", "risk": "critical"},
            {"name": "Heparin", "dose": "Continuous drip", "risk": "critical"},
            {"name": "Vancomycin", "dose": "Loading dose", "risk": "warning"},
            {"name": "Piperacillin-Tazobactam", "dose": "Standard", "risk": "normal"},
        ],
        "alerts": [
            {"type": "critical", "category": "Vital Signs", "message": "Severe Hypotension: BP 68/40 (Shock range)"},
            {"type": "critical", "category": "Vital Signs", "message": "Severe Tachycardia: HR 142 (>140 threshold)"},
            {"type": "critical", "category": "Vital Signs", "message": "High Fever: Temperature 103.8°F"},
            {"type": "critical", "category": "Vital Signs", "message": "Critical Hypoxemia: SpO2 88% on 100% FiO2"},
            {"type": "critical", "category": "Lab Values", "message": "Elevated Lactate: 5.2 mmol/L (indicates poor perfusion)"},
            {"type": "critical", "category": "Lab Values", "message": "Severe Leukocytosis: WBC 24,000 (sepsis indicator)"},
            {"type": "critical", "category": "Lab Values", "message": "Critical Thrombocytopenia: Platelets 45,000 (bleeding risk)"},
            {"type": "critical", "category": "Lab Values", "message": "Severe Hyperkalemia: K+ 6.2 (cardiac arrest risk)"},
            {"type": "warning", "category": "Lab Values", "message": "Elevated INR: 2.8 with heparin (bleeding risk)"},
            {"type": "critical", "category": "Medications", "message": "High-dose vasopressor: Norepinephrine 15 mcg/min"},
            {"type": "critical", "category": "Medications", "message": "Anticoagulation: Heparin + elevated INR (hemorrhage risk)"},
        ]
    },
    "Cardiac - STEMI": {
        "transcript": """This is Michael Chen, 45-year-old male, MRN-789012, presenting with acute STEMI.
Patient has severe substernal chest pain 9 out of 10. Blood pressure is elevated at 178 over 105.
Heart rate 105, regular rhythm. EKG shows ST elevations in leads two, three, and AVF. Troponin
critically elevated at 8.4. Got aspirin 325 milligrams, plavix 600 milligram loading dose. Started
heparin bolus 80 units per kilogram then 18 units per kilogram per hour drip. Given morphine 4
milligrams IV for pain. Oxygen saturation 94% on room air. Potassium is 5.8. Cath lab activated,
team is ready. Interventional cardiologist Dr. Williams on the way. Patient consented, family present
and aware. Full code status confirmed.""",
        "patient_name": "Michael Chen",
        "mrn": "MRN-789012",
        "age": 45,
        "vitals": {
            "BP": {"value": "178/105", "normal": "90-140/60-90", "status": "warning"},
            "HR": {"value": "105", "normal": "60-100", "status": "warning"},
            "Temp": {"value": "98.6°F", "normal": "97-99°F", "status": "normal"},
            "SpO2": {"value": "94%", "normal": ">92%", "status": "normal"},
            "Pain": {"value": "9/10", "normal": "<4/10", "status": "critical"},
        },
        "labs": {
            "Troponin": {"value": "8.4", "normal": "<0.04", "unit": "ng/mL", "status": "critical"},
            "K+": {"value": "5.8", "normal": "3.5-5.0", "unit": "mEq/L", "status": "warning"},
        },
        "medications": [
            {"name": "Aspirin", "dose": "325 mg", "risk": "warning"},
            {"name": "Plavix (Clopidogrel)", "dose": "600 mg loading", "risk": "critical"},
            {"name": "Heparin", "dose": "80 U/kg bolus + drip", "risk": "critical"},
            {"name": "Morphine", "dose": "4 mg IV", "risk": "warning"},
        ],
        "alerts": [
            {"type": "critical", "category": "Cardiac", "message": "STEMI Alert: ST elevations in leads II, III, AVF (Inferior MI)"},
            {"type": "critical", "category": "Lab Values", "message": "Severely elevated Troponin: 8.4 ng/mL (210x normal)"},
            {"type": "critical", "category": "Vital Signs", "message": "Severe chest pain: 9/10 (ischemia indicator)"},
            {"type": "warning", "category": "Vital Signs", "message": "Hypertensive: BP 178/105"},
            {"type": "warning", "category": "Vital Signs", "message": "Tachycardia: HR 105"},
            {"type": "warning", "category": "Lab Values", "message": "Elevated Potassium: 5.8 mEq/L"},
            {"type": "critical", "category": "Medications", "message": "Triple anticoagulation/antiplatelet: Aspirin + Plavix + Heparin (bleeding risk)"},
            {"type": "critical", "category": "Procedure", "message": "Cath lab activated - Emergent PCI required"},
        ]
    },
    "Trauma - Major Hemorrhage": {
        "transcript": """Trauma alert, 28-year-old female, Jane Morrison, MRN-998877, motor vehicle collision
with ejection. GCS 12 on scene, now intubated. Blood pressure unstable, currently 82 over 50 on
two liters of crystalloid. Heart rate 135. FAST exam positive for intraabdominal free fluid.
Hemoglobin dropped from 12.8 to 7.2 in last hour. Massive transfusion protocol activated. Given
two units packed red blood cells, two units FFP, one unit platelets. INR is 1.8. Lactate 4.5.
Base deficit negative 8. Pelvis unstable on exam, binder applied. Left femur deformity, traction
splint placed. Right pneumothorax, chest tube placed with 400 mL blood output. Trauma surgery
taking to OR emergently for exploratory laparotomy. Orthopedics aware for pelvic and femur
fixation. Patient on fentanyl and versed drips. Family notified, en route to hospital.""",
        "patient_name": "Jane Morrison",
        "mrn": "MRN-998877",
        "age": 28,
        "vitals": {
            "BP": {"value": "82/50", "normal": "90-140/60-90", "status": "critical"},
            "HR": {"value": "135", "normal": "60-100", "status": "critical"},
            "GCS": {"value": "12", "normal": "15", "status": "warning"},
        },
        "labs": {
            "Hemoglobin": {"value": "7.2", "normal": "12-16", "unit": "g/dL", "status": "critical"},
            "Lactate": {"value": "4.5", "normal": "<2.0", "unit": "mmol/L", "status": "critical"},
            "Base Deficit": {"value": "-8", "normal": "-2 to +2", "unit": "mEq/L", "status": "critical"},
            "INR": {"value": "1.8", "normal": "0.8-1.2", "unit": "", "status": "warning"},
        },
        "medications": [
            {"name": "Packed RBCs", "dose": "2 units", "risk": "critical"},
            {"name": "Fresh Frozen Plasma", "dose": "2 units", "risk": "critical"},
            {"name": "Platelets", "dose": "1 unit", "risk": "warning"},
            {"name": "Fentanyl drip", "dose": "Continuous", "risk": "warning"},
        ],
        "alerts": [
            {"type": "critical", "category": "Trauma", "message": "Massive transfusion protocol activated"},
            {"type": "critical", "category": "Vital Signs", "message": "Hemorrhagic shock: BP 82/50 despite 2L fluids"},
            {"type": "critical", "category": "Vital Signs", "message": "Severe tachycardia: HR 135"},
            {"type": "critical", "category": "Lab Values", "message": "Severe anemia: Hemoglobin 7.2 (dropped 5.6 in 1 hour)"},
            {"type": "critical", "category": "Lab Values", "message": "Elevated lactate: 4.5 (shock indicator)"},
            {"type": "critical", "category": "Lab Values", "message": "Severe base deficit: -8 (metabolic acidosis)"},
            {"type": "critical", "category": "Imaging", "message": "FAST positive: Intraabdominal hemorrhage"},
            {"type": "critical", "category": "Injury", "message": "Pneumothorax with 400mL hemothorax"},
            {"type": "critical", "category": "Injury", "message": "Unstable pelvis fracture (high mortality risk)"},
            {"type": "critical", "category": "Procedure", "message": "Emergent OR: Exploratory laparotomy"},
        ]
    },
    "Pediatric - Critical Labs": {
        "transcript": """This is 8-year-old Emma Rodriguez, MRN-334455, admitted with diabetic ketoacidosis.
Patient presented with 3 days of vomiting, polyuria, and altered mental status. Initial glucose
was 642. pH is 7.08, critically acidotic. Bicarbonate is 8. Anion gap 28. Potassium initially
5.9, now 3.2 after fluid resuscitation. Started on insulin drip at 0.1 units per kilogram per
hour. Patient is on two liters of normal saline with 40 milliequivalents of potassium chloride.
Weight is 25 kilograms. Patient lethargic but arousable, responding to questions. No signs of
cerebral edema currently. Blood pressure 95 over 60, heart rate 118. Oxygen saturation 98% on
room air. Neurological checks every hour. Endocrinology consulted and following. Parents at
bedside, very anxious. Patient is full code.""",
        "patient_name": "Emma Rodriguez",
        "mrn": "MRN-334455",
        "age": 8,
        "vitals": {
            "BP": {"value": "95/60", "normal": "90-110/55-75 (peds)", "status": "normal"},
            "HR": {"value": "118", "normal": "70-110 (peds)", "status": "warning"},
            "SpO2": {"value": "98%", "normal": ">92%", "status": "normal"},
            "Mental Status": {"value": "Lethargic", "normal": "Alert", "status": "warning"},
        },
        "labs": {
            "Glucose": {"value": "642", "normal": "70-100", "unit": "mg/dL", "status": "critical"},
            "pH": {"value": "7.08", "normal": "7.35-7.45", "unit": "", "status": "critical"},
            "Bicarbonate": {"value": "8", "normal": "22-26", "unit": "mEq/L", "status": "critical"},
            "Anion Gap": {"value": "28", "normal": "3-11", "unit": "mEq/L", "status": "critical"},
            "K+ (Initial)": {"value": "5.9", "normal": "3.5-5.0", "unit": "mEq/L", "status": "warning"},
            "K+ (Current)": {"value": "3.2", "normal": "3.5-5.0", "unit": "mEq/L", "status": "warning"},
        },
        "medications": [
            {"name": "Insulin drip", "dose": "0.1 U/kg/hr (2.5 U/hr)", "risk": "critical"},
            {"name": "Normal Saline", "dose": "2L with KCl 40 mEq", "risk": "warning"},
        ],
        "alerts": [
            {"type": "critical", "category": "Diagnosis", "message": "Diabetic Ketoacidosis (DKA) - Life threatening"},
            {"type": "critical", "category": "Lab Values", "message": "Severe hyperglycemia: Glucose 642 mg/dL"},
            {"type": "critical", "category": "Lab Values", "message": "Severe acidosis: pH 7.08 (critical)"},
            {"type": "critical", "category": "Lab Values", "message": "Severe metabolic acidosis: Bicarbonate 8"},
            {"type": "critical", "category": "Lab Values", "message": "Elevated anion gap: 28 (DKA indicator)"},
            {"type": "warning", "category": "Lab Values", "message": "Hypokalemia developing: K+ dropped from 5.9 to 3.2"},
            {"type": "critical", "category": "Medications", "message": "Insulin drip in pediatric patient - Tight monitoring required"},
            {"type": "critical", "category": "Neuro", "message": "Altered mental status - Monitor for cerebral edema (DKA complication)"},
            {"type": "warning", "category": "Pediatric", "message": "8-year-old patient - Weight-based dosing critical"},
        ]
    }
}

# Main content
selected_data = scenarios[scenario]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Patient", selected_data["patient_name"])
with col2:
    st.metric("MRN", selected_data["mrn"])
with col3:
    st.metric("Age", f"{selected_data['age']} years old")

st.markdown("---")

# Step 1: Voice Recording
st.markdown("## Step 1: Upload Voice Recording")
st.text_area("Recorded Handoff Transcript", value=selected_data["transcript"], height=200, disabled=True)

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🎙️ Record New Handoff", use_container_width=True):
        st.info("Recording feature simulated for demo")

with col_btn2:
    if st.button("🔍 Analyze for Critical Alerts", type="primary", use_container_width=True):
        with st.spinner("Analyzing transcript for critical values..."):
            time.sleep(2)
        st.session_state.analyzed = True
        st.session_state.alerts = selected_data["alerts"]
        st.rerun()

if st.session_state.analyzed:
    st.markdown("---")
    st.markdown("## Step 2: AI Analysis Results")

    # Summary metrics
    critical_count = len([a for a in st.session_state.alerts if a["type"] == "critical"])
    warning_count = len([a for a in st.session_state.alerts if a["type"] == "warning"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Alerts", len(st.session_state.alerts))
    with col2:
        st.metric("🔴 Critical", critical_count)
    with col3:
        st.metric("🟡 Warnings", warning_count)
    with col4:
        st.metric("Analysis Time", "2.3 sec")

    st.markdown("---")

    # Detailed alerts
    st.markdown("### 🚨 Critical Alerts Detected")

    # Filter options
    filter_category = st.multiselect(
        "Filter by Category",
        options=["All"] + list(set([a["category"] for a in st.session_state.alerts])),
        default=["All"]
    )

    for alert in st.session_state.alerts:
        if "All" not in filter_category and alert["category"] not in filter_category:
            continue

        if alert["type"] == "critical":
            alert_class = "alert-critical"
            icon = "🔴"
            badge_class = "critical-badge"
        elif alert["type"] == "warning":
            alert_class = "alert-warning"
            icon = "🟡"
            badge_class = "warning-badge"
        else:
            alert_class = "alert-normal"
            icon = "🟢"
            badge_class = "normal-badge"

        st.markdown(f"""
        <div class="{alert_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <strong>{icon} {alert["category"]}</strong>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">{alert["message"]}</p>
                </div>
                <span class="{badge_class}">{alert["type"].upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Vital Signs Summary
    st.markdown("### 📊 Vital Signs Summary")

    cols = st.columns(len(selected_data["vitals"]))
    for idx, (vital_name, vital_data) in enumerate(selected_data["vitals"].items()):
        with cols[idx]:
            if vital_data["status"] == "critical":
                color = ALERT_RED
                icon = "🔴"
            elif vital_data["status"] == "warning":
                color = ALERT_YELLOW
                icon = "🟡"
            else:
                color = ALERT_GREEN
                icon = "🟢"

            st.markdown(f"""
            <div class="vital-card" style="border-top: 4px solid {color};">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="font-weight: bold; margin: 0.5rem 0;">{vital_name}</div>
                <div style="font-size: 1.5rem; color: {color}; font-weight: bold;">{vital_data["value"]}</div>
                <div style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Normal: {vital_data["normal"]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Lab Values
    st.markdown("### 🔬 Laboratory Values")

    lab_cols = st.columns(min(3, len(selected_data["labs"])))
    for idx, (lab_name, lab_data) in enumerate(selected_data["labs"].items()):
        col_idx = idx % 3
        with lab_cols[col_idx]:
            if lab_data["status"] == "critical":
                color = ALERT_RED
                icon = "🔴"
            elif lab_data["status"] == "warning":
                color = ALERT_YELLOW
                icon = "🟡"
            else:
                color = ALERT_GREEN
                icon = "🟢"

            st.markdown(f"""
            <div class="vital-card" style="border-top: 4px solid {color}; margin-bottom: 1rem;">
                <div style="font-size: 1.2rem;">{icon}</div>
                <div style="font-weight: bold; margin: 0.5rem 0;">{lab_name}</div>
                <div style="font-size: 1.3rem; color: {color}; font-weight: bold;">{lab_data["value"]} {lab_data["unit"]}</div>
                <div style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Normal: {lab_data["normal"]} {lab_data["unit"]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # High-Risk Medications
    st.markdown("### 💊 High-Risk Medications")

    for med in selected_data["medications"]:
        if med["risk"] == "critical":
            color = ALERT_RED
            icon = "🔴"
        elif med["risk"] == "warning":
            color = ALERT_YELLOW
            icon = "🟡"
        else:
            color = ALERT_GREEN
            icon = "🟢"

        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid {color}; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: between; align-items: center;">
                <div style="flex: 1;">
                    <strong>{icon} {med["name"]}</strong>
                    <p style="margin: 0.25rem 0 0 0; color: #666;">{med["dose"]}</p>
                </div>
                <span style="background: {color}; color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.85rem; font-weight: bold;">
                    {med["risk"].upper()}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Actions
    st.markdown("### 🎯 Recommended Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📢 Send to Team", use_container_width=True, type="primary"):
            st.success("✅ Critical alerts sent to care team!")

    with col2:
        if st.button("📱 Page Physician", use_container_width=True):
            st.success("✅ Physician paged!")

    with col3:
        if st.button("📋 Generate SBAR", use_container_width=True):
            st.success("✅ SBAR report generated with critical alerts highlighted!")

    with col4:
        if st.button("🏥 Send to EHR", use_container_width=True):
            st.success("✅ Alerts documented in EHR!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>EclipseLink AI™</strong> - Intelligent Critical Alert Detection</p>
    <p style="font-size: 0.9rem;">© 2025 Rohimaya Health AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
