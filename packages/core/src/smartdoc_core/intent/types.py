#!/usr/bin/env python3
"""
Pydantic Types for Intent Classification System

Defines structured input/output types for LLM-based intent classification
with validation and type safety.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class IntentLLMIn(BaseModel):
    """Input data for LLM intent classification."""

    doctor_input: str = Field(..., description="The doctor's question or statement to classify")
    context: Optional[Literal["anamnesis", "exam", "labs"]] = Field(
        None,
        description="Clinical context phase for context-aware classification"
    )


class IntentLLMOut(BaseModel):
    """Output from LLM intent classification with validation."""

    intent_id: str = Field(..., description="The classified intent ID")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )
    explanation: str = Field(..., description="Brief explanation of the classification")
