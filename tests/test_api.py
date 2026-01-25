import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import create_app
from app.services.category_service import create_category
from app.services.article_service import create_article


def test_articles_api_returns_created_article():
    app = create_app()
    with app.app_context():
        from app.models.db import db
        db.drop_all()
        db.create_all()

        c = create_category('APIcat')
        create_article('API title', 'api body', c.id)

        client = app.test_client()
        resp = client.get('/api/articles')
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, list)
        assert any(it['title'] == 'API title' for it in data)
