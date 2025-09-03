"""
Types for SmartDoc Virtual Patient Simulation

Provides structured data types for simulation events, responses,
configuration, and state management in the SmartDoc simulation engine.
"""

from pydantic import BaseModel, Field
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from datetime import datetime


class SimulationDiscovery(BaseModel):
    """Represents a discovery within a simulation response."""
    block_id: str
    block_type: str
    content: str
    is_critical: bool
    discovery_notification: str
    label: str
    category: str
    summary: str
    confidence: float = Field(ge=0, le=1)


class SimulationResponse(BaseModel):
    """Structured response from simulation engine."""
    text: str
    discoveries: List[SimulationDiscovery]
    discovery_count: int
    has_discoveries: bool
    context_filtered: Optional[bool] = None


class BiasWarning(BaseModel):
    """Bias detection warning."""
    detected: bool
    bias_type: Optional[str] = None
    message: Optional[str] = None
    confidence: float = Field(ge=0, le=1, default=0.5)


class SimulationResult(BaseModel):
    """Complete result from processing a doctor query."""
    success: bool
    intent_classification: Dict[str, Any]
    discovery_result: Dict[str, Any]
    response: SimulationResponse
    session_stats: Dict[str, Any]
    bias_warning: Optional[BiasWarning] = None
    error: Optional[str] = None
    fallback_response: Optional[str] = None


# === State Management Types ===

@dataclass
class InformationBlock:
    """Represents a single discoverable information block."""

    block_id: str
    block_type: str  # History, PhysicalExam, Labs, Imaging
    content: str
    is_critical: bool
    is_revealed: bool = False
    revealed_at: Optional[datetime] = None
    revealed_by_query: Optional[str] = None

    # Escalation system fields
    group_id: Optional[str] = None
    level: Optional[int] = None
    prerequisites: Optional[List[str]] = None
    reveal_policy: str = "escalate"  # "escalate" or "all"


@dataclass
class StudentInteraction:
    """Tracks a student's interaction with the progressive disclosure system."""

    timestamp: datetime
    action: str  # 'reveal_block', 'submit_hypothesis', 'request_category'
    block_id: Optional[str] = None
    category: Optional[str] = None
    hypothesis: Optional[str] = None
    reasoning: Optional[str] = None


@dataclass
class ProgressiveDisclosureSession:
    """Manages a single progressive disclosure session."""

    session_id: str
    case_id: str
    start_time: datetime
    blocks: Dict[str, InformationBlock] = field(default_factory=dict)
    revealed_blocks: Set[str] = field(default_factory=set)
    interactions: List[StudentInteraction] = field(default_factory=list)
    working_hypotheses: List[Dict[str, str]] = field(default_factory=list)
    final_diagnosis: Optional[str] = None
    session_complete: bool = False


@dataclass
class DiscoveryEvent:
    """Represents a discovery event triggered by an intent."""

    event_id: str
    session_id: str
    intent_id: str
    user_query: str
    discovered_blocks: List[str]
    timestamp: datetime
    trigger_type: str  # 'direct', 'indirect', 'follow_up'
    confidence: float


@dataclass
class SessionInteraction:
    """Represents a logged interaction between user and VSP."""

    intent_id: str
    user_query: str
    vsp_response: str
    timestamp: datetime
    nlu_output: Dict[str, Any] = field(default_factory=dict)
    dialogue_state: str = "UNKNOWN"
