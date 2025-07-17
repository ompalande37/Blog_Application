# JWT Authentication and AJAX Guide

## Overview

This guide covers the JWT (JSON Web Token) authentication system and AJAX functionality implemented in the Django blog application.

## 🔐 JWT Authentication

### What is JWT?

JSON Web Tokens (JWT) are a secure way to authenticate API requests. They are:
- **Stateless**: No server-side session storage needed
- **Secure**: Cryptographically signed tokens
- **Scalable**: Works well with microservices
- **Flexible**: Can contain custom claims

### JWT Flow

1. **User Registration**: User creates account → receives access + refresh tokens
2. **User Login**: User authenticates → receives new access + refresh tokens
3. **API Requests**: Include access token in Authorization header
4. **Token Refresh**: Use refresh token to get new access token when expired

### API Endpoints

#### Authentication Endpoints

```bash
# User Registration
POST /api/register/
{
    "username": "your_username",
    "email": "your_email@example.com",
    "password": "your_password",
    "first_name": "Your",
    "last_name": "Name"
}

# User Login
POST /api/login/
{
    "username": "your_username",
    "password": "your_password"
}

# Token Refresh
POST /api/token/refresh/
{
    "refresh": "your_refresh_token"
}

# Standard JWT Token (Django REST Framework)
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

#### Response Format

```json
{
    "user": {
        "id": 1,
        "username": "your_username",
        "email": "your_email@example.com",
        "first_name": "Your",
        "last_name": "Name"
    },
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Using JWT Tokens

#### In API Requests

```javascript
// Include token in headers
const headers = {
    'Authorization': 'Bearer your_access_token',
    'Content-Type': 'application/json'
};

// Example request
fetch('/api/posts/', {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(postData)
});
```

#### Token Storage

```javascript
// Store token in localStorage
localStorage.setItem('access_token', token);

// Retrieve token
const token = localStorage.getItem('access_token');

// Remove token on logout
localStorage.removeItem('access_token');
```

## ⚡ AJAX Functionality

### Features Implemented

1. **Like/Unlike Posts**: Real-time like functionality
2. **Comment System**: Add comments without page reload
3. **Search**: Dynamic search with instant results
4. **Pagination**: Load more posts dynamically
5. **User Authentication**: Login/register via AJAX
6. **Error Handling**: User-friendly error messages

### AJAX Class Structure

```javascript
class BlogAJAX {
    constructor() {
        this.baseURL = '/api/';
        this.token = localStorage.getItem('access_token');
        this.setupEventListeners();
    }
    
    // Methods for different functionalities
    handleLike(event) { /* ... */ }
    handleComment(event) { /* ... */ }
    handleSearch(event) { /* ... */ }
    handleLogin(event) { /* ... */ }
    handleRegister(event) { /* ... */ }
}
```

### Event Listeners

The AJAX class automatically sets up event listeners for:

- **Like buttons**: `.like-btn` class
- **Comment forms**: `.comment-form` class
- **Search forms**: `#search-form` ID
- **Login forms**: `#login-form` ID
- **Register forms**: `#register-form` ID

### Like Functionality

#### HTML Structure

```html
<button class="like-btn" data-post-id="{{ post.id }}">
    <i class="far fa-heart"></i>
    <span class="like-count">{{ post.likes_count }}</span>
</button>
```

#### JavaScript Handling

```javascript
async handleLike(event) {
    const button = event.target;
    const postId = button.dataset.postId;
    
    const response = await fetch(`${this.baseURL}posts/${postId}/like/`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
    });
    
    if (response.ok) {
        const data = await response.json();
        // Update button appearance
        // Show success message
    }
}
```

### Comment Functionality

#### HTML Structure

```html
<form class="comment-form" data-post-id="{{ post.id }}">
    <textarea name="content" required></textarea>
    <button type="submit">Add Comment</button>
</form>
<div class="comments-container">
    <!-- Comments will be dynamically added here -->
</div>
```

#### JavaScript Handling

```javascript
async handleComment(event) {
    const form = event.target;
    const postId = form.dataset.postId;
    const content = form.querySelector('textarea[name="content"]').value;
    
    const response = await fetch(`${this.baseURL}posts/${postId}/add_comment/`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ content: content })
    });
    
    if (response.ok) {
        const data = await response.json();
        // Add comment to page
        // Clear form
        // Update comment count
    }
}
```

### Search Functionality

#### HTML Structure

```html
<form id="search-form">
    <input type="text" name="search" placeholder="Search posts...">
    <button type="submit">Search</button>
</form>
<div id="search-results">
    <!-- Search results will appear here -->
</div>
```

#### JavaScript Handling

```javascript
async handleSearch(event) {
    const form = event.target;
    const query = form.querySelector('input[name="search"]').value;
    
    const response = await fetch(`${this.baseURL}posts/?search=${encodeURIComponent(query)}`);
    
    if (response.ok) {
        const data = await response.json();
        this.updateSearchResults(data.results);
    }
}
```

### Authentication via AJAX

#### Login Form

```html
<form id="login-form">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <button type="submit">Login</button>
</form>
```

#### JavaScript Handling

```javascript
async handleLogin(event) {
    const form = event.target;
    const formData = new FormData(form);
    
    const response = await fetch('/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: formData.get('username'),
            password: formData.get('password')
        })
    });
    
    if (response.ok) {
        const result = await response.json();
        this.setToken(result.access);
        this.showMessage('Login successful!', 'success');
        // Redirect or update UI
    }
}
```

## 🛠️ Implementation Details

### Backend Components

#### Views (`blog/views.py`)

```python
class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
```

#### Serializers (`blog/serializers.py`)

```python
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
```

#### URLs (`blog/urls.py`)

```python
urlpatterns = [
    # API URLs
    path('api/register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('api/login/', views.UserLoginView.as_view(), name='user_login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Frontend URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='user_logout'),
    path('register/', views.RegisterView.as_view(), name='user_register'),
]
```

### Frontend Components

#### Templates

- `templates/registration/login.html`: Login form with AJAX
- `templates/registration/register.html`: Registration form with AJAX
- `templates/base.html`: Includes AJAX JavaScript

#### JavaScript

- `static/js/ajax.js`: Main AJAX functionality class

## 🧪 Testing

### Running Tests

```bash
# Test JWT and AJAX functionality
python test_jwt_ajax.py

# Test basic API functionality
python test_api.py
```

### Manual Testing

1. **Registration**: Visit `/register/` and create a new account
2. **Login**: Visit `/login/` and authenticate
3. **API Testing**: Use the test scripts or tools like Postman
4. **Frontend Testing**: Test like/comment functionality on blog posts

### Test Endpoints

```bash
# Test registration
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123", "email": "test@example.com"}'

# Test login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# Test protected endpoint
curl -X GET http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer your_access_token"
```

## 🔒 Security Considerations

### JWT Security

1. **Token Expiration**: Access tokens expire in 1 hour
2. **Refresh Tokens**: Valid for 1 day
3. **HTTPS**: Always use HTTPS in production
4. **Token Storage**: Store in localStorage (consider httpOnly cookies for production)

### AJAX Security

1. **CSRF Protection**: Django's built-in CSRF protection
2. **Input Validation**: Server-side validation for all inputs
3. **XSS Protection**: Sanitize user inputs
4. **Rate Limiting**: Implement rate limiting for API endpoints

## 🚀 Next Steps

### Potential Enhancements

1. **Password Reset**: Implement password reset functionality
2. **Email Verification**: Add email verification for new accounts
3. **Social Authentication**: Add OAuth providers (Google, Facebook, etc.)
4. **Two-Factor Authentication**: Implement 2FA for enhanced security
5. **Token Blacklisting**: Implement token blacklisting for logout
6. **Real-time Updates**: Add WebSocket support for real-time features
7. **Advanced Search**: Implement Elasticsearch for better search
8. **File Upload**: Add image upload functionality for posts

### Production Considerations

1. **Environment Variables**: Move sensitive settings to environment variables
2. **Database Optimization**: Optimize database queries and add indexes
3. **Caching**: Implement Redis caching for better performance
4. **CDN**: Use CDN for static files
5. **Monitoring**: Add application monitoring and logging
6. **Backup Strategy**: Implement database backup strategy

## 📚 Additional Resources

- [Django REST Framework JWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
- [JWT.io](https://jwt.io/) - JWT debugger and documentation
- [MDN AJAX Guide](https://developer.mozilla.org/en-US/docs/Web/Guide/AJAX)
- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)

---

This guide covers the complete JWT authentication and AJAX functionality implementation. The system provides a secure, scalable foundation for the blog application with modern web development practices. 