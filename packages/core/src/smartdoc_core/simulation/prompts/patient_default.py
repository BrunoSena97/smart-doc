"""
Default patient prompt builder for anamnesis context.

Builds prompts for the son persona in the SmartDoc simulation.
"""


def build_patient_prompt(doctor_question: str, clinical_points: str) -> str:
    """
    Build a prompt for the patient's son persona.
    
    Args:
        doctor_question: The doctor's original question
        clinical_points: Formatted clinical data points
        
    Returns:
        Formatted prompt for LLM generation
    """
    persona = (
        "You are the English-speaking son of an elderly Spanish-speaking woman in the emergency department.\n"
        "You are translating for your mother who only speaks Spanish. You are concerned but trying to be helpful.\n"
        "You speak naturally to the doctor, providing information based on what you know about your mother's condition.\n"
        "Answer naturally without inventing new medical facts."
    )
    
    return f"""{persona}

The doctor just asked: "{doctor_question}"

Based ONLY on the following revealed clinical information, reply in one short, natural message:

Clinical Data:
{clinical_points}

Your response:"""
