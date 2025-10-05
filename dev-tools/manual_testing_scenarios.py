"""
Manual testing scenarios for validating the enhanced evaluation system.
These tests can be run through the API endpoints to verify functionality.
"""

import json
import requests
from typing import Dict, Any

class EvaluationTestRunner:
    """Class to run manual tests against the evaluation API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api/v1/evaluation"

    def test_structured_json_validation(self) -> Dict[str, Any]:
        """Test the structured JSON validation endpoint."""
        print("🔍 Testing Structured JSON Validation...")

        # Test valid evaluation data
        valid_evaluation = {
            "overall_score": 78,
            "diagnostic_accuracy": {
                "score": 85,
                "analysis": "Strong diagnostic performance with accurate final diagnosis",
                "correct_elements": ["systematic_approach", "appropriate_differential"],
                "missed_elements": ["early_medication_history"]
            },
            "information_gathering": {
                "score": 72,
                "analysis": "Good information gathering but could be more efficient",
                "strengths": ["thorough_physical_exam", "appropriate_investigations"],
                "areas_for_improvement": ["earlier_social_history", "medication_review"]
            },
            "cognitive_bias_awareness": {
                "score": 80,
                "analysis": "Good recognition and correction of initial anchoring bias",
                "detected_biases_impact": "Initial heart failure focus corrected after contradictory evidence",
                "metacognitive_quality": "High quality reflective responses showing self-awareness"
            },
            "clinical_reasoning": {
                "score": 75,
                "analysis": "Sound clinical reasoning with appropriate hypothesis revision",
                "hypothesis_generation": "Multiple differential diagnoses appropriately considered",
                "evidence_synthesis": "Good integration of clinical findings and test results"
            },
            "constructive_feedback": {
                "positive_reinforcement": "Excellent diagnostic accuracy and self-correction abilities",
                "key_learning_points": ["Early social history importance", "Systematic approach benefits"],
                "specific_recommendations": ["Always consider medication effects", "Weight loss as red flag"],
                "bias_education": "Continue monitoring for anchoring bias in similar presentations"
            },
            "confidence_assessment": 82
        }

        return self._post_request("/validate", {"evaluation_data": valid_evaluation})

    def test_comprehensive_evaluation(self) -> Dict[str, Any]:
        """Test comprehensive evaluation with realistic clinical case."""
        print("🏥 Testing Comprehensive Clinical Evaluation...")

        payload = {
            "diagnosis": "Miliary tuberculosis secondary to immunosuppression from infliximab therapy",
            "dialogue_transcript": [
                {"role": "user", "content": "A 45-year-old patient presents with progressive shortness of breath and weight loss over 3 months."},
                {"role": "assistant", "content": "I need to gather more history. Can you tell me about any medications or medical conditions?"},
                {"role": "user", "content": "The patient has Crohn's disease and is on infliximab. What physical examination would you perform?"},
                {"role": "assistant", "content": "I'll perform a systematic physical examination, focusing on respiratory and lymphatic systems."},
                {"role": "user", "content": "Physical exam reveals decreased breath sounds bilaterally and lymphadenopathy. What investigations?"},
                {"role": "assistant", "content": "Given the immunosuppression and bilateral findings, I'm concerned about opportunistic infections. I'd order chest imaging and consider TB screening."},
                {"role": "user", "content": "Chest CT shows bilateral miliary nodules. What's your diagnosis?"},
                {"role": "assistant", "content": "The miliary pattern in an immunosuppressed patient strongly suggests miliary tuberculosis."}
            ],
            "metacognitive_responses": {
                "information_gathering": "I systematically gathered medication history and recognized the significance of immunosuppression. I performed appropriate physical examination and ordered relevant investigations.",
                "diagnostic_reasoning": "The combination of immunosuppression from infliximab, bilateral symptoms, and miliary pattern on CT led me to consider opportunistic infections, specifically TB. The classic miliary pattern was key.",
                "bias_awareness": "I initially considered more common respiratory conditions but the immunosuppression context made me broaden my differential. I avoided anchoring on common diagnoses in immunocompetent patients."
            },
            "case_context": {
                "case_type": "diagnostic_challenge",
                "correct_diagnosis": "Miliary tuberculosis secondary to immunosuppression",
                "key_features": ["immunosuppression", "infliximab_therapy", "bilateral_symptoms", "miliary_pattern", "weight_loss"],
                "total_blocks": 18,
                "difficulty_level": "high"
            },
            "session_id": f"test_comprehensive_{self._generate_session_id()}"
        }

        return self._post_request("/submit", payload)

    def test_bias_heavy_scenario(self) -> Dict[str, Any]:
        """Test evaluation of a case designed to trigger cognitive biases."""
        print("🧠 Testing Bias-Heavy Clinical Scenario...")

        payload = {
            "diagnosis": "Heart failure exacerbation",
            "dialogue_transcript": [
                {"role": "user", "content": "78-year-old presents with acute shortness of breath. Previous chest X-ray showed cardiomegaly."},
                {"role": "assistant", "content": "Given the history of cardiomegaly and acute SOB, this looks like heart failure exacerbation. I'll focus on cardiac evaluation."},
                {"role": "user", "content": "Patient has a history of COPD and is a heavy smoker. BNP is 150 (normal < 400). What's your assessment?"},
                {"role": "assistant", "content": "The BNP is borderline, but in elderly patients it can be falsely low. I still think this is primarily heart failure."},
                {"role": "user", "content": "Echocardiogram shows normal systolic function (EF 55%) and no diastolic dysfunction. Spirometry shows severe obstruction."},
                {"role": "assistant", "content": "The echo might miss subtle diastolic issues. Given the cardiomegaly history, I maintain this is heart failure related."},
                {"role": "user", "content": "Patient improves significantly with bronchodilators and steroids, minimal response to diuretics."},
                {"role": "assistant", "content": "I believe this is still primarily heart failure with some COPD component contributing."}
            ],
            "metacognitive_responses": {
                "information_gathering": "I focused primarily on cardiac evaluation given the initial presentation and cardiomegaly history.",
                "diagnostic_reasoning": "The acute presentation with known cardiomegaly made heart failure the most likely diagnosis in my mind.",
                "bias_awareness": "I'm confident in my cardiac focus despite some contradictory findings. The cardiomegaly history is significant."
            },
            "case_context": {
                "case_type": "bias_trigger",
                "correct_diagnosis": "COPD exacerbation",
                "key_features": ["COPD_history", "normal_BNP", "normal_echo", "severe_obstruction", "bronchodilator_response"],
                "total_blocks": 12,
                "bias_triggers": {
                    "anchoring": "early_cardiomegaly_focus",
                    "confirmation": "ignored_normal_cardiac_studies",
                    "premature_closure": "insufficient_pulmonary_evaluation"
                }
            },
            "session_id": f"test_bias_{self._generate_session_id()}"
        }

        return self._post_request("/submit", payload)

    def test_variance_analysis(self) -> Dict[str, Any]:
        """Test multi-seed evaluation for consistency assessment."""
        print("📊 Testing Variance Analysis...")

        payload = {
            "diagnosis": "Acute myocardial infarction",
            "dialogue_transcript": [
                {"role": "user", "content": "55-year-old male with acute chest pain."},
                {"role": "assistant", "content": "I need to evaluate for acute coronary syndrome. What are the pain characteristics?"},
                {"role": "user", "content": "Crushing substernal pain radiating to left arm, started 2 hours ago."},
                {"role": "assistant", "content": "Classic presentation for MI. I need ECG and cardiac enzymes immediately."},
                {"role": "user", "content": "ECG shows ST elevation in leads II, III, aVF. Troponin is elevated."},
                {"role": "assistant", "content": "This is inferior STEMI. Need immediate reperfusion therapy."}
            ],
            "metacognitive_responses": {
                "information_gathering": "I immediately focused on ACS evaluation given the classic presentation",
                "diagnostic_reasoning": "The combination of typical chest pain, ECG changes, and elevated biomarkers confirmed STEMI",
                "bias_awareness": "The presentation was classic, so I appropriately focused on rapid ACS evaluation"
            },
            "case_context": {
                "case_type": "emergency_diagnosis",
                "correct_diagnosis": "Inferior ST-elevation myocardial infarction",
                "key_features": ["typical_chest_pain", "st_elevation", "elevated_troponin"],
                "total_blocks": 8
            },
            "num_runs": 3,
            "seed_values": [42, 123, 789],
            "session_id": f"test_variance_{self._generate_session_id()}"
        }

        return self._post_request("/variance-test", payload)

    def test_reliability_metrics(self) -> Dict[str, Any]:
        """Test reliability metrics endpoint."""
        print("📈 Testing Reliability Metrics...")

        return self._get_request("/reliability")

    def _post_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request to API endpoint."""
        try:
            response = requests.post(
                f"{self.api_base}{endpoint}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            return {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "data": response.json() if response.status_code == 200 else None,
                "error": response.text if response.status_code != 200 else None
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": None,
                "success": False,
                "data": None,
                "error": str(e)
            }

    def _get_request(self, endpoint: str) -> Dict[str, Any]:
        """Make GET request to API endpoint."""
        try:
            response = requests.get(
                f"{self.api_base}{endpoint}",
                timeout=30
            )

            return {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "data": response.json() if response.status_code == 200 else None,
                "error": response.text if response.status_code != 200 else None
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": None,
                "success": False,
                "data": None,
                "error": str(e)
            }

    def _generate_session_id(self) -> str:
        """Generate unique session ID for testing."""
        import time
        return str(int(time.time() * 1000))[-8:]

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all manual tests and return results."""
        print("🚀 Starting Manual API Tests")
        print("=" * 50)

        results = {}

        try:
            # Test 1: JSON Validation
            results['json_validation'] = self.test_structured_json_validation()

            # Test 2: Comprehensive Evaluation
            results['comprehensive'] = self.test_comprehensive_evaluation()

            # Test 3: Bias Detection
            results['bias_detection'] = self.test_bias_heavy_scenario()

            # Test 4: Variance Analysis
            results['variance'] = self.test_variance_analysis()

            # Test 5: Reliability Metrics
            results['reliability'] = self.test_reliability_metrics()

        except Exception as e:
            results['error'] = str(e)

        # Print summary
        print("\n" + "=" * 50)
        print("📊 MANUAL TEST RESULTS")
        print("=" * 50)

        for test_name, result in results.items():
            if test_name == 'error':
                print(f"❌ CRITICAL ERROR: {result}")
                continue

            success = result.get('success', False)
            status_code = result.get('status_code', 'N/A')
            emoji = "✅" if success else "❌"

            print(f"{emoji} {test_name}: {status_code} - {'PASSED' if success else 'FAILED'}")

            if not success and result.get('error'):
                print(f"   Error: {result['error'][:100]}...")

        return results


def main():
    """Run manual testing scenarios."""
    runner = EvaluationTestRunner()

    print("🔧 Manual Testing Guide for Enhanced Evaluation System")
    print("=" * 60)
    print()
    print("To run these tests:")
    print("1. Start the API server: make api")
    print("2. Run this script: python scripts/manual_testing_scenarios.py")
    print("3. Or run individual tests by importing EvaluationTestRunner")
    print()
    print("Available test scenarios:")
    print("- Structured JSON validation")
    print("- Comprehensive clinical evaluation")
    print("- Bias-heavy diagnostic scenario")
    print("- Multi-seed variance analysis")
    print("- Reliability metrics assessment")
    print()

    # Check if API is running
    runner_test = EvaluationTestRunner()
    try:
        health_check = runner_test._get_request("/reliability")
        if not health_check['success']:
            print("⚠️  API server may not be running. Start with: make api")
            print("   Then re-run this script.")
            return
    except:
        print("⚠️  Cannot connect to API server. Start with: make api")
        print("   Then re-run this script.")
        return

    # Run all tests
    results = runner.run_all_tests()

    # Save results for analysis
    import json
    import time
    timestamp = int(time.time())

    results_file = f"manual_test_results_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: {results_file}")

    return results


if __name__ == "__main__":
    main()
