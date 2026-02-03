from .. import create_app
from ..services.category_service import create_category, list_categories
from ..services.article_service import create_article, list_articles
from ..services.media_service import list_media
import os

def seed():
    app = create_app()
    with app.app_context():
        # Check if data already exists
        existing_cats = list_categories()
        existing_articles = list_articles()
        existing_media = list_media()
        
        if existing_cats and existing_articles:
            print(f'Database already contains {len(existing_cats)} categories, {len(existing_articles)} articles, and {len(existing_media)} media files. Skipping seed.')
            return
        
        # Ensure upload directory exists
        upload_dir = 'static/uploads'
        os.makedirs(upload_dir, exist_ok=True)
        gitkeep_path = os.path.join(upload_dir, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write('# Keep this directory in git\n')
        
        # Create sample categories if they don't exist
        if not existing_cats:
            print('Creating sample categories...')
            tech = create_category('Technology', 'Latest technology news and updates')
            world = create_category('World', 'Global news and international affairs')
            local = create_category('Local', 'Local community news and events')
            business = create_category('Business', 'Business and financial news')
            sports = create_category('Sports', 'Sports news and updates')
            entertainment = create_category('Entertainment', 'Movies, music, and celebrity news')
        else:
            # Get existing categories
            categories = list_categories()
            cat_dict = {cat.name: cat for cat in categories}
            tech = cat_dict.get('Technology')
            world = cat_dict.get('World')
            local = cat_dict.get('Local')

        # Create sample articles if they don't exist
        if not existing_articles:
            print('Creating sample articles...')
            create_article('Welcome to Our News Platform', 
                         'This is your comprehensive news management system. You can create, edit, and manage articles across different categories with media upload support.',
                         local.id if local else None, 'Admin')
            create_article('Latest Technology Trends 2024', 
                         'Exploring the cutting-edge technology trends that are shaping our future. From AI advancements to sustainable tech solutions with media integration.',
                         tech.id if tech else None, 'Tech Editor')
            create_article('Global Economic Outlook', 
                         'An analysis of current global economic conditions and future projections for businesses worldwide. Categories help organize content effectively.',
                         world.id if world else None, 'Business Analyst')
            create_article('Community Events This Month', 
                         'Stay updated with local community events, festivals, and activities. Media management makes sharing event photos easy.',
                         local.id if local else None, 'Community Manager')
        
        final_articles = list_articles()
        final_categories = list_categories()
        final_media = list_media()
        print(f'✅ Seed complete! Database contains {len(final_articles)} articles, {len(final_categories)} categories, and {len(final_media)} media files')

if __name__ == '__main__':
    seed()
