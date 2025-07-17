#!/usr/bin/env python3
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_anonymous_access():
    print("🔒 Testing Anonymous Access")
    print("="*50)
    try:
        session = requests.Session()
        home_response = session.get(f"{BASE_URL}/")
        if home_response.status_code == 200:
            if "Welcome to Django Blog" in home_response.text:
                print("✅ Anonymous users see welcome page")
            else:
                print("❌ Anonymous users don't see welcome page")
        else:
            print(f"❌ Homepage not accessible: {home_response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_authenticated_access():
    print("🔓 Testing Authenticated Access")
    print("="*50)
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
    try:
        session = requests.Session()
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        if login_response.status_code == 200:
            print("✅ Login successful")
            home_response = session.get(f"{BASE_URL}/")
            if home_response.status_code == 200:
                if "Welcome back" in home_response.text:
                    print("✅ Shows blog list page")
                else:
                    print("❌ Doesn't show blog list page")
            else:
                print(f"❌ Homepage not accessible: {home_response.status_code}")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🚀 Starting Restricted Access Tests")
    print("="*60)
    test_anonymous_access()
    test_authenticated_access()
    print("\n" + "="*60)
    print("🎉 Tests completed!")
    print("="*60)

if __name__ == "__main__":
    main() 