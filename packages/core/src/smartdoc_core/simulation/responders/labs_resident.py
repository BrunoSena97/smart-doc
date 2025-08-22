"""
Labs Resident Responder for laboratory/imaging context.

Implements the medical resident persona for laboratory and imaging
contexts in the SmartDoc simulation engine.
"""

from typing import Dict, List
from .base import Responder
from smartdoc_core.simulation.prompts.resident_default import build_resident_prompt


class LabsResidentResponder(Responder):
    """
    Responder for labs context using medical resident persona.

    Generates professional, clinical responses as a medical resident
    providing laboratory and imaging results to the attending physician.
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
        Build prompt for medical resident persona.

        Args:
            intent_id: The classified intent ID
            doctor_question: The attending physician's question
            clinical_data: List of clinical data with label, content, summary
            context: The clinical context (should be 'labs')

        Returns:
            Formatted prompt for LLM generation
        """
        # Format clinical data points for the prompt
        points = []
        for data in clinical_data:
            label = data.get('label', data.get('type', 'Result'))
            # For labs context, prefer actual content over summary
            content = data.get('content', data.get('summary', ''))
            if content:
                points.append(f"- {label}: {content}")

        clinical_points = "\n".join(points) if points else "No specific results available"

        return build_resident_prompt(doctor_question, clinical_points)
