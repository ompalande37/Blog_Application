#!/usr/bin/env python3
"""
Test script to verify comment functionality
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_comment_functionality():
    """Test comment functionality"""
    print("💬 Testing Comment Functionality")
    print("="*50)
    
    # Test data
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    comment_data = {
        "content": "This is a test comment from debuguser!"
    }
    
    try:
        # Create a session
        session = requests.Session()
        
        # Login
        print("1. Logging in as debuguser...")
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Get the first post
            print("2. Getting first blog post...")
            posts_response = session.get(f"{BASE_URL}/")
            
            if posts_response.status_code == 200:
                print("✅ Retrieved posts page")
                
                # Try to comment on the first post (we'll need to get a specific post)
                print("3. Testing comment submission...")
                
                # For now, let's test the API endpoint
                api_comment_response = session.post(
                    f"{BASE_URL}/api/posts/1/add_comment/",
                    json=comment_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                print(f"API Comment Status: {api_comment_response.status_code}")
                
                if api_comment_response.status_code == 201:
                    print("✅ API comment successful!")
                    result = api_comment_response.json()
                    print(f"Comment: {result.get('content')}")
                    print(f"Author: {result.get('author', {}).get('username')}")
                else:
                    print("❌ API comment failed")
                    print(f"Response: {api_comment_response.text}")
                    
            else:
                print(f"❌ Failed to get posts: {posts_response.status_code}")
                
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_regular_form_comment():
    """Test regular form comment submission"""
    print("\n📝 Testing Regular Form Comment")
    print("="*50)
    
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    comment_data = {
        "comment_content": "This is a test comment via regular form!"
    }
    
    try:
        session = requests.Session()
        
        # Login
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Try to comment on post with slug 'first-blog-post'
            comment_response = session.post(
                f"{BASE_URL}/post/first-blog-post/",
                data=comment_data,
                allow_redirects=True
            )
            
            print(f"Comment Form Status: {comment_response.status_code}")
            
            if comment_response.status_code == 200:
                print("✅ Comment form submission successful!")
                if "Comment posted successfully" in comment_response.text:
                    print("✅ Success message found!")
                else:
                    print("⚠️  No success message found")
            else:
                print(f"❌ Comment form failed: {comment_response.status_code}")
                
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Comment Tests")
    print("="*60)
    
    # Test API comment
    test_comment_functionality()
    
    # Test regular form comment
    test_regular_form_comment()
    
    print("\n" + "="*60)
    print("🎉 Tests completed!")
    print("="*60)
    
    print("\n📋 Manual Testing Steps:")
    print("1. Login as debuguser at http://localhost:8000/login/")
    print("2. Go to any blog post")
    print("3. Try to add a comment using the form")
    print("4. Check if the comment appears")
    print("5. Try commenting on another user's post")

if __name__ == "__main__":
    main() 