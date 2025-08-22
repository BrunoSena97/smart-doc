"""
Default exam prompt builder for physical examination context.

Provides basic templating for objective examination findings.
"""


def build_exam_prompt(doctor_question: str, clinical_points: str) -> str:
    """
    Build a prompt for physical examination findings.
    
    Note: Physical exam typically doesn't need LLM generation as it provides
    direct objective findings, but this template is available if needed.
    
    Args:
        doctor_question: The doctor's examination request
        clinical_points: Formatted examination findings
        
    Returns:
        Formatted prompt or template
    """
    return f"""Physical Examination Findings:

Requested: {doctor_question}

Objective Findings:
{clinical_points}"""
