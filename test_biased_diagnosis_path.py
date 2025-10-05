#!/usr/bin/env python3
"""
Test Script: Biased/Incorrect Diagnostic Path
Simulates a clinical interview with cognitive biases that leads to incorrect diagnosis.
This demonstrates anchoring, confirmation bias, and framing effects that result in misdiagnosis.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List

# Add packages to path
import sys
sys.path.insert(0, str(Path(__file__).parent / "packages" / "core" / "src"))

try:
    from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager
    from smartdoc_core.llm.providers.ollama import OllamaProvider
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class BiasedDiagnosisPath:
    """Simulates a biased clinical path leading to incorrect diagnosis."""

    def __init__(self):
        self.case_file = Path(__file__).parent / "data" / "raw" / "cases" / "intent_driven_case.json"
        self.engine = IntentDrivenDisclosureManager(case_file_path=str(self.case_file))
        self.session_id = "biased_diagnosis_test"
        self.discovered_critical_findings = []
        self.all_discoveries = []
        self.biases_demonstrated = []

    async def run_biased_workup(self):
        """Run a biased clinical workup demonstrating cognitive errors."""

        print("⚠️  BIASED DIAGNOSTIC PATH - HEART FAILURE MISDIAGNOSIS")
        print("=" * 80)
        print("Simulating clinical interview with cognitive biases")
        print("Demonstrating anchoring, confirmation bias, and framing effects")
        print("⚠️  THIS LEADS TO INCORRECT DIAGNOSIS FOR EDUCATIONAL PURPOSES")
        print("=" * 80)

        # Start session
        self.engine.start_intent_driven_session(self.session_id)

        # Phase 1: Framing Effect - Start with Heart Failure Assumption
        await self._phase1_framing_bias()

        # Phase 2: Anchoring Bias - Focus on Initial X-ray Interpretation
        await self._phase2_anchoring_bias()

        # Phase 3: Confirmation Bias - Seek Supporting Evidence Only
        await self._phase3_confirmation_bias()

        # Phase 4: Premature Closure - Skip Critical Information
        await self._phase4_premature_closure()

        # Final Analysis - Demonstrate Misdiagnosis
        await self._final_biased_analysis()

    async def _phase1_framing_bias(self):
        """Phase 1: Demonstrate framing effect by starting with heart failure assumption."""
        print("\n🧠 PHASE 1: FRAMING BIAS - 'Elderly Woman with Heart Failure'")
        print("-" * 50)
        print("🚨 BIAS: Starting with preconceived notion based on referral diagnosis")

        queries = [
            {
                "query": "Tell me about this elderly woman's heart failure exacerbation",
                "context": "anamnesis",
                "bias": "FRAMING",
                "explanation": "Assuming heart failure diagnosis from the start"
            },
            {
                "query": "What are her cardiac symptoms?",
                "context": "anamnesis",
                "bias": "FRAMING",
                "explanation": "Focusing immediately on cardiac etiology"
            }
        ]

        for i, query_info in enumerate(queries, 1):
            await self._execute_biased_query(
                f"1.{i}",
                query_info["query"],
                query_info["context"],
                query_info["bias"],
                query_info["explanation"]
            )

        self.biases_demonstrated.append("FRAMING_EFFECT")

    async def _phase2_anchoring_bias(self):
        """Phase 2: Demonstrate anchoring on initial chest X-ray interpretation."""
        print("\n🧠 PHASE 2: ANCHORING BIAS - Initial X-ray Interpretation")
        print("-" * 50)
        print("🚨 BIAS: Anchoring on preliminary radiology read")

        queries = [
            {
                "query": "Can I see the chest X-ray?",
                "context": "labs",
                "bias": "ANCHORING",
                "explanation": "Getting initial imaging that suggests heart failure"
            },
            {
                "query": "This X-ray shows pulmonary vascular congestion - classic heart failure",
                "context": "labs",
                "bias": "ANCHORING",
                "explanation": "Interpreting findings through heart failure lens"
            }
        ]

        for i, query_info in enumerate(queries, 1):
            await self._execute_biased_query(
                f"2.{i}",
                query_info["query"],
                query_info["context"],
                query_info["bias"],
                query_info["explanation"]
            )

        self.biases_demonstrated.append("ANCHORING_BIAS")

    async def _phase3_confirmation_bias(self):
        """Phase 3: Seek only information that confirms heart failure."""
        print("\n🧠 PHASE 3: CONFIRMATION BIAS - Seeking Supporting Evidence Only")
        print("-" * 50)
        print("🚨 BIAS: Only looking for evidence that supports heart failure")

        queries = [
            {
                "query": "What does the lung examination show?",
                "context": "exam",
                "bias": "CONFIRMATION",
                "explanation": "Expecting to find crackles that support heart failure"
            },
            {
                "query": "Show me the BNP level",
                "context": "labs",
                "bias": "CONFIRMATION",
                "explanation": "Looking for elevated BNP to confirm heart failure"
            },
            {
                "query": "What medications is she taking for heart failure?",
                "context": "anamnesis",
                "bias": "CONFIRMATION",
                "explanation": "Assuming she's already on heart failure medications"
            }
        ]

        for i, query_info in enumerate(queries, 1):
            await self._execute_biased_query(
                f"3.{i}",
                query_info["query"],
                query_info["context"],
                query_info["bias"],
                query_info["explanation"]
            )

        self.biases_demonstrated.append("CONFIRMATION_BIAS")

    async def _phase4_premature_closure(self):
        """Phase 4: Demonstrate premature closure by skipping critical information."""
        print("\n🧠 PHASE 4: PREMATURE CLOSURE - Skipping Critical Information")
        print("-" * 50)
        print("🚨 BIAS: Stopping investigation early, missing critical findings")

        # Notice what we're NOT asking about:
        print("❌ NOT ASKING ABOUT:")
        print("   • Constitutional symptoms (weight loss)")
        print("   • Complete medication reconciliation")
        print("   • Cardiac examination findings")
        print("   • Final radiologist interpretation")
        print("   • Echocardiogram")
        print("   • Immunosuppressive medications")

        # Make premature conclusion
        queries = [
            {
                "query": "This looks like classic heart failure exacerbation",
                "context": "anamnesis",
                "bias": "PREMATURE_CLOSURE",
                "explanation": "Drawing conclusion without complete workup"
            }
        ]

        for i, query_info in enumerate(queries, 1):
            await self._execute_biased_query(
                f"4.{i}",
                query_info["query"],
                query_info["context"],
                query_info["bias"],
                query_info["explanation"]
            )

        self.biases_demonstrated.append("PREMATURE_CLOSURE")

    async def _execute_biased_query(self, step: str, query: str, context: str, bias: str, explanation: str):
        """Execute a biased clinical query and analyze results."""
        print(f"\n--- Step {step}: {bias} ---")
        print(f"Query: '{query}'")
        print(f"Bias: {explanation}")

        try:
            result = self.engine.process_doctor_query(self.session_id, query, context=context)
            discovery_result = result.get("discovery_result", {})
            discovered_blocks = discovery_result.get("discovered_blocks", [])

            if discovered_blocks:
                # Load case data to get block details
                with open(self.case_file, 'r') as f:
                    case_data = json.load(f)

                for block_id in discovered_blocks:
                    for block in case_data.get("informationBlocks", []):
                        if block.get("blockId") == block_id:
                            self.all_discoveries.append(block)
                            is_critical = block.get("isCritical", False)

                            if is_critical:
                                self.discovered_critical_findings.append(block_id)
                                print(f"   ⚠️  CRITICAL (but overlooked): {block_id}")
                            else:
                                print(f"   ✅ Discovery: {block_id}")

                            print(f"   Content: {block.get('content', 'N/A')[:100]}...")

                            # Show how bias affects interpretation
                            if bias == "CONFIRMATION" and "crackles" in block.get('content', ''):
                                print(f"   🧠 BIASED INTERPRETATION: 'See! Crackles confirm heart failure!'")
                            elif bias == "CONFIRMATION" and "BNP" in block.get('content', ''):
                                print(f"   🧠 BIASED INTERPRETATION: 'Elevated BNP confirms heart failure!'")
                            elif bias == "ANCHORING" and "pulmonary vascular congestion" in block.get('content', ''):
                                print(f"   🧠 BIASED INTERPRETATION: 'This X-ray proves it's heart failure!'")
                            break
            else:
                print(f"   ℹ️  No new discoveries")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    async def _final_biased_analysis(self):
        """Demonstrate the consequences of biased reasoning."""
        print("\n" + "=" * 80)
        print("⚠️  BIASED DIAGNOSTIC CONCLUSION")
        print("=" * 80)

        # Load ground truth
        with open(self.case_file, 'r') as f:
            case_data = json.load(f)

        ground_truth = case_data.get("groundTruth", {})
        expected_critical_findings = ground_truth.get("criticalFindingIds", [])
        correct_diagnosis = ground_truth.get("finalDiagnosis", "")
        bias_triggers = case_data.get("biasTriggers", {})

        print(f"\n📊 BIASED REASONING SUMMARY:")
        print(f"Total discoveries: {len(self.all_discoveries)}")
        print(f"Critical findings found: {len(self.discovered_critical_findings)}")
        print(f"Expected critical findings: {len(expected_critical_findings)}")
        print(f"Biases demonstrated: {', '.join(self.biases_demonstrated)}")

        # Show what was missed
        missing_critical = [f for f in expected_critical_findings if f not in self.discovered_critical_findings]
        found_critical = [f for f in expected_critical_findings if f in self.discovered_critical_findings]

        print(f"\n❌ MISSED CRITICAL FINDINGS (due to bias):")
        critical_misses = {
            "hpi_weight_changes": "Constitutional symptoms ignored",
            "exam_cardiac_negative": "Normal cardiac exam not sought",
            "critical_cxr_formal": "Didn't get final radiology interpretation",
            "critical_infliximab": "Medication reconciliation incomplete",
            "critical_echo": "Echo not ordered to confirm diagnosis",
            "critical_ct_chest": "Advanced imaging not pursued"
        }

        for finding in missing_critical:
            explanation = critical_misses.get(finding, "Critical finding missed")
            print(f"   ❌ {finding}: {explanation}")

        if found_critical:
            print(f"\n✅ FOUND (but misinterpreted):")
            for finding in found_critical:
                print(f"   ⚠️  {finding} (interpreted through biased lens)")

        # Show the incorrect conclusion
        completeness_score = len(found_critical) / len(expected_critical_findings) * 100

        print(f"\n🧠 BIASED DIAGNOSTIC REASONING:")
        print(f"Completeness Score: {completeness_score:.1f}% (INADEQUATE)")
        print(f"❌ INCORRECT DIAGNOSIS: Heart Failure Exacerbation")
        print(f"✅ CORRECT DIAGNOSIS: {correct_diagnosis}")

        print(f"\n⚠️  CONSEQUENCES OF BIAS:")
        print(f"   • Anchored on preliminary X-ray interpretation")
        print(f"   • Confirmed bias with selective evidence (crackles, BNP)")
        print(f"   • Ignored contradictory evidence")
        print(f"   • Missed immunosuppression risk factor")
        print(f"   • Failed to rule out heart failure definitively")
        print(f"   • Did not discover infectious etiology")

        print(f"\n🎓 EDUCATIONAL VALUE:")
        print(f"This case demonstrates how cognitive biases lead to:")
        print(f"   ✓ Anchoring Bias: Stuck on initial impression")
        print(f"   ✓ Confirmation Bias: Seeking supporting evidence only")
        print(f"   ✓ Framing Effect: Influenced by initial presentation")
        print(f"   ✓ Premature Closure: Stopping investigation too early")

        print(f"\n💡 LEARNING POINTS:")
        print(f"   • Always get complete medication history")
        print(f"   • Don't anchor on preliminary interpretations")
        print(f"   • Actively seek contradictory evidence")
        print(f"   • Consider immunosuppression in differential")
        print(f"   • Use confirmatory testing (echo for heart failure)")

        return completeness_score < 50  # Returns True if appropriately incomplete (biased)


async def main():
    """Run the biased diagnosis pathway test."""
    tester = BiasedDiagnosisPath()
    appropriately_biased = await tester.run_biased_workup()

    print(f"\n" + "=" * 80)
    if appropriately_biased:
        print("⚠️  BIASED DIAGNOSTIC PATH COMPLETED!")
        print("This case demonstrates how cognitive biases lead to misdiagnosis.")
        print("Perfect for frontend demonstration of diagnostic errors.")
        print("Educational value: Shows what NOT to do in clinical reasoning.")
    else:
        print("🤔 BIAS DEMONSTRATION INCOMPLETE")
        print("Too much information was discovered - adjust for stronger bias effect.")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
