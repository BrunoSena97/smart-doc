# main.py

from dialogue_fsm import DialogueState
from knowledge_base_manager import KnowledgeBaseManager
from dialogue_fsm_data import canonical_question_mappings # Import mappings
from nlu_service import NLUService
from dialogue_manager import DialogueManager
from system_logger import SystemLogger # Import the logger

def run_smartdoc_session():
    print("Initializing SmartDoc...")

    # 1. Initialize Knowledge Base Manager
    kb_filepath = "case01.json"  # Ensure this path is correct
    kb_manager = KnowledgeBaseManager(filepath=kb_filepath)
    if not kb_manager.is_loaded():
        print(f"CRITICAL ERROR: Could not load knowledge base from {kb_filepath}. Exiting.")
        return

    # 2. Initialize NLU Service
    # Pass the imported canonical_question_mappings
    nlu_service = NLUService(mappings_data=canonical_question_mappings, similarity_cutoff=0.70) # Adjust cutoff as needed
    if not nlu_service.model:
        print("CRITICAL ERROR: NLUService model could not be loaded. Exiting.")
        return

    # 3. Initialize Dialogue Manager
    dm_manager = DialogueManager(kb_manager=kb_manager)

    # 4. Initialize Logger
    logger = SystemLogger(logfile_path="smartdoc_conversation_log.txt")

    print("\nSmartDoc Initialized. Welcome to the clinical interview simulation.")
    print(f"Current case: {kb_manager.get_case_title()}")
    print("Type 'quit' at any time to end the session.\n")

    # Provide initial VSP statement from Dialogue Manager (usually a greeting)
    # We can get this by processing a "system" greet intent or having a dedicated method.
    # For simplicity, let's simulate an initial "greet" from the student to kick things off
    # or call a specific DM method if it has one for starting.
    # The DM's scripted_responses for "greeting_response" will be used.
    
    # Let's get an initial greeting directly from the DM to start the conversation
    initial_nlu_output_for_greeting = {
        "intent_id": "general_greet", 
        "action_type": "generic_response_or_state_change", 
        "target_details": {"response_key": "greeting_response", "next_state_suggestion": "CHIEF_COMPLAINT_EXPLORATION"}
    }
    initial_vsp_response = dm_manager.get_vsp_response(initial_nlu_output_for_greeting)
    print(f"SmartDoc: {initial_vsp_response}")
    logger.log_interaction("System: [Session Start]", initial_vsp_response, dm_manager.get_current_state())


    # 5. Main Interaction Loop
    while True:
        try:
            student_input = input("Student: ").strip()
        except EOFError: # Handle Ctrl+D in some terminals
            print("\nSmartDoc: Exiting session (EOF detected).")
            break
        except KeyboardInterrupt: # Handle Ctrl+C
            print("\nSmartDoc: Exiting session (Interrupted by user).")
            break


        if student_input.lower() == "quit":
            print("SmartDoc: Exiting session as requested.")
            logger.log_interaction(student_input, "Session ended by user.", dm_manager.get_current_state())
            break

        if not student_input: # Handle empty input from student
            nlu_output = {"intent_id": "empty_input"}
        else:
            nlu_output = nlu_service.process_input(student_input)
        
        vsp_response = dm_manager.get_vsp_response(nlu_output)
        
        print(f"SmartDoc: {vsp_response}")

        # Log interaction
        logger.log_interaction(
            student_input, 
            vsp_response, 
            dm_manager.get_current_state(),
            nlu_output.get("intent_id"),
            nlu_output.get("score")
        )

        if dm_manager.get_current_state() == DialogueState.END_SIMULATION:
            print("SmartDoc: The simulation has reached its end point.")
            break
            
    print("\n--- End of SmartDoc Session ---")

if __name__ == "__main__":
    run_smartdoc_session()