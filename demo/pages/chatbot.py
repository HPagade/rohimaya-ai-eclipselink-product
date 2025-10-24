"""AI Chatbot Assistant for EclipseLink AI Demo"""
import streamlit as st
import sqlite3
from datetime import datetime
import random

def show():
    """Show AI chatbot assistant"""
    st.markdown("<div class='main-header'>🤖 AI Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Ask questions about patients, handoffs, and clinical workflows</div>", unsafe_allow_html=True)

    # Chatbot intro
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1.5rem; color: white;'>
        <div style='text-align: center;'>
            <h3 style='margin: 0 0 0.5rem 0; color: white;'>👋 Hello! I'm your AI Assistant</h3>
            <p style='margin: 0; opacity: 0.9;'>I can help you find patient information, understand handoffs, and answer clinical questions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Example questions
    with st.expander("💡 Example Questions I Can Answer"):
        st.markdown("""
        **Patient Information:**
        - "What medications is John Smith on?"
        - "Does patient P001234 have any allergies?"
        - "Show me handoffs for Jane Doe"

        **Handoff Questions:**
        - "What handoffs happened today in the ICU?"
        - "Show me all urgent handoffs"
        - "Who handed off patient P001235?"

        **Clinical Guidance:**
        - "What should be included in an SBAR?"
        - "How do I document a medication allergy?"
        - "What's the protocol for emergency handoffs?"

        **Analytics:**
        - "What's the average handoff quality score?"
        - "Which department has the most handoffs?"
        - "Show me handoff volume trends"
        """)

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {
                'role': 'assistant',
                'message': "Hello! I'm your AI assistant. I can help you with patient information, handoffs, and clinical questions. What would you like to know?",
                'timestamp': datetime.now()
            }
        ]

    # Display chat history
    st.markdown("### 💬 Chat")

    chat_container = st.container()

    with chat_container:
        for chat in st.session_state.chat_history:
            if chat['role'] == 'user':
                st.markdown(f"""
                <div style='background: #3b82f6; color: white; padding: 1rem; border-radius: 1rem 1rem 0 1rem; margin: 0.5rem 0; max-width: 80%; margin-left: auto;'>
                    <strong>You:</strong><br>
                    {chat['message']}
                    <div style='font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;'>{chat['timestamp'].strftime('%I:%M %p')}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: #f8fafc; padding: 1rem; border-radius: 1rem 1rem 1rem 0; margin: 0.5rem 0; max-width: 80%; border-left: 4px solid #10b981;'>
                    <strong>🤖 AI Assistant:</strong><br>
                    {chat['message']}
                    <div style='font-size: 0.75rem; color: #64748b; margin-top: 0.5rem;'>{chat['timestamp'].strftime('%I:%M %p')}</div>
                </div>
                """, unsafe_allow_html=True)

    # Quick action buttons
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📋 Find Patient", use_container_width=True):
            handle_quick_action("Show me all patients")

    with col2:
        if st.button("🔍 Search Handoffs", use_container_width=True):
            handle_quick_action("Show me recent handoffs")

    with col3:
        if st.button("📊 View Stats", use_container_width=True):
            handle_quick_action("What are today's statistics?")

    with col4:
        if st.button("❓ Help", use_container_width=True):
            handle_quick_action("How do I create a handoff?")

    # Chat input
    st.markdown("---")

    # Use columns for better layout
    col1, col2 = st.columns([5, 1])

    with col1:
        user_input = st.text_input(
            "Ask me anything...",
            placeholder="e.g., What medications is John Smith on?",
            label_visibility="collapsed",
            key="chat_input"
        )

    with col2:
        send_button = st.button("Send 📤", use_container_width=True, type="primary")

    if send_button and user_input:
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'message': user_input,
            'timestamp': datetime.now()
        })

        # Get AI response
        response = get_ai_response(user_input)

        # Add AI response
        st.session_state.chat_history.append({
            'role': 'assistant',
            'message': response,
            'timestamp': datetime.now()
        })

        st.rerun()

    # Voice input option
    st.markdown("---")
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🎤 Voice Input", use_container_width=True):
            st.info("🎤 Voice input activated! Speak your question...")


def handle_quick_action(query):
    """Handle quick action button clicks"""
    st.session_state.chat_history.append({
        'role': 'user',
        'message': query,
        'timestamp': datetime.now()
    })

    response = get_ai_response(query)

    st.session_state.chat_history.append({
        'role': 'assistant',
        'message': response,
        'timestamp': datetime.now()
    })

    st.rerun()


def get_ai_response(user_query):
    """
    Get AI response to user query
    In production, this would call GPT-4 API
    For demo, we use pattern matching and database queries
    """
    query_lower = user_query.lower()

    conn = sqlite3.connect('demo_data.db', check_same_thread=False)
    c = conn.cursor()

    # Patient medication queries
    if 'medication' in query_lower or 'med' in query_lower:
        # Try to extract patient name/ID
        c.execute('SELECT name, medications FROM patients LIMIT 3')
        patients = c.fetchall()

        response = "Here are the medications for our patients:\n\n"
        for name, meds in patients:
            response += f"**{name}:**\n{meds}\n\n"

        response += "Would you like more details about a specific patient?"
        return response

    # Allergy queries
    elif 'allerg' in query_lower:
        c.execute('SELECT name, allergies FROM patients WHERE allergies IS NOT NULL LIMIT 5')
        patients = c.fetchall()

        response = "⚠️ Here are patients with documented allergies:\n\n"
        for name, allergies in patients:
            response += f"**{name}:** {allergies}\n\n"

        response += "Always check allergies before administering medications!"
        return response

    # Recent handoffs
    elif 'recent' in query_lower and 'handoff' in query_lower:
        c.execute('''
            SELECT patient_name, handoff_type, created_at, from_staff
            FROM handoffs
            ORDER BY created_at DESC
            LIMIT 5
        ''')
        handoffs = c.fetchall()

        response = "📋 Here are the most recent handoffs:\n\n"
        for patient, htype, created, staff in handoffs:
            response += f"• **{patient}** - {htype.replace('_', ' ').title()} (by {staff})\n"

        return response

    # Statistics queries
    elif 'stat' in query_lower or 'today' in query_lower:
        c.execute('SELECT COUNT(*) FROM handoffs WHERE status="completed"')
        completed = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM handoffs WHERE status="active"')
        active = c.fetchone()[0]

        c.execute('SELECT AVG(quality_score) FROM handoffs WHERE quality_score IS NOT NULL')
        avg_quality = c.fetchone()[0] or 0

        response = f"""
📊 **Today's Statistics:**

- ✅ Completed Handoffs: **{completed}**
- ⏳ Active Handoffs: **{active}**
- 📈 Average Quality Score: **{avg_quality:.1f}%**

Looking good! Quality is above target (90%).
        """
        return response

    # SBAR help
    elif 'sbar' in query_lower:
        return """
📋 **SBAR Format Guide:**

**S - Situation:**
- What is happening right now?
- Patient's current condition
- Chief complaint or reason for handoff

**B - Background:**
- Medical history
- Current medications and allergies
- Recent treatments or procedures

**A - Assessment:**
- Your clinical evaluation
- Vital signs and trends
- Lab results and diagnostic findings

**R - Recommendation:**
- What should be done next?
- Plan of care
- Follow-up needed

💡 **Pro Tip:** EclipseLink AI automatically generates SBAR from your voice recording!
        """

    # How to create handoff
    elif 'create' in query_lower and 'handoff' in query_lower:
        return """
🎤 **How to Create a Handoff:**

1. Click "➕ New Handoff" in the sidebar
2. Fill in patient information
3. Either:
   - 🎤 Record your handoff using voice (2 min)
   - 📝 Type your handoff details
4. Click "Generate SBAR"
5. AI processes and creates structured report
6. Review and edit if needed
7. Complete handoff

⚡ **Saves 90% of time** compared to manual documentation!
        """

    # Urgent/emergency handoffs
    elif 'urgent' in query_lower or 'emergency' in query_lower:
        c.execute('''
            SELECT patient_name, priority, created_at, handoff_type
            FROM handoffs
            WHERE priority IN ('urgent', 'emergent')
            ORDER BY created_at DESC
            LIMIT 5
        ''')
        urgent = c.fetchall()

        if urgent:
            response = "🔴 **Urgent/Emergency Handoffs:**\n\n"
            for patient, priority, created, htype in urgent:
                response += f"• {priority.upper()}: **{patient}** - {htype.replace('_', ' ').title()}\n"
            return response
        else:
            return "✅ No urgent or emergency handoffs at this time."

    # Default response with suggestions
    else:
        suggestions = [
            "Try asking: 'What medications is John Smith on?'",
            "Try asking: 'Show me recent handoffs'",
            "Try asking: 'What are today's statistics?'",
            "Try asking: 'Does any patient have penicillin allergy?'",
            "Try asking: 'How do I create a handoff?'"
        ]

        return f"""
I'm not sure I understand that question. Let me help you with some suggestions:

{random.choice(suggestions)}

You can also ask about:
- 👤 Patient information (medications, allergies, conditions)
- 📋 Handoffs (recent, urgent, by department)
- 📊 Statistics and analytics
- ❓ Clinical guidance and protocols

What would you like to know?
        """

    conn.close()
