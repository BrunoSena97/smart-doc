"""
Exam Objective Responder for physical examination context.

Implements objective clinical findings presentation for physical
examination contexts in the SmartDoc simulation engine.
"""

from typing import Dict, List
from .base import Responder


class ExamObjectiveResponder(Responder):
    """
    Responder for exam context using objective clinical findings.

    Provides direct, objective clinical findings when available.
    Returns simple message when findings are not available - no LLM generation needed.
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
        Build prompt for examination findings (not used for objective exam).

        Returns:
            Empty string as prompts are not used for objective findings
        """
        return ""  # Not used for objective exam findings

    def respond(
        self,
        *,
        intent_id: str,
        doctor_question: str,
        clinical_data: List[Dict],
        context: str
    ) -> str:
        """
        Generate response by concatenating objective findings.

        Args:
            intent_id: The classified intent ID
            doctor_question: The doctor's examination request
            clinical_data: List of clinical examination data
            context: The clinical context (should be 'exam')

        Returns:
            Objective clinical findings or simple message if not available
        """
        # Extract objective findings directly from clinical data
        findings = []
        for data in clinical_data:
            # For exam context, use actual content rather than summaries
            content = data.get("content")
            summary = data.get("summary")
            finding = content or summary

            if finding:
                findings.append(finding)

        if findings:
            # Return objective findings directly
            return " ".join(findings)
        else:
            # Simple message when examination findings not available
            return "That examination finding is not available in this case."
