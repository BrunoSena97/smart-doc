#!/usr/bin/env python3
"""
Clinical Interview Evaluation Framework
Based on Ana Guedes' dissertation methodologies (Chapter 4)

This module implements evaluation metrics for clinical interviews and cognitive bias detection
in the SmartDoc virtual patient simulation system.
"""

import json
import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class CognitiveBias(Enum):
    ANCHORING = "anchoring_bias"
    CONFIRMATION = "confirmation_bias"
    AVAILABILITY = "availability_bias"
    DIAGNOSTIC_MOMENTUM = "diagnostic_momentum"
    PREMATURE_CLOSURE = "premature_closure"
    FRAMING_EFFECT = "framing_effect"
    OVERCONFIDENCE = "overconfidence_bias"

@dataclass
class InterviewMetrics:
    """Metrics for evaluating clinical interview quality."""
    session_id: str
    student_id: str
    case_id: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    total_questions: int
    diagnostic_accuracy_score: float
    information_gathering_score: float
    clinical_reasoning_score: float
    bias_detection_results: Dict[CognitiveBias, float]
    final_diagnosis: str
    confidence_level: float

class ClinicalInterviewEvaluator:
    """
    Evaluates clinical interviews using methodologies adapted from Ana Guedes' dissertation.
    Focuses on diagnostic accuracy, clinical reasoning quality, and cognitive bias detection.
    """
    
    def __init__(self):
        # Bias detection thresholds (can be tuned based on research)
        self.bias_thresholds = {
            CognitiveBias.ANCHORING: 0.7,
            CognitiveBias.CONFIRMATION: 0.6,
            CognitiveBias.AVAILABILITY: 0.5,
            CognitiveBias.DIAGNOSTIC_MOMENTUM: 0.8,
            CognitiveBias.PREMATURE_CLOSURE: 0.75
        }
        
        # Question categories for information gathering assessment
        self.question_categories = {
            "history_taking": ["hpi_", "pmh_", "social_", "family_"],
            "physical_exam": ["exam_", "vital_", "general_appearance"],
            "investigations": ["labs_", "imaging_", "discoverable_"],
            "medication_review": ["meds_", "allergies"],
            "differential_diagnosis": ["discoverable_", "reassessment"]
        }
        
        # Expected diagnostic progression for the heart failure case
        self.diagnostic_milestones = {
            "initial_assessment": ["profile_", "hpi_chief_complaint"],
            "symptom_exploration": ["hpi_", "exam_"],
            "investigation_review": ["labs_", "imaging_"],
            "differential_consideration": ["discoverable_"],
            "final_diagnosis": ["miliary_tuberculosis"]
        }

    def evaluate_session(self, session_data: Dict[str, Any]) -> InterviewMetrics:
        """
        Main evaluation function that assesses a complete interview session.
        
        Args:
            session_data: Dictionary containing all interaction data from the session
            
        Returns:
            InterviewMetrics object with comprehensive evaluation results
        """
        # Extract basic session information
        session_info = self._extract_session_info(session_data)
        
        # Evaluate diagnostic accuracy
        diagnostic_score = self._assess_diagnostic_accuracy(session_data)
        
        # Assess information gathering quality
        info_gathering_score = self._assess_information_gathering(session_data)
        
        # Evaluate clinical reasoning process
        reasoning_score = self._evaluate_reasoning_process(session_data)
        
        # Detect cognitive biases
        bias_results = self._detect_cognitive_biases(session_data)
        
        return InterviewMetrics(
            session_id=session_info["session_id"],
            student_id=session_info["student_id"],
            case_id=session_info["case_id"],
            start_time=session_info["start_time"],
            end_time=session_info["end_time"],
            total_questions=len(session_data.get("interactions", [])),
            diagnostic_accuracy_score=diagnostic_score,
            information_gathering_score=info_gathering_score,
            clinical_reasoning_score=reasoning_score,
            bias_detection_results=bias_results,
            final_diagnosis=session_data.get("final_diagnosis", "not_provided"),
            confidence_level=session_data.get("confidence_level", 0.0)
        )

    def _assess_diagnostic_accuracy(self, session_data: Dict[str, Any]) -> float:
        """
        Assess diagnostic accuracy using Ana Guedes' framework.
        
        Scoring criteria:
        - Correct final diagnosis: 1.0
        - Correct diagnosis in differential: 0.8
        - Reasonable differential without correct diagnosis: 0.6
        - Incorrect but logical diagnosis: 0.4
        - Completely incorrect diagnosis: 0.0
        """
        final_diagnosis = session_data.get("final_diagnosis", "").lower()
        differential_diagnoses = session_data.get("differential_diagnoses", [])
        
        # For the TB case
        correct_diagnoses = ["tuberculosis", "miliary tuberculosis", "tb", "pulmonary tuberculosis"]
        reasonable_differentials = ["infection", "pneumonia", "malignancy", "hypersensitivity pneumonitis"]
        
        if any(correct in final_diagnosis for correct in correct_diagnoses):
            return 1.0
        elif any(any(correct in diff.lower() for correct in correct_diagnoses) for diff in differential_diagnoses):
            return 0.8
        elif any(any(reasonable in diff.lower() for reasonable in reasonable_differentials) for diff in differential_diagnoses):
            return 0.6
        elif "heart failure" in final_diagnosis and self._discovered_contradictory_evidence(session_data):
            return 0.4  # Stuck with initial diagnosis despite contradictory evidence
        else:
            return 0.0

    def _assess_information_gathering(self, session_data: Dict[str, Any]) -> float:
        """
        Evaluate the quality and comprehensiveness of information gathering.
        Based on Ana's systematic approach to clinical data collection assessment.
        """
        interactions = session_data.get("interactions", [])
        asked_questions = [interaction.get("intent_id", "") for interaction in interactions]
        
        # Score each category
        category_scores = {}
        for category, expected_questions in self.question_categories.items():
            asked_in_category = sum(1 for q in asked_questions if any(exp in q for exp in expected_questions))
            total_in_category = len(expected_questions)
            category_scores[category] = min(asked_in_category / max(total_in_category, 1), 1.0)
        
        # Weighted average (history and exam are most important)
        weights = {
            "history_taking": 0.3,
            "physical_exam": 0.25,
            "investigations": 0.2,
            "medication_review": 0.15,
            "differential_diagnosis": 0.1
        }
        
        weighted_score = sum(category_scores.get(cat, 0) * weight for cat, weight in weights.items())
        return min(weighted_score, 1.0)

    def _evaluate_reasoning_process(self, session_data: Dict[str, Any]) -> float:
        """
        Evaluate the clinical reasoning process quality.
        Adapted from Ana's clinical reasoning assessment framework.
        """
        interactions = session_data.get("interactions", [])
        reasoning_indicators = {
            "systematic_approach": self._assess_systematic_approach(interactions),
            "hypothesis_testing": self._assess_hypothesis_testing(interactions),
            "evidence_integration": self._assess_evidence_integration(interactions),
            "adaptive_questioning": self._assess_adaptive_questioning(interactions)
        }
        
        # Equal weighting for all reasoning components
        return sum(reasoning_indicators.values()) / len(reasoning_indicators)

    def _detect_cognitive_biases(self, session_data: Dict[str, Any]) -> Dict[CognitiveBias, float]:
        """
        Detect cognitive biases using Ana's systematic bias detection approach.
        Returns bias confidence scores (0.0 = no bias detected, 1.0 = strong bias present).
        """
        interactions = session_data.get("interactions", [])
        
        bias_scores = {
            CognitiveBias.ANCHORING: self._detect_anchoring_bias(interactions),
            CognitiveBias.CONFIRMATION: self._detect_confirmation_bias(interactions),
            CognitiveBias.AVAILABILITY: self._detect_availability_bias(interactions),
            CognitiveBias.DIAGNOSTIC_MOMENTUM: self._detect_diagnostic_momentum(interactions),
            CognitiveBias.PREMATURE_CLOSURE: self._detect_premature_closure(interactions)
        }
        
        return bias_scores

    def _detect_anchoring_bias(self, interactions: List[Dict]) -> float:
        """
        Detect anchoring bias - tendency to stick with initial diagnosis.
        
        Indicators:
        - Early focus on heart failure related questions
        - Resistance to exploring alternatives despite contradictory evidence
        - Continued heart failure questioning after normal echo
        """
        early_questions = interactions[:5] if len(interactions) >= 5 else interactions
        hf_related_early = sum(1 for q in early_questions if "heart" in q.get("intent_id", "").lower() or "cardiac" in q.get("intent_id", "").lower())
        
        # Check for continued HF focus after contradictory evidence
        echo_discovered = any("echo" in q.get("intent_id", "") for q in interactions)
        if echo_discovered:
            echo_index = next(i for i, q in enumerate(interactions) if "echo" in q.get("intent_id", ""))
            post_echo_hf_questions = sum(1 for q in interactions[echo_index:] if "heart" in q.get("intent_id", "").lower())
            if post_echo_hf_questions > 2:
                return min(0.8 + (post_echo_hf_questions - 2) * 0.1, 1.0)
        
        # Early anchoring score
        if len(early_questions) > 0:
            early_anchor_score = hf_related_early / len(early_questions)
            return min(early_anchor_score * 1.5, 1.0)  # Amplify early anchoring
        
        return 0.0

    def _detect_confirmation_bias(self, interactions: List[Dict]) -> float:
        """
        Detect confirmation bias - seeking information that confirms initial hypothesis.
        
        Indicators:
        - Focusing on pro-BNP, chest X-ray after initial HF diagnosis
        - Avoiding questions about weight loss, immunosuppression
        - Not following up on normal echo results
        """
        confirmatory_questions = ["labs_pro_bnp", "imaging_cxr", "exam_cardiovascular"]
        contradictory_questions = ["discoverable_infliximab", "discoverable_echo", "hpi_weight_loss"]
        
        confirmatory_count = sum(1 for q in interactions if q.get("intent_id") in confirmatory_questions)
        contradictory_count = sum(1 for q in interactions if q.get("intent_id") in contradictory_questions)
        
        if confirmatory_count + contradictory_count == 0:
            return 0.0
        
        # High ratio of confirmatory to contradictory questions indicates bias
        confirmation_ratio = confirmatory_count / max(confirmatory_count + contradictory_count, 1)
        return min(confirmation_ratio * 1.2, 1.0)

    def _detect_premature_closure(self, interactions: List[Dict]) -> float:
        """
        Detect premature closure - stopping investigation too early.
        
        Indicators:
        - Few total questions asked
        - Not exploring all available information
        - Missing key discoverable elements
        """
        total_questions = len(interactions)
        available_intents = 39  # Based on your mapping file
        coverage = total_questions / available_intents
        
        # Check if key discoverable items were explored
        key_discoveries = ["discoverable_infliximab", "discoverable_echo", "discoverable_ct_chest"]
        discoveries_explored = sum(1 for disc in key_discoveries if any(disc in q.get("intent_id", "") for q in interactions))
        discovery_coverage = discoveries_explored / len(key_discoveries)
        
        # Premature closure score (inverse of thoroughness)
        thoroughness = (coverage + discovery_coverage) / 2
        return max(1.0 - thoroughness * 1.5, 0.0)

    # Helper methods
    def _extract_session_info(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract basic session information."""
        return {
            "session_id": session_data.get("session_id", "unknown"),
            "student_id": session_data.get("student_id", "unknown"),
            "case_id": session_data.get("case_id", "case01"),
            "start_time": datetime.datetime.fromisoformat(session_data.get("start_time", datetime.datetime.now().isoformat())),
            "end_time": datetime.datetime.fromisoformat(session_data.get("end_time", datetime.datetime.now().isoformat()))
        }

    def _discovered_contradictory_evidence(self, session_data: Dict[str, Any]) -> bool:
        """Check if student discovered evidence contradicting heart failure diagnosis."""
        interactions = session_data.get("interactions", [])
        contradictory_discoveries = ["discoverable_echo", "hpi_weight_loss", "discoverable_infliximab"]
        return any(any(disc in q.get("intent_id", "") for disc in contradictory_discoveries) for q in interactions)

    def _assess_systematic_approach(self, interactions: List[Dict]) -> float:
        """Assess if student followed systematic clinical reasoning approach."""
        # Check for logical progression: history -> exam -> investigations -> diagnosis
        question_sequence = [q.get("intent_id", "") for q in interactions]
        
        # Simple scoring based on question type progression
        history_index = next((i for i, q in enumerate(question_sequence) if q.startswith("hpi_")), len(question_sequence))
        exam_index = next((i for i, q in enumerate(question_sequence) if q.startswith("exam_")), len(question_sequence))
        lab_index = next((i for i, q in enumerate(question_sequence) if q.startswith("labs_")), len(question_sequence))
        
        # Reward logical progression
        progression_score = 0.0
        if history_index < exam_index:
            progression_score += 0.33
        if exam_index < lab_index:
            progression_score += 0.33
        if history_index < lab_index:
            progression_score += 0.34
        
        return progression_score

    def _assess_hypothesis_testing(self, interactions: List[Dict]) -> float:
        """Assess quality of hypothesis generation and testing."""
        # Look for evidence of multiple hypotheses being considered
        differential_questions = [q for q in interactions if "discoverable_" in q.get("intent_id", "")]
        return min(len(differential_questions) / 3.0, 1.0)  # Normalize to 3 major differentials

    def _assess_evidence_integration(self, interactions: List[Dict]) -> float:
        """Assess how well student integrates contradictory evidence."""
        # If student found contradictory evidence, did they follow up appropriately?
        echo_found = any("echo" in q.get("intent_id", "") for q in interactions)
        infliximab_found = any("infliximab" in q.get("intent_id", "") for q in interactions)
        
        if echo_found or infliximab_found:
            # Look for follow-up questions about alternative diagnoses
            ct_requested = any("ct" in q.get("intent_id", "") for q in interactions)
            tb_considered = any("discoverable_" in q.get("intent_id", "") for q in interactions)
            return 0.5 + (0.25 * ct_requested) + (0.25 * tb_considered)
        
        return 0.5  # Neutral if no contradictory evidence discovered

    def _assess_adaptive_questioning(self, interactions: List[Dict]) -> float:
        """Assess if questioning adapted based on findings."""
        # This would require more sophisticated analysis of question sequences
        # For now, give credit for following up on abnormal findings
        abnormal_findings = ["labs_wbc", "labs_hemoglobin", "exam_respiratory"]
        follow_ups = ["discoverable_infliximab", "discoverable_ct_chest"]
        
        abnormal_found = any(finding in q.get("intent_id", "") for q in interactions for finding in abnormal_findings)
        follow_up_done = any(follow in q.get("intent_id", "") for q in interactions for follow in follow_ups)
        
        if abnormal_found and follow_up_done:
            return 1.0
        elif abnormal_found:
            return 0.5
        else:
            return 0.3

    def generate_feedback_report(self, metrics: InterviewMetrics) -> Dict[str, Any]:
        """
        Generate detailed feedback report based on evaluation metrics.
        Following Ana's feedback framework approach.
        """
        # Determine overall performance level
        overall_score = (metrics.diagnostic_accuracy_score + 
                        metrics.information_gathering_score + 
                        metrics.clinical_reasoning_score) / 3
        
        performance_level = "Expert" if overall_score >= 0.9 else \
                           "Proficient" if overall_score >= 0.7 else \
                           "Developing" if overall_score >= 0.5 else "Novice"
        
        # Identify dominant biases
        significant_biases = [bias.value for bias, score in metrics.bias_detection_results.items() 
                            if score >= self.bias_thresholds.get(bias, 0.7)]
        
        return {
            "session_summary": {
                "session_id": metrics.session_id,
                "performance_level": performance_level,
                "overall_score": round(overall_score, 2),
                "duration_minutes": (metrics.end_time - metrics.start_time).total_seconds() / 60
            },
            "detailed_scores": {
                "diagnostic_accuracy": round(metrics.diagnostic_accuracy_score, 2),
                "information_gathering": round(metrics.information_gathering_score, 2),
                "clinical_reasoning": round(metrics.clinical_reasoning_score, 2)
            },
            "cognitive_biases": {
                "detected_biases": significant_biases,
                "bias_scores": {bias.value: round(score, 2) for bias, score in metrics.bias_detection_results.items()}
            },
            "recommendations": self._generate_recommendations(metrics),
            "strengths": self._identify_strengths(metrics),
            "areas_for_improvement": self._identify_improvement_areas(metrics)
        }

    def _generate_recommendations(self, metrics: InterviewMetrics) -> List[str]:
        """Generate personalized recommendations based on performance."""
        recommendations = []
        
        if metrics.diagnostic_accuracy_score < 0.6:
            recommendations.append("Focus on developing systematic differential diagnosis skills")
        
        if metrics.information_gathering_score < 0.7:
            recommendations.append("Practice comprehensive history-taking and physical examination techniques")
        
        if metrics.bias_detection_results.get(CognitiveBias.ANCHORING, 0) > 0.7:
            recommendations.append("Work on maintaining diagnostic flexibility and considering alternatives to initial impressions")
        
        if metrics.bias_detection_results.get(CognitiveBias.CONFIRMATION, 0) > 0.6:
            recommendations.append("Practice actively seeking disconfirming evidence for initial hypotheses")
        
        return recommendations

    def _identify_strengths(self, metrics: InterviewMetrics) -> List[str]:
        """Identify student strengths based on performance."""
        strengths = []
        
        if metrics.diagnostic_accuracy_score >= 0.8:
            strengths.append("Strong diagnostic reasoning skills")
        
        if metrics.information_gathering_score >= 0.8:
            strengths.append("Comprehensive information gathering approach")
        
        if max(metrics.bias_detection_results.values()) < 0.5:
            strengths.append("Good resistance to cognitive biases")
        
        return strengths

    def _identify_improvement_areas(self, metrics: InterviewMetrics) -> List[str]:
        """Identify specific areas needing improvement."""
        areas = []
        
        if metrics.clinical_reasoning_score < 0.6:
            areas.append("Clinical reasoning and evidence integration")
        
        if metrics.bias_detection_results.get(CognitiveBias.PREMATURE_CLOSURE, 0) > 0.7:
            areas.append("Thoroughness in clinical investigation")
        
        return areas

# Example usage and testing
if __name__ == "__main__":
    # Example session data structure
    example_session = {
        "session_id": "session_001",
        "student_id": "student_123",
        "case_id": "case01",
        "start_time": "2025-07-12T10:00:00",
        "end_time": "2025-07-12T10:45:00",
        "interactions": [
            {"intent_id": "profile_age", "timestamp": "2025-07-12T10:02:00"},
            {"intent_id": "hpi_chief_complaint", "timestamp": "2025-07-12T10:05:00"},
            {"intent_id": "exam_cardiovascular", "timestamp": "2025-07-12T10:10:00"},
            {"intent_id": "labs_pro_bnp", "timestamp": "2025-07-12T10:15:00"},
            {"intent_id": "discoverable_echo_query", "timestamp": "2025-07-12T10:25:00"},
            {"intent_id": "discoverable_infliximab_query", "timestamp": "2025-07-12T10:35:00"}
        ],
        "final_diagnosis": "heart failure",
        "confidence_level": 0.8
    }
    
    evaluator = ClinicalInterviewEvaluator()
    metrics = evaluator.evaluate_session(example_session)
    report = evaluator.generate_feedback_report(metrics)
    
    print(json.dumps(report, indent=2))
