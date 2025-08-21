from flask import request, jsonify
from . import create_app
from smartdoc_core import reply_to

app = create_app()


@app.post("/chat")
def chat():
    """Chat endpoint for SmartDoc AI interaction."""
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    try:
        answer = reply_to(message)
        return jsonify({"reply": answer})
    except Exception as e:
        return jsonify({"error": f"AI processing failed: {str(e)}"}), 500


if __name__ == "__main__":
    # Development server
    app.run(debug=True, host="0.0.0.0", port=8000)
