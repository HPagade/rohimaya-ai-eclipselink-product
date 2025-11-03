# EclipseLink AI Marketing Website

Professional marketing website built with Astro and optimized for Cloudflare Pages deployment.

## 🚀 Features

- **Lightning Fast**: Static site generation with Astro
- **SEO Optimized**: Meta tags, Open Graph, semantic HTML
- **Responsive**: Mobile-first design with Tailwind CSS
- **Cloudflare Ready**: Optimized for Cloudflare Pages deployment
- **Zero Config**: Deploy in minutes

## 📦 What's Included

- **Landing Page**: Hero, features, pricing, demo request
- **Features Section**: 6 key features with descriptions
- **Pricing Page**: 3 pricing tiers (Pilot, Growth, Enterprise)
- **Demo Request Form**: Lead capture and contact form
- **Documentation Links**: Integration with main documentation
- **Cost Breakdown**: Transparent pricing display
- **Architecture Highlights**: Technology stack showcase

## 🛠️ Tech Stack

- **Framework**: Astro 4.0
- **Styling**: Tailwind CSS 3.4
- **Deployment**: Cloudflare Pages
- **Fonts**: Inter (Google Fonts)
- **Icons**: Heroicons (inline SVG)

## 📋 Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Cloudflare account (free tier works)

## 🚦 Quick Start

### 1. Install Dependencies

```bash
cd website
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

Visit: http://localhost:4321

### 3. Build for Production

```bash
npm run build
```

Output: `dist/` folder

### 4. Preview Production Build

```bash
npm run preview
```

## ☁️ Cloudflare Pages Deployment

### Option 1: Automatic Deployment (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add marketing website"
   git push
   ```

2. **Connect to Cloudflare Pages**
   - Go to https://dash.cloudflare.com
   - Navigate to **Pages** → **Create a project**
   - Connect your GitHub repository
   - Select `rohimaya-ai-eclipselink-product`

3. **Configure Build Settings**
   ```
   Framework preset: Astro
   Build command: cd website && npm install && npm run build
   Build output directory: website/dist
   Root directory: /
   Node version: 18
   ```

4. **Deploy**
   - Click "Save and Deploy"
   - Your site will be live in ~2 minutes
   - Custom domain: Add in Pages settings

### Option 2: Manual Deployment via Wrangler

1. **Install Wrangler**
   ```bash
   npm install -g wrangler
   ```

2. **Login to Cloudflare**
   ```bash
   wrangler login
   ```

3. **Deploy**
   ```bash
   cd website
   npm run build
   wrangler pages deploy dist --project-name=eclipselink-ai
   ```

## 🧪 Testing (3x Verification)

### Test 1: Local Development
```bash
npm run dev
# ✓ Check all links work
# ✓ Test mobile responsiveness (DevTools)
# ✓ Verify form submission (console logs)
# ✓ Test smooth scrolling to anchors
```

### Test 2: Production Build
```bash
npm run build
npm run preview
# ✓ Check build errors (none expected)
# ✓ Verify asset optimization
# ✓ Test loading speed
# ✓ Validate all pages render correctly
```

### Test 3: Cloudflare Deployment
```bash
# After deploying to Cloudflare
# ✓ Test live site on actual domain
# ✓ Check SSL certificate (auto-enabled)
# ✓ Verify CDN caching (fast global load)
# ✓ Test from multiple devices/locations
```

## 📝 Customization

### Update Content

**Site Title & Description**: `src/layouts/Layout.astro`
```astro
<Layout
  title="Your Custom Title"
  description="Your custom description"
/>
```

**Domain/URL**: `astro.config.mjs`
```js
export default defineConfig({
  site: 'https://yourdomain.com',
  // ...
});
```

### Update Pricing

Edit `src/pages/index.astro` - Pricing Section (lines ~400-550):
```astro
<div class="text-4xl font-bold mb-2">
  $29<span class="text-xl text-gray-500">/user/mo</span>
</div>
```

### Update Colors

Edit `tailwind.config.mjs`:
```js
colors: {
  primary: {
    500: '#0ea5e9', // Change this
    600: '#0284c7', // and this
    // ...
  }
}
```

### Add New Pages

```bash
# Create new page
touch src/pages/about.astro

# Will be accessible at: /about
```

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `astro.config.mjs` | Astro configuration |
| `tailwind.config.mjs` | Tailwind CSS customization |
| `tsconfig.json` | TypeScript configuration |
| `package.json` | Dependencies and scripts |
| `.cloudflarerc` | Cloudflare Pages settings |

## 📊 Performance

- **Lighthouse Score**: 100/100 (expected)
- **First Contentful Paint**: < 0.5s
- **Time to Interactive**: < 1s
- **Total Size**: < 100KB (gzipped)

## 🌐 SEO Features

- ✓ Semantic HTML5 elements
- ✓ Open Graph meta tags
- ✓ Twitter Card meta tags
- ✓ Structured data ready
- ✓ Sitemap generation (auto)
- ✓ robots.txt (auto)
- ✓ Fast loading (Core Web Vitals)

## 🔒 Security

- ✓ No client-side secrets
- ✓ Static site (no server vulnerabilities)
- ✓ HTTPS only (Cloudflare auto)
- ✓ Content Security Policy ready
- ✓ No external dependencies at runtime

## 🎨 Design System

**Colors**:
- Primary Blue: #0ea5e9 (clinical technology)
- Medical Green: #22c55e (healthcare)
- Gray scale: Tailwind default

**Typography**:
- Font: Inter (Google Fonts)
- Headings: 700-900 weight
- Body: 400-500 weight

**Spacing**:
- Container: max-w-6xl
- Padding: px-6 (mobile), px-0 (container handles)
- Sections: py-20 standard

## 📱 Responsive Breakpoints

```css
sm: 640px   /* Mobile landscape */
md: 768px   /* Tablet */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
```

## 🐛 Troubleshooting

### Build Fails
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Styles Not Applying
```bash
# Rebuild Tailwind
npx tailwindcss -i ./src/styles/global.css -o ./dist/assets/output.css
```

### 404 on Deployment
- Check `astro.config.mjs` - ensure `output: 'static'`
- Verify build output directory is `dist`
- Clear Cloudflare cache

## 🔗 Links

- **Production Site**: https://eclipselink.ai (set your custom domain)
- **Cloudflare Dashboard**: https://dash.cloudflare.com
- **Astro Docs**: https://docs.astro.build
- **Tailwind Docs**: https://tailwindcss.com/docs

## 📞 Support

For questions about the marketing website:
1. Check the main project README
2. Review `ERROR-REPORT-AND-FIXES.md` in root
3. See `COMPLETE-DEPLOYMENT-GUIDE.md` for product deployment

## 📄 License

Same as main EclipseLink AI project.

---

**Status**: Production Ready ✅
**Last Updated**: November 2024
**Deployment**: Cloudflare Pages
