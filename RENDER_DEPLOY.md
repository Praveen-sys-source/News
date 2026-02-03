# Render Deployment Guide

## Quick Deployment (Recommended)

### Option 1: Using Render Blueprint (Auto-deploy)

1. Push your code to a GitHub repository

2. Go to [Render Dashboard](https://dashboard.render.com)

3. Click "New +" and select "Blueprint"

4. Select your repository

5. Render will detect the `render.yaml` file and configure:
   - Web Service: Your Flask app
   - PostgreSQL Database: news-db
   - Environment variables will be automatically configured

6. Click "Apply"

### Option 2: Manual Deployment

#### Step 1: Create a PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)

2. Click "New +" and select "PostgreSQL"

3. Configure:
   - Name: `news-db`
   - Database Name: `news`
   - User: `news`
   - Plan: `Free`

4. Click "Create Database"

5. Wait for the database to be provisioned (green status)

6. Copy the "External Database URL" - you'll need it later

#### Step 2: Create a Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)

2. Click "New +" and select "Web Service"

3. Select your repository

4. Configure:
   - Name: `news-app`
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --timeout 120 --workers 1 --bind 0.0.0.0:$PORT`

5. Add Environment Variables:
   - `DATABASE_URL`: (paste the External Database URL from Step 1)
   - `SECRET_KEY`: (generate a secure random key, e.g., `openssl rand -base64 32`)
   - `NEWS_API_KEY`: (get from https://newsapi.org/register)
   - `FLASK_ENV`: `production`

6. Add Disk (optional but recommended for file uploads):
   - Mount Path: `/workspaces/News/static/uploads`
   - Size: `256 MB`

7. Click "Create Web Service"

#### Step 3: Configure NewsAPI Key as Secret

1. Go to [Render Dashboard](https://dashboard.render.com)

2. Click "New +" and select "Secret"

3. Configure:
   - Name: `news-api-key`
   - Value: (your NewsAPI key)

4. Click "Create Secret"

5. Go to your web service settings

6. Under "Secrets", add the `news-api-key` secret

## After Deployment

### Initialize Database

The database tables will be automatically created when the app first starts. However, if you want to seed initial data:

1. Go to your web service on Render

2. Click "Shell" to open a shell

3. Run:
   ```bash
   python -c "from app import create_app; from app.seed import seed_database; app = create_app(); with app.app_context(): seed_database()"
   ```

### Verify Health

Visit `https://your-app-name.onrender.com/health` to verify the app is running.

### Troubleshooting

#### Database Connection Issues

If you see database errors:

1. Check that the `DATABASE_URL` is correctly set in environment variables
2. Ensure the database is in the same region as your web service
3. Check the logs for specific error messages

#### Static Files Not Loading

If CSS/JS files are not loading:

1. Ensure the `static` folder is properly configured
2. Check that the mount path for uploads is correct if using file uploads

#### Application Errors

Check the logs in Render Dashboard:
1. Go to your web service
2. Click "Logs" tab
3. Look for error messages

#### Upgrade from SQLite to PostgreSQL

If you were using SQLite locally and want to migrate:

1. Export your local database:
   ```bash
   sqlite3 instance/news.db .dump > backup.sql
   ```

2. Import to PostgreSQL on Render:
   ```bash
   psql $DATABASE_URL < backup.sql
   ```

   Note: You may need to adjust the SQL syntax as PostgreSQL and SQLite have some differences.

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string (auto-set by Render) |
| `SECRET_KEY` | Yes | Secret key for session security |
| `NEWS_API_KEY` | Yes | API key for NewsAPI integration |
| `FLASK_ENV` | No | Set to `production` for production mode |

## Scaling

### Free Tier Limitations

- Web service sleeps after 15 minutes of inactivity
- Database has storage limits
- No automatic SSL (Render provides this automatically)

### Upgrading

To upgrade from free tier:
1. Go to your service settings
2. Change the plan to "Starter" or "Pro"
3. This removes the idle timeout

## Security Considerations

1. **Never commit `.env` files** to version control
2. **Use Render Secrets** for sensitive keys like `NEWS_API_KEY`
3. **Enable HTTPS** (Render does this automatically)
4. **Set `FLASK_ENV=production`** for production mode

## Local Development After Deployment

To work locally with the production database:

1. Set the environment variables:
   ```bash
   export DATABASE_URL="postgresql://..."
   export SECRET_KEY="..."
   export NEWS_API_KEY="..."
   ```

2. Run the app locally:
   ```bash
   python app.py
   ```

