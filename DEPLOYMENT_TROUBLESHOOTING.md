# Deployment Troubleshooting Guide

## Quick Fix Summary

The main issue was in the `Procfile`. It has been fixed:

**Before (WRONG):**
```
web: gunicorn news_app:app --timeout 120 --workers 1 --bind 0.0.0.0:$PORT
```

**After (CORRECT):**
```
web: gunicorn app:app --timeout 120 --workers 1 --bind 0.0.0.0:$PORT
```

## Verification Steps

Run these commands to verify everything works:

```bash
# 1. Check deployment configuration
python check_deployment.py

# 2. Test the app locally
python test_app.py

# 3. Test with gunicorn (production server)
gunicorn app:app --bind 0.0.0.0:8080 --timeout 120
```

## Common Issues and Solutions

### 1. 500 Internal Server Error

**Cause:** Usually due to incorrect Procfile or missing dependencies

**Solution:**
- Verify Procfile uses `app:app` not `news_app:app`
- Check all dependencies are in requirements.txt
- Verify DATABASE_URL is set correctly for production

### 2. Static Files Not Loading

**Cause:** Incorrect static file paths or MIME types

**Solution:**
- The app already has custom static file handlers in `news_app/__init__.py`
- Verify static files exist in `news_app/Frontend/static/`
- Check browser console for 404 errors

### 3. Database Connection Issues

**For SQLite (Development):**
```python
# Automatically uses: sqlite:///news.db
```

**For PostgreSQL (Production):**
```bash
# Set environment variable:
export DATABASE_URL="postgresql://user:pass@host:port/dbname"
```

### 4. Template Not Found Errors

**Cause:** Incorrect template directory configuration

**Solution:**
- Templates are in `news_app/Frontend/templates/`
- This is configured in `news_app/__init__.py`
- Verify all template files exist

## Environment Variables

Required for production:

```bash
# Database (PostgreSQL for production)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Secret key for sessions
SECRET_KEY=your-secret-key-here

# Port (usually set by hosting platform)
PORT=8080
```

## Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Or with gunicorn
gunicorn app:app --bind 0.0.0.0:8080
```

## Deployment Checklist

- [x] Procfile uses correct app reference (`app:app`)
- [x] All dependencies in requirements.txt
- [x] Static files in correct location
- [x] Templates in correct location
- [x] Database configuration working
- [x] Environment variables set
- [x] App starts without errors

## File Structure

```
News/
├── app.py                          # Main entry point (creates app)
├── Procfile                        # Deployment config (FIXED)
├── requirements.txt                # Dependencies
├── news_app/
│   ├── __init__.py                # App factory (create_app)
│   ├── Frontend/
│   │   ├── static/                # CSS, JS, uploads
│   │   └── templates/             # HTML templates
│   └── Backend/
│       ├── controllers/           # Route handlers
│       ├── models/                # Database models
│       └── services/              # Business logic
```

## Support

If issues persist:

1. Check application logs for specific errors
2. Run `python check_deployment.py` to verify configuration
3. Test locally with `python test_app.py`
4. Verify all environment variables are set correctly
