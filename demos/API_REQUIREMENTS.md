# API Requirements for EclipseLink AI Demos

## 🎯 Current Demo Status: NO APIs Required

The current Streamlit demos are **fully functional without any API connections**. They use:
- ✅ Hardcoded sample data
- ✅ Simulated processing
- ✅ Client-side calculations
- ✅ Mock workflows

**You can deploy these demos TODAY with ZERO API setup!**

---

## 🔮 Future: Connecting Real Services

When you're ready to move beyond demos and connect real services, here's what you'll need:

### 1. Azure OpenAI API (For Voice & SBAR Generation)

**What it's for:**
- Real voice-to-text transcription (Whisper)
- Real SBAR report generation (GPT-4)

**Required Credentials:**
```python
AZURE_OPENAI_API_KEY = "your-api-key-here"
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com"
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4-32k"
AZURE_OPENAI_WHISPER_DEPLOYMENT = "whisper"
```

**How to Add:**
1. Get Azure OpenAI access (requires application approval)
2. Create a resource in Azure Portal
3. Deploy Whisper and GPT-4 models
4. Add credentials to Streamlit Secrets

**Add to Streamlit Cloud:**
```toml
# In Streamlit Cloud → App Settings → Secrets
[azure]
openai_api_key = "sk-..."
openai_endpoint = "https://..."
openai_deployment = "gpt-4-32k"
whisper_deployment = "whisper"
```

**Cost:** ~$0.002 per transcription + $0.06 per SBAR generation = ~$0.062 per handoff

---

### 2. Supabase Database (For Real Data Storage)

**What it's for:**
- Store real handoff records
- Patient information (HIPAA-compliant)
- User authentication
- Audit logs

**Required Credentials:**
```python
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key-here"
SUPABASE_SERVICE_ROLE_KEY = "your-service-role-key"
```

**How to Add:**
1. Sign up at https://supabase.com (free tier available)
2. Create a new project
3. Run database migrations from `/database` folder
4. Get API credentials from project settings

**Add to Streamlit Cloud:**
```toml
# In Streamlit Cloud → App Settings → Secrets
[supabase]
url = "https://xxxxx.supabase.co"
anon_key = "eyJ..."
service_role_key = "eyJ..."
```

**Cost:** Free tier (500MB database, 50,000 monthly active users)

---

### 3. Cloudflare R2 (For Audio File Storage)

**What it's for:**
- Store voice recording files
- Secure, S3-compatible storage
- HIPAA-compliant

**Required Credentials:**
```python
R2_ACCOUNT_ID = "your-account-id"
R2_ACCESS_KEY_ID = "your-access-key"
R2_SECRET_ACCESS_KEY = "your-secret-key"
R2_BUCKET_NAME = "eclipselink-recordings"
```

**How to Add:**
1. Sign up for Cloudflare R2
2. Create a bucket
3. Generate API tokens
4. Configure CORS for uploads

**Add to Streamlit Cloud:**
```toml
# In Streamlit Cloud → App Settings → Secrets
[r2]
account_id = "xxx"
access_key_id = "xxx"
secret_access_key = "xxx"
bucket_name = "eclipselink-recordings"
```

**Cost:** $0.015/GB/month + $0.36/million Class B operations

---

### 4. Upstash Redis (For Job Queue & Caching)

**What it's for:**
- Background job processing
- Rate limiting
- Session caching

**Required Credentials:**
```python
UPSTASH_REDIS_URL = "https://xxx.upstash.io"
UPSTASH_REDIS_TOKEN = "your-token-here"
```

**How to Add:**
1. Sign up at https://upstash.com
2. Create a Redis database
3. Get connection credentials

**Add to Streamlit Cloud:**
```toml
# In Streamlit Cloud → App Settings → Secrets
[redis]
url = "https://xxx.upstash.io"
token = "AXX..."
```

**Cost:** Free tier (10,000 commands/day)

---

## 🔄 Migration Path: Demo → Production

### Phase 1: Current State (DONE ✅)
- Streamlit demos with simulated data
- No API connections needed
- Perfect for sales demos and investor presentations
- **Status:** Ready to deploy NOW

### Phase 2: Backend Integration (Optional)
If you want to connect the Streamlit demos to your backend:

**Option A: Direct API Connection**
```python
# Add to demos/utils/api_client.py
import requests

def transcribe_audio(audio_file):
    """Call your backend API for transcription"""
    response = requests.post(
        "https://api.eclipselink.ai/v1/voice/upload",
        files={"audio": audio_file},
        headers={"Authorization": f"Bearer {st.secrets['api']['token']}"}
    )
    return response.json()
```

**Option B: Keep Demos Separate**
- Demos stay as-is (simulated data)
- Build separate production app with real APIs
- Use demos for marketing, production app for real users

**Recommended:** Option B - Keep demos simple and fast

### Phase 3: Full Production App (Future)
Build a complete production app with:
- Full API integration
- Real user authentication
- HIPAA compliance
- Database storage
- Audit logging
- EHR integration

**Note:** This would be a separate codebase, not the demos

---

## 🎯 Recommended Approach

### For NOW (Next 1-3 months):
**Deploy the demos as-is**
- ✅ No API setup needed
- ✅ Fast deployment (5 minutes)
- ✅ Zero ongoing costs
- ✅ Perfect for sales and investor demos
- ✅ Get feedback from users

**URL:** https://eclipselink-demo.streamlit.app

**Use for:**
- 🏥 Healthcare prospect demos
- 💼 Investor pitch presentations
- 👥 Stakeholder reviews
- 📱 Team collaboration
- 🎯 Marketing website embeds

### For LATER (3-6 months):
**Build production app**
- Connect real APIs
- Implement authentication
- Add HIPAA compliance
- Deploy on secure infrastructure
- Use feedback from demos to guide features

**URL:** https://app.eclipselink.ai

**Use for:**
- 🏥 Real healthcare facilities
- 👨‍⚕️ Real clinical staff
- 📊 Real patient data
- 🔐 HIPAA-compliant workflows

---

## 📊 Cost Comparison

### Current Demos (Simulated):
```
Streamlit Cloud:    $0/month
APIs:               $0/month
Database:           $0/month
Storage:            $0/month
─────────────────────────────
TOTAL:              $0/month
```

### Future Production (Real APIs):
```
Streamlit Cloud:    $0/month (or $42/user for Teams)
Azure OpenAI:       ~$200/month (1000 handoffs)
Supabase:           $0/month (free tier) or $25/month (Pro)
Cloudflare R2:      ~$5/month
Upstash Redis:      $0/month (free tier) or $10/month
─────────────────────────────
TOTAL:              ~$210/month (1000 handoffs)
                    or ~$0.21 per handoff
```

### Alternative Backend:
If you deploy your Express.js backend (already built in `/apps/backend`):
```
Railway/Render:     ~$20/month (backend hosting)
Azure OpenAI:       ~$200/month (1000 handoffs)
Supabase:           $25/month (Pro tier)
Cloudflare R2:      ~$5/month
Upstash Redis:      $10/month
─────────────────────────────
TOTAL:              ~$260/month
```

---

## 🔧 Example: Adding Real APIs to Demos

If you decide to connect real APIs later, here's an example:

### Before (Current - Simulated):
```python
# In 1_Voice_to_SBAR.py
def transcribe_audio(audio_file):
    """Simulate transcription"""
    time.sleep(2)  # Simulate processing
    return predefined_transcript  # Return hardcoded text
```

### After (Real API):
```python
# In 1_Voice_to_SBAR.py
import openai
from azure.identity import DefaultAzureCredential

def transcribe_audio(audio_file):
    """Real transcription with Azure OpenAI"""
    openai.api_key = st.secrets["azure"]["openai_api_key"]
    openai.api_base = st.secrets["azure"]["openai_endpoint"]
    openai.api_type = "azure"

    result = openai.Audio.transcribe(
        model=st.secrets["azure"]["whisper_deployment"],
        file=audio_file
    )
    return result["text"]
```

### Secrets Configuration:
```toml
# In Streamlit Cloud → App Settings → Secrets
[azure]
openai_api_key = "your-key"
openai_endpoint = "https://your-resource.openai.azure.com"
whisper_deployment = "whisper"
```

---

## ✅ Current Status Summary

### What You Have NOW:
- ✅ 3 fully functional Streamlit demos
- ✅ Professional EclipseLink branding
- ✅ Simulated clinical workflows
- ✅ Sample data and scenarios
- ✅ Interactive features
- ✅ Ready to deploy in 5 minutes
- ✅ $0 cost to run

### What You DON'T Need NOW:
- ❌ Azure OpenAI API
- ❌ Supabase database
- ❌ Cloudflare R2 storage
- ❌ Redis cache
- ❌ Any API keys or secrets
- ❌ Any backend deployment

### What You MIGHT Want LATER:
- 🔮 Connect real Azure OpenAI for live transcription
- 🔮 Add authentication for private demos
- 🔮 Store demo usage analytics
- 🔮 Connect to your backend API
- 🔮 Build full production app

---

## 🚀 Next Steps

### Right NOW:
1. **Deploy the demos** (5 minutes)
   - Go to https://share.streamlit.io
   - Connect GitHub repo
   - Deploy `demos/Home.py`
   - Done!

2. **Share with stakeholders**
   - Send demo URL to prospects
   - Embed in website
   - Use for pitch decks
   - Gather feedback

3. **Iterate based on feedback**
   - Update scenarios
   - Refine calculations
   - Improve UI/UX
   - Add more features

### In 1-3 Months:
1. **Evaluate feedback**
   - What features do users want?
   - What's missing?
   - What needs improvement?

2. **Decide on APIs**
   - Do you need real transcription?
   - Do you need data storage?
   - Do you need authentication?

3. **Plan production app**
   - Use existing backend (`/apps/backend`)
   - Or build new Streamlit app with APIs
   - Implement HIPAA compliance
   - Deploy securely

---

## 📞 Questions?

**Q: Can I use these demos for sales?**
A: Yes! They're perfect for sales demos, investor pitches, and stakeholder presentations.

**Q: Are they HIPAA compliant?**
A: The demos use simulated data only, so HIPAA doesn't apply. For production with real patient data, you'll need additional security measures.

**Q: Can I customize the scenarios?**
A: Absolutely! Edit the transcript and SBAR dictionaries in `1_Voice_to_SBAR.py`.

**Q: When should I add real APIs?**
A: Only when you have real users who need real transcription. For demos and sales, simulated data works perfectly.

**Q: How much will APIs cost?**
A: See "Cost Comparison" section above. Roughly $0.21 per handoff with Azure OpenAI.

---

## 📚 Resources

### For Demo Deployment:
- Streamlit Cloud: https://share.streamlit.io
- Documentation: See `DEPLOYMENT.md` and `DEPLOYMENT_CHECKLIST.md`

### For API Setup (Later):
- Azure OpenAI: https://azure.microsoft.com/en-us/products/ai-services/openai-service
- Supabase: https://supabase.com
- Cloudflare R2: https://www.cloudflare.com/products/r2/
- Upstash: https://upstash.com

### Support:
- Email: support@rohimaya.ai
- Product: EclipseLink AI™
- Company: Rohimaya Health AI

---

© 2025 Rohimaya Health AI. All rights reserved.
