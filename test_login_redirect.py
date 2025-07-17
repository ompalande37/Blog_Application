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
    
    print("Testing regular form login:")
    print(f"Login data: {login_data}")
    
    try:
        # Test regular form submission
        response = requests.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=False)
        
        print(f"Status Code: {response.status_code}")
        print(f"Location Header: {response.headers.get('Location', 'None')}")
        
        if response.status_code == 302:
            redirect_url = response.headers.get('Location')
            if redirect_url == '/':
                print("✅ Login redirect working correctly!")
                print(f"Redirected to: {redirect_url}")
            else:
                print(f"❌ Unexpected redirect: {redirect_url}")
        elif response.status_code == 200:
            print("❌ Login failed - no redirect")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_login():
    """Test API login functionality"""
    print("\n🔐 Testing API Login")
    print("="*50)
    
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API login successful!")
            print(f"User: {data.get('user', {}).get('username')}")
            print(f"Access Token: {data.get('access', '')[:20]}...")
        else:
            print("❌ API login failed")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_homepage_after_login():
    """Test homepage after login"""
    print("\n🏠 Testing Homepage After Login")
    print("="*50)
    
    try:
        # First login
        login_data = {
            "username": "debuguser",
            "password": "debugpass123"
        }
        
        session = requests.Session()
        
        # Login
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Check homepage
            homepage_response = session.get(f"{BASE_URL}/")
            
            if homepage_response.status_code == 200:
                content = homepage_response.text
                if "Welcome back" in content or "debuguser" in content:
                    print("✅ Homepage shows logged-in user")
                else:
                    print("❌ Homepage doesn't show logged-in user")
            else:
                print(f"❌ Homepage failed to load: {homepage_response.status_code}")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Login Redirect Tests")
    print("="*60)
    
    # Test API login
    test_api_login()
    
    # Test regular form login
    test_login_redirect()
    
    # Test homepage after login
    test_homepage_after_login()
    
    print("\n" + "="*60)
    print("🎉 Tests completed!")
    print("="*60)
    
    print("\n📋 Manual Testing Steps:")
    print("1. Visit http://localhost:8000/login/")
    print("2. Fill in username: debuguser, password: debugpass123")
    print("3. Click Login")
    print("4. Should redirect to homepage")
    print("5. Check if user is logged in on homepage")

if __name__ == "__main__":
    main() 