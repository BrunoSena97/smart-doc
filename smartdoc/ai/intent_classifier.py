#!/usr/bin/env python3
"""
LLM-based Intent Classification Service for SmartDoc
Uses Ollama to analyze doctor's input and classify clinical interview intents
"""

import requests
import json
from typing import Dict, Any, Optional
from smartdoc.utils.logger import sys_logger
from smartdoc.config.settings import config

class LLMIntentClassifier:
    """
    LLM-based intent classifier that uses Ollama to understand doctor's queries
    and map them to appropriate clinical interview intents.
    """

    def __init__(self, ollama_url: str = None, model: str = None):
        """
        Initialize the LLM Intent Classifier.

        Args:
            ollama_url (str): URL for Ollama API (defaults to config value)
            model (str): Model name to use (defaults to config value)
        """
        self.ollama_url = ollama_url or config.OLLAMA_BASE_URL
        self.model = model or config.OLLAMA_MODEL

        # Define clinical interview intent categories mapped to specific system intent IDs
        self.intent_categories = {
            # Patient Profile and Background
            "profile_age": {
                "description": "Questions about patient's age",
                "examples": ["How old is the patient?", "What is the patient's age?", "Patient age?"],
                "category": "profile"
            },
            "profile_language": {
                "description": "Questions about language barriers or patient's spoken language",
                "examples": ["Does the patient speak English?", "Language barrier?", "What language?"],
                "category": "profile"
            },
            "profile_social_context_historian": {
                "description": "Questions about who is providing the history",
                "examples": ["Who is giving the history?", "Is the patient alone?", "Family member present?"],
                "category": "profile"
            },
            "pmh_general": {
                "description": "Questions about past medical history in general",
                "examples": ["Past medical history?", "Any previous conditions?", "Medical history?"],
                "category": "past_medical_history"
            },
            "profile_medical_records": {
                "description": "Questions about medical record access or availability",
                "examples": ["Do you have medical records?", "Previous records available?", "Medical record access?"],
                "category": "profile"
            },

            # History of Present Illness (HPI)
            "hpi_source_of_history": {
                "description": "Questions about who is providing the current history",
                "examples": ["Who is telling me about this?", "Source of history?"],
                "category": "history_present_illness"
            },
            "hpi_chief_complaint": {
                "description": "Questions about the main complaint or what brought patient to clinic",
                "examples": ["What brings you here?", "Chief complaint?", "Main problem?", "What's wrong?"],
                "category": "chief_complaint"
            },
            "hpi_onset_duration_primary": {
                "description": "Questions about when symptoms started and their duration",
                "examples": ["When did this start?", "How long have you had this?", "Duration of symptoms?"],
                "category": "history_present_illness"
            },
            "hpi_associated_symptoms_general": {
                "description": "Questions about associated symptoms",
                "examples": ["Any other symptoms?", "Associated symptoms?", "What else do you feel?"],
                "category": "history_present_illness"
            },
            "hpi_pertinent_negatives": {
                "description": "Questions about important symptoms that are absent",
                "examples": ["Any chest pain?", "Any fever?", "Pertinent negatives?"],
                "category": "history_present_illness"
            },
            "hpi_recent_medical_care": {
                "description": "Questions about recent medical care or treatments",
                "examples": ["Recent doctor visits?", "Any recent treatment?", "Medical care recently?"],
                "category": "history_present_illness"
            },
            "hpi_travel_contacts": {
                "description": "Questions about recent travel or sick contacts",
                "examples": ["Any recent travel?", "Sick contacts?", "Been anywhere recently?"],
                "category": "history_present_illness"
            },

            # Medications
            "meds_current_known": {
                "description": "Questions about current medications",
                "examples": ["What medications are you taking?", "Current meds?", "Any prescriptions?"],
                "category": "medications"
            },
            "meds_uncertainty": {
                "description": "Questions when medication information is unclear",
                "examples": ["Not sure about medications?", "Medication uncertainty?"],
                "category": "medications"
            },
            "meds_ra_specific_initial_query": {
                "description": "Specific questions about rheumatoid arthritis medications",
                "examples": ["Rheumatoid arthritis medications?", "RA treatment?", "What does she take for her arthritis?", "What medications for RA?", "Arthritis drugs?", "What does she take for rheumatoid arthritis?"],
                "category": "medications"
            },
            "meds_full_reconciliation_query": {
                "description": "Follow-up questions requesting complete medication reconciliation or specific drug details",
                "examples": ["Can you check her records for RA medications?", "What specific drugs for arthritis?", "Any biologics?", "Complete medication list?", "Check previous records", "What about infliximab?", "Any immunosuppressive medications?"],
                "category": "medications"
            },
            "meds_other_meds_initial_query": {
                "description": "Questions about other medications beyond known ones",
                "examples": ["Any other medications?", "Other meds?", "Additional prescriptions?"],
                "category": "medications"
            },
            "meds_allergies": {
                "description": "Questions about medication allergies",
                "examples": ["Any drug allergies?", "Medication allergies?", "Allergic to any meds?"],
                "category": "medications"
            },

            # Physical Examination
            "exam_general_appearance": {
                "description": "General physical examination and appearance",
                "examples": ["Let me examine you", "Physical exam", "General appearance"],
                "category": "physical_exam_general"
            },
            "exam_vital": {
                "description": "Requests for vital signs",
                "examples": ["Check blood pressure", "Vital signs?", "Temperature?", "Heart rate?"],
                "category": "vital_signs"
            },
            "exam_cardiovascular": {
                "description": "Heart and cardiovascular examination",
                "examples": ["Listen to your heart", "Heart sounds", "Cardiovascular exam"],
                "category": "physical_exam_cardiovascular"
            },
            "exam_respiratory": {
                "description": "Lung and breathing examination",
                "examples": ["Listen to your lungs", "Breathing sounds", "Lung exam"],
                "category": "physical_exam_respiratory"
            },

            # Symptom-Specific HPI Questions
            "hpi_weight_loss": {
                "description": "Questions about weight loss or weight changes",
                "examples": ["Weight loss?", "Has patient lost weight?", "Any weight changes?"],
                "category": "history_present_illness"
            },
            "hpi_appetite": {
                "description": "Questions about appetite changes or eating habits",
                "examples": ["How is her appetite?", "Has she been eating well?", "Any appetite changes?", "Is she eating?"],
                "category": "history_present_illness"
            },
            "hpi_eating": {
                "description": "Questions specifically about eating habits and food intake",
                "examples": ["Has she been eating well lately?", "How much is she eating?", "Any changes in eating?"],
                "category": "history_present_illness"
            },
            "hpi_fever": {
                "description": "Questions about fever or temperature changes",
                "examples": ["Any fever?", "Temperature?", "Running a fever?"],
                "category": "history_present_illness"
            },
            "hpi_night_sweats": {
                "description": "Questions about night sweats",
                "examples": ["Night sweats?", "Sweating at night?", "Any sweats?"],
                "category": "history_present_illness"
            },
            "hpi_cough": {
                "description": "Questions about cough or sputum production",
                "examples": ["Any cough?", "Coughing?", "Sputum production?"],
                "category": "history_present_illness"
            },
            "hpi_shortness_of_breath": {
                "description": "Questions about dyspnea or breathing difficulty",
                "examples": ["Short of breath?", "Breathing problems?", "Dyspnea?"],
                "category": "history_present_illness"
            },
            "hpi_chest_pain": {
                "description": "Questions about chest pain or chest discomfort",
                "examples": ["Chest pain?", "Any chest discomfort?", "Pain in chest?"],
                "category": "history_present_illness"
            },

            # Diagnostic and Testing
            "labs_general": {
                "description": "Questions about laboratory tests or results",
                "examples": ["Lab results?", "Blood tests?", "Laboratory findings?"],
                "category": "diagnostics"
            },
            "imaging_chest": {
                "description": "Questions about chest imaging",
                "examples": ["Chest X-ray?", "Chest CT?", "Chest imaging?"],
                "category": "diagnostics"
            },
            "imaging_general": {
                "description": "Questions about imaging studies",
                "examples": ["Any imaging?", "Radiology results?", "Scan results?"],
                "category": "diagnostics"
            },

            # General Communication
            "general_greeting": {
                "description": "General greetings and conversation starters",
                "examples": ["Hello", "Good morning", "How are you?"],
                "category": "general"
            },
            "clarification": {
                "description": "Asking for clarification or more details",
                "examples": ["Can you clarify?", "Tell me more", "What do you mean?"],
                "category": "clarification"
            }
        }

        # Create reverse mapping from broad categories to specific intent IDs
        self.category_to_intents = {}
        for intent_id, details in self.intent_categories.items():
            category = details.get("category", "general")
            if category not in self.category_to_intents:
                self.category_to_intents[category] = []
            self.category_to_intents[category].append(intent_id)

        sys_logger.log_system("info", f"LLMIntentClassifier initialized with model: {self.model}")

    def classify_intent(self, doctor_input: str, context: str = None) -> Dict[str, Any]:
        """
        Classify the doctor's input into a clinical interview intent.

        Args:
            doctor_input (str): The doctor's question or statement
            context (str): Clinical context (anamnesis, exam, labs) for filtering intents

        Returns:
            Dict containing intent classification results compatible with dialogue manager
        """
        if not doctor_input or not doctor_input.strip():
            return {
                "intent_id": "empty_input",
                "confidence": 0.0,
                "explanation": "No input provided",
                "action_type": "generic_response_or_state_change",
                "target_details": {"response_key": "empty_input"}
            }

        # Use context-aware classification if context provided
        if context:
            return self.classify_intent_with_context(doctor_input, context)

        # Create prompt for LLM intent classification
        prompt = self._create_classification_prompt(doctor_input)

        try:
            # Call Ollama API
            response = self._call_ollama(prompt)

            # Parse LLM response
            result = self._parse_llm_response(response, doctor_input)

            sys_logger.log_system("debug", f"LLM Intent Classification: '{doctor_input}' -> {result['intent_id']} (confidence: {result['confidence']:.2f})")

            return result

        except Exception as e:
            sys_logger.log_system("warning", f"LLM Intent Classification error: {e}")
            # Fallback to keyword-based classification
            return self._fallback_classification(doctor_input, str(e))

    def classify_intent_with_context(self, doctor_input: str, context: str) -> Dict[str, Any]:
        """
        Classify the doctor's input into a clinical interview intent based on clinical context.

        Args:
            doctor_input (str): The doctor's question or statement
            context (str): Clinical context (anamnesis, exam, labs)

        Returns:
            Dict containing intent classification results compatible with dialogue manager
        """
        if not doctor_input or not doctor_input.strip():
            return {
                "intent_id": "empty_input",
                "confidence": 0.0,
                "explanation": "No input provided",
                "action_type": "generic_response_or_state_change",
                "target_details": {"response_key": "empty_input"}
            }

        # Define context-specific intent mappings
        context_intents = {
            "anamnesis": {
                # History taking intents
                "hpi_chief_complaint", "hpi_onset_duration_primary", "hpi_location_primary",
                "hpi_character_quality", "hpi_severity", "hpi_alleviating_factors",
                "hpi_aggravating_factors", "hpi_associated_symptoms_general",
                "hpi_timing_pattern", "pmh_general", "pmh_chronic_conditions",
                "pmh_hospitalizations", "pmh_surgeries", "pmh_cardiac_conditions",
                "pmh_pulmonary_conditions", "pmh_gi_conditions", "pmh_neuro_conditions",
                "meds_current_known", "meds_allergies", "meds_recent_changes",
                "social_smoking", "social_alcohol", "social_occupation",
                "social_exercise", "social_diet", "family_cardiac",
                "family_diabetes", "family_cancer", "family_general",
                "profile_age", "profile_gender", "profile_occupation",
                # General communication
                "general_greeting", "clarification", "confirmation"
            },
            "exam": {
                # Physical examination intents
                "exam_general_appearance", "exam_vital", "exam_cardiovascular",
                "exam_respiratory", "exam_abdominal", "exam_neurological",
                "exam_musculoskeletal", "exam_skin", "exam_head_neck",
                "exam_extremities", "exam_lymph_nodes", "exam_psychiatric",
                "exam_eyes", "exam_ears", "exam_throat",
                # General communication
                "general_greeting", "clarification", "confirmation"
            },
            "labs": {
                # Laboratory and imaging intents
                "labs_cbc", "labs_bmp", "labs_liver", "labs_cardiac_enzymes",
                "labs_lipid", "labs_thyroid", "labs_coagulation", "labs_urinalysis",
                "labs_cultures", "labs_other", "imaging_chest_xray",
                "imaging_ecg", "imaging_echo", "imaging_ct", "imaging_mri",
                "imaging_ultrasound", "imaging_nuclear", "imaging_other",
                # General communication
                "general_greeting", "clarification", "confirmation"
            }
        }

        # Get valid intents for this context
        valid_intents = context_intents.get(context, set())
        if not valid_intents:
            # If context not recognized, use general classification
            return self.classify_intent(doctor_input)

        # Filter intent categories to only include valid intents for this context
        filtered_intents = {
            intent_id: details
            for intent_id, details in self.intent_categories.items()
            if intent_id in valid_intents
        }

        # Create context-aware prompt
        prompt = self._create_context_aware_prompt(doctor_input, context, filtered_intents)

        try:
            # Call Ollama API
            response = self._call_ollama(prompt)

            # Parse LLM response with context validation
            result = self._parse_llm_response_with_context(response, doctor_input, valid_intents)

            sys_logger.log_system("debug", f"Context-Aware LLM Intent Classification [{context}]: '{doctor_input}' -> {result['intent_id']} (confidence: {result['confidence']:.2f})")

            return result

        except Exception as e:
            sys_logger.log_system("warning", f"Context-Aware LLM Intent Classification error: {e}")
            # Fallback to context-aware keyword classification
            return self._fallback_classification_with_context(doctor_input, context, valid_intents, str(e))

    def _create_classification_prompt(self, doctor_input: str) -> str:
        """Create a prompt for the LLM to classify the doctor's intent."""

        # Create intent descriptions for the prompt - use exact intent IDs
        intent_list = []
        for intent_id, details in self.intent_categories.items():
            examples = ", ".join(details["examples"][:2])  # First 2 examples
            intent_list.append(f"- {intent_id}: {details['description']} (e.g., {examples})")

        prompt = f"""You are a clinical AI assistant. Classify the doctor's input into ONE of these EXACT intent IDs:

{chr(10).join(intent_list)}

Doctor's input: "{doctor_input}"

IMPORTANT: You MUST respond with one of the exact intent IDs listed above. For example:
- If asking about chief complaint or main problem -> use EXACTLY "hpi_chief_complaint"
- If asking about medications -> use EXACTLY "meds_current_known"
- If asking about heart exam -> use EXACTLY "exam_cardiovascular"
- If asking about lung exam -> use EXACTLY "exam_respiratory"
- If asking about vital signs -> use EXACTLY "exam_vitals"
- If asking about patient age -> use EXACTLY "profile_age"

Respond with ONLY a JSON object in this exact format:
{{
    "intent_id": "exact_intent_id_from_list_above",
    "confidence": 0.95,
    "explanation": "Brief explanation of why this specific intent was chosen"
}}

The intent_id MUST be one of the exact IDs listed above. Do not use any other intent names."""

        return prompt

    def _create_context_aware_prompt(self, doctor_input: str, context: str, filtered_intents: Dict[str, Any]) -> str:
        """Create a context-aware prompt for the LLM to classify the doctor's intent."""

        # Create intent descriptions for the prompt - use exact intent IDs from filtered set
        intent_list = []
        for intent_id, details in filtered_intents.items():
            examples = ", ".join(details["examples"][:2])  # First 2 examples
            intent_list.append(f"- {intent_id}: {details['description']} (e.g., {examples})")

        # Context-specific instructions
        context_instructions = {
            "anamnesis": "You are in the CLINICAL INTERVIEW (ANAMNESIS) phase. Focus on history-taking intents including chief complaint, onset, past medical history, medications, social history, and family history.",
            "exam": "You are in the PHYSICAL EXAMINATION phase. Focus on examination intents including vital signs, cardiovascular, respiratory, neurological, and other physical assessment intents.",
            "labs": "You are in the LABORATORY/IMAGING phase. Focus on diagnostic test intents including blood work, imaging studies, and other diagnostic procedures."
        }

        context_instruction = context_instructions.get(context, f"You are in the {context.upper()} phase.")

        prompt = f"""You are a clinical AI assistant in a medical simulation. {context_instruction}

Classify the doctor's input into ONE of these EXACT intent IDs that are appropriate for the {context} context:

{chr(10).join(intent_list)}

Doctor's input: "{doctor_input}"

IMPORTANT: You MUST respond with one of the exact intent IDs listed above that are appropriate for the {context} phase. For example:
- If in anamnesis and asking about chief complaint -> use EXACTLY "hpi_chief_complaint"
- If in anamnesis and asking about medications -> use EXACTLY "meds_current_known"
- If in exam and asking about heart exam -> use EXACTLY "exam_cardiovascular"
- If in exam and asking about lung exam -> use EXACTLY "exam_respiratory"
- If in labs and asking for blood work -> use an appropriate "labs_" intent
- If in labs and asking for imaging -> use an appropriate "imaging_" intent

Respond with ONLY a JSON object in this exact format:
{{
    "intent_id": "exact_intent_id_from_list_above",
    "confidence": 0.95,
    "explanation": "Brief explanation of why this specific intent was chosen for the {context} context"
}}

The intent_id MUST be one of the exact IDs listed above for the {context} context. Do not use any other intent names."""

        return prompt

    def _call_ollama(self, prompt: str) -> str:
        """Call the Ollama API with the given prompt."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            raise Exception(f"Ollama API error: {response.status_code} - {response.text}")

    def _parse_llm_response(self, llm_response: str, original_input: str) -> Dict[str, Any]:
        """Parse the LLM's JSON response into a structured result."""
        try:
            # Try to extract JSON from response
            llm_response = llm_response.strip()

            # Handle cases where LLM adds extra text around JSON
            if "{" in llm_response and "}" in llm_response:
                start = llm_response.find("{")
                end = llm_response.rfind("}") + 1
                json_str = llm_response[start:end]

                parsed = json.loads(json_str)

                # Validate required fields
                intent_id = parsed.get("intent_id", "general")
                confidence = float(parsed.get("confidence", 0.5))
                explanation = parsed.get("explanation", "LLM classification")

                # Ensure intent_id is valid
                if intent_id not in self.intent_categories:
                    intent_id = "clarification"
                    confidence = max(0.3, confidence * 0.5)  # Reduce confidence for invalid intent

                return {
                    "intent_id": intent_id,
                    "confidence": confidence,
                    "explanation": explanation,
                    "original_input": original_input
                }

            else:
                # Fallback if JSON parsing fails
                return {
                    "intent_id": "clarification",
                    "confidence": 0.3,
                    "explanation": "Could not parse LLM response",
                    "raw_response": llm_response
                }

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Fallback for parsing errors
            return {
                "intent_id": "clarification",
                "confidence": 0.2,
                "explanation": f"Response parsing error: {str(e)}",
                "raw_response": llm_response
            }

    def _parse_llm_response_with_context(self, llm_response: str, original_input: str, valid_intents: set) -> Dict[str, Any]:
        """Parse the LLM's JSON response with context validation."""
        try:
            # Try to extract JSON from response
            llm_response = llm_response.strip()

            # Handle cases where LLM adds extra text around JSON
            if "{" in llm_response and "}" in llm_response:
                start = llm_response.find("{")
                end = llm_response.rfind("}") + 1
                json_str = llm_response[start:end]

                parsed = json.loads(json_str)

                # Validate required fields
                intent_id = parsed.get("intent_id", "clarification")
                confidence = float(parsed.get("confidence", 0.5))
                explanation = parsed.get("explanation", "Context-aware LLM classification")

                # Ensure intent_id is valid for this context
                if intent_id not in valid_intents:
                    # Try to find a similar intent in valid set or default to clarification
                    intent_id = "clarification" if "clarification" in valid_intents else list(valid_intents)[0]
                    confidence = max(0.3, confidence * 0.5)  # Reduce confidence for invalid intent
                    explanation += " (adjusted for context)"

                return {
                    "intent_id": intent_id,
                    "confidence": confidence,
                    "explanation": explanation,
                    "original_input": original_input
                }

            else:
                # Fallback if JSON parsing fails
                fallback_intent = "clarification" if "clarification" in valid_intents else list(valid_intents)[0]
                return {
                    "intent_id": fallback_intent,
                    "confidence": 0.3,
                    "explanation": "Could not parse LLM response (context-aware fallback)",
                    "raw_response": llm_response
                }

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Fallback for parsing errors
            fallback_intent = "clarification" if "clarification" in valid_intents else list(valid_intents)[0]
            return {
                "intent_id": fallback_intent,
                "confidence": 0.2,
                "explanation": f"Response parsing error: {str(e)} (context-aware fallback)",
                "raw_response": llm_response
            }

    def _fallback_classification(self, doctor_input: str, error_msg: str) -> Dict[str, Any]:
        """
        Fallback classification using simple keyword matching when LLM is unavailable.
        """
        input_lower = doctor_input.lower()

        # Simple keyword-based classification using specific intent IDs
        intent_id = "clarification"  # Default

        if any(word in input_lower for word in ["what brings", "main problem", "chief complaint", "why here"]):
            intent_id = "hpi_chief_complaint"
        elif any(word in input_lower for word in ["age", "old", "elderly", "years"]):
            intent_id = "profile_age"
        elif any(word in input_lower for word in ["medications", "meds", "taking", "prescriptions"]):
            intent_id = "meds_current_known"
        elif any(word in input_lower for word in ["heart", "cardiovascular", "pulse", "cardiac"]):
            intent_id = "exam_cardiovascular"
        elif any(word in input_lower for word in ["lungs", "breathing", "respiratory", "chest sounds"]):
            intent_id = "exam_respiratory"
        elif any(word in input_lower for word in ["blood pressure", "vital signs", "temperature", "bp"]):
            intent_id = "exam_vital"
        elif any(word in input_lower for word in ["when", "start", "duration", "how long"]):
            intent_id = "hpi_onset_duration_primary"
        elif any(word in input_lower for word in ["symptoms", "other", "associated", "feel"]):
            intent_id = "hpi_associated_symptoms_general"
        elif any(word in input_lower for word in ["medical history", "past", "previous", "pmh"]):
            intent_id = "pmh_general"
        elif any(word in input_lower for word in ["examine", "physical", "check", "look at"]):
            intent_id = "exam_general_appearance"
        elif any(word in input_lower for word in ["hello", "hi", "good morning", "good afternoon"]):
            intent_id = "general_greeting"

        # Build simplified response for intent-driven discovery
        result = {
            "intent_id": intent_id,
            "confidence": 0.6 if intent_id != "clarification" else 0.3,
            "explanation": f"Keyword-based fallback (LLM error: {error_msg})",
            "error": error_msg
        }

        return result

    def _fallback_classification_with_context(self, doctor_input: str, context: str, valid_intents: set, error_msg: str) -> Dict[str, Any]:
        """
        Context-aware fallback classification using simple keyword matching when LLM is unavailable.
        """
        input_lower = doctor_input.lower()

        # Context-specific keyword mappings
        intent_id = "clarification"  # Default

        if context == "anamnesis":
            # History-taking keywords
            if any(word in input_lower for word in ["what brings", "main problem", "chief complaint", "why here"]):
                intent_id = "hpi_chief_complaint" if "hpi_chief_complaint" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["age", "old", "elderly", "years"]):
                intent_id = "profile_age" if "profile_age" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["medications", "meds", "taking", "prescriptions"]):
                intent_id = "meds_current_known" if "meds_current_known" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["when", "start", "duration", "how long"]):
                intent_id = "hpi_onset_duration_primary" if "hpi_onset_duration_primary" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["medical history", "past", "previous", "pmh"]):
                intent_id = "pmh_general" if "pmh_general" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["smoking", "alcohol", "social"]):
                intent_id = "social_smoking" if "social_smoking" in valid_intents else "clarification"

        elif context == "exam":
            # Physical examination keywords
            if any(word in input_lower for word in ["heart", "cardiovascular", "pulse", "cardiac"]):
                intent_id = "exam_cardiovascular" if "exam_cardiovascular" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["lungs", "breathing", "respiratory", "chest sounds"]):
                intent_id = "exam_respiratory" if "exam_respiratory" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["blood pressure", "vital signs", "temperature", "bp"]):
                intent_id = "exam_vital" if "exam_vital" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["examine", "physical", "check", "look at"]):
                intent_id = "exam_general_appearance" if "exam_general_appearance" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["abdomen", "stomach", "belly"]):
                intent_id = "exam_abdominal" if "exam_abdominal" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["neuro", "neurological", "reflexes"]):
                intent_id = "exam_neurological" if "exam_neurological" in valid_intents else "clarification"

        elif context == "labs":
            # Laboratory and imaging keywords
            if any(word in input_lower for word in ["blood work", "cbc", "complete blood count"]):
                intent_id = "labs_cbc" if "labs_cbc" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["chest x-ray", "cxr", "chest xray"]):
                intent_id = "imaging_chest_xray" if "imaging_chest_xray" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["ecg", "ekg", "electrocardiogram"]):
                intent_id = "imaging_ecg" if "imaging_ecg" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["ct scan", "ct", "computed tomography"]):
                intent_id = "imaging_ct" if "imaging_ct" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["echo", "echocardiogram", "ultrasound heart"]):
                intent_id = "imaging_echo" if "imaging_echo" in valid_intents else "clarification"
            elif any(word in input_lower for word in ["liver function", "liver enzymes"]):
                intent_id = "labs_liver" if "labs_liver" in valid_intents else "clarification"

        # General keywords applicable to all contexts
        if intent_id == "clarification":
            if any(word in input_lower for word in ["hello", "hi", "good morning", "good afternoon"]):
                intent_id = "general_greeting" if "general_greeting" in valid_intents else "clarification"

        # Ensure the selected intent is valid for this context
        if intent_id not in valid_intents:
            intent_id = "clarification" if "clarification" in valid_intents else list(valid_intents)[0]

        # Build simplified response for intent-driven discovery
        result = {
            "intent_id": intent_id,
            "confidence": 0.6 if intent_id != "clarification" else 0.3,
            "explanation": f"Context-aware keyword-based fallback for {context} (LLM error: {error_msg})",
            "error": error_msg,
            "context": context
        }

        return result

    def get_intent_info(self, intent_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific intent category."""
        return self.intent_categories.get(intent_id)

    def list_all_intents(self) -> Dict[str, Dict[str, Any]]:
        """Get all available intent categories."""
        return self.intent_categories.copy()


# Example usage and testing
if __name__ == "__main__":
    # Test the LLM Intent Classifier
    classifier = LLMIntentClassifier()

    test_inputs = [
        "What brings you here today?",
        "Can you describe your chest pain?",
        "Let me listen to your heart",
        "I'd like to order a chest X-ray",
        "What medications are you currently taking?",
        "I think you have heart failure, let's start treatment",
        "Any family history of heart disease?",
        "Let me check your blood pressure",
        "We need to do some blood tests",
        "Based on the examination, you likely have pneumonia"
    ]

    print("🧠 Testing LLM Intent Classifier")
    print("=" * 50)

    for test_input in test_inputs:
        result = classifier.classify_intent(test_input)
        print(f"Input: '{test_input}'")
        print(f"Intent: {result['intent_id']} (confidence: {result['confidence']:.2f})")
        print(f"Explanation: {result['explanation']}")
        print()
