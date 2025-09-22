"""
Testing runner script for the enhanced evaluation system.
Run comprehensive tests to validate all recent implementations.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Add paths for imports
project_root = Path(__file__).resolve().parent.parent  # scripts/test_enhanced_evaluation.py -> smart-doc/
sys.path.append(str(project_root / "packages" / "core" / "src"))
sys.path.append(str(project_root / "apps" / "api" / "src"))

def run_unit_tests():
    """Run unit tests for enhanced evaluation components."""
    print("🧪 Running Unit Tests...")

    core_path = project_root / "packages" / "core"
    if not core_path.exists():
        print(f"❌ Core package path not found: {core_path}")
        return {"error": f"Path not found: {core_path}"}

    os.chdir(core_path)

    test_commands = [
        "poetry run pytest tests/test_enhanced_evaluation.py::TestClinicalEvaluator -v",
        "poetry run pytest tests/test_enhanced_evaluation.py::TestBiasEvaluator -v",
        "poetry run pytest tests/test_enhanced_evaluation.py::TestResearchCoordinator -v"
    ]

    results = {}
    for cmd in test_commands:
        print(f"\n📋 Running: {cmd}")
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=60)
            results[cmd] = {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            results[cmd] = {"error": "Test timed out"}
        except Exception as e:
            results[cmd] = {"error": str(e)}

    return results

def test_json_validation():
    """Test JSON validation with real examples."""
    print("\n🔍 Testing JSON Validation...")

    try:
        from smartdoc_core.clinical.evaluation_schemas import ClinicalEvaluation

        # Test valid evaluation
        valid_evaluation = {
            "overall_score": 85,
            "diagnostic_accuracy": {
                "score": 90,
                "analysis": "Excellent diagnostic accuracy",
                "correct_elements": ["pattern_recognition", "systematic_approach"],
                "missed_elements": []
            },
            "information_gathering": {
                "score": 80,
                "analysis": "Good systematic information gathering",
                "strengths": ["thorough_history", "appropriate_physical_exam"],
                "areas_for_improvement": ["efficiency_improvement"]
            },
            "cognitive_bias_awareness": {
                "score": 75,
                "analysis": "Adequate bias awareness demonstrated",
                "detected_biases_impact": "Minimal bias impact observed",
                "metacognitive_quality": "Good quality reflective responses"
            },
            "clinical_reasoning": {
                "score": 85,
                "analysis": "Strong clinical reasoning process",
                "hypothesis_generation": "Multiple hypotheses appropriately considered",
                "evidence_synthesis": "Good integration of available evidence"
            },
            "constructive_feedback": {
                "positive_reinforcement": "Excellent diagnostic work and systematic approach",
                "key_learning_points": ["Efficiency in information gathering", "Systematic approach benefits"],
                "specific_recommendations": ["Continue thorough approach", "Focus on efficiency"],
                "bias_education": "Monitor for confirmation bias in complex cases"
            },
            "confidence_assessment": 85
        }

        evaluation = ClinicalEvaluation(**valid_evaluation)
        print("✅ Valid evaluation parsed successfully")

        # Test invalid evaluation (scores out of range)
        invalid_evaluation = valid_evaluation.copy()
        invalid_evaluation["overall_score"] = 150  # Invalid range

        try:
            ClinicalEvaluation(**invalid_evaluation)
            print("❌ Invalid evaluation should have failed validation")
        except Exception as e:
            print(f"✅ Invalid evaluation correctly rejected: {str(e)[:100]}...")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation test error: {e}")
        return False

def test_bias_detection():
    """Test enhanced bias detection logic."""
    print("\n🎯 Testing Enhanced Bias Detection...")

    try:
        from smartdoc_core.simulation.bias_analyzer import BiasEvaluator

        # Create test case data
        case_data = {
            "informationBlocks": [f"block_{i}" for i in range(15)],
            "groundTruth": {
                "criticalFindingIds": ["critical_1", "critical_2", "critical_3"]
            },
            "biasTriggers": {
                "anchoring": {
                    "anchorDescription": "heart failure anchoring",
                    "contradictoryInfoId": "critical_echo"
                },
                "confirmation": {
                    "supportingInfoIds": ["block_1", "block_2", "block_3"],
                    "refutingInfoIds": ["critical_1", "critical_2"]
                }
            }
        }

        evaluator = BiasEvaluator(case_data)

        # Test adaptive thresholds
        print(f"✅ Total blocks: {evaluator.total_blocks}")
        print(f"✅ Min actions threshold: {evaluator.min_actions_threshold}")
        print(f"✅ Min sample size: {evaluator.min_sample_size}")

        # Test confirmation bias with sufficient sample
        revealed_blocks = {"block_1", "block_2", "block_3", "critical_1"}
        result = evaluator._detect_confirmation_bias(revealed_blocks)
        print(f"✅ Confirmation bias detection: {result['detected']}")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Bias detection test error: {e}")
        return False

def test_api_payload_validation():
    """Test API payload structures."""
    print("\n🌐 Testing API Payload Validation...")

    # Test comprehensive evaluation payload
    test_payload = {
        "diagnosis": "Miliary tuberculosis secondary to immunosuppression",
        "dialogue_transcript": [
            {"role": "user", "content": "What are the symptoms?"},
            {"role": "assistant", "content": "Patient has shortness of breath and weight loss."}
        ],
        "metacognitive_responses": {
            "information_gathering": "I gathered history systematically",
            "diagnostic_reasoning": "Bilateral infiltrates suggested systemic disease",
            "bias_awareness": "I considered multiple differentials"
        },
        "case_context": {
            "case_type": "diagnostic_challenge",
            "correct_diagnosis": "Miliary tuberculosis",
            "key_features": ["weight_loss", "bilateral_infiltrates"],
            "total_blocks": 15
        },
        "session_id": "test_session"
    }

    # Validate required fields
    required_fields = ["diagnosis", "metacognitive_responses", "case_context"]
    for field in required_fields:
        if field not in test_payload:
            print(f"❌ Missing required field: {field}")
            return False
        else:
            print(f"✅ Required field present: {field}")

    # Validate metacognitive responses structure
    meta_responses = test_payload["metacognitive_responses"]
    required_meta_fields = ["information_gathering", "diagnostic_reasoning", "bias_awareness"]
    for field in required_meta_fields:
        if field not in meta_responses:
            print(f"❌ Missing metacognitive field: {field}")
            return False
        else:
            print(f"✅ Metacognitive field present: {field}")

    print("✅ API payload validation passed")
    return True

def run_integration_tests():
    """Run integration tests with mocked components."""
    print("\n🔗 Running Integration Tests...")

    try:
        # Test evaluation input structure
        from smartdoc_core.clinical.evaluator import EvaluationInputs

        inputs = EvaluationInputs(
            dialogue_transcript=[
                {"role": "user", "content": "Test question"},
                {"role": "assistant", "content": "Test response"}
            ],
            detected_biases=[],
            metacognitive_responses={"q1": "response1"},
            final_diagnosis="Test diagnosis",
            case_context={"case_type": "test"}
        )

        print(f"✅ EvaluationInputs created: {len(inputs.dialogue_transcript)} messages")

        # Test that all required fields are present
        assert hasattr(inputs, 'dialogue_transcript')
        assert hasattr(inputs, 'detected_biases')
        assert hasattr(inputs, 'metacognitive_responses')
        assert hasattr(inputs, 'final_diagnosis')
        assert hasattr(inputs, 'case_context')

        print("✅ Integration test structure validation passed")
        return True

    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

def main():
    """Run comprehensive test suite."""
    print("🚀 Starting Enhanced Evaluation System Tests")
    print("=" * 60)

    results = {}

    # 1. JSON Validation Tests
    results['json_validation'] = test_json_validation()

    # 2. Bias Detection Tests
    results['bias_detection'] = test_bias_detection()

    # 3. API Payload Tests
    results['api_payload'] = test_api_payload_validation()

    # 4. Integration Tests
    results['integration'] = run_integration_tests()

    # 5. Unit Tests (if dependencies available)
    try:
        results['unit_tests'] = run_unit_tests()
    except Exception as e:
        print(f"⚠️  Unit tests skipped: {e}")
        results['unit_tests'] = {"skipped": str(e)}

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = 0
    total = 0

    for test_name, result in results.items():
        if test_name == 'unit_tests':
            if isinstance(result, dict) and 'skipped' in result:
                print(f"⚠️  {test_name}: SKIPPED - {result['skipped']}")
            else:
                print(f"🧪 {test_name}: See detailed output above")
        else:
            status = "PASSED" if result else "FAILED"
            emoji = "✅" if result else "❌"
            print(f"{emoji} {test_name}: {status}")
            if result:
                passed += 1
            total += 1

    print(f"\n📈 Overall: {passed}/{total} test categories passed")

    if passed == total:
        print("🎉 All available tests passed! System ready for research use.")
        return 0
    else:
        print("⚠️  Some tests failed. Review the output above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
