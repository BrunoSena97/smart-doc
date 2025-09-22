from __future__ import annotations
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from smartdoc_core.clinical.evaluator import ClinicalEvaluator, EvaluationInputs
from smartdoc_core.clinical.research_coordinator import ResearchEvaluationCoordinator
from smartdoc_core.utils.logger import sys_logger

bp = Blueprint("evaluation", __name__, url_prefix="/api/v1/evaluation")

# Initialize research-grade evaluation coordinator
research_coordinator = ResearchEvaluationCoordinator(
    enable_agreement_tracking=True,
    enable_discrepancy_logging=True,
    agreement_threshold=0.7
)

@bp.post("/submit")
def submit_diagnosis_with_reflection():
    """
    Submit diagnosis with metacognitive reflection for comprehensive evaluation.

    Payload:
    {
      "diagnosis": "text",
      "metacognitive_responses": { "Q1": "A1", ... },
      "case_context": {...},            # optional (correct_diagnosis, key_features...)
      "session_id": "session_id"        # optional, gets current active session if not provided
    }
    """
    data = request.get_json(silent=True) or {}
    diagnosis = (data.get("diagnosis") or "").strip()
    reflection = data.get("metacognitive_responses") or {}
    case_context = data.get("case_context") or {}
    session_id = data.get("session_id")

    if not diagnosis or not reflection:
        return jsonify({
            "success": False,
            "error": "diagnosis and metacognitive_responses are required"
        }), 400

    try:
        # Get comprehensive session data for research-grade evaluation
        from smartdoc_api.routes.legacy import intent_driven_manager

        if intent_driven_manager and session_id:
            # Get comprehensive session data
            session_summary = intent_driven_manager.get_session_summary(session_id)
            transcript = session_summary.get("interactions", [])
            bias_data = session_summary.get("bias_summary", {})
            bias_warnings = bias_data.get("warnings", [])

            # Get session state for rule-based analysis
            session_state = intent_driven_manager.store.get_session(session_id)
            if session_state:
                revealed_blocks = session_state.revealed_blocks
                hypotheses = [{"diagnosis": h.get("hypothesis", ""), "timestamp": h.get("timestamp", "")}
                             for h in session_state.working_hypotheses]
                # Convert StudentInteraction objects to dictionaries
                session_log = [
                    {
                        "action_type": "interaction",
                        "timestamp": interaction.timestamp.isoformat() if hasattr(interaction.timestamp, 'isoformat') else str(interaction.timestamp),
                        "action": interaction.action,
                        "intent_id": getattr(interaction, 'intent_id', ''),
                        "user_query": getattr(interaction, 'user_query', ''),
                        "block_id": interaction.block_id,
                        "category": interaction.category,
                        "hypothesis": interaction.hypothesis,
                        "reasoning": interaction.reasoning
                    }
                    for interaction in session_state.interactions
                ]
                case_data = intent_driven_manager.store.case_data or {}
            else:
                revealed_blocks = set()
                hypotheses = []
                session_log = []
                case_data = {}
        else:
            # Fallback if no session or manager available
            transcript = []
            bias_warnings = []
            revealed_blocks = set()
            hypotheses = []
            session_log = []
            case_data = {}
            sys_logger.log_system("warning", "No session data available for evaluation - using fallback data")

        # Prepare inputs for comprehensive evaluation
        inputs = EvaluationInputs(
            dialogue_transcript=transcript,
            detected_biases=bias_warnings,
            metacognitive_responses=reflection,
            final_diagnosis=diagnosis,
            case_context=case_context,
        )

        # Run comprehensive research-grade evaluation
        sys_logger.log_system("info", f"Submit endpoint: coordinator history length before = {len(research_coordinator.evaluation_history)}")
        comprehensive_results = research_coordinator.comprehensive_evaluation(
            inputs=inputs,
            case_data=case_data,
            session_log=session_log,
            revealed_blocks=revealed_blocks,
            hypotheses=hypotheses
        )

        # Extract results for database storage
        llm_eval = comprehensive_results.get("llm_evaluation", {})
        evaluation = llm_eval.get("evaluation", {})

        overall_score = evaluation.get("overall_score", 0)
        score_breakdown = {
            "diagnostic_accuracy": evaluation.get("diagnostic_accuracy", {}).get("score", 0),
            "information_gathering": evaluation.get("information_gathering", {}).get("score", 0),
            "cognitive_bias_awareness": evaluation.get("cognitive_bias_awareness", {}).get("score", 0),
            "clinical_reasoning": evaluation.get("clinical_reasoning", {}).get("score", 0),
            "llm_evaluation_raw": evaluation,
            "rule_based_bias_analysis": comprehensive_results.get("rule_based_bias_analysis", {}),
            "agreement_metrics": comprehensive_results.get("agreement_metrics", {}),
            "discrepancies": comprehensive_results.get("discrepancies", [])
        }

        # Build comprehensive feedback including agreement analysis
        feedback_parts = []
        if evaluation.get("constructive_feedback"):
            feedback_parts.append(f"Clinical Evaluation: {evaluation['constructive_feedback']}")

        llm_bias = comprehensive_results.get("llm_bias_analysis", {})
        if llm_bias.get("success") and llm_bias.get("bias_analysis"):
            feedback_parts.append(f"LLM Bias Analysis: {llm_bias['bias_analysis']}")

        rule_bias = comprehensive_results.get("rule_based_bias_analysis", {})
        if rule_bias.get("success"):
            feedback_parts.append(f"Rule-based Bias Analysis: {rule_bias['bias_analysis']}")

        agreement_metrics = comprehensive_results.get("agreement_metrics", {})
        if agreement_metrics:
            agreement_score = agreement_metrics.get("overall_agreement", 0)
            feedback_parts.append(f"Method Agreement: {agreement_score:.2%}")

        comprehensive_feedback = " | ".join(feedback_parts) if feedback_parts else "Comprehensive evaluation completed"

        # Store evaluation results in database for research data persistence
        from smartdoc_api.services.repo import submit_diagnosis

        submit_diagnosis(
            session_id=session_id or "unknown_session",
            diagnosis_text=diagnosis,
            score_overall=int(overall_score) if overall_score else None,
            score_breakdown=score_breakdown,
            feedback=comprehensive_feedback,
            reflections=reflection
        )

        # Build comprehensive response for research
        resp = {
            "success": comprehensive_results["success"],
            "session_id": comprehensive_results.get("session_id", session_id),
            "llm_evaluation": comprehensive_results.get("llm_evaluation", {}),
            "llm_bias_analysis": comprehensive_results.get("llm_bias_analysis", {}),
            "rule_based_bias_analysis": comprehensive_results.get("rule_based_bias_analysis", {}),
            "agreement_metrics": comprehensive_results.get("agreement_metrics", {}),
            "discrepancies": comprehensive_results.get("discrepancies", []),
            "processing_time_seconds": comprehensive_results.get("processing_time_seconds", 0),
            "database_stored": True,
            "research_grade": True,
            "evaluation_timestamp": comprehensive_results.get("evaluation_timestamp")
        }

        sys_logger.log_system("info", f"Research-grade evaluation completed for session: {session_id}")
        return jsonify(resp), 200

    except Exception as e:
        sys_logger.log_system("error", f"Evaluation failed: {e}")
        return jsonify({
            "success": False,
            "error": f"Evaluation failed: {str(e)}"
        }), 500


@bp.get("/reliability")
def get_reliability_metrics():
    """
    Get comprehensive reliability metrics for research validation.

    Returns inter-method agreement, consistency rates, discrepancy analysis,
    and other metrics useful for research paper methodology and limitations sections.
    """
    try:
        from smartdoc_api.services.repo import get_session
        import json

        # Get evaluation data from database instead of in-memory coordinator
        # Use raw SQL to get evaluation records
        from sqlalchemy import text
        session = get_session()
        try:
            evaluations = session.execute(
                text("SELECT session_id, diagnosis_text, score_overall, score_breakdown, created_at "
                     "FROM diagnosis_submissions ORDER BY created_at DESC")
            ).fetchall()
        finally:
            session.close()

        if not evaluations:
            return jsonify({
                "success": True,
                "reliability_report": {"error": "No evaluations performed yet"},
                "research_data_summary": {
                    "total_evaluations": 0,
                    "total_discrepancies": 0,
                    "configuration": {
                        "agreement_threshold": 0.7,
                        "agreement_tracking_enabled": True,
                        "discrepancy_logging_enabled": True,
                        "evaluator_temperature": 0.1,
                        "validation_enabled": True
                    }
                },
                "recommendations": {
                    "inter_method_agreement": 0,
                    "suitable_for_research": False,
                    "discrepancy_analysis_available": False
                }
            }), 200

        # Analyze stored evaluation data
        total_evaluations = len(evaluations)
        successful_evaluations = 0
        agreement_scores = []
        total_discrepancies = 0

        for eval_record in evaluations:
            try:
                # eval_record is a tuple: (session_id, diagnosis_text, score_overall, score_breakdown, created_at)
                session_id, diagnosis_text, score_overall, score_breakdown_str, created_at = eval_record

                score_breakdown = json.loads(score_breakdown_str) if score_breakdown_str else {}

                # Check if evaluation was successful (has LLM evaluation data)
                if 'llm_evaluation_raw' in score_breakdown:
                    successful_evaluations += 1

                # Extract agreement metrics
                agreement_metrics = score_breakdown.get('agreement_metrics', {})
                if agreement_metrics and 'overall_agreement' in agreement_metrics:
                    agreement_scores.append(agreement_metrics['overall_agreement'])

                # Count discrepancies
                discrepancies = score_breakdown.get('discrepancies', [])
                total_discrepancies += len(discrepancies)

            except (json.JSONDecodeError, KeyError, ValueError) as e:
                sys_logger.log_system("warning", f"Failed to parse evaluation data for record: {e}")
                continue

        # Calculate reliability metrics
        avg_agreement = sum(agreement_scores) / len(agreement_scores) if agreement_scores else 0
        success_rate = successful_evaluations / total_evaluations if total_evaluations > 0 else 0
        avg_discrepancies = total_discrepancies / total_evaluations if total_evaluations > 0 else 0

        reliability_report = {
            "total_evaluations": total_evaluations,
            "successful_evaluations": successful_evaluations,
            "success_rate": success_rate,
            "average_agreement_score": avg_agreement,
            "average_discrepancies_per_evaluation": avg_discrepancies,
            "total_discrepancies_logged": total_discrepancies,
            "agreement_threshold": 0.7,
            "evaluations_above_threshold": sum(1 for score in agreement_scores if score >= 0.7),
            "reliability_metrics": {
                "inter_method_agreement": avg_agreement,
                "consistency_rate": success_rate,
                "discrepancy_rate": avg_discrepancies / 3.0 if avg_discrepancies else 0  # Normalize by 3 bias types
            }
        }

        return jsonify({
            "success": True,
            "reliability_report": reliability_report,
            "research_data_summary": {
                "total_evaluations": total_evaluations,
                "total_discrepancies": total_discrepancies,
                "configuration": {
                    "agreement_threshold": 0.7,
                    "agreement_tracking_enabled": True,
                    "discrepancy_logging_enabled": True,
                    "evaluator_temperature": 0.1,
                    "validation_enabled": True
                }
            },
            "recommendations": {
                "inter_method_agreement": avg_agreement,
                "suitable_for_research": success_rate > 0.8 and avg_agreement > 0.7,
                "discrepancy_analysis_available": total_discrepancies > 0
            }
        }), 200

    except Exception as e:
        sys_logger.log_system("error", f"Reliability metrics failed: {e}")
        return jsonify({
            "success": False,
            "error": f"Failed to generate reliability metrics: {str(e)}"
        }), 500


@bp.post("/validate")
def validate_against_expert():
    """
    Validate LLM evaluation against expert human scoring for reliability assessment.

    Payload:
    {
      "session_id": "session_id",
      "expert_scores": {
        "overall_score": 0-100,
        "diagnostic_accuracy": 0-100,
        "information_gathering": 0-100,
        "cognitive_bias_awareness": 0-100,
        "clinical_reasoning": 0-100
      },
      "expert_bias_detection": {
        "anchoring_bias": {"detected": true/false, "confidence": 0-100},
        "confirmation_bias": {"detected": true/false, "confidence": 0-100},
        "premature_closure": {"detected": true/false, "confidence": 0-100}
      },
      "expert_id": "expert_identifier"
    }
    """
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    expert_scores = data.get("expert_scores", {})
    expert_bias_detection = data.get("expert_bias_detection", {})
    expert_id = data.get("expert_id", "unknown_expert")

    if not session_id or not expert_scores:
        return jsonify({
            "success": False,
            "error": "session_id and expert_scores are required"
        }), 400

    try:
        # Find corresponding LLM evaluation in history
        llm_evaluation = None
        for eval_entry in research_coordinator.evaluation_history:
            if eval_entry["session_id"] == session_id:
                # This would need to be enhanced to store full evaluation results
                llm_evaluation = eval_entry
                break

        if not llm_evaluation:
            return jsonify({
                "success": False,
                "error": f"No LLM evaluation found for session {session_id}"
            }), 404

        # Calculate correlation metrics (simplified implementation)
        # In a full implementation, you'd compute Pearson/Spearman correlation
        correlation_metrics = {
            "session_id": session_id,
            "expert_id": expert_id,
            "validation_timestamp": datetime.now().isoformat(),
            "note": "Expert validation comparison - implement full correlation analysis for research paper"
        }

        sys_logger.log_system("info", f"Expert validation recorded for session {session_id} by {expert_id}")

        return jsonify({
            "success": True,
            "correlation_metrics": correlation_metrics,
            "expert_scores": expert_scores,
            "expert_bias_detection": expert_bias_detection,
            "note": "This endpoint provides foundation for inter-rater reliability analysis in Chapter 5/6"
        }), 200

    except Exception as e:
        sys_logger.log_system("error", f"Expert validation failed: {e}")
        return jsonify({
            "success": False,
            "error": f"Expert validation failed: {str(e)}"
        }), 500


@bp.post("/variance-test")
def multi_seed_variance_test():
    """
    Run multiple evaluations with different seeds to assess LLM consistency.
    Useful for research methodology validation and understanding evaluation reliability.

    Payload:
    {
      "diagnosis": "text",
      "metacognitive_responses": { "Q1": "A1", ... },
      "case_context": {...},
      "session_id": "session_id",
      "num_runs": 3,
      "seed_values": [42, 123, 789]  // optional
    }
    """
    data = request.get_json(silent=True) or {}
    diagnosis = (data.get("diagnosis") or "").strip()
    reflection = data.get("metacognitive_responses") or {}
    case_context = data.get("case_context") or {}
    session_id = data.get("session_id")
    num_runs = data.get("num_runs", 3)
    seed_values = data.get("seed_values")

    if not diagnosis or not reflection:
        return jsonify({
            "success": False,
            "error": "diagnosis and metacognitive_responses are required"
        }), 400

    try:
        # Get session data (reuse logic from main evaluation)
        from smartdoc_api.routes.legacy import intent_driven_manager

        if intent_driven_manager and session_id:
            session_summary = intent_driven_manager.get_session_summary(session_id)
            transcript = session_summary.get("interactions", [])
            bias_warnings = session_summary.get("bias_summary", {}).get("warnings", [])
        else:
            transcript = []
            bias_warnings = []

        # Prepare inputs
        inputs = EvaluationInputs(
            dialogue_transcript=transcript,
            detected_biases=bias_warnings,
            metacognitive_responses=reflection,
            final_diagnosis=diagnosis,
            case_context=case_context,
        )

        # Run multi-seed variance test
        variance_results = research_coordinator.multi_seed_evaluation(
            inputs=inputs,
            num_runs=num_runs,
            seed_values=seed_values
        )

        sys_logger.log_system("info", f"Multi-seed variance test completed for session: {session_id}")

        return jsonify({
            "success": variance_results["success"],
            "session_id": session_id,
            "variance_analysis": variance_results,
            "research_note": "Use this data for inter-rater reliability and consistency analysis in research paper",
            "methodology_section": "This endpoint supports Chapter 5 methodology validation"
        }), 200

    except Exception as e:
        sys_logger.log_system("error", f"Variance test failed: {e}")
        return jsonify({
            "success": False,
            "error": f"Variance test failed: {str(e)}"
        }), 500
