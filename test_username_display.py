#!/usr/bin/env python3
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_username_display():
    print("🔎 Testing Username Display")
    print("="*50)
    login_data = {
        "username": "debuguser",
        "password": "debugpass123"
    }
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
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=True)
        if login_response.status_code == 200:
            print("✅ Login successful")
            if "debuguser" in login_response.text or "Debuguser" in login_response.text:
                print("✅ Username displayed after login")
            else:
                print("❌ Username not displayed after login")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🚀 Starting Username Display Test")
    print("="*60)
    test_username_display()
    print("\n" + "="*60)
    print("🎉 Test completed!")
    print("="*60)

if __name__ == "__main__":
    main() 