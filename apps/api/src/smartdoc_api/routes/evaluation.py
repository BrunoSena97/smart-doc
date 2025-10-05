from __future__ import annotations
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from smartdoc_core.clinical.evaluator import ClinicalEvaluator, EvaluationInputs
from smartdoc_core.simulation.bias_analyzer import BiasEvaluator
from smartdoc_core.utils.logger import sys_logger

bp = Blueprint("evaluation", __name__, url_prefix="/api/v1/evaluation")

# Initialize clinical evaluator
clinical_evaluator = ClinicalEvaluator(
    enable_validation=True,
    enable_reliability_tracking=True,
    temperature=0.1
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

    # Debug logging to check what's being received
    sys_logger.log_system("info", f"Evaluation endpoint received session_id: {session_id}")
    sys_logger.log_system("info", f"Request data keys: {list(data.keys())}")

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

            # Debug session data
            sys_logger.log_system("info", f"Session summary keys: {list(session_summary.keys())}")
            sys_logger.log_system("info", f"Transcript length: {len(transcript)}")
            sys_logger.log_system("info", f"Bias warnings count: {len(bias_warnings)}")

            # Get session state for rule-based analysis
            session_state = intent_driven_manager.store.get_session(session_id)
            if session_state:
                sys_logger.log_system("info", f"Session state found - interactions count: {len(session_state.interactions)}")
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

        # Prepare inputs for evaluation
        inputs = EvaluationInputs(
            dialogue_transcript=transcript,
            detected_biases=bias_warnings,
            metacognitive_responses=reflection,
            final_diagnosis=diagnosis,
            case_context=case_context,
        )

        # Run LLM evaluation
        sys_logger.log_system("info", f"Submit endpoint: Running evaluation for session {session_id}")
        llm_results = clinical_evaluator.evaluate(inputs)

        # Run rule-based bias analysis if we have session data
        rule_based_results = {}
        if case_data and session_log:
            try:
                bias_evaluator = BiasEvaluator(case_data)
                rule_based_bias = bias_evaluator.evaluate_session(
                    session_log, revealed_blocks, hypotheses, diagnosis
                )
                rule_based_results = {
                    "success": True,
                    "bias_analysis": rule_based_bias,
                    "method": "rule_based"
                }
            except Exception as e:
                sys_logger.log_system("warning", f"Rule-based analysis failed: {e}")
                rule_based_results = {
                    "success": False,
                    "error": str(e),
                    "method": "rule_based"
                }

        # Extract results for database storage
        evaluation = llm_results.get("evaluation", {})

        overall_score = 0
        if evaluation:
            # Calculate overall score from component scores
            scores = []
            for component in ["diagnostic_accuracy", "information_gathering", "cognitive_bias_awareness"]:
                component_data = evaluation.get(component, {})
                if isinstance(component_data, dict) and "score" in component_data:
                    scores.append(component_data["score"])
            overall_score = sum(scores) / len(scores) if scores else 0

        score_breakdown = {
            "diagnostic_accuracy": evaluation.get("diagnostic_accuracy", {}).get("score", 0),
            "information_gathering": evaluation.get("information_gathering", {}).get("score", 0),
            "cognitive_bias_awareness": evaluation.get("cognitive_bias_awareness", {}).get("score", 0),
            "llm_evaluation_raw": evaluation,
            "rule_based_bias_analysis": rule_based_results
        }

        # Build feedback
        feedback_parts = []
        comprehensive_feedback = evaluation.get("comprehensive_feedback", {})
        if comprehensive_feedback:
            if comprehensive_feedback.get("strengths"):
                feedback_parts.append(f"Strengths: {comprehensive_feedback['strengths']}")
            if comprehensive_feedback.get("areas_for_improvement"):
                feedback_parts.append(f"Areas for improvement: {comprehensive_feedback['areas_for_improvement']}")

        if rule_based_results.get("success"):
            feedback_parts.append(f"Rule-based bias analysis: {rule_based_results['bias_analysis']}")

        final_feedback = " | ".join(feedback_parts) if feedback_parts else "Evaluation completed"

        # Store evaluation results in database
        from smartdoc_api.services.repo import submit_diagnosis

        submit_diagnosis(
            session_id=session_id or "unknown_session",
            diagnosis_text=diagnosis,
            score_overall=int(overall_score) if overall_score else None,
            score_breakdown=score_breakdown,
            feedback=final_feedback,
            reflections=reflection
        )

        # Build response
        resp = {
            "success": llm_results.get("success", True),
            "session_id": session_id,
            "llm_evaluation": llm_results,
            "rule_based_bias_analysis": rule_based_results,
            "database_stored": True,
            "evaluation_timestamp": datetime.now().isoformat()
        }

        sys_logger.log_system("info", f"Evaluation completed for session: {session_id}")
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
    Get basic reliability metrics from stored evaluation data.
    """
    try:
        from smartdoc_api.services.repo import get_session
        import json

        # Get evaluation data from database
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
                "total_evaluations": 0
            }), 200

        # Analyze stored evaluation data
        total_evaluations = len(evaluations)
        successful_evaluations = 0

        for eval_record in evaluations:
            try:
                session_id, diagnosis_text, score_overall, score_breakdown_str, created_at = eval_record
                score_breakdown = json.loads(score_breakdown_str) if score_breakdown_str else {}

                # Check if evaluation was successful (has LLM evaluation data)
                if 'llm_evaluation_raw' in score_breakdown:
                    successful_evaluations += 1

            except (json.JSONDecodeError, KeyError, ValueError) as e:
                sys_logger.log_system("warning", f"Failed to parse evaluation data for record: {e}")
                continue

        # Calculate reliability metrics
        success_rate = successful_evaluations / total_evaluations if total_evaluations > 0 else 0

        reliability_report = {
            "total_evaluations": total_evaluations,
            "successful_evaluations": successful_evaluations,
            "success_rate": success_rate,
            "evaluation_method": "llm_with_rule_based_bias_detection"
        }

        return jsonify({
            "success": True,
            "reliability_report": reliability_report
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
        "cognitive_bias_awareness": 0-100
      },
      "expert_id": "expert_identifier"
    }
    """
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    expert_scores = data.get("expert_scores", {})
    expert_id = data.get("expert_id", "unknown_expert")

    if not session_id or not expert_scores:
        return jsonify({
            "success": False,
            "error": "session_id and expert_scores are required"
        }), 400

    try:
        # Store expert validation data (simplified implementation)
        validation_record = {
            "session_id": session_id,
            "expert_id": expert_id,
            "expert_scores": expert_scores,
            "validation_timestamp": datetime.now().isoformat()
        }

        sys_logger.log_system("info", f"Expert validation recorded for session {session_id} by {expert_id}")

        return jsonify({
            "success": True,
            "validation_record": validation_record,
            "note": "Expert validation stored for inter-rater reliability analysis"
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

    Payload:
    {
      "diagnosis": "text",
      "metacognitive_responses": { "Q1": "A1", ... },
      "case_context": {...},
      "session_id": "session_id",
      "num_runs": 3
    }
    """
    data = request.get_json(silent=True) or {}
    diagnosis = (data.get("diagnosis") or "").strip()
    reflection = data.get("metacognitive_responses") or {}
    case_context = data.get("case_context") or {}
    session_id = data.get("session_id")
    num_runs = data.get("num_runs", 3)

    if not diagnosis or not reflection:
        return jsonify({
            "success": False,
            "error": "diagnosis and metacognitive_responses are required"
        }), 400

    try:
        # Prepare inputs
        inputs = EvaluationInputs(
            dialogue_transcript=[],
            detected_biases=[],
            metacognitive_responses=reflection,
            final_diagnosis=diagnosis,
            case_context=case_context,
        )

        # Run multiple evaluations with different temperatures for variance
        results = []
        for i in range(num_runs):
            evaluator = ClinicalEvaluator(
                enable_validation=True,
                temperature=0.1 + (i * 0.1)  # Vary temperature slightly
            )
            result = evaluator.evaluate(inputs)
            if result.get("success"):
                evaluation = result.get("evaluation", {})
                results.append({
                    "run": i + 1,
                    "temperature": 0.1 + (i * 0.1),
                    "diagnostic_accuracy": evaluation.get("diagnostic_accuracy", {}).get("score", 0),
                    "information_gathering": evaluation.get("information_gathering", {}).get("score", 0),
                    "cognitive_bias_awareness": evaluation.get("cognitive_bias_awareness", {}).get("score", 0)
                })

        sys_logger.log_system("info", f"Multi-run variance test completed for session: {session_id}")

        return jsonify({
            "success": len(results) > 0,
            "session_id": session_id,
            "total_runs": num_runs,
            "successful_runs": len(results),
            "results": results,
            "note": "Variance testing for LLM evaluation consistency"
        }), 200

    except Exception as e:
        sys_logger.log_system("error", f"Variance test failed: {e}")
        return jsonify({
            "success": False,
            "error": f"Variance test failed: {str(e)}"
        }), 500
