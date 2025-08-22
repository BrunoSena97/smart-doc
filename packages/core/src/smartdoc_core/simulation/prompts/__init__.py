"""
Simulation prompts module.

Provides prompt builders for different personas and contexts
in the SmartDoc simulation engine.
"""

from .patient_default import build_patient_prompt
from .resident_default import build_resident_prompt
from .exam_default import build_exam_prompt

__all__ = [
    "build_patient_prompt",
    "build_resident_prompt",
    "build_exam_prompt"
]
