"""
Voice Recording Demo - EclipseLink AI™
Demonstrates voice-to-text functionality for clinical handoffs
"""

import streamlit as st
import time
from datetime import datetime
import random

st.set_page_config(
    page_title="Voice Recording Demo - EclipseLink AI",
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .recording-active {
        background-color: #ef4444;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        font-weight: 700;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .transcript-box {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0ea5e9;
        min-height: 200px;
        font-family: monospace;
    }
    .metadata-box {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🎙️ Voice Recording Demo")
st.markdown("Experience how clinicians can record handoff notes using voice input with Azure Whisper transcription.")

st.markdown("---")

# Initialize session state
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'duration' not in st.session_state:
    st.session_state.duration = 0

# Demo Instructions
with st.expander("📖 How to Use This Demo", expanded=True):
    st.markdown("""
    ### Voice Recording Workflow

    1. **Click "Start Recording"** to begin capturing your voice
    2. **Speak naturally** - describe the patient handoff in your own words
    3. **Click "Stop Recording"** when finished
    4. **Review the transcription** - Azure Whisper will convert speech to text
    5. **Submit to SBAR Generation** - Send transcript for AI processing

    **Note**: This is a simulated demo. In production, it uses Azure Whisper for real-time transcription.
    """)

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Recording Control")

    # Recording button
    if not st.session_state.recording:
        if st.button("🎙️ Start Recording", type="primary", use_container_width=True):
            st.session_state.recording = True
            st.session_state.duration = 0
            st.rerun()
    else:
        st.markdown('<div class="recording-active">🔴 RECORDING IN PROGRESS...</div>', unsafe_allow_html=True)
        st.markdown("")
        if st.button("⏹️ Stop Recording", type="secondary", use_container_width=True):
            st.session_state.recording = False
            # Simulate transcription
            st.session_state.transcript = """Patient John Doe, 67-year-old male, admitted three days ago with acute exacerbation of COPD. Currently on room air with oxygen saturation 94%. Patient has a history of hypertension and diabetes mellitus type 2.

Background: Patient was admitted through the ED with shortness of breath and productive cough. Chest X-ray showed bilateral lower lobe infiltrates. Started on antibiotics and steroids. Blood glucose has been elevated, ranging from 180 to 220.

Assessment: Patient is improving, respiratory status is stable. However, blood sugar control needs optimization. Patient is eager to go home but may need one more day for glucose monitoring.

Recommendation: Continue current antibiotic course, consider endocrinology consult for diabetes management, plan for discharge tomorrow if glucose levels stabilize. Patient education on inhaler technique before discharge."""
            st.rerun()

    # Recording duration (simulated)
    if st.session_state.recording:
        duration_placeholder = st.empty()
        for i in range(3):
            st.session_state.duration += 1
            duration_placeholder.metric("Recording Duration", f"{st.session_state.duration} seconds")
            time.sleep(1)
        st.rerun()

with col2:
    st.subheader("Recording Info")
    st.metric("Status", "🔴 Recording" if st.session_state.recording else "⚪ Ready")
    st.metric("Duration", f"{st.session_state.duration}s")
    st.metric("Format", "WebM/Opus")
    st.metric("Sample Rate", "16 kHz")

# Transcription Display
st.markdown("---")
st.subheader("📝 Transcription")

if st.session_state.transcript:
    st.markdown(f'<div class="transcript-box">{st.session_state.transcript}</div>', unsafe_allow_html=True)

    # Metadata
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Word Count", len(st.session_state.transcript.split()))
    with col2:
        st.metric("Characters", len(st.session_state.transcript))
    with col3:
        st.metric("Confidence", "96.8%")
    with col4:
        st.metric("Language", "English")

    # Actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤖 Generate SBAR Report", type="primary", use_container_width=True):
            st.success("✅ Transcript sent to SBAR generation!")
            time.sleep(1)
            st.switch_page("pages/2_SBAR_Generation.py")

    with col2:
        if st.button("✏️ Edit Transcript", use_container_width=True):
            st.info("Opening editor...")

    with col3:
        if st.button("🔄 Record Again", use_container_width=True):
            st.session_state.transcript = ""
            st.session_state.duration = 0
            st.rerun()

else:
    st.info("👆 Click 'Start Recording' to begin capturing voice notes")

# Technical Details
st.markdown("---")
with st.expander("🔧 Technical Details"):
    st.markdown("""
    ### Azure Whisper Integration

    **Transcription Engine**: Azure OpenAI Whisper API

    **Features**:
    - Real-time speech-to-text with 95%+ accuracy
    - Medical terminology recognition
    - Multi-language support (English, Spanish, etc.)
    - Speaker diarization for multi-person handoffs
    - Automatic punctuation and formatting

    **Processing Pipeline**:
    1. Audio captured via WebRTC (browser microphone)
    2. Audio compressed to WebM/Opus format
    3. Uploaded to secure Azure Blob Storage
    4. Processed by Azure Whisper API
    5. Transcription returned with confidence scores
    6. Queued for SBAR generation via BullMQ

    **Security**:
    - End-to-end encryption
    - HIPAA-compliant storage
    - Automatic PHI detection
    - Audit logging
    """)

# Sample Handoff Scripts
with st.expander("💡 Sample Handoff Scripts"):
    st.markdown("""
    ### Example Clinical Handoffs to Try

    **COPD Patient**:
    "Patient John Doe, 67-year-old male with COPD exacerbation. Admitted 3 days ago. Currently stable on 2L oxygen. History of hypertension. Recommend discharge tomorrow with home oxygen and pulmonology follow-up."

    **Post-Surgical Patient**:
    "Mary Smith, 45-year-old female, post-op day 2 from cholecystectomy. Pain controlled with oral medications. Tolerating regular diet. Ambulating well. Plan for discharge today with surgical follow-up in one week."

    **Diabetic Crisis**:
    "Robert Johnson, 52-year-old with DKA. Admitted with glucose 450 and pH 7.2. Started on insulin drip. Currently glucose 180, gap closed. Transitioning to subcutaneous insulin. Needs diabetes education before discharge."
    """)
