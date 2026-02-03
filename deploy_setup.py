#!/usr/bin/env python3
"""
Deployment setup script for Render.com
Ensures database is initialized and seeded with articles, categories, and media setup
"""
import os
import sys
from news_app import create_app
from news_app.models.db import db
from news_app.services.category_service import create_category, list_categories
from news_app.services.article_service import create_article, list_articles
from news_app.services.media_service import list_media

def setup_upload_directory():
    """Ensure upload directory exists with proper permissions"""
    upload_dirs = [
        'static/uploads',
        '/workspaces/News/static/uploads'  # For Render.com disk mount
    ]
    
    for upload_dir in upload_dirs:
        try:
            os.makedirs(upload_dir, exist_ok=True)
            # Create .gitkeep file to ensure directory is tracked
            gitkeep_path = os.path.join(upload_dir, '.gitkeep')
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, 'w') as f:
                    f.write('# Keep this directory in git\n')
            print(f"✅ Upload directory ready: {upload_dir}")
        except Exception as e:
            print(f"⚠️  Could not create upload directory {upload_dir}: {e}")

def setup_database():
    """Initialize database and seed with sample data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Setup upload directories
        setup_upload_directory()
        
        # Check if categories exist
        existing_cats = list_categories()
        if not existing_cats:
            print("🌱 Seeding categories...")
            tech = create_category('Technology', 'Latest technology news and updates')
            world = create_category('World', 'Global news and international affairs')
            local = create_category('Local', 'Local community news and events')
            business = create_category('Business', 'Business and financial news')
            sports = create_category('Sports', 'Sports news and updates')
            entertainment = create_category('Entertainment', 'Movies, music, and celebrity news')
            print(f"✅ Created {len(list_categories())} categories")
        else:
            print(f"✅ Found {len(existing_cats)} existing categories")
        
        # Check if articles exist
        existing_articles = list_articles()
        if not existing_articles:
            print("🌱 Seeding sample articles...")
            categories = list_categories()
            cat_dict = {cat.name: cat.id for cat in categories}
            
            # Create sample articles
            articles_data = [
                {
                    'title': 'Welcome to Our News Platform',
                    'content': 'This is your comprehensive news management system. You can create, edit, and manage articles across different categories. The platform supports both internal articles and live news integration with media upload capabilities.',
                    'author': 'Admin',
                    'category_id': cat_dict.get('Local')
                },
                {
                    'title': 'Latest Technology Trends 2024',
                    'content': 'Exploring the cutting-edge technology trends that are shaping our future. From AI advancements to sustainable tech solutions, discover what\'s driving innovation in 2024. Upload images and media to enhance your articles.',
                    'author': 'Tech Editor',
                    'category_id': cat_dict.get('Technology')
                },
                {
                    'title': 'Global Economic Outlook',
                    'content': 'An analysis of current global economic conditions and future projections. Understanding market trends and their impact on businesses worldwide. Categories help organize content effectively.',
                    'author': 'Business Analyst',
                    'category_id': cat_dict.get('Business')
                },
                {
                    'title': 'Community Events This Month',
                    'content': 'Stay updated with local community events, festivals, and activities happening in your area. Join us for various cultural and social gatherings. Media management makes sharing event photos easy.',
                    'author': 'Community Manager',
                    'category_id': cat_dict.get('Local')
                }
            ]
            
            for article_data in articles_data:
                create_article(
                    title=article_data['title'],
                    content=article_data['content'],
                    category_id=article_data['category_id'],
                    author=article_data['author']
                )
            
            print(f"✅ Created {len(articles_data)} sample articles")
        else:
            print(f"✅ Found {len(existing_articles)} existing articles")
        
        # Check media setup
        existing_media = list_media()
        print(f"✅ Media system ready - {len(existing_media)} files in database")
        
        # Final verification
        final_articles = list_articles()
        final_categories = list_categories()
        final_media = list_media()
        print(f"🎉 Setup complete! Database contains {len(final_articles)} articles, {len(final_categories)} categories, and {len(final_media)} media files")
        
        return True

if __name__ == '__main__':
    try:
        setup_database()
        print("✅ Deployment setup completed successfully")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Deployment setup failed: {str(e)}")
        sys.exit(1)