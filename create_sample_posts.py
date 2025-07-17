#!/usr/bin/env python3
"""
Sample Blog Posts Creator
This script creates sample blog posts to demonstrate all features of the Django blog application.
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import BlogPost, Comment, Like

def create_sample_posts():
    """Create sample blog posts with rich content"""
    
    # Get or create a user
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        user.set_password('admin123')
        user.save()
        print(f"✅ Created admin user: {user.username}")
    
    # Sample blog posts data
    sample_posts = [
        {
            'title': 'Welcome to Django Blog - A Complete Guide',
            'excerpt': 'Learn how to build a full-featured blog application with Django, MySQL, and modern web technologies.',
            'content': '''
            <h2>Introduction to Django Blog</h2>
            <p>Welcome to our comprehensive guide on building a modern blog application with Django! This application demonstrates the power of Django's framework and showcases various features that make it perfect for content management.</p>
            
            <h3>Key Features</h3>
            <ul>
                <li><strong>User Authentication:</strong> JWT-based authentication system</li>
                <li><strong>Rich Text Editor:</strong> CKEditor integration for content creation</li>
                <li><strong>Comments System:</strong> Users can comment on posts with approval workflow</li>
                <li><strong>Like System:</strong> AJAX-powered like/unlike functionality</li>
                <li><strong>Search:</strong> Real-time search across titles and content</li>
                <li><strong>API:</strong> RESTful API with comprehensive endpoints</li>
            </ul>
            
            <h3>Technology Stack</h3>
            <p>This blog is built with:</p>
            <ul>
                <li>Django 4.2+</li>
                <li>Django REST Framework</li>
                <li>MySQL Database</li>
                <li>Bootstrap 5 for responsive design</li>
                <li>CKEditor for rich text editing</li>
                <li>JWT Authentication</li>
            </ul>
            
            <h3>Getting Started</h3>
            <p>To get started with this blog application:</p>
            <ol>
                <li>Clone the repository</li>
                <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
                <li>Run migrations: <code>python manage.py migrate</code></li>
                <li>Create superuser: <code>python manage.py createsuperuser</code></li>
                <li>Start server: <code>python manage.py runserver</code></li>
            </ol>
            
            <p>Happy blogging! 🚀</p>
            ''',
            'status': 'published'
        },
        {
            'title': 'Building REST APIs with Django REST Framework',
            'excerpt': 'A comprehensive guide to creating powerful REST APIs using Django REST Framework and best practices.',
            'content': '''
            <h2>Understanding Django REST Framework</h2>
            <p>Django REST Framework (DRF) is a powerful toolkit for building Web APIs. It provides a set of tools and utilities that make it easy to build RESTful APIs with Django.</p>
            
            <h3>Key Concepts</h3>
            <h4>1. Serializers</h4>
            <p>Serializers allow you to convert complex data types, such as Django models, to Python data types that can then be easily rendered into JSON, XML, or other content types.</p>
            
            <h4>2. ViewSets</h4>
            <p>ViewSets provide a way to combine the logic for a set of related views into a single class. They are particularly useful for API endpoints.</p>
            
            <h4>3. Authentication</h4>
            <p>DRF provides several authentication schemes including:</p>
            <ul>
                <li>Token Authentication</li>
                <li>Session Authentication</li>
                <li>JWT Authentication</li>
                <li>OAuth2</li>
            </ul>
            
            <h3>Example API Endpoints</h3>
            <p>Our blog application provides these API endpoints:</p>
            <ul>
                <li><code>GET /api/posts/</code> - List all blog posts</li>
                <li><code>POST /api/posts/</code> - Create a new blog post</li>
                <li><code>GET /api/posts/{id}/</code> - Get specific post</li>
                <li><code>PUT /api/posts/{id}/</code> - Update post</li>
                <li><code>DELETE /api/posts/{id}/</code> - Delete post</li>
                <li><code>POST /api/posts/{id}/like/</code> - Like/unlike post</li>
                <li><code>POST /api/posts/{id}/add_comment/</code> - Add comment</li>
            </ul>
            
            <h3>Testing APIs</h3>
            <p>You can test these endpoints using tools like:</p>
            <ul>
                <li>Postman</li>
                <li>cURL</li>
                <li>Django REST Framework's browsable API</li>
            </ul>
            
            <p>This demonstrates the power and flexibility of Django REST Framework! 🎯</p>
            ''',
            'status': 'published'
        },
        {
            'title': 'Modern Frontend Development with Bootstrap 5',
            'excerpt': 'Explore the latest features of Bootstrap 5 and how to create responsive, modern web interfaces.',
            'content': '''
            <h2>Bootstrap 5 Features</h2>
            <p>Bootstrap 5 brings significant improvements and new features to help you build better web applications faster.</p>
            
            <h3>What's New in Bootstrap 5</h3>
            <ul>
                <li><strong>Removed jQuery:</strong> Bootstrap 5 no longer depends on jQuery</li>
                <li><strong>Improved Grid System:</strong> Enhanced responsive grid with better breakpoints</li>
                <li><strong>New Components:</strong> Offcanvas, floating labels, and more</li>
                <li><strong>Better Utilities:</strong> Enhanced utility classes for spacing, colors, and typography</li>
                <li><strong>CSS Custom Properties:</strong> Better theming support</li>
            </ul>
            
            <h3>Responsive Design</h3>
            <p>Our blog application uses Bootstrap 5's responsive grid system to ensure it looks great on all devices:</p>
            
            <div class="row">
                <div class="col-md-6">
                    <h4>Mobile First</h4>
                    <p>Design for mobile devices first, then scale up for larger screens.</p>
                </div>
                <div class="col-md-6">
                    <h4>Flexible Grid</h4>
                    <p>12-column grid system that adapts to different screen sizes.</p>
                </div>
            </div>
            
            <h3>Components Used in Our Blog</h3>
            <ul>
                <li><strong>Navbar:</strong> Responsive navigation with dropdown menus</li>
                <li><strong>Cards:</strong> Blog post cards with hover effects</li>
                <li><strong>Forms:</strong> Styled forms with validation</li>
                <li><strong>Buttons:</strong> Various button styles and states</li>
                <li><strong>Alerts:</strong> Success, warning, and error messages</li>
                <li><strong>Pagination:</strong> Page navigation for blog posts</li>
            </ul>
            
            <h3>Custom Styling</h3>
            <p>We've added custom CSS to enhance the Bootstrap design:</p>
            <ul>
                <li>Custom color scheme</li>
                <li>Hover effects on blog posts</li>
                <li>Gradient backgrounds</li>
                <li>Custom animations</li>
                <li>Responsive typography</li>
            </ul>
            
            <p>Bootstrap 5 makes it easy to create beautiful, responsive web applications! 🎨</p>
            ''',
            'status': 'published'
        },
        {
            'title': 'Database Design Best Practices for Django Applications',
            'excerpt': 'Learn how to design efficient database schemas and optimize performance for Django applications.',
            'content': '''
            <h2>Database Design Principles</h2>
            <p>Good database design is crucial for the performance and maintainability of your Django applications. Here are some best practices to follow.</p>
            
            <h3>1. Model Design</h3>
            <p>Our blog application demonstrates several good practices:</p>
            <ul>
                <li><strong>Proper Relationships:</strong> Foreign keys for comments and likes</li>
                <li><strong>Indexing:</strong> Automatic indexing on foreign keys</li>
                <li><strong>Constraints:</strong> Unique constraints for likes</li>
                <li><strong>Meta Options:</strong> Proper ordering and verbose names</li>
            </ul>
            
            <h3>2. Database Models</h3>
            <h4>BlogPost Model</h4>
            <ul>
                <li><code>title</code>: CharField with max_length for SEO</li>
                <li><code>content</code>: RichTextField for formatted content</li>
                <li><code>author</code>: ForeignKey to User with CASCADE delete</li>
                <li><code>timestamp</code>: Auto-created timestamp</li>
                <li><code>status</code>: Choices for draft/published</li>
                <li><code>slug</code>: URL-friendly identifier</li>
                <li><code>excerpt</code>: Brief summary for listings</li>
            </ul>
            
            <h4>Comment Model</h4>
            <ul>
                <li><code>post</code>: ForeignKey to BlogPost</li>
                <li><code>author</code>: ForeignKey to User</li>
                <li><code>content</code>: TextField for comment text</li>
                <li><code>is_approved</code>: Boolean for moderation</li>
            </ul>
            
            <h4>Like Model</h4>
            <ul>
                <li><code>post</code>: ForeignKey to BlogPost</li>
                <li><code>user</code>: ForeignKey to User</li>
                <li><code>unique_together</code>: Prevents duplicate likes</li>
            </ul>
            
            <h3>3. Performance Optimization</h3>
            <ul>
                <li><strong>Select Related:</strong> Use select_related() for foreign keys</li>
                <li><strong>Prefetch Related:</strong> Use prefetch_related() for reverse foreign keys</li>
                <li><strong>Database Indexes:</strong> Add indexes for frequently queried fields</li>
                <li><strong>Query Optimization:</strong> Minimize database queries</li>
            </ul>
            
            <h3>4. Database Choices</h3>
            <p>Our application supports both SQLite and MySQL:</p>
            <ul>
                <li><strong>SQLite:</strong> Great for development and small applications</li>
                <li><strong>MySQL:</strong> Better for production with high traffic</li>
                <li><strong>PostgreSQL:</strong> Excellent for complex queries and data integrity</li>
            </ul>
            
            <p>Good database design is the foundation of a scalable application! 🏗️</p>
            ''',
            'status': 'published'
        },
        {
            'title': 'User Authentication and Security in Django',
            'excerpt': 'Implement secure user authentication using JWT tokens and best practices for Django applications.',
            'content': '''
            <h2>Authentication in Django</h2>
            <p>Security is paramount in web applications. Django provides robust authentication systems, and we've enhanced it with JWT tokens for API access.</p>
            
            <h3>JWT Authentication</h3>
            <p>JSON Web Tokens (JWT) provide a secure way to authenticate API requests:</p>
            <ul>
                <li><strong>Stateless:</strong> No server-side session storage needed</li>
                <li><strong>Secure:</strong> Cryptographically signed tokens</li>
                <li><strong>Scalable:</strong> Works well with microservices</li>
                <li><strong>Flexible:</strong> Can contain custom claims</li>
            </ul>
            
            <h3>Implementation Details</h3>
            <h4>Token Generation</h4>
            <p>Users can obtain tokens by making a POST request:</p>
            <pre><code>POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}</code></pre>
            
            <h4>Token Usage</h4>
            <p>Include the token in API requests:</p>
            <pre><code>Authorization: Bearer &lt;your_access_token&gt;</code></pre>
            
            <h4>Token Refresh</h4>
            <p>Refresh expired tokens:</p>
            <pre><code>POST /api/token/refresh/
{
    "refresh": "your_refresh_token"
}</code></pre>
            
            <h3>Security Features</h3>
            <ul>
                <li><strong>Password Validation:</strong> Django's built-in password validators</li>
                <li><strong>CSRF Protection:</strong> Cross-site request forgery protection</li>
                <li><strong>XSS Protection:</strong> Content Security Policy headers</li>
                <li><strong>SQL Injection Protection:</strong> Django ORM prevents SQL injection</li>
                <li><strong>HTTPS:</strong> Always use HTTPS in production</li>
            </ul>
            
            <h3>Permission System</h3>
            <p>Our application implements several permission levels:</p>
            <ul>
                <li><strong>IsAuthenticatedOrReadOnly:</strong> Anyone can read, only authenticated users can write</li>
                <li><strong>IsAuthenticated:</strong> Only authenticated users can access</li>
                <li><strong>Owner Permissions:</strong> Users can only edit their own content</li>
            </ul>
            
            <h3>Best Practices</h3>
            <ul>
                <li>Use strong passwords</li>
                <li>Implement rate limiting</li>
                <li>Log authentication attempts</li>
                <li>Use HTTPS in production</li>
                <li>Regular security updates</li>
                <li>Monitor for suspicious activity</li>
            </ul>
            
            <p>Security should always be a top priority in web development! 🔒</p>
            ''',
            'status': 'published'
        }
    ]
    
    # Create sample posts
    created_posts = []
    for i, post_data in enumerate(sample_posts):
        # Set different timestamps for variety
        timestamp = datetime.now() - timedelta(days=i*2, hours=i*3)
        
        post = BlogPost.objects.create(
            title=post_data['title'],
            content=post_data['content'],
            excerpt=post_data['excerpt'],
            author=user,
            status=post_data['status'],
            timestamp=timestamp
        )
        created_posts.append(post)
        print(f"✅ Created post: {post.title}")
    
    # Create some sample comments
    sample_comments = [
        "Great article! Very informative and well-written.",
        "This helped me understand Django better. Thanks!",
        "Excellent guide for beginners like me.",
        "The examples are very clear and practical.",
        "Looking forward to more content like this!"
    ]
    
    for post in created_posts[:3]:  # Add comments to first 3 posts
        for i, comment_text in enumerate(sample_comments[:2]):  # 2 comments per post
            comment = Comment.objects.create(
                post=post,
                author=user,
                content=comment_text,
                is_approved=True
            )
            print(f"✅ Added comment to '{post.title}': {comment_text[:50]}...")
    
    # Add some likes
    for post in created_posts[:2]:  # Like first 2 posts
        like = Like.objects.create(
            post=post,
            user=user
        )
        print(f"✅ Added like to '{post.title}'")
    
    print(f"\n🎉 Successfully created {len(created_posts)} sample blog posts!")
    print(f"📝 Added {len(created_posts) * 2} sample comments")
    print(f"❤️  Added {len(created_posts[:2])} sample likes")
    print("\n🌐 Visit http://localhost:8000 to see your blog!")
    print("🔧 Admin panel: http://localhost:8000/admin/")

if __name__ == "__main__":
    create_sample_posts() 