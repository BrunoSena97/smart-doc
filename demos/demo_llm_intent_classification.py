#!/usr/bin/env python3
"""
Demo of LLM-based Intent Classification vs Rigid Question Mapping
"""

def demo_llm_vs_rigid_mapping():
    """
    Demonstrate the difference between rigid question mapping and flexible LLM classification
    """

    print("🧠 LLM Intent Classification vs Rigid Question Mapping")
    print("=" * 70)

    # Example doctor inputs that would fail with rigid mapping
    flexible_doctor_inputs = [
        "What's going on with this patient?",
        "Tell me about the chest discomfort",
        "I want to check the cardiovascular system",
        "Let's listen to heart sounds",
        "We should get some labs done",
        "Based on everything, I think this is heart failure",
        "Patient needs treatment for this condition",
        "Can you explain what's happening to the patient?",
        "I'd like to examine the respiratory system",
        "What's the family medical background?"
    ]

    # Simulated LLM classifications (what the system would do)
    llm_classifications = [
        {"intent": "chief_complaint", "confidence": 0.92, "reason": "General inquiry about patient's main problem"},
        {"intent": "history_present_illness", "confidence": 0.88, "reason": "Asking about specific symptom details"},
        {"intent": "physical_exam_cardiovascular", "confidence": 0.95, "reason": "Intent to examine heart/cardiovascular system"},
        {"intent": "physical_exam_cardiovascular", "confidence": 0.93, "reason": "Specific cardiac examination request"},
        {"intent": "lab_tests", "confidence": 0.89, "reason": "Request for laboratory investigations"},
        {"intent": "assessment", "confidence": 0.91, "reason": "Clinical diagnosis/assessment statement"},
        {"intent": "treatment_plan", "confidence": 0.87, "reason": "Treatment recommendation"},
        {"intent": "explanation", "confidence": 0.84, "reason": "Request to explain condition to patient"},
        {"intent": "physical_exam_respiratory", "confidence": 0.90, "reason": "Respiratory system examination"},
        {"intent": "family_history", "confidence": 0.86, "reason": "Inquiry about family medical history"}
    ]

    print("📊 COMPARISON RESULTS:")
    print()

    for i, (input_text, classification) in enumerate(zip(flexible_doctor_inputs, llm_classifications)):
        print(f"🔍 Doctor Input #{i+1}:")
        print(f"   Text: \"{input_text}\"")
        print(f"   🚫 Rigid Mapping: Would likely return 'intent_not_understood'")
        print(f"   ✅ LLM Classification: {classification['intent']} (confidence: {classification['confidence']:.2f})")
        print(f"      Reasoning: {classification['reason']}")
        print()

    print("🎯 KEY ADVANTAGES OF LLM INTENT CLASSIFICATION:")
    print("✅ Handles natural, varied language expressions")
    print("✅ No need to predefine thousands of question variations")
    print("✅ Understands context and intent, not just keywords")
    print("✅ More flexible for real clinical conversations")
    print("✅ Easier to maintain and extend")
    print()

    print("🔧 IMPLEMENTATION BENEFITS:")
    print("✅ Replaces rigid SBERT similarity matching")
    print("✅ Uses Ollama LLM for intelligent intent understanding")
    print("✅ Maintains same API for dialogue manager integration")
    print("✅ Improves cognitive bias detection accuracy")
    print("✅ More realistic clinical interview simulation")

    print("\n🚀 NEXT STEPS:")
    print("1. Start Ollama service: 'ollama serve'")
    print("2. Test with SmartDoc application")
    print("3. See natural language understanding in action!")

if __name__ == "__main__":
    demo_llm_vs_rigid_mapping()
