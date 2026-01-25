import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import create_app
from app.services.category_service import list_categories, create_category
from app.services.article_service import list_articles, create_article, get_article


def test_category_and_article_crud():
    app = create_app()
    with app.app_context():
        from app.models.db import db
        db.drop_all()
        db.create_all()

        # Category CRUD
        c = create_category('TestCat')
        assert c.id is not None
        cats = list_categories()
        assert any(x.name == 'TestCat' for x in cats)

        # Article CRUD
        a = create_article('Test Title', 'Test content body', c.id)
        assert a.id is not None
        fetched = get_article(a.id)
        assert fetched.title == 'Test Title'
        assert fetched.content == 'Test content body'
