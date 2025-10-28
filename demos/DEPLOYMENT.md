# EclipseLink AI Demos - Deployment Guide

Complete guide for deploying the interactive demo suite to Streamlit Cloud.

## 📋 Prerequisites

- [x] GitHub account
- [x] Streamlit Cloud account (sign up free at [share.streamlit.io](https://share.streamlit.io))
- [x] Git repository with the demos

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

1. **Ensure all files are committed:**
```bash
cd /path/to/rohimaya-ai-eclipselink-product
git status
```

2. **If there are uncommitted changes:**
```bash
git add demos/
git commit -m "feat: add interactive Streamlit demo suite"
git push origin main
```

3. **Verify the demos directory structure:**
```bash
demos/
├── Home.py                    # ✅ Required - Entry point
├── 1_Voice_to_SBAR.py        # ✅ Demo page
├── 2_Clinical_Dashboard.py   # ✅ Demo page
├── 3_ROI_Calculator.py       # ✅ Demo page
├── requirements.txt          # ✅ Required - Dependencies
└── .streamlit/
    └── config.toml           # ✅ Optional - Theme config
```

### Step 2: Deploy to Streamlit Cloud

#### Option A: Deploy via Web Interface

1. **Go to Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App:**
   - Click "New app" button
   - Select your repository: `HPagade/rohimaya-ai-eclipselink-product`
   - Select branch: `main` (or your preferred branch)
   - Set main file path: `demos/Home.py`
   - Click "Deploy"

3. **Wait for Deployment:**
   - Streamlit will install dependencies (1-2 minutes)
   - Your app will be live once deployment completes
   - Default URL: `https://[auto-generated-name].streamlit.app`

#### Option B: Deploy via Streamlit CLI (Advanced)

```bash
# Install Streamlit CLI
pip install streamlit

# Login to Streamlit Cloud
streamlit cloud login

# Deploy the app
streamlit cloud deploy demos/Home.py
```

### Step 3: Configure Your App

1. **Access App Settings:**
   - Go to your app dashboard
   - Click on the app name
   - Navigate to "Settings"

2. **Set Custom URL (Optional):**
   - Go to "General" → "Custom subdomain"
   - Set subdomain: `eclipselink-demo`
   - Your app will be at: `https://eclipselink-demo.streamlit.app`

3. **Configure Secrets (if needed):**
   - Go to "Secrets" section
   - Add any environment variables (not needed for these demos)

### Step 4: Test Your Deployment

1. **Visit your app URL:**
   - Click "Open app" from the Streamlit Cloud dashboard
   - Or visit your custom URL

2. **Test all pages:**
   - ✅ Home page loads correctly
   - ✅ Navigate to Voice-to-SBAR demo
   - ✅ Navigate to Clinical Dashboard
   - ✅ Navigate to ROI Calculator
   - ✅ Check all interactive features

3. **Test on mobile:**
   - Open URL on mobile device
   - Verify responsive design works

## 🎯 Post-Deployment

### Share Your Demo

Your demos are now live! Share these URLs:

- **Main Demo Suite:** `https://[your-app].streamlit.app`
- **Direct Links:**
  - Voice-to-SBAR: `https://[your-app].streamlit.app/1_Voice_to_SBAR`
  - Dashboard: `https://[your-app].streamlit.app/2_Clinical_Dashboard`
  - ROI Calculator: `https://[your-app].streamlit.app/3_ROI_Calculator`

### Embed in Website

```html
<!-- Embed in iframe -->
<iframe
  src="https://[your-app].streamlit.app/?embedded=true"
  width="100%"
  height="800px"
  frameborder="0">
</iframe>
```

## 🔧 Advanced Configuration

### Custom Domain (Streamlit for Teams)

For a fully custom domain like `demo.eclipselink.ai`:

1. **Upgrade to Streamlit for Teams**
   - Required for custom domains
   - Contact Streamlit sales

2. **Configure DNS:**
   - Add CNAME record pointing to Streamlit's servers
   - Follow Streamlit's custom domain setup guide

3. **Update in Streamlit Cloud:**
   - Add custom domain in app settings
   - Wait for SSL certificate provisioning (automatic)

### Password Protection (Streamlit for Teams)

```python
# Add to Home.py
import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    # Show the app content
    st.title("EclipseLink AI Demos")
    # ... rest of your app
```

Then add to Streamlit secrets:
```toml
# .streamlit/secrets.toml
password = "your-secure-password"
```

### Analytics Integration

Add Google Analytics or other tracking:

```python
# Add to Home.py
import streamlit.components.v1 as components

# Google Analytics
components.html("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", height=0)
```

## 🔄 Updating Your Deployment

### Automatic Updates

Streamlit Cloud automatically redeploys when you push to your repository:

```bash
# Make changes to demos
vim demos/Home.py

# Commit and push
git add demos/
git commit -m "Update demo content"
git push origin main

# Streamlit Cloud will auto-redeploy
```

### Manual Reboot

If you need to manually restart:
1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Click "⋮" menu → "Reboot app"

## 🐛 Troubleshooting

### Deployment Fails

**Problem:** Deployment fails during dependency installation

**Solution:**
```bash
# Test locally first
cd demos
pip install -r requirements.txt
streamlit run Home.py

# If it works locally, check requirements.txt versions
# Pin specific versions:
streamlit==1.31.0
pandas==2.1.4
plotly==5.18.0
```

### App is Slow

**Problem:** App loads slowly or times out

**Solutions:**
1. Check data generation functions (add `@st.cache_data`)
2. Reduce sample data size
3. Optimize chart rendering
4. Enable Streamlit's caching

```python
# Add caching to expensive operations
@st.cache_data
def generate_handoff_data():
    # ... your data generation code
    return df
```

### Pages Not Showing

**Problem:** Multipage navigation doesn't work

**Solution:**
- Ensure `Home.py` exists (required for multipage apps)
- Page files must be in same directory as `Home.py`
- Page files must start with a number (e.g., `1_`, `2_`, `3_`)

### Styling Issues

**Problem:** Custom CSS not rendering correctly

**Solutions:**
1. Check `.streamlit/config.toml` is being read
2. Clear browser cache
3. Verify CSS syntax in `st.markdown()` calls
4. Use `unsafe_allow_html=True` flag

## 📊 Monitoring

### View App Analytics

Streamlit Cloud provides basic analytics:
1. Go to app dashboard
2. Click "Analytics"
3. View:
   - Total visitors
   - Active users
   - Page views
   - Session duration

### Check Logs

View real-time logs:
1. Go to app dashboard
2. Click "︙" → "Logs"
3. Monitor for errors or warnings

## 🔒 Security Best Practices

### For Demo Deployment

- ✅ No real patient data
- ✅ Simulated scenarios only
- ✅ No API keys needed
- ✅ Public access safe

### For Production Use

If adapting for production:
- 🔐 Add authentication
- 🔐 Use Streamlit secrets for API keys
- 🔐 Implement HIPAA compliance
- 🔐 Enable audit logging
- 🔐 Restrict access with password

## 💰 Cost Considerations

### Streamlit Cloud Free Tier

- ✅ **1 private app** (unlimited public apps)
- ✅ **1 GB RAM**
- ✅ **1 vCPU**
- ✅ **Community support**
- ✅ **Perfect for demos**

### Streamlit for Teams (Paid)

If you need:
- Multiple private apps
- Custom domains
- Password protection
- Priority support
- Higher resource limits

Pricing: Contact Streamlit sales

## 📞 Support

### Streamlit Resources

- **Docs:** [docs.streamlit.io](https://docs.streamlit.io)
- **Forum:** [discuss.streamlit.io](https://discuss.streamlit.io)
- **Gallery:** [streamlit.io/gallery](https://streamlit.io/gallery)

### EclipseLink Support

- **Email:** support@rohimaya.ai
- **Website:** https://rohimaya.ai

## ✅ Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed successfully
- [ ] All pages working correctly
- [ ] Custom subdomain configured (optional)
- [ ] Mobile experience tested
- [ ] Demo URLs shared with team
- [ ] Analytics configured (optional)
- [ ] Documentation updated

## 🎉 Success!

Your EclipseLink AI demo suite is now live and ready to share with:
- 🏥 Healthcare prospects
- 💼 Investors
- 👥 Stakeholders
- 📱 Team members

---

© 2025 Rohimaya Health AI. All rights reserved.
