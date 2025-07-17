#!/usr/bin/env python3
"""
Test script to verify login redirect functionality
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_login_redirect():
    """Test login redirect functionality"""
    print("🔐 Testing Login Redirect")
    print("="*50)
    
    # Test data
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    try:
        session = requests.Session()
        
        # First, check what anonymous users see
        print("1. Checking anonymous user view...")
        home_response = session.get(f"{BASE_URL}/")
        
        if home_response.status_code == 200:
            if "Welcome to Django Blog" in home_response.text:
                print("✅ Anonymous users see welcome page")
            else:
                print("❌ Anonymous users don't see welcome page")
        else:
            print(f"❌ Homepage not accessible: {home_response.status_code}")
        
        # Now test login
        print("\n2. Testing login...")
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Check if we're redirected to the blog list
            if "Welcome back" in login_response.text:
                print("✅ Redirected to blog list page")
            else:
                print("❌ Not redirected to blog list page")
                
            # Check if blog posts are visible
            if "blog-post" in login_response.text or "post-meta" in login_response.text:
                print("✅ Blog posts are visible after login")
            else:
                print("❌ Blog posts not visible after login")
                
            # Check if user info is displayed
            if "debuguser" in login_response.text or "Debuguser" in login_response.text:
                print("✅ User info displayed after login")
            else:
                print("❌ User info not displayed after login")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_direct_homepage_access():
    """Test direct homepage access after login"""
    print("\n🏠 Testing Direct Homepage Access After Login")
    print("="*50)
    
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    try:
        session = requests.Session()
        
        # Login first
        print("1. Logging in...")
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Now access homepage directly
            print("2. Accessing homepage directly...")
            home_response = session.get(f"{BASE_URL}/")
            
            if home_response.status_code == 200:
                print("✅ Homepage accessible after login")
                
                # Check if it shows blog posts
                if "Welcome back" in home_response.text:
                    print("✅ Shows blog list page")
                else:
                    print("❌ Doesn't show blog list page")
                    
                # Check for blog posts
                if "blog-post" in home_response.text or "post-meta" in home_response.text:
                    print("✅ Blog posts visible")
                else:
                    print("❌ Blog posts not visible")
            else:
                print(f"❌ Homepage not accessible: {home_response.status_code}")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Login Redirect Tests")
    print("="*60)
    
    # Test login redirect
    test_login_redirect()
    
    # Test direct homepage access
    test_direct_homepage_access()
    
    print("\n" + "="*60)
    print("🎉 Tests completed!")
    print("="*60)
    
    print("\n📋 Manual Testing Steps:")
    print("1. Visit http://localhost:8000/ (should show welcome page)")
    print("2. Click 'Login' button")
    print("3. Enter credentials and submit")
    print("4. Should redirect to homepage with blog posts visible")
    print("5. Check that user info is displayed")

if __name__ == "__main__":
    main() 