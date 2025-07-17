#!/usr/bin/env python3
"""
Test script to verify username display functionality
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_username_display():
    """Test username display functionality"""
    print("👤 Testing Username Display")
    print("="*50)
    
    # Test data
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    try:
        session = requests.Session()
        
        # Test homepage without login
        print("1. Testing homepage without login...")
        home_response = session.get(f"{BASE_URL}/")
        
        if home_response.status_code == 200:
            print("✅ Homepage accessible")
            if "Login" in home_response.text and "Register" in home_response.text:
                print("✅ Login/Register links visible for anonymous users")
            else:
                print("⚠️  Login/Register links not found")
        else:
            print(f"❌ Homepage not accessible: {home_response.status_code}")
        
        # Test login
        print("\n2. Testing login...")
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Check if username is displayed
            if "debuguser" in login_response.text or "Debuguser" in login_response.text:
                print("✅ Username displayed after login")
            else:
                print("⚠️  Username not found in response")
                
            # Test homepage after login
            print("\n3. Testing homepage after login...")
            home_logged_in = session.get(f"{BASE_URL}/")
            
            if home_logged_in.status_code == 200:
                print("✅ Homepage accessible after login")
                if "Welcome back" in home_logged_in.text:
                    print("✅ Welcome message found")
                else:
                    print("⚠️  Welcome message not found")
                    
                if "debuguser" in home_logged_in.text or "Debuguser" in home_logged_in.text:
                    print("✅ Username visible on homepage")
                else:
                    print("⚠️  Username not visible on homepage")
            else:
                print(f"❌ Homepage not accessible after login: {home_logged_in.status_code}")
                
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_navbar_username():
    """Test username display in navbar"""
    print("\n🧭 Testing Navbar Username Display")
    print("="*50)
    
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    try:
        session = requests.Session()
        
        # Login
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Check navbar for username
            if "debuguser" in login_response.text or "Debuguser" in login_response.text:
                print("✅ Username visible in navbar")
            else:
                print("⚠️  Username not found in navbar")
                
            # Check for dropdown menu
            if "dropdown" in login_response.text or "Logout" in login_response.text:
                print("✅ User dropdown menu found")
            else:
                print("⚠️  User dropdown menu not found")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Username Display Tests")
    print("="*60)
    
    # Test username display
    test_username_display()
    
    # Test navbar username
    test_navbar_username()
    
    print("\n" + "="*60)
    print("🎉 Tests completed!")
    print("="*60)
    
    print("\n📋 Manual Testing Steps:")
    print("1. Visit http://localhost:8000/ (should show Login/Register)")
    print("2. Login as any user")
    print("3. Check navbar - should show username")
    print("4. Check homepage - should show welcome message with username")
    print("5. Check sidebar - should show user status")
    print("6. Check blog posts - should show author names")

if __name__ == "__main__":
    main() 