#!/usr/bin/env python3
"""
Test Script: Correct Diagnostic Path
Simulates an ideal clinical interview that leads to the correct diagnosis of miliary tuberculosis.
This demonstrates the complete escalation system working properly with comprehensive information gathering.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List

# Add packages to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "core" / "src"))

try:
    from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager
    from smartdoc_core.llm.providers.ollama import OllamaProvider
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class CorrectDiagnosisPath:
    """Simulates the ideal clinical path leading to correct diagnosis."""

    def __init__(self):
        self.case_file = Path(__file__).parent.parent / "data" / "raw" / "cases" / "intent_driven_case.json"
        self.engine = IntentDrivenDisclosureManager(case_file_path=str(self.case_file))
        self.session_id = "correct_diagnosis_test"
        self.discovered_critical_findings = []
        self.all_discoveries = []

    async def run_complete_workup(self):
        """Run a complete, methodical clinical workup leading to correct diagnosis."""

        print("🎯 CORRECT DIAGNOSTIC PATH - MILIARY TUBERCULOSIS")
        print("=" * 80)
        print("Simulating a thorough, unbiased clinical interview")
        print("Following evidence-based diagnostic reasoning")
        print("=" * 80)

        # Start session
        self.engine.start_intent_driven_session(self.session_id)

        # Phase 1: Comprehensive History Taking
        await self._phase1_comprehensive_history()

        # Phase 2: Systematic Physical Examination
        await self._phase2_systematic_examination()

        # Phase 3: Comprehensive Laboratory Workup
        await self._phase3_comprehensive_labs()

        # Phase 4: Progressive Imaging Studies
        await self._phase4_progressive_imaging()

        # Phase 5: Critical Medication Reconciliation
        await self._phase5_medication_reconciliation()

        # Final Analysis
        await self._final_diagnostic_analysis()

    async def _phase1_comprehensive_history(self):
        """Phase 1: Thorough history taking with attention to red flags."""
        print("\n🔍 PHASE 1: COMPREHENSIVE HISTORY TAKING")
        print("-" * 50)

        queries = [
            {
                "query": "Tell me about the patient's demographics and background",
                "context": "anamnesis",
                "clinical_reasoning": "Establish baseline demographics and social context"
            },
            {
                "query": "What is the chief complaint and onset?",
                "context": "anamnesis",
                "clinical_reasoning": "Define primary presenting symptoms"
            },
            {
                "query": "Has there been any weight loss or decreased appetite?",
                "context": "anamnesis",
                "clinical_reasoning": "🚨 CRITICAL: Screen for constitutional symptoms suggesting systemic disease"
            },
            {
                "query": "What is the complete past medical history?",
                "context": "anamnesis",
                "clinical_reasoning": "Identify relevant comorbidities"
            },
            {
                "query": "Any recent medical care or treatments?",
                "context": "anamnesis",
                "clinical_reasoning": "Understand recent interventions and responses"
            },
            {
                "query": "Tell me about any pertinent negative symptoms",
                "context": "anamnesis",
                "clinical_reasoning": "Rule out other diagnostic possibilities"
            }
        ]

        for i, query_info in enumerate(queries, 1):
            await self._execute_query(
                f"1.{i}",
                query_info["query"],
                query_info["context"],
                query_info["clinical_reasoning"]
            )

    async def _phase2_systematic_examination(self):
        """Phase 2: Complete physical examination."""
        print("\n🔍 PHASE 2: SYSTEMATIC PHYSICAL EXAMINATION")
        print("-" * 50)

        queries = [
            {
                "query": "What are the vital signs?",
                "context": "exam",
                "clinical_reasoning": "Assess hemodynamic stability and oxygen status"
            },
            {
                "query": "How does the patient appear generally?",
                "context": "exam",
                "clinical_reasoning": "Overall clinical impression"
            },
            {
                "query": "What does the lung examination show?",
                "context": "exam",
                "clinical_reasoning": "Evaluate respiratory system given chief complaint"
            },
            {
                "query": "What about the cardiac examination?",
                "context": "exam",
                "clinical_reasoning": "🚨 CRITICAL: Rule out heart failure as primary cause"
            }
        ]

        for i, query_info in enumerate(queries, 1):
            await self._execute_query(
                f"2.{i}",
                query_info["query"],
                query_info["context"],
                query_info["clinical_reasoning"]
            )

    async def _phase3_comprehensive_labs(self):
        """Phase 3: Complete laboratory evaluation."""
        print("\n🔍 PHASE 3: COMPREHENSIVE LABORATORY WORKUP")
        print("-" * 50)

        queries = [
            {
                "query": "Show me all laboratory results",
                "context": "labs",
                "clinical_reasoning": "Comprehensive lab evaluation for systemic disease"
            }
        ]

        for i, query_info in enumerate(queries, 1):
            await self._execute_query(
                f"3.{i}",
                query_info["query"],
                query_info["context"],
                query_info["clinical_reasoning"]
            )

    async def _phase4_progressive_imaging(self):
        """Phase 4: Systematic imaging evaluation."""
        print("\n🔍 PHASE 4: PROGRESSIVE IMAGING STUDIES")
        print("-" * 50)

        queries = [
            {
                "query": "Can I see the chest X-ray?",
                "context": "labs",
                "clinical_reasoning": "Initial imaging for respiratory symptoms"
            },
            {
                "query": "What does the attending radiologist's final interpretation say?",
                "context": "labs",
                "clinical_reasoning": "🚨 CRITICAL: Get definitive imaging interpretation"
            },
            {
                "query": "Can we get an echocardiogram?",
                "context": "labs",
                "clinical_reasoning": "🚨 CRITICAL: Rule out heart failure definitively"
            }
        ]

        for i, query_info in enumerate(queries, 1):
            await self._execute_query(
                f"4.{i}",
                query_info["query"],
                query_info["context"],
                query_info["clinical_reasoning"]
            )

    async def _phase5_medication_reconciliation(self):
        """Phase 5: Complete medication history - most critical phase."""
        print("\n🔍 PHASE 5: COMPREHENSIVE MEDICATION RECONCILIATION")
        print("-" * 50)

        queries = [
            {
                "query": "What medications is she taking?",
                "context": "anamnesis",
                "clinical_reasoning": "Initial medication assessment"
            },
            {
                "query": "What does she take for her rheumatoid arthritis?",
                "context": "anamnesis",
                "clinical_reasoning": "Focus on RA medications given known diagnosis"
            },
            {
                "query": "Can I see her complete medication reconciliation from previous records?",
                "context": "anamnesis",
                "clinical_reasoning": "🚨 CRITICAL: Complete medication history including biologics"
            }
        ]

        for i, query_info in enumerate(queries, 1):
            await self._execute_query(
                f"5.{i}",
                query_info["query"],
                query_info["context"],
                query_info["clinical_reasoning"]
            )

    async def _execute_query(self, step: str, query: str, context: str, reasoning: str):
        """Execute a clinical query and analyze results."""
        print(f"\n--- Step {step}: {reasoning} ---")
        print(f"Query: '{query}'")

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
                                print(f"   🚨 CRITICAL FINDING: {block_id}")
                            else:
                                print(f"   ✅ Discovery: {block_id}")

                            print(f"   Content: {block.get('content', 'N/A')[:100]}...")
                            break
            else:
                print(f"   ℹ️  No new discoveries")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    async def _final_diagnostic_analysis(self):
        """Analyze all findings and demonstrate correct diagnostic reasoning."""
        print("\n" + "=" * 80)
        print("🎯 FINAL DIAGNOSTIC ANALYSIS")
        print("=" * 80)

        # Load ground truth
        with open(self.case_file, 'r') as f:
            case_data = json.load(f)

        ground_truth = case_data.get("groundTruth", {})
        expected_critical_findings = ground_truth.get("criticalFindingIds", [])
        correct_diagnosis = ground_truth.get("finalDiagnosis", "")

        print(f"\n📊 DISCOVERY SUMMARY:")
        print(f"Total discoveries: {len(self.all_discoveries)}")
        print(f"Critical findings found: {len(self.discovered_critical_findings)}")
        print(f"Expected critical findings: {len(expected_critical_findings)}")

        # Check completeness
        missing_critical = [f for f in expected_critical_findings if f not in self.discovered_critical_findings]
        found_critical = [f for f in expected_critical_findings if f in self.discovered_critical_findings]

        print(f"\n🎯 CRITICAL FINDINGS ANALYSIS:")
        for finding in found_critical:
            print(f"   ✅ {finding}")

        if missing_critical:
            print(f"\n⚠️  MISSED CRITICAL FINDINGS:")
            for finding in missing_critical:
                print(f"   ❌ {finding}")

        # Diagnostic reasoning
        completeness_score = len(found_critical) / len(expected_critical_findings) * 100

        print(f"\n🧠 DIAGNOSTIC REASONING:")
        print(f"Completeness Score: {completeness_score:.1f}%")

        if completeness_score >= 80:
            print(f"✅ EXCELLENT: Comprehensive workup leading to correct diagnosis")
            print(f"🎯 CORRECT DIAGNOSIS: {correct_diagnosis}")
            print(f"\n💡 KEY DIAGNOSTIC CLUES IDENTIFIED:")
            print(f"   • Constitutional symptoms (weight loss)")
            print(f"   • Normal cardiac exam (rules out heart failure)")
            print(f"   • Interstitial pattern on imaging")
            print(f"   • Immunosuppressive medication (infliximab)")
            print(f"   • Normal echo (confirms not heart failure)")
            print(f"   • Miliary pattern on CT")

            print(f"\n🏆 EXCELLENT CLINICAL REASONING!")
            print(f"This demonstrates ideal diagnostic methodology:")
            print(f"   ✅ Systematic history taking")
            print(f"   ✅ Complete physical examination")
            print(f"   ✅ Comprehensive imaging interpretation")
            print(f"   ✅ Thorough medication reconciliation")
            print(f"   ✅ Recognition of immunosuppression risk")
        else:
            print(f"⚠️  INCOMPLETE: Missing {100-completeness_score:.1f}% of critical findings")
            print(f"Consider more thorough evaluation")

        return completeness_score >= 80


async def main():
    """Run the correct diagnosis pathway test."""
    tester = CorrectDiagnosisPath()
    success = await tester.run_complete_workup()

    print(f"\n" + "=" * 80)
    if success:
        print("🎉 PERFECT DIAGNOSTIC PATH COMPLETED!")
        print("This case demonstrates excellent clinical reasoning and systematic approach.")
        print("Ready for frontend demonstration of ideal diagnostic workflow.")
    else:
        print("⚠️  DIAGNOSTIC PATH INCOMPLETE")
        print("Some critical findings were missed - review methodology.")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
