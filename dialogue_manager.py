# dialogue_manager.py (Fully refactored to use NLGService)

from dialogue_fsm import DialogueState
from knowledge_base_manager import KnowledgeBaseManager
from nlg_service import NLGService # <-- Import the NLG service

class DialogueManager:
    """
    Manages the dialogue flow, state, and response generation strategy.
    It determines WHAT information to convey and delegates HOW to say it to the NLGService.
    """
    def __init__(self, kb_manager: KnowledgeBaseManager, nlg_service: NLGService, initial_state=DialogueState.INTRODUCTION):
        """
        Initializes the DialogueManager.

        Args:
            kb_manager (KnowledgeBaseManager): An instance of the knowledge base manager.
            nlg_service (NLGService): An instance of the natural language generation service.
            initial_state (DialogueState): The starting state of the dialogue.
        """
        self.kb_manager = kb_manager
        self.nlg_service = nlg_service  # <-- Store the NLG service instance
        self.initial_state = initial_state
        self.current_state = self.initial_state
        self.revealed_discoveries = set()

        # These responses are for simple cases that DON'T require the LLM's creativity.
        self.scripted_responses = {
            "intent_not_understood": "I'm sorry, I didn't quite understand that. Could you please rephrase your question?",
            "nlu_error_model_not_loaded": "I'm having trouble understanding due to an NLU model issue. Please try again later.",
            "empty_input": "I didn't receive any input. Could you please ask a question?",
            "acknowledgement_and_closing": "Thank you for the interview. This concludes the current simulation.",
            "no_info_available": "I don't have specific information on that right now."
        }

    def reset_state(self):
        """
        Resets the dialogue manager to its initial state for a new session.
        """
        self.current_state = self.initial_state
        self.revealed_discoveries.clear()
        print("DM Debug: Dialogue state has been reset.")

    def get_vsp_response(self, nlu_output: dict) -> str:
        """
        Generates the VSP's response by determining the data to convey and using the NLGService.

        Args:
            nlu_output (dict): The output from the NLUService.

        Returns:
            str: The final, natural language response from the VSP.
        """
        intent_id = nlu_output.get("intent_id")
        action_type = nlu_output.get("action_type")
        target_details = nlu_output.get("target_details")

        print(f"DM Debug: Current State='{self.current_state}', NLU Intent='{intent_id}', Action='{action_type}'")

        # --- 1. Handle simple, non-LLM cases first for efficiency ---
        if intent_id in ["nlu_error_model_not_loaded", "empty_input", "intent_not_understood"]:
            return self.scripted_responses.get(intent_id, "I'm not sure how to respond to that.")

        # --- 2. Determine the raw data to be spoken by the LLM ---
        data_to_convey = ""
        nlg_action = "inform"  # Default action for the NLG service

        if action_type == "fetch_from_kb":
            kb_method_name = target_details.get("method")
            if hasattr(self.kb_manager, kb_method_name):
                method_to_call = getattr(self.kb_manager, kb_method_name)
                kb_data = method_to_call() # Assuming no args for simplicity, adjust if needed
                if isinstance(kb_data, list):
                    data_to_convey = "; ".join(map(str, kb_data)) if kb_data else ""
                elif kb_data is not None:
                    data_to_convey = str(kb_data)

        elif action_type == "trigger_discoverable":
            discoverable_item_key = target_details.get("discoverable_item_key")
            if discoverable_item_key not in self.revealed_discoveries:
                item_data = self.kb_manager.get_discoverable_item_details(discoverable_item_key)
                if item_data:
                    data_to_convey = f"Regarding {item_data.get('item', '')}: {item_data.get('details', '')}"
                    self.revealed_discoveries.add(discoverable_item_key)
            else: # Already revealed
                item_data = self.kb_manager.get_discoverable_item_details(discoverable_item_key)
                data_to_convey = f"As we already discussed about {item_data.get('item', '')}: {item_data.get('details')}"
                nlg_action = "inform_repeat" # Could use a different action for repeated info

        elif action_type == "generic_response_or_state_change":
            if target_details.get("response_key") == "greeting_response":
                nlg_action = "greet"
                data_to_convey = f"I'm here to discuss my mother's case, which is about '{self.kb_manager.get_case_title()}'."
            else:
                 # Handle other generic cases like "thank you"
                return self.scripted_responses.get(target_details.get("response_key"), "Okay, understood.")

        # --- 3. Call the NLG Service to generate the final response ---
        if data_to_convey:
            print(f"DM Debug: Sending to NLG -> action='{nlg_action}', data='{data_to_convey}'")
            structured_nlg_input = {"action": nlg_action, "data": data_to_convey}
            response = self.nlg_service.generate_response(structured_nlg_input)
        else:
            # Fallback if the NLU mapping was correct but no data was found in the KB
            response = self.scripted_responses["no_info_available"]

        # --- 4. Update state machine (logic can remain the same) ---
        if self.current_state == DialogueState.INTRODUCTION:
            self.current_state = DialogueState.CHIEF_COMPLAINT_EXPLORATION
        elif self.current_state == DialogueState.CHIEF_COMPLAINT_EXPLORATION and intent_id == "hpi_chief_complaint":
            self.current_state = DialogueState.HPI_GATHERING
        # ... (add all other state transition rules here) ...

        print(f"DM Debug: Final VSP response='{response}', Next State='{self.current_state}'")
        return response

    def get_current_state(self):
        return self.current_state
