from sentence_transformers import SentenceTransformer, util
from smartdoc.utils.logger import sys_logger  # Use the singleton system logger
from smartdoc.core.intents import canonical_question_mappings
from smartdoc.config.settings import config
from smartdoc.utils.exceptions import SBERTModelError, NLUError

class NLUService:
    """
    Natural Language Understanding service using SBERT to map student queries
    to predefined canonical questions and their associated actions.
    """
    def __init__(self, mappings_data, sbert_model_name=None, similarity_cutoff=None):
        """
        Initializes the NLUService.

        Args:
            mappings_data (list): The list of canonical question mapping dictionaries.
            sbert_model_name (str): The name of the pre-trained SBERT model to use. Defaults to config value.
            similarity_cutoff (float): The minimum cosine similarity score to consider a match. Defaults to config value.
        """
        self.sbert_model_name = sbert_model_name or config.SBERT_MODEL
        self.similarity_cutoff = similarity_cutoff or config.SIMILARITY_CUTOFF

        try:
            sys_logger.log_system("info", f"NLUService: Loading SBERT model '{self.sbert_model_name}'...")
            self.model = SentenceTransformer(self.sbert_model_name)
            sys_logger.log_system("info", "NLUService: SBERT model loaded successfully.")
        except Exception as e:
            sys_logger.log_system("error", f"Error loading SBERT model '{self.sbert_model_name}': {e}")
            sys_logger.log_system("error", "Please ensure the model name is correct and you have an internet connection for the first download.")
            sys_logger.log_system("error", "You might need to install sentence-transformers: pip install sentence-transformers")
            raise SBERTModelError(f"Failed to load SBERT model: {e}")

        self.mappings_data = mappings_data
        self.all_reference_texts = []
        self.reference_mapping_indices = []

        try:
            self._build_reference_embeddings()
        except Exception as e:
            sys_logger.log_system("error", f"Failed to build reference embeddings: {e}")
            raise NLUError(f"NLUService initialization failed: {e}")

    def _build_reference_embeddings(self):
        """Build reference embeddings from mappings data."""
        for i, item in enumerate(self.mappings_data):
            self.all_reference_texts.append(item['canonical_question'])
            self.reference_mapping_indices.append(i)
            if 'variations' in item and item['variations']:
                for var_question in item['variations']:
                    self.all_reference_texts.append(var_question)
                    self.reference_mapping_indices.append(i)

        if self.all_reference_texts:
            sys_logger.log_system("info", f"NLUService: Encoding {len(self.all_reference_texts)} reference texts...")
            try:
                self.reference_embeddings = self.model.encode(self.all_reference_texts, convert_to_tensor=True)
                sys_logger.log_system("info", "NLUService: Reference embeddings created successfully.")
            except Exception as e:
                sys_logger.log_system("error", f"Failed to encode reference texts: {e}")
                raise NLUError(f"Failed to create reference embeddings: {e}")
        else:
            sys_logger.log_system("warning", "NLUService: No reference texts found in mappings_data.")
            raise NLUError("No reference texts available for NLU processing")

    def process_input(self, student_query: str):
        """
        Processes the student's query to find the best matching canonical question.
        Enhanced with better error handling and validation.

        Args:
            student_query (str): The free-text input from the student.

        Returns:
            dict: A dictionary containing the match details (id, action_type, target_details, score)
                  or an indication that the intent was not understood.
        """
        if not hasattr(self, 'model') or not self.model:
            sys_logger.log_system("error", "NLUService Error: Model not initialized.")
            return {"intent_id": "nlu_error_model_not_loaded", "score": 0.0}

        if not hasattr(self, 'reference_embeddings') or self.reference_embeddings is None:
            sys_logger.log_system("error", "NLUService Error: Reference embeddings not available.")
            return {"intent_id": "nlu_error_embeddings_not_loaded", "score": 0.0}

        if not student_query or not student_query.strip():
            return {"intent_id": "empty_input", "score": 0.0}

        try:
            query_embedding = self.model.encode([student_query], convert_to_tensor=True)
            similarities = util.pytorch_cos_sim(query_embedding, self.reference_embeddings)[0]
            best_match_idx_in_flat_list = similarities.argmax().item()
            best_score = similarities[best_match_idx_in_flat_list].item()

            if best_score >= self.similarity_cutoff:
                original_mapping_idx = self.reference_mapping_indices[best_match_idx_in_flat_list]
                matched_item_details = self.mappings_data[original_mapping_idx]
                sys_logger.log_system(
                    "debug",
                    f"NLU Debug: Query='{student_query}', BestMatch='{self.all_reference_texts[best_match_idx_in_flat_list]}', Score={best_score:.4f}, ID='{matched_item_details['id']}'"
                )
                return {
                    "intent_id": matched_item_details["id"],
                    "action_type": matched_item_details["action_type"],
                    "target_details": matched_item_details["target_details"],
                    "matched_canonical_question": self.all_reference_texts[best_match_idx_in_flat_list],
                    "score": best_score
                }
            else:
                sys_logger.log_system(
                    "debug",
                    f"NLU Debug: Query='{student_query}', No confident match. Best score={best_score:.4f} (below cutoff {self.similarity_cutoff}) to '{self.all_reference_texts[best_match_idx_in_flat_list]}'"
                )
                return {
                    "intent_id": "intent_not_understood",
                    "best_match_attempt": self.all_reference_texts[best_match_idx_in_flat_list] if self.all_reference_texts else "N/A",
                    "score": best_score
                }

        except Exception as e:
            sys_logger.log_system("error", f"NLUService Error: Exception during query processing: {e}")
            return {
                "intent_id": "nlu_processing_error",
                "error_message": str(e),
                "score": 0.0
            }

# --- Example Usage (for testing this module directly) ---
if __name__ == "__main__":
    sys_logger.log_system("info", "Initializing NLUService for testing...")
    nlu = NLUService(mappings_data=canonical_question_mappings, similarity_cutoff=0.65)

    if nlu.model:
        sys_logger.log_system("info", "NLUService Initialized. Ready for queries.")
        test_queries = [
            "Hello there",
            "What's the patient's primary issue?",
            "What is the patient's medical history?",
            "Tell me about the patient age",
            "For how long does she have a cough?",
            "What did the chest x-ray show?",
            "Is she on any medication for arthritis?",
            "What is the white blood cell count?",
            "kdjshfkjdsfhdskjfh"
        ]

        for query in test_queries:
            result = nlu.process_input(query)
            sys_logger.log_system("info", f"Query: '{query}' -> Result: {result}\n")
    else:
        sys_logger.log_system("error", "NLUService could not be initialized properly (SBERT model likely failed to load).")
