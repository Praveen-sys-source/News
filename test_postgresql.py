#!/usr/bin/env python3
"""
Test PostgreSQL connection for Render.com deployment
"""
import os
import sys
from news_app import create_app
from news_app.models.db import db

def test_postgresql_connection():
    """Test PostgreSQL database connection"""
    app = create_app()
    
    with app.app_context():
        try:
            # Test database connection (SQLAlchemy 2.0+ compatible)
            with db.engine.connect() as connection:
                connection.execute(db.text('SELECT 1'))
            print("✅ Database connection successful")
            
            # Test table creation
            db.create_all()
            print("✅ Database tables created/verified")
            
            # Get database info
            database_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if 'postgresql' in database_url:
                print("✅ Using PostgreSQL database")
                print(f"   Database: {database_url.split('/')[-1] if '/' in database_url else 'Unknown'}")
            else:
                print("ℹ️  Using SQLite database (development mode)")
            
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            return False

if __name__ == '__main__':
    try:
        success = test_postgresql_connection()
        if success:
            print("\n🎉 Database connection test passed!")
            sys.exit(0)
        else:
            print("\n❌ Database connection test failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {str(e)}")
        sys.exit(1)