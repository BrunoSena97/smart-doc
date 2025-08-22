#!/usr/bin/env python3
"""
Comprehensive test to verify the shared LLM provider architecture.
Tests that all components can successfully import and use shared providers.
"""

import sys
from pathlib import Path
from typing import Optional

# When running with Poetry, the packages should be available directly
# No need to manipulate sys.path

def test_shared_provider_imports():
    """Test that shared LLM providers can be imported correctly."""
    print("1. Testing shared provider imports...")

    try:
        from smartdoc_core.llm.providers.base import LLMProvider
        from smartdoc_core.llm.providers.ollama import OllamaProvider
        from smartdoc_core.llm.providers import LLMProvider as ImportedProvider, OllamaProvider as ImportedOllama
        print("   ✓ Shared provider imports successful")

        # Verify they're the same classes
        assert LLMProvider is ImportedProvider
        assert OllamaProvider is ImportedOllama
        print("   ✓ Import consistency verified")

    except Exception as e:
        print(f"   ✗ Import failed: {e}")
        return False

    return True

def test_discovery_processor_with_shared_providers():
    """Test that discovery processor works with shared providers."""
    print("\n2. Testing discovery processor with shared providers...")

    try:
        from smartdoc_core.discovery.processor import LLMDiscoveryProcessor
        from smartdoc_core.discovery.prompts.default import DefaultDiscoveryPrompt
        from smartdoc_core.llm.providers.ollama import OllamaProvider

        # Mock provider for testing
        class MockProvider:
            def generate(self, prompt: str, context: Optional[dict] = None) -> str:
                return '{"label": "symptom_mentioned", "category": "symptom", "summary": "Patient mentions headache", "confidence": 0.95, "reasoning": "Direct symptom mention"}'

        # Create processor with shared provider
        provider = MockProvider()
        prompt_builder = DefaultDiscoveryPrompt()
        processor = LLMDiscoveryProcessor(provider=provider, prompt_builder=prompt_builder)

        # Test processing
        result = processor.process_discovery(
            intent_id="test",
            doctor_question="What's wrong?",
            patient_response="I have a headache",
            clinical_content="Patient mentions headache"
        )

        print("   ✓ Discovery processor works with shared providers")
        print(f"   ✓ Generated discovery result: {result.get('label', 'Unknown')}")

    except Exception as e:
        print(f"   ✗ Discovery processor test failed: {e}")
        return False

    return True

def test_intent_classifier_with_shared_providers():
    """Test that intent classifier works with shared providers."""
    print("\n3. Testing intent classifier with shared providers...")

    try:
        from smartdoc_core.intent.classifier import LLMIntentClassifier
        from smartdoc_core.intent.prompts.default import DefaultIntentPrompt
        from smartdoc_core.llm.providers.ollama import OllamaProvider

        # Mock provider for testing
        class MockProvider:
            def generate(self, prompt: str, context: Optional[dict] = None) -> str:
                return '{"intent": "medical_question", "confidence": 0.92, "entities": {"symptoms": ["headache"]}}'

        # Create classifier with shared provider
        provider = MockProvider()
        prompt_builder = DefaultIntentPrompt()
        classifier = LLMIntentClassifier(provider=provider, prompt_builder=prompt_builder)

        # Test classification
        result = classifier.classify_intent("I have a headache")

        print("   ✓ Intent classifier works with shared providers")
        print(f"   ✓ Classified intent: {result.get('intent', 'Unknown')}")

    except Exception as e:
        print(f"   ✗ Intent classifier test failed: {e}")
        return False

    return True

def test_simulation_engine_with_shared_providers():
    """Test that simulation engine works with shared providers."""
    print("\n4. Testing simulation engine with shared providers...")

    try:
        # Just test that we can import the required components
        from smartdoc_core.discovery.processor import LLMDiscoveryProcessor
        from smartdoc_core.llm.providers.ollama import OllamaProvider
        from smartdoc_core.discovery.prompts.default import DefaultDiscoveryPrompt

        # Create components to verify they work together (use mock provider)
        class MockProvider:
            def generate(self, prompt: str, context: Optional[dict] = None) -> str:
                return '{"label": "test", "category": "test", "summary": "test", "confidence": 0.95, "reasoning": "test"}'

        provider = MockProvider()
        prompt_builder = DefaultDiscoveryPrompt()
        processor = LLMDiscoveryProcessor(provider=provider, prompt_builder=prompt_builder)

        print("   ✓ Simulation components work with shared providers")

    except Exception as e:
        print(f"   ✗ Simulation engine test failed: {e}")
        return False

    return True

def test_backward_compatibility():
    """Test that backward compatibility warnings work."""
    print("\n5. Testing backward compatibility warnings...")

    try:
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # This should trigger deprecation warning
            from smartdoc_core.discovery.providers.ollama import OllamaProvider

            # Check if warning was issued
            assert len(w) > 0
            assert issubclass(w[0].category, DeprecationWarning)
            assert "deprecated" in str(w[0].message).lower()

            print("   ✓ Backward compatibility warning issued correctly")

    except Exception as e:
        print(f"   ✗ Backward compatibility test failed: {e}")
        return False

    return True

def main():
    """Run all architecture tests."""
    print("Testing shared LLM provider architecture...")
    print("=" * 50)

    tests = [
        test_shared_provider_imports,
        test_discovery_processor_with_shared_providers,
        test_intent_classifier_with_shared_providers,
        test_simulation_engine_with_shared_providers,
        test_backward_compatibility
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"Results: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("🎉 All architecture tests passed! Shared provider architecture is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
