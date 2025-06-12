# app.py (Corrected to initialize and pass NLGService)

from flask import Flask, render_template, request, jsonify
from dialogue_fsm import DialogueState
from knowledge_base_manager import KnowledgeBaseManager
from dialogue_fsm_data import canonical_question_mappings
from nlu_service import NLUService
from dialogue_manager import DialogueManager
from system_logger import SystemLogger
from nlg_service import NLGService  # <-- IMPORT THE NEW SERVICE

# --- 1. Initialize the Flask App ---
app = Flask(__name__)

# --- 2. Initialize All SmartDoc Components (ONCE at startup) ---
try:
    print("Initializing SmartDoc Components for the Web App...")

    # Knowledge Base Manager
    kb_manager = KnowledgeBaseManager(filepath="case01.json")
    if not kb_manager.is_loaded():
        raise RuntimeError("Could not load knowledge base.")

    # NLU Service
    nlu_service = NLUService(mappings_data=canonical_question_mappings, similarity_cutoff=0.70)
    if not nlu_service.model:
        raise RuntimeError("NLUService model could not be loaded.")

    # Initialize the NLG Service
    nlg_service = NLGService() # This uses the default gemma3:4b model
    if not nlg_service.is_initialized:
        raise RuntimeError("NLGService could not connect to Ollama.")

    # Dialogue Manager (Pass BOTH kb_manager and nlg_service)
    dm_manager = DialogueManager(kb_manager=kb_manager, nlg_service=nlg_service)

    # System Logger
    logger = SystemLogger(logfile_path="smartdoc_conversation_log.txt")

    print("SmartDoc Components Initialized Successfully.")

except Exception as e:
    print(f"CRITICAL ERROR during initialization: {e}")
    kb_manager = nlu_service = dm_manager = logger = nlg_service = None

# --- Routes remain the same, no changes needed below this line ---

@app.route("/")
def home():
    if not dm_manager:
        return "Error: SmartDoc application is not initialized. Please check the server logs.", 500
    dm_manager.reset_state()
    initial_nlu_output = {
        "intent_id": "general_greet",
        "action_type": "generic_response_or_state_change",
        "target_details": {"response_key": "greeting_response"}
    }
    initial_bot_message = dm_manager.get_vsp_response(initial_nlu_output)
    logger.log_interaction("System: [Session Start]", initial_bot_message, dm_manager.get_current_state())
    return render_template("index.html", initial_bot_message=initial_bot_message)

@app.route("/get")
def get_bot_response():
    if not dm_manager:
        return jsonify({"response": "Error: SmartDoc is not initialized."})
    user_input = request.args.get('msg')
    if user_input.lower() == "quit":
        response_text = "Session ended."
        logger.log_interaction(user_input, response_text, dm_manager.get_current_state())
        return jsonify({"response": response_text})
    nlu_output = nlu_service.process_input(user_input)
    vsp_response = dm_manager.get_vsp_response(nlu_output)
    logger.log_interaction(
        user_input, vsp_response, dm_manager.get_current_state(),
        nlu_output.get("intent_id"), nlu_output.get("score")
    )
    return jsonify({"response": vsp_response})

if __name__ == "__main__":
    print("Starting Flask web server...")
    print("Open your browser and go to http://127.0.0.1:5000")
    app.run()
