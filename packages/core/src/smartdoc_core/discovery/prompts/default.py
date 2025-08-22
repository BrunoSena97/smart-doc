"""
Default discovery prompt builder

Implements the standard prompt template for clinical discovery processing.
"""

from .base import PromptBuilder


class DefaultDiscoveryPrompt(PromptBuilder):
    """Default implementation of discovery prompt builder."""

    def build(
        self,
        *,
        schema,
        all_labels,
        intent_id,
        doctor_question,
        patient_response,
        clinical_content
    ) -> str:
        """Build the default discovery processing prompt."""
        label_lines = [
            f"- {label}: {info['description']} (category: {info['category']})"
            for label, info in all_labels.items()
        ]

        return f"""You are a clinical AI assistant. Analyze this clinical information exchange and categorize it using ONE of the predefined labels.

CLINICAL CONTEXT:
- Doctor's Intent: {intent_id}
- Doctor asked: "{doctor_question}"
- Patient/Family responded: "{patient_response}"
- Clinical Content: "{clinical_content}"

AVAILABLE LABELS (choose EXACTLY one):
{chr(10).join(label_lines)}

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
    "confidence": "a number between 0 and 1",
    "reasoning": "brief explanation of label choice"
}}

The label MUST be one of the exact labels listed above. Do not create new labels."""
