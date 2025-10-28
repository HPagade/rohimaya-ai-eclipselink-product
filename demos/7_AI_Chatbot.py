"""
EclipseLink AI - AI Chatbot Query Demo
Instant answers from patient data using natural language
"""

import streamlit as st
import time
import random
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="AI Chatbot - EclipseLink AI",
    page_icon="💬",
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
    .chat-container {{
        max-width: 800px;
        margin: 0 auto;
    }}
    .user-message {{
        background: {PEACOCK_TEAL};
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 5px 15px;
        margin: 0.5rem 0;
        margin-left: 20%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .ai-message {{
        background: white;
        color: {ECLIPSE_NAVY};
        padding: 1rem;
        border-radius: 15px 15px 15px 5px;
        margin: 0.5rem 0;
        margin-right: 20%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid {PEACOCK_TEAL};
    }}
    .quick-query {{
        background: white;
        border: 2px solid {PEACOCK_TEAL};
        color: {PEACOCK_TEAL};
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        margin: 0.5rem;
        display: inline-block;
        cursor: pointer;
        transition: all 0.3s;
    }}
    .quick-query:hover {{
        background: {PEACOCK_TEAL};
        color: white;
    }}
    .source-card {{
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 3px solid {PEACOCK_TEAL};
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }}
    .metric-badge {{
        background: {PHOENIX_GOLD};
        color: {ECLIPSE_NAVY};
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
        margin-left: 0.5rem;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💬 AI Chatbot Query Demo</h1>
    <p style="font-size: 1.2rem; margin: 0;">Ask questions about patient data in natural language - Get instant answers</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = "Sarah Johnson"

# Sidebar
with st.sidebar:
    st.image("https://img.shields.io/badge/EclipseLink-AI-1a9b8e?style=for-the-badge", use_container_width=True)
    st.markdown("---")
    st.markdown("### Select Patient")

    patient = st.selectbox(
        "Active Patient",
        ["Sarah Johnson - ICU", "Michael Chen - Cardiac", "Robert Williams - Med-Surg"]
    )

    st.session_state.selected_patient = patient.split(" - ")[0]

    st.markdown("---")
    st.markdown("### Chatbot Features")
    st.info("""
    **Ask anything:**
    - 💊 Medications
    - 🔬 Lab results
    - 📈 Vital signs
    - 📅 Procedures
    - 👥 Care team
    - 📝 Recent notes
    - ⚠️ Allergies
    - 📊 Trends
    """)

    st.markdown("---")
    st.markdown("### Privacy & Security")
    st.success("""
    ✅ HIPAA compliant
    ✅ Audit trail logged
    ✅ Source citations
    ✅ Role-based access
    """)

    if st.button("Clear Chat History", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()

# Patient mock data
patients_db = {
    "Sarah Johnson": {
        "mrn": "MRN-123456",
        "age": 68,
        "gender": "Female",
        "admission_date": datetime.now() - timedelta(days=2),
        "diagnosis": "Post-op CABG x4",
        "medications": [
            {"name": "Aspirin", "dose": "81 mg", "route": "PO", "frequency": "daily", "started": "2025-01-25"},
            {"name": "Metoprolol", "dose": "25 mg", "route": "PO", "frequency": "BID", "started": "2025-01-25"},
            {"name": "Atorvastatin", "dose": "80 mg", "route": "PO", "frequency": "QHS", "started": "2025-01-25"},
            {"name": "Lisinopril", "dose": "10 mg", "route": "PO", "frequency": "daily", "started": "2025-01-26"},
            {"name": "Heparin", "dose": "5000 units", "route": "SQ", "frequency": "Q12H", "started": "2025-01-25"},
        ],
        "vitals": {
            "current": {"BP": "118/72", "HR": "78", "RR": "16", "SpO2": "98%", "Temp": "98.2°F"},
            "6h_ago": {"BP": "122/75", "HR": "82", "RR": "18", "SpO2": "97%", "Temp": "98.4°F"},
            "12h_ago": {"BP": "128/80", "HR": "88", "RR": "20", "SpO2": "96%", "Temp": "98.6°F"},
        },
        "labs": {
            "latest": {"Hemoglobin": "10.2", "WBC": "11.2", "Platelets": "185", "Creatinine": "0.9", "Potassium": "4.2"},
            "previous": {"Hemoglobin": "9.8", "WBC": "12.5", "Platelets": "180", "Creatinine": "0.9", "Potassium": "4.5"},
        },
        "procedures": [
            {"name": "CABG x4", "date": "2025-01-25 08:00", "status": "Completed"},
            {"name": "Chest X-ray", "date": "2025-01-26 06:00", "status": "Completed"},
            {"name": "Echocardiogram", "date": "2025-01-27 09:00", "status": "Scheduled"},
        ],
        "allergies": ["Penicillin (rash)", "Morphine (nausea)"],
        "care_team": ["Dr. Williams (Cardiothoracic Surgery)", "Dr. Chen (Cardiology)", "RN Sarah Martinez", "PT John Davis"],
        "recent_notes": [
            {"time": "2 hours ago", "author": "Dr. Williams", "note": "Patient progressing well post-op. Plan to transfer to step-down unit tomorrow."},
            {"time": "8 hours ago", "author": "RN Martinez", "note": "Ambulated 100 feet with PT. Tolerated well, no SOB."},
        ]
    },
    "Michael Chen": {
        "mrn": "MRN-789012",
        "age": 45,
        "gender": "Male",
        "admission_date": datetime.now() - timedelta(days=1),
        "diagnosis": "STEMI, s/p PCI with stent to RCA",
        "medications": [
            {"name": "Aspirin", "dose": "325 mg", "route": "PO", "frequency": "daily", "started": "2025-01-26"},
            {"name": "Ticagrelor", "dose": "90 mg", "route": "PO", "frequency": "BID", "started": "2025-01-26"},
            {"name": "Atorvastatin", "dose": "80 mg", "route": "PO", "frequency": "QHS", "started": "2025-01-26"},
            {"name": "Lisinopril", "dose": "5 mg", "route": "PO", "frequency": "daily", "started": "2025-01-26"},
            {"name": "Metoprolol", "dose": "12.5 mg", "route": "PO", "frequency": "BID", "started": "2025-01-26"},
        ],
        "vitals": {
            "current": {"BP": "128/78", "HR": "72", "RR": "14", "SpO2": "98%", "Temp": "98.6°F"},
            "6h_ago": {"BP": "135/82", "HR": "78", "RR": "16", "SpO2": "97%", "Temp": "98.4°F"},
        },
        "labs": {
            "latest": {"Troponin": "3.2", "CK-MB": "45", "LDL": "145", "HDL": "35", "Triglycerides": "220"},
            "previous": {"Troponin": "8.4", "CK-MB": "89", "LDL": "N/A", "HDL": "N/A", "Triglycerides": "N/A"},
        },
        "procedures": [
            {"name": "Cardiac catheterization with PCI", "date": "2025-01-26 14:30", "status": "Completed"},
            {"name": "Echocardiogram", "date": "2025-01-27 08:00", "status": "Completed"},
        ],
        "allergies": ["No known drug allergies"],
        "care_team": ["Dr. Rodriguez (Interventional Cardiology)", "Dr. Patel (Cardiology)", "RN Lisa Anderson"],
        "recent_notes": [
            {"time": "1 hour ago", "author": "Dr. Patel", "note": "Patient doing well post-PCI. Echo shows EF 50%, mild inferior wall hypokinesis. Plan for discharge tomorrow with cardiac rehab referral."},
        ]
    },
    "Robert Williams": {
        "mrn": "MRN-556677",
        "age": 72,
        "gender": "Male",
        "admission_date": datetime.now() - timedelta(days=3),
        "diagnosis": "COPD exacerbation",
        "medications": [
            {"name": "Albuterol/Ipratropium", "dose": "1 neb", "route": "INH", "frequency": "Q6H", "started": "2025-01-24"},
            {"name": "Prednisone", "dose": "40 mg", "route": "PO", "frequency": "daily", "started": "2025-01-24"},
            {"name": "Azithromycin", "dose": "500 mg", "route": "PO", "frequency": "daily", "started": "2025-01-24"},
        ],
        "vitals": {
            "current": {"BP": "135/80", "HR": "84", "RR": "18", "SpO2": "94%", "Temp": "98.2°F"},
            "oxygen": "1L nasal cannula",
        },
        "labs": {
            "latest": {"WBC": "9.2", "pH": "7.38", "pCO2": "48", "pO2": "72"},
        },
        "procedures": [
            {"name": "Chest X-ray", "date": "2025-01-26", "status": "Completed", "result": "Improved, less infiltrate"},
        ],
        "allergies": ["Penicillin (anaphylaxis)"],
        "care_team": ["Dr. Thompson (Pulmonology)", "RN Maria Garcia", "RT Kevin Brown"],
        "recent_notes": [
            {"time": "3 hours ago", "author": "RT Brown", "note": "Respiratory status improving. Weaned to 1L from 2L NC. Continue breathing treatments."},
        ]
    }
}

# Query processing function
def process_query(query, patient_data):
    """Simulate AI processing of natural language query"""
    query_lower = query.lower()

    # Medication queries
    if any(word in query_lower for word in ["medication", "medicine", "drug", "taking", "prescribed"]):
        meds_list = "\n".join([f"• **{m['name']}** {m['dose']} {m['route']} {m['frequency']}" for m in patient_data['medications']])
        response = f"**Current Medications:**\n\n{meds_list}"
        source = f"Medication Administration Record - Last updated {datetime.now().strftime('%I:%M %p')}"
        return response, source

    # Blood pressure queries
    elif any(word in query_lower for word in ["blood pressure", "bp", "pressure"]):
        current_bp = patient_data['vitals']['current']['BP']
        if '6h_ago' in patient_data['vitals']:
            prev_bp = patient_data['vitals']['6h_ago']['BP']
            response = f"**Current Blood Pressure:** {current_bp} mmHg\n\n**6 hours ago:** {prev_bp} mmHg\n\nThe blood pressure is stable and within normal limits."
        else:
            response = f"**Current Blood Pressure:** {current_bp} mmHg\n\nThe blood pressure is stable and within normal limits."
        source = f"Vital Signs Monitor - Real-time data"
        return response, source

    # Lab queries
    elif any(word in query_lower for word in ["lab", "blood work", "test result", "hemoglobin", "wbc", "platelet"]):
        if "latest" in patient_data['labs']:
            labs = patient_data['labs']['latest']
            labs_list = "\n".join([f"• **{k}:** {v}" for k, v in labs.items()])
            response = f"**Latest Lab Results:**\n\n{labs_list}"
            if "previous" in patient_data['labs']:
                response += "\n\n📊 **Trends:**\n"
                for key in labs.keys():
                    if key in patient_data['labs']['previous'] and patient_data['labs']['previous'][key] != "N/A":
                        old_val = float(patient_data['labs']['previous'][key])
                        new_val = float(labs[key])
                        if new_val > old_val:
                            response += f"• {key}: ↑ Increased from {old_val} to {new_val}\n"
                        elif new_val < old_val:
                            response += f"• {key}: ↓ Decreased from {old_val} to {new_val}\n"
                        else:
                            response += f"• {key}: → Stable at {new_val}\n"
        source = f"Laboratory Information System - Drawn {(datetime.now() - timedelta(hours=4)).strftime('%I:%M %p')}"
        return response, source

    # Vital signs queries
    elif any(word in query_lower for word in ["vital", "temperature", "temp", "heart rate", "oxygen", "spo2"]):
        vitals = patient_data['vitals']['current']
        vitals_list = "\n".join([f"• **{k}:** {v}" for k, v in vitals.items()])
        response = f"**Current Vital Signs:**\n\n{vitals_list}"
        if 'oxygen' in patient_data['vitals']:
            response += f"\n• **Oxygen:** {patient_data['vitals']['oxygen']}"
        source = f"Bedside Monitor - Last updated {datetime.now().strftime('%I:%M %p')}"
        return response, source

    # Allergy queries
    elif any(word in query_lower for word in ["allerg", "adverse", "reaction"]):
        allergies = patient_data['allergies']
        if allergies[0] == "No known drug allergies":
            response = "✅ **No known drug allergies (NKDA)**"
        else:
            allergies_list = "\n".join([f"⚠️ **{a}**" for a in allergies])
            response = f"**Known Allergies:**\n\n{allergies_list}"
        source = "Electronic Health Record - Allergy List"
        return response, source

    # Procedure queries
    elif any(word in query_lower for word in ["procedure", "surgery", "operation", "test", "scheduled"]):
        procedures = patient_data['procedures']
        procs_list = ""
        for p in procedures:
            status_icon = "✅" if p['status'] == "Completed" else "📅"
            procs_list += f"{status_icon} **{p['name']}** - {p['date']} ({p['status']})\n"
        response = f"**Procedures:**\n\n{procs_list}"
        source = "Procedure Schedule & History"
        return response, source

    # Care team queries
    elif any(word in query_lower for word in ["doctor", "physician", "nurse", "team", "who is", "provider"]):
        team_list = "\n".join([f"• {member}" for member in patient_data['care_team']])
        response = f"**Care Team:**\n\n{team_list}"
        source = "Care Team Directory"
        return response, source

    # Recent notes queries
    elif any(word in query_lower for word in ["note", "update", "recent", "latest", "progress"]):
        notes_list = ""
        for note in patient_data['recent_notes']:
            notes_list += f"**{note['time']}** - {note['author']}\n{note['note']}\n\n"
        response = f"**Recent Clinical Notes:**\n\n{notes_list}"
        source = "Clinical Documentation System"
        return response, source

    # Diagnosis queries
    elif any(word in query_lower for word in ["diagnosis", "admitted", "why", "condition"]):
        response = f"**Admission Diagnosis:** {patient_data['diagnosis']}\n\n**Admitted:** {patient_data['admission_date'].strftime('%B %d, %Y')}"
        source = "Admission Summary"
        return response, source

    # Default response
    else:
        response = f"I can help you find information about **{patient_data['diagnosis']}**. Try asking about:\n\n• Medications\n• Vital signs\n• Lab results\n• Procedures\n• Care team\n• Recent notes\n• Allergies"
        source = "EclipseLink AI Assistant"
        return response, source

# Main content
patient_name = st.session_state.selected_patient
patient_data = patients_db[patient_name]

# Patient info header
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Patient", patient_name)
with col2:
    st.metric("MRN", patient_data["mrn"])
with col3:
    st.metric("Age/Gender", f"{patient_data['age']} / {patient_data['gender']}")
with col4:
    st.metric("Diagnosis", patient_data["diagnosis"][:30] + "...")

st.markdown("---")

# Quick query buttons
st.markdown("### 💡 Quick Queries")
st.markdown("Click a button or type your own question below:")

quick_queries = [
    "What medications is the patient taking?",
    "What was the last blood pressure?",
    "Show me all lab results",
    "When is the next procedure?",
    "Who is on the care team?",
    "What are the patient's allergies?",
    "What are the current vital signs?",
    "Show recent clinical notes"
]

cols = st.columns(4)
for idx, query in enumerate(quick_queries):
    col_idx = idx % 4
    with cols[col_idx]:
        if st.button(query, key=f"quick_{idx}", use_container_width=True):
            # Process query
            response, source = process_query(query, patient_data)

            # Add to chat history
            st.session_state.chat_history.append({
                "type": "user",
                "content": query,
                "timestamp": datetime.now()
            })
            st.session_state.chat_history.append({
                "type": "ai",
                "content": response,
                "source": source,
                "timestamp": datetime.now()
            })
            st.rerun()

st.markdown("---")

# Chat interface
st.markdown("### 💬 Chat with EclipseLink AI")

# Display chat history
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    if len(st.session_state.chat_history) == 0:
        st.info("👋 Hello! I'm your EclipseLink AI Assistant. Ask me anything about the patient's care. Try clicking a quick query above or type your question below.")
    else:
        for message in st.session_state.chat_history:
            if message["type"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ai-message">
                    <strong>🤖 EclipseLink AI:</strong><br>
                    {message['content']}
                    <div class="source-card">
                        📍 <strong>Source:</strong> {message['source']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Input area
st.markdown("---")
col_input, col_send = st.columns([5, 1])

with col_input:
    user_query = st.text_input("Ask a question...", placeholder="e.g., What medications is the patient taking?", label_visibility="collapsed", key="user_input")

with col_send:
    send_button = st.button("Send", type="primary", use_container_width=True)

if send_button and user_query:
    # Simulate AI processing
    with st.spinner("🤖 Thinking..."):
        time.sleep(0.8)  # Simulate processing delay
        response, source = process_query(user_query, patient_data)

    # Add to chat history
    st.session_state.chat_history.append({
        "type": "user",
        "content": user_query,
        "timestamp": datetime.now()
    })
    st.session_state.chat_history.append({
        "type": "ai",
        "content": response,
        "source": source,
        "timestamp": datetime.now()
    })
    st.rerun()

# Stats
st.markdown("---")
st.markdown("### 📊 Chatbot Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Avg Response Time", "0.8 sec")
with col2:
    st.metric("Accuracy Rate", "98.5%")
with col3:
    st.metric("Queries Today", "47")
with col4:
    st.metric("Time Saved", "23 min")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>EclipseLink AI™</strong> - Instant Answers from Patient Data</p>
    <p style="font-size: 0.9rem;">© 2025 Rohimaya Health AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
