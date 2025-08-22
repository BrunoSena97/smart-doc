"""
Base prompt builder interface

Defines the abstract interface for prompt builders used in discovery processing.
"""

from abc import ABC, abstractmethod
from typing import Dict


class PromptBuilder(ABC):
    """Abstract base class for prompt builders."""

    @abstractmethod
    def build(
        self,
        *,
        schema: Dict,
        all_labels: Dict,
        intent_id: str,
        doctor_question: str,
        patient_response: str,
        clinical_content: str
    ) -> str:
        """
        Build a prompt for LLM discovery processing.

        Args:
            schema: Complete discovery schema
            all_labels: Flattened label dictionary
            intent_id: Doctor's classified intent
            doctor_question: Original question from doctor
            patient_response: Patient/family response
            clinical_content: Raw clinical content

        Returns:
            Formatted prompt string for the LLM
        """
        pass
