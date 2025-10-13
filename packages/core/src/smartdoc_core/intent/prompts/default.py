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

        # Build phase-specific classification guidance
        phase_guidance = ""
        if context == "anamnesis":
            phase_guidance = """
CRITICAL MEDICATION CLASSIFICATION RULES:
- Basic medication questions (general, current meds, other meds) → "meds_current_known"
- Specific RA/arthritis medication questions (including uncertainty) → "meds_ra_specific_initial_query"
- Medication reconciliation/previous records/biologics/infliximab → "meds_full_reconciliation_query"
- Medical record access questions → "profile_medical_records"

MEDICATION EXAMPLES:
- "What medications is she taking?" → "meds_current_known"
- "Any other medications?" → "meds_current_known"
- "What does she take for arthritis?" → "meds_ra_specific_initial_query"
- "Not sure about RA medications?" → "meds_ra_specific_initial_query"
- "Complete medication list from previous hospitalizations" → "meds_full_reconciliation_query"
- "Any biologics or infliximab?" → "meds_full_reconciliation_query"
- "Check her previous records" → "profile_medical_records"

FALLBACK RULE:
- If the query does NOT fit any specific clinical intent above for this clinical scenario → "clarification"
- Use "clarification" when the doctor asks about information that is not available in this specific case
- Use "clarification" for nonsense input or unclear queries
"""
        elif context == "exam":
            phase_guidance = """
PHYSICAL EXAMINATION CLASSIFICATION RULES:
- Vital signs (BP, HR, temp, RR, O2) → "exam_vital"
- General appearance → "exam_general_appearance"
- Heart/cardiac exam → "exam_cardiovascular"
- Lung/respiratory exam → "exam_respiratory"

EXAM EXAMPLES:
- "What are her vital signs?" → "exam_vital"
- "Check her blood pressure" → "exam_vital"
- "Listen to her heart" → "exam_cardiovascular"
- "Examine her lungs" → "exam_respiratory"
- "How does she look?" → "exam_general_appearance"

FALLBACK RULE:
- If the query does NOT fit any physical examination intent for this clinical scenario → "clarification"
- Use "clarification" when the doctor asks about exam findings not available in this case
- Use "clarification" for nonsense input or unclear queries
"""
        elif context == "labs":
            phase_guidance = """
LABORATORY & IMAGING CLASSIFICATION RULES:
- General lab questions → "labs_general"
- Specific lab values (BNP, WBC, Hgb) → use specific intent
- Specific imaging (CXR, echo, CT) → use specific intent
- General imaging questions → "imaging_general"

LABS/IMAGING EXAMPLES:
- "Any lab results?" → "labs_general"
- "What's the BNP?" → "labs_bnp"
- "White blood cell count?" → "labs_wbc"
- "Chest X-ray?" → "imaging_chest_xray"
- "Echocardiogram?" → "imaging_echo"
- "CT chest?" → "imaging_ct_chest"
- "Any imaging studies?" → "imaging_general"

FALLBACK RULE:
- If the query does NOT fit any laboratory/imaging intent for this clinical scenario → "clarification"
- Use "clarification" when the doctor asks about tests/imaging not available in this case
- Use "clarification" for nonsense input or unclear queries
"""

        return f"""You are a clinical AI assistant in the {phase_description}

Classify the doctor's input into ONE of these EXACT intent IDs that are appropriate for the {context} context:

{chr(10).join(intent_lines)}

Doctor's input: "{doctor_input}"
{phase_guidance}
Respond with ONLY a JSON object in this exact format:
{{
    "intent_id": "exact_intent_id_from_list_above",
    "confidence": your_confidence_score_between_0_and_1,
    "explanation": "Brief explanation of why this specific intent was chosen for the {context} context"
}}

The intent_id MUST be one of the exact IDs listed above for the {context} context. Do not use any other intent names."""
