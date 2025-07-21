# SmartDoc Virtual Patient Web Application

from flask import Flask, render_template, request, jsonify
from smartdoc.ai.intent_classifier import LLMIntentClassifier
from smartdoc.ai.clinical_evaluator import ClinicalEvaluator
from smartdoc.simulation.engine import IntentDrivenDisclosureManager
from smartdoc.utils.logger import sys_logger
from smartdoc.config.settings import config
from smartdoc.utils.exceptions import SmartDocError
from smartdoc.simulation.session_tracker import get_current_session, start_new_session
import uuid
import os

# Set template and static folder paths
web_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(web_dir))  # Go up two levels from smartdoc/web/
app = Flask(__name__,
            template_folder=os.path.join(web_dir, 'templates'),
            static_folder=os.path.join(project_root, 'static'))

app.secret_key = config.SECRET_KEY

# Global components
llm_intent_classifier = intent_driven_manager = clinical_evaluator = None

def initialize_components():
    """Initialize SmartDoc components (simplified for intent-driven discovery only)."""
    global llm_intent_classifier, intent_driven_manager, clinical_evaluator

    try:
        sys_logger.log_system("info", "Initializing SmartDoc Components (Intent-Driven Discovery)...")

        # LLM Intent Classifier
        sys_logger.log_system("info", f"Initializing LLM Intent Classifier with model: {config.OLLAMA_MODEL}")
        llm_intent_classifier = LLMIntentClassifier()

        # Clinical Evaluator
        sys_logger.log_system("info", "Initializing Clinical Evaluator...")
        clinical_evaluator = ClinicalEvaluator()

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

        initial_bot_message = "Hello! I'm the son of the patient, my mother doesn't speak english so I'm here to answer your questions. What would you like to know doctor?"

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

@app.route("/get_bot_response", methods=["POST"])
def get_bot_response():
    """Get bot response using intent-driven discovery."""
    if not intent_driven_manager or not llm_intent_classifier:
        return jsonify({
            "response": "The system is starting up. Please try again in a moment.",
            "error": True
        })

    try:
        # Get JSON data from POST request
        data = request.get_json()
        user_input = data.get('message', '').strip() if data else ''

        if not user_input:
            return jsonify({
                "response": "I didn't receive any input. Could you please ask a question?",
                "error": False
            })

        if user_input.lower() == "quit":
            return jsonify({"response": "Session ended.", "session_ended": True})

        # Process user input with Intent-Driven Discovery
        session_id = data.get('session_id', f"web_session_{uuid.uuid4().hex[:8]}") if data else f"web_session_{uuid.uuid4().hex[:8]}"

        try:
            discovery_result = intent_driven_manager.process_doctor_query(session_id, user_input)

            if discovery_result['success']:
                response_data = {
                    "response": discovery_result['response']['text'],
                    "discovery_events": [],
                    "discovery_stats": {},
                    "bias_warnings": []
                }

                # Process discoveries into events for the frontend
                if 'discoveries' in discovery_result['response'] and discovery_result['response']['discoveries']:
                    discovery_events = []
                    for discovery in discovery_result['response']['discoveries']:
                        # Use the structured discovery data from LLM Discovery Processor
                        discovery_events.append({
                            "category": discovery['category'],
                            "field": discovery['label'],  # Fixed label as key to prevent duplication
                            "value": discovery['summary'],  # Clean clinical summary
                            "confidence": discovery.get('confidence', 1.0),
                            "block_id": discovery['block_id']
                        })
                    response_data["discovery_events"] = discovery_events

                # Add discovery stats
                if 'discovery_stats' in discovery_result:
                    response_data["discovery_stats"] = discovery_result['discovery_stats']

                # Get current session for bias tracking
                session_logger = get_current_session()
                if session_logger:
                    # Log the interaction first so bias detection can run
                    session_logger.log_interaction(
                        intent_id=discovery_result['intent_classification']['intent_id'],
                        user_query=user_input,
                        vsp_response=discovery_result['response']['text'],
                        nlu_output=discovery_result['intent_classification']
                    )

                    # Check for new bias warnings from the session tracker
                    latest_bias = session_logger.get_latest_bias_warning()
                    if latest_bias and latest_bias.get('interaction_count') == len(session_logger.get_interactions()):
                        # This is a new bias warning from the current interaction
                        bias_warning = {
                            "bias_type": latest_bias.get('bias_type'),
                            "description": latest_bias.get('message')
                        }
                        response_data["bias_warnings"].append(bias_warning)
                        sys_logger.log_system("warning", f"Session tracker bias warning: {latest_bias.get('bias_type')}")

                # Add bias warning from discovery result if detected
                if 'bias_warning' in discovery_result:
                    response_data["bias_warnings"].append(discovery_result['bias_warning'])
                    sys_logger.log_system("warning", f"Discovery bias warning sent to frontend: {discovery_result['bias_warning']['bias_type']}")

                # Add discovery count and total for progress tracking
                if 'discovery_result' in discovery_result:
                    discovery_data = discovery_result['discovery_result']
                    total_blocks = len(discovery_data.get('case_data', {}).get('content_blocks', []))
                    discovered_blocks = len(discovery_data.get('discovered_blocks', []))

                    response_data["discovery_stats"] = {
                        "total": total_blocks,
                        "discovered": discovered_blocks
                    }

                sys_logger.log_system("info", f"Intent-driven discovery successful: {len(discovery_result.get('discovery_result', {}).get('discovered_blocks', []))} blocks discovered")
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

@app.route("/get")
def get_bot_response_legacy():
    """Legacy GET endpoint for compatibility."""
    return jsonify({
        "response": "Please use the new interface. This endpoint is deprecated.",
        "error": False
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
    """Comprehensive bias evaluation endpoint using real session data."""
    try:
        # Get the most recent session data
        session_logger = get_current_session()
        session_data = session_logger.get_session_data()

        # Use the bias analyzer from the intent-driven manager
        if intent_driven_manager and intent_driven_manager.bias_analyzer:
            # Convert session interactions to the format expected by bias analyzer
            interactions = session_data.get('interactions', [])
            revealed_blocks = set()  # You'd need to get this from the progressive disclosure session
            hypotheses = []  # You'd need to track hypotheses
            final_diagnosis = ""  # You'd get this from session data

            # Run comprehensive bias evaluation
            evaluation = intent_driven_manager.bias_analyzer.evaluate_session(
                session_log=interactions,
                revealed_blocks=revealed_blocks,
                hypotheses=hypotheses,
                final_diagnosis=final_diagnosis
            )

            # Get bias summary from session tracker
            bias_summary = session_logger.get_bias_summary()

            return jsonify({
                "success": True,
                "evaluation": evaluation,
                "session_summary": bias_summary,
                "session_id": session_data.get('session_id'),
                "total_interactions": len(interactions)
            })
        else:
            # Fallback to static response if bias analyzer not available
            return jsonify({
                "success": True,
                "evaluation": {
                    "overall_score": 0,
                    "anchoring_bias": {"detected": False, "reason": "Bias analyzer not available"},
                    "confirmation_bias": {"detected": False, "reason": "Bias analyzer not available"},
                    "premature_closure": {"detected": False, "reason": "Bias analyzer not available"}
                },
                "message": "Bias analyzer not available - using fallback"
            })

    except Exception as e:
        sys_logger.log_system("error", f"Error in bias evaluation: {e}")
        return jsonify({"error": f"Failed to evaluate bias: {str(e)}"}), 500

@app.route('/submit_diagnosis', methods=['POST'])
def submit_diagnosis():
    """Handle diagnosis submission and return performance analysis."""
    try:
        data = request.get_json()
        diagnosis = data.get('diagnosis', '')
        session_data = data.get('session_data', {})

        # Get current session from session tracker
        current_session = get_current_session()

        # Calculate performance metrics
        discovered_count = session_data.get('discovered_count', 0)
        total_available = session_data.get('total_available', 1)
        bias_warnings = session_data.get('bias_warnings', 0)

        # Calculate scores
        discovery_percentage = (discovered_count / total_available) * 100 if total_available > 0 else 0
        bias_score = max(0, 100 - (bias_warnings * 10))  # Deduct 10 points per bias warning

        # Overall score calculation
        overall_score = round((discovery_percentage * 0.6) + (bias_score * 0.4))

        # Generate performance feedback
        discovery_rating = "Excellent" if discovery_percentage >= 80 else \
                          "Good" if discovery_percentage >= 60 else \
                          "Fair" if discovery_percentage >= 40 else "Needs Improvement"

        bias_rating = "Excellent" if bias_warnings == 0 else \
                     "Good" if bias_warnings <= 2 else \
                     "Fair" if bias_warnings <= 4 else "Needs Improvement"

        # Generate feedback text
        feedback_parts = []

        if discovery_percentage >= 80:
            feedback_parts.append("You demonstrated excellent information gathering skills, discovering most of the available clinical information.")
        elif discovery_percentage >= 60:
            feedback_parts.append("You gathered a good amount of clinical information, but there may be additional details that could inform your diagnosis.")
        else:
            feedback_parts.append("Consider asking more comprehensive questions to gather additional clinical information before making a diagnosis.")

        if bias_warnings == 0:
            feedback_parts.append("You showed excellent clinical reasoning without triggering cognitive bias warnings.")
        elif bias_warnings <= 2:
            feedback_parts.append("You demonstrated good clinical reasoning with minimal bias concerns.")
        else:
            feedback_parts.append("Be mindful of potential cognitive biases that may affect your clinical reasoning.")

        feedback_parts.append(f"Your submitted diagnosis: \"{diagnosis}\"")

        performance_data = {
            "score": f"{overall_score}/100",
            "feedback": " ".join(feedback_parts),
            "performance_summary": {
                "information_discovery": f"{discovery_rating} ({discovered_count}/{total_available} items)",
                "bias_awareness": f"{bias_rating} ({bias_warnings} warnings)",
                "diagnostic_accuracy": "Requires expert review"
            }
        }

        # Log the diagnosis submission
        if current_session:
            sys_logger.log_system("info", f"Diagnosis submitted for session {current_session.get('session_id', 'unknown')}: {diagnosis}")

        return jsonify(performance_data)

    except Exception as e:
        sys_logger.log_system("error", f"Error in diagnosis submission: {e}")
        return jsonify({
            "score": "Error",
            "feedback": "An error occurred while processing your diagnosis. Please try again.",
            "performance_summary": {
                "information_discovery": "N/A",
                "bias_awareness": "N/A",
                "diagnostic_accuracy": "N/A"
            }
        }), 500

@app.route('/submit_diagnosis_with_reflection', methods=['POST'])
def submit_diagnosis_with_reflection():
    """Handle diagnosis submission with metacognitive reflection and advanced LLM evaluation."""
    try:
        data = request.get_json()
        diagnosis = data.get('diagnosis', '')
        metacognitive_responses = data.get('metacognitive_responses', {})
        session_data = data.get('session_data', {})

        # Get current session from session tracker
        current_session = get_current_session()

        if not current_session:
            return jsonify({
                "error": "No active session found",
                "score": "N/A",
                "feedback": "Session error occurred. Please try again."
            }), 400

        # Get dialogue transcript from session
        session_interactions = current_session.get_interactions()
        dialogue_transcript = []

        for interaction in session_interactions:
            # Add user query
            dialogue_transcript.append({
                "role": "user",
                "message": interaction.get('user_query', ''),
                "timestamp": interaction.get('timestamp', '')
            })
            # Add bot response
            dialogue_transcript.append({
                "role": "assistant",
                "message": interaction.get('vsp_response', ''),
                "timestamp": interaction.get('timestamp', '')
            })

        # Get detected biases from session
        bias_summary = current_session.get_bias_summary()
        detected_biases = []

        if bias_summary and 'bias_warnings' in bias_summary:
            for bias_warning in bias_summary['bias_warnings']:
                detected_biases.append({
                    "bias_type": bias_warning.get('bias_type', 'Unknown'),
                    "description": bias_warning.get('message', ''),
                    "interaction_count": bias_warning.get('interaction_count', 0)
                })

        # Case context for evaluation
        case_context = {
            "case_type": "Inflammatory Bowel Disease - Crohn's Disease",
            "correct_diagnosis": "Crohn's Disease with potential complications",
            "key_features": "Chronic diarrhea, abdominal pain, weight loss, family history, current Infliximab treatment"
        }

        # Run LLM-based comprehensive evaluation
        llm_evaluation_result = None
        bias_analysis_result = None

        if clinical_evaluator:
            try:
                sys_logger.log_system("info", "Starting comprehensive LLM evaluation...")

                # Comprehensive clinical performance evaluation
                llm_evaluation_result = clinical_evaluator.evaluate_clinical_performance(
                    dialogue_transcript=dialogue_transcript,
                    detected_biases=detected_biases,
                    metacognitive_responses=metacognitive_responses,
                    final_diagnosis=diagnosis,
                    case_context=case_context
                )

                # Additional bias analysis using Chain-of-Thought
                bias_analysis_result = clinical_evaluator.analyze_cognitive_biases(
                    dialogue_transcript=dialogue_transcript,
                    final_diagnosis=diagnosis
                )

                sys_logger.log_system("info", f"LLM evaluation completed successfully: {llm_evaluation_result.get('success', False)}")

            except Exception as llm_error:
                sys_logger.log_system("error", f"LLM evaluation failed: {llm_error}")

        # Calculate basic performance metrics for fallback
        discovered_count = session_data.get('discovered_count', 0)
        total_available = session_data.get('total_available', 1)
        bias_warnings = session_data.get('bias_warnings', 0)

        # Calculate scores
        discovery_percentage = (discovered_count / total_available) * 100 if total_available > 0 else 0
        bias_score = max(0, 100 - (bias_warnings * 10))

        # Build comprehensive response
        response_data = {
            "llm_evaluation": llm_evaluation_result,
            "bias_analysis": bias_analysis_result,
            "metacognitive_responses": metacognitive_responses,
            "session_stats": {
                "total_interactions": len(session_interactions),
                "discovery_percentage": discovery_percentage,
                "bias_warnings_count": bias_warnings,
                "session_duration": current_session.get_session_duration_minutes()
            }
        }

        # If LLM evaluation succeeded, use it as primary feedback
        if llm_evaluation_result and llm_evaluation_result.get('success'):
            evaluation = llm_evaluation_result['evaluation']
            response_data.update({
                "score": f"{evaluation.get('overall_score', 75)}/100",
                "feedback": "Comprehensive LLM-based evaluation completed. See detailed analysis below.",
                "performance_summary": {
                    "information_discovery": f"{evaluation.get('information_gathering', {}).get('score', 75)}/100",
                    "bias_awareness": f"{evaluation.get('cognitive_bias_awareness', {}).get('score', 75)}/100",
                    "diagnostic_accuracy": f"{evaluation.get('diagnostic_accuracy', {}).get('score', 75)}/100"
                }
            })
        else:
            # Fallback to basic evaluation
            overall_score = round((discovery_percentage * 0.6) + (bias_score * 0.4))
            response_data.update({
                "score": f"{overall_score}/100",
                "feedback": "Evaluation completed with basic metrics. LLM analysis was not available.",
                "performance_summary": {
                    "information_discovery": f"Good ({discovered_count}/{total_available} items)",
                    "bias_awareness": f"{'Excellent' if bias_warnings == 0 else 'Good'} ({bias_warnings} warnings)",
                    "diagnostic_accuracy": "Requires expert review"
                }
            })

        # Log the comprehensive evaluation
        sys_logger.log_system("info", f"Comprehensive evaluation completed for diagnosis: {diagnosis}")
        sys_logger.log_system("info", f"Metacognitive responses collected: {len(metacognitive_responses)} questions")

        return jsonify(response_data)

    except Exception as e:
        sys_logger.log_system("error", f"Error in comprehensive evaluation: {e}")
        return jsonify({
            "score": "Error",
            "feedback": "An error occurred during the comprehensive evaluation. Please try again.",
            "performance_summary": {
                "information_discovery": "N/A",
                "bias_awareness": "N/A",
                "diagnostic_accuracy": "N/A"
            },
            "error": str(e)
        }), 500

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
