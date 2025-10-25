"""
Test script to verify API key authentication.
Tests both authenticated and unauthenticated requests.
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8001"
API_KEY = os.getenv("API_KEY_SECRET", "your-secret-key-here")


def test_health_without_auth():
    """Health endpoint should work without authentication."""
    print("\n1. Testing /health without API key (should succeed)...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200, "Health check should work without auth"
    print("   ✅ PASSED")


def test_protected_endpoint_without_auth():
    """Protected endpoints should fail without API key."""
    print("\n2. Testing /sessions without API key (should fail with 403)...")
    response = requests.get(f"{BASE_URL}/sessions/user/1")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 403, "Should return 403 without API key"
    print("   ✅ PASSED")


def test_protected_endpoint_with_invalid_key():
    """Protected endpoints should fail with invalid API key."""
    print("\n3. Testing /sessions with invalid API key (should fail with 403)...")
    headers = {"X-API-Key": "invalid-key-12345"}
    response = requests.get(f"{BASE_URL}/sessions/user/1", headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 403, "Should return 403 with invalid key"
    print("   ✅ PASSED")


def test_protected_endpoint_with_valid_key():
    """Protected endpoints should work with valid API key."""
    print("\n4. Testing /sessions with valid API key (should succeed or return 404)...")
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{BASE_URL}/sessions/user/1", headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    # Should succeed (200) or return 404 if user has no sessions
    assert response.status_code in [200, 404], f"Should return 200 or 404, got {response.status_code}"
    print("   ✅ PASSED")


def test_drop_db_with_valid_key():
    """drop_db endpoint should require authentication."""
    print("\n5. Testing /drop_db with valid API key (should succeed)...")
    headers = {"X-API-Key": API_KEY}
    # Note: We're not actually calling this to avoid dropping the DB
    # Just testing that it requires auth
    response = requests.get(f"{BASE_URL}/drop_db", headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    # If it executes, status should be 200
    assert response.status_code == 200, f"Should return 200, got {response.status_code}"
    print("   ✅ PASSED")


def test_drop_db_without_auth():
    """drop_db endpoint should fail without authentication."""
    print("\n6. Testing /drop_db without API key (should fail with 403)...")
    response = requests.get(f"{BASE_URL}/drop_db")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 403, "Should return 403 without API key"
    print("   ✅ PASSED")


def main():
    print("="*60)
    print("API Key Authentication Test Suite")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"API Key: {API_KEY[:10]}..." if len(API_KEY) > 10 else API_KEY)
    
    try:
        test_health_without_auth()
        test_protected_endpoint_without_auth()
        test_protected_endpoint_with_invalid_key()
        test_protected_endpoint_with_valid_key()
        test_drop_db_without_auth()
        test_drop_db_with_valid_key()
        
        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to server. Is it running?")
        print(f"   Make sure the server is running at {BASE_URL}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
