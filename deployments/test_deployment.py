#!/usr/bin/env python3
"""
Test script to verify deployment configuration
"""

import requests
import sys
import time

def test_api_health(base_url="http://localhost:8000"):
    """Test API health endpoints"""
    print(f"🏥 Testing API health at {base_url}")

    try:
        # Test /health endpoint
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ /health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ /health endpoint failed: {response.status_code}")
            return False

        # Test /healthz endpoint
        response = requests.get(f"{base_url}/healthz", timeout=5)
        if response.status_code == 200:
            print("✅ /healthz endpoint working")
        else:
            print(f"❌ /healthz endpoint failed: {response.status_code}")
            return False

        return True

    except requests.ConnectionError:
        print("❌ Cannot connect to API")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_frontend(base_url="http://localhost:8000"):
    """Test frontend availability"""
    print(f"🌐 Testing frontend at {base_url}")

    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend failed: {response.status_code}")
            return False
    except requests.ConnectionError:
        print("❌ Cannot connect to frontend")
        return False
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
        return False

def test_api_proxy(base_url="http://localhost:8000"):
    """Test API proxy through Nginx"""
    print(f"🔄 Testing API proxy at {base_url}/api")

    try:
        response = requests.get(f"{base_url}/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ API proxy working through Nginx")
            return True
        else:
            print(f"❌ API proxy failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing API proxy: {e}")
        return False

def main():
    """Run all deployment tests"""
    print("🧪 SmartDoc Deployment Test Suite")
    print("=" * 40)

    # Wait a moment for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(3)

    all_passed = True

    # Test direct API access
    if not test_api_health():
        all_passed = False

    print()

    # Test frontend
    if not test_frontend():
        all_passed = False

    print()

    # Test API through proxy
    if not test_api_proxy():
        all_passed = False

    print()
    print("=" * 40)

    if all_passed:
        print("🎉 All tests passed! Deployment is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the logs and configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()
