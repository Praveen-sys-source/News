from flask import Blueprint, render_template
from app.services.article_service import list_articles
from app.services.category_service import list_categories

admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.route('/admin')
def dashboard():
    articles = list_articles()
    categories = list_categories()
    return render_template('admin_dashboard.html', articles=articles, categories=categories)
