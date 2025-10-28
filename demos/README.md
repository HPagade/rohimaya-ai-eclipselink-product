# EclipseLink AI - Interactive Demo Suite

This directory contains interactive Streamlit demos showcasing the key features of EclipseLink AI™.

## 🎯 Demo Applications

### 1. **Voice-to-SBAR Demo** (`1_Voice_to_SBAR.py`)
Experience the core functionality of converting voice recordings to structured SBAR reports.

**Features:**
- Multiple clinical scenarios (Post-Surgery ICU, Emergency Admission, End of Shift)
- Real-time transcription simulation
- AI-powered SBAR generation
- Interactive editing interface
- EHR export preview

### 2. **Clinical Dashboard** (`2_Clinical_Dashboard.py`)
Explore the management interface for healthcare facilities.

**Features:**
- Real-time handoff tracking (list, card, and timeline views)
- Analytics and insights with interactive charts
- Team activity monitoring
- System alerts and notifications
- Department performance metrics

### 3. **ROI Calculator** (`3_ROI_Calculator.py`)
Calculate potential time savings and cost reduction for facilities.

**Features:**
- Customizable facility parameters
- Real-time cost calculations
- 5-year financial projections
- Pricing plan comparisons
- Detailed benefit breakdown

## 🚀 Quick Start

### Installation

1. **Navigate to the demos directory:**
```bash
cd demos
```

2. **Install dependencies (only 4 packages needed):**
```bash
pip install -r requirements.txt
```

Required packages:
- `streamlit` - Web framework
- `pandas` - Data manipulation
- `plotly` - Interactive charts
- `numpy` - Numerical operations

### Running Locally

**Run all demos (multipage app):**
```bash
streamlit run Home.py
```

The app will open in your browser at `http://localhost:8501`

**Run individual demos:**
```bash
streamlit run 1_Voice_to_SBAR.py
streamlit run 2_Clinical_Dashboard.py
streamlit run 3_ROI_Calculator.py
```

## 🌐 Deploying to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Deployment Steps

1. **Push to GitHub:**
```bash
git add demos/
git commit -m "Add Streamlit demo suite"
git push origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set the main file path: `demos/Home.py`
   - Click "Deploy"

3. **Configuration:**
   - The app will automatically detect `requirements.txt`
   - Streamlit Cloud will install all dependencies
   - Your app will be live at `https://[your-app-name].streamlit.app`

### Custom Domain (Optional)

Once deployed, you can set up a custom domain:
- Go to your app settings in Streamlit Cloud
- Navigate to "General" → "Custom subdomain"
- Set your preferred subdomain (e.g., `eclipselink-demo`)
- Your app will be available at `https://eclipselink-demo.streamlit.app`

For a fully custom domain (e.g., `demo.eclipselink.ai`):
- Upgrade to Streamlit Cloud for Teams
- Follow the custom domain setup instructions

## 📁 Directory Structure

```
demos/
├── Home.py                      # Main landing page (required for multipage apps)
├── 1_Voice_to_SBAR.py          # Voice-to-SBAR demo
├── 2_Clinical_Dashboard.py      # Clinical dashboard demo
├── 3_ROI_Calculator.py          # ROI calculator demo
├── requirements.txt             # Python dependencies (4 packages only)
├── README.md                    # This file
├── DEPLOYMENT.md                # Streamlit Cloud deployment guide
├── run_demos.sh                 # Quick start script (Unix)
├── run_demos.bat                # Quick start script (Windows)
└── .streamlit/
    └── config.toml             # Streamlit configuration
```

## 🎨 Customization

### Brand Colors

The demos use EclipseLink AI's brand colors:
- **Peacock Teal:** `#1a9b8e`
- **Phoenix Gold:** `#f4c430`
- **Lunar Blue:** `#2c3e50`
- **Eclipse Navy:** `#1a2332`
- **Moon White:** `#f8f9fa`
- **Accent Copper:** `#b87333`

### Updating Content

To customize the demos for your needs:

1. **Edit clinical scenarios** in `1_Voice_to_SBAR.py`:
   - Update the `transcripts` dictionary with your own scenarios
   - Modify `sbar_reports` dictionary with corresponding SBAR content

2. **Adjust ROI parameters** in `3_ROI_Calculator.py`:
   - Update default values in the sidebar inputs
   - Modify pricing tiers in the `pricing` dictionary
   - Customize benefit descriptions

3. **Change dashboard data** in `2_Clinical_Dashboard.py`:
   - Modify `generate_handoff_data()` function for different sample data
   - Update chart configurations and metrics

## 🔧 Configuration

### Streamlit Configuration

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#1a9b8e"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#1a2332"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

## 📊 Demo Features

### Voice-to-SBAR Demo
- ✅ Sample clinical scenarios
- ✅ Simulated processing stages
- ✅ Interactive transcript editing
- ✅ SBAR report generation
- ✅ PDF export simulation
- ✅ EHR integration preview

### Clinical Dashboard
- ✅ Sample handoff data (50 records)
- ✅ Multiple view modes (list, card, timeline)
- ✅ Interactive filters
- ✅ Real-time charts (Plotly)
- ✅ Analytics insights
- ✅ Team performance tracking

### ROI Calculator
- ✅ Customizable facility parameters
- ✅ Real-time calculations
- ✅ Interactive charts
- ✅ 5-year projections
- ✅ Pricing comparisons
- ✅ Export functionality

## 🎥 Screenshots

### Home Page
The landing page provides an overview of all demos and key features.

### Voice-to-SBAR Demo
Step-by-step workflow from voice recording to SBAR report generation.

### Clinical Dashboard
Real-time monitoring and analytics for clinical handoff management.

### ROI Calculator
Interactive calculator showing cost savings and time efficiency gains.

## 🔒 Security Notes

These demos are designed for **demonstration purposes only** and use:
- Simulated data (no real patient information)
- Mock processing (no actual API calls)
- Sample scenarios for illustration

For production deployment with real data:
- Implement proper authentication
- Add PHI protection measures
- Enable HIPAA-compliant logging
- Use secure API endpoints
- Implement proper data encryption

## 🐛 Troubleshooting

### Common Issues

**1. Import errors:**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt --upgrade
```

**2. Port already in use:**
```bash
# Run on a different port
streamlit run Home.py --server.port 8502
```

**3. Charts not displaying:**
```bash
# Reinstall plotly
pip uninstall plotly
pip install plotly==5.18.0
```

**4. Styling issues:**
- Clear browser cache
- Try a different browser
- Check if custom CSS is rendering correctly

## 📞 Support

For questions or issues with the demos:

- **Email:** support@rohimaya.ai
- **Website:** https://rohimaya.ai
- **Product:** EclipseLink AI™

## 📄 License

© 2025 Rohimaya Health AI. All rights reserved.

These demos are part of the proprietary EclipseLink AI™ product suite.

---

## 🎯 Demo URLs (After Deployment)

Once deployed, share these links:

- **Main Demo Suite:** `https://[your-app].streamlit.app`
- **Direct to Voice-to-SBAR:** `https://[your-app].streamlit.app/1_Voice_to_SBAR`
- **Direct to Dashboard:** `https://[your-app].streamlit.app/2_Clinical_Dashboard`
- **Direct to ROI Calculator:** `https://[your-app].streamlit.app/3_ROI_Calculator`

## 🚀 Next Steps

1. **Test locally** to ensure everything works
2. **Customize content** for your specific use case
3. **Deploy to Streamlit Cloud** for sharing
4. **Share the link** with prospects, investors, or stakeholders
5. **Gather feedback** and iterate on the demos

---

Made with ❤️ by Rohimaya Health AI

**EclipseLink AI™** - Transforming Clinical Handoffs with AI
