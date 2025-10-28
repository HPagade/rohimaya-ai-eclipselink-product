# EclipseLink AI™ - Streamlit Demos

Interactive demos showcasing the voice-enabled clinical handoff platform with AI-powered SBAR generation.

## 🚀 Quick Start

### Deploy to Streamlit Cloud

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

1. **Fork this repository** to your GitHub account
2. **Sign in** to [Streamlit Cloud](https://share.streamlit.io)
3. **Create new app** and select this repository
4. **Set main file path** to `demos/Home.py`
5. **Deploy!**

### Run Locally

```bash
# Navigate to demos directory
cd demos

# Install dependencies
pip install -r requirements.txt

# Run the demo
streamlit run Home.py
```

The demo will open in your browser at `http://localhost:8501`

## 📁 Demo Structure

```
demos/
├── Home.py                          # Main landing page
├── pages/
│   ├── 1_Voice_Recording.py         # Voice-to-text demo
│   ├── 2_SBAR_Generation.py         # AI SBAR generation demo
│   └── 3_Analytics_Dashboard.py     # Analytics and insights
├── .streamlit/
│   └── config.toml                  # Streamlit configuration
├── requirements.txt                 # Python dependencies
├── packages.txt                     # System packages (for cloud deployment)
└── README.md                        # This file
```

## 🎯 Demo Features

### 🏠 Home Page
- Product overview
- Key features showcase
- Technology stack information
- Quick navigation to all demos

### 🎙️ Voice Recording Demo
- Simulated voice recording interface
- Azure Whisper transcription demo
- Real-time transcript display
- Metadata and quality metrics

### 🤖 SBAR Generation Demo
- AI-powered SBAR report generation
- GPT-4 clinical note processing
- Quality assessment metrics
- Version control showcase

### 📊 Analytics Dashboard
- Comprehensive KPI metrics
- Interactive charts and graphs
- Provider performance tracking
- Patient safety metrics
- System performance monitoring

## 🛠️ Technology Stack

**Frontend Framework:**
- Streamlit 1.31.0
- Plotly for interactive charts
- Pandas for data processing

**Simulated Backend:**
- Azure OpenAI GPT-4 (demo mode)
- Azure Whisper (demo mode)
- PostgreSQL concepts
- Redis/BullMQ concepts

**Deployment:**
- Streamlit Cloud
- Docker support
- GitHub Actions ready

## 🔧 Configuration

### Streamlit Cloud Deployment

The demos are pre-configured for Streamlit Cloud deployment with:

- **Theme**: Custom healthcare-themed dark mode
- **Port**: 8501 (default)
- **CORS**: Disabled for security
- **XSRF Protection**: Enabled

### Environment Variables (Optional)

For production deployment with real backend:

```bash
# .env file (not required for demos)
API_BASE_URL=https://your-api-url.com
AZURE_OPENAI_ENDPOINT=https://your-azure-openai.com
AZURE_OPENAI_KEY=your-key-here
```

## 📦 Dependencies

### Python Packages (`requirements.txt`)
- streamlit==1.31.0 - Web framework
- pandas==2.2.0 - Data processing
- plotly==5.18.0 - Interactive charts
- requests==2.31.0 - HTTP client
- python-dotenv==1.0.0 - Environment variables

### System Packages (`packages.txt`)
- libportaudio2 - Audio processing
- libsndfile1 - Sound file support
- ffmpeg - Media handling

## 🎨 Customization

### Theme Colors

Edit `.streamlit/config.toml` to customize colors:

```toml
[theme]
primaryColor = "#0ea5e9"        # Primary blue
backgroundColor = "#0f172a"      # Dark background
secondaryBackgroundColor = "#1e293b"  # Secondary dark
textColor = "#f1f5f9"           # Light text
```

### Adding New Demo Pages

1. Create new file in `pages/` directory
2. Name it with number prefix: `4_New_Demo.py`
3. Add navigation link in `Home.py`
4. Update this README

## 🚨 Important Notes

### Demo Mode
These demos are **simulated** and do NOT connect to real backend services:
- ✅ Voice recording is simulated (no actual audio processing)
- ✅ SBAR generation shows pre-written examples
- ✅ Analytics data is randomly generated
- ✅ No real patient data is used

### For Production
To connect to real EclipseLink AI backend:
1. Set environment variables for API endpoints
2. Implement API client in `utils/api_client.py`
3. Replace simulated data with real API calls
4. Add authentication and authorization
5. Implement proper error handling

## 📚 Documentation

For more information about EclipseLink AI:

- [Main README](../README.md) - Project overview
- [Developer Guide](../README-DEVELOPERS.md) - Development setup
- [User Guide](../README-USERS.md) - End-user documentation
- [Architecture](../eclipse-ai-part1-architecture.md) - System architecture

## 🤝 Contributing

Contributions welcome! To add or improve demos:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-demo`)
3. Make your changes
4. Test locally (`streamlit run Home.py`)
5. Commit changes (`git commit -m 'Add new demo'`)
6. Push to branch (`git push origin feature/new-demo`)
7. Create Pull Request

## 📄 License

Proprietary - Rohimaya Health AI
© 2024 All rights reserved.

## 🆘 Support

For issues or questions:
- 📧 Email: support@rohimaya.com
- 🐛 Issues: [GitHub Issues](https://github.com/HPagade/rohimaya-ai-eclipselink-product/issues)
- 📖 Docs: [Documentation](../README.md)

## 🎉 Quick Deploy Checklist

- [ ] Fork repository to your GitHub
- [ ] Sign in to Streamlit Cloud
- [ ] Create new app
- [ ] Select repository and branch
- [ ] Set main file: `demos/Home.py`
- [ ] Click "Deploy"
- [ ] Share your demo URL!

---

Built with ❤️ for healthcare professionals using Streamlit and Azure AI
