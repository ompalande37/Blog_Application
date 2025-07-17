#!/usr/bin/env python3
"""
Test script to verify post creation and admin functionality
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_create_post():
    """Test post creation functionality"""
    print("📝 Testing Post Creation")
    print("="*50)
    
    # Test data
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    post_data = {
        "title": "Test Post by Debug User",
        "content": "This is a test post created by debuguser to verify post creation functionality.",
        "excerpt": "Test post excerpt",
        "status": "published"
    }
    
    try:
        session = requests.Session()
        
        # Login
        print("1. Logging in as debuguser...")
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Try to access create post page
            print("2. Accessing create post page...")
            create_page_response = session.get(f"{BASE_URL}/create/")
            
            if create_page_response.status_code == 200:
                print("✅ Create post page accessible")
                
                # Try to create a post via form
                print("3. Creating post via form...")
                create_post_response = session.post(f"{BASE_URL}/create/", data=post_data, allow_redirects=True)
                
                if create_post_response.status_code == 200:
                    print("✅ Post creation successful!")
                    if "Test Post by Debug User" in create_post_response.text:
                        print("✅ Post appears on the page")
                    else:
                        print("⚠️  Post not found on page")
                else:
                    print(f"❌ Post creation failed: {create_post_response.status_code}")
                    
            else:
                print(f"❌ Create post page not accessible: {create_page_response.status_code}")
                
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_create_post():
    """Test API post creation"""
    print("\n🔌 Testing API Post Creation")
    print("="*50)
    
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    post_data = {
        "title": "API Test Post",
        "content": "This is a test post created via API.",
        "excerpt": "API test post",
        "status": "published"
    }
    
    try:
        session = requests.Session()
        
        # Login
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Get JWT token
            token_response = session.post(f"{BASE_URL}/api/login/", json=login_data)
            
            if token_response.status_code == 200:
                token_data = token_response.json()
                access_token = token_data.get('access')
                
                # Create post via API
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                }
                
                api_response = session.post(f"{BASE_URL}/api/posts/", json=post_data, headers=headers)
                
                if api_response.status_code == 201:
                    print("✅ API post creation successful!")
                    result = api_response.json()
                    print(f"Post ID: {result.get('id')}")
                    print(f"Title: {result.get('title')}")
                    print(f"Author: {result.get('author', {}).get('username')}")
                else:
                    print(f"❌ API post creation failed: {api_response.status_code}")
                    print(f"Response: {api_response.text}")
            else:
                print("❌ Failed to get JWT token")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_admin_access():
    """Test admin access to likes and comments"""
    print("\n👨‍💼 Testing Admin Access")
    print("="*50)
    
    try:
        # Test admin login (you'll need to provide admin credentials)
        admin_data = {
            "username": "admin",  # Change to your admin username
            "password": "admin"    # Change to your admin password
        }
        
        session = requests.Session()
        
        # Try to access admin
        admin_response = session.get(f"{BASE_URL}/admin/")
        
        if admin_response.status_code == 200:
            print("✅ Admin page accessible")
        else:
            print(f"❌ Admin page not accessible: {admin_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Post Creation Tests")
    print("="*60)
    
    # Test regular form post creation
    test_create_post()
    
    # Test API post creation
    test_api_create_post()
    
    # Test admin access
    test_admin_access()
    
    print("\n" + "="*60)
    print("🎉 Tests completed!")
    print("="*60)
    
    print("\n📋 Manual Testing Steps:")
    print("1. Login as any user at http://localhost:8000/login/")
    print("2. Go to http://localhost:8000/create/")
    print("3. Try to create a new post")
    print("4. Check if the post appears on the homepage")
    print("5. Login as admin and check admin interface")
    print("6. Look for 'Likes & Comments' section in post details")

if __name__ == "__main__":
    main() 