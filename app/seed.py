from app.main import create_app
from app.services.category_service import create_category
from app.services.article_service import create_article

def seed():
    app = create_app()
    with app.app_context():
        # create sample categories
        tech = create_category('Technology')
        world = create_category('World')
        local = create_category('Local')

        # create sample articles
        create_article('Tech News Today', 'An update about the latest in tech.', tech.id)
        create_article('Global Affairs', 'Top stories around the world.', world.id)
        create_article('Community Notice', 'Local community updates and events.', local.id)

if __name__ == '__main__':
    seed()
    print('Seed complete')
