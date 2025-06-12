# nlg_service.py (Migrated to use Ollama with the 4B model)
import requests
import json
import traceback

class NLGService:
    def __init__(self, model_name="gemma3:4b-it-q4_K_M", ollama_base_url="http://localhost:11434"):
        """
        Initializes the Natural Language Generation Service to use a model running in Ollama.

        Args:
            model_name (str): The name of the model as it is in Ollama (e.g., 'gemma3:4b-it-q4_K_M').
            ollama_base_url (str): The base URL for the Ollama API.
        """
        self.model_name = model_name
        self.base_url = ollama_base_url
        self.chat_endpoint = f"{self.base_url}/api/chat"
        self.is_initialized = False

        print(f"NLGService: Initializing for model '{self.model_name}' on Ollama.")

        # Check if the Ollama server is reachable
        try:
            response = requests.head(self.base_url)
            if response.status_code == 200:
                print("NLGService: Ollama server is reachable.")
                self.is_initialized = True
            else:
                print(f"NLGService Error: Ollama server at {self.base_url} is not reachable (status code: {response.status_code}).")
        except requests.ConnectionError:
            print(f"NLGService Error: Could not connect to Ollama server at {self.base_url}.")
            print("Please ensure the Ollama application is running.")

    def generate_response(self, structured_info: dict, max_new_tokens=100, temperature=0.7, do_sample=True):
        if not self.is_initialized:
            return "NLG Service is not properly initialized. Cannot generate response."

        # --- Prompt Engineering for Gemma using Chat Roles ---
        system_message_content = (
            "You are acting as the patient's son. The patient is an elderly Spanish-speaking woman. "
            "You are providing information to a medical student. Your responses should be natural, "
            "empathetic, concise, and directly based *only* on the information provided to you. "
            "Do not add any medical details, opinions, or information not explicitly given. "
            "Keep your answers short and directly address what you are asked to convey. "
            "Avoid conversational fillers unless it makes sense for the specific information."
        )

        user_message_content = ""
        action = structured_info.get("action", "inform")
        data_to_convey = structured_info.get("data", "")

        if action == "inform" and data_to_convey:
            user_message_content = f"Please tell the medical student the following information: '{data_to_convey}'"
        elif action == "state_uncertainty" and data_to_convey:
            user_message_content = f"The medical student asked something you are unsure about. Please convey this uncertainty: '{data_to_convey}'"
        elif action == "answer_yes_no" and data_to_convey:
            user_message_content = f"Please answer the student's query by conveying: '{data_to_convey}'"
        elif action == "greet" and data_to_convey:
            user_message_content = f"The medical student has started the conversation. Please provide an initial greeting and state: '{data_to_convey}'"
        else: # Fallback
            user_message_content = f"Please respond based on this information: '{data_to_convey}'"

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

        print(f"NLG Debug: Payload sent to Ollama:\n{json.dumps(payload, indent=2)}")

        try:
            response = requests.post(self.chat_endpoint, json=payload)
            response.raise_for_status()

            response_data = response.json()
            generated_text = response_data.get("message", {}).get("content", "")

            print(f"NLG Debug: Raw Generated Output from Ollama: '{generated_text.strip()}'")
            return generated_text.strip()

        except requests.RequestException as e:
            print(f"NLGService Error: API request to Ollama failed. Error: {e}")
            if "model" in str(e) and "not found" in str(e):
                print(f"Hint: Make sure you have run 'ollama pull {self.model_name}'")
            return "I'm having trouble connecting to my knowledge base right now."
        except Exception as e:
            print(f"NLGService Error: An unexpected error occurred during response generation. Error: {e}")
            print(traceback.format_exc())
            return "I'm having a bit of trouble formulating a response right now."


# --- Example Usage (for testing this module directly) ---
if __name__ == "__main__":
    print("Initializing NLGService for testing with Ollama...")
    # Make sure you have run `ollama pull gemma3:4b-it-q4_K_M` in your terminal first!
    nlg = NLGService(model_name="gemma3:4b-it-q4_K_M")

    if nlg.is_initialized:
        print("\nNLGService Initialized. Ready for generation.")

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
            print(f"\n--- Test Case: {case['desc']} ---")
            print(f"Input Data to NLG: {case['info']}")
            response = nlg.generate_response(case['info'], max_new_tokens=case['max_tokens'])
            print(f"VSP (Son): {response}")
    else:
        print("NLGService could not be initialized. Check Ollama server errors above.")
