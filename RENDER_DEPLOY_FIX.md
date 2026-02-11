# CRITICAL: Render Deployment Instructions

## The Problem
Render is using CACHED old code. Even though we pushed the fix, Render hasn't rebuilt with the new code.

## Solution: Force Clean Deploy

### Step 1: Go to Render Dashboard
https://dashboard.render.com

### Step 2: Select Your Service
Click on "news-app" (or whatever your service is named)

### Step 3: Manual Deploy with Cache Clear
1. Click the "Manual Deploy" button (top right)
2. **IMPORTANT**: Select "Clear build cache & deploy" from the dropdown
3. Wait for deployment to complete (5-10 minutes)

### Step 4: Verify Deployment
After deployment completes, check:
- Visit: https://your-app.onrender.com/manage
- Visit: https://your-app.onrender.com/bookmarks
- Visit: https://your-app.onrender.com/api/articles

All should work without 500 errors.

## Why This Happens
Render caches:
- Python packages
- Built files
- Sometimes even source code

"Clear build cache & deploy" forces Render to:
1. Delete all cached files
2. Pull fresh code from GitHub
3. Reinstall all dependencies
4. Build from scratch

## Alternative: Trigger Redeploy via Git
If manual deploy doesn't work:

```bash
# Make a small change to force redeploy
echo "# Force redeploy" >> README.md
git add README.md
git commit -m "Force Render redeploy"
git push origin main
```

Then in Render, still select "Clear build cache & deploy"

## Verification Commands
After deployment, check logs in Render dashboard for:
- ✅ "Database tables initialized successfully"
- ✅ No import errors
- ✅ No "str object has no attribute" errors

## Current Code Status
✅ Local testing: ALL ROUTES WORK (200 OK)
✅ Git: Latest code pushed
❌ Render: Using old cached code

**Action Required: Clear build cache & deploy in Render Dashboard**
