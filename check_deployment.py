#!/usr/bin/env python3
"""
Startup script to verify deployment configuration
Run this before starting the app to catch configuration issues
"""

import os
import sys

def check_environment():
    """Check environment variables and configuration"""
    print("=" * 60)
    print("Deployment Configuration Check")
    print("=" * 60)
    
    # Check Python version
    print(f"\nPython Version: {sys.version}")
    
    # Check environment variables
    print("\nEnvironment Variables:")
    env_vars = {
        'DATABASE_URL': os.getenv('DATABASE_URL', 'Not set (will use SQLite)'),
        'SECRET_KEY': 'Set' if os.getenv('SECRET_KEY') else 'Not set (will use default)',
        'PORT': os.getenv('PORT', 'Not set (will use 8080)'),
    }
    
    for key, value in env_vars.items():
        print(f"  {key}: {value}")
    
    # Check if required directories exist
    print("\nDirectory Structure:")
    dirs_to_check = [
        'news_app',
        'news_app/Frontend',
        'news_app/Frontend/static',
        'news_app/Frontend/static/css',
        'news_app/Frontend/static/js',
        'news_app/Frontend/static/uploads',
        'news_app/Frontend/templates',
        'news_app/Backend',
        'news_app/Backend/controllers',
        'news_app/Backend/models',
        'news_app/Backend/services',
    ]
    
    all_exist = True
    for dir_path in dirs_to_check:
        exists = os.path.isdir(dir_path)
        status = "✓" if exists else "✗"
        print(f"  {status} {dir_path}")
        if not exists:
            all_exist = False
    
    # Check if critical files exist
    print("\nCritical Files:")
    files_to_check = [
        'app.py',
        'news_app/__init__.py',
        'news_app/Frontend/static/css/style.css',
        'news_app/Frontend/static/js/main.js',
        'news_app/Frontend/templates/layout.html',
        'news_app/Frontend/templates/index.html',
        'Procfile',
        'requirements.txt',
    ]
    
    for file_path in files_to_check:
        exists = os.path.isfile(file_path)
        status = "✓" if exists else "✗"
        print(f"  {status} {file_path}")
        if not exists:
            all_exist = False
    
    # Try to import the app
    print("\nApp Import Test:")
    try:
        from news_app import create_app
        app = create_app()
        print("  ✓ App imported and created successfully")
        
        # Test a simple route
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("  ✓ Home route works (200 OK)")
            else:
                print(f"  ✗ Home route failed ({response.status_code})")
                all_exist = False
                
    except Exception as e:
        print(f"  ✗ Failed to import app: {e}")
        all_exist = False
    
    print("\n" + "=" * 60)
    if all_exist:
        print("✓ All checks passed! Ready for deployment.")
    else:
        print("✗ Some checks failed. Fix issues before deploying.")
    print("=" * 60)
    
    return 0 if all_exist else 1

if __name__ == '__main__':
    sys.exit(check_environment())
