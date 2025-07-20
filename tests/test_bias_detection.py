#!/usr/bin/env python3
"""
Test script for cognitive bias detection system
"""

import requests
import time
import json

def test_bias_detection():
    """Test the cognitive bias detection system with various scenarios"""

    base_url = "http://localhost:8080"

    print("🧠 Testing Cognitive Bias Detection System")
    print("=" * 50)

    # Test 1: Anchoring Bias Detection
    print("\n📍 Test 1: Anchoring Bias Detection")
    print("Asking multiple heart failure related questions...")

    heart_failure_questions = [
        "Does the patient have chest pain?",
        "Is there shortness of breath?",
        "Any swelling in legs?",
        "History of heart disease?",
        "Taking heart medications?",
        "Previous heart attack?"
    ]

    session = requests.Session()

    for i, question in enumerate(heart_failure_questions):
        response = session.get(f"{base_url}/get", params={"msg": question})
        data = response.json()

        print(f"Q{i+1}: {question}")
        print(f"Response: {data.get('response', 'No response')[:100]}...")

        if data.get('bias_warning') and data['bias_warning'].get('show'):
            print(f"🚨 BIAS DETECTED: {data['bias_warning']['type']}")
            print(f"   Message: {data['bias_warning']['message']}")
        else:
            print("   No bias warning")
        print()

        time.sleep(1)  # Small delay between requests

    # Test 2: Quick closure detection
    print("\n⚡ Test 2: Premature Closure Detection")
    print("Starting new session with few questions...")

    # Start fresh session
    session = requests.Session()

    quick_questions = [
        "What brings you here today?",
        "Any chest pain?",
        "We should run some tests"
    ]

    for i, question in enumerate(quick_questions):
        response = session.get(f"{base_url}/get", params={"msg": question})
        data = response.json()

        print(f"Q{i+1}: {question}")

        if data.get('bias_warning') and data['bias_warning'].get('show'):
            print(f"🚨 BIAS DETECTED: {data['bias_warning']['type']}")
            print(f"   Message: {data['bias_warning']['message']}")
        else:
            print("   No bias warning")
        print()

    print("✅ Bias detection testing completed!")
    print("\nTo manually test in browser:")
    print("1. Open http://localhost:8080")
    print("2. Ask 6+ heart failure related questions to trigger anchoring bias")
    print("3. Or ask very few questions (<8) to trigger premature closure bias")

if __name__ == "__main__":
    test_bias_detection()
