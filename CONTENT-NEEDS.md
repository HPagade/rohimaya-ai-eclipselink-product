# 📸 EclipseLink AI - Content & Asset Needs

This document lists all images, videos, and other content you need to create for the MVP and demo.

---

## 🎨 BRANDING & LOGO

### 1. Primary Logo
**File:** `public/logo.svg` or `public/logo.png`
- **Size:** 512×512px (vector preferred)
- **Design:** Combine your brand symbols
  - 🦚 **Peacock** (protection, watchfulness)
  - 🔥 **Phoenix** (rebirth, transformation)
  - 🌙 **Moon** (guidance, night shift care)
- **Colors:** Use Rohimaya brand palette
  - Peacock Teal: `#0D9488`
  - Lunar Blue: `#1E3A8A`
  - Phoenix Orange: `#EA580C`
- **Usage:** Login page, navigation bar, favicon
- **Tool suggestions:**
  - Figma (free tier)
  - Canva Pro ($13/month - has medical icons)
  - Adobe Illustrator (if you have access)
  - Midjourney/DALL-E ($10-20) for AI generation

### 2. Favicon Set
**Files:** `public/favicon.ico`, `public/favicon-16x16.png`, `public/favicon-32x32.png`
- **Design:** Simplified version of primary logo
- **Generator:** Use https://realfavicongenerator.net/
- **Upload** your logo, download all sizes

### 3. App Icon (PWA)
**Files:** `public/icon-192.png`, `public/icon-512.png`
- **Usage:** When users "Add to Home Screen" on mobile
- **Design:** Same as logo, optimized for mobile

---

## 📷 SCREENSHOTS & UI MOCKUPS

### 4. Dashboard Screenshot
**File:** `docs/screenshots/dashboard.png`
- **Content:** Shows:
  - User name "Sarah Williams, RN"
  - Points: 45 points
  - Recent handoffs (3-4 items)
  - "Create Handoff" button
  - Quick stats
- **Purpose:** README, GitHub, marketing
- **How:** Take screenshot after logging in (use demo data)

### 5. Voice Recording Screenshot
**File:** `docs/screenshots/voice-recording.png`
- **Content:** Shows:
  - Patient info bar (Sarah Johnson)
  - Waveform animation (mid-recording)
  - Timer showing "0:23"
  - Pause and Stop buttons
  - Tips section visible
- **Purpose:** Demo the core feature
- **How:** Screen capture while recording

### 6. SBAR Results Screenshot
**File:** `docs/screenshots/sbar-results.png`
- **Content:** Shows:
  - "Handoff Complete!" celebration
  - Points earned (+10)
  - All 4 SBAR sections visible
  - Transcript section
- **Purpose:** Show the end result
- **How:** Take screenshot after completing handoff

### 7. Mobile View Screenshots
**Files:** `docs/screenshots/mobile-*.png` (3-4 images)
- **Content:** Key screens on mobile
  - Login screen
  - Patient selection
  - Voice recording (portrait orientation)
- **Purpose:** Show mobile-first design
- **How:** Use Chrome DevTools mobile simulator, take screenshots

---

## 👥 PATIENT PHOTOS (HIPAA-Safe)

### 8. Generic Patient Avatars
**Files:** `public/images/avatars/patient-*.png` (5 images)
- **Design:** Generic, diverse avatars (NOT real patient photos!)
- **Style:** Illustrated or abstract icons
- **Usage:** Patient cards, handoff list
- **Sources:**
  - **Free:** https://www.dicebear.com/ (API for generating avatars)
  - **Free:** https://avatar.iran.liara.run/ (Persian avatar generator)
  - **Paid:** Canva Pro avatar templates

**IMPORTANT:** Never use real patient photos! HIPAA violation!

---

## 🎥 DEMO VIDEO

### 9. Product Demo Video (2-3 minutes)
**File:** `docs/demo/eclipselink-demo.mp4`
- **Script:**
  1. **Intro (15 sec):** "EclipseLink AI: Voice-powered clinical handoffs with AI-generated SBAR documentation"
  2. **Problem (30 sec):** "Traditional handoffs take 10 minutes, are error-prone, and repetitive"
  3. **Solution (90 sec):** Demo the flow
     - Login as nurse
     - Select patient (show baseline vs update)
     - Record 20-second voice note
     - Watch AI processing animation
     - Show generated SBAR
     - Export to PDF
  4. **Update-Only Model™ (30 sec):** "Updates take only 30 seconds - 80% time savings!"
  5. **Call to Action (15 sec):** "Try it free: eclipselnk.ai"

- **Tools:**
  - **Free:** OBS Studio (screen recording)
  - **Free:** Loom (easy screen recording with face cam)
  - **Paid:** Camtasia ($300 one-time)
  - **Editing:** DaVinci Resolve (free) or iMovie (Mac)

- **Tips:**
  - Record in 1920×1080 resolution
  - Use demo data (seed-data.sql)
  - Add captions for accessibility
  - Background music (copyright-free from YouTube Audio Library)

### 10. Feature Highlights (15-second clips)
**Files:** `docs/demo/feature-*.mp4` (3-5 clips)
- Clip 1: Voice recording with waveform
- Clip 2: AI processing animation
- Clip 3: SBAR generation reveal
- Clip 4: Points earned celebration
- **Usage:** Social media (LinkedIn, Twitter, Instagram)

---

## 📊 DIAGRAMS & INFOGRAPHICS

### 11. Architecture Diagram
**File:** `docs/diagrams/architecture.png`
- **Content:** Show:
  - Frontend (React + Vite)
  - Backend (FastAPI)
  - Database (PostgreSQL)
  - AI APIs (OpenAI Whisper + Anthropic Claude)
  - File storage (local for MVP)
- **Tool:**
  - **Free:** draw.io / diagrams.net
  - **Free:** Excalidraw (hand-drawn style)
  - **Paid:** Lucidchart ($8/month)

### 12. Update-Only Model™ Infographic
**File:** `docs/marketing/update-only-model.png`
- **Content:**
  - Side-by-side comparison
  - **Traditional:** 10 min × 3 shifts = 30 min/patient/day
  - **EclipseLink:** 5 min baseline + (2 × 30 sec updates) = 6 min total
  - **Savings:** 80% (24 minutes saved!)
- **Purpose:** Explain your innovation visually
- **Tool:** Canva (use infographic templates)

### 13. SBAR Format Guide
**File:** `docs/guides/sbar-format.png`
- **Content:** Visual guide to SBAR
  - **S**ituation: What's happening now?
  - **B**ackground: What's the context?
  - **A**ssessment: What's your assessment?
  - **R**ecommendation: What should we do?
- **Purpose:** Education for users
- **Tool:** PowerPoint or Canva

---

## 📄 DOCUMENTATION IMAGES

### 14. Setup Instructions Visuals
**Files:** `docs/setup/*.png` (5-8 images)
- Database setup in pgAdmin
- Backend running in terminal
- Frontend dev server in browser
- API docs (Swagger UI) screenshot
- Environment variables file example
- **Purpose:** Make SETUP-LOCAL.md easier to follow
- **How:** Take screenshots while following your own guide

---

## 🎬 MARKETING MATERIALS

### 15. Social Media Graphics
**Files:** `docs/marketing/social/*.png` (3-5 posts)

**Post 1: Announcement**
- Template: Product announcement
- Text: "Introducing EclipseLink AI: Transform voice notes into clinical documentation in seconds"
- Size: 1080×1080 (Instagram) or 1200×675 (Twitter/LinkedIn)

**Post 2: Time Savings**
- Template: Before/After comparison
- Text: "From 10 minutes to 30 seconds per handoff"
- Include Update-Only Model™ infographic

**Post 3: Features**
- Template: Feature list
- Text: Voice recording, AI transcription, SBAR generation, points system
- Icons for each feature

**Post 4: Call to Action**
- Template: CTA card
- Text: "Join our beta program"
- Include QR code or short link

**Tool:** Canva (has healthcare templates)

### 16. Pitch Deck Slides
**File:** `docs/pitch/eclipselink-pitch.pdf`
- **Slide 1:** Title - EclipseLink AI logo, tagline
- **Slide 2:** Problem - Clinical handoffs are broken
- **Slide 3:** Solution - Voice + AI + Update-Only Model™
- **Slide 4:** Demo - Screenshots of product
- **Slide 5:** Market - $X billion healthcare documentation market
- **Slide 6:** Business Model - Subscription pricing
- **Slide 7:** Traction - Beta users, Master's research
- **Slide 8:** Team - You + advisors
- **Slide 9:** Ask - Funding/partnership needs
- **Tool:** Google Slides or PowerPoint

---

## 🖼️ PLACEHOLDER IMAGES (Temporary)

### 17. User Avatars (Temporary)
**Files:** `public/images/users/placeholder-*.png`
- Generic user silhouettes for demo users
- Different colors for different roles (blue=RN, green=MD, yellow=PT)
- **Source:** UI Avatars API: https://ui-avatars.com/api/?name=Sarah+Williams&background=0D9488&color=fff&size=128

### 18. Empty State Illustrations
**Files:** `public/images/empty-states/*.svg`
- "No handoffs yet" - clipboard with checkmark
- "No patients found" - hospital bed icon
- "No notifications" - bell with slash
- **Source:**
  - **Free:** https://undraw.co/illustrations (customizable)
  - **Free:** https://www.manypixels.co/gallery (MIT license)

---

## 📝 TEXT CONTENT NEEDS

### 19. About Page Copy
**File:** `docs/content/about.md`
- Company story
- Your background (Master's student + healthcare innovator)
- Mission statement
- **Length:** 300-500 words

### 20. FAQ Content
**File:** `docs/content/faq.md`
- Q: Is EclipseLink HIPAA compliant?
- Q: How accurate is the AI transcription?
- Q: What happens if internet goes down?
- Q: Can I edit the SBAR after generation?
- Q: How much does it cost?
- **Length:** 10-15 Q&As

### 21. Privacy Policy & Terms
**Files:** `docs/legal/privacy-policy.md`, `docs/legal/terms-of-service.md`
- **Option 1:** Use template from https://www.termsfeed.com/ ($29)
- **Option 2:** Hire lawyer ($500-1000) - recommended for healthcare!
- **Required by:** HIPAA, Apple App Store, Google Play

---

## 🎯 PRIORITY MATRIX

### Must Have (Before Demo)
- ✅ Primary logo (even if simple)
- ✅ Favicon
- ✅ Dashboard screenshot
- ✅ Voice recording screenshot
- ✅ SBAR results screenshot
- ✅ Demo video (2-3 min)

### Should Have (Before Beta Launch)
- ⏳ Mobile screenshots
- ⏳ Patient avatars
- ⏳ Architecture diagram
- ⏳ Update-Only Model™ infographic
- ⏳ Social media graphics (3 posts)

### Nice to Have (Future)
- 🔮 Feature highlight clips
- 🔮 Pitch deck
- 🔮 Setup instruction visuals
- 🔮 FAQ page
- 🔮 Legal documents (hire lawyer)

---

## 🛠️ TOOLS BUDGET

| Tool | Cost | Purpose |
|------|------|---------|
| Canva Pro | $13/month | Graphics, social media, infographics |
| Loom | $8/month | Screen recording for demos |
| Adobe Stock | $30/month | Professional icons/images (optional) |
| TermsFeed | $29 one-time | Privacy policy generator |
| **Total** | **~$50-80/month** | (Can cancel after creating assets) |

**Free alternatives:**
- Canva Free (limited templates)
- OBS Studio (screen recording)
- draw.io (diagrams)
- Unsplash/Pexels (stock photos)

---

## 📅 SUGGESTED TIMELINE

**Day 3 (Oct 29):** Logo + Screenshots
- Morning: Create logo (2-3 hours)
- Afternoon: Take 5 key screenshots (1 hour)

**Day 4 (Oct 30):** Demo Video
- Morning: Write script, practice (1 hour)
- Afternoon: Record and edit demo video (3-4 hours)

**Day 5 (Oct 31 - DEADLINE):** Polish
- Morning: Social media graphics (2 hours)
- Afternoon: Architecture diagram (1 hour)
- Evening: Final review and prep for presentation

---

## 💡 CONTENT CREATION TIPS

### For Screenshots
1. Use demo data (seed-data.sql)
2. Clear browser cache for clean UI
3. Use browser zoom at 100% (not 125% or 150%)
4. Take screenshots in 1920×1080 resolution
5. Annotate with arrows/highlights if needed (use Snagit or macOS Preview)

### For Demo Video
1. Write and practice script 3× before recording
2. Close unnecessary apps/tabs
3. Use "Do Not Disturb" mode (no notifications!)
4. Record audio separately with good mic if possible
5. Show your face in corner (builds trust)
6. Use cursor highlighting (OBS has this feature)

### For Graphics
1. Stick to brand colors (Peacock Teal, Lunar Blue, Phoenix Orange)
2. Use professional fonts (Inter, Poppins, Roboto)
3. Keep text large and readable
4. Test on mobile (50% of viewers are mobile)
5. Export as PNG for photos, SVG for logos/icons

---

## 🎓 RECOMMENDED LEARNING

### Design Basics (1-2 hours)
- **Free Course:** "Canva Design School" on YouTube
- **Free Course:** "Figma for Beginners" by Figma
- **Blog:** "7 Rules for Creating Beautiful Healthcare UIs"

### Video Production (1 hour)
- **YouTube:** "How to Make a SaaS Product Demo Video" by Y Combinator
- **YouTube:** "Screen Recording Best Practices" by Loom

### Healthcare Marketing (30 min)
- **Blog:** "How to Market Healthcare Software Without Violating HIPAA"
- **Blog:** "The Ultimate Guide to Medical Device Marketing"

---

## 📞 WHERE TO GET HELP

### Design Help
- **Fiverr:** Logo design ($25-100)
- **99designs:** Design contests ($299+)
- **Upwork:** Freelance designers ($15-50/hour)

### Video Editing Help
- **Fiverr:** Video editing ($50-150)
- **Freelancer.com:** Video editors ($20-40/hour)

### Legal Documents
- **Rocket Lawyer:** $40/month (includes consultations)
- **Local healthcare lawyer:** $200-500/hour (best for HIPAA)

---

## ✅ CHECKLIST

Before your Master's presentation:
- [ ] Logo created and added to app
- [ ] 3+ screenshots taken
- [ ] 2-3 minute demo video recorded
- [ ] Architecture diagram created
- [ ] Update-Only Model™ infographic ready
- [ ] At least 2 social media posts prepared
- [ ] Pitch deck with 9-10 slides
- [ ] Favicon added (shows in browser tab)

**You got this! 🚀**

---

## 📎 ASSETS LOCATION

Once created, save all assets to:
```
eclipselink-ai/
├── public/
│   ├── logo.svg
│   ├── favicon.ico
│   ├── images/
│   │   ├── avatars/
│   │   └── empty-states/
├── docs/
│   ├── screenshots/
│   ├── demo/
│   ├── diagrams/
│   ├── marketing/
│   └── guides/
```

**Status:** Ready to create content! Use this as your checklist.
