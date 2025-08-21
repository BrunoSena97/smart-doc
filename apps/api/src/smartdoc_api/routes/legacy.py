"""
Legacy Routes Blueprint

Maintains backward compatibility with existing frontend during migration.
These routes mirror the original API structure and will be deprecated
once the frontend is updated to use the new /api/v1/ endpoints.
"""

from flask import Blueprint, request, jsonify, send_from_directory
import uuid
import os

# Import real SmartDoc components
try:
    from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager
    from smartdoc_core.clinical.evaluator import ClinicalEvaluator
    from smartdoc_core.utils.logger import sys_logger
    from smartdoc_core.config.settings import config
    from smartdoc_core.simulation.session_tracker import (
        get_current_session,
        start_new_session,
    )

    SMARTDOC_AVAILABLE = True

    # Initialize SmartDoc components
    print("🔧 Initializing SmartDoc components...")

    # Initialize Intent-Driven Disclosure Manager
    # Navigate from apps/api/src/smartdoc_api/routes/ to project root, then to data
    project_root = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        )
    )
    case_file_path = os.path.join(
        project_root, "data", "raw", "cases", "intent_driven_case.json"
    )
    print(f"🔍 Looking for case file at: {case_file_path}")

    intent_driven_manager = IntentDrivenDisclosureManager(case_file_path=case_file_path)
    clinical_evaluator = ClinicalEvaluator()

    print("✅ SmartDoc components initialized successfully!")

except ImportError as e:
    print(f"⚠️ SmartDoc core not available: {e}")
    SMARTDOC_AVAILABLE = False

    # Mock components as fallback
    class MockLogger:
        def log_system(self, level, message):
            print(f"[{level.upper()}] {message}")

    sys_logger = MockLogger()
    intent_driven_manager = None
    clinical_evaluator = None

    _current_session = None

    def get_current_session():
        global _current_session
        return _current_session

    def start_new_session():
        global _current_session

        class MockSession:
            def __init__(self):
                self.interactions = []
                self.session_id = f"mock_session_{uuid.uuid4().hex[:8]}"

            def log_interaction(self, **kwargs):
                self.interactions.append(kwargs)

            def get_interactions(self):
                return self.interactions

            def get_bias_summary(self):
                return {"bias_warnings": []}

            def get_latest_bias_warning(self):
                return None

            def save_session(self):
                pass

        _current_session = MockSession()
        return _current_session


bp = Blueprint("legacy", __name__)

# Mock session storage (will be replaced with proper session management)
_sessions = {}


@bp.route("/get_bot_response", methods=["POST"])
def get_bot_response():
    """Legacy endpoint for bot responses - uses real SmartDoc engine when available."""
    data = request.get_json() or {}
    user_input = data.get("message", "").strip()
    context = data.get("context", "anamnesis")
    session_id = data.get("session_id", f"legacy_session_{uuid.uuid4().hex[:8]}")

    if not user_input:
        return jsonify(
            {
                "response": "I didn't receive any input. Could you please ask a question?",
                "error": False,
            }
        )

    # Try to use real SmartDoc engine
    if SMARTDOC_AVAILABLE and intent_driven_manager:
        try:
            sys_logger.log_system(
                "info", f"Processing query with SmartDoc engine: {user_input}"
            )

            # Process with Intent-Driven Discovery and context filtering
            discovery_result = intent_driven_manager.process_doctor_query(
                session_id, user_input, context
            )

            if discovery_result["success"]:
                # Generate context-appropriate response
                response_text = discovery_result["response"]["text"]

                response_data = {
                    "response": response_text,
                    "discovery_events": [],
                    "discovery_stats": {},
                    "bias_warnings": [],
                    "context": context,
                    "smartdoc_engine": True,
                }

                # Process discoveries into events for the frontend
                if (
                    "discoveries" in discovery_result["response"]
                    and discovery_result["response"]["discoveries"]
                ):
                    discovery_events = []
                    for discovery in discovery_result["response"]["discoveries"]:
                        # Use the structured discovery data from LLM Discovery Processor
                        discovery_event = {
                            "category": discovery["category"],
                            "field": discovery[
                                "label"
                            ],  # Fixed label as key to prevent duplication
                            "value": discovery["summary"],  # Clean clinical summary
                            "confidence": discovery.get("confidence", 1.0),
                            "block_id": discovery["block_id"],
                        }
                        discovery_events.append(discovery_event)
                        sys_logger.log_system(
                            "debug", f"Created discovery event: {discovery_event}"
                        )
                    response_data["discovery_events"] = discovery_events
                    sys_logger.log_system(
                        "info",
                        f"Sending {len(discovery_events)} discovery events to frontend",
                    )

                # Add discovery stats from the session manager
                if "session_stats" in discovery_result:
                    session_stats = discovery_result["session_stats"]
                    response_data["discovery_stats"] = {
                        "total": session_stats.get("total_blocks", 0),
                        "discovered": session_stats.get("revealed_blocks", 0),
                    }

                # Add bias warning from discovery result if detected
                if "bias_warning" in discovery_result:
                    response_data["bias_warnings"].append(
                        discovery_result["bias_warning"]
                    )
                    sys_logger.log_system(
                        "warning",
                        f"Discovery bias warning sent to frontend: {discovery_result['bias_warning']['bias_type']}",
                    )

                return jsonify(response_data)
            else:
                sys_logger.log_system(
                    "error",
                    f"SmartDoc processing failed: {discovery_result.get('error', 'Unknown error')}",
                )
                # Fall through to mock response

        except Exception as e:
            sys_logger.log_system("error", f"SmartDoc engine error: {e}")
            # Fall through to mock response

    # Fallback to mock response when SmartDoc engine is not available
    sys_logger.log_system(
        "warning", "Using mock response - SmartDoc engine not available"
    )

    # Mock response based on context (original implementation)
    context_responses = {
        "anamnesis": f"Thank you for asking about {user_input}. My mother has been experiencing symptoms for several weeks now.",
        "physical-exam": f"For the physical examination regarding {user_input}, let me help position my mother.",
        "exams": f"About the tests you mentioned ({user_input}), we have some recent results to share.",
    }

    response_text = context_responses.get(
        context,
        f"I understand you're asking about {user_input}. Let me help answer that.",
    )

    # Mock discovery event
    discovery_event = {
        "category": "Clinical History",
        "field": f"Response to {user_input[:20]}...",
        "value": "Patient information revealed (mock)",
        "confidence": 0.5,
        "block_id": f"mock_block_{uuid.uuid4().hex[:8]}",
    }

    return jsonify(
        {
            "response": response_text,
            "discovery_events": [discovery_event],
            "discovery_stats": {"total": 20, "discovered": 3},  # Mock values
            "bias_warnings": [],
            "context": context,
            "smartdoc_engine": False,
        }
    )


@bp.route("/submit_diagnosis", methods=["POST"])
def submit_diagnosis():
    """Legacy endpoint for diagnosis submission."""
    data = request.get_json() or {}
    diagnosis = data.get("diagnosis", "")
    session_data = data.get("session_data", {})

    discovered_count = session_data.get("discovered_count", 0)
    bias_warnings = session_data.get("bias_warnings", 0)

    # Calculate scores
    discovery_percentage = (discovered_count / 20) * 100 if discovered_count else 0
    bias_score = max(0, 100 - (bias_warnings * 10))
    overall_score = round((discovery_percentage * 0.6) + (bias_score * 0.4))

    return jsonify(
        {
            "score": f"{overall_score}/100",
            "feedback": f"You discovered {discovered_count} clinical findings. Your diagnosis: '{diagnosis}'",
            "performance_summary": {
                "information_discovery": f"{'Excellent' if discovery_percentage >= 80 else 'Good'} ({discovered_count}/20 items)",
                "bias_awareness": f"{'Excellent' if bias_warnings == 0 else 'Good'} ({bias_warnings} warnings)",
                "diagnostic_accuracy": "Requires expert review",
            },
        }
    )


@bp.route("/submit_diagnosis_with_reflection", methods=["POST"])
def submit_diagnosis_with_reflection():
    """Legacy endpoint for comprehensive diagnosis submission with reflection."""
    data = request.get_json() or {}
    diagnosis = data.get("diagnosis", "")
    metacognitive_responses = data.get("metacognitive_responses", {})
    session_data = data.get("session_data", {})

    # Mock comprehensive evaluation
    return jsonify(
        {
            "score": "85/100",
            "feedback": "Comprehensive evaluation completed with metacognitive reflection.",
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
        }
    )


@bp.route("/static/<path:filename>")
def serve_static(filename):
    """Serve static files for legacy compatibility."""
    static_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "web",
        "public",
    )
    return send_from_directory(static_dir, filename)


@bp.post("/chat")
def legacy_chat():
    """Legacy chat endpoint for simple API compatibility."""
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    try:
        reply = f"SmartDoc AI: I understand you're asking about '{message}'. How can I help with your clinical simulation?"
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": f"AI processing failed: {str(e)}"}), 500
