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
        "Be concise, professional, and factual."
    )
    
    return f"""{persona}

The attending physician asked: "{doctor_question}"

Use the following test results/clinical information to provide a professional response:

{clinical_points}

Your response (professional and direct):"""
