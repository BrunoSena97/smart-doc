"""
Simulation Engine for SmartDoc Virtual Patient System

This module orchestrates the core simulation engine that integrates AI intent classification
with progressive information disclosure, enabling natural conver                        bias_warning = {
                            "bias_type": bias_result.get("bias_type"),
                            "message": bias_result.get("message"),
                            "confidence": bias_result.get("confidence", 0.5),
                        }
                        sys_logger.log_system(
                            "warning",
                            f"Bias detected: {bias_result.get('bias_type')} - {bias_result.get('message')}",
                        )

                        # Log bias warning to session logger
                        logger = self._session_loggers.get(session_id)
                        if logger:
                            logger.log_bias_warning(bias_warning)

                except Exception as bias_error:cal interviews.
"""

import json
import uuid
from typing import Dict, List, Set, Optional, Any, Tuple, Callable
from datetime import datetime

from smartdoc_core.utils.logger import sys_logger
from smartdoc_core.config.settings import config
from smartdoc_core.simulation.disclosure_store import ProgressiveDisclosureStore
from smartdoc_core.simulation.session_logger import SessionLogger, create_session_logger
from smartdoc_core.simulation.types import DiscoveryEvent, InformationBlock
from smartdoc_core.intent.classifier import LLMIntentClassifier
from smartdoc_core.discovery.processor import DiscoveryClassifier
from smartdoc_core.llm.providers.ollama import OllamaProvider
from smartdoc_core.simulation.bias_analyzer import BiasEvaluator
from smartdoc_core.simulation.responders import (
    AnamnesisSonResponder,
    LabsResidentResponder,
    ExamObjectiveResponder
)


class IntentDrivenDisclosureManager:
    """
    Manages intent-driven progressive disclosure where natural conversation
    triggers information discovery rather than manual clicking.

    Uses dependency injection for provider, classifiers, and responders
    to support configurable LLM services and personas.
    """

    def __init__(
        self,
        case_file_path: Optional[str] = None,
        provider=None,
        intent_classifier=None,
        discovery_processor=None,
        responders: Optional[Dict[str, Any]] = None,
        bias_evaluator_cls=BiasEvaluator,
        session_logger_factory=None,
        store: Optional[ProgressiveDisclosureStore] = None,
        on_discovery: Optional[Callable] = None,
        on_message: Optional[Callable] = None
    ):
        """
        Initialize the Intent-Driven Disclosure Manager with dependency injection.

        Args:
            case_file_path: Path to case file (defaults to config)
            provider: LLM provider instance (defaults to Ollama from config)
            intent_classifier: Intent classifier instance (defaults to LLMIntentClassifier)
            discovery_processor: Discovery processor instance (defaults to LLMDiscoveryProcessor)
            responders: Dict mapping context to responder instances
            bias_evaluator_cls: Bias evaluator class (defaults to BiasEvaluator)
            session_logger_factory: Factory function for creating session loggers
            store: Progressive disclosure store instance (defaults to new ProgressiveDisclosureStore)
            on_discovery: Optional callback for discovery events (for DB persistence)
            on_message: Optional callback for message events (for DB persistence)
        """
        self.case_file_path = case_file_path or config.CASE_FILE

        # Initialize disclosure store (state management) with dependency injection
        self.store = store or ProgressiveDisclosureStore(
            case_file_path=self.case_file_path,
            on_reveal=on_discovery,
            on_interaction=on_message
        )

        # Session logger factory for creating loggers per session
        self.session_logger_factory = session_logger_factory or create_session_logger

        # Initialize providers and components with dependency injection
        self.provider = provider or OllamaProvider(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)

        self.intent_classifier = intent_classifier or LLMIntentClassifier(provider=self.provider)

        # Initialize modular discovery processor with dependency injection
        self.discovery_processor = discovery_processor or DiscoveryClassifier(
            provider=self.provider,
            mode="deterministic"  # Use deterministic mode for intent-driven cases
        )

        # Build case labels mapping for deterministic discovery classification
        self.case_labels_map = self._build_case_labels_mapping()

        # Initialize responders by context with dependency injection
        self.responders = responders or {
            "anamnesis": AnamnesisSonResponder(self.provider),
            "labs": LabsResidentResponder(self.provider),
            "exam": ExamObjectiveResponder(),  # No LLM needed for objective findings
        }

        # Enhanced intent-to-block mappings
        self.intent_block_mappings = {}
        self.load_enhanced_mappings()

        # Discovery tracking
        self.discovery_events: Dict[str, List[DiscoveryEvent]] = {}

        # Session loggers (one per session)
        self._session_loggers: Dict[str, SessionLogger] = {}

        # Initialize bias analyzer with case data
        self.bias_analyzer = None
        if self.store.case_data and bias_evaluator_cls:
            try:
                self.bias_analyzer = bias_evaluator_cls(self.store.case_data)
                sys_logger.log_system("info", "Bias analyzer initialized successfully")
            except Exception as e:
                sys_logger.log_system(
                    "warning", f"Bias analyzer initialization failed: {e}"
                )

                sys_logger.log_system("info", "Intent-Driven Disclosure Manager initialized (refactored with DI)")

    def load_enhanced_mappings(self):
        """Load intent-to-block mappings directly from JSON case file."""
        if not self.store.case_data:
            self.intent_block_mappings = {}
            sys_logger.log_system(
                "warning", "No case data available - using empty mappings"
            )
            return

        case_data = self.store.case_data

        if "intentBlockMappings" in case_data:
            self.intent_block_mappings = case_data["intentBlockMappings"]
            sys_logger.log_system(
                "info",
                f"Loaded intent mappings for {len(self.intent_block_mappings)} intents from JSON",
            )
        else:
            # Empty mappings if not specified in case file
            self.intent_block_mappings = {}
            sys_logger.log_system(
                "warning",
                "No intentBlockMappings found in case file - using empty mappings",
            )

    def _build_case_labels_mapping(self) -> Dict[str, Dict[str, str]]:
        """
        Build case labels mapping from information blocks for deterministic discovery.
        Maps blockId -> {label, category, description}
        """
        case_labels_map = {}

        if not self.store.case_data or "informationBlocks" not in self.store.case_data:
            return case_labels_map

        # Mapping from blockType and content patterns to discovery labels
        block_type_to_labels = {
            "Demographics": {
                "age": "Patient Age",
                "language": "Language Barrier",
                "records": "Medical Records",
                "social": "Social Context"
            },
            "History": {
                "chief": "Chief Complaint",
                "onset": "Onset and Duration",
                "shortness": "Shortness of Breath",
                "dyspnea": "Shortness of Breath",
                "cough": "Cough Symptoms",
                "weight": "Weight Loss",
                "appetite": "Appetite Changes",
                "eating": "Appetite Changes",
                "chest_pain": "Pertinent Negatives",
                "fever": "Pertinent Negatives",
                "chills": "Pertinent Negatives",
                "medical_care": "Recent Medical Care",
                "pmh": "Past Medical History"
            },
            "Medications": {
                "current": "Current Medications",
                "uncertainty": "Medication Uncertainty",
                "arthritis": "Arthritis Medications",
                "infliximab": "Arthritis Medications",
                "blood_pressure": "Blood Pressure Medications",
                "diabetes": "Diabetes Medications"
            },
            "PhysicalExam": {
                "vital": "Vital Signs",
                "general": "General Appearance",
                "cardiac": "Heart Examination",
                "cardiovascular": "Heart Examination",
                "respiratory": "Lung Examination",
                "pulmonary": "Lung Examination"
            },
            "Labs": {
                "bnp": "Cardiac Lab Results",
                "wbc": "Blood Results",
                "white": "Blood Results",
                "hemoglobin": "Blood Results",
                "blood": "Blood Results",
                "cbc": "Blood Results",
                "hematocrit": "Blood Results",
                "platelet": "Blood Results",
                "default": "Lab Results"
            },
            "Imaging": {
                "chest": "Chest X-ray",
                "echo": "Echocardiogram",
                "ct": "CT Scan",
                "default": "Other Imaging"
            }
        }

        for block in self.store.case_data["informationBlocks"]:
            block_id = block["blockId"]
            block_type = block["blockType"]
            content = block["content"].lower()

            # Find appropriate label based on block type and content
            label = "Clinical Concerns"  # Default

            if block_type in block_type_to_labels:
                type_labels = block_type_to_labels[block_type]

                # Look for keyword matches in content
                for keyword, candidate_label in type_labels.items():
                    if keyword == "default":
                        label = candidate_label
                    elif keyword in content or keyword in block_id.lower():
                        label = candidate_label
                        break

            # Map block type to category
            category = self._map_block_type_to_category(block_type)

            case_labels_map[block_id] = {
                "label": label,
                "category": category,
                "description": f"{label} information from {block_type.lower()}"
            }

        sys_logger.log_system("info", f"Built case labels mapping for {len(case_labels_map)} blocks")
        return case_labels_map

    def _map_block_type_to_category(self, block_type: str) -> str:
        """Map block type to discovery category."""
        return {
            "Demographics": "patient_profile",
            "History": "presenting_symptoms",
            "Medications": "current_medications",
            "PhysicalExam": "physical_examination",
            "Labs": "diagnostic_results",
            "Imaging": "imaging"
        }.get(block_type, "clinical_assessment")

    def start_intent_driven_session(self, session_id: Optional[str] = None) -> str:
        """Start a new intent-driven disclosure session."""
        if session_id is None:
            session_id = f"intent_session_{uuid.uuid4().hex[:8]}"

        # Start progressive disclosure session
        pd_session = self.store.start_new_session(session_id)

        # Initialize discovery tracking
        self.discovery_events[session_id] = []

        # Create session logger
        self._session_loggers[session_id] = self.session_logger_factory(session_id)

        sys_logger.log_system("info", f"Started intent-driven session: {session_id}")
        return session_id

    def process_doctor_query(
        self, session_id: str, user_query: str, context: str = "anamnesis"
    ) -> Dict[str, Any]:
        """
        Process a doctor's query and trigger appropriate information discovery with context filtering.

        Args:
            session_id: The session ID
            user_query: The doctor's question or statement
            context: The clinical context ('anamnesis', 'exam', 'labs')

        Returns:
            Dictionary containing response, discovered information, and discovery notifications
        """
        if session_id not in self.discovery_events:
            # Auto-start session if not exists
            self.start_intent_driven_session(session_id)

        try:
            # 1. Classify the intent with context filtering
            intent_result = self.intent_classifier.classify_intent(user_query, context)
            intent_id = intent_result["intent_id"]
            confidence = intent_result["confidence"]

            sys_logger.log_system(
                "debug",
                f"Query '{user_query}' in context '{context}' classified as '{intent_id}' (confidence: {confidence:.2f})",
            )

            # 2. Discover relevant information blocks (filtered by context)
            discovery_result = self._discover_blocks_for_intent_with_context(
                session_id, intent_id, user_query, confidence, context
            )

            # 3. Generate contextual response
            response_result = self._generate_discovery_response_with_context(
                session_id, intent_result, discovery_result, context
            )

            # 4. Real-time bias detection
            bias_warning = None
            if self.bias_analyzer:
                try:
                    # Get session interactions for bias analysis
                    session_interactions = self._get_session_interactions(session_id)

                    bias_result = self.bias_analyzer.check_real_time_bias(
                        session_interactions=session_interactions,
                        current_intent=intent_id,
                        user_input=user_query,
                        vsp_response=response_result["text"],
                    )

                    if bias_result.get("detected"):
                        bias_warning = {
                            "detected": True,
                            "bias_type": bias_result.get("bias_type"),
                            "message": bias_result.get("message"),
                            "confidence": bias_result.get("confidence", 0.5),
                        }
                        sys_logger.log_system(
                            "warning",
                            f"Bias detected: {bias_result.get('bias_type')} - {bias_result.get('message')}",
                        )

                        # Log bias warning to session logger (already handled above)

                except Exception as bias_error:
                    sys_logger.log_system(
                        "warning", f"Bias detection failed: {bias_error}"
                    )

            # 5. Log the discovery event
            if discovery_result["discovered_blocks"]:
                event = DiscoveryEvent(
                    event_id=f"discovery_{uuid.uuid4().hex[:8]}",
                    session_id=session_id,
                    intent_id=intent_id,
                    user_query=user_query,
                    discovered_blocks=discovery_result["discovered_blocks"],
                    timestamp=datetime.now(),
                    trigger_type=discovery_result["trigger_type"],
                    confidence=confidence,
                )
                self.discovery_events[session_id].append(event)

            result = {
                "success": True,
                "intent_classification": intent_result,
                "discovery_result": discovery_result,
                "response": response_result,
                "session_stats": self._get_session_discovery_stats(session_id),
            }

            # Add bias warning if detected
            if bias_warning:
                result["bias_warning"] = bias_warning

            return result

        except Exception as e:
            sys_logger.log_system(
                "error", f"Error processing query '{user_query}': {e}"
            )
            return {
                "success": False,
                "error": str(e),
                "fallback_response": "I understand you're asking about the patient. Let me think about what information I can provide...",
            }

    def _discover_blocks_for_intent(
        self, session_id: str, intent_id: str, user_query: str, confidence: float
    ) -> Dict[str, Any]:
        """Discover information blocks based on the classified intent with escalation support."""
        session = self.store.get_session(session_id)
        if not session:
            return {
                "discovered_blocks": [],
                "trigger_type": "none",
                "message": "Session not found",
            }

        discovered_blocks = []
        trigger_type = "none"

        # Enhanced intent mapping with group escalation support
        if intent_id in self.intent_block_mappings:
            mapped_targets = self.intent_block_mappings[intent_id]

            for target in mapped_targets:
                # Check if target is a groupId or blockId
                if self._is_group_id(target):
                    # Group escalation: find next eligible block in group
                    next_block = self._find_next_eligible_block_in_group(session, target)
                    if next_block:
                        reveal_result = self.store.reveal_block(
                            session_id, next_block.block_id, user_query
                        )
                        if reveal_result.get("success"):
                            discovered_blocks.append(next_block.block_id)
                            trigger_type = "escalate"
                else:
                    # Legacy block ID support
                    if (
                        target in session.blocks
                        and not session.blocks[target].is_revealed
                    ):
                        reveal_result = self.store.reveal_block(
                            session_id, target, user_query
                        )
                        if reveal_result.get("success"):
                            discovered_blocks.append(target)
                            trigger_type = "direct"

        return {
            "discovered_blocks": discovered_blocks,
            "new_discoveries": discovered_blocks,
            "trigger_type": trigger_type,
            "intent_id": intent_id,
            "confidence": confidence,
        }

    def _is_group_id(self, target: str) -> bool:
        """Check if target is a group ID (starts with 'grp_')."""
        return target.startswith("grp_")

    def _find_next_eligible_block_in_group(self, session, group_id: str):
        """Find the next unrevealed block in a group whose prerequisites are met."""
        # Get all blocks in the group
        group_blocks = []
        for block in session.blocks.values():
            block_group_id = getattr(block, 'group_id', None)
            if block_group_id == group_id:
                group_blocks.append(block)

        # Sort by level (ascending), then by block_id for deterministic ordering
        group_blocks.sort(key=lambda x: (getattr(x, 'level', 999), x.block_id))

        # Find first unrevealed block whose prerequisites are satisfied
        for block in group_blocks:
            if not block.is_revealed and self._prerequisites_satisfied(session, block):
                return block

        return None

    def _clean_response_text(self, text: str) -> str:
        """Remove quotes and clean up response text, including Unicode quotes."""
        if not text:
            return text

        text = text.strip()

        # Remove Unicode quotes (\u201c and \u201d)
        unicode_quotes = [
            ('\u201c', '\u201d'),
            ('“', '”'),
        ]
        for start, end in unicode_quotes:
            if text.startswith(start) and text.endswith(end):
                text = text[len(start):-len(end)].strip()

        # Remove ASCII quotes
        quote_pairs = [
            ('"', '"'),
            ("'", "'"),
        ]
        changed = True
        while changed:
            changed = False
            for start_quote, end_quote in quote_pairs:
                if text.startswith(start_quote) and text.endswith(end_quote):
                    text = text[len(start_quote):-len(end_quote)].strip()
                    changed = True
                    break

        return text

    def _prerequisites_satisfied(self, session, block) -> bool:
        """Check if all prerequisites for a block are satisfied."""
        prerequisites = getattr(block, 'prerequisites', []) or []
        if not prerequisites:
            return True

        # All prerequisite blocks must be revealed
        for req_block_id in prerequisites:
            if req_block_id not in session.revealed_blocks:
                return False

        return True

    def _generate_labs_fallback_response(self, intent_result: Dict, session) -> str:
        """
        Generate resident response when requested tests are not available.

        Simple, direct responses without unnecessary clarification questions.
        The resident just states that the test hasn't been performed.
        """
        intent_id = intent_result.get("intent_id", "")
        original_query = intent_result.get("original_input", "")
        confidence = intent_result.get("confidence", 0)

        # For low confidence or actual clarification intents, ask for clarification
        if intent_id == "clarification" or confidence < 0.3:
            return "I'm not sure I understand. Could you clarify what test or imaging you're asking about?"

        # For all other cases, simply state the test hasn't been performed
        # No need for LLM - just a direct, professional response
        return "That test hasn't been performed at this time."

    def _generate_patient_fallback_response(self, intent_result: Dict, session) -> str:
        """
        Generate a fallback response when no new information is discovered.

        Uses LLM to respond naturally based on the actual question, not just the classified intent.
        This prevents mismatched responses when intent classification is incorrect.

        IMPORTANT: Grounds the response in ONLY the information that has been revealed so far
        to prevent hallucination of false clinical information.
        """
        intent_id = intent_result["intent_id"]
        confidence = intent_result.get("confidence", 0)
        original_query = intent_result.get("original_input", "")

        # Handle clarification with context-aware helpful guidance
        if intent_id == "clarification" or confidence < 0.4:
            return self._generate_clarification_response(intent_result, session)

        # Collect ALL revealed information to ground the LLM response
        all_revealed_content = []
        for block_id in session.revealed_blocks:
            if block_id in session.blocks:
                block = session.blocks[block_id]
                all_revealed_content.append(f"- {block.content}")

        # Check if information was already revealed for this specific intent
        already_revealed_info = None
        if intent_id in self.intent_block_mappings:
            mapped_blocks = self.intent_block_mappings[intent_id]
            already_revealed = [
                block_id
                for block_id in mapped_blocks
                if block_id in session.blocks and session.blocks[block_id].is_revealed
            ]

            if already_revealed:
                # Collect the content that was already revealed for this intent
                revealed_content = []
                for block_id in already_revealed:
                    if block_id in session.blocks:
                        revealed_content.append(session.blocks[block_id].content)

                if revealed_content:
                    already_revealed_info = " ".join(revealed_content)

        # Use LLM to generate context-aware response based on actual question
        responder = self.responders.get("anamnesis")
        if not responder:
            return "I'm not sure I have more information about that right now."

        # Build GROUNDED prompt with all revealed information
        grounding_context = ""
        if all_revealed_content:
            grounding_context = f"""
IMPORTANT - ONLY USE THIS INFORMATION (what you've already told the doctor):
{chr(10).join(all_revealed_content)}

You MUST base your answer ONLY on the information above. Do NOT invent or add any other symptoms, complaints, or details.
"""
        else:
            grounding_context = "\nYou haven't provided any specific information yet to the doctor.\n"

        # Build context-aware prompt
        if already_revealed_info:
            # Special case: if asking about RA meds again after Level 2 revelation, hint at medical records
            if intent_id == "meds_ra_specific_initial_query" and "meds_ra_uncertainty" in session.revealed_blocks:
                specific_note = f"""

You have ALREADY told the doctor: "{already_revealed_info}"

The doctor is asking again about the same topic. Acknowledge you already mentioned this, and helpfully suggest they might want to check previous hospital records or medical records from other facilities for complete information about her medications.

Example response: "Like I mentioned, I'm not sure about her rheumatoid arthritis medications. Maybe you could check her previous hospital records? I know she's had some treatments at other facilities."
"""
            else:
                specific_note = f"\n\nYou have ALREADY told the doctor about this topic: {already_revealed_info}\n\nAcknowledge this briefly but naturally."
        else:
            specific_note = "\n\nYou don't have specific detailed information to provide about this particular question. Be honest about not having those details."

        prompt = f"""You are the English-speaking son of an elderly Spanish-speaking woman in the emergency department.
You are translating for your mother who only speaks Spanish. You are concerned but trying to be helpful.
{grounding_context}
The doctor just asked: "{original_query}"
{specific_note}

Respond naturally as the patient's son. CRITICAL RULES:
1. ONLY use information EXPLICITLY provided above - nothing else
2. Answer ONLY the specific question asked - don't mention unrelated topics
3. If you don't have information about what was asked, say "I'm not sure about that" or "I don't have information about that specifically"
4. NEVER invent details, numbers, dates, symptoms, or medical events
5. Stay focused on the doctor's actual question

Your response (brief and natural):"""

        try:
            response = self.provider.generate(prompt, temperature=0.3)
            return self._clean_response_text(response)
        except Exception as e:
            sys_logger.log_system("warning", f"LLM fallback generation failed: {e}")
            return "I'm not sure I have more specific information about that right now. Is there something else you'd like to know?"

    def _generate_fallback_response(self, intent_result: Dict, session) -> str:
        """Generate a fallback response when no new information is discovered."""
        intent_id = intent_result["intent_id"]

        # Check if information was already revealed
        if intent_id in self.intent_block_mappings:
            mapped_blocks = self.intent_block_mappings[intent_id]
            already_revealed = [
                block_id
                for block_id in mapped_blocks
                if block_id in session.blocks and session.blocks[block_id].is_revealed
            ]

            if already_revealed:
                return "I've already provided that information earlier in our conversation. Is there anything specific you'd like me to clarify or expand on?"

        # Generic contextual responses based on intent
        fallback_responses = {
            "hpi_chief_complaint": "I understand you're asking about the patient's main concern. Let me review what we know so far...",
            "exam_cardiovascular": "You'd like to examine the cardiovascular system. Let me provide the relevant findings...",
            "exam_respiratory": "For the respiratory examination, here are the findings...",
            "meds_current_known": "Regarding current medications, let me tell you what I know...",
            "clarification": "I'm not sure I understood your question completely. Could you be more specific about what you'd like to know?",
        }

        return fallback_responses.get(
            intent_id,
            "I understand your question. Let me think about what information might be most relevant...",
        )

    def _generate_clarification_response(self, intent_result: Dict, session) -> str:
        """
        Generate LLM-powered clarification response for anamnesis context.

        Uses the patient's son responder to generate natural responses that:
        - Acknowledge nonsense/unclear questions: "I'm not sure I can answer that particular question, I didn't understand."
        - Acknowledge unavailable information: "I'm not sure I have information about that specifically."
        """
        confidence = intent_result.get("confidence", 0)
        original_query = intent_result.get("original_input", "")

        # Use AnamnesisSonResponder to generate natural response
        responder = self.responders.get("anamnesis")
        if not responder:
            return "I'm not sure I can answer that particular question."

        # Build prompt for clarification with guidance
        clarification_guidance = """You need to respond to a question that you either:
1. Didn't understand (nonsense or unclear) → Say: "I'm not sure I can answer that particular question, I didn't understand."
2. Don't have information about → Say: "I'm not sure I have information about that specifically."

Be natural and stay in character as the patient's son."""

        prompt = f"""You are the English-speaking son of an elderly Spanish-speaking woman in the emergency department.
You are translating for your mother who only speaks Spanish. You are concerned but trying to be helpful.

The doctor just asked: "{original_query}"

{clarification_guidance}

Your response:"""

        try:
            response = self.provider.generate(prompt, temperature=0.3)
            return self._clean_response_text(response)
        except Exception as e:
            sys_logger.log_system("warning", f"LLM clarification generation failed: {e}")
            # Fallback based on confidence
            if confidence < 0.3:
                return "I'm not sure I can answer that particular question, I didn't understand."
            else:
                return "I'm not sure I have information about that specifically."

    def _get_session_discovery_stats(self, session_id: str) -> Dict[str, Any]:
        """Get discovery statistics for the session."""
        session = self.store.get_session(session_id)
        events = self.discovery_events.get(session_id, [])

        if not session:
            return {}

        total_blocks = len(session.blocks)
        revealed_blocks = len(session.revealed_blocks)
        total_discoveries = len(events)

        discovery_types = {}
        for event in events:
            discovery_types[event.trigger_type] = (
                discovery_types.get(event.trigger_type, 0) + 1
            )

        return {
            "total_blocks": total_blocks,
            "revealed_blocks": revealed_blocks,
            "discovery_percentage": (revealed_blocks / total_blocks * 100)
            if total_blocks > 0
            else 0,
            "total_discovery_events": total_discoveries,
            "discovery_types": discovery_types,
            "session_duration_minutes": (
                datetime.now() - session.start_time
            ).total_seconds()
            / 60,
        }

    def get_session_discoveries(self, session_id: str) -> Dict[str, Any]:
        """Get all discoveries for a session."""
        events = self.discovery_events.get(session_id, [])
        session = self.store.get_session(session_id)

        if not session:
            return {"success": False, "error": "Session not found"}

        discoveries_summary = []
        for event in events:
            discoveries_summary.append(
                {
                    "event_id": event.event_id,
                    "intent_id": event.intent_id,
                    "user_query": event.user_query,
                    "discovered_blocks": event.discovered_blocks,
                    "timestamp": event.timestamp.isoformat(),
                    "trigger_type": event.trigger_type,
                    "confidence": event.confidence,
                }
            )

        return {
            "success": True,
            "session_id": session_id,
            "discoveries": discoveries_summary,
            "stats": self._get_session_discovery_stats(session_id),
        }

    def get_available_information_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of available vs. discovered information."""
        session = self.store.get_session(session_id)
        if not session:
            return {"success": False, "error": "Session not found"}

        categories = {}
        for block_id, block in session.blocks.items():
            if block.block_type not in categories:
                categories[block.block_type] = {
                    "total": 0,
                    "revealed": 0,
                    "critical_total": 0,
                    "critical_revealed": 0,
                }

            categories[block.block_type]["total"] += 1
            if block.is_critical:
                categories[block.block_type]["critical_total"] += 1

            if block.is_revealed:
                categories[block.block_type]["revealed"] += 1
                if block.is_critical:
                    categories[block.block_type]["critical_revealed"] += 1

        return {
            "success": True,
            "categories": categories,
            "total_blocks": len(session.blocks),
            "total_revealed": len(session.revealed_blocks),
        }

    def _get_session_interactions(self, session_id: str) -> List[Dict[str, Any]]:
        """Get session interactions formatted for bias analysis."""
        logger = self._session_loggers.get(session_id)
        if logger:
            return logger.get_interactions()

        # Fallback to discovery events if no logger
        interactions = []
        events = self.discovery_events.get(session_id, [])

        for event in events:
            interaction = {
                "intent_id": event.intent_id,
                "user_query": event.user_query,
                "timestamp": event.timestamp.isoformat(),
                "discovered_blocks": event.discovered_blocks,
                "confidence": event.confidence,
                "trigger_type": event.trigger_type,
            }
            interactions.append(interaction)

        return interactions

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session summary including logs and bias analysis."""
        logger = self._session_loggers.get(session_id)
        if logger:
            return logger.get_session_summary()
        return {"error": "Session logger not found"}

    def _discover_blocks_for_intent_with_context(
        self,
        session_id: str,
        intent_id: str,
        user_query: str,
        confidence: float,
        context: str,
    ) -> Dict[str, Any]:
        """Discover blocks for intent with context filtering."""
        # Filter intents based on context
        if not self._is_intent_valid_for_context(intent_id, context):
            return {
                "discovered_blocks": [],
                "new_discoveries": [],
                "context_filtered": True,
                "original_intent": intent_id,
            }

        # Use existing discovery logic but with context awareness
        return self._discover_blocks_for_intent(
            session_id, intent_id, user_query, confidence
        )

    def _is_intent_valid_for_context(self, intent_id: str, context: str) -> bool:
        """Check if an intent is valid for the given context."""
        # Define context-specific intent mappings
        context_intents = {
            "anamnesis": [
                # History and medication related intents
                "hpi_chief_complaint",
                "hpi_shortness_of_breath",
                "hpi_cough",
                "hpi_weight_changes",
                "hpi_onset_duration_primary",
                "hpi_associated_symptoms_general",
                "hpi_pertinent_negatives",
                "hpi_chest_pain",
                "hpi_fever",
                "hpi_chills",
                "hpi_recent_medical_care",
                "pmh_general",
                "meds_current_known",
                "meds_ra_specific_initial_query",
                "meds_full_reconciliation_query",
                "profile_age",
                "profile_language",
                "profile_social_context_historian",
                "profile_medical_records",
                "clarification",  # Allow clarification in anamnesis
            ],
            "exam": [
                # Physical examination related intents
                "exam_vital",
                "exam_general_appearance",
                "exam_respiratory",
                "exam_cardiovascular",
                "clarification",  # Allow clarification in exam
            ],
            "labs": [
                # Laboratory and imaging related intents
                "labs_general",
                "labs_bnp",
                "labs_wbc",
                "labs_hemoglobin",
                "imaging_chest_xray",
                "imaging_echo",
                "imaging_ct_chest",
                "imaging_general",
                "clarification",  # Allow clarification in labs
            ],
        }

        return intent_id in context_intents.get(context, [])

    def _generate_discovery_response_with_context(
        self,
        session_id: str,
        intent_result: Dict[str, Any],
        discovery_result: Dict[str, Any],
        context: str,
    ) -> Dict[str, Any]:
        """Generate response with context-appropriate responder using dependency injection."""
        # Check if intent was filtered due to context
        if discovery_result.get("context_filtered"):
            return self._generate_context_filtered_response(
                intent_result["intent_id"], context
            )

        # Collect clinical_data consistently
        session = self.store.get_session(session_id)
        if not session:
            return {
                "text": "Session not found",
                "discoveries": [],
                "discovery_count": 0,
                "has_discoveries": False
            }

        clinical_data = []
        discoveries = []

        for block_id in discovery_result.get("new_discoveries", []):
            if block_id in session.blocks:
                block = session.blocks[block_id]

                # Use Discovery Processor to categorize and label the discovery
                discovery_info = self.discovery_processor.process_discovery(
                    block_id=block_id,
                    block_type=block.block_type,
                    clinical_content=block.content,
                    intent_id=intent_result["intent_id"],
                    doctor_question=intent_result.get("original_input", ""),
                    patient_response="",
                    case_labels_map=self.case_labels_map,
                )

                discoveries.append({
                    "block_id": block_id,
                    "block_type": block.block_type,
                    "content": block.content,
                    "is_critical": block.is_critical,
                    "discovery_notification": f"📋 **{context.title()} Information**: {discovery_info['label']}",
                    "label": discovery_info["label"],
                    "category": discovery_info["category"],
                    "summary": block.content if context in ("exam", "labs") else discovery_info["summary"],
                    "confidence": discovery_info["confidence"],
                })

                clinical_data.append({
                    "type": block.block_type,
                    "content": block.content,
                    "label": discovery_info["label"],
                    "summary": discovery_info["summary"],
                })

        # Check if this is a pertinent negatives query and accumulate with previous ones
        if intent_result["intent_id"] in ["hpi_pertinent_negatives", "hpi_chest_pain", "hpi_fever", "hpi_chills"] and context == "anamnesis":
            # Get all previously revealed pertinent negative blocks for this session
            accumulated_pertinent_negatives = []

            for block_id, block in session.blocks.items():
                if block_id in ["hpi_chest_pain", "hpi_fever", "hpi_chills"] and hasattr(block, 'is_revealed') and block.is_revealed:
                    # Add previously revealed pertinent negatives to clinical data
                    discovery_info = self.discovery_processor.process_discovery(
                        block_id=block_id,
                        block_type=block.block_type,
                        clinical_content=block.content,
                        intent_id=intent_result["intent_id"],
                        doctor_question=intent_result.get("original_input", ""),
                        patient_response="",
                        case_labels_map=self.case_labels_map,
                    )

                    if not any(cd["content"] == block.content for cd in clinical_data):
                        clinical_data.append({
                            "type": block.block_type,
                            "content": block.content,
                            "label": discovery_info["label"],
                            "summary": discovery_info["summary"],
                        })

                    accumulated_pertinent_negatives.append(block.content)

            # If we have accumulated pertinent negatives, create a combined discovery entry for the UI
            if accumulated_pertinent_negatives:
                combined_content = " ".join(accumulated_pertinent_negatives)

                # Replace or update the pertinent negatives discovery with accumulated content
                pertinent_discovery = None
                for i, discovery in enumerate(discoveries):
                    if discovery["block_id"] in ["hpi_chest_pain", "hpi_fever", "hpi_chills"]:
                        pertinent_discovery = discovery
                        break

                if pertinent_discovery:
                    # Update the existing discovery with accumulated content
                    pertinent_discovery["content"] = combined_content
                    pertinent_discovery["summary"] = combined_content
                    pertinent_discovery["label"] = "Pertinent Negatives (All)"
                elif discoveries:  # If we have new discoveries but no pertinent negative in them
                    # Add a combined pertinent negatives discovery
                    discoveries.append({
                        "block_id": "hpi_pertinent_negatives_combined",
                        "block_type": "History",
                        "content": combined_content,
                        "is_critical": False,
                        "discovery_notification": f"📋 **{context.title()} Information**: Pertinent Negatives (All)",
                        "label": "Pertinent Negatives (All)",
                        "category": "presenting_symptoms",
                        "summary": combined_content,
                        "confidence": 0.95,
                    })        # Choose responder based on context
        responder = self.responders.get(context) or self.responders["anamnesis"]

        # Generate response text
        if discoveries or clinical_data:  # Also generate response if we have accumulated clinical data
            text = responder.respond(
                intent_id=intent_result["intent_id"],
                doctor_question=intent_result.get("original_input", ""),
                clinical_data=clinical_data,
                context=context,
            )

            # Note: Discovery events are now automatically persisted via store hooks
        else:
            # No new discoveries → use context-appropriate fallback
            if context == "exam":
                text = self._generate_exam_fallback_response(intent_result, session)
            elif context == "labs":
                text = self._generate_labs_fallback_response(intent_result, session)
            else:
                text = self._generate_patient_fallback_response(intent_result, session)

        response = {
            "text": self._clean_response_text(text),
            "discoveries": discoveries,
            "discovery_count": len(discoveries),
            "has_discoveries": bool(discoveries)
        }

        # Log interaction with session logger
        logger = self._session_loggers.get(session_id)
        if logger:
            logger.log_interaction(
                intent_id=intent_result["intent_id"],
                user_query=intent_result.get("original_input", ""),
                vsp_response=response["text"],
                nlu_output=intent_result,
                dialogue_state=context.upper()
            )

        return response

    def _generate_exam_fallback_response(self, intent_result: Dict, session) -> str:
        """
        Generate simple response when requested examination findings are not available.

        No LLM generation needed - just return a clear message that the information
        is not available in the case.
        """
        return "That examination finding is not available in this case."

    def _generate_context_filtered_response(
        self, intent_id: str, context: str
    ) -> Dict[str, Any]:
        """Generate response when intent is filtered due to context mismatch."""
        responses = {
            "anamnesis": {
                "exam": "I'm here to provide history about my mother. For physical examination findings, you'll need to examine her directly.",
                "labs": "I don't have access to laboratory results. You might want to speak with the resident about ordering tests.",
                "default": "I can help you with information about my mother's history and symptoms. What would you like to know?",
            },
            "exam": {
                "anamnesis": "This is the physical examination. For history questions, please speak with the patient's son.",
                "labs": "For laboratory or imaging results, please consult with the resident.",
                "default": "What aspect of the physical examination would you like me to perform?",
            },
            "labs": {
                "anamnesis": "For patient history, please speak with the patient's son.",
                "exam": "For physical examination, you'll need to examine the patient directly.",
                "default": "What laboratory tests or imaging studies would you like me to order or review?",
            },
        }

        # Determine the response based on current context and appropriate persona
        if context == "labs":
            response_text = "What laboratory tests or imaging studies would you like me to order or review for this patient?"
        elif context == "exam":
            response_text = "What aspect of the physical examination would you like me to perform?"
        else:
            response_text = "I can help you with information about my mother's history and symptoms. What would you like to know?"

        return {"text": response_text, "discoveries": [], "context_filtered": True}
