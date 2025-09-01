"""
Test the refactored clinical evaluator to ensure it works with the new architecture.
"""

import pytest
from smartdoc_core.clinical.evaluator import ClinicalEvaluator, EvaluationInputs


def test_eval_smoke():
    """Basic smoke test for the refactored evaluator."""
    ev = ClinicalEvaluator()
    inputs = EvaluationInputs(
        dialogue_transcript=[{"role": "user", "message": "Hello, I have chest pain"}],
        detected_biases=[],
        metacognitive_responses={"What did you learn?": "A long enough answer about learning."},
        final_diagnosis="Test Diagnosis",
        case_context={"correct_diagnosis": "CHF"},
    )
    out = ev.evaluate(inputs)
    assert out["success"]
    assert "evaluation" in out


def test_legacy_compatibility():
    """Test that legacy method names still work."""
    ev = ClinicalEvaluator()

    # Test legacy evaluate_clinical_performance method
    result = ev.evaluate_clinical_performance(
        dialogue_transcript=[{"role": "user", "message": "chest pain"}],
        detected_biases=[],
        metacognitive_responses={"Q": "A"},
        final_diagnosis="Test Dx",
        case_context={}
    )

    assert result["success"]
    assert "evaluation" in result


def test_bias_analysis():
    """Test the deep bias analysis functionality."""
    ev = ClinicalEvaluator()

    transcript = [
        {"role": "user", "message": "patient has chest pain"},
        {"role": "assistant", "message": "Tell me more about the chest pain"},
        {"role": "user", "message": "sharp, radiating to left arm"}
    ]

    result = ev.deep_bias_analysis(transcript, "Myocardial infarction")
    assert result["success"]
    assert "bias_analysis" in result


def test_fallback_behavior():
    """Test that fallback works when LLM fails."""
    from unittest.mock import Mock

    # Create evaluator with mocked provider that fails
    mock_provider = Mock()
    mock_provider.generate.side_effect = Exception("LLM failed")

    ev = ClinicalEvaluator(provider=mock_provider)
    inputs = EvaluationInputs(
        dialogue_transcript=[],
        detected_biases=[],
        metacognitive_responses={"Q": "A"},
        final_diagnosis="Test",
        case_context={}
    )

    result = ev.evaluate(inputs)
    assert result["success"]  # Should still succeed with fallback
    assert "fallback_used" in result or result["evaluation"]["overall_score"] == 75  # fallback score


if __name__ == "__main__":
    test_eval_smoke()
    test_legacy_compatibility()
    test_bias_analysis()
    test_fallback_behavior()
    print("✅ All evaluator tests passed!")
