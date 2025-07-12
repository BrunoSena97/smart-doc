# nlg_service.py (Enhanced with better error handling and configuration)
import requests
import json
import traceback
import time

from smartdoc.utils.logger import sys_logger  # Import the singleton system logger
from smartdoc.config.settings import config
from smartdoc.utils.exceptions import OllamaConnectionError, OllamaModelError, NLGError

class NLGService:
    def __init__(self, model_name=None, ollama_base_url=None):
        """
        Initializes the Natural Language Generation Service to use a model running in Ollama.

        Args:
            model_name (str): The name of the model as it is in Ollama. Defaults to config value.
            ollama_base_url (str): The base URL for the Ollama API. Defaults to config value.
        """
        self.model_name = model_name or config.OLLAMA_MODEL
        self.base_url = ollama_base_url or config.OLLAMA_BASE_URL
        self.chat_endpoint = f"{self.base_url}/api/chat"
        self.is_initialized = False
        self.retry_count = 0

        sys_logger.log_system("info", f"NLGService: Initializing for model '{self.model_name}' on Ollama.")

        # Check if the Ollama server is reachable with retries
        self._initialize_with_retries()

    def _initialize_with_retries(self):
        """Initialize connection to Ollama with retry logic."""
        for attempt in range(config.MAX_RETRIES):
            try:
                response = requests.head(self.base_url, timeout=5)
                if response.status_code == 200:
                    sys_logger.log_system("info", "NLGService: Ollama server is reachable.")
                    self.is_initialized = True
                    return
                else:
                    raise OllamaConnectionError(f"Ollama server returned status code: {response.status_code}")

            except requests.ConnectionError as e:
                if attempt < config.MAX_RETRIES - 1:
                    sys_logger.log_system("warning", f"NLGService: Connection attempt {attempt + 1} failed, retrying in {config.RETRY_DELAY_SECONDS}s...")
                    time.sleep(config.RETRY_DELAY_SECONDS)
                else:
                    sys_logger.log_system("error", f"NLGService Error: Could not connect to Ollama server at {self.base_url} after {config.MAX_RETRIES} attempts.")
                    sys_logger.log_system("error", "Please ensure the Ollama application is running.")
                    if config.FALLBACK_RESPONSES_ENABLED:
                        sys_logger.log_system("info", "NLGService: Fallback responses enabled, continuing with limited functionality.")
                    else:
                        raise OllamaConnectionError(f"Failed to connect to Ollama: {e}")

            except Exception as e:
                sys_logger.log_system("error", f"NLGService: Unexpected error during initialization: {e}")
                if attempt == config.MAX_RETRIES - 1:
                    raise NLGError(f"NLGService initialization failed: {e}")

    def generate_response(self, structured_info: dict, max_new_tokens=None, temperature=None, do_sample=True):
        """Generate response with enhanced error handling and fallback mechanisms."""
        # Use config defaults if not specified
        max_new_tokens = max_new_tokens or config.NLG_MAX_TOKENS
        temperature = temperature or config.NLG_TEMPERATURE

        if not self.is_initialized and not config.FALLBACK_RESPONSES_ENABLED:
            raise NLGError("NLG Service is not properly initialized and fallback responses are disabled.")

        if not self.is_initialized:
            return self._get_fallback_response(structured_info)

        # --- Prompt Engineering for Gemma using Chat Roles ---
        system_message_content = (
            "You are acting as the patient's son. The patient is an elderly Spanish-speaking woman. "
            "You are providing information to a medical student. Your responses should be natural, "
            "empathetic, concise, and directly based *only* on the information provided to you. "
            "Do not add any medical details, opinions, or information not explicitly given. "
            "Keep your answers short and directly address what you are asked to convey. "
            "Avoid conversational fillers unless it makes sense for the specific information."
        )

        user_message_content = self._build_user_message(structured_info)

        # The messages payload for the Ollama chat API
        messages = [
            {"role": "system", "content": system_message_content},
            {"role": "user", "content": user_message_content}
        ]

        # The data payload for the POST request
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_new_tokens
            }
        }

        sys_logger.log_system("debug", f"NLG Debug: Payload sent to Ollama:\n{json.dumps(payload, indent=2)}")

        # Try generation with retries
        for attempt in range(config.MAX_RETRIES):
            try:
                response = requests.post(self.chat_endpoint, json=payload, timeout=30)
                response.raise_for_status()

                response_data = response.json()
                generated_text = response_data.get("message", {}).get("content", "")

                if not generated_text.strip():
                    raise OllamaModelError("Ollama returned empty response")

                sys_logger.log_system("debug", f"NLG Debug: Raw Generated Output from Ollama: '{generated_text.strip()}'")
                return generated_text.strip()

            except requests.RequestException as e:
                if "model" in str(e) and "not found" in str(e):
                    sys_logger.log_system("error", f"Model '{self.model_name}' not found. Run 'ollama pull {self.model_name}'")
                    raise OllamaModelError(f"Model not found: {self.model_name}")

                if attempt < config.MAX_RETRIES - 1:
                    sys_logger.log_system("warning", f"NLG request attempt {attempt + 1} failed, retrying: {e}")
                    time.sleep(config.RETRY_DELAY_SECONDS)
                else:
                    sys_logger.log_system("error", f"NLGService Error: API request to Ollama failed after {config.MAX_RETRIES} attempts. Error: {e}")
                    if config.FALLBACK_RESPONSES_ENABLED:
                        return self._get_fallback_response(structured_info)
                    raise OllamaConnectionError(f"Failed to connect to Ollama after retries: {e}")

            except Exception as e:
                sys_logger.log_system("error", f"NLGService Error: An unexpected error occurred during response generation. Error: {e}")
                sys_logger.log_system("error", traceback.format_exc())
                if config.FALLBACK_RESPONSES_ENABLED:
                    return self._get_fallback_response(structured_info)
                raise NLGError(f"Unexpected error in NLG generation: {e}")

        # If we get here, all retries failed
        if config.FALLBACK_RESPONSES_ENABLED:
            return self._get_fallback_response(structured_info)
        raise NLGError("Failed to generate response after all retry attempts")

    def _build_user_message(self, structured_info: dict) -> str:
        """Build user message from structured info."""
        action = structured_info.get("action", "inform")
        data_to_convey = structured_info.get("data", "")

        if action == "inform" and data_to_convey:
            return f"Please tell the medical student the following information: '{data_to_convey}'"
        elif action == "state_uncertainty" and data_to_convey:
            return f"The medical student asked something you are unsure about. Please convey this uncertainty: '{data_to_convey}'"
        elif action == "answer_yes_no" and data_to_convey:
            return f"Please answer the student's query by conveying: '{data_to_convey}'"
        elif action == "greet" and data_to_convey:
            return f"The medical student has started the conversation. Please provide an initial greeting and state: '{data_to_convey}'"
        else: # Fallback
            return f"Please respond based on this information: '{data_to_convey}'"

    def _get_fallback_response(self, structured_info: dict) -> str:
        """Generate fallback response when LLM is unavailable."""
        action = structured_info.get("action", "inform")
        data_to_convey = structured_info.get("data", "No information available")

        fallback_responses = {
            "greet": f"Hello, I'm here to talk about my mother. {data_to_convey}",
            "inform": f"{data_to_convey}",
            "state_uncertainty": f"I'm not sure about that. {data_to_convey}",
            "answer_yes_no": f"{data_to_convey}",
        }

        response = fallback_responses.get(action, data_to_convey)
        sys_logger.log_system("info", "NLG: Using fallback response (LLM unavailable)")
        return response


# --- Example Usage (for testing this module directly) ---
if __name__ == "__main__":
    sys_logger.log_system("info", "Initializing NLGService for testing with Ollama...")
    # Make sure you have run `ollama pull gemma3:4b-it-q4_K_M` in your terminal first!
    nlg = NLGService(model_name="gemma3:4b-it-q4_K_M")

    if nlg.is_initialized:
        sys_logger.log_system("info", "NLGService Initialized. Ready for generation.")

        test_cases = [
            # Test cases remain the same
            {
                "info": {"persona": "son", "action": "greet", "data": "I'm here to talk about my mother. She's an elderly Spanish-speaking woman."},
                "max_tokens": 70, "desc": "Greeting"
            },
            {
                "info": {"persona": "son", "action": "inform", "data": "She has been experiencing worsening shortness of breath for about two months, especially when she exerts herself, and also has a nonproductive cough."},
                "max_tokens": 70, "desc": "Chief Complaint Details"
            },
            {
                "info": {"persona": "son", "action": "inform", "data": "Her white blood cell count is 13.0 x10^9/L, which is elevated."},
                "max_tokens": 40, "desc": "Lab Result"
            },
            {
                "info": {"persona": "son", "action": "state_uncertainty", "data": "I'm not sure what medications she takes for her rheumatoid arthritis; her records are at another hospital."},
                "max_tokens": 60, "desc": "Uncertainty about RA Meds"
            },
            {
                "info": {"persona": "son", "action": "inform", "data": "She denies any chest pain or fevers."},
                "max_tokens": 30, "desc": "Pertinent Negative"
            }
        ]

        for case in test_cases:
            sys_logger.log_system("info", f"\n--- Test Case: {case['desc']} ---")
            sys_logger.log_system("info", f"Input Data to NLG: {case['info']}")
            response = nlg.generate_response(case['info'], max_new_tokens=case['max_tokens'])
            sys_logger.log_system("info", f"VSP (Son): {response}")
    else:
        sys_logger.log_system("error", "NLGService could not be initialized. Check Ollama server errors above.")
