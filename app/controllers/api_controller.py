from flask import Blueprint, jsonify, request
from app.services.news_service import top_headlines

api_bp = Blueprint('api', __name__)


@api_bp.route('/live')
def live_news():
    country = request.args.get('country', 'us')
    category = request.args.get('category')
    data = top_headlines(country=country, category=category)
    # return articles list only
    return jsonify(data)
