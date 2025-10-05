#!/usr/bin/env python3
"""
Test the corrected labs structure with specific intents instead of escalation.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any

# Add packages to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "core" / "src"))

try:
    from smartdoc_core.intent.classifier import LLMIntentClassifier
    from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager
    from smartdoc_core.llm.providers.ollama import OllamaProvider
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class TestLabsSpecificIntents:
    """Test the corrected labs structure with specific intents."""

    def __init__(self):
        self.case_file = Path(__file__).parent.parent.parent / "data" / "raw" / "cases" / "intent_driven_case.json"

        # Initialize with gemma model
        self.engine = IntentDrivenDisclosureManager(
            case_file_path=str(self.case_file)
        )

        # Initialize classifier with gemma model
        self.llm_provider = OllamaProvider(
            base_url="http://localhost:11434",
            model="gemma3:4b-it-q4_K_M"
        )
        self.classifier = LLMIntentClassifier(provider=self.llm_provider)

    async def load_case(self) -> Dict[str, Any]:
        """Load the case file."""
        with open(self.case_file, 'r') as f:
            return json.load(f)

    async def test_labs_classification_accuracy(self):
        """Test specific lab intent classification."""
        print("\n=== Testing Lab-Specific Intent Classification ===")

        # Test queries for different specific lab requests
        test_queries = [
            {
                "query": "What's the BNP level?",
                "expected": "labs_bnp",  # More specific intent should be preferred
                "context": "labs"
            },
            {
                "query": "Pro-BNP results?",
                "expected": "labs_bnp",  # More specific intent should be preferred
                "context": "labs"
            },
            {
                "query": "Cardiac markers?",
                "expected": "labs_cardiac",  # General cardiac labs query
                "context": "labs"
            },
            {
                "query": "What's the white blood cell count?",
                "expected": "labs_infection",
                "context": "labs"
            },
            {
                "query": "Any signs of infection in the labs?",
                "expected": "labs_infection",
                "context": "labs"
            },
            {
                "query": "What's the hemoglobin level?",
                "expected": "labs_anemia",
                "context": "labs"
            },
            {
                "query": "Hgb results?",
                "expected": "labs_anemia",
                "context": "labs"
            },
            {
                "query": "Complete blood count?",
                "expected": "labs_blood_work",
                "context": "labs"
            },
            {
                "query": "Any lab results?",
                "expected": "labs_general",
                "context": "labs"
            }
        ]

        correct = 0
        total = len(test_queries)

        for i, test in enumerate(test_queries, 1):
            try:
                result = self.classifier.classify_intent(
                    test["query"],
                    test["context"]
                )

                intent_id = result.get("intent_id")
                confidence = result.get("confidence", 0.0)

                is_correct = intent_id == test["expected"]
                if is_correct:
                    correct += 1

                print(f"\n{i}. Query: '{test['query']}'")
                print(f"   Expected: {test['expected']}")
                print(f"   Got: {intent_id}")
                print(f"   Confidence: {confidence:.2f}")
                print(f"   Result: {'✅ CORRECT' if is_correct else '❌ WRONG'}")

            except Exception as e:
                print(f"\n{i}. Query: '{test['query']}'")
                print(f"   Error: {e}")

        accuracy = (correct / total) * 100
        print(f"\n=== Lab Classification Results ===")
        print(f"Correct: {correct}/{total}")
        print(f"Accuracy: {accuracy:.1f}%")

        return accuracy >= 70  # 70% accuracy threshold

    async def test_labs_specific_discovery(self):
        """Test that specific lab queries reveal the right specific labs."""
        print("\n\n=== Testing Lab-Specific Discovery ===")

        # Test specific lab requests
        test_sequence = [
            {
                "query": "What's the BNP level?",
                "expected_blocks": ["labs_bnp"],
                "description": "Specific BNP request"
            },
            {
                "query": "What's the white blood cell count?",
                "expected_blocks": ["labs_wbc"],
                "description": "Specific WBC request"
            },
            {
                "query": "What's the hemoglobin level?",
                "expected_blocks": ["labs_hemoglobin"],
                "description": "Specific hemoglobin request"
            },
            {
                "query": "Show me all lab results",
                "expected_blocks": ["labs_bnp", "labs_wbc", "labs_hemoglobin"],
                "description": "General labs request (should reveal all)"
            }
        ]

        discovery_success = True
        all_revealed_blocks = set()

        # Start a session
        session_id = "test_labs_session"
        self.engine.start_intent_driven_session(session_id)

        for i, test in enumerate(test_sequence, 1):
            print(f"\n--- Step {i}: {test['description']} ---")
            print(f"Query: '{test['query']}'")

            try:
                # Process the query
                result = self.engine.process_doctor_query(
                    session_id,
                    test["query"],
                    context="labs"
                )

                # Check what was revealed
                discovery_result = result.get("discovery_result", {})

                if isinstance(discovery_result, dict):
                    discovered_block_ids = discovery_result.get("discovered_blocks", [])

                    if discovered_block_ids:
                        for block_id in discovered_block_ids:
                            all_revealed_blocks.add(block_id)

                            if block_id in test["expected_blocks"]:
                                print(f"   ✅ Revealed expected lab: {block_id}")
                            else:
                                print(f"   ℹ️  Revealed additional lab: {block_id}")

                        # Check if we got all expected blocks
                        expected_found = all(
                            block in discovered_block_ids for block in test["expected_blocks"]
                        )

                        if expected_found:
                            print(f"   ✅ All expected labs found")
                        else:
                            missing = [b for b in test["expected_blocks"] if b not in discovered_block_ids]
                            print(f"   ❌ Missing expected labs: {missing}")
                            discovery_success = False
                    else:
                        print(f"   ❌ No discoveries for step {i}")
                        discovery_success = False
                else:
                    print(f"   ❌ Invalid discovery result format")
                    discovery_success = False

            except Exception as e:
                print(f"   ❌ Error processing query: {e}")
                discovery_success = False

        print(f"\n=== Lab Discovery Results ===")
        print(f"All revealed lab blocks: {sorted(all_revealed_blocks)}")

        expected_all_labs = {"labs_bnp", "labs_wbc", "labs_hemoglobin"}
        all_labs_discovered = expected_all_labs.issubset(all_revealed_blocks)

        print(f"Expected all labs: {sorted(expected_all_labs)}")
        print(f"All labs discovered: {'✅ YES' if all_labs_discovered else '❌ NO'}")
        print(f"Discovery success: {'✅ YES' if discovery_success else '❌ NO'}")

        return discovery_success and all_labs_discovered

    async def run_all_tests(self):
        """Run all lab tests."""
        print("🧪 Testing Lab-Specific Intents (No More Escalation)")
        print("=" * 70)

        # Test 1: Classification accuracy
        classification_success = await self.test_labs_classification_accuracy()

        # Test 2: Specific discovery
        discovery_success = await self.test_labs_specific_discovery()

        # Overall results
        print("\n" + "=" * 70)
        print("🏁 FINAL LAB RESULTS")
        print("=" * 70)
        print(f"Intent Classification: {'✅ PASS' if classification_success else '❌ FAIL'}")
        print(f"Specific Discovery: {'✅ PASS' if discovery_success else '❌ FAIL'}")

        overall_success = classification_success and discovery_success
        print(f"Overall Test: {'🎉 SUCCESS' if overall_success else '💥 FAILURE'}")

        if overall_success:
            print("\n🎯 Lab-specific intent system is working correctly!")
            print("✨ No more inappropriate escalation - each lab test has specific intent!")
        else:
            print("\n🔧 Lab system needs adjustments.")

        return overall_success


async def main():
    """Run the lab-specific intent test."""
    tester = TestLabsSpecificIntents()
    success = await tester.run_all_tests()

    if success:
        print("\n✨ Lab tests passed!")
    else:
        print("\n⚠️  Some lab tests failed. Check output above.")


if __name__ == "__main__":
    asyncio.run(main())
