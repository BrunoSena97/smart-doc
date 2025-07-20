#!/usr/bin/env python3
"""
Test the improved premature closure detection that looks for actual conclusion attempts
"""

import requests
import time

def test_realistic_premature_closure():
    """Test premature closure detection with realistic clinical scenarios"""

    base_url = "http://localhost:8080"

    print("🧠 Testing Realistic Premature Closure Detection")
    print("=" * 60)

    # Test 1: Premature Diagnosis Attempt
    print("\n⚡ Test 1: Premature Diagnosis (Should Trigger Warning)")
    print("Doctor tries to diagnose without proper assessment...")

    session = requests.Session()

    premature_scenario = [
        "What brings you here today?",
        "Any chest pain?",
        "I think you have heart failure, let's start treatment with Lisinopril"
    ]

    for i, question in enumerate(premature_scenario):
        response = session.get(f"{base_url}/get", params={"msg": question})
        data = response.json()

        print(f"Q{i+1}: {question}")
        print(f"Response: {data.get('response', 'No response')[:80]}...")

        if data.get('bias_warning') and data['bias_warning'].get('show'):
            print(f"🚨 BIAS DETECTED: {data['bias_warning']['type']}")
            print(f"   Message: {data['bias_warning']['message']}")
        else:
            print("   ✅ No bias warning")
        print()

        time.sleep(0.5)

    # Test 2: Proper Investigation (Should NOT Trigger Warning)
    print("\n✅ Test 2: Thorough Assessment (Should NOT Trigger Warning)")
    print("Doctor conducts proper investigation before concluding...")

    session = requests.Session()

    thorough_scenario = [
        "What brings you here today?",
        "Tell me about your symptoms and when they started",
        "Can I examine your heart and lungs?",
        "Let's check your blood pressure and vital signs",
        "I'd like to order some blood tests",
        "Based on the examination and tests, you likely have heart failure"
    ]

    for i, question in enumerate(thorough_scenario):
        response = session.get(f"{base_url}/get", params={"msg": question})
        data = response.json()

        print(f"Q{i+1}: {question}")
        print(f"Response: {data.get('response', 'No response')[:80]}...")

        if data.get('bias_warning') and data['bias_warning'].get('show'):
            print(f"🚨 BIAS DETECTED: {data['bias_warning']['type']}")
            print(f"   Message: {data['bias_warning']['message']}")
        else:
            print("   ✅ No bias warning")
        print()

        time.sleep(0.5)

    # Test 3: Another Premature Scenario
    print("\n⚡ Test 3: Early Treatment Decision (Should Trigger Warning)")
    print("Doctor jumps to treatment without assessment...")

    session = requests.Session()

    early_treatment = [
        "What's wrong?",
        "Let's prescribe some medication for your condition"
    ]

    for i, question in enumerate(early_treatment):
        response = session.get(f"{base_url}/get", params={"msg": question})
        data = response.json()

        print(f"Q{i+1}: {question}")
        print(f"Response: {data.get('response', 'No response')[:80]}...")

        if data.get('bias_warning') and data['bias_warning'].get('show'):
            print(f"🚨 BIAS DETECTED: {data['bias_warning']['type']}")
            print(f"   Message: {data['bias_warning']['message']}")
        else:
            print("   ✅ No bias warning")
        print()

        time.sleep(0.5)

    print("\n" + "="*60)
    print("✅ Realistic Premature Closure Testing Complete!")
    print("\n📋 Expected Results:")
    print("- Test 1: Should trigger premature closure warning")
    print("- Test 2: Should NOT trigger warning (proper assessment)")
    print("- Test 3: Should trigger premature closure warning")
    print("\n🧠 This tests detection of ACTUAL conclusion attempts,")
    print("   not just counting questions!")

if __name__ == "__main__":
    test_realistic_premature_closure()
