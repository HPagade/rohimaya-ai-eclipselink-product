"""
Analytics Dashboard Demo - EclipseLink AI™
Demonstrates comprehensive analytics and insights on handoff quality
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Analytics Dashboard - EclipseLink AI",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .trend-up {
        color: #10b981;
        font-weight: 600;
    }
    .trend-down {
        color: #ef4444;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Analytics Dashboard")
st.markdown("Comprehensive insights into handoff quality, provider performance, and patient safety metrics.")

st.markdown("---")

# Time period selector
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    date_range = st.date_input(
        "Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now()
    )
with col2:
    facility = st.selectbox("Facility", ["All Facilities", "Main Hospital", "Clinic A", "Clinic B"])
with col3:
    department = st.selectbox("Department", ["All Departments", "Emergency", "ICU", "Med-Surg", "Pediatrics"])
with col4:
    handoff_type = st.selectbox("Type", ["All Types", "Initial", "Update", "Discharge"])

# Key Metrics
st.markdown("---")
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">1,247</div>
        <div class="metric-label">Total Handoffs</div>
        <div class="trend-up">↑ 12.3% vs last month</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">94.8%</div>
        <div class="metric-label">Completion Rate</div>
        <div class="trend-up">↑ 2.1% vs last month</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">4.2 min</div>
        <div class="metric-label">Avg. Time to Complete</div>
        <div class="trend-up">↓ 18% vs last month</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">96.5%</div>
        <div class="metric-label">SBAR Quality Score</div>
        <div class="trend-up">↑ 1.2% vs last month</div>
    </div>
    """, unsafe_allow_html=True)

# Charts Section
st.markdown("---")

# Row 1: Handoff Trends
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Handoff Volume Trends")

    # Generate sample data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    handoff_data = pd.DataFrame({
        'Date': dates,
        'Handoffs': [random.randint(30, 60) for _ in range(30)],
        'Completed': [random.randint(28, 58) for _ in range(30)],
        'Incomplete': [random.randint(1, 5) for _ in range(30)]
    })

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=handoff_data['Date'],
        y=handoff_data['Handoffs'],
        name='Total Handoffs',
        line=dict(color='#0ea5e9', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=handoff_data['Date'],
        y=handoff_data['Completed'],
        name='Completed',
        line=dict(color='#10b981', width=2)
    ))
    fig.update_layout(
        template='plotly_dark',
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("⏱️ Average Completion Time by Type")

    completion_data = pd.DataFrame({
        'Type': ['Initial Handoff', 'Update', 'Discharge', 'Emergency'],
        'Time (minutes)': [5.2, 3.8, 6.1, 4.5],
        'Target': [6.0, 4.0, 7.0, 5.0]
    })

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=completion_data['Type'],
        y=completion_data['Time (minutes)'],
        name='Actual',
        marker_color='#0ea5e9'
    ))
    fig.add_trace(go.Scatter(
        x=completion_data['Type'],
        y=completion_data['Target'],
        name='Target',
        mode='markers+lines',
        marker=dict(color='#ef4444', size=10),
        line=dict(color='#ef4444', dash='dash')
    ))
    fig.update_layout(
        template='plotly_dark',
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# Row 2: Quality Metrics
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 SBAR Quality Distribution")

    quality_data = pd.DataFrame({
        'Score Range': ['90-100%', '80-89%', '70-79%', '60-69%', '<60%'],
        'Count': [892, 243, 87, 19, 6],
        'Percentage': [71.5, 19.5, 7.0, 1.5, 0.5]
    })

    fig = px.pie(
        quality_data,
        values='Count',
        names='Score Range',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig.update_layout(
        template='plotly_dark',
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Handoffs by Department")

    dept_data = pd.DataFrame({
        'Department': ['Emergency', 'ICU', 'Med-Surg', 'Pediatrics', 'Surgery', 'Other'],
        'Handoffs': [342, 289, 256, 178, 123, 59]
    })

    fig = px.bar(
        dept_data,
        x='Department',
        y='Handoffs',
        color='Handoffs',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        template='plotly_dark',
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# Provider Performance
st.markdown("---")
st.subheader("👨‍⚕️ Provider Performance")

provider_data = pd.DataFrame({
    'Provider': ['Dr. Smith', 'Dr. Johnson', 'Nurse Williams', 'Dr. Brown', 'Nurse Davis',
                 'Dr. Garcia', 'Nurse Martinez', 'Dr. Wilson', 'Nurse Anderson', 'Dr. Taylor'],
    'Handoffs': [89, 76, 103, 82, 95, 71, 88, 79, 92, 67],
    'Avg Quality': [97.2, 95.8, 96.5, 94.3, 98.1, 93.7, 96.9, 95.2, 97.8, 94.8],
    'Completion Rate': [98, 96, 99, 93, 99, 91, 97, 95, 98, 94],
    'Avg Time (min)': [3.8, 4.2, 3.5, 5.1, 3.9, 4.8, 4.0, 4.5, 3.7, 4.3]
})

# Display as interactive table
st.dataframe(
    provider_data.style.background_gradient(subset=['Avg Quality', 'Completion Rate'], cmap='Blues')
                       .format({'Avg Quality': '{:.1f}%', 'Completion Rate': '{:.0f}%', 'Avg Time (min)': '{:.1f}'}),
    use_container_width=True,
    height=400
)

# Patient Safety Metrics
st.markdown("---")
st.subheader("🛡️ Patient Safety Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Critical Information Capture**")
    st.metric("Allergies Documented", "99.2%", "+0.3%")
    st.metric("Medications Listed", "98.7%", "+0.5%")
    st.metric("Vital Signs Included", "97.3%", "+1.2%")

with col2:
    st.markdown("**Adverse Events**")
    st.metric("Medication Errors", "0", "-100%")
    st.metric("Missed Handoffs", "2", "-75%")
    st.metric("Communication Gaps", "5", "-60%")

with col3:
    st.markdown("**Compliance Metrics**")
    st.metric("HIPAA Compliance", "100%", "0%")
    st.metric("Audit Trail Complete", "100%", "0%")
    st.metric("Required Fields", "98.9%", "+1.1%")

# Voice Recognition Metrics
st.markdown("---")
st.subheader("🎙️ Voice Recognition Performance")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Transcription Accuracy**")

    accuracy_data = pd.DataFrame({
        'Date': pd.date_range(end=datetime.now(), periods=14, freq='D'),
        'Accuracy': [random.uniform(94, 98) for _ in range(14)]
    })

    fig = px.line(
        accuracy_data,
        x='Date',
        y='Accuracy',
        markers=True
    )
    fig.update_layout(
        template='plotly_dark',
        height=250,
        margin=dict(l=0, r=0, t=30, b=0),
        yaxis_range=[90, 100]
    )
    fig.add_hline(y=95, line_dash="dash", line_color="red", annotation_text="Target: 95%")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Average Recording Duration**")

    duration_data = pd.DataFrame({
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Duration (min)': [2.8, 2.5, 2.3, 2.1]
    })

    fig = px.bar(
        duration_data,
        x='Week',
        y='Duration (min)',
        color='Duration (min)',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        template='plotly_dark',
        height=250,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# System Performance
st.markdown("---")
st.subheader("⚡ System Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("API Response Time", "142ms", "-18ms")
    st.metric("Uptime", "99.97%", "+0.02%")

with col2:
    st.metric("SBAR Generation Time", "2.3s", "-0.4s")
    st.metric("Database Queries", "1,247", "+12%")

with col3:
    st.metric("Active Users", "87", "+5")
    st.metric("Concurrent Sessions", "23", "+3")

with col4:
    st.metric("Storage Used", "1.2 TB", "+45 GB")
    st.metric("API Calls", "12,470", "+8%")

# Export Options
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Export to Excel", use_container_width=True):
        st.success("✅ Excel report generated!")

with col2:
    if st.button("📄 Generate PDF Report", use_container_width=True):
        st.success("✅ PDF report created!")

with col3:
    if st.button("📧 Email Report", use_container_width=True):
        st.success("✅ Report sent!")

with col4:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

# Insights and Recommendations
with st.expander("💡 AI-Powered Insights & Recommendations"):
    st.markdown("""
    ### Key Insights from Last 30 Days

    ✅ **Positive Trends:**
    - Handoff completion time decreased by 18% (now 4.2 min average)
    - SBAR quality scores improved to 96.5% average
    - Zero medication errors reported
    - Emergency department adoption increased by 23%

    ⚠️ **Areas for Improvement:**
    - 5.2% of handoffs still incomplete (down from 7.3%)
    - Surgery department has lower adoption (15% vs 40% hospital average)
    - 3 providers below 95% completion rate threshold
    - Weekend handoff volume 22% lower than weekdays

    🎯 **Recommendations:**
    1. **Provider Training**: Offer refresher training for 3 providers with <95% completion rate
    2. **Surgery Department**: Conduct focused implementation sessions with surgery staff
    3. **Weekend Coverage**: Analyze staffing patterns and consider incentives for weekend adoption
    4. **Quality Monitoring**: Set up automated alerts for handoffs with <90% quality scores
    5. **Best Practices**: Share Dr. Brown's workflow (98.1% avg quality) across departments

    📈 **Projected Impact:**
    - Expected 10% improvement in completion rate within 60 days
    - Potential 30-minute daily time savings per provider
    - Estimated 5% reduction in adverse events
    """)
