#!/usr/bin/env python3
"""
Test script for the new LLM Discovery Processor integration
"""

from smartdoc.ai.discovery_processor import LLMDiscoveryProcessor

def test_discovery_processor():
    """Test the LLM Discovery Processor functionality."""

    print("🔍 Testing LLM Discovery Processor Integration")
    print("=" * 50)

    # Initialize processor
    processor = LLMDiscoveryProcessor()
    print(f"✅ Discovery Processor initialized with {len(processor.all_labels)} labels")

    # Test discovery schema
    print(f"\n📋 Available Categories:")
    for category, labels in processor.discovery_schema.items():
        print(f"  - {category}: {len(labels)} labels")

    # Test sample discovery processing
    test_case = {
        "intent_id": "profile_age",
        "doctor_question": "How old is the patient?",
        "patient_response": "She's elderly, yes. I help her because she only speaks Spanish.",
        "clinical_content": "Patient is elderly, approximately 70+ years old. Family member present to assist with translation."
    }

    print(f"\n🧪 Testing Discovery Processing:")
    print(f"Intent: {test_case['intent_id']}")
    print(f"Question: {test_case['doctor_question']}")

    try:
        result = processor.process_discovery(**test_case)
        print(f"✅ Result:")
        print(f"  - Label: {result['label']}")
        print(f"  - Category: {result['category']}")
        print(f"  - Summary: {result['summary']}")
        print(f"  - Confidence: {result['confidence']:.2f}")
        print(f"  - Reasoning: {result['reasoning']}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_discovery_processor()
