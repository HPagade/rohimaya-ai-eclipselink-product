# ECLIPSELINK AI & PHOENIX & PEACOCK HONORS™
## MVP Development Brief for ClaudeCode
**Rohimaya Health AI, LLC**  
**Target Delivery: Friday, October 31, 2025**

---

## 📋 TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Company Background & Branding](#company-background--branding)
3. [Product Overview](#product-overview)
4. [Answers to Your 8 Questions](#answers-to-your-8-questions)
5. [Technical Stack Decisions](#technical-stack-decisions)
6. [MVP Feature Breakdown](#mvp-feature-breakdown)
7. [UI/UX Mockups & Placeholders](#uiux-mockups--placeholders)
8. [Educational Requirements](#educational-requirements)
9. [Development Approach](#development-approach)
10. [Success Criteria](#success-criteria)
11. [ClaudeCode Prompt](#claudecode-prompt)

---

## 1. EXECUTIVE SUMMARY

**What We're Building:**  
EclipseLink AI - the world's first AI-powered clinical handoff system using the revolutionary "Update-Only Model™" that reduces handoff time by 80% (from 8-12 minutes to 1.5 minutes). Integrated with Phoenix & Peacock Honors™ rewards program to drive adoption and quality.

**Timeline:** Working prototype by Friday, October 31, 2025

**Purpose:** 
- Launch my health-tech startup (Rohimaya Health AI)
- Learning milestone for my dual Master's in AI/ML and Computer Science
- Real product for investor demos and hospital pilots
- Professional portfolio piece for Customer Success/Partnership roles

**Key Innovation:** The Update-Only Model™
- **Initial handoff** = Complete baseline SBAR (3-5 min voice recording)
- **All subsequent handoffs** = Record ONLY what changed (30-45 seconds)
- **AI automatically** compares to baseline and generates complete updated SBAR
- **Result:** 80% time savings while improving quality and safety

---

## 2. COMPANY BACKGROUND & BRANDING

### Company Story
**Rohimaya Health AI** was founded by Hannah (CEO, RN with 15+ years experience) and Prasad Pagade (CTO). The name represents our blended Southern American and Maharashtrian Indian heritage:

- **Rohi** = Phoenix 🔥 (Prasad's spirit animal) - Rebirth, transformation, rising from ashes
- **Maya** = Peacock 🦚 (Hannah's spirit animal) - Protection, vision, grace, healing
- **-ya** = Moon 🌙 (from Hindi Rohini constellation) - Guidance through darkness

**Brand Meaning:** *Rebirth • Protection • Guidance*

### Visual Brand Identity

**Logo Files Available:**
- `rohimaya-logo-circle.png` - Circular peacock design logo
- `rohimaya-banner.png` - Full banner with peacock, mission statement

**Color Palette:**

**Phoenix Colors (Fire/Energy):**
```
🔥 Burning Orange: #ff6b35
🔶 Golden Flame: #f7931e  
✨ Bright Gold: #f4c430 (Primary Brand Gold)
```

**Peacock Colors (Grace/Healing):**
```
💙 Deep Teal: #1a9b8e (Primary Brand Teal)
🦚 Iridescent Blue: #6f42c1
💚 Emerald: #20c997
```

**Foundation:**
```
🌙 Lunar Blue: #2c3e50 (Primary Dark)
⚪ Clean White: #ffffff
🌫️ Light Gray: #f8f9fa
```

**Design Principles:**
- Gradients blending phoenix fire → peacock feathers
- Iridescent shimmer effects on interactive elements
- Radial glows suggesting flames and peacock eye-spots
- Professional yet warm - clinical but not cold

### Product Ecosystem (7 Products)
1. **EclipseLink AI** (MVP Focus) - Clinical handoffs
2. **PlumeDose AI** - Medication management
3. **RiseGuard AI** - Falls prevention
4. **LunarBridge AI** - Clinical trials matching
5. **FeatherSight AI** - Lab intelligence
6. **PhoenixBreath AI** - Respiratory care
7. **WingStrength AI** - PT/OT therapy

**All unified by:** Phoenix & Peacock Honors™ rewards program

---

## 3. PRODUCT OVERVIEW

### EclipseLink AI - Core Features

**15 Integrated Elements:**
1. Voice-to-text transcription (Whisper API)
2. AI-powered SBAR generation (GPT-4)
3. Update-Only Model™ (baseline + changes)
4. Critical alert detection
5. Real-time translator (50+ languages)
6. AI chatbot assistant
7. Family portal (plain-language updates)
8. EHR integration (Epic, Cerner, MEDITECH)
9. 15 profession-specific dashboards
10. Integration with 6 other Rohimaya products
11. Phoenix & Peacock Honors™ rewards
12. HIPAA-compliant audit logging
13. Multi-device support (mobile, tablet, desktop)
14. Offline mode with sync
15. Advanced analytics & reporting

### Target Users (15 Clinical Roles)

**Nursing:**
- Registered Nurses (RN)
- Licensed Practical/Vocational Nurses (LPN/LVN)
- Certified Nursing Assistants (CNA)
- Nurse Practitioners (NP)

**Allied Health:**
- Physical Therapists (PT)
- Occupational Therapists (OT)
- Respiratory Therapists (RT)
- Speech-Language Pathologists (SLP)
- Social Workers (SW)
- Case Managers
- Dietitians/Nutritionists
- Pharmacists

**Medical:**
- Physicians (MD/DO)
- Physician Assistants (PA)
- Medical Assistants (MA)

**Market Size:** 10.6+ million healthcare professionals in the US

### The Revolutionary Update-Only Model™

**Traditional Handoff Problem:**
Every shift, clinicians repeat 90% of the same information:
- "Mr. Smith is 65yo M, admitted 3 days ago for CHF..."
- Wastes 8-12 minutes per handoff
- Listener must mentally identify what changed
- Critical updates get buried in repeated information

**Our Solution:**

```
INITIAL ADMISSION (Day 1, 7 AM):
├─ RN records comprehensive baseline (3-5 min)
├─ AI generates complete SBAR with all patient context
└─ Becomes "source of truth" for entire admission

SHIFT UPDATE (Day 1, 7 PM):
├─ RN records ONLY what changed (30-45 sec)
│   "Overnight patient weaned to room air, O2 sats 
│    holding at 96%. Temperature down to 99.1. WBC 
│    trending down to 11.8. PT consult ordered."
├─ AI compares to baseline
├─ AI extracts new information
├─ AI generates complete updated SBAR
└─ Highlights changes in yellow

RESULT:
✅ Complete patient picture maintained
✅ 80% time reduction (10 min → 2 min)
✅ Changes automatically highlighted
✅ No information lost
✅ Safer, faster, better
```

---

## 4. ANSWERS TO YOUR 8 QUESTIONS

### Q1: Initial vs Update Detection
**ANSWER: Option A (Automatic) with Override**

**How it works:**
```
When clinician starts new handoff:
├─ System checks: "Does patient have baseline handoff?"
│   ├─ NO → "Create Initial Handoff" mode
│   │         (Full SBAR with complete patient context)
│   └─ YES → "Update Existing Patient" mode
│             (Show previous SBAR, record only changes)
│
└─ Override button visible:
    "Switch to Initial Handoff" (if transfer from another facility)
    "Switch to Update Mode" (if patient previously admitted)
```

**Why automatic:**
- Reduces cognitive load (one less decision)
- Prevents errors (forgetting to select correct mode)
- Smart default behavior

**Why override:**
- Patient may transfer from another facility (need new baseline)
- Clinician may want to create fresh baseline if previous one incomplete
- Gives user control when needed

**MVP Implementation:**
- Database field: `is_baseline` (boolean)
- Each handoff links to: `baseline_handoff_id` (if update)
- Simple check: `SELECT COUNT(*) WHERE patient_id = ? AND is_baseline = true`

---

### Q2: Update Workflow Details
**ANSWER: Option C (Version History) - Like Git Commits**

**How it works:**

**Clinician View:**
```
┌─────────────────────────────────────────────┐
│ Patient: John Doe (MRN: 12345)             │
│ Current Status: Day 3 Post-Op              │
├─────────────────────────────────────────────┤
│ 📝 MOST RECENT SBAR (7:00 PM, Oct 28)     │
│                                             │
│ S: Post-op day 3, pain well-controlled     │
│ B: 65yo M s/p cholecystectomy, HTN, DM2   │
│ A: Vitals stable, ambulating with PT...    │
│ R: Continue PCA, advance diet as tolerated │
│                                             │
│ 🔄 Changes from baseline:                  │
│ • Pain: 8/10 → 4/10 ✅ IMPROVED            │
│ • Ambulation: Bedbound → Walking 50ft ✅    │
│ • Diet: NPO → Clear liquids ✅             │
├─────────────────────────────────────────────┤
│ 📚 Version History (Click to expand)       │
│ ▶ Oct 28, 7:00 PM - RN Martinez (Update)  │
│ ▶ Oct 28, 7:00 AM - RN Johnson (Update)   │
│ ▶ Oct 27, 7:00 PM - RN Williams (Update)  │
│ ▶ Oct 26, 2:00 PM - RN Smith (Baseline)   │
└─────────────────────────────────────────────┘
```

**Behind the Scenes:**
```javascript
// Database structure
handoffs: {
  id: "uuid-123",
  patient_id: "patient-456",
  is_baseline: false,
  baseline_handoff_id: "baseline-abc",
  created_at: "2025-10-28T19:00:00Z",
  created_by: "user-789",
  handoff_type: "shift_update",
  
  // Current complete SBAR (merged)
  sbar_situation: "Post-op day 3, pain well-controlled",
  sbar_background: "65yo M s/p cholecystectomy...",
  sbar_assessment: "Vitals stable, ambulating...",
  sbar_recommendation: "Continue PCA, advance diet...",
  
  // What changed in THIS update
  changes_from_previous: [
    {
      field: "pain_level",
      old_value: "8/10",
      new_value: "4/10",
      change_type: "improvement"
    },
    {
      field: "ambulation",
      old_value: "bedbound",
      new_value: "walking 50ft with PT",
      change_type: "improvement"
    }
  ]
}
```

**Benefits:**
- ✅ Clinician always sees most current complete SBAR
- ✅ Changes highlighted automatically
- ✅ Full audit trail preserved (Joint Commission requirement)
- ✅ Can "rewind" to any previous state
- ✅ AI learns from edit patterns
- ✅ Quality improvement data (trending analysis)

**MVP Implementation:**
- Display: Most recent merged SBAR
- Collapsed section: "View History" (shows all previous versions)
- Yellow highlights on changed sections
- Simple version comparison view

---

### Q3: Role-Specific SBAR Customization
**ANSWER: Option C (Same Structure, Role Emphasis)**

**Rationale:**
SBAR is a universal healthcare communication standard. Changing the structure for different roles would:
- ❌ Break interoperability (RN can't understand PT handoff)
- ❌ Confuse teams (everyone expects S-B-A-R format)
- ❌ Violate Joint Commission standards

**Better Solution: AI Emphasizes Role-Relevant Information**

**Example: Same Patient, Different Role Views**

**Registered Nurse Focus:**
```
S: 65yo M, post-op day 3 cholecystectomy
B: PMH: HTN, DM2, obesity (BMI 38)
A: Vitals stable. Pain 4/10 on PCA morphine.
   IV site patent. Breath sounds clear. BS+.
   Voiding adequate. Ambulated 50ft with PT.
R: Continue PCA, monitor pain control q4h.
   Advance diet as tolerated. D/C Foley today.
```

**Physical Therapist Focus:**
```
S: 65yo M, post-op day 3 cholecystectomy
B: PMH: HTN, DM2, obesity (BMI 38)
   🎯 MOBILITY: Previously independent, no assistive device
A: Vitals stable. Pain 4/10 (controlled).
   🎯 AMBULATION: Walked 50ft hallway with CGA
   🎯 BALANCE: Steady, no dizziness
   🎯 ENDURANCE: Minimal SOB, no chest pain
   🎯 FUNCTIONAL STATUS: Requires assist for ADLs
R: 🎯 Continue ambulation BID, increase distance daily
   🎯 Goal: Independent ambulation before discharge
   🎯 D/C planning: Recommend home PT 2x/week
```

**Respiratory Therapist Focus:**
```
S: 65yo M, post-op day 3 cholecystectomy
B: PMH: HTN, DM2, obesity (BMI 38)
   🎯 RESP HX: Former smoker (quit 5 yrs ago), no COPD
A: 🎯 O2 STATUS: Room air, SpO2 96%
   🎯 BREATH SOUNDS: Clear bilaterally
   🎯 RESPIRATORY EFFORT: Unlabored, RR 16
   🎯 INCENTIVE SPIROMETRY: Using q2h, volume improving
   🎯 COUGH: Productive, clear sputum
R: 🎯 Continue IS q2h while awake
   🎯 Encourage deep breathing with ambulation
   🎯 Monitor for atelectasis
```

**How AI Does This:**
```python
# AI prompt includes role context
system_prompt = f"""
You are generating an SBAR handoff report for a {user.role}.

Standard SBAR format required, but emphasize information 
relevant to {user.role}:

{role_emphasis_rules[user.role]}
"""

role_emphasis_rules = {
  "RN": "vitals, medications, IV access, pain, elimination",
  "PT": "mobility, balance, endurance, functional status, fall risk",
  "RT": "oxygen status, breath sounds, respiratory effort, ventilation",
  "Pharmacist": "medications, allergies, drug interactions, renal function",
  "Social Worker": "discharge planning, family support, resources, barriers"
}
```

**MVP Implementation:**
- Same SBAR structure for all roles
- AI prompt adapts based on user role
- 🎯 Emoji markers highlight role-specific info
- User can toggle "Show All Details" vs "Role-Focused View"

---

### Q4: Critical Alert Detection
**ANSWER: Option C (Keywords + AI + Configurable Notifications)**

**How It Works:**

**Layer 1: Keyword Triggers (Immediate)**
```javascript
CRITICAL_KEYWORDS = {
  // Cardiovascular
  "chest pain": "CRITICAL - Cardiac",
  "chest pressure": "CRITICAL - Cardiac",
  "heart attack": "CRITICAL - Cardiac",
  "MI": "CRITICAL - Cardiac",
  "stroke": "CRITICAL - Neuro",
  "CVA": "CRITICAL - Neuro",
  
  // Respiratory
  "can't breathe": "CRITICAL - Respiratory",
  "respiratory distress": "CRITICAL - Respiratory",
  "unresponsive": "CRITICAL - Code Blue",
  "not breathing": "CRITICAL - Code Blue",
  
  // Hemorrhage
  "bleeding": "WARNING - Assess severity",
  "hemorrhage": "CRITICAL - Bleeding",
  "blood pressure 70": "CRITICAL - Shock",
  
  // Neuro
  "seizure": "CRITICAL - Neuro",
  "altered mental status": "WARNING - Neuro",
  "pupils unequal": "CRITICAL - Neuro",
  
  // Pain
  "pain 10": "WARNING - Severe pain",
  "pain radiating": "WARNING - Assess cardiac",
  
  // Fall
  "fell": "WARNING - Fall",
  "found on floor": "CRITICAL - Fall with possible injury"
}
```

**Layer 2: AI Context Analysis**
```python
# AI evaluates severity based on full context
def analyze_critical_alert(transcript, patient_data):
    """
    Example: "Patient reports chest pain"
    
    AI considers:
    - Where: "chest pain radiating to left arm" → MORE severe
    - When: "chest pain started 2 hours ago" → MORE urgent
    - Trending: Pain was 2/10 yesterday, now 8/10 → ESCALATING
    - Patient history: Known cardiac disease → HIGHER risk
    - Vital signs: BP 180/110, HR 120 → CONCERNING
    - Response to treatment: Given nitro x3, no relief → FAILING THERAPY
    
    AI Assessment: 🚨 CRITICAL - Possible STEMI
    Confidence: 94%
    Recommended Actions:
    1. Stat EKG
    2. Cardiology consult
    3. Prepare for cath lab
    4. Notify attending MD immediately
    """
    
    context = {
        "transcript": transcript,
        "patient_age": patient_data.age,
        "patient_history": patient_data.medical_history,
        "current_vitals": patient_data.latest_vitals,
        "recent_trends": patient_data.trend_analysis,
        "medications": patient_data.current_meds
    }
    
    ai_response = anthropic.messages.create(
        model="claude-sonnet-4",
        messages=[{
            "role": "user",
            "content": f"""Analyze this clinical scenario for critical alerts:
            
            {json.dumps(context, indent=2)}
            
            Determine:
            1. Severity (CRITICAL / WARNING / INFO)
            2. Urgency (IMMEDIATE / URGENT / ROUTINE)
            3. Recommended actions
            4. Who should be notified
            5. Confidence level (0-100%)
            """
        }]
    )
    
    return ai_response
```

**Layer 3: Configurable Notification Rules**
```javascript
// Hospital configures who gets alerted for what
NOTIFICATION_RULES = {
  facility_id: "hospital-123",
  
  alerts: {
    "CRITICAL_CARDIAC": {
      notify: [
        { role: "bedside_rn", method: "app_push", delay: "0sec" },
        { role: "charge_nurse", method: "app_push", delay: "0sec" },
        { role: "rapid_response_team", method: "page", delay: "0sec" },
        { role: "attending_md", method: "page", delay: "30sec" },
        { role: "cardiology_on_call", method: "page", delay: "2min" }
      ],
      escalation: {
        if_not_acknowledged: "5min",
        escalate_to: ["nursing_supervisor", "chief_resident"]
      }
    },
    
    "WARNING_PAIN": {
      notify: [
        { role: "bedside_rn", method: "app_push", delay: "0sec" },
        { role: "charge_nurse", method: "app_notification", delay: "0sec" }
      ],
      escalation: {
        if_not_acknowledged: "15min",
        escalate_to: ["charge_nurse"]
      }
    },
    
    "INFO_ROUTINE": {
      notify: [
        { role: "bedside_rn", method: "app_notification", delay: "0sec" }
      ]
    }
  }
}
```

**User Experience:**

**Scenario: Critical Alert Detected**
```
┌─────────────────────────────────────────────────┐
│ 🚨 CRITICAL ALERT DETECTED                     │
├─────────────────────────────────────────────────┤
│                                                 │
│ Patient: John Doe (Room 302A)                  │
│ Alert: Possible Cardiac Event                  │
│ Confidence: 94%                                 │
│                                                 │
│ KEY FINDINGS:                                   │
│ • Chest pain radiating to left arm             │
│ • Diaphoresis present                          │
│ • BP: 180/110 (elevated)                       │
│ • HR: 120 (tachycardia)                        │
│ • Patient reports "squeezing sensation"        │
│ • No relief with nitroglycerin x3              │
│                                                 │
│ RECOMMENDED ACTIONS:                            │
│ ☐ Stat 12-lead EKG                             │
│ ☐ Cardiology consult                           │
│ ☐ Prepare for possible cath lab                │
│ ☐ Notify attending MD                          │
│                                                 │
│ NOTIFICATIONS SENT TO:                          │
│ ✓ Bedside RN (Sarah Johnson)                   │
│ ✓ Charge Nurse (Mike Chen)                     │
│ ✓ Rapid Response Team                          │
│ ✓ Dr. Smith (Attending) - Paged               │
│ ⏳ Cardiology On-Call - Will page in 2 min     │
│                                                 │
│ [ ACKNOWLEDGE ALERT ]  [ FALSE ALARM ]         │
└─────────────────────────────────────────────────┘
```

**MVP Implementation:**
- Predefined keyword list (50+ critical terms)
- AI context analysis for severity scoring
- Basic notification rules (RN + Charge Nurse + MD)
- Simple escalation (if not acknowledged in 5 min)
- Full configuration panel comes in Phase 2

---

### Q5: MVP Feature Priority
**ANSWER: APPROVED with Modifications**

**MUST-HAVE by Friday (Core MVP):**
✅ 1. Login/registration system
   - All 15 clinical roles supported
   - NIST 2025 password policy (12-16 chars, complexity)
   - Email verification
   - Password reset flow

✅ 2. Voice recording → AI pipeline (CRITICAL PATH)
   - Voice recording interface (tap to start/stop)
   - Audio upload to backend
   - Whisper transcription
   - GPT-4 SBAR generation
   - Display formatted SBAR

✅ 3. Initial vs Update handoff differentiation
   - Automatic detection (baseline check)
   - Override button for user control
   - "New Patient" vs "Update Existing" workflows

✅ 4. Patient management
   - Add new patient
   - Patient list view
   - Patient detail view
   - Search/filter patients

✅ 5. Handoff history & viewing
   - List all handoffs for a patient
   - View individual handoff (SBAR display)
   - Version history (collapsed by default)
   - Changes highlighted

✅ 6. Basic dashboard
   - Role-specific landing page
   - Recent handoffs list
   - Patients assigned to me
   - Quick stats (handoffs today, pending reviews)

✅ 7. Role-based permissions (HIPAA requirement)
   - RN: Create, edit own handoffs, view assigned patients
   - Charge Nurse: View all unit handoffs, reassign patients
   - MD: View all patients, create progress notes
   - CNA: Create updates, cannot delete
   - Admin: Full access, manage users

✅ 8. Admin panel (basic)
   - Add users manually
   - Assign roles
   - View system logs
   - Facility settings

✅ 9. Audit logging (HIPAA/Joint Commission)
   - Who accessed what, when
   - All CRUD operations logged
   - Searchable audit trail
   - Export to CSV

✅ 10. Docker deployment (demo-ready)
   - docker-compose.yml with all services
   - One-command setup
   - Sample data preloaded
   - README with deployment instructions

**NICE-TO-HAVE (If Time Permits - Friday Evening):**
⭐ 11. Basic rewards points display
   - Show points earned after each handoff
   - Total points on dashboard
   - Simple leaderboard (top 10)
   - No redemption catalog yet

⭐ 12. Critical alert detection (keywords only)
   - Basic keyword matching
   - Simple notification (in-app only)
   - No escalation yet

⭐ 13. UI mockups for future features
   - Family portal (static HTML mockup)
   - Translator (static UI showing concept)
   - EHR integration settings page (non-functional)
   - Advanced rewards catalog (visual only)

**PHASE 2 (Next Week):**
🔜 14. Full critical alert system (AI + escalation)
🔜 15. Real-time translator (API integration)
🔜 16. Family portal (functional with SMS invites)
🔜 17. EHR integration (Epic sandbox)
🔜 18. Full rewards system (redemption catalog)
🔜 19. Mobile app (React Native)
🔜 20. Offline mode with sync

**PRIORITY ORDER for Friday:**
```
Day 1: Authentication + Database + Patient Management
Day 2: Voice Recording + Whisper + GPT-4 Integration
Day 3: SBAR Generation + Update-Only Logic
Day 4: Dashboard + Handoff Viewing + Permissions
Day 5: Audit Logs + Docker Setup + Testing + Polish
```

---

### Q6: Rewards Program for MVP
**ANSWER: Option B (Basic Points Display) + Education**

**What We're Building Friday:**

**1. Points Tracking Backend**
```javascript
// Automatic points awarded after each action
POINTS_SYSTEM = {
  handoff_completed: 10,
  handoff_on_time: 15,        // Within 30 min of shift end
  update_only_used: 25,        // Used update-only feature
  high_quality_sbar: 20,       // Completeness score >90%
  critical_alert_caught: 50,   // Detected critical change
  zero_omissions: 15,          // All required fields completed
  peer_acknowledgment: 10,     // Receiving RN marks as helpful
  patient_education: 20,       // Documented patient teaching
  family_update: 15,           // Shared update with family
  cross_discipline: 25         // Collaborated across roles
}
```

**2. Points Display UI**
```
After completing handoff:
┌─────────────────────────────────────────────────┐
│ ✅ Handoff Submitted Successfully!             │
├─────────────────────────────────────────────────┤
│                                                 │
│ 🏆 YOU EARNED POINTS!                          │
│                                                 │
│ Handoff Completed.................... +10 pts  │
│ Submitted On Time.................... +15 pts  │
│ Used Update-Only Feature............. +25 pts  │
│ High Quality SBAR (95%).............. +20 pts  │
│                                                 │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│ TOTAL EARNED:........................ +70 pts  │
│                                                 │
│ Your new total: 847 points                     │
│ Next tier: 🥈 Silver Peacock (153 pts away)    │
│                                                 │
│ [ VIEW LEADERBOARD ]  [ CONTINUE ]             │
└─────────────────────────────────────────────────┘
```

**3. Dashboard Widget**
```
┌─────────────────────────────────────────────────┐
│ 🦚 YOUR PHOENIX & PEACOCK HONORS™              │
├─────────────────────────────────────────────────┤
│                                                 │
│ Sarah Johnson, RN                              │
│ 🥉 Bronze Peacock                              │
│                                                 │
│ Total Points: 847                              │
│ Rank: #23 out of 150 nurses                    │
│                                                 │
│ Progress to Silver:                            │
│ [████████████░░░░░░░░] 85%                     │
│ 153 points to go!                              │
│                                                 │
│ This Week:                                     │
│ • Handoffs completed: 12                       │
│ • Points earned: 347                           │
│ • Quality score: 94% ⭐                        │
│                                                 │
│ [ VIEW FULL PROFILE ]  [ LEADERBOARD ]         │
└─────────────────────────────────────────────────┘
```

**4. Simple Leaderboard**
```
┌─────────────────────────────────────────────────┐
│ 🏆 PHOENIX & PEACOCK HONORS™ LEADERBOARD       │
├─────────────────────────────────────────────────┤
│                                                 │
│ 🥇 1. Maria Garcia, RN........... 2,847 pts 💎  │
│ 🥈 2. James Wilson, RN........... 2,654 pts 💎  │
│ 🥉 3. Lisa Chen, RN.............. 2,341 pts 🥇  │
│    4. Ahmed Hassan, RN........... 1,923 pts 🥇  │
│    5. Jennifer Lee, RN........... 1,847 pts 🥇  │
│    ...                                          │
│    23. Sarah Johnson, RN......... 847 pts 🥉    │
│                                                 │
│ Filter: [All Roles ▼] [This Month ▼]          │
│                                                 │
│ Team Standings:                                │
│ 🥇 Medical-Surgical Unit......... 18,473 pts   │
│ 🥈 ICU........................... 16,892 pts   │
│ 🥉 Emergency Department.......... 15,234 pts   │
└─────────────────────────────────────────────────┘
```

**5. Rewards Catalog (Static UI Only)**
```
┌─────────────────────────────────────────────────┐
│ 🎁 REWARDS CATALOG                             │
├─────────────────────────────────────────────────┤
│                                                 │
│ 🥉 BRONZE TIER (100-500 points)                │
│                                                 │
│ ☕ Starbucks Gift Card ($10)........ 250 pts   │
│ 🎟️ Movie Tickets (2)............... 350 pts   │
│ 🍕 Pizza Party for Unit............. 500 pts   │
│                                                 │
│ 🥈 SILVER TIER (501-2,000 points)              │
│                                                 │
│ 👕 Premium Scrubs Set............... 750 pts   │
│ 🎵 Spotify Premium (3 months)...... 850 pts   │
│ 💆 Spa Day Gift Card............... 1,200 pts  │
│                                                 │
│ 🥇 GOLD TIER (2,001-5,000 points)              │
│                                                 │
│ 📱 AirPods Pro.................... 2,500 pts   │
│ 🏖️ Weekend Getaway................ 3,500 pts   │
│ 📚 Certification Exam Fee......... 4,000 pts   │
│                                                 │
│ 💎 PLATINUM TIER (5,001+ points)               │
│                                                 │
│ 💻 iPad Pro....................... 8,000 pts   │
│ ✈️ Vacation Package (7 days)..... 12,000 pts  │
│ 🎓 Tuition Reimbursement ($1K)... 15,000 pts  │
│                                                 │
│ ⚠️ COMING SOON: Redemption system             │
│    For demo purposes only - Phase 2            │
└─────────────────────────────────────────────────┘
```

**Educational Documentation for Rewards:**
```markdown
# PHOENIX & PEACOCK HONORS™ - HOW IT WORKS

## What Is It?
A universal rewards program that recognizes healthcare professionals
for quality work, not just productivity. Earn points for:
- Completing excellent handoffs
- Catching critical issues early
- Helping colleagues
- Patient education
- Family communication

## Why It Matters
Traditional healthcare has no reward system. You can work hard,
catch a life-threatening issue, and get...nothing. Phoenix & Peacock
Honors™ changes that by:

1. **Recognition:** Points = visible appreciation
2. **Motivation:** See progress toward rewards
3. **Gamification:** Friendly competition improves quality
4. **Retention:** Staff with rewards programs stay 30% longer
5. **Morale:** Tangible rewards for excellent work

## Tier System
🥉 Bronze Peacock: 0-500 pts (Starting tier)
🥈 Silver Peacock: 501-2,000 pts (Regular performer)
🥇 Gold Peacock: 2,001-5,000 pts (High performer)
💎 Platinum Peacock: 5,001+ pts (Excellence)
🔥 Phoenix Elite: 10,000+ pts (Leadership)

## How Points Are Calculated
AUTOMATIC - You don't do anything special!

Every time you:
- Complete a handoff: +10 pts (baseline)
- Submit on time: +15 pts (within 30 min of shift end)
- Use update-only feature: +25 pts (efficiency bonus)
- High quality (>90%): +20 pts (AI scores completeness)
- Zero omissions: +15 pts (all required fields)
- Critical alert detected: +50 pts (patient safety)

Example: Submit excellent handoff on time using update-only:
10 + 15 + 25 + 20 + 15 = 85 points

## Strategic Advantage
Once you've earned 5,000+ points across all Rohimaya products,
you're unlikely to switch to a competitor because you'd lose
all accumulated rewards. This creates customer stickiness.

## MVP vs. Full System
**Friday MVP:**
- Points tracking ✅
- Dashboard display ✅
- Leaderboard ✅
- Tier badges ✅
- Catalog (view only) ✅

**Phase 2 (Next Week):**
- Redemption system
- Admin approval workflow
- Physical rewards fulfillment
- Integration with HR systems
- Tax reporting (rewards may be taxable income)
```

---

### Q7: Family Portal for MVP
**ANSWER: Option C (UI Mockup Only) + Education**

**What We're Building Friday:**

**1. Static HTML Mockup**
```html
<!-- family-portal-mockup.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Family Portal - EclipseLink AI</title>
    <!-- Rohimaya branding -->
</head>
<body>
    <!-- Non-functional demo showing concept -->
    
    <header>
        <h1>👨‍👩‍👧 Patient Updates for John Doe</h1>
        <p>Last updated: Oct 28, 2025 at 7:45 PM</p>
    </header>
    
    <section class="latest-update">
        <h2>📝 Latest Update from Your Care Team</h2>
        <div class="update-card">
            <p class="timestamp">Evening Update - 7:00 PM</p>
            <p class="summary">
                John had a good day today! He was able to walk 
                in the hallway with help from the physical therapist. 
                His pain is much better and he's eating regular food 
                now. The doctor says he's healing well and might be 
                able to go home in 2-3 days.
            </p>
            <div class="key-points">
                <h3>Key Points:</h3>
                <ul>
                    <li>✅ Pain improved (now mild)</li>
                    <li>✅ Walking with assistance</li>
                    <li>✅ Eating regular meals</li>
                    <li>✅ No fever</li>
                    <li>📅 Expected discharge: Oct 30-31</li>
                </ul>
            </div>
        </div>
    </section>
    
    <section class="timeline">
        <h2>📅 Update Timeline</h2>
        <!-- Previous updates listed -->
    </section>
    
    <section class="care-team">
        <h2>👥 Your Care Team</h2>
        <div class="team-member">
            <p><strong>Today's Nurse:</strong> Sarah Johnson, RN</p>
            <p><strong>Doctor:</strong> Dr. Michael Smith</p>
        </div>
    </section>
    
    <section class="questions">
        <h2>❓ Have Questions?</h2>
        <p>Call the nurse station: (555) 123-4567</p>
        <button disabled>💬 Ask a Question (Coming Soon)</button>
    </section>
    
    <footer>
        <p>🔒 Secure Family Portal by EclipseLink AI</p>
        <p>⚠️ DEMO MODE - This is a preview of Phase 2 features</p>
    </footer>
</body>
</html>
```

**2. Educational Documentation**
```markdown
# FAMILY PORTAL - DESIGN RATIONALE

## The Problem
Families call nurse stations every 2-3 hours asking:
- "How is my mom doing?"
- "Did she eat today?"
- "When can she come home?"

This interrupts clinical workflow. A single 200-bed hospital
receives 600-800 family calls per day, consuming 15-20 hours
of nursing time daily.

## Our Solution
Plain-language automated updates sent to family members'
phones or email after each clinical handoff.

## How It Works (Phase 2)

### Step 1: Family Enrollment
When patient admitted:
├─ RN asks: "Would you like text updates?"
├─ Family provides: phone # or email
├─ System sends: verification code
└─ Family clicks: secure link to portal

### Step 2: Automated Translation
After each handoff:
├─ Clinician creates SBAR (medical language)
├─ AI translates to plain language
├─ Removes jargon ("SOB" → "shortness of breath")
├─ Focuses on family-relevant info
└─ Family receives text notification

### Step 3: Family Views Update
├─ Click secure link (no password needed)
├─ See plain-language summary
├─ View update timeline
├─ See expected discharge date
└─ Option to call if concerned

## Privacy & Security
✅ HIPAA-compliant secure links
✅ Family must verify phone/email
✅ Patient must consent to sharing
✅ Links expire after 7 days
✅ No PHI in text messages (just notification)
✅ Audit log of all family access

## Example Transformation

**Clinical SBAR:**
"S: POD3 s/p lap chole, A&O x3, tolerating clears
B: 65yoM PMH HTN, DM2, obesity (BMI 38)
A: VS stable, afebrile, pain 4/10 PCA, IS use adequate,
   amb 50ft w/ PT, BS+, voiding adequate
R: Advance diet as tolerated, wean PCA, PT eval for DC"

**Family Portal:**
"John had a good day today! This is his third day after
surgery. He's alert and comfortable, with mild pain that
is well-controlled. He walked 50 feet with the physical
therapist and is eating light meals. His vital signs are
good and he has no fever. The plan is to continue his
recovery, increase his activity, and prepare for going
home in the next 2-3 days."

## Benefits
**For Families:**
- ✅ Reduce anxiety (know what's happening)
- ✅ Fewer calls needed
- ✅ Understand medical updates
- ✅ Feel connected to care team

**For Clinicians:**
- ✅ 60% reduction in family phone calls
- ✅ More time for patient care
- ✅ Fewer interruptions
- ✅ Better family satisfaction scores

**For Hospitals:**
- ✅ Save 15-20 nursing hours/day
- ✅ Improve patient satisfaction (HCAHPS)
- ✅ Reduce complaints
- ✅ Competitive advantage

## MVP vs. Full Implementation
**Friday MVP:**
- Static HTML mockup ✅
- Demonstrates concept ✅
- Shows visual design ✅

**Phase 2 (Next Week):**
- Functional portal
- SMS/email notifications
- AI translation engine
- Access control
- Consent management
- Multi-language support (Spanish, Mandarin, etc.)
```

**Why Static for MVP:**
Family portal requires:
- SMS gateway integration ($)
- Email service integration
- Secure link generation
- Consent management system
- AI translation pipeline

These are complex and not core to proving the Update-Only Model™.
Better to show the concept visually and build functionality in Phase 2.

---

### Q8: UX Details
**ANSWERS:**

**A. Voice Recording Method: Tap-to-Start/Stop (Toggle)**

**Rationale:**
- ✅ Works with gloves (large button)
- ✅ Hands-free after start (can reference notes)
- ✅ Clear visual feedback (recording indicator)
- ✅ Easy to pause/resume
- ❌ Tap-and-hold is awkward for 2-3 minute recordings

**Implementation:**
```
┌─────────────────────────────────────────────────┐
│ 🎤 Record Handoff                              │
├─────────────────────────────────────────────────┤
│                                                 │
│ Patient: John Doe (Room 302A)                  │
│ Type: Update Existing Patient                  │
│                                                 │
│ ┌─────────────────────────────────────────┐    │
│ │                                         │    │
│ │        [Large Circular Button]          │    │
│ │                                         │    │
│ │         ⚪ TAP TO START                  │    │
│ │           RECORDING                      │    │
│ │                                         │    │
│ │  (Button size: 150px diameter, easy to  │    │
│ │   press with gloved hand or elbow)      │    │
│ │                                         │    │
│ └─────────────────────────────────────────┘    │
│                                                 │
│ 💡 TIP: Speak naturally. The AI will format   │
│    your recording into a professional SBAR.    │
│                                                 │
│ [ CANCEL ]                                     │
└─────────────────────────────────────────────────┘

WHILE RECORDING:
┌─────────────────────────────────────────────────┐
│ 🎤 Recording Handoff                           │
├─────────────────────────────────────────────────┤
│                                                 │
│ Patient: John Doe (Room 302A)                  │
│                                                 │
│ ┌─────────────────────────────────────────┐    │
│ │                                         │    │
│ │        [Large Circular Button]          │    │
│ │                                         │    │
│ │         🔴 TAP TO STOP                  │    │
│ │           RECORDING                      │    │
│ │                                         │    │
│ │         [Waveform Animation]            │    │
│ │         ▁▂▃▅▇▅▃▂▁                       │    │
│ │                                         │    │
│ │         ⏱️ 00:42                        │    │
│ │                                         │    │
│ └─────────────────────────────────────────┘    │
│                                                 │
│ 🔊 Volume: [▮▮▮▮▮▮▮▮▮░] Good                  │
│                                                 │
│ [ PAUSE ]  [ CANCEL ]                          │
└─────────────────────────────────────────────────┘
```

**B. SBAR Templates: YES (Optional)**

**Rationale:**
Common scenarios happen repeatedly. Templates save time and ensure
consistency for routine admissions.

**Templates to Include:**
1. **New Admission from ER**
2. **Post-Op Admission from PACU**
3. **Transfer from ICU to Floor**
4. **Shift Change (No Changes)**
5. **Discharge Planning**
6. **Palliative Care Transition**

**Implementation:**
```
┌─────────────────────────────────────────────────┐
│ 🎤 Start New Handoff                           │
├─────────────────────────────────────────────────┤
│                                                 │
│ Patient: [Select Patient ▼]                    │
│                                                 │
│ Handoff Type:                                  │
│ ⚪ Update Existing Patient (Recommended)        │
│ ⚪ New Patient Admission                        │
│                                                 │
│ Template (Optional):                           │
│ [ Select Template ▼ ]                          │
│   - None (Free Form)                           │
│   - New Admission from ER                      │
│   - Post-Op from PACU                          │
│   - Transfer from ICU                          │
│   - Shift Change (Stable)                      │
│   - Discharge Planning                         │
│   - Palliative Care                            │
│                                                 │
│ ℹ️ Templates provide prompts to guide your     │
│    recording. You can still speak freely!      │
│                                                 │
│ [ START RECORDING ]  [ CANCEL ]                │
└─────────────────────────────────────────────────┘

IF TEMPLATE SELECTED - DURING RECORDING:
┌─────────────────────────────────────────────────┐
│ 🎤 Recording: Post-Op from PACU                │
├─────────────────────────────────────────────────┤
│                                                 │
│ 📋 Template Prompts:                           │
│                                                 │
│ ✅ Surgery performed                            │
│ ✅ Anesthesia type                              │
│ ⏳ Current: Post-op complications or concerns   │
│ ⏳ Pain level and management                    │
│ ⏳ Vital signs on arrival to unit               │
│ ⏳ Activity level / mobility restrictions       │
│ ⏳ Diet orders                                  │
│ ⏳ Expected course and monitoring plan          │
│                                                 │
│ [Recording Waveform]                           │
│ ⏱️ 01:23                                       │
│                                                 │
│ [ STOP RECORDING ]                             │
└─────────────────────────────────────────────────┘
```

**Templates help but don't restrict:**
- Clinician can speak freely
- AI checks recording against template prompts
- Flags any missing information
- Completeness score considers template items

**C. Staff Assignment: Manual Selection for MVP**

**Rationale:**
- Auto-suggestion requires:
  - Shift schedules in system
  - Unit assignments
  - Patient assignments
  - ML model to predict best match
- Complex for MVP
- Manual is safer and still fast

**Phase 2:** Add auto-suggestions using:
```python
def suggest_recipient(patient_id, shift, unit):
    """
    Suggest best recipient based on:
    - Who's currently assigned to this patient
    - Who took previous handoff (continuity)
    - Who's scheduled for upcoming shift
    - Who's on the same unit
    - Who has lightest current patient load
    """
    pass
```

**MVP Implementation:**
```
┌─────────────────────────────────────────────────┐
│ 📤 Submit Handoff                              │
├─────────────────────────────────────────────────┤
│                                                 │
│ Your handoff is ready to submit!              │
│                                                 │
│ Assign to:                                     │
│ [ Search for nurse... ]                        │
│                                                 │
│ 🔍 Recent Recipients:                          │
│ ⚪ Jennifer Lee, RN (last took this patient)   │
│ ⚪ James Wilson, RN (on your unit)             │
│ ⚪ Maria Garcia, RN (charge nurse)             │
│                                                 │
│ 🔍 All Available:                              │
│ ⚪ Ahmed Hassan, RN                            │
│ ⚪ Lisa Chen, RN                               │
│ ⚪ Michael Johnson, RN                          │
│ ... (show all nurses on upcoming shift)        │
│                                                 │
│ ✅ Notify recipient via:                       │
│ ☑ In-app notification                          │
│ ☑ Email                                        │
│ ☐ SMS (Phase 2)                                │
│                                                 │
│ [ SUBMIT HANDOFF ]  [ SAVE DRAFT ]             │
└─────────────────────────────────────────────────┘
```

---

## 5. TECHNICAL STACK DECISIONS

**Budget-Friendly Choices (Total: ~$100/month for MVP)**

### Backend Framework
**Choice: Python + FastAPI**

**Why:**
- ✅ You're learning Python for AI/ML Master's
- ✅ FastAPI is modern, fast, easy to learn
- ✅ Great for API development
- ✅ Excellent async support (important for AI calls)
- ✅ Auto-generated API docs (Swagger)
- ✅ Strong type hints (catches bugs early)

**Cost:** Free (open source)

### Frontend Framework
**Choice: React + TypeScript**

**Why:**
- ✅ Industry standard (good for job applications)
- ✅ Huge ecosystem and community
- ✅ Works great with mobile (React Native later)
- ✅ Component reusability
- ✅ TypeScript adds safety (fewer bugs)

**Cost:** Free (open source)

### Database
**Choice: PostgreSQL**

**Why:**
- ✅ Most popular open-source relational DB
- ✅ HIPAA-compliant when configured properly
- ✅ Excellent for healthcare data (complex queries)
- ✅ JSON support (flexible for SBAR content)
- ✅ Free tier on many cloud platforms

**Cost:** Free for development, ~$10/month production

### Authentication
**Choice: Supabase Auth**

**Why:**
- ✅ Built on PostgreSQL (integrated)
- ✅ Email/password auth included
- ✅ Email verification built-in
- ✅ Password reset flows included
- ✅ Row-level security (RLS) for HIPAA
- ✅ Free tier: 50,000 monthly active users

**Cost:** Free tier is generous, ~$25/month for 100K users

### File Storage (Audio Files)
**Choice: Supabase Storage**

**Why:**
- ✅ Integrated with Supabase Auth
- ✅ S3-compatible (easy to migrate later)
- ✅ Automatic CDN
- ✅ Free tier: 1GB storage, 2GB bandwidth

**Cost:** Free tier, then $0.021/GB/month

### AI Services
**Voice-to-Text: Whisper API (OpenAI)**

**Why:**
- ✅ Best medical transcription accuracy
- ✅ Simple API
- ✅ Handles medical terminology
- ✅ Multiple language support

**Cost:** $0.006/minute of audio
- 100 handoffs/day × 2 min avg = 200 min/day
- 200 min × $0.006 = $1.20/day = $36/month

**SBAR Generation: Claude Sonnet 4 (Anthropic)**

**Why:**
- ✅ Excellent at structured output (SBAR)
- ✅ Strong medical reasoning
- ✅ Context window: 200K tokens
- ✅ Fast response time
- ✅ Safety-focused company

**Cost:** $3/million input tokens, $15/million output tokens
- Avg handoff: 500 input + 1000 output tokens
- 100 handoffs/day = 50K input + 100K output
- $0.15/day input + $1.50/day output = $1.65/day = $50/month

**Alternative for Cost Savings: Claude Haiku**
- $0.25/$1.25 per million tokens (5× cheaper)
- Good enough for MVP
- Reduces AI costs to ~$10/month

### Email Service
**Choice: Resend**

**Why:**
- ✅ Developer-friendly API
- ✅ Free tier: 100 emails/day
- ✅ Beautiful templates
- ✅ Good deliverability

**Cost:** Free tier, then $20/month for 10K emails

### Deployment
**Choice: Docker + Railway.app**

**Why:**
- ✅ Docker: Consistent environments
- ✅ Railway: Free $5 credit/month
- ✅ One-click deploy from Git
- ✅ Auto-scaling
- ✅ Built-in PostgreSQL
- ✅ Easy environment variables

**Cost:** Free tier covers MVP, ~$10-20/month for production

### Monitoring
**Choice: Sentry**

**Why:**
- ✅ Error tracking
- ✅ Performance monitoring
- ✅ Free tier: 5K errors/month

**Cost:** Free

### **TOTAL MVP COST: ~$100/month**
```
OpenAI Whisper:     $36/month
Anthropic Claude:   $50/month (or $10 with Haiku)
Supabase:          Free
Railway:           Free (or $10-20)
Sentry:            Free
Resend:            Free
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:             ~$86-106/month
```

For Phase 2, consider Azure for free student credits ($100/month).

---

## 6. MVP FEATURE BREAKDOWN

### Feature Checklist (Must Complete by Friday)

**Day 1: Foundation (Monday)**
```
Backend Setup:
☐ Initialize FastAPI project
☐ Setup PostgreSQL with Supabase
☐ Configure authentication (Supabase Auth)
☐ Create database schema (tables below)
☐ Setup Docker Compose
☐ Environment variables configuration

Frontend Setup:
☐ Initialize React + TypeScript
☐ Setup Tailwind CSS (Phoenix/Peacock colors)
☐ Configure routing (React Router)
☐ Create base layout (header, sidebar, content)
☐ Setup Axios for API calls

Authentication:
☐ Login page
☐ Registration page (15 role options)
☐ Password requirements (NIST 2025: 12-16 chars)
☐ Email verification flow
☐ Password reset flow
☐ Protected routes (redirect if not logged in)
```

**Day 2: Voice & AI Pipeline (Tuesday)**
```
Voice Recording:
☐ Recording component (tap to start/stop)
☐ Waveform visualization
☐ Duration timer
☐ Pause/resume functionality
☐ Audio file upload to Supabase Storage

AI Integration:
☐ Whisper API integration (transcription)
☐ Claude API integration (SBAR generation)
☐ API endpoint: POST /api/handoffs/process-audio
☐ Streaming response for SBAR (real-time display)
☐ Error handling (API failures, retries)

Testing:
☐ Test with sample medical audio
☐ Verify SBAR format correctness
☐ Check transcription accuracy
```

**Day 3: Update-Only Logic (Wednesday)**
```
Baseline Detection:
☐ Check if patient has baseline handoff
☐ Display "New Patient" vs "Update" UI
☐ Override button to switch modes

Baseline Handoff:
☐ Record full patient history
☐ Generate comprehensive SBAR
☐ Mark as is_baseline = true
☐ Store complete patient context

Update Handoff:
☐ Load previous baseline SBAR
☐ Display side-by-side: previous vs new recording
☐ AI compares and extracts changes
☐ Generate update-only SBAR
☐ Highlight changes in yellow
☐ Link to baseline: baseline_handoff_id

Change Detection:
☐ AI identifies what's new/different
☐ Store changes in handoff_changes table
☐ Calculate change type (improvement/decline/stable)
☐ Display change indicators (⬆️⬇️🔄)
```

**Day 4: Dashboard & Permissions (Thursday)**
```
Patient Management:
☐ Add new patient form
☐ Patient list view (table with search/filter)
☐ Patient detail page
☐ Recent handoffs for patient
☐ Assign patient to nurse

Dashboard:
☐ Role-specific landing page
☐ "My Patients" widget
☐ "Recent Handoffs" widget
☐ "Pending Reviews" widget
☐ Quick stats (handoffs today, quality score)

Handoff Viewing:
☐ List all handoffs (filterable)
☐ Individual handoff detail page
☐ SBAR display (formatted nicely)
☐ Version history (collapsible)
☐ Changes highlighted
☐ Audio playback (original recording)
☐ Edit handoff (basic)

Permissions:
☐ Role-based access control (RBAC)
☐ RN: Create/edit own, view assigned patients
☐ Charge Nurse: View all unit, reassign
☐ MD: View all, create progress notes
☐ CNA: Create updates, no delete
☐ Admin: Full access
☐ Middleware: Check permissions on API routes
```

**Day 5: Polish & Deploy (Friday)**
```
Admin Panel:
☐ User management (add, edit, deactivate)
☐ Role assignment
☐ Facility settings
☐ System logs view (searchable)
☐ Export audit logs to CSV

Audit Logging:
☐ Log all CRUD operations
☐ Log all user logins/logouts
☐ Log all data access (who viewed what, when)
☐ Searchable audit trail
☐ HIPAA-compliant retention (7+ years)

Rewards Points (Basic):
☐ Award points after handoff (automatic)
☐ Display points earned (toast notification)
☐ Dashboard widget showing total points
☐ Basic leaderboard (top 10)
☐ Tier calculation (Bronze/Silver/Gold/Platinum)

Docker & Deployment:
☐ Create Dockerfile (backend)
☐ Create Dockerfile (frontend)
☐ docker-compose.yml (all services)
☐ Sample data SQL script
☐ README with setup instructions
☐ Deploy to Railway.app
☐ Configure environment variables
☐ Test production deployment

Testing:
☐ End-to-end test (login → record → view handoff)
☐ Test all 15 user roles
☐ Test update-only flow
☐ Test permissions enforcement
☐ Load test (100 concurrent users)

Documentation:
☐ README.md (setup instructions)
☐ API documentation (Swagger)
☐ User guide (how to use system)
☐ Architecture diagram
☐ Educational docs (why we made these choices)
```

---

## 7. UI/UX MOCKUPS & PLACEHOLDERS

### Design System

**Color Variables:**
```css
:root {
  /* Phoenix Colors */
  --phoenix-orange: #ff6b35;
  --phoenix-gold: #f7931e;
  --brand-gold: #f4c430;
  
  /* Peacock Colors */
  --peacock-teal: #1a9b8e;
  --peacock-blue: #6f42c1;
  --peacock-emerald: #20c997;
  
  /* Foundation */
  --lunar-blue: #2c3e50;
  --white: #ffffff;
  --light-gray: #f8f9fa;
  --med-gray: #6c757d;
  --dark-gray: #343a40;
  
  /* Semantic */
  --success: #20c997;
  --warning: #f7931e;
  --danger: #dc3545;
  --info: #17a2b8;
  
  /* Gradients */
  --gradient-phoenix: linear-gradient(135deg, var(--phoenix-orange) 0%, var(--brand-gold) 100%);
  --gradient-peacock: linear-gradient(135deg, var(--peacock-teal) 0%, var(--peacock-blue) 100%);
  --gradient-full: linear-gradient(135deg, var(--phoenix-orange) 0%, var(--brand-gold) 50%, var(--peacock-teal) 100%);
}
```

**Typography:**
```css
/* Headers */
h1 { font-size: 2.5rem; font-weight: 700; color: var(--lunar-blue); }
h2 { font-size: 2rem; font-weight: 600; color: var(--lunar-blue); }
h3 { font-size: 1.5rem; font-weight: 600; color: var(--lunar-blue); }

/* Body */
body { font-family: 'Inter', -apple-system, sans-serif; font-size: 1rem; color: var(--dark-gray); }

/* Accent */
.gradient-text {
  background: var(--gradient-full);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### Logo & Branding Usage

**Locations for Logo:**
```
1. Navigation Bar (Top Left):
   - rohimaya-logo-circle.png (40px × 40px)
   - Next to: "EclipseLink AI" text
   
2. Sidebar (Collapsed View):
   - rohimaya-logo-circle.png (48px × 48px)
   - Center aligned
   
3. Login Page:
   - rohimaya-banner.png (full width, hero section)
   - rohimaya-logo-circle.png (centered, above form)
   
4. Loading Screens:
   - rohimaya-logo-circle.png (animated pulse)
   
5. Email Templates:
   - rohimaya-banner.png (header)
   
6. 404/Error Pages:
   - rohimaya-logo-circle.png (centered)
```

### Placeholder Images Needed

Create these placeholder images (can use Unsplash or generate):

**1. Healthcare Professional Portraits** (profile pictures)
```
Format: Square, 200×200px minimum
Needed: 15-20 diverse healthcare workers
Use for: User avatars, team photos
Style: Professional headshots, scrubs/white coats
```

**2. Hospital Environment Photos**
```
- nurse-station.jpg: Modern nurse station
- patient-room.jpg: Hospital patient room
- hallway.jpg: Hospital corridor
- doctor-patient.jpg: Doctor with patient
- team-meeting.jpg: Healthcare team discussion
Style: Clean, modern, professional, diverse
Use for: Dashboard backgrounds, marketing pages
```

**3. Medical Equipment/Icons**
```
- stethoscope-icon.svg
- clipboard-icon.svg
- heart-monitor-icon.svg
- medication-icon.svg
- iv-bag-icon.svg
Style: Line icons, peacock teal color
Use for: Dashboard widgets, feature illustrations
```

**4. Rewards/Achievements Graphics**
```
- bronze-badge.svg: Bronze peacock badge
- silver-badge.svg: Silver peacock badge
- gold-badge.svg: Gold peacock badge
- platinum-badge.svg: Platinum peacock badge
- phoenix-elite-badge.svg: Phoenix elite badge
Style: Detailed badges with peacock feathers, golden accents
Use for: Rewards dashboard, leaderboard
```

**5. Empty State Illustrations**
```
- no-patients.svg: Empty patient list
- no-handoffs.svg: No handoffs yet
- 404-page.svg: Page not found
- error-state.svg: Something went wrong
Style: Minimalist line art, peacock teal accent
Use for: Empty states, errors
```

**6. Onboarding/Tutorial Graphics**
```
- record-audio.svg: Microphone illustration
- ai-processing.svg: AI brain processing
- sbar-generation.svg: Document generation
- team-collaboration.svg: Team working together
Style: Friendly, approachable, colorful
Use for: Tutorial, help docs, marketing
```

### Mockup Pages to Create

**1. Login Page**
```html
<!-- Full-width banner background -->
<img src="rohimaya-banner.png" class="hero-bg">

<div class="login-container">
  <img src="rohimaya-logo-circle.png" width="120">
  <h1>EclipseLink AI</h1>
  <p>Rebirth • Protection • Guidance</p>
  
  <form>
    <input type="email" placeholder="Email">
    <input type="password" placeholder="Password">
    <button class="gradient-btn">Sign In</button>
  </form>
  
  <a href="/forgot-password">Forgot Password?</a>
  <a href="/register">Create Account</a>
</div>
```

**2. Dashboard (Role-Specific)**
```
┌─────────────────────────────────────────────────┐
│ [Logo] EclipseLink AI        👤 Sarah Johnson ▼│
├─────────────────────────────────────────────────┤
│                                                 │
│ 👋 Good evening, Sarah!                        │
│ Medical-Surgical Unit • Night Shift            │
│                                                 │
│ ┌───────────┬───────────┬───────────┬─────────┐│
│ │ Patients  │ Handoffs  │ Quality   │ Points  ││
│ │    8      │    12     │   94%     │  847    ││
│ └───────────┴───────────┴───────────┴─────────┘│
│                                                 │
│ 🦚 Phoenix & Peacock Honors                    │
│ 🥉 Bronze Peacock • 153 pts to Silver          │
│ [████████████░░░░░░░] 85%                      │
│                                                 │
│ 🏥 My Patients (8)                             │
│ ┌─────────────────────────────────────────────┐│
│ │ Room 302A • John Doe • POD3 Cholecystectomy ││
│ │ Last handoff: 2 hours ago                   ││
│ │ [VIEW] [UPDATE]                             ││
│ ├─────────────────────────────────────────────┤│
│ │ Room 304B • Jane Smith • CHF Exacerbation   ││
│ │ Last handoff: 30 min ago                    ││
│ │ [VIEW] [UPDATE]                             ││
│ └─────────────────────────────────────────────┘│
│                                                 │
│ 📝 Recent Handoffs                             │
│ • 7:15 PM - Updated John Doe (Room 302A)       │
│ • 6:45 PM - Updated Jane Smith (Room 304B)     │
│ • 6:30 PM - New admit: Mike Johnson (308C)     │
│                                                 │
│ [+ CREATE NEW HANDOFF]                         │
└─────────────────────────────────────────────────┘
```

**3. Voice Recording Interface**
```
┌─────────────────────────────────────────────────┐
│ ← Back    🎤 Record Handoff                    │
├─────────────────────────────────────────────────┤
│                                                 │
│ Patient: John Doe (Room 302A)                  │
│ MRN: 12345678 • DOB: 01/15/1960               │
│ Diagnosis: Post-op cholecystectomy             │
│                                                 │
│ Handoff Type:                                  │
│ ⚪ Update Existing Patient ✅ RECOMMENDED       │
│ ⚪ New Patient Admission                        │
│                                                 │
│ Template (Optional):                           │
│ [Select Template ▼] None                       │
│                                                 │
│ ┌─────────────────────────────────────────────┐│
│ │                                             ││
│ │                                             ││
│ │        [Large Circular Button]              ││
│ │                                             ││
│ │         ⚪ TAP TO START                      ││
│ │           RECORDING                          ││
│ │                                             ││
│ │        (Glove-friendly size)                ││
│ │                                             ││
│ │                                             ││
│ └─────────────────────────────────────────────┘│
│                                                 │
│ 💡 Speak naturally about what changed since    │
│    the last handoff. The AI will handle the    │
│    formatting for you.                         │
│                                                 │
│ [ CANCEL ]                                     │
└─────────────────────────────────────────────────┘
```

**4. SBAR Display**
```
┌─────────────────────────────────────────────────┐
│ ← Back    Handoff: John Doe (Room 302A)       │
├─────────────────────────────────────────────────┤
│                                                 │
│ Created: Oct 28, 2025 at 7:15 PM              │
│ By: Sarah Johnson, RN                          │
│ Type: Shift Update (Changes Only)              │
│ Quality Score: 94% ⭐⭐⭐⭐                     │
│                                                 │
│ 📝 SITUATION                                   │
│ ┌─────────────────────────────────────────────┐│
│ │ 65-year-old male, post-operative day 3      ││
│ │ following laparoscopic cholecystectomy.     ││
│ │ Pain is well-controlled at 4/10. Patient    ││
│ │ is ambulating with physical therapy.        ││
│ └─────────────────────────────────────────────┘│
│                                                 │
│ 📋 BACKGROUND                                  │
│ ┌─────────────────────────────────────────────┐│
│ │ PMH: Hypertension, Type 2 Diabetes,         ││
│ │ Obesity (BMI 38)                            ││
│ │                                             ││
│ │ Allergies: Penicillin (hives)               ││
│ │                                             ││
│ │ Current Medications:                        ││
│ │ • Morphine PCA 1mg q10min                   ││
│ │ • Metformin 1000mg BID                      ││
│ │ • Lisinopril 20mg daily                     ││
│ └─────────────────────────────────────────────┘│
│                                                 │
│ 🔍 ASSESSMENT                                  │
│ ┌─────────────────────────────────────────────┐│
│ │ Vitals: Stable                              ││
│ │ • BP: 132/78 • HR: 76 • Temp: 98.6°F       ││
│ │ • RR: 16 • SpO2: 96% on room air            ││
│ │                                             ││
│ │ Pain: 4/10 ⬇️ IMPROVED from 8/10            ││
│ │                                             ││
│ │ Ambulation: Walking 50ft with PT ⬆️         ││
│ │ IMPROVED from bedbound                      ││
│ │                                             ││
│ │ Diet: Tolerating clear liquids ⬆️           ││
│ │ ADVANCED from NPO                           ││
│ │                                             ││
│ │ Elimination: Voiding adequately             ││
│ └─────────────────────────────────────────────┘│
│                                                 │
│ 💡 RECOMMENDATION                               │
│ ┌─────────────────────────────────────────────┐│
│ │ • Continue PCA morphine, monitor q4h        ││
│ │ • Advance diet as tolerated to regular      ││
│ │ • Continue ambulation BID with PT           ││
│ │ • D/C Foley catheter today                  ││
│ │ • Expected discharge: 2-3 days if stable    ││
│ └─────────────────────────────────────────────┘│
│                                                 │
│ 🔄 Changes from Baseline (Oct 26, 2:00 PM)    │
│ [▼ Click to expand version history]           │
│                                                 │
│ 🎵 Listen to Original Recording                │
│ [▶️ Play Audio] (2:15)                         │
│                                                 │
│ [ EDIT ]  [ PRINT ]  [ SHARE ]                 │
└─────────────────────────────────────────────────┘
```

**5. Rewards Dashboard**
```
┌─────────────────────────────────────────────────┐
│ 🏆 Phoenix & Peacock Honors™                   │
├─────────────────────────────────────────────────┤
│                                                 │
│ Sarah Johnson, RN                              │
│ Medical-Surgical Unit                          │
│                                                 │
│ ┌─────────────────────────────────────────────┐│
│ │          🥉 BRONZE PEACOCK                  ││
│ │                                             ││
│ │              847 Points                     ││
│ │        Rank: #23 of 150 nurses              ││
│ │                                             ││
│ │ Progress to Silver Peacock:                 ││
│ │ [████████████████░░░░░░░] 85%               ││
│ │ 153 points to go!                           ││
│ └─────────────────────────────────────────────┘│
│                                                 │
│ 📊 This Week                                   │
│ ┌──────────┬──────────┬──────────┬──────────┐ │
│ │ Handoffs │  Points  │ Quality  │   Rank   │ │
│ │    12    │   347    │   94%    │    ⬆️ +5  │ │
│ └──────────┴──────────┴──────────┴──────────┘ │
│                                                 │
│ 🎯 Recent Achievements                         │
│ • Quality Champion: 5 days >90% SBAR score     │
│ • Speed Demon: 10 updates using update-only    │
│ • Safety Star: Caught 2 critical alerts        │
│                                                 │
│ 🎁 Available Rewards                           │
│ ┌─────────────────────────────────────────────┐│
│ │ ☕ Starbucks Card ($10).......... 250 pts   ││
│ │ 🎟️ Movie Tickets (2).............. 350 pts   ││
│ │ 🍕 Pizza Party (Unit)............ 500 pts   ││
│ │ 👕 Premium Scrubs................ 750 pts   ││
│ │ 💆 Spa Day...................... 1,200 pts   ││
│ │                                             ││
│ │ ⚠️ REDEMPTION COMING SOON - PHASE 2        ││
│ └─────────────────────────────────────────────┘│
│                                                 │
│ [ VIEW FULL CATALOG ]  [ LEADERBOARD ]         │
└─────────────────────────────────────────────────┘
```

---

## 8. EDUCATIONAL REQUIREMENTS

### Documentation to Create

**1. Architecture Overview** (`ARCHITECTURE.md`)
```markdown
# EclipseLink AI Architecture

## High-Level Overview
[Diagram showing: Frontend → API → Database + AI Services]

## Technology Stack
**Frontend:** React + TypeScript
- Why: Industry standard, component reusability
- Learning: State management (useState, useContext)
- Skills gained: Modern web development

**Backend:** Python + FastAPI
- Why: Perfect for AI integration, async support
- Learning: REST API design, async/await
- Skills gained: Backend development, API security

**Database:** PostgreSQL + Supabase
- Why: HIPAA-compliant, JSON support
- Learning: SQL, database design
- Skills gained: Data modeling, queries

**AI:** Whisper + Claude
- Why: Best transcription + reasoning
- Learning: API integration, prompt engineering
- Skills gained: AI/ML application development

## Key Design Decisions

### Decision 1: Why Update-Only Model?
Traditional handoffs waste time repeating unchanged info.
Our solution: Record baseline once, then only changes.
Result: 80% time reduction
Learning: Algorithmic thinking, change detection

### Decision 2: Why PostgreSQL over NoSQL?
Healthcare data is relational (patients → handoffs → users).
Complex queries needed (audit trails, analytics).
Learning: When to use SQL vs NoSQL

### Decision 3: Why Separate Audio Storage?
Audio files are large (2-5MB each).
Storing in DB would slow queries.
Solution: Store in Supabase Storage, link by URL.
Learning: Database normalization, file handling

... (continue for all major decisions)
```

**2. Code Walkthrough** (`CODE_GUIDE.md`)
```markdown
# Understanding the Codebase

## Project Structure
```
eclipselink-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   └── utils/        # Helper functions
│   └── main.py           # FastAPI entry point
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page views
│   │   ├── services/     # API calls
│   │   └── utils/        # Helpers
│   └── App.tsx           # React entry point
└── docker-compose.yml    # Deploy all services
```

## Key Files Explained

### `backend/app/services/ai_service.py`
What it does: Integrates Whisper + Claude
```python
async def process_audio_to_sbar(audio_file, patient_context):
    """
    1. Send audio to Whisper API → get transcript
    2. Send transcript + context to Claude → get SBAR
    3. Return formatted SBAR
    """
```

Why async: Multiple API calls can run in parallel
Learning: Async/await patterns, API integration

### `frontend/src/components/VoiceRecorder.tsx`
What it does: Records audio from microphone
```typescript
const startRecording = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  // Record audio...
};
```

Why: Browser MediaRecorder API
Learning: Browser APIs, audio handling

... (continue for all major files)
```

**3. Learning Milestones** (`LEARNING_GOALS.md`)
```markdown
# What You'll Learn Building This

## Computer Science Concepts
✅ RESTful API design
✅ Database normalization
✅ Authentication & authorization
✅ Asynchronous programming
✅ File upload handling
✅ Error handling & logging
✅ Docker containerization
✅ Git version control

## AI/ML Concepts
✅ Prompt engineering (how to write effective prompts)
✅ API integration (Whisper, Claude)
✅ Natural language processing basics
✅ Context management (sending right info to AI)
✅ Structured output generation (SBAR format)
✅ Error handling with AI (retries, fallbacks)

## Healthcare Domain
✅ SBAR communication protocol
✅ Clinical workflows (how handoffs actually work)
✅ HIPAA compliance basics
✅ Healthcare roles and permissions
✅ Medical terminology (in context)

## Software Engineering Practices
✅ Code organization (separation of concerns)
✅ Environment configuration
✅ Testing strategies
✅ Documentation
✅ Deployment
✅ Monitoring and debugging

## Business Skills
✅ Product development (MVP approach)
✅ User-centered design
✅ Feature prioritization
✅ Technical documentation for investors
✅ Demo presentation skills
```

**4. Troubleshooting Guide** (`TROUBLESHOOTING.md`)
```markdown
# Common Issues & Solutions

## Issue: "ModuleNotFoundError"
**Symptom:** Python can't find a package
**Cause:** Package not installed
**Solution:** 
```bash
pip install -r requirements.txt
```

## Issue: "CORS Error" in browser
**Symptom:** Frontend can't call backend API
**Cause:** Missing CORS configuration
**Solution:**
```python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)
```

... (continue for common issues)
```

**5. Deployment Guide** (`DEPLOYMENT.md`)
```markdown
# How to Deploy

## Local Development (Docker)
```bash
# 1. Clone repository
git clone https://github.com/yourusername/eclipselink-ai.git
cd eclipselink-ai

# 2. Create .env file
cp .env.example .env
# Edit .env with your API keys

# 3. Start all services
docker-compose up

# 4. Open browser
http://localhost:3000
```

## Production (Railway.app)
[Step-by-step with screenshots]

## Environment Variables Needed
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql://...
SUPABASE_URL=https://...
SUPABASE_KEY=...
JWT_SECRET=...
```

## Post-Deployment Checklist
☐ Test login/registration
☐ Test voice recording
☐ Test SBAR generation
☐ Test all user roles
☐ Check audit logs
☐ Load test with 100 users
```

---

## 9. DEVELOPMENT APPROACH

### How ClaudeCode Should Work

**Your Role:**
1. **Developer:** Write all code
2. **Educator:** Explain what you're doing and why
3. **Advisor:** Suggest best practices
4. **Quality Checker:** Test and validate everything

**Communication Style:**
```
✅ DO:
- Explain each major code block
- Show before/after when making changes
- Provide "why" not just "what"
- Ask clarifying questions
- Suggest alternatives when applicable
- Create comprehensive documentation

❌ DON'T:
- Just dump code without explanation
- Use jargon without defining it
- Skip error handling
- Ignore security concerns
- Assume prior knowledge
- Rush through complex topics
```

**Example Interaction:**
```
ClaudeCode: "I'm about to create the voice recording component.
This component will:

1. Request microphone access (browser API)
2. Record audio using MediaRecorder
3. Show visual feedback (waveform)
4. Upload audio file to Supabase Storage
5. Call backend API to process

I'm using the Web Audio API because:
- Built into modern browsers (no library needed)
- Real-time access to audio data (for waveform)
- Works on mobile devices

The code will look like this:
[Shows code with inline comments]

Questions before I proceed:
- Do you want the ability to pause/resume?
- Should we set a maximum recording duration?
- What audio format? (I recommend WebM for size)"

Hannah: [Answers questions]

ClaudeCode: "Great! Implementing now..."
[Creates code]

"Here's what I created: [Explanation]

To test it:
1. Click 'Record Handoff'
2. Grant microphone permission
3. Speak for 30 seconds
4. Click stop
5. You should see the audio upload

If you see an error about microphone access, make sure:
- You're using HTTPS (or localhost)
- You granted browser permission
- No other app is using the mic

Next, I'll connect this to the backend API..."
```

### Check-In Schedule

**Daily Check-Ins:**
```
End of each day:
├─ "Here's what I completed today:"
├─ [List with checkboxes]
├─ "Here's what I learned/discovered:"
├─ [Insights, gotchas, best practices]
├─ "Tomorrow I'll focus on:"
├─ [Priority tasks]
└─ "Any concerns or blockers?"
```

**Mid-Day Check-Ins:**
```
When encountering decisions:
├─ "I need your input on this:"
├─ [Present 2-3 options]
├─ [Pros/cons of each]
└─ "My recommendation: [X] because..."
```

### Educational Deliverables

**After Each Major Feature:**
```
1. Code Walkthrough Doc
   - What this feature does
   - How it works (step-by-step)
   - Key files and functions
   - How to test it

2. Design Decision Doc
   - Why I chose this approach
   - Alternatives I considered
   - Trade-offs
   - Learning resources for deeper understanding

3. Troubleshooting Guide
   - Common errors
   - How to debug
   - Solutions
```

**At End of Project:**
```
1. Complete Architecture Doc
2. API Documentation (Swagger + explanatory guide)
3. Database Schema with ERD
4. User Guide (how to use the system)
5. Developer Guide (how to extend/modify)
6. Learning Summary (skills gained)
7. Video Walkthrough (optional but recommended)
```

---

## 10. SUCCESS CRITERIA

### Friday Demo Goals

**Functional Requirements:**
```
✅ User can register and login (all 15 roles)
✅ User can add a new patient
✅ User can record audio handoff
✅ AI transcribes audio → generates SBAR
✅ System detects if initial or update
✅ User can view SBAR (formatted nicely)
✅ Changes are highlighted (update-only)
✅ User sees points earned
✅ Dashboard shows key metrics
✅ Admin can manage users
✅ Audit log captures all actions
✅ Docker deployment works (one command)
```

**Quality Requirements:**
```
✅ Code is well-commented
✅ No security vulnerabilities (basic)
✅ Error handling on all API calls
✅ Loading states for async operations
✅ Mobile-responsive (works on phone)
✅ Passes basic accessibility checks
✅ README with setup instructions
✅ Sample data preloaded
```

**Demo Scenarios:**
```
Scenario 1: Initial Handoff
1. Login as RN Sarah Johnson
2. Add new patient John Doe
3. Record 2-minute initial handoff
4. Show generated SBAR
5. Show points earned (+70)

Scenario 2: Update Handoff
1. Login as RN Jennifer Lee (next shift)
2. Open patient John Doe
3. Record 30-second update ("pain improved, ambulating")
4. Show AI compares to baseline
5. Show changes highlighted
6. Show points earned (+85, including bonus for update-only)

Scenario 3: Admin Functions
1. Login as Admin
2. Add new user (RN Mike Chen)
3. View audit logs
4. Export logs to CSV

Scenario 4: Rewards Dashboard
1. Login as RN Sarah Johnson
2. View rewards dashboard
3. Show tier progress
4. Show leaderboard
5. Browse rewards catalog
```

**Investor Pitch Elements:**
```
✅ Shows Update-Only Model™ in action
✅ Demonstrates 80% time savings
✅ Highlights AI intelligence (SBAR quality)
✅ Shows multi-role support (scalability)
✅ Demonstrates security (audit logs)
✅ Shows rewards program (retention strategy)
✅ Professional UI (market-ready)
✅ Works on multiple devices
```

---

## 11. CLAUDECODE PROMPT

**Copy this entire prompt into ClaudeCode:**

```
# PROJECT: ECLIPSELINK AI MVP DEVELOPMENT

## ROLE
You are an expert full-stack developer with expertise in:
- Python (FastAPI) backend development
- React/TypeScript frontend development
- AI integration (Whisper, Claude)
- Healthcare software (HIPAA compliance)
- Docker deployment

You are also an educator who explains WHY you make decisions, not just WHAT you're building.

## MISSION
Build a working MVP of EclipseLink AI by Friday, October 31, 2025. This is a clinical handoff system using AI that will:
1. Serve as a real product demo for investors
2. Be a learning milestone for a Computer Science Master's student
3. Showcase the revolutionary "Update-Only Model™"
4. Demonstrate professional software development practices

## CONTEXT
The founder (Hannah) is:
- A registered nurse with 15+ years experience
- Pursuing dual Master's in AI/ML and Computer Science
- Building Rohimaya Health AI (3 companies, 7 products)
- Learning to code while building a real business
- Seeking Customer Success roles in health-tech

This means:
- Explain technical concepts as you build
- Create educational documentation
- Ask clarifying questions when needed
- Suggest best practices
- Balance learning with delivery

## REQUIREMENTS

### Must Complete by Friday:
1. Authentication system (15 clinical roles)
2. Voice recording → AI pipeline (Whisper + Claude)
3. Update-Only Model™ (baseline + changes)
4. Patient management
5. Handoff viewing (SBAR display)
6. Basic dashboard (role-specific)
7. Role-based permissions
8. Admin panel
9. Audit logging
10. Basic rewards points display
11. Docker deployment

### Technology Stack (REQUIRED):
- Backend: Python + FastAPI
- Frontend: React + TypeScript
- Database: PostgreSQL (Supabase)
- Auth: Supabase Auth
- Storage: Supabase Storage
- AI: OpenAI Whisper + Anthropic Claude Sonnet
- Deployment: Docker + Railway.app

### Design Requirements:
- Rohimaya branding (peacock teal #1a9b8e, phoenix gold #f4c430)
- Logo: rohimaya-logo-circle.png
- Banner: rohimaya-banner.png
- Mobile-responsive
- Professional healthcare UI

### Security Requirements:
- NIST 2025 password policy (12-16 chars)
- Email verification
- Role-based access control (RBAC)
- Audit logging (HIPAA compliance)
- Input validation and sanitization

## YOUR APPROACH

### 1. Read This Document First
This entire brief contains:
- Answers to your 8 questions
- Technical stack decisions
- Feature breakdown
- Database schema (implied, you'll design)
- UI mockups and placeholders
- Educational requirements

### 2. Create a 5-Day Plan
Break down the work into daily chunks:
- Day 1: Foundation (auth, database, basic UI)
- Day 2: Voice & AI pipeline
- Day 3: Update-Only logic
- Day 4: Dashboard & permissions
- Day 5: Polish & deploy

Present your plan and get approval before starting.

### 3. Build Iteratively
- Start with smallest working version
- Add features incrementally
- Test after each addition
- Document as you go

### 4. Communicate Constantly
- Daily check-ins (morning: plan, evening: progress)
- Mid-day check-ins for decisions
- Explain your reasoning
- Ask questions when uncertain

### 5. Create Educational Content
After each major feature:
- Code walkthrough
- Design decisions document
- Troubleshooting guide

At end:
- Complete architecture doc
- API documentation
- Database schema diagram
- User guide
- Developer guide
- Learning summary

## SPECIFIC INSTRUCTIONS

### For Voice Recording:
- Use Web Audio API (MediaRecorder)
- Tap to start/stop (not hold)
- Visual waveform feedback
- Duration timer
- Large button (glove-friendly)
- Upload to Supabase Storage

### For AI Integration:
- Whisper API for transcription
- Claude Sonnet 4 for SBAR generation
- Include patient context in prompt
- Handle API errors gracefully
- Show streaming response (real-time)

### For Update-Only Model™:
- Check if patient has baseline handoff
- If NO → full SBAR (mark is_baseline=true)
- If YES → show previous SBAR, AI extracts changes
- Highlight changes in yellow
- Store changes in handoff_changes table
- Link to baseline: baseline_handoff_id

### For Rewards:
- Award points automatically after handoff
- Show points earned (toast notification)
- Display total points on dashboard
- Simple leaderboard (top 10)
- Tier badges (Bronze/Silver/Gold/Platinum)
- Catalog is view-only (no redemption yet)

### For Database:
Create schema for:
- users (with role, facility)
- patients (demographics, MRN)
- handoffs (SBAR content, audio URL, metadata)
- handoff_changes (what changed, old vs new)
- rewards_points (activity log, balance)
- audit_logs (who did what when)

Use PostgreSQL best practices:
- Foreign keys with proper constraints
- Indexes on frequently queried fields
- JSON columns for flexible data (SBAR content)
- Timestamps (created_at, updated_at)

### For UI:
- Use Tailwind CSS for styling
- Peacock teal, phoenix gold colors
- Place logo in nav bar (top left)
- Banner on login page (full width)
- Mobile-first responsive design
- Loading states for all async operations
- Error messages that are helpful

### For Deployment:
- Create Dockerfiles (backend, frontend)
- docker-compose.yml with all services
- Environment variables via .env
- Sample data SQL script
- One-command setup: `docker-compose up`
- README with clear instructions

## COMMUNICATION STYLE

### When Explaining Code:
```
"I'm creating the voice recording component. Here's how it works:

1. Request microphone access (navigator.mediaDevices.getUserMedia)
2. Create MediaRecorder to capture audio
3. Store audio chunks as they're recorded
4. On stop, combine chunks into Blob
5. Upload Blob to Supabase Storage
6. Pass storage URL to backend API

I chose MediaRecorder because:
- Built into browsers (no external libraries)
- Works on mobile devices
- Small file size (WebM format)
- Real-time access for waveform visualization

The code looks like this:
[Show code with comments]

To test:
1. Click 'Record Handoff'
2. Grant mic permission
3. Speak for 30 seconds
4. Click stop
5. Should see upload progress

Common issues:
- If mic access denied → check browser permissions
- If upload fails → check Supabase storage bucket settings
- If no waveform → check AudioContext initialization

Questions before I continue?"
```

### When Making Decisions:
```
"I need to decide on the database schema for handoffs. Here are the options:

Option A: Single handoffs table with JSON for SBAR
Pros: Simple, flexible
Cons: Harder to query specific SBAR fields

Option B: Separate tables for each SBAR section
Pros: Easy to query, normalized
Cons: More complex, more JOINs

Option C: Hybrid - main handoffs table + handoff_changes table
Pros: Best of both (queryable + flexible)
Cons: Slightly more complex

My recommendation: Option C because:
- We need to query for changes frequently (update-only model)
- Keeping full SBAR in JSON allows flexibility
- Separate changes table enables analytics

Do you agree, or would you prefer a different approach?"
```

### Daily Check-In Format:
```
📅 DAY 1 EVENING CHECK-IN

✅ COMPLETED TODAY:
- FastAPI backend initialized
- PostgreSQL database connected
- User registration endpoint created
- Login endpoint with JWT created
- Email verification flow implemented
- Password validation (NIST 2025)
- React frontend initialized
- Login/registration UI created
- Protected routes setup

📚 WHAT I LEARNED:
- FastAPI's dependency injection system for auth
- Supabase Auth setup and configuration
- React Router v6 protected routes pattern

🎯 TOMORROW'S PLAN:
- Voice recording component
- Whisper API integration
- Claude API integration
- Test full audio → SBAR pipeline

❓ QUESTIONS/CONCERNS:
- Whisper API costs $0.006/min - should we add length limit?
- Claude prompts getting long - should we use prompt caching?

📄 DOCS CREATED:
- setup-guide.md (how to run locally)
- auth-flow.md (explains authentication)
- api-docs.md (started, will complete daily)

🔗 COMMIT:
https://github.com/eclipselink-ai/commit/abc123
"All Day 1 features complete - auth working!"
```

## SUCCESS METRICS

You'll know you succeeded when:
✅ Hannah can demo the full flow to an investor
✅ All 15 clinical roles can login and use the system
✅ Voice recording → SBAR generation works reliably
✅ Update-Only Model™ correctly detects and highlights changes
✅ System can be deployed with one Docker command
✅ Code is well-documented and educational
✅ Hannah understands how everything works
✅ Project is ready for Phase 2 development next week

## FINAL NOTES

Remember:
- This is both a product AND a learning experience
- Explain WHY, not just WHAT
- Ask questions when unsure
- Suggest improvements
- Be educational but not condescending
- Balance quality with deadlines
- Have fun building something innovative!

The Update-Only Model™ is genuinely first-of-its-kind in healthcare.
You're building something that could save lives and reduce burnout.
Take pride in the work!

Good luck! Let's build something amazing by Friday! 🚀

---

FIRST TASK:
1. Read this entire document carefully
2. Create your 5-day development plan
3. Ask any clarifying questions
4. Get approval on the plan
5. Start building!
```

---

## APPENDIX A: DATABASE SCHEMA

### Core Tables

**users**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  role VARCHAR(50) NOT NULL, -- RN, LPN, CNA, MD, PT, etc.
  facility_id UUID REFERENCES facilities(id),
  is_active BOOLEAN DEFAULT true,
  email_verified BOOLEAN DEFAULT false,
  last_password_change TIMESTAMP,
  failed_login_attempts INT DEFAULT 0,
  locked_until TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_facility ON users(facility_id);
```

**patients**
```sql
CREATE TABLE patients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mrn VARCHAR(50) UNIQUE NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  date_of_birth DATE NOT NULL,
  gender VARCHAR(20),
  room_number VARCHAR(20),
  admission_date TIMESTAMP,
  discharge_date TIMESTAMP,
  attending_physician_id UUID REFERENCES users(id),
  primary_nurse_id UUID REFERENCES users(id),
  facility_id UUID REFERENCES facilities(id),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_patients_mrn ON patients(mrn);
CREATE INDEX idx_patients_primary_nurse ON patients(primary_nurse_id);
```

**handoffs**
```sql
CREATE TABLE handoffs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID REFERENCES patients(id) NOT NULL,
  created_by_user_id UUID REFERENCES users(id) NOT NULL,
  assigned_to_user_id UUID REFERENCES users(id),
  
  handoff_type VARCHAR(50) NOT NULL, -- 'initial_admission', 'shift_update', 'transfer'
  is_baseline BOOLEAN DEFAULT false,
  baseline_handoff_id UUID REFERENCES handoffs(id),
  
  audio_url TEXT, -- Supabase Storage URL
  audio_duration_seconds INT,
  transcript TEXT,
  
  -- SBAR content (JSON for flexibility)
  sbar_situation JSONB,
  sbar_background JSONB,
  sbar_assessment JSONB,
  sbar_recommendation JSONB,
  
  -- Quality metrics
  completeness_score INT, -- 0-100
  clarity_score INT, -- 0-100
  
  -- Status
  status VARCHAR(50) DEFAULT 'draft', -- 'draft', 'submitted', 'acknowledged'
  acknowledged_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_handoffs_patient ON handoffs(patient_id);
CREATE INDEX idx_handoffs_created_by ON handoffs(created_by_user_id);
CREATE INDEX idx_handoffs_baseline ON handoffs(baseline_handoff_id);
```

**handoff_changes**
```sql
CREATE TABLE handoff_changes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  handoff_id UUID REFERENCES handoffs(id) NOT NULL,
  field_name VARCHAR(100) NOT NULL, -- 'pain_level', 'vitals', 'medications'
  old_value TEXT,
  new_value TEXT,
  change_type VARCHAR(50), -- 'improvement', 'decline', 'stable', 'new'
  severity VARCHAR(50), -- 'critical', 'warning', 'info'
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_handoff_changes_handoff ON handoff_changes(handoff_id);
```

**rewards_points**
```sql
CREATE TABLE rewards_points (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) NOT NULL,
  points_earned INT NOT NULL,
  activity_type VARCHAR(100) NOT NULL, -- 'handoff_completed', 'high_quality', etc.
  related_handoff_id UUID REFERENCES handoffs(id),
  description TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_rewards_points_user ON rewards_points(user_id);
```

**audit_logs**
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  action VARCHAR(100) NOT NULL, -- 'create', 'read', 'update', 'delete'
  resource_type VARCHAR(100) NOT NULL, -- 'handoff', 'patient', 'user'
  resource_id UUID,
  ip_address VARCHAR(45),
  user_agent TEXT,
  details JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

---

## APPENDIX B: API ENDPOINTS

### Authentication
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/verify-email
POST   /api/auth/forgot-password
POST   /api/auth/reset-password
GET    /api/auth/me
```

### Patients
```
GET    /api/patients
POST   /api/patients
GET    /api/patients/:id
PUT    /api/patients/:id
DELETE /api/patients/:id
GET    /api/patients/:id/handoffs
```

### Handoffs
```
GET    /api/handoffs
POST   /api/handoffs
GET    /api/handoffs/:id
PUT    /api/handoffs/:id
DELETE /api/handoffs/:id
POST   /api/handoffs/process-audio
GET    /api/handoffs/:id/changes
GET    /api/handoffs/:id/history
```

### Rewards
```
GET    /api/rewards/points/:userId
GET    /api/rewards/leaderboard
GET    /api/rewards/catalog
POST   /api/rewards/redeem (Phase 2)
```

### Admin
```
GET    /api/admin/users
POST   /api/admin/users
PUT    /api/admin/users/:id
DELETE /api/admin/users/:id
GET    /api/admin/audit-logs
GET    /api/admin/stats
```

---

## APPENDIX C: ENVIRONMENT VARIABLES

```bash
# .env.example

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/eclipselink

# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# AI Services
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Auth
JWT_SECRET=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Email
RESEND_API_KEY=re_...
FROM_EMAIL=noreply@eclipselink.ai

# Frontend
REACT_APP_API_URL=http://localhost:8000

# Deployment
RAILWAY_ENVIRONMENT=production
```

---

**END OF DOCUMENT**

This comprehensive brief provides everything ClaudeCode needs to build your MVP by Friday. Copy the final prompt (Section 11) into ClaudeCode to begin development!

Good luck, Hannah! You're building something truly innovative! 🚀🦚🔥
