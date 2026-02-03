from .. import create_app
from ..services.category_service import create_category, list_categories
from ..services.article_service import create_article

def seed():
    app = create_app()
    with app.app_context():
        # Check if data already exists
        existing_cats = list_categories()
        if existing_cats:
            print(f'Database already contains {len(existing_cats)} categories. Skipping seed.')
            return
        
        # create sample categories
        print('Creating sample categories...')
        tech = create_category('Technology')
        world = create_category('World')
        local = create_category('Local')

        # create sample articles
        print('Creating sample articles...')
        create_article('Tech News Today', 'An update about the latest in tech.', tech.id)
        create_article('Global Affairs', 'Top stories around the world.', world.id)
        create_article('Community Notice', 'Local community updates and events.', local.id)
        
        print('✅ Seed complete!')

if __name__ == '__main__':
    seed()
