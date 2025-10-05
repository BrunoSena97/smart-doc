#!/usr/bin/env python3
"""
LLM-based Intent Classification Service for SmartDoc (Refactored)
Uses configurable LLM providers to analyze doctor's input and classify clinical interview intents
"""

import json
import time
from typing import Dict, Any, Optional, Set
from smartdoc_core.utils.logger import sys_logger
from smartdoc_core.config.settings import config

# Reuse shared LLM providers
from smartdoc_core.llm.providers import OllamaProvider
from smartdoc_core.intent.prompts.default import DefaultIntentPrompt
from smartdoc_core.intent.types import IntentLLMOut


class LLMIntentClassifier:
    """
    LLM-based intent classifier with modular architecture.

    Uses dependency injection for provider and prompt builder to support
    different LLM services and customizable prompts.
    """

    def __init__(
        self,
        provider=None,
        prompt_builder=None,
        intent_categories: Optional[Dict[str, Dict[str, Any]]] = None
    ):
        """
        Initialize the LLM Intent Classifier.

        Args:
            provider: LLM provider instance (defaults to Ollama from config)
            prompt_builder: Prompt builder instance (defaults to DefaultIntentPrompt)
            intent_categories: Custom intent categories (defaults to built-in categories)
        """
        # Use dependency injection with sensible defaults
        self.provider = provider or OllamaProvider(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
        self.prompt_builder = prompt_builder or DefaultIntentPrompt()
        self.intent_categories = intent_categories or self._default_intent_categories()

        # Build category index for lookup
        self.category_to_intents = {}
        for intent_id, details in self.intent_categories.items():
            category = details.get("category", "general")
            if category not in self.category_to_intents:
                self.category_to_intents[category] = []
            self.category_to_intents[category].append(intent_id)

        # Simple circuit breaker state
        self._fail_count = 0
        self._open_until: float = 0.0

        model_name = getattr(self.provider, 'model', 'unknown')
        sys_logger.log_system(
            "info",
            f"LLMIntentClassifier initialized with {len(self.intent_categories)} intents (model: {model_name})"
        )

    # ---- Public API ----
    def classify_intent(self, doctor_input: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Classify the doctor's input into a clinical interview intent.

        Args:
            doctor_input: The doctor's question or statement
            context: Clinical context (anamnesis, exam, labs) for filtering intents

        Returns:
            Dict containing intent classification results compatible with dialogue manager
        """
        if not doctor_input or not doctor_input.strip():
            return self._empty_input_result()

        if context:
            return self.classify_intent_with_context(doctor_input, context)

        # Build general prompt
        prompt = self.prompt_builder.build_general(
            doctor_input=doctor_input,
            intent_categories=self.intent_categories
        )

        return self._generate_and_parse(prompt, doctor_input, valid_intents=None)

    def classify_intent_with_context(self, doctor_input: str, context: str) -> Dict[str, Any]:
        """
        Classify the doctor's input into a clinical interview intent based on clinical context.

        Args:
            doctor_input: The doctor's question or statement
            context: Clinical context (anamnesis, exam, labs)

        Returns:
            Dict containing intent classification results compatible with dialogue manager
        """
        if not doctor_input or not doctor_input.strip():
            return self._empty_input_result()

        # Get valid intents for this context
        valid_intents = self._valid_intents_for_context(context)
        if not valid_intents:
            # Unknown context -> use general classification
            return self.classify_intent(doctor_input)

        # Filter to only include valid intents for this context
        filtered_intents = {
            intent_id: details
            for intent_id, details in self.intent_categories.items()
            if intent_id in valid_intents
        }

        # Build context-aware prompt
        prompt = self.prompt_builder.build_context_aware(
            doctor_input=doctor_input,
            context=context,
            filtered_intents=filtered_intents
        )

        return self._generate_and_parse(prompt, doctor_input, valid_intents=valid_intents, context=context)

    # ---- Core LLM processing with resilience ----
    def _generate_and_parse(
        self,
        prompt: str,
        original_input: str,
        valid_intents: Optional[Set[str]],
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate LLM response and parse with circuit breaker protection."""

        # Check circuit breaker
        now = time.time()
        if now < self._open_until:
            return self._fallback_classification_with_optional_context(
                original_input, context, valid_intents, "circuit_breaker_open"
            )

        try:
            # Call LLM provider
            raw_response = self.provider.generate(
                prompt,
                temperature=0.1,
                top_p=0.9,
                timeout_s=60
            )

            # Parse and validate response
            parsed_result = self._parse_llm_json(raw_response, original_input, valid_intents)

            # Reset failure count on success
            self._fail_count = 0

            sys_logger.log_system(
                "debug",
                f"LLM Intent Classification: '{original_input}' -> {parsed_result['intent_id']} (confidence: {parsed_result['confidence']:.2f})"
            )

            return parsed_result

        except Exception as e:
            # Track failures for circuit breaker
            self._fail_count += 1
            if self._fail_count >= 3:
                self._open_until = time.time() + 60  # Open circuit for 1 minute

            sys_logger.log_system("warning", f"LLM Intent Classification error: {e}")
            return self._fallback_classification_with_optional_context(
                original_input, context, valid_intents, str(e)
            )

    def _parse_llm_json(
        self,
        llm_text: str,
        original_input: str,
        valid_intents: Optional[Set[str]]
    ) -> Dict[str, Any]:
        """Parse LLM JSON response with validation."""

        text = llm_text.strip()
        if "{" not in text or "}" not in text:
            return self._fallback_parse(original_input, "no_json_found", valid_intents)

        # Extract JSON from response
        json_start = text.find("{")
        json_end = text.rfind("}") + 1
        json_str = text[json_start:json_end]

        try:
            # Parse JSON
            data = json.loads(json_str)

            # Validate with Pydantic
            dto = IntentLLMOut(**{
                "intent_id": data.get("intent_id"),
                "confidence": float(data.get("confidence", 0.5)),
                "explanation": data.get("explanation") or "LLM classification"
            })

            intent_id = dto.intent_id
            confidence = dto.confidence

            # Validate intent ID exists in our categories
            if intent_id not in self.intent_categories:
                intent_id, confidence = self._adjust_invalid_intent(intent_id, confidence, valid_intents)

            # Validate intent ID is valid for context
            if valid_intents and intent_id not in valid_intents:
                intent_id, confidence = self._adjust_invalid_intent(intent_id, confidence, valid_intents)

            return {
                "intent_id": intent_id,
                "confidence": confidence,
                "explanation": dto.explanation,
                "original_input": original_input,
            }

        except Exception as e:
            return self._fallback_parse(original_input, f"parse_error: {e}", valid_intents)

    def _adjust_invalid_intent(
        self,
        invalid_intent: str,
        confidence: float,
        valid_intents: Optional[Set[str]]
    ) -> tuple[str, float]:
        """Adjust invalid intent to a valid fallback."""

        # Prefer clarification if allowed, else use first valid intent
        if valid_intents:
            new_intent = "clarification" if "clarification" in valid_intents else next(iter(valid_intents))
        else:
            new_intent = "clarification" if "clarification" in self.intent_categories else next(iter(self.intent_categories))

        # Reduce confidence for invalid intent
        new_confidence = max(0.3, confidence * 0.5)
        return new_intent, new_confidence

    def _fallback_parse(
        self,
        original_input: str,
        reason: str,
        valid_intents: Optional[Set[str]]
    ) -> Dict[str, Any]:
        """Fallback parsing when JSON parsing fails."""

        fallback_intent = "clarification"
        if valid_intents and fallback_intent not in valid_intents:
            fallback_intent = next(iter(valid_intents))
        elif fallback_intent not in self.intent_categories:
            fallback_intent = next(iter(self.intent_categories))

        return {
            "intent_id": fallback_intent,
            "confidence": 0.3,
            "explanation": f"Could not parse LLM response ({reason})",
            "original_input": original_input,
        }

    def _fallback_classification_with_optional_context(
        self,
        doctor_input: str,
        context: Optional[str],
        valid_intents: Optional[Set[str]],
        error_msg: str
    ) -> Dict[str, Any]:
        """Route to appropriate fallback based on context availability."""

        if context and valid_intents:
            return self._fallback_classification_with_context(doctor_input, context, valid_intents, error_msg)
        return self._fallback_classification(doctor_input, error_msg)

    # ---- Helper methods ----
    def _valid_intents_for_context(self, context: str) -> Set[str]:
        """Get valid intent IDs for the given clinical context."""

        # Define context-specific intent mappings - ONLY intents supported by case file
        context_intents = {
            "anamnesis": {
                # Profile and demographics
                "profile_age",
                "profile_language",
                "profile_social_context_historian",
                "profile_medical_records",
                # History of Present Illness
                "hpi_chief_complaint",
                "hpi_shortness_of_breath",
                "hpi_cough",
                "hpi_weight_changes",
                "hpi_onset_duration_primary",
                "hpi_associated_symptoms_general",
                "hpi_pertinent_negatives",
                "hpi_chest_pain",
                "hpi_fever",
                "hpi_chills",
                "hpi_recent_medical_care",
                # Past Medical History
                "pmh_general",
                # Medications
                "meds_current_known",
                "meds_uncertainty",
                "meds_ra_specific_initial_query",
                "meds_full_reconciliation_query",
                "meds_other_meds_initial_query",
                # General communication
                "general_greeting",
                "clarification",
            },
            "exam": {
                # Physical examination intents - ONLY those in case file
                "exam_vital",
                "exam_general_appearance",
                "exam_respiratory",
                "exam_cardiovascular",
                # General communication
                "general_greeting",
                "clarification",
            },
            "labs": {
                # Laboratory and imaging intents - ONLY those in case file
                "labs_general",
                "labs_bnp",
                "labs_wbc",
                "labs_hemoglobin",
                "imaging_chest",
                "imaging_general",
                # General communication
                "general_greeting",
                "clarification",
            },
        }

        return context_intents.get(context, set())

    def _empty_input_result(self) -> Dict[str, Any]:
        """Return result for empty input."""
        return {
            "intent_id": "empty_input",
            "confidence": 0.0,
            "explanation": "No input provided",
            "action_type": "generic_response_or_state_change",
            "target_details": {"response_key": "empty_input"},
        }

    def _default_intent_categories(self) -> Dict[str, Dict[str, Any]]:
        """Get the default intent categories dictionary."""
        return {
            # Patient Profile and Background
            "profile_age": {
                "description": "Questions about patient's age",
                "examples": [
                    "How old is the patient?",
                    "What is the patient's age?",
                    "Patient age?",
                ],
                "category": "profile",
            },
            "profile_language": {
                "description": "Questions about language barriers or patient's spoken language",
                "examples": [
                    "Does the patient speak English?",
                    "Language barrier?",
                    "What language?",
                ],
                "category": "profile",
            },
            "profile_social_context_historian": {
                "description": "Questions about who is providing the history",
                "examples": [
                    "Who is giving the history?",
                    "Is the patient alone?",
                    "Family member present?",
                ],
                "category": "profile",
            },
            "pmh_general": {
                "description": "Questions about past medical history in general",
                "examples": [
                    "Past medical history?",
                    "Any previous conditions?",
                    "Medical history?",
                ],
                "category": "past_medical_history",
            },
            "profile_medical_records": {
                "description": "Questions about medical record access or availability",
                "examples": [
                    "Do you have medical records?",
                    "Previous records available?",
                    "Medical record access?",
                ],
                "category": "profile",
            },
            # History of Present Illness (HPI)
            "hpi_chief_complaint": {
                "description": "Questions about the main complaint or what brought patient to clinic",
                "examples": [
                    "What brings you here?",
                    "Chief complaint?",
                    "Main problem?",
                    "What's wrong?",
                ],
                "category": "chief_complaint",
            },
            "hpi_onset_duration_primary": {
                "description": "Questions about when symptoms started and their duration",
                "examples": [
                    "When did this start?",
                    "How long have you had this?",
                    "Duration of symptoms?",
                ],
                "category": "history_present_illness",
            },
            "hpi_associated_symptoms_general": {
                "description": "Questions about associated symptoms",
                "examples": [
                    "Any other symptoms?",
                    "Associated symptoms?",
                    "What else do you feel?",
                ],
                "category": "history_present_illness",
            },
            "hpi_pertinent_negatives": {
                "description": "Questions about important symptoms that are absent",
                "examples": ["Any chest pain?", "Any fever?", "Pertinent negatives?"],
                "category": "history_present_illness",
            },
            "hpi_recent_medical_care": {
                "description": "Questions about recent medical care or treatments",
                "examples": [
                    "Recent doctor visits?",
                    "Any recent treatment?",
                    "Medical care recently?",
                ],
                "category": "history_present_illness",
            },
            # Medications
            "meds_current_known": {
                "description": "Questions about current medications (Level 1 - basic medication list)",
                "examples": [
                    "What medications are you taking?",
                    "What medications is she currently taking?",
                    "Current meds?",
                    "Any prescriptions?",
                    "What drugs is she on?",
                    "Tell me about her medications",
                ],
                "category": "medications",
            },
            "meds_uncertainty": {
                "description": "Questions when medication information is unclear or uncertain",
                "examples": [
                    "Not sure about medications?",
                    "Medication uncertainty?",
                    "Are there other medications we don't know about?",
                    "Uncertain about her medication list?",
                ],
                "category": "medications",
            },
            "meds_ra_specific_initial_query": {
                "description": "Specific questions about rheumatoid arthritis medications (Level 2 - RA medication uncertainty)",
                "examples": [
                    "What medications does she take for rheumatoid arthritis?",
                    "What does she take for her arthritis?",
                    "RA medications?",
                    "Rheumatoid arthritis treatment?",
                    "What medications for RA?",
                    "Arthritis drugs?",
                    "What does she take for her RA?",
                    "Any arthritis medications?",
                ],
                "category": "medications",
            },
            "meds_full_reconciliation_query": {
                "description": "Complete medication reconciliation requests (Level 3 - reveals critical infliximab)",
                "examples": [
                    "I need a complete medication reconciliation from previous hospitalizations",
                    "Can you get her complete medication list from previous hospitalizations?",
                    "Check her previous hospital records for medications",
                    "What specific drugs for arthritis from old records?",
                    "Any biologics or immunosuppressive medications?",
                    "Complete medication list from all sources?",
                    "Check previous medical records for RA medications",
                    "What about infliximab or other biologics?",
                    "Any TNF inhibitors?",
                    "Medication reconciliation from other hospitals",
                ],
                "category": "medications",
            },
            "meds_other_meds_initial_query": {
                "description": "Questions about other medications beyond currently known ones",
                "examples": [
                    "Any other medications?",
                    "Other meds we should know about?",
                    "Additional prescriptions?",
                    "What other drugs is she taking?",
                ],
                "category": "medications",
            },
            # Physical Examination
            "exam_general_appearance": {
                "description": "General physical examination and appearance",
                "examples": [
                    "Let me examine you",
                    "Physical exam",
                    "General appearance",
                ],
                "category": "physical_exam_general",
            },
            "exam_vital": {
                "description": "Requests for vital signs",
                "examples": [
                    "Check blood pressure",
                    "Vital signs?",
                    "Temperature?",
                    "Heart rate?",
                ],
                "category": "vital_signs",
            },
            "exam_cardiovascular": {
                "description": "Heart and cardiovascular examination",
                "examples": [
                    "Listen to your heart",
                    "Heart sounds",
                    "Cardiovascular exam",
                ],
                "category": "physical_exam_cardiovascular",
            },
            "exam_respiratory": {
                "description": "Lung and breathing examination",
                "examples": ["Listen to your lungs", "Breathing sounds", "Lung exam"],
                "category": "physical_exam_respiratory",
            },
            # Symptom-Specific HPI Questions
            "hpi_fever": {
                "description": "Questions about fever or temperature changes",
                "examples": ["Any fever?", "Temperature?", "Running a fever?"],
                "category": "history_present_illness",
            },
            "hpi_cough": {
                "description": "Questions about cough or sputum production",
                "examples": ["Any cough?", "Coughing?", "Sputum production?"],
                "category": "history_present_illness",
            },
            "hpi_shortness_of_breath": {
                "description": "Questions about dyspnea or breathing difficulty",
                "examples": ["Short of breath?", "Breathing problems?", "Dyspnea?"],
                "category": "history_present_illness",
            },
            "hpi_chest_pain": {
                "description": "Questions about chest pain or chest discomfort",
                "examples": ["Chest pain?", "Any chest discomfort?", "Pain in chest?"],
                "category": "history_present_illness",
            },
            "hpi_chills": {
                "description": "Questions about chills or feeling cold",
                "examples": ["Any chills?", "Feeling cold?", "Chills or rigors?"],
                "category": "history_present_illness",
            },
            "hpi_weight_changes": {
                "description": "Questions about weight loss or weight changes",
                "examples": [
                    "Weight loss?",
                    "Any weight changes?",
                    "Has patient lost weight?",
                ],
                "category": "history_present_illness",
            },
            # Diagnostic and Testing
            "labs_general": {
                "description": "Questions about laboratory tests or results",
                "examples": ["Lab results?", "Blood tests?", "Laboratory findings?"],
                "category": "diagnostics",
            },
            "labs_bnp": {
                "description": "Questions about BNP or pro-BNP levels",
                "examples": ["BNP level?", "What's the pro-BNP?", "Brain natriuretic peptide?"],
                "category": "diagnostics",
            },
            "labs_wbc": {
                "description": "Questions about white blood cell count",
                "examples": ["White blood cell count?", "WBC?", "What's the white count?"],
                "category": "diagnostics",
            },
            "labs_hemoglobin": {
                "description": "Questions about hemoglobin levels",
                "examples": ["Hemoglobin level?", "What's the Hgb?", "Hematocrit?"],
                "category": "diagnostics",
            },
            "imaging_chest": {
                "description": "Questions about chest imaging",
                "examples": ["Chest X-ray?", "Chest CT?", "Chest imaging?"],
                "category": "diagnostics",
            },
            "imaging_general": {
                "description": "Questions about imaging studies",
                "examples": ["Any imaging?", "Radiology results?", "Scan results?"],
                "category": "diagnostics",
            },
            # General Communication
            "general_greeting": {
                "description": "General greetings and conversation starters",
                "examples": ["Hello", "Good morning", "How are you?"],
                "category": "general",
            },
            "clarification": {
                "description": "Asking for clarification or more details",
                "examples": ["Can you clarify?", "Tell me more", "What do you mean?"],
                "category": "clarification",
            },
        }

    # ---- Existing fallback methods (preserved for compatibility) ----
    def _fallback_classification(
        self, doctor_input: str, error_msg: str
    ) -> Dict[str, Any]:
        """
        Fallback classification using simple keyword matching when LLM is unavailable.
        """
        input_lower = doctor_input.lower()

        # Simple keyword-based classification using specific intent IDs
        intent_id = "clarification"  # Default

        if any(
            word in input_lower
            for word in ["what brings", "main problem", "chief complaint", "why here"]
        ):
            intent_id = "hpi_chief_complaint"
        elif any(word in input_lower for word in ["age", "old", "elderly", "years"]):
            intent_id = "profile_age"
        elif any(
            word in input_lower
            for word in ["complete medication", "medication reconciliation", "previous hospitalizations", "hospital records", "biologics", "infliximab", "tnf"]
        ):
            intent_id = "meds_full_reconciliation_query"
        elif any(
            word in input_lower
            for word in ["arthritis", "rheumatoid", "ra medications", "arthritis medications"]
        ):
            intent_id = "meds_ra_specific_initial_query"
        elif any(
            word in input_lower
            for word in ["medications", "meds", "taking", "prescriptions"]
        ):
            intent_id = "meds_current_known"
        elif any(
            word in input_lower
            for word in ["heart", "cardiovascular", "pulse", "cardiac"]
        ):
            intent_id = "exam_cardiovascular"
        elif any(
            word in input_lower
            for word in ["lungs", "breathing", "respiratory", "chest sounds"]
        ):
            intent_id = "exam_respiratory"
        elif any(
            word in input_lower
            for word in ["blood pressure", "vital signs", "temperature", "bp"]
        ):
            intent_id = "exam_vital"
        elif any(
            word in input_lower for word in ["when", "start", "duration", "how long"]
        ):
            intent_id = "hpi_onset_duration_primary"
        elif any(
            word in input_lower for word in ["symptoms", "other", "associated", "feel"]
        ):
            intent_id = "hpi_associated_symptoms_general"
        elif any(
            word in input_lower
            for word in ["medical history", "past", "previous", "pmh"]
        ):
            intent_id = "pmh_general"
        elif any(
            word in input_lower for word in ["examine", "physical", "check", "look at"]
        ):
            intent_id = "exam_general_appearance"
        elif any(
            word in input_lower
            for word in ["hello", "hi", "good morning", "good afternoon"]
        ):
            intent_id = "general_greeting"

        # Build simplified response for intent-driven discovery
        result = {
            "intent_id": intent_id,
            "confidence": 0.6 if intent_id != "clarification" else 0.3,
            "explanation": f"Keyword-based fallback (LLM error: {error_msg})",
            "error": error_msg,
        }

        return result

    def _fallback_classification_with_context(
        self, doctor_input: str, context: str, valid_intents: Set[str], error_msg: str
    ) -> Dict[str, Any]:
        """
        Context-aware fallback classification using simple keyword matching when LLM is unavailable.
        """
        input_lower = doctor_input.lower()

        # Context-specific keyword mappings
        intent_id = "clarification"  # Default

        if context == "anamnesis":
            # History-taking keywords
            if any(
                word in input_lower
                for word in [
                    "what brings",
                    "main problem",
                    "chief complaint",
                    "why here",
                ]
            ):
                intent_id = (
                    "hpi_chief_complaint"
                    if "hpi_chief_complaint" in valid_intents
                    else "clarification"
                )
            elif any(
                word in input_lower for word in ["age", "old", "elderly", "years"]
            ):
                intent_id = (
                    "profile_age" if "profile_age" in valid_intents else "clarification"
                )
            elif any(
                word in input_lower
                for word in ["complete medication", "medication reconciliation", "previous hospitalizations", "hospital records", "biologics", "infliximab", "tnf"]
            ):
                intent_id = (
                    "meds_full_reconciliation_query"
                    if "meds_full_reconciliation_query" in valid_intents
                    else "clarification"
                )
            elif any(
                word in input_lower
                for word in ["arthritis", "rheumatoid", "ra medications", "arthritis medications", " ra ", "ra?", "ra.", "for ra"]
            ):
                intent_id = (
                    "meds_ra_specific_initial_query"
                    if "meds_ra_specific_initial_query" in valid_intents
                    else "clarification"
                )
            elif any(
                word in input_lower
                for word in ["medications", "meds", "taking", "prescriptions"]
            ):
                intent_id = (
                    "meds_current_known"
                    if "meds_current_known" in valid_intents
                    else "clarification"
                )
            elif any(
                word in input_lower
                for word in ["when", "start", "duration", "how long"]
            ):
                intent_id = (
                    "hpi_onset_duration_primary"
                    if "hpi_onset_duration_primary" in valid_intents
                    else "clarification"
                )
            elif any(
                word in input_lower
                for word in ["medical history", "past", "previous", "pmh"]
            ):
                intent_id = (
                    "pmh_general" if "pmh_general" in valid_intents else "clarification"
                )

        elif context == "exam":
            # Physical examination keywords
            if any(
                word in input_lower
                for word in ["heart", "cardiovascular", "pulse", "cardiac"]
            ):
                intent_id = (
                    "exam_cardiovascular"
                    if "exam_cardiovascular" in valid_intents
                    else "clarification"
                )
            elif any(
                word in input_lower
                for word in ["lungs", "breathing", "respiratory", "chest sounds"]
            ):
                intent_id = (
                    "exam_respiratory"
                    if "exam_respiratory" in valid_intents
                    else "clarification"
                )
            elif any(
                word in input_lower
                for word in ["blood pressure", "vital signs", "temperature", "bp"]
            ):
                intent_id = (
                    "exam_vital" if "exam_vital" in valid_intents else "clarification"
                )
            elif any(
                word in input_lower
                for word in ["examine", "physical", "check", "look at"]
            ):
                intent_id = (
                    "exam_general_appearance"
                    if "exam_general_appearance" in valid_intents
                    else "clarification"
                )

        elif context == "labs":
            # Laboratory and imaging keywords
            if any(
                word in input_lower
                for word in ["blood work", "cbc", "complete blood count"]
            ):
                intent_id = (
                    "labs_general" if "labs_general" in valid_intents else "clarification"
                )
            elif any(
                word in input_lower for word in ["chest x-ray", "cxr", "chest xray"]
            ):
                intent_id = (
                    "imaging_chest"
                    if "imaging_chest" in valid_intents
                    else "clarification"
                )
            elif any(
                word in input_lower for word in ["imaging", "radiology", "scan"]
            ):
                intent_id = (
                    "imaging_general"
                    if "imaging_general" in valid_intents
                    else "clarification"
                )

        # General keywords applicable to all contexts
        if intent_id == "clarification":
            if any(
                word in input_lower
                for word in ["hello", "hi", "good morning", "good afternoon"]
            ):
                intent_id = (
                    "general_greeting"
                    if "general_greeting" in valid_intents
                    else "clarification"
                )

        # Ensure the selected intent is valid for this context
        if intent_id not in valid_intents:
            intent_id = (
                "clarification"
                if "clarification" in valid_intents
                else next(iter(valid_intents))
            )

        # Build simplified response for intent-driven discovery
        result = {
            "intent_id": intent_id,
            "confidence": 0.6 if intent_id != "clarification" else 0.3,
            "explanation": f"Context-aware keyword-based fallback for {context} (LLM error: {error_msg})",
            "error": error_msg,
            "context": context,
        }

        return result

    # ---- Utility methods ----
    def get_intent_info(self, intent_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific intent category."""
        return self.intent_categories.get(intent_id)

    def list_all_intents(self) -> Dict[str, Dict[str, Any]]:
        """Get all available intent categories."""
        return self.intent_categories.copy()
