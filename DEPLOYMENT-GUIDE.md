# 🚀 EclipseLink AI - Complete Deployment & Setup Guide

**For Team Use | Production Ready | Responsive Design**

---

## 📋 Table of Contents
1. [Quick Start (Local Development)](#quick-start)
2. [Team Setup](#team-setup)
3. [Production Deployment Options](#production-deployment)
4. [Mobile & Responsive Testing](#responsive-testing)
5. [Team Collaboration Workflow](#team-workflow)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Quick Start (Local Development)

### Prerequisites
- Node.js 18+ ([Download](https://nodejs.org))
- Python 3.11+ ([Download](https://python.org))
- Git

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/HPagade/rohimaya-ai-eclipselink-product.git
cd rohimaya-ai-eclipselink-product

# Create environment file
cp .env.example .env
```

### 2. Install Dependencies

```bash
# Install frontend dependencies
cd apps/frontend
npm install
cd ../..

# Install backend dependencies
cd apps/backend
pip install -r requirements.txt
cd ../..
```

### 3. Initialize Database

```bash
cd apps/backend
python3 init_db.py
cd ../..
```

### 4. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd apps/backend
DATABASE_URL="sqlite:///./eclipselink.db" python3 -m uvicorn app.main:app --host 0.0.0.0 --port 4000
```

**Terminal 2 - Frontend:**
```bash
cd apps/frontend
VITE_API_URL=http://localhost:4000/api npm run dev
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:4000
- **API Docs**: http://localhost:4000/api/docs

### 6. Create Your First Account

1. Go to http://localhost:3000
2. Click "Sign up"
3. Fill in your details
4. Start using EclipseLink AI!

---

## 👥 Team Setup

### For Each Team Member

**1. Get Repository Access**
```bash
git clone https://github.com/HPagade/rohimaya-ai-eclipselink-product.git
cd rohimaya-ai-eclipselink-product
```

**2. Install Dependencies (One Time)**
```bash
# Frontend
cd apps/frontend && npm install && cd ../..

# Backend
cd apps/backend && pip install -r requirements.txt && cd ../..
```

**3. Set Up Environment**
```bash
cp .env.example .env
# Edit .env with your local settings (usually defaults are fine)
```

**4. Initialize Database (One Time)**
```bash
cd apps/backend && python3 init_db.py && cd ../..
```

**5. Daily Workflow**

Start both servers (in separate terminals):

```bash
# Terminal 1 - Backend
cd apps/backend
DATABASE_URL="sqlite:///./eclipselink.db" python3 -m uvicorn app.main:app --host 0.0.0.0 --port 4000

# Terminal 2 - Frontend
cd apps/frontend
npm run dev
```

Access at: http://localhost:3000

---

## 🌐 Production Deployment Options

### Option 1: Cloud Deployment (Recommended for Small Teams)

#### Services Needed:
- **Frontend**: Vercel or Netlify (Free tier available)
- **Backend**: Railway or Render (Starts at $5/month)
- **Database**: Supabase (Free tier available)

#### Step-by-Step: Vercel + Railway + Supabase

**A. Deploy Backend to Railway**

1. Go to [Railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Configure:
   - Root Directory: `apps/backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   ```
   DATABASE_URL=(your Supabase connection string)
   SECRET_KEY=(generate with: openssl rand -hex 32)
   CORS_ORIGINS=["https://your-frontend-url.vercel.app"]
   ```
6. Deploy! You'll get a URL like: `https://your-app.railway.app`

**B. Set Up Supabase Database**

1. Go to [Supabase.com](https://supabase.com) and sign up
2. Create new project
3. Go to Settings → Database
4. Copy the **Connection String** (Connection pooling mode)
5. In Supabase SQL Editor, run:
   ```bash
   # Copy contents from database/schema.sql and run it
   ```
6. Update Railway backend with this DATABASE_URL

**C. Deploy Frontend to Vercel**

1. Go to [Vercel.com](https://vercel.com) and sign up
2. Click "New Project" → Import your GitHub repository
3. Configure:
   - Framework Preset: Vite
   - Root Directory: `apps/frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Environment Variables:
   ```
   VITE_API_URL=https://your-backend.railway.app/api
   ```
5. Deploy! You'll get: `https://your-app.vercel.app`

**D. Update CORS**

Go back to Railway and update:
```
CORS_ORIGINS=["https://your-app.vercel.app"]
```

### Option 2: Single Server Deployment (VPS)

**Requirements:**
- VPS (DigitalOcean, Linode, AWS EC2)
- Ubuntu 22.04+
- Domain name (optional)

**Setup Script:**

```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Install dependencies
sudo apt update
sudo apt install -y python3-pip nodejs npm nginx certbot python3-certbot-nginx

# 3. Clone repository
git clone https://github.com/HPagade/rohimaya-ai-eclipselink-product.git
cd rohimaya-ai-eclipselink-product

# 4. Install app dependencies
cd apps/backend && pip3 install -r requirements.txt && cd ../..
cd apps/frontend && npm install && cd ../..

# 5. Build frontend
cd apps/frontend && npm run build && cd ../..

# 6. Set up database
cd apps/backend && python3 init_db.py && cd ../..

# 7. Create systemd service for backend
sudo nano /etc/systemd/system/eclipselink-backend.service
```

**Backend Service File:**
```ini
[Unit]
Description=EclipseLink AI Backend
After=network.target

[Service]
User=your-user
WorkingDirectory=/home/your-user/rohimaya-ai-eclipselink-product/apps/backend
Environment="DATABASE_URL=sqlite:///./eclipselink.db"
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 4000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /home/your-user/rohimaya-ai-eclipselink-product/apps/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**Enable and Start:**
```bash
# Start backend
sudo systemctl enable eclipselink-backend
sudo systemctl start eclipselink-backend

# Configure nginx
sudo ln -s /etc/nginx/sites-available/eclipselink /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Get SSL certificate (if you have a domain)
sudo certbot --nginx -d your-domain.com
```

### Option 3: Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:3000
```

---

## 📱 Mobile & Responsive Testing

### The App is Fully Responsive!

**Breakpoints:**
- Mobile: 320px - 640px
- Tablet: 641px - 1024px
- Desktop: 1025px+

### Test Responsiveness:

**Browser DevTools:**
1. Open app in Chrome/Firefox
2. Press F12 (DevTools)
3. Click device icon (Ctrl+Shift+M)
4. Test different devices

**Real Device Testing:**

1. **Find your local IP:**
   ```bash
   # Mac/Linux
   ifconfig | grep "inet "

   # Windows
   ipconfig
   ```

2. **Start frontend on network:**
   ```bash
   cd apps/frontend
   npm run dev -- --host
   ```

3. **Access from phone:**
   ```
   http://YOUR-LOCAL-IP:3000
   ```

**Supported Devices:**
- ✅ iPhone (all models)
- ✅ Android phones
- ✅ iPads & tablets
- ✅ Desktop browsers
- ✅ ChromeOS

---

## 🤝 Team Collaboration Workflow

### Git Workflow

**For New Features:**
```bash
# 1. Pull latest changes
git pull origin main

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes

# 4. Commit
git add .
git commit -m "feat: your feature description"

# 5. Push
git push origin feature/your-feature-name

# 6. Create Pull Request on GitHub
```

**Branch Naming Convention:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring

### Code Review Process

1. Create Pull Request
2. Request review from team member
3. Address feedback
4. Merge to main after approval

### Deployment Process

**Development → Staging → Production**

1. **Development**: Test locally
2. **Staging**: Deploy to test environment
3. **Production**: Deploy after testing

---

## 🐛 Troubleshooting

### Backend Won't Start

**Issue**: `ModuleNotFoundError`
```bash
# Solution: Install dependencies
cd apps/backend
pip install -r requirements.txt
```

**Issue**: `Database not found`
```bash
# Solution: Initialize database
cd apps/backend
python3 init_db.py
```

**Issue**: `Port 4000 already in use`
```bash
# Solution: Kill process
# Mac/Linux
lsof -ti:4000 | xargs kill -9

# Windows
netstat -ano | findstr :4000
taskkill /PID <PID> /F
```

### Frontend Won't Start

**Issue**: `Cannot find module`
```bash
# Solution: Reinstall dependencies
cd apps/frontend
rm -rf node_modules package-lock.json
npm install
```

**Issue**: `API calls failing`
```bash
# Check .env file has:
VITE_API_URL=http://localhost:4000/api

# Restart frontend after changing .env
```

### Login/Register Not Working

**Issue**: CORS errors in browser console
```
# Solution: Update backend .env
CORS_ORIGINS='["http://localhost:3000","http://localhost:5173"]'
```

**Issue**: "Internal server error" on registration
```bash
# Check backend logs
# Make sure SHA-256 password hashing is working
# See STATUS-REPORT.md for bcrypt fix
```

### Database Issues

**Reset database:**
```bash
cd apps/backend
rm eclipselink.db
python3 init_db.py
```

**View database:**
```bash
cd apps/backend
sqlite3 eclipselink.db
.tables
SELECT * FROM users;
.quit
```

---

## 🔐 Security Best Practices

### For Production:

1. **Use Strong Secrets**
   ```bash
   # Generate secure secret
   openssl rand -hex 32
   ```

2. **Enable HTTPS**
   - Use Certbot for free SSL
   - Or use Cloudflare

3. **Set Secure Environment Variables**
   ```bash
   SECRET_KEY=<strong-random-key>
   DEBUG=false
   ENVIRONMENT=production
   ```

4. **Use PostgreSQL in Production**
   - SQLite is fine for development
   - Use Supabase/PostgreSQL for production

5. **Regular Updates**
   ```bash
   # Update dependencies
   npm update
   pip install --upgrade -r requirements.txt
   ```

---

## 📊 Monitoring & Maintenance

### Application Logs

**Backend:**
```bash
# View logs in production
journalctl -u eclipselink-backend -f
```

**Frontend:**
- Use Vercel/Netlify dashboard logs
- Or check browser console

### Database Backups

**Manual Backup:**
```bash
cd apps/backend
cp eclipselink.db eclipselink_backup_$(date +%Y%m%d).db
```

**Automated Backups (Cron):**
```bash
# Add to crontab
0 2 * * * cd /path/to/apps/backend && cp eclipselink.db backups/eclipselink_$(date +\%Y\%m\%d).db
```

### Health Checks

```bash
# Check backend
curl http://localhost:4000/health

# Check frontend
curl http://localhost:3000
```

---

## 📞 Support & Resources

### Documentation
- **API Docs**: http://localhost:4000/api/docs
- **README**: See README.md in project root
- **STATUS**: See STATUS-REPORT.md for current status

### Getting Help
- Check this guide first
- Review STATUS-REPORT.md
- Check GitHub Issues
- Contact: support@rohimaya.ai

---

## ✨ Features Checklist

✅ **Core Features Working:**
- User registration & login
- Patient management (CRUD)
- Handoff creation & management
- SBAR report structure
- Role-based access (15+ roles)
- Responsive design (mobile, tablet, desktop)
- API documentation

📋 **To Be Added (Optional):**
- Voice recording
- AI transcription (OpenAI Whisper)
- AI SBAR generation (Anthropic Claude)
- EHR integration
- Rewards system UI
- Advanced analytics

---

**🎉 You're Ready to Deploy!**

Follow this guide and your entire team will be up and running with EclipseLink AI in minutes!

For questions: Hannah Pagade (CEO) | Prasad Pagade (CTO) | Rohimaya Health AI
