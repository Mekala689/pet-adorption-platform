#!/usr/bin/env python
"""
Test script to verify the Pet Adoption Platform is working correctly
"""
import requests
import sys

def test_url(url, description):
    """Test if a URL returns a successful response"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {description}: OK")
            return True
        else:
            print(f"❌ {description}: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {description}: {e}")
        return False

def main():
    """Test main platform URLs"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Pet Adoption Platform...")
    print("=" * 50)
    
    tests = [
        (f"{base_url}/", "Home Page"),
        (f"{base_url}/pets/", "Pet Listings"),
        (f"{base_url}/about/", "About Page"),
        (f"{base_url}/contact/", "Contact Page"),
        (f"{base_url}/users/login/", "Login Page"),
        (f"{base_url}/users/register/", "Registration Page"),
        (f"{base_url}/admin/", "Admin Panel"),
    ]
    
    passed = 0
    total = len(tests)
    
    for url, description in tests:
        if test_url(url, description):
            passed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Platform is working correctly.")
        print("\n🔗 Quick Links:")
        print(f"   • Home: {base_url}/")
        print(f"   • Browse Pets: {base_url}/pets/")
        print(f"   • Admin Panel: {base_url}/admin/")
        print("\n🔑 Login Credentials:")
        print("   • Admin: admin / admin123")
        print("   • Shelter: happypaws_shelter / shelter123")
        print("   • Adopter: john_doe / adopter123")
    else:
        print("⚠️  Some tests failed. Please check the server logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
