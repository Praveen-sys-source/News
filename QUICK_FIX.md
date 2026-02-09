# Quick Fix Reference

## What Was Fixed

**Problem:** 500 Internal Server Error - Frontend not connecting to backend

**Solution:** Fixed Procfile to use correct app reference

## The Fix

**File:** `Procfile`

```diff
- web: gunicorn news_app:app --timeout 120 --workers 1 --bind 0.0.0.0:$PORT
+ web: gunicorn app:app --timeout 120 --workers 1 --bind 0.0.0.0:$PORT
```

## Why This Works

- `app.py` is the entry point that creates the Flask app
- It imports `create_app()` from the `news_app` package
- Gunicorn needs to reference `app:app` (module:variable)
- The first `app` = `app.py` file
- The second `app` = Flask app instance in that file

## Verify It Works

```bash
# Test locally
python test_app.py

# Check deployment config
python check_deployment.py
```

## Deploy

Your app is now ready to deploy. The Procfile is correct and all routes work.

## Status: ✓ FIXED

All tests pass:
- ✓ Home page loads
- ✓ Articles page loads
- ✓ Static files (CSS/JS) load
- ✓ Database works
- ✓ All routes return 200 OK
