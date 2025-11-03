# Security Advisory: Development Dependencies

## Current Status

### ✅ Production is Secure

The repository has a **development-only** vulnerability in `esbuild` (used by Vite dev server). This does **NOT** affect production deployments.

### Vulnerability Details

- **Package:** esbuild <=0.24.2
- **Severity:** Moderate
- **CVE:** [GHSA-67mh-4wv8-2f99](https://github.com/advisories/GHSA-67mh-4wv8-2f99)
- **Description:** "esbuild enables any website to send any requests to the development server and read the response"
- **Impact:** Development server only
- **Production Impact:** None

### Why This Doesn't Affect Production

1. **Production uses built static files** - The Vite development server (which uses esbuild) is never used in production
2. **Docker production builds** - Use multi-stage builds that don't include development dependencies
3. **Frontend deployed as static assets** - Served via nginx, no development server involved
4. **Backend is Python** - Not affected by Node.js development dependencies

### Fix Options

#### Option 1: Accept Risk (Recommended)
- Development-only vulnerability
- Developers should only run dev server in trusted environments
- No production impact
- Wait for Vite to update to esbuild 0.24.3+ in stable release

#### Option 2: Force Update (Breaking Changes)
```bash
npm audit fix --force
```
⚠️ **Warning:** This will update Vite to v7.x which may have breaking changes

#### Option 3: Use Alternative Dev Server
```bash
# Use Vite preview instead of dev for testing
npm run build
npm run preview
```

### Development Best Practices

To minimize risk during development:

1. **Only run dev server on localhost**
   ```bash
   # Good
   npm run dev
   
   # Avoid
   npm run dev -- --host 0.0.0.0
   ```

2. **Use firewall rules** - Block external access to port 5173 (Vite dev server)

3. **Don't expose dev server to internet** - Use SSH tunnels for remote development

4. **Use production builds for demos** - Use `npm run build && npm run preview` instead of dev server

### Production Deployment Verification

Verify that production doesn't use the vulnerable package:

```bash
# Frontend production Dockerfile doesn't include dev dependencies
grep -A 5 "npm ci" apps/frontend/Dockerfile
# Should see: npm ci --only=production

# Check production build
docker build -f apps/frontend/Dockerfile --target production -t test-frontend .
docker run test-frontend ls -la node_modules/
# Should not contain esbuild (only in devDependencies)
```

### Timeline

- **Immediate:** No action required for production deployments
- **Short-term:** Monitor Vite releases for stable esbuild update
- **Long-term:** Update Vite when they release stable version with esbuild 0.24.3+

### References

- [GitHub Advisory Database - GHSA-67mh-4wv8-2f99](https://github.com/advisories/GHSA-67mh-4wv8-2f99)
- [esbuild Release Notes](https://github.com/evanw/esbuild/releases)
- [Vite Issue Tracker](https://github.com/vitejs/vite/issues)

---

**Last Updated:** November 2024  
**Next Review:** When Vite releases stable update  
**Status:** Acknowledged, No Action Required for Production
