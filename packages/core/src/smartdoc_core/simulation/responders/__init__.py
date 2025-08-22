"""
Simulation responders module.

Provides persona-based responders for different clinical contexts
in the SmartDoc simulation engine.
"""

from .base import Responder
from .anamnesis_son import AnamnesisSonResponder
from .labs_resident import LabsResidentResponder
from .exam_objective import ExamObjectiveResponder

__all__ = [
    "Responder",
    "AnamnesisSonResponder",
    "LabsResidentResponder",
    "ExamObjectiveResponder"
]
