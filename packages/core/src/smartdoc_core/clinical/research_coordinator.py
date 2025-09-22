"""
Research-grade evaluation coordinator that integrates rule-based and LLM analysis
with agreement tracking, discrepancy logging, and reliability validation.
"""

from typing import Dict, List, Any, Optional, Tuple
import json
from datetime import datetime

from smartdoc_core.utils.logger import sys_logger
from smartdoc_core.clinical.evaluator import ClinicalEvaluator, EvaluationInputs
from smartdoc_core.simulation.bias_analyzer import BiasEvaluator
from smartdoc_core.clinical.evaluation_schemas import ResearchEvaluationOutput, ReliabilityMetrics


class ResearchEvaluationCoordinator:
    """
    Coordinates comprehensive research-grade evaluation by:
    1. Running rule-based bias detection
    2. Running LLM evaluation and bias analysis
    3. Computing agreement metrics between approaches
    4. Flagging discrepancies for research analysis
    5. Providing reliability and validation metrics
    """

    def __init__(
        self,
        clinical_evaluator: Optional[ClinicalEvaluator] = None,
        enable_agreement_tracking: bool = True,
        enable_discrepancy_logging: bool = True,
        agreement_threshold: float = 0.7,
    ):
        self.clinical_evaluator = clinical_evaluator or ClinicalEvaluator(
            enable_validation=True,
            enable_reliability_tracking=True,
            temperature=0.1  # Lower temperature for research consistency
        )
        self.enable_agreement_tracking = enable_agreement_tracking
        self.enable_discrepancy_logging = enable_discrepancy_logging
        self.agreement_threshold = agreement_threshold

        # Tracking for research analysis
        self.evaluation_history = []
        self.discrepancy_log = []

        sys_logger.log_system("info", f"ResearchEvaluationCoordinator initialized with agreement_threshold={agreement_threshold}")

    def comprehensive_evaluation(
        self,
        inputs: EvaluationInputs,
        case_data: Dict[str, Any],
        session_log: List[Dict[str, Any]],
        revealed_blocks: set,
        hypotheses: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Perform comprehensive research-grade evaluation with agreement analysis.

        Args:
            inputs: Standard evaluation inputs for LLM
            case_data: Case metadata for rule-based analysis
            session_log: Complete session interaction log
            revealed_blocks: Set of information blocks revealed
            hypotheses: List of student hypotheses

        Returns:
            Comprehensive evaluation results with agreement metrics
        """
        evaluation_start = datetime.now()
        session_id = f"eval_{evaluation_start.strftime('%Y%m%d_%H%M%S')}"

        try:
            # 1. Run rule-based bias analysis
            rule_based_results = self._run_rule_based_analysis(
                case_data, session_log, revealed_blocks, hypotheses, inputs.final_diagnosis
            )

            # 2. Run LLM evaluation (includes LLM bias analysis)
            llm_results = self.clinical_evaluator.evaluate(inputs)
            llm_bias_results = self.clinical_evaluator.deep_bias_analysis(
                inputs.dialogue_transcript, inputs.final_diagnosis
            )

            # 3. Compute agreement metrics if both succeeded
            agreement_metrics = {}
            discrepancies = []

            if self.enable_agreement_tracking and rule_based_results["success"] and llm_results["success"]:
                agreement_metrics, discrepancies = self._compute_agreement_metrics(
                    rule_based_results["bias_analysis"],
                    llm_bias_results.get("bias_analysis", {}),
                    session_id
                )

            # 4. Build comprehensive response
            comprehensive_results = {
                "success": True,
                "session_id": session_id,
                "llm_evaluation": llm_results,
                "llm_bias_analysis": llm_bias_results,
                "rule_based_bias_analysis": rule_based_results,
                "agreement_metrics": agreement_metrics,
                "discrepancies": discrepancies,
                "evaluation_timestamp": evaluation_start.isoformat(),
                "processing_time_seconds": (datetime.now() - evaluation_start).total_seconds()
            }

            # 5. Log discrepancies for research analysis
            if self.enable_discrepancy_logging and discrepancies:
                self._log_discrepancies(session_id, discrepancies, inputs, case_data)

            # 6. Add to evaluation history for research tracking
            history_entry = {
                "session_id": session_id,
                "timestamp": evaluation_start.isoformat(),
                "agreement_score": agreement_metrics.get("overall_agreement", 0),
                "discrepancy_count": len(discrepancies),
                "rule_based_success": rule_based_results.get("success", False),
                "llm_success": llm_results.get("success", False)
            }
            self.evaluation_history.append(history_entry)
            sys_logger.log_system("info", f"Added evaluation to history. Total evaluations: {len(self.evaluation_history)}")

            return comprehensive_results

        except Exception as e:
            sys_logger.log_system("error", f"Comprehensive evaluation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id,
                "evaluation_timestamp": evaluation_start.isoformat()
            }

    def _run_rule_based_analysis(
        self,
        case_data: Dict[str, Any],
        session_log: List[Dict[str, Any]],
        revealed_blocks: set,
        hypotheses: List[Dict[str, Any]],
        final_diagnosis: str
    ) -> Dict[str, Any]:
        """Run enhanced rule-based bias analysis."""
        try:
            bias_evaluator = BiasEvaluator(case_data)
            bias_results = bias_evaluator.evaluate_session(
                session_log, revealed_blocks, hypotheses, final_diagnosis
            )

            return {
                "success": True,
                "bias_analysis": bias_results,
                "method": "enhanced_rule_based"
            }

        except Exception as e:
            sys_logger.log_system("warning", f"Rule-based analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "method": "enhanced_rule_based"
            }

    def _compute_agreement_metrics(
        self,
        rule_based_analysis: Dict[str, Any],
        llm_bias_analysis: Dict[str, Any],
        session_id: str
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Compute agreement metrics between rule-based and LLM bias analysis."""

        bias_types = ["anchoring_bias", "confirmation_bias", "premature_closure"]
        agreements = []
        disagreements = []

        for bias_type in bias_types:
            rule_detected = rule_based_analysis.get(bias_type, {}).get("detected", False)
            rule_confidence = rule_based_analysis.get(bias_type, {}).get("confidence", 0)

            llm_detected = llm_bias_analysis.get(bias_type, {}).get("detected", False)
            llm_confidence = llm_bias_analysis.get(bias_type, {}).get("confidence", 0)

            # Calculate agreement
            if rule_detected == llm_detected:
                # Both agree on detection/non-detection
                confidence_diff = abs(rule_confidence - llm_confidence) if rule_detected else 0
                agreement_score = 1.0 - (confidence_diff / 100.0)  # Normalize confidence difference
                agreements.append({
                    "bias_type": bias_type,
                    "agreement": "detected" if rule_detected else "not_detected",
                    "agreement_score": agreement_score,
                    "rule_confidence": rule_confidence,
                    "llm_confidence": llm_confidence
                })
            else:
                # Disagreement on detection
                disagreements.append({
                    "bias_type": bias_type,
                    "rule_detected": rule_detected,
                    "llm_detected": llm_detected,
                    "rule_confidence": rule_confidence,
                    "llm_confidence": llm_confidence,
                    "rule_reason": rule_based_analysis.get(bias_type, {}).get("reason", ""),
                    "llm_explanation": llm_bias_analysis.get(bias_type, {}).get("explanation", "")
                })

        # Calculate overall agreement metrics
        total_comparisons = len(bias_types)
        agreement_count = len(agreements)
        overall_agreement = agreement_count / total_comparisons if total_comparisons > 0 else 0

        # Calculate weighted agreement (considering confidence)
        if agreements:
            weighted_agreement = sum(a["agreement_score"] for a in agreements) / len(agreements)
        else:
            weighted_agreement = 0

        agreement_metrics = {
            "overall_agreement": overall_agreement,
            "weighted_agreement": weighted_agreement,
            "agreement_count": agreement_count,
            "disagreement_count": len(disagreements),
            "total_comparisons": total_comparisons,
            "agreements": agreements,
            "session_id": session_id
        }

        return agreement_metrics, disagreements

    def _log_discrepancies(
        self,
        session_id: str,
        discrepancies: List[Dict[str, Any]],
        inputs: EvaluationInputs,
        case_data: Dict[str, Any]
    ):
        """Log discrepancies for research analysis and paper discussion."""

        discrepancy_entry = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "discrepancies": discrepancies,
            "context": {
                "final_diagnosis": inputs.final_diagnosis,
                "case_type": case_data.get("case_type", "unknown"),
                "total_blocks": len(case_data.get("informationBlocks", [])),
                "critical_findings": len(case_data.get("groundTruth", {}).get("criticalFindingIds", [])),
                "dialogue_length": len(inputs.dialogue_transcript),
                "reflection_completeness": len([v for v in inputs.metacognitive_responses.values() if v.strip()])
            }
        }

        self.discrepancy_log.append(discrepancy_entry)

        # Log for immediate research attention
        sys_logger.log_system(
            "info",
            f"RESEARCH: Bias detection discrepancies logged for session {session_id}. "
            f"Count: {len(discrepancies)}. Consider for Discussion/Limitations section."
        )

    def generate_reliability_report(self) -> Dict[str, Any]:
        """Generate comprehensive reliability report for research validation."""

        if not self.evaluation_history:
            return {"error": "No evaluations performed yet"}

        total_evaluations = len(self.evaluation_history)
        successful_evaluations = sum(1 for e in self.evaluation_history if e.get("rule_based_success") and e.get("llm_success", {}).get("success"))

        agreement_scores = [e["agreement_score"] for e in self.evaluation_history if "agreement_score" in e]
        avg_agreement = sum(agreement_scores) / len(agreement_scores) if agreement_scores else 0

        discrepancy_counts = [e["discrepancy_count"] for e in self.evaluation_history]
        avg_discrepancies = sum(discrepancy_counts) / len(discrepancy_counts) if discrepancy_counts else 0

        return {
            "total_evaluations": total_evaluations,
            "successful_evaluations": successful_evaluations,
            "success_rate": successful_evaluations / total_evaluations if total_evaluations > 0 else 0,
            "average_agreement_score": avg_agreement,
            "average_discrepancies_per_evaluation": avg_discrepancies,
            "total_discrepancies_logged": len(self.discrepancy_log),
            "agreement_threshold": self.agreement_threshold,
            "evaluations_above_threshold": sum(1 for score in agreement_scores if score >= self.agreement_threshold),
            "reliability_metrics": {
                "inter_method_agreement": avg_agreement,
                "consistency_rate": successful_evaluations / total_evaluations if total_evaluations > 0 else 0,
                "discrepancy_rate": avg_discrepancies / 3.0 if avg_discrepancies else 0  # Normalize by 3 bias types
            }
        }

    def multi_seed_evaluation(
        self,
        inputs: EvaluationInputs,
        num_runs: int = 3,
        seed_values: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Run multiple evaluations with different seeds to assess variance.
        Useful for reliability analysis and understanding LLM consistency.
        """
        if seed_values is None:
            seed_values = [42, 123, 789][:num_runs]

        results = []
        for i, seed in enumerate(seed_values):
            sys_logger.log_system("info", f"Running evaluation {i+1}/{num_runs} with seed {seed}")

            # Create evaluator with specific seed (if supported by provider)
            evaluator = ClinicalEvaluator(
                enable_validation=True,
                enable_reliability_tracking=True,
                temperature=0.1  # Keep temperature low for consistency
            )

            # Run evaluation
            result = evaluator.evaluate(inputs)
            if result.get("success"):
                evaluation = result.get("evaluation", {})
                results.append({
                    "seed": seed,
                    "overall_score": evaluation.get("overall_score", 0),
                    "diagnostic_accuracy": evaluation.get("diagnostic_accuracy", {}).get("score", 0),
                    "information_gathering": evaluation.get("information_gathering", {}).get("score", 0),
                    "cognitive_bias_awareness": evaluation.get("cognitive_bias_awareness", {}).get("score", 0),
                    "clinical_reasoning": evaluation.get("clinical_reasoning", {}).get("score", 0),
                    "confidence_assessment": evaluation.get("confidence_assessment", 0)
                })

        # Calculate variance metrics
        if len(results) >= 2:
            variance_metrics = self._calculate_variance_metrics(results)
        else:
            variance_metrics = {"error": "Insufficient successful runs for variance calculation"}

        return {
            "success": len(results) > 0,
            "total_runs": num_runs,
            "successful_runs": len(results),
            "individual_results": results,
            "variance_metrics": variance_metrics,
            "methodology_note": "Multi-seed evaluation for assessing LLM evaluation consistency"
        }

    def _calculate_variance_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate variance metrics across multiple evaluation runs."""
        import statistics

        metrics = ["overall_score", "diagnostic_accuracy", "information_gathering",
                  "cognitive_bias_awareness", "clinical_reasoning", "confidence_assessment"]

        variance_analysis = {}

        for metric in metrics:
            values = [r[metric] for r in results if metric in r]
            if len(values) >= 2:
                variance_analysis[metric] = {
                    "mean": statistics.mean(values),
                    "stdev": statistics.stdev(values),
                    "min": min(values),
                    "max": max(values),
                    "range": max(values) - min(values),
                    "coefficient_of_variation": statistics.stdev(values) / statistics.mean(values) if statistics.mean(values) > 0 else 0
                }

        # Overall consistency assessment
        overall_cv = variance_analysis.get("overall_score", {}).get("coefficient_of_variation", 0)
        consistency_rating = "high" if overall_cv < 0.1 else "moderate" if overall_cv < 0.2 else "low"

        return {
            "dimension_variance": variance_analysis,
            "overall_consistency": consistency_rating,
            "coefficient_of_variation_threshold": {
                "high_consistency": "< 0.1",
                "moderate_consistency": "0.1 - 0.2",
                "low_consistency": "> 0.2"
            },
            "research_interpretation": "Lower coefficient of variation indicates more consistent LLM evaluation across runs"
        }

    def export_research_data(self) -> Dict[str, Any]:
        """Export comprehensive data for research analysis and paper writing."""

        return {
            "evaluation_history": self.evaluation_history,
            "discrepancy_log": self.discrepancy_log,
            "reliability_report": self.generate_reliability_report(),
            "configuration": {
                "agreement_tracking_enabled": self.enable_agreement_tracking,
                "discrepancy_logging_enabled": self.enable_discrepancy_logging,
                "agreement_threshold": self.agreement_threshold,
                "evaluator_temperature": getattr(self.clinical_evaluator, "temperature", None),
                "validation_enabled": getattr(self.clinical_evaluator, "enable_validation", None)
            },
            "research_methodologies_available": [
                "inter_method_agreement_analysis",
                "discrepancy_logging",
                "multi_seed_variance_testing",
                "expert_validation_framework"
            ],
            "export_timestamp": datetime.now().isoformat(),
            "total_sessions_analyzed": len(self.evaluation_history)
        }
