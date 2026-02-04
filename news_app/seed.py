from .models.db import db
from .models.article import Article
from .models.category import Category
from .services.category_service import create_category, list_categories
from .services.article_service import create_article, list_articles
from .services.media_service import list_media
from flask import Flask
import os

def seed_data(app=None):
    """
    Seed the database with initial data if it doesn't exist.
    
    This function is idempotent - running it multiple times won't create duplicates.
    It should be called during app initialization to ensure data exists.
    """
    if app is None:
        app = create_app()
    
    with app.app_context():
        try:
            # Check if data already exists
            existing_cats = list_categories()
            existing_articles = list_articles()
            
            if existing_cats and existing_articles:
                print(f'[INFO] Database already seeded with {len(existing_cats)} categories and {len(existing_articles)} articles. Skipping seed.')
                return True
            
            print('[INFO] Database is empty. Seeding initial data...')
            
            # Ensure upload directory exists
            upload_dir = 'static/uploads'
            os.makedirs(upload_dir, exist_ok=True)
            gitkeep_path = os.path.join(upload_dir, '.gitkeep')
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, 'w') as f:
                    f.write('# Keep this directory in git\n')
            
            # Create sample categories
            categories_to_create = [
                ('Technology', 'Latest technology news and updates'),
                ('World', 'Global news and international affairs'),
                ('Local', 'Local community news and events'),
                ('Business', 'Business and financial news'),
                ('Sports', 'Sports news and updates'),
                ('Entertainment', 'Movies, music, and celebrity news')
            ]
            
            cat_map = {}
            for name, desc in categories_to_create:
                # Check if category already exists
                existing = next((c for c in existing_cats if c.name == name), None)
                if existing:
                    cat_map[name] = existing
                else:
                    cat = create_category(name, desc)
                    cat_map[name] = cat
                    print(f'[INFO] Created category: {name}')
            
            # Create sample articles only if database was empty
            if not existing_articles:
                articles_to_create = [
                    ('Welcome to Our News Platform', 
                     'This is your comprehensive news management system. You can create, edit, and manage articles across different categories with media upload support.',
                     'Local', 'Admin'),
                    ('Latest Technology Trends 2024', 
                     'Exploring the cutting-edge technology trends that are shaping our future. From AI advancements to sustainable tech solutions with media integration.',
                     'Technology', 'Tech Editor'),
                    ('Global Economic Outlook', 
                     'An analysis of current global economic conditions and future projections for businesses worldwide. Categories help organize content effectively.',
                     'Business', 'Business Analyst'),
                    ('Community Events This Month', 
                     'Stay updated with local community events, festivals, and activities. Media management makes sharing event photos easy.',
                     'Local', 'Community Manager'),
                    ('Breaking: Major Tech Announcement', 
                     'A major technology company has just announced revolutionary changes to their platform. Industry experts are calling it a game-changer.',
                     'Technology', 'Tech Reporter'),
                    ('Sports Championship Results', 
                     'The finals have concluded with an spectacular display of athletic prowess. Here are the complete results and highlights from the championship.',
                     'Sports', 'Sports Desk')
                ]
                
                for title, content, cat_name, author in articles_to_create:
                    cat = cat_map.get(cat_name)
                    create_article(title, content, cat.id if cat else None, author)
                    print(f'[INFO] Created article: {title}')
            
            # Commit changes to ensure persistence
            try:
                db.session.commit()
            except Exception as commit_error:
                db.session.rollback()
                print(f'[WARNING] Commit warning (data may already be persisted): {commit_error}')
            
            final_articles = list_articles()
            final_categories = list_categories()
            print(f'[SUCCESS] Database seeded! Contains {len(final_articles)} articles and {len(final_categories)} categories.')
            return True
            
        except Exception as e:
            print(f'[ERROR] Error seeding database: {e}')
            import traceback
            traceback.print_exc()
            return False


def create_app_with_seeding():
    """
    Create Flask app with automatic database seeding.
    This is an alternative to create_app() that ensures data persistence.
    """
    from . import create_app
    
    app = create_app()
    
    # Seed data on startup
    with app.app_context():
        seed_data(app)
    
    return app


if __name__ == '__main__':
    # Run seeding when executed directly
    success = seed_data()
    if success:
        print('[SUCCESS] Seeding completed successfully!')
    else:
        print('[FAILED] Seeding failed. Check errors above.')

