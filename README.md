# Django Blog Application

A fully functional blog platform built with Django, MySQL, and Django REST Framework. This application provides a complete blogging experience with user authentication, rich text editing, comments, likes, and a modern responsive frontend.

## Features

### Backend Features
- **User Authentication**: JWT-based authentication system
- **Blog Post Management**: Create, read, update, and delete blog posts
- **Rich Text Editor**: CKEditor integration for content creation
- **Comments System**: Users can comment on posts with approval workflow
- **Like System**: Users can like/unlike posts
- **Search Functionality**: Search posts by title, content, or excerpt
- **Pagination**: API and frontend pagination (10 posts per page)
- **Admin Interface**: Customized Django admin panel
- **API**: RESTful API with comprehensive endpoints

### Frontend Features
- **Responsive Design**: Modern Bootstrap 5 interface
- **Dynamic Content**: AJAX-powered likes and comments
- **Real-time Updates**: Live comment posting and like updates
- **Search**: Real-time search functionality
- **Share**: Native sharing and clipboard fallback
- **User Management**: Login/logout with user profile dropdown

### Bonus Features
- **Comment System**: Full CRUD operations for comments
- **Like System**: Toggle likes with AJAX
- **Search**: Advanced search across titles and content
- **Share**: Native Web Share API with fallback

## Technology Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: Bootstrap 5, jQuery, Font Awesome
- **Rich Text**: CKEditor
- **API**: RESTful API with pagination

## Installation & Setup

### Prerequisites

1. **Python 3.8+**
2. **MySQL Server**
3. **Git**

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd django_blog_project
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

1. **Create MySQL Database**:
```sql
CREATE DATABASE django_blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. **Update Database Settings** (if needed):
Edit `django_blog/settings.py` and update the database configuration:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_blog_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Usage

### Frontend Usage

1. **View Blog Posts**: Visit the homepage to see all published posts
2. **Read Posts**: Click "Read More" to view full posts
3. **Create Posts**: Login and click "Create Post" to add new content
4. **Edit Posts**: Authors can edit their own posts
5. **Like Posts**: Click the heart icon to like/unlike posts
6. **Comment**: Add comments to posts (requires login)
7. **Search**: Use the search bar to find specific posts

### API Usage

#### Authentication

Get JWT tokens:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Refresh token:
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'
```

#### Blog Posts API

**List Posts**:
```bash
GET /api/posts/
```

**Get Single Post**:
```bash
GET /api/posts/{id}/
```

**Create Post**:
```bash
POST /api/posts/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "title": "My Blog Post",
  "content": "Post content here...",
  "excerpt": "Brief summary",
  "status": "published"
}
```

**Update Post**:
```bash
PUT /api/posts/{id}/
Authorization: Bearer <your_access_token>
```

**Delete Post**:
```bash
DELETE /api/posts/{id}/
Authorization: Bearer <your_access_token>
```

**Like/Unlike Post**:
```bash
POST /api/posts/{id}/like/
Authorization: Bearer <your_access_token>
```

**Get Post Comments**:
```bash
GET /api/posts/{id}/comments/
```

**Add Comment**:
```bash
POST /api/posts/{id}/add_comment/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "content": "Your comment here..."
}
```

#### Comments API

**List Comments**:
```bash
GET /api/comments/
```

**Create Comment**:
```bash
POST /api/comments/
Authorization: Bearer <your_access_token>
```

**Update Comment**:
```bash
PUT /api/comments/{id}/
Authorization: Bearer <your_access_token>
```

**Delete Comment**:
```bash
DELETE /api/comments/{id}/
Authorization: Bearer <your_access_token>
```

#### Likes API

**List Likes**:
```bash
GET /api/likes/
Authorization: Bearer <your_access_token>
```

**Create Like**:
```bash
POST /api/likes/
Authorization: Bearer <your_access_token>
```

**Delete Like**:
```bash
DELETE /api/likes/{id}/
Authorization: Bearer <your_access_token>
```

### API Features

- **Pagination**: All list endpoints support pagination (10 items per page)
- **Search**: Use `?search=query` parameter for searching
- **Filtering**: Filter by status, author, etc.
- **Ordering**: Sort by timestamp, title, etc.

## Project Structure

```
django_blog_project/
├── django_blog/          # Main project settings
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── blog/                 # Blog application
│   ├── models.py        # Database models
│   ├── views.py         # API and frontend views
│   ├── serializers.py   # API serializers
│   ├── admin.py         # Admin interface
│   └── urls.py          # Blog URL patterns
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   └── blog/            # Blog templates
├── static/              # Static files
├── requirements.txt     # Python dependencies
├── manage.py           # Django management
└── README.md           # This file
```

## Models

### BlogPost
- `title`: Post title (CharField)
- `content`: Rich text content (RichTextField)
- `author`: Foreign key to User
- `timestamp`: Creation timestamp
- `updated_at`: Last update timestamp
- `status`: Draft or Published
- `slug`: URL-friendly identifier
- `excerpt`: Brief summary

### Comment
- `post`: Foreign key to BlogPost
- `author`: Foreign key to User
- `content`: Comment text
- `created_at`: Creation timestamp
- `is_approved`: Approval status

### Like
- `post`: Foreign key to BlogPost
- `user`: Foreign key to User
- `created_at`: Creation timestamp

## Admin Interface

Access the admin interface at `http://localhost:8000/admin/`

Features:
- **Blog Post Management**: Create, edit, delete posts
- **Comment Moderation**: Approve/disapprove comments
- **User Management**: Manage users and permissions
- **Statistics**: View like and comment counts
- **Search**: Search posts by title, content, author

## Deployment

### Production Settings

1. **Update settings.py**:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECRET_KEY = 'your-secure-secret-key'
```

2. **Static Files**:
```bash
python manage.py collectstatic
```

3. **Database**:
- Use production MySQL server
- Configure proper database credentials

4. **Web Server**:
- Use Gunicorn or uWSGI
- Configure Nginx or Apache

### Environment Variables

Create a `.env` file:
```
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://user:password@localhost/django_blog_db
DEBUG=False
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue on the repository.

## Acknowledgments

- Django team for the excellent framework
- Bootstrap team for the responsive UI components
- CKEditor team for the rich text editor
- Font Awesome for the beautiful icons 