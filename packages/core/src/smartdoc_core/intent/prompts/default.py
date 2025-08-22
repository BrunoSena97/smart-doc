#!/usr/bin/env python3
"""
Default Intent Classification Prompt Builder

Implements the default prompt strategy for LLM intent classification
using structured JSON response format.
"""

from typing import Dict, Any
from .base import IntentPromptBuilder


class DefaultIntentPrompt(IntentPromptBuilder):
    """
    Default implementation of intent prompt builder.

    Creates structured prompts that request JSON responses with specific
    intent IDs, confidence scores, and explanations.
    """

    def build_general(
        self,
        *,
        doctor_input: str,
        intent_categories: Dict[str, Dict[str, Any]]
    ) -> str:
        """Build a general intent classification prompt."""

        # Create intent descriptions for the prompt
        intent_lines = []
        for intent_id, details in intent_categories.items():
            examples = details.get("examples", [])
            example_text = ", ".join(examples[:2]) if examples else "No examples"
            intent_lines.append(
                f"- {intent_id}: {details.get('description', 'No description')} (e.g., {example_text})"
            )

        return f"""You are a clinical AI assistant. Classify the doctor's input into ONE of these EXACT intent IDs:

{chr(10).join(intent_lines)}

Doctor's input: "{doctor_input}"

IMPORTANT: You MUST respond with one of the exact intent IDs listed above. For example:
- If asking about chief complaint or main problem → use EXACTLY "hpi_chief_complaint"
- If asking about medications → use EXACTLY "meds_current_known"
- If asking about heart exam → use EXACTLY "exam_cardiovascular"
- If asking about lung exam → use EXACTLY "exam_respiratory"
- If asking about vital signs → use EXACTLY "exam_vital"
- If asking about patient age → use EXACTLY "profile_age"

Respond with ONLY a JSON object in this exact format:
{{
    "intent_id": "exact_intent_id_from_list_above",
    "confidence": 0.95,
    "explanation": "Brief explanation of why this specific intent was chosen"
}}

The intent_id MUST be one of the exact IDs listed above. Do not use any other intent names."""

    def build_context_aware(
        self,
        *,
        doctor_input: str,
        context: str,
        filtered_intents: Dict[str, Dict[str, Any]]
    ) -> str:
        """Build a context-aware intent classification prompt."""

        # Create intent descriptions for the prompt
        intent_lines = []
        for intent_id, details in filtered_intents.items():
            examples = details.get("examples", [])
            example_text = ", ".join(examples[:2]) if examples else "No examples"
            intent_lines.append(
                f"- {intent_id}: {details.get('description', 'No description')} (e.g., {example_text})"
            )

        # Context-specific instructions
        phase_descriptions = {
            "anamnesis": "CLINICAL INTERVIEW (ANAMNESIS) phase. Focus on history-taking intents including chief complaint, onset, past medical history, medications, social history, and family history.",
            "exam": "PHYSICAL EXAMINATION phase. Focus on examination intents including vital signs, cardiovascular, respiratory, neurological, and other physical assessment intents.",
            "labs": "LABORATORY/IMAGING phase. Focus on diagnostic test intents including blood work, imaging studies, and other diagnostic procedures.",
        }

        phase_description = phase_descriptions.get(
            context, f"{context.upper()} phase."
        )

        return f"""You are a clinical AI assistant in the {phase_description}

Classify the doctor's input into ONE of these EXACT intent IDs that are appropriate for the {context} context:

{chr(10).join(intent_lines)}

Doctor's input: "{doctor_input}"

IMPORTANT: You MUST respond with one of the exact intent IDs listed above that are appropriate for the {context} phase. For example:
- If in anamnesis and asking about chief complaint → use EXACTLY "hpi_chief_complaint"
- If in anamnesis and asking about medications → use EXACTLY "meds_current_known"
- If in exam and asking about heart exam → use EXACTLY "exam_cardiovascular"
- If in exam and asking about lung exam → use EXACTLY "exam_respiratory"
- If in labs and asking for blood work → use an appropriate "labs_" intent
- If in labs and asking for imaging → use an appropriate "imaging_" intent

Respond with ONLY a JSON object in this exact format:
{{
    "intent_id": "exact_intent_id_from_list_above",
    "confidence": 0.95,
    "explanation": "Brief explanation of why this specific intent was chosen for the {context} context"
}}

The intent_id MUST be one of the exact IDs listed above for the {context} context. Do not use any other intent names."""
