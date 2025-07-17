#!/usr/bin/env python3
"""
Simple test script to verify registration functionality
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_registration():
    """Test user registration"""
    print("🧪 Testing User Registration")
    print("="*50)
    
    # Test data
    test_user = {
        "username": "testuser123",
        "email": "test123@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        # Test registration
        response = requests.post(f"{BASE_URL}/api/register/", json=test_user)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            data = response.json()
            print(f"User ID: {data.get('user', {}).get('id')}")
            print(f"Username: {data.get('user', {}).get('username')}")
            print(f"Access Token: {data.get('access', '')[:20]}...")
            return data.get('access')
        else:
            print("❌ Registration failed")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_login():
    """Test user login"""
    print("\n🔐 Testing User Login")
    print("="*50)
    
    login_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            data = response.json()
            print(f"User: {data.get('user', {}).get('username')}")
            print(f"Access Token: {data.get('access', '')[:20]}...")
            return data.get('access')
        else:
            print("❌ Login failed")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_homepage():
    """Test homepage loads correctly"""
    print("\n🏠 Testing Homepage")
    print("="*50)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Homepage loads successfully!")
            
            # Check if registration buttons are present
            content = response.text
            if "Register" in content and "Login" in content:
                print("✅ Registration/Login buttons found on homepage!")
            else:
                print("❌ Registration/Login buttons not found")
                
        else:
            print("❌ Homepage failed to load")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Registration and Homepage Tests")
    print("="*60)
    
    # Test homepage first
    test_homepage()
    
    # Test registration
    token = test_registration()
    
    # Test login
    if token:
        test_login()
    
    print("\n" + "="*60)
    print("🎉 Tests completed!")
    print("="*60)
    
    print("\n📋 Manual Testing Steps:")
    print("1. Visit http://localhost:8000")
    print("2. Look for the 'Register' and 'Login' buttons")
    print("3. Click 'Register' to test registration")
    print("4. Click 'Login' to test login")
    print("5. Try creating a blog post after login")

if __name__ == "__main__":
    main() 