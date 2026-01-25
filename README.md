# News Management System

A comprehensive news management system built with Flask backend and vanilla JavaScript frontend. Features include live news integration, article management, category management, and an admin dashboard.

## Features

- **Live News**: Integration with NewsAPI for real-time news updates
- **Article Management**: Create, view, edit, and delete internal articles
- **Category Management**: Organize articles by categories
- **Media Management**: Upload and manage media files
- **Admin Dashboard**: Comprehensive admin interface for managing all content
- **Dark/Light Mode**: Toggle between themes for better user experience
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
News/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── cert.pem                        # SSL certificate (for HTTPS)
├── key.pem                         # SSL private key (for HTTPS)
├── README.md                       # This file
├── TODO.md                         # Development tasks and roadmap
├── .env                            # Environment variables (create this)
│
├── app/                            # Main application package
│   ├── __init__.py                # Flask app factory and configuration
│   ├── seed.py                    # Database seeding script
│   │
│   ├── controllers/               # Request handlers
│   │   ├── __init__.py
│   │   ├── admin_controller.py    # Admin dashboard and management routes
│   │   ├── api_controller.py      # REST API endpoints
│   │   ├── article_controller.py  # Article CRUD operations
│   │   ├── category_controller.py # Category management
│   │   └── media_controller.py    # Media upload and management
│   │
│   ├── models/                    # Database models
│   │   ├── __init__.py
│   │   ├── db.py                  # SQLAlchemy setup and initialization
│   │   ├── article.py             # Article model
│   │   ├── category.py            # Category model
│   │   └── media.py               # Media model
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── article_service.py     # Article-related business logic
│   │   ├── category_service.py    # Category-related business logic
│   │   ├── media_service.py       # Media-related business logic
│   │   └── news_service.py        # Live news API integration
│   │
│   ├── templates/                 # HTML templates (Jinja2)
│   │   ├── layout.html            # Base layout template
│   │   ├── index.html             # Home page
│   │   ├── live_news.html         # Live news page
│   │   ├── articles.html          # Articles listing
│   │   ├── article_detail.html    # Single article view
│   │   ├── latest.html            # Latest news page
│   │   ├── categories.html        # Categories listing
│   │   ├── create_article.html    # Create new article
│   │   ├── admin_dashboard.html   # Admin dashboard
│   │   ├── manage_articles.html   # Manage all articles
│   │   ├── manage_categories.html # Manage categories
│   │   └── manage_media.html      # Manage media files
│   │
│   ├── static/                    # Static assets
│   │   ├── css/
│   │   │   └── style.css          # Main stylesheet
│   │   ├── js/
│   │   │   ├── main.js            # Main JavaScript file
│   │   │   └── state.js           # State management
│   │   └── uploads/               # Uploaded media files
│   │
│   └── instance/                  # Instance-specific files
│       └── news.db                # SQLite database
│
├── static/                        # Static assets (symlinked)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   └── state.js
│   └── uploads/                   # Uploaded media files
│
├── tests/                         # Unit tests
│   ├── test_api.py
│   └── test_services.py
│
├── instance/                      # Instance files
│   └── news.db                    # SQLite database
│
└── Documentation Files:
    ├── IMPORT_STRUCTURE_DIAGRAM.md
    ├── IMPORT_AUDIT_COMPLETE.md
    ├── LIVE_NEWS_COMPLETE_SUMMARY.md
    ├── LIVE_NEWS_DOCUMENTATION.md
    ├── LIVE_NEWS_IMPLEMENTATION.md
    ├── MANAGE_NEWS_DOCUMENTATION.md
    ├── MANAGE_NEWS_IMPLEMENTATION.md
    └── MANAGE_NEWS_QUICK_REFERENCE.md
```

## Database Schema

### Article Model
- `id`: Integer, Primary Key
- `title`: String(200)
- `content`: Text
- `created_at`: DateTime
- `category_id`: ForeignKey to Category

### Category Model
- `id`: Integer, Primary Key
- `name`: String(100)
- `description`: Text (optional)

### Media Model
- `id`: Integer, Primary Key
- `filename`: String(255)
- `filepath`: String(500)
- `mime_type`: String(100)
- `created_at`: DateTime

## API Endpoints

### Articles
- `GET /articles` - List all articles
- `GET /articles/<id>` - Get single article
- `POST /articles/create` - Create new article
- `POST /articles/<id>/edit` - Update article
- `POST /articles/<id>/delete` - Delete article

### Categories
- `GET /categories` - List all categories
- `POST /categories/manage` - Create/Edit category

### Media
- `GET /media/manage` - Media management page
- `POST /media/upload` - Upload media file

### Admin
- `GET /manage` - Admin dashboard
- `GET /admin/stats` - Get system statistics

## Quick Start

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=sqlite:///news.db

# NewsAPI Key (for live news)
NEWS_API_KEY=pub_b6ea65c0579b42b5a8f61d11f2eac14f

# SSL Configuration (optional, for HTTPS)
SSL_CERT=/path/to/cert.pem
SSL_KEY=/path/to/key.pem

# Secret Key for sessions
SECRET_KEY=your-secret-key-here
```

### 3. Run the Application

```bash
python app.py
```

### 4. Access the Application

- **HTTP**: http://localhost:8080
- **HTTPS**: https://localhost:8443 (if SSL configured)

## Generate Self-Signed Certificate (for development)

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"
```

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Tailwind CSS
- **API Integration**: NewsAPI

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Database Migrations

The database is automatically created when the application starts. To reset:

```bash
rm instance/news.db
python app.py
```

## License

This project is open source and available for personal and commercial use.

## Credits

- Developed by Praveen
- Live news powered by [NewsAPI](https://newsapi.org)

