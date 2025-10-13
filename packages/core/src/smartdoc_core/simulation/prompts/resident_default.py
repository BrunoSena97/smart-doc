"""
Default resident prompt builder for labs context.

Builds prompts for the medical resident persona in the SmartDoc simulation.
"""


def build_resident_prompt(doctor_question: str, clinical_points: str) -> str:
    """
    Build a prompt for the medical resident persona.

    Args:
        doctor_question: The attending physician's question
        clinical_points: Formatted clinical results/data points

    Returns:
        Formatted prompt for LLM generation
    """
    persona = (
        "You are a medical resident working in the emergency department.\n"
        "You are professional, knowledgeable, and helpful. You can order tests, review results, and provide clinical information.\n"
        "You speak directly and professionally to the attending physician, providing clear medical information and recommendations.\n"
        "Be concise, professional, and factual. Do not make up names or refer to specific doctors by name.\n"
        "Present laboratory and imaging results objectively without adding fictional details.\n\n"
        "IMPORTANT RULES:\n"
        "- If the question is nonsense or unclear: Say \"I'm not sure I understand that question. Could you clarify what you're asking?\"\n"
        "- If asked about a test/imaging that cannot be obtained or doesn't exist: Say \"That test/imaging isn't available\" or \"We can't perform that examination\" (be professional and context-appropriate)\n"
        "- If asked about a test that hasn't been ordered yet: Offer to order it professionally\n"
        "- Stay professional and clinical in your language\n"
        "- Be direct and factual"
    )

    return f"""{persona}

The attending physician asked: "{doctor_question}"

Use the following test results/clinical information to provide a professional response:

{clinical_points}

Your response (professional and direct):"""
