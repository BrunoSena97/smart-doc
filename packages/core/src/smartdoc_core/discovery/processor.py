#!/usr/bin/env python3
"""
LLM-based Discovery Processing Service for SmartDoc
Uses configurable LLM providers to analyze discovered clinical information and categorize it with fixed labels
"""

import json
import time
from typing import Dict, Any, Optional
from smartdoc_core.utils.logger import sys_logger
from smartdoc_core.config.settings import config
from smartdoc_core.llm.providers import OllamaProvider
from .prompts.default import DefaultDiscoveryPrompt
from .types import DiscoveryLLMOut


class LLMDiscoveryProcessor:
    """
    LLM-based discovery processor that analyzes clinical information blocks
    and categorizes them using fixed labels to prevent duplication.

    Uses dependency injection for provider and prompt builder to support
    different LLM services and customizable prompts.
    """

    def __init__(self, provider=None, prompt_builder=None, discovery_schema: Optional[Dict[str, Dict[str, str]]] = None):
        """
        Initialize the LLM Discovery Processor.

        Args:
            provider: LLM provider instance (defaults to Ollama from config)
            prompt_builder: Prompt builder instance (defaults to DefaultDiscoveryPrompt)
            discovery_schema: Custom discovery schema (defaults to built-in schema)
        """
        # Use dependency injection with sensible defaults
        self.provider = provider or OllamaProvider(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
        self.prompt_builder = prompt_builder or DefaultDiscoveryPrompt()

        # Use provided schema or default
        self.discovery_schema = discovery_schema or self._default_schema()
        self.all_labels = self._flatten_labels(self.discovery_schema)

        # Simple circuit breaker state
        self._fail_count = 0
        self._open_until: float = 0.0

        sys_logger.log_system(
            "info",
            f"LLMDiscoveryProcessor initialized with {len(self.all_labels)} possible labels",
        )

    def _default_schema(self) -> Dict[str, Dict[str, str]]:
        """Get the default discovery schema."""
        return {
            "patient_profile": {
                "Patient Age": "Patient's age and demographic information",
                "Language Barrier": "Communication and language needs",
                "Medical Records": "Availability and access to previous medical records",
                "Social Context": "Family members present, who provides history",
            },
            "medical_history": {
                "Past Medical History": "Chronic conditions, previous diagnoses",
                "Previous Treatments": "Past medical interventions and treatments",
                "Recent Medical Care": "Recent doctor visits, treatments, or hospitalizations",
            },
            "current_medications": {
                "Current Medications": "Currently prescribed medications",
                "Blood Pressure Medications": "Antihypertensive medications",
                "Diabetes Medications": "Diabetic treatment medications",
                "Arthritis Medications": "Rheumatoid arthritis and joint medications",
                "Recent Antibiotics": "Recently prescribed antibiotic treatments",
                "Medication Uncertainty": "Unknown or unclear medication information",
            },
            "presenting_symptoms": {
                "Chief Complaint": "Primary reason for visit",
                "Onset and Duration": "When symptoms started and progression",
                "Shortness of Breath": "Dyspnea and breathing difficulties",
                "Cough Symptoms": "Cough characteristics and patterns",
                "Weight Loss": "Unintentional weight loss",
                "Appetite Changes": "Changes in eating habits and appetite",
                "Associated Symptoms": "Other related symptoms",
            },
            "physical_examination": {
                "Vital Signs": "Temperature, blood pressure, heart rate, respiratory rate, oxygen saturation",
                "General Appearance": "Overall patient appearance and demeanor",
                "Heart Examination": "Cardiovascular examination findings",
                "Lung Examination": "Respiratory examination findings",
            },
            "diagnostic_results": {
                "Lab Results": "Blood tests and laboratory findings",
                "Chest X-ray": "Chest imaging results",
                "CT Scan": "Computed tomography findings",
                "Echocardiogram": "Cardiac ultrasound results",
                "Other Imaging": "Additional imaging studies",
            },
            "clinical_assessment": {
                "Pertinent Negatives": "Important symptoms that are absent",
                "Risk Factors": "Identified risk factors for conditions",
                "Clinical Concerns": "Medical concerns and differential diagnoses",
            },
        }

    def _flatten_labels(self, schema: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
        """Create flat mapping of all possible labels."""
        all_labels = {}
        for category, labels in schema.items():
            for label, description in labels.items():
                all_labels[label] = {
                    "category": category,
                    "description": description,
                }
        return all_labels

    def process_discovery(
        self,
        intent_id: str,
        doctor_question: str,
        patient_response: str,
        clinical_content: str,
        *,
        agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a discovery event and return structured categorization.

        Args:
            intent_id: The classified intent from the doctor's question
            doctor_question: The doctor's original question
            patient_response: The patient's/family's response
            clinical_content: The raw clinical content from the information block
            agent: Optional agent type for prompt customization

        Returns:
            Dict containing structured discovery information with fixed labels
        """
        # Simple circuit breaker check
        now = time.time()
        if now < self._open_until:
            return self._fallback_discovery_processing(
                intent_id, clinical_content, "circuit_open"
            )

        try:
            # Build prompt using injected prompt builder
            prompt = self.prompt_builder.build(
                schema=self.discovery_schema,
                all_labels=self.all_labels,
                intent_id=intent_id,
                doctor_question=doctor_question,
                patient_response=patient_response,
                clinical_content=clinical_content,
            )

            # Call LLM via injected provider
            response = self.provider.generate(
                prompt, temperature=0.1, top_p=0.9, timeout_s=30
            )

            # Parse LLM response
            result = self._parse_discovery_response(
                response, intent_id, clinical_content
            )

            # Reset circuit breaker on success
            self._fail_count = 0

            sys_logger.log_system(
                "debug",
                f"Discovery processed: {intent_id} -> {result.get('label', 'unknown')} "
                f"(confidence: {result.get('confidence', 0):.2f})",
            )

            return result

        except Exception as e:
            # Circuit breaker logic
            self._fail_count += 1
            if self._fail_count >= 3:
                self._open_until = time.time() + 60  # 1 minute cool-off

            sys_logger.log_system(
                "warning",
                f"LLM Discovery Processing failed (#{self._fail_count}): {e}"
            )

            # Fallback to rule-based classification
            return self._fallback_discovery_processing(
                intent_id, clinical_content, str(e)
            )

    def _parse_discovery_response(
        self, llm_response: str, intent_id: str, clinical_content: str
    ) -> Dict[str, Any]:
        """Parse the LLM's JSON response into structured discovery data using Pydantic."""
        try:
            # Try to extract JSON from response
            text = llm_response.strip()

            # Handle cases where LLM adds extra text around JSON
            if "{" not in text or "}" not in text:
                return self._create_fallback_result(
                    intent_id, clinical_content, "no_json"
                )

            json_str = text[text.find("{"):text.rfind("}") + 1]
            data = json.loads(json_str)

            # Validate with Pydantic
            dto = DiscoveryLLMOut(
                label=data.get("label", ""),
                category=data.get("category", ""),
                summary=data.get("summary", clinical_content),
                confidence=float(data.get("confidence", 0.5)),
                reasoning=data.get("reasoning", "LLM classification"),
            )

            label = dto.label
            category = dto.category
            confidence = dto.confidence

            # Ensure label is valid
            if label not in self.all_labels:
                # Try to find a close match or use fallback
                label = self._find_fallback_label(intent_id, clinical_content)
                category = self.all_labels[label]["category"]
                confidence = max(0.3, confidence * 0.5)  # Reduce confidence for fallback

            # Ensure category matches label
            if label in self.all_labels:
                category = self.all_labels[label]["category"]

            return {
                "label": label,
                "category": category,
                "summary": dto.summary,
                "confidence": confidence,
                "reasoning": dto.reasoning,
                "original_content": clinical_content,
                "intent_context": intent_id,
            }

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Fallback for parsing errors
            return self._create_fallback_result(
                intent_id, clinical_content, f"Response parsing error: {str(e)}"
            )

    def _fallback_discovery_processing(
        self, intent_id: str, clinical_content: str, error_msg: str
    ) -> Dict[str, Any]:
        """
        Fallback discovery processing using rule-based matching when LLM is unavailable.
        """
        content_lower = clinical_content.lower()

        # Rule-based label assignment
        label = self._find_fallback_label(intent_id, clinical_content)
        category = self.all_labels[label]["category"]

        return self._create_fallback_result(
            intent_id, clinical_content, error_msg, label, category
        )

    def _find_fallback_label(self, intent_id: str, clinical_content: str) -> str:
        """Find the most appropriate label using fallback rules."""
        content_lower = clinical_content.lower()

        # Intent-based mapping for common cases
        intent_to_label_mapping = {
            "profile_age": "Patient Age",
            "profile_language": "Language Barrier",
            "profile_medical_records": "Medical Records",
            "profile_social_context_historian": "Social Context",
            "hpi_chief_complaint": "Chief Complaint",
            "hpi_onset_duration_primary": "Onset and Duration",
            "hpi_shortness_of_breath": "Shortness of Breath",
            "hpi_cough": "Cough Symptoms",
            "hpi_weight_changes": "Weight Loss",
            "hpi_appetite": "Appetite Changes",
            "hpi_eating": "Appetite Changes",
            "hpi_associated_symptoms_general": "Associated Symptoms",
            "hpi_pertinent_negatives": "Pertinent Negatives",
            "hpi_chest_pain": "Pertinent Negatives",
            "hpi_fever": "Pertinent Negatives",
            "hpi_chills": "Pertinent Negatives",
            "hpi_weight_changes": "Weight Loss",
            "hpi_recent_medical_care": "Recent Medical Care",
            "meds_current_known": "Current Medications",  # Mixed BP and diabetes meds
            "meds_uncertainty": "Medication Uncertainty",
            "meds_ra_specific_initial_query": "Arthritis Medications",
            "meds_full_reconciliation_query": "Arthritis Medications",
            "meds_other_meds_initial_query": "Arthritis Medications",
            "exam_vital": "Vital Signs",
            "exam_general_appearance": "General Appearance",
            "exam_cardiovascular": "Heart Examination",
            "exam_respiratory": "Lung Examination",
            "labs_general": "Lab Results",
            "imaging_chest": "Chest X-ray",
            "imaging_general": "Other Imaging",
            "pmh_general": "Past Medical History",
        }

        # Try intent-based mapping first
        if intent_id in intent_to_label_mapping:
            return intent_to_label_mapping[intent_id]

        # Content-based fallback rules
        if any(word in content_lower for word in ["age", "elderly", "years", "old"]):
            return "Patient Age"
        elif any(
            word in content_lower
            for word in ["spanish", "language", "translat", "speak"]
        ):
            return "Language Barrier"
        elif any(
            word in content_lower
            for word in ["vital", "temperature", "blood pressure", "heart rate"]
        ):
            return "Vital Signs"
        elif any(
            word in content_lower
            for word in ["lisinopril", "atenolol", "blood pressure"]
        ):
            return "Blood Pressure Medications"
        elif any(
            word in content_lower for word in ["infliximab", "arthritis", "rheumatoid"]
        ):
            return "Arthritis Medications"
        elif any(word in content_lower for word in ["diabetes", "diabetic"]):
            return "Diabetes Medications"
        elif any(word in content_lower for word in ["short", "breath", "dyspnea"]):
            return "Shortness of Breath"
        elif any(word in content_lower for word in ["cough", "coughing"]):
            return "Cough Symptoms"
        elif any(word in content_lower for word in ["weight", "eating", "appetite"]):
            return "Weight Loss"
        elif any(
            word in content_lower for word in ["heart", "cardiac", "cardiovascular"]
        ):
            return "Heart Examination"
        elif any(
            word in content_lower for word in ["lung", "respiratory", "breathing"]
        ):
            return "Lung Examination"
        elif any(word in content_lower for word in ["x-ray", "chest", "imaging"]):
            return "Chest X-ray"
        elif any(word in content_lower for word in ["lab", "blood", "test"]):
            return "Lab Results"

        # Default fallback
        return "Clinical Concerns"

    def _create_fallback_result(
        self,
        intent_id: str,
        clinical_content: str,
        error_msg: str,
        label: Optional[str] = None,
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a fallback result structure."""
        if not label:
            label = self._find_fallback_label(intent_id, clinical_content)

        if not category:
            category = self.all_labels[label]["category"]

        return {
            "label": label,
            "category": category,
            "summary": clinical_content,
            "confidence": 0.6,
            "reasoning": f"Fallback classification (LLM error: {error_msg})",
            "original_content": clinical_content,
            "intent_context": intent_id,
            "error": error_msg,
        }

    def get_label_info(self, label: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific label."""
        return self.all_labels.get(label)

    def get_category_labels(self, category: str) -> Dict[str, str]:
        """Get all labels for a specific category."""
        return {
            label: info["description"]
            for label, info in self.all_labels.items()
            if info["category"] == category
        }

    def list_all_labels(self) -> Dict[str, Dict[str, Any]]:
        """Get all available labels and their information."""
        return self.all_labels.copy()

    def get_discovery_schema(self) -> Dict[str, Dict[str, str]]:
        """Get the complete discovery schema."""
        return self.discovery_schema.copy()


# Example usage and testing
if __name__ == "__main__":
    # Test the LLM Discovery Processor
    processor = LLMDiscoveryProcessor()

    test_cases = [
        {
            "intent_id": "profile_age",
            "doctor_question": "How old is the patient?",
            "patient_response": "She's elderly, yes. I help her because she only speaks Spanish.",
            "clinical_content": "Patient is elderly, approximately 70+ years old. Family member present to assist with translation.",
        },
        {
            "intent_id": "meds_ra_specific_initial_query",
            "doctor_question": "What medications does she take for her arthritis?",
            "patient_response": "Oh yes! The doctor found her old records. She's been getting infusions for her arthritis - something called infliximab.",
            "clinical_content": "Patient receives infliximab infusions for rheumatoid arthritis treatment. Multiple treatments over past months.",
        },
        {
            "intent_id": "exam_vital_signs",
            "doctor_question": "Let me check her vital signs",
            "patient_response": "*The nurse takes vital signs* Temperature is a little high at 99.9°F...",
            "clinical_content": "Vital signs: T 99.9°F, HR 105, BP 140/70, RR 24, O2 sat 89%",
        },
    ]

    print("🔍 Testing LLM Discovery Processor")
    print("=" * 50)

    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        result = processor.process_discovery(**test_case)
        print(f"Label: {result['label']}")
        print(f"Category: {result['category']}")
        print(f"Summary: {result['summary']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Reasoning: {result['reasoning']}")
        print()
