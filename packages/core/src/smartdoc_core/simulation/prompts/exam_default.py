"""
Default exam prompt builder for physical examination context.

Provides templating for objective examination findings with LLM support for unavailable findings.
"""


def build_exam_prompt(doctor_question: str, clinical_points: str) -> str:
    """
    Build a prompt for physical examination findings.

    Used when examination findings are not available in the case data,
    or when the question is nonsense/unclear.

    Args:
        doctor_question: The doctor's examination request
        clinical_points: Formatted examination findings (may be empty or "No findings available")

    Returns:
        Formatted prompt for LLM generation
    """
    persona = (
        "You are providing objective physical examination findings in a clinical simulation.\n"
        "Be factual, clinical, and objective. Use proper medical terminology.\n\n"
        "IMPORTANT RULES:\n"
        "- If the question is nonsense or unclear: Say \"I'm not sure what examination you're requesting. Could you clarify?\"\n"
        "- If the examination doesn't exist in our case data: Say \"That examination finding is not available for this case.\"\n"
        "- If it's a valid examination but not documented: Say \"This examination was not performed\" or \"No significant findings noted for this system.\"\n"
        "- Be brief and clinical\n"
        "- Do not invent findings\n"
        "- Stay objective and professional"
    )

    return f"""{persona}

Examination requested: "{doctor_question}"

Available findings:
{clinical_points}

Your response (brief and clinical):"""
