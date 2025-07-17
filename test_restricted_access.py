#!/usr/bin/env python3
"""
Test script to verify restricted access functionality
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_anonymous_access():
    """Test what anonymous users see"""
    print("👤 Testing Anonymous User Access")
    print("="*50)
    
    try:
        session = requests.Session()
        
        # Test homepage access
        print("1. Testing homepage access...")
        home_response = session.get(f"{BASE_URL}/")
        
        if home_response.status_code == 200:
            print("✅ Homepage accessible")
            
            # Check if it's the welcome page
            if "Welcome to Django Blog" in home_response.text:
                print("✅ Welcome page displayed")
            else:
                print("❌ Welcome page not displayed")
                
            # Check for login/register buttons
            if "Register" in home_response.text and "Login" in home_response.text:
                print("✅ Login/Register buttons visible")
            else:
                print("❌ Login/Register buttons not found")
                
            # Check that no blog posts are visible
            if "blog-post" not in home_response.text and "post-meta" not in home_response.text:
                print("✅ No blog posts visible to anonymous users")
            else:
                print("❌ Blog posts are visible to anonymous users")
        else:
            print(f"❌ Homepage not accessible: {home_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_authenticated_access():
    """Test what authenticated users see"""
    print("\n🔐 Testing Authenticated User Access")
    print("="*50)
    
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    try:
        session = requests.Session()
        
        # Login
        print("1. Logging in...")
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Test homepage after login
            print("2. Testing homepage after login...")
            home_response = session.get(f"{BASE_URL}/")
            
            if home_response.status_code == 200:
                print("✅ Homepage accessible after login")
                
                # Check if it's the blog list page
                if "Welcome back" in home_response.text:
                    print("✅ Blog list page displayed")
                else:
                    print("❌ Blog list page not displayed")
                    
                # Check for blog posts
                if "blog-post" in home_response.text or "post-meta" in home_response.text:
                    print("✅ Blog posts visible to authenticated users")
                else:
                    print("❌ Blog posts not visible to authenticated users")
                    
                # Check for navigation links
                if "Create Post" in home_response.text:
                    print("✅ Create Post link visible")
                else:
                    print("❌ Create Post link not visible")
            else:
                print(f"❌ Homepage not accessible after login: {home_response.status_code}")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_blog_detail_access():
    """Test blog detail access"""
    print("\n📄 Testing Blog Detail Access")
    print("="*50)
    
    try:
        session = requests.Session()
        
        # Try to access blog detail as anonymous user
        print("1. Testing blog detail as anonymous user...")
        detail_response = session.get(f"{BASE_URL}/post/first-blog-post/", allow_redirects=False)
        
        if detail_response.status_code == 302:
            print("✅ Anonymous users redirected from blog detail")
        else:
            print(f"❌ Unexpected response: {detail_response.status_code}")
            
        # Login and try again
        login_data = {
            "username": "debuguser",
            "password": "debugpass123"
        }
        
        print("2. Testing blog detail as authenticated user...")
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            detail_response = session.get(f"{BASE_URL}/post/first-blog-post/")
            
            if detail_response.status_code == 200:
                print("✅ Authenticated users can access blog detail")
            else:
                print(f"❌ Blog detail not accessible: {detail_response.status_code}")
        else:
            print("❌ Login failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Restricted Access Tests")
    print("="*60)
    
    # Test anonymous access
    test_anonymous_access()
    
    # Test authenticated access
    test_authenticated_access()
    
    # Test blog detail access
    test_blog_detail_access()
    
    print("\n" + "="*60)
    print("🎉 Tests completed!")
    print("="*60)
    
    print("\n📋 Manual Testing Steps:")
    print("1. Visit http://localhost:8000/ (should show welcome page)")
    print("2. Check that no blog posts are visible")
    print("3. Login as any user")
    print("4. Check that blog posts are now visible")
    print("5. Try accessing blog detail without login (should redirect)")
    print("6. Try accessing blog detail with login (should work)")

if __name__ == "__main__":
    main() 