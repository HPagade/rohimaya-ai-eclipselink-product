# Rohimaya Health AI - Product Suite Architecture

## 🏗️ Platform Overview

**Rohimaya Health AI** is an integrated healthcare AI platform with 8 products serving 10.6M+ healthcare professionals with a combined TAM of $50+ billion.

### Architecture Model: **Unified Platform**
- **Single Authentication**: One login for all products
- **Shared Database**: PostgreSQL with product-specific tables
- **Shared Navigation**: Seamless switching between products
- **Cross-Product Integration**: Real-time data sharing and alerts
- **Universal Rewards**: Phoenix & Peacock Honors across all products

---

## 📦 Product Suite

### 1. ✅ **EclipseLink AI™** - Clinical Handoffs ($18.9B TAM)
**Status**: COMPLETE ✅
- Voice-to-SBAR conversion
- Update-Only Model™
- Shift handoff management
- HIPAA-compliant audit trail

### 2. 🔥 **PlumeDose AI™** - Medication Management ($8.4B TAM)
**Status**: BUILDING - FULL MVP
- Medication schedule tracking
- Administration verification (barcode scanning)
- Drug interaction warnings
- PRN (as-needed) tracking
- Medication reconciliation
- Alerts for missed doses

### 3. 🛡️ **RiseGuard AI™** - Fall Prevention ($6.2B TAM)
**Status**: BUILDING - FULL MVP
- Morse Fall Scale risk scoring
- Real-time fall alerts
- Incident reporting and tracking
- Environmental risk assessment
- Patient mobility tracking
- Predictive analytics

### 4. 🧪 **LunarBridge AI™** - Clinical Trial Matching ($3.8B TAM)
**Status**: BUILDING - FULL MVP
- Patient eligibility matching
- Trial database with advanced search
- Enrollment tracking
- Consent management
- Automated eligibility screening
- Trial progress monitoring

### 5. 🔬 **FeatherSight AI™** - Lab Intelligence ($5.1B TAM)
**Status**: BUILDING - Basic Prototype
- Lab results dashboard
- Critical value alerts
- Trend analysis
- Abnormal result flagging
- Export to EHR

### 6. 🫁 **PhoenixBreath AI™** - Respiratory Monitoring ($2.9B TAM)
**Status**: BUILDING - Basic Prototype
- Respiratory vitals tracking (SpO2, RR)
- Ventilator data display
- Oxygen saturation trends
- ABG (arterial blood gas) tracking
- Alert system for critical values

### 7. 💪 **WingStrength AI™** - PT/OT Optimization ($4.6B TAM)
**Status**: BUILDING - Basic Prototype
- Therapy session tracking
- Exercise plan management
- Progress notes
- Goal setting and tracking
- Mobility assessment

### 8. 🏆 **Phoenix & Peacock Honors™** - Universal Rewards Program
**Status**: BUILDING - Basic Prototype
- Points earned across all products
- Rewards catalog (PTO, meals, spa, education)
- Leaderboard
- Achievement badges
- Points redemption

---

## 🗄️ Database Schema

### Shared Tables (All Products)
```
facilities          - Healthcare facilities
users              - All healthcare professionals
patients           - Patient master records
audit_logs         - Cross-product audit trail
notifications      - Real-time alerts
reward_points      - Phoenix & Peacock points
reward_transactions - Point earning/redemption history
```

### Product-Specific Tables

**EclipseLink AI™**
```
handoffs           - Clinical handoffs
handoff_versions   - Version history
```

**PlumeDose AI™**
```
medications        - Medication master list
medication_orders  - Prescribed medications
medication_admin   - Administration records
drug_interactions  - Known interactions
medication_alerts  - Active alerts
```

**RiseGuard AI™**
```
fall_assessments   - Risk assessment records
fall_incidents     - Reported falls
fall_alerts        - Active alerts
environmental_risks - Room/area hazards
```

**LunarBridge AI™**
```
clinical_trials    - Trial database
trial_criteria     - Inclusion/exclusion criteria
trial_enrollments  - Patient enrollments
trial_consents     - Consent documents
```

**FeatherSight AI™**
```
lab_results        - Lab test results
lab_panels         - Test panels/groups
critical_values    - Critical thresholds
```

**PhoenixBreath AI™**
```
respiratory_vitals - Respiratory measurements
ventilator_settings - Vent configurations
abg_results        - ABG test results
```

**WingStrength AI™**
```
therapy_sessions   - PT/OT sessions
exercise_plans     - Exercise prescriptions
therapy_goals      - Patient goals
mobility_assessments - Mobility evaluations
```

---

## 🎨 Frontend Architecture

### Structure
```
apps/frontend/src/
├── pages/
│   ├── Dashboard.tsx              (Main hub - all products)
│   ├── eclipselink/               (Handoffs)
│   │   ├── Handoffs.tsx
│   │   ├── HandoffDetail.tsx
│   │   └── VoiceRecorder.tsx
│   ├── plumedose/                 (Medications)
│   │   ├── Medications.tsx
│   │   ├── MedicationOrders.tsx
│   │   ├── Administration.tsx
│   │   └── Alerts.tsx
│   ├── riseguard/                 (Falls)
│   │   ├── FallRiskAssessments.tsx
│   │   ├── FallIncidents.tsx
│   │   └── Alerts.tsx
│   ├── lunarbridge/               (Trials)
│   │   ├── ClinicalTrials.tsx
│   │   ├── TrialMatching.tsx
│   │   └── Enrollments.tsx
│   ├── feathersight/              (Labs)
│   │   ├── LabResults.tsx
│   │   └── CriticalValues.tsx
│   ├── phoenixbreath/             (Respiratory)
│   │   ├── RespiratoryVitals.tsx
│   │   └── Ventilator.tsx
│   ├── wingstrength/              (PT/OT)
│   │   ├── TherapySessions.tsx
│   │   └── ExercisePlans.tsx
│   └── rewards/                   (Honors)
│       ├── PointsBalance.tsx
│       ├── RewardsCatalog.tsx
│       └── Leaderboard.tsx
├── components/
│   ├── Layout.tsx                 (Unified navigation)
│   ├── ProductSwitcher.tsx        (Switch between products)
│   └── [product-specific]/
└── services/
    ├── authService.ts
    ├── plumedoseService.ts
    ├── riseguardService.ts
    └── [other services]
```

### Navigation
- **Top Bar**: Product switcher (dropdown or tabs)
- **Sidebar**: Product-specific navigation
- **Dashboard**: Hub showing all products at a glance
- **Notifications**: Cross-product alerts

---

## 🔧 Backend Architecture

### Structure
```
apps/backend/app/
├── models/
│   ├── facility.py
│   ├── user.py
│   ├── patient.py
│   ├── handoff.py              (EclipseLink)
│   ├── medication.py           (PlumeDose)
│   ├── fall_assessment.py      (RiseGuard)
│   ├── clinical_trial.py       (LunarBridge)
│   ├── lab_result.py           (FeatherSight)
│   ├── respiratory_vital.py    (PhoenixBreath)
│   ├── therapy_session.py      (WingStrength)
│   └── reward.py               (Honors)
├── routers/
│   ├── auth.py
│   ├── patients.py
│   ├── eclipselink/
│   │   └── handoffs.py
│   ├── plumedose/
│   │   ├── medications.py
│   │   └── administration.py
│   ├── riseguard/
│   │   ├── assessments.py
│   │   └── incidents.py
│   ├── lunarbridge/
│   │   ├── trials.py
│   │   └── matching.py
│   └── [other products]
└── services/
    ├── alert_service.py       (Cross-product alerts)
    ├── rewards_service.py     (Points calculation)
    └── integration_service.py (Product integration)
```

---

## 🔗 Cross-Product Integration Examples

### Example 1: Medication → Fall Risk
```
PlumeDose detects sedative medication administered
  ↓
RiseGuard automatically increases fall risk score
  ↓
Nurse receives alert in EclipseLink handoff
  ↓
All products earn reward points
```

### Example 2: Lab Result → Respiratory Alert
```
FeatherSight receives critical ABG result
  ↓
PhoenixBreath flags respiratory distress
  ↓
Alert sent to all staff via notifications
  ↓
EclipseLink adds to next handoff automatically
```

### Example 3: Trial Eligibility
```
New patient admitted via EclipseLink
  ↓
LunarBridge scans for trial eligibility
  ↓
Physician notified of matching trials
  ↓
Enrollment process initiated
```

---

## 🌐 Marketing Website

### Separate Next.js App
```
apps/marketing/
├── pages/
│   ├── index.tsx              (Homepage)
│   ├── products/
│   │   ├── eclipselink.tsx
│   │   ├── plumedose.tsx
│   │   └── [other products]
│   ├── pricing.tsx
│   ├── about.tsx
│   └── contact.tsx
└── components/
    ├── Hero.tsx
    ├── ProductCard.tsx
    └── Testimonials.tsx
```

---

## 🚀 Deployment Strategy

### Development
- SQLite database (apps/backend/eclipselink.db)
- All products in one backend instance
- One frontend with all routes
- Local development on ports 4000 (backend) and 3000 (frontend)

### Production
- PostgreSQL (Supabase)
- Backend on Railway (auto-scaling)
- Frontend on Vercel/Cloudflare Pages
- Marketing site on separate domain (rohimaya.ai)
- Product platform on (app.rohimaya.ai)

---

## 📊 Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (SQLite for dev)
- **ORM**: SQLAlchemy
- **Auth**: JWT tokens
- **API Docs**: Swagger/OpenAPI

### Frontend (Platform)
- **Framework**: React 18 + TypeScript + Vite
- **State**: Zustand
- **HTTP**: Axios
- **UI**: Tailwind CSS
- **Router**: React Router

### Marketing Website
- **Framework**: Next.js 14
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Forms**: React Hook Form

---

## 📈 Development Phases

### ✅ Phase 1: Foundation (COMPLETE)
- Shared auth system
- Database schema
- EclipseLink AI complete

### 🔥 Phase 2: Full MVPs (IN PROGRESS)
- PlumeDose AI (medication management)
- RiseGuard AI (fall prevention)
- LunarBridge AI (clinical trials)

### 📦 Phase 3: Basic Prototypes
- FeatherSight AI
- PhoenixBreath AI
- WingStrength AI
- Phoenix & Peacock Honors

### 🌐 Phase 4: Marketing Website
- Homepage with hero
- 8 product pages
- Pricing, about, contact

### 🔗 Phase 5: Integration
- Cross-product alerts
- Shared rewards system
- Unified dashboard

### ✨ Phase 6: Polish
- Animations
- Comprehensive testing
- Documentation

---

**Built with ❤️ by Rohimaya Health AI**
*Transforming Healthcare, One Innovation at a Time*
