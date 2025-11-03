# Repository Naming Strategy Guide

**Security through obscurity for public Streamlit deployment**

---

## 🎯 Purpose

This repository needs to remain **public** for Streamlit prototype deployment, but we want to make it **harder to discover** by:
1. Using an obscured, non-descriptive repository name
2. Avoiding obvious healthcare/medical/AI keywords
3. Preventing easy association with Rohimaya or EclipseLink brands

---

## 🔒 Current Situation

**Current Name:** `rohimaya-ai-eclipselink-product`  
**Problem:** Extremely discoverable via search
- Contains brand name "rohimaya"
- Contains product name "eclipselink"
- Contains "ai" keyword
- Contains "product" keyword

**Why Public:** Streamlit requires public repositories for free deployment

---

## ✅ Recommended Repository Naming Strategy

### Naming Principles
1. **Use generic technical terms** - Make it sound like a personal project
2. **Avoid healthcare keywords** - No "health", "medical", "clinical", "hospital"
3. **Avoid AI/ML keywords** - No "ai", "ml", "openai", "chatbot"
4. **Avoid brand names** - No "rohimaya", "eclipselink", "phoenix", "peacock"
5. **Make it boring** - Generic project names are less discoverable

### Suggested Naming Patterns

#### Pattern 1: Generic Tech Stack Names
```
typescript-fullstack-starter
nextjs-fastapi-template
react-python-boilerplate
fullstack-web-application
modern-web-stack-demo
```

#### Pattern 2: Random/Obscure Technical Terms
```
sentinel-framework
nexus-platform-core
vertex-application-suite
prism-web-services
catalyst-system-base
```

#### Pattern 3: Meaningless Code Names
```
project-nebula
system-aurora
platform-genesis
framework-apex
application-vertex
```

#### Pattern 4: Generic Project Names
```
typescript-demo-project
web-app-prototype-2024
fullstack-application-demo
nodejs-python-integration
react-api-starter
```

---

## 🎨 Our Recommendation

**Recommended Name:** `typescript-web-platform` or `fullstack-demo-application`

**Why:**
- ✅ Generic and boring
- ✅ No healthcare/AI keywords
- ✅ No brand associations
- ✅ Sounds like a personal learning project
- ✅ Won't rank in searches for healthcare software
- ✅ Still descriptive enough for you to remember

**Alternative Options (in order of preference):**
1. `modern-fullstack-template`
2. `typescript-application-base`
3. `web-platform-framework`
4. `nodejs-api-project`
5. `react-python-starter`

---

## 📝 How to Rename the Repository

### Option A: Via GitHub Web Interface (Easiest)
1. Go to repository settings on GitHub
2. Scroll to "Repository name" section
3. Enter new name
4. Click "Rename"
5. Update local clone:
   ```bash
   git remote set-url origin https://github.com/HPagade/[NEW-NAME].git
   ```

### Option B: Create New Repository
1. Create new repository with obscured name
2. Clone this repository locally
3. Change remote URL:
   ```bash
   git remote set-url origin https://github.com/HPagade/[NEW-NAME].git
   ```
4. Push to new repository
5. Delete old repository

---

## 🔄 After Renaming - Update These Files

Once you rename the repository, update references in:

### Files Already Updated (Generic Placeholders)
- ✅ `README.md` - Uses `[REPOSITORY-NAME]` placeholder
- ✅ `package.json` - Uses generic URL
- ✅ This guide - Explains strategy

### Files You May Need to Update Manually
- [ ] `website/` - Any hardcoded URLs in marketing site
- [ ] `.github/workflows/` - CI/CD pipeline references
- [ ] `docker-compose.yml` - Container names (optional)
- [ ] `k8s/` manifests - Deployment names (optional)
- [ ] Any deployment scripts or configs

### Update Command After Renaming
```bash
# Replace [NEW-NAME] with your actual new repository name
find . -type f -name "*.md" -exec sed -i 's/rohimaya-ai-eclipselink-product/[NEW-NAME]/g' {} +
find . -type f -name "*.json" -exec sed -i 's/rohimaya-ai-eclipselink-product/[NEW-NAME]/g' {} +
find . -type f -name "*.yml" -exec sed -i 's/rohimaya-ai-eclipselink-product/[NEW-NAME]/g' {} +
find . -type f -name "*.yaml" -exec sed -i 's/rohimaya-ai-eclipselink-product/[NEW-NAME]/g' {} +
```

---

## 🛡️ Additional Security Measures

### 1. Update Repository Description
**Current:** Likely contains "EclipseLink" or "Rohimaya"  
**Recommended:** "Full-stack web application template" or "TypeScript application framework"

### 2. Remove Topics/Tags
Remove any healthcare, AI, or brand-related topics from repository settings

### 3. Update README Badge URLs
If README has badges linking to the repository, update them

### 4. .gitignore Sensitive Files
Ensure `.env`, `.env.local`, and any files with credentials are properly ignored

### 5. Secrets Management
- Never commit API keys
- Use environment variables
- Use GitHub Secrets for CI/CD
- Rotate any exposed keys

---

## 🎯 Streamlit Deployment Considerations

### Maintaining Public Access
- Repository **must** remain public for free Streamlit deployment
- You can make it less discoverable but not private

### Streamlit-Specific Files
If you have Streamlit apps, they're typically in:
- `streamlit_app.py` (root)
- `pages/` directory (multi-page apps)
- `prototypes/` or similar directory

Keep these files but ensure they:
- Don't expose sensitive data
- Use environment variables for API keys
- Have minimal branding (if obscurity is desired)

### Streamlit Secrets
Use Streamlit's secrets management:
- Don't commit `.streamlit/secrets.toml`
- Add to `.gitignore`
- Configure secrets in Streamlit Cloud dashboard

---

## 📊 Discoverability Analysis

### High Discoverability (Current)
- GitHub search for "eclipselink" → Finds it
- Google search for "rohimaya github" → Finds it
- Search for "clinical handoff ai" → May find it

### Low Discoverability (After Rename)
- GitHub search for "eclipselink" → Won't find it
- Google search for "rohimaya github" → Won't find it
- Search for "clinical handoff ai" → Won't find it
- Only discoverable if someone knows exact repo name

---

## ⚖️ Trade-offs

### Pros of Obscured Naming
- ✅ Harder for competitors to find
- ✅ Reduces unsolicited attention
- ✅ Maintains IP secrecy during development
- ✅ Still allows public Streamlit deployment

### Cons of Obscured Naming
- ⚠️ Harder to share with team members
- ⚠️ Less SEO if you want to showcase work later
- ⚠️ Need to maintain "real" name separately for marketing
- ⚠️ More complex documentation (need placeholders)

---

## 🎓 Final Recommendation

**Action Items for You:**

1. **Choose New Name** (Our suggestion: `typescript-web-platform`)
2. **Rename Repository** via GitHub settings
3. **Update Local Clone** with new remote URL
4. **Update Any Hardcoded References** in documentation
5. **Change Repository Description** to something generic
6. **Remove Revealing Topics/Tags** from repository settings
7. **Test Streamlit Deployment** with new name

**Remember:** The code and documentation inside the repository still describe EclipseLink AI clearly - that's fine. We're just making the repository itself harder to stumble upon.

---

## 📞 Questions?

If you need help with:
- Choosing a name
- Renaming process
- Updating references
- Streamlit deployment after rename

Contact: support@rohimaya.ai

---

**Last Updated:** November 2025  
**Status:** Repository currently named `rohimaya-ai-eclipselink-product` (to be renamed)
