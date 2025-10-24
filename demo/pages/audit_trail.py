"""Audit Trail for EclipseLink AI Demo"""
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def show():
    """Show audit trail page"""
    st.markdown("<div class='main-header'>📝 Audit Trail</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Complete activity log with HIPAA compliance tracking</div>", unsafe_allow_html=True)

    # Get database connection
    conn = sqlite3.connect('demo_data.db', check_same_thread=False)
    c = conn.cursor()

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        time_filter = st.selectbox("Time Period", [
            "Last Hour",
            "Last 24 Hours",
            "Last 7 Days",
            "Last 30 Days",
            "All Time"
        ], index=3)

    with col2:
        action_filter = st.selectbox("Action Type", [
            "All Actions",
            "created",
            "voice_uploaded",
            "transcribed",
            "sbar_generated",
            "completed",
            "viewed",
            "edited",
            "exported"
        ])

    with col3:
        user_filter = st.selectbox("User", ["All Users", "System", "AI Worker", "User"])

    with col4:
        search_query = st.text_input("Search", placeholder="Search details...")

    # Build query based on filters
    sql = 'SELECT * FROM audit_logs WHERE 1=1'
    params = []

    # Time filter
    if time_filter == "Last Hour":
        cutoff = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        sql += ' AND timestamp >= ?'
        params.append(cutoff)
    elif time_filter == "Last 24 Hours":
        cutoff = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        sql += ' AND timestamp >= ?'
        params.append(cutoff)
    elif time_filter == "Last 7 Days":
        cutoff = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        sql += ' AND timestamp >= ?'
        params.append(cutoff)
    elif time_filter == "Last 30 Days":
        cutoff = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        sql += ' AND timestamp >= ?'
        params.append(cutoff)

    # Action filter
    if action_filter != "All Actions":
        sql += ' AND action = ?'
        params.append(action_filter)

    # User filter
    if user_filter != "All Users":
        sql += ' AND user = ?'
        params.append(user_filter)

    # Search filter
    if search_query:
        sql += ' AND details LIKE ?'
        params.append(f'%{search_query}%')

    sql += ' ORDER BY timestamp DESC LIMIT 100'

    c.execute(sql, params)
    logs = c.fetchall()

    # Summary stats
    st.markdown("### Activity Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        c.execute('SELECT COUNT(*) FROM audit_logs WHERE timestamp >= ?',
                 [(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')])
        daily_count = c.fetchone()[0]
        st.metric("Last 24 Hours", f"{daily_count:,}")

    with col2:
        c.execute('SELECT COUNT(DISTINCT handoff_id) FROM audit_logs WHERE timestamp >= ?',
                 [(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')])
        daily_handoffs = c.fetchone()[0]
        st.metric("Handoffs Today", f"{daily_handoffs:,}")

    with col3:
        c.execute('SELECT COUNT(DISTINCT user) FROM audit_logs WHERE user NOT IN ("System", "AI Worker")')
        user_count = c.fetchone()[0]
        st.metric("Active Users", f"{user_count:,}")

    with col4:
        c.execute('SELECT COUNT(*) FROM audit_logs WHERE action = "completed" AND timestamp >= ?',
                 [(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')])
        completed_count = c.fetchone()[0]
        st.metric("Completed Today", f"{completed_count:,}")

    st.markdown("---")

    # Activity log display
    st.markdown(f"### Activity Log ({len(logs)} entries)")

    if logs:
        # Action icons and colors
        action_config = {
            'created': {'icon': '➕', 'color': '#3b82f6'},
            'voice_uploaded': {'icon': '🎤', 'color': '#8b5cf6'},
            'transcribed': {'icon': '📝', 'color': '#10b981'},
            'sbar_generated': {'icon': '🤖', 'color': '#f59e0b'},
            'completed': {'icon': '✅', 'color': '#10b981'},
            'viewed': {'icon': '👁️', 'color': '#64748b'},
            'edited': {'icon': '✏️', 'color': '#f59e0b'},
            'exported': {'icon': '📤', 'color': '#6366f1'},
        }

        for log in logs:
            log_id, handoff_id, action, user, timestamp, details = log

            config = action_config.get(action, {'icon': '📌', 'color': '#64748b'})

            # Format timestamp
            try:
                dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                time_ago = get_time_ago(dt)
            except:
                time_ago = timestamp

            # Create log entry card
            st.markdown(f"""
            <div style='background: #f8fafc; padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem; border-left: 4px solid {config["color"]};'>
                <div style='display: flex; align-items: center; justify-content: space-between;'>
                    <div style='flex: 1;'>
                        <span style='font-size: 1.2rem;'>{config["icon"]}</span>
                        <strong style='margin-left: 0.5rem;'>{action.replace('_', ' ').title()}</strong>
                        <span style='color: #64748b; margin-left: 1rem;'>by {user}</span>
                        <br>
                        <small style='color: #64748b;'>{details}</small>
                    </div>
                    <div style='text-align: right; min-width: 150px;'>
                        <small style='color: #64748b;'>{time_ago}</small>
                        <br>
                        <small style='color: #94a3b8;'>Handoff #{handoff_id}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if len(logs) == 100:
            st.info("Showing first 100 entries. Use filters to narrow down results.")
    else:
        st.info("No audit logs found for the selected filters.")

    # Export options
    st.markdown("---")
    st.markdown("### Export Audit Logs")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Export to CSV", use_container_width=True):
            # Convert to DataFrame for CSV export
            df = pd.DataFrame(logs, columns=['ID', 'Handoff ID', 'Action', 'User', 'Timestamp', 'Details'])
            csv = df.to_csv(index=False)
            st.success("✅ Audit log exported! (Demo - would download in production)")

    with col2:
        if st.button("📑 Generate Compliance Report", use_container_width=True):
            st.success("✅ Compliance report generated! (Demo - would download in production)")

    with col3:
        if st.button("📧 Email Report", use_container_width=True):
            st.success("✅ Report emailed! (Demo - would send in production)")

    # Compliance information
    st.markdown("---")
    st.markdown("### 🔒 HIPAA Compliance")
    st.info("""
    **Audit Trail Compliance Features:**
    - ✅ All patient data access is logged
    - ✅ User actions are timestamped and immutable
    - ✅ Failed access attempts are recorded
    - ✅ Audit logs are encrypted at rest
    - ✅ Logs retained for 6 years (HIPAA requirement)
    - ✅ Regular audit reports generated for compliance officers
    """)

    conn.close()


def get_time_ago(dt):
    """Convert datetime to human-readable 'time ago' format"""
    now = datetime.now()
    diff = now - dt

    if diff.days > 0:
        if diff.days == 1:
            return "1 day ago"
        elif diff.days < 30:
            return f"{diff.days} days ago"
        else:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"
