from flask import Flask
from app.models.db import db
from app.controllers.article_controller import article_bp
from app.controllers.category_controller import category_bp
from app.controllers.admin_controller import admin_bp
from app.controllers.api_controller import api_bp
from app.controllers.media_controller import media_bp
import os

def create_app():
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
    
    # Use persistent SQLite file-based database
    if os.getenv('DATABASE_URL'):
        db_uri = os.getenv('DATABASE_URL')
    else:
        # Ensure instance directory exists for database file
        app_dir = os.path.dirname(os.path.abspath(__file__))
        instance_dir = os.path.abspath(os.path.join(app_dir, '..', 'instance'))
        os.makedirs(instance_dir, exist_ok=True)
        db_path = os.path.join(instance_dir, 'app.db')
        db_uri = f'sqlite:///{db_path}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'timeout': 15},
        'pool_size': 10,
        'pool_recycle': 3600,
    }

    db.init_app(app)

    # Create tables within app context
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")
    
    app.register_blueprint(article_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(media_bp)

    return app

