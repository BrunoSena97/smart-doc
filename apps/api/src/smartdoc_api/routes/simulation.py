"""
Clinical Simulation API Routes

Handles complex clinical simulation interactions, discovery management,
bias evaluation, and performance assessment.
"""

from flask import request, jsonify
from . import bp
import uuid

# Mock session storage (will be replaced with proper session management)
_sessions = {}


@bp.post("/simulation/start")
def start_simulation():
    """
    Start a new clinical simulation session.

    Response JSON:
        {
            "session_id": "string - Unique session identifier",
            "initial_message": "string - Opening message from virtual patient",
            "status": "active"
        }
    """
    session_id = f"sim_session_{uuid.uuid4().hex[:8]}"

    initial_message = "Hello! I'm the son of the patient. My mother doesn't speak English so I'm here to answer your questions. What would you like to know, doctor?"

    _sessions[session_id] = {
        "id": session_id,
        "status": "active",
        "interactions": [],
        "discoveries": [],
        "bias_warnings": [],
    }

    return jsonify(
        {
            "session_id": session_id,
            "initial_message": initial_message,
            "status": "active",
        }
    )


@bp.post("/simulation/interact")
def simulation_interact():
    """
    Process a clinical interaction within a simulation session.

    Request JSON:
        {
            "session_id": "string - Session identifier",
            "message": "string - Doctor's question/input",
            "context": "string - Current clinical context (anamnesis, physical-exam, labs)"
        }

    Response JSON:
        {
            "response": "string - Virtual patient response",
            "discovery_events": ["array of new discoveries"],
            "bias_warnings": ["array of bias alerts"],
            "discovery_stats": {"total": int, "discovered": int}
        }
    """
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    message = (data.get("message") or "").strip()
    context = data.get("context", "anamnesis")

    if not session_id or not message:
        return jsonify({"error": "session_id and message are required"}), 400

    if session_id not in _sessions:
        return jsonify({"error": "Invalid session_id"}), 404

    try:
        # Mock response based on context
        context_responses = {
            "anamnesis": f"Regarding the history, {message.lower()}... Well, my mother has been experiencing these symptoms for several weeks now.",
            "physical-exam": f"For the physical examination, {message.lower()}... Let me help position my mother for the examination.",
            "exams": f"About the laboratory tests, {message.lower()}... Yes, we have some recent results we can share.",
        }

        response_text = context_responses.get(
            context,
            f"I understand you're asking about {message}. Let me help answer that.",
        )

        # Mock discovery (would be real AI discovery in full implementation)
        discovery_event = {
            "category": "Clinical History",
            "field": "Symptom Duration",
            "value": "Several weeks of symptoms",
            "confidence": 0.8,
            "block_id": f"block_{len(_sessions[session_id]['interactions'])}",
        }

        # Update session
        _sessions[session_id]["interactions"].append(
            {"message": message, "response": response_text, "context": context}
        )
        _sessions[session_id]["discoveries"].append(discovery_event)

        return jsonify(
            {
                "response": response_text,
                "discovery_events": [discovery_event],
                "bias_warnings": [],
                "discovery_stats": {
                    "total": 20,  # Mock total
                    "discovered": len(_sessions[session_id]["discoveries"]),
                },
            }
        )

    except Exception as e:
        return jsonify({"error": f"Simulation processing failed: {str(e)}"}), 500


@bp.post("/simulation/submit_diagnosis")
def submit_diagnosis():
    """
    Submit final diagnosis and get performance evaluation.

    Request JSON:
        {
            "session_id": "string - Session identifier",
            "diagnosis": "string - Submitted diagnosis",
            "session_data": "object - Session statistics"
        }

    Response JSON:
        {
            "score": "string - Performance score",
            "feedback": "string - Detailed feedback",
            "performance_summary": "object - Breakdown by categories"
        }
    """
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    diagnosis = data.get("diagnosis", "")

    if not session_id:
        return jsonify({"error": "session_id is required"}), 400

    if session_id not in _sessions:
        return jsonify({"error": "Invalid session_id"}), 404

    try:
        session = _sessions[session_id]
        discovered_count = len(session["discoveries"])

        # Mock performance calculation
        discovery_score = min(
            100, (discovered_count / 15) * 100
        )  # Assuming 15 total items
        overall_score = int(discovery_score * 0.8 + 20)  # Basic scoring

        return jsonify(
            {
                "score": f"{overall_score}/100",
                "feedback": f"You discovered {discovered_count} clinical findings. Your submitted diagnosis: '{diagnosis}'",
                "performance_summary": {
                    "information_discovery": f"Good ({discovered_count}/15 items)",
                    "bias_awareness": "Excellent (0 warnings)",
                    "diagnostic_accuracy": "Requires expert review",
                },
            }
        )

    except Exception as e:
        return jsonify({"error": f"Evaluation failed: {str(e)}"}), 500


@bp.get("/simulation/<session_id>/status")
def simulation_status(session_id):
    """Get current status of a simulation session."""
    if session_id not in _sessions:
        return jsonify({"error": "Session not found"}), 404

    session = _sessions[session_id]
    return jsonify(
        {
            "session_id": session_id,
            "status": session["status"],
            "interactions_count": len(session["interactions"]),
            "discoveries_count": len(session["discoveries"]),
            "bias_warnings_count": len(session["bias_warnings"]),
        }
    )
