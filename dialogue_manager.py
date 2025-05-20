# dialogue_manager.py

from dialogue_fsm import DialogueState # Assuming this is in dialogue_fsm.py
# We'll need KnowledgeBaseManager if DM directly instantiates or uses it.
# For now, let's assume the main loop will pass necessary info from KBM via NLUService output or direct calls.
# However, the DM will often need to call KBM methods directly based on NLU output.
from knowledge_base_manager import KnowledgeBaseManager


class DialogueManager:
    def __init__(self, kb_manager: KnowledgeBaseManager, initial_state=DialogueState.INTRODUCTION):
        """
        Initializes the DialogueManager.

        Args:
            kb_manager (KnowledgeBaseManager): An instance of the knowledge base manager.
            initial_state (DialogueState): The starting state of the dialogue.
        """
        self.kb_manager = kb_manager
        self.current_state = initial_state
        self.revealed_discoveries = set() # To keep track of what has been revealed

        # A simple way to store responses that are scripted within the DM or very generic
        self.scripted_responses = {
            "greeting_response": f"Hello, I am SmartDoc, your virtual patient assistant for this clinical scenario. This case is: '{self.kb_manager.get_case_title()}'. The patient's history will be provided by their son. How would you like to begin?",
            "intent_not_understood": "I'm sorry, I didn't quite understand that. Could you please rephrase your question?",
            "nlu_error_model_not_loaded": "I'm having trouble understanding due to an NLU model issue. Please try again later.",
            "empty_input": "I didn't receive any input. Could you please ask a question?",
            "acknowledgement_and_closing": "Thank you for the interview. This concludes the current simulation.",
            "allergies_unknown_or_none_reported_by_son": "The patient's son is not aware of any allergies, and there are no known allergies listed in the initial information.",
            "abdominal_exam_not_detailed_initially": "The initial emergency department assessment did not include detailed findings for the abdominal exam as the focus was primarily cardiorespiratory.",
            "social_history_smoking_not_reported_by_son": "The patient's son did not report any history of smoking.", # Or fetch if added
            "family_history_not_detailed_by_son": "The patient's son does not have detailed information about her extended family history at this moment."
            # Add more as needed
        }

    def get_vsp_response(self, nlu_output: dict):
        """
        Generates the VSP's response based on NLU output and current dialogue state.

        Args:
            nlu_output (dict): The output from the NLUService, containing intent, action_type, target_details, etc.

        Returns:
            str: The VSP's response.
        """
        response = self.scripted_responses["intent_not_understood"] # Default response
        intent_id = nlu_output.get("intent_id")
        action_type = nlu_output.get("action_type")
        target_details = nlu_output.get("target_details")
        # score = nlu_output.get("score") # Could be used for confidence-based responses later

        print(f"DM Debug: Current State='{self.current_state}', NLU Intent='{intent_id}', Action='{action_type}'")

        # Handle NLU errors or empty input first
        if intent_id == "nlu_error_model_not_loaded":
            return self.scripted_responses["nlu_error_model_not_loaded"]
        if intent_id == "empty_input":
            return self.scripted_responses["empty_input"]
        if intent_id == "intent_not_understood":
            # Keep default "I didn't understand" or provide more context if needed
            return self.scripted_responses["intent_not_understood"]


        # --- Initial State Handling ---
        if self.current_state == DialogueState.INTRODUCTION:
            if intent_id == "general_greet" or action_type == "generic_response_or_state_change": # Or student asks "tell me about the patient"
                response = self.scripted_responses.get(target_details.get("response_key"), self.scripted_responses["greeting_response"])
                self.current_state = DialogueState.CHIEF_COMPLAINT_EXPLORATION # Auto-transition
                return response
            # Allow direct jump to chief complaint if student asks
            elif intent_id == "hpi_chief_complaint":
                 action_type = "fetch_from_kb" # Override to handle it now
                 target_details = {"method": "get_chief_complaints"} # Override


        # --- Main Logic based on Action Type from NLU ---
        if action_type == "fetch_from_kb":
            kb_method_name = target_details.get("method")
            kb_method_args = target_details.get("args", [])
            if hasattr(self.kb_manager, kb_method_name):
                method_to_call = getattr(self.kb_manager, kb_method_name)
                kb_data = method_to_call(*kb_method_args)
                if isinstance(kb_data, list):
                    response = "; ".join(kb_data) if kb_data else "No information available on that."
                elif kb_data is not None:
                    response = str(kb_data)
                else:
                    response = "I don't have specific information on that right now."
            else:
                response = "I'm sorry, I couldn't retrieve that specific information."
        
        elif action_type == "provide_scripted_response":
            response_key = target_details.get("response_key")
            response = self.scripted_responses.get(response_key, "I don't have a scripted response for that exact query, but I can try to answer more generally.")

        elif action_type == "trigger_discoverable":
            discoverable_item_key = target_details.get("discoverable_item_key")
            # For prototype: simple reveal if directly asked, or check if already revealed.
            # More complex logic for "conditions" would go here.
            # E.g., some items might only be revealed after specific prior questions or states.

            # Check if this is a relevant question for RA meds / Infliximab
            if discoverable_item_key == "Infliximab use" and intent_id == "discoverable_infliximab_query":
                 # Initially, the KB manager gives a scripted uncertain response.
                 # If student persists or asks for outside records (which we aren't simulating yet),
                 # then we could reveal. For now, let's assume this query alone doesn't
                 # immediately reveal it unless other conditions are met.
                 # The get_initial_response_for_ra_meds() is already mapped via canonical questions.
                 # This "trigger_discoverable" is for WHEN the actual data is given.
                 # Let's have a placeholder: if a student asks a *second time* or more specifically
                 # after initial evasiveness, then reveal. This needs more state.

                 # Simple reveal for now if it's not yet revealed:
                if discoverable_item_key not in self.revealed_discoveries:
                    item_data = self.kb_manager.get_discoverable_item_details(discoverable_item_key)
                    if item_data:
                        response = f"Regarding {item_data.get('item', discoverable_item_key)}: {item_data.get('details', 'Details not found.')} (This was found: {item_data.get('discoveryPoint', '')})"
                        self.revealed_discoveries.add(discoverable_item_key)
                    else:
                        response = f"I understand you're asking about {discoverable_item_key}, but I don't have those details yet."
                else:
                    item_data = self.kb_manager.get_discoverable_item_details(discoverable_item_key)
                    response = f"As previously mentioned regarding {item_data.get('item', discoverable_item_key)}: {item_data.get('details')}."

            elif discoverable_item_key not in self.revealed_discoveries:
                item_data = self.kb_manager.get_discoverable_item_details(discoverable_item_key)
                if item_data:
                    # Here you might add more complex logic based on item_data['triggerForVSPRevelation']
                    # For the prototype, let's assume a direct query (matched by SBERT) is enough to trigger
                    response = f"Regarding {item_data.get('item', discoverable_item_key)}: {item_data.get('details', 'Details not found.')} (This became available: {item_data.get('discoveryPoint', '')})"
                    self.revealed_discoveries.add(discoverable_item_key)
                else:
                    response = f"I understand you're asking about {discoverable_item_key}, but I don't have those details available at this moment."
            else: # Already revealed
                item_data = self.kb_manager.get_discoverable_item_details(discoverable_item_key)
                if item_data:
                    response = f"As previously discussed for {item_data.get('item', discoverable_item_key)}: {item_data.get('details')}."
                else:
                    response = f"We've talked about {discoverable_item_key}, but I can't recall the specifics now."
        
        elif action_type == "generic_response_or_state_change":
            response_key = target_details.get("response_key")
            suggested_next_state_str = target_details.get("next_state_suggestion")
            
            response = self.scripted_responses.get(response_key, "Okay.")
            if suggested_next_state_str and hasattr(DialogueState, suggested_next_state_str):
                self.current_state = getattr(DialogueState, suggested_next_state_str)
                if self.current_state == DialogueState.END_SIMULATION:
                    response += "\nSimulation ended." # Or handle this in main loop

        # --- State Transition Logic (can be more sophisticated) ---
        # This is a very basic transition logic. More rules can be added.
        if self.current_state == DialogueState.CHIEF_COMPLAINT_EXPLORATION and intent_id == "hpi_chief_complaint":
            self.current_state = DialogueState.HPI_GATHERING
        elif self.current_state == DialogueState.HPI_GATHERING and intent_id.startswith("hpi_"):
            pass # Stay in HPI gathering
        elif intent_id.startswith("pmh_") and self.current_state != DialogueState.PMH_GATHERING:
             self.current_state = DialogueState.PMH_GATHERING
        elif intent_id.startswith("meds_") and self.current_state != DialogueState.MEDICATION_REVIEW:
             self.current_state = DialogueState.MEDICATION_REVIEW
        elif intent_id.startswith("exam_") and self.current_state != DialogueState.PHYSICAL_EXAM_QUERY:
             self.current_state = DialogueState.PHYSICAL_EXAM_QUERY
        elif intent_id.startswith("labs_") or intent_id.startswith("imaging_") and self.current_state != DialogueState.INVESTIGATIONS_QUERY:
             self.current_state = DialogueState.INVESTIGATIONS_QUERY
        # Add transitions for SOCIAL_HISTORY_GATHERING, FAMILY_HISTORY_GATHERING, REVIEW_OF_SYSTEMS etc.

        if intent_id == "general_thank_you_conclude": # Already handled by generic_response_or_state_change
             pass


        print(f"DM Debug: Responding with='{response}', Next State='{self.current_state}'")
        return response

    def get_current_state(self):
        return self.current_state

# --- Example Usage (Conceptual - would be driven by main.py) ---
if __name__ == "__main__":
    # This test requires NLUService and canonical_question_mappings to be available
    # For simplicity, we'll mock NLU output.
    
    kb_file = "case01.json" # Make sure this file exists
    kb_m = KnowledgeBaseManager(filepath=kb_file)
    
    if not kb_m.is_loaded():
        print(f"Could not load {kb_file} for DM testing. Exiting.")
    else:
        dm = DialogueManager(kb_manager=kb_m)
        print(f"DM Initialized. Current state: {dm.get_current_state()}")

        # Simulate NLU output for "Hello"
        nlu_output_greet = {
            "intent_id": "general_greet", 
            "action_type": "generic_response_or_state_change", 
            "target_details": {"response_key": "greeting_response", "next_state_suggestion": "CHIEF_COMPLAINT_EXPLORATION"},
            "score": 0.9
        }
        vsp_response = dm.get_vsp_response(nlu_output_greet)
        print(f"VSP: {vsp_response}")
        print(f"DM Current state: {dm.get_current_state()}")

        # Simulate NLU output for "What is the chief complaint?"
        nlu_output_cc = {
            "intent_id": "hpi_chief_complaint",
            "action_type": "fetch_from_kb",
            "target_details": {"method": "get_chief_complaints"},
            "score": 0.85
        }
        vsp_response = dm.get_vsp_response(nlu_output_cc)
        print(f"VSP: {vsp_response}")
        print(f"DM Current state: {dm.get_current_state()}")
        
        # Simulate NLU output for "What were her vital signs?"
        nlu_output_vitals = {
            "intent_id": "exam_vital_signs",
            "action_type": "fetch_from_kb",
            "target_details": {"method": "get_vital_signs_initial"},
            "score": 0.92
        }
        vsp_response = dm.get_vsp_response(nlu_output_vitals) # Assuming state allows this or transitions
        print(f"VSP: {vsp_response}") 
        print(f"DM Current state: {dm.get_current_state()}") # State should change based on intent_id prefix

        # Simulate NLU output for "Is she on Infliximab?" (a discoverable item)
        # This would come from your canonical_question_mappings for discoverable_infliximab_query
        nlu_output_infliximab = {
            "intent_id": "discoverable_infliximab_query",
            "action_type": "trigger_discoverable",
            "target_details": {"discoverable_item_key": "Infliximab use"},
            "score": 0.88
        }
        # First time asking about infliximab (or RA meds generally that maps here)
        # The initial response for RA meds is often a specific evasive one from KBM
        # This DM's trigger_discoverable needs more refinement to model that initial evasiveness
        # For now, it directly reveals or says "not available yet" if truly not in discoverable section.
        # Let's assume KBM's "get_initial_response_for_ra_meds" would be hit first if SBERT matches that canonical question
        # If SBERT matches a *more specific* "is she on infliximab" canonical question directly mapped to trigger_discoverable:
        
        print("\n--- Testing Discoverable (Infliximab) ---")
        # We need to ensure the NLU can distinguish between a general RA med query and a specific discoverable query
        # Let's assume the NLU mapped to the specific discoverable one here.
        vsp_response = dm.get_vsp_response(nlu_output_infliximab)
        print(f"VSP (1st Infliximab query): {vsp_response}")
        print(f"Revealed items: {dm.revealed_discoveries}")

        # Asking again
        vsp_response = dm.get_vsp_response(nlu_output_infliximab)
        print(f"VSP (2nd Infliximab query): {vsp_response}")
        print(f"Revealed items: {dm.revealed_discoveries}")

        # Simulate NLU "intent_not_understood"
        nlu_output_unknown = {"intent_id": "intent_not_understood", "score": 0.3}
        vsp_response = dm.get_vsp_response(nlu_output_unknown)
        print(f"VSP: {vsp_response}")
        print(f"DM Current state: {dm.get_current_state()}")