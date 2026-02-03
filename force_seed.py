#!/usr/bin/env python3
"""
Force reseed script - adds sample data even if database has existing content
"""
import os
import sys
from news_app import create_app
from news_app.models.db import db
from news_app.services.category_service import create_category, list_categories
from news_app.services.article_service import create_article, list_articles

def force_seed():
    """Force seed sample data"""
    app = create_app()
    
    with app.app_context():
        print("🌱 Force seeding database...")
        
        # Get existing categories
        existing_cats = list_categories()
        cat_names = [cat.name for cat in existing_cats]
        
        # Add missing categories
        required_cats = [
            ('Technology', 'Latest technology news and updates'),
            ('World', 'Global news and international affairs'),
            ('Local', 'Local community news and events'),
            ('Business', 'Business and financial news'),
            ('Sports', 'Sports news and updates'),
            ('Entertainment', 'Movies, music, and celebrity news')
        ]
        
        for cat_name, cat_desc in required_cats:
            if cat_name not in cat_names:
                create_category(cat_name, cat_desc)
                print(f"✅ Created category: {cat_name}")
        
        # Get updated categories
        categories = list_categories()
        cat_dict = {cat.name: cat.id for cat in categories}
        
        # Check if we need sample articles
        existing_articles = list_articles()
        sample_titles = [
            'Welcome to Our News Platform',
            'Latest Technology Trends 2024',
            'Global Economic Outlook',
            'Community Events This Month'
        ]
        
        existing_titles = [art.title for art in existing_articles]
        
        # Add sample articles if they don't exist
        sample_articles = [
            {
                'title': 'Welcome to Our News Platform',
                'content': 'This is your comprehensive news management system. You can create, edit, and manage articles across different categories with media upload support.',
                'author': 'Admin',
                'category_id': cat_dict.get('Local')
            },
            {
                'title': 'Latest Technology Trends 2024',
                'content': 'Exploring the cutting-edge technology trends that are shaping our future. From AI advancements to sustainable tech solutions with media integration.',
                'author': 'Tech Editor',
                'category_id': cat_dict.get('Technology')
            },
            {
                'title': 'Global Economic Outlook',
                'content': 'An analysis of current global economic conditions and future projections for businesses worldwide. Categories help organize content effectively.',
                'author': 'Business Analyst',
                'category_id': cat_dict.get('World')
            },
            {
                'title': 'Community Events This Month',
                'content': 'Stay updated with local community events, festivals, and activities. Media management makes sharing event photos easy.',
                'author': 'Community Manager',
                'category_id': cat_dict.get('Local')
            }
        ]
        
        for article_data in sample_articles:
            if article_data['title'] not in existing_titles:
                create_article(
                    title=article_data['title'],
                    content=article_data['content'],
                    category_id=article_data['category_id'],
                    author=article_data['author']
                )
                print(f"✅ Created article: {article_data['title']}")
        
        # Final count
        final_articles = list_articles()
        final_categories = list_categories()
        print(f"🎉 Force seed complete! Database now has {len(final_articles)} articles and {len(final_categories)} categories")

if __name__ == '__main__':
    try:
        force_seed()
        print("✅ Force seed completed successfully")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Force seed failed: {str(e)}")
        sys.exit(1)