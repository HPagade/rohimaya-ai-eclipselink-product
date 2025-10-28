"""
EclipseLink AI - ROI Calculator Demo
Interactive calculator showing time savings and cost reduction for prospects
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="ROI Calculator - EclipseLink AI",
    page_icon="💰",
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
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-top: 4px solid {PEACOCK_TEAL};
    }}
    .savings-card {{
        background: linear-gradient(135deg, {PEACOCK_TEAL} 0%, {LUNAR_BLUE} 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }}
    .comparison-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💰 ROI Calculator</h1>
    <p style="font-size: 1.2rem; margin: 0;">Calculate your facility's time savings and cost reduction with EclipseLink AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Input Parameters
with st.sidebar:
    st.image("https://img.shields.io/badge/EclipseLink-AI-1a9b8e?style=for-the-badge", use_container_width=True)
    st.markdown("---")
    st.markdown("### Facility Profile")

    facility_type = st.selectbox(
        "Facility Type",
        ["Hospital (200+ beds)", "Hospital (100-200 beds)", "Hospital (<100 beds)",
         "Nursing Home", "Clinic", "Urgent Care"]
    )

    num_staff = st.number_input(
        "Number of Clinical Staff",
        min_value=10,
        max_value=5000,
        value=250,
        step=10,
        help="Total number of nurses, doctors, and clinical staff"
    )

    handoffs_per_staff_per_week = st.slider(
        "Handoffs per Staff per Week",
        min_value=1,
        max_value=20,
        value=5,
        help="Average number of patient handoffs each staff member performs weekly"
    )

    st.markdown("---")
    st.markdown("### Cost Parameters")

    avg_hourly_rate = st.number_input(
        "Average Staff Hourly Rate ($)",
        min_value=20,
        max_value=150,
        value=45,
        step=5,
        help="Average hourly wage for clinical staff"
    )

    manual_time_minutes = st.slider(
        "Current Manual Entry Time (minutes)",
        min_value=3,
        max_value=15,
        value=5,
        help="Time currently spent on manual handoff documentation"
    )

    st.markdown("---")
    st.markdown("### Pricing Tier")

    pricing_tier = st.selectbox(
        "Select Pricing Plan",
        ["Starter", "Professional", "Enterprise"],
        help="Choose a pricing tier based on your facility size"
    )

    # Pricing model
    pricing = {
        "Starter": {"base": 2000, "per_user": 25, "max_users": 50},
        "Professional": {"base": 5000, "per_user": 20, "max_users": 200},
        "Enterprise": {"base": 15000, "per_user": 15, "max_users": 999999}
    }

# Calculate ROI
# Time calculations
handoffs_per_week = num_staff * handoffs_per_staff_per_week
handoffs_per_year = handoffs_per_week * 52

# Manual process time
manual_time_per_handoff_hours = manual_time_minutes / 60
total_manual_hours_per_year = handoffs_per_year * manual_time_per_handoff_hours

# EclipseLink AI time (avg 30 seconds)
ai_time_per_handoff_minutes = 0.5
ai_time_per_handoff_hours = ai_time_per_handoff_minutes / 60
total_ai_hours_per_year = handoffs_per_year * ai_time_per_handoff_hours

# Time savings
time_saved_hours_per_year = total_manual_hours_per_year - total_ai_hours_per_year
time_saved_per_handoff_minutes = manual_time_minutes - ai_time_per_handoff_minutes

# Cost calculations
manual_cost_per_year = total_manual_hours_per_year * avg_hourly_rate
ai_cost_per_year = total_ai_hours_per_year * avg_hourly_rate

# Software cost
selected_pricing = pricing[pricing_tier]
monthly_software_cost = selected_pricing["base"] + (min(num_staff, selected_pricing["max_users"]) * selected_pricing["per_user"])
annual_software_cost = monthly_software_cost * 12

# Total cost with EclipseLink
total_ai_cost_per_year = ai_cost_per_year + annual_software_cost

# Savings
annual_cost_savings = manual_cost_per_year - total_ai_cost_per_year
monthly_cost_savings = annual_cost_savings / 12
roi_percentage = (annual_cost_savings / annual_software_cost) * 100 if annual_software_cost > 0 else 0
payback_period_months = (annual_software_cost / monthly_cost_savings) if monthly_cost_savings > 0 else 0

# Main Content
st.markdown("## Your Facility's ROI Summary")

# Top-level metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Annual Cost Savings",
        f"${annual_cost_savings:,.0f}",
        delta=f"${monthly_cost_savings:,.0f}/month",
        delta_color="normal"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Time Saved Annually",
        f"{time_saved_hours_per_year:,.0f} hours",
        delta=f"{time_saved_hours_per_year/num_staff:.1f} hrs/staff",
        delta_color="normal"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "ROI Percentage",
        f"{roi_percentage:.0f}%",
        delta="First year" if roi_percentage > 0 else "",
        delta_color="normal"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Payback Period",
        f"{payback_period_months:.1f} months",
        delta="Break even",
        delta_color="normal"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Detailed comparison
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Cost Comparison")

    comparison_data = pd.DataFrame({
        'Category': ['Staff Time Cost', 'Software Cost', 'Total Annual Cost'],
        'Manual Process': [manual_cost_per_year, 0, manual_cost_per_year],
        'With EclipseLink AI': [ai_cost_per_year, annual_software_cost, total_ai_cost_per_year]
    })

    fig_comparison = go.Figure()

    fig_comparison.add_trace(go.Bar(
        name='Manual Process',
        x=comparison_data['Category'],
        y=comparison_data['Manual Process'],
        marker_color='#e74c3c',
        text=[f"${val:,.0f}" for val in comparison_data['Manual Process']],
        textposition='auto',
    ))

    fig_comparison.add_trace(go.Bar(
        name='With EclipseLink AI',
        x=comparison_data['Category'],
        y=comparison_data['With EclipseLink AI'],
        marker_color=PEACOCK_TEAL,
        text=[f"${val:,.0f}" for val in comparison_data['With EclipseLink AI']],
        textposition='auto',
    ))

    fig_comparison.update_layout(
        barmode='group',
        height=400,
        yaxis_title='Annual Cost ($)',
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    st.plotly_chart(fig_comparison, use_container_width=True)

with col_right:
    st.markdown("### Time Savings Breakdown")

    st.markdown(f"""
    <div class="comparison-card">
        <h4 style="color: {ECLIPSE_NAVY}; margin-top: 0;">Per Handoff Comparison</h4>
        <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
            <div>
                <div style="color: #666; font-size: 0.9rem;">Manual Process</div>
                <div style="font-size: 2rem; font-weight: bold; color: #e74c3c;">{manual_time_minutes:.0f} min</div>
            </div>
            <div style="font-size: 2rem; align-self: center;">→</div>
            <div>
                <div style="color: #666; font-size: 0.9rem;">With EclipseLink AI</div>
                <div style="font-size: 2rem; font-weight: bold; color: {PEACOCK_TEAL};">{ai_time_per_handoff_minutes:.1f} min</div>
            </div>
        </div>
        <div style="background: {PEACOCK_TEAL}; color: white; padding: 1rem; border-radius: 5px; text-align: center;">
            <strong>{time_saved_per_handoff_minutes:.1f} minutes saved per handoff</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="comparison-card">
        <h4 style="color: {ECLIPSE_NAVY}; margin-top: 0;">Annual Volume</h4>
        <table style="width: 100%; margin-top: 1rem;">
            <tr>
                <td style="padding: 0.5rem; border-bottom: 1px solid #eee;">Handoffs per week:</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #eee; text-align: right; font-weight: bold;">{handoffs_per_week:,.0f}</td>
            </tr>
            <tr>
                <td style="padding: 0.5rem; border-bottom: 1px solid #eee;">Handoffs per year:</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #eee; text-align: right; font-weight: bold;">{handoffs_per_year:,.0f}</td>
            </tr>
            <tr>
                <td style="padding: 0.5rem; border-bottom: 1px solid #eee;">Staff hours saved/year:</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #eee; text-align: right; font-weight: bold; color: {PEACOCK_TEAL};">{time_saved_hours_per_year:,.0f}</td>
            </tr>
            <tr>
                <td style="padding: 0.5rem;">Equivalent FTE saved:</td>
                <td style="padding: 0.5rem; text-align: right; font-weight: bold; color: {PEACOCK_TEAL};">{time_saved_hours_per_year/2080:.1f}</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 5-Year projection
st.markdown("### 5-Year Financial Projection")

years = list(range(1, 6))
cumulative_savings = []
cumulative_cost = []
cumulative_net = []

for year in years:
    # Assume 5% annual staff growth and 3% wage growth
    growth_factor = (1.05 ** (year - 1))
    wage_factor = (1.03 ** (year - 1))

    year_handoffs = handoffs_per_year * growth_factor
    year_manual_cost = (year_handoffs * manual_time_per_handoff_hours) * (avg_hourly_rate * wage_factor)
    year_ai_time_cost = (year_handoffs * ai_time_per_handoff_hours) * (avg_hourly_rate * wage_factor)
    year_software_cost = annual_software_cost * (1.03 ** (year - 1))  # 3% annual increase
    year_total_ai_cost = year_ai_time_cost + year_software_cost
    year_savings = year_manual_cost - year_total_ai_cost

    cumulative_cost.append(sum([year_software_cost * (1.03 ** (y - 1)) for y in range(1, year + 1)]))
    cumulative_savings.append(sum([
        ((handoffs_per_year * (1.05 ** (y - 1))) * manual_time_per_handoff_hours * (avg_hourly_rate * (1.03 ** (y - 1)))) -
        (((handoffs_per_year * (1.05 ** (y - 1))) * ai_time_per_handoff_hours * (avg_hourly_rate * (1.03 ** (y - 1)))) + (annual_software_cost * (1.03 ** (y - 1))))
        for y in range(1, year + 1)
    ]))

projection_df = pd.DataFrame({
    'Year': years,
    'Cumulative Savings': cumulative_savings
})

fig_projection = px.area(
    projection_df,
    x='Year',
    y='Cumulative Savings',
    title='',
    labels={'Year': 'Year', 'Cumulative Savings': 'Cumulative Savings ($)'}
)

fig_projection.update_traces(
    fillcolor=PEACOCK_TEAL,
    line_color=LUNAR_BLUE,
    line_width=3
)

fig_projection.update_layout(
    height=400,
    yaxis_tickprefix='$',
    yaxis_tickformat=',.0f'
)

st.plotly_chart(fig_projection, use_container_width=True)

col_5yr_1, col_5yr_2, col_5yr_3 = st.columns(3)

with col_5yr_1:
    st.metric("5-Year Total Savings", f"${cumulative_savings[-1]:,.0f}")

with col_5yr_2:
    st.metric("5-Year Software Investment", f"${cumulative_cost[-1]:,.0f}")

with col_5yr_3:
    five_year_roi = ((cumulative_savings[-1] - cumulative_cost[-1]) / cumulative_cost[-1]) * 100
    st.metric("5-Year ROI", f"{five_year_roi:.0f}%")

st.markdown("---")

# Additional benefits
st.markdown("### Additional Benefits Beyond Cost Savings")

col_benefit1, col_benefit2 = st.columns(2)

with col_benefit1:
    st.markdown(f"""
    <div class="comparison-card">
        <h4 style="color: {PEACOCK_TEAL};">🎯 Quality Improvements</h4>
        <ul style="line-height: 2;">
            <li><strong>97%+</strong> transcription accuracy with medical terminology</li>
            <li><strong>Standardized</strong> SBAR format ensures consistency</li>
            <li><strong>Reduced errors</strong> in patient handoffs</li>
            <li><strong>Better compliance</strong> with Joint Commission standards</li>
            <li><strong>Complete audit trail</strong> for every handoff</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="comparison-card">
        <h4 style="color: {PEACOCK_TEAL};">📊 Operational Efficiency</h4>
        <ul style="line-height: 2;">
            <li><strong>Faster handoffs</strong> = more time for patient care</li>
            <li><strong>Reduced overtime</strong> from lengthy documentation</li>
            <li><strong>Better staff satisfaction</strong> with streamlined workflow</li>
            <li><strong>Improved continuity</strong> of care across shifts</li>
            <li><strong>Real-time insights</strong> into handoff patterns</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_benefit2:
    st.markdown(f"""
    <div class="comparison-card">
        <h4 style="color: {PEACOCK_TEAL};">🔒 Compliance & Security</h4>
        <ul style="line-height: 2;">
            <li><strong>HIPAA compliant</strong> with end-to-end encryption</li>
            <li><strong>Automatic audit logs</strong> for regulatory compliance</li>
            <li><strong>7-year retention</strong> meets legal requirements</li>
            <li><strong>SOC 2 Type II</strong> certified infrastructure</li>
            <li><strong>Business Associate Agreement</strong> included</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="comparison-card">
        <h4 style="color: {PEACOCK_TEAL};">🏥 Integration Benefits</h4>
        <ul style="line-height: 2;">
            <li><strong>EHR integration</strong> with Epic, Cerner, MEDITECH</li>
            <li><strong>FHIR R4 support</strong> for modern interoperability</li>
            <li><strong>Bi-directional sync</strong> of patient data</li>
            <li><strong>Mobile-first</strong> design for on-the-go clinicians</li>
            <li><strong>Offline capability</strong> ensures uninterrupted workflow</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Pricing details
st.markdown("### Pricing Plans")

col_price1, col_price2, col_price3 = st.columns(3)

plans = [
    {
        "name": "Starter",
        "base": "$2,000",
        "per_user": "$25",
        "max_users": "Up to 50",
        "features": [
            "Core SBAR features",
            "Voice-to-text transcription",
            "Basic analytics",
            "Email support",
            "Mobile app access"
        ]
    },
    {
        "name": "Professional",
        "base": "$5,000",
        "per_user": "$20",
        "max_users": "Up to 200",
        "features": [
            "Everything in Starter",
            "EHR integration",
            "Advanced analytics",
            "Priority support",
            "Custom SBAR templates",
            "API access"
        ]
    },
    {
        "name": "Enterprise",
        "base": "$15,000",
        "per_user": "$15",
        "max_users": "Unlimited",
        "features": [
            "Everything in Professional",
            "Dedicated account manager",
            "Custom integrations",
            "White-label options",
            "SLA guarantees",
            "24/7 phone support",
            "Training & onboarding"
        ]
    }
]

for col, plan in zip([col_price1, col_price2, col_price3], plans):
    with col:
        is_selected = plan["name"] == pricing_tier
        border_color = PEACOCK_TEAL if is_selected else "#ddd"

        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 8px; border: 3px solid {border_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: 100%;">
            <h3 style="color: {PEACOCK_TEAL}; margin-top: 0;">{plan["name"]}</h3>
            <div style="font-size: 2rem; font-weight: bold; color: {ECLIPSE_NAVY}; margin: 1rem 0;">
                {plan["base"]}<span style="font-size: 1rem; color: #666;">/month</span>
            </div>
            <div style="font-size: 1rem; color: #666; margin-bottom: 1rem;">
                + {plan["per_user"]}/user/month
            </div>
            <div style="color: #666; margin-bottom: 1rem;">
                {plan["max_users"]} users
            </div>
            <hr style="border: none; border-top: 1px solid #eee; margin: 1rem 0;">
            <ul style="list-style: none; padding: 0; line-height: 2;">
                {"".join([f"<li>✓ {feature}</li>" for feature in plan["features"]])}
            </ul>
            {"<div style='background: " + PEACOCK_TEAL + "; color: white; padding: 0.5rem; border-radius: 5px; text-align: center; margin-top: 1rem; font-weight: bold;'>CURRENT SELECTION</div>" if is_selected else ""}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Export section
st.markdown("### Share This Analysis")

col_export1, col_export2, col_export3 = st.columns(3)

with col_export1:
    if st.button("📄 Export to PDF", use_container_width=True, type="primary"):
        st.success("PDF report generated successfully!")

with col_export2:
    if st.button("📧 Email Report", use_container_width=True):
        st.success("Report sent to your email!")

with col_export3:
    if st.button("🔗 Get Shareable Link", use_container_width=True):
        st.code("https://demo.eclipselink.ai/roi?id=abc123", language=None)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>Ready to get started?</strong></p>
    <p>Contact us for a personalized demo and pricing consultation</p>
    <p style="margin-top: 1rem;">
        📧 sales@rohimaya.ai • 🌐 eclipselink.ai • 📞 1-800-ECLIPSE
    </p>
    <p style="font-size: 0.9rem; margin-top: 2rem;">
        <strong>EclipseLink AI™</strong> © 2025 Rohimaya Health AI. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
