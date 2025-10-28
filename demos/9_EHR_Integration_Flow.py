"""
EclipseLink AI - EHR Integration Flow Demo
Demonstrates seamless integration with Epic, Cerner, and MEDITECH
"""

import streamlit as st
import json
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="EHR Integration Flow - EclipseLink AI",
    page_icon="🏥",
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
    .integration-step {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 6px solid {PEACOCK_TEAL};
    }}
    .step-number {{
        background: {PEACOCK_TEAL};
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
        margin-right: 1rem;
    }}
    .data-flow {{
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 8px;
        text-align: center;
        margin: 2rem 0;
    }}
    .flow-box {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        display: inline-block;
        min-width: 150px;
    }}
    .flow-arrow {{
        color: {PEACOCK_TEAL};
        font-size: 2rem;
        font-weight: bold;
        margin: 0 1rem;
    }}
    .json-viewer {{
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        overflow-x: auto;
        max-height: 400px;
        overflow-y: auto;
    }}
    .hl7-message {{
        background: #1e1e1e;
        color: #4ec9b0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
        overflow-x: auto;
    }}
    .success-badge {{
        background: #2ecc71;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
    }}
    .config-card {{
        background: #e8f8f5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid {PEACOCK_TEAL};
        margin-bottom: 0.5rem;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏥 EHR Integration Flow Demo</h1>
    <p style="font-size: 1.2rem; margin: 0;">Seamless bi-directional integration with Epic, Cerner, and MEDITECH</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'integration_step' not in st.session_state:
    st.session_state.integration_step = 0
if 'data_pulled' not in st.session_state:
    st.session_state.data_pulled = False
if 'sbar_created' not in st.session_state:
    st.session_state.sbar_created = False
if 'data_pushed' not in st.session_state:
    st.session_state.data_pushed = False

# Sidebar
with st.sidebar:
    st.image("https://img.shields.io/badge/EclipseLink-AI-1a9b8e?style=for-the-badge", use_container_width=True)
    st.markdown("---")
    st.markdown("### Select EHR System")

    ehr_system = st.selectbox(
        "EHR Platform",
        ["Epic", "Cerner", "MEDITECH"]
    )

    st.markdown("---")
    st.markdown("### Integration Methods")
    st.info("""
    **FHIR R4 (Recommended):**
    - Modern REST API
    - JSON format
    - OAuth 2.0 authentication
    - Real-time access

    **HL7 v2.x (Legacy):**
    - Message-based
    - Pipe-delimited format
    - TCP/IP or MLLP
    - Batch processing
    """)

    st.markdown("---")
    st.markdown("### Supported Data")
    st.success("""
    **Pull from EHR:**
    ✅ Patient demographics
    ✅ Medications
    ✅ Allergies
    ✅ Lab results
    ✅ Vital signs
    ✅ Problem list
    ✅ Recent notes

    **Push to EHR:**
    ✅ SBAR reports
    ✅ Handoff documentation
    ✅ Clinical notes
    """)

    if st.button("Reset Demo", type="secondary"):
        st.session_state.integration_step = 0
        st.session_state.data_pulled = False
        st.session_state.sbar_created = False
        st.session_state.data_pushed = False
        st.rerun()

# Sample FHIR data
fhir_patient = {
    "resourceType": "Patient",
    "id": "example-patient-123",
    "identifier": [
        {
            "use": "usual",
            "type": {"text": "MRN"},
            "system": "urn:oid:2.16.840.1.113883.19.5",
            "value": "MRN-123456"
        }
    ],
    "active": True,
    "name": [
        {
            "use": "official",
            "family": "Johnson",
            "given": ["Sarah", "Marie"]
        }
    ],
    "gender": "female",
    "birthDate": "1957-03-15",
    "address": [
        {
            "use": "home",
            "line": ["123 Main Street"],
            "city": "Springfield",
            "state": "IL",
            "postalCode": "62701"
        }
    ]
}

fhir_medication = {
    "resourceType": "MedicationRequest",
    "id": "med-example-001",
    "status": "active",
    "intent": "order",
    "medicationCodeableConcept": {
        "coding": [
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "197361",
                "display": "Metoprolol Tartrate 25 MG Oral Tablet"
            }
        ],
        "text": "Metoprolol 25mg PO BID"
    },
    "subject": {
        "reference": "Patient/example-patient-123",
        "display": "Sarah Johnson"
    },
    "dosageInstruction": [
        {
            "text": "Take 25mg by mouth twice daily",
            "timing": {
                "repeat": {
                    "frequency": 2,
                    "period": 1,
                    "periodUnit": "d"
                }
            }
        }
    ]
}

fhir_allergy = {
    "resourceType": "AllergyIntolerance",
    "id": "allergy-example-001",
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                "code": "active"
            }
        ]
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                "code": "confirmed"
            }
        ]
    },
    "type": "allergy",
    "category": ["medication"],
    "criticality": "high",
    "code": {
        "coding": [
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "7980",
                "display": "Penicillin"
            }
        ],
        "text": "Penicillin"
    },
    "patient": {
        "reference": "Patient/example-patient-123"
    },
    "reaction": [
        {
            "manifestation": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "271807003",
                            "display": "Skin rash"
                        }
                    ]
                }
            ],
            "severity": "moderate"
        }
    ]
}

# HL7 v2 message example
hl7_message = """MSH|^~\\&|EclipseLink|RohimayaHealth|EPIC|HospitalSystem|20250128103045||ADT^A08|MSG00001|P|2.5
EVN|A08|20250128103045
PID|1||MRN-123456^^^HospitalSystem^MRN||Johnson^Sarah^M||19570315|F|||123 Main Street^^Springfield^IL^62701||5555551234|||S||12345678|123-45-6789
PV1|1|I|ICU^101^01^HospitalSystem^^^^ICU|||1234567^Williams^John^A^^^MD||SUR||||ADM|||1234567^Williams^John^A^^^MD|IP|V12345|||||||||||||||||||||||||20250125080000
OBX|1|NM|8867-4^Heart Rate^LN||78|/min|60-100|N|||F|||20250128100000
OBX|2|NM|8480-6^Systolic BP^LN||118|mmHg|90-140|N|||F|||20250128100000
OBX|3|NM|8462-4^Diastolic BP^LN||72|mmHg|60-90|N|||F|||20250128100000"""

# Main content
st.markdown("## Integration Architecture Overview")

st.markdown("""
<div class="data-flow">
    <div class="flow-box">
        <strong>🏥 EHR System</strong><br>
        <span style="color: #666;">Epic / Cerner / MEDITECH</span>
    </div>
    <span class="flow-arrow">⇄</span>
    <div class="flow-box" style="border: 3px solid {PEACOCK_TEAL};">
        <strong>🦚 EclipseLink AI</strong><br>
        <span style="color: #666;">Integration Layer</span>
    </div>
    <span class="flow-arrow">⇄</span>
    <div class="flow-box">
        <strong>👨‍⚕️ Clinicians</strong><br>
        <span style="color: #666;">Voice Handoffs</span>
    </div>
</div>
""".replace("{PEACOCK_TEAL}", PEACOCK_TEAL), unsafe_allow_html=True)

st.markdown("---")

# Integration flow steps
st.markdown("## Integration Flow Walkthrough")

tab1, tab2, tab3, tab4 = st.tabs(["1️⃣ Pull Patient Data", "2️⃣ Create Handoff", "3️⃣ Push to EHR", "4️⃣ Configuration"])

with tab1:
    st.markdown("### Step 1: Pull Patient Data from EHR")

    st.markdown(f"""
    <div class="integration-step">
        <div style="display: flex; align-items: center;">
            <div class="step-number">1</div>
            <div>
                <h4 style="margin: 0;">Query Patient Data via {ehr_system}</h4>
                <p style="margin: 0.5rem 0 0 0; color: #666;">EclipseLink queries the EHR for patient demographics, medications, allergies, and recent labs</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_query, col_button = st.columns([3, 1])

    with col_query:
        patient_mrn = st.text_input("Enter Patient MRN", value="MRN-123456", key="mrn_input")

    with col_button:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Query EHR", type="primary", use_container_width=True):
            with st.spinner(f"Connecting to {ehr_system} via FHIR R4..."):
                time.sleep(1.5)
            st.session_state.data_pulled = True
            st.rerun()

    if st.session_state.data_pulled:
        st.success(f"✅ Successfully retrieved patient data from {ehr_system}!")

        st.markdown("---")
        st.markdown("### Retrieved Data")

        data_tab1, data_tab2, data_tab3 = st.tabs(["Patient Demographics", "Medications", "Allergies"])

        with data_tab1:
            st.markdown("**FHIR Patient Resource (R4)**")
            st.markdown(f'<div class="json-viewer">{json.dumps(fhir_patient, indent=2)}</div>', unsafe_allow_html=True)

            st.markdown("**Parsed Data:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Name", "Sarah Johnson")
            with col2:
                st.metric("MRN", "MRN-123456")
            with col3:
                st.metric("DOB", "03/15/1957 (68 yrs)")

        with data_tab2:
            st.markdown("**FHIR MedicationRequest Resource (R4)**")
            st.markdown(f'<div class="json-viewer">{json.dumps(fhir_medication, indent=2)}</div>', unsafe_allow_html=True)

            st.markdown("**Parsed Medications:**")
            st.markdown("""
            - **Metoprolol Tartrate 25mg** - PO BID (Active)
            - **Aspirin 81mg** - PO Daily (Active)
            - **Atorvastatin 80mg** - PO QHS (Active)
            """)

        with data_tab3:
            st.markdown("**FHIR AllergyIntolerance Resource (R4)**")
            st.markdown(f'<div class="json-viewer">{json.dumps(fhir_allergy, indent=2)}</div>', unsafe_allow_html=True)

            st.markdown("**Parsed Allergies:**")
            st.warning("⚠️ **Penicillin** - Skin rash (Moderate severity, Confirmed)")

with tab2:
    st.markdown("### Step 2: Create Handoff in EclipseLink")

    st.markdown(f"""
    <div class="integration-step">
        <div style="display: flex; align-items: center;">
            <div class="step-number">2</div>
            <div>
                <h4 style="margin: 0;">Voice-to-SBAR Generation</h4>
                <p style="margin: 0.5rem 0 0 0; color: #666;">Clinician records handoff, AI generates SBAR with EHR data pre-populated</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.data_pulled:
        st.info("👈 First pull patient data from the EHR in Step 1")
    else:
        st.markdown("**EHR Data Pre-Populated:**")
        st.markdown("""
        <div class="config-card">
            ✅ Patient demographics auto-filled<br>
            ✅ Current medications imported<br>
            ✅ Allergies flagged<br>
            ✅ Recent lab values available
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Clinician Records Voice Handoff:**")

        if st.button("🎙️ Simulate Voice Recording", type="primary"):
            with st.spinner("Recording and transcribing..."):
                time.sleep(2)
            with st.spinner("Generating SBAR with AI..."):
                time.sleep(1.5)
            st.session_state.sbar_created = True
            st.rerun()

        if st.session_state.sbar_created:
            st.success("✅ SBAR Report Generated!")

            st.markdown("---")
            st.markdown("### Generated SBAR Report")

            st.markdown("""
            **Situation:** Post-operative day 0 status-post CABG x4. Patient stable in ICU requiring close monitoring.

            **Background:** 68-year-old female with CAD, HTN, Type 2 DM. Admitted 3 days ago with unstable angina.
            - **Allergies:** Penicillin (rash) ⚠️ *[Auto-imported from EHR]*
            - **Current Medications:** Metoprolol 25mg BID, Aspirin 81mg daily, Atorvastatin 80mg QHS *[Auto-imported from EHR]*

            **Assessment:** Currently intubated and sedated. Vital signs stable: BP 118/72, HR 78, SpO2 98% on FiO2 40%.

            **Recommendation:** Continue sedation, monitor chest tube output hourly. Plan extubation in AM if stable.
            """)

with tab3:
    st.markdown("### Step 3: Push SBAR Report to EHR")

    st.markdown(f"""
    <div class="integration-step">
        <div style="display: flex; align-items: center;">
            <div class="step-number">3</div>
            <div>
                <h4 style="margin: 0;">Send Documentation to {ehr_system}</h4>
                <p style="margin: 0.5rem 0 0 0; color: #666;">SBAR report sent as clinical note to patient's chart in EHR</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.sbar_created:
        st.info("👈 First create a handoff in Step 2")
    else:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**Select Destination in EHR:**")
            note_type = st.selectbox(
                "Note Type",
                ["Clinical Note - Nursing Handoff", "Progress Note", "Transfer Summary", "Clinical Documentation"]
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📤 Send to EHR", type="primary", use_container_width=True):
                with st.spinner(f"Sending to {ehr_system} via FHIR API..."):
                    time.sleep(1.5)
                st.session_state.data_pushed = True
                st.rerun()

        if st.session_state.data_pushed:
            st.success(f"✅ SBAR report successfully sent to {ehr_system}!")

            st.markdown("---")
            st.markdown("### FHIR DocumentReference Resource (Sent to EHR)")

            fhir_document = {
                "resourceType": "DocumentReference",
                "id": "handoff-doc-001",
                "status": "current",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "28570-0",
                            "display": "Provider-unspecified Procedure note"
                        }
                    ],
                    "text": "Nursing Handoff - SBAR Report"
                },
                "subject": {
                    "reference": "Patient/example-patient-123",
                    "display": "Sarah Johnson"
                },
                "date": datetime.now().isoformat(),
                "author": [
                    {
                        "reference": "Practitioner/nurse-001",
                        "display": "RN Sarah Martinez"
                    }
                ],
                "description": "EclipseLink AI Generated SBAR Handoff Report",
                "content": [
                    {
                        "attachment": {
                            "contentType": "text/plain",
                            "data": "U0lUVUFUSU9OOiBQb3N0LW9wZXJhdGl2ZSBkYXkgMC4uLg=="
                        }
                    }
                ]
            }

            st.markdown(f'<div class="json-viewer">{json.dumps(fhir_document, indent=2)}</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### Alternative: HL7 v2.x Message")
            st.markdown("For legacy systems, EclipseLink can also send via HL7 v2.x:")

            hl7_outbound = """MSH|^~\\&|EclipseLink|RohimayaHealth|EPIC|HospitalSystem|20250128105030||MDM^T02|MSG00002|P|2.5
EVN|T02|20250128105030
PID|1||MRN-123456^^^HospitalSystem^MRN||Johnson^Sarah^M||19570315|F
PV1|1|I|ICU^101^01^HospitalSystem^^^^ICU|||1234567^Williams^John^A^^^MD
TXA|1|CN|TX|||20250128105030|||1234567^Martinez^Sarah^^^RN||||||AU|AV
OBX|1|FT|^Nursing Handoff SBAR||SITUATION: Post-operative day 0 status-post CABG x4...||||||F"""

            st.markdown(f'<div class="hl7-message">{hl7_outbound}</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("### EHR Connection Configuration")

    st.markdown("#### Authentication & Connection Settings")

    config_method = st.radio(
        "Integration Method",
        ["FHIR R4 (REST API)", "HL7 v2.x (MLLP)"],
        horizontal=True
    )

    if config_method == "FHIR R4 (REST API)":
        st.markdown("**FHIR R4 Configuration:**")

        col1, col2 = st.columns(2)

        with col1:
            st.text_input("FHIR Base URL", value=f"https://fhir.{ehr_system.lower()}.com/api/FHIR/R4", disabled=True)
            st.text_input("Client ID", value="eclipselink-prod-client", disabled=True)
            st.selectbox("Authentication", ["OAuth 2.0 Client Credentials", "OAuth 2.0 Authorization Code", "SMART on FHIR"], disabled=True)

        with col2:
            st.text_input("Tenant ID", value=f"{ehr_system.lower()}-hospital-001", disabled=True)
            st.text_input("Client Secret", value="••••••••••••••••", type="password", disabled=True)
            st.multiselect("FHIR Scopes", ["patient/Patient.read", "patient/MedicationRequest.read", "patient/AllergyIntolerance.read", "patient/DocumentReference.write"], default=["patient/Patient.read", "patient/MedicationRequest.read"], disabled=True)

        st.markdown("---")
        st.markdown("**Supported FHIR Resources:**")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("""
            **Read Operations:**
            - ✅ Patient
            - ✅ MedicationRequest
            - ✅ AllergyIntolerance
            - ✅ Observation (Labs, Vitals)
            - ✅ Condition (Problem List)
            - ✅ Encounter
            """)

        with col_b:
            st.markdown("""
            **Write Operations:**
            - ✅ DocumentReference (SBAR Reports)
            - ✅ ClinicalImpression
            - ✅ Communication (Team Messages)
            - ✅ Task (Care Team Assignments)
            """)

    else:
        st.markdown("**HL7 v2.x Configuration:**")

        col1, col2 = st.columns(2)

        with col1:
            st.text_input("HL7 Server Host", value=f"hl7.{ehr_system.lower()}.hospital.local", disabled=True)
            st.text_input("Port", value="6661", disabled=True)
            st.selectbox("Protocol", ["MLLP (Minimal Lower Layer Protocol)", "TCP/IP"], disabled=True)

        with col2:
            st.text_input("Sending Application", value="EclipseLink", disabled=True)
            st.text_input("Sending Facility", value="RohimayaHealth", disabled=True)
            st.selectbox("HL7 Version", ["2.5", "2.4", "2.3"], disabled=True)

        st.markdown("---")
        st.markdown("**Supported HL7 Message Types:**")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("""
            **Inbound (Receive):**
            - ✅ ADT^A01 (Patient Admit)
            - ✅ ADT^A08 (Patient Update)
            - ✅ ORM^O01 (Orders)
            - ✅ ORU^R01 (Lab Results)
            """)

        with col_b:
            st.markdown("""
            **Outbound (Send):**
            - ✅ MDM^T02 (Document Update)
            - ✅ MDM^T06 (Document Addendum)
            - ✅ ORU^R01 (Observations)
            """)

    st.markdown("---")
    st.markdown("#### Security & Compliance")

    col_sec1, col_sec2 = st.columns(2)

    with col_sec1:
        st.markdown("""
        **Data Encryption:**
        - ✅ TLS 1.3 for all API calls
        - ✅ AES-256 encryption at rest
        - ✅ End-to-end encrypted data transfer
        - ✅ Certificate-based authentication
        """)

    with col_sec2:
        st.markdown("""
        **Compliance:**
        - ✅ HIPAA compliant
        - ✅ SOC 2 Type II certified
        - ✅ Complete audit logging
        - ✅ BAA (Business Associate Agreement)
        """)

# Implementation timeline
st.markdown("---")
st.markdown("## Implementation Timeline")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="integration-step">
        <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">Week 1-2</h4>
        <strong>Discovery & Planning</strong>
        <ul style="margin: 0.5rem 0 0 0; padding-left: 1.5rem;">
            <li>Technical discovery call</li>
            <li>EHR environment access</li>
            <li>API credentials setup</li>
            <li>Security review</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="integration-step">
        <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">Week 3-4</h4>
        <strong>Development & Testing</strong>
        <ul style="margin: 0.5rem 0 0 0; padding-left: 1.5rem;">
            <li>Configure connections</li>
            <li>Map data fields</li>
            <li>Sandbox testing</li>
            <li>Error handling setup</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="integration-step">
        <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">Week 5-6</h4>
        <strong>Pilot Deployment</strong>
        <ul style="margin: 0.5rem 0 0 0; padding-left: 1.5rem;">
            <li>Deploy to pilot unit</li>
            <li>User acceptance testing</li>
            <li>Performance monitoring</li>
            <li>Refinements</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="integration-step">
        <h4 style="color: {PEACOCK_TEAL}; margin-top: 0;">Week 7-8</h4>
        <strong>Full Rollout</strong>
        <ul style="margin: 0.5rem 0 0 0; padding-left: 1.5rem;">
            <li>Hospital-wide deployment</li>
            <li>Staff training</li>
            <li>Go-live support</li>
            <li>Ongoing monitoring</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Benefits
st.markdown("---")
st.markdown("## Integration Benefits")

col_ben1, col_ben2, col_ben3 = st.columns(3)

with col_ben1:
    st.markdown("""
    ### 🎯 Reduced Manual Entry
    - Auto-populate patient data
    - No duplicate data entry
    - Minimize transcription errors
    - Save 2-3 minutes per handoff
    """)

with col_ben2:
    st.markdown("""
    ### 🔄 Single Source of Truth
    - EHR remains central repository
    - Real-time data synchronization
    - Consistent information across systems
    - Audit trail maintained
    """)

with col_ben3:
    st.markdown("""
    ### 💼 Minimal IT Burden
    - Standard integration protocols
    - Pre-built connectors
    - Ongoing support included
    - 6-8 week implementation
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>EclipseLink AI™</strong> - Seamless EHR Integration for Modern Hospitals</p>
    <p style="font-size: 0.9rem;">© 2025 Rohimaya Health AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
