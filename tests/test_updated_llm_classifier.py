#!/usr/bin/env python3
"""
Test the updated LLM Intent Classifier with specific intent IDs
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smartdoc.services.llm_intent_classifier import LLMIntentClassifier
from smartdoc.utils.logger import sys_logger

def test_llm_intent_classifier():
    """Test the LLM Intent Classifier with updated specific intent IDs."""

    print("🧠 Testing Updated LLM Intent Classifier")
    print("=" * 60)

    # Initialize the classifier
    classifier = LLMIntentClassifier()

    # Test cases for specific intent IDs
    test_cases = [
        "What brings you here today?",  # Should map to hpi_chief_complaint
        "How old is the patient?",      # Should map to profile_age
        "What medications is she taking?",  # Should map to meds_current_known
        "Let me listen to your heart",  # Should map to exam_cardiovascular
        "When did this start?",         # Should map to hpi_onset_duration_primary
        "Any other symptoms?",          # Should map to hpi_associated_symptoms_general
        "Tell me about her medical history",  # Should map to pmh_general
        "Check blood pressure",         # Should map to exam_vital_signs
        "Hello, good morning",          # Should map to general_greeting
        "Can you clarify that?"         # Should map to clarification
    ]

    for i, test_input in enumerate(test_cases, 1):
        print(f"\n🔍 Test Case #{i}: '{test_input}'")

        try:
            result = classifier.classify_intent(test_input)

            print(f"   Intent ID: {result.get('intent_id')}")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
            print(f"   Action Type: {result.get('action_type')}")
            print(f"   Target Details: {result.get('target_details')}")
            print(f"   Explanation: {result.get('explanation')}")

            # Verify it has the structured output
            if 'action_type' in result and 'target_details' in result:
                print("   ✅ Structured output for dialogue manager: YES")
            else:
                print("   ❌ Structured output for dialogue manager: NO")

        except Exception as e:
            print(f"   ❌ ERROR: {e}")

    print("\n" + "=" * 60)
    print("📊 Testing Complete")
    print("\n🔧 Expected Intent Mappings:")
    for intent_id in classifier.intent_categories.keys():
        action_info = classifier.intent_to_action_map.get(intent_id, {})
        print(f"   {intent_id} -> {action_info.get('action_type', 'N/A')}")

if __name__ == "__main__":
    test_llm_intent_classifier()
