# TODO: Fix Gunicorn import error (app:app naming conflict)

## Issue
There's a naming conflict between `app.py` (file) and `app/` (directory). When Gunicorn runs `gunicorn app:app`, Python imports the `app/` directory as a package instead of the `app.py` file.

## Plan

### Step 1: Rename app/ directory to news_app/
- [ ] Rename `app/` → `news_app/` to avoid naming conflict

### Step 2: Update app.py imports
- [ ] Change `from app import create_app` → `from news_app import create_app`

### Step 3: Update internal imports in news_app/
- [ ] Update `news_app/__init__.py` - change absolute imports to relative
- [ ] Update `news_app/services/article_service.py`
- [ ] Update `news_app/services/category_service.py`
- [ ] Update `news_app/services/media_service.py`
- [ ] Update `news_app/controllers/article_controller.py`
- [ ] Update `news_app/controllers/category_controller.py`
- [ ] Update `news_app/controllers/admin_controller.py`
- [ ] Update `news_app/controllers/api_controller.py`
- [ ] Update `news_app/controllers/media_controller.py`
- [ ] Update `news_app/models/article.py`
- [ ] Update `news_app/models/category.py`
- [ ] Update `news_app/models/media.py`
- [ ] Update `news_app/seed.py`

### Step 4: Update external file imports
- [ ] Update `test_database.py`
- [ ] Update `tests/test_api.py`
- [ ] Update `tests/test_services.py`
- [ ] Update `verify_health.py`

### Step 5: Update configuration files
- [ ] Update `Procfile` to use `news_app:app`
- [ ] Update `render.yaml` to use `news_app:app`

### Step 6: Test
- [ ] Verify the application runs correctly

