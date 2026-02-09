from flask import Flask, send_from_directory, Response
from .Backend.models.db import db
from .Backend.controllers.article_controller import article_bp
from .Backend.controllers.category_controller import category_bp
from .Backend.controllers.admin_controller import admin_bp
from .Backend.controllers.api_controller import api_bp
from .Backend.controllers.media_controller import media_bp
import os
import mimetypes

def create_app():
    template_dir = os.path.join(os.path.dirname(__file__), 'Frontend', 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'Frontend', 'static')
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
    
    # Ensure correct MIME types
    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('application/javascript', '.js')
    
    # Configure database - PostgreSQL for production, SQLite for development
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Production: Use PostgreSQL from Render.com
        if database_url.startswith('postgres://'):
            # Fix for newer SQLAlchemy versions
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
        }
        print(f"[INFO] Using PostgreSQL database for production")
    else:
        # Development: Use SQLite
        db_path = os.path.abspath('news.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'connect_args': {'timeout': 15, 'check_same_thread': False},
            'pool_pre_ping': True,
        }
        print(f"[INFO] Using SQLite database for development: {db_path}")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

    db.init_app(app)

    # Create tables and seed data within app context
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print(f"[INFO] Database tables initialized successfully")
            
            # Seed initial data if tables are empty
            from .Backend.seed import seed_data
            seed_data(app)
            
        except Exception as e:
            print(f"[WARNING] Database initialization error: {e}")
    
    app.register_blueprint(article_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(media_bp)

    return app

