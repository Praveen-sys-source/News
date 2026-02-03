#!/usr/bin/env python3
"""
Verification script for complete news management system
Tests articles, categories, and media functionality
"""
import os
import sys
from news_app import create_app
from news_app.services.article_service import list_articles
from news_app.services.category_service import list_categories
from news_app.services.media_service import list_media

def verify_system():
    """Verify all management systems are working"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Verifying News Management System...")
        
        # Check articles
        articles = list_articles()
        print(f"📰 Articles: {len(articles)} found")
        for article in articles[:3]:  # Show first 3
            print(f"   - {article.title} (by {article.author})")
        
        # Check categories
        categories = list_categories()
        print(f"📂 Categories: {len(categories)} found")
        for category in categories:
            print(f"   - {category.name}: {category.description or 'No description'}")
        
        # Check media
        media_files = list_media()
        print(f"🖼️  Media Files: {len(media_files)} found")
        for media in media_files[:3]:  # Show first 3
            print(f"   - {media.original_name} ({media.file_type})")
        
        # Check upload directory
        upload_dir = 'static/uploads'
        if os.path.exists(upload_dir):
            files = os.listdir(upload_dir)
            actual_files = [f for f in files if not f.startswith('.')]
            print(f"📁 Upload Directory: {len(actual_files)} physical files")
        else:
            print("❌ Upload directory not found")
        
        print(f"\n✅ System Verification Complete!")
        print(f"   📰 {len(articles)} articles ready")
        print(f"   📂 {len(categories)} categories ready") 
        print(f"   🖼️  {len(media_files)} media files ready")
        
        return len(articles) > 0 and len(categories) > 0

if __name__ == '__main__':
    try:
        success = verify_system()
        if success:
            print("\n🎉 All management systems verified successfully!")
            sys.exit(0)
        else:
            print("\n❌ System verification failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Verification failed: {str(e)}")
        sys.exit(1)