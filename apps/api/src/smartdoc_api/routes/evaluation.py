from __future__ import annotations
from flask import Blueprint, request, jsonify, current_app
from smartdoc_core.clinical.evaluator import ClinicalEvaluator, EvaluationInputs
from smartdoc_core.utils.logger import sys_logger

bp = Blueprint("evaluation", __name__, url_prefix="/api/v1/evaluation")

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
        # Try to get session data via the intent driven manager
        # This mimics the pattern used in legacy.py and chat.py
        from smartdoc_api.routes.legacy import intent_driven_manager

        if intent_driven_manager and session_id:
            # Get session summary which includes interactions and bias data
            session_summary = intent_driven_manager.get_session_summary(session_id)
            transcript = session_summary.get("interactions", [])
            bias_data = session_summary.get("bias_summary", {})
            bias_warnings = bias_data.get("warnings", [])
        else:
            # Fallback if no session or manager available
            transcript = []
            bias_warnings = []
            sys_logger.log_system("warning", "No session data available for evaluation - using empty transcript")

        evaluator = ClinicalEvaluator()  # uses shared provider & config
        inputs = EvaluationInputs(
            dialogue_transcript=transcript,
            detected_biases=bias_warnings,
            metacognitive_responses=reflection,
            final_diagnosis=diagnosis,
            case_context=case_context,
        )

        eval_out = evaluator.evaluate(inputs)
        deep_bias = evaluator.deep_bias_analysis(transcript, diagnosis)

        resp = {
            "success": True,
            "llm_evaluation": eval_out,
            "bias_analysis": deep_bias if deep_bias.get("success") else None,
            "session_id": session_id,
        }
        sys_logger.log_system("info", f"Returned metacognitive evaluation for session: {session_id}")
        return jsonify(resp), 200

    except Exception as e:
        sys_logger.log_system("error", f"Evaluation failed: {e}")
        return jsonify({
            "success": False,
            "error": f"Evaluation failed: {str(e)}"
        }), 500
