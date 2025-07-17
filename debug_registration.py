#!/usr/bin/env python3
"""
Debug script to identify registration issues
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def debug_registration():
    """Debug registration with detailed error information"""
    print("🔍 Debugging Registration Issue")
    print("="*50)
    
    # Test with minimal data first
    test_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    print("Testing with minimal data:")
    print(f"Data: {test_data}")
    
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=test_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("Could not parse error response as JSON")
        
    except Exception as e:
        print(f"Exception: {e}")
    
    print("\n" + "="*50)
    print("Testing with full data:")
    
    # Test with full data
    full_data = {
        "username": "debuguser2",
        "email": "debug@example.com",
        "password": "debugpass123",
        "first_name": "Debug",
        "last_name": "User"
    }
    
    print(f"Data: {full_data}")
    
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=full_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            data = response.json()
            print(f"User created: {data.get('user', {}).get('username')}")
        elif response.status_code == 400:
            try:
                error_data = response.json()
                print(f"Validation errors: {json.dumps(error_data, indent=2)}")
            except:
                print("Could not parse error response as JSON")
        
    except Exception as e:
        print(f"Exception: {e}")

def debug_login():
    """Debug login functionality"""
    print("\n🔍 Debugging Login Issue")
    print("="*50)
    
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    
    print(f"Login data: {login_data}")
    
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
        elif response.status_code == 401:
            print("❌ Login failed - Invalid credentials")
        elif response.status_code == 400:
            print("❌ Login failed - Bad request")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("Could not parse error response as JSON")
        
    except Exception as e:
        print(f"Exception: {e}")

def test_frontend_registration():
    """Test the frontend registration form"""
    print("\n🌐 Testing Frontend Registration")
    print("="*50)
    
    try:
        # Get the registration page
        response = requests.get(f"{BASE_URL}/register/")
        print(f"Registration page status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Registration page loads successfully")
            
            # Check if the form is present
            content = response.text
            if 'id="register-form"' in content:
                print("✅ Registration form found")
            else:
                print("❌ Registration form not found")
                
            if 'name="username"' in content and 'name="password"' in content:
                print("✅ Username and password fields found")
            else:
                print("❌ Required form fields missing")
        else:
            print("❌ Registration page failed to load")
            
    except Exception as e:
        print(f"Exception: {e}")

def main():
    """Main debug function"""
    print("🚀 Starting Registration Debug")
    print("="*60)
    
    # Test frontend first
    test_frontend_registration()
    
    # Debug registration
    debug_registration()
    
    # Debug login
    debug_login()
    
    print("\n" + "="*60)
    print("🔧 Debug Summary")
    print("="*60)
    print("1. Check if registration page loads")
    print("2. Check if form fields are present")
    print("3. Check API endpoint responses")
    print("4. Check for validation errors")
    print("5. Check for server errors")

if __name__ == "__main__":
    main() 