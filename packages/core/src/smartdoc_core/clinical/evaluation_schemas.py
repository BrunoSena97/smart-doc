"""
Pydantic models for structured clinical evaluation output validation.
Ensures LLM responses conform to expected schemas with proper validation.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator


class SimplifiedDimensionScore(BaseModel):
    """Simplified schema for evaluation dimension scores."""
    score: int = Field(..., ge=0, le=100, description="Score from 0-100")
    analysis: str = Field(..., min_length=10, description="Brief analysis of performance")


class ComprehensiveFeedback(BaseModel):
    """Comprehensive feedback focused on practical improvement."""
    strengths: str = Field(..., min_length=10, description="What the student did well")
    areas_for_improvement: str = Field(..., min_length=10, description="Areas needing development")
    key_recommendations: List[str] = Field(..., description="Actionable recommendations")

    @validator('key_recommendations')
    def validate_recommendations(cls, v):
        if len(v) < 1:
            raise ValueError("At least one recommendation is required")
        return v


class SimplifiedClinicalEvaluation(BaseModel):
    """Simplified clinical evaluation focused on three core areas."""
    information_gathering: SimplifiedDimensionScore
    diagnostic_accuracy: SimplifiedDimensionScore
    cognitive_bias_awareness: SimplifiedDimensionScore
    comprehensive_feedback: ComprehensiveFeedback


# Keep the original complex schema for backward compatibility
class DimensionScore(BaseModel):
    """Base schema for evaluation dimension scores."""
    score: int = Field(..., ge=0, le=100, description="Score from 0-100")
    analysis: str = Field(..., min_length=10, description="Detailed analysis (minimum 10 characters)")


class DiagnosticAccuracy(DimensionScore):
    """Diagnostic accuracy evaluation with evidence tracking."""
    correct_elements: List[str] = Field(default_factory=list, description="Correct diagnostic elements identified")
    missed_elements: List[str] = Field(default_factory=list, description="Critical diagnostic elements missed")


class InformationGathering(DimensionScore):
    """Information gathering evaluation with strengths/weaknesses."""
    strengths: List[str] = Field(default_factory=list, description="Strengths in information gathering")
    areas_for_improvement: List[str] = Field(default_factory=list, description="Areas needing improvement")


class CognitiveBiasAwareness(DimensionScore):
    """Cognitive bias awareness evaluation."""
    detected_biases_impact: str = Field(..., min_length=10, description="Impact of detected biases")
    metacognitive_quality: str = Field(..., min_length=10, description="Quality of metacognitive reflection")


class ClinicalReasoning(DimensionScore):
    """Clinical reasoning evaluation with process assessment."""
    hypothesis_generation: str = Field(..., min_length=10, description="Quality of hypothesis generation")
    evidence_synthesis: str = Field(..., min_length=10, description="Quality of evidence synthesis")


class ConstructiveFeedback(BaseModel):
    """Structured constructive feedback for learners."""
    positive_reinforcement: str = Field(..., min_length=10, description="Positive reinforcement message")
    key_learning_points: List[str] = Field(..., description="Key learning points (minimum 1)")
    specific_recommendations: List[str] = Field(..., description="Specific recommendations (minimum 1)")
    bias_education: str = Field(..., min_length=10, description="Cognitive bias education message")

    @validator('key_learning_points')
    def validate_key_learning_points(cls, v):
        if len(v) < 1:
            raise ValueError("At least one key learning point is required")
        return v

    @validator('specific_recommendations')
    def validate_specific_recommendations(cls, v):
        if len(v) < 1:
            raise ValueError("At least one specific recommendation is required")
        return v


class ClinicalEvaluation(BaseModel):
    """Complete clinical evaluation schema with validation."""
    overall_score: int = Field(..., ge=0, le=100, description="Overall score from 0-100")
    diagnostic_accuracy: DiagnosticAccuracy
    information_gathering: InformationGathering
    cognitive_bias_awareness: CognitiveBiasAwareness
    clinical_reasoning: ClinicalReasoning
    constructive_feedback: ConstructiveFeedback
    confidence_assessment: int = Field(..., ge=0, le=100, description="Evaluator confidence from 0-100")

    @validator('overall_score')
    def validate_overall_score(cls, v, values):
        """Ensure overall score is reasonable given dimension scores."""
        if 'diagnostic_accuracy' in values and 'information_gathering' in values and 'cognitive_bias_awareness' in values and 'clinical_reasoning' in values:
            # Calculate weighted average as sanity check
            weights = {'diagnostic_accuracy': 0.30, 'information_gathering': 0.25, 'cognitive_bias_awareness': 0.25, 'clinical_reasoning': 0.20}
            weighted_avg = (
                values['diagnostic_accuracy'].score * weights['diagnostic_accuracy'] +
                values['information_gathering'].score * weights['information_gathering'] +
                values['cognitive_bias_awareness'].score * weights['cognitive_bias_awareness'] +
                values['clinical_reasoning'].score * weights['clinical_reasoning']
            )
            # Allow ±15 points variance from calculated average
            if abs(v - weighted_avg) > 15:
                raise ValueError(f"Overall score {v} deviates significantly from weighted average {weighted_avg:.1f}")
        return v


class BiasAnalysisDetail(BaseModel):
    """Individual bias analysis result."""
    detected: bool = Field(..., description="Whether bias was detected")
    confidence: int = Field(..., ge=0, le=100, description="Detection confidence from 0-100")
    evidence: str = Field(..., min_length=5, description="Evidence supporting detection")
    explanation: str = Field(..., min_length=10, description="Detailed explanation")


class BiasAnalysis(BaseModel):
    """Structured bias analysis schema."""
    anchoring_bias: BiasAnalysisDetail
    confirmation_bias: BiasAnalysisDetail
    premature_closure: BiasAnalysisDetail
    overall_reasoning_quality: int = Field(..., ge=0, le=100, description="Overall reasoning quality score")
    key_insights: List[str] = Field(default_factory=list, description="Key insights from analysis")


class ReliabilityMetrics(BaseModel):
    """Reliability and validation metrics for research."""
    model_temperature: float = Field(..., description="Model temperature used")
    model_name: str = Field(..., description="Model name/version")
    evaluation_timestamp: str = Field(..., description="Timestamp of evaluation")
    seed_value: Optional[int] = Field(None, description="Random seed if used")
    inter_rater_agreement: Optional[float] = Field(None, ge=0, le=1, description="Agreement with human expert")
    confidence_calibration: Optional[float] = Field(None, ge=0, le=1, description="Confidence calibration score")


class ResearchEvaluationOutput(BaseModel):
    """Complete research-grade evaluation output with reliability metrics."""
    evaluation: ClinicalEvaluation
    bias_analysis: Optional[BiasAnalysis] = None
    reliability_metrics: ReliabilityMetrics
    rule_based_bias_results: Optional[Dict[str, Any]] = None
    llm_rule_agreement: Optional[Dict[str, float]] = None
    raw_llm_response: Optional[str] = None
    validation_errors: List[str] = Field(default_factory=list, description="Any validation issues encountered")
