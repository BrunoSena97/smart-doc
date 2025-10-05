#!/usr/bin/env python3
"""
Test imaging escalation flow with the correct gemma model.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any

# Add packages to path
import sys
sys.path.insert(0, str(Path(__file__).parent / "packages" / "core" / "src"))

try:
    from smartdoc_core.intent.classifier import LLMIntentClassifier
    from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager
    from smartdoc_core.llm.providers.ollama import OllamaProvider
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class TestImagingEscalationFlow:
    """Test the imaging escalation flow."""

    def __init__(self):
        self.case_file = Path(__file__).parent / "data" / "raw" / "cases" / "intent_driven_case.json"

        # Initialize with gemma model
        self.engine = IntentDrivenDisclosureManager(
            case_file_path=str(self.case_file)
        )

        # Initialize classifier with gemma model
        self.llm_provider = OllamaProvider(
            base_url="http://localhost:11434",
            model="gemma3:4b-it-q4_K_M"  # Using available gemma model
        )
        self.classifier = LLMIntentClassifier(provider=self.llm_provider)

    async def load_case(self) -> Dict[str, Any]:
        """Load the case file."""
        with open(self.case_file, 'r') as f:
            return json.load(f)

    async def test_imaging_classification_accuracy(self):
        """Test imaging intent classification."""
        print("\n=== Testing Imaging Intent Classification ===")

        # Test queries for different imaging requests
        test_queries = [
            {
                "query": "Can I see the chest X-ray?",
                "expected": "imaging_chest",
                "context": "labs"
            },
            {
                "query": "What does the chest radiograph show?",
                "expected": "imaging_chest",
                "context": "labs"
            },
            {
                "query": "Any imaging studies?",
                "expected": "imaging_general",
                "context": "labs"
            },
            {
                "query": "Can we get an echo?",
                "expected": "imaging_general",
                "context": "labs"
            },
            {
                "query": "What about a CT scan?",
                "expected": "imaging_general",
                "context": "labs"
            },
            {
                "query": "Show me all imaging results",
                "expected": "imaging_general",
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
        print(f"\n=== Imaging Classification Results ===")
        print(f"Correct: {correct}/{total}")
        print(f"Accuracy: {accuracy:.1f}%")

        return accuracy >= 70  # 70% accuracy threshold for imaging

    async def test_imaging_escalation_flow(self):
        """Test imaging escalation sequence."""
        print("\n\n=== Testing Imaging Escalation Flow ===")

        # Test escalation sequence
        test_sequence = [
            {
                "query": "Can I see the chest X-ray?",
                "expected_groups": ["grp_cxr"],
                "expected_levels": [1],
                "description": "Initial chest X-ray request"
            },
            {
                "query": "What does the attending radiologist say about the chest X-ray?",
                "expected_groups": ["grp_cxr"],
                "expected_levels": [2],
                "description": "Formal chest X-ray interpretation (Level 2)"
            },
            {
                "query": "Can we get an echocardiogram?",
                "expected_groups": ["grp_echo", "grp_advanced_imaging"],
                "expected_levels": [1, 2],
                "description": "Echo request (triggers echo + CT due to satisfied prerequisites)"
            }
        ]

        escalation_success = True
        revealed_groups = {}  # group -> max_level

        # Start a session
        session_id = "test_imaging_session"
        self.engine.start_intent_driven_session(session_id)

        for i, test in enumerate(test_sequence, 1):
            print(f"\n--- Step {i}: {test['description']} ---")
            print(f"Query: '{test['query']}'")

            try:
                # Process the query
                result = self.engine.process_doctor_query(
                    session_id,
                    test["query"],
                    context="labs"  # Imaging typically requested in labs phase
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
                        for block in case_data.get("informationBlocks", []):
                            if block.get("blockId") == block_id:
                                discoveries.append(block)
                                break

                    if discoveries:
                        for discovery in discoveries:
                            group_id = discovery.get('groupId')
                            level = discovery.get('level', 0)
                            block_type = discovery.get('blockType')

                            if block_type == "Imaging":
                                # Track the highest level revealed for each group
                                if group_id not in revealed_groups:
                                    revealed_groups[group_id] = level
                                else:
                                    revealed_groups[group_id] = max(revealed_groups[group_id], level)

                                print(f"   ✅ Revealed {group_id} level {level}")
                                print(f"   Content: {discovery.get('content', 'N/A')[:80]}...")

                                # Check if this matches expected groups/levels
                                if group_id in test['expected_groups']:
                                    group_index = test['expected_groups'].index(group_id)
                                    expected_level = test['expected_levels'][group_index]
                                    if level >= expected_level:
                                        print(f"   ✅ Expected level {expected_level} achieved")
                                    else:
                                        print(f"   ❌ Expected level {expected_level}, got {level}")
                                        escalation_success = False
                                else:
                                    # This discovery wasn't expected for this step, but might be valid due to prerequisites
                                    print(f"   ℹ️  Unexpected discovery (prerequisites satisfied): {group_id} level {level}")
                            else:
                                print(f"   Info: Revealed non-imaging {group_id} ({block_type})")
                    else:
                        # Only mark as failure if no expected groups were found
                        expected_found = any(
                            group in [d.get('groupId') for d in discoveries if d.get('blockType') == 'Imaging']
                            for group in test['expected_groups']
                        )
                        if not expected_found:
                            print(f"   ❌ No expected discoveries for step {i}")
                            escalation_success = False
                        else:
                            print(f"   ℹ️  Expected groups found, but also other discoveries due to prerequisites")
                else:
                    print(f"   ❌ Invalid discovery result format")
                    escalation_success = False

            except Exception as e:
                print(f"   ❌ Error processing query: {e}")
                escalation_success = False

        print(f"\n=== Imaging Escalation Results ===")
        print(f"Revealed imaging groups: {revealed_groups}")

        # Check if we got the expected imaging escalation
        expected_final_state = {
            "grp_cxr": 2,      # Should reach level 2 (formal interpretation)
            "grp_echo": 1,     # Single level
            "grp_advanced_imaging": 2  # Advanced CT (requires prerequisites)
        }

        all_groups_revealed = all(
            group in revealed_groups and revealed_groups[group] >= expected_level
            for group, expected_level in expected_final_state.items()
        )

        print(f"Expected final state: {expected_final_state}")
        print(f"All imaging groups revealed correctly: {'✅ YES' if all_groups_revealed else '❌ NO'}")
        print(f"Escalation success: {'✅ YES' if escalation_success else '❌ NO'}")

        return escalation_success and all_groups_revealed

    async def run_all_tests(self):
        """Run all imaging tests."""
        print("🧪 Testing Imaging Escalation Flow with Gemma Model")
        print("=" * 70)

        # Test 1: Classification accuracy
        classification_success = await self.test_imaging_classification_accuracy()

        # Test 2: Escalation flow
        escalation_success = await self.test_imaging_escalation_flow()

        # Overall results
        print("\n" + "=" * 70)
        print("🏁 FINAL IMAGING RESULTS")
        print("=" * 70)
        print(f"Intent Classification: {'✅ PASS' if classification_success else '❌ FAIL'}")
        print(f"Escalation Flow: {'✅ PASS' if escalation_success else '❌ FAIL'}")

        overall_success = classification_success and escalation_success
        print(f"Overall Test: {'🎉 SUCCESS' if overall_success else '💥 FAILURE'}")

        if overall_success:
            print("\n🎯 Imaging escalation system is working correctly!")
        else:
            print("\n🔧 Imaging escalation system needs adjustments.")

        return overall_success


async def main():
    """Run the imaging escalation flow test."""
    tester = TestImagingEscalationFlow()
    success = await tester.run_all_tests()

    if success:
        print("\n✨ Imaging tests passed!")
    else:
        print("\n⚠️  Some imaging tests failed. Check output above.")


if __name__ == "__main__":
    asyncio.run(main())
