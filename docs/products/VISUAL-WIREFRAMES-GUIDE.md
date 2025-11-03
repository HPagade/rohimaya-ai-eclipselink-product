# ECLIPSELINK AI - VISUAL WIREFRAMES
**Screen-by-Screen Design Guide for ClaudeCode**

---

## 📱 RESPONSIVE BREAKPOINTS

```
Mobile: 320px - 767px (phone)
Tablet: 768px - 1023px (iPad)
Desktop: 1024px+ (laptop/monitor)
```

---

## 1. LOGIN PAGE

### Desktop View (1024px+)
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  [Full-width Banner Image: rohimaya-banner.png with peacock]   │
│  [Semi-transparent dark overlay]                               │
│                                                                 │
│            ┌───────────────────────────────────┐               │
│            │  [Logo: rohimaya-logo-circle.png] │               │
│            │         120px × 120px              │               │
│            │                                   │               │
│            │     EclipseLink AI                │               │
│            │  Rebirth • Protection • Guidance  │               │
│            │                                   │               │
│            │  ┌─────────────────────────────┐  │               │
│            │  │ 📧 Email                    │  │               │
│            │  └─────────────────────────────┘  │               │
│            │                                   │               │
│            │  ┌─────────────────────────────┐  │               │
│            │  │ 🔒 Password                 │  │               │
│            │  └─────────────────────────────┘  │               │
│            │                                   │               │
│            │  ┌─────────────────────────────┐  │               │
│            │  │    SIGN IN                  │  │               │
│            │  │  [Gradient: teal→gold]      │  │               │
│            │  └─────────────────────────────┘  │               │
│            │                                   │               │
│            │  Forgot Password? | Create Account│               │
│            │                                   │               │
│            └───────────────────────────────────┘               │
│                                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Mobile View (320px-767px)
```
┌──────────────────────┐
│  [Banner: stacked]   │
│                      │
│  [Logo 80px]         │
│                      │
│  EclipseLink AI      │
│  Rebirth • Protection│
│                      │
│  ┌────────────────┐  │
│  │ Email          │  │
│  └────────────────┘  │
│                      │
│  ┌────────────────┐  │
│  │ Password       │  │
│  └────────────────┘  │
│                      │
│  ┌────────────────┐  │
│  │   SIGN IN      │  │
│  └────────────────┘  │
│                      │
│  Forgot Password?    │
│  Create Account      │
│                      │
└──────────────────────┘
```

---

## 2. REGISTRATION PAGE

```
┌─────────────────────────────────────────────────────────────────┐
│ ← Back to Login              Create Your Account                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Logo 80px]                                                    │
│                                                                 │
│  Join the EclipseLink AI community of healthcare professionals  │
│                                                                 │
│  ┌────────────────────┐  ┌────────────────────┐               │
│  │ First Name         │  │ Last Name          │               │
│  └────────────────────┘  └────────────────────┘               │
│                                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │ Email                                       │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │ Password                                    │               │
│  │ ⚠️ 12-16 chars, uppercase, lowercase, number│               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │ Confirm Password                            │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │ Role                                    ▼   │               │
│  │ • Registered Nurse (RN)                     │               │
│  │ • Licensed Practical Nurse (LPN)            │               │
│  │ • Certified Nursing Assistant (CNA)         │               │
│  │ • Nurse Practitioner (NP)                   │               │
│  │ • Physician (MD/DO)                         │               │
│  │ • Physician Assistant (PA)                  │               │
│  │ • Medical Assistant (MA)                    │               │
│  │ • Physical Therapist (PT)                   │               │
│  │ • Occupational Therapist (OT)               │               │
│  │ • Respiratory Therapist (RT)                │               │
│  │ • Speech-Language Pathologist (SLP)         │               │
│  │ • Social Worker (SW)                        │               │
│  │ • Case Manager                              │               │
│  │ • Dietitian/Nutritionist                    │               │
│  │ • Pharmacist                                │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │ Facility/Hospital                       ▼   │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  ☐ I agree to Terms of Service and Privacy Policy              │
│                                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │         CREATE ACCOUNT                      │               │
│  │       [Gradient Button]                     │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  Already have an account? Sign In                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. DASHBOARD (RN View)

```
┌─────────────────────────────────────────────────────────────────┐
│ [Logo] EclipseLink AI          🔔(3)    👤 Sarah Johnson, RN ▼  │
├──────┬──────────────────────────────────────────────────────────┤
│      │                                                          │
│  🏠  │  👋 Good evening, Sarah!                                │
│  📊  │  Medical-Surgical Unit • Night Shift • Oct 28, 7:00 PM │
│  👥  │                                                          │
│  🎤  │  ┌────────┬────────┬────────┬────────┐                 │
│  🏆  │  │Patients│Handoffs│Quality │ Points │                 │
│  ⚙️  │  │   8    │   12   │  94%   │  847   │                 │
│      │  └────────┴────────┴────────┴────────┘                 │
│      │                                                          │
│      │  🦚 Phoenix & Peacock Honors™                          │
│      │  ┌────────────────────────────────────────────────┐    │
│      │  │ 🥉 Bronze Peacock                              │    │
│      │  │ Total: 847 points • Rank: #23 of 150          │    │
│      │  │                                                │    │
│      │  │ Progress to Silver:                           │    │
│      │  │ [████████████████░░░░] 85%                    │    │
│      │  │ 153 points to go!                             │    │
│      │  │                                                │    │
│      │  │ [VIEW FULL PROFILE] [LEADERBOARD]             │    │
│      │  └────────────────────────────────────────────────┘    │
│      │                                                          │
│      │  🏥 My Patients (8)                [+ ADD PATIENT]      │
│      │  ┌────────────────────────────────────────────────┐    │
│      │  │ Room 302A • John Doe • 65M                    │    │
│      │  │ POD3 Cholecystectomy                          │    │
│      │  │ Last handoff: 2 hours ago by RN Martinez      │    │
│      │  │ Status: Stable • Pain 4/10 • Ambulating       │    │
│      │  │                                                │    │
│      │  │ [VIEW DETAILS]  [🎤 UPDATE]                   │    │
│      │  ├────────────────────────────────────────────────┤    │
│      │  │ Room 304B • Jane Smith • 72F                  │    │
│      │  │ CHF Exacerbation                              │    │
│      │  │ Last handoff: 30 min ago by You               │    │
│      │  │ Status: ⚠️ Monitoring • Increased SOB         │    │
│      │  │                                                │    │
│      │  │ [VIEW DETAILS]  [🎤 UPDATE]                   │    │
│      │  ├────────────────────────────────────────────────┤    │
│      │  │ ... (6 more patients)                         │    │
│      │  └────────────────────────────────────────────────┘    │
│      │                                                          │
│      │  📝 Recent Handoffs                                     │
│      │  • 7:15 PM - Updated John Doe (Room 302A) +70 pts      │
│      │  • 6:45 PM - Updated Jane Smith (Room 304B) +85 pts    │
│      │  • 6:30 PM - New admit: Mike Johnson (308C) +50 pts    │
│      │                                                          │
│      │  ┌────────────────────────────────────────────────┐    │
│      │  │       🎤 CREATE NEW HANDOFF                    │    │
│      │  │         [Large CTA Button]                     │    │
│      │  └────────────────────────────────────────────────┘    │
│      │                                                          │
└──────┴──────────────────────────────────────────────────────────┘
```

---

## 4. NEW HANDOFF - PATIENT SELECT

```
┌─────────────────────────────────────────────────────────────────┐
│ ← Back                  🎤 Create Handoff                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Select Patient                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │ 🔍 Search by name, MRN, or room...          │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  MY PATIENTS                                                    │
│  ┌─────────────────────────────────────────────┐               │
│  │ ⚪ Room 302A • John Doe (MRN: 12345)        │               │
│  │    65M • POD3 Cholecystectomy               │               │
│  ├─────────────────────────────────────────────┤               │
│  │ ⚪ Room 304B • Jane Smith (MRN: 12346)      │               │
│  │    72F • CHF Exacerbation                   │               │
│  ├─────────────────────────────────────────────┤               │
│  │ ... (6 more patients)                       │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  OTHER UNIT PATIENTS                                            │
│  ┌─────────────────────────────────────────────┐               │
│  │ ⚪ Room 310A • Robert Brown (MRN: 12350)    │               │
│  │    55M • Post-op Hip Replacement            │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  ──────────── OR ────────────                                   │
│                                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │         + ADD NEW PATIENT                   │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  [ CANCEL ]                    [ NEXT → ]                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. VOICE RECORDING INTERFACE

```
┌─────────────────────────────────────────────────────────────────┐
│ ← Back                  🎤 Record Handoff                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Patient: John Doe (Room 302A)                                 │
│  MRN: 12345678 • DOB: 01/15/1960 • 65M                        │
│  Diagnosis: Post-op cholecystectomy (POD3)                     │
│                                                                 │
│  Handoff Type:                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │ ⚫ Update Existing Patient  ✅ RECOMMENDED  │               │
│  │    (Record only what changed - faster!)     │               │
│  │                                             │               │
│  │ ⚪ New Patient Admission                    │               │
│  │    (Full baseline handoff)                  │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  Template (Optional):                                          │
│  ┌─────────────────────────────────────────────┐               │
│  │ Select Template                         ▼   │               │
│  │ • None (Free Form)                          │               │
│  │ • Shift Change (Stable Patient)             │               │
│  │ • Post-Op from PACU                         │               │
│  │ • Transfer from ICU                         │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│                                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │                                             │               │
│  │                                             │               │
│  │        ┌───────────────────────┐            │               │
│  │        │                       │            │               │
│  │        │    [Large Circle]     │            │               │
│  │        │      150px × 150px    │            │               │
│  │        │                       │            │               │
│  │        │    ⚪ TAP TO START     │            │               │
│  │        │      RECORDING         │            │               │
│  │        │                       │            │               │
│  │        │  (Glove-friendly)     │            │               │
│  │        │                       │            │               │
│  │        └───────────────────────┘            │               │
│  │                                             │               │
│  │                                             │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  💡 TIP: Speak naturally about what changed since the last     │
│     handoff. The AI will handle the formatting for you.        │
│                                                                 │
│  Examples of what to mention:                                  │
│  • Changes in pain level or symptoms                           │
│  • New medications or treatments                               │
│  • Improvements or concerns                                    │
│  • Lab results or vital signs changes                          │
│                                                                 │
│  [ CANCEL ]                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### While Recording
```
┌─────────────────────────────────────────────────────────────────┐
│ ← Back                  🎤 Recording Handoff                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Patient: John Doe (Room 302A)                                 │
│                                                                 │
│                                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │                                             │               │
│  │        ┌───────────────────────┐            │               │
│  │        │                       │            │               │
│  │        │    [Pulsing Circle]   │            │               │
│  │        │       Red/Gold        │            │               │
│  │        │                       │            │               │
│  │        │    🔴 TAP TO STOP     │            │               │
│  │        │      RECORDING         │            │               │
│  │        │                       │            │               │
│  │        │     [Waveform]        │            │               │
│  │        │   ▁▂▃▅▇▅▃▂▁▃▅        │            │               │
│  │        │                       │            │               │
│  │        │     ⏱️ 00:42          │            │               │
│  │        │                       │            │               │
│  │        └───────────────────────┘            │               │
│  │                                             │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  🔊 Volume Level: [▮▮▮▮▮▮▮▮▮░] Good                          │
│                                                                 │
│  ✅ AI is listening for:                                       │
│  • Patient name/identifiers                                    │
│  • Changes in condition                                        │
│  • New symptoms or concerns                                    │
│  • Treatment updates                                           │
│                                                                 │
│  [ ⏸️ PAUSE ]              [ ❌ CANCEL ]                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. AI PROCESSING

```
┌─────────────────────────────────────────────────────────────────┐
│                     Processing Your Handoff...                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                                                                 │
│                  [Animated Spinning Logo]                       │
│                  [rohimaya-logo-circle.png]                     │
│                                                                 │
│                                                                 │
│                  ✅ Audio uploaded (2.3 MB)                     │
│                  ⏳ Transcribing with Whisper AI...             │
│                  ⏳ Generating SBAR with Claude AI...           │
│                  ⏳ Detecting changes from baseline...          │
│                  ⏳ Calculating quality score...                │
│                                                                 │
│                                                                 │
│  [Progress Bar: ████████████░░░░░░░] 75%                       │
│                                                                 │
│                                                                 │
│  💡 This usually takes 15-30 seconds                           │
│     Grab a coffee while AI does the work! ☕                   │
│                                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. SBAR REVIEW & EDIT

```
┌─────────────────────────────────────────────────────────────────┐
│ ← Back          Review & Submit Handoff            [ EDIT ]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Patient: John Doe (Room 302A) • 65M                           │
│  Created: Oct 28, 2025 at 7:15 PM                             │
│  Type: Shift Update (Changes Only)                             │
│  Quality Score: 94% ⭐⭐⭐⭐                                    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 📝 SITUATION                                            │   │
│  │ ┌───────────────────────────────────────────────────┐   │   │
│  │ │ 65-year-old male, post-operative day 3 following  │   │   │
│  │ │ laparoscopic cholecystectomy. Pain is             │   │   │
│  │ │ well-controlled at 4/10. Patient is ambulating    │   │   │
│  │ │ with physical therapy assistance.                 │   │   │
│  │ └───────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │ 📋 BACKGROUND                                           │   │
│  │ ┌───────────────────────────────────────────────────┐   │   │
│  │ │ PMH: Hypertension, Type 2 Diabetes, Obesity (BMI  │   │   │
│  │ │ 38)                                               │   │   │
│  │ │                                                   │   │   │
│  │ │ Allergies: Penicillin (hives)                     │   │   │
│  │ │                                                   │   │   │
│  │ │ Current Medications:                              │   │   │
│  │ │ • Morphine PCA 1mg q10min                         │   │   │
│  │ │ • Metformin 1000mg BID                            │   │   │
│  │ │ • Lisinopril 20mg daily                           │   │   │
│  │ └───────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │ 🔍 ASSESSMENT                                           │   │
│  │ ┌───────────────────────────────────────────────────┐   │   │
│  │ │ Vitals: Stable                                    │   │   │
│  │ │ • BP: 132/78 • HR: 76 • Temp: 98.6°F             │   │   │
│  │ │ • RR: 16 • SpO2: 96% on room air                  │   │   │
│  │ │                                                   │   │   │
│  │ │ Pain: 4/10 ⬇️ IMPROVED from 8/10                  │   │   │
│  │ │                                                   │   │   │
│  │ │ Ambulation: Walking 50ft with PT ⬆️               │   │   │
│  │ │ IMPROVED from bedbound                            │   │   │
│  │ │                                                   │   │   │
│  │ │ Diet: Tolerating clear liquids ⬆️                │   │   │
│  │ │ ADVANCED from NPO                                 │   │   │
│  │ │                                                   │   │   │
│  │ │ Elimination: Voiding adequately                   │   │   │
│  │ └───────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │ 💡 RECOMMENDATION                                       │   │
│  │ ┌───────────────────────────────────────────────────┐   │   │
│  │ │ • Continue PCA morphine, monitor pain q4h         │   │   │
│  │ │ • Advance diet as tolerated to regular            │   │   │
│  │ │ • Continue ambulation BID with PT                 │   │   │
│  │ │ • D/C Foley catheter today                        │   │   │
│  │ │ • Expected discharge: 2-3 days if stable          │   │   │
│  │ └───────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🔄 Changes from Baseline (Oct 26, 2:00 PM)                    │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ • Pain: 8/10 → 4/10 ⬇️ IMPROVED (50% decrease)        │    │
│  │ • Mobility: Bedbound → Ambulating 50ft ⬆️ IMPROVED     │    │
│  │ • Diet: NPO → Clear liquids ⬆️ ADVANCED               │    │
│  │                                                        │    │
│  │ [▼ View Full Version History]                         │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  🎵 Original Recording                                         │
│  [▶️ Play Audio] (2:15) [Download]                            │
│                                                                 │
│  Assign To:                                                    │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 🔍 Search for recipient...                            │    │
│  │                                                        │    │
│  │ SUGGESTED:                                             │    │
│  │ ⚪ Jennifer Lee, RN (last took this patient)          │    │
│  │ ⚪ Maria Garcia, RN (charge nurse)                     │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Notify via:  ☑ In-app  ☑ Email  ☐ SMS                       │
│                                                                 │
│  [ SAVE DRAFT ]              [ SUBMIT HANDOFF → ]             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. POINTS EARNED MODAL

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    ✅ Handoff Submitted!                        │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                                                        │    │
│  │              🏆 YOU EARNED POINTS!                     │    │
│  │                                                        │    │
│  │  Handoff Completed...................... +10 pts      │    │
│  │  Submitted On Time...................... +15 pts      │    │
│  │  Used Update-Only Feature............... +25 pts      │    │
│  │  High Quality SBAR (94%)................ +20 pts      │    │
│  │  Zero Omissions......................... +15 pts      │    │
│  │                                                        │    │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │    │
│  │  TOTAL EARNED:.......................... +85 pts      │    │
│  │                                                        │    │
│  │  Your new total: 932 points                           │    │
│  │  Progress to Silver: [█████████████░░░░] 93%          │    │
│  │  Only 68 points away! 🎉                              │    │
│  │                                                        │    │
│  │  [VIEW LEADERBOARD]        [CONTINUE]                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Handoff delivered to: Jennifer Lee, RN                        │
│  ✉️ Email notification sent                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. HANDOFF DETAIL VIEW

```
┌─────────────────────────────────────────────────────────────────┐
│ ← Back to Patient      Handoff Details          [⋮ Options ▼]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Patient: John Doe (Room 302A) • 65M • MRN: 12345678          │
│  Diagnosis: Post-op cholecystectomy (POD3)                     │
│                                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                 │
│  Created: Oct 28, 2025 at 7:15 PM                             │
│  By: Sarah Johnson, RN                                         │
│  Type: Shift Update (Changes from baseline)                    │
│  Assigned to: Jennifer Lee, RN                                 │
│  Status: ✅ Acknowledged (Oct 28, 7:20 PM)                     │
│  Quality: 94% ⭐⭐⭐⭐                                          │
│                                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                 │
│  [Full SBAR display - same as review screen]                   │
│                                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                 │
│  📅 VERSION HISTORY                                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ ⚫ Oct 28, 7:15 PM - Sarah Johnson, RN (Current)      │    │
│  │   Type: Update • Points: +85                          │    │
│  │   Changes: Pain improved, ambulating, diet advanced   │    │
│  │   [VIEW THIS VERSION]                                 │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │ ⚪ Oct 28, 7:00 AM - Jennifer Lee, RN                 │    │
│  │   Type: Update • Points: +70                          │    │
│  │   Changes: Vital signs stable, pain management        │    │
│  │   [VIEW THIS VERSION]                                 │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │ ⚪ Oct 27, 7:00 PM - Mark Williams, RN                │    │
│  │   Type: Update • Points: +65                          │    │
│  │   Changes: First ambulation attempt                   │    │
│  │   [VIEW THIS VERSION]                                 │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │ ⚪ Oct 26, 2:00 PM - Sarah Johnson, RN (Baseline)     │    │
│  │   Type: Initial Admission • Points: +50               │    │
│  │   Complete baseline SBAR created                      │    │
│  │   [VIEW THIS VERSION]                                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  [ 🎵 LISTEN TO AUDIO ]  [ 📄 EXPORT PDF ]  [ 🖨️ PRINT ]     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. REWARDS DASHBOARD

```
┌─────────────────────────────────────────────────────────────────┐
│ ← Back         🏆 Phoenix & Peacock Honors™                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Sarah Johnson, RN                                             │
│  Medical-Surgical Unit                                         │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                                                        │    │
│  │            🥉 BRONZE PEACOCK                           │    │
│  │         [Peacock Badge Image]                          │    │
│  │                                                        │    │
│  │               932 Points                               │    │
│  │          Rank: #23 of 150 nurses                       │    │
│  │                                                        │    │
│  │  Progress to Silver Peacock:                          │    │
│  │  [█████████████████░] 93%                             │    │
│  │  Only 68 points to go!                                │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                 │
│  📊 THIS WEEK                                                  │
│  ┌───────┬───────┬───────┬───────┐                             │
│  │Handoff│Points │Quality│ Rank  │                             │
│  │  12   │  347  │  94%  │ ⬆️ +5 │                             │
│  └───────┴───────┴───────┴───────┘                             │
│                                                                 │
│  🎯 RECENT ACHIEVEMENTS                                        │
│  🏅 Quality Champion: 5 days straight >90% SBAR score          │
│  ⚡ Speed Demon: 10 handoffs using update-only feature         │
│  🛡️ Safety Star: Caught 2 critical alerts early                │
│  🤝 Team Player: Helped 3 new nurses this week                 │
│                                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                 │
│  🎁 REWARDS CATALOG                       [Filter: All Tiers ▼]│
│                                                                 │
│  🥉 BRONZE TIER (100-500 points)                               │
│  ┌─────────────┬─────────────┬─────────────┐                  │
│  │  ☕         │  🎟️         │  🍕         │                  │
│  │  Starbucks  │  Movie      │  Pizza      │                  │
│  │  $10 Card   │  Tickets    │  Party      │                  │
│  │  250 pts    │  350 pts    │  500 pts    │                  │
│  │  [REDEEM]   │  [REDEEM]   │  [REDEEM]   │                  │
│  └─────────────┴─────────────┴─────────────┘                  │
│                                                                 │
│  🥈 SILVER TIER (501-2,000 points) 🔒 68 points away          │
│  ┌─────────────┬─────────────┬─────────────┐                  │
│  │  👕         │  🎵         │  💆         │                  │
│  │  Premium    │  Spotify    │  Spa Day    │                  │
│  │  Scrubs     │  3 Months   │  Gift Card  │                  │
│  │  750 pts    │  850 pts    │  1,200 pts  │                  │
│  └─────────────┴─────────────┴─────────────┘                  │
│                                                                 │
│  🥇 GOLD TIER (2,001-5,000 points)                             │
│  💎 PLATINUM TIER (5,001+ points)                              │
│                                                                 │
│  ⚠️ REDEMPTION COMING SOON - PHASE 2                          │
│  For demo purposes only. Full catalog and redemption          │
│  system will be available in next release.                    │
│                                                                 │
│  [ VIEW ALL REWARDS ]           [ LEADERBOARD ]                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. LEADERBOARD

```
┌─────────────────────────────────────────────────────────────────┐
│ ← Back         🏆 Phoenix & Peacock Honors™ Leaderboard         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [All Roles ▼]  [This Month ▼]  [My Unit ▼]                   │
│                                                                 │
│  🔥 TOP PERFORMERS                                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 🥇  1. Maria Garcia, RN............2,847 pts  💎       │    │
│  │        Med-Surg Unit • 48 handoffs • 96% quality      │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │ 🥈  2. James Wilson, RN............2,654 pts  💎       │    │
│  │        ICU • 42 handoffs • 95% quality                │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │ 🥉  3. Lisa Chen, RN...............2,341 pts  🥇       │    │
│  │        Emergency • 55 handoffs • 94% quality          │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │     4. Ahmed Hassan, RN............1,923 pts  🥇       │    │
│  │        Med-Surg Unit • 38 handoffs • 93% quality      │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │     5. Jennifer Lee, RN............1,847 pts  🥇       │    │
│  │        Med-Surg Unit • 35 handoffs • 95% quality      │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │     ...                                                │    │
│  │                                                        │    │
│  │ ⭐  23. Sarah Johnson, RN (You)....932 pts   🥉        │    │
│  │         Med-Surg Unit • 12 handoffs • 94% quality     │    │
│  │         ⬆️ Up 5 spots this week!                      │    │
│  │                                                        │    │
│  │     ...                                                │    │
│  │                                                        │    │
│  │     150. Robert Brown, RN..........124 pts   🥉        │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  🏥 TEAM STANDINGS                                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 🥇 Medical-Surgical Unit........18,473 pts (avg 92%)  │    │
│  │ 🥈 Intensive Care Unit..........16,892 pts (avg 95%)  │    │
│  │ 🥉 Emergency Department.........15,234 pts (avg 88%)  │    │
│  │    4. Pediatrics................12,567 pts (avg 91%)  │    │
│  │    5. Cardiac Care Unit.........11,234 pts (avg 93%)  │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  [ BACK TO REWARDS ]                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. ADMIN PANEL

```
┌─────────────────────────────────────────────────────────────────┐
│ [Logo] EclipseLink AI               👤 Admin ▼                  │
├──────┬──────────────────────────────────────────────────────────┤
│      │                                                          │
│  🏠  │  ⚙️ SYSTEM ADMINISTRATION                               │
│  👥  │                                                          │
│  📊  │  ┌────────┬────────┬────────┬────────┐                 │
│  📝  │  │ Users  │Facilities│Handoff│ Alerts │                 │
│  🔐  │  │  156   │    3    │ 1,247 │   12   │                 │
│      │  └────────┴────────┴────────┴────────┘                 │
│      │                                                          │
│      │  👥 USER MANAGEMENT              [+ ADD USER]           │
│      │  ┌────────────────────────────────────────────────┐    │
│      │  │ 🔍 Search users...                   [Export ▼] │    │
│      │  ├────────────────────────────────────────────────┤    │
│      │  │ Name          │ Role │ Status  │ Last Login    │    │
│      │  ├───────────────┼──────┼─────────┼───────────────┤    │
│      │  │ Sarah Johnson │  RN  │ Active  │ 2 hours ago   │    │
│      │  │ [Edit] [Deactivate] [View Activity]          │    │
│      │  ├───────────────┼──────┼─────────┼───────────────┤    │
│      │  │ Jennifer Lee  │  RN  │ Active  │ 15 min ago    │    │
│      │  │ [Edit] [Deactivate] [View Activity]          │    │
│      │  ├───────────────┼──────┼─────────┼───────────────┤    │
│      │  │ Mike Chen     │ MD   │ Active  │ 1 hour ago    │    │
│      │  │ [Edit] [Deactivate] [View Activity]          │    │
│      │  ├───────────────┼──────┼─────────┼───────────────┤    │
│      │  │ ... (153 more users)                         │    │
│      │  └────────────────────────────────────────────────┘    │
│      │                                                          │
│      │  📊 SYSTEM LOGS                      [Filter ▼] [Export]│
│      │  ┌────────────────────────────────────────────────┐    │
│      │  │ Time         │ User    │ Action     │ Resource │    │
│      │  ├──────────────┼─────────┼────────────┼──────────┤    │
│      │  │ 7:15 PM      │ Sarah J │ Created    │ Handoff  │    │
│      │  │ 7:12 PM      │ Jennifer│ Viewed     │ Patient  │    │
│      │  │ 7:10 PM      │ Mike C  │ Updated    │ Patient  │    │
│      │  │ 7:08 PM      │ Admin   │ Added User │ User     │    │
│      │  │ ... (1,000+ entries)                         │    │
│      │  └────────────────────────────────────────────────┘    │
│      │                                                          │
│      │  ⚙️ FACILITY SETTINGS                                   │
│      │  • Facility Name: Memorial Hospital                    │
│      │  • Time Zone: Mountain (UTC-7)                         │
│      │  • Default Shift Times: 7AM/7PM                        │
│      │  • Auto-logout: 15 minutes                             │
│      │  • Password Requirements: NIST 2025                    │
│      │                                                          │
│      │  [EDIT SETTINGS]                                       │
│      │                                                          │
└──────┴──────────────────────────────────────────────────────────┘
```

---

## 13. MOBILE VIEWS (320px-767px)

### Mobile Dashboard
```
┌──────────────────────┐
│ ☰  EclipseLink   🔔 │
├──────────────────────┤
│                      │
│ 👋 Sarah Johnson     │
│ Med-Surg • Night     │
│                      │
│ ┌──────────────────┐ │
│ │ Patients    8    │ │
│ │ Handoffs    12   │ │
│ │ Quality     94%  │ │
│ │ Points      932  │ │
│ └──────────────────┘ │
│                      │
│ 🦚 Bronze Peacock    │
│ [████░░░] 93%        │
│ 68 pts to Silver     │
│                      │
│ 🏥 My Patients       │
│ ┌──────────────────┐ │
│ │ 302A • John Doe  │ │
│ │ POD3 Chole       │ │
│ │ [VIEW] [UPDATE]  │ │
│ ├──────────────────┤ │
│ │ 304B • Jane S.   │ │
│ │ CHF Exacerb      │ │
│ │ [VIEW] [UPDATE]  │ │
│ └──────────────────┘ │
│                      │
│ ┌──────────────────┐ │
│ │ 🎤 NEW HANDOFF   │ │
│ └──────────────────┘ │
│                      │
└──────────────────────┘
```

### Mobile Voice Recording
```
┌──────────────────────┐
│ ← 🎤 Record Handoff  │
├──────────────────────┤
│                      │
│ John Doe (302A)      │
│ 65M • MRN: 12345     │
│                      │
│ Type:                │
│ ⚫ Update Existing   │
│ ⚪ New Admission     │
│                      │
│                      │
│   ┌──────────────┐   │
│   │              │   │
│   │   [Circle]   │   │
│   │    120px     │   │
│   │              │   │
│   │ ⚪ TAP TO    │   │
│   │    START     │   │
│   │              │   │
│   └──────────────┘   │
│                      │
│                      │
│ 💡 Speak naturally   │
│    about changes     │
│                      │
│ [ CANCEL ]           │
│                      │
└──────────────────────┘
```

---

## COLOR USAGE GUIDE

```css
/* Primary Actions */
.primary-button {
  background: linear-gradient(135deg, 
    var(--peacock-teal) 0%, 
    var(--phoenix-gold) 100%
  );
}

/* Success States */
.success {
  color: #20c997; /* Peacock emerald */
  background: #d4edda;
}

/* Warning/Alerts */
.warning {
  color: #f7931e; /* Phoenix gold */
  background: #fff3cd;
}

/* Critical/Danger */
.danger {
  color: #dc3545;
  background: #f8d7da;
}

/* Info */
.info {
  color: #17a2b8; /* Peacock blue-teal */
  background: #d1ecf1;
}

/* Improvements (up arrows) */
.improvement {
  color: #20c997;
}

/* Declines (down arrows) */
.decline {
  color: #dc3545;
}

/* Changes (circular arrow) */
.change {
  color: #17a2b8;
}
```

---

## ANIMATION GUIDELINES

```css
/* Button Hover */
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transition: all 0.2s ease;
}

/* Button Active/Click */
button:active {
  transform: scale(0.95);
  transition: all 0.1s ease;
}

/* Recording Button Pulse */
.recording-button {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* Logo Spin (Loading) */
.loading-logo {
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Progress Bar Fill */
.progress-bar {
  transition: width 0.5s ease-in-out;
}

/* Toast Notification Slide In */
.toast {
  animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
```

---

**Use these wireframes as exact templates for building the UI!**

All screens should maintain consistent:
- Header height: 64px
- Sidebar width: 240px (collapsed: 64px)
- Content padding: 24px
- Card border-radius: 8px
- Button border-radius: 6px
- Font sizes: h1:32px, h2:24px, h3:20px, body:16px
- Line height: 1.5
- Spacing: 8px increments (8, 16, 24, 32, 40...)
