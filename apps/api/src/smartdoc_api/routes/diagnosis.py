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

            # Use real SmartDoc LLM evaluation
            from smartdoc_core.clinical.evaluator import EvaluationInputs

            # Get session data for comprehensive evaluation
            session_id = data.get("session_id", "unknown_session")
            transcript = []
            bias_warnings = []
            discovered_information = None

            sys_logger.log_system("info", f"[DEBUG] Session ID received: '{session_id}'")

            # Try to get session data from the database (not in-memory loggers)
            try:
                from smartdoc_api.services.repo import session_scope
                from smartdoc_api.db.models import SimulationSession, Message, DiscoveryEvent, BiasWarning
                from sqlalchemy import select

                sys_logger.log_system("info", f"[DEBUG] Retrieving session data from database for session: '{session_id}'")

                with session_scope() as s:
                    # Get session info
                    session = s.get(SimulationSession, session_id)
                    if session:
                        sys_logger.log_system("info", f"[DEBUG] Found session in database: {session.id}")

                        # Get conversation messages (transcript)
                        if session.conversation_id:
                            message_records = s.execute(
                                select(Message).where(Message.conversation_id == session.conversation_id)
                                .order_by(Message.created_at)
                            ).scalars().all()

                            transcript = []
                            for msg in message_records:
                                transcript.append({
                                    "role": "user" if msg.role.value == "user" else "assistant",
                                    "message": msg.content,
                                    "content": msg.content,
                                    "context": msg.context,
                                    "timestamp": msg.created_at.isoformat(),
                                    "user_query": msg.content if msg.role.value == "user" else "",
                                    "vsp_response": msg.content if msg.role.value == "assistant" else ""
                                })

                            sys_logger.log_system("info", f"[DEBUG] Retrieved {len(transcript)} messages from database")
                        else:
                            sys_logger.log_system("warning", f"[DEBUG] Session has no conversation_id")

                        # Get bias warnings from database
                        bias_records = s.execute(
                            select(BiasWarning).where(BiasWarning.session_id == session_id)
                            .order_by(BiasWarning.created_at)
                        ).scalars().all()

                        bias_warnings = []
                        for bias in bias_records:
                            bias_warnings.append({
                                "bias_type": bias.bias_type,
                                "description": bias.description,
                                "timestamp": bias.created_at.isoformat()
                            })

                        sys_logger.log_system("info", f"[DEBUG] Retrieved {len(bias_warnings)} bias warnings from database")

                        # Get discovered information from database
                        discovery_records = s.execute(
                            select(DiscoveryEvent).where(DiscoveryEvent.session_id == session_id)
                            .order_by(DiscoveryEvent.created_at)
                        ).scalars().all()

                        discovered_blocks = {}
                        for discovery in discovery_records:
                            category = discovery.category
                            if category not in discovered_blocks:
                                discovered_blocks[category] = []

                            discovered_blocks[category].append({
                                "label": discovery.label,
                                "value": discovery.value,
                                "content": discovery.value,
                                "isRevealed": True,
                                "timestamp": discovery.created_at.isoformat()
                            })

                        discovered_information = discovered_blocks if discovered_blocks else None
                        sys_logger.log_system("info", f"[DEBUG] Retrieved {len(discovered_blocks)} discovery categories from database")

                    else:
                        sys_logger.log_system("warning", f"[DEBUG] No session found in database for session_id: '{session_id}'")
                        transcript = []
                        bias_warnings = []
                        discovered_information = None

                # Also try the in-memory system as fallback (for development)
                from smartdoc_api.routes.legacy import intent_driven_manager
                if intent_driven_manager and len(transcript) == 0:
                    sys_logger.log_system("info", f"[DEBUG] No database transcript, trying in-memory fallback")
                    if session_id in intent_driven_manager._session_loggers:
                        session_logger = intent_driven_manager._session_loggers[session_id]
                        transcript = session_logger.get_interactions()
                        bias_data = session_logger.get_bias_summary()
                        bias_warnings = bias_data.get("warnings", [])
                        sys_logger.log_system("info", f"[DEBUG] Retrieved from in-memory: {len(transcript)} interactions")
                    else:
                        available_sessions = list(intent_driven_manager._session_loggers.keys())
                        sys_logger.log_system("info", f"[DEBUG] Session not in memory either. Available: {available_sessions}")

                sys_logger.log_system("info", f"Final session data: {len(transcript)} interactions, {len(bias_warnings)} bias warnings")
            except Exception as e:
                sys_logger.log_system("error", f"Could not retrieve session data from database: {e}")
                transcript = []
                bias_warnings = []
                discovered_information = None

            # Prepare inputs for LLM evaluation
            evaluation_inputs = EvaluationInputs(
                dialogue_transcript=transcript,
                detected_biases=bias_warnings,
                metacognitive_responses=metacognitive_responses,
                final_diagnosis=diagnosis,
                case_context=session_data,
                discovered_information=discovered_information
            )

            # Run LLM evaluation
            llm_result = clinical_evaluator.evaluate(evaluation_inputs)

            if llm_result.get("success") and llm_result.get("evaluation"):
                evaluation = llm_result["evaluation"]

                # Extract scores from LLM evaluation
                diagnostic_accuracy = evaluation.get("diagnostic_accuracy", {}).get("score", 0)
                information_gathering = evaluation.get("information_gathering", {}).get("score", 0)
                cognitive_bias_awareness = evaluation.get("cognitive_bias_awareness", {}).get("score", 0)

                # Calculate overall score as average
                overall_score = round((diagnostic_accuracy + information_gathering + cognitive_bias_awareness) / 3)

                # Extract feedback - prioritize comprehensive feedback over individual parts
                comprehensive_feedback = evaluation.get("comprehensive_feedback", {})
                if comprehensive_feedback.get("strengths"):
                    feedback_text = f"Strengths: {comprehensive_feedback['strengths']}"
                    if comprehensive_feedback.get("areas_for_improvement"):
                        feedback_text += f" | Areas for improvement: {comprehensive_feedback['areas_for_improvement']}"
                else:
                    feedback_text = "LLM evaluation completed."

                # Check if this was an automatic low score due to quality issues
                quality_note = ""
                if llm_result.get("automatic_low_score"):
                    issues = llm_result.get("quality_issues_detected", [])
                    quality_note = f" | Quality issues detected: {', '.join(issues)}"
                    feedback_text += quality_note                # Persist diagnosis with LLM evaluation
                submit_diagnosis(
                    session_id=session_id,
                    diagnosis_text=diagnosis,
                    score_overall=overall_score,
                    score_breakdown={
                        "information_gathering": information_gathering,
                        "cognitive_bias_awareness": cognitive_bias_awareness,
                        "diagnostic_accuracy": diagnostic_accuracy,
                        "llm_evaluation_raw": evaluation
                    },
                    feedback=feedback_text,
                    reflections=metacognitive_responses
                )

                return jsonify({
                    "score": f"{overall_score}/100",
                    "feedback": feedback_text,
                    "performance_summary": {
                        "information_discovery": f"{information_gathering}/100",
                        "bias_awareness": f"{cognitive_bias_awareness}/100",
                        "diagnostic_accuracy": f"{diagnostic_accuracy}/100",
                    },
                    "llm_evaluation": llm_result,
                    "metacognitive_responses": metacognitive_responses,
                    "smartdoc_engine": True
                })
            else:
                # Fallback if LLM evaluation fails
                sys_logger.log_system("warning", f"LLM evaluation failed: {llm_result}")
                overall_score = 75  # Default fallback score

                submit_diagnosis(
                    session_id=session_id,
                    diagnosis_text=diagnosis,
                    score_overall=overall_score,
                    score_breakdown={
                        "information_gathering": 75,
                        "cognitive_bias_awareness": 75,
                        "diagnostic_accuracy": 75
                    },
                    feedback="Evaluation completed (LLM evaluation failed, using fallback).",
                    reflections=metacognitive_responses
                )

                return jsonify({
                    "score": f"{overall_score}/100",
                    "feedback": "Evaluation completed (LLM evaluation failed, using fallback).",
                    "performance_summary": {
                        "information_discovery": "75/100",
                        "bias_awareness": "75/100",
                        "diagnostic_accuracy": "75/100",
                    },
                    "llm_evaluation": {"success": False, "error": "LLM evaluation failed"},
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
