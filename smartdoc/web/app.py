# app.py (Enhanced with configuration and error handling)

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from smartdoc.core.state_machine import DialogueState
from smartdoc.services.knowledge_manager import KnowledgeBaseManager
from smartdoc.core.intents import canonical_question_mappings
from smartdoc.services.llm_intent_classifier import LLMIntentClassifier  # <-- New LLM Intent Classifier
from smartdoc.core.dialogue_manager import DialogueManager
from smartdoc.utils.logger import SystemLogger
from smartdoc.services.nlg import NLGService  # <-- IMPORT THE NEW SERVICE
from smartdoc.utils.logger import sys_logger      # <-- Import the system logger singleton
from smartdoc.config.settings import config, SmartDocConfig
from smartdoc.utils.exceptions import SmartDocError, KnowledgeBaseError, NLUError, NLGError
from smartdoc.utils.session_logger import get_current_session, start_new_session  # <-- Add session logging
try:
    from smartdoc.web.virtual_patient import VirtualPatientManager  # <-- Add Virtual Patient Manager
except ImportError:
    VirtualPatientManager = None  # Virtual Patient is optional
import requests
import json
import os

# --- 1. Initialize the Flask App ---
import os
# Set template and static folder paths relative to project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app = Flask(__name__,
           template_folder=os.path.join(project_root, 'templates'),
           static_folder=os.path.join(project_root, 'static'))

# --- 2. Initialize All SmartDoc Components (ONCE at startup) ---
kb_manager = llm_intent_classifier = dm_manager = nlg_service = logger = None

def initialize_components():
    """Initialize all SmartDoc components with enhanced error handling."""
    global kb_manager, llm_intent_classifier, dm_manager, nlg_service, logger

    try:
        sys_logger.log_system("info", "Initializing SmartDoc Components for the Web App...")

        # Knowledge Base Manager
        sys_logger.log_system("info", f"Loading knowledge base from: {config.CASE_FILE}")
        kb_manager = KnowledgeBaseManager()
        if not kb_manager.is_loaded():
            raise KnowledgeBaseError("Could not load knowledge base.")

        # LLM Intent Classifier (with fallback mode)
        sys_logger.log_system("info", f"Initializing LLM Intent Classifier with model: {config.OLLAMA_MODEL}")
        llm_intent_classifier = LLMIntentClassifier()

        # Test the LLM connection with graceful fallback
        try:
            test_result = llm_intent_classifier.classify_intent("test connection")
            sys_logger.log_system("info", f"LLM Intent Classifier test successful: {test_result['intent_id']}")
        except Exception as llm_error:
            sys_logger.log_system("warning", f"LLM Intent Classifier test failed: {llm_error}")
            sys_logger.log_system("warning", "Continuing with fallback intent classification...")
            # Continue anyway - we'll handle LLM errors gracefully in classify_intent method

        # Initialize the NLG Service (with fallback)
        sys_logger.log_system("info", f"Initializing NLG with Ollama model: {config.OLLAMA_MODEL}")
        try:
            nlg_service = NLGService()
        except Exception as nlg_error:
            sys_logger.log_system("warning", f"NLG Service initialization failed: {nlg_error}")
            sys_logger.log_system("warning", "Continuing with fallback response generation...")
            nlg_service = None  # Will use fallback responses

        # Dialogue Manager (Pass BOTH kb_manager and nlg_service, handle None nlg_service)
        if nlg_service:
            dm_manager = DialogueManager(kb_manager=kb_manager, nlg_service=nlg_service)
        else:
            # Create a simple fallback dialogue manager
            from smartdoc.services.nlg import NLGService
            fallback_nlg = NLGService()
            fallback_nlg.is_initialized = False  # Mark as fallback
            dm_manager = DialogueManager(kb_manager=kb_manager, nlg_service=fallback_nlg)

        # System Logger for conversation logs
        logger = SystemLogger(logfile_path=config.CONVERSATION_LOG_FILE)

        sys_logger.log_system("info", "SmartDoc Components Initialized Successfully (with fallbacks if needed).")
        return True

    except Exception as e:
        sys_logger.log_system("critical", f"CRITICAL ERROR during initialization: {e}")
        # Return True anyway but log the error - we'll use fallback modes
        sys_logger.log_system("warning", "Continuing with fallback mode...")
        
        # Create minimal fallback components
        try:
            if not kb_manager:
                kb_manager = KnowledgeBaseManager()
            if not llm_intent_classifier:
                llm_intent_classifier = LLMIntentClassifier()
            if not dm_manager and kb_manager:
                from smartdoc.services.nlg import NLGService
                fallback_nlg = NLGService()
                fallback_nlg.is_initialized = False
                dm_manager = DialogueManager(kb_manager=kb_manager, nlg_service=fallback_nlg)
            if not logger:
                logger = SystemLogger(logfile_path=config.CONVERSATION_LOG_FILE)
            return True
        except Exception as fallback_error:
            sys_logger.log_system("critical", f"Even fallback initialization failed: {fallback_error}")
            return False

# Initialize components at startup
initialization_success = initialize_components()
if not initialization_success:
    sys_logger.log_system("warning", "SmartDoc initialization had issues but continuing with fallback mode.")
    # Components might be None or partially initialized, routes will handle this gracefully

# --- Routes remain the same, no changes needed below this line ---

@app.route("/")
def home():
    """Home route with enhanced error handling and session tracking."""
    if not dm_manager:
        error_msg = "SmartDoc application is not initialized. Please check the server logs."
        sys_logger.log_system("error", f"Home route accessed but system not initialized")
        return render_template("error.html", error_message=error_msg), 500

    try:
        # Start a new session for bias tracking
        session_logger = start_new_session()

        dm_manager.reset_state()
        initial_nlu_output = {
            "intent_id": "general_greet",
            "action_type": "generic_response_or_state_change",
            "target_details": {"response_key": "greeting_response"}
        }
        initial_bot_message = dm_manager.get_vsp_response(initial_nlu_output)

        # Log the initial interaction
        session_logger.log_interaction(
            intent_id="general_greet",
            user_query="[Session Start]",
            vsp_response=initial_bot_message,
            nlu_output=initial_nlu_output
        )

        if logger:
            logger.log_interaction("System: [Session Start]", initial_bot_message, dm_manager.get_current_state())

        return render_template("index.html", initial_bot_message=initial_bot_message)

    except Exception as e:
        sys_logger.log_system("error", f"Error in home route: {e}")
        return render_template("error.html", error_message="An error occurred starting the session."), 500

@app.route("/get")
def get_bot_response():
    """Get bot response route with enhanced error handling."""
    if not dm_manager or not llm_intent_classifier:
        # Try to reinitialize if components are missing
        sys_logger.log_system("warning", "Components not initialized, attempting re-initialization...")
        initialize_components()
        
        if not dm_manager or not llm_intent_classifier:
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
            response_text = "Session ended."
            if logger:
                logger.log_interaction(user_input, response_text, dm_manager.get_current_state())
            return jsonify({"response": response_text, "session_ended": True})

        # Process user input with LLM Intent Classifier (with fallback)
        try:
            intent_output = llm_intent_classifier.classify_intent(user_input)
        except Exception as intent_error:
            sys_logger.log_system("warning", f"Intent classification failed: {intent_error}")
            # Use fallback intent
            intent_output = {
                "intent_id": "clarification",
                "confidence": 0.3,
                "explanation": "Fallback due to classification error",
                "action_type": "generic_response_or_state_change",
                "target_details": {"response_key": "intent_not_understood"}
            }

        # Use the structured output from LLM Intent Classifier directly
        nlu_output = {
            "intent_id": intent_output["intent_id"],
            "confidence": intent_output["confidence"],
            "explanation": intent_output.get("explanation", ""),
            "action_type": intent_output.get("action_type", "generic_response_or_state_change"),
            "target_details": intent_output.get("target_details", {"response_key": "intent_not_understood"})
        }

        # Get VSP response (with fallback)
        try:
            vsp_response = dm_manager.get_vsp_response(nlu_output)
        except Exception as dm_error:
            sys_logger.log_system("warning", f"Dialogue manager error: {dm_error}")
            vsp_response = "I'm having trouble processing that right now. Could you rephrase your question?"

        # Get current session for bias tracking
        session_logger = get_current_session()

        # Log interaction with enhanced bias detection
        session_logger.log_interaction(
            intent_id=nlu_output.get("intent_id", "unknown"),
            user_query=user_input,
            vsp_response=vsp_response,
            nlu_output=nlu_output,
            dialogue_state=str(dm_manager.get_current_state()) if dm_manager else "UNKNOWN"
        )

        # Enhanced bias detection using the case data
        bias_warning = None
        try:
            from smartdoc.utils.bias_evaluator import BiasEvaluator
            if kb_manager and kb_manager.is_loaded():
                bias_evaluator = BiasEvaluator(kb_manager.get_case_data())
                session_interactions = session_logger.get_session_data()["interactions"]
                
                # Perform real-time bias check
                bias_check = bias_evaluator.check_real_time_bias(
                    session_interactions, 
                    nlu_output.get("intent_id"),
                    user_input,
                    vsp_response
                )
                
                if bias_check.get("detected"):
                    session_logger._add_bias_warning(
                        bias_check["bias_type"], 
                        bias_check["message"]
                    )
                    bias_warning = session_logger.get_latest_bias_warning()
        except Exception as bias_error:
            sys_logger.log_system("warning", f"Bias detection error: {bias_error}")

        # Check for bias warnings if not already set
        if not bias_warning:
            bias_warning = session_logger.get_latest_bias_warning()

        # Log interaction (existing logger)
        if logger:
            logger.log_interaction(
                user_input, vsp_response, dm_manager.get_current_state() if dm_manager else "UNKNOWN",
                nlu_output.get("intent_id"), nlu_output.get("confidence")
            )

        response_data = {
            "response": vsp_response,
            "error": False,
            "debug_info": {
                "intent_id": nlu_output.get("intent_id"),
                "confidence": nlu_output.get("confidence"),
                "dialogue_state": str(dm_manager.get_current_state()) if dm_manager else "UNKNOWN"
            } if config.FLASK_DEBUG else None
        }

        # Add bias warning if detected
        if bias_warning:
            response_data["bias_warning"] = {
                "type": bias_warning.get("bias_type"),
                "message": bias_warning.get("message"),
                "show": True
            }

        return jsonify(response_data)

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
        "status": "healthy" if all([kb_manager, llm_intent_classifier, dm_manager, nlg_service]) else "unhealthy",
        "components": {
            "knowledge_base": kb_manager is not None and kb_manager.is_loaded(),
            "llm_intent_classifier": llm_intent_classifier is not None,
            "dialogue_manager": dm_manager is not None,
            "nlg_service": nlg_service is not None and nlg_service.is_initialized
        },
        "config": {
            "case_file": config.CASE_FILE,
            "ollama_model": config.OLLAMA_MODEL
        }
    }

    status_code = 200 if status["status"] == "healthy" else 503
    return jsonify(status), status_code

@app.route("/bias_evaluation")
def get_bias_evaluation():
    """Get comprehensive bias evaluation for the current session."""
    try:
        session_logger = get_current_session()
        session_data = session_logger.get_session_data()
        
        # Initialize bias evaluator with case data
        from smartdoc.utils.bias_evaluator import BiasEvaluator
        bias_evaluator = BiasEvaluator(kb_manager.get_case_data())
        
        # Create simulated data for full evaluation
        revealed_blocks = set()  # This would be tracked in a real progressive disclosure scenario
        hypotheses = []  # Extract from session interactions
        final_diagnosis = "pending"  # Not yet submitted
        
        # Extract hypotheses from session interactions
        for interaction in session_data["interactions"]:
            if "diagnosis" in interaction.get("user_query", "").lower():
                hypotheses.append({
                    "diagnosis": interaction["user_query"],
                    "timestamp": interaction["timestamp"]
                })
        
        # Run comprehensive evaluation
        evaluation = bias_evaluator.evaluate_session(
            session_data["interactions"],
            revealed_blocks,
            hypotheses,
            final_diagnosis
        )
        
        # Generate feedback
        feedback = bias_evaluator.generate_feedback_report(evaluation)
        
        return jsonify({
            "evaluation": evaluation,
            "feedback": feedback,
            "session_summary": {
                "total_interactions": len(session_data["interactions"]),
                "detected_biases": session_data["detected_biases"],
                "current_state": session_data["current_state"]
            }
        })
        
    except Exception as e:
        sys_logger.log_system("error", f"Error in bias evaluation: {e}")
        return jsonify({"error": "Failed to generate bias evaluation"}), 500

# --- Virtual Patient Routes ---
vp_manager = None

@app.route("/vp")
def virtual_patient():
    """Virtual patient interface route."""
    global vp_manager
    
    # Initialize VP manager with case file
    case_file = os.path.join(project_root, 'data', 'cases', 'mull_diagnostic_error.json')
    if not os.path.exists(case_file):
        return render_template("error.html", error_message="Case file not found"), 404
    
    try:
        vp_manager = VirtualPatientManager(case_file)
        initial_presentation = vp_manager.get_initial_presentation()
        
        return render_template("virtual_patient.html", 
                             case_title=initial_presentation.get("caseTitle", "Virtual Patient"),
                             initial_presentation=initial_presentation)
    except Exception as e:
        sys_logger.log_system("error", f"Error initializing virtual patient: {e}")
        return render_template("error.html", error_message="Failed to load virtual patient"), 500

@app.route("/vp/blocks")
def get_blocks():
    """Get available information blocks."""
    global vp_manager
    if not vp_manager:
        return jsonify({"error": "Virtual patient not initialized"}), 400
    
    try:
        blocks = vp_manager.get_available_blocks()
        return jsonify({"blocks": blocks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/vp/reveal", methods=["POST"])
def reveal_block():
    """Reveal a specific information block."""
    global vp_manager
    if not vp_manager:
        return jsonify({"error": "Virtual patient not initialized"}), 400
    
    try:
        block_id = request.form.get("blockId")
        if not block_id:
            return jsonify({"error": "Block ID required"}), 400
        
        result = vp_manager.reveal_block(block_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/vp/hypothesis", methods=["POST"])
def add_hypothesis():
    """Add a working hypothesis."""
    global vp_manager
    if not vp_manager:
        return jsonify({"error": "Virtual patient not initialized"}), 400
    
    try:
        diagnosis = request.form.get("diagnosis")
        if not diagnosis:
            return jsonify({"error": "Diagnosis required"}), 400
        
        result = vp_manager.add_hypothesis(diagnosis)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/vp/submit", methods=["POST"])
def submit_diagnosis():
    """Submit final diagnosis."""
    global vp_manager
    if not vp_manager:
        return jsonify({"error": "Virtual patient not initialized"}), 400
    
    try:
        diagnosis = request.form.get("diagnosis")
        reasoning = request.form.get("reasoning", "")
        
        if not diagnosis:
            return jsonify({"error": "Diagnosis required"}), 400
        
        result = vp_manager.submit_final_diagnosis(diagnosis, reasoning)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/vp/bias-warnings")
def get_bias_warnings():
    """Get current bias warnings."""
    try:
        session_logger = get_current_session()
        latest_warning = session_logger.get_latest_bias_warning()
        
        if latest_warning:
            return jsonify({"warning": {
                "type": latest_warning.get("bias_type"),
                "message": latest_warning.get("message")
            }})
        else:
            return jsonify({"warning": None})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Admin Settings Routes ---
@app.route("/admin/settings", methods=["GET", "POST"])
def admin_settings():
    """Admin settings page for managing Ollama configuration."""
    if request.method == "GET":
        # Check Ollama status
        ollama_status = False
        try:
            response = requests.head(config.OLLAMA_BASE_URL, timeout=5)
            ollama_status = response.status_code == 200
        except:
            ollama_status = False
        
        return render_template("admin_settings.html", 
                             current_config=config,
                             ollama_status=ollama_status)
    
    elif request.method == "POST":
        try:
            # Get form data
            new_base_url = request.form.get("ollama_base_url", "").strip()
            new_model = request.form.get("ollama_model", "").strip()
            new_max_tokens = int(request.form.get("nlg_max_tokens", config.NLG_MAX_TOKENS))
            new_temperature = float(request.form.get("nlg_temperature", config.NLG_TEMPERATURE))
            
            # Validate inputs
            if not new_base_url or not new_model:
                return render_template("admin_settings.html",
                                     current_config=config,
                                     ollama_status=False,
                                     message="Base URL and Model are required",
                                     message_type="error")
            
            if not (0.0 <= new_temperature <= 2.0):
                return render_template("admin_settings.html",
                                     current_config=config,
                                     ollama_status=False,
                                     message="Temperature must be between 0.0 and 2.0",
                                     message_type="error")
            
            if not (1 <= new_max_tokens <= 4096):
                return render_template("admin_settings.html",
                                     current_config=config,
                                     ollama_status=False,
                                     message="Max tokens must be between 1 and 4096",
                                     message_type="error")
            
            # Test connection before applying changes
            try:
                test_response = requests.head(new_base_url, timeout=5)
                if test_response.status_code != 200:
                    raise Exception(f"Server returned status code: {test_response.status_code}")
            except Exception as e:
                return render_template("admin_settings.html",
                                     current_config=config,
                                     ollama_status=False,
                                     message=f"Cannot connect to Ollama server: {e}",
                                     message_type="error")
            
            # Update global config (for session)
            config.OLLAMA_BASE_URL = new_base_url
            config.OLLAMA_MODEL = new_model
            config.NLG_MAX_TOKENS = new_max_tokens
            config.NLG_TEMPERATURE = new_temperature
            
            # Reinitialize NLG service with new settings
            global nlg_service
            try:
                nlg_service = NLGService(new_model, new_base_url)
                if nlg_service.is_initialized:
                    success_message = "Settings updated successfully! NLG service reinitialized."
                    message_type = "success"
                else:
                    success_message = "Settings updated, but NLG service failed to initialize. Check the model name."
                    message_type = "warning"
            except Exception as e:
                success_message = f"Settings updated, but NLG service failed to reinitialize: {e}"
                message_type = "warning"
            
            sys_logger.log_system("info", f"Admin updated Ollama settings: {new_model} at {new_base_url}")
            
            return render_template("admin_settings.html",
                                 current_config=config,
                                 ollama_status=True,
                                 message=success_message,
                                 message_type=message_type)
                                 
        except ValueError as e:
            return render_template("admin_settings.html",
                                 current_config=config,
                                 ollama_status=False,
                                 message="Invalid input format",
                                 message_type="error")
        except Exception as e:
            sys_logger.log_system("error", f"Error updating admin settings: {e}")
            return render_template("admin_settings.html",
                                 current_config=config,
                                 ollama_status=False,
                                 message="An error occurred while updating settings",
                                 message_type="error")

@app.route("/admin/test-connection", methods=["POST"])
def test_ollama_connection():
    """Test connection to Ollama server and model."""
    try:
        data = request.get_json()
        base_url = data.get("ollama_base_url", config.OLLAMA_BASE_URL)
        model_name = data.get("ollama_model", config.OLLAMA_MODEL)
        
        # Test server connection
        try:
            response = requests.head(base_url, timeout=5)
            if response.status_code != 200:
                return jsonify({
                    "success": False,
                    "error": f"Server returned status code: {response.status_code}"
                })
        except requests.ConnectionError:
            return jsonify({
                "success": False,
                "error": "Cannot connect to Ollama server. Make sure it's running."
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Connection error: {str(e)}"
            })
        
        # Test model with a simple request
        try:
            chat_endpoint = f"{base_url}/api/chat"
            test_payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": "Hello"}],
                "stream": False,
                "options": {
                    "num_predict": 10,
                    "temperature": 0.1
                }
            }
            
            response = requests.post(chat_endpoint, json=test_payload, timeout=30)
            if response.status_code == 200:
                return jsonify({
                    "success": True,
                    "message": "Connection and model test successful"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": f"Model test failed with status {response.status_code}: {response.text}"
                })
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Model test failed: {str(e)}"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Test failed: {str(e)}"
        })

@app.route("/admin/list-models", methods=["POST"])
def list_ollama_models():
    """List available models from Ollama server."""
    try:
        data = request.get_json()
        base_url = data.get("ollama_base_url", config.OLLAMA_BASE_URL)
        
        # Get list of models
        try:
            models_endpoint = f"{base_url}/api/tags"
            response = requests.get(models_endpoint, timeout=10)
            
            if response.status_code == 200:
                models_data = response.json()
                models = models_data.get("models", [])
                
                # Format models for display
                formatted_models = []
                for model in models:
                    formatted_models.append({
                        "name": model.get("name", "Unknown"),
                        "size": _format_bytes(model.get("size", 0)),
                        "modified_at": model.get("modified_at", "Unknown")
                    })
                
                return jsonify({
                    "success": True,
                    "models": formatted_models
                })
            else:
                return jsonify({
                    "success": False,
                    "error": f"Failed to get models: HTTP {response.status_code}"
                })
                
        except requests.ConnectionError:
            return jsonify({
                "success": False,
                "error": "Cannot connect to Ollama server"
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Error listing models: {str(e)}"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Request failed: {str(e)}"
        })

def _format_bytes(bytes_size):
    """Format bytes size to human readable format."""
    if bytes_size == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes_size >= 1024 and i < len(size_names) - 1:
        bytes_size /= 1024
        i += 1
    
    return f"{bytes_size:.1f} {size_names[i]}"

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
    print(f"Virtual Patient available at: http://{config.FLASK_HOST}:{config.FLASK_PORT}/vp")

    # Final check before starting server
    if not all([kb_manager, llm_intent_classifier, dm_manager, nlg_service]):
        print("WARNING: Some components failed to initialize. Server will start but may not function correctly.")
        print("Check the system logs for details.")

    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )
