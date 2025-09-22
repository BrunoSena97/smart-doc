"""
Comprehensive test suite for the enhanced clinical evaluation system.
Tests structured validation, rubric-based scoring, bias detection, and research features.
"""

import pytest
import json
from datetime import datetime
from unittest.mock import Mock, patch
from typing import Dict, Any

# Import the modules we're testing
from smartdoc_core.clinical.evaluator import ClinicalEvaluator, EvaluationInputs
from smartdoc_core.clinical.research_coordinator import ResearchEvaluationCoordinator
from smartdoc_core.clinical.evaluation_schemas import ClinicalEvaluation, BiasAnalysis
from smartdoc_core.simulation.bias_analyzer import BiasEvaluator


class TestClinicalEvaluator:
    """Test the enhanced ClinicalEvaluator with structured validation."""

    @pytest.fixture
    def mock_provider(self):
        """Mock LLM provider for testing."""
        provider = Mock()
        provider.model = "test-model"
        return provider

    @pytest.fixture
    def sample_evaluation_inputs(self):
        """Sample inputs for evaluation testing."""
        return EvaluationInputs(
            dialogue_transcript=[
                {"role": "user", "content": "What are the patient's symptoms?"},
                {"role": "assistant", "content": "The patient reports shortness of breath and chest pain."},
                {"role": "user", "content": "Can you perform a physical examination?"},
                {"role": "assistant", "content": "Physical exam reveals decreased breath sounds bilaterally."}
            ],
            detected_biases=[
                {"bias_type": "anchoring", "description": "Early focus on heart failure"}
            ],
            metacognitive_responses={
                "reflection_1": "I initially thought about heart failure but reconsidered after finding normal echo.",
                "reflection_2": "I should have gathered more social history earlier.",
                "reflection_3": "The bilateral findings made me consider systemic causes."
            },
            final_diagnosis="Miliary tuberculosis secondary to immunosuppression",
            case_context={
                "case_type": "diagnostic_challenge",
                "correct_diagnosis": "Miliary tuberculosis",
                "key_features": ["weight_loss", "immunosuppression", "bilateral_infiltrates"],
                "total_blocks": 15
            }
        )

    @pytest.fixture
    def valid_json_response(self):
        """Valid JSON response from LLM."""
        return '''
        <<<JSON_START>>>
        {
          "overall_score": 78,
          "diagnostic_accuracy": {
            "score": 85,
            "analysis": "Correct final diagnosis with solid reasoning",
            "correct_elements": ["miliary_pattern", "immunosuppression_link"],
            "missed_elements": ["early_weight_loss_significance"]
          },
          "information_gathering": {
            "score": 72,
            "analysis": "Good systematic approach but missed social history initially",
            "strengths": ["thorough_physical_exam", "appropriate_imaging"],
            "areas_for_improvement": ["earlier_social_history", "medication_review"]
          },
          "cognitive_bias_awareness": {
            "score": 80,
            "analysis": "Good recognition of initial anchoring and self-correction",
            "detected_biases_impact": "Initial anchoring on heart failure was corrected",
            "metacognitive_quality": "Reflective responses show good self-awareness"
          },
          "clinical_reasoning": {
            "score": 75,
            "analysis": "Sound reasoning process with hypothesis revision",
            "hypothesis_generation": "Multiple differential diagnoses considered",
            "evidence_synthesis": "Good integration of clinical and imaging findings"
          },
          "constructive_feedback": {
            "positive_reinforcement": "Excellent self-correction and diagnostic accuracy",
            "key_learning_points": ["Early social history importance", "Systematic approach benefits"],
            "specific_recommendations": ["Always consider immunosuppression", "Weight loss red flag"],
            "bias_education": "Good awareness of anchoring bias and correction"
          },
          "confidence_assessment": 85
        }
        <<<JSON_END>>>
        '''

    def test_structured_json_extraction(self, mock_provider, sample_evaluation_inputs, valid_json_response):
        """Test robust JSON extraction with sentinel markers."""
        mock_provider.generate.return_value = valid_json_response

        evaluator = ClinicalEvaluator(
            provider=mock_provider,
            enable_validation=True,
            temperature=0.1
        )

        result = evaluator.evaluate(sample_evaluation_inputs)

        assert result["success"] is True
        assert result["extraction_success"] is True
        assert "validation_errors" in result
        assert len(result["validation_errors"]) == 0

        evaluation = result["evaluation"]
        assert evaluation["overall_score"] == 78
        assert evaluation["diagnostic_accuracy"]["score"] == 85
        assert len(evaluation["constructive_feedback"]["key_learning_points"]) >= 1

    def test_json_extraction_fallback_strategies(self, mock_provider, sample_evaluation_inputs):
        """Test fallback JSON extraction strategies."""
        # Test case: JSON without sentinels
        json_without_sentinels = '''
        Here is my evaluation:
        {
          "overall_score": 65,
          "diagnostic_accuracy": {"score": 70, "analysis": "Partially correct"},
          "information_gathering": {"score": 60, "analysis": "Limited exploration"},
          "cognitive_bias_awareness": {"score": 65, "analysis": "Some awareness"},
          "clinical_reasoning": {"score": 60, "analysis": "Basic reasoning"},
          "constructive_feedback": {
            "positive_reinforcement": "Good effort",
            "key_learning_points": ["Gather more info"],
            "specific_recommendations": ["Be more systematic"],
            "bias_education": "Watch for anchoring"
          },
          "confidence_assessment": 70
        }
        This completes the evaluation.
        '''

        mock_provider.generate.return_value = json_without_sentinels

        evaluator = ClinicalEvaluator(provider=mock_provider, enable_validation=False)
        result = evaluator.evaluate(sample_evaluation_inputs)

        assert result["success"] is True
        evaluation = result["evaluation"]
        assert evaluation["overall_score"] == 65

    def test_validation_and_repair_mechanism(self, mock_provider, sample_evaluation_inputs):
        """Test Pydantic validation with repair mechanism."""
        # Invalid JSON (missing required fields)
        invalid_json = '''
        <<<JSON_START>>>
        {
          "overall_score": 150,
          "diagnostic_accuracy": {"score": 95},
          "information_gathering": {"score": 80},
          "cognitive_bias_awareness": {"score": 70},
          "clinical_reasoning": {"score": 85},
          "confidence_assessment": 90
        }
        <<<JSON_END>>>
        '''

        # Repaired JSON
        repaired_json = '''
        <<<JSON_START>>>
        {
          "overall_score": 85,
          "diagnostic_accuracy": {
            "score": 95,
            "analysis": "Strong diagnostic performance",
            "correct_elements": ["accurate_diagnosis"],
            "missed_elements": []
          },
          "information_gathering": {
            "score": 80,
            "analysis": "Good information gathering",
            "strengths": ["systematic_approach"],
            "areas_for_improvement": ["efficiency"]
          },
          "cognitive_bias_awareness": {
            "score": 70,
            "analysis": "Adequate bias awareness",
            "detected_biases_impact": "Minimal impact observed",
            "metacognitive_quality": "Basic reflection quality"
          },
          "clinical_reasoning": {
            "score": 85,
            "analysis": "Strong reasoning process",
            "hypothesis_generation": "Multiple hypotheses considered",
            "evidence_synthesis": "Good evidence integration"
          },
          "constructive_feedback": {
            "positive_reinforcement": "Strong clinical performance",
            "key_learning_points": ["Efficiency improvement"],
            "specific_recommendations": ["Time management"],
            "bias_education": "Continue monitoring for biases"
          },
          "confidence_assessment": 85
        }
        <<<JSON_END>>>
        '''

        mock_provider.generate.side_effect = [invalid_json, repaired_json]

        evaluator = ClinicalEvaluator(provider=mock_provider, enable_validation=True)
        result = evaluator.evaluate(sample_evaluation_inputs)

        assert result["success"] is True
        assert len(result.get("validation_errors", [])) == 0  # Should be repaired
        assert result["evaluation"]["overall_score"] == 85  # Corrected value

    def test_bias_analysis_with_evidence_linking(self, mock_provider, sample_evaluation_inputs):
        """Test enhanced bias analysis with evidence linking."""
        bias_response = '''
        <<<JSON_START>>>
        {
          "anchoring_bias": {
            "detected": true,
            "confidence": 80,
            "evidence": "Turn 1-3: Repeated focus on cardiac causes despite normal echo in turn 4",
            "explanation": "Student anchored on heart failure but showed good self-correction"
          },
          "confirmation_bias": {
            "detected": false,
            "confidence": 20,
            "evidence": "Balanced information seeking across categories",
            "explanation": "No evidence of selective information gathering"
          },
          "premature_closure": {
            "detected": false,
            "confidence": 15,
            "evidence": "Adequate information gathering with 12 blocks revealed",
            "explanation": "Thorough investigation before final diagnosis"
          },
          "overall_reasoning_quality": 75,
          "key_insights": ["Good self-correction", "Systematic approach"]
        }
        <<<JSON_END>>>
        '''

        mock_provider.generate.return_value = bias_response

        evaluator = ClinicalEvaluator(provider=mock_provider)
        result = evaluator.deep_bias_analysis(
            sample_evaluation_inputs.dialogue_transcript,
            sample_evaluation_inputs.final_diagnosis
        )

        assert result["success"] is True
        bias_analysis = result["bias_analysis"]
        assert bias_analysis["anchoring_bias"]["detected"] is True
        assert "Turn 1-3" in bias_analysis["anchoring_bias"]["evidence"]


class TestBiasEvaluator:
    """Test enhanced bias detection with case-adaptive logic."""

    @pytest.fixture
    def sample_case_data(self):
        """Sample case data for bias testing."""
        return {
            "informationBlocks": [f"block_{i}" for i in range(20)],  # 20 total blocks
            "groundTruth": {
                "criticalFindingIds": ["critical_1", "critical_2", "critical_3", "critical_4"]
            },
            "biasTriggers": {
                "anchoring": {
                    "anchorDescription": "heart failure exacerbation anchored by preliminary chest x-ray",
                    "contradictoryInfoId": "critical_echo"
                },
                "confirmation": {
                    "supportingInfoIds": ["pe_resp", "lab_bnp", "img_prelim_cxr"],
                    "refutingInfoIds": ["hist_weight_loss", "pe_cardiac_neg", "critical_formal_cxr", "critical_echo"]
                }
            }
        }

    @pytest.fixture
    def sample_session_log(self):
        """Sample session log for bias detection."""
        return [
            {
                "action_type": "add_hypothesis",
                "details": {"diagnosis": "Heart failure exacerbation"},
                "timestamp": "2025-07-20T10:00:00",
                "intent_id": "diagnosis"
            },
            {
                "action_type": "view_info",
                "details": {"blockId": "pe_resp"},
                "timestamp": "2025-07-20T10:01:00",
                "intent_id": "exam_cardiovascular",
                "user_query": "examine heart and lungs"
            },
            {
                "action_type": "view_info",
                "details": {"blockId": "lab_bnp"},
                "timestamp": "2025-07-20T10:02:00",
                "intent_id": "lab_tests_cardiac"
            },
            {
                "action_type": "view_info",
                "details": {"blockId": "critical_echo"},
                "timestamp": "2025-07-20T10:03:00",
                "intent_id": "imaging_cardiac"
            },
            {
                "action_type": "view_info",
                "details": {"blockId": "pe_resp"},
                "timestamp": "2025-07-20T10:04:00",
                "intent_id": "exam_cardiovascular",
                "user_query": "check heart sounds again"
            },
            {
                "action_type": "submit_final_diagnosis",
                "details": {"diagnosis": "Heart failure exacerbation"},
                "timestamp": "2025-07-20T10:05:00"
            }
        ]

    def test_case_adaptive_thresholds(self, sample_case_data):
        """Test that bias evaluator adapts thresholds based on case complexity."""
        evaluator = BiasEvaluator(sample_case_data)

        # Should calculate adaptive thresholds
        assert evaluator.total_blocks == 20
        assert evaluator.min_actions_threshold == max(3, round(0.2 * 20))  # 4
        assert evaluator.min_critical_threshold == 0.5
        assert evaluator.min_sample_size == 3

    def test_anchoring_persistence_detection(self, sample_case_data, sample_session_log):
        """Test enhanced anchoring detection with persistence after contradiction."""
        evaluator = BiasEvaluator(sample_case_data)

        hypotheses = [{"diagnosis": "Heart failure exacerbation", "timestamp": "2025-07-20T10:00:00"}]
        final_diagnosis = "Heart failure exacerbation"

        result = evaluator._detect_anchoring_bias(sample_session_log, hypotheses, final_diagnosis)

        assert result["detected"] is True
        assert "persistence_score" in result
        assert result["confidence"] > 0.6  # Should have high confidence due to persistence

    def test_confirmation_bias_minimum_sample_size(self, sample_case_data):
        """Test confirmation bias detection respects minimum sample size."""
        evaluator = BiasEvaluator(sample_case_data)

        # Test with insufficient sample (< 3 pieces of evidence)
        small_revealed_blocks = {"pe_resp", "lab_bnp"}  # Only 2 blocks
        result = evaluator._detect_confirmation_bias(small_revealed_blocks)

        assert result["detected"] is False
        assert "sample size" in result["reason"].lower()

    def test_confirmation_bias_with_sufficient_sample(self, sample_case_data):
        """Test confirmation bias detection with sufficient evidence sample."""
        evaluator = BiasEvaluator(sample_case_data)

        # Test with sufficient supporting evidence, minimal refuting
        revealed_blocks = {"pe_resp", "lab_bnp", "img_prelim_cxr", "hist_weight_loss"}  # 3 supporting, 1 refuting
        result = evaluator._detect_confirmation_bias(revealed_blocks)

        assert result["detected"] is True
        assert result["evidence_sample_size"] >= evaluator.min_sample_size
        assert result["support_ratio"] > result["refute_ratio"]

    def test_premature_closure_adaptive_thresholds(self, sample_case_data, sample_session_log):
        """Test premature closure detection with case-adaptive thresholds."""
        evaluator = BiasEvaluator(sample_case_data)

        # Test with minimal exploration (should trigger detection)
        minimal_revealed_blocks = {"pe_resp", "lab_bnp"}  # Only 2 blocks out of 20
        result = evaluator._detect_premature_closure(minimal_revealed_blocks, sample_session_log[:3])

        assert result["detected"] is True
        assert result["exploration_ratio"] < 0.15  # Less than 15% exploration
        assert "criteria_violations" in result

    def test_intent_based_real_time_detection(self, sample_case_data):
        """Test real-time bias detection using intent taxonomy."""
        evaluator = BiasEvaluator(sample_case_data)

        # Mock interactions with high cardiovascular intent focus
        interactions = [
            {"intent_id": "exam_cardiovascular", "user_query": "check heart"},
            {"intent_id": "lab_tests_cardiac", "user_query": "bnp level"},
            {"intent_id": "imaging_cardiac", "user_query": "echo results"},
            {"intent_id": "exam_cardiovascular", "user_query": "heart sounds"}
        ]

        result = evaluator._real_time_anchoring_check(interactions, "exam_cardiovascular", "check heart again")

        assert result["detected"] is True
        assert result["intent_based"] is True
        assert result["confidence"] > 0.6


class TestResearchCoordinator:
    """Test research coordination and agreement analysis."""

    @pytest.fixture
    def mock_evaluator(self):
        """Mock clinical evaluator for testing."""
        evaluator = Mock()
        evaluator.temperature = 0.1
        evaluator.enable_validation = True
        return evaluator

    @pytest.fixture
    def coordinator(self, mock_evaluator):
        """Research coordinator for testing."""
        return ResearchEvaluationCoordinator(
            clinical_evaluator=mock_evaluator,
            enable_agreement_tracking=True,
            enable_discrepancy_logging=True
        )

    def test_agreement_metrics_calculation(self, coordinator):
        """Test agreement metrics between rule-based and LLM analysis."""
        rule_based_analysis = {
            "anchoring_bias": {"detected": True, "confidence": 80},
            "confirmation_bias": {"detected": False, "confidence": 20},
            "premature_closure": {"detected": True, "confidence": 70}
        }

        llm_bias_analysis = {
            "anchoring_bias": {"detected": True, "confidence": 85},
            "confirmation_bias": {"detected": False, "confidence": 15},
            "premature_closure": {"detected": False, "confidence": 40}  # Disagreement
        }

        agreement_metrics, discrepancies = coordinator._compute_agreement_metrics(
            rule_based_analysis, llm_bias_analysis, "test_session"
        )

        assert agreement_metrics["total_comparisons"] == 3
        assert agreement_metrics["agreement_count"] == 2  # 2 agreements, 1 disagreement
        assert agreement_metrics["disagreement_count"] == 1
        assert len(discrepancies) == 1
        assert discrepancies[0]["bias_type"] == "premature_closure"

    def test_multi_seed_variance_testing(self, coordinator, mock_evaluator):
        """Test multi-seed evaluation for consistency testing."""
        # Mock different evaluation results for different seeds
        mock_results = [
            {
                "success": True,
                "evaluation": {
                    "overall_score": 75,
                    "diagnostic_accuracy": {"score": 80},
                    "information_gathering": {"score": 70},
                    "cognitive_bias_awareness": {"score": 75},
                    "clinical_reasoning": {"score": 75},
                    "confidence_assessment": 80
                }
            },
            {
                "success": True,
                "evaluation": {
                    "overall_score": 78,
                    "diagnostic_accuracy": {"score": 82},
                    "information_gathering": {"score": 74},
                    "cognitive_bias_awareness": {"score": 76},
                    "clinical_reasoning": {"score": 80},
                    "confidence_assessment": 85
                }
            },
            {
                "success": True,
                "evaluation": {
                    "overall_score": 73,
                    "diagnostic_accuracy": {"score": 78},
                    "information_gathering": {"score": 68},
                    "cognitive_bias_awareness": {"score": 74},
                    "clinical_reasoning": {"score": 72},
                    "confidence_assessment": 75
                }
            }
        ]

        mock_evaluator.evaluate.side_effect = mock_results

        inputs = EvaluationInputs(
            dialogue_transcript=[],
            detected_biases=[],
            metacognitive_responses={"q1": "a1"},
            final_diagnosis="test diagnosis",
            case_context={}
        )

        result = coordinator.multi_seed_evaluation(inputs, num_runs=3, seed_values=[42, 123, 789])

        assert result["success"] is True
        assert result["successful_runs"] == 3
        assert "variance_metrics" in result

        variance_metrics = result["variance_metrics"]
        assert "overall_score" in variance_metrics["dimension_variance"]
        assert variance_metrics["overall_consistency"] in ["high", "moderate", "low"]


class TestIntegrationWithAPI:
    """Integration tests for the API endpoints."""

    def test_comprehensive_evaluation_payload(self):
        """Test the payload structure for comprehensive evaluation."""
        test_payload = {
            "diagnosis": "Miliary tuberculosis secondary to immunosuppression from infliximab therapy",
            "metacognitive_responses": {
                "information_gathering": "I initially focused on cardiac causes but broadened my investigation after the normal echo. I should have asked about medications and social history earlier.",
                "diagnostic_reasoning": "The bilateral infiltrates with weight loss made me consider systemic causes. The history of infliximab was the key finding.",
                "bias_awareness": "I recognize I may have anchored on heart failure initially due to the presenting symptoms and preliminary CXR."
            },
            "case_context": {
                "case_type": "diagnostic_challenge",
                "correct_diagnosis": "Miliary tuberculosis",
                "key_features": ["weight_loss", "immunosuppression", "bilateral_infiltrates", "infliximab_therapy"],
                "total_blocks": 18
            },
            "session_id": "test_session_123"
        }

        # Validate payload structure
        assert "diagnosis" in test_payload
        assert "metacognitive_responses" in test_payload
        assert len(test_payload["metacognitive_responses"]) >= 3
        assert "case_context" in test_payload
        assert test_payload["case_context"]["total_blocks"] > 0

    def test_reliability_metrics_structure(self):
        """Test the expected structure of reliability metrics."""
        expected_reliability_structure = {
            "success": True,
            "reliability_report": {
                "total_evaluations": 0,
                "successful_evaluations": 0,
                "success_rate": 0.0,
                "average_agreement_score": 0.0,
                "inter_method_agreement": 0.0
            },
            "research_data_summary": {
                "total_evaluations": 0,
                "total_discrepancies": 0,
                "configuration": {}
            }
        }

        # This structure should be returned by /api/v1/evaluation/reliability
        assert "reliability_report" in expected_reliability_structure
        assert "research_data_summary" in expected_reliability_structure


if __name__ == "__main__":
    # Run specific test categories
    print("🧪 Running Enhanced Clinical Evaluation Tests...")

    # You can run individual test classes
    import subprocess

    test_commands = [
        "python -m pytest test_enhanced_evaluation.py::TestClinicalEvaluator -v",
        "python -m pytest test_enhanced_evaluation.py::TestBiasEvaluator -v",
        "python -m pytest test_enhanced_evaluation.py::TestResearchCoordinator -v"
    ]

    for cmd in test_commands:
        print(f"\n📋 Running: {cmd}")
        # subprocess.run(cmd.split(), capture_output=True)
