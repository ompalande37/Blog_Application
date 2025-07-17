#!/usr/bin/env python3
"""
API Testing Script for Django Blog Application
This script tests all the REST API endpoints to ensure they're working correctly.
"""

import requests
import json
import time

# API Base URL
BASE_URL = "http://localhost:8000/api"

def print_response(response, title):
    """Print formatted API response"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"URL: {response.url}")
    
    if response.headers.get('content-type', '').startswith('application/json'):
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except:
            print(f"Response: {response.text}")
    else:
        print(f"Response: {response.text[:200]}...")

def test_authentication():
    """Test JWT authentication endpoints"""
    print("\n🔐 Testing Authentication Endpoints")
    
    # Test token endpoint
    token_data = {
        "username": "ompalande37@gmail.com",
        "password": "your_password_here" 
    }
    
    print("\n  Note: You'll need to replace 'your_password_here' with your actual password")
    print("   or create a test user in the admin panel first.")
    
    response = requests.post(f"{BASE_URL}/token/", json=token_data)
    print_response(response, "Get JWT Token")
    
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get('access')
        refresh_token = token_info.get('refresh')
        
        # Test refresh token
        refresh_data = {"refresh": refresh_token}
        response = requests.post(f"{BASE_URL}/token/refresh/", json=refresh_data)
        print_response(response, "Refresh JWT Token")
        
        return access_token
    else:
        print("❌ Authentication failed. Please check your credentials.")
        return None

def test_blog_posts_api(access_token=None):
    """Test blog posts API endpoints"""
    print("\n Testing Blog Posts API")
    
    headers = {}
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'
    
    # Test list posts
    response = requests.get(f"{BASE_URL}/posts/")
    print_response(response, "List Blog Posts")
    
    if response.status_code == 200:
        posts = response.json()
        if posts.get('results'):
            first_post = posts['results'][0]
            post_id = first_post['id']
            
            # Test get single post
            response = requests.get(f"{BASE_URL}/posts/{post_id}/")
            print_response(response, f"Get Single Post (ID: {post_id})")
            
            # Test post comments
            response = requests.get(f"{BASE_URL}/posts/{post_id}/comments/")
            print_response(response, f"Get Post Comments (ID: {post_id})")
            
            # Test like post (if authenticated)
            if access_token:
                response = requests.post(f"{BASE_URL}/posts/{post_id}/like/", headers=headers)
                print_response(response, f"Like Post (ID: {post_id})")
                
                # Test add comment (if authenticated)
                comment_data = {"content": "This is a test comment via API!"}
                response = requests.post(f"{BASE_URL}/posts/{post_id}/add_comment/", 
                                      json=comment_data, headers=headers)
                print_response(response, f"Add Comment to Post (ID: {post_id})")
            
            return post_id
    else:
        print("❌ Failed to get posts list")
        return None

def test_comments_api(access_token=None):
    """Test comments API endpoints"""
    print("\n💬 Testing Comments API")
    
    headers = {}
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'
    
    # Test list comments
    response = requests.get(f"{BASE_URL}/comments/")
    print_response(response, "List Comments")
    
    if response.status_code == 200:
        comments = response.json()
        if comments.get('results') and comments['results']:
            first_comment = comments['results'][0]
            comment_id = first_comment['id']
            
            # Test get single comment
            response = requests.get(f"{BASE_URL}/comments/{comment_id}/")
            print_response(response, f"Get Single Comment (ID: {comment_id})")
            
            # Test update comment (if authenticated)
            if access_token:
                update_data = {"content": "Updated comment via API!"}
                response = requests.put(f"{BASE_URL}/comments/{comment_id}/", 
                                     json=update_data, headers=headers)
                print_response(response, f"Update Comment (ID: {comment_id})")
            
            return comment_id
    else:
        print("❌ Failed to get comments list")
        return None

def test_likes_api(access_token=None):
    """Test likes API endpoints"""
    print("\n❤️  Testing Likes API")
    
    headers = {}
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'
    
    # Test list likes
    response = requests.get(f"{BASE_URL}/likes/", headers=headers)
    print_response(response, "List Likes")
    
    if response.status_code == 200:
        likes = response.json()
        if likes.get('results') and likes['results']:
            first_like = likes['results'][0]
            like_id = first_like['id']
            
            # Test get single like
            response = requests.get(f"{BASE_URL}/likes/{like_id}/", headers=headers)
            print_response(response, f"Get Single Like (ID: {like_id})")
            
            return like_id
    else:
        print("❌ Failed to get likes list or authentication required")
        return None

def test_search_and_filtering():
    """Test search and filtering functionality"""
    print("\n🔍 Testing Search and Filtering")
    
    # Test search
    response = requests.get(f"{BASE_URL}/posts/?search=django")
    print_response(response, "Search Posts (keyword: django)")
    
    # Test ordering
    response = requests.get(f"{BASE_URL}/posts/?ordering=-timestamp")
    print_response(response, "Order Posts by Latest First")
    
    # Test pagination
    response = requests.get(f"{BASE_URL}/posts/?page=1")
    print_response(response, "Get First Page of Posts")

def test_error_handling():
    """Test error handling"""
    print("\n⚠️  Testing Error Handling")
    
    # Test non-existent post
    response = requests.get(f"{BASE_URL}/posts/99999/")
    print_response(response, "Get Non-existent Post")
    
    # Test invalid comment
    response = requests.post(f"{BASE_URL}/posts/1/add_comment/", 
                           json={"content": ""})
    print_response(response, "Add Empty Comment (should fail)")

def main():
    """Main testing function"""
    print("🚀 Django Blog API Testing")
    print("=" * 50)
    
    # Test authentication
    access_token = test_authentication()
    
    # Test blog posts API
    post_id = test_blog_posts_api(access_token)
    
    # Test comments API
    comment_id = test_comments_api(access_token)
    
    # Test likes API
    like_id = test_likes_api(access_token)
    
    # Test search and filtering
    test_search_and_filtering()
    
    # Test error handling
    test_error_handling()
    
    print("\n" + "="*50)
    print("🎉 API Testing Complete!")
    print("="*50)
    
    if access_token:
        print("✅ Authentication successful - All authenticated endpoints tested")
    else:
        print("⚠️  Authentication failed - Only public endpoints tested")
        print("💡 To test authenticated endpoints:")
        print("   1. Create a user in admin panel")
        print("   2. Update the credentials in this script")
        print("   3. Run the script again")
    
    print("\n📋 API Endpoints Summary:")
    print("   GET  /api/posts/              - List all posts")
    print("   POST /api/posts/              - Create new post")
    print("   GET  /api/posts/{id}/         - Get specific post")
    print("   PUT  /api/posts/{id}/         - Update post")
    print("   DELETE /api/posts/{id}/       - Delete post")
    print("   POST /api/posts/{id}/like/    - Like/unlike post")
    print("   GET  /api/posts/{id}/comments/ - Get post comments")
    print("   POST /api/posts/{id}/add_comment/ - Add comment")
    print("   GET  /api/comments/           - List all comments")
    print("   POST /api/comments/           - Create comment")
    print("   GET  /api/likes/              - List all likes")
    print("   POST /api/token/              - Get JWT token")
    print("   POST /api/token/refresh/      - Refresh JWT token")

if __name__ == "__main__":
    main() 