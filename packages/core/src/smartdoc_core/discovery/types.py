"""
Pydantic types for LLM Discovery Processing

Provides strict type validation for input/output data structures
used in the discovery processing pipeline.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class DiscoveryLLMIn(BaseModel):
    """Input data for LLM discovery processing."""
    intent_id: str
    doctor_question: str
    patient_response: str
    clinical_content: str
    agent: Optional[Literal["son", "resident", "examiner"]] = None  # for prompt selection


class DiscoveryLLMOut(BaseModel):
    """Expected output structure from LLM discovery processing."""
    label: str
    category: str
    summary: str
    confidence: float = Field(ge=0, le=1)
    reasoning: str
