# nlg_service.py
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import os

os.environ["TORCHINDUCTOR_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["DISABLE_TORCH_COMPILE"] = "1"
os.environ["TORCH_LOGS"] = "-dynamo"

class NLGService:
    def __init__(self, model_name_or_path="google/gemma-3-1b-it", use_quantization=True): # Changed default model, Gemma 3-1b might not exist, using 2b-it as an example
        """
        Initializes the Natural Language Generation Service.
        Gemma 1.1 2b-it is used as an example, ensure "google/gemma-3-1b-it" is a valid HF identifier if you use it.

        Args:
            model_name_or_path (str): The Hugging Face model identifier or local path.
            use_quantization (bool): Whether to load the model with 8-bit/4-bit quantization.
                                      For Gemma models, bfloat16 is often preferred over 8-bit if supported.
        """
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"NLGService: Using device: {self.device}")

        # Gemma models often work well with bfloat16 on compatible GPUs
        # and might not always benefit from bitsandbytes 8-bit in the same way as other models.
        # However, quantization can still save memory.
        # For this version, let's prioritize bfloat16 if on CUDA, and allow quantization.
        
        model_kwargs = {"device_map": "auto"}
        if self.device == "cuda":
            model_kwargs["torch_dtype"] = torch.bfloat16 # Gemma often trained with bfloat16
            print("NLGService: Using torch_dtype=torch.bfloat16 for CUDA device.")

        quantization_config = None
        if use_quantization and self.device == "cuda": # bitsandbytes quantization primarily targets CUDA
            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True # Or load_in_4bit=True for more aggressive quantization
                # For 4-bit with Gemma, you might need to check optimal bnb settings
                # load_in_4bit=True,
                # bnb_4bit_quant_type="nf4", # or "fp4"
                # bnb_4bit_compute_dtype=torch.bfloat16
            )
            model_kwargs["quantization_config"] = quantization_config
            print(f"NLGService: Applying quantization_config (load_in_8bit={quantization_config.load_in_8bit}).")
        elif use_quantization and self.device == "cpu":
            print("NLGService: Quantization with bitsandbytes is typically for CUDA. Will load model in default precision for CPU.")


        try:
            # Ensure you are logged in if the model requires it (some Gemma models might)
            from huggingface_hub import login
            login("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") # If needed
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
            # Gemma's tokenizer might not have a pad_token set by default in some versions/uses.
            # Using eos_token as pad_token is a common strategy for causal LMs if pad_token is None.
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                print("NLGService: Tokenizer pad_token set to eos_token.")

            self.model = AutoModelForCausalLM.from_pretrained(
                model_name_or_path,
                **model_kwargs # Pass dtype and quantization here
            )
            self.model.eval() # Set model to evaluation mode
            print(f"NLGService: Loaded model '{model_name_or_path}' successfully.")

        except Exception as e:
            print(f"NLGService Error: Could not load model or tokenizer '{model_name_or_path}'. Error: {e}")
            print("Make sure the model name is correct, you have accepted any terms on Hugging Face Hub if required (e.g., for Gemma),")
            print("you have a stable internet connection for the first download, sufficient disk space, and compatible hardware/drivers.")
            self.model = None
            self.tokenizer = None


    def generate_response(self, structured_info: dict, max_new_tokens=100, temperature=0.7, do_sample=True):
        if not self.model or not self.tokenizer:
            return "NLG Service is not properly initialized. Cannot generate response."

        persona = structured_info.get("persona", "a helpful assistant")
        action = structured_info.get("action", "inform")
        data_to_convey = structured_info.get("data", "")
        # current_topic = structured_info.get("current_topic", "the patient's condition") # Context

        # --- Prompt Engineering for Gemma using Chat Template ---
        # Gemma instruct models are typically fine-tuned using a specific chat format.
        # Using tokenizer.apply_chat_template is the recommended way.
        
        # System prompt sets the overall behavior and persona
        system_message_content = (
            f"You are acting as the patient's son. The patient is an elderly Spanish-speaking woman. "
            f"You are providing information to a medical student. Your responses should be natural, "
            f"empathetic, concise, and directly based *only* on the information provided to you. "
            f"Do not add any medical details, opinions, or information not explicitly given. "
            f"Keep your answers short and directly address what you are asked to convey. "
            f"Avoid conversational fillers unless it makes sense for the specific information."
        )

        user_message_content = ""
        if action == "inform" and data_to_convey:
            user_message_content = f"Please tell the medical student the following information: '{data_to_convey}'"
        elif action == "state_uncertainty" and data_to_convey:
            user_message_content = f"The medical student asked something you are unsure about. Please convey this uncertainty: '{data_to_convey}'"
        elif action == "answer_yes_no" and data_to_convey:
            user_message_content = f"Please answer the student's query by conveying: '{data_to_convey}'"
        elif action == "greet" and data_to_convey: # Specific greeting action
             user_message_content = f"The medical student has started the conversation. Please provide an initial greeting and state: '{data_to_convey}'"
        else: # Fallback
            user_message_content = f"Please respond based on this information: '{data_to_convey}'"

        # Construct the messages list for the chat template
        # Some models handle system prompts as the first message, others as part of the user message.
        # The apply_chat_template should ideally handle the model's specific needs.
        # For Gemma, the system prompt is often implicitly part of the turn structure or the first user message.
        # Let's try with a user role for the system instructions, then another user role for the task.
        # Or, more commonly for Gemma, the "system" prompt sets the context for the entire conversation.
        # However, for single-turn generation, it's often simpler to blend system instructions into the user prompt.
        # Let's use the structure that's more likely to work with `apply_chat_template` if the tokenizer has a good default template.
        
        # It's often better to represent the system instructions as a "system" role if the template supports it.
        # If not, including it in the first user message is a common workaround.
        # The example you gave for Gemma (`google/gemma-3-1b-it` with pipeline) used a `system` role:
        # `{"role": "system", "content": [{"type": "text", "text": "You are a helpful assistant."},]}`
        # And then a `user` role. Let's try to follow that structure.
        # Note: The content format `[{"type": "text", "text": "..."}]` is specific to multimodal inputs or certain pipeline expectations.
        # For text-only models with `apply_chat_template`, simple string content is usually sufficient.

        messages = [
            {"role": "system", "content": system_message_content},
            {"role": "user", "content": user_message_content}
        ]
        
        try:
            # `add_generation_prompt=True` is important for instruct/chat models
            # as it appends the tokens that signal to the model it's its turn to speak.
            prompt_text = self.tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
        except Exception as e:
            print(f"NLGService Warning: Could not apply chat template: {e}. Falling back to simpler prompt structure (might be less effective).")
            # Fallback simple prompt if chat template fails (less ideal for Gemma)
            prompt_text = f"<start_of_turn>user\n{system_message_content}\n{user_message_content}<end_of_turn>\n<start_of_turn>model\n"


        try:
            inputs = self.tokenizer(prompt_text, return_tensors="pt", padding=True, truncation=True).to(self.device)
            
            generation_params = {
                "input_ids": inputs.input_ids,
                "attention_mask": inputs.attention_mask,
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "do_sample": do_sample,
                "pad_token_id": self.tokenizer.pad_token_id if self.tokenizer.pad_token_id is not None else self.tokenizer.eos_token_id
            }
            # Some models benefit from other parameters like top_p, top_k
            if do_sample:
                 generation_params["top_p"] = 0.9 # Example value

            with torch.no_grad():
                generation_output = self.model.generate(**generation_params)
            
            num_input_tokens = inputs.input_ids.shape[1]
            generated_text = self.tokenizer.decode(generation_output[0, num_input_tokens:], skip_special_tokens=True)
            
            # Post-processing: Sometimes models add extra role tokens or instructions. Clean them up.
            # E.g., if it generates "<end_of_turn>" or similar, remove it.
            # This is highly model-specific.
            # generated_text = generated_text.split("<end_of_turn>")[0] # Example, adjust as needed
            
            print(f"NLG Debug: Final Prompt sent to LLM (after template):\n'''{prompt_text}'''")
            print(f"NLG Debug: Raw Generated Output (from LLM): '{generated_text.strip()}'")
            return generated_text.strip()

        except Exception as e:
            print(f"NLGService Error: Could not generate response. Error: {e}")
            # Provide more details for debugging if possible
            import traceback
            print(traceback.format_exc())
            return "I'm having a bit of trouble formulating a response right now."


# --- Example Usage (for testing this module directly) ---
if __name__ == "__main__":
    print("Initializing NLGService for testing with Gemma...")
    # IMPORTANT: Replace "google/gemma-1.1-2b-it" with the actual "google/gemma-3-1b-it" if it's available
    # and you have accepted terms on Hugging Face Hub if required.
    # For smaller models, you might not need `use_quantization=True` if you have enough VRAM/RAM
    # or if bfloat16 is sufficient. Test what works best for your hardware.
    nlg = NLGService(model_name_or_path="google/gemma-3-1b-it", use_quantization=False) # Using a known smaller Gemma, quantization off for bfloat16 focus

    if nlg.model and nlg.tokenizer:
        print("\nNLGService Initialized. Ready for generation.")
        
        test_cases = [
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
        print("NLGService could not be initialized. Check model loading errors above.")