"""
Diagnosis API Routes

Handles diagnosis submission and evaluation with the SmartDoc AI system.
"""

from flask import request, jsonify
from . import bp
import uuid

# Import repository functions for data persistence
from smartdoc_api.services.repo import submit_diagnosis
from smartdoc_api.services.auth_service import require_auth

# Import real SmartDoc components
try:
    from smartdoc_core.clinical.evaluator import ClinicalEvaluator
    from smartdoc_core.utils.logger import sys_logger
    from smartdoc_core.config.settings import config

    SMARTDOC_AVAILABLE = True
    clinical_evaluator = ClinicalEvaluator()
    print("✅ SmartDoc diagnosis evaluator initialized for v1 API!")

except ImportError as e:
    print(f"⚠️ SmartDoc core not available for diagnosis API: {e}")
    SMARTDOC_AVAILABLE = False

    # Mock components as fallback
    class MockLogger:
        def log_system(self, level, message):
            print(f"[DIAGNOSIS-{level.upper()}] {message}")

    sys_logger = MockLogger()
    clinical_evaluator = None


@bp.post("/diagnosis")
@require_auth
def v1_submit_diagnosis():
    """
    Submit a diagnosis for evaluation.

    Request JSON:
        {
            "diagnosis": "string - The diagnosis text",
            "session_data": {
                "discovered_count": int,
                "bias_warnings": int,
                "discovered_info": object
            }
        }

    Response JSON:
        {
            "score": "string - Score in format 'X/100'",
            "feedback": "string - Feedback message",
            "performance_summary": {
                "information_discovery": "string",
                "bias_awareness": "string",
                "diagnostic_accuracy": "string"
            }
        }
    """
    data = request.get_json() or {}
    diagnosis = data.get("diagnosis", "")
    session_data = data.get("session_data", {})

    if not diagnosis.strip():
        return jsonify({"error": "diagnosis is required"}), 400

    try:
        if SMARTDOC_AVAILABLE and clinical_evaluator:
            sys_logger.log_system(
                "info", f"[V1] Evaluating diagnosis with SmartDoc: {diagnosis[:50]}..."
            )

            # TODO: Implement real evaluation with clinical_evaluator
            # For now, use the same logic as legacy
            discovered_count = session_data.get("discovered_count", 0)
            bias_warnings = session_data.get("bias_warnings", 0)

            # Calculate scores
            discovery_percentage = (discovered_count / 20) * 100 if discovered_count else 0
            bias_score = max(0, 100 - (bias_warnings * 10))
            overall_score = round((discovery_percentage * 0.6) + (bias_score * 0.4))

            # Persist diagnosis
            submit_diagnosis(
                session_id=data.get("session_id", "unknown_session"),  # include session_id in FE calls
                diagnosis_text=diagnosis,
                score_overall=overall_score,
                score_breakdown={
                    "information_discovery": discovery_percentage,
                    "bias_awareness": bias_score
                },
                feedback=f"You discovered {discovered_count} clinical findings. Your diagnosis: '{diagnosis}'",
                reflections=None
            )

            return jsonify({
                "score": f"{overall_score}/100",
                "feedback": f"You discovered {discovered_count} clinical findings. Your diagnosis: '{diagnosis}'",
                "performance_summary": {
                    "information_discovery": f"{'Excellent' if discovery_percentage >= 80 else 'Good'} ({discovered_count}/20 items)",
                    "bias_awareness": f"{'Excellent' if bias_warnings == 0 else 'Good'} ({bias_warnings} warnings)",
                    "diagnostic_accuracy": "Requires expert review",
                },
                "smartdoc_engine": True
            })
        else:
            # Fallback mock evaluation
            return jsonify({
                "score": "75/100",
                "feedback": f"Mock evaluation completed. Your diagnosis: '{diagnosis}'",
                "performance_summary": {
                    "information_discovery": "Good (mock data)",
                    "bias_awareness": "Good (mock data)",
                    "diagnostic_accuracy": "Mock evaluation",
                },
                "smartdoc_engine": False
            })

    except Exception as e:
        sys_logger.log_system("error", f"[V1] Diagnosis evaluation error: {e}")
        return jsonify({"error": f"Diagnosis evaluation failed: {str(e)}"}), 500


@bp.post("/diagnosis/reflection")
@require_auth
def v1_submit_diagnosis_with_reflection():
    """
    Submit a diagnosis with metacognitive reflection for comprehensive evaluation.

    Request JSON:
        {
            "diagnosis": "string - The diagnosis text",
            "metacognitive_responses": {
                "question1": "answer1",
                "question2": "answer2",
                ...
            },
            "session_data": {
                "discovered_count": int,
                "bias_warnings": int,
                "discovered_info": object
            }
        }

    Response JSON:
        {
            "score": "string - Score in format 'X/100'",
            "feedback": "string - Feedback message",
            "performance_summary": {
                "information_discovery": "string",
                "bias_awareness": "string",
                "diagnostic_accuracy": "string"
            },
            "llm_evaluation": {
                "success": boolean,
                "evaluation": {
                    "overall_score": int,
                    "information_gathering": {"score": int},
                    "cognitive_bias_awareness": {"score": int},
                    "diagnostic_accuracy": {"score": int}
                }
            },
            "metacognitive_responses": object
        }
    """
    data = request.get_json() or {}
    diagnosis = data.get("diagnosis", "")
    metacognitive_responses = data.get("metacognitive_responses", {})
    session_data = data.get("session_data", {})

    if not diagnosis.strip():
        return jsonify({"error": "diagnosis is required"}), 400

    if not metacognitive_responses:
        return jsonify({"error": "metacognitive_responses is required"}), 400

    try:
        if SMARTDOC_AVAILABLE and clinical_evaluator:
            sys_logger.log_system(
                "info", f"[V1] Evaluating diagnosis with reflection: {diagnosis[:50]}..."
            )

            # TODO: Implement real comprehensive evaluation with clinical_evaluator
            # For now, use enhanced mock evaluation
            discovered_count = session_data.get("discovered_count", 0)
            bias_warnings = session_data.get("bias_warnings", 0)

            # Enhanced scoring with reflection
            discovery_percentage = (discovered_count / 20) * 100 if discovered_count else 0
            bias_score = max(0, 100 - (bias_warnings * 10))
            reflection_quality = len([r for r in metacognitive_responses.values() if len(r.strip()) >= 10])
            reflection_bonus = min(10, reflection_quality * 2)  # Up to 10 bonus points

            overall_score = min(100, round((discovery_percentage * 0.5) + (bias_score * 0.3) + (reflection_bonus * 2)))

            # Persist diagnosis with reflection
            submit_diagnosis(
                session_id=data.get("session_id", "unknown_session"),
                diagnosis_text=diagnosis,
                score_overall=overall_score,
                score_breakdown={
                    "information_gathering": int(discovery_percentage * 0.8),
                    "cognitive_bias_awareness": bias_score,
                    "diagnostic_accuracy": overall_score
                },
                feedback="Comprehensive evaluation completed with metacognitive reflection.",
                reflections=metacognitive_responses
            )

            return jsonify({
                "score": f"{overall_score}/100",
                "feedback": "Comprehensive evaluation completed with metacognitive reflection.",
                "performance_summary": {
                    "information_discovery": f"{'Excellent' if discovery_percentage >= 80 else 'Good'} ({discovered_count}/20 items)",
                    "bias_awareness": f"{'Excellent' if bias_warnings == 0 else 'Good'} ({bias_warnings} warnings)",
                    "diagnostic_accuracy": f"{overall_score}/100",
                },
                "llm_evaluation": {
                    "success": True,
                    "evaluation": {
                        "overall_score": overall_score,
                        "information_gathering": {"score": int(discovery_percentage * 0.8)},
                        "cognitive_bias_awareness": {"score": bias_score},
                        "diagnostic_accuracy": {"score": overall_score},
                    },
                },
                "metacognitive_responses": metacognitive_responses,
                "smartdoc_engine": True
            })
        else:
            # Fallback mock comprehensive evaluation
            return jsonify({
                "score": "85/100",
                "feedback": "Mock comprehensive evaluation completed with metacognitive reflection.",
                "performance_summary": {
                    "information_discovery": "Good (15/20 items)",
                    "bias_awareness": "Excellent (0 warnings)",
                    "diagnostic_accuracy": "85/100",
                },
                "llm_evaluation": {
                    "success": True,
                    "evaluation": {
                        "overall_score": 85,
                        "information_gathering": {"score": 80},
                        "cognitive_bias_awareness": {"score": 95},
                        "diagnostic_accuracy": {"score": 85},
                    },
                },
                "metacognitive_responses": metacognitive_responses,
                "smartdoc_engine": False
            })

    except Exception as e:
        sys_logger.log_system("error", f"[V1] Diagnosis reflection evaluation error: {e}")
        return jsonify({"error": f"Diagnosis evaluation failed: {str(e)}"}), 500


@bp.get("/diagnosis/health")
def v1_diagnosis_health():
    """Health check for diagnosis functionality."""
    return jsonify({
        "status": "ok",
        "endpoint": "diagnosis",
        "smartdoc_available": SMARTDOC_AVAILABLE
    })
