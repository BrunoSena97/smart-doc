"""
Anamnesis Son Responder for patient history context.

Implements the patient's son persona for anamnesis conversations
in the SmartDoc simulation engine.
"""

from typing import Dict, List
from .base import Responder
from smartdoc_core.simulation.prompts.patient_default import build_patient_prompt


class AnamnesisSonResponder(Responder):
    """
    Responder for anamnesis context using patient's son persona.

    Generates natural, conversational responses as the English-speaking son
    translating for his Spanish-speaking mother in the emergency department.
    """

    def build_prompt(
        self,
        *,
        intent_id: str,
        doctor_question: str,
        clinical_data: List[Dict],
        context: str
    ) -> str:
        """
        Build prompt for patient's son persona.

        Args:
            intent_id: The classified intent ID
            doctor_question: The doctor's original question
            clinical_data: List of clinical data with label, summary, content
            context: The clinical context (should be 'anamnesis')

        Returns:
            Formatted prompt for LLM generation
        """
        # Format clinical data points for the prompt
        points = []
        for data in clinical_data:
            label = data.get('label', data.get('type', 'Information'))
            summary = data.get('summary', data.get('content', ''))
            if summary:
                points.append(f"- {label}: {summary}")

        clinical_points = "\n".join(points) if points else "No specific clinical data"

        return build_patient_prompt(doctor_question, clinical_points)
