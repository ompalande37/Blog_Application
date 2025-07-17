# 🧪 Complete Testing Guide for Django Blog

## 📋 Overview

This guide covers all testing methods for your Django blog application, including JWT authentication, AJAX functionality, and frontend features.

## 🚀 Quick Start Testing

### 1. Start the Server
```bash
python manage.py runserver
```

### 2. Run Automated Tests
```bash
# Test JWT and AJAX functionality
python test_jwt_ajax.py

# Test basic API functionality
python test_api.py
```

## 🔐 JWT Authentication Testing

### Manual Testing

#### **Step 1: User Registration**
1. **Visit**: `http://localhost:8000/register/`
2. **Fill the form**:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123`
   - First Name: `Test`
   - Last Name: `User`
3. **Click**: "Register"
4. **Expected**: Success message and automatic login

#### **Step 2: User Login**
1. **Visit**: `http://localhost:8000/login/`
2. **Fill the form**:
   - Username: `testuser`
   - Password: `testpass123`
3. **Click**: "Login"
4. **Expected**: Success message and redirect to homepage

#### **Step 3: API Testing with cURL**
```bash
# Test registration
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "apiuser",
    "email": "api@example.com",
    "password": "apipass123",
    "first_name": "API",
    "last_name": "User"
  }'

# Test login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "apiuser",
    "password": "apipass123"
  }'

# Test with token (replace YOUR_TOKEN with actual token)
curl -X GET http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## ⚡ AJAX Functionality Testing

### Frontend Testing

#### **Step 1: Like/Unlike Posts**
1. **Visit**: `http://localhost:8000/`
2. **Find a blog post** with a heart icon
3. **Click the heart icon**
4. **Expected**: 
   - Heart turns red (filled)
   - Like count increases
   - Success message appears
5. **Click again**
6. **Expected**: 
   - Heart turns gray (empty)
   - Like count decreases
   - Success message appears

#### **Step 2: Add Comments**
1. **Visit**: `http://localhost:8000/post/any-post-slug/`
2. **Scroll to comments section**
3. **Fill comment form**:
   - Comment: "This is a test comment"
4. **Click**: "Add Comment"
5. **Expected**:
   - Comment appears immediately
   - Form clears
   - Comment count updates
   - Success message appears

#### **Step 3: Search Functionality**
1. **Visit**: `http://localhost:8000/`
2. **Use search bar** (if available)
3. **Type**: "django"
4. **Press Enter**
5. **Expected**: Posts containing "django" appear

### API Testing for AJAX Features

```bash
# Test like functionality (requires authentication)
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test comment functionality
curl -X POST http://localhost:8000/api/posts/1/add_comment/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Test comment via API"}'

# Test search
curl -X GET "http://localhost:8000/api/posts/?search=django"

# Test pagination
curl -X GET "http://localhost:8000/api/posts/?page=1"

# Test ordering
curl -X GET "http://localhost:8000/api/posts/?ordering=-timestamp"
```

## 🌐 Frontend Testing

### **Step 1: Navigation**
1. **Visit**: `http://localhost:8000/`
2. **Test navigation links**:
   - Home link
   - Create Post (if logged in)
   - Login/Register links
   - User dropdown (if logged in)

### **Step 2: Blog Post Operations**
1. **Create a Post**:
   - Click "Create Post"
   - Fill title, content, excerpt
   - Select status (published/draft)
   - Click "Create Post"
   - **Expected**: Redirect to homepage with new post

2. **Edit a Post**:
   - Find your post
   - Click "Edit"
   - Modify content
   - Click "Update Post"
   - **Expected**: Changes saved

3. **Delete a Post**:
   - Find your post
   - Click "Delete"
   - Confirm deletion
   - **Expected**: Post removed

### **Step 3: Responsive Design**
1. **Test on different screen sizes**:
   - Desktop (1920x1080)
   - Tablet (768x1024)
   - Mobile (375x667)
2. **Check elements**:
   - Navigation menu collapses
   - Cards stack properly
   - Text remains readable

## 🔧 API Endpoint Testing

### **Complete API Test Suite**

```bash
# 1. Authentication Tests
echo "=== Testing Authentication ==="
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123", "email": "test@example.com"}'

# 2. Get Token
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}')

ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['access'])")

echo "=== Testing Protected Endpoints ==="
# 3. Create Post
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Post", "content": "<p>Test content</p>", "excerpt": "Test excerpt", "status": "published"}'

# 4. Get Posts
curl -X GET http://localhost:8000/api/posts/

# 5. Like Post
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# 6. Add Comment
curl -X POST http://localhost:8000/api/posts/1/add_comment/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Test comment"}'

# 7. Search Posts
curl -X GET "http://localhost:8000/api/posts/?search=test"

# 8. Pagination
curl -X GET "http://localhost:8000/api/posts/?page=1"

echo "=== Testing Complete ==="
```

## 🐛 Debugging Common Issues

### **Issue 1: Template Errors**
```bash
# Error: Invalid block tag 'static'
# Solution: Add {% load static %} to templates
```

### **Issue 2: Authentication Errors**
```bash
# Error: 401 Unauthorized
# Solution: Check if token is valid and included in headers
```

### **Issue 3: AJAX Not Working**
```bash
# Check browser console for JavaScript errors
# Verify ajax.js is loaded
# Check network tab for failed requests
```

### **Issue 4: Database Issues**
```bash
# Reset database
python manage.py flush

# Recreate superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate
```

## 📊 Performance Testing

### **Load Testing with Apache Bench**
```bash
# Install Apache Bench (if not available)
# On Windows: Download from Apache website
# On Linux: sudo apt-get install apache2-utils

# Test homepage
ab -n 100 -c 10 http://localhost:8000/

# Test API endpoints
ab -n 50 -c 5 http://localhost:8000/api/posts/
```

### **Database Performance**
```bash
# Enable Django debug toolbar
pip install django-debug-toolbar

# Add to settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

## 🧪 Automated Testing

### **Run All Tests**
```bash
# Run Django tests
python manage.py test

# Run custom test scripts
python test_jwt_ajax.py
python test_api.py

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📱 Mobile Testing

### **Browser Developer Tools**
1. **Open Chrome DevTools** (F12)
2. **Click device icon** (mobile/tablet)
3. **Select device** (iPhone, iPad, etc.)
4. **Test functionality**:
   - Navigation
   - Forms
   - AJAX features
   - Responsive design

### **Real Device Testing**
1. **Find your computer's IP address**:
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```
2. **Update ALLOWED_HOSTS** in settings.py:
   ```python
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'YOUR_IP_ADDRESS']
   ```
3. **Run server on all interfaces**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
4. **Access from mobile**: `http://YOUR_IP_ADDRESS:8000`

## 🔒 Security Testing

### **Authentication Security**
```bash
# Test invalid credentials
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "wrong", "password": "wrong"}'

# Test expired token
curl -X GET http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer expired_token"

# Test missing token
curl -X POST http://localhost:8000/api/posts/1/like/
```

### **Input Validation**
```bash
# Test XSS prevention
curl -X POST http://localhost:8000/api/posts/1/add_comment/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "<script>alert(\"xss\")</script>"}'

# Test SQL injection prevention
curl -X GET "http://localhost:8000/api/posts/?search=' OR 1=1--"
```

## 📈 Monitoring and Logging

### **Enable Django Logging**
```python
# Add to settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### **Monitor Performance**
```bash
# Check server logs
tail -f debug.log

# Monitor database queries
python manage.py shell
>>> from django.db import connection
>>> connection.queries
```

## ✅ Testing Checklist

### **Pre-Testing Setup**
- [ ] Server is running (`python manage.py runserver`)
- [ ] Database is migrated (`python manage.py migrate`)
- [ ] Superuser exists (`python manage.py createsuperuser`)
- [ ] Sample data exists (run `create_sample_posts.py`)

### **JWT Authentication**
- [ ] User registration works
- [ ] User login works
- [ ] Token refresh works
- [ ] Protected endpoints require authentication
- [ ] Invalid tokens are rejected

### **AJAX Functionality**
- [ ] Like/unlike posts works
- [ ] Comments can be added
- [ ] Search functionality works
- [ ] Pagination works
- [ ] Error messages are displayed

### **Frontend Features**
- [ ] Navigation works on all pages
- [ ] Forms submit correctly
- [ ] Responsive design works
- [ ] No JavaScript errors in console
- [ ] All links work correctly

### **API Endpoints**
- [ ] All CRUD operations work
- [ ] Search and filtering work
- [ ] Pagination works
- [ ] Error handling is proper
- [ ] Response format is correct

### **Security**
- [ ] Authentication is required for protected endpoints
- [ ] CSRF protection works
- [ ] Input validation prevents XSS
- [ ] SQL injection is prevented
- [ ] Sensitive data is not exposed

## 🎯 Quick Test Commands

```bash
# 1. Start server
python manage.py runserver

# 2. Run automated tests
python test_jwt_ajax.py

# 3. Test frontend (manual)
# Open http://localhost:8000 in browser

# 4. Test API (manual)
# Use Postman or curl commands above

# 5. Check for errors
# Monitor server logs and browser console
```

## 🚨 Troubleshooting

### **Common Issues and Solutions**

1. **Server won't start**:
   ```bash
   # Check if port 8000 is in use
   netstat -an | findstr :8000
   # Kill process or use different port
   python manage.py runserver 8001
   ```

2. **Database errors**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Static files not loading**:
   ```bash
   python manage.py collectstatic
   ```

4. **Template errors**:
   - Check for missing `{% load static %}`
   - Verify template syntax
   - Check for missing template files

5. **AJAX not working**:
   - Check browser console for errors
   - Verify JavaScript files are loaded
   - Check network tab for failed requests

---

**Happy Testing! 🎉**

Your Django blog application is now ready for comprehensive testing across all features and functionality. 