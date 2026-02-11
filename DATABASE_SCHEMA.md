# Database Schema Documentation

## Overview
The application uses **SQLAlchemy ORM** with **SQLite** database (stored on persistent disk at `/opt/render/project/src/news.db` on Render.com).

## Database Models

### 1. Category Table
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(255)
);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Category name |
| description | VARCHAR(255) | NULLABLE | Category description |

**Relationships:**
- One-to-Many with Articles (cascade delete)

---

### 2. Article Table
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100),
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    category_id INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| title | VARCHAR(255) | NOT NULL | Article headline |
| author | VARCHAR(100) | NULLABLE | Author name |
| content | TEXT | NOT NULL | Full article content |
| image_url | VARCHAR(500) | NULLABLE | Featured image path |
| category_id | INTEGER | FOREIGN KEY | Links to categories.id |
| created_at | DATETIME | Auto-generated | Creation timestamp |
| updated_at | DATETIME | Auto-updated | Last modification timestamp |

**Relationships:**
- Many-to-One with Category

---

### 3. Media Table
```sql
CREATE TABLE media (
    id INTEGER PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_at DATETIME
);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| filename | VARCHAR(255) | NOT NULL | Saved filename (unique) |
| original_name | VARCHAR(255) | NOT NULL | Original upload name |
| file_type | VARCHAR(50) | NOT NULL | MIME type (image/jpeg, etc.) |
| file_size | INTEGER | NOT NULL | Size in bytes |
| file_path | VARCHAR(500) | NOT NULL | Server path to file |
| uploaded_at | DATETIME | Auto-generated | Upload timestamp |

---

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  Category   │       │   Article   │       │    Media    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │◄──────│ category_id │       │ id (PK)     │
│ name        │       │ id (PK)     │       │ filename    │
│ description │       │ title       │       │ file_type   │
└─────────────┘       │ content     │       │ file_size   │
      │               │ author      │       │ file_path   │
      │               │ image_url   │       │ uploaded_at │
      └──────────────►│ created_at  │       └─────────────┘
                     │ updated_at  │
                     └─────────────┘

Relationships:
- Category 1 ───► N Article (one-to-many)
```

---

## Default Categories (Seeded Data)

| ID | Name | Description |
|----|------|-------------|
| 1 | Technology | Latest technology news and updates |
| 2 | World | Global news and international affairs |
| 3 | Local | Local community news and events |
| 4 | Business | Business and financial news |
| 5 | Sports | Sports news and updates |
| 6 | Entertainment | Movies, music, and celebrity news |

---

## Database Location

| Environment | Location |
|-------------|----------|
| **Local Development** | `./news.db` (project root) |
| **Render.com** | `/opt/render/project/src/news.db` (persistent disk) |

---

## Accessing the Database

### Via Python Shell
```python
from news_app import create_app
from news_app.models.db import db
from news_app.models.article import Article
from news_app.models.category import Category

app = create_app()
with app.app_context():
    # Query examples
    articles = Article.query.all()
    categories = Category.query.all()
    
    # Filter by category
    tech_articles = Article.query.filter_by(category_id=1).all()
```

### Via SQLite CLI (Local)
```bash
sqlite3 news.db
SQL> .tables
SQL> SELECT * FROM articles;
SQL> .schema articles
```

### Via Render.com
- Use **Render Dashboard** → **PostgreSQL** (if using PostgreSQL)
- Or connect via CLI with connection string from `DATABASE_URL` env var

---

## Migration Note

The database is automatically created via SQLAlchemy's `db.create_all()` on app startup. No migrations are currently implemented (schema changes require manual intervention or Flask-Migrate integration).

