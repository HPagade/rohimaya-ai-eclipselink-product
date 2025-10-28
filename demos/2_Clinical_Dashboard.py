"""
EclipseLink AI - Clinical Dashboard Demo
Interactive dashboard showing handoff management and analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Clinical Dashboard - EclipseLink AI",
    page_icon="📊",
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
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .status-badge {{
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
    }}
    .status-pending {{
        background-color: #ffeaa7;
        color: #2d3436;
    }}
    .status-processing {{
        background-color: {PHOENIX_GOLD};
        color: {ECLIPSE_NAVY};
    }}
    .status-completed {{
        background-color: {PEACOCK_TEAL};
        color: white;
    }}
    .status-approved {{
        background-color: #00b894;
        color: white;
    }}
    .patient-card {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid {PEACOCK_TEAL};
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    .priority-high {{
        border-left-color: #d63031;
    }}
    .priority-medium {{
        border-left-color: {PHOENIX_GOLD};
    }}
    .priority-low {{
        border-left-color: {PEACOCK_TEAL};
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 Clinical Dashboard</h1>
    <p style="font-size: 1.2rem; margin: 0;">Real-time handoff management and analytics</p>
</div>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def generate_handoff_data():
    """Generate sample handoff data for demonstration"""
    statuses = ['Pending', 'Processing', 'Completed', 'Approved']
    priorities = ['High', 'Medium', 'Low']
    departments = ['ICU', 'Emergency', 'Medical-Surgical', 'Cardiac', 'Pediatrics']

    data = []
    for i in range(50):
        created = datetime.now() - timedelta(hours=random.randint(0, 72))
        status = random.choice(statuses)

        record = {
            'id': f'HO-{1000+i}',
            'patient_name': f'{random.choice(["John", "Sarah", "Michael", "Emily", "David", "Lisa"])} {random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"])}',
            'mrn': f'MRN-{random.randint(100000, 999999)}',
            'department': random.choice(departments),
            'priority': random.choice(priorities),
            'status': status,
            'created_at': created,
            'created_by': f'Dr. {random.choice(["Williams", "Chen", "Patel", "Garcia", "Anderson"])}',
            'processing_time': random.randint(15, 45) if status != 'Pending' else None,
            'accuracy_score': random.uniform(0.92, 0.99) if status in ['Completed', 'Approved'] else None
        }
        data.append(record)

    return pd.DataFrame(data)

# Generate analytics data
@st.cache_data
def generate_analytics_data():
    """Generate analytics data for charts"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')

    # Daily handoffs
    daily_handoffs = pd.DataFrame({
        'date': dates,
        'handoffs': [random.randint(15, 45) for _ in range(30)]
    })

    # Department distribution
    departments = ['ICU', 'Emergency', 'Medical-Surgical', 'Cardiac', 'Pediatrics', 'Other']
    dept_dist = pd.DataFrame({
        'department': departments,
        'count': [45, 38, 52, 28, 22, 15]
    })

    # Time savings
    time_data = pd.DataFrame({
        'month': ['Oct', 'Nov', 'Dec', 'Jan'],
        'manual_time': [320, 315, 310, 305],
        'ai_time': [35, 32, 30, 28]
    })

    return daily_handoffs, dept_dist, time_data

df_handoffs = generate_handoff_data()
daily_handoffs, dept_dist, time_data = generate_analytics_data()

# Sidebar - Filters
with st.sidebar:
    st.image("https://img.shields.io/badge/EclipseLink-AI-1a9b8e?style=for-the-badge", use_container_width=True)
    st.markdown("---")
    st.markdown("### Dashboard Filters")

    selected_department = st.multiselect(
        "Department",
        options=['All'] + sorted(df_handoffs['department'].unique().tolist()),
        default=['All']
    )

    selected_status = st.multiselect(
        "Status",
        options=['All'] + sorted(df_handoffs['status'].unique().tolist()),
        default=['All']
    )

    selected_priority = st.multiselect(
        "Priority",
        options=['All'] + ['High', 'Medium', 'Low'],
        default=['All']
    )

    date_range = st.date_input(
        "Date Range",
        value=(datetime.now() - timedelta(days=7), datetime.now()),
        max_value=datetime.now()
    )

    st.markdown("---")

    # Quick actions
    st.markdown("### Quick Actions")
    if st.button("🎙️ New Handoff", use_container_width=True, type="primary"):
        st.info("Opening Voice Recorder...")

    if st.button("📊 Export Report", use_container_width=True):
        st.success("Report exported successfully!")

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Filter data
filtered_df = df_handoffs.copy()

if 'All' not in selected_department and selected_department:
    filtered_df = filtered_df[filtered_df['department'].isin(selected_department)]

if 'All' not in selected_status and selected_status:
    filtered_df = filtered_df[filtered_df['status'].isin(selected_status)]

if 'All' not in selected_priority and selected_priority:
    filtered_df = filtered_df[filtered_df['priority'].isin(selected_priority)]

# Key Metrics
st.markdown("### Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_handoffs = len(filtered_df)
    st.metric("Total Handoffs", total_handoffs, f"+{random.randint(2, 8)} today")

with col2:
    pending = len(filtered_df[filtered_df['status'] == 'Pending'])
    st.metric("Pending", pending, delta_color="inverse")

with col3:
    processing = len(filtered_df[filtered_df['status'] == 'Processing'])
    st.metric("Processing", processing)

with col4:
    completed = len(filtered_df[filtered_df['status'].isin(['Completed', 'Approved'])])
    completion_rate = (completed / total_handoffs * 100) if total_handoffs > 0 else 0
    st.metric("Completed", f"{completion_rate:.1f}%", f"+{random.randint(1, 5)}%")

with col5:
    avg_time = filtered_df['processing_time'].mean()
    if pd.notna(avg_time):
        st.metric("Avg Processing", f"{avg_time:.0f}s", f"-{random.randint(2, 5)}s")
    else:
        st.metric("Avg Processing", "N/A")

st.markdown("---")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Active Handoffs", "📈 Analytics", "👥 Team Activity", "⚠️ Alerts"])

with tab1:
    st.markdown("### Active Handoffs")

    # View selector
    view_mode = st.radio(
        "View Mode",
        ["List View", "Card View", "Timeline"],
        horizontal=True
    )

    if view_mode == "List View":
        # Display as table
        display_df = filtered_df[[
            'id', 'patient_name', 'mrn', 'department',
            'priority', 'status', 'created_at', 'created_by'
        ]].copy()

        display_df['created_at'] = display_df['created_at'].dt.strftime('%Y-%m-%d %H:%M')

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.TextColumn("Handoff ID", width="small"),
                "patient_name": st.column_config.TextColumn("Patient", width="medium"),
                "mrn": st.column_config.TextColumn("MRN", width="small"),
                "department": st.column_config.TextColumn("Department", width="medium"),
                "priority": st.column_config.TextColumn("Priority", width="small"),
                "status": st.column_config.TextColumn("Status", width="small"),
                "created_at": st.column_config.TextColumn("Created", width="medium"),
                "created_by": st.column_config.TextColumn("Created By", width="medium"),
            }
        )

    elif view_mode == "Card View":
        # Display as cards
        for _, row in filtered_df.head(10).iterrows():
            priority_class = f"priority-{row['priority'].lower()}"
            status_class = f"status-{row['status'].lower()}"

            st.markdown(f"""
            <div class="patient-card {priority_class}">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h4 style="margin: 0 0 0.5rem 0;">{row['patient_name']}</h4>
                        <p style="margin: 0; color: #666; font-size: 0.9rem;">
                            {row['mrn']} • {row['department']} • {row['id']}
                        </p>
                    </div>
                    <span class="status-badge {status_class}">{row['status']}</span>
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #666;">
                    <strong>Priority:</strong> {row['priority']} •
                    <strong>Created:</strong> {row['created_at'].strftime('%Y-%m-%d %H:%M')} •
                    <strong>By:</strong> {row['created_by']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_a, col_b, col_c = st.columns([1, 1, 2])
            with col_a:
                if st.button("View Details", key=f"view_{row['id']}"):
                    st.info(f"Opening details for {row['id']}")
            with col_b:
                if st.button("Edit SBAR", key=f"edit_{row['id']}"):
                    st.info(f"Opening SBAR editor for {row['id']}")

            st.markdown("<br>", unsafe_allow_html=True)

    else:  # Timeline view
        st.info("Timeline view shows handoffs chronologically with processing stages")

        timeline_df = filtered_df.sort_values('created_at', ascending=False).head(15)

        for _, row in timeline_df.iterrows():
            time_ago = (datetime.now() - row['created_at']).total_seconds() / 3600
            if time_ago < 1:
                time_str = f"{int(time_ago * 60)} minutes ago"
            else:
                time_str = f"{int(time_ago)} hours ago"

            status_class = f"status-{row['status'].lower()}"

            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 1rem; padding: 0.5rem;">
                <div style="width: 100px; text-align: right; padding-right: 1rem; color: #666; font-size: 0.85rem;">
                    {time_str}
                </div>
                <div style="width: 4px; height: 40px; background: {PEACOCK_TEAL}; margin: 0 1rem;"></div>
                <div style="flex: 1;">
                    <strong>{row['patient_name']}</strong> ({row['department']})
                    <span class="status-badge {status_class}" style="margin-left: 1rem;">{row['status']}</span>
                    <br>
                    <span style="font-size: 0.85rem; color: #666;">{row['id']} • {row['created_by']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("### Analytics & Insights")

    # Charts row 1
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Daily Handoff Volume (Last 30 Days)")
        fig_daily = px.line(
            daily_handoffs,
            x='date',
            y='handoffs',
            title='',
            labels={'date': 'Date', 'handoffs': 'Number of Handoffs'}
        )
        fig_daily.update_traces(line_color=PEACOCK_TEAL, line_width=3)
        fig_daily.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=20, b=0),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_daily, use_container_width=True)

    with col2:
        st.markdown("#### Handoffs by Department")
        fig_dept = px.pie(
            dept_dist,
            values='count',
            names='department',
            title='',
            color_discrete_sequence=px.colors.sequential.Teal
        )
        fig_dept.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig_dept, use_container_width=True)

    # Charts row 2
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Time Savings Comparison")
        fig_time = go.Figure()
        fig_time.add_trace(go.Bar(
            name='Manual Entry',
            x=time_data['month'],
            y=time_data['manual_time'],
            marker_color='#e74c3c'
        ))
        fig_time.add_trace(go.Bar(
            name='AI-Powered',
            x=time_data['month'],
            y=time_data['ai_time'],
            marker_color=PEACOCK_TEAL
        ))
        fig_time.update_layout(
            barmode='group',
            height=300,
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis_title='',
            yaxis_title='Avg Time (seconds)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        st.plotly_chart(fig_time, use_container_width=True)

    with col4:
        st.markdown("#### Processing Time Distribution")

        processing_times = filtered_df[filtered_df['processing_time'].notna()]['processing_time']

        fig_dist = px.histogram(
            processing_times,
            nbins=20,
            title='',
            labels={'value': 'Processing Time (seconds)', 'count': 'Frequency'}
        )
        fig_dist.update_traces(marker_color=PEACOCK_TEAL)
        fig_dist.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=20, b=0),
            showlegend=False
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    # Performance metrics
    st.markdown("---")
    st.markdown("#### Performance Metrics")

    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a:
        st.metric("Avg Transcription Accuracy", "97.2%", "+0.3%")
    with col_b:
        st.metric("Avg SBAR Generation Time", "18.5s", "-2.1s")
    with col_c:
        st.metric("User Satisfaction Score", "4.8/5.0", "+0.2")
    with col_d:
        st.metric("EHR Export Success Rate", "99.1%", "+0.5%")

with tab3:
    st.markdown("### Team Activity")

    # Top users
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Most Active Users (This Week)")

        top_users = pd.DataFrame({
            'user': ['Dr. Williams', 'Dr. Chen', 'Dr. Patel', 'Dr. Garcia', 'Dr. Anderson'],
            'handoffs': [45, 38, 35, 32, 28],
            'avg_time': [32, 28, 35, 30, 33]
        })

        for _, user in top_users.iterrows():
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{user['user']}</strong><br>
                        <span style="color: #666; font-size: 0.9rem;">{user['handoffs']} handoffs</span>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: {PEACOCK_TEAL}; font-weight: bold;">{user['avg_time']}s</div>
                        <div style="color: #666; font-size: 0.85rem;">avg time</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### Department Performance")

        dept_performance = pd.DataFrame({
            'department': ['ICU', 'Emergency', 'Cardiac', 'Med-Surg', 'Pediatrics'],
            'completion_rate': [98, 95, 97, 93, 96],
            'avg_time': [35, 28, 32, 38, 30]
        })

        fig_perf = px.scatter(
            dept_performance,
            x='avg_time',
            y='completion_rate',
            size=[100]*5,
            text='department',
            title='',
            labels={'avg_time': 'Avg Processing Time (s)', 'completion_rate': 'Completion Rate (%)'}
        )
        fig_perf.update_traces(marker_color=PEACOCK_TEAL, textposition='top center')
        fig_perf.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig_perf, use_container_width=True)

with tab4:
    st.markdown("### System Alerts & Notifications")

    # Alert types
    alert_type = st.selectbox(
        "Filter by Type",
        ["All Alerts", "System", "Processing", "Security", "Compliance"]
    )

    alerts = [
        {
            'type': 'System',
            'severity': 'Info',
            'message': 'Scheduled maintenance completed successfully',
            'time': '2 hours ago',
            'icon': 'ℹ️'
        },
        {
            'type': 'Processing',
            'severity': 'Warning',
            'message': '3 handoffs taking longer than average to process',
            'time': '45 minutes ago',
            'icon': '⚠️'
        },
        {
            'type': 'Security',
            'severity': 'Info',
            'message': 'Daily security audit completed - no issues found',
            'time': '3 hours ago',
            'icon': '🔒'
        },
        {
            'type': 'Compliance',
            'severity': 'Success',
            'message': 'HIPAA compliance check passed for all active handoffs',
            'time': '5 hours ago',
            'icon': '✅'
        },
        {
            'type': 'System',
            'severity': 'Success',
            'message': 'Azure OpenAI API connection stable - 99.9% uptime',
            'time': '6 hours ago',
            'icon': '✅'
        }
    ]

    for alert in alerts:
        severity_colors = {
            'Info': '#3498db',
            'Warning': '#f39c12',
            'Success': '#2ecc71',
            'Error': '#e74c3c'
        }

        color = severity_colors.get(alert['severity'], '#95a5a6')

        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid {color}; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">{alert['icon']} <strong>{alert['type']}</strong></div>
                    <div style="margin-bottom: 0.5rem;">{alert['message']}</div>
                    <div style="color: #666; font-size: 0.85rem;">{alert['time']}</div>
                </div>
                <span style="background: {color}; color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.85rem; font-weight: bold;">
                    {alert['severity']}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>EclipseLink AI™</strong> - Real-time Clinical Handoff Management</p>
    <p style="font-size: 0.9rem;">© 2025 Rohimaya Health AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
