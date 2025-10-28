"""
EclipseLink AI™ - Streamlit Demo Home Page
Voice-enabled Clinical Handoff Platform with AI-powered SBAR Generation
"""

import streamlit as st
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="EclipseLink AI™ - Clinical Handoff Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #0ea5e9;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0ea5e9;
        margin-bottom: 1rem;
    }
    .stats-card {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        color: white;
    }
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
    }
    .stats-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏥 EclipseLink AI™</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Voice-Enabled Clinical Handoff Platform with AI-Powered SBAR Generation</p>', unsafe_allow_html=True)

# Introduction
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">60%</div>
        <div class="stats-label">Faster Handoffs</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">95%</div>
        <div class="stats-label">Accuracy Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">HIPAA</div>
        <div class="stats-label">Compliant</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# About Section
st.header("🎯 About EclipseLink AI")
st.markdown("""
EclipseLink AI™ is a revolutionary healthcare platform that transforms clinical handoffs through:

- **🎙️ Voice-to-Text**: Capture handoff notes naturally through voice recording
- **🤖 AI-Powered SBAR**: Automatically generate structured SBAR reports using Azure OpenAI GPT-4
- **📊 Real-time Analytics**: Track handoff quality, completeness, and patient safety metrics
- **🔒 HIPAA Compliance**: Bank-grade encryption and audit trails for patient data security
- **📱 Mobile-First**: Progressive Web App works seamlessly on any device
""")

# Key Features
st.header("✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🎤 Voice Recording</h3>
        <p>Record clinical handoffs naturally using voice. Our system supports multi-language transcription with Azure Whisper for high accuracy.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h3>🤖 AI SBAR Generation</h3>
        <p>Automatically generate structured SBAR reports from transcribed voice notes. GPT-4 analyzes clinical context and creates standardized reports.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h3>📋 Version Control</h3>
        <p>Track all changes to SBAR reports with complete version history and audit trails for compliance.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>👥 Team Collaboration</h3>
        <p>Seamlessly hand off patients between providers with role-based access control and real-time notifications.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h3>📊 Analytics Dashboard</h3>
        <p>Gain insights into handoff quality, completion rates, and identify areas for improvement.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h3>🔐 Security & Compliance</h3>
        <p>HIPAA-compliant with encryption at rest and in transit, comprehensive audit logs, and role-based access control.</p>
    </div>
    """, unsafe_allow_html=True)

# Demo Navigation
st.markdown("---")
st.header("🚀 Explore the Demos")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🎙️ Voice Recording Demo")
    st.markdown("Experience how clinicians can record handoff notes using voice input.")
    if st.button("Launch Voice Demo", key="voice"):
        st.switch_page("pages/1_Voice_Recording.py")

with col2:
    st.markdown("### 🤖 SBAR Generation Demo")
    st.markdown("See how AI transforms clinical notes into structured SBAR reports.")
    if st.button("Launch SBAR Demo", key="sbar"):
        st.switch_page("pages/2_SBAR_Generation.py")

with col3:
    st.markdown("### 📊 Analytics Demo")
    st.markdown("View comprehensive analytics and insights on handoff quality.")
    if st.button("Launch Analytics Demo", key="analytics"):
        st.switch_page("pages/3_Analytics_Dashboard.py")

# Technology Stack
st.markdown("---")
st.header("🛠️ Technology Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Frontend**")
    st.markdown("""
    - Next.js 14
    - React 18
    - TypeScript
    - Tailwind CSS
    - PWA Support
    """)

with col2:
    st.markdown("**Backend**")
    st.markdown("""
    - Node.js + Express
    - PostgreSQL
    - Redis (BullMQ)
    - Azure OpenAI
    - Azure Whisper
    """)

with col3:
    st.markdown("**Infrastructure**")
    st.markdown("""
    - Docker
    - Azure Cloud
    - GitHub Actions
    - Nginx
    - SSL/TLS
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem 0;">
    <p>EclipseLink AI™ - Transforming Healthcare Communication</p>
    <p>© 2024 Rohimaya Health AI. All rights reserved.</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        🔒 HIPAA Compliant | 📱 Mobile-First | 🤖 AI-Powered
    </p>
</div>
""", unsafe_allow_html=True)
