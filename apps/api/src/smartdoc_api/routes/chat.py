"""
Chat API Routes

Handles basic chat interactions with the SmartDoc AI system.
"""

from flask import request, jsonify
from . import bp
import uuid

# Import SmartDoc core functionality
try:
    from smartdoc_core import reply_to
    SMARTDOC_AVAILABLE = True
except ImportError:
    SMARTDOC_AVAILABLE = False
    def reply_to(message: str) -> str:
        """Fallback response generator."""
        return f"SmartDoc AI: Thank you for your question: '{message}'. I'm here to help with your clinical simulation."

@bp.post("/chat")
def chat():
    """
    Process a chat message and return AI response.

    Request JSON:
        {
            "message": "string - User's message"
        }

    Response JSON:
        {
            "reply": "string - AI response"
        }

    Error Response:
        {
            "error": "string - Error description"
        }
    """
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    try:
        reply = reply_to(message)
        return jsonify({
            "reply": reply,
            "smartdoc_core_available": SMARTDOC_AVAILABLE
        })
    except Exception as e:
        return jsonify({"error": f"AI processing failed: {str(e)}"}), 500@bp.get("/chat/health")
def chat_health():
    """Health check for chat functionality."""
    return jsonify({"status": "ok", "endpoint": "chat"})
