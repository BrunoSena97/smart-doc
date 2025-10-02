#!/usr/bin/env python3
"""
Test medication escalation flow end-to-end with improved intent classification.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any

# Add packages to path
import sys
sys.path.insert(0, str(Path(__file__).parent / "packages" / "core" / "src"))
sys.path.insert(0, str(Path(__file__).parent / "packages" / "shared" / "src"))

try:
    from smartdoc_core.intent.classifier import LLMIntentClassifier
    from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager
    from smartdoc_core.simulation.disclosure_store import ProgressiveDisclosureStore
    from smartdoc_core.llm.providers.ollama import OllamaProvider
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure the packages are properly installed.")
    sys.exit(1)


class TestMedicationEscalationFlow:
    """Test the complete medication escalation flow."""

    def __init__(self):
        self.case_file = Path(__file__).parent / "data" / "raw" / "cases" / "intent_driven_case.json"

        # Initialize with the case file path for the engine
        self.engine = IntentDrivenDisclosureManager(
            case_file_path=str(self.case_file)
        )

        # Initialize classifier separately for testing
        self.llm_provider = OllamaProvider(
            base_url="http://localhost:11434",
            model="gemma3:4b-it-q4_K_M"
        )
        self.classifier = LLMIntentClassifier(provider=self.llm_provider)

    async def load_case(self) -> Dict[str, Any]:
        """Load the case file."""
        with open(self.case_file, 'r') as f:
            return json.load(f)

    async def test_medication_classification_accuracy(self):
        """Test improved intent classification for medication queries."""
        print("\n=== Testing Medication Intent Classification ===")

        case_data = await self.load_case()

        # Test queries for different medication escalation levels
        test_queries = [
            {
                "query": "What medications is she taking?",
                "expected": "meds_current_known",
                "level": 1,
                "context": "anamnesis"
            },
            {
                "query": "What does she take for her arthritis?",
                "expected": "meds_ra_specific_initial_query",
                "level": 2,
                "context": "anamnesis"
            },
            {
                "query": "What does she take for RA?",
                "expected": "meds_ra_specific_initial_query",
                "level": 2,
                "context": "anamnesis"
            },
            {
                "query": "Can I see her complete medication list from previous records?",
                "expected": "meds_full_reconciliation_query",
                "level": 3,
                "context": "anamnesis"
            },
            {
                "query": "Any biologics or infliximab in her history?",
                "expected": "meds_full_reconciliation_query",
                "level": 3,
                "context": "anamnesis"
            },
            {
                "query": "Show me her full medication reconciliation",
                "expected": "meds_full_reconciliation_query",
                "level": 3,
                "context": "anamnesis"
            }
        ]

        correct = 0
        total = len(test_queries)

        for i, test in enumerate(test_queries, 1):
            try:
                # Use the direct classify_intent method
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
                print(f"   Expected: {test['expected']} (Level {test['level']})")
                print(f"   Got: {intent_id}")
                print(f"   Confidence: {confidence:.2f}")
                print(f"   Result: {'✅ CORRECT' if is_correct else '❌ WRONG'}")

            except Exception as e:
                print(f"\n{i}. Query: '{test['query']}'")
                print(f"   Error: {e}")

        accuracy = (correct / total) * 100
        print(f"\n=== Classification Results ===")
        print(f"Correct: {correct}/{total}")
        print(f"Accuracy: {accuracy:.1f}%")

        return accuracy >= 80  # 80% accuracy threshold

    async def test_end_to_end_escalation(self):
        """Test complete medication escalation flow."""
        print("\n\n=== Testing End-to-End Medication Escalation ===")

        # Test escalation sequence
        test_sequence = [
            {
                "query": "What medications is she taking?",
                "expected_level": 1,
                "description": "Basic medication query"
            },
            {
                "query": "What does she take for her rheumatoid arthritis?",
                "expected_level": 2,
                "description": "RA-specific medication query"
            },
            {
                "query": "Can I see her complete medication reconciliation including biologics?",
                "expected_level": 3,
                "description": "Full medication reconciliation"
            }
        ]

        escalation_success = True
        revealed_levels = set()

        # Start a session
        session_id = "test_session"
        self.engine.start_intent_driven_session(session_id)

        for i, test in enumerate(test_sequence, 1):
            print(f"\n--- Step {i}: {test['description']} ---")
            print(f"Query: '{test['query']}'")

            try:
                # Process the query through the simulation engine
                result = self.engine.process_doctor_query(
                    session_id,
                    test["query"],
                    context="anamnesis"
                )

                # Check what was revealed
                discovery_result = result.get("discovery_result", {})

                if isinstance(discovery_result, dict):
                    discovered_block_ids = discovery_result.get("discovered_blocks", [])

                    # Load case data to lookup block details
                    case_data = await self.load_case()

                    # Convert block IDs to actual block data
                    discoveries = []
                    for block_id in discovered_block_ids:
                        # Find the block in the case data
                        for block in case_data.get("informationBlocks", []):
                            if block.get("blockId") == block_id:
                                discoveries.append(block)
                                break
                else:
                    print(f"   Warning: discovery_result is not a dict, it's {type(discovery_result)}")
                    discoveries = []
                if discoveries:
                    for discovery in discoveries:
                        if discovery.get('groupId') == 'grp_meds_ra':
                            level = discovery.get('level', 0)
                            revealed_levels.add(level)
                            print(f"   ✅ Revealed medication level {level}")
                            print(f"   Content: {discovery.get('content', 'N/A')[:100]}...")

                            if level >= test['expected_level']:
                                print(f"   ✅ Expected level {test['expected_level']} achieved")
                            else:
                                print(f"   ❌ Expected level {test['expected_level']}, got {level}")
                                escalation_success = False
                        else:
                            print(f"   Info: Revealed {discovery.get('groupId', 'unknown')}")
                else:
                    print(f"   ❌ No discoveries for expected level {test['expected_level']}")
                    escalation_success = False

            except Exception as e:
                print(f"   ❌ Error processing query: {e}")
                escalation_success = False

        print(f"\n=== Escalation Results ===")
        print(f"Revealed levels: {sorted(revealed_levels)}")
        print(f"Expected levels: [1, 2, 3]")

        expected_levels = {1, 2, 3}
        levels_achieved = revealed_levels >= expected_levels

        print(f"All levels revealed: {'✅ YES' if levels_achieved else '❌ NO'}")
        print(f"Escalation success: {'✅ YES' if escalation_success else '❌ NO'}")

        return escalation_success and levels_achieved

    async def run_all_tests(self):
        """Run all medication escalation tests."""
        print("🧪 Testing Medication Escalation Flow with Improved Classification")
        print("=" * 70)

        # Test 1: Classification accuracy
        classification_success = await self.test_medication_classification_accuracy()

        # Test 2: End-to-end escalation
        escalation_success = await self.test_end_to_end_escalation()

        # Overall results
        print("\n" + "=" * 70)
        print("🏁 FINAL RESULTS")
        print("=" * 70)
        print(f"Intent Classification: {'✅ PASS' if classification_success else '❌ FAIL'}")
        print(f"Escalation Flow: {'✅ PASS' if escalation_success else '❌ FAIL'}")

        overall_success = classification_success and escalation_success
        print(f"Overall Test: {'🎉 SUCCESS' if overall_success else '💥 FAILURE'}")

        if overall_success:
            print("\n🎯 Medication escalation system is working correctly!")
        else:
            print("\n🔧 Medication escalation system needs further improvements.")

        return overall_success


async def main():
    """Run the medication escalation flow test."""
    tester = TestMedicationEscalationFlow()
    success = await tester.run_all_tests()

    if success:
        print("\n✨ All tests passed! The medication escalation system is ready.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    asyncio.run(main())
