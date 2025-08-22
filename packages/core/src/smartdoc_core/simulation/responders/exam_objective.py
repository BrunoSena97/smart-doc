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

    Provides direct, objective clinical findings without LLM generation,
    as physical examination results should be factual and unembellished.
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
        Build prompt for examination findings (not typically used).

        Physical examination responder typically doesn't use LLM generation,
        but this method is required by the interface.

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
            Concatenated objective clinical findings
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
            return " ".join(findings)
        else:
            return "No examination findings available for this request."
