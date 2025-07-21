# SmartDoc Virtual Patient Web Application

from flask import Flask, render_template, request, jsonify
from smartdoc.ai.intent_classifier import LLMIntentClassifier
from smartdoc.simulation.engine import IntentDrivenDisclosureManager
from smartdoc.utils.logger import sys_logger
from smartdoc.config.settings import config
from smartdoc.utils.exceptions import SmartDocError
from smartdoc.simulation.session_tracker import get_current_session, start_new_session
import uuid
import os

# Set template and static folder paths within web module
web_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__,
            template_folder=os.path.join(web_dir, 'templates'),
            static_folder=os.path.join(web_dir, 'static'))

app.secret_key = config.SECRET_KEY

# Global components
llm_intent_classifier = intent_driven_manager = None

def initialize_components():
    """Initialize SmartDoc components (simplified for intent-driven discovery only)."""
    global llm_intent_classifier, intent_driven_manager

    try:
        sys_logger.log_system("info", "Initializing SmartDoc Components (Intent-Driven Discovery)...")

        # LLM Intent Classifier
        sys_logger.log_system("info", f"Initializing LLM Intent Classifier with model: {config.OLLAMA_MODEL}")
        llm_intent_classifier = LLMIntentClassifier()

        # Intent-Driven Disclosure Manager
        sys_logger.log_system("info", "Initializing Intent-Driven Disclosure Manager...")
        intent_driven_manager = IntentDrivenDisclosureManager(
            case_file_path='/Users/bruno.sena/Projects/personal/masters/smart-doc/data/cases/intent_driven_case.json'
        )

        # Test the LLM connection
        try:
            test_result = llm_intent_classifier.classify_intent("test connection")
            sys_logger.log_system("info", f"LLM Intent Classifier test successful: {test_result['intent_id']}")
        except Exception as llm_error:
            sys_logger.log_system("warning", f"LLM Intent Classifier test failed: {llm_error}")
            sys_logger.log_system("warning", "Continuing with fallback intent classification...")

        sys_logger.log_system("info", "SmartDoc Components Initialized Successfully.")
        return True

    except Exception as e:
        sys_logger.log_system("critical", f"CRITICAL ERROR during initialization: {e}")
        return False

# Initialize components at startup
initialization_success = initialize_components()
if not initialization_success:
    sys_logger.log_system("warning", "SmartDoc initialization had issues.")

@app.route("/")
def home():
    """Home route for intent-driven discovery."""
    if not intent_driven_manager:
        error_msg = "SmartDoc application is not initialized. Please check the server logs."
        sys_logger.log_system("error", f"Home route accessed but system not initialized")
        return render_template("error.html", error_message=error_msg), 500

    try:
        # Start a new session for bias tracking
        session_logger = start_new_session()

        initial_bot_message = "Hello! I'm here to help with this clinical simulation. What would you like to know about the patient?"

        # Log the initial interaction
        session_logger.log_interaction(
            intent_id="general_greet",
            user_query="[Session Start]",
            vsp_response=initial_bot_message,
            nlu_output={"intent_id": "general_greet", "confidence": 1.0}
        )

        return render_template("index.html", initial_bot_message=initial_bot_message)

    except Exception as e:
        sys_logger.log_system("error", f"Error in home route: {e}")
        return render_template("error.html", error_message="An error occurred starting the session."), 500

@app.route("/get")
def get_bot_response():
    """Get bot response using intent-driven discovery."""
    if not intent_driven_manager or not llm_intent_classifier:
        return jsonify({
            "response": "The system is starting up. Please try again in a moment.",
            "error": True
        })

    try:
        user_input = request.args.get('msg', '').strip()

        if not user_input:
            return jsonify({
                "response": "I didn't receive any input. Could you please ask a question?",
                "error": False
            })

        if user_input.lower() == "quit":
            return jsonify({"response": "Session ended.", "session_ended": True})

        # Process user input with Intent-Driven Discovery
        session_id = request.args.get('session_id', f"web_session_{uuid.uuid4().hex[:8]}")

        try:
            discovery_result = intent_driven_manager.process_doctor_query(session_id, user_input)

            if discovery_result['success']:
                response_data = {
                    "response": discovery_result['response']['text'],
                    "has_discoveries": discovery_result['response']['has_discoveries'],
                    "discoveries": discovery_result['response']['discoveries'],
                    "discovery_count": discovery_result['response']['discovery_count'],
                    "session_id": session_id
                }

                # Add discovery stats if available
                if 'discovery_stats' in discovery_result:
                    response_data["discovery_stats"] = discovery_result['discovery_stats']

                # Get current session for bias tracking
                session_logger = get_current_session()
                session_logger.log_interaction(
                    intent_id=discovery_result['intent_classification']['intent_id'],
                    user_query=user_input,
                    vsp_response=discovery_result['response']['text'],
                    nlu_output=discovery_result['intent_classification']
                )

                sys_logger.log_system("info", f"Intent-driven discovery successful: {len(discovery_result['discovery_result']['discovered_blocks'])} blocks discovered")
                return jsonify(response_data)
            else:
                return jsonify({
                    "response": "I'm having trouble processing that right now. Could you rephrase your question?",
                    "error": True
                })

        except Exception as discovery_error:
            sys_logger.log_system("error", f"Intent-driven discovery failed: {discovery_error}")
            return jsonify({
                "response": "I'm having trouble processing that right now. Could you rephrase your question?",
                "error": True
            })

    except Exception as e:
        sys_logger.log_system("error", f"Error in get_bot_response: {e}")
        return jsonify({
            "response": "An unexpected error occurred. Please try again.",
            "error": True
        })

# Intent-Driven Discovery API Endpoints

@app.route("/api/discovery/start", methods=["POST"])
def start_discovery_session():
    """Start a new intent-driven discovery session."""
    if not intent_driven_manager:
        return jsonify({"error": "Intent-driven discovery not available"}), 503

    try:
        session_id = intent_driven_manager.start_intent_driven_session()
        return jsonify({
            "session_id": session_id,
            "message": "Discovery session started successfully"
        })
    except Exception as e:
        sys_logger.log_system("error", f"Error starting discovery session: {e}")
        return jsonify({"error": "Failed to start session"}), 500

@app.route("/api/discovery/stats/<session_id>")
def get_discovery_stats(session_id):
    """Get discovery statistics for a session."""
    if not intent_driven_manager:
        return jsonify({"error": "Intent-driven discovery not available"}), 503

    try:
        stats = intent_driven_manager._get_session_discovery_stats(session_id)
        return jsonify(stats)
    except Exception as e:
        sys_logger.log_system("error", f"Error getting discovery stats: {e}")
        return jsonify({"error": "Failed to get stats"}), 500

@app.route("/api/discovery/discoveries/<session_id>")
def get_session_discoveries(session_id):
    """Get all discoveries for a session."""
    if not intent_driven_manager:
        return jsonify({"error": "Intent-driven discovery not available"}), 503

    try:
        result = intent_driven_manager.get_session_discoveries(session_id)
        return jsonify(result)
    except Exception as e:
        sys_logger.log_system("error", f"Error getting session discoveries: {e}")
        return jsonify({"error": "Failed to get discoveries"}), 500

@app.route("/api/discovery/info/<session_id>")
def get_available_info(session_id):
    """Get available information summary for a session."""
    if not intent_driven_manager:
        return jsonify({"error": "Intent-driven discovery not available"}), 503

    try:
        result = intent_driven_manager.get_available_information_summary(session_id)
        return jsonify(result)
    except Exception as e:
        sys_logger.log_system("error", f"Error getting available info: {e}")
        return jsonify({"error": "Failed to get info"}), 500

@app.route("/test", methods=["GET", "POST"])
def test_discovery():
    """Test endpoint for intent-driven discovery."""
    if not intent_driven_manager:
        return jsonify({"error": "Intent-driven discovery not available"}), 503

    try:
        query = request.args.get('query', 'What brings you here today?')
        session_id = request.args.get('session_id')

        if not session_id:
            session_id = intent_driven_manager.start_intent_driven_session()

        result = intent_driven_manager.process_doctor_query(session_id, query)
        return jsonify(result)

    except Exception as e:
        sys_logger.log_system("error", f"Error in test discovery: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/bias_evaluation")
def bias_evaluation():
    """Comprehensive bias evaluation endpoint for testing."""
    try:
        # Simple bias evaluation response for testing
        evaluation_result = {
            "success": True,
            "evaluation": {
                "overall_score": 75,
                "anchoring_bias": {
                    "detected": False,
                    "reason": "No evidence of premature fixation on initial diagnosis",
                    "score": 25
                },
                "confirmation_bias": {
                    "detected": False,
                    "reason": "Doctor explored multiple avenues of inquiry",
                    "score": 30
                },
                "premature_closure": {
                    "detected": False,
                    "reason": "Adequate information gathering before diagnosis",
                    "score": 20
                }
            },
            "recommendations": [
                "Continue comprehensive history taking",
                "Consider alternative diagnoses",
                "Gather more objective data before concluding"
            ]
        }

        return jsonify(evaluation_result)

    except Exception as e:
        sys_logger.log_system("error", f"Error in bias evaluation: {e}")
        return jsonify({"error": "Failed to evaluate bias"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template("error.html", error_message="Page not found."), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    sys_logger.log_system("error", f"Internal server error: {error}")
    return render_template("error.html", error_message="Internal server error."), 500

if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, host=config.FLASK_HOST, port=config.FLASK_PORT)
