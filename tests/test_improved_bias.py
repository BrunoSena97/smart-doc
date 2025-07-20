#!/usr/bin/env python3
"""
Improved test script for cognitive bias detection system using properly formatted clinical questions
"""

import requests
import time
import json

def test_bias_detection_improved():
    """Test the cognitive bias detection system with properly formatted clinical questions"""

    base_url = "http://localhost:8080"

    print("🧠 Testing Cognitive Bias Detection System (Improved)")
    print("=" * 60)

    # Test 1: Anchoring Bias Detection with proper clinical questions
    print("\n📍 Test 1: Anchoring Bias Detection")
    print("Asking multiple cardiovascular-focused questions...")

    # Questions that should map to cardiovascular/heart failure intents
    cardiovascular_questions = [
        "Can you describe your chest symptoms?",
        "Do you have any chest pain or discomfort?",
        "Are you experiencing any shortness of breath?",
        "Have you noticed any swelling in your legs or feet?",
        "What cardiovascular medications are you currently taking?",
        "Can I listen to your heart?",
        "Let's get a chest X-ray to check your heart",
        "I'd like to order a BNP blood test"
    ]

    session = requests.Session()

    for i, question in enumerate(cardiovascular_questions):
        response = session.get(f"{base_url}/get", params={"msg": question})
        data = response.json()

        print(f"Q{i+1}: {question}")
        print(f"Response: {data.get('response', 'No response')[:80]}...")

        if data.get('bias_warning') and data['bias_warning'].get('show'):
            print(f"🚨 BIAS DETECTED: {data['bias_warning']['type']}")
            print(f"   Message: {data['bias_warning']['message']}")
        else:
            print("   No bias warning")
        print()

        time.sleep(0.5)  # Small delay between requests

    print("\n" + "="*60)
    print("✅ Testing completed!")
    print("\nTo manually test in browser:")
    print("1. Open http://localhost:8080")
    print("2. Ask the cardiovascular questions above to trigger anchoring bias")
    print("3. Try different types of questions to test other bias patterns")

if __name__ == "__main__":
    test_bias_detection_improved()
