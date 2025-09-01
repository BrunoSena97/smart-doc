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
            "exam": ExamObjectiveResponder(),  # No provider needed for objective findings
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
            "Imaging": "diagnostic_results"
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
        """Discover information blocks based on the classified intent."""
        session = self.store.get_session(session_id)
        if not session:
            return {
                "discovered_blocks": [],
                "trigger_type": "none",
                "message": "Session not found",
            }

        discovered_blocks = []
        trigger_type = "none"

        # Direct intent mapping - rely on LLM classification
        if intent_id in self.intent_block_mappings:
            mapped_blocks = self.intent_block_mappings[intent_id]
            for block_id in mapped_blocks:
                if (
                    block_id in session.blocks
                    and not session.blocks[block_id].is_revealed
                ):
                    # Reveal the block
                    reveal_result = self.store.reveal_block(
                        session_id, block_id, user_query
                    )
                    if reveal_result.get("success"):
                        discovered_blocks.append(block_id)
                        trigger_type = "direct"

        return {
            "discovered_blocks": discovered_blocks,
            "new_discoveries": discovered_blocks,  # Add this key for consistency
            "trigger_type": trigger_type,
            "intent_id": intent_id,
            "confidence": confidence,
        }

    def _generate_labs_fallback_response(self, intent_id: str) -> str:
        """Generate appropriate resident response when requested tests are not available."""
        labs_fallbacks = {
            "labs_general": "I can order comprehensive laboratory studies for you. What specific tests would you like me to prioritize?",
            "imaging_chest": "I can order a chest X-ray and have the results available shortly. Would you like me to proceed?",
            "imaging_general": "What imaging studies would you like me to order? I can arrange CT, MRI, or other modalities as needed.",
            "labs_cbc": "I can order a complete blood count with differential. The results should be available within the hour.",
            "labs_bmp": "I'll order a basic metabolic panel for you. Any other chemistry studies you'd like to add?",
            "labs_cardiac": "I can order cardiac enzymes and BNP. Given the presentation, would you like me to add troponins?",
        }

        return labs_fallbacks.get(
            intent_id,
            "I can order that test for you. What specific information are you looking for?",
        )

    def _generate_patient_fallback_response(self, intent_result: Dict, session) -> str:
        """Generate a fallback response when no new information is discovered."""
        intent_id = intent_result["intent_id"]
        confidence = intent_result.get("confidence", 0)

        # Always provide contextually appropriate responses based on the specific question type
        # Even if we don't have new information blocks to reveal
        intent_specific_responses = {
            # Chief complaint and history
            "hpi_chief_complaint": "The main reason we're here is her breathing problems and how she's been feeling weak lately.",
            "hpi_onset_duration_primary": "It all started about two months ago and has been getting slowly worse since then.",
            "hpi_shortness_of_breath": "Her breathing has been getting worse over the past couple of months. It's especially bad when she tries to walk around.",
            "hpi_appetite": "She hasn't been eating as well lately. I've noticed she doesn't finish her meals like she used to.",
            "hpi_eating": "Her appetite has definitely decreased. She's been eating smaller portions and doesn't seem interested in food.",
            "hpi_weight_loss": "I've noticed her clothes are getting loose on her. She's definitely lost some weight recently.",
            "hpi_cough": "She has this dry cough that won't go away. It's worse at night and keeps her up.",
            "hpi_fever": "No, she hasn't had any fever. Her temperature has been normal.",
            "hpi_chest_pain": "No, she says she doesn't have any chest pain.",
            # Physical exam
            "exam_cardiovascular": "Would you like to examine her heart? She's sitting here if you need to listen.",
            "exam_respiratory": "You can examine her lungs if you need to. Her breathing has been the main problem.",
            "exam_vital_signs": "The nurses already took her vital signs when we arrived.",
            "exam_general_appearance": "As you can see, she looks tired and is breathing a bit fast.",
            # Medications
            "meds_current_known": "I think I told you all the medications I know about. There might be others her regular doctor prescribed.",
            "meds_ra_specific_initial_query": "I'm sorry, I don't know much about her arthritis treatments. Her rheumatologist handles that.",
            "meds_full_reconciliation_query": "Let me check if they found her records from the other hospital... Yes! They found her previous records with her complete medication list.",
            "meds_other_meds_initial_query": "I'm not sure about other medications. She sees different doctors for her various conditions.",
            # Imaging and tests
            "imaging_chest": "I think they did a chest X-ray when we got here. Did you see the results?",
            "imaging_general": "They've done some imaging tests. I think there was a chest X-ray, and maybe they mentioned other scans?",
            "labs_general": "They drew some blood when we arrived. I don't know the results yet.",
            # Profile and background
            "profile_age": "She's elderly, in her 70s. I help her because she only speaks Spanish.",
            "profile_language": "My mother only speaks Spanish, so I'm translating for her.",
            "pmh_general": "She has diabetes, high blood pressure, and arthritis. She's also quite overweight.",
            # General responses
            "clarification": "I'm not sure I understand what you're asking. Could you ask it differently?",
        }

        # First check if we have a specific contextual response for this intent
        if intent_id in intent_specific_responses:
            return intent_specific_responses[intent_id]

        # Check if information was already revealed for this intent and give acknowledging responses
        if intent_id in self.intent_block_mappings:
            mapped_blocks = self.intent_block_mappings[intent_id]
            already_revealed = [
                block_id
                for block_id in mapped_blocks
                if block_id in session.blocks and session.blocks[block_id].is_revealed
            ]

            if already_revealed:
                # Provide brief acknowledgment but still try to be helpful
                if intent_id == "hpi_weight_loss":
                    return "I already mentioned her weight loss, but yes, she's definitely been losing weight over the past few weeks."
                elif intent_id == "hpi_shortness_of_breath":
                    return "I talked about her breathing before - it's been getting worse over the past couple of months, especially with walking."
                elif intent_id.startswith("imaging_"):
                    return "I believe they've done some imaging studies. Have you had a chance to review the results?"
                elif intent_id.startswith("meds_"):
                    return "I mentioned her medications earlier. Is there something specific about her medications you'd like to know?"
                else:
                    return "I think we discussed that already, but let me know if you need me to clarify anything specific."

        # If confidence is low, acknowledge uncertainty
        if confidence < 0.5:
            return "I'm not sure I understood your question completely. Could you be more specific about what you'd like to know?"

        # Default response
        return "I'm not sure I have more information about that right now. Is there something else you'd like to know?"

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
                "meds_uncertainty",
                "meds_ra_specific_initial_query",
                "meds_full_reconciliation_query",
                "meds_other_meds_initial_query",
                "profile_age",
                "profile_language",
                "profile_social_context_historian",
                "profile_medical_records",
            ],
            "exam": [
                # Physical examination related intents
                "exam_vital",
                "exam_general_appearance",
                "exam_respiratory",
                "exam_cardiovascular",
            ],
            "labs": [
                # Laboratory and imaging related intents
                "labs_general",
                "imaging_chest",
                "imaging_general",
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

        # Choose responder based on context
        responder = self.responders.get(context) or self.responders["anamnesis"]

        # Generate response text
        if discoveries:
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
                text = self._generate_exam_fallback_response(intent_result["intent_id"])
            elif context == "labs":
                text = self._generate_labs_fallback_response(intent_result["intent_id"])
            else:
                text = self._generate_patient_fallback_response(intent_result, session)

        response = {
            "text": text,
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

    def _generate_exam_fallback_response(self, intent_id: str) -> str:
        """Generate appropriate response when requested examination findings are not available."""
        exam_fallbacks = {
            "exam_vital": "The vital signs have not been obtained yet. Would you like me to measure them?",
            "exam_cardiovascular": "The cardiovascular examination reveals no abnormalities of clinical significance at this time.",
            "exam_respiratory": "The respiratory examination does not reveal any significant findings of note.",
            "exam_neurological": "The neurological examination appears unremarkable at this time.",
            "exam_abdominal": "The abdominal examination does not reveal any significant abnormalities.",
            "exam_musculoskeletal": "The musculoskeletal examination shows no obvious deformities or limitations.",
            "exam_skin": "The skin examination reveals no notable lesions or changes.",
            "exam_general_appearance": "The patient appears comfortable and in no acute distress.",
        }

        return exam_fallbacks.get(
            intent_id,
            "This aspect of the physical examination does not reveal anything of particular clinical significance.",
        )

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
