"""
Chat API Routes

Handles chat interactions with the full SmartDoc AI system including
Intent-Driven Disclosure Manager and clinical evaluation.
"""

from flask import request, jsonify
from . import bp
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
    print("🔧 Initializing SmartDoc components for v1 API...")

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

    print("✅ SmartDoc components initialized successfully for v1 API!")

except ImportError as e:
    print(f"⚠️ SmartDoc core not available for v1 API: {e}")
    SMARTDOC_AVAILABLE = False

    # Mock components as fallback
    class MockLogger:
        def log_system(self, level, message):
            print(f"[V1-{level.upper()}] {message}")

    sys_logger = MockLogger()
    intent_driven_manager = None
    clinical_evaluator = None


@bp.post("/chat")
def v1_chat():
    """
    Process a chat message and return AI response with full SmartDoc functionality.

    Request JSON:
        {
            "message": "string - User's message",
            "context": "string - Optional context (anamnesis, physical-exam, exams)",
            "session_id": "string - Optional session ID"
        }

    Response JSON:
        {
            "reply": "string - AI response",
            "response": "string - AI response (legacy compatibility)",
            "discovery_events": [],
            "discovery_stats": {},
            "bias_warnings": [],
            "context": "string",
            "smartdoc_engine": boolean
        }

    Error Response:
        {
            "error": "string - Error description"
        }
    """
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    context = data.get("context", "anamnesis")
    session_id = data.get("session_id", f"v1_session_{uuid.uuid4().hex[:8]}")

    if not message:
        return jsonify({"error": "message is required"}), 400

    # Try to use real SmartDoc engine
    if SMARTDOC_AVAILABLE and intent_driven_manager:
        try:
            sys_logger.log_system(
                "info", f"[V1] Processing query with SmartDoc engine: {message}"
            )

            # Process with Intent-Driven Discovery and context filtering
            discovery_result = intent_driven_manager.process_doctor_query(
                session_id, message, context
            )

            if discovery_result["success"]:
                # Generate context-appropriate response
                response_text = discovery_result["response"]["text"]

                response_data = {
                    "reply": response_text,  # v1 format
                    "response": response_text,  # legacy compatibility
                    "discovery_events": [],
                    "discovery_stats": {},
                    "bias_warnings": [],
                    "context": context,
                    "smartdoc_engine": True,
                    "smartdoc_core_available": True
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
                            "field": discovery["label"],  # Fixed label as key to prevent duplication
                            "value": discovery["summary"],  # Clean clinical summary
                            "confidence": discovery.get("confidence", 1.0),
                            "block_id": discovery["block_id"],
                        }
                        discovery_events.append(discovery_event)
                        sys_logger.log_system(
                            "debug", f"[V1] Created discovery event: {discovery_event}"
                        )
                    response_data["discovery_events"] = discovery_events
                    sys_logger.log_system(
                        "info",
                        f"[V1] Sending {len(discovery_events)} discovery events to frontend",
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
                        f"[V1] Discovery bias warning sent to frontend: {discovery_result['bias_warning']['bias_type']}",
                    )

                return jsonify(response_data)
            else:
                sys_logger.log_system(
                    "error",
                    f"[V1] SmartDoc processing failed: {discovery_result.get('error', 'Unknown error')}",
                )
                # Fall through to mock response

        except Exception as e:
            sys_logger.log_system("error", f"[V1] SmartDoc engine error: {e}")
            # Fall through to mock response

    # Fallback to mock response when SmartDoc engine is not available
    sys_logger.log_system(
        "warning", "[V1] Using mock response - SmartDoc engine not available"
    )

    # Mock response based on context
    context_responses = {
        "anamnesis": f"Thank you for asking about {message}. My mother has been experiencing symptoms for several weeks now.",
        "physical-exam": f"For the physical examination regarding {message}, let me help position my mother.",
        "exams": f"About the tests you mentioned ({message}), we have some recent results to share.",
    }

    response_text = context_responses.get(
        context,
        f"I understand you're asking about {message}. Let me help answer that.",
    )

    # Mock discovery event
    discovery_event = {
        "category": "Clinical History",
        "field": f"Response to {message[:20]}...",
        "value": "Patient information revealed (mock)",
        "confidence": 0.5,
        "block_id": f"mock_block_{uuid.uuid4().hex[:8]}",
    }

    return jsonify({
        "reply": response_text,  # v1 format
        "response": response_text,  # legacy compatibility
        "discovery_events": [discovery_event],
        "discovery_stats": {"total": 20, "discovered": 3},  # Mock values
        "bias_warnings": [],
        "context": context,
        "smartdoc_engine": False,
        "smartdoc_core_available": SMARTDOC_AVAILABLE
    })


@bp.get("/chat/health")
def v1_chat_health():
    """Health check for chat functionality."""
    return jsonify({
        "status": "ok",
        "endpoint": "chat",
        "smartdoc_available": SMARTDOC_AVAILABLE
    })
