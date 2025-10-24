# EclipseLink AI™ - Streamlit Demo

🚀 **Live Demo Prototype** - Deployable in 5 minutes!

## What This Is

A fully functional Streamlit prototype of EclipseLink AI™ that demonstrates the core workflow:
- User authentication (demo mode)
- Dashboard with statistics
- Complete handoff creation flow
- Voice recording simulation
- AI-powered SBAR generation (simulated)
- SBAR viewing and editing

## Quick Deploy to Streamlit Cloud (5 Minutes!)

### Option 1: Deploy from GitHub (Recommended)

1. **Commit and push this demo folder** (if not already done)

2. **Go to [streamlit.io/cloud](https://streamlit.io/cloud)**

3. **Sign in** with GitHub

4. **Click "New app"**

5. **Configure:**
   - Repository: `HPagade/rohimaya-ai-eclipselink-product`
   - Branch: `claude/continue-work-011CUSVg26sb4UrzRb8S1NAr`
   - Main file path: `demo/app.py`

6. **Click "Deploy"** - That's it! You'll get a URL like:
   ```
   https://eclipselink-ai-demo.streamlit.app
   ```

7. **Share the URL** with anyone you want to demo to!

### Option 2: Run Locally

```bash
# From the repository root
cd demo

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Features in This Demo

✅ **Authentication**
- Demo mode (no real auth needed)
- Just click "Try Demo" or enter any credentials

✅ **Dashboard**
- Real-time statistics
- Recent handoffs list
- Status indicators
- Priority badges

✅ **Create Handoff Workflow**
- 3-step process
- Patient information form
- Voice recording simulation
- Text input alternative (for demo)
- Automatic SBAR generation

✅ **SBAR Reports**
- AI-generated (simulated) SBAR
- All 4 sections: Situation, Background, Assessment, Recommendation
- Quality scores
- Inline editing
- Save functionality

✅ **Data Persistence**
- SQLite database (auto-created)
- Sample data included
- Edits are saved

## Demo Credentials

**No credentials needed!** Just click "Try Demo" button.

Or enter any email/password - all credentials work in demo mode.

## Customization

### Add Real Azure OpenAI Integration

If you want real AI generation instead of simulated:

1. Edit `demo/pages/create_handoff.py`

2. Add at the top:
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="your-key",
    api_version="2024-02-15-preview",
    azure_endpoint="your-endpoint"
)
```

3. Replace the `generate_sample_sbar()` function with real API calls

### Change Theme Colors

Edit `demo/.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#your-color"
```

## File Structure

```
demo/
├── app.py                  # Main application
├── pages/
│   ├── __init__.py
│   ├── create_handoff.py  # Create handoff page
│   └── view_handoff.py    # View handoff page
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Sharing with Stakeholders

Once deployed to Streamlit Cloud, you'll get a public URL that you can share with:
- Investors
- Potential customers
- Healthcare administrators
- Board members
- Team members

**No installation required** - they just click the link and start using it!

## Limitations (Demo Mode)

- Voice recording is simulated (no actual audio processing)
- SBAR generation uses templates (not real Azure OpenAI)
- No real authentication (anyone can access)
- SQLite database (resets on redeploy)
- No file storage (audio files not saved)

## Production vs Demo

| Feature | Demo | Full Product |
|---------|------|--------------|
| UI/UX | ✅ Same | ✅ Same |
| Workflow | ✅ Same | ✅ Same |
| Voice Recording | 🔶 Simulated | ✅ Real audio |
| AI Generation | 🔶 Template | ✅ Azure OpenAI |
| Authentication | 🔶 Demo mode | ✅ JWT + RBAC |
| Database | 🔶 SQLite | ✅ PostgreSQL |
| Deployment | ✅ Streamlit | ✅ Railway/Vercel |

## Troubleshooting

**App won't start:**
```bash
# Make sure you're in the demo folder
cd demo

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Database errors:**
```bash
# Delete and recreate
rm demo_data.db
streamlit run app.py
```

**Deployment fails:**
- Check that `requirements.txt` has correct package versions
- Ensure `config.toml` is in `.streamlit/` folder
- Verify `pages/__init__.py` exists

## Next Steps

After demoing, you can:

1. **Get feedback** from stakeholders
2. **Deploy the full product** (see main SETUP.md)
3. **Add real Azure OpenAI integration**
4. **Customize branding** and colors
5. **Add more features** as needed

## Support

Questions? Contact: admin@rohimaya.com

---

**EclipseLink AI™** - Rohimaya Health AI
© 2025 All Rights Reserved

Built with ❤️ by Hannah Kraulik Pagade (CEO) & Prasad Pagade (CTO)
