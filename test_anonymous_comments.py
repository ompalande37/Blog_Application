#!/usr/bin/env python3
"""
Test script to verify anonymous comment functionality
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_anonymous_comment():
    """Test anonymous comment functionality"""
    print("👤 Testing Anonymous Comment Functionality")
    print("="*50)
    
    comment_data = {
        "content": "This is a test comment from an anonymous user!",
        "guest_name": "Test Guest"
    }
    
    try:
        # Test API comment without authentication
        print("1. Testing API comment without login...")
        api_response = requests.post(
            f"{BASE_URL}/api/posts/1/add_comment/",
            json=comment_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"API Status: {api_response.status_code}")
        
        if api_response.status_code == 201:
            print("✅ API anonymous comment successful!")
            result = api_response.json()
            print(f"Comment: {result.get('content')}")
            print(f"Guest Name: {result.get('guest_name')}")
            print(f"Display Name: {result.get('display_name')}")
        else:
            print("❌ API anonymous comment failed")
            print(f"Response: {api_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_regular_form_anonymous_comment():
    """Test regular form anonymous comment submission"""
    print("\n📝 Testing Regular Form Anonymous Comment")
    print("="*50)
    
    comment_data = {
        "comment_content": "This is a test comment via regular form from anonymous user!",
        "guest_name": "Form Guest"
    }
    
    try:
        # Test regular form submission without authentication
        print("1. Testing regular form comment without login...")
        form_response = requests.post(
            f"{BASE_URL}/post/first-blog-post/",
            data=comment_data,
            allow_redirects=True
        )
        
        print(f"Form Status: {form_response.status_code}")
        
        if form_response.status_code == 200:
            print(" Form anonymous comment successful!")
            if "Comment posted successfully" in form_response.text:
                print(" Success message found!")
            else:
                print("  No success message found")
        else:
            print(f"❌ Form anonymous comment failed: {form_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_authenticated_comment():
    """Test authenticated comment functionality"""
    print("\n🔐 Testing Authenticated Comment")
    print("="*50)
    
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    comment_data = {
        "content": "This is a test comment from authenticated user!"
    }
    
    try:
        session = requests.Session()
        
        # Login
        print("1. Logging in as debuguser...")
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Test API comment with authentication
            print("2. Testing API comment with login...")
            api_response = session.post(
                f"{BASE_URL}/api/posts/1/add_comment/",
                json=comment_data,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"API Status: {api_response.status_code}")
            
            if api_response.status_code == 201:
                print("✅ API authenticated comment successful!")
                result = api_response.json()
                print(f"Comment: {result.get('content')}")
                print(f"Author: {result.get('author', {}).get('username')}")
            else:
                print("❌ API authenticated comment failed")
                print(f"Response: {api_response.text}")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Anonymous Comment Tests")
    print("="*60)
    
    # Test anonymous API comment
    test_anonymous_comment()
    
    # Test anonymous form comment
    test_regular_form_anonymous_comment()
    
    # Test authenticated comment
    test_authenticated_comment()
    
    print("\n" + "="*60)
    print("🎉 Tests completed!")
    print("="*60)
    
    print("\n📋 Manual Testing Steps:")
    print("1. Go to any blog post without logging in")
    print("2. Try to add a comment using the form")
    print("3. Enter a name (optional) and comment")
    print("4. Check if the comment appears")
    print("5. Try commenting without entering a name (should show as Anonymous)")

if __name__ == "__main__":
    main() 