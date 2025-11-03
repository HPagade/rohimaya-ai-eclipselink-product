# ECLIPSELINK AI - QUICK REFERENCE CHEAT SHEET
**For ClaudeCode Developer Reference**

---

## 🎯 PROJECT ESSENTIALS

**Deadline:** Friday, October 31, 2025  
**Goal:** Working MVP demo for investors  
**Innovation:** Update-Only Model™ (80% time savings)  
**Budget:** ~$100/month

---

## 🎨 BRANDING

```css
/* Colors */
--peacock-teal: #1a9b8e
--phoenix-gold: #f4c430
--lunar-blue: #2c3e50

/* Assets */
rohimaya-logo-circle.png (40×40px in nav)
rohimaya-banner.png (full-width hero)

/* Typography */
Font: Inter, -apple-system, sans-serif
Headers: 700 weight, lunar-blue
Body: 400 weight, dark-gray
```

---

## 🏗️ TECH STACK

```yaml
Backend:
  - Python 3.11+
  - FastAPI 0.104+
  - Uvicorn (ASGI server)
  - PostgreSQL 15+
  - Supabase (auth + storage)

Frontend:
  - React 18+
  - TypeScript 5+
  - Vite (build tool)
  - Tailwind CSS 3+
  - React Router v6
  - Axios (HTTP client)

AI:
  - OpenAI Whisper API (transcription)
  - Anthropic Claude Sonnet 4 (SBAR generation)

Deployment:
  - Docker + Docker Compose
  - Railway.app (hosting)
```

---

## 📊 DATABASE QUICK REFERENCE

### Core Tables

**users**
```sql
id, email, password_hash, first_name, last_name, 
role [RN|LPN|CNA|MD|PT|etc.], facility_id, 
is_active, email_verified, created_at
```

**patients**
```sql
id, mrn, first_name, last_name, date_of_birth,
room_number, admission_date, primary_nurse_id,
facility_id, created_at
```

**handoffs**
```sql
id, patient_id, created_by_user_id, 
handoff_type, is_baseline, baseline_handoff_id,
audio_url, transcript,
sbar_situation, sbar_background, sbar_assessment, sbar_recommendation,
completeness_score, status, created_at
```

**handoff_changes**
```sql
id, handoff_id, field_name, old_value, new_value,
change_type [improvement|decline|stable|new],
severity [critical|warning|info]
```

**rewards_points**
```sql
id, user_id, points_earned, activity_type,
related_handoff_id, description, created_at
```

**audit_logs**
```sql
id, user_id, action, resource_type, resource_id,
ip_address, details, created_at
```

---

## 🔐 SECURITY CHECKLIST

```
✅ NIST 2025 Password Policy:
   - Length: 12-16 characters
   - Complexity: Mix of upper, lower, number, special
   - No common passwords (check against list)
   - Annual rotation reminders

✅ Authentication:
   - JWT with 60-minute expiration
   - HTTP-only cookies
   - CSRF protection
   - Rate limiting (5 attempts, 15-min lockout)

✅ Authorization:
   - Role-based access control (RBAC)
   - Check permissions on every API route
   - Row-level security in database

✅ Data Protection:
   - Input validation (sanitize all inputs)
   - SQL injection prevention (parameterized queries)
   - XSS prevention (escape HTML)
   - CORS properly configured

✅ HIPAA Compliance:
   - Audit log EVERYTHING
   - Encrypt data at rest (database)
   - Encrypt data in transit (HTTPS)
   - 15-minute auto-logout
   - 7+ year data retention
```

---

## 🎤 VOICE RECORDING FLOW

```javascript
1. Request Mic Access
   navigator.mediaDevices.getUserMedia({ audio: true })

2. Create MediaRecorder
   recorder = new MediaRecorder(stream)

3. Capture Audio Chunks
   recorder.ondataavailable = (e) => chunks.push(e.data)

4. Stop & Create Blob
   blob = new Blob(chunks, { type: 'audio/webm' })

5. Upload to Supabase
   storage.upload(`handoffs/${uuid}.webm`, blob)

6. Get Public URL
   url = storage.getPublicUrl(path)

7. Send to Backend
   POST /api/handoffs/process-audio
   { audioUrl, patientId, isBaseline }
```

---

## 🤖 AI INTEGRATION FLOW

```python
1. DOWNLOAD AUDIO
   audio_bytes = requests.get(audio_url).content

2. TRANSCRIBE WITH WHISPER
   response = openai.Audio.transcribe(
       model="whisper-1",
       file=audio_bytes
   )
   transcript = response.text

3. GENERATE SBAR WITH CLAUDE
   context = get_patient_context(patient_id)
   
   if is_baseline:
       prompt = f"Generate complete SBAR from: {transcript}"
   else:
       baseline = get_baseline_sbar(patient_id)
       prompt = f"""
       Baseline SBAR: {baseline}
       Update transcript: {transcript}
       Extract only what changed and generate updated SBAR.
       """
   
   response = anthropic.messages.create(
       model="claude-sonnet-4",
       messages=[{"role": "user", "content": prompt}]
   )
   sbar = response.content

4. DETECT CHANGES (if update)
   changes = extract_changes(baseline, sbar)
   
5. CALCULATE SCORES
   completeness = calculate_completeness(sbar)
   clarity = calculate_clarity(sbar)

6. AWARD POINTS
   points = calculate_points(handoff)
   award_points(user_id, points, activity_types)

7. RETURN TO FRONTEND
   return {
       "sbar": sbar,
       "changes": changes,
       "scores": {"completeness": X, "clarity": Y},
       "points_earned": Z
   }
```

---

## 🏆 REWARDS POINT SYSTEM

```python
POINTS = {
    'handoff_completed': 10,
    'handoff_on_time': 15,      # Within 30 min of shift end
    'update_only_used': 25,     # Used update-only feature
    'high_quality': 20,         # Completeness >90%
    'zero_omissions': 15,       # All required fields
    'critical_alert': 50,       # Detected critical issue
    'peer_ack': 10,             # Receiving RN acknowledged
    'patient_education': 20,    # Documented teaching
    'family_update': 15,        # Shared with family
    'cross_discipline': 25      # Collaborated across roles
}

TIERS = {
    'bronze': (0, 500),
    'silver': (501, 2000),
    'gold': (2001, 5000),
    'platinum': (5001, float('inf'))
}
```

---

## 🎯 UPDATE-ONLY MODEL™ LOGIC

```python
def process_handoff(audio_url, patient_id, user_id):
    """Main handoff processing logic"""
    
    # 1. Check for baseline
    baseline = db.handoffs.find_one({
        'patient_id': patient_id,
        'is_baseline': True
    })
    
    is_baseline = (baseline is None)
    
    # 2. Transcribe audio
    transcript = whisper_transcribe(audio_url)
    
    # 3. Generate SBAR
    if is_baseline:
        # Full SBAR
        sbar = claude_generate_sbar(transcript, patient_context)
        changes = []
    else:
        # Update-only SBAR
        sbar = claude_generate_update_sbar(
            transcript, 
            baseline.sbar,
            patient_context
        )
        changes = extract_changes(baseline.sbar, sbar)
    
    # 4. Calculate quality scores
    scores = calculate_quality_scores(sbar)
    
    # 5. Detect critical alerts
    alerts = detect_critical_alerts(sbar, changes)
    
    # 6. Save to database
    handoff = db.handoffs.insert({
        'patient_id': patient_id,
        'created_by_user_id': user_id,
        'is_baseline': is_baseline,
        'baseline_handoff_id': baseline.id if baseline else None,
        'audio_url': audio_url,
        'transcript': transcript,
        'sbar_situation': sbar['situation'],
        'sbar_background': sbar['background'],
        'sbar_assessment': sbar['assessment'],
        'sbar_recommendation': sbar['recommendation'],
        'completeness_score': scores['completeness'],
        'clarity_score': scores['clarity']
    })
    
    # 7. Save changes
    for change in changes:
        db.handoff_changes.insert({
            'handoff_id': handoff.id,
            'field_name': change['field'],
            'old_value': change['old'],
            'new_value': change['new'],
            'change_type': change['type'],
            'severity': change['severity']
        })
    
    # 8. Award points
    points = calculate_points(handoff, changes, scores)
    award_points(user_id, points)
    
    # 9. Send notifications
    if alerts:
        send_critical_alerts(alerts, patient_id)
    
    return {
        'handoff': handoff,
        'changes': changes,
        'points_earned': points,
        'alerts': alerts
    }
```

---

## 🔍 CHANGE DETECTION LOGIC

```python
def extract_changes(baseline_sbar, update_sbar):
    """Compare baseline to update and identify changes"""
    
    changes = []
    
    # Define trackable fields
    TRACKABLE_FIELDS = [
        'pain_level',
        'vital_signs',
        'medications',
        'oxygen_status',
        'mobility',
        'mental_status',
        'diet',
        'elimination',
        'wound_care',
        'labs'
    ]
    
    for field in TRACKABLE_FIELDS:
        baseline_value = extract_field(baseline_sbar, field)
        update_value = extract_field(update_sbar, field)
        
        if baseline_value != update_value:
            change_type = determine_change_type(
                field, 
                baseline_value, 
                update_value
            )
            
            severity = determine_severity(
                field,
                baseline_value,
                update_value,
                change_type
            )
            
            changes.append({
                'field': field,
                'old': baseline_value,
                'new': update_value,
                'type': change_type,  # improvement|decline|stable|new
                'severity': severity  # critical|warning|info
            })
    
    return changes
```

---

## 🎨 UI COMPONENT PATTERNS

### Large Touch-Friendly Button
```tsx
<button className="
  w-40 h-40 rounded-full
  bg-gradient-to-br from-peacock-teal to-phoenix-gold
  text-white text-xl font-bold
  shadow-lg hover:shadow-2xl
  active:scale-95 transition-all
  flex items-center justify-center
">
  {isRecording ? '🔴 STOP' : '⚪ START'}
</button>
```

### Change Indicator
```tsx
{change.type === 'improvement' && (
  <span className="text-green-600">⬆️ IMPROVED</span>
)}
{change.type === 'decline' && (
  <span className="text-red-600">⬇️ DECLINED</span>
)}
{change.type === 'stable' && (
  <span className="text-blue-600">🔄 CHANGED</span>
)}
```

### SBAR Section
```tsx
<div className="sbar-section">
  <h3 className="text-xl font-semibold text-lunar-blue mb-2">
    📝 SITUATION
  </h3>
  <div className="bg-light-gray p-4 rounded-lg">
    {sbar.situation}
  </div>
</div>
```

### Progress Bar
```tsx
<div className="w-full bg-gray-200 rounded-full h-4">
  <div 
    className="bg-gradient-to-r from-peacock-teal to-phoenix-gold h-4 rounded-full transition-all"
    style={{ width: `${progress}%` }}
  />
</div>
<p className="text-sm text-gray-600 mt-1">
  {pointsToNext} points to next tier
</p>
```

---

## 📡 API RESPONSE PATTERNS

### Success Response
```json
{
  "success": true,
  "data": {
    "handoff": {...},
    "changes": [...],
    "points_earned": 85
  },
  "message": "Handoff created successfully"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Patient not found",
    "details": {
      "field": "patient_id",
      "value": "invalid-id"
    }
  }
}
```

### Streaming Response (SBAR Generation)
```python
async def stream_sbar():
    async for chunk in anthropic.messages.stream(...):
        yield f"data: {json.dumps(chunk)}\n\n"
```

---

## 🧪 TESTING CHECKLIST

```
AUTHENTICATION:
☐ Register with valid credentials
☐ Register with weak password (should fail)
☐ Register with duplicate email (should fail)
☐ Login with correct credentials
☐ Login with wrong password (should fail, count attempts)
☐ Login after 5 failed attempts (should be locked)
☐ Email verification flow
☐ Password reset flow

VOICE RECORDING:
☐ Request mic access
☐ Record 30 seconds
☐ Pause/resume
☐ Stop recording
☐ Upload to storage
☐ Verify file in Supabase bucket

AI PROCESSING:
☐ Transcription accuracy (medical terms)
☐ SBAR generation quality
☐ Baseline detection
☐ Change extraction
☐ Critical alert detection

PERMISSIONS:
☐ RN can create handoff for assigned patient
☐ RN cannot delete other's handoff
☐ Charge nurse can view all unit handoffs
☐ MD can view all patients
☐ CNA can create but not delete

REWARDS:
☐ Points awarded after handoff
☐ Correct point calculation
☐ Tier updates
☐ Leaderboard accuracy

AUDIT LOGGING:
☐ All actions logged
☐ Searchable by user/date/resource
☐ Export to CSV works

DEPLOYMENT:
☐ docker-compose up starts all services
☐ Database migrations run
☐ Sample data loads
☐ Environment variables work
☐ HTTPS configured (production)
```

---

## 🚨 COMMON ERRORS & FIXES

### "CORS Error"
```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Connection Refused (Database)"
```bash
# Check PostgreSQL is running
docker-compose ps

# Check DATABASE_URL in .env
echo $DATABASE_URL
```

### "Audio Upload Fails"
```python
# Check Supabase storage bucket exists
# Check bucket is public or has proper RLS policies
# Check SUPABASE_KEY in .env
```

### "AI API Rate Limit"
```python
# Add retry logic with exponential backoff
import time

def call_with_retry(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if i == max_retries - 1:
                raise
            time.sleep(2 ** i)  # 1s, 2s, 4s
```

---

## 📦 DOCKER QUICK COMMANDS

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Rebuild after code changes
docker-compose up -d --build

# Stop all services
docker-compose down

# Reset everything (caution: deletes data)
docker-compose down -v

# Run database migrations
docker-compose exec backend alembic upgrade head

# Access database
docker-compose exec db psql -U postgres eclipselink
```

---

## 📚 HELPFUL RESOURCES

```
FastAPI Docs: https://fastapi.tiangolo.com/
React Docs: https://react.dev/
Supabase Docs: https://supabase.com/docs
Whisper API: https://platform.openai.com/docs/guides/speech-to-text
Claude API: https://docs.anthropic.com/claude/reference
Tailwind CSS: https://tailwindcss.com/docs
Docker Compose: https://docs.docker.com/compose/
```

---

## 💡 PRO TIPS

1. **Use Environment Variables**: Never hardcode API keys
2. **Log Everything**: Helps debug issues fast
3. **Handle Errors Gracefully**: Show helpful messages to users
4. **Test As You Build**: Don't wait until the end
5. **Commit Often**: Small, focused commits with clear messages
6. **Document Decisions**: Future you will thank present you
7. **Ask Questions**: Better to clarify than assume
8. **Keep It Simple**: MVP means minimum viable, not perfect
9. **User Experience Matters**: Even simple UI should be pleasant
10. **Have Fun**: You're building something innovative! 🚀

---

**Quick access during development - bookmark this!** 🔖
