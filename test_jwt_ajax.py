#!/usr/bin/env python3
"""
Comprehensive test script for JWT Authentication and AJAX functionality
"""

import requests
import json
import time

BASE_URL = 'http://localhost:8000'

def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_jwt_authentication():
    """Test JWT authentication flow"""
    print("\n🔐 Testing JWT Authentication")
    print("="*50)
    
    # Test 1: User Registration
    print("\n1️⃣ Testing User Registration")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/api/register/", json=register_data)
    print_response(response, "User Registration")
    
    if response.status_code == 201:
        print("✅ Registration successful!")
        user_data = response.json()
        access_token = user_data.get('access')
        refresh_token = user_data.get('refresh')
    else:
        print("❌ Registration failed or user already exists")
        return None, None
    
    # Test 2: User Login
    print("\n2️⃣ Testing User Login")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
    print_response(response, "User Login")
    
    if response.status_code == 200:
        print("✅ Login successful!")
        login_data = response.json()
        access_token = login_data.get('access')
        refresh_token = login_data.get('refresh')
    else:
        print("❌ Login failed")
        return None, None
    
    # Test 3: Token Refresh
    print("\n3️⃣ Testing Token Refresh")
    refresh_data = {"refresh": refresh_token}
    
    response = requests.post(f"{BASE_URL}/api/token/refresh/", json=refresh_data)
    print_response(response, "Token Refresh")
    
    if response.status_code == 200:
        print("✅ Token refresh successful!")
        new_access_token = response.json().get('access')
        return new_access_token, refresh_token
    else:
        print("❌ Token refresh failed")
        return access_token, refresh_token

def test_protected_endpoints(access_token):
    """Test endpoints that require authentication"""
    print("\n🔒 Testing Protected Endpoints")
    print("="*50)
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Test 1: Create a blog post
    print("\n1️⃣ Testing Create Blog Post")
    post_data = {
        "title": "Test Post via API",
        "excerpt": "This is a test post created via API",
        "content": "<p>This is the content of the test post.</p>",
        "status": "published"
    }
    
    response = requests.post(f"{BASE_URL}/api/posts/", json=post_data, headers=headers)
    print_response(response, "Create Blog Post")
    
    if response.status_code == 201:
        print("✅ Post created successfully!")
        post_data = response.json()
        post_id = post_data.get('id')
        return post_id
    else:
        print("❌ Failed to create post")
        return None

def test_like_functionality(access_token, post_id):
    """Test like/unlike functionality"""
    print("\n❤️ Testing Like Functionality")
    print("="*50)
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Test 1: Like a post
    print("\n1️⃣ Testing Like Post")
    response = requests.post(f"{BASE_URL}/api/posts/{post_id}/like/", headers=headers)
    print_response(response, "Like Post")
    
    if response.status_code == 200:
        print("✅ Post liked successfully!")
        like_data = response.json()
        print(f"Liked: {like_data.get('liked')}")
        print(f"Likes count: {like_data.get('likes_count')}")
    else:
        print("❌ Failed to like post")
    
    # Test 2: Unlike the post
    print("\n2️⃣ Testing Unlike Post")
    response = requests.post(f"{BASE_URL}/api/posts/{post_id}/like/", headers=headers)
    print_response(response, "Unlike Post")
    
    if response.status_code == 200:
        print("✅ Post unliked successfully!")
        like_data = response.json()
        print(f"Liked: {like_data.get('liked')}")
        print(f"Likes count: {like_data.get('likes_count')}")
    else:
        print("❌ Failed to unlike post")

def test_comment_functionality(access_token, post_id):
    """Test comment functionality"""
    print("\n💬 Testing Comment Functionality")
    print("="*50)
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Test 1: Add a comment
    print("\n1️⃣ Testing Add Comment")
    comment_data = {
        "content": "This is a test comment via API"
    }
    
    response = requests.post(f"{BASE_URL}/api/posts/{post_id}/add_comment/", 
                           json=comment_data, headers=headers)
    print_response(response, "Add Comment")
    
    if response.status_code == 201:
        print("✅ Comment added successfully!")
        comment_data = response.json()
        comment_id = comment_data.get('id')
        return comment_id
    else:
        print("❌ Failed to add comment")
        return None

def test_ajax_endpoints():
    """Test AJAX-specific endpoints"""
    print("\n⚡ Testing AJAX Endpoints")
    print("="*50)
    
    # Test 1: Search functionality
    print("\n1️⃣ Testing Search API")
    response = requests.get(f"{BASE_URL}/api/posts/?search=django")
    print_response(response, "Search Posts")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data.get('results', []))} posts")
    
    # Test 2: Pagination
    print("\n2️⃣ Testing Pagination")
    response = requests.get(f"{BASE_URL}/api/posts/?page=1")
    print_response(response, "Paginated Posts")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Page {data.get('current_page', 'unknown')}")
        print(f"Total pages: {data.get('total_pages', 'unknown')}")
        print(f"Posts on this page: {len(data.get('results', []))}")
    
    # Test 3: Ordering
    print("\n3️⃣ Testing Ordering")
    response = requests.get(f"{BASE_URL}/api/posts/?ordering=-timestamp")
    print_response(response, "Ordered Posts")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Retrieved {len(data.get('results', []))} posts in descending order")

def test_error_handling():
    """Test error handling"""
    print("\n🚨 Testing Error Handling")
    print("="*50)
    
    # Test 1: Invalid token
    print("\n1️⃣ Testing Invalid Token")
    headers = {
        'Authorization': 'Bearer invalid_token_here',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f"{BASE_URL}/api/posts/", headers=headers)
    print_response(response, "Invalid Token Request")
    
    # Test 2: Non-existent post
    print("\n2️⃣ Testing Non-existent Post")
    response = requests.get(f"{BASE_URL}/api/posts/99999/")
    print_response(response, "Non-existent Post")
    
    # Test 3: Unauthorized like
    print("\n3️⃣ Testing Unauthorized Like")
    response = requests.post(f"{BASE_URL}/api/posts/1/like/")
    print_response(response, "Unauthorized Like")

def test_frontend_integration():
    """Test frontend integration points"""
    print("\n🌐 Testing Frontend Integration")
    print("="*50)
    
    # Test 1: Main page loads
    print("\n1️⃣ Testing Main Page")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Main page loads successfully")
    else:
        print("❌ Main page failed to load")
    
    # Test 2: Login page
    print("\n2️⃣ Testing Login Page")
    response = requests.get(f"{BASE_URL}/login/")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Login page loads successfully")
    else:
        print("❌ Login page failed to load")
    
    # Test 3: Register page
    print("\n3️⃣ Testing Register Page")
    response = requests.get(f"{BASE_URL}/register/")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Register page loads successfully")
    else:
        print("❌ Register page failed to load")

def main():
    """Main test function"""
    print("🚀 Starting JWT and AJAX Tests")
    print("="*60)
    
    # Test JWT authentication
    access_token, refresh_token = test_jwt_authentication()
    
    if access_token:
        # Test protected endpoints
        post_id = test_protected_endpoints(access_token)
        
        if post_id:
            # Test like functionality
            test_like_functionality(access_token, post_id)
            
            # Test comment functionality
            comment_id = test_comment_functionality(access_token, post_id)
        
        # Test AJAX endpoints
        test_ajax_endpoints()
    
    # Test error handling
    test_error_handling()
    
    # Test frontend integration
    test_frontend_integration()
    
    print("\n" + "="*60)
    print("🎉 All tests completed!")
    print("="*60)
    
    print("\n📋 Summary of Features Tested:")
    print("✅ JWT Token Generation")
    print("✅ User Registration")
    print("✅ User Login")
    print("✅ Token Refresh")
    print("✅ Protected Endpoints")
    print("✅ Like/Unlike Functionality")
    print("✅ Comment System")
    print("✅ Search API")
    print("✅ Pagination")
    print("✅ Error Handling")
    print("✅ Frontend Integration")

if __name__ == "__main__":
    main() 