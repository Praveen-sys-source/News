#!/usr/bin/env python3
"""
Test script to verify SQLite database functionality
"""
import sys
from app import create_app, db
from app.models.article import Article
from app.models.category import Category

def test_database():
    """Run comprehensive database tests"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("SQLite Database Test Suite")
        print("="*60)
        
        # Test 1: Connection
        print("\n[TEST 1] Database Connection")
        try:
            from sqlalchemy import text
            db.session.execute(text("SELECT 1"))
            print("✓ Connected to SQLite database successfully")
        except Exception as e:
            print(f"✗ Failed to connect: {e}")
            return False
        
        # Test 2: Tables
        print("\n[TEST 2] Database Tables")
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"✓ Found {len(tables)} tables: {tables}")
        
        # Test 3: Categories
        print("\n[TEST 3] Categories")
        cats = Category.query.all()
        print(f"✓ Found {len(cats)} categories:")
        for cat in cats:
            articles_count = len(cat.articles) if cat.articles else 0
            print(f"  - {cat.name} ({articles_count} articles)")
        
        # Test 4: Articles
        print("\n[TEST 4] Articles")
        arts = Article.query.all()
        print(f"✓ Found {len(arts)} articles:")
        for art in arts:
            cat_name = art.category.name if art.category else "No category"
            print(f"  - {art.title} ({art.author}) - {cat_name}")
        
        # Test 5: Create new article
        print("\n[TEST 5] Create New Article")
        try:
            tech_cat = Category.query.filter_by(name='Technology').first()
            new_art = Article(
                title='Database Test Article',
                content='This article was created by the database test script',
                author='Test Script',
                category_id=tech_cat.id if tech_cat else None
            )
            db.session.add(new_art)
            db.session.commit()
            print(f"✓ Created article: '{new_art.title}' (ID: {new_art.id})")
        except Exception as e:
            print(f"✗ Failed to create article: {e}")
            db.session.rollback()
            return False
        
        # Test 6: Query new article
        print("\n[TEST 6] Query New Article")
        test_art = Article.query.filter_by(title='Database Test Article').first()
        if test_art:
            print(f"✓ Retrieved article: '{test_art.title}' (ID: {test_art.id})")
        else:
            print("✗ Failed to retrieve new article")
            return False
        
        # Test 7: Update article
        print("\n[TEST 7] Update Article")
        try:
            test_art.content = 'Updated content from test script'
            db.session.commit()
            updated = Article.query.get(test_art.id)
            print(f"✓ Updated article content")
        except Exception as e:
            print(f"✗ Failed to update: {e}")
            return False
        
        # Final Summary
        print("\n" + "="*60)
        print("Database Summary")
        print("="*60)
        final_cat_count = Category.query.count()
        final_art_count = Article.query.count()
        print(f"Total Categories: {final_cat_count}")
        print(f"Total Articles: {final_art_count}")
        print(f"Database File: /workspaces/News/instance/app.db")
        print("\n✓ SQLite Database is fully functional!")
        print("="*60 + "\n")
        
        return True

if __name__ == '__main__':
    success = test_database()
    sys.exit(0 if success else 1)
