# app.py (Enhanced with configuration and error handling)

from flask import Flask, render_template, request, jsonify
from smartdoc.core.state_machine import DialogueState
from smartdoc.services.knowledge_manager import KnowledgeBaseManager
from smartdoc.core.intents import canonical_question_mappings
from smartdoc.services.nlu import NLUService
from smartdoc.core.dialogue_manager import DialogueManager
from smartdoc.utils.logger import SystemLogger
from smartdoc.services.nlg import NLGService  # <-- IMPORT THE NEW SERVICE
from smartdoc.utils.logger import sys_logger      # <-- Import the system logger singleton
from smartdoc.config.settings import config
from smartdoc.utils.exceptions import SmartDocError, KnowledgeBaseError, NLUError, NLGError

# --- 1. Initialize the Flask App ---
import os
# Set template and static folder paths relative to project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app = Flask(__name__, 
           template_folder=os.path.join(project_root, 'templates'),
           static_folder=os.path.join(project_root, 'static'))

# --- 2. Initialize All SmartDoc Components (ONCE at startup) ---
kb_manager = nlu_service = dm_manager = nlg_service = logger = None

def initialize_components():
    """Initialize all SmartDoc components with enhanced error handling."""
    global kb_manager, nlu_service, dm_manager, nlg_service, logger

    try:
        sys_logger.log_system("info", "Initializing SmartDoc Components for the Web App...")

        # Knowledge Base Manager
        sys_logger.log_system("info", f"Loading knowledge base from: {config.CASE_FILE}")
        kb_manager = KnowledgeBaseManager()
        if not kb_manager.is_loaded():
            raise KnowledgeBaseError("Could not load knowledge base.")

        # NLU Service
        sys_logger.log_system("info", f"Initializing NLU with model: {config.SBERT_MODEL}")
        nlu_service = NLUService(mappings_data=canonical_question_mappings)

        # Initialize the NLG Service
        sys_logger.log_system("info", f"Initializing NLG with Ollama model: {config.OLLAMA_MODEL}")
        nlg_service = NLGService()

        # Dialogue Manager (Pass BOTH kb_manager and nlg_service)
        dm_manager = DialogueManager(kb_manager=kb_manager, nlg_service=nlg_service)

        # System Logger for conversation logs
        logger = SystemLogger(logfile_path=config.CONVERSATION_LOG_FILE)

        sys_logger.log_system("info", "SmartDoc Components Initialized Successfully.")
        return True

    except (KnowledgeBaseError, NLUError, NLGError) as e:
        sys_logger.log_system("critical", f"Component initialization failed: {e}")
        return False
    except Exception as e:
        sys_logger.log_system("critical", f"CRITICAL ERROR during initialization: {e}")
        return False

# Initialize components at startup
if not initialize_components():
    sys_logger.log_system("critical", "SmartDoc failed to initialize. Check logs for details.")
    # Components will be None, routes will handle this gracefully

# --- Routes remain the same, no changes needed below this line ---

@app.route("/")
def home():
    """Home route with enhanced error handling."""
    if not dm_manager:
        error_msg = "SmartDoc application is not initialized. Please check the server logs."
        sys_logger.log_system("error", f"Home route accessed but system not initialized")
        return render_template("error.html", error_message=error_msg), 500

    try:
        dm_manager.reset_state()
        initial_nlu_output = {
            "intent_id": "general_greet",
            "action_type": "generic_response_or_state_change",
            "target_details": {"response_key": "greeting_response"}
        }
        initial_bot_message = dm_manager.get_vsp_response(initial_nlu_output)

        if logger:
            logger.log_interaction("System: [Session Start]", initial_bot_message, dm_manager.get_current_state())

        return render_template("index.html", initial_bot_message=initial_bot_message)

    except Exception as e:
        sys_logger.log_system("error", f"Error in home route: {e}")
        return render_template("error.html", error_message="An error occurred starting the session."), 500

@app.route("/get")
def get_bot_response():
    """Get bot response route with enhanced error handling."""
    if not dm_manager or not nlu_service:
        return jsonify({
            "response": "Error: SmartDoc is not initialized.",
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
            response_text = "Session ended."
            if logger:
                logger.log_interaction(user_input, response_text, dm_manager.get_current_state())
            return jsonify({"response": response_text, "session_ended": True})

        # Process user input
        nlu_output = nlu_service.process_input(user_input)
        vsp_response = dm_manager.get_vsp_response(nlu_output)

        # Log interaction
        if logger:
            logger.log_interaction(
                user_input, vsp_response, dm_manager.get_current_state(),
                nlu_output.get("intent_id"), nlu_output.get("score")
            )

        return jsonify({
            "response": vsp_response,
            "error": False,
            "debug_info": {
                "intent_id": nlu_output.get("intent_id"),
                "confidence": nlu_output.get("score"),
                "dialogue_state": str(dm_manager.get_current_state())
            } if config.FLASK_DEBUG else None
        })

    except Exception as e:
        sys_logger.log_system("error", f"Error processing user input: {e}")
        return jsonify({
            "response": "I'm having trouble processing your request right now. Please try again.",
            "error": True
        })

@app.route("/health")
def health_check():
    """Health check endpoint for monitoring."""
    status = {
        "status": "healthy" if all([kb_manager, nlu_service, dm_manager, nlg_service]) else "unhealthy",
        "components": {
            "knowledge_base": kb_manager is not None and kb_manager.is_loaded(),
            "nlu_service": nlu_service is not None,
            "dialogue_manager": dm_manager is not None,
            "nlg_service": nlg_service is not None and nlg_service.is_initialized
        },
        "config": {
            "case_file": config.CASE_FILE,
            "sbert_model": config.SBERT_MODEL,
            "ollama_model": config.OLLAMA_MODEL
        }
    }

    status_code = 200 if status["status"] == "healthy" else 503
    return jsonify(status), status_code

@app.errorhandler(404)
def not_found(error):
    """Custom 404 handler."""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 handler."""
    sys_logger.log_system("error", f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("Starting Flask web server...")
    print(f"Open your browser and go to http://{config.FLASK_HOST}:{config.FLASK_PORT}")

    # Final check before starting server
    if not all([kb_manager, nlu_service, dm_manager, nlg_service]):
        print("WARNING: Some components failed to initialize. Server will start but may not function correctly.")
        print("Check the system logs for details.")

    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )
