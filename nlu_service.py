from sentence_transformers import SentenceTransformer, util
# Assuming canonical_question_mappings is defined in dialogue_fsm.py for now
# You'll need to make sure this import path is correct based on your project structure.
# If dialogue_fsm.py is in the same directory:
from dialogue_fsm_data import canonical_question_mappings # Or however you've named it

class NLUService:
    """
    Natural Language Understanding service using SBERT to map student queries
    to predefined canonical questions and their associated actions.
    """
    def __init__(self, mappings_data, sbert_model_name='all-MiniLM-L6-v2', similarity_cutoff=0.70):
        """
        Initializes the NLUService.

        Args:
            mappings_data (list): The list of canonical question mapping dictionaries.
            sbert_model_name (str): The name of the pre-trained SBERT model to use.
            similarity_cutoff (float): The minimum cosine similarity score to consider a match.
        """
        try:
            self.model = SentenceTransformer(sbert_model_name)
        except Exception as e:
            print(f"Error loading SBERT model '{sbert_model_name}': {e}")
            print("Please ensure the model name is correct and you have an internet connection for the first download.")
            print("You might need to install sentence-transformers: pip install sentence-transformers")
            self.model = None # Ensure model is None if loading fails
            return

        self.mappings_data = mappings_data
        self.similarity_cutoff = similarity_cutoff

        # Prepare a flat list of all canonical questions and their variations for embedding
        self.all_reference_texts = []
        # This list will store the original mapping item for each text in all_reference_texts
        self.reference_mapping_indices = [] 

        for i, item in enumerate(self.mappings_data):
            # Add the main canonical question
            self.all_reference_texts.append(item['canonical_question'])
            self.reference_mapping_indices.append(i) # Store index to original mapping item
            
            # Add all variations if they exist
            if 'variations' in item and item['variations']:
                for var_question in item['variations']:
                    self.all_reference_texts.append(var_question)
                    self.reference_mapping_indices.append(i) # This variation also maps to the i-th item

        if self.model and self.all_reference_texts:
            print(f"NLUService: Encoding {len(self.all_reference_texts)} reference texts...")
            self.reference_embeddings = self.model.encode(self.all_reference_texts, convert_to_tensor=True)
            print("NLUService: Reference embeddings created.")
        elif not self.model:
            self.reference_embeddings = None
        else:
            print("NLUService: No reference texts found in mappings_data.")
            self.reference_embeddings = None


    def process_input(self, student_query: str):
        """
        Processes the student's query to find the best matching canonical question.

        Args:
            student_query (str): The free-text input from the student.

        Returns:
            dict: A dictionary containing the match details (id, action_type, target_details, score)
                  or an indication that the intent was not understood.
        """
        if not self.model or self.reference_embeddings is None:
            print("NLUService Error: Model or reference embeddings not initialized.")
            return {"intent_id": "nlu_error_model_not_loaded", "score": 0.0}

        if not student_query or not student_query.strip():
            return {"intent_id": "empty_input", "score": 0.0}

        query_embedding = self.model.encode([student_query], convert_to_tensor=True)
        
        # Compute cosine similarities
        # util.pytorch_cos_sim returns a tensor of shape (num_query_embeddings, num_reference_embeddings)
        similarities = util.pytorch_cos_sim(query_embedding, self.reference_embeddings)[0] # We have one query
        
        best_match_idx_in_flat_list = similarities.argmax().item()
        best_score = similarities[best_match_idx_in_flat_list].item()

        if best_score >= self.similarity_cutoff:
            # Get the index of the original mapping item in self.mappings_data
            original_mapping_idx = self.reference_mapping_indices[best_match_idx_in_flat_list]
            matched_item_details = self.mappings_data[original_mapping_idx]
            
            print(f"NLU Debug: Query='{student_query}', BestMatch='{self.all_reference_texts[best_match_idx_in_flat_list]}', Score={best_score:.4f}, ID='{matched_item_details['id']}'")
            
            return {
                "intent_id": matched_item_details["id"], # Using 'id' from mapping as intent_id
                "action_type": matched_item_details["action_type"],
                "target_details": matched_item_details["target_details"],
                "matched_canonical_question": self.all_reference_texts[best_match_idx_in_flat_list], # Good for debugging
                "score": best_score
            }
        else:
            print(f"NLU Debug: Query='{student_query}', No confident match. Best score={best_score:.4f} (below cutoff {self.similarity_cutoff}) to '{self.all_reference_texts[best_match_idx_in_flat_list]}'")
            return {
                "intent_id": "intent_not_understood",
                "best_match_attempt": self.all_reference_texts[best_match_idx_in_flat_list] if self.all_reference_texts else "N/A",
                "score": best_score
            }

# --- Example Usage (for testing this module directly) ---
if __name__ == "__main__":
    # This assumes 'canonical_question_mappings' is imported from dialogue_fsm.py
    # and dialogue_fsm.py is in the same directory or Python path.
    
    print("Initializing NLUService for testing...")
    nlu = NLUService(mappings_data=canonical_question_mappings, similarity_cutoff=0.65) # Using a slightly lower cutoff for broad testing

    if nlu.model: # Check if model loaded
        print("\nNLUService Initialized. Ready for queries.")
        
        test_queries = [
            "Hello there",
            "What's the patient's primary issue?",
            "What is the patient's medical history?",
            "Tell me about the patient age",
            "For how long does she have a cough?", # This is not a canonical Q, tests semantic similarity
            "What did the chest x-ray show?",
            "Is she on any medication for arthritis?", # Should trigger discoverable infliximab query
            "What is the white blood cell count?",
            "kdjshfkjdsfhdskjfh" # Gibberish
        ]

        for query in test_queries:
            result = nlu.process_input(query)
            print(f"Query: '{query}' -> Result: {result}\n")
    else:
        print("NLUService could not be initialized properly (SBERT model likely failed to load).")