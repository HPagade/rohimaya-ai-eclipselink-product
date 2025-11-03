# EclipseLink AI - Wireframes & User Flows
**Created:** October 28, 2025
**Purpose:** MVP Prototype Design (Tue-Fri Sprint)

---

## 1. OVERALL APPLICATION ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                    EclipseLink AI Platform                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                                           ↓
┌───────────────────┐                    ┌──────────────────────┐
│   ON-PREMISE      │                    │   CLOUD (HIPAA)      │
│  (Large Hospitals)│                    │  (Small Hospitals)   │
├───────────────────┤                    ├──────────────────────┤
│ • Kubernetes      │                    │ • Railway Backend    │
│ • Self-hosted DB  │                    │ • Supabase Database  │
│ • Local Storage   │                    │ • Cloudflare Pages   │
│ • Air-gapped OK   │                    │ • Cloudflare R2      │
└───────────────────┘                    └──────────────────────┘
         ↓                                           ↓
         └───────────────────┬───────────────────────┘
                             ↓
              ┌──────────────────────────┐
              │   Shared Services        │
              ├──────────────────────────┤
              │ • Azure OpenAI (Whisper) │
              │ • Azure OpenAI (GPT-4)   │
              │ • EHR Adapters           │
              │ • Rewards API            │
              └──────────────────────────┘
```

---

## 2. USER ROLES & NAVIGATION

### **Primary User Roles** (All get tailored views)
1. **Registered Nurses (RN)** - Most frequent users
2. **Licensed Practical Nurses (LPN)**
3. **Certified Nursing Assistants (CNA)**
4. **Physicians (MD/DO)**
5. **Nurse Practitioners (NP)**
6. **Physician Assistants (PA)**
7. **Respiratory Therapists (RT)**
8. **Physical/Occupational Therapists (PT/OT)**
9. **Pharmacists (PharmD)**
10. **Social Workers (MSW/LCSW)**
11. **Case Managers**
12. **Facility Administrators**
13. **IT Staff / System Admins**

### **Navigation Structure**
```
┌──────────────────────────────────────────────────────────┐
│  [≡] EclipseLink AI    [Profile] [🏆 2,450 pts] [Notify] │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  📊 Dashboard    🎤 New Handoff    📋 My Patients       │
│  📚 Handoff History    👥 Team    ⚙️ Settings           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 3. KEY USER FLOWS

### **Flow 1: New Handoff (Voice-to-SBAR)**
```
START
  ↓
[Login] → [Dashboard] → [New Handoff Button]
                              ↓
                    ┌─────────────────────┐
                    │ Select Patient       │
                    │ (Search or Scan ID)  │
                    └──────────┬───────────┘
                              ↓
                    ┌─────────────────────┐
                    │ Record Voice         │
                    │ (Tap & Hold)         │
                    │ [●] REC 00:45       │
                    │ Waveform animation   │
                    └──────────┬───────────┘
                              ↓
                    ┌─────────────────────┐
                    │ Processing...        │
                    │ [Progress: 30%]      │
                    │ • Transcribing       │
                    │ • Analyzing          │
                    └──────────┬───────────┘
                              ↓
                    ┌─────────────────────┐
                    │ Review SBAR          │
                    │ (Edit if needed)     │
                    │ S: [...]             │
                    │ B: [...]             │
                    │ A: [...]             │
                    │ R: [...]             │
                    └──────────┬───────────┘
                              ↓
                    ┌─────────────────────┐
                    │ Assign to Staff      │
                    │ ☑ RN Johnson         │
                    │ ☑ Dr. Smith          │
                    │ ☐ PT Williams        │
                    └──────────┬───────────┘
                              ↓
                    ┌─────────────────────┐
                    │ Submit Handoff       │
                    │ [Submit Button]      │
                    └──────────┬───────────┘
                              ↓
                    ┌─────────────────────┐
                    │ Success!             │
                    │ +50 pts earned 🏆    │
                    │ [View Dashboard]     │
                    └─────────────────────┘
END
```

### **Flow 2: Update-Only Model (Subsequent Handoff)**
```
[Dashboard] → [My Patients] → [Select Patient: John Doe]
                                      ↓
                          ┌───────────────────────┐
                          │ Previous SBAR shown   │
                          │ Last updated: 6h ago  │
                          │ by RN Martinez        │
                          └──────────┬────────────┘
                                    ↓
                          ┌───────────────────────┐
                          │ [Record Update Only]  │
                          │ "BP increased to 140" │
                          │ 🎤 00:15 (quick!)     │
                          └──────────┬────────────┘
                                    ↓
                          ┌───────────────────────┐
                          │ AI merges update      │
                          │ into existing SBAR    │
                          │ Changes highlighted   │
                          └──────────┬────────────┘
                                    ↓
                          ┌───────────────────────┐
                          │ Submit (80% faster!)  │
                          │ +25 pts earned 🏆     │
                          └───────────────────────┘
```

### **Flow 3: Critical Alert Detection**
```
[Voice Recording] → [AI Processing]
                          ↓
              ┌───────────────────────┐
              │ ⚠️ CRITICAL DETECTED   │
              │ "Chest pain, SOB"     │
              │ Auto-escalate to MD?  │
              │ [YES] [NO]            │
              └───────────┬───────────┘
                         ↓ (YES)
              ┌───────────────────────┐
              │ 🚨 Urgent notification │
              │ sent to:              │
              │ • Dr. Smith (MD)      │
              │ • RN Supervisor       │
              │ • Rapid Response Team │
              └───────────────────────┘
```

---

## 4. MAIN SCREENS (Desktop/Tablet)

### **Screen 1: Login / Registration**
```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│                     [EclipseLink Logo]                   │
│                  Voice-Enabled Clinical Handoffs         │
│                                                          │
│              ┌────────────────────────────┐              │
│              │  Email: [____________]     │              │
│              │  Password: [__________]    │              │
│              │                            │              │
│              │  [Sign In]                 │              │
│              │                            │              │
│              │  Forgot Password?          │              │
│              │  New User? Register        │              │
│              └────────────────────────────┘              │
│                                                          │
│  🔒 HIPAA Compliant • SOC 2 Type II • SSL Encrypted     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### **Screen 2: Dashboard (RN View)**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [≡] EclipseLink AI    Welcome, RN Martinez  [🏆 2,450] [🔔 3]      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📊 Dashboard    🎤 New Handoff    📋 My Patients    👥 Team        │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 🎤 Quick Actions                                              │ │
│  │  [New Handoff]  [Update Patient]  [View Team Activity]       │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌─────────────────────────┐  ┌─────────────────────────────────┐ │
│  │ 📋 My Active Patients  │  │ 🏆 Rewards & Achievements       │ │
│  ├─────────────────────────┤  ├─────────────────────────────────┤ │
│  │ • John Doe (Rm 301)    │  │ Total Points: 2,450             │ │
│  │   Last update: 2h ago  │  │ This Week: +150 pts             │ │
│  │   [Update] [View SBAR] │  │                                 │ │
│  │                         │  │ 🎯 Next Goal: 3,000 pts         │ │
│  │ • Jane Smith (Rm 305)  │  │ Unlock: Premium Coffee ☕       │ │
│  │   Last update: 4h ago  │  │                                 │ │
│  │   [Update] [View SBAR] │  │ Recent Rewards:                 │ │
│  │                         │  │ • Handoff completed: +50 pts   │ │
│  │ • Bob Johnson (Rm 310) │  │ • Update-only used: +25 pts    │ │
│  │   ⚠️ Critical alerts   │  │ • Early submission: +10 pts    │ │
│  │   [URGENT]             │  │                                 │ │
│  └─────────────────────────┘  └─────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 📊 Today's Statistics                                         │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │  Handoffs Completed: 12    Avg Time Saved: 4.2 min          │ │
│  │  Critical Alerts: 2        Team Collaboration: 8 shared       │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 🔔 Recent Activity Feed                                       │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │ 10:45 AM - Dr. Smith reviewed handoff for John Doe           │ │
│  │ 10:30 AM - You submitted handoff for Jane Smith (+50 pts)    │ │
│  │ 09:15 AM - RN Johnson shared handoff with PT Williams        │ │
│  │ 08:45 AM - Critical alert: Bob Johnson vitals abnormal       │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### **Screen 3: New Handoff - Voice Recorder**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [← Back]  New Handoff                              [🏆 2,450] [🔔] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Step 1 of 3: Record Voice Handoff                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ Patient: John Doe (MRN: 12345678)                             │ │
│  │ Room: 301-A  |  Age: 68  |  Dx: Post-op hip replacement       │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                               │ │
│  │                     🎤 Voice Recorder                          │ │
│  │                                                               │ │
│  │               ╔════════════════════════╗                      │ │
│  │               ║                        ║                      │ │
│  │               ║     [●] Recording      ║                      │ │
│  │               ║                        ║                      │ │
│  │               ║      ┃┃┃┃┃┃┃┃┃┃┃      ║  (Waveform)         │ │
│  │               ║      ┃┃┃┃┃┃┃┃┃┃┃      ║                      │ │
│  │               ║                        ║                      │ │
│  │               ║      02:34 / 10:00     ║                      │ │
│  │               ║                        ║                      │ │
│  │               ╚════════════════════════╝                      │ │
│  │                                                               │ │
│  │         [Stop Recording]  [Pause]  [Cancel]                   │ │
│  │                                                               │ │
│  │  💡 Tips:                                                     │ │
│  │  • Speak clearly and at normal pace                           │ │
│  │  • Include SBAR format: Situation, Background, Assessment...  │ │
│  │  • Mention critical alerts clearly                            │ │
│  │  • You can edit the transcript after recording                │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 🔄 Offline Mode: Audio will upload when connection restored   │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### **Screen 4: Processing & SBAR Generation**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [← Back]  New Handoff                              [🏆 2,450] [🔔] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Step 2 of 3: AI Processing                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                               │ │
│  │                  🤖 Generating SBAR Report                    │ │
│  │                                                               │ │
│  │                  [████████████░░░░░░░░]  65%                 │ │
│  │                                                               │ │
│  │                  Current Step:                                │ │
│  │                  ✓ Voice uploaded                             │ │
│  │                  ✓ Transcription complete (Azure Whisper)    │ │
│  │                  ⏳ Analyzing clinical context...             │ │
│  │                  ⏱️ Generating structured SBAR...             │ │
│  │                  ⏱️ Detecting critical alerts...              │ │
│  │                                                               │ │
│  │                  Estimated time: 15 seconds                   │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 📝 Transcript Preview:                                        │ │
│  │                                                               │ │
│  │ "Patient is a 68-year-old male, post-op day 2 from right     │ │
│  │  hip replacement. Vitals stable, BP 135/82, HR 78...         │ │
│  │  Patient reports pain 6/10, managed with scheduled Norco...  │ │
│  │  Physical therapy initiated today, patient ambulated 10 ft   │ │
│  │  with walker and assistance..."                               │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### **Screen 5: Review & Edit SBAR**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [← Back]  New Handoff                              [🏆 2,450] [🔔] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Step 3 of 3: Review SBAR Report                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                     │
│  ⚠️ CRITICAL ALERT DETECTED: Pain level 6/10 - Requires review    │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ Patient: John Doe (MRN: 12345678)  |  Recorded: 10/28 10:45 AM│ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 📋 SBAR Report                                [Edit] [Export] │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │                                                               │ │
│  │ S - SITUATION                                                 │ │
│  │ ──────────────────────────────────────────────────            │ │
│  │ 68-year-old male, post-op day 2 from right hip replacement.  │ │
│  │ Currently on orthopedic unit, Room 301-A. Requesting pain    │ │
│  │ management review.                                            │ │
│  │                                                 [Edit Section] │ │
│  │                                                               │ │
│  │ B - BACKGROUND                                                │ │
│  │ ──────────────────────────────────────────────────            │ │
│  │ PMH: Osteoarthritis, HTN, Type 2 DM                          │ │
│  │ Allergies: Penicillin (rash)                                 │ │
│  │ Surgery: 10/26 - Right total hip arthroplasty (Dr. Johnson)  │ │
│  │ Current meds: Norco q4h PRN, Metformin 1000mg BID, Lisinopril│ │
│  │                                                 [Edit Section] │ │
│  │                                                               │ │
│  │ A - ASSESSMENT                                                │ │
│  │ ──────────────────────────────────────────────────            │ │
│  │ Vitals: BP 135/82, HR 78, Temp 98.6°F, SpO2 98% RA           │ │
│  │ Pain: 6/10 right hip, worse with movement                    │ │
│  │ Mobility: Ambulated 10 ft with walker, PT supervision        │ │
│  │ Incision: Clean, dry, intact. No signs of infection.         │ │
│  │ ⚠️ ALERT: Pain score trending up from 4/10 this AM           │ │
│  │                                                 [Edit Section] │ │
│  │                                                               │ │
│  │ R - RECOMMENDATION                                            │ │
│  │ ──────────────────────────────────────────────────            │ │
│  │ 1. Consider pain medication adjustment - consult MD           │ │
│  │ 2. Continue PT sessions twice daily                           │ │
│  │ 3. Monitor incision site q8h                                  │ │
│  │ 4. Encourage incentive spirometry q2h while awake            │ │
│  │ 5. DVT prophylaxis: Lovenox 40mg SubQ daily (scheduled)      │ │
│  │                                                 [Edit Section] │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 👥 Assign Handoff To:                                         │ │
│  │ ☑ RN Johnson (incoming shift)                                │ │
│  │ ☑ Dr. Smith (attending physician)                            │ │
│  │ ☑ PT Williams (physical therapy)                             │ │
│  │ ☐ Social Work                                                │ │
│  │ ☐ Pharmacy                                                   │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│         [🎤 Re-record]    [💾 Save Draft]    [📤 Submit Handoff]   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### **Screen 6: Patient List & Handoff History**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [← Back]  My Patients                              [🏆 2,450] [🔔] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [Search Patients...]                    [Filter ▼] [Sort by: Name]│
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 📋 Active Patients (8)                                        │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │                                                               │ │
│  │ ┌─────────────────────────────────────────────────────────┐  │ │
│  │ │ 👤 John Doe (MRN: 12345678)              Room: 301-A    │  │ │
│  │ │    Age: 68 | Dx: Post-op hip replacement                │  │ │
│  │ │    ⚠️ Critical Alert: Pain management needed             │  │ │
│  │ │                                                          │  │ │
│  │ │    Last Handoff: 2h ago by RN Martinez                   │  │ │
│  │ │    Assigned to: RN Johnson, Dr. Smith, PT Williams      │  │ │
│  │ │                                                          │  │ │
│  │ │    [View SBAR] [Update] [Add Note] [History: 12 total]  │  │ │
│  │ └─────────────────────────────────────────────────────────┘  │ │
│  │                                                               │ │
│  │ ┌─────────────────────────────────────────────────────────┐  │ │
│  │ │ 👤 Jane Smith (MRN: 87654321)            Room: 305-B    │  │ │
│  │ │    Age: 54 | Dx: CHF exacerbation                       │  │ │
│  │ │    ✓ Stable - No alerts                                 │  │ │
│  │ │                                                          │  │ │
│  │ │    Last Handoff: 4h ago by RN Martinez                   │  │ │
│  │ │    Assigned to: RN Johnson, Dr. Lee                     │  │ │
│  │ │                                                          │  │ │
│  │ │    [View SBAR] [Update] [Add Note] [History: 8 total]   │  │ │
│  │ └─────────────────────────────────────────────────────────┘  │ │
│  │                                                               │ │
│  │ ┌─────────────────────────────────────────────────────────┐  │ │
│  │ │ 👤 Bob Johnson (MRN: 11223344)           Room: 310-A    │  │ │
│  │ │    Age: 72 | Dx: Pneumonia                              │  │ │
│  │ │    🚨 URGENT: SpO2 dropping - 88% RA                    │  │ │
│  │ │                                                          │  │ │
│  │ │    Last Handoff: 30m ago by RN Davis                     │  │ │
│  │ │    Assigned to: YOU, Dr. Smith, RT Brown                │  │ │
│  │ │                                                          │  │ │
│  │ │    [VIEW NOW] [Update] [Call RT] [History: 15 total]    │  │ │
│  │ └─────────────────────────────────────────────────────────┘  │ │
│  │                                                               │ │
│  │  ... 5 more patients ...                                     │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 📊 Quick Stats                                                │ │
│  │ Total Active: 8  |  Critical Alerts: 2  |  Due for Update: 3 │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### **Screen 7: Family Portal (Patient-Facing)**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [EclipseLink Family Portal]                    [Español] [中文] [AR]│
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Welcome, Smith Family 👋                                          │
│  Viewing updates for: Jane Smith                                   │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 📰 Latest Update - Today at 2:30 PM                           │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │                                                               │ │
│  │ Your loved one is doing well today. Here's what's happening: │ │
│  │                                                               │ │
│  │ ✓ Jane is resting comfortably in her room                    │ │
│  │ ✓ Vitals are stable and looking good                         │ │
│  │ ✓ She ate 75% of lunch and is drinking fluids                │ │
│  │ ✓ Physical therapy session completed this morning            │ │
│  │ ✓ Doctor visited and is pleased with progress                │ │
│  │                                                               │ │
│  │ 🏥 What's Next:                                               │ │
│  │ • Evening medication at 6 PM                                  │ │
│  │ • Light dinner around 5:30 PM                                 │ │
│  │ • Another therapy session tomorrow morning                    │ │
│  │                                                               │ │
│  │ 💬 Questions? [Message Care Team]                            │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 📊 Today's Overview                                           │ │
│  │ ☺️ Comfort Level: Good         💊 Medications: On schedule   │ │
│  │ 🍽️ Appetite: Fair              🚶 Activity: Light walking    │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 📅 Previous Updates                                           │ │
│  │ • Oct 28, 10:00 AM - Morning care completed                  │ │
│  │ • Oct 27, 6:00 PM - Evening update                           │ │
│  │ • Oct 27, 2:00 PM - Afternoon check-in                       │ │
│  │ [View All Updates]                                            │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  🔔 Get text alerts for important updates  [Enable Notifications] │
│                                                                     │
│  🔒 This portal is secure and HIPAA compliant                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### **Screen 8: AI Chatbot (Clinical Q&A)**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [← Back]  AI Assistant                             [🏆 2,450] [🔔] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🤖 EclipseLink AI Assistant                                       │
│  Ask questions about your patients and handoffs                    │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ Chat History                                                  │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │                                                               │ │
│  │ You: What's the latest on John Doe in 301?                   │ │
│  │                                                               │ │
│  │ 🤖 Assistant: John Doe (Room 301-A) was last updated 2 hours │ │
│  │    ago. Key points:                                           │ │
│  │    • Post-op day 2 from hip replacement                       │ │
│  │    • Pain level: 6/10 (⚠️ increased from 4/10)               │ │
│  │    • Vitals stable: BP 135/82, HR 78                         │ │
│  │    • PT session completed today                               │ │
│  │    • Critical alert: Pain management needs MD review          │ │
│  │                                                               │ │
│  │    [View Full SBAR] [Update Patient]                         │ │
│  │                                                               │ │
│  │ ─────────────────────────────────────────────────             │ │
│  │                                                               │ │
│  │ You: Has Dr. Smith reviewed the pain management plan?        │ │
│  │                                                               │ │
│  │ 🤖 Assistant: Not yet. Dr. Smith was notified 15 minutes ago │ │
│  │    about the critical alert. Would you like me to send a     │ │
│  │    follow-up notification?                                    │ │
│  │                                                               │ │
│  │    [Yes, Send Follow-up] [No, Thanks]                        │ │
│  │                                                               │ │
│  │ ─────────────────────────────────────────────────             │ │
│  │                                                               │ │
│  │ You: Show me all patients with critical alerts               │ │
│  │                                                               │ │
│  │ 🤖 Assistant: Found 2 patients with active critical alerts:  │ │
│  │                                                               │ │
│  │    1. John Doe (301-A) - Pain 6/10, needs MD review          │ │
│  │    2. Bob Johnson (310-A) - SpO2 88%, RT notified            │ │
│  │                                                               │ │
│  │    [View Details] [Clear Alerts]                             │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ Type your question... [🎤 Voice]                  [Send →]    │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  💡 Try asking:                                                    │
│  • "Who needs a handoff update in the next hour?"                  │
│  • "Summarize all patients with diabetes"                          │
│  • "What medications is Jane Smith taking?"                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### **Screen 9: Admin Panel (System Configuration)**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [← Back]  Admin Panel                             [🏆 2,450] [🔔] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ⚙️ System Administration                                          │
│                                                                     │
│  [Facility Settings] [User Management] [EHR Integration] [Security]│
│  [Audit Logs] [Rewards Config] [Reports] [Support]                 │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 🏥 Facility Settings                                          │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │                                                               │ │
│  │ Facility Name: [Memorial Hospital                        ]   │ │
│  │ Facility ID: [MEML-001                                   ]   │ │
│  │ Time Zone: [America/New_York                      ▼]          │ │
│  │ Address: [123 Medical Center Dr, City, ST 12345         ]   │ │
│  │                                                               │ │
│  │ Deployment Type: ○ Cloud (HIPAA)   ● On-Premise             │ │
│  │                                                               │ │
│  │ [Save Changes]                                                │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 👥 User Management (247 active users)                        │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │                                                               │ │
│  │ [+ Add New User]  [Import from CSV]  [Bulk Actions ▼]        │ │
│  │                                                               │ │
│  │ [Search users...]                              [Filter: All ▼]│ │
│  │                                                               │ │
│  │ Name               Role        Department    Status    Actions│ │
│  │ ─────────────────────────────────────────────────────────────│ │
│  │ Sarah Martinez     RN          ICU           ✓ Active  [Edit] │ │
│  │ John Smith         MD          Cardiology    ✓ Active  [Edit] │ │
│  │ Lisa Johnson       LPN         Med-Surg      ✓ Active  [Edit] │ │
│  │ Mike Williams      PT          Rehab         ✓ Active  [Edit] │ │
│  │ ...                                                           │ │
│  │                                                               │ │
│  │ Showing 10 of 247 users                    [1] 2 3 ... 25 >  │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 🔗 EHR Integration                                            │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │                                                               │ │
│  │ EHR System: [Epic                                      ▼]     │ │
│  │                                                               │ │
│  │ Status: ⚠️ Not Connected                                      │ │
│  │                                                               │ │
│  │ Connection Details:                                           │ │
│  │ API Endpoint: [https://fhir.epic.com/                    ]   │ │
│  │ Client ID: [your-client-id                               ]   │ │
│  │ Client Secret: [••••••••••••••••                        ]   │ │
│  │                                                               │ │
│  │ Features:                                                     │ │
│  │ ☑ Auto-import patient demographics                           │ │
│  │ ☑ Sync medications and allergies                             │ │
│  │ ☑ Push SBAR reports to EHR notes                             │ │
│  │ ☐ Real-time vitals monitoring                                │ │
│  │                                                               │ │
│  │ [Test Connection]  [Save Configuration]                      │ │
│  │                                                               │ │
│  │ Other Supported Systems:                                      │ │
│  │ • Cerner/Oracle Health [Configure]                           │ │
│  │ • MEDITECH [Configure]                                       │ │
│  │ • Allscripts [Configure]                                     │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 🏆 Rewards Program Configuration                              │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │                                                               │ │
│  │ Program Status: ✓ Enabled (Phoenix & Peacock Honors™)        │ │
│  │                                                               │ │
│  │ Point Values:                                                 │ │
│  │ • Complete handoff: [50] points                              │ │
│  │ • Update-only handoff: [25] points                           │ │
│  │ • Critical alert detected: [10] points                       │ │
│  │ • Early submission: [10] points                              │ │
│  │ • Team collaboration: [15] points                            │ │
│  │                                                               │ │
│  │ Rewards Catalog:                                              │ │
│  │ • 500 pts - Coffee shop gift card                            │ │
│  │ • 1,000 pts - Meal delivery credit                           │ │
│  │ • 2,500 pts - Paid time off (4 hours)                        │ │
│  │ • 5,000 pts - Spa day package                                │ │
│  │                                                               │ │
│  │ [Edit Point Values]  [Manage Catalog]                        │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### **Screen 10: Rewards Dashboard (Phoenix & Peacock Honors)**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [← Back]  My Rewards                               [🏆 2,450] [🔔] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🏆 Phoenix & Peacock Honors™                                      │
│  Your Rewards Dashboard                                            │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ Your Total Points: 2,450                                      │ │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 49%                │ │
│  │ Next Goal: 3,000 pts - Unlock Premium Tier! (550 pts away)   │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────┐  ┌───────────────────────────────────┐ │
│  │ 📊 This Week          │  │ 🎯 Achievements                   │ │
│  ├───────────────────────┤  ├───────────────────────────────────┤ │
│  │ Points Earned: +150   │  │ 🥇 Early Bird (10/10 on-time)    │ │
│  │ Handoffs: 12          │  │ 🏅 Team Player (50 collaborations)│ │
│  │ Updates: 8            │  │ 🌟 Quality Pro (98% accuracy)    │ │
│  │ Rank: #3 in ICU       │  │ 🔥 Week Streak: 52 weeks!        │ │
│  └───────────────────────┘  └───────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 🛍️ Rewards Catalog                                            │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │                                                               │ │
│  │ ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐│ │
│  │ │  ☕ Coffee Card   │  │  🍕 Meal Credit  │  │ 🏖️ PTO 4hrs  ││ │
│  │ │  500 points      │  │  1,000 points    │  │ 2,500 points ││ │
│  │ │  [Redeem Now]    │  │  [Redeem Now]    │  │ [Redeem Now] ││ │
│  │ └──────────────────┘  └──────────────────┘  └──────────────┘│ │
│  │                                                               │ │
│  │ ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐│ │
│  │ │  💆 Spa Day      │  │  🎟️ Event Tix    │  │ 🏝️ PTO 8hrs  ││ │
│  │ │  5,000 points    │  │  3,500 points    │  │ 7,500 points ││ │
│  │ │  [Redeem Now]    │  │  [Save & Earn]   │  │ [Save & Earn]││ │
│  │ └──────────────────┘  └──────────────────┘  └──────────────┘│ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 📈 Points History                                             │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │ Oct 28 - +50 pts - Handoff completed (John Doe)              │ │
│  │ Oct 28 - +25 pts - Update-only handoff (Jane Smith)          │ │
│  │ Oct 27 - +50 pts - Handoff completed (Bob Johnson)           │ │
│  │ Oct 27 - +15 pts - Team collaboration bonus                  │ │
│  │ Oct 26 - +10 pts - Early submission bonus                    │ │
│  │ [View All History]                                            │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  💡 Tip: Complete 5 more handoffs this week to earn a 50pt bonus! │
│                                                                     │
│  🔗 Works across all Rohimaya Health AI products:                 │
│     EclipseLink • PlumeDose • RiseGuard • LunarBridge + more      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. MOBILE / TABLET RESPONSIVE VIEWS

### **Mobile: Dashboard (Portrait)**
```
┌────────────────────────┐
│ ≡  EclipseLink AI  🔔3│
├────────────────────────┤
│                        │
│ Welcome, RN Martinez   │
│ 🏆 2,450 pts           │
│                        │
│ ┌────────────────────┐ │
│ │ 🎤 NEW HANDOFF     │ │
│ └────────────────────┘ │
│                        │
│ 📋 My Patients (8)     │
│ ┌────────────────────┐ │
│ │ John Doe - 301-A   │ │
│ │ ⚠️ Pain mgmt needed│ │
│ │ [Update] [View]    │ │
│ └────────────────────┘ │
│                        │
│ ┌────────────────────┐ │
│ │ Jane Smith - 305-B │ │
│ │ ✓ Stable           │ │
│ │ [Update] [View]    │ │
│ └────────────────────┘ │
│                        │
│ ┌────────────────────┐ │
│ │ Bob Johnson - 310  │ │
│ │ 🚨 URGENT: Low O2  │ │
│ │ [VIEW NOW]         │ │
│ └────────────────────┘ │
│                        │
│ [... 5 more ...]       │
│                        │
│ ═══════════════════════│
│ 📊 Dashboard           │
│ 🎤 New Handoff         │
│ 📋 Patients            │
│ 👥 Team                │
│ ⚙️ Settings            │
└────────────────────────┘
```

### **Tablet: Voice Recorder (Landscape)**
```
┌────────────────────────────────────────────────────────────┐
│ [← Back]  New Handoff                    [🏆 2,450] [🔔 3]│
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Patient: John Doe (MRN: 12345678)  |  Room: 301-A        │
│                                                            │
│ ┌────────────────────────────────────────────────────────┐│
│ │                                                        ││
│ │                   🎤 Voice Recorder                    ││
│ │                                                        ││
│ │            ╔═══════════════════════════╗               ││
│ │            ║                           ║               ││
│ │            ║     [●] Recording         ║               ││
│ │            ║                           ║               ││
│ │            ║     ┃┃┃┃┃┃┃┃┃┃┃┃┃        ║               ││
│ │            ║     ┃┃┃┃┃┃┃┃┃┃┃┃┃        ║               ││
│ │            ║                           ║               ││
│ │            ║     02:34 / 10:00         ║               ││
│ │            ║                           ║               ││
│ │            ╚═══════════════════════════╝               ││
│ │                                                        ││
│ │      [STOP RECORDING]  [PAUSE]  [CANCEL]              ││
│ │                                                        ││
│ └────────────────────────────────────────────────────────┘│
│                                                            │
│ 💡 Speak clearly at normal pace. Mention critical info.   │
│                                                            │
│ 🔄 Offline Mode Active - Will sync when online            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 6. EHR INTEGRATION WORKFLOWS

### **Epic Integration Flow**
```
┌──────────────────┐
│  EclipseLink AI  │
└────────┬─────────┘
         │ FHIR API (HL7)
         ↓
┌──────────────────┐
│  Epic EHR        │
├──────────────────┤
│ 1. Patient Import│ → Demographics, MRN, Allergies, Meds
│ 2. Vitals Sync   │ → Real-time BP, HR, Temp, SpO2
│ 3. SBAR Export   │ → Push to Epic clinical notes
│ 4. Alert Routing │ → Send critical alerts to Epic inbox
└──────────────────┘

Authentication: OAuth 2.0 / JWT
Data Format: FHIR R4
Sync Frequency: Real-time for vitals, Batch for demographics
```

### **Cerner/Oracle Health Integration Flow**
```
┌──────────────────┐
│  EclipseLink AI  │
└────────┬─────────┘
         │ Cerner Millennium API
         ↓
┌──────────────────┐
│ Cerner/Oracle    │
├──────────────────┤
│ 1. Patient Data  │ → Demographics, ADT messages
│ 2. Clinical Data │ → Medications, Labs, Vitals
│ 3. Documentation │ → Export SBAR to Progress Notes
│ 4. Notifications │ → Integration with PowerChart alerts
└──────────────────┘

Authentication: OAuth 2.0 / Custom tokens
Data Format: FHIR R4 / HL7 v2 messages
Sync Frequency: Configurable (5-15 min intervals)
```

### **MEDITECH Integration Flow**
```
┌──────────────────┐
│  EclipseLink AI  │
└────────┬─────────┘
         │ MEDITECH Web Services API
         ↓
┌──────────────────┐
│  MEDITECH        │
├──────────────────┤
│ 1. Patient Query │ → Get patient demographics, orders
│ 2. Clinical Fetch│ → Retrieve meds, allergies, vitals
│ 3. Note Creation │ → Push SBAR as nursing note
│ 4. Alert System  │ → Trigger MEDITECH clinical alerts
└──────────────────┘

Authentication: API Keys / Custom auth
Data Format: HL7 v2 / Proprietary XML
Sync Frequency: Polling every 10 minutes
```

---

## 7. OFFLINE MODE ARCHITECTURE

```
┌─────────────────────────────────────────────┐
│         User's Device (Tablet/Phone)        │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Progressive Web App (PWA)           │  │
│  ├──────────────────────────────────────┤  │
│  │  • Service Worker (caching)          │  │
│  │  • IndexedDB (local storage)         │  │
│  │  • Background Sync API               │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  OFFLINE CAPABILITIES:                      │
│  ✓ Record voice (stores locally)           │
│  ✓ View cached patient list                │
│  ✓ Read previous SBAR reports              │
│  ✓ Queue handoffs for upload               │
│  ✓ View recent activity (cached)           │
│                                             │
│  ❌ NOT AVAILABLE OFFLINE:                  │
│  • AI processing (requires cloud)          │
│  • Real-time team updates                  │
│  • EHR data sync                            │
│  • Critical alerts (send when online)      │
│                                             │
└─────────────────────────────────────────────┘
              ↓ (when connection restored)
┌─────────────────────────────────────────────┐
│         Background Sync Process             │
│  1. Upload queued voice recordings          │
│  2. Process SBAR generation                 │
│  3. Send pending notifications              │
│  4. Sync latest patient data                │
│  5. Notify user of completion               │
└─────────────────────────────────────────────┘
```

---

## 8. DEPLOYMENT ARCHITECTURE

### **Option A: Cloud (Small Hospitals)**
```
┌────────────────────────────────────────────────┐
│            Cloudflare Network                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Cloudflare Pages (Frontend)             │  │
│  │  • CDN distribution (195+ cities)        │  │
│  │  • SSL/TLS termination                   │  │
│  │  • DDoS protection                       │  │
│  └──────────────────────────────────────────┘  │
└────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────┐
│            Railway (Backend)                   │
│  ┌──────────────────────────────────────────┐  │
│  │  Express.js API Server                   │  │
│  │  • Auto-scaling                          │  │
│  │  • Load balancing                        │  │
│  │  • Health checks                         │  │
│  └──────────────────────────────────────────┘  │
└────────────────────────────────────────────────┘
         ↓                    ↓
┌──────────────────┐   ┌──────────────────┐
│  Supabase        │   │  Upstash Redis   │
│  (PostgreSQL)    │   │  (Cache/Queue)   │
└──────────────────┘   └──────────────────┘
         ↓
┌──────────────────┐
│  Cloudflare R2   │
│  (File Storage)  │
└──────────────────┘
```

### **Option B: On-Premise (Large Hospitals)**
```
┌────────────────────────────────────────────────┐
│     Hospital Data Center / Private Cloud       │
│  ┌──────────────────────────────────────────┐  │
│  │  Kubernetes Cluster                      │  │
│  │  ┌────────────┐  ┌────────────────────┐  │  │
│  │  │  Ingress   │  │  Frontend Pods (3) │  │  │
│  │  │  (NGINX)   │→│  (Next.js)        │  │  │
│  │  └────────────┘  └────────────────────┘  │  │
│  │                  ┌────────────────────┐  │  │
│  │                  │  Backend Pods (5)  │  │  │
│  │                  │  (Express.js)      │  │  │
│  │                  └────────────────────┘  │  │
│  │                  ┌────────────────────┐  │  │
│  │                  │  Worker Pods (3)   │  │  │
│  │                  │  (BullMQ)          │  │  │
│  │                  └────────────────────┘  │  │
│  └──────────────────────────────────────────┘  │
│                                                │
│  ┌──────────────────┐   ┌──────────────────┐  │
│  │  PostgreSQL HA   │   │  Redis Cluster   │  │
│  │  (Primary+Replic)│   │  (Sentinel)      │  │
│  └──────────────────┘   └──────────────────┘  │
│                                                │
│  ┌──────────────────────────────────────────┐  │
│  │  Storage (NFS/SAN)                       │  │
│  │  • Voice recordings (encrypted)          │  │
│  │  • Documents                             │  │
│  │  • Backups (7-year retention)            │  │
│  └──────────────────────────────────────────┘  │
│                                                │
│  ┌──────────────────────────────────────────┐  │
│  │  Monitoring & Logging                    │  │
│  │  • Prometheus + Grafana                  │  │
│  │  • ELK Stack (logs)                      │  │
│  │  • Alert Manager                         │  │
│  └──────────────────────────────────────────┘  │
└────────────────────────────────────────────────┘
            ↓ (outbound only for AI)
┌────────────────────────────────────────────────┐
│      Azure OpenAI (Whisper + GPT-4)            │
│      • VPN tunnel or private endpoint          │
└────────────────────────────────────────────────┘
```

---

## 9. USER PERMISSIONS & ROLES

### **Role-Based Access Control (RBAC) Matrix**
```
Feature/Action           | RN | LPN | CNA | MD | NP | PA | RT | PT | Admin
─────────────────────────|────|─────|─────|────|────|────|────|────|──────
View own patients        | ✓  | ✓   | ✓   | ✓  | ✓  | ✓  | ✓  | ✓  | ✓
View all patients        | ✓  | ✓   | ○   | ✓  | ✓  | ✓  | ○  | ○  | ✓
Create new handoff       | ✓  | ✓   | ✓   | ✓  | ✓  | ✓  | ✓  | ✓  | ✓
Update handoff (own)     | ✓  | ✓   | ✓   | ✓  | ✓  | ✓  | ✓  | ✓  | ✓
Update handoff (others)  | ✓  | ○   | ○   | ✓  | ✓  | ✓  | ○  | ○  | ✓
Delete handoff           | ○  | ○   | ○   | ✓  | ○  | ○  | ○  | ○  | ✓
View SBAR reports        | ✓  | ✓   | ✓   | ✓  | ✓  | ✓  | ✓  | ✓  | ✓
Edit SBAR (after submit) | ○  | ○   | ○   | ✓  | ✓  | ○  | ○  | ○  | ✓
Assign handoffs          | ✓  | ○   | ○   | ✓  | ✓  | ✓  | ○  | ○  | ✓
Manage critical alerts   | ✓  | ○   | ○   | ✓  | ✓  | ✓  | ✓  | ○  | ✓
Access family portal     | ○  | ○   | ○   | ○  | ○  | ○  | ○  | ○  | ✓
Manage users             | ○  | ○   | ○   | ○  | ○  | ○  | ○  | ○  | ✓
Configure EHR            | ○  | ○   | ○   | ○  | ○  | ○  | ○  | ○  | ✓
View audit logs          | ○  | ○   | ○   | ○  | ○  | ○  | ○  | ○  | ✓
Manage rewards program   | ○  | ○   | ○   | ○  | ○  | ○  | ○  | ○  | ✓

Legend: ✓ = Full Access | ○ = Limited/Conditional | ✗ = No Access
```

---

## 10. NEXT STEPS (Implementation Order)

### **Phase 1: Core Infrastructure (Today - Tuesday)**
1. Clean up repository (remove demos, consolidate docs)
2. Create Docker Compose setup
3. Set up database with seed data
4. Configure environment variables

### **Phase 2: Backend Development (Wednesday)**
1. Implement voice upload endpoint
2. Azure OpenAI integration (Whisper transcription)
3. SBAR generation service (GPT-4)
4. Critical alert detection logic
5. Rewards points calculation

### **Phase 3: Frontend Development (Thursday AM)**
1. Login/registration screens
2. Dashboard with patient list
3. Voice recorder component
4. SBAR viewer/editor
5. Responsive mobile/tablet layouts

### **Phase 4: Advanced Features (Thursday PM)**
1. Family portal (plain-language summaries)
2. AI chatbot (clinical Q&A)
3. Multi-language translation
4. Admin panel basics

### **Phase 5: Integration & Testing (Friday)**
1. EHR adapter framework (Epic/Cerner/MEDITECH)
2. Offline mode + PWA setup
3. Rewards dashboard
4. End-to-end testing
5. Demo data population

---

## 11. SUCCESS CRITERIA

**By Friday EOD, you should be able to:**
1. ✓ Deploy locally with `docker-compose up`
2. ✓ Login as different user roles (RN, MD, Admin)
3. ✓ Record a voice handoff on tablet/phone
4. ✓ See AI-generated SBAR report (real Azure OpenAI)
5. ✓ View patient list with critical alerts
6. ✓ See rewards points earned
7. ✓ Configure EHR settings (UI ready, actual connection later)
8. ✓ Test offline mode (record voice, syncs when online)
9. ✓ View family portal as patient family member
10. ✓ Ask AI chatbot questions about patients

---

**Ready to start building! 🚀**
**Next action: Clean up repository and set up Docker.**
