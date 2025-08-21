#!/usr/bin/env python3
"""
LLM-based Discovery Processing Service for SmartDoc
Uses Ollama to analyze discovered clinical information and categorize it with fixed labels
"""

import requests
import json
from typing import Dict, Any, Optional, List
from smartdoc_core.utils.logger import sys_logger
from smartdoc_core.config.settings import config


class LLMDiscoveryProcessor:
    """
    LLM-based discovery processor that analyzes clinical information blocks
    and categorizes them using fixed labels to prevent duplication.
    """

    def __init__(self, ollama_url: str = None, model: str = None):
        """
        Initialize the LLM Discovery Processor.

        Args:
            ollama_url (str): URL for Ollama API (defaults to config value)
            model (str): Model name to use (defaults to config value)
        """
        self.ollama_url = ollama_url or config.OLLAMA_BASE_URL
        self.model = model or config.OLLAMA_MODEL

        # Define fixed discovery categories and labels
        self.discovery_schema = {
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

        # Create flat mapping of all possible labels
        self.all_labels = {}
        for category, labels in self.discovery_schema.items():
            for label, description in labels.items():
                self.all_labels[label] = {
                    "category": category,
                    "description": description,
                }

        sys_logger.log_system(
            "info",
            f"LLMDiscoveryProcessor initialized with {len(self.all_labels)} possible labels",
        )

    def process_discovery(
        self,
        intent_id: str,
        doctor_question: str,
        patient_response: str,
        clinical_content: str,
    ) -> Dict[str, Any]:
        """
        Process a discovery event and return structured categorization.

        Args:
            intent_id (str): The classified intent from the doctor's question
            doctor_question (str): The doctor's original question
            patient_response (str): The patient's/family's response
            clinical_content (str): The raw clinical content from the information block

        Returns:
            Dict containing structured discovery information with fixed labels
        """
        try:
            # Create prompt for LLM discovery processing
            prompt = self._create_discovery_prompt(
                intent_id, doctor_question, patient_response, clinical_content
            )

            # Call Ollama API
            response = self._call_ollama(prompt)

            # Parse LLM response
            result = self._parse_discovery_response(
                response, intent_id, clinical_content
            )

            sys_logger.log_system(
                "debug",
                f"Discovery processed: {intent_id} -> {result.get('label', 'unknown')} (confidence: {result.get('confidence', 0):.2f})",
            )

            return result

        except Exception as e:
            sys_logger.log_system("warning", f"LLM Discovery Processing error: {e}")
            # Fallback to rule-based classification
            return self._fallback_discovery_processing(
                intent_id, clinical_content, str(e)
            )

    def _create_discovery_prompt(
        self,
        intent_id: str,
        doctor_question: str,
        patient_response: str,
        clinical_content: str,
    ) -> str:
        """Create a prompt for the LLM to process discovery information."""

        # Create label options for the prompt
        label_list = []
        for label, info in self.all_labels.items():
            label_list.append(
                f"- {label}: {info['description']} (category: {info['category']})"
            )

        prompt = f"""You are a clinical AI assistant. Analyze this clinical information exchange and categorize it using ONE of the predefined labels.

CLINICAL CONTEXT:
- Doctor's Intent: {intent_id}
- Doctor asked: "{doctor_question}"
- Patient/Family responded: "{patient_response}"
- Clinical Content: "{clinical_content}"

AVAILABLE LABELS (choose EXACTLY one):
{chr(10).join(label_list)}

INSTRUCTIONS:
1. Analyze the clinical content and context
2. Choose the MOST APPROPRIATE label from the list above
3. Provide a clean, clinical summary suitable for medical records
4. Assess confidence in the categorization

RESPOND with ONLY a JSON object in this exact format:
{{
    "label": "exact_label_from_list_above",
    "category": "category_name",
    "summary": "clean clinical summary (1-2 sentences)",
    "confidence": 0.95,
    "reasoning": "brief explanation of label choice"
}}

The label MUST be one of the exact labels listed above. Do not create new labels."""

        return prompt

    def _call_ollama(self, prompt: str) -> str:
        """Call the Ollama API with the given prompt."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for consistent categorization
                "top_p": 0.9,
            },
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            f"{self.ollama_url}/api/generate", json=payload, headers=headers, timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            raise Exception(
                f"Ollama API error: {response.status_code} - {response.text}"
            )

    def _parse_discovery_response(
        self, llm_response: str, intent_id: str, clinical_content: str
    ) -> Dict[str, Any]:
        """Parse the LLM's JSON response into structured discovery data."""
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
                label = parsed.get("label", "")
                category = parsed.get("category", "")
                summary = parsed.get("summary", clinical_content)
                confidence = float(parsed.get("confidence", 0.5))
                reasoning = parsed.get("reasoning", "LLM classification")

                # Ensure label is valid
                if label not in self.all_labels:
                    # Try to find a close match or use fallback
                    label = self._find_fallback_label(intent_id, clinical_content)
                    category = self.all_labels[label]["category"]
                    confidence = max(
                        0.3, confidence * 0.5
                    )  # Reduce confidence for fallback

                # Ensure category matches label
                if label in self.all_labels:
                    category = self.all_labels[label]["category"]

                return {
                    "label": label,
                    "category": category,
                    "summary": summary,
                    "confidence": confidence,
                    "reasoning": reasoning,
                    "original_content": clinical_content,
                    "intent_context": intent_id,
                }

            else:
                # Fallback if JSON parsing fails
                return self._create_fallback_result(
                    intent_id, clinical_content, "Could not parse LLM response"
                )

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
        label: str = None,
        category: str = None,
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
