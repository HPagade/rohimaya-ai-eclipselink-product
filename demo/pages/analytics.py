"""Analytics Dashboard for EclipseLink AI Demo"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database import get_analytics_data
import sqlite3

def show():
    """Show analytics dashboard"""
    st.markdown("<div class='main-header'>📊 Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Insights and metrics from your handoffs</div>", unsafe_allow_html=True)

    # Get database connection
    conn = sqlite3.connect('demo_data.db', check_same_thread=False)

    # Get analytics data
    analytics = get_analytics_data(conn)

    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Avg Quality Score", f"{analytics['avg_quality']:.1f}%", "↑ 2.3%")

    with col2:
        st.metric("Avg Completeness", f"{analytics['avg_completeness']:.1f}%", "↑ 1.8%")

    with col3:
        st.metric("Avg Critical Elements", f"{analytics['avg_critical']:.1f}%", "↑ 3.1%")

    with col4:
        avg_min = int(analytics['avg_duration'] // 60)
        avg_sec = int(analytics['avg_duration'] % 60)
        st.metric("Avg Duration", f"{avg_min}:{avg_sec:02d}", "↓ 15s")

    st.markdown("---")

    # Charts Row 1: Handoffs by Type and Priority
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Handoffs by Type")
        if analytics['handoffs_by_type']:
            df_type = pd.DataFrame(analytics['handoffs_by_type'], columns=['Type', 'Count'])
            df_type['Type'] = df_type['Type'].str.replace('_', ' ').str.title()

            fig = px.pie(df_type, values='Count', names='Type',
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hole=0.4)
            fig.update_layout(
                showlegend=True,
                height=400,
                margin=dict(t=30, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available")

    with col2:
        st.markdown("### Handoffs by Priority")
        if analytics['handoffs_by_priority']:
            df_priority = pd.DataFrame(analytics['handoffs_by_priority'], columns=['Priority', 'Count'])
            df_priority['Priority'] = df_priority['Priority'].str.title()

            colors = {'Routine': '#10b981', 'Urgent': '#f59e0b', 'Emergent': '#ef4444'}
            df_priority['Color'] = df_priority['Priority'].map(colors)

            fig = go.Figure(data=[go.Bar(
                x=df_priority['Priority'],
                y=df_priority['Count'],
                marker_color=df_priority['Color'],
                text=df_priority['Count'],
                textposition='auto',
            )])
            fig.update_layout(
                showlegend=False,
                height=400,
                margin=dict(t=30, b=50, l=50, r=0),
                xaxis_title="Priority Level",
                yaxis_title="Count"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available")

    # Charts Row 2: Specialty Distribution and Daily Trend
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Top Specialties")
        if analytics['handoffs_by_specialty']:
            df_specialty = pd.DataFrame(analytics['handoffs_by_specialty'], columns=['Specialty', 'Count'])

            fig = go.Figure(data=[go.Bar(
                y=df_specialty['Specialty'],
                x=df_specialty['Count'],
                orientation='h',
                marker_color='#667eea',
                text=df_specialty['Count'],
                textposition='auto',
            )])
            fig.update_layout(
                showlegend=False,
                height=400,
                margin=dict(t=30, b=50, l=150, r=0),
                xaxis_title="Count",
                yaxis_title="Specialty"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available")

    with col2:
        st.markdown("### Daily Handoff Volume (Last 30 Days)")
        if analytics['daily_handoffs']:
            df_daily = pd.DataFrame(analytics['daily_handoffs'], columns=['Date', 'Count'])
            df_daily['Date'] = pd.to_datetime(df_daily['Date'])

            fig = px.line(df_daily, x='Date', y='Count',
                         markers=True,
                         line_shape='spline')
            fig.update_traces(
                line_color='#3b82f6',
                marker=dict(size=8, color='#1e40af')
            )
            fig.update_layout(
                showlegend=False,
                height=400,
                margin=dict(t=30, b=50, l=50, r=0),
                xaxis_title="Date",
                yaxis_title="Handoffs"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available")

    # Quality Metrics Distribution
    st.markdown("### Quality Metrics Distribution")

    c = conn.cursor()
    c.execute('''
        SELECT quality_score, completeness_score, critical_elements_score
        FROM handoffs
        WHERE status = 'completed' AND quality_score IS NOT NULL
    ''')
    scores_data = c.fetchall()

    if scores_data:
        df_scores = pd.DataFrame(scores_data, columns=['Quality', 'Completeness', 'Critical Elements'])

        fig = go.Figure()
        fig.add_trace(go.Box(y=df_scores['Quality'], name='Quality Score', marker_color='#3b82f6'))
        fig.add_trace(go.Box(y=df_scores['Completeness'], name='Completeness Score', marker_color='#10b981'))
        fig.add_trace(go.Box(y=df_scores['Critical Elements'], name='Critical Elements', marker_color='#f59e0b'))

        fig.update_layout(
            showlegend=True,
            height=400,
            yaxis_title="Score (%)",
            margin=dict(t=30, b=50, l=50, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No quality data available")

    # Performance by Staff
    st.markdown("### Top Performers (By Handoff Count)")

    c.execute('''
        SELECT from_staff, COUNT(*) as count, AVG(quality_score) as avg_quality
        FROM handoffs
        WHERE status = 'completed' AND from_staff IS NOT NULL
        GROUP BY from_staff
        ORDER BY count DESC
        LIMIT 10
    ''')
    staff_data = c.fetchall()

    if staff_data:
        df_staff = pd.DataFrame(staff_data, columns=['Staff', 'Handoffs', 'Avg Quality'])

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(df_staff, x='Staff', y='Handoffs',
                        color='Avg Quality',
                        color_continuous_scale='viridis',
                        labels={'Avg Quality': 'Quality Score'})
            fig.update_layout(
                height=400,
                margin=dict(t=30, b=100, l=50, r=0),
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Detailed Staff Performance")
            for idx, row in df_staff.iterrows():
                staff, count, avg_q = row
                st.markdown(f"""
                <div style='background: #f8fafc; padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem; border-left: 4px solid #3b82f6;'>
                    <strong>{staff}</strong><br>
                    <small style='color: #64748b;'>
                        {int(count)} handoffs • {avg_q:.1f}% quality
                    </small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No staff performance data available")

    # Time-based Analysis
    st.markdown("### Handoff Timing Analysis")

    c.execute('''
        SELECT
            CAST(strftime('%H', created_at) AS INTEGER) as hour,
            COUNT(*) as count
        FROM handoffs
        WHERE status = 'completed'
        GROUP BY hour
        ORDER BY hour
    ''')
    hourly_data = c.fetchall()

    if hourly_data:
        df_hourly = pd.DataFrame(hourly_data, columns=['Hour', 'Count'])

        fig = px.bar(df_hourly, x='Hour', y='Count',
                    labels={'Hour': 'Hour of Day (24hr)', 'Count': 'Handoffs'},
                    color='Count',
                    color_continuous_scale='blues')
        fig.update_layout(
            height=400,
            margin=dict(t=30, b=50, l=50, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Peak hours insight
        peak_hour = df_hourly.loc[df_hourly['Count'].idxmax(), 'Hour']
        peak_count = df_hourly.loc[df_hourly['Count'].idxmax(), 'Count']
        st.info(f"**Peak Handoff Time:** {peak_hour:02d}:00 with {int(peak_count)} handoffs")
    else:
        st.info("No timing data available")

    # Export Data
    st.markdown("---")
    st.markdown("### Export Analytics Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Export Charts (PNG)", use_container_width=True):
            st.success("Charts exported! (Demo - would download in production)")

    with col2:
        if st.button("📈 Export Data (CSV)", use_container_width=True):
            st.success("Data exported! (Demo - would download in production)")

    with col3:
        if st.button("📑 Generate Report (PDF)", use_container_width=True):
            st.success("Report generated! (Demo - would download in production)")

    conn.close()
